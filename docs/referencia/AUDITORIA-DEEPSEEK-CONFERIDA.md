# A auditoria do DeepSeek, conferida contra o código — 10/09/2026

**Regra que vale aqui, e ela não é formalidade:** auditoria de terceiro é **hipótese**, não
achado. O projeto inteiro existe porque um arquivo pode declarar um comportamento que o
código não tem. Um documento que *descreve* defeitos está sujeito exatamente ao mesmo
risco. Então cada item foi rodado contra o código real antes de virar pendência.

**Resultado:** os quatro críticos são **verdadeiros**. Um deles é pior do que a auditoria
diz, e um dos "altos" a auditoria descreveu pela metade.

---

## C4 — duplicata `etf.IMAB11` · **CONFIRMADO, e o diagnóstico está errado**

A auditoria manda rodar `yaml.safe_load` e diz: *"se falhar com ConstructorError, o
arquivo tem chave duplicada e não carrega."*

**Ele não falha. Carrega perfeitamente.** PyYAML não reclama de chave duplicada — ele fica
**silenciosamente com a última**. Conferido:

```
custos.yaml linha 171:  IMAB11: valor 0.0025, status PARCIAL     <- fonte de 05/09
custos.yaml linha 253:  IMAB11: valor null,   status NAO_CONFIRMADO
```

E o que o motor lê hoje:

```python
C['etf']['IMAB11']
-> {'valor': None, 'status': 'NAO_CONFIRMADO',
    'motivo': 'taxa de administracao nao obtida; regulamento nao baixado',
    'bloqueia': ['rota_etf_renda_fixa_protecao_real']}
```

**A entrada de 05/09 — a que tem valor, fonte e data de acesso — está morta.** Foi
escrita, versionada, e nunca é lida.

Isto é a família do **F-02** numa camada nova. Lá, insumo ausente virava zero e zero
ganhava de todos. Aqui, **um insumo presente é sobrescrito por um ausente** — e a
`bloqueia` do segundo é que está em vigor. O sistema está mais conservador do que deveria,
não menos, o que é a direção menos perigosa do erro. Mas está errado do mesmo jeito, e por
um motivo que nenhum teste pega.

**Pergunta que isto abre e que não tem resposta ainda:** o `PENDENCIAS.md` registra
*"F-03 medida e refutada (IMAB11 perde do Tesouro)"*. Se o motor lê `None` e a rota está
bloqueada, **com que número essa medição foi feita?** Ou ela usou 0,25% por fora, e o
motor não consegue reproduzi-la, ou ela usou o bloqueio. Precisa ser respondido antes de
apagar qualquer uma das duas entradas.

**Correção:** apagar a entrada de baixo (a `NAO_CONFIRMADO`), manter a de 05/09.
**Teste que faltava, e ele vale para o arquivo inteiro, não para o IMAB11:**

```python
def test_nenhuma_chave_duplicada_em_custos_yaml():
    """PyYAML nao reclama de chave duplicada -- fica com a ultima, em silencio.
    Este teste le o texto bruto e acusa. Ele falha contra a versao de 10/09/2026."""
```

Um teste que checasse só o IMAB11 seria um patch. O que pega a classe inteira é varrer o
YAML cru procurando chaves repetidas em qualquer mapping.

---

## C3 — `HOJE = dt.date(2026, 9, 1)` fixo · **CONFIRMADO**

`motor.py:20`. **Hoje é 10/09.** O mecanismo de expiração está mudo há nove dias.

E isto tem consequência datada: `macro.poupanca_am` **expira em 28/09/2026**, e o
`CLAUDE.md` diz, na seção "Números que envelhecem", que `val()` avisa em stderr quando
passa da data. **Não vai avisar.**

O agravante é o achado que o próprio projeto registrou em 05/09: quando `cdi_aa` e
`selic_aa` venceram, o aviso disparou, os dois foram reconferidos, e **os dois estavam
certos** — era prazo vencido, não número errado. O mecanismo funcionou exatamente como
devia. Congelar a data desliga isso.

**Correção:** `HOJE = dt.date.today()`, e — melhor — permitir `val(..., hoje=None)` para o
teste poder fixar a data sem congelar a produção. Um teste com `dt.date.today()` embutido
é um teste que muda de resultado sozinho.

---

## C1 — `dividas` e `objetivos` voltam como `dict` · **CONFIRMADO**

```
estado_io.py:75   d["dividas"]   = doc.get("dividas") or []
alocacao.py:739   pior = max(estado.dividas, key=lambda d: d.taxa_am)
alocacao.py:1059  prazo_max = max(o.prazo_anos for o in estado.objetivos)
```

`AttributeError` na primeira carteira com dívida ou objetivo. **Ainda não estourou porque
as duas listas estão vazias** — não porque o código esteja certo.

Vale notar o que isso diz sobre a suíte: 269 testes, e nenhum carrega um `estado.yaml` com
dívida **pelo caminho real** (`estado_io.carregar`). Os testes do G1 montam `Divida(...)`
direto, então testam o portão e nunca a porta de entrada. **O defeito mora exatamente na
costura entre dois módulos que cada um testa sozinho.**

---

## C2 — `aporte_mensal <= 0` bloqueia o carregamento · **CONFIRMADO**

`estado_io.py:119`. E a auditoria está certa sobre o motivo: contradiz a **U-01** — o
sistema tem de funcionar para um cliente novo, e cliente novo tem aporte zero.

`test_usuario_novo.py` passa porque monta o cadastro em memória; o caminho `carregar()`
nunca vê o zero. É a mesma costura da C1, no outro sentido.

> **Nota de 10/09:** isto acabou de deixar de ser o caso do Osvaldo — ele fez o primeiro
> aporte de R$500. Mas continua sendo defeito, e agora é *só* do sistema. É a U-01
> inteira: o problema não era a carteira dele, era o motor tratar um estado legítimo como
> erro.

---

## A1 — o bônus arredondado · **CONFIRMADO, e a auditoria descreveu pela metade**

`aporte.py:69` — `m % max(1, round(intervalo)) == 0`. Medido:

| extraordinários/ano declarados | disparos reais/ano | erro |
|---|---|---|
| 1, 2, 3, 4, 6, 12 | igual | nenhum |
| **5** | **6** | **+20%** |
| **7** | **6** | **−14%** |
| **11** | **12** | **+9%** |

A auditoria diz *"projeção otimista"*. **Erra nos dois sentidos.** Com 7 por ano o sistema
é *pessimista* — projeta menos dinheiro do que entra, e a Fase A parece mais longa do que
é. Um viés que troca de sinal conforme o input é pior que um viés constante: não dá para
corrigir de cabeça.

A correção proposta (distribuir por `int(m*12/n)`) está certa.

---

## O que a auditoria acertou como classe, e vale mais que os itens

**Campos mortos, 4ª ocorrência:** `reserva_empenhada`, `DIFERIDOS_K`,
`status_do_variavel`, `corretora.promocional`. O projeto tem
`test_P28_secao_operacional_nao_tem_chave_morta` protegendo o **YAML** e **nada
equivalente para o Python**. Isso é uma assimetria real, e é a N-01 esperando acontecer do
lado do código.

**Duplicação de fórmula:** `simular` × `simular_custo`, `taxa_liquida_reserva` ×
`retorno_liquido_aa`, `meses_cobertos` × `res/despesa`. Duas implementações da mesma conta
é a N-01 na sua forma canônica: elas concordam por acidente até o dia em que não
concordam.

**Referência cruzada quebrada:** `estado.exemplo.yaml` cita "P-48" onde deveria citar
"U-01" — e isso é meu, escrito na sessão de 06/09.

---

## Onde eu discordo da auditoria, e não é detalhe

O documento fecha com quatro semanas de trabalho no motor e a Fase 0 **depois**.

**Isso é exatamente o erro que este projeto já mediu e nomeou.** O `CLAUDE.md` §11.1
registra: sete rodadas seguidas de qualidade de engenharia, zero de propósito, todas
propostas por mim. E a P-44 virou regra por causa disso: *o próximo passo não pode ser de
engenharia duas vezes seguidas.*

E o **X-01**, de 06/09, torna o argumento mais forte: descobrimos que o dado estruturado
da CVM responde **3 dos 10 passos** que uma leitura de incorporadora exige. Se isso vale
para outros setores — e não há razão para supor que não —, **o desenho do pipeline muda**,
e nenhuma refatoração do motor antecipa essa descoberta.

Some-se o prazo que a própria CVM declarou por escrito: os arquivos dos **últimos cinco
anos** são reescritos **semanalmente** com reapresentações. Cada semana sem captura é uma
rodada de reapresentações que deixou de ser observável — e isso não se compra depois.

**A ordem que eu defendo:**

1. **C4, C3, C1, C2** — as quatro críticas. São horas, não semanas, e duas delas
   (C1 e C2) estão na costura entre módulos, que é onde o próximo bug real vai morar.
2. **Fase 0** — `coletar_b3.py`, depois `cvm_catalogo.py`. É o único item da fila que
   pode **deixar de existir**.
3. A1 e o resto, **em paralelo com a Fase 0**, não antes dela.

A auditoria é boa e vale executar. **A ordem dela é que repete o erro que custou sete
rodadas.**

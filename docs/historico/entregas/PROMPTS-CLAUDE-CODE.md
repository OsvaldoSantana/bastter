> VENCIDO — executado em 11/09/2026 (9e1aa8a a 6378b0c). Não é instrução vigente.

# Hora de começar o Claude Code — 11/09/2026

**É agora, e eu devo o aviso que você pediu.**

O motivo é específico, não é "chegou a hora". A fila do projeto acabou de mudar de forma:
o dado perecível foi capturado, e o que sobrou são **quatro correções dentro de arquivos
do repositório, cada uma com teste e commit**. Isso é exatamente o trabalho que o Claude
Code faz melhor e que o Cowork faz com ritual de zip.

| | Claude Code (terminal) | aqui (Cowork) |
|---|---|---|
| editar `alocacao/*.py`, rodar `pytest`, `ruff`, `mypy` | **sim, sem ritual** | precisa empacotar e gravar |
| `git add / commit / push` | **sim, direto** | não alcança |
| pesquisa com fonte primária, subagentes | não | **sim** |
| processar o acervo depois que ele existir | não | **sim** |

**A cota é a mesma.** Plano Pro divide o limite entre os dois — não é orçamento novo, é o
mesmo gasto de outro jeito. Por isso o primeiro princípio abaixo importa tanto.

---

## Como escrever prompt NESTE repositório — e por que o bom prompt aqui é curto

A regra geral de engenharia de prompt é "dê contexto". **Aqui ela se inverte em parte**,
e o motivo é mecânico: ao abrir o Claude Code na pasta, ele **já carrega o `CLAUDE.md`
inteiro** — as sete doutrinas, o protocolo de mudança, as regras de sessão — e as três
skills de `.claude/skills/`.

Consequências práticas:

1. **Não repita a doutrina no prompt.** Escrever "lembre-se de que toda constante precisa
   de procedência" gasta cota para dizer o que ele acabou de ler. Pior: se a sua frase
   divergir do arquivo, você criou **duas fontes de verdade** — que é o achado N-01, e
   ele já custou caro aqui.
2. **Cite o achado pela letra.** "Corrija o Y-01" carrega mais informação que um parágrafo
   de explicação, porque a letra puxa o registro inteiro do `ACHADOS.md`.
3. **O que o prompt precisa trazer é só o que NÃO está nos arquivos:** o que você quer
   agora, o critério de pronto, e o que está fora de escopo.

### A anatomia que funciona aqui

```
[ALVO]      qual achado ou pendência, pela letra/número
[FATO]      o que foi medido, com arquivo e linha — não a sua interpretação
[PRONTO]    como se sabe que acabou, em critério verificável
[LIMITE]    o que NÃO fazer nesta sessão
```

O `[LIMITE]` é o que mais economiza cota, e é contra-intuitivo. Sem ele, a resposta certa
para "corrija o IMAB11" pode virar uma refatoração do `custos.yaml` inteiro — defensável,
não pedida, e cara.

---

## Os cinco prompts, em ordem

Copie e cole um por vez. **Não junte dois** — cada um termina em commit, e commit
pequeno é o que permite desfazer um sem perder o outro.

### 0. Abrir (uma vez)

```powershell
cd C:\Users\osvaldo.junior\Desktop\Bastter
claude
```

Se ele entrar com a conta errada: `/logout`, depois `/login`.

---

### 1. Y-01 — a chave YAML duplicada

```
[ALVO] Y-01 e a pendencia P-69.

[FATO] custos.yaml tem duas entradas etf.IMAB11, nas linhas 171 e 253. PyYAML nao
reclama de chave duplicada: fica com a ultima, em silencio. Confirmei que
yaml.safe_load(custos.yaml)['etf']['IMAB11'] devolve hoje {'valor': None,
'status': 'NAO_CONFIRMADO'}. A entrada de 05/09, com valor 0.0025 e fonte, esta
morta desde que foi escrita.

[PRONTO]
1. Um teste novo que varre o TEXTO BRUTO de custos.yaml, catalogo.yaml,
   politica.yaml, perfil.yaml, teses.yaml e instituicoes.yaml procurando chave
   repetida em qualquer mapping, e que FALHA contra o custos.yaml de hoje.
   Um teste que cheque so o IMAB11 nao serve: o defeito e da classe, nao do ativo.
2. So depois disso, a duplicata removida.
3. pytest, ruff e mypy em zero.
4. Um commit.

[LIMITE] Nao decida ainda QUAL das duas entradas fica. Antes disso ha uma pergunta
sem resposta, e ela e mais importante que a limpeza: PENDENCIAS.md registra
"F-03 medida e refutada (IMAB11 perde do Tesouro)". Se o motor le None e a rota
esta bloqueada, com que numero essa medicao foi feita? Procure no git log, nos
REGISTRO-v*.md e no politica.yaml, e ME DIGA o que achou antes de apagar qualquer
linha. Se nao achar, diga que nao achou.
```

---

### 2. P-70 — a data congelada

```
[ALVO] P-70.

[FATO] motor.py linha 20: HOJE = dt.date(2026, 9, 1). Hoje e 11/09. O aviso de
expiracao do val() esta mudo ha 10 dias, e custos.yaml -> macro.poupanca_am vence
em 28/09/2026.

[PRONTO]
1. val() passa a aceitar `hoje` como parametro opcional, com default None que
   resolve para dt.date.today() NO MOMENTO DA CHAMADA — nao no import do modulo.
2. Um teste que injeta uma data futura e exige o aviso em stderr, e outro que
   injeta uma data anterior a expira e exige silencio. Teste que dependa do
   relogio real e teste que muda de resultado sozinho: nao serve.
3. pytest, ruff, mypy em zero. Um commit.

[LIMITE] Nao renove nenhuma constante vencida nesta sessao. Renovar exige ir a
fonte primaria e registrar acesso — e outro trabalho, e ele e meu, nao seu.
```

---

### 3. P-71 e P-72 — a costura entre `estado_io` e o motor

```
[ALVO] P-71 e P-72, juntas, porque sao o mesmo defeito em dois sentidos.

[FATO] estado_io.py linhas 75-76 devolvem dividas e objetivos como lista de dict.
alocacao.py linha 739 faz `d.taxa_am` e a linha 1059 faz `o.prazo_anos`. E
AttributeError na primeira carteira com divida — nao estourou ainda so porque as
duas listas estao vazias. E estado_io.py linha 119 bloqueia o carregamento com
aporte_mensal <= 0, o que contradiz o achado U-01.

O que os dois tem em comum importa mais que os dois: sao 269 testes, e NENHUM
carrega um estado pelo caminho real, via estado_io.carregar(). Os testes do G1
montam Divida(...) na mao; test_usuario_novo.py monta o cadastro em memoria.
A porta de entrada do sistema nao e exercitada por teste nenhum.

[PRONTO]
1. Um teste que escreve um estado.yaml TEMPORARIO com divida, objetivo e
   aporte_mensal 0, carrega por estado_io.carregar(), e roda alocar() ate o fim.
   Ele falha hoje, com AttributeError. E o teste que faltava.
2. A conversao para dataclass, no lugar certo — se houver import circular entre
   estado_io e alocacao, resolva e explique a escolha em comentario.
3. aporte_mensal == 0 vira AVISO; negativo continua problema.
4. pytest, ruff, mypy em zero. Um commit.

[LIMITE] Nao mexa no estado.yaml real. O teste usa tmp_path do pytest. E nao
"conserte" test_usuario_novo.py para passar pelo caminho novo: ele mede outra
coisa, de proposito.
```

---

### 4. Campos mortos — a assimetria entre YAML e Python

```
[ALVO] O item 3.1 do AUDITORIA-DEEPSEEK-CONFERIDA.md.

[FATO] Ha quatro campos declarados, lidos e nunca consumidos:
estado_io.reserva_empenhada, tese.DIFERIDOS_K, aporte.status_do_variavel e
corretora.promocional (P-32). O projeto tem
test_P28_secao_operacional_nao_tem_chave_morta protegendo o YAML e NADA
equivalente para o Python. E o N-01 esperando acontecer do lado do codigo.

[PRONTO]
1. Uma guarda para o Python, no espirito do impacto.py: todo campo de dataclass e
   toda constante de modulo em alocacao/ deve ser referenciada em algum lugar alem
   da propria definicao. Use AST, nao regex — regex acha o nome em comentario.
2. A guarda precisa declarar os proprios pontos cegos, como impacto.py ja faz:
   acesso dinamico (getattr, **kwargs, chave de dict) nao aparece na AST, e fingir
   que aparece e pior que nao ter a guarda.
3. Os quatro campos: removidos, ou usados. Decida um por um e escreva o porque.
4. pytest, ruff, mypy em zero. Um commit.

[LIMITE] Se a guarda acusar mais de cinco campos alem dos quatro, PARE e me
mostre a lista antes de remover qualquer coisa. Volume alto ai significa que a
guarda esta com falso positivo, nao que o codigo esta podre.
```

---

### 5. A esteira do histórico longo de proventos

```
[ALVO] A lacuna declarada na secao 7 do CLAUDE.md: o
GetListedSupplementCompany devolve uma JANELA recente, nao a serie completa.

[FATO] A captura de 11/09 trouxe 24 proventos da PETR. O endpoint paginado
GetListedCashDividends reportou 343 registros desde 2010 — ele aceita
{"language":"pt-br","pageNumber":N,"pageSize":99,"tradingName":"PETROBRAS"} em
base64 no caminho, e a chave e o tradingName (TEXTO), nao o codigo de 4 letras.

Armadilha ja observada e que precisa virar teste: tradingName errado devolve
totalRecords 0 com HTTP 200, em silencio. E o A-01 outra vez, num campo novo.

[PRONTO]
1. fase0/coletar_b3.py ganha --proventos-completos, que percorre as paginas ate o
   fim e grava por emissora no mesmo acervo datado.
2. O tradingName vem do acervo que JA existe (o campo esta em cada .json de
   eventos) — nao invente o texto, nao monte a partir do ticker.
3. Testes em fase0/test_coletar_b3.py, sem rede: paginacao que para no fim,
   paginacao que nao entra em laco infinito, e resposta com totalRecords 0 sendo
   ACUSADA e nao gravada como "empresa sem proventos".
4. pytest em zero. Um commit. NAO rode a coleta ainda — eu rodo depois.

[LIMITE] Nao toque no caminho --eventos que ja funciona. O acervo de 11/09 e
imutavel e nao se recupera.
```

---

## Três coisas para esperar, e o que fazer em cada uma

**Ele vai propor mais do que você pediu.** É útil e é caro. A resposta certa é *"registre
como pendência no PENDENCIAS.md com dono e gatilho, e siga no escopo"* — foi assim que
sete rodadas de engenharia viraram a alavanca errada, e a P-44 existe por causa disso.

**Ele vai querer rodar a suíte inteira toda hora.** Peça `python -m pytest -q | Select-Object -Last 3`.
São 269 testes; a saída inteira custa mais que a informação.

**Ele pode "consertar" um teste para ficar verde.** É o erro mais caro possível neste
repositório. O `CLAUDE.md` já diz *"a suíte é o júri, nunca o guia"* — se acontecer, a
frase para cortar é: *"o teste está medindo o comportamento certo? se sim, o código é que
está errado."*

---

## Quando voltar para cá

Quando o trabalho for **pesquisa com fonte primária**, **processar o acervo** ou
**subagente**. O container tem rede aberta, disco, e lê muito documento sem estourar a
sessão. O que ele não tem é a sua pasta e o seu git — e é por isso que os dois existem.

> VENCIDO — executado em 14/09/2026 (c0cbda2). Não é instrução vigente.

# Segunda, 14/09/2026 — o pacote completo

> **Tudo isto veio num único `.zip`**, já com a árvore de pastas montada. Descompacte
> por cima de `C:\Users\osvaldo.junior\Desktop\Bastter` e a estrutura cai no lugar —
> a pasta `auditoria\` é criada sozinha. **Confira o `git status` antes de commitar**:
> o zip substitui `CLAUDE.md`, `LEIA-NA-SEGUNDA.md` e `DESENHO-PIPELINE.md`, e não toca
> em mais nada que já exista.

Escrito no fim de semana, com a sua máquina desligada. **Nada aqui foi executado.**
Este arquivo substitui todas as versões anteriores: ele é a lista inteira.

**Tempo estimado:** ~30 min para os passos 0 a 4 (o essencial). O resto é por
disponibilidade.

---

## 0. Os arquivos — tudo que precisa entrar na pasta

`C:\Users\osvaldo.junior\Desktop\Bastter`

### Raiz

| arquivo | o que é |
|---|---|
| `CLAUDE.md` | **substitui** — 1.628 linhas, com tudo de 12 e 13/09 |
| `LEIA-NA-SEGUNDA.md` | **substitui** — este arquivo |
| `DESENHO-PIPELINE.md` | realinhado com a implementação |
| `PROMPTS-E01-E03.md` | os três prompts de Claude Code |
| `DEPENDE-DE-VOCE.md` | **os 9 itens que dependem de você, com instruções** |
| `B04-patch.py` | remendo de uma vez — **apagar depois de aplicado** |

### `fase0\`

| arquivo | o que é |
|---|---|
| `refinar.py` | bronze → silver dos eventos da B3 |
| `test_refinar.py` | 41 testes |

### `alocacao\`

| arquivo | o que é |
|---|---|
| `E02-patch.py` | remendo de uma vez — **apagar depois** |
| `test_e02_registros.py` | 13 testes |
| `P77-patch.py` | remendo de uma vez — **apagar depois** |
| `JCP-patch.py` | remendo de uma vez — **apagar depois** |
| `jcp.py` | alíquota do JCP por data — 4 vigências |
| `test_jcp.py` | 16 testes, os de fronteira são os que importam |
| `E08-patch.py` | remendo de uma vez — **apagar depois** |
| `IMAB11-patch.py` | remendo de uma vez — **apagar depois** |
| `test_chaves_duplicadas.py` | 10 testes — a guarda do E-09 |
| `test_e08_bloqueio_e_copia.py` | 17 testes, todos verdes |
| `test_p77_duas_pontas.py` | 14 testes |

### `auditoria\` — **pasta nova, crie**

| arquivo | o que é |
|---|---|
| `pares_irmaos.py` | ferramenta: condições tratadas de formas diferentes |
| `chaves_orfas.py` | ferramenta: chave declarada que ninguém lê |
| `test_chaves_orfas.py` | 3 portões (2 passam, 1 xfail proposital) |
| `AUDITORIA-A07-FUNCOES-IRMAS.md` | os achados E-01 a E-06 |
| `E06-O-QUE-CONTA-COMO-VARIANTE.md` | as três definições de variante |
| `PRE-REGISTRO-MODELO-DE-DADOS.md` | o esquema do pré-registro |
| `P77-CAMPO-MORTO.md` | a P-77 inteira |
| `CVM-DOWNLOAD-MANUAL.md` | **o passo a passo do download da CVM** |
| `E08-RESOLVEDOR.md` | o resolvedor de referência do `instituicoes.yaml` |
| `chaves_duplicadas.py` | ferramenta: chave YAML duplicada (E-09) |
| `F03-IMAB11-E09.md` | a taxa do IMAB11 e a chave que a apagava |
| `PREREGISTRO-EVIDENCIA.md` | **a evidência contraria minha recomendação** |
| `PREREGISTRO-RELATORIO-COMPLETO.md` | 25 fontes, status `PARCIAL` |
| `CUSTO-POR-OPERACAO.md` | o item 1, e por que a medição estreita a pergunta |
| `P76-P78-B04.md` | as três últimas |
| `FDR-PESQUISA-AMPLIADA.md` | a pesquisa de testes múltiplos — a conclusão |
| `FDR-RELATORIO-COMPLETO.md` | o relatório de pesquisa com as 21 fontes (status `PARCIAL`) |

### `docs\fontes\`

| arquivo | o que é |
|---|---|
| `lei-9249-1995-jcp-planalto.md` | JCP: 17,5%, não 15% |

> ### `coletar_b3.py` **NÃO** está na lista, e é de propósito
> O da sua máquina tem as correções B-02/B-03 que o Claude Code fez aí e que eu não
> tenho. Substituí-lo por uma cópia minha **desfaria aquele trabalho em silêncio**. Ele
> muda por remendo cirúrgico — **Prompt 1-A do `PROMPTS-E01-E03.md`**, e esse remendo
> **bloqueia o passo 4**.

---

## 1. Antes de tudo

```powershell
cd C:\Users\osvaldo.junior\Desktop\Bastter
git status --short
git ls-files | Select-String "estado.yaml"      # tem de sair VAZIO — P-67
py -3.11 -m pytest -q                            # tem de estar VERDE antes
```

**A segunda linha não pode ser pulada.** A terceira também não: remendo aplicado sobre
suíte vermelha não se distingue de remendo que quebrou.

> O `python` puro da máquina é o **3.13** e produz número que **não reproduz** o
> registrado. Para motor e testes: **`py -3.11`**. Para os coletores tanto faz — eles
> não produzem número, só gravam bytes.

---

## 2. Os três remendos prontos — 10 minutos, e são independentes

Cada um é idempotente e **aborta** se a região que espera não estiver lá. Se algum
abortar, **pare e me diga**: significa que o arquivo da máquina divergiu do que eu li.

```powershell
# B-04 — remove [build-system] do pyproject
py -3.11 B04-patch.py pyproject.toml

# E-02 — ausente / vazio / ilegível como três estados
cd alocacao
py -3.11 E02-patch.py tese.py

# P-77 — o campo morto aliquota_ganho
py -3.11 P77-patch.py alocacao.py
py -3.11 JCP-patch.py custos.yaml
py -3.11 E08-patch.py .
py -3.11 IMAB11-patch.py custos.yaml
cd ..

py -3.11 -m pytest -q
py -3.11 alocacao\ambiente.py
```

**Esperado:** suíte verde com **70 testes a mais** (13 do E-02 + 14 da P-77 + 16 do JCP + 17 do E-08), e o selo
dizendo *"O ambiente instalado É o registrado"*, com impressão **`7565df1381e2c1ed`**.

> **A impressão do ambiente não pode mudar com o B-04.** Medi aqui: `7565df1381e2c1ed`
> com e sem `[build-system]`. Se mudar na sua máquina, **pare** — significa que o
> `pyproject.toml` da máquina não é o que eu li.

Depois, apague os três `*-patch.py`. São remendos de uma vez, não ferramentas.

```powershell
git add -A
git commit -m "B-04, E-02, P-77: tres remendos com teste"
```

---

## 3. A auditoria — dois comandos, e o segundo é o que importa

```powershell
py -3.11 -m pytest auditoria -q
py -3.11 auditoria\chaves_orfas.py alocacao alocacao\politica.yaml alocacao\custos.yaml alocacao\catalogo.yaml alocacao\instituicoes.yaml
```

**Esperado no primeiro:** `2 passed, 1 xfailed`. O `xfailed` é o **E-03** e está assim
de propósito — o defeito existe, e o `strict=True` faz o teste **falhar no dia em que
alguém consertar**, obrigando a tirar o marcador.

**Se vier `3 passed`**, algum commit já corrigiu o G3/G4 e o marcador sai.

**No segundo**, confira a seção **"LIDA SÓ POR TESTE"**. É a categoria que a P-77
inventou e é pior que órfã pura: campo que só o teste toca é campo que o motor não usa —
o teste prova o esquema e ninguém prova o comportamento.

---

## 4. O primeiro silver — mas o Prompt 1-A vem antes

```powershell
py -3.11 -m pytest fase0 -q          # esperado: 41 testes, verdes
python fase0\refinar.py
```

Produz `data\silver\eventos_silver_2026-09-11.csv` — as ~8 mil linhas tipadas, cada uma
ligada ao bronze por sha256.

**O que conferir, e não é o total:** a contagem por `fator_status`.

| status | significa |
|---|---|
| `CALCULADO` | provento do paginado, com preço de véspera — **o que serve** |
| `SEM_PRECO` | provento do suplemento — redundante, sem preço |
| `FACTOR_AMBIGUO` | desdobramento/grupamento — **C-01, ver §6** |
| `SEM_FATOR` | subscrição: é direito, não ajuste de preço |
| `TIPO_DESCONHECIDO` | **A-05** — tipo fora da enumeração; a linha entrou, nada foi adivinhado |

**E três relatórios novos no fim.** Nenhum é fatal; todos pedem olho:

| relatório | o que fazer |
|---|---|
| `TIPO FORA DA ENUMERACAO (A-05)` | descubra o que o tipo faz com o preço e **aí** acrescente a `TIPOS_OBSERVADOS` — nunca ao contrário |
| `MAIS DE UM REGISTRO (A-07)` | o silver usou o primeiro. Não é regra, é a ordem em que a B3 devolveu |
| `PAGINA QUE NAO DESEMBRULHA (A-07)` | não entrou no silver; o bronze continua no disco |

Se `CALCULADO` vier muito abaixo de ~8 mil, investigue antes de seguir.

---

## 5. O COTAHIST existe? — um comando, e ele decide a semana

```powershell
Get-ChildItem data -Recurse -Filter "COTAHIST*" | Select-Object FullName, Length
```

- **Existe:** o pipeline anda até o fim e o C-01 fecha no mesmo dia.
- **Não existe:** é download da B3, gratuito e **sem prazo** — ao contrário de tudo que
  já foi capturado. Não é urgência; é agenda.

**Me mande a saída.** Ela muda a ordem do resto.

---

## 6. C-01 — o erro que eu propaguei, e como medir a correção

Escrevi em três arquivos que a PETR *"desdobrou 100:1"* e que *"o preço cai 99%"*.
**Provavelmente errado.** `factor: 100` num `DESDOBRAMENTO` é quase certamente **100%** —
cada ação vira duas e o preço cai **pela metade**.

```
leitura percentual     fator = 1/(1 + 100/100) = 0,5
leitura multiplicador  fator = 1/100           = 0,01
```

Diferem por **50 vezes**, e o `refinar.py` **não escolhe**: grava `FACTOR_AMBIGUO`.

**Com o COTAHIST, é uma consulta:**

```
PETR4, fechamento de 24/04/2008 vs 25/04/2008
   razão ≈ 2    -> factor é PERCENTUAL    (fator = 1/(1+f/100))
   razão ≈ 100  -> factor é MULTIPLICADOR (fator = 1/f)
```

Confirme em **pelo menos três** desdobramentos de emissoras diferentes e com `factor`
diferente. Coincidência em um caso não é regra.

---

## 7. Os prompts de Claude Code — `PROMPTS-E01-E03.md`

**Um commit por prompt**, nesta ordem:

| # | o quê | por quê |
|---|---|---|
| **1-A** | **A-06** — extrair `desembrulhar` do `coletar_b3.py` | **bloqueia o §4**: sem ele o `refinar.py` aborta no import |
| **1** | **E-01** — guarda `if not r.confiavel: raise` no `motor.simular` | número errado saindo: a BOVV11 bloqueada devolve R$1.329,68, empatada com a rota que não cobra nada |
| **2** | **E-03** — `g3_atrito` e `g4_dominancia` lendo `ativo` | interruptor morto produz **conclusão errada**, e conclusão errada não aparece em teste |

O Prompt 3 (E-02) já está aplicado pelo §2 — use-o só se quiser a conferência
adversarial, que inclui uma pergunta minha sobre os **outros seis carregadores**.

---

## 8. O `estado.yaml` — **não mexa**, e eu tinha escrito isto errado

A versão anterior deste arquivo mandava você digitar `reserva_atual: 8181.71` e mais
dois números. **Você me corrigiu em 12/09 e a correção está certa:** os R$500 são o
**aporte mensal**, em outro cofrinho; o Cofrinho do Cartão **não é reserva**, e isso já
estava decidido. **A reserva é ZERO.**

**O que fazer: nada.** O `estado.yaml` continua como está. A U-01 é sua e vale aqui
inteira: dado de usuário não bloqueia nem move o desenvolvimento.

> **E o ~mai/2031 do M-01 VOLTA A VALER** — eu o declarei inválido *"porque a reserva
> não é zero"*. Ela é. **Risque o `demo_aporte.py` da fila:** não há o que recalcular.

---

## 9. Em aberto — e o que é decisão sua

| # | o quê | dono |
|---|---|---|
| ~~F-03~~ | **FECHADA 13/09, COMPLETO** — a lâmina do gestor deu 0,25% (0,04+0,03+0,18) e "cobrada"=="máxima". O Tesouro vence em todas as faixas. Antes dizia: — a taxa do IMAB11 (0,25%) está em três documentos e **não** no `custos.yaml`, que ainda diz `NAO_CONFIRMADO`. E a margem é de **5 pontos-base** | **você**: pôr o valor com fonte é entrada de `custos.yaml`, e eu não abri a página do gestor |
| **P-78** | o ranking deve pontuar custo por operação além da corretagem de ação? (`mesa_minimo`, `corretagem_fii`, `exercicio_opcao_pct`) | **você** |
| **P-78-b** | `corretagem_etf_pct` é N-01: o 0,50% da XP está no `instituicoes.yaml` **e** no `catalogo.yaml`. Referenciar, não duplicar | Claude |
| **E-06** | Bonferroni × FDR: a pesquisa fechou contra o FDR (BH na 1ª descoberta **é** Bonferroni; BY é **mais** severo). Faltam as 3 escolhas do §6 do modelo de dados | **você** |
| ~~JCP~~ | **FECHADA 13/09** — 15% · **18% em 01/01→08/03/2016** · 15% · 17,5% desde **01/01/2026** (não 01/04, eu tinha errado o inciso). Ver `docs/fontes/lei-9249-1995-jcp-planalto.md` | feito |
| **JCP-b** | conferir se o acervo tem JCP pago na janela de 68 dias de 2016 — é onde a série líquida muda | você, no §4 |
| **A-04** | Marfrig: a história não está sob `MRFG` nem `MBRF`. O caminho é a CVM por `CD_CVM` — **passo a passo em `auditoria\CVM-DOWNLOAD-MANUAL.md`** | você baixa, eu processo |
| ~~E-08~~ | **FECHADO 13/09** — resolvedor `{de:}` no `instituicoes.yaml`; o ranking se nomeia e honra o `bloqueia`; as 6 cópias viraram referência e herdaram o `expira` | feito |
| — | bump de versão do `politica.yaml` + changelog, cobrindo os commits | Claude Code |

---

## 10. O que me mandar de volta

Em ordem de valor para a próxima sessão:

1. **a saída do §5** (COTAHIST existe?) — muda a ordem de tudo;
2. **quantos testes** antes e depois do §2, e se algum patch abortou;
3. **a impressão do ambiente** depois do B-04 — tem de ser `7565df1381e2c1ed`;
4. **a contagem por `fator_status`** do §4, e os três relatórios novos;
5. **`2 passed, 1 xfailed`** do §3 — ou o que vier no lugar;
6. dos prompts: as **duas reproduções** (o R$1.329,68 da BOVV11 e o `5 / 5` do G3). Se
   qualquer uma vier diferente, algum commit desde 06/09 já mexeu ali e **a auditoria
   inteira precisa ser remedida antes de qualquer outra coisa**.

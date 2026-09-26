RASCUNHO — não é o pré-registro. O pré-registro é o merge deste PR depois do 'pode empurrar' dele e do sha256 do silver na §2.

# C-02, critério v2 do degrau — pré-registro para 2016–2020

**RASCUNHO, revisão 4 de 26/09/2026. Em PR de rascunho, sem merge.** Decisão dele (P-115, `115a`): o
critério corrigido do degrau é redigido a partir de `docs/auditoria/C02-JANELA-2021-2025.md`
e **só é empurrado depois do "pode empurrar" dele**. Esta revisão incorpora a análise de
26/09 (dez pontos) e as respostas dele do mesmo dia:
- a faixa do JCP é [0,85; 1,15];
- o teto de 10% por teste e a tolerância do K5 estão aceitos;
- a dúvida entre JCP bruto e líquido sai da estatística e vai para um **portão documental**
  (§3.1).

A revisão 4 aplica os quatro ajustes que o claude.ai pediu sobre o D1: prova por evento,
`NENHUM` vira `NAO_CONFIRMADO`, o D1 gravado antes de executar, e o viés de seleção
declarado. Cada um tem a sua nota no fim (N-D1a a N-D1d).

O "pode empurrar" é **condicionado**: o texto só é gravado com a §2 preenchida pela sessão
local e depois que ele ler a versão completa. Nenhum dado de 2016 a 2020 foi tocado para escrevê-la. Ela vale **a
partir do commit empurrado que a contém** (P4, P-116), e só se a §2 estiver preenchida: o que
torna o "antes" verificável é o histórico público datado, não a data escrita aqui.

## 1. Por que um critério novo

O critério v1 (`|média ajustada do dia ex| < 0,2%`, `|t| < 2`) reprovou em 4 dos 5 anos de
2021–2025. As três causas foram medidas **depois** de ver, e em nenhuma delas o erro é do
ajuste:

1. **O nulo estava errado.** O dia ex ajustado carrega o retorno do **mercado** daquele dia,
   não zero, e as datas ex se amontoam.
2. **Dias contaminados entravam na média:** evento de quantidade no mesmo papel e dia, a
   bonificação que o COTAHIST marca e o silver não tem (A-11), e evento sem fator no mesmo
   dia.
3. **Tipos diferentes numa média única.** No dividendo, o preço cai mais do que o valor pago
   (1,164; IC 95% iid [1,092; 1,240]). No JCP, cai o que paga (0,951; [0,859; 1,044]).

O v2 corrige as três. Ele foi desenhado **vendo 2021–2025**, e por isso só vale como
pré-registro para dado **ainda não medido**: 2016–2020.

## 2. Os insumos, por impressão — nada de "vigente" nem "mais recente"

**COTAHIST anual.** São as versões fixadas em `docs/aprendizado/preregistro-ml-v2.pins.yaml`.
A **impressão de conteúdo** (`impressao.sha256`, P-139) é o que se confere. O sha256 do ZIP
identifica o byte; se a B3 reempacotar o mesmo conteúdo, a impressão não muda.

| ano | impressão de conteúdo (sha256) | registros | pregões | ZIP (sha256) |
|---|---|---|---|---|
| 2016 | `06d21272c87cb97575b98958d7086514820e8ad5e4ca4de5d6cdc6767c3dd4a6` | 466.734 | 249 | `ffc82a9b973cb5901e68dc11bea1bbc9bf0a2c46749e0efe5a7a89229bc0d81f` |
| 2017 | `016178392231bfdb0042ec33d3f9a0166c72aaf4af9cdb46ae8a2bae5639aa04` | 489.115 | 246 | `af6aaa85187c1d58ec6565522644066da573a7dc5b579c1d4c906ae95a2dea86` |
| 2018 | `c93ef4a8373ff02d98633d1017b5d2c9d01cc83abfb7df08438635aec17f46f8` | 580.155 | 245 | `9d66136179d9822476c6035000167aecf2665f4396619e4d74c0011745a0c507` |
| 2019 | `7d87898098f2cd1731e216f19b30b69b246d405696c2a441dcf6ccdac322d672` | 779.229 | 248 | `5170d3f8f079c3306424b36c2fae9b467391f8fa37d16d389f487b4c5c28edb9` |
| 2020 | `a91a6dae423744ddab18dd9672343451f7469613cc58abaf1bd8437161376a67` | 1.251.646 | 249 | `86442168939b9da7b3cc1ec1662c333ee5ab4c75f2be1865b5bf55ba4c52168f` |

**Silver de eventos.** O nome segue a P-117: `eventos_silver_<captura>_cal-<ini>-<fim>.csv`.
O calendário tem de cobrir 2016-01-01 a 2020-12-31.

| arquivo | sha256 |
|---|---|
| `eventos_silver_<PREENCHER>_cal-<PREENCHER>.csv` | `<PREENCHER NA SESSÃO LOCAL>` |

> **Com o `<PREENCHER>` o pré-registro não vale.** O silver mora no disco dele, e a sessão da
> nuvem não o alcança (§5-B.17). A sessão local gera o silver com o `refinar.py` da P-117,
> calcula o `sha256sum` e preenche as duas células. Esse é o commit que empurra. A corrida
> recusa qualquer insumo cujo sha256 difira destes.

**Código.** A corrida usa o `fase0/ajustar.py` do commit que empurra este texto, e o sha do
commit sai impresso na saída.

## 3. Definições

**Provento.** É o **valor em dinheiro por ação que a B3 publica**, e só ele. O silver o lê
de `valueCash` na listagem paginada e de `rate` no suplemento (`fase0/refinar.py`, linha 369
e vizinhança). O `ajustar.py` o aplica **sem nenhum ajuste de imposto**: o fator é
`(P_véspera − valor) / P_véspera`, e o rendimento é `y = 1 − fator` (medido no código em
26/09, `residuo_de_mercado`).

- **JCP é o valor BRUTO, antes da retenção** (Lei 9.249/1995, art. 9º §2º; transcrição em
  `docs/fontes/lei-9249-1995-jcp-planalto.md`). A série de preço é **antes de imposto**:
  nenhum passo do ajuste desconta IR.
- **Que o `valueCash` da B3 para JCP seja o bruto é `NAO_CONFIRMADO` no repositório.**
  Nenhuma fonte transcrita diz isso. Quem decide não é a estatística, é o **portão
  documental D1** (§3.1).
- **Janela de 18%.** Entre 01/01 e 08/03/2016 a alíquota do JCP foi 18% (MP 694/2015).
  Isso importa para o D1 e para a mutação M4, que lê a alíquota por data
  (`alocacao/jcp.py`, `jcp_liquido`).

### 3.1 Portão documental D1: o valor de JCP da B3 é o bruto?

**Por que é documental.** Um valor líquido no silver faria a razão do JCP subir cerca de 15%.
Mas o K2 aceita de 0,85 a 1,15, e a razão de 2021–2025 foi 0,951. Então a estatística não
separa "o mercado cai 0,95 do bruto" de "o ajuste usa o líquido". O aviso aos acionistas diz
qual dos dois valores a companhia pagou, e isso se lê na fonte.

**A amostra.**
- **Universo:** todo evento do silver fixado na §2 cujo tipo é exatamente `JRS CAP PROPRIO`,
  com data ex de 01/01/2016 a 31/12/2020 e valor > 0. Um par (ticker, data ex) conta uma vez.
- **Ordem canônica:** (data ex, ticker, valor), crescente.
- **Sorteio:** `numpy.random.default_rng(20260927).permutation(n)` sobre a ordem canônica. A
  semente é outra que a do bootstrap, para que os dois sorteios não se correlacionem.
- **Percorre-se a permutação na ordem** até ter **10** eventos com documento encontrado.
  Cada evento pulado é listado com o motivo (documento não achado, arquivo ilegível).
- **Limite de 30 tentativas.** Com menos de 10 documentos em 30 tentativas, o D1 é
  `NAO_CONFIRMADO`.

**O que se transcreve de cada evento.** Tudo vai para `docs/fontes/jcp-amostra-2016-2020.md`,
com o PDF no armazém. **Cada evento carrega a sua prova, em quatro campos, e um evento sem
os quatro não conta** *(revisão 4, nota N-D1a)*:

| prova | o que é |
|---|---|
| **URL** | o endereço de onde o PDF foi baixado (CVM/RAD ou o site de RI da companhia), com a data do acesso |
| **sha256 do PDF** | do arquivo exatamente como baixado, antes de qualquer conversão |
| **página** | a página do PDF onde está o valor |
| **trecho** | a frase do documento, copiada literalmente, que contém o valor bruto (e o líquido e a alíquota, se estiverem nela) |

E, junto com a prova:
- o documento da companhia: aviso aos acionistas, fato relevante ou comunicado, com
  protocolo e data;
- o **valor bruto** por ação, o **valor líquido** por ação (se o documento o der) e a
  **alíquota** declarada;
- a data com;
- o **valor que a B3 publicou** para o mesmo evento (`valueCash` ou `rate`, lido do silver).

**A comparação, por evento.** "Igual" quer dizer diferença ≤ meia unidade da última casa
decimal impressa no documento, porque o aviso arredonda. O líquido esperado é o do documento
ou, se ele não o der, `bruto × (1 − alíquota)`.

| classe | quando |
|---|---|
| `BRUTO` | o valor da B3 é igual ao bruto e diferente do líquido |
| `LIQUIDO` | o valor da B3 é igual ao líquido e diferente do bruto |
| `NENHUM` | não é igual a nenhum dos dois |

**O veredito do D1.**
- **PASSA** se os **10** forem `BRUTO`.
- **REPROVA** se **algum** for `LIQUIDO`. Isso vale também para a mistura: uma série com parte
  bruta e parte líquida não é ajustável por uma regra só.
- **`NAO_CONFIRMADO`** nos outros casos. **Um único `NENHUM` já deixa o D1 `NAO_CONFIRMADO`**,
  mesmo com os outros nove `BRUTO`, e nunca vira `PASSA` *(revisão 4, nota N-D1b)*. O evento
  `NENHUM` **não é trocado** pelo seguinte da permutação: pular só vale para documento não
  achado ou ilegível, antes de olhar o valor. Cada `NENHUM` sai com a diferença medida e o
  motivo provável (por exemplo, valor já ajustado por desdobramento), sem que o motivo mude
  a classe.
- **A alíquota é registrada, não julgada.** Se o documento declarar uma alíquota diferente da
  lei (15%, ou 18% de 01/01 a 08/03/2016), isso vai escrito ao lado.

**Só com D1 = PASSA a corrida de 2016–2020 roda.** REPROVA é **achado sobre o insumo**
(`ACHADOS.md`), não resultado do ajuste: o silver passa a precisar de conversão, e este
critério volta para revisão. `NAO_CONFIRMADO` também não roda.

**A ordem, gravada antes de executar** *(revisão 4, nota N-D1c)*. Três commits, cada um antes
do passo seguinte:

1. **o sorteio:** a lista das 30 primeiras posições da permutação (ticker, data ex, valor da
   B3), com o sha256 do silver de onde saiu, é empurrada **antes de abrir qualquer
   documento**. Depois disso, a ordem não muda;
2. **a transcrição:** a prova de cada evento e a classe dele, empurradas **antes da corrida**
   de 2016–2020;
3. **a corrida:** só depois do D1 = `PASSA` gravado.

Um D1 refeito depois de ver o resultado da corrida não vale: vira D1 novo, com semente nova e
nota do porquê.

**Quem faz.** A sessão local sorteia, porque o silver mora no disco dele. Os documentos são
buscados por quem alcançar a fonte, a sessão local ou a nuvem.

**Dia limpo.** `classe_do_degrau(...) == "LIMPO"`: o dia não tem evento de quantidade, nem
marca B/G do ESPECI sem evento no silver, nem evento sem fator no mesmo papel e dia.

**Excesso.** `residuo_de_mercado`: é o retorno ajustado do dia ex **menos** o mercado do dia.
O mercado do dia é a mediana do retorno bruto, no mesmo pregão, dos papéis do universo de
eventos da janela que não têm evento naquele dia (`mercado_do_dia`, mínimo de **20** papéis).
Um dia com menos papéis fica de fora e é contado.

**Razão queda/provento, por tipo.** Vem de `queda_por_provento`, `1 − Σ(e·y)/Σ(y²)`, e só
usa dias limpos cujo evento é **só DIVIDENDO** ou **só JCP**. Um ajuste perfeito dá razão
igual à queda que o **mercado** impõe por real pago. A razão 1,0 quer dizer que o preço cai
o que se paga.

**Intervalo: bootstrap por pregão.** A unidade reamostrada é o **pregão**, não o ponto: todos
os pontos de uma mesma data ex entram ou saem juntos. As datas ex se amontoam, e o mercado do
dia é comum a todos os pontos da data, de modo que reamostrar pontos trataria como
independentes resíduos que não são. A implementação:

- sorteia as datas distintas com `p88_block_bootstrap.indices(rng, n_datas, L=1)`, que com
  L=1 é o iid sobre a lista de datas, e concatena os pontos de cada data sorteada;
- faz **2.000** reamostras com **semente 20260926**, `numpy.random.default_rng`;
- gera o IC 95% pelo percentil;
- toma σ̂ como o desvio padrão das 2.000 razões.

## 4. Os critérios

### 4.1 Julgados na JANELA inteira: um teste por tipo

As razões são julgadas **uma vez, sobre 2016–2020 agrupado**. A razão de cada ano sai na
saída **só como descrição**: não julga nada, e ano nenhum reprova por ela.

**Equivalência, não "contém 1".** "Contém 1,0" premia o ruído: quanto menos dado, mais largo
o IC e mais fácil passar. Aqui é o contrário: **o IC 95% inteiro tem de caber na faixa
declarada.** Um IC largo não cabe, e ter pouco dado deixa de ser atalho para passar.

| # | tipo | faixa de equivalência | σ_max | por que esta faixa |
|---|---|---|---|---|
| K2 | JCP | **[0,85; 1,15]** | **0,0416** | escolha dele (26/09). Ela **não** tem o papel de pegar o erro bruto/líquido: esse papel é do D1 (§3.1) |
| K3 | dividendo | **[0,85; 1,35]** | **0,0463** | tem de conter **as duas** hipóteses de ajuste correto: 1,0 (o preço cai o que paga) e 1,176 (H-FISCAL, §6). K3 julga o ajuste, não o imposto |

**Veredito de cada um:**

- o IC cabe na faixa → **PASSA**;
- o IC não cabe e σ̂ ≤ σ_max → **REPROVA**;
- o IC não cabe e σ̂ > σ_max → **`NAO_CONFIRMADO` (sem poder)**;
- menos de 30 pontos ou menos de 20 pregões distintos no tipo → **`NAO_CONFIRMADO`**.

**O σ_max** é o maior desvio com que um ajuste perfeito ainda reprova em no máximo **10%** das
vezes: no K2, com razão verdadeira 1,0; no K3, no pior caso entre 1,0 e 1,176. É calculado
pela aproximação normal: a probabilidade de o IC `est ± 1,96σ` sair da faixa. Assim, "não
coube" com σ acima disso não é prova contra o ajuste, e sim falta de dado.

**Nível e multiplicidade.** Cada teste usa IC 95%. Pelo TOST, é o nível **α = 0,025** por
teste. É o que `multiplicidade.py` dá para a família: `ALFA_FAMILIAR / m`, com
`ALFA_FAMILIAR = 0,05` e **m = 2**, ou seja 0,025. Como a janela só passa se os **dois**
passarem (teste de interseção-união), a chance de declarar PASSA com um ajuste errado fica em
no máximo 0,025, sem correção. A divisão por m entra para o lado que a correção protege, o de
não reprovar à toa.

**A probabilidade de reprovar um ajuste perfeito, calculada** (aproximação normal; script
em [`C02-CRITERIO-V2-poder.py`](C02-CRITERIO-V2-poder.py), no mesmo PR):

| cenário | K2 JCP | K3 dividendo | janela |
|---|---|---|---|
| σ no teto (σ = σ_max nos dois) | REPROVA ≤ 10,0% | REPROVA ≤ 10,0% (razão 1,0) · 3,6% (razão 1,176) | **REPROVA ≤ 19,0%** (`1 − 0,9²`) |
| σ iid de 2021–2025 (JCP 0,0472, n=819; div. 0,0378, n=400) | REPROVA 0%; `NAO_CONFIRMADO` 22,3% (σ > σ_max) | REPROVA 2,2% (razão 1,0) · 0,4% (razão 1,176) | REPROVA ≤ 2,2%; não-PASSA 24,1% |
| a faixa-exemplo [0,90; 1,10] no JCP, σ de 2021–2025 | **não cabe 87,4%** (σ_max 0,0277) | — | — |

**Leitura:**

- **O bootstrap por pregão alarga o IC**, e o quanto é desconhecido antes de rodar. Os
  números iid da segunda linha são o **piso** da chance de não passar, não a estimativa.
  Com os dados de 2021–2025, o JCP já sairia `NAO_CONFIRMADO` por falta de poder em 22% das
  vezes. É provável que 2016–2020, com menos JCP, saia sem poder: o critério **diz** isso em
  vez de reprovar.
- **Com o iid de 2021–2025, a própria janela teria passado:** 0,951 [0,859; 1,044] cabe em
  [0,85; 1,15], e 1,164 [1,092; 1,240] cabe em [0,85; 1,35]. Não passaria na faixa
  [0,90; 1,10].
- A razão medida do JCP (0,951) não é 1,0. Se a verdadeira for 0,95, a chance de não caber
  sobe. Ela está dentro da faixa, e a faixa não é uma afirmação de que o valor é 1,0.

### 4.2 Julgados ANO A ANO: determinísticos ou de contagem, sem multiplicidade a corrigir

| # | critério | passa se | por quê |
|---|---|---|---|
| K1 | **controle** | nos pares de pregões sem evento no segundo dia, `max |r_aj / r_bruto − 1| ≤ 1e-12` | o ajuste não pode mexer onde não há evento |
| K5 | **quantidade, sobre o resíduo** | todo evento de quantidade grande (fator ≤ 0,67 ou ≥ 1,5) com preço no dia e na véspera tem **excesso** (ajustado − mercado do dia) em **±15%**; **tolerância: no máximo 1 evento por ano fora**, e cada evento fora sai listado por ticker, data e fator | a leitura do `factor` (C-01) continua testada fora da amostra, sem que o crash de março de 2020 reprove um desdobramento certo |
| — | **completude** | no máximo **1/3** dos degraus do ano fora dos dias limpos; no máximo 1/3 dos eventos grandes de quantidade sem mercado do dia | acima disso, o ano mede o acervo, não o ajuste |

**K1: o valor medido e a tolerância.** Em 2021–2025, o controle deu pior divergência
**1,0e-27 em cada um dos 5 anos** (n = 632.384 pares; 42.534 deles com diferença ≠ 0).
Não é zero exato, e o motivo é aritmético (`ajustar.controle`): o acumulado é um `Decimal`
de 28 dígitos significativos, e `(p·k)/(q·k)` arredonda na última casa. Por que 1e-12
relativo:

- **fica 15 ordens de grandeza acima do medido**, de modo que o arredondamento acumulado do
  `Decimal` nunca reprova, mesmo com milhares de eventos por série;
- **acomoda uma troca do acumulado para `float64`**: com épsilon de 2,2e-16 e dezenas de
  operações, o erro fica ~1e-14;
- **fica ao menos 8 ordens abaixo do menor defeito real.** Um fator aplicado no dia errado
  move o retorno pelo tamanho do provento: um rendimento de 0,01% já é 1e-4. Numa ação de
  R$ 1.000, 1e-12 é R$ 1e-9.

Hoje `controle_por_ano` mede `|r1 − r0|` absoluto. Sobre razões de preço perto de 1, o
absoluto e o relativo coincidem na ordem de grandeza. O critério fixa o **relativo**, e a
implementação passa a medir o relativo antes da corrida, com teste.

**K5: por que ±15% e 1 por ano.** A janela tem março de 2020, com dias em que o próprio
mercado caiu dois dígitos, e por isso K5 julga o **resíduo** contra o mercado, não o retorno
ajustado. Um desdobramento pode coincidir com notícia da própria empresa (balanço no mesmo
dia) e passar de 15% com o ajuste certo, uma vez. Dois no mesmo ano são padrão, não acaso.
Um ano **sem** evento grande de quantidade não aplica K5, e isso é escrito. Na janela, K5
exige ao menos **10** eventos grandes somados; com menos, a **janela** fica
`NAO_CONFIRMADA` (em 2021–2025 foram 54 eventos de quantidade no total).

### 4.3 O resultado da janela

- **Pré-condição:** D1 = PASSA (§3.1). Sem isso a corrida não roda, e não há resultado de
  janela.
- **PASSA** só se os **cinco anos** forem aprovados (K1, K5 e completude) **e** K2 e K3
  passarem **e** K6 (§5) tiver poder.
- **REPROVA** se qualquer ano reprovar em K1 ou K5, ou se K2 ou K3 reprovar.
- **`NAO_CONFIRMADA`** nos demais casos: qualquer `NAO_CONFIRMADO` num ano (inclusive por
  completude) ou em K2, K3 ou K5, sem reprovação. Nunca vira PASSA por maioria.
- **`CRITERIO_SEM_PODER`** se K6 falhar, qualquer que seja o resto. Nesse caso o critério não
  mede nada, e **não existe PASSA**.

## 5. K6 — o critério pode reprovar?

Cada mutação altera **só a entrada do ajuste**. O `y` da estatística vem sempre do silver
**não mutado**, o valor verdadeiro. Se o `y` viesse do silver mutado, "provento ignorado"
tiraria os pontos da conta e viraria `NAO_CONFIRMADO` em vez de reprovar. Com `k` a queda
verdadeira do mercado e `c` o múltiplo do valor que o ajuste usa, a razão medida é
`1 − c + k`, e a coluna "razão esperada" sai dessa conta.

| mutação | o que muda | razão esperada (k=1) | tem de levar a |
|---|---|---|---|
| M1 data ex deslocada | o fator entra no último dia com direito | ≈ 0 (no dia deslocado o preço não cai e o ajuste soma `y`) | REPROVA em K2 **e** em K3 |
| M2 fator invertido | `1/f` em todo evento | — | REPROVA em K5 em ≥ 3 dos 5 anos |
| M3 provento ×1000 | `valor × 1000` | ≈ −998 | REPROVA em K2 **e** em K3 |
| M4 JCP líquido | na **amostra do D1**, o valor da B3 trocado por `jcp_liquido(bruto, data, C)`: 15%, ou 18% de 01/01 a 08/03/2016 | não se aplica: coberta pelo D1, não pelo K2 | **D1 REPROVA**, com os 10 eventos `LIQUIDO` |
| M5 provento ignorado | valor = 0 | ≈ 2,0 | REPROVA em K2 **e** em K3 |

**K6 passa se cada uma das cinco produzir a reprovação da sua linha.** M1, M2, M3 e M5 rodam
no mesmo dado de 2016–2020; a M4 roda sobre a amostra transcrita do D1. Um `NAO_CONFIRMADO`
numa mutação conta como falha do K6: um critério que não distingue a leitura errada da certa
não tem poder.

**Por que a M4 saiu do K2.** Na revisão 2 ela ficava em cima da borda da faixa do JCP. Se a
razão verdadeira fosse 0,95 (2021–2025 mediu 0,951), a M4 cairia para ~1,10, caberia na faixa,
e o K6 falharia por uma pergunta que a estatística não consegue responder. No D1 a diferença
entre bruto e líquido é de 15% (18% em 2016) contra uma tolerância de arredondamento de
centésimos de centavo, então a M4 é pega com folga.

## 6. Hipótese secundária H-FISCAL — previsão, não julga o ajuste

Elton e Gruber (1970): no dia ex, o preço cai o que o investidor marginal fica indiferente
entre receber como provento ou como ganho de capital. No Brasil de 2016–2020:

- **dividendo isento, ganho de capital a 15%:** a razão prevista é `1/(1 − 0,15) = 1,176`;
- **JCP retido a 15% na fonte, ganho a 15%:** a razão prevista é **≈ 1,0**.

**Registrada como previsão:** razão do dividendo ≈ 1,176 e do JCP ≈ 1,0. O que se reporta
é se o IC do dividendo contém 1,176 e se o do JCP contém 1,0. **Ela não julga o ajuste:** o
K3 foi desenhado para passar com 1,0 e com 1,176.

**A ressalva.** O investidor que forma o preço pode ter outra carga de imposto. O
estrangeiro e o fundo têm regimes próprios, e a pessoa física que vende menos de R$ 20 mil
por mês é isenta no ganho (Lei 11.033/2004, art. 3º, I). Para esses, a assimetria não existe
e 1,176 deixa de ser a previsão. O mecanismo segue `NAO_CONFIRMADO`: um IC que contém 1,176
é compatível com a hipótese, não a prova.

## 7. O que acontece se reprovar

**O resultado é o achado.** O critério não é afrouxado depois de ver: o teste entra como
foi escrito, em `xfail(strict=True)` com a causa medida no motivo, a mesma decisão dele de
21/09 para o v1. `NAO_CONFIRMADA` e `CRITERIO_SEM_PODER` também entram como estão, com a
razão escrita. Um critério v3, se vier, vale para dado que ninguém mediu ainda.

## 8. O que este pré-registro não protege (P5) — os limiares escolhidos

Nenhum destes é derivado. Estão escritos antes para não serem escolhidos depois:

| limiar | valor | onde |
|---|---|---|
| janela | 2016–2020 | tudo |
| faixa do JCP | [0,85; 1,15] | K2 |
| faixa do dividendo | [0,85; 1,35] | K3 |
| teto de reprovar ajuste perfeito | 10% por teste | σ_max |
| nível | 95% (α 0,025 por teste, m = 2) | K2, K3 |
| pontos e pregões mínimos | 30 e 20 | K2, K3 |
| mercado do dia | mediana, ≥ 20 papéis | excesso |
| tolerância do controle | 1e-12 relativo | K1 |
| evento de quantidade grande | fator ≤ 0,67 ou ≥ 1,5 | K5 |
| banda do resíduo | ±15% | K5 |
| tolerância de contagem | 1 por ano; ≥ 10 na janela | K5 |
| completude | ≤ 1/3 fora | por ano |
| bootstrap | por pregão, 2.000, semente 20260926, percentil | K2, K3 |
| M2 | ≥ 3 de 5 anos | K6 |
| amostra do D1 | 10 eventos, semente 20260927, até 30 tentativas | D1 |
| igualdade no D1 | ≤ meia unidade da última casa do documento | D1 |
| veredito do D1 | 10 de 10 `BRUTO`; qualquer `LIQUIDO` reprova; qualquer `NENHUM` deixa `NAO_CONFIRMADO` | D1 |
| prova do D1 | URL, sha256 do PDF, página e trecho literal, por evento | D1 |

Além deles, ficam fora da proteção:

- **As faixas dependem da aproximação normal para o σ_max.** O bootstrap real pode ser
  assimétrico. O σ_max é uma regra declarada, não uma garantia exata.
- **O K3 não detecta erro pequeno no dividendo.** A faixa tem de conter 1,0 e 1,176, e com
  isso um erro de 15% no valor do dividendo passa. O K3 pega os erros grosseiros (M3, M5 e o
  fator invertido); o fino fica sem proteção, e isso é escrito.
- **O D1 é uma amostra, não um censo.** Dez eventos `BRUTO` não provam que todos os JCPs de
  2016–2020 são brutos: um erro em 5% dos eventos passaria em 60% das amostras de 10
  (`0,95¹⁰ = 0,60`). O D1 pega um erro **sistemático** (a B3 publicar sempre o líquido), que
  é o que a dúvida levantava. Um erro esporádico fica sem proteção, e isso é escrito.
- **O D1 tem viés de seleção, e ele é declarado** *(revisão 4, nota N-D1d)*. Três fontes:
  - **o universo é o silver**, que cobre as emissoras capturadas da B3 (74 no acervo de
    11/09) — companhias que saíram da bolsa antes da captura não estão nele;
  - **só entra o evento cujo documento foi achado**, e documento de 2016 é mais fácil de
    achar em companhia grande e ainda listada, com site de RI mantido;
  - **o pulo por documento não achado** tira da amostra justamente os eventos de companhias
    menores ou extintas.

  O D1 fala dos JCPs **com documento acessível** das emissoras do silver, não de todos os JCPs
  de 2016–2020. Quantos foram pulados, e por quê, sai na transcrição; mais de 10 pulos nas 30
  tentativas é escrito como sinal de que a amostra encolheu para as companhias mais visíveis.
- **Os sha256 cobrem o insumo, não a fonte.** Se a B3 tiver publicado um valor errado em
  2016, o ajuste aplica o erro fielmente e o critério não vê.

---

## Notas de revisão

*Revisão 4, 26/09/2026 — os quatro ajustes pedidos pelo claude.ai, aplicados no Claude Code (nuvem).*

- **N-D1a · prova do D1.** Cada evento da amostra carrega URL, sha256 do PDF, página e trecho
  literal. Sem os quatro, o evento não conta: é a P1 aplicada ao portão, e o que permite a
  qualquer pessoa conferir a classe sem refazer a busca.
- **N-D1b · `NENHUM` vira `NAO_CONFIRMADO`.** Na revisão 3, `NENHUM` já não passava, mas o
  texto não dizia que um só bastava, nem proibia trocar o evento pelo próximo da permutação.
  Trocar seria escolher a amostra depois de ver o valor.
- **N-D1c · o D1 gravado antes de executar.** A lista sorteada é empurrada antes de abrir
  documento, e a transcrição antes da corrida: três commits, na ordem. É a P4 aplicada ao
  próprio portão, que antes só dizia "a transcrição entra num commit próprio antes da
  corrida" e deixava o sorteio sem data verificável.
- **N-D1d · viés de seleção declarado.** O universo é o silver (emissoras capturadas), e o
  pulo por documento não achado favorece companhias grandes e listadas. O D1 passa a dizer do
  que ele fala: JCPs com documento acessível, não todos os JCPs da janela.

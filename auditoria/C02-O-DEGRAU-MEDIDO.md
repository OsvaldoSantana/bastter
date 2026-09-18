# C-02 — o degrau medido: o ajuste de preço contra 293 datas-ex de 2023

**Medido em 18/09/2026**, sobre o silver de `dt_captura=2026-09-11` (9.272 linhas) e o
`COTAHIST_A2023`. Módulo: `fase0/ajustar.py`. Suíte: `fase0/test_ajustar.py`, 32 testes —
24 sintéticos e 8 contra o acervo. Status: **MEDIDO**.

## A pergunta, e por que ela não se responde lendo campo

O C-01 fechou em 16/09 a leitura do campo `factor` **pela distribuição** dos 180 valores,
com **uma** corroboração de preço. A distribuição é um argumento forte e continua de pé;
o que ela não pode fazer é falar sobre a outra metade do ajuste — o fator de provento, o
sentido em que ele se aplica, e a data em que o degrau cai.

O preço responde tudo isso de uma vez, e com uma pergunta só:

> No dia em que a ação fica ex, o retorno cai porque saiu dinheiro da empresa. Depois do
> ajuste, esse retorno tem de deixar de ser distinguível de zero.

**Se o degrau não encolher, o ajuste está errado.** Não há resposta intermediária, e é por
isso que o teste que decide não mede um campo: mede duas séries.

## O resultado

```
O DEGRAU DO DIA EX -- 293 datas ex com pregao no dia e na vespera
  retorno BRUTO    media  -1.6263%   t   -9.88
  retorno AJUSTADO media  -0.0360%   t   -0.29
  CONTROLE: 86736 pares de pregoes SEM evento; 6500 com retorno diferente (pior 1.0e-27)
```

O degrau bruto é **−1,63%**, a dez desvios-padrão de zero. Depois do ajuste sobra
**−0,036%**, com t = −0,29 — dentro do ruído por qualquer critério. A média cai por um
fator de **45**.

O que se mede é a **média**, nunca o caso: o desvio-padrão diário de uma ação brasileira é
~1,9% e engole qualquer provento de 1%. Nenhum dia ex isolado prova nada aqui, e é
exatamente por isso que a corroboração de 16/09, com um caso, precisava desta.

### O controle, que é metade da prova

Em 86.736 pares de pregões consecutivos **sem evento**, o retorno tem de ser idêntico
antes e depois. É o par obrigatório do teste acima: uma função que multiplicasse a série
inteira por um número qualquer também encolheria degraus — e estragaria todo o resto sem
ninguém ver.

A única diferença observada é de **1e-27**, e ela é aritmética, não conceitual: o fator
acumulado é um `Decimal` de 28 dígitos significativos, e `(p·k)/(q·k)` arredonda na última
casa. Trinta ordens de grandeza abaixo do centavo.

## As duas mutações — porque guarda que nunca falhou é guarda que ninguém sabe se funciona

Reintroduzi os dois erros que o ajuste existe para evitar, e remedi os **mesmos 293 dias**:

| | média no dia ex | t | o que acontece |
|---|---|---|---|
| ajuste correto | **−0,04%** | −0,29 | o degrau some |
| **data ex deslocada** (usa `lastDatePrior`) | **−1,63%** | −9,88 | o degrau fica **inteiro** |
| … e na véspera | **+1,91%** | +11,20 | nasce um degrau **falso** |
| **fator invertido** (1/f) | **−3,16%** | −12,98 | o degrau **dobra** |

Duas coisas saem daí:

1. **Um dia de erro não "erra um pouco".** A data deslocada deixa o degrau onde estava
   *e* cria outro, do mesmo tamanho e sinal contrário, um pregão antes. Piora duas vezes.
   Em 16/09 essa afirmação tinha **um** caso (a FLRY); agora tem 293.
2. **Não existe leitura errada de fator que encolha um degrau.** Ela inverte ou aumenta.
   É isso que transforma o resultado acima em prova e não em coincidência.

As duas mutações estão presas na suíte (`test_REAL_a_data_ex_DESLOCADA_reprova_em_293_casos`,
`test_REAL_o_fator_INVERTIDO_dobra_o_degrau`), além das versões sintéticas exatas.

## O que esta medição NÃO decide — e a distinção vale mais que o resultado

Das 293 datas ex medidas, **292 são provento em dinheiro e UMA é evento de quantidade**
(a bonificação da FLRY). Escrevendo em uma frase o que a medição mediu:

> O ajuste remove o degrau de **provento em dinheiro**, na **data ex derivada do
> calendário observado**, com o fator aplicado no **sentido** certo.

Confirmado com 293 casos: a data ex, o sentido do fator, e a fórmula
`(P_véspera − valor)/P_véspera`.

**Não confirmado por esta medição:** a leitura *percentual* do campo `factor` nos 178
eventos de quantidade. Essa continua sustentada pela distribuição (`C01-FATOR.md`) mais
este único caso de preço. Fechar a ponta custa **um download**: o COTAHIST de **2021** (19
eventos de quantidade) e **2025** (31) levaria a corroboração de preço de 1 para 51 — e os
casos grandes, que são os que o preço resolve com folga.

## Duas fontes independentes conferem, e nenhuma delas era esperada

### O preço de véspera da B3 bate com o COTAHIST em 352 de 352

O `closingPricePriorExDate` vem do endpoint de proventos; o fechamento vem do arquivo de
cotações. São duas bases diferentes da mesma casa — as mesmas duas que divergiram no B-02
e no B-03 sobre o *nome* da empresa. Sobre o **preço**, em 352 casos, batem **exatamente,
ao centavo, sem uma exceção**.

Isso não é redundância: é o que prova que o casamento evento↔ticker está certo. Um ticker
errado não dá um preço parecido, dá o preço de outra empresa.

### O COTAHIST escreve a data ex dentro do próprio arquivo de preço

Achado lateral, e ele não custou nada. O campo **ESPECI** não é só `ON`/`PN`: ele carrega a
marca de ex — `ON  ED  NM` (ex-dividendo), `PN  EJ  N1` (ex-juros), `ON  EB  NM`
(ex-bonificação), `ON  EG` (ex-grupamento).

| | resultado |
|---|---|
| datas ex derivadas em que o ESPECI **muda naquele dia** | **284 de 293 (96,9%)** |
| pares de pregões **sem evento** em que ele muda assim mesmo | 1.382 de 86.736 (**1,59%**) |
| datas ex em que o dia **não** carrega marca nenhuma | **0** |

As 9 que não mudam são datas ex **consecutivas**, em que a véspera já estava marcada —
inconclusivas, não contrárias. **É uma terceira fonte para a data ex, dentro do mesmo
arquivo de preço, e que não depende de preço nenhum.**

Ela **não** entra em nenhuma conta do módulo, de propósito: usá-la exigiria enumerar as
marcas, e a tabela ESPECI do layout publicado está **incompleta** — 2023 traz `EX`, `EC`,
`EBG`, `ERC`, `EDG`, `ERG`, `EDC` e `EDS`, que ela não lista. As duas colunas ficam em
bruto no CSV de degraus, para conferência humana. Enumerar a partir do dado é o caminho
(A-05), e ele está aberto.

## Achados que a corrida produziu

### A-09 — a B3 devolve o mesmo provento duas vezes, byte a byte

`ALOS/pagina-001.json` traz o dividendo de 28/04/2023 **repetido**, campo a campo, na mesma
página. São **334 duplicatas exatas** no silver inteiro, 16 delas na janela de 2023.

Somar as duas subtrai o dividendo duas vezes do preço. Colapsar é a decisão — e ela **não é
hipótese, é medida**, nos 13 casos com data ex em 2023:

| | resíduo médio no dia ex |
|---|---|
| colapsando a duplicata | **−0,62%** |
| contando as duas | **+0,28%** |

A duplicata sobre-ajusta em ~0,9 pp, exatamente a ordem do dividendo. Colapsar fica.

O arquivo de origem entra na chave de propósito: dois registros iguais em **páginas
diferentes** são sobreposição de paginação, e aí o julgamento seria outro. Hoje não existe
nenhum — e no dia em que existir, a contagem aparece em vez de ser absorvida.

### A-08 — o evento na borda: o único defeito que não muda número nenhum hoje

Oito eventos com `ultimo_dia_com_direito = 28/12/2023` — **o último pregão observado**.
A data ex deles é 02/01/2024, que o calendário não alcança, então não foi derivada.

O fator desses eventos multiplicaria a série **inteira**. Consequência: **nenhum retorno de
dentro de 2023 muda**, e o **nível** fica deslocado. Não aparece no degrau, não aparece no
controle, não aparece em teste nenhum de retorno.

Aparece no dia em que o COTAHIST de 2024 entrar no acervo e as duas pontas forem
emendadas — com um salto artificial exatamente na virada do ano. Sete tickers:
**B3SA3, CMIN3, ENGI3, ENGI4, ENGI11, ITUB3, ITUB4**, marcados `NIVEL_INCERTO` em toda
linha da tabela.

**A distinção que dá valor ao achado:** 1.368 eventos têm data ex *posterior* à janela e
também não foram aplicados — e isso **não é defeito**, é propriedade do ajuste retroativo,
que reescala o passado a partir do fim da série. Marcar os dois casos juntos poria 1.368
linhas no relatório e ensinaria a ignorá-lo. São contados separadamente.

### 13 eventos dentro da janela sem ticker nenhum — o A-03/A-04 chegando ao preço

| emissora no evento | ticker de 2023 | eventos |
|---|---|---|
| AXIA (ON, PNA, PNB) | ELET3 / ELET5 / ELET6 | 3 |
| AZZA (ON) | ARZZ3 | 4 |
| ISAE (ON, PN) | TRPL3 / TRPL4 | 4 |
| MOTV (ON) | CCRO3 | 2 |

A emissora trocou de código; o evento chega com o código **novo** e o preço de 2023 está
sob o **antigo**. O evento não casa com nada — e a série do código antigo fica **sem esse
ajuste, em silêncio**, porque não há a quem atribuir a marca.

O módulo acusa os 13 no relatório e sai com código ≠ 0. Não remenda: a ponte
ticker-antigo ↔ ticker-novo é o mesmo mapeamento bitemporal que o A-03 já pediu, e
inventá-la aqui por semelhança de nome seria o A-01 outra vez.

## O que a série NÃO sabe (P5), declarado por ticker

Cada linha da tabela de preços carrega `ajuste_status` — a marca viaja com o dado, para que
quem leia uma fatia não possa deixar de ver:

| status | tickers | o que significa |
|---|---|---|
| `AJUSTADO` | 74 | todo evento capturado que alcança a série foi aplicado |
| `NIVEL_INCERTO` | 7 | A-08: retornos certos, nível deslocado |
| `INCOMPLETO` | 0 | evento dentro da janela **sem fator** — hoje não há nenhum |
| `SEM_EVENTO_CAPTURADO` | 373 | nenhum evento **do acervo** alcança esta série |

O nome do último tem `CAPTURADO` porque a alternativa mentiria: o acervo de eventos cobre
as 74 emissoras do IBOV e o COTAHIST cobre 454 papéis à vista. Um FII que pagou rendimento
todo mês sai daqui sem evento — e `SEM_EVENTO` seria lido como afirmação sobre a **empresa**
quando é afirmação sobre o **acervo**.

## Saídas

```
data/silver/precos_ajustados_2026-09-11.csv      87.483 linhas, 454 papeis
data/silver/degrau_datas_ex_2026-09-11.csv      293 linhas -- a evidencia desta medicao
```

O segundo é a tabela que sustenta cada número acima, linha a linha, com o ESPECI da véspera
e do dia ex ao lado.

## Instantâneo dourado do refactor

`calendario.py` ganhou `arquivos()`, `registros()` e `data_de()` — extraídos para que os
**dois** leitores de COTAHIST do projeto não reimplementem a descoberta de arquivo nem a
posição da data (N-01). `pregoes()` antes e depois: **248 pregões**, cobertura
`2023-01-02 … 2023-12-28`, `sha256 = e4a9d81d3d6d4cb8810b86322de3d08415f7a3fed23b32d923b4291c13bd551c`
— **idêntico**.

## O que continua aberto

1. **A leitura percentual do `factor` tem uma corroboração de preço.** COTAHIST de 2021 e
   2025 leva a 51. É o download mais barato que existe no projeto hoje. ⚙ desktop.
2. **Os 13 eventos sem ticker** exigem a ponte de código antigo↔novo (A-03/A-04).
3. **O ESPECI como fonte de data ex** — enumerar as marcas a partir do dado observado,
   como o A-05 manda, e usá-lo para conferir o calendário sem depender de preço.
4. **A regra do grupamento continua sem nenhuma confirmação de preço**: os 41 grupamentos
   são todos fora de 2023.

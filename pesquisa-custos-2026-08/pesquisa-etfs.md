# ETFs na B3 e regime de BDRs — pesquisa auditável

**Data de acesso de todas as fontes: 31/08/2026** (salvo indicação em contrário)
**Regra aplicada:** só há número aqui se ele foi lido numa fonte. Onde não confirmei, está escrito **NÃO CONFIRMADO**. Nenhuma taxa de administração e nenhuma liquidez foi estimada.

---

## AVISO METODOLÓGICO — leia antes da tabela

Três decisões de procedência que mudam a leitura de tudo o que vem abaixo:

1. **A lista oficial de ETFs da B3 NÃO foi obtida.** A página `b3.com.br/.../etfs-listados/` apenas redireciona para `https://sistemaswebb3-listados.b3.com.br/fundsListedPage/ETF`, que é uma aplicação JavaScript. A API por trás dela (`.../fundsListedProxy/Search/GetListFunds/<base64>`) foi localizada no bundle da própria B3 e respondeu, mas devolveu `totalRecords: 0` para todos os filtros testados, e outras variações caíram em bloqueio Cloudflare. **Status: NÃO OBTIDO.**

2. **No lugar dela usei o registro da CVM**, que é o regulador e é fonte primária de hierarquia igual ou superior à B3 para razão social, gestor, PL e situação cadastral:
   `https://dados.cvm.gov.br/dados/FI/CAD/DADOS/registro_fundo_classe.zip` (arquivos internos `registro_classe.csv` + `registro_fundo.csv`, `Last-Modified: 31/08/2026 04:38 GMT`; conteúdo datado de 31/08/2026 01:30).
   ETFs aparecem como `Tipo_Classe = "Classes de Cotas de Fundos FIIM"` (FIIM = Fundo de Investimento em Índice de Mercado).
   **Ressalva importante:** o campo `Data_Inicio` desse arquivo traz, para muitos fundos, a data de adaptação à RCVM 175 (2025), **não** a data de início original do fundo. Por isso, sempre que tive a lâmina do gestor, usei a data dela.

3. **A liquidez não é estimada nem copiada de agregador.** Foi calculada por mim a partir do arquivo oficial de cotações históricas da B3:
   `https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2026.ZIP` (79.474.595 bytes; arquivo interno `COTAHIST_A2026.TXT`, 646.136.439 bytes, com pregões de 02/01/2026 a 28/08/2026).
   Critério: mercado à vista (`TPMERC = 010`), campo `VOLTOT` (posições 171–188), somado sobre os **20 pregões de agosto/2026 (03/08 a 28/08)** e dividido por 20. É volume financeiro realizado, não uma média projetada.

**Consequência crítica do item 3:** os ETFs de **renda fixa** (IMAB11, IRFM11, B5P211, IB5M11, AREA11 etc.) **não aparecem em nenhuma linha do COTAHIST_A2026** — zero ocorrências no arquivo inteiro. Isso **não** significa que foram encerrados: a lâmina do Itaú para IMAB11 é datada de 31/07/2026 e a de B5P211 de 31/07/2026, ambas vigentes. A leitura mais provável é que esses ETFs negociam no ambiente de renda fixa da B3, fora do arquivo à vista do segmento Bovespa. **Não consegui confirmar essa explicação em fonte da B3 — está NÃO CONFIRMADO.** O que está confirmado é o fato bruto: ausência no COTAHIST à vista.

---

## 1. LISTA OFICIAL E TAMANHO DO UNIVERSO

| Métrica | Valor | Fonte | Status |
|---|---|---|---|
| ETFs (classes FIIM) registrados na CVM, situação "Em Funcionamento Normal" | **222** | CVM `registro_fundo_classe.zip`, 31/08/2026 | COMPLETO |
| ETFs (classes FIIM) em "Fase Pré-Operacional" | **26** | idem | COMPLETO |
| Total de classes FIIM no cadastro | **248** | idem | COMPLETO |
| Soma do patrimônio líquido dos 222 em funcionamento | **R$ 134.657.698.272,98** | idem (datas de PL entre 20/08 e 27/08/2026, campo `Data_Patrimonio_Liquido`) | COMPLETO — mas é soma de PLs com datas-base ligeiramente diferentes |
| Tickers com espécie `CI` (ETF + FII + FIAgro etc.) que negociaram à vista em ago/2026 | **600** | COTAHIST_A2026 | COMPLETO |
| Lista oficial da B3 com ticker + razão social + gestor + taxa | — | b3.com.br | **NÃO OBTIDO** |

**Gestores por número de ETFs** (CVM, 31/08/2026): BTG Pactual Asset 34 · Itaú Unibanco Asset 33 · Investo 31 · XP Allocation 23 · Buena Vista 16 · Bradesco 14 · Nu Asset 13 · BB Gestão 11 · Galápagos 10 · Hashdex 9 · BlackRock Brasil 7 · Safra 4 · QR Asset 3 · Empiricus 2.

Observação de leitura: **a BlackRock tem só 7 ETFs e o maior PL individual do mercado.** A concentração de produto (BTG/Itaú/Investo/XP) e a concentração de patrimônio são coisas diferentes.

### Os 15 maiores ETFs por patrimônio líquido (CVM, PL de 20–27/08/2026)

| # | Razão social | PL (R$) | Gestor |
|---|---|---|---|
| 1 | ISHARES IBOVESPA CLASSE DE ÍNDICE | 14.947.483.239,92 | BlackRock Brasil |
| 2 | B-INDEX ETF TEVA LFT CURTO PRAZO FUNDO DE ÍNDICE | 13.524.090.574,34 | Banco Bradesco |
| 3 | IT NOW IBOVESPA FUNDO DE ÍNDICE | 7.660.408.131,40 | Itaú Unibanco Asset |
| 4 | ISHARES S&P 500 CLASSE DE ÍNDICE EM COTAS DE CLASSES DE ÍNDICE IE | 7.580.780.653,89 | BlackRock Brasil |
| 5 | INVESTO ETF MARKETVECTOR BRAZIL TREASURY 760 DAY TARGET DURATION | 5.396.292.342,15 | Investo |
| 6 | IT NOW S&P 500 FUTURES QUANTO BRL FUNDO DE ÍNDICE | 4.794.930.502,20 | Itaú Unibanco Asset |
| 7 | BTG PACTUAL TEVA TESOURO SELIC FUNDO DE ÍNDICE | 4.320.025.144,81 | BTG Pactual Asset |
| 8 | IT NOW IMA-B5 P2 FUNDO DE ÍNDICE | 4.001.480.704,20 | Itaú Unibanco Asset |
| 9 | IT NOW ID ETF IMA-B FUNDO DE ÍNDICE | 3.589.397.916,40 | Itaú Unibanco Asset |
| 10 | IT NOW TEVA TESOURO SELIC FUNDO DE ÍNDICE | 3.199.914.119,80 | Itaú Unibanco Asset |
| 11 | HASHDEX NASDAQ CME CRYPTO INDEX FUNDO DE ÍNDICE | 2.668.358.171,70 | Hashdex |
| 12 | BTG PACTUAL IMA-B 5 P2 FUNDO DE ÍNDICE | 2.627.563.919,50 | BTG Pactual Asset |
| 13 | IT NOW IDIV FUNDO DE ÍNDICE | 2.294.904.938,70 | Itaú Unibanco Asset |
| 14 | ETF BRADESCO IBOVESPA (classe de investimento) | 2.279.910.637,08 | Banco Bradesco |
| 15 | INVESTO TEVA TESOURO SELIC ETF CLASSE DE ÍNDICE | 2.124.680.032,22 | Investo |

Note que **6 dos 15 maiores são de renda fixa** (LFT/Selic/IMA-B) — o mercado brasileiro de ETF é muito mais um mercado de renda fixa do que a conversa pública sugere.

---

## (A) TABELA MESTRE — ficha por ETF

Legenda: **Taxa adm.** e **PL** só aparecem com fonte. **Liq. méd. diária** = calculada por mim do COTAHIST_A2026, agosto/2026, 20 pregões. `NC` = NÃO CONFIRMADO.

### Renda variável Brasil

| Ticker | Nome / razão social | Gestor | Índice | Taxa adm. | Perf. | PL | Liq. méd. diária ago/26 | Início | Distribui? |
|---|---|---|---|---|---|---|---|---|---|
| **BOVA11** | iShares Ibovespa Fundo de Índice | BlackRock Brasil | Ibovespa | **0,10%** ¹ | NC | **R$ 14.166.867.545** (28/08/2026) ¹ · CVM: R$ 14.947.483.239,92 (26/08) | **R$ 657.501.985,85** (863.661 negócios; 20/20 pregões) | 28/11/2008 ¹ | NC |
| **PIBB11** | It Now PIBB IBrX-50 Fundo de Índice | Itaú Unibanco Asset | IBrX-50 | **0,059%** ² | NC ² | CVM: R$ 969.009.270,32 (20/08) | **R$ 2.538.704,42** (1.614 negócios) | NC | NC |
| **BOVV11** | It Now Ibovespa Fundo de Índice | Itaú Unibanco Asset | Ibovespa | **NC** ³ | NC | CVM: R$ 7.660.408.131,40 (20/08) | **R$ 107.957.108,17** (82.066 negócios) | NC | NC |
| **BOVB11** | ETF BRA IBOV (nome COTAHIST) | NC | Ibovespa | NC | NC | NC | **R$ 7.284.533,10** (4.167 negócios) | NC | NC |
| **SMAL11** | iShares BM&FBOVESPA Small Cap Fundo de Índice | BlackRock Brasil | Índice BM&FBOVESPA Small Cap | **0,50%** ⁴ | NC | **R$ 1.895.137.520** (28/08/2026) ⁴ · CVM: R$ 1.873.626.145,83 (26/08) | **R$ 191.388.414,03** (615.877 negócios) | 28/11/2008 ⁴ | NC |
| **DIVO11** | It Now IDIV Fundo de Índice RL | Itaú Unibanco Asset | IDIV (B3) | **0,04%** ⁵ | **Não há** ⁵ | PL médio 3 anos R$ 1.051.300.504,98 ⁵ · CVM: R$ 2.294.904.938,70 (20/08) | **R$ 31.403.602,27** (121.227 negócios) | **31/01/2012** ⁵ | NC |
| **MATB11** | It Now IMAT | Itaú Unibanco Asset | IMAT | NC | NC | NC | **R$ 2.925.942,83** (926 negócios) | NC | NC |
| **XFIX11** | Trend IFIX-L | XP Allocation (a confirmar) | IFIX-L | NC | NC | NC | **R$ 285.912,65** (11.277 negócios) | NC | NC |
| **ISUS11** | It Now ISE | Itaú Unibanco Asset | ISE | NC | NC | NC | **R$ 33.071,50** (182 negócios; 19/20 pregões) | NC | NC |
| **GOVE11** | It Now IGCT | Itaú Unibanco Asset | IGCT | NC | NC | CVM: R$ 14.548.631,20 (20/08) | **R$ 15.122,91** (128 negócios) | NC | NC |
| **ECOO11** | iShares ECOO | BlackRock Brasil | ICO2 | NC | NC | NC | **R$ 8.144,12** (118 negócios; **só 16/20 pregões**) | NC | NC |
| *BRAX11* (extra) | iShares IBrX-Índice Brasil (IBrX-100) | BlackRock Brasil | IBrX-100 | **0,20%** ⁶ | NC | **R$ 235.458.608** (28/08/2026) ⁶ | **R$ 1.347.854,17** | 22/02/2010 ⁶ | NC |

**Sobre XFIX11:** você pediu para sinalizar se é FII de índice. No COTAHIST ele aparece com espécie `CI` e nome resumido `TREND IFIX-L`. Não consegui confirmar em fonte primária se é constituído como fundo de índice (FIIM) ou como FII. **NÃO CONFIRMADO** — e a diferença é fiscalmente enorme (FII tem isenção de rendimento para PF nas condições legais; ETF não).

**Leitura de liquidez:** ISUS11, GOVE11 e ECOO11 negociam a dezenas de milhares de reais por dia — ECOO11 ficou sem negócio em 4 dos 20 pregões. Para qualquer posição relevante, isso é um problema de execução, não um detalhe.

### Internacional listado na B3

| Ticker | Nome | Gestor | Índice | Taxa adm. | PL | Liq. méd. diária ago/26 | Início |
|---|---|---|---|---|---|---|---|
| **IVVB11** | iShares S&P 500 FI em Cotas de Fundo de Índice – Inv. no Exterior | BlackRock Brasil | **S&P 500 PTAX Brazilian Real (TR)** ⁷ | **0,23%** ⁷ | **R$ 7.740.608.821** (28/08/2026) ⁷ · CVM: R$ 7.580.780.653,89 (26/08) | **R$ 61.224.935,36** (147.628 negócios) | **28/04/2014** ⁷ |
| **SPXI11** | It Now S&P 500 (COTAHIST: IT NOW SPXI) | Itaú Unibanco Asset | S&P 500 | NC | CVM (It Now S&P500® TRN): R$ 1.738.407.843,13 (20/08) | **R$ 26.482.924,30** (11.873 negócios) | NC |
| **NASD11** | Trend ETF Nasdaq 100 | XP Vista Asset Management ⁸ | Nasdaq 100 ⁸ | **0,30%** ⁸ | CVM: R$ 1.019.565.966,42 (26/08) | **R$ 18.938.296,71** (91.949 negócios) | **21/05/2021** ⁸ (CNPJ 35.578.672/0001-63) |
| **EURP11** | — | — | — | — | — | **sem negócio à vista em todo o COTAHIST 2026** | — |
| **ACWI11** | Trend ETF Bloomberg All Countries | XP Asset | Bloomberg All Countries ⁹ | **0,30%** ⁹ ⚠ | NC | **R$ 1.999.022,96** (18.434 negócios) | **29/01/2021** ⁹ |
| **WRLD11** | Investo FTSE All-World Fundo de Índice (CVM) / "replica o VT" ¹⁰ | Investo | FTSE All-World ¹⁰ | **NC** ¹⁰ | CVM: R$ 114.447.285,53 (26/08) | **R$ 6.403.197,10** (58.513 negócios) | NC |
| **XINA11** | XPETFCHINA | XP Allocation | China | NC | NC | **R$ 1.131.037,04** (37.333 negócios) | NC |
| **ASIA11** | — | — | — | — | — | **sem negócio à vista em todo o COTAHIST 2026** | — |
| **EMER11** | — | — | — | — | — | **sem negócio à vista em todo o COTAHIST 2026** | — |
| **TECK11** | It Now TECK | Itaú Unibanco Asset | NC | NC | NC | **R$ 10.128.986,58** (29.953 negócios) | NC |
| **USTK11** | Investo USTK | Investo | NC | NC | NC | **R$ 170.866,98** (3.970 negócios) | NC |

⚠ **ACWI11 — divergência na própria fonte do gestor.** A página `xpasset.com.br/fundos/acwi11/` traz "0,30%" na ficha e, em outra seção da mesma página, "0,75% – 0,95%". Registro as duas leituras porque a fonte primária se contradiz. **Não escolha um número desses sem ler o regulamento vigente.**

**EURP11, ASIA11 e EMER11:** zero ocorrências em todo o arquivo de 2026 da B3. Ou não existem mais sob esses tickers, ou nunca negociaram no período. **Status: NÃO CONFIRMADO se foram encerrados/incorporados** — não achei documento de encerramento.

### Renda fixa

**Todos ausentes do COTAHIST à vista 2026 — ver aviso metodológico. Liquidez: NÃO OBTIDA para todos.**

| Ticker | Nome | Gestor | Índice | Taxa adm. | Perf. | PL | Início |
|---|---|---|---|---|---|---|---|
| **IMAB11** | IT NOW ID ETF IMA-B FUNDO DE ÍNDICE RL | Itaú Unibanco Asset | **IMA-B (Anbima)** ¹¹ | **0,04%** ¹¹ | **Não há** ¹¹ | PL médio 3 anos R$ 2.425.457.102,16 ¹¹ · CVM: R$ 3.589.397.916,40 (20/08) | **17/05/2019** ¹¹ (CNPJ 31.024.153/0001-00) |
| **B5P211** | IT NOW IMA-B5 P2 FUNDO DE ÍNDICE RL | Itaú Unibanco Asset | **IMA-B 5 P2 (Anbima)** ¹² | **0,04%** ¹² | **Não há** ¹² | PL médio 3 anos R$ 2.024.468.777,61 ¹² · CVM: R$ 4.001.480.704,20 (20/08) | **16/11/2020** ¹² (CNPJ 38.354.864/0001-84) |
| **IB5M11** | It Now IMA-B5+ Fundo de Índice RL | Itaú Unibanco Asset | IMA-B 5+ | NC | NC | CVM: R$ 896.355.381,60 (20/08) | NC |
| **IRFM11** | It Now IRF-M P2 Fundo de Índice RL | Itaú Unibanco Asset | IRF-M P2 | NC | NC | CVM: R$ 1.029.229.440,00 (20/08) | NC |
| **FIXA11** | **NÃO EXISTE sob esse ticker no COTAHIST 2026.** Existe **FIXX11** ("ETF FIXX"), que negociou R$ 126.357,57/dia em ago/26 (243 negócios) | NC | NC | NC | NC | NC | NC |
| **IMBB11** | — | — | — | — | — | **ausente do COTAHIST 2026** | — |
| **LFTS11** | — | — | — | — | — | **ausente do COTAHIST 2026**. Existe categoria LFT: "B-INDEX ETF TEVA LFT CURTO PRAZO", PL R$ 13.524.090.574,34 (Bradesco, CVM) | — |
| **IDKA11** | — | — | — | — | — | **ausente do COTAHIST 2026** | — |

### Cripto

| Ticker | Nome | Gestor | Índice | Taxa adm. | PL | Liq. méd. diária ago/26 | Início |
|---|---|---|---|---|---|---|---|
| **HASH11** | Hashdex Nasdaq CME Crypto Index FI | Hashdex | **Nasdaq CME Crypto Index (NCI)** ¹³ | **0,3% a.a.; "taxa máxima global incluindo fundo alvo: 1,3% a.a."** ¹³ | **R$ 2.664.133.118,1** (28/08/2026) ¹³ · CVM: R$ 2.668.358.171,70 (26/08) | **R$ 13.117.564,44** (80.850 negócios) | **22/04/2021** ¹³ |
| **BITH11** | Hashdex Nasdaq Bitcoin Reference Price | Hashdex | Nasdaq Bitcoin Ref. Price | NC | CVM: R$ 1.407.592.725,40 (26/08) | **R$ 7.706.760,94** (54.237 negócios) | NC |
| **ETHE11** | Hashdex Nasdaq Ethereum Reference Price | Hashdex | Nasdaq Ethereum Ref. Price | NC | CVM: R$ 313.048.425,98 (26/08) | **R$ 6.215.699,23** (31.843 negócios) | NC |
| **QBTC11** | QR Bitcoin | QR Asset | Bitcoin | NC | NC | **R$ 3.184.155,18** (29.132 negócios) | NC |
| **QETH11** | QR Ether | QR Asset | Ether | NC | NC | **R$ 457.632,11** (6.036 negócios) | NC |
| **BITI11** | ETF Galaxy B (COTAHIST) | NC | Bitcoin | NC | NC | **R$ 563.880,54** (1.536 negócios) | NC |

> ⚠ **HASH11 — a taxa que importa é 1,3%, não 0,3%.** O próprio gestor declara "taxa máxima global incluindo fundo alvo: 1,3% a.a.". A taxa de 0,3% é só a camada brasileira; o fundo investe num veículo alvo que cobra por cima. Comparar 0,3% do HASH11 com 0,10% do BOVA11 é comparar coisas diferentes.

---

## 5. O SEGMENTO DE "ETF DE RENDA" (distribuição periódica)

Levantei todos os ETFs em funcionamento normal cujo nome contém RENDA / RENDIMENTO / INCOME / DIVIDEND / MENSAL. Fonte: CVM, 31/08/2026. Liquidez: COTAHIST ago/2026.

| Fundo | Ticker | Gestor | PL (R$) | Início (CVM) | Liq. méd. diária ago/26 |
|---|---|---|---|---|---|
| BUENA VISTA NEOS BITCOIN HIGH INCOME INDEX | NC | Buena Vista | 401.690.515,10 | 31/10/2024 | NC |
| BUENA VISTA US HIGH INCOME ETF (NEOS U.S. Equity High Income) | **SPYI11** | Buena Vista | 277.825.118,41 | 29/04/2024 | **R$ 1.593.974,69** (9.283 neg.) |
| IT NOW IDIV RENDA DIVIDENDOS | **DIVD11** (a confirmar) | Itaú Unibanco Asset | 175.098.228,52 | 13/03/2024 | **R$ 1.145.331,33** (14.126 neg.) |
| BUENA VISTA NASDAQ-100 NEOS HIGH INCOME (NDXHIEN) | **QQQI11** | Buena Vista | 171.990.133,54 | 22/04/2024 | **R$ 1.559.623,43** (9.879 neg.) |
| NU RENDA IBOV SMART DIVIDENDOS | **NDIV11** | Nu Asset | 146.631.103,04 | 10/06/2025 | **R$ 1.072.614,83** (9.740 neg.) |
| BB ETF RENDA FIXA PRÉ ÍNDICE FUTURO DE JUROS S&P/B3 | NC | BB Gestão | 121.473.150,85 | 30/06/2025 | NC |
| NU IBOV SMART DIVIDENDOS | NC | Nu Asset | 99.206.337,08 | 10/06/2025 | NC |
| **BTG PACTUAL TEVA AUVP RENDA AUTOMÁTICA ITBR IPCA RENDIMENTO** | **AREA11** | BTG Pactual Asset | **70.514.910,35** (26/08/2026) | **05/09/2025** | **ausente do COTAHIST à vista** |
| BUENA VISTA DEX VETTAFI NEOS BOOSTED BITCOIN HIGH INCOME | NC | Buena Vista | 52.051.256,64 | 10/03/2026 | NC |
| BUENA VISTA DEX VETTAFI NEOS ETHEREUM HIGH INCOME | NC | Buena Vista | 51.675.939,78 | 26/11/2025 | NC |
| BUENA VISTA NEOS GOLD HIGH INCOME INDEX | NC | Buena Vista | 44.718.287,35 | 13/08/2025 | NC |
| BUENA VISTA NEOS REAL ESTATE HIGH INCOME BR | NC | Buena Vista | 24.061.049,47 | 26/02/2025 | NC |
| BUENA VISTA NEOS RUSSELL 2000 HIGH INCOME | NC | Buena Vista | 21.420.452,74 | 31/10/2024 | NC |
| BUENA VISTA DEX NEOS INTERNATIONAL HIGH INCOME | **GDIV11** | Buena Vista | 9.032.081,30 | 15/10/2025 | **R$ 73.919,84** (1.278 neg.) |
| BUENA VISTA NEOS ENHANCED INCOME 1-3 MONTH T-BILL BR | NC | Buena Vista | 8.512.979,57 | 07/03/2025 | NC |
| BUENA VISTA DEX VETTAFI NEOS MULTI HIGH INCOME | NC | Buena Vista | 6.650.740,08 | 30/03/2026 | NC |
| BUENA VISTA DEX VETTAFI NEOS BOOSTED S&P 500 HIGH INCOME | NC | Buena Vista | 6.538.007,84 | 10/03/2025 | NC |
| BB ETF S&P DIVIDENDOS BRASIL | **BBSD11** | BB Gestão | 6.516.061,07 | 29/04/2025 | **R$ 17.186,17** (129 neg.) |
| BUENA VISTA DEX VETTAFI NEOS ENERGY INFRASTRUCTURE HIGH INCOME | NC | Buena Vista | 5.811.452,70 | 12/01/2026 | NC |
| BTG PACTUAL TEVA DIVIDENDOS ATIVOS REAIS LISTADOS | NC | BTG Pactual Asset | **0,00** (31/07/2026) | 29/08/2024 | NC |

*(Também negocia: **AUVP11** "BTGTEVA AUVP", R$ 1.268.016,33/dia, 10.139 negócios — não capturado pela busca por palavra-chave.)*

### AREA11 — ficha detalhada

Fonte primária do parceiro/gestor: `https://analitica.auvp.com.br/campanhas/area11` (acesso 31/08/2026); PL e razão social pela CVM.

- **Nome:** BTG Pactual Teva AUVP Renda Automática ITBR IPCA Rendimento Fundo de Índice
- **Gestor:** BTG Pactual Asset Management
- **Índice:** ITBR-IPCA Rendimento Mensal
- **Taxa de administração: 0,30%**
- **Distribuição: mensal**
- **Origem do rendimento declarada:** *"Carteira diversificada de títulos públicos Tesouro IPCA+ com cupons"* — ou seja, **cupons de NTN-B, que é renda efetivamente gerada pelos ativos**, e não venda de cota. A fonte também menciona "reinvestimento de parte dos fluxos para crescimento real do patrimônio".
- **Início:** 22/09/2025 (fonte AUVP) — **divergente** de 05/09/2025 no cadastro da CVM. Registro a divergência.
- **PL: R$ 70.514.910,35** (CVM, 26/08/2026)
- **Liquidez: NÃO OBTIDA** (ausente do COTAHIST à vista)
- **Histórico: menos de 12 meses.** Não há histórico que permita avaliar aderência ao índice, tracking error ou sustentabilidade da distribuição.
- **Análise crítica independente publicada: NÃO ENCONTRADA.**

### A distinção que separa este segmento em dois

Você perguntou se o rendimento distribuído é renda gerada pelos ativos ou venda de cota/retorno de capital. **A resposta é diferente para os dois blocos, e essa é a informação mais importante desta seção:**

**Bloco 1 — AREA11 (BTG/Teva/AUVP) e os ETFs de dividendos (NDIV11, DIVD11, BBSD11):** a fonte de renda declarada é cupom de NTN-B ou dividendo de ações. É **renda efetivamente produzida pelos ativos da carteira**.

**Bloco 2 — a família Buena Vista/NEOS (13 dos 20 fundos da lista, e a maior parte do patrimônio do segmento):** a estratégia é **covered call**. O FAQ do próprio gestor (`buenavista.capital/etf-faq/`, acesso 31/08/2026) descreve "estratégia escalonada com opções de compra" e define a abordagem como Covered Call, em que "o investidor que vende opções de compra possui uma quantidade equivalente do título subjacente". O rendimento distribuído vem, portanto, de **prêmio de opções vendidas**, não de dividendos ou cupons.

Isso importa porque prêmio de opção não é renda nova: é a venda antecipada da valorização futura do ativo. Em mercado de alta, o fundo entrega o cupom e abre mão da alta — o "yield" alto convive com retorno total menor. O próprio gestor adverte, no mesmo FAQ: *"Esta classe utiliza estratégias que podem resultar em significativas perdas patrimoniais para seus cotistas"* e *"não há garantia de completa eliminação da possibilidade de perdas"*.

**O que eu NÃO consegui confirmar e você deveria exigir antes de qualquer conclusão:** se as distribuições da família Buena Vista/NEOS são classificadas, no todo ou em parte, como **retorno de capital** (devolução do principal). Não achei demonstrativo de composição da distribuição por natureza. **NÃO CONFIRMADO.** Um "yield mensal" que é parcialmente devolução do seu próprio dinheiro é indistinguível, no extrato, de um yield genuíno — e só o demonstrativo separa os dois.

**Datas de início:** a maioria desses fundos começou entre 2024 e 2026; quatro começaram em **2026** (12/01/2026, 10/03/2026, 30/03/2026). **Não há histórico relevante em nenhum deles.**

---

## (B) SEÇÃO DE TRIBUTAÇÃO — com citação legal

### B.1 — ETF de renda variável: alíquota e a isenção de R$ 20 mil

**Sua compreensão está correta, e agora está confirmada na fonte.**

**Alíquota.** IN RFB 1.585/2015, **art. 27, I**: na alienação de cotas de fundo de índice de ações, o ganho "será tributado (…) de acordo com as disposições previstas no art. 56, em operações realizadas em bolsa". O art. 56 é a seção de **ganhos líquidos em bolsa**. As alíquotas estão na Lei 11.033/2004, **art. 2º**: *"I - 20% (vinte por cento), no caso de operação day trade; II - 15% (quinze por cento), nas demais hipóteses."* O art. 2º, §1º acrescenta o IRRF de **0,005%** ("dedo-duro") nas operações que não sejam day trade.

**A isenção NÃO se aplica.** Duas fontes independentes fecham isso:

- Lei 11.033/2004, **art. 3º, I**: ficam isentos *"os ganhos líquidos auferidos por pessoa física em operações no **mercado à vista de ações** nas bolsas de valores e em operações com ouro ativo financeiro cujo valor das alienações, realizadas em cada mês, seja igual ou inferior a R$ 20.000,00"*.
- IN RFB 1.585/2015, **art. 59**: *"São isentos do imposto sobre a renda os ganhos líquidos auferidos por pessoa física em operações efetuadas: **I - com ações**, no mercado à vista de bolsas de valores ou mercado de balcão, se o total das alienações desse ativo, realizadas no mês, não exceder a R$ 20.000,00; **II - com ouro**, ativo financeiro (…); **III - com ações de pequenas e médias empresas** a que se refere o art. 66."*

A lista do art. 59 é fechada e **não inclui cota de fundo de índice**. Cota de ETF não é ação. **Logo: ETF de renda variável paga 15% sobre todo o ganho, desde o primeiro real, sem piso de isenção.**

> ⚠ **Cuidado com uma armadilha de leitura.** A IN 1.585/2015 **menciona** R$ 20.000,00 no art. 25, §1º, mas num contexto totalmente diferente: a **integralização de cotas mediante entrega de ações** (você entrega ações ao fundo e recebe cotas). Nessa operação o que está sendo alienado são **ações**, e por isso a isenção se aplica àquele evento. Isso **não** cria isenção na venda das cotas do ETF. Vi resumos secundários confundirem exatamente esses dois artigos.

**Recolhimento:** o imposto sobre ganho líquido em bolsa é apurado mensalmente e pago **pelo próprio contribuinte** via DARF até o último dia útil do mês seguinte (IN 1.585/2015, art. 56, §5º).

### B.2 — ETF de renda fixa: tabela por prazo médio, confirmada

**Sua compreensão está correta e os valores conferem.** Base legal dupla:

**Lei 13.043/2014, art. 2º** (texto literal do Planalto):
> *"Os rendimentos e ganhos de capital auferidos por cotistas de fundos de investimento cujas cotas sejam admitidas à negociação no mercado secundário administrado por bolsa de valores ou entidade do mercado de balcão organizado, cujas carteiras sejam compostas por ativos financeiros que busquem refletir as variações e rentabilidade de índices de renda fixa (Fundos de Índice de Renda Fixa) e cujos regulamentos determinem que suas carteiras sejam compostas, no mínimo, por 75% (setenta e cinco por cento) de ativos financeiros que integrem o índice de renda fixa de referência, sujeitam-se ao imposto sobre a renda às seguintes alíquotas:*
> *I - 25% (vinte e cinco por cento), no caso de (…) prazo médio de repactuação igual ou inferior a 180 (cento e oitenta) dias;*
> *II - 20% (vinte por cento), no caso de (…) prazo médio de repactuação superior a cento e oitenta dias e igual ou inferior a 720 (setecentos e vinte) dias; e*
> *III - 15% (quinze por cento), no caso de (…) prazo médio de repactuação superior a 720 (setecentos e vinte) dias."*

**IN RFB 1.585/2015, art. 28** reproduz a mesma tabela nos mesmos termos.

| Prazo médio de repactuação da carteira | Alíquota |
|---|---|
| ≤ 180 dias | **25%** |
| > 180 e ≤ 720 dias | **20%** |
| > 720 dias | **15%** |

**Retenção na fonte: SIM.** A Lei 13.043/2014, art. 4º, atribui a responsabilidade tributária a instituições ("responsáveis tributários"), e o art. 3º e seus parágrafos disciplinam o envio de custo de aquisição pela bolsa a esses responsáveis. O §4º do art. 4º traz uma consequência prática dura: *"A falta da autorização de que trata o § 2º ou a falta de comprovação do custo de aquisição (…) implicam considerar o custo de aquisição (…) igual a 0 (zero), para fins de cômputo da base de cálculo."* Ou seja: **se você transferiu custódia ou comprou por uma corretora e vendeu por outra sem autorizar o envio do custo, o IR pode ser calculado sobre o valor bruto da venda, como se o custo fosse zero.** Este é, na prática, o maior risco operacional do ETF de renda fixa.

**Mudança de faixa:** Lei 13.043/2014, art. 2º, §2º — se o prazo médio mudar de faixa, aplica-se a alíquota antiga até o dia anterior à alteração, e a nova a partir de então.

**Diferença estrutural vs. renda variável:** no ETF de RV **você** apura e recolhe (DARF mensal). No ETF de RF **a fonte retém**. São regimes operacionais distintos.

### B.3 — Come-cotas: NÃO HÁ. Confirmado na lei.

**Sua compreensão está correta.** Lei 14.754/2023, **Seção III — "Do Regime Específico dos Fundos NÃO Sujeitos à Tributação Periódica"**, **art. 18**:
> *"Quando forem enquadrados como entidades de investimento e cumprirem os demais requisitos previstos nesta Seção, ficarão sujeitos ao regime de tributação de que trata esta Seção os seguintes fundos de investimento: I - Fundo de Investimento em Participações (FIP); **II - Fundo de Investimento em Índice de Mercado (Exchange Traded Fund - ETF), com exceção dos ETFs de Renda Fixa**; e III - Fundo de Investimento em Direitos Creditórios (FIDC)."*

E o **art. 24, §1º** fecha: *"Os fundos de que trata este artigo **não ficarão sujeitos à tributação periódica** nas datas previstas no inciso I do caput do art. 17 desta Lei"* — o inciso I do art. 17 é justamente o come-cotas de maio e novembro.

O art. 24, caput, define a alíquota desses fundos: *"ficarão sujeitos à retenção na fonte do IRRF à alíquota de 15% (quinze por cento), na data da distribuição de rendimentos, da amortização ou do resgate de cotas."*

**E os ETFs de renda fixa?** Estão **fora da Lei 14.754 inteira**: art. 39, VII exclui *"os ETFs de Renda Fixa de que trata o art. 2º da Lei nº 13.043, de 13 de novembro de 2014"*. Eles continuam sob a Lei 13.043/2014. **Também não têm come-cotas.**

**Conclusão: nenhuma categoria de ETF na B3 tem come-cotas.** ETF de RV: sem tributação periódica por força do art. 24, §1º. ETF de RF: fora do escopo da lei que criou a regra.

> **Nota de vigência:** os dispositivos da Lei 14.754/2023 e da Lei 11.033/2004 citados trazem, no texto do Planalto, a anotação *"(Vide Medida Provisória nº 1.303, de 2025) — Produção de efeitos — Vigência encerrada"*. Ou seja, a MP 1.303/2025 tentou alterar esse regime e **perdeu a vigência**; o texto legal citado é o que vale. Se você vir análises de 2025 com alíquotas diferentes, provavelmente estão baseadas nessa MP que caducou.

### B.4 — Distribuição de rendimentos por ETF

Quando um ETF distribui rendimento, incide **IRRF de 15% na data da distribuição**, por força da Lei 14.754/2023, **art. 24**: *"na data da distribuição de rendimentos, da amortização ou do resgate de cotas."*

**Isso não muda em 2026 com a nova tributação de dividendos.** A Lei 15.270/2025 criou o art. 6º-A:
> *"A partir do mês de janeiro do ano-calendário de 2026, o pagamento, o creditamento, o emprego ou a entrega de **lucros e dividendos por uma mesma pessoa jurídica a uma mesma pessoa física** residente no Brasil em montante superior a R$ 50.000,00 (cinquenta mil reais) em um mesmo mês fica sujeito à retenção na fonte do Imposto sobre a Renda das Pessoas Físicas à alíquota de 10% (dez por cento) sobre o total do valor pago."* (art. 8º: *"produzirá efeitos a partir de 1º de janeiro de 2026"*.)

O fato gerador é **lucro/dividendo pago por pessoa jurídica a pessoa física**. Distribuição de ETF é rendimento de fundo, regido pelo art. 24 da Lei 14.754/2023 — regime diferente. **Não se somam nem se substituem.**

**O efeito indireto existe, porém, e é NÃO CONFIRMADO em fonte:** os dividendos que as empresas pagam *para dentro* da carteira do ETF podem ter tratamento próprio na esfera do fundo. Não localizei fonte que trate especificamente do impacto da Lei 15.270/2025 sobre dividendos recebidos por fundos de índice. **NÃO CONFIRMADO** — e é uma pergunta legítima a fazer aos gestores.

### B.5 — ETF de cripto

Não há regime especial de cripto. HASH11, BITH11, ETHE11, QBTC11, QETH11 e BITI11 estão registrados na CVM como **FIIM** (fundo de índice) — a mesma classe de BOVA11. Enquadram-se, portanto, no **art. 18, II da Lei 14.754/2023** (ETF que não é de renda fixa) e seguem a regra geral de ETF de renda variável: **15% sobre ganho líquido em bolsa (20% day trade), sem isenção de R$ 20 mil, sem come-cotas.**

**Status: PARCIAL.** Deduzi o enquadramento a partir da classificação cadastral na CVM e do texto legal. **Não localizei manifestação da RFB específica sobre ETF de cripto.**

### B.6 — ETF internacional listado na B3 (IVVB11 etc.)

**É tratado como renda variável Brasil.** IVVB11 é um fundo brasileiro (razão social "iShares S&P 500 FI em Cotas de Fundo de Índice – Investimento No Exterior"), registrado na CVM como classe FIIM, com cotas negociadas na B3. Não é aplicação financeira no exterior do investidor: o investidor detém cota de fundo brasileiro.

Logo: **art. 18, II da Lei 14.754/2023** (ETF que não é de renda fixa) → **15% sobre ganho líquido, sem isenção de R$ 20 mil, sem come-cotas**, exatamente como BOVA11.

**Consequência prática que quase ninguém considera:** o investidor de IVVB11 **não** cai no regime de "aplicações financeiras no exterior" da Lei 14.754/2023 (que tem regras próprias) e **não** tem que declarar bem no exterior. Em compensação, não tem nenhuma isenção. **Status: PARCIAL** — o enquadramento decorre da leitura combinada da natureza jurídica e do art. 18, II; não achei manifestação da RFB tratando nominalmente de ETF brasileiro de índice estrangeiro.

---

## 4. BDRs

### Quantidade

| Métrica | Valor | Fonte | Status |
|---|---|---|---|
| **BDRs distintos que efetivamente negociaram em ago/2026** | **933** | Cálculo meu sobre COTAHIST_A2026 (espécies DRN/DRE/DR1/DR2/DR3, mercado à vista, 20 pregões) | COMPLETO |
| Quebra por espécie (linhas-pregão) | DRN 8.433 · DRE 2.450 · DR1 108 · DR2 40 · DR3 40 | idem | COMPLETO |
| Quebra por sufixo de ticker | **34**: 705 · **39**: 215 · **31**: 8 · **33**: 2 · **32**: 2 · **35**: 1 | idem | COMPLETO |
| BDRs listados (relatório da B3) | *"quase 850 ativos listados"* (835 em 2025) | B3, Relatório Anual de BDRs 2025 | COMPLETO — **mas referente a 2025** |
| Volume diário médio (ADTV) | **R$ 985 milhões** (out/2025) | idem | COMPLETO — out/2025 |
| Investidores | *"mais de 900 mil investidores"* (2025) | idem | COMPLETO — 2025 |
| Quebra oficial patrocinado × não patrocinado × nível | — | B3 não quantifica no relatório | **NÃO OBTIDO** |

O número da B3 (≈850, base 2025) e o meu (933 com negócio em ago/2026) são consistentes entre si e mostram crescimento — mas medem coisas diferentes: "listados" vs. "com negócio no mês". Não os some nem os troque.

### Quem pode comprar — restrição de varejo já caiu

**Resolução CVM nº 3, de 11/08/2020**, em vigor desde **1º/09/2020** (fonte: CVM, notícia oficial). Alterou as Instruções CVM 332, 359, 480 e 555. O que mudou:
- **Antes:** BDR Nível I era restrito a **investidor qualificado**.
- **Depois:** *"Permissão para que, a depender do mercado em que os valores mobiliários lastro dos BDR Nível I sejam listados, investidores que não sejam considerados qualificados possam negociá-los."*
- Também permitiu **BDRs lastreados em cotas de fundos de índice no exterior** (BDRs de ETF), com **registro automático** para esses programas.

**Estado atual: liberado para o varejo**, com a condicionante do mercado de listagem do ativo-lastro. Não localizei norma posterior revertendo isso. **Status: COMPLETO quanto à Resolução CVM 3; PARCIAL quanto a "estado atual em ago/2026"** — não achei fonte de 2026 reconfirmando que nada mudou desde 2020.

### Tributação de BDR

**Ganho de capital: 15% (20% day trade), como bolsa.** IN RFB 1.585/2015, **art. 56, §1º, I, "a"** — a seção de ganhos líquidos em bolsa aplica-se *"na alienação de Brazilian Depositary Receipts (BDR), em bolsa"*. As alíquotas vêm da Lei 11.033/2004, art. 2º (15% / 20% day trade).

**Isenção de R$ 20 mil: NÃO HÁ.** Mesmo raciocínio do ETF: o art. 59 da IN 1.585/2015 lista apenas ações, ouro e ações de PME. BDR não é ação — é certificado de depósito — e não está na lista. Confirmação editorial da própria B3 (Bora Investir, guia de IR 2026): *"BDR não entra na regra de isenção dos R$ 20 mil (de lucro com vendas em ações), ou seja, todo lucro obtido é tributável"*.

**Dividendos de BDR: regime de rendimento do exterior, não de dividendo brasileiro.** Fonte B3/Bora Investir: os dividendos de BDRs são *"tratados como rendimentos do exterior (mesmo sendo recebidos no Brasil)"*, devem ser informados na ficha de "Rendimentos Tributáveis Recebidos de Pessoa Física e do Exterior", e *"todo recebimento de dividendos do exterior está sujeito, em regra, à tributação de 15% aqui no Brasil"*, com **carnê-leão** ao longo do ano quando houver imposto a pagar.

> ⚠ **Esta é a assimetria mais relevante entre ETF internacional e BDR.** No IVVB11 você não recebe dividendo (é acumulação) e só paga 15% quando vende. No BDR você recebe dividendo tributado como rendimento do exterior, com obrigação de carnê-leão mensal, **e** paga 15% sobre o ganho quando vende, **e** não tem isenção em nenhum dos dois. O BDR carrega uma obrigação acessória mensal que o ETF não carrega.
>
> **Status desta seção sobre dividendos: PARCIAL.** A fonte é editorial da B3, não a legislação. Não localizei o dispositivo legal específico nem Solução de Consulta da RFB tratando de dividendo via BDR. Antes de operar com valores relevantes, exija a base legal.

### Custos embutidos

**Taxa do banco depositário e spread cambial implícito: NÃO CONFIRMADO.** A página da B3 sobre BDRs de ETF não traz percentuais; afirma apenas que o investidor não paga *"custos relacionados à remessa de recursos para o Exterior"*. Não localizei tabela pública de taxa de depositário nem metodologia de conversão cambial. **Não vou estimar.** Esses custos existem e são cobrados por dentro (reduzindo o valor do provento ou do lastro), mas o número tem de vir do prospecto do programa de BDR específico.

### Risco de jurisdição — BDR vs. ação lá fora

Isto é análise, não dado; separo explicitamente do que é fonte.

Comprando **BDR**, você detém um valor mobiliário **brasileiro**, emitido por instituição depositária no Brasil, custodiado no Brasil, liquidado em reais, sob jurisdição da CVM e da lei brasileira. Você tem exposição econômica ao ativo estrangeiro mas **não** é titular da ação. Entre você e a ação existe uma camada: o depositário. Se o programa for **não patrocinado** (a maioria — 705 dos 933 tickers negociados têm sufixo 34), a empresa emissora **não participa** do programa, não tem obrigação com você, e o depositário pode **encerrar o programa** — evento em que você é liquidado, não consultado. Você tipicamente não tem direito de voto.

Comprando a **ação lá fora**, você é titular direto, sob jurisdição estrangeira, com o ativo em corretora estrangeira. Ganha direitos societários e elimina o risco do depositário. Em troca assume: risco de jurisdição estrangeira, exposição a imposto sucessório americano em caso de falecimento (para ativos situados nos EUA — **NÃO CONFIRMADO nesta pesquisa**, mencione apenas como ponto a verificar), obrigação de declarar bens no exterior, e o regime da Lei 14.754/2023 para aplicações no exterior.

**A troca real é:** BDR elimina fricção operacional e jurisdicional e adiciona risco de intermediário e ausência de direitos societários. Ação direta faz o inverso. Nenhum dos dois é "mais seguro" em abstrato — depende de qual risco você prefere carregar.

---

## 6. O QUE FALTA NO MERCADO BRASILEIRO

### Existe ETF de mercado global amplo (tipo VT/ACWI) com taxa competitiva?

Existem os produtos; a taxa **não** é competitiva.

| Produto | Taxa | Fonte |
|---|---|---|
| **ACWI11** (Trend ETF Bloomberg All Countries, XP) | **0,30%** — ⚠ a mesma página do gestor também traz "0,75% – 0,95%" | xpasset.com.br |
| **WRLD11** (Investo FTSE All-World; site do gestor diz que "replica no Brasil o ETF VT") | **NÃO CONFIRMADO** — a página do produto não publica a taxa | investoetf.com |
| **VT** (Vanguard Total World Stock, EUA) | **0,06%** | advisors.vanguard.com |
| **VWRA** (Vanguard FTSE All-World UCITS Acc, Irlanda, ISIN IE00BK5BQT80) | **0,14%** (ongoing charges, doc. de 31/07/2026) | fund-docs.vanguard.com |

**ACWI11 a 0,30% custa 5x o VT (0,06%) e mais que o dobro do VWRA (0,14%).** E a liquidez do ACWI11 em ago/2026 foi de R$ 1,999 milhão/dia — não é um instrumento para posição grande.

Registro à parte: **a Investo não publica a taxa do WRLD11 na página do produto.** Para um ETF que se vende como "o VT brasileiro", omitir a taxa de administração na página do produto é uma escolha que vale notar.

### Existe S&P 500 abaixo de 0,10% a.a.? Qual a taxa do IVVB11?

**IVVB11: 0,23% a.a.** (BlackRock, página do produto, 28/08/2026). PL R$ 7.740.608.821, início 28/04/2014, índice "S&P 500 PTAX Brazilian Real (TR)".

**Não encontrei nenhum ETF de S&P 500 na B3 abaixo de 0,10% a.a.** Não confirmei as taxas de SPXI11 (Itaú), do BTG Pactual S&P 500 nem do Investo GP ETF S&P 500 — **NÃO CONFIRMADO** para esses três, então não afirmo que 0,23% é o menor do mercado; afirmo que não achei nada abaixo de 0,10%.

### Comparação com a mesma exposição comprada lá fora

| ETF | Taxa | Fonte | Data |
|---|---|---|---|
| **IVV** (iShares Core S&P 500) | **0,03%** | ishares.com — net assets US$ 886.658.038.256, inception 15/05/2000 | 28/08/2026 |
| **VOO** (Vanguard S&P 500) | **0,03%** | advisors.vanguard.com — total net assets US$ 997,4 B | 31/08/2026 |
| **VT** (Vanguard Total World Stock) | **0,06%** | advisors.vanguard.com | 31/08/2026 |
| **VWRA** (Vanguard FTSE All-World UCITS Acc) | **0,14%** | fund-docs.vanguard.com | 31/07/2026 |
| **VTI** (Vanguard Total Stock Market) | **NÃO OBTIDO** | — | — |

**IVVB11 (0,23%) custa cerca de 7,7x o IVV/VOO (0,03%)** para a mesma exposição ao S&P 500.

**Mas o custo não é a única variável, e a comparação direta é enganosa.** O IVVB11 evita: remessa de recursos ao exterior e spread cambial de envio, declaração de bens no exterior, e o regime da Lei 14.754/2023 para aplicações no exterior. Em contrapartida, quem compra IVV lá fora tem 0,03% e enfrenta aquelas fricções. **Os 0,20 p.p. de diferença anual são o preço da conveniência jurisdicional e operacional** — se valem a pena depende do tamanho da posição e do horizonte, e essa é uma conta que você faz, não que a pesquisa faz.

Comparação doméstica que talvez seja mais útil: **BOVA11 cobra 0,10%** para Ibovespa, enquanto **SMAL11 cobra 0,50%** e **DIVO11 e IMAB11 cobram 0,04%**. A dispersão de taxa dentro da própria B3 (0,04% a 0,50%, com HASH11 a até 1,3% global) é maior do que a diferença entre Brasil e EUA no S&P 500.

---

## (C) REGISTRO DE FONTES

Todas acessadas em **31/08/2026**.

### Fontes primárias — legislação (todas COMPLETO)

| # | Fonte | URL | Status |
|---|---|---|---|
| L1 | Lei 13.043/2014 (ETF de renda fixa, art. 2º a 4º) | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l13043.htm | COMPLETO |
| L2 | Lei 11.033/2004 (ganhos líquidos em bolsa, art. 2º; isenção R$20k, art. 3º) | https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm | COMPLETO |
| L3 | Lei 14.754/2023 (come-cotas; arts. 17, 18, 22, 24, 26, 39, 40) | https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14754.htm | COMPLETO |
| L4 | Lei 15.270/2025 (IRRF 10% dividendos > R$50k/mês, art. 6º-A; vigência art. 8º) | https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15270.htm | COMPLETO |
| L5 | IN RFB 1.585/2015 (arts. 24–28 fundos de índice; art. 56 ganhos líquidos e BDR; art. 59 isenções) | https://www.normaslegais.com.br/legislacao/instrucao-normativa-1585-2015.htm | COMPLETO — ⚠ site compilador, não o portal da RFB; texto conferido contra a Lei 13.043 e bateu literalmente |

### Fontes primárias — dados oficiais

| # | Fonte | URL | Status |
|---|---|---|---|
| D1 | CVM — registro de fundos e classes (222 ETFs, PL, gestor, situação) | https://dados.cvm.gov.br/dados/FI/CAD/DADOS/registro_fundo_classe.zip | COMPLETO |
| D2 | B3 — COTAHIST_A2026 (liquidez, universo de tickers, contagem de BDRs) | https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2026.ZIP | COMPLETO |
| D3 | CVM — cadastro histórico de FI | https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv | COMPLETO — mas só continha registros CANCELADA para fundos de índice; não usado |
| D4 | B3 — Relatório Anual de BDRs 2025 | https://www.b3.com.br/data/files/5D/D3/83/92/6430B9105B12E5A9AC094EA8/Relatorio%20Anual%20BDRs%202025.pdf | PARCIAL — sem quebra por tipo/nível |
| D5 | CVM — notícia oficial sobre Resolução CVM 3/2020 (BDR e varejo) | https://www.gov.br/cvm/pt-br/assuntos/noticias/2020/cvm-atualiza-regras-de-bdr-27792b5cda4a4035a50cca8ca75c35f0 | COMPLETO |

### Fontes primárias — gestores

| # | Fonte | URL | Status |
|---|---|---|---|
| G1 ¹ | BlackRock — BOVA11 | https://www.blackrock.com/br/products/251816/ishares-ibovespa-fundo-de-ndice-fund | COMPLETO |
| G2 ⁴ | BlackRock — SMAL11 | https://www.blackrock.com/br/products/251752/ishares-bmfbovespa-small-cap-fundo-de-ndice-fund | COMPLETO |
| G3 ⁷ | BlackRock — IVVB11 | https://www.blackrock.com/br/products/251902/ishares-sp-500-fi-em-cotas-de-fundo-de-ndice-inv-no-exterior-fund | COMPLETO |
| G4 ⁶ | BlackRock — BRAX11 | https://www.blackrock.com/br/products/251817/... | COMPLETO |
| G5 ¹¹ | Itaú Asset — lâmina IMAB11 (doc. 31/07/2026) | https://assetfront.arquivosparceiros.cloud.itau.com.br/FND/ITAUIMAB64066_It_Now_ID_ETF_IMA-B.pdf | COMPLETO |
| G6 ¹² | Itaú Asset — lâmina B5P211 (doc. 31/07/2026) | https://assetfront.arquivosparceiros.cloud.itau.com.br/FND/ITAUIMA5P2070_It_Now_IMA-B5_P2.pdf | COMPLETO |
| G7 ⁵ | Itaú Asset — lâmina DIVO11 (doc. 31/07/2026) | https://assetfront.arquivosparceiros.cloud.itau.com.br/FND/ITAUCARD49295_It_Now_IDIV.pdf | COMPLETO |
| G8 ² | It Now — PIBB11 | https://www.itnow.com.br/pibb11/ | PARCIAL — taxa obtida; PL e data de início não renderizam sem JS |
| G9 ³ | It Now — BOVV11 (taxas e tributos) | https://www.itnow.com.br/bovv11/taxas-e-tributos/ e https://www.itnow.com.br/bovv11/ | **NÃO OBTIDO** — "Too many redirects" via fetch; "Access Denied" (Akamai ref. 18.c7263e17) via curl |
| G10 ⁸ | XP Asset — NASD11 | https://www.xpasset.com.br/fundos/nasd11/ | COMPLETO |
| G11 ⁹ | XP Asset — ACWI11 | https://www.xpasset.com.br/fundos/acwi11/ | PARCIAL — ⚠ taxa contraditória na própria página (0,30% vs 0,75–0,95%) |
| G12 ¹⁰ | Investo — WRLD11 | https://www.investoetf.com/etf/wrld11/ | PARCIAL — taxa **não publicada** na página do produto |
| G13 ¹³ | Hashdex — HASH11 | https://hashdex.com/pt-BR/products/hash11 | COMPLETO |
| G14 | Buena Vista — FAQ dos ETFs de high income | https://www.buenavista.capital/etf-faq/ | PARCIAL — estratégia e advertência sim; taxa não |
| G15 | AUVP Analítica — AREA11 | https://analitica.auvp.com.br/campanhas/area11 | COMPLETO — ⚠ data de início diverge da CVM |
| G16 | iShares EUA — IVV | https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf | COMPLETO |
| G17 | Vanguard — VOO | https://advisors.vanguard.com/investments/products/voo/vanguard-sp-500-etf | PARCIAL — taxa e AUM sim; inception não |
| G18 | Vanguard — VT | https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf | PARCIAL — só a taxa |
| G19 | Vanguard — VWRA (KIID) | https://fund-docs.vanguard.com/FTSE_All-World_UCITS_ETF_USD_Accumulating_9679_EU_INT_UK_EN.pdf | COMPLETO |

### Fontes B3 — editorial

| # | Fonte | URL | Status |
|---|---|---|---|
| B1 | B3 Bora Investir — guia de IR 2026 para BDRs | https://borainvestir.b3.com.br/noticias/imposto-de-renda/renda-variavel-imposto-de-renda/como-declarar-bdrs-no-imposto-de-renda-2026-veja-guia-completo-para-nao-cometer-erros/ | COMPLETO — editorial da B3, **não** é a legislação |
| B2 | B3 Bora Investir — comparador BOVA11 × IVVB11 | https://borainvestir.b3.com.br/comparador-de-etfs/BOVA11/IVVB11/ | PARCIAL — **não publica taxa de administração, PL nem data de início** |
| B3 | B3 — página de BDRs de ETF | https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/brazilian-depositary-receipts-bdrs-de-etf.htm | PARCIAL — sem custos |
| B4 | B3 — lista oficial de ETFs listados | https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/etf/renda-variavel/etfs-listados/ → https://sistemaswebb3-listados.b3.com.br/fundsListedPage/ETF | **NÃO OBTIDO** |
| B5 | B3 — página de ETF de renda fixa | https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-fixa/etf-de-renda-fixa.htm | PARCIAL — só texto conceitual |

### Agregadores

**Nenhum dado deste relatório veio de StatusInvest, Investidor10, ETFs Brasil, Mais Retorno, InfoMoney, Suno ou similares.** Esses domínios apareceram em resultados de busca e foram usados apenas para **localizar URLs de fontes primárias** (por exemplo, para descobrir o endereço da lâmina do Itaú). Nenhum número foi copiado deles.

---

## Lacunas conhecidas — o que esta pesquisa NÃO entregou

1. **Lista oficial da B3 com taxa por ETF** — NÃO OBTIDO (SPA + Cloudflare). O universo veio da CVM.
2. **Liquidez dos ETFs de renda fixa** (IMAB11, IRFM11, B5P211, IB5M11, AREA11, FIXX11 parcial) — NÃO OBTIDA; ausentes do arquivo à vista da B3.
3. **Taxa de administração de 20 dos ~26 tickers pedidos** — NÃO CONFIRMADA. Confirmadas apenas: BOVA11 0,10%, SMAL11 0,50%, IVVB11 0,23%, BRAX11 0,20%, PIBB11 0,059%, DIVO11 0,04%, IMAB11 0,04%, B5P211 0,04%, NASD11 0,30%, ACWI11 0,30%(⚠), HASH11 0,3%/1,3%, AREA11 0,30%.
4. **BOVV11** — nenhum dado do gestor obtido (site bloqueia acesso automatizado). É o 3º maior ETF do país por PL.
5. **EURP11, ASIA11, EMER11, IMBB11, LFTS11, IDKA11, FIXA11** — sem qualquer ocorrência no arquivo de 2026 da B3. Se foram encerrados ou incorporados, **não achei o documento** — NÃO CONFIRMADO.
6. **Composição das distribuições dos ETFs Buena Vista/NEOS** (quanto é prêmio de opção e quanto é retorno de capital) — NÃO CONFIRMADO. É a pergunta mais importante em aberto sobre o segmento de "ETF de renda".
7. **Custos de depositário e spread cambial em BDR** — NÃO CONFIRMADO. Não estimei.
8. **Base legal específica do dividendo de BDR** — a afirmação de 15%/carnê-leão vem de material editorial da B3, não da lei. PARCIAL.
9. **Impacto da Lei 15.270/2025 sobre dividendos recebidos dentro da carteira de um ETF** — NÃO CONFIRMADO.
10. **VTI** — taxa NÃO OBTIDA.
11. **XFIX11: é FIIM ou FII?** — NÃO CONFIRMADO. Diferença fiscal grande.

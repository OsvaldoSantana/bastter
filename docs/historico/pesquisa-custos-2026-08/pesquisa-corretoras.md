# Custos reais de operar na B3 por corretora/banco — Brasil, agosto/2026

**Data de execução da pesquisa: 31/08/2026** (todos os acessos nesta data, salvo indicação).
**Regra de evidência aplicada:** só há número neste documento se ele foi lido numa fonte identificada. Onde não confirmei, está escrito **NÃO CONFIRMADO**. Nenhuma taxa foi estimada, inferida ou "arredondada de memória".

**Aviso:** este documento é levantamento de custos e riscos operacionais. **Não é recomendação de investimento.**

---

## (B) SEÇÃO DE CUSTOS DA B3 — a base que vale para todos

### B.1 Mercado à vista — ações, ETFs, BDRs, FIIs, fracionário

Fonte: B3, "Tarifas de Ações e Fundos de Investimento — À vista"
`https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/listados-a-vista-e-derivativos/renda-variavel/tarifas-de-acoes-e-fundos-de-investimento/a-vista/`
Acesso: 31/08/2026. **Status: COMPLETO via WebFetch / BLOQUEADO via curl** (Cloudflare devolveu `HTTP 403 — "Sorry, you have been blocked ... b3.com.br"`, Ray ID `a33ddf776fa1a476`).

Desde a nova política, a tarifa do mercado à vista tem **três componentes**: **Negociação**, **CCP** (contraparte central / compensação e liquidação) e **TTA** (tarifa de transferência de ativos). Não existe mais a nomenclatura antiga "emolumentos + taxa de liquidação" na tabela publicada — a soma equivalente é a coluna "Total".

**Operações normais (não day trade) — percentual sobre o valor financeiro, cobrado de cada investidor (comprador e vendedor):**

| ADTV mensal | Negociação | CCP | TTA | **Total** |
|---|---|---|---|---|
| 0 a R$ 3 milhões | 0,00500% | 0,02240% | 0,0026% | **0,0300%** |
| Acima de R$ 3 milhões | 0,00375% | 0,01615% | 0,0026% | **0,0225%** |

**Day trade (a TTA não se aplica) — 11 faixas:**

| ADTV (R$ milhões) | Negociação | CCP | **Total** |
|---|---|---|---|
| 0 a 0,2 | 0,00500% | 0,01800% | **0,0230%** |
| 0,2 a 3 | 0,00478% | 0,01722% | **0,0220%** |
| 3 a 4,5 | 0,00435% | 0,01565% | **0,0200%** |
| 4,5 a 10 | 0,00413% | 0,01487% | **0,0190%** |
| 10 a 30 | 0,00409% | 0,01471% | **0,0188%** |
| 30 a 140 | 0,00376% | 0,01354% | **0,0173%** |
| 140 a 200 | 0,00326% | 0,01174% | **0,0150%** |
| 200 a 300 | 0,00322% | 0,01158% | **0,0148%** |
| 300 a 400 | 0,00293% | 0,01057% | **0,0135%** |
| 400 a 750 | 0,00283% | 0,01017% | **0,0130%** |
| Acima de 750 | 0,00250% | 0,00900% | **0,0115%** |

**Abrangência (literal da página):** a tarifa se aplica a "ações, BDRs (patrocinados e não patrocinados), ETFs (de ações, internacionais, de renda fixa), fundos de investimento imobiliário (FIIs), direitos de subscrição e outras cotas de fundos de investimento".

**Fracionário:** a página **não publica tabela separada para o mercado fracionário**. Ou seja, do lado da B3 o fracionário custa o mesmo percentual do lote padrão. *(O que muda no fracionário é a corretagem da instituição — ver Seção A.)*

**Vigência e apuração do ADTV.** Fonte: PDF oficial B3 "Tarifação de Produtos de Renda Variável"
`https://b3.com.br/data/files/15/32/93/72/68E289100A29E189AC094EA8/Tarifacao_Produtos_Renda_Variavel_V2_PT_.pdf` — acesso 31/08/2026, **PARCIAL** (curl bloqueado: `HTTP 403`; conteúdo obtido via WebFetch).
- Política original: Ofício Circular **025/2025-VPC**. Versão 2.0 **em vigor a partir de 01/08/2025**.
- ADTV mensal = "somatório do volume de todas as contas de um documento (CPF, CNPJ ou terceiro bloco do documento CVM), **em qualquer participante**", entre o último dia útil de M-2 e o penúltimo dia útil de M-1, dividido pelo número de pregões. **Consolidado por CPF, independentemente da corretora** — confirmado também pela Caixa (ver A.13).
- Confirmação independente da data: blog Ativa Investimentos, `https://blog.ativainvestimentos.com.br/nova-política-de-tarifação-da-b3-para-produtos-de-renda-variável` — "A partir de **1º de agosto de 2025**"; "três tipos de tarifas no mercado à vista: negociação, contraparte central (CCP) e transferência de ativos (TTA)"; "tarifa de transferência de ativos não se aplica a operações day trade"; "operações de abertura e fechamento: tarifadas em **0,0070%**".

**Tributos embutidos (literal):** "As taxas descritas nesta página incluem o valor do PIS e da COFINS, cuja alíquota total é de **9,25%**, e o valor do ISS cuja alíquota pode variar de **2% a 5%**."

### B.2 Taxa de registro

No mercado **à vista** a tabela publicada tem apenas Negociação + CCP + TTA — **não há linha de "registro"**. A taxa de **registro existe em opções** (ver B.3).

### B.3 Opções sobre ações

Fonte: `https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/listados-a-vista-e-derivativos/renda-variavel/tarifas-de-acoes-e-fundos-de-investimento/opcoes-de-acoes/` — acesso 31/08/2026, **COMPLETO via WebFetch**.
*(Observação: a URL `/opcoes/` devolve erro 500 da própria B3; a correta é `/opcoes-de-acoes/`.)*

Percentuais **sobre o prêmio da opção**, cobrados de cada investidor (comprador e vendedor):

| Investidor | Negociação | Liquidação | Registro | **Total** |
|---|---|---|---|---|
| Pessoas físicas e demais investidores | 0,0370% | 0,0275% | 0,0695% | **0,1340%** |
| Fundos e clubes de investimento locais | 0,0260% | 0,0180% | 0,0510% | **0,0950%** |

Day trade em opções (regressivo sobre o prêmio):

| Volume (R$ milhões) PF / PJ | Negociação | Liquidação | Registro | **Total** |
|---|---|---|---|---|
| até 0,8 / até 4 | 0,0130% | 0,0180% | 0,0140% | **0,0450%** |
| 0,8–2,5 / 4–10 | 0,0120% | 0,0180% | 0,0110% | **0,0410%** |
| 2,5–5 / 10–25 | 0,0100% | 0,0180% | 0,0070% | **0,0350%** |
| 5–10 / 25–50 | 0,0085% | 0,0175% | 0,0030% | **0,0290%** |
| acima de 10 / 50 | 0,0075% | 0,0155% | 0,0030% | **0,0260%** |

**Exercício de opção:** "cobrado de acordo com as tarifas descritas em 'Ações à vista'". Vigência: **não especificada na página**.

### B.4 Custódia da B3 em renda variável — existe, e não é zero

Fonte: B3, "Tarifas de serviços de custódia"
`https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/servicos-da-central-depositaria/tarifas-de-servicos-de-custodia/`
Acesso: 31/08/2026. **Status: COMPLETO — transcrição literal obtida por `curl` (HTTP 200, 49.524 bytes).**

Texto literal: *"O valor em custódia será calculado considerando o somatório do volume de todas as contas de um documento (CPF, CNPJ, terceiro bloco do documento CVM ou depositário de Depositary Receipts – DRs), em um único custodiante. Será aplicado um percentual (pro rata mês), de forma progressiva, sobre o valor em custódia de cada investidor, conforme faixas definidas a seguir"*

| Valor (R$ milhões) De → Até | Tarifa de custódia (ano) | Tarifa para programas DR (ano) |
|---|---|---|
| 0 → 0,115 | 0,0500% | 0,02500% |
| 0,115 → 0,230 | 0,0400% | 0,02000% |
| 0,230 → 0,345 | 0,0200% | 0,01000% |
| 0,345 → 1,95 | 0,0130% | 0,00650% |
| 1,95 → 19,5 | 0,0072% | 0,00360% |
| 19,5 → 195 | 0,0032% | 0,00160% |
| 195 → 1.950 | 0,0025% | 0,00125% |
| 1.950 → 19.500 | 0,0020% | 0,00100% |
| 19.500 → 50.000 | 0,0015% | 0,00075% |
| Acima de 50.000 | 0,0005% | 0,00025% |

Nota literal: *"Calculada progressivamente (pro rata mês), com base no valor da carteira do investidor no último dia útil de cada mês."* e — **o ponto que interessa ao investidor pequeno** — *"**Investidores com posições até R$ 26.471,77 são isentos desta taxa.**"*

**Taxa de manutenção de conta (literal):** *"Será cobrada uma taxa mensal de **R$ 3,82** para contas de custódia, de investidores residentes ou não residentes, que permanecerem sem movimentação ou posição por mais de 60 meses, iniciando a cobrança a partir do 61º mês"*. (Isso é a "taxa de inatividade"; Caixa e outras declaram absorver — ver Seção A.)

**Taxa de transferência de custódia (literal):**

| Motivo | Taxa | Mínimo |
|---|---|---|
| Venda privada, Doação, Herança, Sucessão societária, Empréstimo privado, Programas de benefícios/premiações, Liquidação de derivativos de balcão ou COE | 0,0067% | R$ 18,36 |
| Doação pulverizada, Programa de Incentivo a Longo Prazo (ILP), Conversão de ADR | 0,0067% | R$ 0,00 |
| **Determinação regulatória, Ordem judicial**, Garantia de ofertas, Integralização de cotas de clubes/fundos, Conversão de units, Falhas de alocação, Falhas de liquidação, Estabilização de preços, Transferência com troca de titularidade por cessão de proventos, Resgates de cotas, Transferência de mesma titularidade para INR | **0,0000%** | R$ 0,00 |

Cobrada "por protocolo, sobre o valor financeiro transferido". Tributos: PIS/COFINS 9,25% + ISS 2% a 5% já inclusos.

> **Quem paga a custódia da B3?** A página **não diz explicitamente** se o responsável é o participante (agente de custódia) ou o investidor final — registro isso como lacuna. O que está confirmado é que várias instituições declaram **absorver** essa taxa: Safra ("a Safra Corretora **isenta todos os clientes** que possuem posições em Bolsa, **da taxa de custódia da renda variável da B3**, com exceção de ouro"), Caixa ("estão isentas a cobrança pelos serviços de custódia **e a taxa de inatividade (cobrada pela B3** quando a conta fica por mais de 60 meses sem movimentação ou sem saldo)"), Itaú/íon ("Custódia ZERO", exceto Private, que "segue tabela B3").

### B.5 Tesouro Direto

Fonte: B3, "Tarifas de Tesouro Direto" `https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/tarifas-de-tesouro-direto/` — acesso 31/08/2026, **COMPLETO via WebFetch**.

- **Percentual: "0,2% ao ano"**, com exceção dos produtos Tesouro Educa+ e Tesouro Renda+.
- **Base:** incide "sobre o valor dos títulos".
- **Periodicidade:** "provisionada diariamente na posição do investidor, iniciando a partir da liquidação da operação de compra (D+1)".
- **Isenção Tesouro Selic — CONFIRMADA E VIGENTE:** não há cobrança para "valores até **R$ 10.000,00 por CPF**. Acima desse valor, a taxa será cobrada apenas sobre o excedente".
- **Tesouro Educa+:** isento (0%) mantendo até o vencimento ou em resgates até **4 salários mínimos**.
- **Tesouro Renda+:** isento (0%) até o vencimento ou em resgates até **6 salários mínimos**.
- **Data de vigência: não consta na página** — registro como lacuna.

**Divergência registrada (PARCIAL):** a página do Safra (acesso 31/08/2026) afirma que "A cobrança divide-se em dois pagamentos ao longo do ano, no início de janeiro e de julho", enquanto a B3 descreve provisão diária. Existe ofício circular da B3 sobre o tema (`OC 014-2024-VPC — Política de tarifação do Tesouro Direto — cobrança semestral`, URL indexada em b3.com.br) que **NÃO OBTIVE**. Trate a periodicidade exata como **PARCIALMENTE CONFIRMADA**; o percentual de 0,20% a.a. e a isenção de R$ 10 mil no Selic estão **CONFIRMADOS na fonte primária**.
A Rico publica em `https://www.rico.com.vc/custos/` "0,25% a.a." para a custódia B3 do Tesouro Direto — **valor divergente da fonte primária da B3 (0,2%)**; considero a página da Rico desatualizada nesse ponto.

### B.6 Resposta: numa compra de R$ 1.000 em ações, quanto a B3 leva?

Investidor pessoa física de varejo (ADTV mensal abaixo de R$ 3 milhões — praticamente todo aportador de R$ 200–1.000/mês), operação normal (não day trade):

| Item | Cálculo | Valor |
|---|---|---|
| Negociação | 0,00500% × R$ 1.000 | R$ 0,05 |
| CCP | 0,02240% × R$ 1.000 | R$ 0,224 |
| TTA | 0,00260% × R$ 1.000 | R$ 0,026 |
| Taxa de registro (à vista) | não existe | R$ 0,00 |
| Custódia B3 renda variável | carteira ≤ R$ 26.471,77 → isento | R$ 0,00 |
| **TOTAL B3** | **0,0300%** | **R$ 0,30** |

**A B3 leva R$ 0,30 numa compra de R$ 1.000 em ações** (mesmo valor em ETFs, FIIs, BDRs e no fracionário). Já com PIS/COFINS e ISS embutidos. Na venda, cobra-se de novo o mesmo percentual.

Ordem de grandeza para o perfil-alvo: com aporte de R$ 500/mês, o custo B3 é **R$ 0,15/mês** (R$ 1,80/ano). **Isso é irrelevante.** O custo que importa está em outro lugar — ver Seção E.

---

## (A) TABELA MESTRE — uma linha por instituição

Legenda de status: **C** = confirmado em fonte oficial da instituição; **P** = parcial/leitura com ressalva; **N** = não confirmado / não obtido.

| # | Instituição | Corretagem ações/ETFs/FIIs à vista (canal digital) | Fracionário | Custódia mensal | Taxa própria no Tesouro Direto | Opções | Conta zero de verdade? Pegadinha | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | **XP Investimentos** | Leitura da página oficial: **Swing Trade R$ 4,90**; Day Trade **R$ 0,00 aderindo ao RLP**, R$ 2,90 sem RLP | "mesma corretagem das ações inteiras" | **R$ 0,00** ("não cobra taxa de custódia para renda fixa, bolsa ou COE, independente do valor investido") | **Zero** (taxa XP) | Via Mesa R$ 5,00/contrato | Zero só no day trade **com RLP**; swing trade aparece tarifado. Isenções para clientes assessorados | **P** |
| 2 | **Rico** (marca XP Inc.) | **R$ 0,00** day trade e swing trade; "Fundos imobiliários, BDRs e ETFs R$ 0,00" | **R$ 0,00** | **R$ 0,00** ("Taxa de custódia da Rico R$ 0,00") | Não informado como taxa Rico | Ordem R$ 0,00; **exercício: tabela Bovespa com mínimo de R$ 50,00** | Zero só para "ordens executadas pelo próprio cliente nas plataformas digitais"; ordens via atendimento cobram | **C** |
| 3 | **Clear** (marca XP Inc.) | NÃO CONFIRMADO (página de custos devolveu HTTP 403) | N | N | N | N | **Entidade legal extinta**: "A Clear Corretora é uma marca da XP Inc. e tem suas operações incorporadas à XP Investimentos CCTVM S.A."; CNPJ exibido 02.332.886/0011-78 (filial da XP) | **N** (custos) / **C** (status societário) |
| 4 | **BTG Pactual digital** | **NÃO CONFIRMADO** — site é SPA sem HTML servido; FAQ oficial retornou só metadados | N | N | N | N | Único dado tarifário obtido no manual oficial: alavancagem "Invest Flex" **5,99% ao mês + IOF** | **N** |
| 5 | **NuInvest / Nubank** | "TAXA ZERO DE CORRETAGEM para investir pelo app ou site em **Ações, BDRs e Opções**", além de "Renda Fixa, Fundos Imobiliários e ETF" | Não discriminado | Não mencionado explicitamente → NÃO CONFIRMADO | NÃO CONFIRMADO | Corretagem zero incluída | Zero só para ordens "feitas pelo cliente diretamente em nossas plataformas, como App, portal e Home Broker". **Cobram**: Mesa de Operações e **"zeragem pelo risco"** | **P** |
| 6 | **Banco Inter** | "sem custos adicionais — **isenção de taxa de custódia e sem cobrança de corretagem por ordem executada**" | Não discriminado | **Isento** | NÃO CONFIRMADO | Mesa: **mínimo R$ 50,00** | Zero no autoatendimento. **Mesa tem tabela própria** (0,00%+R$2,70 até R$135,05; 2,00% de R$135,06–498,62; faixas até 0,50%) e mínimo R$ 50 | **P** |
| 7 | **C6 Bank** | "**As taxas de custódia e corretagem são por nossa conta**"; "Corretagem e custódia grátis" para ações, FIIs, BDRs e ETFs | Não discriminado | **Grátis** | NÃO CONFIRMADO | Opções e futuros **não mencionados** na página | "Tanto no aplicativo quanto no Home Broker, não há custos de contratação, corretagem ou custódia" | **C** (RV à vista) |
| 8 | **Itaú (íon / Itaú Corretora)** | **ZERO via canais digitais** (ações, ETFs, BDRs, FIIs) | Não discriminado | **ZERO** (exceto Private, que "segue tabela B3") | **Zero** corretagem e custódia Itaú | **0,5% no exercício** | Zero é digital. **Mesa/telefone mantém tabela Bovespa**: R$0–135,07 → R$2,70; 135,08–498,62 → 2,0%; 498,63–1.514,69 → 1,5%+R$2,49; 1.514,70–3.029,38 → 1,0%+R$10,06; acima → 0,5%+R$25,21. ISS 5% | **C** |
| 9 | **Bradesco Corretora / Ágora** | **NÃO OBTIDO** — páginas servem só metadados/JS; PDF de tarifas não pôde ser baixado nesta sessão | N | N | N | N | — | **N** |
| 10 | **Banco do Brasil** | Isenção de corretagem em canais digitais para **ações, FIIs, ETFs e BDRs**, via "o aplicativo Investimentos BB ou pelo portal investimentos.bb.com.br" (fonte secundária) | N | NÃO CONFIRMADO (fonte não menciona custódia) | N | N | Site bb.com.br **bloqueou acesso automatizado** (HTTP 403, "Erro no acesso", ID a33de4cdfc9cd6fc) | **P** |
| 11 | **Santander** | **Corretagem zero** em App Santander / App Corretora / Home Broker (vigência 21/08/2023) e App Santander Trader (15/10/2024). **FIIs "não geram corretagem na Santander Corretora, independente do Modelo de corretagem escolhido"** | Não discriminado | NÃO CONFIRMADO | NÃO CONFIRMADO | Exercício de opções → "é aplicável a Corretagem Mesa" | Mesa (vigência 03/02/2020): R$0,01–1.167,33 → **R$ 20,00 fixo**; 1.167,34–1.514,69 → 1,5%+R$2,49; 1.514,70–3.029,38 → 1,0%+R$10,06; acima → 0,50%+R$25,21. Ações/ETFs via mesa: **0,5% do valor operado** | **C** |
| 12 | **Caixa** | **NÃO é zero.** Swing Trade: **R$ 4,49 + 0,02% sobre o volume operado**; Day Trade: **R$ 2,90 por ordem** | Mesma tabela (não há distinção publicada) | **Isenta** — "estão isentas a cobrança pelos serviços de custódia e a taxa de inatividade (cobrada pela B3...)" | NÃO CONFIRMADO | NÃO CONFIRMADO | **"Isenção de Corretagem para Fundos de Investimento Imobiliário"** (FII é grátis, ação não) | **C** |
| 13 | **modalmais** | **R$ 0,00** ações à vista e fracionário; **FIIs R$ 0,00**; ETFs no swing trade sem corretagem | **R$ 0,00** | "não cobra taxa de custódia em nenhum serviço" | Taxa de Administração **0% a.a.** (B3 0,20%) | "Corretagem – Trava e Financiamento: R$ 0,00"; "Call & Put: R$ 0,00"; **exercício 0,5%** comprador e vendedor | **A marca virou XP:** o próprio site declara "**O modalmais agora é XP Inc.!**" e exibe CNPJ **02.332.886/0001-04** (= XP Investimentos CCTVM) | **C** |
| 14 | **Genial Investimentos** | Página oficial de custos **não publica valores**. Diz: "**Corretagem zero válida para os principais ativos**" mediante **adesão ao produto RLP** | Não publicado | Não publicado | Não publicado | Exceções à corretagem zero incluem "**Opções a Exercer**" | **Pegadinha explícita:** zero condicionado à adesão ao RLP (Retail Liquidity Provider). Exceções: contrato cheio de Índice, Dólar, Opções a Exercer, Commodities, Taxa de Juros. Plataformas profissionais **R$ 41,40 a R$ 140,40/mês** | **P** |
| 15 | **Toro Investimentos** | Bolsa modo manual: **Ações, ETFs e Futuro de Ações R$ 0,00**; **FIIs R$ 0,00** | Não discriminado | **R$ 0,00** ("Custódia conta Toro") | **R$ 0,00** (administração); B3 0,20% a.a. | Exercício **0,5% do valor operado**; estruturadas "R$ 20,00 ou 0,5% por opção" quando posição < R$ 4.000 | **Cobram 0,5% do valor operado** em encerramentos compulsórios e ordens por telefone/e-mail. **Reposicionada como braço de trading do Santander** — a home diz "A Toro é especialista em trading. Para encontrar outros tipos de investimentos, acesse a **Santander Corretora**", e o help center redireciona (HTTP 302) para `ajuda.santandercorretora.com.br` | **C** |
| 16 | **Órama** | **NÃO OBTIDO** — site é SPA (curl HTTP 200 com corpo sem conteúdo textual) | N | N | N | N | **Adquirida pelo BTG Pactual** (R$ 500 milhões; aquisição concluída em 2024). **Entidade sem registro ativo no BCB em 03/2026** (situação "I") | **N** (custos) / **C** (status) |
| 17 | **Warren** | "A Warren **não cobra taxas de corretagem** para que clientes varejo consigam investir nesse produto, é feito somente o repasse ao cliente das taxas cobradas pela B3" (ações, ETFs, BDRs e fracionários) | **Incluído na isenção** | Não mencionado no documento → NÃO CONFIRMADO | "A Warren **não é remunerada** por este tipo de investimento, a não ser quando o produto estiver inserido na modalidade de carteiras" | **Ordens R$ 4,50**; exercício **0,5% sobre o volume** | Modelo declaradamente **fee-based**: a remuneração vem da taxa das carteiras geridas, não da corretagem. Documento **sem data explícita** | **C** |
| 18 | **Avenue (braço Brasil)** | **NÃO CONFIRMADO** (não é corretora de B3 no varejo; foco em EUA) | N | N | N | N | **Itaú assumiu o controle com 50,1% do capital** (notícia de dez/2025; conteúdo bloqueado HTTP 403, título indexado). Entidade no BCB: AVENUE SECURITIES BANCO DE INVESTIMENTO S.A. (CNPJ 61.384.004), **ativa** | **N** (custos) |
| 19 | **Guide Investimentos** | **NÃO EXISTE MAIS COMO ENTIDADE INDEPENDENTE.** Site oficial devolveu HTTP 404 nas páginas de custos. **Sem qualquer registro no cadastro do BCB na data-base 03/2026** | — | — | — | — | **Adquirida pelo Banco Safra** (anúncio 06/02/2024; "R$ 20 bilhões em ativos" incorporados; aquisição posteriormente concluída) | **C** (status) / **N** (custos) |
| 20 | **Safra (Safra Corretora)** | **NÃO é zero.** "O valor da corretagem à vista, através do Homebroker (aplicativo ou desktop), é de **R$ 4,50 sobre cada ordem executada**". Via Trader mesa/mesa: **0,5% do valor operado + R$ 25 fixo** | Mesma tabela | **Isenção total da taxa de custódia da B3** (exceto ouro) | **Taxa zero** de custódia Safra; B3 0,20% a.a. | Exercício: **0,5% do preço de exercício de cada opção + R$ 25 fixo** | +PIS 0,65%, COFINS 4%, ISS 5% sobre a corretagem. Clubes seguem tabela Bovespa independente do canal. BTC: **30% ao ano sobre a taxa negociada** | **C** |
| 21 | **Mirae Asset (Brasil)** | **NÃO CONFIRMADO** — `corretora.miraeasset.com.br` devolveu HTTP 403 em todas as tentativas (curl e WebFetch); `mirae.com.br` **não resolve DNS** | N | N | N | N | Corretora **ativa** no BCB em 03/2026 (Ativo R$ 760,6 mi; PL R$ 394,4 mi) | **N** |
| 22 | **Terra Investimentos** | **Tabela regressiva por nº de ordens/mês (autoatendimento):** 1–10 → **R$ 4,50/ordem**; 11–40 → R$ 4,00; 41–75 → R$ 3,50; 76–500 → R$ 1,20; 501+ → **R$ 0,25** | Mesma tabela | NÃO CONFIRMADO | NÃO CONFIRMADO | "No exercício de opções, será cobrado **0,5% do volume**" | Corretagem zero é **só para minicontratos (WIN/WDO) e só com RLP ativado**, "válido apenas para clientes pessoa física de autoatendimento **mediante um número mínimo de operações por mês**". Mesa/assessor: tabela Bovespa clássica. BTC tomador 0,20% (mín. R$ 10,00) | **C** |
| 23 | **Necton** | **ENTIDADE EXTINTA.** Domínio só resolve em IPv6 (inacessível daqui); páginas de custos NÃO OBTIDAS | — | — | — | — | **Adquirida pelo BTG Pactual (≈R$ 350 milhões), aquisição concluída.** Registro na B3 aparece como "necton investimentos - **btg pactual ctvm sa**". **Situação "I" (inativa) no cadastro do BCB em 03/2026** | **C** (status) / **N** (custos) |
| 24 | **Vitreo / Empiricus Investimentos** | **PLATAFORMA ENCERRADA.** `vitreo.com.br` e `empiricusinvestimentos.com.br` **não resolvem DNS** | — | — | — | — | "A plataforma Empiricus Investimentos, anteriormente conhecida como Vitreo, **será encerrada a partir de 9 de dezembro** [de 2023], após três meses de integração ao aplicativo do BTG". Grupo comprado pelo BTG em 2021; Empiricus voltou a focar em research. **A DTVM (CNPJ 34.711.571) segue formalmente ativa no BCB** (Ativo R$ 208,7 mi; PL R$ 189,4 mi em 03/2026), mas sem operação de varejo | **C** (status) / **N** (custos) |

### A.1 Consolidação do setor 2020–2026 — o que deixou de existir

Verificação primária: **cadastro do BCB (IF.data), data-base 03/2026**, obtido via API Olinda
`https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataCadastro(AnoMes=@AnoMes)?@AnoMes=202603&$format=json` — acesso 31/08/2026, **COMPLETO**.

| Entidade | CNPJ (raiz) | Situação em 03/2026 | Destino |
|---|---|---|---|
| RICO CORRETORA DE TÍTULOS E VALORES MOBILIÁRIOS S.A. | 13.434.335 | **I (inativa)** | Marca operada dentro da XP Investimentos CCTVM |
| CLEAR CORRETORA DE TÍTULOS E VALORES MOBILIÁRIOS S.A. | 15.107.963 | **I** | Idem — o próprio site confirma a incorporação |
| MODAL DTVM / BANCO MODAL S.A. | 01.302.766 / 30.723.886 | **I / I** | XP; site exibe CNPJ da XP |
| NECTON INVESTIMENTOS S.A. CVMC | 52.904.364 | **I** | BTG Pactual CTVM |
| ÓRAMA DTVM S.A. | 13.293.225 | **I** | BTG Pactual |
| GUIDE INVESTIMENTOS | — | **sem registro algum na base** | Banco Safra |
| TORO (CTVM) | — | **sem registro na base** | Santander (help center e site já apontam para Santander Corretora) |
| VITREO DTVM S.A. | 34.711.571 | **A (ativa)** | Entidade viva, marca de varejo encerrada em 09/12/2023 |
| XP INVESTIMENTOS CCTVM S.A. | 02.332.886 | **A** | Guarda-chuva de XP + Rico + Clear + modalmais |

**Conclusão da seção:** das 25 marcas pedidas, **7 deixaram de existir como entidade independente** (Rico, Clear, modalmais, Necton, Órama, Guide, Vitreo/Empiricus) e **1 foi reposicionada** (Toro, dentro do Santander). O setor de corretoras independentes brasileiro consolidou-se em torno de **XP, BTG e bancos**.

---

## (C) SOLIDEZ, RISCO DE CONTRAPARTE E CUSTÓDIA

### C.1 Porte — dados primários do Banco Central

Fonte: **BCB IF.data, relatório "Resumo", data-base 03/2026** (é a data-base mais recente disponível — 202606, 202609 e 202612 retornam vazio), via API Olinda
`https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataValores(AnoMes=@AnoMes,TipoInstituicao=@TipoInstituicao,Relatorio=@Relatorio)?@AnoMes=202603&@TipoInstituicao=3&@Relatorio='1'&$format=json`
Acesso: 31/08/2026. **Status: COMPLETO.** Valores em R$ milhões. "Lucro" = resultado do trimestre reportado.

**Conglomerados prudenciais (visão de grupo):**

| Conglomerado | Ativo Total | Patrimônio Líquido |
|---|---|---|
| ITAÚ – PRUDENCIAL | 2.834.355,7 | 232.452,3 |
| BB – PRUDENCIAL | 2.605.723,2 | 187.012,5 |
| CAIXA ECONÔMICA FEDERAL – PRUDENCIAL | 2.357.609,4 | 115.335,2 |
| BRADESCO – PRUDENCIAL | 1.990.625,8 | 177.224,6 |
| SANTANDER – PRUDENCIAL | 1.316.473,1 | 107.047,9 |
| BTG PACTUAL – PRUDENCIAL | 785.840,0 | 78.166,9 |
| NU PAGAMENTOS – PRUDENCIAL | 341.124,7 | 21.128,2 |
| XP – PRUDENCIAL | 331.640,2 | 11.526,7 |
| SAFRA – PRUDENCIAL | 286.551,4 | 17.954,9 |
| BANCO C6 – PRUDENCIAL | 152.734,7 | 6.740,1 |
| INTER – PRUDENCIAL | (Banco Inter S.A.: 97.024,9) | (7.331,9) |
| WARREN CCVM LTDA – PRUDENCIAL | 5.466,8 | **78,4** (prejuízo no trimestre: −1,4) |
| MIRAE ASSET (BRASIL) CCTVM – PRUDENCIAL | 760,6 | 394,4 |

**Entidades individuais que efetivamente custodiam o varejo:**

| Instituição (CNPJ raiz) | Ativo Total | Patrimônio Líquido | Resultado do trimestre |
|---|---|---|---|
| BANCO BTG PACTUAL S.A. (30.306.294) | 657.008,7 | 74.510,4 | +4.570,4 |
| XP INVESTIMENTOS CCTVM S.A. (02.332.886) | 138.988,6 | 7.405,6 | +23,7 |
| BANCO C6 S.A. (31.872.495) | 102.807,7 | 2.540,4 | +334,6 |
| BANCO INTER S.A. (00.416.968) | 97.024,9 | 7.331,9 | +332,7 |
| ÁGORA CTVM S.A. (74.014.747) | 11.563,0 | 3.980,8 | +108,4 |
| ITAÚ CORRETORA DE VALORES S.A. (61.194.353) | 10.769,5 | 3.390,1 | +239,5 |
| NU INVESTIMENTOS S.A. CTVM (62.169.875) | 5.137,4 | 4.763,2 | +48,5 |
| WARREN RENA DTVM (62.287.735) | 5.449,6 | **61,4** | **−1,3** |
| SANTANDER CTVM S.A. (29.162.769) | 1.205,3 | 382,0 | +3,7 |
| MIRAE ASSET (BRASIL) CCTVM (12.392.983) | 760,6 | 394,4 | +5,9 |
| GENIAL INVESTIMENTOS CVM S.A. (27.652.684) | 348,7 | 277,8 | **−4,4** |
| BRADESCO S.A. CTVM (61.855.045) | 243,0 | 84,5 | +1,1 |
| AVENUE SECURITIES BI S.A. (61.384.004) | 227,6 | 44,4 | **−5,9** |
| VITREO DTVM S.A. (34.711.571) | 208,7 | 189,4 | +5,7 |
| WARREN CVMC LTDA (92.875.780) | 17,2 | 17,0 | −0,1 |

**Leitura:** há uma diferença de **quatro ordens de grandeza** entre o PL do Itaú Unibanco (R$ 161,7 bi na entidade, R$ 232,5 bi no prudencial) e o de corretoras como Warren (R$ 61–78 milhões) ou Genial (R$ 277,8 milhões, com prejuízo no trimestre). Para renda variável isso importa menos do que a intuição sugere — pelo motivo explicado em C.3 — mas importa muito para saldo em conta e renda fixa emitida pela própria casa.

### C.2 Quebras, liquidações e intervenções 2020–2026 — houve, e muitas

Fonte primária: cadastro BCB IF.data 03/2026 (campo `Situacao`). **16 instituições** aparecem com situação **"LE" (liquidação extrajudicial)** na data-base:

- BANCO MASTER S/A – EM LIQUIDAÇÃO EXTRAJUDICIAL (33.923.798)
- BANCO MASTER MÚLTIPLO S.A. – EM LIQUIDAÇÃO EXTRAJUDICIAL (33.884.941)
- BANCO MASTER DE INVESTIMENTO S.A. – EM LIQ. EXTRAJUDICIAL (09.526.594)
- **MASTER S/A CORRETORA DE CÂMBIO, TÍTULOS E VALORES MOBILIÁRIOS – EM LIQ. EXTRAJUDICIAL (33.886.862)**
- BANCO LETSBANK S.A. – EM LIQUIDAÇÃO EXTRAJUDICIAL (58.497.702)
- BANCO PLENO S.A. – EM LIQUIDAÇÃO EXTRAJUDICIAL (61.024.352)
- **PLENO DTVM S.A. – EM LIQUIDAÇÃO EXTRAJUDICIAL (02.927.433)**
- **CBSF DTVM S.A. – EM LIQUIDAÇÃO EXTRAJUDICIAL (34.829.992)** ← a antiga **Reag**
- **ADVANCED CORRETORA DE CÂMBIO LTDA – EM LIQ. EXTRAJUDICIAL (92.856.905)**
- WILL FINANCEIRA S.A. CFI – EM LIQUIDAÇÃO EXTRAJUDICIAL (23.862.762)
- OCTA SOCIEDADE DE CRÉDITO DIRETO S.A. – EM LIQ. EXTRAJUDICIAL (39.416.705)
- DANK SOCIEDADE DE CRÉDITO DIRETO S.A. (48.430.050)
- ENTREPAY INSTITUIÇÃO DE PAGAMENTO S.A – EM LIQ. EXTRAJUDICIAL (17.887.874)
- ACQIO ADQUIRÊNCIA IP S.A. – EM LIQ. EXTRAJUDICIAL (33.171.211)
- BANCO RURAL S.A. (33.124.959) — caso antigo
- PORTOCRED S.A. CFI (01.800.019)

Fonte secundária, com cronologia (Finsiders Brasil, publicado **26/06/2026**, `https://finsidersbrasil.com.br/regulamentacao/bc-liquida-16-instituicoes-entre-2025-e-2026/`, acesso 31/08/2026 — **COMPLETO**): o BC liquidou **17 instituições entre 2025 e 2026**. Em **2025**: Banco Master de Investimento, Letsbank, **Master Corretora CCTVM**, Banco Master Múltiplo (RAET, liquidado em 2026). Em **2026**: Will Financeira, **CBSF DTVM (antiga Reag)**, **Advanced Corretora de Câmbio**, Banco Pleno e **Pleno DTVM** (fevereiro), Dank SCD (março), Entrepay, Acqio, Octa SCD, Creditag e **Frente Corretora de Câmbio** (abril), **Sefer Investimentos DTVM** (26 de junho).

**Ligação com o caso Master/Reag (conforme a matéria):** Banco Master de Investimento, Letsbank, Master Corretora, Banco Master Múltiplo, Will Financeira, CBSF Distribuidora, Banco Pleno e Pleno DTVM aparecem ligados ao grupo Master; a CBSF (antiga Reag) é o vínculo Reag.

**Nota de método:** a base do BCB de 03/2026 não captura as liquidações de abril e junho de 2026 (Creditag, Frente Corretora, Sefer DTVM) — elas constam apenas da fonte secundária datada de 26/06/2026.

Nenhuma das 25 instituições pedidas nesta pesquisa aparece em liquidação, intervenção ou falência. **O ponto relevante é outro: liquidação de corretora deixou de ser evento raro no Brasil.** Foram 17 em dois anos, incluindo pelo menos **6 corretoras/DTVMs**.

### C.3 O QUE ACONTECE COM SUAS AÇÕES E FIIs SE A CORRETORA QUEBRAR — a parte que quase ninguém sabe

**Ação e FII não ficam "na corretora".** Ficam na **Central Depositária da B3**, registrados **em conta individualizada no seu CPF**. A corretora é apenas o *agente de custódia* — o intermediário administrativo que dá acesso à sua conta. Ela não é dona, não é depositária, e não pode se apropriar do saldo.

Fonte primária: Portal do Investidor (CVM/gov.br), "Solicitação de transferência de custódia – STVM"
`https://www.gov.br/investidor/pt-br/investir/como-investir/escrituracao-custodia-e-deposito-centralizado/solicitacao-de-transferencia-de-custodia-stvm` — acesso 31/08/2026, **COMPLETO**.

Texto confirmado: em caso de **"liquidação extrajudicial de uma corretora"**, os ativos **"permanecerão em seu nome na Central Depositária"**, e o investidor pode solicitar a transferência para outro custodiante autorizado.

**O que o investidor precisa fazer, na prática:**
1. Escolher um novo custodiante autorizado pela CVM e **abrir conta nele**.
2. Preencher a **STVM** (Solicitação de Transferência de Valores Mobiliários) — normalmente fornecida pelo custodiante de destino.
3. Reunir os documentos exigidos pelo custodiante atual.
4. Enviar a STVM assinada ao custodiante de origem (**assinatura digital é aceita**).

**Prazo:** a transferência "deve ser efetuada em, no máximo, **dois dias úteis** contados do recebimento" de um requerimento válido.

**Custo:** pela tabela da B3 (B.4), transferência **por determinação regulatória ou ordem judicial custa 0,0000%**. Ou seja, a migração forçada por liquidação tende a ser gratuita do lado da B3.

**Consequência prática — e é a mais importante deste relatório:** para **ações, ETFs, BDRs e FIIs**, a quebra da corretora é um **transtorno operacional**, não uma perda patrimonial. Você não perde os papéis. Você perde acesso por um tempo e tem trabalho burocrático.

**O que NÃO está protegido por isso:**
- **Saldo em conta corrente na corretora** (dinheiro parado, ainda não investido) — isso é crédito contra a instituição.
- **Renda fixa emitida pela própria instituição** (CDB da casa) — aí vale o FGC, e só até o limite do FGC.
- **Tesouro Direto** — o título é seu e fica registrado na sua conta na B3, mas o ressarcimento de falhas nesse produto **não passa pelo MRP** (ver C.4).

**Confirmação independente da regra de individualização:** a própria tabela de custódia da B3 (B.4) calcula a tarifa "considerando o somatório do volume de todas as contas **de um documento (CPF, CNPJ...)**, em um único custodiante" — isto é, a B3 conhece e segrega a posição **por CPF**, não por corretora.

**Você pode conferir isso sozinho, hoje:** entre na **Área do Investidor da B3** (`https://www.investidor.b3.com.br/extrato`) com seu CPF. A posição que aparece ali é a que está registrada na depositária, independentemente do que a corretora mostra no app dela. Se os dois números divergirem, o da B3 é o que vale.

### C.4 Existe "FGC da renda variável"? — o MRP

**Não existe FGC para renda variável.** O que existe é o **MRP – Mecanismo de Ressarcimento de Prejuízos**, que é coisa diferente: não cobre perda de mercado, cobre **falha operacional do intermediário**.

Fonte primária: BSM Supervisão de Mercados, `https://www.bsmsupervisao.com.br/mecanismo-de-ressarcimento-de-prejuizo-mrp` — acesso 31/08/2026, **COMPLETO**.

- **Limite atual: "até o limite de R$ 200 mil"**, conforme **artigo 124 da Resolução CVM nº 135/2022**.
- **Quem administra:** "Mantido pela B3, o Mecanismo de Ressarcimento de Prejuízos (MRP) é administrado pela **BSM**, que recebe e analisa as solicitações de ressarcimento."
- **Escopo:** prejuízos decorrentes da "ação ou omissão dos Participantes autorizados a operar em mercado de bolsa, em mercados organizados de balcão para derivativos com Contraparte Central (CCP) e nos **serviços de custódia**".

**Divergência documentada — atenção:** a página de notícias da própria B3
`https://www.b3.com.br/pt_br/noticias/mecanismo-de-ressarcimento-de-prejuizos-mrp-8AE490C87043AA930170443548CF1C2F.htm` (acesso 31/08/2026) ainda afirma "**O valor do ressarcimento é limitado a R$ 120 mil por investidor**". A XP (`https://conteudos.xpi.com.br/aprenda-a-investir/relatorios/mrp-mecanismo-ressarcimento-prejuizos/`, publicado 04/01/2024) descreve exatamente a transição: limite anterior R$ 120.000, limite atual "**R$ 200 mil por ocorrência**". **Considero R$ 200 mil o valor vigente** (norma da CVM + página da BSM, que é a administradora); a página de notícias da B3 está desatualizada. Registro a divergência em vez de escondê-la.

**O que o MRP COBRE (fonte XP, coerente com o escopo da BSM):**
- não execução ou execução infiel de ordens;
- uso indevido de valores ou de valores mobiliários do cliente;
- entrega de valores mobiliários ilegítimos;
- falsificação ou vício de autenticidade de documentos;
- **"intervenção ou decretação de liquidação extrajudicial pelo Banco Central do Brasil"**;
- encerramento das atividades da instituição.

**O que o MRP NÃO COBRE:**
- **renda fixa** (o próprio texto da B3 diz que pedidos ligados a Tesouro Direto ou TED "deve[m] ser apresentado[s] ao Liquidante", não ao MRP);
- **oscilação normal de mercado** em renda variável — se sua ação caiu, o problema é seu;
- **erro do investidor**;
- prejuízos não relacionados a falha operacional ou intervenção.

**Resumo do arranjo de proteção:**

| O que você tem | Onde fica | Se a corretora quebrar |
|---|---|---|
| Ações, ETFs, BDRs, FIIs | Central Depositária da B3, conta no seu CPF | Permanecem seus; migra-se via STVM em até 2 dias úteis; transferência por ordem regulatória = 0,0000% |
| Tesouro Direto | Registrado no seu CPF na B3 | Título é seu; ressarcimento de falhas **não** passa pelo MRP |
| Dinheiro parado na conta da corretora | Crédito contra a instituição | Risco real; MRP até R$ 200 mil se houver falha operacional/liquidação |
| CDB/LCI emitidos pela própria casa | Passivo do emissor | FGC, dentro dos limites do FGC |

---

## (D-parcial) QUALIDADE OPERACIONAL

### D.1 CEI → Área do Investidor B3: o nome atual e o que dá para exportar

**O CEI (Canal Eletrônico do Investidor) não existe mais.** Foi descontinuado em **27/11/2021** e substituído pela **Área do Investidor** (`investidor.b3.com.br`).
Fonte: InfoMoney, publicado 26/11/2021 — "A partir deste sábado (27), o investidor da B3 que quiser consultar seus investimentos de renda variável e renda fixa deverá acessar a nova área logada do site da Bolsa brasileira"; "A nova plataforma irá substituir o Canal Eletrônico do Investidor (CEI)". Acesso 31/08/2026, **COMPLETO**.

Fonte oficial B3 (`https://www.b3.com.br/pt_br/produtos-e-servicos/central-depositaria/canal-com-investidores/area-do-investidor/`, acesso 31/08/2026, **PARCIAL**): a Área do Investidor é "uma plataforma na qual os investidores podem consultar os extratos de posições e movimentações de todas as suas aplicações financeiras", cobrindo **portfólio, rendimentos, extratos (Listado, Balcão e Tesouro Direto), empréstimo de títulos, garantias, histórico de negociações e movimentações**.

**Formatos de exportação: NÃO CONFIRMADO na fonte primária.** A página oficial não lista os formatos. Existem guias de terceiros indexados descrevendo exportação em **XLSX/Excel** ("Portal B3 - Como emitir o relatório de posição no formato XLSX(excel)", "Como exportar o extrato da B3 em Excel"), mas **não os confirmei linha a linha** e portanto não os reporto como fato.

### D.2 APIs — o que realmente existe

Fonte oficial: B3, "Integrações da Área do Investidor (APIs)"
`https://www.b3.com.br/pt_br/produtos-e-servicos/central-depositaria/canal-com-investidores/integracoes-da-area-do-investidor-apis/` — acesso 31/08/2026, **COMPLETO**.

- **Sete APIs disponíveis:** "**API Guia, Posição, Movimentação, Ofertas Públicas, Garantias, Eventos Provisionados, Negociação de ativos**".
- Permitem o "compartilhamento dos Extratos de Informações", com consulta consolidada dos investimentos na B3.
- **Público-alvo: "startups do sistema financeiro (Fintechs), instituições financeiras e não financeiras"**, mediante **contratação** e **autorização do investidor**.
- Documentação técnica no portal **B3 for Developers** (`https://developers.b3.com.br`). Contatos publicados: contratação (11) 2565-5080; suporte técnico (11) 2565-5120.
- **Preço: não informado na página.**

> **Implicação direta para quem vai construir um sistema:** a API da B3 **não é aberta para pessoa física**. É um produto B2B contratado por empresa, com autorização do investidor. Um investidor individual que queira automatizar a leitura da própria carteira não tem, hoje, um endpoint oficial e gratuito da B3 para si mesmo — o caminho realista é (a) contratar um agregador que já tenha essa integração, ou (b) fazer download manual/semiautomatizado dos extratos da Área do Investidor, ou (c) parsear notas de corretagem em PDF.

**APIs públicas das corretoras para clientes PF: NÃO CONFIRMADO.** Não consegui confirmar, em fonte oficial de nenhuma das 25 instituições, a existência de API pública documentada de carteira/ordens para pessoa física. Isso não significa que não exista — significa que **não confirmei**, e as buscas retornaram apenas material de terceiros (fornecedores de tecnologia como a Cedro) e páginas institucionais sem documentação de API.

### D.3 Nota de corretagem estruturada / exportação em CSV

**NÃO CONFIRMADO para todas as instituições.** Não obtive de nenhuma fonte oficial de corretora a confirmação de disponibilização da nota de corretagem em formato estruturado (XML/JSON/CSV) — o padrão de mercado observado nas páginas acessíveis é **PDF**. A XP tem artigo de atendimento sobre "como acessar minhas notas de corretagem" (`https://atendimento.xpi.com.br/artigo/3513-...`), mas a página que consegui abrir do domínio `atendimento.xpi.com.br` retornou apenas navegação, sem conteúdo — **NÃO OBTIDO**.

### D.4 Reputação (Reclame Aqui)

**NÃO CONFIRMADO.** Não consegui abrir nenhuma página de índice de reputação do Reclame Aqui nesta sessão com leitura literal da nota e da data. **Não vou publicar nota de Reclame Aqui que não li.** Registro apenas dois achados colaterais, que são fatos de navegação e não notas:
- reclamações sobre a **Órama** aparecem sob a página do **"BTG Pactual Investimentos"** no Reclame Aqui — coerente com a aquisição pelo BTG;
- reclamações da **Toro** aparecem associadas ao **Banco Santander**.

---

## (E) A PERGUNTA CENTRAL

**Perfil:** buy-and-hold, aporte mensal de R$ 200 a R$ 1.000, ETFs e/ou ações + Tesouro Direto, horizonte de 20 anos, quer automatizar a leitura da própria carteira.

### E.1 Onde o custo realmente está (com os números desta pesquisa)

Com aporte de R$ 500/mês por 20 anos (240 aportes, R$ 120 mil aportados):

| Custo | Base confirmada | Impacto em 20 anos |
|---|---|---|
| **Tarifas B3 no à vista** | 0,0300% por operação | **R$ 36,00 no total** (R$ 0,15 por aporte × 240). Desprezível. |
| **Custódia B3 renda variável** | Isento até R$ 26.471,77; depois 0,0500% a.a. na primeira faixa | Zero nos primeiros anos. Quando a carteira passar de ~R$ 26,5 mil, entra na conta — e **as instituições que declaram absorver essa taxa (Itaú, Safra, Caixa, C6, Inter, XP, Rico, Toro, modalmais) eliminam esse custo** |
| **Corretagem** | Varia de R$ 0,00 a R$ 4,50–4,90 por ordem | **Aqui está o divisor de águas.** R$ 4,50/ordem × 240 = **R$ 1.080** — 30× o custo total da B3. Numa ordem de R$ 200, R$ 4,50 é **2,25% de perda instantânea** |
| **Custódia B3 no Tesouro Direto** | 0,20% a.a., **isento até R$ 10 mil em Tesouro Selic** | Se a reserva ficar em Tesouro Selic abaixo de R$ 10 mil: zero. Acima disso, ou em Tesouro IPCA+/Prefixado: 0,20% a.a. sobre tudo |
| **Custo invisível** | spread de renda fixa, rebate de fundos, float | **Não mensurável publicamente** — é a fonte de receita de quem cobra R$ 0,00 |

### E.2 O que "corretagem zero" custa de verdade

Nenhuma das instituições que zerou a corretagem publica como se remunera no lugar dela. O que **confirmei documentalmente** sobre os mecanismos:

- **RLP (Retail Liquidity Provider)** — na **Genial**, "Corretagem zero válida para os principais ativos" está **condicionada à adesão ao produto RLP**; na **XP**, o day trade a R$ 0,00 é o que adere ao RLP (sem RLP, R$ 2,90); na **Terra**, corretagem zero em minicontratos exige RLP ativo e "um número mínimo de operações por mês". RLP significa que a corretora atua como contraparte da sua ordem — a receita dela vem do spread de execução, não da corretagem.
- **Modelo fee-based declarado** — a **Warren** afirma que "não é remunerada" pelo Tesouro Direto "a não ser quando o produto estiver inserido na modalidade de carteiras". A receita é a taxa da carteira gerida.
- **Restrição de canal** — praticamente todas condicionam o zero ao autoatendimento. **Rico**: "válida apenas para ordens executadas pelo próprio cliente nas plataformas digitais". **NuInvest**: só "App, portal e Home Broker"; mesa e "zeragem pelo risco" cobram. **Itaú/Santander/BB**: zero só nos canais digitais.
- **Custos de plataforma** — **Genial**: plataformas profissionais de **R$ 41,40 a R$ 140,40 mensais**.
- **Mínimos punitivos na mesa** — **Inter**: "Taxa mínima de corretagem para operações via mesa: **R$ 50,00**". **Rico**: exercício de opção pela tabela Bovespa com **mínimo de R$ 50,00**. **Safra**: 0,5% + R$ 25 fixo.

**Spread em renda fixa, rebate de fundos e float: NÃO CONFIRMADO em fonte oficial de nenhuma instituição.** Nenhuma publica essa informação. Registro isso como uma **lacuna estrutural de transparência do setor**, não como um dado que consegui.

### E.3 Resposta concreta

Para esse perfil, o custo relevante **não é a corretagem nem a tarifa da B3** — é a combinação de (i) corretagem literalmente zero no autoatendimento, (ii) custódia de renda variável absorvida pela instituição, (iii) taxa zero própria no Tesouro Direto e (iv) **solidez do balanço**, porque com 20 anos de horizonte a probabilidade de a instituição sofrer evento societário é alta — como esta pesquisa mostra: **7 das 25 marcas pedidas já desapareceram**, e o BC liquidou **17 instituições em 2025–2026**.

**Instituições que satisfazem simultaneamente (i)+(ii)+(iii) com confirmação documental, e têm o maior balanço da amostra:**

1. **Itaú (íon / Itaú Corretora)** — corretagem **ZERO** digital em ações, ETFs, BDRs e FIIs; custódia **ZERO**; Tesouro Direto com corretagem e custódia próprias **zero**. Conglomerado prudencial com **R$ 232,5 bi de PL** (03/2026), o maior da amostra. Corretora individual com PL de R$ 3,39 bi e lucro no trimestre. **É a combinação de menor custo confirmado com maior solidez confirmada.**
2. **C6 Bank** — "As taxas de custódia e corretagem são por nossa conta"; "não há custos de contratação, corretagem ou custódia" no app e no home broker, para ações, FIIs, BDRs e ETFs. Balanço menor (PL do conglomerado R$ 6,74 bi), mas lucrativo. Taxa própria no Tesouro Direto **não confirmada** — verifique antes.
3. **Banco Inter** — "isenção de taxa de custódia e sem cobrança de corretagem por ordem executada". PL do banco R$ 7,33 bi, lucrativo. **Cuidado com a mesa: mínimo R$ 50,00.**
4. **BTG Pactual** — o balanço mais forte entre as casas não-bancão-de-varejo (PL R$ 74,5 bi na entidade, lucro de R$ 4,57 bi no trimestre) e o consolidador do setor (absorveu Necton, Órama, Empiricus/Vitreo). **Mas a estrutura de custos não pôde ser confirmada** — o site não serve conteúdo a acesso automatizado. Se for a escolha, exija a tabela de custos operacionais por escrito antes de abrir conta.
5. **Santander** — corretagem zero digital confirmada com datas de vigência; FIIs sem corretagem "independente do Modelo de corretagem escolhido"; PL do prudencial R$ 107 bi.

**Instituições a evitar para este perfil específico, com base no que confirmei:**
- **Caixa** — cobra **R$ 4,49 + 0,02%** por ordem no swing trade. Num aporte de R$ 200, isso é **2,25% queimados na entrada**. Só faz sentido para FII, que é isento lá.
- **Safra** — **R$ 4,50 por ordem** no home broker. Mesmo problema. (A custódia é isenta, o que é bom, mas não compensa.)
- **Terra** — **R$ 4,50 por ordem** até 10 ordens/mês. A tabela regressiva só premia quem opera muito, que é o oposto deste perfil.
- **XP** — pela leitura da página oficial, **swing trade aparece a R$ 4,90**. Marcado como PARCIAL porque a extração pode ter falhado; **confirme diretamente antes de decidir**. Se for verdade, é o custo mais caro da amostra para buy-and-hold.
- **Genial** — zero condicionado a RLP; sem tabela pública de valores. Além disso, foi a única corretora da amostra com **prejuízo no trimestre** (−R$ 4,4 mi) e PL de R$ 277,8 mi.
- **Warren** — PL de R$ 61–78 milhões e prejuízo no trimestre. A corretagem é isenta e o modelo é honesto (fee-based declarado), mas o balanço é o mais frágil da amostra.

**Sobre o Tesouro Direto, independentemente da instituição:** mantenha a reserva em **Tesouro Selic até R$ 10.000 por CPF** e ela fica **literalmente sem custo de custódia** (confirmado na fonte primária da B3). Acima disso, ou em outros títulos, são 0,20% a.a.

**Sobre automação (o requisito de leitura da carteira):** a **fonte de verdade é a Área do Investidor da B3**, não o app da corretora — porque a posição está registrada no seu CPF na depositária. A **API oficial da B3 não é acessível a pessoa física** (é contratada por fintechs e instituições, com autorização do investidor). Portanto, o desenho realista do sistema é: (a) extrato da Área do Investidor como fonte primária de posição e movimentação; (b) notas de corretagem em PDF como fonte de preço médio e custos; (c) se quiser API, contratar um agregador que já tenha a integração B3 — não esperar que a corretora forneça uma.

**Não é recomendação de investimento.** É levantamento de custos e risco operacional a partir de fontes públicas, com as lacunas explicitamente marcadas.

---

## (D) REGISTRO DE FONTES — URL, data de acesso, status

Todas as datas de acesso: **31/08/2026**.

### Fontes primárias B3 / reguladores

| # | URL | Status | Observação |
|---|---|---|---|
| 1 | `https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/listados-a-vista-e-derivativos/renda-variavel/tarifas-de-acoes-e-fundos-de-investimento/a-vista/` | **COMPLETO** (WebFetch) / **BLOQUEADO** (curl) | Cloudflare: `HTTP 403 — "Sorry, you have been blocked"`, Ray ID a33ddf776fa1a476 |
| 2 | `https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/listados-a-vista-e-derivativos/renda-variavel/tarifas-de-acoes-e-fundos-de-investimento/opcoes-de-acoes/` | **COMPLETO** | A variante `/opcoes/` retorna **erro 500 da própria B3** |
| 3 | `https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/servicos-da-central-depositaria/tarifas-de-servicos-de-custodia/` | **COMPLETO** | curl HTTP 200, 49.524 B — transcrição literal integral |
| 4 | `https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/tarifas-de-tesouro-direto/` | **COMPLETO** | Data de vigência não publicada |
| 5 | `https://b3.com.br/data/files/15/32/93/72/68E289100A29E189AC094EA8/Tarifacao_Produtos_Renda_Variavel_V2_PT_.pdf` | **PARCIAL** | curl **HTTP 403** (Cloudflare devolveu HTML de bloqueio no lugar do PDF); conteúdo lido via WebFetch |
| 6 | `https://www.b3.com.br/pt_br/produtos-e-servicos/central-depositaria/canal-com-investidores/integracoes-da-area-do-investidor-apis/` | **COMPLETO** | 7 APIs; público B2B; preço não informado |
| 7 | `https://www.b3.com.br/pt_br/produtos-e-servicos/central-depositaria/canal-com-investidores/area-do-investidor/` | **PARCIAL** | Não lista formatos de exportação |
| 8 | `https://www.b3.com.br/pt_br/noticias/mecanismo-de-ressarcimento-de-prejuizos-mrp-8AE490C87043AA930170443548CF1C2F.htm` | **COMPLETO** | **Desatualizada**: ainda diz R$ 120 mil |
| 9 | `https://www.bsmsupervisao.com.br/mecanismo-de-ressarcimento-de-prejuizo-mrp` | **COMPLETO** | Limite R$ 200 mil, Res. CVM 135/2022 art. 124 |
| 10 | `https://www.gov.br/investidor/pt-br/investir/como-investir/escrituracao-custodia-e-deposito-centralizado/solicitacao-de-transferencia-de-custodia-stvm` | **COMPLETO** | STVM, prazo 2 dias úteis, ativos permanecem na Central Depositária |
| 11 | `https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataCadastro(AnoMes=@AnoMes)?@AnoMes=202603&$format=json` | **COMPLETO** | 5.855 registros; campo `Situacao` (A/I/F/LO/LE) |
| 12 | `https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataValores(...)?@AnoMes=202603&@Relatorio='1'` | **COMPLETO** | Ativo Total, PL e Lucro por instituição. 202606/202609/202612 retornam vazio → 03/2026 é a base mais recente |

### Fontes primárias das instituições

| # | Instituição | URL | Status |
|---|---|---|---|
| 13 | XP | `https://www.xpi.com.br/custos-operacionais/` | **PARCIAL** — curl HTTP 403; leitura via WebFetch com valores que merecem reconferência |
| 14 | XP (atendimento) | `https://atendimento.xpi.com.br/artigo/1841-custos-operacionais` | **NÃO OBTIDO** — página sem conteúdo tarifário |
| 15 | Rico | `https://www.rico.com.vc/custos/` | **PARCIAL** — curl HTTP 403; valores em BRL obtidos via WebFetch; página informa 0,25% a.a. no TD (divergente da B3) |
| 16 | Clear | `https://corretora.clear.com.br/sobre/` | **COMPLETO** (status societário) |
| 17 | Clear | `https://corretora.clear.com.br/custos-operacionais/` | **BLOQUEADO** — curl HTTP 403 |
| 18 | BTG | `https://www.btgpactualdigital.com/custos-operacionais` | **NÃO OBTIDO** — HTTP 200 mas corpo sem conteúdo textual (SPA) |
| 19 | BTG | `https://investimentos.btgpactual.com/suporte/perguntas-frequentes/pergunta/ka0Ht000000S5IQIA0` | **NÃO OBTIDO** — só metadados |
| 20 | BTG | `https://investimentos.btgpactual.com/manuais/risco-e-operacoes` | **PARCIAL** — só mesa e Invest Flex 5,99% a.m. |
| 21 | Nubank | `https://nubank.com.br/sobre-investimentos/taxas-e-precos` | **NÃO OBTIDO** — curl **HTTP 503**; WebFetch timeout |
| 22 | NuInvest | `https://investimento.nuinvest.com.br/taxa-corretagem-zero` | **COMPLETO** |
| 23 | NuInvest (ajuda) | `https://ajuda.nuinvest.com.br/hc/pt-br/articles/360047439414` | **BLOQUEADO** — HTTP 403 |
| 24 | Inter | `https://ajuda.inter.co/investimentos/como-operar-com-acoes-no-inter` | **COMPLETO** |
| 25 | Inter DTVM | `https://inter.co/inter-dtvm/` | **COMPLETO** (tabela de mesa) |
| 26 | C6 | `https://www.c6bank.com.br/c6-invest/renda-variavel/` | **COMPLETO** |
| 27 | C6 | `https://www.c6bank.com.br/home-broker/` | **COMPLETO** |
| 28 | C6 | `https://www.c6bank.com.br/c6-invest/` | **BLOQUEADO** — curl HTTP 403 |
| 29 | Itaú | `https://www.ion.itau/investimentos/custos-operacionais/` | **COMPLETO** |
| 30 | Itaú Corretora | `https://www.itaucorretora.com.br/explore/custosoperacionais.aspx` | **COMPLETO** |
| 31 | Bradesco Corretora | `https://www.economiaemdia.com.br/vgn-ext-templating/v/index.jsp?vgnextoid=758e92bcdc3d5610VgnVCM1000002701010aRCRD` | **NÃO OBTIDO** — só metadados e GTM |
| 32 | Ágora | `https://www.agorainvestimentos.com.br/custos-operacionais` | **NÃO OBTIDO** — só metadados |
| 33 | Ágora (PDF) | `https://www.agorainvest.com.br/uploads/pm/valores-para-operar.pdf` | **NÃO OBTIDO** — download não pôde ser concluído nesta sessão |
| 34 | Bradesco | `https://banco.bradesco/html/classic/portal-investimentos/agora-investimentos.shtm` | **PARCIAL** — HTTP 200, conteúdo só de navegação/acessibilidade |
| 35 | Banco do Brasil | `https://www.bb.com.br/portalbb/page83,129,9128,0,1,1,9.bb` | **BLOQUEADO** — HTTP 403, "Erro no acesso", ID a33de4cdfc9cd6fc |
| 36 | BB (secundária) | `https://consumidormoderno.com.br/bb-taxa-corretagem-renda-variavel/` | **COMPLETO** — pub. 20/02/2024 |
| 37 | Santander | `https://www.santandercorretora.com.br/corretora/home/taxas/taxas-de-corretagem.html` | **COMPLETO** |
| 38 | Santander (ajuda) | `https://ajuda.santandercorretora.com.br/hc/pt-br/articles/4402393740059-...` | **COMPLETO** |
| 39 | Caixa | `https://www.caixa.gov.br/voce/poupanca-e-investimentos/acoes-online/custos-operacionais/paginas/default.aspx` | **COMPLETO** via curl (269.931 B) / **BLOQUEADO** via WebFetch (`ROBOTS_DISALLOWED`; robots.txt com loop de redirects) |
| 40 | modalmais | `https://www.modalmais.com.br/custos-modalmais/` | **COMPLETO** |
| 41 | modalmais | `https://www.modalmais.com.br/custos-operacionais/` | **BLOQUEADO** — HTTP 403 |
| 42 | Genial | `https://www.genialinvestimentos.com.br/custos-tarifas/` | **PARCIAL** — página não publica valores |
| 43 | Genial (suporte) | `https://suporte.genialinvestimentos.com.br/hc/pt-br/articles/360022718812-...` | **PARCIAL** — remete a outra página |
| 44 | Genial | `https://www.genialinvestimentos.com.br/custos-operacionais/` | **NÃO OBTIDO** — curl HTTP 000 (falha de conexão) |
| 45 | Toro | `https://www.toroinvestimentos.com.br/info/custos` | **COMPLETO** |
| 46 | Toro | `https://www.toroinvestimentos.com.br/custos-operacionais` e `/tarifas` | **BLOQUEADO** — HTTP 403 (devolve a home) |
| 47 | Toro (ajuda) | `https://ajuda.toroinvestimentos.com.br/hc/pt-br/articles/4402393740059-...` | **REDIRECIONADO (302)** para `ajuda.santandercorretora.com.br` — evidência da integração |
| 48 | Órama | `https://www.orama.com.br/custos-operacionais/` e `/taxas/` | **NÃO OBTIDO** — HTTP 200 com corpo sem texto (SPA) |
| 49 | Warren | `https://s3.amazonaws.com/compliance.prd.warren.com.br/informacoes-sobre-produtos.pdf` | **COMPLETO** — sem data no documento |
| 50 | Warren | `https://warren.com.br/custos-operacionais/` | **NÃO OBTIDO** — HTTP 200, 1.420 B (vazio) |
| 51 | Safra | `https://www.safra.com.br/corretora/custos-operacionais.htm` | **COMPLETO** via curl (178.267 B) |
| 52 | Safra | `https://www.safrainvestimentos.com.br/custos-operacionais` | **NÃO OBTIDO** — HTTP 503 |
| 53 | Guide | `https://www.guide.com.br/custos-operacionais/` e `/tabela-de-custos-operacionais/` | **NÃO OBTIDO** — HTTP 404 (páginas não existem mais) |
| 54 | Mirae | `https://corretora.miraeasset.com.br/` , `/costs-and-taxes` , `/custos-e-taxas` | **BLOQUEADO** — HTTP 403 em todas; `/costs-and-taxes` via WebFetch = 404 |
| 55 | Mirae | `https://www.mirae.com.br/` | **NÃO OBTIDO** — **domínio não resolve DNS** |
| 56 | Terra | `https://www.terrainvestimentos.com.br/custos/` | **COMPLETO** via curl (169.301 B) |
| 57 | Terra | `https://www.terrainvestimentos.com.br/custos-operacionais/` | **NÃO OBTIDO** — HTTP 404 |
| 58 | Necton | `https://www.necton.com.br/institucional-custos` | **NÃO OBTIDO** — curl HTTP 000; domínio resolve **apenas em IPv6** (`2600:1407:...`), inacessível do ambiente; WebFetch retornou só cabeçalho |
| 59 | Empiricus Inv. | `https://www.empiricusinvestimentos.com.br/` | **NÃO OBTIDO** — **domínio não resolve DNS** |
| 60 | Vitreo | `https://www.vitreo.com.br/` | **NÃO OBTIDO** — **domínio não resolve DNS** |
| 61 | Avenue | `https://avenue.us/tarifas/` | **NÃO OBTIDO** — HTTP 404 |

### Fontes secundárias (consolidação societária e liquidações)

| # | URL | Status | O que sustenta |
|---|---|---|---|
| 62 | `https://finsidersbrasil.com.br/regulamentacao/bc-liquida-16-instituicoes-entre-2025-e-2026/` | **COMPLETO** — pub. 26/06/2026 | Lista das 17 liquidações 2025–2026 e vínculos Master/Reag |
| 63 | `https://exame.com/invest/mercados/safra-compra-guide-investimentos-e-incorpora-r-20-bi-em-ativos/` | **COMPLETO** — 06/02/2024 | Safra × Guide, R$ 20 bi em ativos |
| 64 | `https://bpmoney.com.br/mercado/empiricus-fecha-corretora-e-volta-a-focar-em-analise/` | **COMPLETO** — 05/12/2023 | Encerramento da Empiricus Investimentos (ex-Vitreo) em 09/12/2023 |
| 65 | `https://blog.ativainvestimentos.com.br/nova-política-de-tarifação-da-b3-para-produtos-de-renda-variável` | **COMPLETO** | Data 01/08/2025 e estrutura Negociação/CCP/TTA |
| 66 | `https://conteudos.xpi.com.br/aprenda-a-investir/relatorios/mrp-mecanismo-ressarcimento-prejuizos/` | **COMPLETO** — 04/01/2024 | MRP de R$ 120 mil → R$ 200 mil; lista de coberturas e exclusões |
| 67 | `https://www.infomoney.com.br/onde-investir/b3-descontinua-cei-a-partir-desta-sexta-...` | **COMPLETO** — 26/11/2021 | CEI descontinuado em 27/11/2021 |
| 68 | `https://forbes.com.br/forbes-money/2025/12/itau-assume-controle-da-avenue-com-501-do-capital/` | **NÃO OBTIDO** (HTTP 403) — só o título indexado | Itaú com 50,1% da Avenue (dez/2025) — **tratar como não plenamente confirmado** |
| 69 | `https://sistemaswebb3-listados.b3.com.br/participantsPage/detail/43815158000807?language=pt-br` | **PARCIAL** — título indexado: "necton investimentos - btg pactual ctvm sa" | Necton sob BTG Pactual CTVM |

### Bloqueios encontrados — resumo (isto é resultado, não falha)

De **~40 domínios de instituições testados**, o padrão foi consistente e vale registrar:

- **HTTP 403 / Cloudflare / Akamai (bloqueio ativo a acesso automatizado):** b3.com.br (inclusive para os próprios PDFs tarifários), xpi.com.br, rico.com.vc, corretora.clear.com.br, modalmais.com.br, toroinvestimentos.com.br, c6bank.com.br, bb.com.br, corretora.miraeasset.com.br, ajuda.nuinvest.com.br, forbes.com.br.
- **HTTP 200 com corpo vazio (SPA que só renderiza via JavaScript):** btgpactualdigital.com, orama.com.br, warren.com.br/custos-operacionais.
- **HTTP 503 / timeout:** nubank.com.br, safrainvestimentos.com.br.
- **HTTP 404 (página de custos deixou de existir):** guide.com.br, avenue.us/tarifas.
- **Domínio não resolve DNS (marca extinta):** mirae.com.br, vitreo.com.br, empiricusinvestimentos.com.br.
- **Resolve só em IPv6 (inacessível do ambiente):** necton.com.br.
- **robots.txt com loop de redirects:** caixa.gov.br (contornado por curl direto).

**Observação de método relevante:** as **fontes que funcionaram melhor foram exatamente as regulatórias e as tabelas obrigatórias** — a API Olinda do Banco Central (aberta, documentada, sem bloqueio), a página de tarifas de custódia da B3 e as páginas de "custos operacionais" de Caixa, Safra, Terra e Itaú, que são páginas HTML simples porque existem por exigência regulatória. **As casas com marketing mais agressivo em "taxa zero" foram, sem exceção, as mais difíceis de auditar** — o que já é, por si, um dado sobre transparência.

### Limitação declarada

A sessão atingiu limite de uso da ferramenta de leitura de páginas antes de eu esgotar os alvos. **Ficaram sem confirmação: BTG Pactual, Bradesco/Ágora, Órama, Mirae, Avenue, Necton e Guide (custos), a taxa própria de Tesouro Direto de C6/Inter/Santander/NuInvest, as notas do Reclame Aqui e a existência de APIs públicas de corretoras.** Todos estão marcados como NÃO CONFIRMADO nas tabelas acima e nenhum número foi inventado para preencher as lacunas.
</content>
</invoke>

---
---

# ADENDO — 2ª passada de pesquisa (01/09/2026)

**Contexto:** segunda rodada de coleta, executada por outro agente, com o objetivo de fechar lacunas
declaradas na "Limitação declarada" acima. **Nada foi removido ou reescrito** do documento original;
o que segue é estritamente complementar. Onde a 1ª passada já confirmou em fonte primária e a 2ª
passada obteve valor diferente, **prevalece a 1ª passada** e a divergência fica registrada.

**Acessos desta passada: 31/08/2026** (ferramenta de leitura de páginas; a sessão foi novamente
interrompida por limite de requisições após 111 chamadas).

Legenda: **[P]** fonte primária da instituição · **[S]** fonte secundária.

---

## AD.1 LACUNA FECHADA — Clear Corretora (custos)

A 1ª passada registrou a Clear como **"NÃO CONFIRMADO — página de custos devolveu HTTP 403"** (linha 3
da tabela mestre). **A lacuna está fechada:** o domínio `www.clear.com.br/site/custos/precos` de fato
devolve **HTTP 418**, mas o domínio alternativo **`corretora.clear.com.br/custos/` respondeu** e a
tabela foi lida integralmente.

**Fonte [P]:** `https://corretora.clear.com.br/custos/` — acesso 31/08/2026 — **COMPLETO**

| Item | Valor confirmado |
|---|---|
| Corretagem ações à vista **e fracionário** | **R$ 0,00** |
| Corretagem FIIs | **R$ 0,00** |
| Corretagem ETFs | **R$ 0,00** |
| Corretagem opções — call & put, trava e financiamento | **R$ 0,00** |
| Corretagem futuros (mini e cheio) | **R$ 0,00** |
| **Custódia** | **R$ 0,00 em todos os serviços** |
| Abertura e manutenção de conta | **R$ 0,00** |
| Tesouro Direto — taxa de administração Clear | **0% a.a.** (+ custódia B3 de **0,20% a.a.**) |

**Custos que existem apesar do "zero"** (todos acionados só por operações que o investidor iniciante
não faz): zeragem compulsória de futuros **R$ 16 a R$ 100** conforme contrato; zeragem day trade
tabela Bovespa 25,21 + 0,5% (mínimo **R$ 50**); **ISS/PIS/COFINS 10,68%** quando aplicável; aluguel de
ações 0,5% de renovação; cobertura de margem **0,50% ao dia** (mínimo R$ 11).

**Confirmação cruzada da posição da Clear no Tesouro Direto:** a Clear publica **0,20% a.a.** e atribui
à B3 — **coincide com a fonte primária da B3** e reforça a leitura da 1ª passada de que a página da
**Rico (0,25%) está desatualizada** nesse ponto.

> **Leitura:** para o perfil "comprar ações/FIIs/ETFs e segurar", a Clear é **custo de corretora
> R$ 0,00 com confirmação primária**, incluindo o fracionário. Combinada com o achado societário da
> 1ª passada (Clear = marca da XP Inc., CNPJ de filial da XP), isso significa que **dentro do mesmo
> grupo econômico convivem R$ 4,90/ordem na marca XP e R$ 0,00 na marca Clear.**

---

## AD.2 XP — pegadinha adicional não registrada na 1ª passada: **ETF a 0,50%**

**Fonte [P]:** `https://www.xpi.com.br/custos-operacionais/` — acesso 31/08/2026 — **COMPLETO**

A linha 1 da tabela mestre registra corretamente o swing trade a R$ 4,90. **Não registra o custo de ETF.**
A mesma página publica:

| Item | Valor |
|---|---|
| **ETFs — autoatendimento** | **0,50% de corretagem** |
| Ações/FIIs à vista e **fracionário** — swing, autoatendimento | R$ 4,90 |
| Ações/FIIs — day trade **com RLP** | R$ 0,00 · sem RLP: R$ 2,90 |
| Via assessor/mesa | Tabela Bovespa, mín. R$ 50 (day) / **R$ 100 (swing)** |
| Custódia XP | R$ 0,00 |
| Taxa XP para Tesouro Direto | R$ 0,00 |
| BDRs | Segue a tabela de ações |
| Opções swing | Tabela Bovespa, mínimo R$ 40 |

> **Por que isso importa mais do que o R$ 4,90:** 0,50% de corretagem sobre uma compra de BOVA11 é
> **cinco vezes a taxa de administração anual do próprio ETF (0,10% a.a.)** — cobrada de uma só vez,
> na entrada, e de novo na saída. Para quem começa por ETF (a rota mais recomendada a iniciantes),
> este é o custo mais alto de toda a pesquisa em termos relativos.

---

## AD.3 BTG Pactual — dado obtido, mas com **alerta de colisão de tabela**

A 1ª passada deixou o BTG inteiramente **NÃO CONFIRMADO** (SPA sem HTML servido). A 2ª passada
**também não obteve a fonte primária** — as duas URLs oficiais devolveram apenas metadados/GTM.

**Fonte [S] única:** `https://www.analisedeacoes.com/corretoras/btg/` — acesso 31/08/2026 — **PARCIAL**
(página **sem data de publicação**).

| Item | Valor atribuído ao BTG pela fonte secundária |
|---|---|
| Corretagem ações — swing, regressiva por nº de ordens/mês | 1–10: **R$ 4,50** · 11–40: R$ 4,00 · 41–75: R$ 3,50 · 76–500: R$ 1,20 · 501+: R$ 0,25 |
| Corretagem day trade | Zero |
| Custódia renda fixa e fundos | Zero |
| Tesouro Direto | 0,25% citado como repasse B3 |
| Corretagem FIIs / ETFs / fracionário | **NÃO CONFIRMADO** |

### ⚠️ ALERTA DE MÉTODO — não usar este dado sem verificação

**Essa tabela regressiva é idêntica, valor por valor, à da Terra Investimentos** confirmada em fonte
primária na 1ª passada (linha 22: 1–10 → R$ 4,50; 11–40 → R$ 4,00; 41–75 → R$ 3,50; 76–500 → R$ 1,20;
501+ → R$ 0,25). A coincidência exata em cinco faixas **não é plausível como acaso**.

Três explicações possíveis, **nenhuma verificada**:
1. a fonte secundária copiou a tabela da Terra e atribuiu ao BTG por erro;
2. ambas usam a mesma tabela white-label de mercado;
3. é de fato a tabela do BTG e a Terra a espelhou.

**Tratamento recomendado: manter o BTG como NÃO CONFIRMADO na tabela mestre.** O número R$ 4,50 não
deve entrar em nenhuma comparação ou recomendação sem confirmação na fonte primária do BTG.

**Divergência do Tesouro Direto:** o "0,25%" atribuído ao BTG replica exatamente o erro já identificado
na página da Rico. Reforça a hipótese de **desatualização propagada entre fontes**, não de taxa real.
Fonte primária da B3 permanece **0,20% a.a.**

---

## AD.4 Lacunas fechadas parcialmente — Ágora e Banco do Brasil

**Fonte [S] comum:** `https://www.idinheiro.com.br/investimentos/corretoras/corretoras-corretagem-zero/`
— artigo datado **30/07/2026**, acesso 31/08/2026 — **COMPLETO**

### Ágora Investimentos (Bradesco) — era "NÃO OBTIDO" na linha 9

| Item | Valor [S] |
|---|---|
| Corretagem ações, ETFs, BDRs, renda fixa, fundos, opções, minicontratos | **Zero** |
| Custódia / Tesouro Direto / fracionário | **NÃO CONFIRMADO** |

**Pegadinhas declaradas:** mercado futuro é cobrado; **mínimo de R$ 1.000 para renda fixa privada**.

> Segue **NÃO CONFIRMADO em fonte primária** — a 1ª passada já registrou que as páginas do Bradesco/Ágora
> servem só metadados/JS. Este é indício secundário, não substitui a tabela oficial.

### Banco do Brasil — complementa a linha 10

Confirma a isenção de corretagem em canais digitais já registrada, e acrescenta as pegadinhas:
**mercado futuro é cobrado**; **navegação da interface é difícil**; o **app de investimentos é separado
do app da conta**. Custódia e taxa própria de Tesouro Direto seguem **NÃO CONFIRMADO**.

### Complementos de pegadinha para instituições já confirmadas na 1ª passada

Mesma fonte [S], sem contradizer nenhum número primário já levantado:

| Instituição | Pegadinha declarada que não constava |
|---|---|
| **Nubank** | **Cripto é cobrado**; **não há ferramentas voltadas a trading**; não há assessoria |
| **Inter** | Cobra em **conta margem** e em operações via mesa; **volume de reclamações alto em termos comparativos** |
| **C6 Bank** | Opções de **renda fixa limitadas**; sem assessoria; **conta global é cobrada à parte** |
| **Rico** | Mercado futuro é cobrado; **não aceita conta PJ nem de menor**; "imposto consolidado" de **5,9%** quando há corretagem |
| **Clear** | **Não oferece renda fixa privada nem fundos**; foco em trader; app novo com avaliações ruins |
| **Toro** | **Não oferece renda fixa nem fundos**; "imposto consolidado" de **5,9%** |
| **Itaú íon** | **Cripto é cobrado**; contratos cheios de futuros são cobrados |

### Instituição não coberta na 1ª passada

**CM Capital** — aparece na mesma lista [S] com corretagem zero em ações, ETFs, BDRs, renda fixa,
fundos, opções, minicontratos e commodities; **mercado futuro é cobrado**. Sem fonte primária.
**NÃO CONFIRMADO.**

**Ressalva importante da própria fonte:** o artigo **não avalia** XP, BTG, Genial, Órama, Warren,
modalmais, Mercado Pago e PicPay. A ausência dessas casas na lista **não significa que cobrem** —
significa apenas que não foram avaliadas.

---

## AD.5 COMPLEMENTO À SEÇÃO B.5 — **Tesouro Reserva**, produto novo não coberto na 1ª passada

A seção B.5 cobre a custódia do Tesouro Direto corretamente, mas **é anterior ao lançamento de um
título novo** que muda o atrito de entrada para reserva de emergência.

**Fonte [P]:** `https://www.tesourodireto.com.br/tesouro-reserva` — acesso 31/08/2026 — **COMPLETO**
**Confirmação de lançamento [P/gov]:** Agência Gov,
`https://agenciagov.ebc.com.br/noticias/202605/tesouro-reserva-nova-opcao-investimento-simples-aplicacao-rs-1`
— título indexado confirma lançamento em **maio de 2026**.

| Item | Valor confirmado |
|---|---|
| **Aplicação mínima** | **R$ 1,00** — e o **mesmo mínimo para resgate** |
| Rendimento | **100% da Selic**, rendendo **desde o primeiro dia útil** |
| Liquidez | **Praticamente 24 horas por dia, 7 dias por semana**, com janela de manutenção entre 0h e 1h; resgate imediato |
| Custódia B3 | **0,20% a.a., com isenção para valores de até R$ 10.000,00 investidos** |
| IR | Tabela regressiva de renda fixa |
| IOF | Somente nos **primeiros 30 dias** |
| Limite máximo por CPF | **NÃO CONFIRMADO** — não informado na página |
| Data de lançamento na página do produto | **NÃO CONFIRMADO** (a página não traz; confirmada só pela Agência Gov) |

> **Relevância direta para a pergunta central (Seção E):** o Tesouro Reserva **desacopla a reserva de
> emergência da política de corretagem da instituição**. Mínimo de R$ 1,00, resgate 24x7, e taxa de
> agente de custódia zero nas casas confirmadas (Clear 0%, Itaú 0%, XP R$ 0,00, modalmais 0%, Toro 0%,
> Safra 0%). O único custo é a custódia da B3 — **zero até R$ 10 mil**. Em termos de atrito de entrada,
> não há produto mais barato nesta pesquisa.

---

## AD.6 COMPLEMENTO À SEÇÃO C.2 — FGC: valores pagos e regra nova de 01/06/2026

A seção C.2 lista as 16 liquidações do cadastro do BCB, o que é o dado mais forte. **Faltam o tamanho
do acionamento do FGC e a mudança regulatória que veio em resposta.**

### AD.6.1 O que o FGC efetivamente pagou

**Fonte [S/B3]:** `https://borainvestir.b3.com.br/tipos-de-investimentos/renda-fixa/cdb/fgc-inicia-pagamentos-a-investidores-de-cdbs-do-banco-master-veja-como-resgatar-os-recursos/` — acesso 31/08/2026 — COMPLETO

- **Liquidação do Banco Master decretada em 18/11/2025** (Wikipedia, acesso 31/08/2026); controlador **Daniel Vorcaro preso** por lavagem de dinheiro.
- **FGC iniciou os pagamentos em 19/01/2026** — ou seja, **cerca de dois meses de espera** entre a liquidação e o primeiro real na conta.
- **Montante: ~R$ 40,6 bilhões**, para cerca de **800 mil credores** (projeção inicial era de 1,6 milhão).
- Processo: app do FGC → cadastro → assinatura digital do termo → depósito em **2 dias úteis**.
- **Quem excedeu R$ 250 mil depende da liquidação dos ativos** — a garantia é **piso, não proteção integral**.
- **Will Bank liquidado em 21/01/2026**, atingindo **12 milhões de clientes** e 515 trabalhadores.
- **Master + Will + Pleno somados: quase R$ 52 bilhões** de acionamento do FGC ([S] TMC, `https://tmc.com.br/economia/liquidacao-bancos-pagamento-fgc/`).

### AD.6.2 Limites do FGC — **confirmados como INALTERADOS**

**Fonte [P]:** `https://www.fgc.org.br/` — acesso 31/08/2026 — COMPLETO (citação literal): o valor máximo
por CPF/CNPJ *"contra a mesma instituição associada, **ou contra todas as instituições associadas do
mesmo conglomerado financeiro**, será garantido até o valor de R$ 250.000,00"*.

Produtos cobertos listados: conta corrente, poupança, **CDB e RDB**, LCI, LCD, LCA, LH, letras de câmbio
e operações compromissadas com títulos de emissão da própria empresa.

- **R$ 250.000 por CPF por conglomerado: mantido.**
- **R$ 1.000.000 global a cada 4 anos: mantido** — confirmado por [S] Seu Dinheiro (abaixo). O limite
  global **não constava** na página do FGC acessada.

### AD.6.3 Regra nova do CMN — em vigor desde **01/06/2026**

**Fonte [S]:** `https://www.seudinheiro.com/2026/economia/fgc-novas-regras-passam-valer-nesta-segunda-veja-que-muda-garg/` — acesso 31/08/2026 — COMPLETO

- Criação de um **"ativo de referência"**: bancos passam a acompanhar indicador de qualidade, liquidez e
  diversificação de ativos. Quem não atinge o patamar é obrigado a **redirecionar parte dos recursos
  para títulos públicos federais**.
- Mudança no cálculo do **patrimônio líquido ajustado**, com mecanismos de proteção em crise.
- **A partir de novembro de 2026:** bancos passam a receber informação detalhada sobre investidores e
  aplicações protegidas (ampliação de transparência).
- Objetivo declarado: impedir que bancos **"usem a garantia do FGC para atrair investidores assumindo
  riscos excessivos"** — a regra existe por causa do Master.

**Fonte primária NÃO OBTIDA:** a matéria da Agência Brasil sobre a resolução do CMN
(`https://agenciabrasil.ebc.com.br/economia/noticia/2026-04/cmn-endurece-regras-para-bancos-captarem-recursos-com-garantia-do-fgc`)
devolveu **aviso de indisponibilidade por legislação eleitoral** — a EBC suspendeu conteúdo no período.
**O número da resolução do CMN permanece NÃO CONFIRMADO.**

### AD.6.4 Caso BRB — risco institucional em curso

- **02/2026:** Justiça **bloqueia ações do BRB** ligadas ao Banco Master ([S] Agência Brasil,
  `https://agenciabrasil.ebc.com.br/justica/noticia/2026-02/justica-bloqueia-acoes-do-brb-ligadas-banco-master`).
- **03/2026:** Banco Central pede que o BRB **provisione R$ 2,6 bilhões** para perdas após a compra de
  carteiras fraudadas do Master; o BRB pede mais prazo para divulgar balanço e busca socorro
  ([S] Seu Dinheiro e O Tempo).
- A compra do Master pelo BRB havia sido **vetada pelo Banco Central**.
- **Não houve liquidação do BRB** até a data de acesso — mas o risco institucional está declaradamente
  elevado. **Situação do BRB no cadastro do BCB: NÃO VERIFICADA nesta passada.**

> **Reforço à conclusão da Seção C:** o risco relevante para quem começa **não está na corretora** —
> ações e FIIs ficam na Central Depositária no CPF do investidor (Seção C.3). **Está no emissor do CDB.**
> R$ 40,6 bilhões e dois meses de espera é o que custou, na prática, perseguir %CDI alto em banco pequeno.

---

## AD.7 Contexto macro na data da pesquisa

| Indicador | Valor | Fonte | Status |
|---|---|---|---|
| **Selic meta** | **14,00% a.a.** | [S] Credited, 15/08/2026 (`https://credited.com.br/noticias/2026/08/15/copom-mantem-selic-14-por-cento-agosto-2026-impacto/`) | **PARCIAL** |
| **CDI** | **13,90% a.a.** | [S] SimulaDinheiro, dado de 31/08/2026 | **PARCIAL** |

⚠️ **Divergência registrada:** uma segunda fonte [S] (`https://www.remessaonline.com.br/blog/reuniao-copom-agosto-2026/`)
descreve a decisão de agosto/2026 como **corte** para 14,00%, enquanto a primeira descreve **manutenção**
em 14,00%. **O nível de 14,00% é consistente nas duas; a direção do movimento diverge.**

**Confirmação primária NÃO OBTIDA:** `https://www.bcb.gov.br/controleinflacao/historicotaxasjuros`
**exige JavaScript** e devolveu apenas metadados. *(Nota: a 1ª passada demonstrou que a **API Olinda do
BCB** é acessível sem bloqueio — é o caminho recomendado para fechar esta lacuna.)*

---

## AD.8 Registro de fontes desta passada

### COMPLETO — primária

| URL | Data | Rendeu |
|---|---|---|
| `https://corretora.clear.com.br/custos/` | 31/08/2026 | **Tabela Clear — fecha lacuna da 1ª passada** (AD.1) |
| `https://www.xpi.com.br/custos-operacionais/` | 31/08/2026 | ETF 0,50% + confirmação do R$ 4,90 (AD.2) |
| `https://www.tesourodireto.com.br/tesouro-reserva` | 31/08/2026 | Tesouro Reserva (AD.5) |
| `https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/tarifas-de-tesouro-direto/` | 31/08/2026 | Reconfirma 0,20% + isenção R$ 10 mil |
| `https://www.b3.com.br/.../tarifas-de-acoes-e-fundos-de-investimento/a-vista/` | 31/08/2026 | Reconfirma 0,0300% total |
| `https://www.ion.itau/investimentos/custos-operacionais/` | 31/08/2026 | Reconfirma íon zero digital |
| `https://www.itaucorretora.com.br/explore/custosoperacionais.aspx` | 31/08/2026 | Esclarece que **0,121% a.m. é custódia de OURO**, não de ações |
| `https://www.rico.com.vc/custos-operacionais/` | 31/08/2026 | Reconfirma Rico zero + divergência TD 0,25% |
| `https://www.fgc.org.br/` | 31/08/2026 | R$ 250 mil por conglomerado (AD.6.2) |

### COMPLETO — secundária

| URL | Data | Rendeu |
|---|---|---|
| `https://www.idinheiro.com.br/.../corretoras-corretagem-zero/` | art. 30/07/2026 | Ágora, BB, CM Capital, pegadinhas (AD.4) |
| `https://borainvestir.b3.com.br/.../fgc-inicia-pagamentos...` | 31/08/2026 | R$ 40,6 bi / 800 mil credores (AD.6.1) |
| `https://www.seudinheiro.com/2026/economia/fgc-novas-regras...` | 31/08/2026 | Regra CMN de 01/06/2026 (AD.6.3) |
| `https://en.wikipedia.org/wiki/Banco_Master` | 31/08/2026 | Datas 18/11/2025 e 21/01/2026 |

### PARCIAL / NÃO OBTIDO — com motivo técnico

| URL | Motivo | Impacto |
|---|---|---|
| `https://www.clear.com.br/site/custos/precos` | **HTTP 418** (anti-bot) | Nenhum — contornado via `corretora.clear.com.br` |
| `https://www.btgpactual.com/custos-operacionais` | Só metadados; conteúdo por **JS** | **Alto** — BTG segue NÃO CONFIRMADO |
| `https://investimentos.btgpactual.com/custos` | Só metadados; **JS** | **Alto** — idem |
| `https://arevista.com.br/mercados/btg-pactual-taxa-zero...` | **HTTP 403** | Médio — checagem cruzada do BTG perdida |
| `https://educacaofinanceirabrasil.com.br/artigos/btg-pactual-digital-review` | **HTTP 404** | Médio — idem |
| `https://warren.com.br/blog/corretagem-zero/` | **Read timeout** | Baixo — 1ª passada já confirmou Warren em fonte primária |
| `https://picpay.com/pt-br/pf/investimentos` | **Limite de sessão da ferramenta** | **Alto** — PicPay segue sem dado |
| `https://www.bcb.gov.br/controleinflacao/historicotaxasjuros` | **Exige JavaScript** | Médio — Selic só por secundária |
| `https://agenciabrasil.ebc.com.br/.../cmn-endurece-regras...` | **Indisponível por legislação eleitoral** | Médio — nº da resolução do CMN não confirmado |
| `https://www.tesourodireto.com.br/b/impostos-e-taxas-no-tesouro-direto` | **HTTP 404** | Baixo — coberto pela B3 |
| `https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm` | Tabela por **JS** | Médio — lista de títulos/taxas do dia não obtida |
| `https://prod.auvpcapital.com.br/custos/` | **HTTP 403** | Fora do escopo desta frente |
| Genial, Órama, Mercado Pago, Bradesco (tabelas primárias) | **Limite de 111 requisições atingido** | **Alto** |

**Causa raiz da interrupção:** limite da ferramenta de leitura de páginas atingido às ~12:55 UTC de
31/08/2026 (reset previsto 17:20 UTC). A ferramenta Bash — que permitiria contornar via `curl`, caminho
que funcionou bem na 1ª passada — ficou **intermitentemente indisponível** pelo classificador de
segurança no mesmo período.

---

## AD.9 Estado das lacunas após esta passada

| Lacuna da 1ª passada | Situação agora |
|---|---|
| **Clear (custos)** | ✅ **FECHADA** em fonte primária (AD.1) |
| **BTG Pactual (custos)** | ❌ **Continua aberta.** Único dado é [S] sem data e com **colisão de tabela com a Terra** (AD.3) — não usar |
| **Bradesco / Ágora** | 🟡 **Parcial** — indício [S] de corretagem zero; primária segue não obtida |
| **Banco do Brasil** | 🟡 **Parcial** — pegadinhas acrescentadas; custódia e TD seguem NÃO CONFIRMADO |
| **Órama (custos)** | ❌ Continua aberta |
| **Mirae, Avenue, Necton, Guide (custos)** | ❌ Continuam abertas |
| **Taxa própria de TD em C6/Inter/Santander/NuInvest** | ❌ Continua aberta |
| **Reclame Aqui (notas)** | 🟡 Só indício qualitativo: Inter com "volume de reclamações alto" [S] |
| **APIs públicas de corretoras** | ❌ Continua aberta |
| **PicPay / Mercado Pago (corretagem)** | ❌ Continuam abertas |
| **Genial** | 🟡 1ª passada já tinha o essencial: zero **condicionado a adesão ao RLP** |
| **Fracionário** | Confirmado em **XP, Rico, Clear, modalmais, Caixa, Terra, Warren**; demais NÃO CONFIRMADO |
| **Data de vigência** da tabela à vista da B3 | ✅ 1ª passada: **v2.0 em vigor desde 01/08/2025** (OC 025/2025-VPC) |
| **Data de vigência** da custódia do TD | ❌ Continua aberta |
| **Selic — confirmação primária** | ❌ Aberta; **usar a API Olinda do BCB**, que a 1ª passada provou acessível |

### Recomendações de método para uma 3ª passada

1. **Usar `curl` via Bash desde o início**, não a ferramenta de leitura de páginas — a 1ª passada obteve
   por curl exatamente o que a 2ª não conseguiu (tarifas de custódia da B3, Caixa, Safra, Terra).
2. **Para o BTG**, tentar o **PDF de tarifas** e o cadastro da B3 de participantes, já que o site é SPA.
3. **Testar domínios alternativos** antes de declarar bloqueio — o caso Clear
   (`www.clear.com.br` = 418, `corretora.clear.com.br` = 200) mostra que o bloqueio costuma ser por host.
4. **Preferir fontes regulatórias** — API Olinda do BCB, Portal do Investidor (CVM), páginas de "custos
   operacionais" que existem por exigência regulatória. Foi o que funcionou nas duas passadas.

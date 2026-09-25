# Investimento no exterior por pessoa física brasileira — custos e tributação

**Data da pesquisa:** 31/08/2026 (todas as consultas de rede foram feitas nesse dia, horário UTC).
**Data de referência do relatório:** agosto/2026.

**Regra de evidência aplicada:** só há número aqui se eu o vi na fonte citada. Onde não vi, está escrito
**NÃO CONFIRMADO** no campo de dado e **NÃO OBTIDO** no registro de fontes, com o motivo técnico.
Nenhum spread, alíquota ou taxa foi estimado, arredondado ou inferido.

**Limitação técnica geral desta rodada:** a ferramenta de fetch com renderização atingiu limite de sessão
por volta das 18:00 UTC e o sandbox de shell (curl) passou a falhar de forma intermitente a partir daí.
Vários itens da lista original ficaram, por isso, com status NÃO OBTIDO — estão todos listados na seção 5.

---

## 1. IOF SOBRE CÂMBIO — alíquota vigente

### 1.1 Norma vigente e o caminho até ela

Fonte primária: texto compilado do **Decreto nº 6.306, de 14/12/2007** (Regulamento do IOF), art. 15-B.
URL: `https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/decreto/d6306.htm` — acessado 31/08/2026.

O histórico registrado no próprio texto compilado do Planalto, na ordem em que aparece:

1. **Decreto nº 12.466, de 11/06/2025** — deu nova redação ao art. 15-B (caput passou de "fica reduzida
   para trinta e oito centésimos por cento" para "A alíquota do IOF será de:") e **revogou o art. 15-C**.
2. **Decreto nº 12.467, de 2025** — repristinou o inciso III e **incluiu o inciso XXI-A** (1,10% para
   remessa com finalidade de investimento).
3. **Decreto nº 12.499, de 11/06/2025** — deu a redação atual a todo o art. 15-B e **revogou o art. 15-C**.
4. **Decreto Legislativo nº 176, de 2025** — *sustou* o Decreto 12.499/2025 e *restabeleceu* a redação anterior.
5. **ADC nº 96 (STF)** — o texto compilado marca "(Vide ADC nº 96)" ao lado da redação dada pelo
   Decreto 12.499/2025, que é **a última versão listada de cada inciso** no compilado do Planalto.

**Conclusão:** a redação vigente do art. 15-B em 31/08/2026 é a **dada pelo Decreto nº 12.499, de 11 de
junho de 2025**, restabelecida por decisão do STF na ADC 96 após a sustação pelo Decreto Legislativo 176/2025.

*Observação de escopo:* eu li o registro "(Vide ADC nº 96)" no compilado do Planalto. O **inteiro teor da
decisão do STF na ADC 96** eu **NÃO OBTIVE** (ver seção 5). A leitura acima é a que o próprio compilado
do Planalto suporta: a última redação apresentada para cada inciso é a do Decreto 12.499/2025.

**Nenhum decreto de 2026 altera o Decreto 6.306/2007.** Busca no texto compilado por
"Decreto nº [0-9.]*, de 202[456]" retornou apenas: 12.132/2024, 12.466/2025, 12.467/2025, 12.499/2025.

### 1.2 Alíquotas vigentes — texto literal (Decreto 6.306/2007, art. 15-B, redação do Decreto 12.499/2025)

| Operação | Inciso | Alíquota (texto literal) |
|---|---|---|
| **Remessa ao exterior com finalidade de investimento** | **XXI-A** | "nas liquidações de operações de câmbio para transferência de recursos ao exterior, com vistas à colocação de disponibilidade de residente no País **com finalidade de investimento**: **1,10%** (um inteiro e dez centésimos por cento)" |
| **Transferência ao exterior para conta própria / de mesma titularidade (disponibilidade de residente)** | **XXI** | "nas liquidações de operações de câmbio para transferência de recursos ao exterior, com vistas à colocação de disponibilidade de residente no País, **ou de seu cônjuge, companheiro ou parente, consanguíneo ou afim**, observado o disposto no inciso XXI-A: **3,5%** (três inteiros e cinco décimos por cento)" |
| **Compra de moeda estrangeira em espécie** | **XX** | "nas liquidações de operações de câmbio, para aquisição de moeda estrangeira, em espécie: **3,5%** (três inteiros e cinco décimos por cento)" |
| **Cartão internacional — compra de bens e serviços no exterior** | **VII** | "...arranjos de pagamento de abrangência transfronteiriça na qualidade de emissores destes, decorrentes de aquisição de bens e serviços do exterior efetuada por seus usuários, observado o disposto no inciso VIII: **3,5%**" |
| **Saque no exterior com cartão** | **IX** | "...decorrentes de saques no exterior efetuados por seus usuários: **3,5%**" |
| **Cheque de viagem e carregamento de cartão pré-pago** | **X** | "...destinadas a atender gastos pessoais em viagens internacionais: **3,5%**" |
| **Demais transferências ao exterior** | **XXIV** | "nas demais operações de câmbio realizadas para transferência de recursos ao exterior, não isentas e não abarcadas nos incisos I a XXIII: **3,5%**" |
| **Retorno de recursos do exterior para o Brasil** | **XXV** | "nas demais operações de câmbio realizadas de entrada de recursos do exterior, não isentas e não abarcadas nos incisos I a XXIV: **0,38%** (trinta e oito centésimos por cento)" |
| **Fundos de investimento no mercado internacional (limites e condições da CVM)** | **III** | "nas operações de câmbio, de transferências do e para o exterior, relativas a aplicações de fundos de investimento no mercado internacional, nos limites e condições fixados pela Comissão de Valores Mobiliários: **zero**" |
| Cartão internacional quando o usuário for União/Estados/Municípios/DF | VIII | zero |

**§ 5º do art. 15-B** (redação do Decreto 12.499/2025): "A Secretaria Especial da Receita Federal do Brasil
do Ministério da Fazenda poderá regulamentar o disposto no inciso XXI-A do caput."

> **Regulamento da RFB sobre o inciso XXI-A** (o que caracteriza "finalidade de investimento" para fins de
> enquadrar a remessa em 1,10% em vez de 3,5%): **NÃO OBTIDO**.

### 1.3 Transferência entre contas de mesma titularidade

Não há inciso específico para "mesma titularidade". A operação se enquadra em **XXI** (colocação de
disponibilidade de residente no País) — **3,5%** — salvo se tiver **finalidade de investimento**, hipótese
do **XXI-A** — **1,10%**.

Essa leitura é corroborada, de forma independente, pela prática declarada das plataformas (todas
verificadas em 31/08/2026):

- **Avenue** (`https://avenue.us/cambio/`): "Conta Corrente Internacional: 3,5% / Conta de Investimentos: 1,1%".
- **Nomad** (`https://www.nomadglobal.com/tarifas-nomad`): "Envio de dinheiro para conta internacional:
  encargos de 3,5%"; "Envio de dinheiro para conta investimento: encargos de 1,1%"; "Envio de dinheiro
  de volta para o Brasil: encargos de 0,38%".
- **Vest (ex-Sproutfi)**, tabela de tarifas datada **AUGUST 2026**: "BRL/USD PIX Deposits: 1.85% plus **1.1% IOF**";
  "BRL/USD PIX Withdrawals: 1.85% plus **0.38% IOF**".
- **Wise**, cotação ao vivo obtida em 31/08/2026 17:55 UTC (remessa comum, não classificada como
  investimento): IOF de **BRL 335,81** sobre base de **BRL 9.594,61** = **3,5000%**.

### 1.4 O que mudou em 2025 — a trajetória de redução foi EXTINTA

O **art. 15-C** do Decreto 6.306/2007, incluído pelo **Decreto nº 10.997, de 2022** (com redação do
Decreto 11.153/2022), estabelecia um cronograma de redução do IOF-câmbio. Texto literal dos incisos:

- II — 5,38% a partir de 02/01/2023 (incisos VII, IX, X e XXII)
- III — 4,38% a partir de 02/01/2024 (idem)
- IV — 3,38% a partir de 02/01/2025 (idem)
- V — 2,38% a partir de 02/01/2026 (idem)
- VI — 1,38% a partir de 02/01/2027 (idem)
- VII — **zero a partir de 02/01/2028**, nas operações dos incisos VII, IX, X, XX, XXI e XXII
- VIII — **"a zero, a partir de 2 de janeiro de 2029, nas operações de câmbio a que se refere o caput do art. 15-B"**

**Todo o art. 15-C foi REVOGADO pelo Decreto nº 12.466, de 2025, e pelo Decreto nº 12.499, de 2025.**

Ou seja: **a zeragem programada do IOF-câmbio para 2029 não existe mais.** Quem planejou a remessa contando
com o cronograma de 2022 está operando com premissa revogada. Em 31/08/2026 a alíquota de remessa para
investimento é **1,10%** e a de remessa comum é **3,5%**, sem cronograma de redução vigente.

---

## 2. FICHA POR PLATAFORMA

### 2.0 Tabela mestre

Legenda de custódia: **(a)** custódia estrangeira e independente de instituição brasileira ·
**(b)** custódia estrangeira, mas com controlador/afiliado brasileiro · **(c)** fachada — dinheiro no Brasil.

| Plataforma | Spread cambial (declarado) | IOF aplicado | Corretagem ações/ETFs | Mínimo | Manutenção | Custodiante de fato | FINRA/SIPC | Vínculo BR | Classe |
|---|---|---|---|---|---|---|---|---|---|
| **Avenue** | 1,95% → 0,50% (regressivo, D+1); 1,00%–2,50% (D0); EUR 1,8% / 2,3% | 3,5% conta / **1,1% investimento** / 0,38% volta | US$2,50 / 5 / 7,50 / 10 por faixa; até 10 grátis/mês | câmbio mín. R$200 | US$0 | NÃO CONFIRMADO (ver 2.1) | FINRA CRD 292589; SIPC US$500k (US$250k cash) | **Itaú controlador (50,1%)** | **(b)** |
| **Nomad** | 2,0% / 1,9% / 1,7% / 1,4% / 1,0% (níveis Nomad Pass) | 3,5% conta / **1,1% investimento** / 0,38% volta | **US$0** | NÃO CONFIRMADO | US$0 | **Apex Clearing Corporation** | Nomad Investment Services, membro SIPC US$500k; conta corrente FDIC US$250k | NÃO CONFIRMADO (distribuição via DTVM brasileira, Parecer CVM 33) | **(a)**, com ressalva |
| **Inter US / Global Account** | NÃO CONFIRMADO (ver 2.3) | NÃO CONFIRMADO na fonte atual | **US$0** ("SEC, TAF e corretagem zero") | NÃO CONFIRMADO | US$0 | **DriveWealth** | Inter&Co Securities LLC, FINRA + SIPC US$500k (US$250k cash) | **Subsidiária do Inter&Co (BR)** | **(b)** |
| **Wise** | **0%** de markup na cotação; tarifa explícita de **0,7253%** medida ao vivo | **3,5%** (medido ao vivo) | não oferece corretagem a brasileiros (NÃO CONFIRMADO) | — | — | — | — | — | não é corretora |
| **Interactive Brokers** | comissão FX **0,20 basis point** × trade value, mín. **US$2,00**/ordem | não aplicável (câmbio feito no Brasil, antes) | Pro Fixed US$0,005/ação, mín. US$1,00; Tiered US$0,0005–0,0035, mín. US$0,35 | "No account minimums" / US$0 | inatividade **US$0** | IBKR LLC (autocustódia) | IBKR LLC | nenhum | **(a)** |
| **Charles Schwab International** | NÃO CONFIRMADO | — | **US$0** (online listed equity) | **US$25.000** (fonte secundária) | NÃO CONFIRMADO | Charles Schwab & Co., Inc. | Member SIPC (valor NÃO CONFIRMADO na fonte) | nenhum | **(a)** |
| **XP Investments US** | NÃO CONFIRMADO | NÃO CONFIRMADO | NÃO CONFIRMADO | US$500 mil (Exclusive) / US$1 mi (Private) | NÃO CONFIRMADO | **Pershing LLC ou Interactive Brokers LLC** | FINRA + NFA + SEC; SIPC US$500k (US$250k cash) | marca XP | **(b)** |
| **BTG US** | FX spot **"up to 2% of notional"** | NÃO CONFIRMADO | Pershing: até 3% (>US$5M) / até 5% (<US$5M). DriveWealth: US$1 a US$7,50/ordem | **US$20** (DriveWealth) | Pershing **US$250/conta/trimestre** (isento >US$500k); DriveWealth sem taxa por AUM | **Pershing LLC (BNY Mellon)** e **DriveWealth LLC**; banco: Regent Bank | BTG Pactual US Capital LLC — FINRA, SIPC, NFA | **subsidiária do Banco BTG Pactual S.A.** | **(b)** |
| **Genial Conta Global** | **2% por compra ou venda**; até **2,5%** no câmbio 24h | ver ressalva em 2.8 | NÃO CONFIRMADO | NÃO CONFIRMADO | sem tarifa de manutenção da conta corrente | NÃO CONFIRMADO (página cita apenas FDIC via banco parceiro) | NÃO CONFIRMADO | Genial (BR) | NÃO CLASSIFICÁVEL |
| **Sproutfi → Vest** | PIX **1,85%**; stablecoin **1,4%** (pode cair a 0,7%) | **1,1%** entrada / **0,38%** saída | **US$0** | US$1 para investir; R$10 depósito | **US$0**/mês | **Northbound Securities LLC** | Northbound, Member FINRA/SIPC, US$500k | distribuição por **Oslo Capital DTVM S.A.** | **(a)**, com ressalva |
| **Passfolio** | — | — | — | — | — | — | — | vendeu carteira BR à Sproutfi | **encerrada no Brasil** |
| **Stake** | — | — | — | — | — | — | — | — | **encerrada no Brasil (2023)** |
| **Toro Global** | NÃO CONFIRMADO | — | — | — | — | — | — | — | **produto não localizado** |
| **Nubank / NuInvest** | — | — | — | — | — | — | — | — | **não oferece conta no exterior** |
| **C6 Global** | 0,90% / 0,85% / 0,75% por faixa (**artigo de 2024**) | "1,1%" (**artigo de 2024**) | NÃO CONFIRMADO | NÃO CONFIRMADO | NÃO CONFIRMADO | NÃO CONFIRMADO | NÃO CONFIRMADO | C6 (BR) | NÃO CLASSIFICÁVEL |

---

### 2.1 Avenue

**Fontes:** `https://avenue.us/custos/`, `https://avenue.us/cambio/`, `https://www.avenue.us/seguranca/`,
API pública do FINRA BrokerCheck `https://api.brokercheck.finra.org/search/firm/292589` — todas 31/08/2026.

**Spread cambial** (`avenue.us/custos/` e `avenue.us/cambio/`, literal):
- "spread regressivo que varia de **1,95% a 0,50%** para liquidação no dia próximo dia útil (D+1)"
- liquidação instantânea (D0): "**1,00% a 2,50%**"
- EUR: "spread de **1,8%** na liquidação no próximo dia útil (D+1) e **2,3%** no câmbio instantâneo"
- "Nosso spread é regressivo: a taxa de intermediação cambial começa em 1,95% e pode cair até 0,50%,
  conforme o valor que você converte."
- "*Spread dinâmico disponível apenas para câmbio entre real e dólar."
- "*Câmbio realizado fora do horário comercial pode apresentar um spread mais elevado devido ao fechamento do mercado."
- **A tabela com as faixas exatas de volume/custódia que definem cada degrau do spread: NÃO CONFIRMADA.**

**IOF** (literal, `avenue.us/cambio/`): Real → moeda estrangeira (conta corrente) **3,5%**;
Real → moeda estrangeira (investimentos) **1,1%**; moeda estrangeira → Real **0,38%**.

**Corretagem, Self Directed** (literal): até US$1.000 → **US$2,50/ordem**; US$1.000–2.000 → **US$5,00**;
US$2.000–3.000 → **US$7,50**; acima de US$3.000 → **US$10,00**.
Mesa de operações: **0,5% do volume ou mínimo US$20**. Ações fracionadas: mesmo custo da ordem inteira.
**UCITS ETFs: 0,25% da ordem ou mínimo US$5** (e não entram no benefício das corretagens grátis).
Fundos: US$20/ordem (mesa US$100); Money Market US$0. Opções: US$1/contrato (compra e venda), US$5 exercício.
Carteira de ETF recomendada: US$2,50/ordem. Carteira de Fundos: US$20/ordem.
**"Você poderá ter a isenção de até 10 corretagens no mês para operar Ações e/ou ETFs"**, disponibilizadas
no primeiro dia útil de cada mês com base nas movimentações e na custódia do mês anterior.

**Mínimo:** câmbio mínimo **R$ 200**. **Abertura US$0, manutenção US$0.**

**Transferências:** depósito wire doméstico US$8 (recebimento de wire doméstico na Conta corrente
internacional é gratuito); depósito wire internacional US$14; retirada wire doméstico US$25; retirada wire
internacional US$45; devolução de wire US$30. Saques EUA/exterior US$2 + taxas ATM; saques Brasil 3% + ATM.
Transferência de custódia: **ACAT entrada US$0, saída US$75**; DTC entrada US$0, saída US$25/posição;
DRS US$115 entrada e saída; DWAC US$100; conversão de ADR US$175 + contraparte.

**Regulação e cobertura** (literal, `avenue.us/seguranca/`): "Avenue Securities LLC é uma corretora de
valores mobiliários norte-americana que presta serviços exclusivamente nos Estados Unidos, registrada
perante o regulador norte-americano FINRA ... e membro do SIPC ... **O SIPC protege contas de clientes de
até US$ 500.000 (incluindo US$ 250.000 para reivindicações de dinheiro).**"

**Dados do registro** (FINRA BrokerCheck API, 31/08/2026):
- `firmName: "AVENUE SECURITIES LLC"`, `firmId: 292589`, `bdSECNumber: "70079"`
- `firmType: "Limited Liability Company"`, `formedState: "Delaware"`, `formedDate: "12/05/2017"`
- `finraLastApprovalDate: "11/08/2018"`, `firmStatus: "Approved"`, `regulator: "SEC"`, `bcScope: "ACTIVE"`
- endereço: 2601 S Bayshore Drive, Suite 1100, Miami, FL 33133
- **`directOwners`: `{"legalName": "AVENUE HOLDINGS INC.", "position": "SOLE MEMBER"}`**
- `disclosures: [{"disclosureType": "Regulatory Event", "disclosureCount": 2}]` — **duas ocorrências
  regulatórias registradas**; o teor delas **NÃO FOI OBTIDO**.

**Onde o dinheiro em caixa fica** (literal, `avenue.us/seguranca/`): dólares em **"Coastal Community Bank,
Membro FDIC e JPMorgan Chase Bank, N.A., Membro FDIC"**; euros em **"J.P. Morgan Private Bank Frankfurt,
localizado na Alemanha"**.

**Clearing / custódia dos valores mobiliários:** **NÃO CONFIRMADO.** Existe uma página `avenue.us/apex/`
no site da Avenue (localizada por busca), o que sugere relação com a Apex Clearing, mas **não consegui
abrir e ler essa página** — o fetch falhou. Não afirmo o custodiante sem ter lido.

**Itaú:** o rodapé de `avenue.us/custos/` traz **"Uma empresa Itaú"** e a frase "A Avenue Banco de
Investimentos recebe uma remuneração fixa mensal decorrente da realização da oferta dos serviços".
Reportagem da Forbes Brasil de **dezembro/2025**, título literal: **"Itaú Assume Controle da Avenue com
50,1% do Capital"** (`https://forbes.com.br/forbes-money/2025/12/itau-assume-controle-da-avenue-com-501-do-capital/`).
O **corpo da matéria e o fato relevante do Itaú NÃO FORAM OBTIDOS** (HTTP 403). O percentual 50,1% está,
portanto, confirmado apenas **no título** da reportagem.

**Classificação: (b) — custódia estrangeira com controlador brasileiro.**
Justificativa: a corretora é norte-americana (Delaware/Miami, FINRA/SIPC) e o *sole member* é a Avenue
Holdings Inc.; mas a própria Avenue se identifica como "uma empresa Itaú" e a controladora passou ao Itaú
Unibanco. Pelo critério de "instituição sem vínculo com o Brasil", **a Avenue não passa** — o controlador
final é um banco brasileiro, sujeito a autoridade brasileira.

---

### 2.2 Nomad

**Fontes:** `https://www.nomadglobal.com/tarifas-nomad`, `https://www.nomadglobal.com/nomad-pass`,
`https://www.nomadglobal.com/investimentos`, `https://www.nomadglobal.com/` — todas 31/08/2026.

**Tarifas de câmbio** (literal, página de tarifas):
- "Envio de dinheiro para conta internacional: **encargos de 3,5% + taxa de conversão a partir de 1%**"
- "Envio de dinheiro para conta investimento: **encargos de 1,1% + taxa de conversão a partir de 1%**"
- "Envio de dinheiro de volta para o Brasil: **encargos de 0,38% + taxa de conversão a partir de 1% + US$ 10**"
- "Saques fora da Rede MoneyPass: **US$ 5 por saque**"
- "*A taxa operacional varia de acordo com o Programa Nomad Pass"

**Escada do spread — Nomad Pass** (literal, tabela "Taxa operacional de câmbio"):

| Nível | Pontuação | Taxa operacional de câmbio |
|---|---|---|
| 1 | 0 a 1 mil | **2,0%** |
| 2 | 1 a 5 mil | **1,9%** |
| 3 | 5 mil a 10 mil | **1,7%** |
| 4 | 10 mil a 20 mil | **1,4%** |
| 5 | + de 20 mil | **1,0%** |

"A cada US$ 1 convertido você ganha 1 ponto." (A página traz duas tabelas com faixas de pontuação
ligeiramente divergentes — 1.000–3.000 e 3.000–10.000 numa delas; registro a divergência.)

**Corretagem:** "**Taxa zero de corretagem** — Economize nas suas movimentações sem pagar taxas de corretagem".
**Abertura e manutenção:** "você não paga nenhuma taxa de abertura nem manutenção da conta."

**Custódia e cobertura** (literal): "A Conta Internacional é protegida pelo **FDIC em até US$ 250 mil**.
Já a Conta Investimentos é oferecida pela **Nomad Investment Services, membro do SIPC**, com valores
mobiliários protegidos em até **US$500 mil**."
E: "os serviços de investimento nos Estados Unidos fornecidos pela Nomad Investment Services dependem de
integrações com parceiros, como a **Apex Clearing Corporation ("Apex"), membro da Financial Industry
Regulatory Authority ("FINRA") ... e da Securities Investor Protection Corporation ("SIPC")**."

**Entidade:** "Nomad Fintech Inc. — 4951 International Drive, Orlando, FL 32819, Estados Unidos da América".
"A Nomad não é um banco, é uma fintech."

**Distribuição no Brasil:** a Nomad declara operar "nos termos do **Parecer de Orientação CVM nº 33, de 30
de setembro de 2005**, do Memorando nº 112/2020-CVM/SMI/GME ... e da decisão proferida pelo Colegiado da CVM
por meio da Reunião nº 08, de 23 de fevereiro de 2021", com referência a um documento "Parceria Global DTVM".
**O nome da DTVM brasileira parceira NÃO FOI CONFIRMADO** (o link do documento não foi aberto).

**Controle societário:** **NÃO CONFIRMADO.** Não obtive cap table nem estrutura de controle.

**Classificação: (a) com ressalva — custódia genuinamente estrangeira e, até onde apurei, independente.**
Justificativa: a custódia dos valores mobiliários é da **Apex Clearing Corporation**, entidade norte-americana
sem relação declarada com instituição brasileira; a corretora é a Nomad Investment Services (SIPC); o caixa
fica em banco FDIC. **A ressalva:** a Nomad é uma empresa fundada e operada por brasileiros, com toda a base
de clientes no Brasil e distribuição sob supervisão indireta da CVM via DTVM parceira — não confirmei quem
controla a holding. Pelo critério estrito do Bastter ("instituição sem vínculo com o Brasil"), a *custódia*
passa (Apex é independente), mas o *ponto de acesso* é uma empresa cuja operação está inteiramente voltada ao Brasil.

---

### 2.3 Inter US / Global Account

**Fontes:** `https://inter.co/pra-voce/global-account/`, `https://inter.co/pt/us/investments/`,
`https://ajuda.inter.co/investimentos/e-seguro-realizar-investimentos-na-plataforma-inter-securities`,
`https://ajuda.inter.co/investimentos/investir-pela-plataforma-inter-securities-tem-taxas` — todas 31/08/2026.

**Spread cambial: NÃO CONFIRMADO para 2026.** A página `inter.co/pra-voce/global-account/` traz uma tabela
comparativa em que a coluna "Global Account" mostra **"Spread R$ 51,77 (0,99%)"** e **"IOF R$ 57,53 (3,5%)"**
sobre compra de US$ 1.000 — mas a própria nota de rodapé da tabela diz:
**"Cotação de $1 = R$ 5,23 (comercial) e R$ 5,43 (turismo) em 1º de setembro de 2022."**
O número 0,99% está, portanto, **datado de setembro de 2022** e **não pode ser tomado como spread vigente
em agosto de 2026**. A página de ajuda com o spread atual retornou HTTP 404.

**Corretagem** (literal, `inter.co/pt/us/investments/`): "**Investimento sem taxas. SEC, TAF e corretagem zero.**"
**Manutenção** (literal): "Conta digital de investimentos, **sem taxa de abertura ou manutenção**."
E na central de ajuda: "**Não há taxas para operações de ativos listados em bolsa americana** (compra e venda
de ações/FIIs/ETFs), esse serviço é gratuito. Outros serviços podem possuir pequenos custos."

**Custódia e regulação** (literal, central de ajuda): a Inter&Co Securities LLC é "uma corretora
norte-americana devidamente registrada e autorizada a operar nos Estados Unidos", regulada pela **FINRA** e
membro da **SIPC**, com **"DriveWealth como custodiante dos ativos"** e proteção de até **"US$ 500 mil por
cliente (sendo até US$ 250 mil em dinheiro) em caso de insolvência"**. A página enfatiza que "os ativos
disponíveis na plataforma não são registrados nem supervisionados pela CVM ou por órgãos reguladores brasileiros".

**Caixa:** cartão de débito emitido pelo **American State Bank** (FDIC); depósitos mantidos junto ao
**Community Federal Savings Bank** (FDIC).

**Depósito mínimo: NÃO CONFIRMADO.**

**Classificação: (b) — custódia estrangeira com controlador brasileiro.**
Justificativa: a custódia é da DriveWealth LLC (EUA, independente), o que é positivo; mas a corretora
Inter&Co Securities LLC é declaradamente **"subsidiária do grupo Inter&Co"**, cujo controlador operacional é
o Banco Inter, brasileiro. O vínculo com o Brasil é direto e admitido.

---

### 2.4 Wise — medição ao vivo

A Wise não é corretora: é serviço de remessa e conta multimoeda. Incluída porque é a rota de câmbio
mais barata que consegui **medir**, não apenas ler.

**Medição ao vivo, 31/08/2026 17:55 UTC.** Endpoint público de cotação:
`POST https://wise.com/gateway/v3/quotes/` com `{"sourceCurrency":"BRL","targetCurrency":"USD","sourceAmount":10000,"profileCountry":"BR"}`

Resposta literal (campos relevantes):
```
"rate": 0.192827, "rateType": "FIXED", "rateTimestamp": "2026-08-31T17:55:37Z"
"sourceAmount": 10000.00, "targetAmount": 1850.10
"items": [ {"type":"TRANSFERWISE","label":"Our fee","value":{"amount":69.59,"currency":"BRL"}},
           {"type":"BRL_TAX","label":"IOF tax","value":{"amount":335.81,"currency":"BRL"}} ]
"total": {"label":"Total fees","value":{"amount":405.40,"currency":"BRL"}}
"calculatedOn": {"unroundedAmountToConvert":{"amount":9594.609798693748,"currency":"BRL"}}
```

**Contas verificáveis a partir desses números:**
- IOF: 335,81 ÷ 9.594,61 = **3,5000%** → confirma o inciso XXI (remessa comum, não classificada como investimento).
- Tarifa Wise: 69,59 ÷ 9.594,61 = **0,7253%** sobre o montante convertido (0,6959% sobre os R$ 10.000 brutos).
- Total de tarifas: 405,40 sobre 10.000 = 4,054%.

**Markup na cotação:** a taxa aplicada (0,192827) é **idêntica** à cotação ao vivo publicada pela própria Wise
(`https://wise.com/rates/live?source=BRL&target=USD` → `{"source":"BRL","target":"USD","value":0.192827}`,
mesmo instante). Invertida: 1 ÷ 0,192827 = **R$ 5,1860 por dólar**.

**Referência independente — PTAX do Banco Central**, API Olinda
(`https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(...)`), 31/08/2026:
`{"cotacaoCompra":5.18100,"cotacaoVenda":5.18160,"dataHoraCotacao":"2026-08-31 13:08:57"}`.

A taxa da Wise (5,1860) fica a **0,086% acima da PTAX de venda** (5,1816) do mesmo dia — dentro da variação
intradiária normal. **Conclusão evidenciada: a Wise não embute markup na cotação; cobra tarifa explícita.**
É a única plataforma desta lista cujo spread eu pude *medir* em vez de apenas *ler*.

**Conta de investimento em ações para brasileiros: NÃO CONFIRMADO** — não localizei fonte oficial da Wise
dizendo se o produto de investimento está disponível a residentes no Brasil.

---

### 2.5 Interactive Brokers

**Fontes:** `https://www.interactivebrokers.com/en/pricing/commissions-home.php`,
`https://www.interactivebrokers.com/en/pricing/commissions-spot-currencies.php`,
`https://www.interactivebrokers.com/en/pricing/other-fees.php` — todas 31/08/2026.

**Corretagem US stocks e ETFs** (literal):
- IBKR Lite: "Commission-free" — **apenas para residentes elegíveis dos EUA**
- IBKR Pro **Fixed**: **USD 0.005 por ação, mínimo USD 1.00 por ordem**
- IBKR Pro **Tiered**: **USD 0.0005 a USD 0.0035 por ação, mínimo USD 0.35**

**Câmbio (Spot Currencies)** — este é o número que praticamente ninguém publica. Texto literal:
> "IBKR passes through the prices that it receives and charges a separate low commission. We do this in the
> interest of providing a transparent pricing structure instead of marking up our quotes and charging nothing
> in commissions as is the practice with many currency brokers."

Tabela literal (Tiered, por Monthly Trade Value em USD):

| Monthly Trade Value (USD) | Comissão |
|---|---|
| ≤ 1.000.000.000 | **0.20 basis point × Trade Value** |
| 1.000.000.000,01 – 2.000.000.000 | 0.15 basis point |
| 2.000.000.000,01 – 5.000.000.000 | 0.10 basis point |
| > 5.000.000.000 | 0.08 basis point |

Mínimo por ordem: **Tier I — USD 2.00**; Tier II — USD 1.50; Tier III — USD 1.25; Tier IV — USD 1.00.
Nota literal: "1 basis point = 0.0001." Spreads exibidos "as small as 0.1 PIP".

**0,20 basis point = 0,002%.** Duas ordens de grandeza abaixo de qualquer plataforma brasileira desta lista.

**Mínimos e manutenção:** "No account minimums"; saldo mínimo **USD 0** nos dois planos;
taxa de inatividade **USD 0**.

**Retiradas:** as **primeiras 2 retiradas por mês são gratuitas**; depois, transferência bancária
**USD 10,00** (EUR 8,00 / GBP 7,00); ACH/SEPA a partir de USD 1,00.

**Qual entidade um brasileiro abre — conta LLC americana vs. IBKR Ireland:**
**NÃO CONFIRMADO em fonte primária.** As páginas de disclosure de entidade da IBKR que tentei retornaram
HTTP 404 e a página `interactivebrokers.com/pt/general/what-you-need-inv.php` veio truncada exatamente na
seção "Other countries". A única evidência que obtive é **secundária**: guia publicado em 12/04/2026
(atualizado 14/04/2026) que traz a linha literal **"Most other countries | IBKR LLC (US) | Broadest product
access"** e observa que "When you start the application and enter your country of residence, IB will
automatically direct you to the appropriate entity"
(`https://scalpelandstocks.com/how-to-open-interactive-brokers-account-non-us-resident/`).
**Não confirmei em fonte IBKR** que o Brasil cai em IBKR LLC.

**Ponto operacional relevante e não resolvido:** se a conta é com a IBKR LLC nos EUA, o brasileiro precisa
*enviar dólares* — ou seja, faz o câmbio numa instituição **brasileira**, pagando o spread dela e o IOF, e a
comissão de 0,20 bp da IBKR só se aplica a conversões feitas *dentro* da conta. **Se a IBKR aceita depósito
em BRL diretamente de residentes no Brasil: NÃO CONFIRMADO.** Isso muda materialmente o custo total e é a
lacuna mais importante desta ficha.

**Classificação: (a) — custódia genuinamente estrangeira e independente.**
Justificativa: IBKR LLC é corretora norte-americana autocustodiante, sem controlador brasileiro, sem
distribuição via DTVM local. É o caso mais limpo da lista pelo critério do Bastter. O preço disso é que
não há atendimento em português nem facilitação de câmbio — o brasileiro resolve a remessa por fora.

---

### 2.6 Charles Schwab International

**Fontes:** `https://international.schwab.com/pricing`,
`https://international.schwab.com/content/how-to-open-international-account` — 31/08/2026.

- Comissão: **"$0"** para ações e ETFs listados, em ordens online.
- Custodiante e regulação (literal): **"Charles Schwab & Co., Inc. ('Schwab') (Member SIPC), is registered
  by the Securities and Exchange Commission ('SEC')"**.
- **Valor da cobertura SIPC: NÃO CONFIRMADO** nas páginas que li.
- **Taxa de conversão de moeda: NÃO CONFIRMADO.** As páginas de pricing internacional não trazem o número.
- **Depósito mínimo: US$ 25.000** — fonte **secundária**, literal: "there is a minimum requirement of
  $25,000 USD to open an individual or joint account"
  (`https://www.brokerage-review.com/investing-firm/foreigner/charles-schwab-for-non-us-citizens.aspx`,
  o próprio site declara "Updated on 12/13/2024"). **NÃO CONFIRMADO em fonte Schwab.**
- **Brasil na lista de países elegíveis: NÃO CONFIRMADO.** A página oficial diz apenas que "você pode abrir
  uma conta internacional através do Schwab.com se você viver em um país qualificador", sem exibir a lista.

**Classificação: (a) — custódia genuinamente estrangeira e independente**, se e quando o brasileiro for
elegível. Justificativa: Charles Schwab & Co. é corretora norte-americana sem vínculo societário brasileiro
e sem distribuição via instituição local. **A elegibilidade do residente no Brasil é o ponto não resolvido.**

---

### 2.7 XP Investments US, BTG US

**XP Investments US, LLC** — fonte: `https://www.xpi.us/`, 31/08/2026. Texto literal:
- "XP Investments US, LLC d/b/a XP Investments", **"FINRA and NFA member broker dealer"**,
  "registered with the United States Securities and Exchange Commission"
- **custódia: "Pershing LLC or Interactive Brokers, LLC"**
- SIPC: **"up to $500,000 (including $250,000 for claims for cash)"**
- Mínimos: **US$ 500 mil (Exclusive)** e **US$ 1 milhão (Private)**
- "is intended only for the United States"; "cannot carry out operations in the Brazilian market"
- **Corretagem, spread cambial e taxa de manutenção: NÃO CONFIRMADOS** (não constam da página)
- **Relação societária explícita com a XP Inc. brasileira: NÃO CONFIRMADA na página** — há apenas as marcas
  "XP International" e "XP Private" no rodapé.

**Classificação XP US: (b)** — custódia em Pershing/IBKR (estrangeiras e independentes), mas a marca, o canal
e a captação são do grupo XP brasileiro. O vínculo societário formal ficou não confirmado; a classificação
(b) é feita pelo vínculo de marca e distribuição, que é evidente.

**BTG Pactual US Capital, LLC** — fontes: `https://www.btgpactual.us/pt/fee-schedule/` e
`https://www.btgpactual.us/pt/international-accounts/`, 31/08/2026. Texto literal:
- **FX Spot: "up to 2% of notional"**
- Ações e ETFs, conforme custodiante: **Pershing** — até **3%** (contas acima de US$ 5M) ou até **5%**
  (abaixo de US$ 5M); **DriveWealth** — **US$ 1 a US$ 7,50 por ordem**, conforme volume
- Manutenção/custódia: **Pershing US$ 250 por conta por trimestre** (dispensável acima de US$ 500k);
  DriveWealth sem taxa sobre AUM
- Depósito mínimo: **US$ 20** (DriveWealth)
- Wire: **US$ 100 por wire** (Pershing)
- Entidade: "BTG Pactual US Capital, LLC", **"member of FINRA, SIPC and NFA"**
- Custodiantes: **Pershing LLC** (subsidiária do Bank of New York Mellon) e **DriveWealth LLC**;
  contas bancárias no **Regent Bank**
- Vínculo: **"BTG Pactual Bank, National Association is an owned subsidiary of Banco BTG Pactual S.A."**;
  os clientes transferem fundos do Brasil pelos aplicativos locais do BTG.

**Classificação BTG US: (b)** — custódia em Pershing/DriveWealth (estrangeiras, independentes), mas a
corretora é do grupo BTG e o banco é subsidiária declarada do Banco BTG Pactual S.A.
**Nota de custo:** a corretagem de "até 3% a 5%" na custódia Pershing é, de longe, a mais cara desta pesquisa
— e some completamente numa conversa focada só em spread cambial.

---

### 2.8 Genial Conta Global (ex-Passfolio), Sproutfi→Vest, Stake, Toro, Nubank, C6

**Genial Conta Global** — `https://www.genialinvestimentos.com.br/conta-global/`, 31/08/2026. Literal:
- **spread: "spread de 2% por compra ou venda"**, podendo chegar a **"2,5% da cotação do dólar comercial
  para o cenário de câmbio 24h"**
- IOF citado na página: **"0,38% para BRL/USD"** (entrada) e **"1,1% para USD/BRL remessas de recursos ao
  exterior"**. **Ressalva expressa:** essa redação está trocada em relação à direção das operações e não
  corresponde ao art. 15-B vigente para uma conta corrente internacional. **Não uso esses números como
  confirmação do IOF aplicado pela Genial — marco como NÃO CONFIRMADO.**
- "A Conta Global não possui tarifas de manutenção da conta corrente"
- cartão de débito emitido por **"Community Federal Savings Bank, membro FDIC"**; "Os valores mantidos nos
  EUA são segurados pelo FDIC, via banco parceiro, até os limites aplicáveis"
- **Corretagem, depósito mínimo, corretora americana, custodiante, FINRA/SIPC: NÃO CONFIRMADOS.**

**Classificação Genial: NÃO CLASSIFICÁVEL** — sem identificar o broker-dealer e o custodiante, não classifico.
A página só menciona proteção **FDIC** (bancária), nunca **SIPC** (mobiliária), o que é uma diferença
substantiva: FDIC protege depósito, não protege posição em ação ou ETF.

**Passfolio:** resultado de busca com título literal "Passfolio vende carteira de clientes no Brasil para
plataforma de investimentos Sproutfi e encerra seus serviços no país" (Seu Dinheiro, 2022);
`https://passfolio.com/` falhou com erro de TLS em 31/08/2026. **Status: encerrada no Brasil (PARCIAL —
corpo da matéria não lido).**

**Sproutfi → Vest** — `https://www.sproutfi.com/` (31/08/2026) serve hoje o site da marca **Vest**.
Literal: "Vest operates through **Northbound Securities LLC**, a FINRA member"; "Insured up to **$500,000
(SIPC)**. Held by a FINRA-member broker."

**Tabela de tarifas oficial**, PDF com cabeçalho literal **"FEE SCHEDULE | AUGUST 2026"**
(`https://storage.googleapis.com/northbound-legal-documents/FeeSchedule_V.02_17_03_2024.pdf`, 31/08/2026) —
é a fonte de tarifas mais recente e mais explícita que encontrei em toda esta pesquisa:

| Item (literal) | Valor |
|---|---|
| Stocks, REITs, and ETFs (U.S.) | "Purchase or sale commission: **$0 USD**" |
| Platform Fee (Monthly) | **$0 USD** |
| SmartVest (Consulting) | "Up to **1.5%** annual fee" |
| **BRL/USD PIX Deposits** | **"1.85% plus 1.1% IOF"** |
| **BRL/USD PIX Withdrawals** | **"1.85% plus 0.38% IOF"** |
| **BRL/USD Stablecoin Deposits** | **"1.4% (IOF does not apply)"** — "May decrease to 0.7% based on deposit amount" |
| USD/BRL Stablecoin Withdrawals | "1.4% (IOF does not apply)" |
| Outgoing Bank Transfer (Wire) USA | $25 USD |
| Outgoing Bank Transfer (Wire) outside the US | $35 USD |
| ACAT Entry / ACAT Departures | Free / **$65 USD por conta** |
| Account opening / maintenance fees | **$0** |
| SEC Commission (Regulatory) | $20.60 USD por $1.000.000 de principal |
| TAF Commission | $0.000166 USD por ação (somente venda), máx. $8.30 |

Notas de rodapé literais: "**Remittance services provided by FacilitaPay Pagamentos S/A**";
"Remittance services provided by **Avenia - BRLA DIGITAL LTDA**" (rota stablecoin).
"Securities offered by Northbound, Securities, LLC ('Vest') **Member FINRA/SIPC**". "As of May 1st, 2025".

Disclosure literal para brasileiros: "None of the Vest Companies are authorized by the Brazilian Securities
and Exchange Commission (CVM) to offer securities distribution services to investors who are residents,
domiciled, or incorporated in the Federative Republic of Brazil. The securities distribution service to
Brazilian investors is offered by **Oslo Capital DTVM S.A., registered under CNPJ 13.673.855/0001-25** ...
duly authorized to operate as a securities broker by the Central Bank of Brazil. This is in accordance with
Guiding Opinion 33 of the Brazilian Securities and Exchange Commission (CVM)". Versão do disclosure: V.06 09/05/2024.

**Classificação Vest: (a) com ressalva.** Custódia em Northbound Securities LLC (EUA, FINRA/SIPC), sem
controlador brasileiro identificado. A ressalva é a mesma da Nomad: a *distribuição* passa por DTVM
brasileira (Oslo Capital) e a *remessa* por instituição de pagamento brasileira (FacilitaPay). O ativo está
fora; o funil de entrada está dentro.
**Chamo atenção para a rota stablecoin: 1,4% sem IOF, contra 1,85% + 1,1% de IOF na rota PIX.** É a única
plataforma da lista que publica uma rota de entrada sem IOF. **Não avalio a licitude tributária dessa rota** —
apenas registro que a tabela oficial da instituição, datada de agosto de 2026, a apresenta assim.

**Stake:** `https://hellostake.com/br` retorna **HTTP 404** em 31/08/2026. Reclamação pública com título
literal "ENCERRAMENTO DAS OPERAÇÕES", postada em 02/03/2023, relata as opções comunicadas aos clientes:
transferência automática para a Sproutfi até 3 de abril; transferência para outra corretora até 20 de março
com taxa "a partir de US$65"; ou liquidação dos ativos até 27 de março e saque até 29 de março
(`https://www.reclameaqui.com.br/stake/encerramento-das-operacoes_p9B7lg7goku4h2yf/`).
**Status: encerrada no Brasil.** (Fonte é reclamação de consumidor, não comunicado da empresa — PARCIAL.)

**Toro Global:** `https://www.toroinvestimentos.com.br/global` retornou **HTTP 403** e
`https://global.toro.com.br/` falhou no túnel do proxy, ambos em 31/08/2026. As buscas retornaram apenas
conteúdo de blog sobre ETFs e BDRs na B3, não um produto de conta internacional próprio.
**Existência de produto "Toro Global": NÃO CONFIRMADA.**

**Nubank / NuInvest:** em 31/08/2026, `https://nubank.com.br/conta-global/` e
`https://nubank.com.br/conta-internacional/` retornam **HTTP 404**. A página
`https://nubank.com.br/investimentos/` não apresenta produto de conta ou corretora no exterior; a única
ocorrência de "Global" no HTML é o link institucional "Nu Global" para `international.nubank.com.br`
(site corporativo, não produto). **Conclusão: não localizei produto de conta de investimento no exterior do
Nubank.** Marco como **PARCIAL** — ausência de evidência não é evidência de ausência, mas procurei nas
páginas de produto e não há.

**C6 Bank Global Account:** `https://www.c6bank.com.br/*` retornou **HTTP 403** a todas as tentativas via
shell em 31/08/2026. O único conteúdo que consegui ler foi o blog do próprio C6
(`https://www.c6bank.com.br/blog/como-pagar-menos-spread-de-cambio`), **artigo datado de 6 de maio de 2024,
atualizado em 6 de novembro de 2024**, com a tabela literal:

| Valor | Spread |
|---|---|
| R$ 20 a R$ 999,99 | **0,90%** |
| R$ 1.000 a R$ 4.999,99 | **0,85%** |
| A partir de R$ 5.000 | **0,75%** |

e a menção a IOF "de apenas 1,1%".

**Ressalva expressa:** o artigo é **anterior aos Decretos 12.466/12.467/12.499 de junho de 2025**. Nem o
spread nem o IOF ali podem ser tomados como vigentes em agosto de 2026.
**Spread C6 vigente, custodiante, corretora americana, FINRA/SIPC, corretagem e mínimo: NÃO CONFIRMADOS.**
**Classificação C6: NÃO CLASSIFICÁVEL.**

### 2.9 Síntese da classificação pelo critério de jurisdição

- **(a) custódia genuinamente estrangeira e independente:** **Interactive Brokers** (o caso mais limpo),
  **Charles Schwab** (se elegível), **Nomad** e **Vest** (custódia em Apex e Northbound, ambas independentes —
  com a ressalva de que distribuição e remessa passam por instituições brasileiras).
- **(b) custódia estrangeira, controlador ou grupo brasileiro:** **Avenue** (Itaú), **Inter US** (Inter&Co),
  **BTG US** (Banco BTG Pactual S.A.), **XP US** (grupo XP).
- **(c) fachada, dinheiro no Brasil:** **nenhuma plataforma desta lista se enquadrou.** Todas as que
  consegui verificar têm broker-dealer registrado nos EUA e custódia declarada em instituição americana.
  Genial e C6 ficaram **não classificáveis** por falta de informação sobre o broker-dealer e o custodiante —
  o que, para o critério do Bastter, é em si um sinal: a instituição que não publica quem custodia seus
  ativos não permite que você avalie o risco de jurisdição.

**Uma observação que atravessa todas as fichas:** o spread cambial é o custo dominante e é o único que
nenhuma plataforma brasileira expõe como número único e verificável. Avenue publica uma faixa (1,95%–0,50%)
sem a tabela de degraus; Nomad publica níveis atrelados a um programa de pontos; BTG publica "up to 2%";
Genial publica "2% a 2,5%". Só a **Wise** (0% de markup + tarifa explícita) e a **IBKR** (0,20 bp) publicam
números que se pode conferir. Foi exatamente por isso que a Wise foi a única que consegui **medir**.

---

## 3. TRIBUTAÇÃO — artigo por artigo

### 3.1 Lei nº 14.754, de 12 de dezembro de 2023

Fonte primária: texto no Planalto, arquivo já baixado e lido integralmente em 31/08/2026.
Vigência (art. 47, II): "a partir de 1º de janeiro de 2024, quanto aos demais dispositivos".

**Art. 2º, caput** (literal): "A pessoa física residente no País declarará, **de forma separada dos demais
rendimentos e dos ganhos de capital, na Declaração de Ajuste Anual (DAA)**, os rendimentos do capital
aplicado no exterior, nas modalidades de **aplicações financeiras** e de **lucros e dividendos de entidades
controladas**."

**Art. 2º, § 1º** (literal): "Os rendimentos de que trata o caput deste artigo ficarão sujeitos à incidência
do Imposto sobre a Renda das Pessoas Físicas (IRPF), **no ajuste anual, à alíquota de 15% (quinze por cento)
sobre a parcela anual dos rendimentos**, hipótese em que **não será aplicada nenhuma dedução da base de cálculo**."

→ **Sim: alíquota única de 15%, apuração ANUAL na DAA, sem dedução alguma na base.** Não há mais tabela
progressiva, não há mais recolhimento mensal para essa categoria.

**Art. 2º, § 2º** (literal): "Os ganhos de capital percebidos pela pessoa física residente no País na
alienação, na baixa ou na liquidação de bens e direitos localizados no exterior **que não constituam
aplicações financeiras** no exterior nos termos desta Lei **permanecem sujeitos às regras específicas de
tributação previstas no art. 21 da Lei nº 8.981, de 20 de janeiro de 1995**."

**Art. 2º, § 3º** (literal): "**A variação cambial de depósitos em conta-corrente ou em cartão de débito ou
crédito no exterior não ficará sujeita à incidência do IRPF**, desde que os depósitos **não sejam remunerados**
e sejam mantidos em instituição financeira no exterior reconhecida e autorizada a funcionar pela autoridade
monetária do país em que estiver situada."

**Art. 2º, § 4º** (literal): "A variação cambial de **moeda estrangeira em espécie** não ficará sujeita à
incidência do IRPF **até o limite de alienação de moeda no ano-calendário equivalente a US$ 5.000,00
(cinco mil dólares americanos)**."

**Art. 2º, § 5º** (literal): "Os ganhos de variação cambial percebidos na alienação de moeda estrangeira em
espécie cujo valor de alienação exceder o limite previsto no § 4º deste artigo ficarão sujeitos
**integralmente** à incidência do IRPF conforme as regras previstas neste artigo."

**Art. 3º, § 1º, I** — definição de aplicação financeira no exterior (literal, íntegra):
"quaisquer operações financeiras fora do País, incluídos, de forma exemplificativa, depósitos bancários
remunerados, certificados de depósitos remunerados, ativos virtuais, carteiras digitais ou contas-correntes
com rendimentos, cotas de fundos de investimento, com exceção daqueles tratados como entidades controladas
no exterior, instrumentos financeiros, apólices de seguro cujo principal e cujos rendimentos sejam
resgatáveis pelo segurado ou pelos seus beneficiários, certificados de investimento ou operações de
capitalização, fundos de aposentadoria ou pensão, **títulos de renda fixa e de renda variável**, operações
de crédito, inclusive mútuo de recursos financeiros, em que o devedor seja residente ou domiciliado no
exterior, derivativos e **participações societárias**, com exceção daquelas tratadas como entidades
controladas no exterior, incluindo os direitos de aquisição."

→ **Ação americana e ETF americano são "aplicação financeira no exterior".** É esse enquadramento que
elimina a isenção de R$ 35 mil (ver 3.2).

**Art. 3º, § 1º, II** — definição de rendimento (literal): "remuneração produzida pelas aplicações
financeiras no exterior, incluídos, de forma exemplificativa, **variação cambial da moeda estrangeira** ou
variação da criptomoeda em relação à moeda nacional, rendimentos em depósitos em carteiras digitais ou
contas-correntes remuneradas, juros, prêmios, comissões, ágio, deságio, participações nos lucros,
**dividendos** e ganhos em negociações no mercado secundário, **inclusive ganhos na venda de ações das
entidades não controladas em bolsa de valores no exterior**."

**Art. 3º, § 2º** (literal): os rendimentos "serão computados na DAA e submetidos à incidência do IRPF **no
período de apuração em que forem efetivamente percebidos** pela pessoa física, como no recebimento de juros
e outras espécies de remuneração e, em relação aos ganhos, **inclusive de variação cambial sobre o principal**,
**no resgate, na amortização, na alienação, no vencimento ou na liquidação** das aplicações financeiras."

**Art. 4º** — dedução do imposto pago no exterior. Literal: pode deduzir do IRPF devido, na ficha da DAA do
art. 2º, o imposto pago no país de origem, desde que **(I)** esteja prevista a compensação em acordo/tratado
para evitar dupla tributação **ou (II)** haja **reciprocidade de tratamento**.
§ 1º: "A dedução não poderá exceder a diferença entre o IRPF calculado com a inclusão do respectivo
rendimento e o IRPF devido sem a sua inclusão."
§ 2º: imposto pago no exterior convertido pela "cotação de fechamento da moeda estrangeira divulgada, **para
compra**, pelo Banco Central do Brasil, para o dia do pagamento do imposto no exterior".
§ 3º: não deduz imposto passível de reembolso/restituição/ressarcimento/compensação no exterior.
§ 4º: "O imposto pago no exterior **não deduzido no ano-calendário não poderá ser deduzido** do IRPF devido
em anos-calendários posteriores ou anteriores."

**Art. 5º, caput** (literal): "Os lucros apurados pelas entidades controladas no exterior por pessoas físicas
residentes no País, enquadradas nas hipóteses previstas neste artigo, serão tributados **em 31 de dezembro
de cada ano**, na forma prevista no art. 2º desta Lei."

**Art. 9º — compensação de perdas** (literal):
- caput: "A pessoa física residente no País poderá compensar as perdas realizadas em aplicações financeiras
  no exterior a que se refere o art. 3º, **quando devidamente comprovadas por documentação hábil e idônea**,
  com rendimentos auferidos em aplicações financeiras no exterior, na ficha da DAA de que trata o art. 2º
  desta Lei, **no mesmo período de apuração**."
- § 1º: se as perdas superarem os ganhos, o excedente "poderá ser compensada com **lucros e dividendos de
  entidades controladas no exterior** ... que tenham sido computados na DAA no mesmo período de apuração."
- § 2º: perdas acumuladas não compensadas "poderão ser compensadas com rendimentos computados na ficha da
  DAA ... em **períodos de apuração posteriores**."
- § 3º: "**As perdas poderão ser compensadas uma única vez.**"

**Art. 15** (literal): "A cotação a ser utilizada para converter os valores em moeda estrangeira em moeda
nacional é a **cotação de fechamento da moeda estrangeira divulgada, para venda, pelo Banco Central do Brasil,
para a data do fato gerador**, ressalvadas as disposições específicas previstas nesta Lei."

**Art. 46 — revogações.** Interessa aqui o inciso **IX, alínea "a": "art. 24" da Medida Provisória nº
2.158-35, de 24 de agosto de 2001** (e alínea "b": art. 28 da mesma MP).

### 3.2 A isenção de R$ 35 mil/mês — o ponto que mais gera confusão

**Resposta direta: para aplicações financeiras no exterior, a isenção ACABOU em 01/01/2024.**
Não foi "revogada a Lei 9.250" — o mecanismo foi outro, e é preciso ver os três degraus:

**Degrau 1 — a isenção continua existindo na lei geral.**
Lei nº 9.250/1995, **art. 22** (redação da Lei nº 11.196/2005), texto literal:
"Fica isento do imposto de renda o ganho de capital auferido na alienação de bens e direitos de pequeno
valor, cujo preço unitário de alienação, no mês em que esta se realizar, seja igual ou inferior a:
**I - R$ 20.000,00** (vinte mil reais), no caso de alienação de ações negociadas no mercado de balcão;
**II - R$ 35.000,00** (trinta e cinco mil reais), nos demais casos."
(`https://www.planalto.gov.br/ccivil_03/leis/l9250.htm`, 31/08/2026)

**Degrau 2 — o que foi revogado foi o regime que dava acesso a ela no exterior.**
A MP 2.158-35/2001, **art. 24**, era o dispositivo que mandava apurar **ganho de capital** na "alienação de
bens ou direitos e da liquidação ou resgate de aplicações financeiras, de propriedade de pessoa física,
adquiridos, a qualquer título, **em moeda estrangeira**". Enquanto a operação era *ganho de capital*, a
isenção de bem de pequeno valor do art. 22 da Lei 9.250 alcançava-a.
O texto do art. 24 no Planalto traz agora a marca literal: **"(Revogado pela Lei nº 14.754, de 2023)"**
(`https://www.planalto.gov.br/ccivil_03/mpv/2158-35.htm`, 31/08/2026).
O § 6º, II do mesmo art. 24 — que isentava a alienação de moeda estrangeira em espécie até
"cinco mil dólares norte-americanos" no ano-calendário — caiu junto (e foi **substituído** pelo art. 2º, § 4º
da Lei 14.754, com o mesmo limite de US$ 5.000; ver 3.4).

**Degrau 3 — a Lei 14.754 reclassificou a operação.** Pelo art. 3º, § 1º, I, ação e ETF no exterior são
**aplicação financeira**, e o ganho na venda é **rendimento** tributado a 15% na DAA (art. 2º, § 1º) — não é
mais "ganho de capital na alienação de bem". A isenção do art. 22 da Lei 9.250 fala de *ganho de capital na
alienação de bens e direitos*; deixou de haver o fato a que ela se aplicava.

**Confirmação da Receita Federal, texto literal**, "Perguntas e Respostas IRPF 2026", pergunta **641**:
> "**641 — A isenção relativa às alienações de até R$ 35.000,00 realizadas dentro de um mês pode ser aplicada
> às liquidações ou resgates de aplicações financeiras mantidas no exterior, como por exemplo 'Bonds', contas
> remuneradas, 'Certified Deposits' ou 'Treasuries'?**
> **1. A partir de 1º de janeiro de 2024:** A partir de 1º de janeiro de 2024, a tributação dos rendimentos e
> ganhos de capital em aplicações financeiras no exterior passou a ser regida pelos arts. 3º e 4º da Lei nº
> 14.754, de 12 de dezembro de 2023, **não havendo previsão legal de isenção do imposto sobre a renda da
> pessoa física incidente sobre o ganho de capital auferido na alienação de bens e direitos de pequeno valor.**
> **2. Até 31 de dezembro de 2023:** ... é isento do imposto sobre a renda o ganho de capital auferido na
> liquidação ou resgate de aplicações financeiras mantidas no exterior por pessoa física residente no Brasil,
> desde que o total das operações financeiras realizadas com aplicações de mesma natureza, dentro de um mesmo
> mês, seja igual ou inferior a R$ 35.000,00."

E, na pergunta **640**, a RFB repete: "**Não há previsão legal de isenção do imposto incidente sobre os
rendimentos ou ganhos de capital em aplicações financeiras no exterior.**" A mesma frase aparece nas
perguntas 130 e 642.

**Onde a isenção de R$ 35 mil AINDA vale no exterior:** para **bens e direitos no exterior que NÃO sejam
aplicações financeiras** — art. 2º, § 2º da Lei 14.754 manda esses ao art. 21 da Lei 8.981/1995, e aí a
isenção do art. 22 da Lei 9.250 volta a operar. Imóvel no exterior é o exemplo típico. **Ação e ETF, não.**

**Alíquota do ganho de capital nos casos que permanecem no art. 21 da Lei 8.981/1995** (redação da Lei nº
13.259/2016, texto literal, `https://www.planalto.gov.br/ccivil_03/leis/l8981.htm`, 31/08/2026):
- I — **15%** sobre a parcela dos ganhos que não ultrapassar **R$ 5.000.000,00**
- II — **17,5%** sobre a parcela que exceder R$ 5 milhões e não ultrapassar **R$ 10.000.000,00**
- III — **20%** sobre a parcela que exceder R$ 10 milhões e não ultrapassar **R$ 30.000.000,00**
- IV — **22,5%** sobre a parcela que ultrapassar R$ 30.000.000,00

**Resumo prático:** ganho na venda de ação ou ETF americano = **15% fixos, na DAA, uma vez por ano, sem
isenção de valor, sem faixa progressiva, sem carnê-leão.**

### 3.3 Dividendos de ações americanas

**Tratado Brasil–EUA: NÃO EXISTE.** Fonte primária: IRS, "United States Income Tax Treaties - A to Z"
(`https://www.irs.gov/businesses/international-businesses/united-states-income-tax-treaties-a-to-z`, 31/08/2026).
A lista de países com "B" é literal e completa: **Bangladesh, Barbados, Belarus, Belgium, Bulgaria** — e passa
direto para Canada. **O Brasil não está na lista.**

**Retenção de 30% na fonte nos EUA: NÃO CONFIRMADO em fonte primária.** Não consegui abrir a Publication 515
nem o texto do §1441 do IRC nesta rodada. **Não afirmo o número sem tê-lo lido.** O que está confirmado é a
premissa que o produz (ausência de tratado, portanto ausência de alíquota reduzida por tratado) — não o
percentual estatutário em si.

**Como se declara no Brasil — resposta confirmada: entrou na apuração ANUAL da Lei 14.754. Não é mais
carnê-leão mensal.**

Base legal: art. 3º, § 1º, II da Lei 14.754 lista expressamente **"dividendos"** entre os *rendimentos* de
aplicação financeira no exterior; art. 2º, § 1º manda tributá-los a **15% no ajuste anual**.

Confirmação literal da Receita Federal ("Perguntas e Respostas IRPF 2026", seção sobre entidades no exterior):
> "**2. Entidades não controladas no exterior** — Os lucros e dividendos recebidos de entidades não
> controladas no exterior são tributados **como rendimentos de aplicações financeiras no exterior**. São
> computados na DAA e submetidos à incidência do IRPF, **à alíquota de 15%**, no período de apuração em que
> forem efetivamente percebidos pela pessoa física, como no recebimento de juros e outras espécies de
> remuneração."

Uma ação da Apple ou da Microsoft é participação em **entidade não controlada** — logo, dividendo dela é
rendimento de aplicação financeira, 15%, anual, na DAA.

**Aproveitamento do imposto retido nos EUA — confirmado.** A RFB, pergunta **140**, texto literal:
> "1. A partir de 01/01/2024, no caso de imposto sobre a renda pago sobre a tributação dos rendimentos e
> ganhos de capital ... de aplicações financeiras no exterior: As pessoas físicas poderão deduzir do Imposto
> sobre a Renda da Pessoa Física – IRPF devido o imposto sobre a renda pago no país de origem dos rendimentos,
> desde que: I – esteja prevista a compensação em acordo, tratado e convenção internacionais ...; ou
> **II – haja reciprocidade de tratamento** em relação aos rendimentos produzidos no País."

E, decisivo — RFB, pergunta 136, texto literal:
> "**Não é necessária a prova de reciprocidade para a Alemanha, o Reino Unido e os Estados Unidos da América**"

→ **Não há tratado, mas há reciprocidade reconhecida com os EUA, e a RFB dispensa a prova dela.** O imposto
retido nos EUA sobre dividendos é, portanto, dedutível do IRPF devido — limitado (art. 4º, § 1º) à diferença
entre o IRPF com e sem a inclusão do rendimento, e **sem** transporte para outros anos (art. 4º, § 4º).
Na prática, sendo a alíquota americana sobre dividendos maior que os 15% brasileiros, o excedente **se perde**.

Onde declarar: no **Quadro "Aplicação Financeira (R$)"** da ficha de Bens e Direitos, campo
**"Imposto pago no Exterior"** (RFB, pergunta 474).

### 3.4 Variação cambial

Três regimes distintos, todos confirmados:

**(i) Variação cambial embutida em aplicação financeira — TRIBUTADA a 15%, na realização.**
Art. 3º, § 1º, II da Lei 14.754 inclui expressamente "variação cambial da moeda estrangeira" entre os
rendimentos. Art. 3º, § 2º: tributa "inclusive de variação cambial sobre o principal, no resgate, na
amortização, na alienação, no vencimento ou na liquidação". Ou seja: se o dólar subiu enquanto você segurava
o ETF, essa valorização em reais entra na base dos 15% quando você vender.

**(ii) Conta-corrente e cartão NÃO remunerados — NÃO TRIBUTADA, sem limite de valor.**
Art. 2º, § 3º (literal, transcrito em 3.1). A RFB confirma e vai além, na pergunta **469**:
> "A variação cambial de depósitos em conta-corrente ou em cartão de débito ou crédito no exterior não ficará
> sujeita à incidência do IRPF, desde que os depósitos não sejam remunerados e sejam mantidos em instituição
> financeira no exterior reconhecida e autorizada a funcionar pela autoridade monetária do país em que
> estiver situada. **Também não está sujeita à incidência do IRPF a utilização, inclusive o saque em espécie,
> dos recursos financeiros do depósito em moeda estrangeira em conta-corrente ou em cartão de débito ou
> crédito no exterior.**"
> **Atenção ao requisito: "não sejam remunerados".** Conta que rende juros deixa de se enquadrar aqui e passa
> a ser aplicação financeira (art. 3º, § 1º, I: "contas-correntes com rendimentos").

**(iii) Moeda estrangeira em ESPÉCIE — isenta até US$ 5.000 de alienação por ano.**
Art. 2º, § 4º e § 5º da Lei 14.754. RFB, pergunta **472**, literal:
> "Os valores isentos decorrentes da não incidência do IRPF sobre a variação cambial de moeda estrangeira em
> espécie **até o limite de alienação de moeda no ano-calendário equivalente a US$ 5.000,00** ... devem ser
> informados na ficha **Rendimentos Isentos e Não Tributáveis**. Caso, no ano-calendário, o valor da alienação
> de moeda estrangeira em espécie **exceder** o valor de US$ 5.000,00, deve ser apurado o ganho de capital
> sobre a variação cambial, **na forma do art. 21 da Lei nº 8.981**, utilizando o Programa de Apuração dos
> Ganhos de Capital - **GCAP – Moedas em Espécie**."

Custo de aquisição da moeda em espécie: **custo médio ponderado** — "resultado da divisão do valor total, em
reais, pago nas aquisições pela quantidade de moeda estrangeira existente" (RFB, perguntas 472 e 643).
RFB, pergunta 643, literal: "Os ganhos em reais obtidos na alienação de moeda estrangeira mantida em espécie
estão sujeitos à **tributação definitiva, sob a forma de ganho de capital**."

### 3.5 Come-cotas e tributação periódica

- **Ativos no exterior detidos diretamente (ações, ETFs, bonds):** **não há come-cotas nem qualquer
  tributação periódica.** O art. 3º, § 2º da Lei 14.754 é explícito: tributa-se "no período de apuração em
  que forem **efetivamente percebidos**" e, quanto aos ganhos, "no resgate, na amortização, na alienação, no
  vencimento ou na liquidação". Enquanto você não vende e não recebe, não há fato gerador.
- **Entidades controladas no exterior (offshore):** **há tributação periódica anual, não come-cotas.**
  Art. 5º, caput: os lucros "serão tributados **em 31 de dezembro de cada ano**", à alíquota de 15%
  (art. 2º, § 1º), **independentemente de distribuição**. A RFB, pergunta 475, confirma: "O lucro apurado por
  entidade controlada no exterior sujeita ao Regime de Tributação Anual dos Lucros ... tributado na
  Declaração de Ajuste Anual – DAA **à alíquota de 15%, independentemente de qualquer deliberação acerca da
  sua distribuição**". Esse lucro já tributado vai para a ficha de Bens e Direitos, **Grupo 05 – Créditos,
  Código 99 – Outros créditos**, como crédito de dividendo a receber.
- **Fundos de investimento NO PAÍS:** o art. 17 da Lei 14.754 institui a retenção do IRRF "nas seguintes
  datas". **As datas específicas eu não extraí do texto — NÃO CONFIRMADAS.** (Registro para não induzir erro:
  a Lei 14.754 tem dois capítulos distintos; o come-cotas do Capítulo II é sobre fundos brasileiros, não
  sobre investimento no exterior. Confundir os dois é o erro mais comum na leitura dessa lei.)

### 3.6 Compensação de prejuízo

Confirmada em duas fontes. Lei 14.754, art. 9º (transcrito na íntegra em 3.1) e RFB, pergunta **476**, literal:
> "**Sim.** A pessoa física residente no País poderá compensar as perdas realizadas em aplicações financeiras
> no exterior na seguinte ordem:
> **I** - rendimentos auferidos em aplicações financeiras no exterior, na Declaração de Ajuste Anual, **no
> mesmo período de apuração**;
> **II** - caso o valor das perdas no período de apuração supere o dos ganhos, esta parcela das perdas poderá
> ser compensada com **lucros e dividendos de entidades controladas no exterior** que tenham sido computados
> na Declaração de Ajuste Anual no mesmo período de apuração; e
> **III** - caso no final do período de apuração haja acúmulo de perdas não compensadas, essas perdas poderão
> ser compensadas com rendimentos computados na Declaração de Ajuste Anual em **períodos de apuração
> posteriores**.
> **As perdas poderão ser compensadas uma única vez.**
> **Atenção:** A compensação de perdas deve ser comprovada por **documentação hábil e idônea**. Os prejuízos
> de controladas no exterior que não estejam sujeitas aos regimes de tributação da Lei nº 14.754, de 2023,
> não são passíveis de serem deduzidos de outros rendimentos."

**Diferença estrutural em relação ao Brasil:** aqui a compensação é **anual e dentro da própria ficha**, sem
a separação por "mesma espécie de operação" e sem o controle mês a mês do mercado brasileiro. É mais simples
e mais generosa. O limite real é o "**uma única vez**" do § 3º.

### 3.7 Como declarar a conta em corretora estrangeira

Tudo abaixo é texto literal da RFB, "Perguntas e Respostas IRPF 2026" (PDF de 340 páginas, versão
v1.00 de 23/04/2026, acessado 31/08/2026).

**Conta corrente NÃO remunerada no exterior — pergunta 469:**
> "O depósito não remunerado mantido em instituições financeiras no exterior deve ser informado na ficha de
> Bens e Direitos, no **Grupo 06 – Depósito à Vista e Numerário** e no **Código 01 – Depósito em conta corrente
> ou conta pagamento**. **Informar o País onde a conta está localizada.**
> No campo 'Discriminação' informar: dados bancários (Banco, agência quando houver, número da conta,
> titularidade, se exclusiva ou conjunta); o valor em moeda estrangeira; o valor convertido em reais pela
> cotação de fechamento da moeda estrangeira divulgada, **para a venda**, pelo Banco Central do Brasil, para
> a data do fato gerador (depósito); se a conta não remunerada é detida por meio de um trust no exterior ou
> por meio de uma entidade controlada ...
> No campo 'Situação em 31/12/2025 (R$)', informar o saldo existente em 31/12/2025, convertido em reais pela
> **cotação de fechamento da moeda estrangeira divulgada, para venda, pelo Banco Central do Brasil, em 31 de
> dezembro de 2025**."

**Aplicações financeiras no exterior (ações, ETFs) — pergunta 474:**
> "As aplicações financeiras fora do País devem ser declaradas na ficha de Bens e Direitos **no respectivo
> Grupo e Código** e deve ser informado: a) se o bem ou direito pertence ao Titular ou ao Dependente;
> b) **o país onde se localiza**; c) no campo 'Discriminação': **a data da aplicação; o tipo da aplicação;
> o valor em moeda estrangeira; a cotação utilizada para conversão em reais**; se a aplicação financeira é
> detida por meio de um trust ... e outras informações relevantes.
> No campo 'Situação em 31/12/2025 (R$)', informe **o valor do custo da aplicação financeira em reais**,
> existente em 31/12/2025, cujo saldo deve ser ajustado a cada aplicação, liquidação ou resgate realizado no
> ano-calendário de 2025.
> **Para a conversão em reais deve ser utilizada a cotação de fechamento da moeda estrangeira divulgada para
> venda pelo Banco Central do Brasil – BCB, para a data do fato gerador (aquisição).**
> **Quadro Aplicação Financeira (R$):** No campo '**Rendimento ou Perda**' informe o valor do rendimento ou
> da perda ... que deverá ser submetido à incidência do IRPF na DAA, **à alíquota de 15%** ... hipótese em que
> **não será aplicada nenhuma dedução na base de cálculo**.
> No campo '**Imposto pago no Exterior**' deve ser informado o valor do imposto pago no exterior sobre os
> rendimentos informados no campo 'Rendimentos ou Perdas' e que sejam passíveis de serem deduzidos do imposto
> devido no Brasil."

**Ponto importante que muita gente erra:** o campo "Situação em 31/12" é o **CUSTO em reais** pela cotação da
**data da aquisição** — **não** é o valor de mercado convertido pelo dólar de 31/12. O saldo só muda quando
há aplicação, liquidação ou resgate.

**Cotação a usar — resumo confirmado:**
| Finalidade | Cotação |
|---|---|
| Converter valores em geral (fato gerador) | fechamento **para VENDA** do BCB, data do fato gerador (Lei 14.754, art. 15) |
| Custo de aquisição de aplicação financeira | fechamento **para VENDA** do BCB, data da aquisição (RFB 474) |
| Saldo de conta não remunerada em 31/12 | fechamento **para VENDA** do BCB em 31 de dezembro (RFB 469) |
| Imposto pago no exterior | fechamento **para COMPRA** do BCB, dia do pagamento do imposto (Lei 14.754, art. 4º, § 2º) |
| Alienação de moeda em espécie | fechamento **para VENDA** do BCB, data da alienação (RFB 472/643) |
| Bens e direitos adquiridos no exterior | converter para USD pela autoridade monetária do país emissor na data da aquisição e, em seguida, para reais pela cotação do dólar **para VENDA** do BCB na data da aquisição (RFB 479) |

**Grupo/código exato para AÇÃO e ETF no exterior: NÃO CONFIRMADO.** A pergunta 474 diz apenas "no respectivo
Grupo e Código" e não abre a tabela. Confirmei apenas: Grupo 06/Código 01 para conta não remunerada (RFB 469);
Grupo 03 – Participações Societárias para **entidades controladas** (RFB 475); Grupo 05/Código 99 para o
crédito de lucro previamente tributado de controlada (RFB 475).

**Obrigatoriedade de entregar a DAA** — RFB, "Perguntas e Respostas IRPF 2026", texto literal dos itens que
interessam ao investidor no exterior:
> "**6** - teve, em 31 de dezembro, a posse ou a propriedade de bens ou direitos, inclusive terra nua, de valor
> total superior a **R$ 800.000,00** (oitocentos mil reais);
> **9** - optou por declarar os bens, direitos e obrigações detidos pela entidade controlada ... no exterior
> como se fossem detidos diretamente pela pessoa física (Regime de Transparência Fiscal, art. 8º da Lei nº 14.754);
> **10** - teve, em 31 de dezembro, a titularidade de trust ...;
> **11** - relativamente ao capital investido em **aplicações financeiras no exterior**, a que se referem os
> arts. 2º a 4º e 9º da Lei nº 14.754 ...: **a) auferiu rendimentos ou ganhos de capital; ou b) pretenda
> compensar, no ano-calendário de 2025 ou posteriores, perdas de anos-calendário anteriores ou do próprio
> ano-calendário de 2025**;
> **12** - auferiu lucros ou dividendos de entidades no exterior, nos termos dos arts. 2º e 5º a 6º-A da Lei
> nº 14.754."

→ **Um único dividendo recebido no exterior já obriga a entregar a DAA**, mesmo sem qualquer outro critério.
E **querer compensar prejuízo** também obriga — item 11, "b".

### 3.8 CBE — Declaração de Capitais Brasileiros no Exterior (Banco Central)

**Status: PARCIAL. Só obtive fonte secundária. O texto normativo primário NÃO FOI OBTIDO.**

Dados obtidos (`https://smabr.com/declaracao-de-capitais-brasileiros-no-exterior-2026-cbe/`,
escritório de advocacia, acessado 31/08/2026), texto literal:
- Norma: "**Resolução nº 279/2022** ('RN 279/2022') do Banco Central do Brasil ('BACEN'), que regulamenta a
  **Lei nº 14.286/2021**"
- **CBE Anual:** obrigatória para "Valores superiores a **US$1.000.000,00**" (data-base 31/12)
- **CBE Trimestral:** "Valores superiores a **US$100.000.000,00**"
- Prazos 2026 (ano-base 2025): **Anual — "15 de fevereiro até às 18 horas do dia 5 de abril de 2026"**;
  Trimestral (base 31/março) — "30 de abril à 5 de junho de 2026"; (base 30/junho) — "31 de julho à 5 de
  setembro de 2026"; (base 30/setembro) — "31 de outubro a 5 de dezembro de 2026"
- Multa: "entre **R$2.500,00** ... e **R$250.000,00** ... podendo ser majoradas em 50% em alguns casos"

**Por que não confirmei na fonte primária:** `https://www.bcb.gov.br/estabilidadefinanceira/cbe` e
`https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=279` retornam página
que **exige JavaScript** ("Essa pagina depende do javascript para abrir"); a API de conteúdo do BCB retornou
HTTP 400; `normativos.bcb.gov.br` retornou 404; a busca no DOU (`in.gov.br`) não retornou o ato.
**Portanto: os valores de US$ 1 milhão / US$ 100 milhões e os prazos acima estão CONFIRMADOS apenas em fonte
secundária.** Recomendo confirmar no BCB antes de agir.

**Ponto prático:** o limite anual de **US$ 1 milhão** é muito alto. **A maioria esmagadora dos investidores
pessoa física NÃO precisa entregar CBE.** A obrigação acessória que efetivamente pega todo mundo é a **DAA**
(item 11 acima — basta um dividendo). Confundir CBE com "declaração obrigatória de quem tem conta lá fora" é
erro comum e superestima o custo de complexidade da rota estrangeira.

---

## 4. COMPARAÇÃO — IVVB11 vs. ETF americano via conta no exterior

### 4.1 O que está confirmado e o que não está

| Parâmetro | Valor | Status |
|---|---|---|
| Taxa de administração do **IVVB11** | 0,23% a.a. (premissa fornecida no pedido) | **NÃO CONFIRMADO** — ver 4.4 |
| Expense ratio do **IVV / VOO** | 0,03% a.a. (premissa fornecida no pedido) | **NÃO CONFIRMADO** — ver 4.4 |
| **Existência de BDR de ETF** | **Existe.** B3 mantém a página de produto "Brazilian Depositary Receipts - BDRs de ETF" e há BDR de ETF de renda fixa. Identifiquei o ticker **BIVB39** descrito como "iShares Core S&P 500 BDR ETF" — ou seja, **BDR do próprio IVV**. | **PARCIAL** — títulos e URLs localizados; páginas não abertas; taxa do BDR **NÃO CONFIRMADA** |
| **Custo de entrada da rota estrangeira** | confirmado por plataforma — ver 4.2 | **COMPLETO** |
| Tributação da rota estrangeira | 15% na DAA, anual, sem isenção | **COMPLETO** (seção 3) |
| Tributação de ETF no Brasil | **NÃO CONFIRMADO** — ver 4.4 | **NÃO OBTIDO** |
| Custo em horas das obrigações acessórias | **NÃO CONFIRMADO** — não existe fonte para isso | — |

### 4.2 O custo de entrada, medido

Este é o número que a rota estrangeira paga **uma vez**, na entrada, e que precisa ser amortizado. Todos os
componentes abaixo são confirmados nas seções 1 e 2:

| Rota | Spread declarado | IOF (art. 15-B, XXI-A) | **Custo de entrada** |
|---|---|---|---|
| **Vest — PIX** | 1,85% | 1,10% | **2,95%** |
| **Vest — stablecoin** | 1,40% | não se aplica (declarado) | **1,40%** |
| **Avenue — melhor degrau** | 0,50% | 1,10% | **1,60%** |
| **Avenue — degrau inicial** | 1,95% | 1,10% | **3,05%** |
| **Nomad — nível 5** | 1,00% | 1,10% | **2,10%** |
| **Nomad — nível 1** | 2,00% | 1,10% | **3,10%** |
| **Genial** | 2,00% | NÃO CONFIRMADO | ≥ 2,00% |
| **BTG US** | até 2,00% | NÃO CONFIRMADO | ≥ 2,00% |
| **Wise** (rota de conta, medida ao vivo) | 0,7253% | 3,50% (medido) | **4,2253%** |

Duas leituras que saltam desta tabela:

1. **O IOF é hoje o maior componente do custo de entrada em várias rotas.** Na Wise, os 3,5% de IOF são
   **4,8 vezes** a tarifa da própria Wise. Enquadrar a remessa no inciso XXI-A (1,10%) em vez do XXI (3,5%)
   vale mais do que qualquer negociação de spread.
2. **A dispersão entre plataformas é de mais de 2 pontos percentuais** (1,60% na Avenue no melhor degrau vs.
   4,23% na Wise como conta). Isso é equivalente a **anos** de diferença de taxa de administração.

### 4.3 A conta do ponto de equilíbrio

**Modelo.** Seja:
- `E` = custo de entrada, em % do aporte (spread + IOF) — **confirmado**, tabela 4.2
- `Δ` = diferença anual de taxa de administração entre o ETF brasileiro e o americano, em pontos percentuais
  ao ano — **NÃO CONFIRMADO** (ver 4.4)
- `S` = saída, se e quando repatriar: IOF de **0,38%** (art. 15-B, XXV) + spread de volta

Ignorando juros compostos (aproximação conservadora que **favorece** a rota estrangeira, pois `Δ` incide
sobre patrimônio crescente), o número de anos para o ganho de taxa pagar o custo de entrada é:

```
                    E
   T (anos)  =  ─────────
                    Δ
```

**Aplicando os custos de entrada confirmados**, com `Δ` deixado como variável (porque não confirmei as taxas):

| Rota (E confirmado) | Δ = 0,10 p.p. | Δ = 0,20 p.p. | Δ = 0,30 p.p. | Δ = 0,50 p.p. |
|---|---|---|---|---|
| Avenue melhor degrau (1,60%) | 16,0 anos | 8,0 anos | 5,3 anos | 3,2 anos |
| Vest stablecoin (1,40%) | 14,0 anos | 7,0 anos | 4,7 anos | 2,8 anos |
| Nomad nível 5 (2,10%) | 21,0 anos | 10,5 anos | 7,0 anos | 4,2 anos |
| Vest PIX (2,95%) | 29,5 anos | 14,8 anos | 9,8 anos | 5,9 anos |
| Avenue degrau inicial (3,05%) | 30,5 anos | 15,3 anos | 10,2 anos | 6,1 anos |
| Nomad nível 1 (3,10%) | 31,0 anos | 15,5 anos | 10,3 anos | 6,2 anos |
| Wise como conta (4,23%) | 42,3 anos | 21,1 anos | 14,1 anos | 8,5 anos |

**Se as premissas do pedido (0,23% e 0,03%) se confirmarem, Δ = 0,20 p.p.** — a coluna do meio. Nesse
cenário, o ponto de equilíbrio de tempo fica entre **7 e 21 anos**, conforme a plataforma e o degrau de spread.

**Sobre "a partir de qual patrimônio compensa":**

Aqui é preciso ser honesto sobre a estrutura do problema, porque a pergunta contém uma armadilha.
**Tanto `E` quanto `Δ` são percentuais.** O custo de entrada é proporcional ao aporte e a economia de taxa
é proporcional ao patrimônio. **Elas escalam juntas.** Logo, **o ponto de equilíbrio NÃO depende do
patrimônio — depende do HORIZONTE.** Dobrar o patrimônio dobra o custo de entrada e dobra a economia anual;
o `T` não se move.

O patrimônio só entra na conta por **dois** canais, e ambos são custos **fixos em dólar**, não percentuais:

1. **Corretagem fixa por ordem.** Avenue cobra US$ 2,50 a US$ 10,00 por ordem (com até 10 grátis/mês);
   BTG via DriveWealth, US$ 1,00 a US$ 7,50. Nomad, Inter, Vest e Schwab cobram **US$ 0**. Numa plataforma de
   corretagem zero, esse canal **desaparece** e o patrimônio deixa de importar por completo.
2. **O custo em horas da obrigação acessória**, que é fixo por ano independentemente do valor.
   **Esse é o único canal em que o patrimônio realmente decide** — e é justamente o que **não tem fonte**.

**Portanto, a formulação correta do critério de decisão é:**

> A rota estrangeira compensa a partir de um **HORIZONTE** (`T = E / Δ` anos), não a partir de um patrimônio.
> O patrimônio só decide se o custo **fixo** anual (horas de declaração + eventual corretagem por ordem)
> ficar diluído: economia anual em reais = `Δ × patrimônio`. Para que essa economia cubra um custo fixo `C`
> por ano, é preciso `patrimônio > C / Δ`.
> Com `Δ = 0,20 p.p.`, cada **R$ 100.000** investidos geram **R$ 200/ano** de economia de taxa.
> **Se você valoriza em mais de R$ 200/ano o trabalho anual de declarar, R$ 100 mil não compensa.**
> **NÃO ATRIBUO um valor a esse trabalho** — não há fonte, e estimá-lo seria exatamente o que esta pesquisa
> se proibiu de fazer. Quem decide é o leitor, com o seu próprio número.

**O que a conta revela, e que costuma ser omitido no debate:**

- **O custo de entrada domina o primeiro decênio.** Em quase toda combinação realista, o investidor passa
  **mais de 5 anos** apenas pagando de volta o spread e o IOF. Quem entra e sai, ou quem aporta mensalmente
  pagando spread a cada aporte, **nunca** atinge o ponto de equilíbrio — o `E` é recobrado em cada aporte.
- **A escolha da plataforma pesa mais que a escolha do ETF.** A diferença entre o melhor degrau da Avenue
  (1,60%) e a Wise como conta (4,23%) é de **2,63 pontos percentuais** de entrada. Com `Δ = 0,20 p.p.`, isso
  são **13 anos** de diferença no ponto de equilíbrio — muito mais do que a diferença entre IVVB11 e IVV.
- **Enquadrar a remessa como investimento (1,10%) e não como conta (3,5%)** economiza 2,40 p.p. — sozinho,
  isso vale **12 anos** de diferença de taxa de administração com `Δ = 0,20 p.p.`
- **A conta de ida e volta é pior que a de ida.** Repatriar custa mais **0,38%** de IOF (inciso XXV,
  confirmado) mais o spread de volta. Se o horizonte inclui repatriação, `E` deve incluir `S`.

**Ressalva metodológica explícita:** os valores de `T` nas tabelas acima são **aritmética sobre `Δ` hipotético**,
não resultado de pesquisa. O único elemento pesquisado e confirmado é `E`. **Se `Δ` for menor que 0,20 p.p.
— por exemplo, se a taxa real do IVVB11 for inferior a 0,23% — todos os prazos aumentam proporcionalmente.**

### 4.4 O que não confirmei nesta comparação, e por quê

- **Taxa de administração do IVVB11: NÃO CONFIRMADO.** Localizei as URLs da fonte primária (página do fundo
  na BlackRock Brasil, fact sheet PDF, regulamento PDF, demonstrações financeiras 2024 PDF) mas **os
  downloads falharam**: a ferramenta de fetch com renderização atingiu limite de sessão e o sandbox de shell
  passou a recusar comandos de forma intermitente. **Não uso 0,23% como confirmado** — é premissa do pedido.
- **Expense ratio do IVV / VOO: NÃO CONFIRMADO.** Mesma causa. A página do iShares não foi aberta.
- **Tributação de ETF de índice no Brasil: NÃO CONFIRMADO.** Não verifiquei nesta rodada se a isenção mensal
  de R$ 20.000 em bolsa alcança ou não os ETFs, nem a alíquota aplicável. É um ponto **decisivo** para a
  comparação — porque, se o ETF brasileiro não tem isenção e é tributado a 15% como o estrangeiro, a
  vantagem tributária da rota doméstica desaparece e sobra só a simplicidade acessória. **Deixo em aberto.**
- **Taxa do BDR de ETF (BIVB39): NÃO CONFIRMADO.**
- **"Sem obrigação acessória" para IVVB11:** essa parte é **confirmável por dedução das fontes que li** —
  a Lei 14.754 e as perguntas 469/474/476 da RFB tratam de bens e aplicações **no exterior**; IVVB11 é fundo
  brasileiro, negociado na B3, e não entra nessa ficha. O item 11 da obrigatoriedade da DAA (aplicações
  financeiras no exterior) não o alcança. **Isso está correto pelas fontes lidas.**

---

## 5. O ARGUMENTO NÃO-FINANCEIRO — status

**(a) Casos históricos de confisco ou bloqueio no Brasil — Plano Collor, 1990: NÃO CONFIRMADO.**

Localizei os instrumentos normativos e suas URLs — **Lei nº 8.024, de 12 de abril de 1990**
(`http://www.planalto.gov.br/ccivil_03/leis/l8024.htm`), **Medida Provisória nº 168, de 1990**
(`https://www.planalto.gov.br/ccivil_03/mpv/1990-1995/168.htm`) e MP nº 180, de 17/04/1990 — mas
**não consegui abrir e ler nenhum desses textos**: as tentativas de download ocorreram já depois da queda
do sandbox de shell, e todas foram recusadas.

**Portanto não descrevo o que foi bloqueado, qual o limite em cruzados novos, o que ficou de fora, o prazo
de retenção, nem a forma de devolução.** Descrever isso de memória seria exatamente a estimativa que esta
pesquisa se proibiu. **NÃO OBTIDO — a lacuna fica declarada.**

**(b) Evidência sobre eficácia de custódia estrangeira nesses cenários: NÃO OBTIDO.** Não pesquisei.

**(c) Custo real dessa proteção em taxa e complexidade — ESTE está confirmado**, e é a parte do argumento
não-financeiro que a pesquisa efetivamente entrega:

- **Custo de entrada:** de **1,60%** (Avenue no melhor degrau) a **4,23%** (Wise como conta) do capital,
  pago **na entrada** e **de novo a cada aporte**. Ver tabela 4.2.
- **Custo de saída:** IOF de **0,38%** (art. 15-B, XXV, confirmado) mais spread de volta.
- **Custo recorrente:** varia de **US$ 0** (Nomad, Inter, Vest, Schwab, IBKR: corretagem zero e sem taxa de
  manutenção) até **US$ 250 por trimestre** (BTG via Pershing, abaixo de US$ 500k) e **3% a 5% por ordem**
  (BTG via Pershing) — uma dispersão enorme, que a escolha de plataforma resolve.
- **Custo tributário:** **15% sobre todo o ganho, sem isenção de valor** (Lei 14.754, art. 2º, § 1º; RFB 640
  e 641). No exterior **não existe** o equivalente à isenção mensal de R$ 20 mil da bolsa brasileira. Em
  compensação: apuração **anual** (não mensal), compensação de prejuízo mais simples, alíquota fixa que não
  sobe com o volume, e **nenhuma tributação até a realização** — sem come-cotas.
- **Custo de complexidade — menor do que a fama.** A CBE só é obrigatória acima de **US$ 1 milhão** (fonte
  secundária), o que dispensa a esmagadora maioria. O que realmente pega é a **DAA**: basta **um dividendo
  recebido** para a entrega virar obrigatória (item 11 da obrigatoriedade), e o preenchimento exige controlar
  custo médio em reais pela cotação de VENDA do BCB da data de **cada** aquisição (RFB 474). É trabalhoso,
  mas é anual e determinístico.
- **E o custo que ninguém contabiliza:** **o risco de jurisdição que se está tentando evitar reaparece pela
  porta dos fundos em 4 das 10 plataformas.** Avenue (Itaú), Inter US (Inter&Co), BTG US (Banco BTG Pactual
  S.A.) e XP US (grupo XP) têm controlador ou grupo brasileiro. Pelo critério estrito — custódia fora, em
  instituição sem vínculo com o Brasil — **pagar 1,60% a 3,10% de entrada numa dessas não compra a proteção
  de jurisdição que se pretendia comprar**; compra conveniência, atendimento em português e facilidade de
  câmbio. Quem quer o critério estrito tem, nesta lista, essencialmente **IBKR** (limpa, mas sem facilitação
  de câmbio no Brasil), **Schwab** (se elegível — não confirmado), e **Nomad**/**Vest** com a ressalva de que
  a custódia é independente (Apex, Northbound) mas a distribuição e a remessa passam por instituições brasileiras.

---

## 6. REGISTRO DE FONTES

Todas as consultas em **31/08/2026 (UTC)**.

### Legislação e normas — fonte primária

| Fonte | URL | Status |
|---|---|---|
| Decreto 6.306/2007 (Regulamento do IOF), texto compilado — art. 15-B e art. 15-C na íntegra | `https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/decreto/d6306.htm` | **COMPLETO** |
| Decreto 12.499/2025 — publicação original | `https://www2.camara.leg.br/legin/fed/decret/2025/decreto-12499-11-junho-2025-797588-publicacaooriginal-175631-pe.html` | **COMPLETO** |
| Lei 14.754/2023 — arts. 1º a 9º, 15, 46, 47 | Planalto (arquivo lido integralmente) | **COMPLETO** |
| MP 2.158-35/2001, art. 24 e §§ (incl. §6º) e art. 28 — com marca "(Revogado pela Lei nº 14.754, de 2023)" | `https://www.planalto.gov.br/ccivil_03/mpv/2158-35.htm` | **COMPLETO** |
| Lei 9.250/1995, art. 22 (isenção R$ 20.000 / R$ 35.000) | `https://www.planalto.gov.br/ccivil_03/leis/l9250.htm` | **COMPLETO** |
| Lei 8.981/1995, art. 21 (15% / 17,5% / 20% / 22,5%) | `https://www.planalto.gov.br/ccivil_03/leis/l8981.htm` | **COMPLETO** |
| RFB — "Perguntas e Respostas IRPF 2026", v1.00 de 23/04/2026, PDF 340 páginas. Perguntas lidas na íntegra: 130, 136, 140, 469, 472, 474, 475, 476, 479, 640, 641, 642, 643, e a lista de obrigatoriedade da DAA | `https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/perguntas-e-respostas/dirpf/p-r-irpf-2026-v1-00-2026-04-23.pdf` | **COMPLETO** |
| IRS — lista de tratados de imposto de renda dos EUA (Brasil ausente) | `https://www.irs.gov/businesses/international-businesses/united-states-income-tax-treaties-a-to-z` | **COMPLETO** |
| **STF — inteiro teor da ADC nº 96** | — | **NÃO OBTIDO** — não pesquisado; a existência foi lida na marca "(Vide ADC nº 96)" do compilado do Planalto |
| **Regulamentação da RFB sobre o inciso XXI-A do art. 15-B** | — | **NÃO OBTIDO** — não localizada |
| **Resolução BCB nº 279/2022 (CBE) — texto normativo** | `https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=279` | **NÃO OBTIDO** — a página do BCB exige JavaScript ("Essa pagina depende do javascript para abrir"); API de conteúdo do BCB retornou HTTP 400; `normativos.bcb.gov.br/.../Res_279_v1_O.pdf` retornou 404; busca no DOU (`in.gov.br`) não retornou o ato; legisweb exige assinatura |
| CBE — valores, prazos 2026 e multas (**fonte secundária**) | `https://smabr.com/declaracao-de-capitais-brasileiros-no-exterior-2026-cbe/` | **PARCIAL** |
| Instrução Normativa RFB 2.180/2024 — texto integral | — | **NÃO OBTIDO** — citada extensivamente pela RFB nas Perguntas e Respostas, mas não li o texto próprio |
| **Lei 8.024/1990 e MP 168/1990 (Plano Collor)** | `http://www.planalto.gov.br/ccivil_03/leis/l8024.htm` · `https://www.planalto.gov.br/ccivil_03/mpv/1990-1995/168.htm` | **NÃO OBTIDO** — URLs localizadas; downloads recusados pela indisponibilidade intermitente do sandbox de shell |
| IRS — retenção de 30% em dividendos (Pub. 515 / IRC §1441) | — | **NÃO OBTIDO** — limite de sessão da ferramenta de fetch |

### Dados de mercado — medições ao vivo

| Fonte | URL / método | Status |
|---|---|---|
| Wise — cotação BRL→USD, tarifa e IOF, 31/08/2026 17:55 UTC | `POST https://wise.com/gateway/v3/quotes/` | **COMPLETO** |
| Wise — cotação mid-market ao vivo | `https://wise.com/rates/live?source=BRL&target=USD` | **COMPLETO** |
| Banco Central — PTAX USD, 25 a 31/08/2026 | `https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(...)` | **COMPLETO** |
| FINRA BrokerCheck — Avenue Securities LLC (CRD 292589): razão social, SEC nº, estado, datas, endereço, *direct owners*, disclosures | `https://api.brokercheck.finra.org/search/firm/292589` | **COMPLETO** |

### Plataformas

| Fonte | URL | Status |
|---|---|---|
| Avenue — custos e taxas | `https://avenue.us/custos/` | **COMPLETO** |
| Avenue — política de câmbio (spread e IOF) | `https://avenue.us/cambio/` | **COMPLETO** |
| Avenue — segurança (FINRA, SIPC, bancos de caixa) | `https://www.avenue.us/seguranca/` | **COMPLETO** |
| **Avenue — clearing/custódia (página Apex)** | `https://avenue.us/apex/` | **NÃO OBTIDO** — página existe (localizada por busca); fetch recusado pela indisponibilidade do sandbox |
| **Itaú — fato relevante sobre a Avenue** | `https://forbes.com.br/forbes-money/2025/12/itau-assume-controle-da-avenue-com-501-do-capital/` | **NÃO OBTIDO** — HTTP 403. O percentual de **50,1%** está confirmado **apenas no título** da reportagem (dez/2025) |
| Nomad — tarifas | `https://www.nomadglobal.com/tarifas-nomad` | **COMPLETO** |
| Nomad — Nomad Pass (escada de spread) | `https://www.nomadglobal.com/nomad-pass` | **COMPLETO** |
| Nomad — investimentos e rodapé regulatório (Apex, SIPC, CVM 33) | `https://www.nomadglobal.com/investimentos` · `https://www.nomadglobal.com/` | **COMPLETO** |
| **Nomad — DTVM parceira e estrutura de controle** | — | **NÃO OBTIDO** |
| Inter — Global Account (tabela com exemplo datado de 01/09/2022) | `https://inter.co/pra-voce/global-account/` | **PARCIAL** — dado desatualizado, marcado como tal |
| Inter — investimentos US (corretagem e manutenção zero) | `https://inter.co/pt/us/investments/` | **COMPLETO** |
| Inter — segurança (DriveWealth, FINRA, SIPC US$500k) | `https://ajuda.inter.co/investimentos/e-seguro-realizar-investimentos-na-plataforma-inter-securities` | **COMPLETO** |
| **Inter — spread cambial vigente em 2026** | `https://ajuda.inter.co/global-account/qual-e-o-spread-da-global-account` | **NÃO OBTIDO** — HTTP 404 |
| IBKR — comissões (stocks/ETFs, mínimos, inatividade) | `https://www.interactivebrokers.com/en/pricing/commissions-home.php` | **COMPLETO** |
| IBKR — comissão de câmbio (0,20 bp, mín. US$2,00) | `https://www.interactivebrokers.com/en/pricing/commissions-spot-currencies.php` | **COMPLETO** |
| IBKR — outras taxas (retiradas) | `https://www.interactivebrokers.com/en/pricing/other-fees.php` | **COMPLETO** |
| **IBKR — entidade aplicável a residentes no Brasil (LLC vs. Ireland)** | `https://www.interactivebrokers.com/pt/general/what-you-need-inv.php` e páginas de disclosure | **NÃO OBTIDO** — página truncada exatamente na seção "Other countries"; demais URLs de disclosure retornaram HTTP 404. Evidência apenas **secundária** (`https://scalpelandstocks.com/how-to-open-interactive-brokers-account-non-us-resident/`, 12–14/04/2026) |
| **IBKR — aceita depósito em BRL de residentes no Brasil?** | — | **NÃO OBTIDO** — redirecionamento para `ibkrcampus.com` não seguido |
| Schwab International — pricing (US$0 equity) e custodiante (Member SIPC) | `https://international.schwab.com/pricing` · `https://international.schwab.com/content/how-to-open-international-account` | **PARCIAL** |
| **Schwab — mínimo de US$25.000 e elegibilidade do Brasil** | `https://www.brokerage-review.com/investing-firm/foreigner/charles-schwab-for-non-us-citizens.aspx` (secundária, "Updated on 12/13/2024") | **PARCIAL** — não confirmado em fonte Schwab |
| XP Investments US — FINRA/NFA/SEC, custódia Pershing ou IBKR, SIPC, mínimos | `https://www.xpi.us/` | **PARCIAL** — corretagem e spread não constam |
| BTG US — tabela de custos (FX até 2%, corretagem, custódia, mínimo, wire) | `https://www.btgpactual.us/pt/fee-schedule/` | **COMPLETO** |
| BTG US — contas internacionais (FINRA/SIPC/NFA, Regent Bank, vínculo com Banco BTG Pactual S.A.) | `https://www.btgpactual.us/pt/international-accounts/` | **COMPLETO** |
| Genial Conta Global — spread 2%/2,5%, sem tarifa de manutenção, FDIC | `https://www.genialinvestimentos.com.br/conta-global/` | **PARCIAL** — broker-dealer, custodiante, SIPC e corretagem ausentes; menção de IOF internamente inconsistente |
| Sproutfi → Vest — site, Northbound Securities LLC, SIPC US$500k, disclosure Oslo Capital DTVM | `https://www.sproutfi.com/` | **COMPLETO** |
| **Vest — tabela de tarifas oficial, cabeçalho "FEE SCHEDULE \| AUGUST 2026"** | `https://storage.googleapis.com/northbound-legal-documents/FeeSchedule_V.02_17_03_2024.pdf` | **COMPLETO** — a fonte de tarifas mais recente e explícita desta pesquisa |
| Vest — depósito via PIX/TED para residentes no Brasil (FacilitaPay; mínimo R$10) | `https://intercom.help/helpvest/en/articles/6544867-deposit-via-pix-or-ted-for-residents-of-brazil` | **PARCIAL** — a página não traz o percentual; o percentual veio da tabela oficial acima |
| Stake — encerramento das operações no Brasil (reclamação de 02/03/2023) | `https://www.reclameaqui.com.br/stake/encerramento-das-operacoes_p9B7lg7goku4h2yf/` | **PARCIAL** — fonte é reclamação de consumidor, não comunicado da empresa |
| Stake — site Brasil | `https://hellostake.com/br` | **HTTP 404** em 31/08/2026 |
| Passfolio | `https://passfolio.com/` | **NÃO OBTIDO** — erro de TLS (`OpenSSL SSL_connect: SSL_ERROR_SYSCALL`) |
| Toro Global | `https://www.toroinvestimentos.com.br/global` · `https://global.toro.com.br/` | **NÃO OBTIDO** — HTTP 403 e falha de túnel do proxy. **Produto não confirmado** |
| Nubank — páginas de conta global / internacional | `https://nubank.com.br/conta-global/` · `https://nubank.com.br/conta-internacional/` | **HTTP 404** — **produto não localizado** |
| Nubank — página de investimentos (sem produto internacional; "Nu Global" é site institucional) | `https://nubank.com.br/investimentos/` | **PARCIAL** |
| **C6 Bank — site institucional e Conta Global** | `https://www.c6bank.com.br/*` | **NÃO OBTIDO** — HTTP 403 em todas as tentativas via shell |
| C6 — spread por faixa (**artigo do blog de 06/05/2024, atualizado 06/11/2024**, anterior aos decretos de 2025) | `https://www.c6bank.com.br/blog/como-pagar-menos-spread-de-cambio` | **PARCIAL** — dados desatualizados, marcados como tais |
| **Wise — disponibilidade de conta de investimento para brasileiros** | — | **NÃO OBTIDO** |

### Comparação IVVB11 / ETF americano

| Fonte | URL | Status |
|---|---|---|
| **IVVB11 — taxa de administração** | `https://www.blackrock.com/br/products/251902/...` · `https://www.blackrock.com/br/literature/fact-sheet/ivvb11-...pdf` · `https://www.blackrock.com/br/literature/bylaws/ishares-ivvb11-brl-regulamento-ptbr.pdf` · `https://www.blackrock.com/br/literature/annual-financial-statements/ishares-ivvb11-brl-demonstrativos-financeiros-2024-ptbr.pdf` | **NÃO OBTIDO** — URLs identificadas; downloads recusados pela indisponibilidade intermitente do sandbox de shell e pelo limite de sessão da ferramenta de fetch |
| **IVV — expense ratio** | `https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf` | **NÃO OBTIDO** — limite de sessão da ferramenta de fetch |
| BDR de ETF — existência e produto | `https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/brazilian-depositary-receipts-bdrs-de-etf.htm` · `https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-fixa/brazilian-depositary-receipts-bdrs-de-etf-de-renda-fixa.htm` | **PARCIAL** — URLs e ticker **BIVB39** ("iShares Core S&P 500 BDR ETF") identificados por busca; páginas não abertas; taxa não confirmada |
| **Tributação de ETF de índice no Brasil (isenção mensal e alíquota)** | — | **NÃO OBTIDO** — não verificado nesta rodada. **Ponto decisivo para a comparação da seção 4, deixado em aberto** |

---

## 7. RESUMO DAS LACUNAS DECLARADAS

Em ordem de impacto sobre as conclusões:

1. **Tributação de ETF de índice no Brasil** — sem isso, a comparação da seção 4 não fecha do lado doméstico.
2. **Taxa do IVVB11 e expense ratio do IVV** — o `Δ` da conta do ponto de equilíbrio ficou como variável.
3. **Retenção de 30% em dividendos nos EUA** — confirmei a ausência de tratado, não o percentual.
4. **Entidade da IBKR aplicável a brasileiros e aceitação de depósito em BRL** — muda materialmente o custo
   total da rota mais barata da lista.
5. **Texto da Resolução BCB 279/2022 (CBE)** — valores e prazos só em fonte secundária.
6. **Plano Collor (Lei 8.024/1990)** — toda a seção 5(a) ficou sem substância verificada.
7. **Custodiante da Avenue** — a única plataforma (b) cujo clearing não confirmei.
8. **C6 Global e Toro Global** — bloqueio por HTTP 403; C6 ficou com dados de 2024, Toro sem produto confirmado.
9. **Spread vigente do Inter** — o número público está datado de setembro de 2022.
10. **Corretagem e spread da XP US e da Genial** — não publicados nas páginas acessíveis.

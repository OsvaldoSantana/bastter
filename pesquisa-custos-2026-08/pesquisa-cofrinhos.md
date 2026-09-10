# Dossiê da Renda Fixa de Varejo — Brasil, Agosto/2026

**Registro de pesquisa auditável**
**Data de acesso a todas as fontes: 31/08/2026**
**Fontes primárias: BCB · FGC · Tesouro Nacional · B3 · Planalto**

---

## REGRA DE EVIDÊNCIA

Só há número aqui se ele foi lido na fonte citada, na data de acesso indicada. Nada foi estimado, arredondado por conveniência ou inferido de memória. Onde a fonte pública não publica o dado, o campo diz **NÃO CONFIRMADO** — e continua dizendo, mesmo quando o valor "todo mundo sabe". Cálculos derivados (Seção 6) são identificados como cálculo e trazem a fórmula e os insumos.

---

## PARÂMETROS MACROECONÔMICOS VIGENTES

| Indicador | Valor | Fonte / valor literal lido | Data |
|---|---:|---|---|
| Selic meta | **14,00% a.a.** | BCB/SGS série 432, valor literal `14.00` | 31/08/2026 |
| CDI anualizado (base 252) | **13,90% a.a.** | BCB/SGS série 4389, valor literal `13.90` | 28/08/2026 |
| CDI diário | **0,051660% a.d.** | BCB/SGS série 12, valor literal `0.051660` | 28/08/2026 |
| Poupança (período 28/08→28/09/2026) | **0,6455% ao mês** | BCB/SGS série 25, valor literal `0.6455` | 28/08/2026 |
| TR (período 28/08→28/09/2026) | **0,1448% ao mês** | BCB/SGS série 226, valor literal `0.1448` | 28/08/2026 |
| Selic efetiva anualizada | **13,90% a.a.** | BCB/SGS série 1178, valor literal `13.90` | 28/08/2026 |

**URL das séries:** `https://api.bcb.gov.br/dados/serie/bcdata.sgs.<n>/dados/ultimos/1?formato=json`
Acessadas em 31/08/2026. Status: **COMPLETO**

**Consistência conferida:** (1 + 0,1390)^(1/252) − 1 = 0,051658% a.d., que bate com a série 12 (`0.051660`).

---

# SEÇÃO 1 — COFRINHOS, CAIXINHAS E CONTAS REMUNERADAS

O que segue é o que cada instituição *publica no próprio site*. É pouco, e essa escassez é o achado: a maioria das fintechs não divulga publicamente o percentual do CDI, o emissor, a carência ou o teto. Esses dados vivem dentro do aplicativo, atrás de login, e mudam sem aviso. Onde a página oficial não diz, este dossiê não inventa.

## 1.1 Tabela de produtos

### Nubank — Conta
- **URL:** https://nubank.com.br/conta/ — acesso 31/08/2026
- **Rendimento (literal):** "Conta com rendimento diário de 100% do CDI"
- **Condição (literal):** "Todo dinheiro que entra na sua conta e que fica por mais de 30 dias após ser depositado tem rendimento de 100% do CDI todos os dias úteis."
- **Carência (literal):** "No 31º dia após o depósito, você terá à disposição o rendimento retroativo total que esse valor teve nesses 30 primeiros dias." / "Após esse período inicial de 30 dias de seu depósito, o valor passa a render todos os dias úteis, ficando à disposição no saldo da conta."
- **Natureza jurídica e emissor (literal):** "Os RDBs emitidos pela Nu Financeira, a empresa financeira do Nubank, e são considerados um investimento de baixo risco já que têm a cobertura do FGC (Fundo Garantidor de Créditos)."
- **Sobre conta de pagamento (literal):** "Os depósitos em Conta de Pagamentos também são considerados seguros, por serem vinculados e garantidos por títulos públicos do Governo Federal."
- **FGC:** SIM (afirmado na página)
- **IR:** não mencionado explicitamente nesta página
- **Status: COMPLETO**

### Nubank — Caixinhas
- **URL:** https://nubank.com.br/nu/caixinhas — acesso 31/08/2026
- **Rendimento (literal):** "Todas as Caixinhas têm rendimento diário de 100% do CDI"
- **Comparação (literal):** "até 30% a mais que a poupança"
- **Valor mínimo (literal):** "Dá para começar com R$ 1"
- **Liquidez (literal):** "Precisou do dinheiro? É só sacar e o valor cai na hora"
- **FGC (literal):** "Todas as Caixinhas são protegidas pelo FGC, como a poupança tradicional"
- **Taxas (literal):** "As Caixinhas não cobram taxa"
- **IR (literal):** "Você só paga imposto sobre o rendimento, que é descontado automaticamente"
- **Teto:** não publicado
- **Natureza jurídica (RDB/CDB/fundo):** NÃO CONFIRMADO — não especificado na página
- **Status: PARCIAL**

### Nubank — Caixinha Turbo
- **URL:** https://nubank.com.br/nu/caixinhas — acesso 31/08/2026
- **Rendimento (literal):** "rendimento de até 120% do CDI" (clientes NuCel/Nubank Croma) ou "115% do CDI" (com movimentação de R$900)
- **Requisito de ativação (literal):** "Movimente R$900 por mês na conta do Nu"
- **Desbloqueio alternativo (literal):** Clientes "Ultravioleta e Nubank+" têm acesso livre
- **Prazo (literal):** "Você pode consultar a validade da sua Caixinha Turbo no momento da aplicação"
- **Resgate antecipado (literal):** "há o pagamento do Imposto de Renda sobre o rendimento, e também do IOF, caso esse resgate aconteça antes de 30 dias"
- **Emissor, natureza jurídica, teto:** NÃO CONFIRMADO
- **FGC:** presumível (a página cobre "todas as Caixinhas"), mas o emissor da Turbo não é nomeado
- **Status: PARCIAL**

> **NOTA DE CORREÇÃO:** a premissa trazida na pergunta ("110% do CDI com liquidez diária") **não se confirma**. A página oficial publica "até 120% do CDI" / "115% do CDI", e o produto tem **validade** (prazo), não sendo puramente de liquidez diária.

### Mercado Pago — Conta
- **URL:** https://www.mercadopago.com.br/ — acesso 31/08/2026
- **Rendimento (literal):** "Até 105% do CDI na sua Conta"
- **Condições do "até":** NÃO CONFIRMADO (não publicadas na home)
- **Status: PARCIAL**

### Mercado Pago — Cofrinhos
- **URL:** https://www.mercadopago.com.br/ — acesso 31/08/2026
- **Rendimento (literal):** "Até 120% do CDI nos Cofrinhos" / "Rendem até 120% do CDI"
- **Frase completa da home (literal):** "Rendimentos Dinheiro que rende todo dia e está sempre disponível Até 105% do CDI na sua Conta Até 120% do CDI nos Cofrinhos"
- **Natureza jurídica (fonte secundária — Seu Dinheiro, 04/03/2026):** "Não é CDB — os cofrinhos investem em títulos públicos da União — mais especificamente, no Tesouro Selic, oferecendo proteção de risco soberano garantido pelo Governo Federal."
- **Campanha 140% do CDI (fonte secundária, 04/03/2026):**
  - Período: "De 3 de março a 3 de abril de 2026"
  - Elegibilidade: exclusivamente clientes Meli+ (a partir de R$ 9,90/mês)
  - Teto (literal): "A rentabilidade só incide sobre reservas de até R$ 10 mil por CPF." Valores acima retornam a 100% do CDI
  - Sem Meli+: 100% CDI padrão, ou 115% CDI com saldo mínimo de R$ 1 mil (até R$ 5 mil)
  - Pós-campanha: Meli+ recebem 120% CDI para valores até R$ 10 mil
- **FGC:** NÃO (se a estrutura for fundo/Tesouro Selic) — **ver ressalva na Seção 8**
- **Status: PARCIAL**

### PicPay — Conta
- **URL:** https://picpay.com/pt-br/pf/conta-digital — acesso 31/08/2026
- **Rendimento (literal):** "Seu dinheiro rende 102% do CDI todo dia útil" / "Conta digital que rende a 102% do CDI todo dia útil"
- **Confirmação independente:** grep na home https://picpay.com/ retornou a string `102% do CDI`
- **Condições, teto, carência, emissor, FGC, IR:** NÃO CONFIRMADO — a página não traz notas de rodapé nem termos
- **Status: PARCIAL**

### Banco Inter — Meu Porquinho
- **URL:** https://inter.co/pra-voce/investimentos/meu-porquinho/ — acesso 31/08/2026
- **Rendimento (literal):** "Rende muito mais que a Poupança" e "pode render até 100% do CDI"
- **Valor mínimo (literal):** "Guarde a partir de R$ 1,00"
- **Liquidez (literal):** "O dinheiro cai na conta em até 1 dia útil"
- **FGC (literal):** "Fundo Garantidor de Crédito (FGC), que garante até R$ 250.000,00 por CPF/CNPJ" com limite de R$ 1.000.000,00 a cada quatro anos
- **Emissor:** Banco Inter
- **Natureza jurídica (CDB/RDB/fundo):** NÃO CONFIRMADO
- **IR:** não mencionado na página
- **Status: PARCIAL**

### Banco Inter — CDB / LCI / LCA
- **URL:** https://inter.co/pra-voce/investimentos/renda-fixa/ — acesso 31/08/2026
- **CDB (literal):** "É garantido pelo FGC e rende mais do que a poupança. Quanto mais tempo deixar investido, maior será o rendimento e a alíquota do IR irá diminuir."
- **LCI (literal):** "É um investimento garantido pelo FGC com lastro em operações de crédito imobiliário financiadas por instituições financeiras e com isenção de IR."
- **LCA (literal):** "Com prazo a partir de 90 dias e isenção de IR, é uma ótima alternativa de investimento para quem busca rentabilidade e segurança."
- **FGC (literal):** "CDB, LC, LCI e LCA contam com a garantia do Fundo Garantidor de Créditos (FGC), que garante a devolução do principal investido acrescido de juros [...] até o limite de R$ 250mil por CPF ou CNPJ"
- **Percentuais do CDI:** NÃO CONFIRMADO — nenhum %CDI publicado
- **Valores mínimos e liquidez:** NÃO CONFIRMADO
- **Status: PARCIAL**

### Neon — CDB
- **URL:** https://neon.com.br/ — acesso 31/08/2026
- **Rendimento (literal, extraído da home):** "dar dinheiro, pois o CDB Neon tem o melhor rendimento do mercado: até 113% do CDI (muito mais do que a poupança)"
- **Condições do "até", prazo, liquidez, valor mínimo, emissor específico:** NÃO CONFIRMADO
- **FGC:** presumível pela natureza do CDB; não afirmado na home
- **Status: PARCIAL**

### Will Bank — EM LIQUIDAÇÃO EXTRAJUDICIAL
- **URL:** https://www.willbank.com.br/ — acesso 31/08/2026
- **Aviso oficial (literal):** "por meio do Ato do Presidente do Banco Central do Brasil número 1.376, de 21.01.2026, foi decretada a liquidação extrajudicial"
- **FGC:** o FGC antecipou pagamentos a credores elegíveis com saldos de até R$ 1.000 pelo app do Will Bank; aproximadamente **R$ 200 milhões** desembolsados
- **Cartões (literal):** "as faturas de cartões de crédito somente poderão ser pagas mediante geração de boleto"
- **Canais:** credores@willbank.com.br / liquidacao@willbank.com.br / 0800 011 7901
- **Não há produto a comparar.**
- **Status: COMPLETO**

### C6 Bank, 99Pay, Iti, Original, Banco Pan, Digio, Sofisa Direto, BMG, Agibank, Daycoval
**NÃO CONFIRMADO — nenhum percentual do CDI publicado em página aberta.**

Resultado da varredura automatizada em 31/08/2026:

| Instituição | URL testada | HTTP | Menção a %CDI |
|---|---|---:|---|
| C6 Bank | https://www.c6bank.com.br/conta-digital | 403 | bloqueado |
| C6 Bank | https://www.c6bank.com.br/investimentos | 403 | bloqueado |
| 99Pay | https://99app.com/pay/ | 429 | limite de requisições |
| Iti | https://www.itiunibanco.com.br/ | 000 | falha de conexão |
| Original | https://www.original.com.br/ | 200 | sem menção |
| Banco Pan | https://www.bancopan.com.br/ | 403 | bloqueado |
| Digio | https://www.digio.com.br/ | 200 | sem menção |
| Sofisa Direto | https://www.sofisadireto.com.br/ | 200 | sem menção |
| Sofisa Direto | https://www.sofisadireto.com.br/investimentos | 200 | sem menção |
| Sofisa Direto | https://www.sofisadireto.com.br/investimento/renda-fixa | 404 (WebFetch) | não obtido |
| BMG | https://www.bancobmg.com.br/ | 403 | bloqueado |
| Agibank | https://www.agibank.com.br/ | 200 | sem menção |
| Daycoval | https://www.daycoval.com.br/ | 200 | sem menção |

**Status: NÃO OBTIDO**

---

## 1.2 Quem anuncia acima de 110% do CDI hoje — e quem é o emissor real

| Oferta anunciada | Quem emite de fato | O que o número esconde |
|---|---|---|
| **Nubank — até 120% do CDI** (Caixinha Turbo) | Nu Financeira S.A. — a página da conta identifica os RDBs como "emitidos pela Nu Financeira" | Exige movimentar R$ 900/mês, ou assinatura Ultravioleta/Nubank+. Tem "validade" — não é taxa perpétua. O patamar sem condição é 100%. |
| **Mercado Pago — até 120% do CDI** (Cofrinhos; campanha chegou a 140%) | **Não é banco emissor.** O dinheiro vai para títulos públicos — "Tesouro Selic" | Teto de R$ 10 mil por CPF; acima disso volta a 100%. O 140% foi campanha de um mês só para assinantes Meli+. **Sem FGC** — a proteção é risco soberano, que é diferente (e, aqui, melhor). |
| **Neon — até 113% do CDI** (CDB Neon) | CDB — emissor específico não nomeado na home | "Até" sem condição publicada. Prazo e liquidez não divulgados. |

**Padrão comum às três:** o número grande é **teto condicional**, não taxa corrente. Em dois dos três casos há limite de valor (R$ 10 mil) ou de comportamento (movimentação mensal, assinatura). O piso incondicional gira em torno de 100% do CDI.

**Contexto de mercado (InvestNews, 12/06/2026):** "Taxas máximas oferecidas nas emissões dos certificados bancários por instituições pequenas e médias alcançaram o equivalente a 106,9% do CDI" (Qista Crédito), com Pine e BMG oferecendo 106% do CDI. Grandes bancos: Banco do Brasil 95%, Caixa Econômica 90%, Santander 97%.

---

## 1.3 Conta remunerada, RDB e CDB — a diferença que importa

São três coisas juridicamente distintas que o aplicativo apresenta com a mesma cara de "saldo que rende". A diferença aparece exatamente no dia ruim.

| | Conta de pagamento | RDB | CDB |
|---|---|---|---|
| **O que é** | Saldo em instituição de pagamento. Não é depósito bancário. | Recibo de Depósito Bancário: um empréstimo seu ao banco, **intransferível**. | Certificado de Depósito Bancário: empréstimo seu ao banco, **negociável** (pode ser cedido). |
| **FGC** | **NÃO.** O saldo puro de conta de pagamento não é crédito coberto. A proteção vem de outra via: segregação e lastro em títulos públicos. | **SIM.** "CDB e RDB" constam na lista de cobertos do FGC. | **SIM.** Mesma lista. |
| **Quem quebra junto com você** | Ninguém, se o lastro estiver segregado — mas você entra na fila da massa se não estiver. | O banco. Até R$ 250 mil o FGC cobre; acima disso você é credor quirografário na liquidação. | Idem RDB. |
| **Liquidez** | Imediata por natureza. | Depende do contrato. Liquidez diária é possível, mas não é automática. | Idem — e, por ser negociável, pode ter mercado secundário. |
| **Tributação** | IR pela tabela regressiva sobre o rendimento. | IR regressivo + IOF se resgatar antes de 30 dias. | Idem RDB. |
| **O risco real** | Operacional e de segregação. | Risco de **crédito do emissor**. É por isso que um banco pequeno paga 120% e o Banco do Brasil paga 95% — você está sendo pago para assumir a chance de ele quebrar. O FGC transforma esse risco em risco de *prazo* (quanto tempo até receber), não o elimina. | Idem RDB. |

**A assimetria que o marketing apaga:** dentro do limite do FGC, escolher o emissor que paga 120% em vez de 100% é quase de graça — o risco foi socializado. É exatamente essa assimetria que produziu o Banco Master, e é exatamente ela que o CMN passou a atacar em 2026 (Seção 2). **Acima** de R$ 250 mil por conglomerado, a lógica se inverte por completo: você assume risco de crédito integral por 20 pontos de CDI.

---

# SEÇÃO 2 — FGC: REGRAS VIGENTES

**Fontes:** https://www.fgc.org.br/sobre-garantia-fgc e https://www.fgc.org.br/pagamento-de-garantia — acesso 31/08/2026. **Status: COMPLETO**

## 2.1 Limites

| Limite | Valor | Texto literal |
|---|---:|---|
| Por CPF/CNPJ, por instituição ou conglomerado | **R$ 250.000,00** | "O FGC garante o pagamento de até R$ 250 mil por CPF ou CNPJ, por instituição financeira ou conglomerado" |
| Teto global por CPF/CNPJ em janela de 4 anos | **R$ 1.000.000,00** | "valor máximo a ser pago pelo FGC para o mesmo CPF ou CNPJ fica limitado a R$ 1 milhão" |

**A palavra decisiva é "conglomerado".** Cinco CDBs de cinco marcas diferentes do mesmo grupo somam um único limite de R$ 250 mil. Foi assim que credores de Banco Master e Will Bank descobriram, em janeiro de 2026, que compartilhavam o mesmo teto.

## 2.2 Produtos cobertos e não cobertos

**COBERTOS pela garantia ordinária:**
- Conta corrente e poupança
- CDB e RDB
- LCI (Letra de Crédito Imobiliário)
- LCD (Letra de Crédito do Desenvolvimento)
- LCA (Letra de Crédito do Agronegócio)
- LH (Letra Hipotecária)
- LC (Letra de Câmbio)
- Conta salário
- Operações compromissadas (títulos emitidos após 08/03/2012)

**NÃO COBERTOS:**
- Títulos Públicos (inclui Tesouro Direto)
- Título de capitalização
- LIG (Letra Imobiliária Garantida)
- LI (Letra Imobiliária)
- **LF (Letra Financeira)**
- **Fundos de Renda Fixa**
- Depósitos no exterior
- Depósitos judiciais
- **Debêntures**
- CRI (Certificado de Recebíveis Imobiliários)
- CRA (Certificado de Recebíveis do Agronegócio)

**Leitura para o investidor:** **LCI e LCA são cobertas** — e ainda são isentas de IR. É a combinação mais eficiente da lista para quem fica dentro do limite. **Fundos de renda fixa não são cobertos**, mas isso raramente é ruim: um fundo DI é dono de títulos públicos em nome dos cotistas, então não precisa de FGC — o risco é do Tesouro, não do gestor. Já **debêntures, CRI, CRA e letras financeiras** não têm nem FGC nem risco soberano: são crédito puro.

## 2.3 Prazo real de pagamento e procedimento

Texto literal de https://www.fgc.org.br/pagamento-de-garantia (acesso 31/08/2026):

1. **Início:** "O pagamento da garantia começa quando o Banco Central decreta a liquidação de uma instituição financeira."
2. **Lista de credores:** "A Instituição em intervenção/liquidação prepara e envia a lista de pessoas e valores a serem pagos para o FGC."
3. **Prazo de formação da lista:** "Esse processo pode levar, em média, 30 dias úteis a partir da falência."
4. **Habilitação:** "Com as informações recebidas da instituição, o FGC libera a solicitação no aplicativo para que os credores cadastrem a conta bancária, façam a validação da biometria e o envio de documentos."
5. **Pagamento:** "Após a assinatura do termo de sub-rogação pelo app, o pagamento é realizado na conta bancária cadastrada."
6. **Prazo final (literal):** "Após a assinatura do documento no aplicativo o crédito do valor é realizado na conta de titularidade do credor em **até 48 horas úteis**."
7. **Canal:** Pessoa Física usa o app do FGC; Pessoa Jurídica usa o Portal Investidor (https://portal-investidor.fgc.org.br)

**Formulação alternativa no comunicado do caso Master (18/11/2025, literal):** "Embora não exista um prazo legal para o início dos pagamentos, por conta das especificidades de cada liquidação, o prazo médio para o início dos pagamentos é de 30 dias."

> **O PRAZO QUE NINGUÉM DIVULGA:** as "48 horas úteis" contam do **fim** do processo, não do começo. O relógio que importa vai da liquidação até seu nome aparecer na lista do liquidante — e esse é discricionário. No caso Master a liquidação foi em **18/11/2025** e os pagamentos começaram em **19/01/2026**: **62 dias corridos** sem acesso ao dinheiro. Para quem tinha ali a reserva de emergência, essa foi a perda real, ainda que nominalmente integral.

## 2.4 Mudança de regra em 2025–2026 — SIM, houve

| Norma | O que muda | Vigência | Status da fonte |
|---|---|---|---|
| **Resolução CMN 5.238/2025** | Contribuição adicional ao FGC sobe de 0,01% para 0,02% dos depósitos garantidos; gatilho cai de 75% para 60% das captações via dívida. | Junho de 2026 | **PARCIAL — fonte secundária** |
| **Resolução CMN 5.295 (2026)** | "A nova norma dobra o multiplicador da Contribuição Adicional (CA) devida pelas instituições garantidas, de 0,01% para **0,02%**". Cria reserva obrigatória em Títulos Públicos Federais (MATPF), acionada por três gatilhos: (a) VR superior em 6× o patrimônio líquido E atingir 80% das captações via dívida; (b) VR superior em 10× o patrimônio líquido; (c) VR superior ao Ativo de Referência. | Em vigor 01/06/2026; escalonada — 5% da reserva em julho/2026, 100% em julho/2028 | **PARCIAL — fonte secundária** |

**Fontes secundárias:**
- InfoMoney, 06/09/2025 — https://www.infomoney.com.br/onde-investir/fim-do-cdb-de-120-do-cdi-nova-regra-do-fgc-impacta-taxas/
- Seu Dinheiro, 24/04/2026 — https://www.seudinheiro.com/2026/renda-fixa/conselho-monetario-nacional-aperta-regras-do-fgc-e-impoe-novas-travas-a-grandes-emissoes-de-cdb-lci-e-lca-mlim/

> **LIMITAÇÃO DESTA SEÇÃO — NÃO CONFIRMADO NA FONTE OFICIAL:** **não consegui abrir o texto oficial de nenhuma das duas resoluções.** O buscador de normativos do BCB (`https://www.bcb.gov.br/api/conteudo/app/normativos/exibenormativo?p1=1&p2=5295`) devolveu `{"navegacao":null,"view":"views/exibenormativo.aspx","conteudo":[]}` e a busca alternativa (`https://www.bcb.gov.br/api/search/app/normativos/buscanormativo`) retornou "Requisição Inválida". Números, percentuais e datas acima vêm de imprensa especializada, **não do Diário Oficial**. Trate-os como indício forte, não como citação normativa.

**Efeito observável nas taxas (InfoMoney, 06/09/2025, literal):** "Os CDBs emitidos em agosto não superaram 107% do CDI, comparado aos 109%-120% em julho. As taxas médias caíram significativamente: em 3 meses (de 100,40% para 99,92%) e em 24 meses (de 99,61% para 99,07%)." O mercado estima em torno de 120% do CDI como limite prático, "mas não há um teto explícito na regulamentação."

---

# SEÇÃO 3 — CASO BANCO MASTER: CRONOLOGIA E NÚMEROS

Este é o caso que dá sentido a todo o resto do dossiê. Um banco pagando **até 140% do CDI** não estava sendo generoso — estava comprando funding a qualquer preço, e o FGC (isto é, os outros bancos, isto é, todo o sistema) estava financiando a aposta.

## 3.1 Cronologia

**11/04/2025 — A taxa que sinalizava tudo**
Gazeta do Povo registra que os CDBs do Banco Master ofereciam "rendimento de até 140% do CDI, taxa muito acima da média do mercado."
Fonte: https://www.gazetadopovo.com.br/economia/cdbs-do-banco-master-o-que-acontece-com-quem-aplicou/

**28/03/2025 — BRB anuncia aquisição do Master**
**17/06/2025 — Aprovação do CADE**
**19/08/2025 — Câmara Legislativa do DF aprova**
**03/09/2025 — Banco Central rejeita a aquisição.** A saída de emergência é fechada.

**17/11/2025 — Prisão de Daniel Vorcaro**
Preso no aeroporto de Guarulhos tentando deixar o país em jato privado rumo a Malta.

**18/11/2025 — Liquidação extrajudicial · Operação Compliance Zero**
Fonte primária: **Comunicado BCB nº 44.238, de 18/11/2025**
URL: https://static.poder360.com.br/2025/11/comunicado-BC-Master-liquidacao-extrajudicial-18nov2025.pdf

Texto literal do comunicado:
> "por meio do Ato do Presidente nº 1.373 desta data, com fundamento nos arts. 15, caput e § 2º, 16, 51 e 52, todos da Lei nº 6.024, de 13 de março de 1974, e considerando o vínculo de interesse, evidenciado pelo exercício do poder de controle e pela existência de administração comum com o BANCO MASTER S.A., CNPJ 33.923.798/0001-00, cuja liquidação extrajudicial é decretada nesta data, foi decretada, por extensão, a liquidação extrajudicial da MASTER S/A CORRETORA DE CÂMBIO, TÍTULOS E VALORES MOBILIÁRIOS, CNPJ 33.886.862/0001-12"

Liquidante nomeado: EFB REGIMES ESPECIAIS DE EMPRESAS LTDA., CNPJ 43.336.034/0001-64, responsável técnico Eduardo Felix Bianchini.

**Bens tornados indisponíveis (art. 36 da Lei 6.024/1974 e art. 2º da Lei 9.447/1997):**

*Controladores:*
- MASTER HOLDING FINANCEIRA S.A., CNPJ 54.331.263/0001-02
- 133 INVESTIMENTOS E PARTICIPAÇÕES LTDA., CNPJ 31.093.039/0001-24
- ARMANDO MIGUEL GALLO NETO
- **DANIEL BUENO VORCARO**
- FELIPE WALLACE SIMONSEN

*Ex-administradores:*
- ANGELO ANTONIO RIBEIRO DA SILVA
- JOSE RICARDO DE QUEIROZ PEREIRA
- LUIZ ANTONIO BULL
- REINALDO HOSSEPIAN SALLES LIMA
- VINICIUS DA SILVA PINTO

**Motivo declarado (via Terra, 20/02/2026, literal):** "Grave crise de liquidez do Conglomerado Master e comprometimento significativo da sua situação econômico-financeira"

**Rombo estimado pela PF:** "Os fundos faltantes do banco podem chegar a 12 bilhões de reais ($2,2 bilhões)". Mínimo de 1,6 milhão de pessoas afetadas.

**18/11/2025 — O FGC dimensiona o estrago**
Fonte primária: **Comunicado ao Mercado do FGC, 18/11/2025**
URL: https://static.poder360.com.br/2025/11/master-comunicado-fgc-18nov2025.pdf

Texto literal:
> "Conforme Atos do Presidente do Banco Central, n.º 1.369, 1.371, 1.372 e 1.373, publicados em 18/11/2025, foram liquidadas extrajudicialmente as instituições Banco Master, Banco Master de Investimento, Banco Letsbank e Master Corretora de Câmbio."

> "As instituições liquidadas possuem uma base estimada de **1,6 milhão de credores** com depósitos e investimentos elegíveis ao pagamento da garantia, que somam um valor aproximado de **R$ 41 bilhões**."

> "O valor estimado para o pagamento da garantia é provisionado pelo FGC, que, conforme números do fechamento de setembro/2025, possuía um patrimônio de **R$ 160 bilhões**, dos quais **R$ 122 bilhões** correspondiam a recursos líquidos em caixa, para o exercício de sua atividade."

**15/01/2026 — Reag Trust DTVM**
Liquidada por "Graves violações às normas que regem as atividades das instituições integrantes do SFN"

**19/01/2026 — Começam os pagamentos do FGC** (62 dias corridos após a liquidação)

**21/01/2026 — Will Bank (Will Financeira S.A. CFI)**
Ato do Presidente do BC nº 1.376. Motivo: comprometimento econômico-financeiro e insolvência vinculada ao Banco Master. Confirmado no próprio site: https://www.willbank.com.br/

**29/01/2026 — R$ 32,5 bi · 580 mil credores**
Fonte: Agência Brasil, 29/01/2026
URL: https://agenciabrasil.ebc.com.br/economia/noticia/2026-01/fgc-ja-pagou-r-325-bilhoes-75-dos-credores-do-banco-master
- Valor pago: **R$ 32,5 bilhões**
- Credores pagos: **580 mil** (75% do total com direito à garantia)
- Literal: "O volume corresponde a 80,05% do valor total previsto para desembolso"
- Valor total elegível: aproximadamente **R$ 40,6 bilhões líquidos**
- Início dos pagamentos: 19 de janeiro de 2026
- Literal sobre conglomerado: "O credor que já recebeu o valor limite da garantia de R$ 250 mil não terá novos pagamentos, uma vez que todas as instituições pertencem ao mesmo conglomerado financeiro"

**06/02/2026 — R$ 36 bi · 89% do valor devido**
Fonte: CNN Brasil, 06/02/2026 (17:54)
URL: https://www.cnnbrasil.com.br/economia/financas/caso-master-fgc-ja-pagou-89-do-valor-devido-a-credores/
- Valor total pago: **R$ 36 bilhões**
- Percentual do valor devido: **89%**
- Credores reembolsados: **628 mil** (**81%**)
- Valor a ser pago ao Will Bank: **R$ 6,3 bilhões**

**18/02/2026 — Banco Pleno S.A. e Pleno DTVM**
Sétima e oitava liquidações do caso. Motivo: "Deterioração da liquidez e infringência às normas regulatórias"

**03–04/03/2026 — Prisão preventiva de Vorcaro**
Fonte: Jornal GGN, 04/03/2026
URL: https://jornalggn.com.br/justica/crimes-prisao-preventiva-vorcaro-operacao-compliance-zero/
- Data da decisão: **3 de março de 2026**
- Juízo: **Supremo Tribunal Federal — Ministro André Mendonça**
- **Crimes investigados:** (1) Gestão fraudulenta de instituição financeira; (2) Corrupção ativa e passiva; (3) Organização criminosa; (4) Lavagem de dinheiro; (5) Violação de sigilo funcional; (6) Fraude processual; (7) Obstrução de justiça
- A decisão descreve **quatro núcleos**: um financeiro (fraudes), um de corrupção institucional (cooptação de servidores do BC), um de ocultação patrimonial e lavagem de dinheiro, e um de "intimidação e obstrução de justiça, que monitorava ilegalmente adversários, jornalistas e autoridades"
- Vorcaro transferido para o Complexo Penitenciário de Potim

**13/05/2026 — R$ 39,7 bi · 97,87%**
Fonte: Blog da Rosana Hessel / Correio Braziliense, 13/05/2026
URL: https://newblogs.correiobraziliense.com.br/blog-da-rosana-hessel/caso-master-fgc-informa-o-pagamento-de-9787-dos-valores-previstos/
- Valor pago: **R$ 39,7 bilhões**
- Percentual do montante a pagar: **97,87%**
- Beneficiários: **915 mil**
- Percentual do total de credores: **92,67%**

## 3.2 Instituições liquidadas ligadas ao caso — as 8

Fonte: Terra, 20/02/2026 (04h58)
URL: https://www.terra.com.br/economia/pleno-reag-e-will-entenda-as-8-liquidacoes-em-torno-do-caso-do-banco-master,efab47968fa81f17857d14e6843b2dc77io1583d.html

| # | Instituição | Data | Motivo declarado |
|---|---|---|---|
| 1 | Banco Master S.A. | 18/11/2025 | "Grave crise de liquidez do Conglomerado Master e comprometimento significativo da sua situação econômico-financeira" |
| 2 | Banco Master de Investimento S.A. | 18/11/2025 | Mesmo das demais empresas Master |
| 3 | Banco Letsbank S.A. | 18/11/2025 | Mesmo das demais empresas Master |
| 4 | Master S/A Corretora de Câmbio, Títulos e Valores Mobiliários | 18/11/2025 | Mesmo das demais empresas Master |
| 5 | Reag Trust Distribuidora de Títulos e Valores Mobiliários S.A. | 15/01/2026 | "Graves violações às normas que regem as atividades das instituições integrantes do SFN" |
| 6 | Will Financeira S.A. Crédito, Financiamento e Investimento | 21/01/2026 | Comprometimento econômico-financeiro e insolvência vinculada ao Banco Master |
| 7 | Banco Pleno S.A. | 18/02/2026 | Deterioração da liquidez e infringência às normas regulatórias |
| 8 | Pleno Distribuidora de Títulos e Valores Mobiliários S.A. | 18/02/2026 | Mesmo do Banco Pleno |

## 3.3 Verificação do número que a pergunta trazia

> **"R$ 32,5 bi para 75% dos credores até janeiro/2026" — CONFIRMADO, LITERAL.** Agência Brasil, 29/01/2026. Mas está desatualizado por quatro meses.

**Trajetória verificada dos pagamentos do FGC:**

| Data | Valor pago | % do valor devido | Credores | % dos credores |
|---|---:|---:|---:|---:|
| jan/2026 | R$ 26 bi | — | — | 67% |
| 29/01/2026 | R$ 32,5 bi | 80,05% | 580 mil | 75% |
| 06/02/2026 | R$ 36 bi | 89% | 628 mil | 81% |
| 13/05/2026 | **R$ 39,7 bi** | **97,87%** | **915 mil** | **92,67%** |

**Tempo total:** da liquidação (18/11/2025) a 97,87% pago (13/05/2026) = aproximadamente **6 meses**. Do início efetivo dos pagamentos (19/01/2026) = aproximadamente **4 meses**.

## 3.4 O %CDI que o Master pagava

**"rendimento de até 140% do CDI, taxa muito acima da média do mercado."**
Fonte: Gazeta do Povo, 11/04/2025 (pré-liquidação)
URL: https://www.gazetadopovo.com.br/economia/cdbs-do-banco-master-o-que-acontece-com-quem-aplicou/
**Status: COMPLETO**

Para comparação, após a quebra (InvestNews, 12/06/2026): bancos pequenos e médios no máximo 106,9% do CDI; grandes bancos entre 90% e 97%.

## 3.5 O que aconteceu com quem tinha acima do limite do FGC

Recebeu R$ 250 mil e virou credor da massa falida pelo excedente — sem prazo, sem garantia e atrás dos créditos trabalhistas e tributários na ordem legal.

Pior: o FGC esclareceu que credores de **Banco Master e Will Bank compartilham o mesmo limite**, porque o Will integra o conglomerado desde agosto de 2024. Nas palavras do fundo (Agência Brasil, 29/01/2026, literal): "O credor que já recebeu o valor limite da garantia de R$ 250 mil não terá novos pagamentos, uma vez que todas as instituições pertencem ao mesmo conglomerado financeiro."

**Quem diversificou entre marcas achando que diversificava emissor não diversificou nada.**

A Gazeta do Povo (11/04/2025) registrava que valores excedentes ao teto do FGC "pode ser exposta a risco em caso de insolvência da instituição", sugerindo como alternativa tentar vender o excedente no mercado secundário antes do vencimento. A ordem exata da fila de credores na liquidação: **NÃO CONFIRMADO** nas fontes consultadas.

## 3.6 O Will Bank foi envolvido — e como

**SIM.** Três formas:

1. **Pertence ao conglomerado Master desde agosto de 2024** — por isso compartilha o limite de R$ 250 mil por CPF (Agência Brasil, 29/01/2026).
2. **Foi liquidado em 21/01/2026** pelo Ato do Presidente do BC nº 1.376, confirmado no próprio site da instituição.
3. **R$ 6,3 bilhões** era o valor a ser pago pelo FGC aos credores do Will Bank (CNN Brasil, 06/02/2026). O FGC antecipou saldos de até R$ 1.000 pelo app do Will Bank — cerca de **R$ 200 milhões** desembolsados nessa antecipação.

Contexto adicional: houve oferta do Mubadala pela fintech Will antes da liquidação (Bloomberg, 21/01/2026) — **detalhes NÃO CONFIRMADOS** (não acessei a matéria).

## 3.7 A lição regulatória

O sistema funcionou no que prometia — 97,87% pago em seis meses, sem corrida bancária — e falhou no que não prometia: impedir que um emissor comprasse R$ 41 bilhões de depósitos garantidos pagando 140% do CDI.

A resposta veio pelo custo, não pela proibição: as Resoluções CMN 5.238/2025 e 5.295/2026 dobram a contribuição adicional ao FGC (de 0,01% para 0,02%), reduzem o gatilho de 75% para 60% das captações via dívida, e criam reserva compulsória em títulos públicos (MATPF) para quem depende demais de captação garantida.

**O resultado prático já apareceu no preço: o teto de mercado caiu de ~120% para ~107% do CDI.**

**Ainda em aberto:** o TCU realiza inspeção sobre a condução da liquidação pelo BC, após o Banco Central desistir de embargos. **Desfecho NÃO APURADO.**

---

# SEÇÃO 4 — TESOURO DIRETO

## 4.0 ACHADO — PRODUTO NOVO: TESOURO RESERVA

**URL:** https://www.tesourodireto.com.br/tesouro-reserva — acesso 31/08/2026. **Status: COMPLETO**

Textos literais:
- **Valor mínimo:** "O investimento mínimo no Tesouro Reserva é de **R$ 1,00**. Esse também é o valor mínimo para movimentações — tanto para guardar quanto para resgatar."
- **Remuneração:** "Seu dinheiro **rende 100% da Selic**" e "seu dinheiro rende **todo dia útil com 100% da Selic**"
- **Liquidez:** "As operações funcionam praticamente 24 horas por dia, 7 dias por semana*, inclusive à noite, fins de semana e feriados. *As operações ficam indisponíveis diariamente no período entre 0h e 1h." Resgate "de forma imediata".
- **Custódia:** "**Taxa de Custódia da B3:** 0,20% ao ano, com isenção para valores de até R$ 10.000,00 investidos."
- **IR:** "segue a tabela regressiva de renda fixa"
- **IOF:** "aplicado apenas se o resgate ocorrer nos primeiros 30 dias"
- **Teto de valor e data de lançamento:** NÃO CONFIRMADO (não mencionados na página)

É um produto de reserva de emergência com risco soberano competindo diretamente com as caixinhas de fintech — e sem depender de FGC.

## 4.1 Valor mínimo de aplicação

**Fonte:** B3 — Perguntas Frequentes Tesouro Direto
URL: https://www.b3.com.br/pt_br/produtos-e-servicos/tesouro-direto/tesouro-direto/perguntas-frequentes/ — acesso 31/08/2026

- **Fração mínima (literal):** "o investidor pode comprar, por exemplo, 0.56, 2.35 ou 3.45 porções de um título" — fração mínima de **0,01 título**
- **Valor mínimo em reais (literal):** "o valor a ser aplicado necessita respeitar o limite financeiro mínimo de **R$ 30,00 (trinta reais)**"
- **Teto de compra (literal):** "O limite financeiro máximo de compra por investidor é de **R$ 1.000.000,00 por mês**"
- **Exceção:** Tesouro Reserva, mínimo de R$ 1,00

**Status: COMPLETO**

## 4.2 Títulos disponíveis e taxas — tabela oficial completa

**Fonte primária:** Tesouro Transparente (CKAN), arquivo `precotaxatesourodireto.csv`
URL: https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/precotaxatesourodireto.csv
Arquivo atualizado: **31/08/2026 às 10:20:09**
Última data-base contida: **28/08/2026**
Total de títulos na data: **58**
**Status: COMPLETO**

| Tipo de Título | Vencimento | Taxa Compra (% a.a.) | Taxa Venda (% a.a.) | PU Compra (R$) | PU Venda (R$) |
|---|---|---:|---:|---:|---:|
| Tesouro Selic | 01/03/2027 | -0,00 | 0,01 | 19.773,11 | 19.761,88 |
| Tesouro Selic | 01/03/2028 | 0,01 | 0,02 | 19.770,18 | 19.756,96 |
| Tesouro Selic | 01/03/2029 | 0,03 | 0,04 | 19.759,60 | 19.744,43 |
| Tesouro Selic | 01/03/2031 | 0,07 | 0,08 | 19.708,55 | 19.689,47 |
| Tesouro Prefixado | 01/01/2027 | 13,44 | 13,56 | 958,83 | 958,01 |
| Tesouro Prefixado | 01/01/2028 | 13,74 | 13,86 | 842,69 | 841,08 |
| Tesouro Prefixado | 01/01/2029 | 14,08 | 14,20 | 737,30 | 735,12 |
| Tesouro Prefixado | 01/01/2031 | 14,40 | 14,52 | 560,62 | 557,80 |
| Tesouro Prefixado | 01/01/2032 | 14,49 | 14,61 | 488,02 | 485,05 |
| Tesouro Prefixado com Juros Semestrais | 01/01/2027 | 13,39 | 13,51 | 1.005,78 | 1.004,92 |
| Tesouro Prefixado com Juros Semestrais | 01/01/2029 | 13,92 | 14,04 | 945,93 | 943,36 |
| Tesouro Prefixado com Juros Semestrais | 01/01/2031 | 14,42 | 14,54 | 886,67 | 882,96 |
| Tesouro Prefixado com Juros Semestrais | 01/01/2033 | 14,53 | 14,65 | 843,40 | 838,91 |
| Tesouro Prefixado com Juros Semestrais | 01/01/2035 | 14,54 | 14,66 | 813,21 | 808,17 |
| Tesouro Prefixado com Juros Semestrais | 01/01/2037 | 14,51 | 14,63 | 791,25 | 785,84 |
| Tesouro IPCA+ | 15/05/2029 | 7,95 | 8,07 | 3.859,60 | 3.848,01 |
| Tesouro IPCA+ | 15/08/2032 | 7,93 | 8,05 | 3.014,24 | 2.994,37 |
| Tesouro IPCA+ | 15/05/2035 | 7,76 | 7,88 | 2.482,41 | 2.458,57 |
| Tesouro IPCA+ | 15/08/2040 | 7,43 | 7,55 | 1.751,74 | 1.724,78 |
| Tesouro IPCA+ | 15/05/2045 | 7,29 | 7,41 | 1.280,52 | 1.254,17 |
| Tesouro IPCA+ | 15/08/2050 | 7,25 | 7,37 | 894,90 | 871,38 |
| Tesouro IPCA+ com Juros Semestrais | 15/08/2030 | 8,00 | 8,12 | 4.452,44 | 4.434,85 |
| Tesouro IPCA+ com Juros Semestrais | 15/08/2032 | 7,93 | 8,05 | 4.343,40 | 4.319,12 |
| Tesouro IPCA+ com Juros Semestrais | 15/05/2035 | 7,79 | 7,91 | 4.318,84 | 4.286,98 |
| Tesouro IPCA+ com Juros Semestrais | 15/05/2037 | 7,63 | 7,75 | 4.291,33 | 4.254,64 |
| Tesouro IPCA+ com Juros Semestrais | 15/08/2040 | 7,53 | 7,65 | 4.160,55 | 4.117,68 |
| Tesouro IPCA+ com Juros Semestrais | 15/05/2045 | 7,43 | 7,55 | 4.175,04 | 4.125,52 |
| Tesouro IPCA+ com Juros Semestrais | 15/08/2050 | 7,40 | 7,52 | 4.046,34 | 3.992,19 |
| Tesouro IPCA+ com Juros Semestrais | 15/05/2055 | 7,31 | 7,43 | 4.115,19 | 4.057,51 |
| Tesouro IPCA+ com Juros Semestrais | 15/08/2060 | 7,30 | 7,42 | 4.016,11 | 3.956,43 |
| Tesouro IGPM+ com Juros Semestrais | 01/01/2031 | 7,96 | 8,08 | 7.626,33 | 7.596,03 |
| Tesouro Renda+ Aposentadoria Extra | 15/12/2049 | 7,51 | 7,63 | 1.975,48 | 1.951,52 |
| Tesouro Renda+ Aposentadoria Extra | 15/12/2054 | 7,35 | 7,47 | 1.411,51 | 1.386,57 |
| Tesouro Renda+ Aposentadoria Extra | 15/12/2059 | 7,23 | 7,35 | 1.015,66 | 992,14 |
| Tesouro Renda+ Aposentadoria Extra | 15/12/2064 | 7,15 | 7,27 | 732,08 | 711,13 |
| Tesouro Renda+ Aposentadoria Extra | 15/12/2069 | 7,09 | 7,21 | 528,48 | 510,49 |
| Tesouro Renda+ Aposentadoria Extra | 15/12/2074 | 7,05 | 7,17 | 381,06 | 366,04 |
| Tesouro Renda+ Aposentadoria Extra | 15/12/2079 | 7,05 | 7,17 | 271,59 | 259,44 |
| Tesouro Renda+ Aposentadoria Extra | 15/12/2084 | 7,05 | 7,17 | 193,59 | 183,90 |
| Tesouro Educa+ | 15/12/2030 | 7,89 | 8,01 | 3.502,82 | 3.494,81 |
| Tesouro Educa+ | 15/12/2031 | 7,91 | 8,03 | 3.847,48 | 3.836,02 |
| Tesouro Educa+ | 15/12/2032 | 7,95 | 8,07 | 3.562,20 | 3.547,68 |
| Tesouro Educa+ | 15/12/2033 | 7,94 | 8,06 | 3.302,81 | 3.285,72 |
| Tesouro Educa+ | 15/12/2034 | 7,90 | 8,02 | 3.067,08 | 3.047,82 |
| Tesouro Educa+ | 15/12/2035 | 7,85 | 7,97 | 2.852,17 | 2.831,12 |
| Tesouro Educa+ | 15/12/2036 | 7,79 | 7,91 | 2.656,86 | 2.634,33 |
| Tesouro Educa+ | 15/12/2037 | 7,72 | 7,84 | 2.479,84 | 2.456,08 |
| Tesouro Educa+ | 15/12/2038 | 7,64 | 7,76 | 2.320,11 | 2.295,32 |
| Tesouro Educa+ | 15/12/2039 | 7,58 | 7,70 | 2.169,55 | 2.144,00 |
| Tesouro Educa+ | 15/12/2040 | 7,51 | 7,63 | 2.032,74 | 2.006,56 |
| Tesouro Educa+ | 15/12/2041 | 7,47 | 7,59 | 1.900,27 | 1.873,70 |
| Tesouro Educa+ | 15/12/2042 | 7,43 | 7,55 | 1.777,77 | 1.750,96 |
| Tesouro Educa+ | 15/12/2043 | 7,40 | 7,52 | 1.662,00 | 1.635,11 |
| Tesouro Educa+ | 15/12/2044 | 7,37 | 7,49 | 1.554,75 | 1.527,89 |
| Tesouro Educa+ | 15/12/2045 | 7,34 | 7,46 | 1.455,35 | 1.428,61 |
| Tesouro Educa+ | 15/12/2046 | 7,31 | 7,43 | 1.363,15 | 1.336,61 |
| Tesouro Educa+ | 15/12/2047 | 7,30 | 7,42 | 1.273,20 | 1.247,02 |
| Tesouro Educa+ | 15/12/2048 | 7,28 | 7,40 | 1.191,57 | 1.165,77 |

**Nota:** **Taxa de compra** é a que o investidor trava ao comprar; **taxa de venda** é a que o Tesouro pratica na recompra antecipada — a diferença de 0,12 p.p. é o spread.

**Observação sobre a página web:** https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm (acesso 31/08/2026) mostrou: "As negociações estão disponíveis no momento", horário "09h30 às 18h00", atualização "31/08/2026 - 09h21 min", e destaque para Tesouro Reserva ("rende desde o 1º dia útil, a partir de R$ 1,00"). **A tabela de títulos não renderizou** (página dependente de JavaScript). **Status: PARCIAL** — dados supridos pelo CSV oficial.

## 4.3 Taxa de custódia da B3

**Fonte:** https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/tarifas-de-tesouro-direto/ — acesso 31/08/2026. **Status: COMPLETO**

| Item | Valor / regra |
|---|---|
| **Percentual** | **0,20% a.a.** |
| **Base de cálculo** | Valor dos títulos |
| **Periodicidade** | **Provisionada diariamente**, cobrada em: venda antecipada, vencimento ou pagamento de juros — **não mais semestralmente** |

**Isenções confirmadas:**

| Título | Regra de isenção |
|---|---|
| **Tesouro Selic** | **Isento até R$ 10.000,00 por CPF.** Taxa aplicada apenas sobre o excedente. |
| **Tesouro Educa+** | Manter até vencimento: 0,00%. Resgate até 4 salários mínimos: 0,00%. Acima de 4 salários mínimos: 0,10% sobre o excedente. |
| **Tesouro Renda+** | Manter até vencimento: 0,00%. Resgate até 6 salários mínimos: 0,00%. Acima de 6 salários mínimos: 0,10% sobre o excedente. |

> **CONFIRMADO: a isenção para estoque de Tesouro Selic continua existindo e é de R$ 10.000,00 por CPF.**

**Contexto (Agência Brasil / B3, dez/2024):** "Taxa de custódia do Tesouro Direto deixa de ser cobrada semestralmente" — mudança de regime confirmada pela página de tarifas da B3.

## 4.4 Taxa da instituição financeira

**NÃO CONFIRMADO.** Não consultei o ranking de agentes de custódia da B3. **Nenhuma instituição é citada neste dossiê como "taxa zero".** Ver Seção 8.

## 4.5 Tributação

### IR — tabela regressiva
**Fonte primária:** Lei nº 11.033, de 21/12/2004, art. 1º
URL: https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm — acesso 31/08/2026
**Status: COMPLETO**

Texto literal:
> "Art. 1º Os rendimentos de que trata o art. 5º da Lei nº 9.779, de 19 de janeiro de 1999, relativamente às aplicações e operações realizadas a partir de 1º de janeiro de 2005, sujeitam-se à incidência do imposto de renda na fonte, às seguintes alíquotas:
> I - **22,5%** (vinte e dois inteiros e cinco décimos por cento), em aplicações com prazo de **até 180 (cento e oitenta) dias**;
> II - **20%** (vinte por cento), em aplicações com prazo de **181 (cento e oitenta e um) dias até 360 (trezentos e sessenta) dias**;
> III - **17,5%** (dezessete inteiros e cinco décimos por cento), em aplicações com prazo de **361 (trezentos e sessenta e um) dias até 720 (setecentos e vinte) dias**;
> IV - **15%** (quinze por cento), em aplicações com prazo **acima de 720 (setecentos e vinte) dias**."

| Prazo da aplicação | Alíquota de IR |
|---|---:|
| Até 180 dias | 22,5% |
| De 181 a 360 dias | 20,0% |
| De 361 a 720 dias | 17,5% |
| Acima de 720 dias | 15,0% |

> **CONFIRMAÇÃO CRÍTICA:** a página do Planalto marca a MP nº 1.303/2025 como **"Vigência encerrada"**. A tabela regressiva **permanece em vigor**. Confirmado independentemente por Daycoval (blog institucional): "A recente rejeição da Medida Provisória (MP) nº 1.303/2025 pela Câmara dos Deputados encerra, por enquanto, a tentativa do governo de reformular o Imposto de Renda sobre investimentos." A MP foi rejeitada em **outubro de 2025**. **LCI/LCA seguem totalmente isentas de IR para pessoa física.**

### IOF — tabela regressiva até 30 dias
**Fonte primária:** Decreto nº 6.306, de 14/12/2007, art. 32 e Anexo
URL: https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/decreto/d6306.htm — acesso 31/08/2026
**Status: COMPLETO**

Texto literal do art. 32:
> "O IOF será cobrado à alíquota de um por cento ao dia sobre o valor do resgate, cessão ou repactuação, **limitado ao rendimento da operação**, em função do prazo, conforme tabela constante do Anexo."

Aplica-se (§1º): "I - às operações realizadas no mercado de renda fixa" (redação do Decreto nº 7.487/2011); "II - ao resgate de cotas de fundos de investimento e de clubes de investimento".

**ANEXO — % LIMITE DO RENDIMENTO (transcrição literal integral):**

| Nº de dias | % | Nº de dias | % | Nº de dias | % |
|---:|---:|---:|---:|---:|---:|
| 01 | 96 | 11 | 63 | 21 | 30 |
| 02 | 93 | 12 | 60 | 22 | 26 |
| 03 | 90 | 13 | 56 | 23 | 23 |
| 04 | 86 | 14 | 53 | 24 | 20 |
| 05 | 83 | 15 | 50 | 25 | 16 |
| 06 | 80 | 16 | 46 | 26 | 13 |
| 07 | 76 | 17 | 43 | 27 | 10 |
| 08 | 73 | 18 | 40 | 28 | 06 |
| 09 | 70 | 19 | 36 | 29 | 03 |
| 10 | 66 | 20 | 33 | **30** | **00** |

**A partir do 30º dia não há IOF.**

## 4.6 Liquidez — horário e prazo de liquidação do resgate

**Fonte:** B3 — Perguntas Frequentes — acesso 31/08/2026. **Status: PARCIAL**

Fluxo da venda antecipada conforme o FAQ da B3:
- **Dia 0:** "Venda antecipada do Título no site do Tesouro Direto" (entre 18h e 5h)
- **Dia 1:** "Repasse dos recursos pelo Tesouro Nacional, pelo valor bruto, ao Agente de Custódia (às 12h30)"
- **Dia 2:** "Repasse ao investidor, pelo Agente de Custódia, do valor líquido" (prazo varia conforme instituição)

**Horário de negociação:** 09h30 às 18h00 (confirmado na página de preços e taxas, 31/08/2026)

> **NÃO É D+0.** A síntese do FAQ indica liquidação **D+1** para o Tesouro Nacional e **D+2** para o investidor receber. **Exceção: o Tesouro Reserva**, cuja página oficial promete resgate "de forma imediata", operando 24×7 exceto entre 0h e 1h.

**O horário exato de crédito ao investidor: NÃO CONFIRMADO** — depende da instituição.

## 4.7 Marcação a mercado — o risco de vender antes do vencimento

Cada título tem duas taxas na tabela acima porque tem dois preços. A taxa contratada só é garantida **no vencimento**. Antes disso o Tesouro recompra ao preço de mercado do dia, que se move na direção contrária à taxa: **se os juros sobem, o preço do seu título cai.**

O tamanho do efeito é visível nos próprios PUs de hoje (28/08/2026):
- Um **Prefixado 2032** custa R$ 488,02 e pagará R$ 1.000 no vencimento — é um título longo, e títulos longos são os mais sensíveis. Um movimento de 1 ponto percentual na taxa mexe muito mais no preço dele do que num **Prefixado 2027** (R$ 958,83).
- O **Tesouro Selic** é o oposto: sua taxa é praticamente zero sobre a Selic (de −0,00% a 0,07%), então o PU quase não oscila — é por isso que ele, e não o IPCA+, é o título de reserva de emergência.

**Onde isso morde:** um IPCA+ 2050 comprado a 7,25% que precise ser vendido num momento de estresse pode ser recomprado com prejuízo nominal relevante. **Prazo do título deve casar com prazo do dinheiro.** A marcação a mercado não é risco de crédito — o Tesouro paga —, é risco de *quando* você precisa sair.

---

# SEÇÃO 5 — POUPANÇA

## 5.1 Regra de rendimento vigente

**Fonte primária:** Lei nº 12.703, de 7 de agosto de 2012 (que alterou o art. 12 da Lei nº 8.177/1991)
URL: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12703.htm — acesso 31/08/2026
**Status: COMPLETO**

Texto literal — remuneração adicional, além da TR, por juros de:
> "a) **0,5% (cinco décimos por cento) ao mês**, enquanto a meta da taxa Selic ao ano, definida pelo Banco Central do Brasil, for **superior a 8,5% (oito inteiros e cinco décimos por cento)**; ou
> b) **70% (setenta por cento) da meta da taxa Selic ao ano**, definida pelo Banco Central do Brasil, mensalizada, vigente na data de início do período de rendimento, nos demais casos."

> "§ 5º O Banco Central do Brasil divulgará as taxas resultantes da aplicação do contido nas alíneas a e b do inciso II do caput deste artigo."

**CONFIRMADO: os números da fórmula são 0,5% a.m. e 8,5% a.a. de Selic como limiar, com 70% da Selic mensalizada abaixo do limiar.**

**Aplicação hoje:** com a Selic meta em **14,00%** (acima de 8,5%), vale a regra (a): **0,5% ao mês + TR**.

**Verificação aritmética com dados do BCB (28/08/2026):**
- TR do período 28/08→28/09/2026 = 0,1448% (SGS 226)
- Poupança publicada para o mesmo período = 0,6455% (SGS 25)
- Conferência: (1,005 × 1,001448) − 1 = 0,006455 = **0,6455%** ✓ A fórmula fecha.

## 5.2 Rendimento efetivo dos últimos 12 meses

**Série mensal oficial (BCB/SGS 25, aniversário dia 1) — valores literais lidos:**

| Período de rendimento | Valor |
|---|---:|
| 01/07/2025 → 01/08/2025 | 0,6767% |
| 01/08/2025 → 01/09/2025 | 0,6731% |
| 01/09/2025 → 01/10/2025 | 0,6751% |
| 01/10/2025 → 01/11/2025 | 0,6767% |
| 01/11/2025 → 01/12/2025 | 0,6642% |
| 01/12/2025 → 01/01/2026 | 0,6751% |
| 01/01/2026 → 01/02/2026 | 0,6727% |
| 01/02/2026 → 01/03/2026 | 0,6213% |
| 01/03/2026 → 01/04/2026 | 0,6744% |
| 01/04/2026 → 01/05/2026 | 0,6687% |
| 01/05/2026 → 01/06/2026 | 0,6695% |
| 01/06/2026 → 01/07/2026 | 0,6718% |
| 01/07/2026 → 01/08/2026 | 0,6738% |
| 01/08/2026 → 01/09/2026 | 0,6701% |

**CDI acumulado no mês (BCB/SGS 4391) — valores literais:**
set/2025 1,22 · out/2025 1,28 · nov/2025 1,05 · dez/2025 1,22 · jan/2026 1,16 · fev/2026 1,00 · mar/2026 1,21 · abr/2026 1,09 · mai/2026 1,07 · jun/2026 1,12 · jul/2026 1,22 · ago/2026 1,04

| Indicador (12 meses: créditos de 01/09/2025 a 01/08/2026) | Valor |
|---|---:|
| **Poupança acumulada** | **8,3144%** |
| **CDI acumulado** | **14,5707%** |
| **Diferença** | **6,26 p.p.** |
| **Poupança como % do CDI** | **~57%** |

> **CÁLCULO, NÃO LEITURA.** Os dois acumulados foram computados por mim a partir das séries mensais oficiais do BCB, compondo doze fatores mensais. **As séries individuais são fonte primária; a composição é derivação minha** e está aberta a conferência.
>
> **Nota de método:** minha primeira tentativa compôs 12 registros *diários* consecutivos da série 25 (cada um representando um período mensal iniciado naquele dia), o que produziu 8,2753% — resultado metodologicamente incorreto. O valor correto usa os aniversários do dia 1.

## 5.3 A regra do aniversário

A poupança credita rendimento **uma vez por mês, na data de aniversário do depósito**. Não há proporcionalidade: sacar no 29º dia rende exatamente **zero** sobre aquele mês. Não é uma multa — é ausência de crédito.

**O cenário de emergência:** você deposita dia 10. No dia 8 do mês seguinte o carro quebra e você saca. Rendimento: **R$ 0,00** por 29 dias de dinheiro parado. No Tesouro Selic ou num CDB de liquidez diária, os mesmos 29 dias renderiam pro rata — descontados IR e IOF, mas nunca zerados.

**É justamente na emergência, que é o uso que a poupança alega servir, que a regra do aniversário cobra o preço mais alto.**

## 5.4 Comparação honesta com Tesouro Selic e CDB de liquidez diária

A poupança tem duas vantagens reais: é **isenta de IR** e **não tem IOF**. E ainda assim perde, em todos os prazos, para o Tesouro Selic e para qualquer CDB de 100% do CDI — como a Seção 6 mostra com os números.

**A razão é aritmética:** 0,6455% ao mês equivale a cerca de **8,03% ao ano**, contra um **CDI de 13,90%**. A isenção de IR não compensa uma taxa bruta 42% menor. Aos 22,5% de IR — a alíquota mais dura, aplicável só nos primeiros 180 dias — um CDB de 100% do CDI ainda entrega cerca de **10,8% líquidos ao ano**.

**Sobre o argumento da segurança:** **poupança e CDB têm exatamente a mesma cobertura do FGC** — os mesmos R$ 250 mil, o mesmo teto de R$ 1 milhão, a mesma fila, o mesmo app. A poupança não é mais garantida; é apenas mais familiar. E o **Tesouro Selic não tem FGC porque não precisa**: o devedor é o Tesouro Nacional.

---

# SEÇÃO 6 — COMPARAÇÃO LÍQUIDA: R$ 1.000 APLICADOS

## 6.1 Insumos e método — declarados

**Taxas utilizadas:**
- **CDI: 13,90% a.a.** — BCB/SGS 4389, valor literal `13.90`, data 28/08/2026
- **Selic efetiva: 13,90% a.a.** — BCB/SGS 1178, valor literal `13.90`, data 28/08/2026
- **Poupança: 0,6455% ao mês** — BCB/SGS 25, período 28/08→28/09/2026, projetada constante

**Método:**
- Capitalização em **dias úteis, base 252**: 30 dias corridos = 21 úteis; 6 meses (182 d) = 126 úteis; 1 ano (365 d) = 252 úteis; 2 anos (730 d) = 504 úteis
- Fator diário = (1 + i)^(1/252) − 1, com o %CDI aplicado ao fator diário
- Poupança capitalizada mensalmente: (1 + 0,006455)^(dias/30)

**Tributação aplicada:**
- **IR** (Lei 11.033/2004): 22,5% (30 dias e 182 dias); 20% (365 dias); 15% (730 dias)
- **IOF: ZERO em todos os horizontes**, pois todos ≥ 30 dias (Decreto 6.306/2007, Anexo)
- **Custódia B3: ZERO**, pois R$ 1.000 está dentro da isenção de R$ 10.000 do Tesouro Selic
- **Poupança e LCI: sem IR**

> **ESTES SÃO VALORES CALCULADOS, NÃO LIDOS.** São projeções sob taxa constante — o CDI e a TR variam.

## 6.2 Valor líquido final (R$) — de R$ 1.000 aplicados

| Aplicação | 30 dias | 6 meses | 1 ano | 2 anos |
|---|---:|---:|---:|---:|
| Poupança | 1.006,46 | 1.039,81 | 1.081,43 | 1.169,49 |
| Tesouro Selic | 1.008,45 | 1.053,79 | 1.114,68 | 1.252,72 |
| CDB 100% CDI | 1.008,45 | 1.053,79 | 1.114,68 | 1.252,72 |
| CDB 110% CDI | 1.009,30 | 1.059,36 | 1.126,98 | 1.281,80 |
| CDB 120% CDI | 1.010,15 | 1.064,97 | 1.139,45 | 1.311,63 |
| LCI 90% CDI (isenta) | 1.009,81 | 1.060,32 | 1.124,28 | 1.263,99 |

## 6.3 Rendimento líquido (R$)

| Aplicação | 30 dias | 6 meses | 1 ano | 2 anos |
|---|---:|---:|---:|---:|
| Poupança | 6,46 | 39,81 | 81,43 | 169,49 |
| Tesouro Selic | 8,45 | 53,79 | 114,68 | 252,72 |
| CDB 100% CDI | 8,45 | 53,79 | 114,68 | 252,72 |
| CDB 110% CDI | 9,30 | 59,36 | 126,98 | 281,80 |
| CDB 120% CDI | 10,15 | 64,97 | 139,45 | 311,63 |
| LCI 90% CDI (isenta) | 9,81 | 60,32 | 124,28 | 263,99 |

## 6.4 IR pago (R$)

| Aplicação | 30 dias | 6 meses | 1 ano | 2 anos |
|---|---:|---:|---:|---:|
| Poupança | 0,00 | 0,00 | 0,00 | 0,00 |
| Tesouro Selic | 2,45 | 13,45 | 24,33 | 44,60 |
| CDB 100% CDI | 2,45 | 13,45 | 24,33 | 44,60 |
| CDB 110% CDI | 2,70 | 14,84 | 26,94 | 49,73 |
| CDB 120% CDI | 2,95 | 16,24 | 29,58 | 54,99 |
| LCI 90% CDI (isenta) | 0,00 | 0,00 | 0,00 | 0,00 |

**IOF pago: R$ 0,00 em todas as linhas e todos os horizontes** (todos ≥ 30 dias).

## 6.5 O que a tabela mostra

1. **A poupança perde para tudo, em todos os prazos.** Em dois anos, R$ 169,49 contra R$ 252,72 do Tesouro Selic — **49% a mais** para o Tesouro, já líquido de IR. A isenção não salva.

2. **Uma LCI isenta a 90% do CDI bate um CDB tributado a 100%** em todos os prazos (R$ 9,81 vs R$ 8,45 em 30 dias; R$ 263,99 vs R$ 252,72 em 2 anos). Regra prática ao comparar: uma LCI a 90% equivale a um CDB de ~116% do CDI na faixa de 22,5%, e de ~106% na faixa de 15%. **A vantagem da isenção encolhe conforme o prazo aumenta e o IR cai.**

3. **Contra um CDB de 110% ou 120%, a LCI de 90% perde** — a isenção não cobre 30 pontos de CDI.

4. **Tesouro Selic e CDB 100% do CDI empatam** nesta simulação, porque CDI e Selic efetiva estão ambos em 13,90% e a custódia é isenta em R$ 1.000. **A partir de R$ 10.000 em Tesouro Selic**, a custódia de 0,20% a.a. incide sobre o excedente e desempata a favor do CDB — desde que o emissor do CDB seja bom.

> **LEITURA OBRIGATÓRIA JUNTO COM A SEÇÃO 3:** a linha "CDB 120% CDI" rende R$ 58,91 a mais que a de 100% em dois anos. **Era esse o prêmio que o Banco Master oferecia — e ele pagava 140%.** Dentro do FGC, o custo desse prêmio foram 62 dias sem acesso ao dinheiro. Acima do FGC, o custo foi o principal.

---

# SEÇÃO 7 — REGISTRO DE FONTES

Todos os acessos em **31/08/2026**.
**COMPLETO** = o dado buscado foi obtido integralmente · **PARCIAL** = a fonte respondeu, mas não continha tudo · **NÃO OBTIDO** = falha de acesso ou ausência do dado.

| # | URL | Tipo | O que forneceu | Status |
|---|---|---|---|---|
| 1 | `api.bcb.gov.br/dados/serie/bcdata.sgs.432` · `.4389` · `.12` · `.25` · `.226` · `.1178` · `.4391` | Primária — BCB | Selic meta 14,00; CDI 13,90; CDI diário 0,051660; poupança 0,6455; TR 0,1448; Selic efetiva 13,90; séries mensais de CDI e poupança | **COMPLETO** |
| 2 | https://www.fgc.org.br/sobre-garantia-fgc | Primária — FGC | R$ 250 mil por conglomerado; R$ 1 mi em 4 anos; listas de cobertos e não cobertos | **COMPLETO** |
| 3 | https://www.fgc.org.br/pagamento-de-garantia | Primária — FGC | Procedimento; ~30 dias úteis para a lista; crédito em até 48 horas úteis; app FGC / Portal Investidor | **COMPLETO** |
| 4 | https://static.poder360.com.br/2025/11/comunicado-BC-Master-liquidacao-extrajudicial-18nov2025.pdf | Primária — Comunicado BC nº 44.238 | Liquidação 18/11/2025; Ato 1.373; base legal; indisponibilidade de bens; nomes de controladores e ex-administradores; liquidante | **COMPLETO** |
| 5 | https://static.poder360.com.br/2025/11/master-comunicado-fgc-18nov2025.pdf | Primária — Comunicado FGC | Atos 1.369/1.371/1.372/1.373; 1,6 mi de credores; ~R$ 41 bi; patrimônio FGC R$ 160 bi / R$ 122 bi líquidos; prazo médio 30 dias | **COMPLETO** |
| 6 | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12703.htm | Primária — Lei 12.703/2012 | Regra da poupança: 0,5% a.m. acima de 8,5%; 70% da Selic mensalizada nos demais casos | **COMPLETO** |
| 7 | https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm | Primária — Lei 11.033/2004 | Tabela regressiva de IR (22,5 / 20 / 17,5 / 15). Página marca a MP 1.303/2025 como "Vigência encerrada" | **COMPLETO** |
| 8 | https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/decreto/d6306.htm | Primária — Decreto 6.306/2007 | Art. 32 e Anexo integral: IOF de 96% do rendimento no 1º dia a 0% no 30º | **COMPLETO** |
| 9 | https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/precotaxatesourodireto.csv | Primária — Tesouro Nacional | 58 títulos com taxas e PUs; data-base 28/08/2026; arquivo atualizado 31/08/2026 10:20 | **COMPLETO** |
| 10 | https://www.tesourodireto.com.br/tesouro-reserva | Primária — Tesouro | R$ 1,00 mínimo; 100% da Selic; 24×7 exceto 0h–1h; custódia 0,20% com isenção até R$ 10.000; IR regressivo; IOF até 30 dias | **COMPLETO** |
| 11 | https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm | Primária — Tesouro | Mercado aberto; 9h30–18h00; atualização "31/08/2026 - 09h21 min". **Tabela de títulos não renderizou** | **PARCIAL** |
| 12 | https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/tarifas-de-tesouro-direto/ | Primária — B3 | 0,20% a.a.; provisionada diariamente; cobrada em venda/vencimento/juros; isenções de Selic (R$ 10 mil), Educa+ e Renda+ | **COMPLETO** |
| 13 | https://www.b3.com.br/pt_br/produtos-e-servicos/tesouro-direto/tesouro-direto/perguntas-frequentes/ | Primária — B3 | Fração 0,01; mínimo R$ 30,00; teto R$ 1 mi/mês; fluxo de liquidação da venda antecipada | **COMPLETO** |
| 14 | https://nubank.com.br/conta/ | Institucional | Conta 100% CDI com regra de 30 dias; RDBs da Nu Financeira; FGC; conta de pagamento lastreada em títulos públicos | **COMPLETO** |
| 15 | https://nubank.com.br/nu/caixinhas | Institucional | Caixinhas 100% CDI; Turbo até 120% / 115%; R$ 900/mês; Ultravioleta e Nubank+; validade; FGC; R$ 1 mínimo; IR e IOF | **COMPLETO** |
| 16 | https://picpay.com/pt-br/pf/conta-digital | Institucional | "102% do CDI todo dia útil". Sem emissor, FGC, teto ou carência | **PARCIAL** |
| 17 | https://www.mercadopago.com.br/ | Institucional | "Até 105% do CDI na sua Conta"; "Até 120% do CDI nos Cofrinhos" | **PARCIAL** |
| 18 | https://inter.co/pra-voce/investimentos/meu-porquinho/ | Institucional | Porquinho até 100% CDI; R$ 1,00; D+1; FGC R$ 250 mil / R$ 1 mi em 4 anos | **PARCIAL** |
| 19 | https://inter.co/pra-voce/investimentos/renda-fixa/ | Institucional | CDB/LCI/LCA com FGC; LCA prazo a partir de 90 dias. **Sem %CDI publicado** | **PARCIAL** |
| 20 | https://neon.com.br/ | Institucional | "CDB Neon tem o melhor rendimento do mercado: até 113% do CDI" | **PARCIAL** |
| 21 | https://www.willbank.com.br/ | Institucional | Aviso de liquidação: Ato 1.376 de 21/01/2026; antecipação FGC até R$ 1.000; ~R$ 200 mi; boleto para faturas; canais de credores | **COMPLETO** |
| 22 | https://agenciabrasil.ebc.com.br/economia/noticia/2026-01/fgc-ja-pagou-r-325-bilhoes-75-dos-credores-do-banco-master | Imprensa · 29/01/2026 | R$ 32,5 bi; 580 mil credores (75%); 80,05% do previsto; base ~R$ 40,6 bi; início 19/01/2026; limite compartilhado Master/Will | **COMPLETO** |
| 23 | https://www.cnnbrasil.com.br/economia/financas/caso-master-fgc-ja-pagou-89-do-valor-devido-a-credores/ | Imprensa · 06/02/2026 | R$ 36 bi; 89% do devido; 628 mil credores (81%); R$ 6,3 bi ao Will Bank | **COMPLETO** |
| 24 | https://newblogs.correiobraziliense.com.br/blog-da-rosana-hessel/caso-master-fgc-informa-o-pagamento-de-9787-dos-valores-previstos/ | Imprensa · 13/05/2026 | R$ 39,7 bi; 97,87%; 915 mil beneficiários; 92,67% dos credores | **COMPLETO** |
| 25 | https://www.terra.com.br/economia/pleno-reag-e-will-entenda-as-8-liquidacoes-em-torno-do-caso-do-banco-master,efab47968fa81f17857d14e6843b2dc77io1583d.html | Imprensa · 20/02/2026 | As 8 liquidações com datas e motivos | **COMPLETO** |
| 26 | https://jornalggn.com.br/justica/crimes-prisao-preventiva-vorcaro-operacao-compliance-zero/ | Imprensa · 04/03/2026 | Prisão preventiva 03/03/2026, STF, min. André Mendonça; sete crimes; quatro núcleos | **COMPLETO** |
| 27 | https://en.wikipedia.org/wiki/Banco_Master_scandal | Terciária | Prisão 17/11/2025 em Guarulhos (jato para Malta); rombo até R$ 12 bi (PF); cronologia BRB; 2ª prisão 04/03/2026; Potim | **PARCIAL** |
| 28 | https://www.gazetadopovo.com.br/economia/cdbs-do-banco-master-o-que-acontece-com-quem-aplicou/ | Imprensa · 11/04/2025 | CDBs do Master "até 140% do CDI, taxa muito acima da média do mercado" | **COMPLETO** |
| 29 | https://investnews.com.br/investimentos/cdbs-bancos-medios-pagam-107-cdi/ | Imprensa · 12/06/2026 | Máximas 106,9% (Qista), 106% (Pine, BMG); BB 95%, Caixa 90%, Santander 97% | **COMPLETO** |
| 30 | https://www.seudinheiro.com/2026/financas-pessoais/cofrinho-de-140-do-cdi-do-mercado-pago-vale-a-pena-campanha-tem-prazo-limitado-e-regras-para-garantir-o-retorno-mlim/ | Imprensa · 04/03/2026 | Campanha 140% CDI 03/03–03/04/2026; só Meli+; teto R$ 10 mil; 115% com R$ 1–5 mil; cofrinhos em Tesouro Selic | **COMPLETO** |
| 31 | https://www.seudinheiro.com/2026/renda-fixa/conselho-monetario-nacional-aperta-regras-do-fgc-e-impoe-novas-travas-a-grandes-emissoes-de-cdb-lci-e-lca-mlim/ | Imprensa · 24/04/2026 | Resolução CMN 5295: CA de 0,01% para 0,02%; gatilho 60%; MATPF; vigência 01/06/2026, escalonada 2026–2028 | **PARCIAL** |
| 32 | https://www.infomoney.com.br/onde-investir/fim-do-cdb-de-120-do-cdi-nova-regra-do-fgc-impacta-taxas/ | Imprensa · 06/09/2025 | CA de 0,01% para 0,02%; gatilho de 75% para 60%; vigência junho/2026; CDBs de agosto não passaram de 107% | **PARCIAL** |
| 33 | https://blog.daycoval.com.br/mp-1303/ | Imprensa/institucional | MP 1.303/2025 rejeitada pela Câmara em outubro/2025; tabela regressiva mantida; LCI/LCA seguem isentas | **COMPLETO** |
| 34 | `bcb.gov.br/api/conteudo/app/normativos/exibenormativo` e `bcb.gov.br/api/search/app/normativos/buscanormativo` | Primária — BCB | **Texto oficial das Resoluções CMN 5.238 e 5.295.** Retornou `{"conteudo":[]}`; busca alternativa: "Requisição Inválida" | **NÃO OBTIDO** |
| 35 | https://www.bcb.gov.br/estabilidadefinanceira/remuneradepositospoupanca · https://www.bcb.gov.br/detalhenoticia/nota/775 | Primária — BCB | Páginas dependentes de JavaScript; sem conteúdo textual. Regra da poupança obtida na Lei 12.703 (Planalto) | **NÃO OBTIDO** |
| 36 | https://www.c6bank.com.br/conta-digital · https://www.c6bank.com.br/investimentos · https://www.bancopan.com.br/ · https://www.bancobmg.com.br/ | Institucional | HTTP 403 — bloqueio a acesso automatizado | **NÃO OBTIDO** |
| 37 | https://99app.com/pay/ | Institucional | HTTP 429 — limite de requisições | **NÃO OBTIDO** |
| 38 | https://www.itiunibanco.com.br/ | Institucional | HTTP 000 — falha de conexão | **NÃO OBTIDO** |
| 39 | https://www.original.com.br/ · https://www.digio.com.br/ · https://www.sofisadireto.com.br/ · https://www.agibank.com.br/ · https://www.daycoval.com.br/ | Institucional | Páginas carregaram (HTTP 200) sem qualquer menção a percentual do CDI | **NÃO OBTIDO** |
| 40 | https://www.sofisadireto.com.br/investimento/renda-fixa · https://www.sofisadireto.com.br/investimentos | Institucional | HTTP 404 (WebFetch) / sem dados numéricos de %CDI, prazo ou mínimo | **NÃO OBTIDO** |
| 41 | https://www.mercadopago.com.br/c/cofrinho · https://www.mercadopago.com.br/blog/investimento-cdb-cofrinhos-mercado-pago | Institucional | HTTP 403 nas duas. Natureza dos Cofrinhos veio de fonte secundária | **NÃO OBTIDO** |
| 42 | https://www.tesourodireto.com.br/tesouro-direto/custos-e-tributos.htm · /conheca/taxas.htm · /conheca/taxas-e-custos.htm · /conheca/imposto-de-renda-e-iof.htm · /b/entenda-a-nova-taxa-de-custodia | Primária — Tesouro | HTTP 404 em todas as variantes testadas. Dados supridos pela B3 e pelo Planalto | **NÃO OBTIDO** |
| 43 | https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json | Primária — Tesouro (API antiga) | HTTP 410 Gone — API descontinuada. Substituída pelo CSV do Tesouro Transparente | **NÃO OBTIDO** |
| 44 | https://www.nubank.com.br/contas/caixinhas/ · https://nubank.com.br/caixinhas/ · https://blog.nubank.com.br/caixinha-turbo-nubank/ · https://blog.nubank.com.br/caixinhas-do-nubank-como-funcionam/ | Institucional | HTTP 404 / 302 (redirect para /nu/caixinhas, seguido) | **NÃO OBTIDO** (supridas pelo item 15) |
| 45 | https://www.bancointer.com.br/investimentos/renda-fixa/ · https://www.bancointer.com.br/meu-porquinho/ · https://inter.co/conta-digital/ | Institucional | HTTP 404. Supridas por inter.co (itens 18–19) | **NÃO OBTIDO** |

**Resumo do registro:** 45 entradas · **COMPLETO: 22** · **PARCIAL: 11** · **NÃO OBTIDO: 12**

---

# SEÇÃO 8 — O QUE NÃO CONSEGUI OBTER

Declarado de forma explícita, para que nada aqui seja confundido com dado verificado.

### 1. %CDI, emissor, carência e teto de C6 Bank, 99Pay, Iti, Original, Banco Pan, Digio, Sofisa Direto, BMG, Agibank e Daycoval
Onze instituições solicitadas, **zero percentuais publicados em página aberta**. Três bloqueiam acesso automatizado (403: C6, Pan, BMG), uma limitou requisições (429: 99Pay), uma falhou na conexão (Iti), as demais simplesmente não divulgam. Esses dados existem apenas dentro dos aplicativos. Obter exigiria acesso autenticado ou navegador real — fora do que esta pesquisa fez.

### 2. Texto oficial das Resoluções CMN 5.238/2025 e 5.295/2026
A API de normativos do BCB devolveu conteúdo vazio (`{"conteudo":[]}`) e o buscador rejeitou as consultas ("Requisição Inválida"). Tudo o que a Seção 2 afirma sobre essas normas vem de imprensa especializada. **Os números 0,01% → 0,02%, o gatilho de 60%, a estrutura do MATPF e as datas de vigência não foram lidos no Diário Oficial.**

### 3. Natureza jurídica e emissor da Caixinha Turbo do Nubank
A página das Caixinhas afirma que "todas as Caixinhas são protegidas pelo FGC", mas **não identifica o emissor da Turbo nem o instrumento**. Por analogia com a página da conta seria RDB da Nu Financeira — **analogia não é confirmação**. Também não obtive o prazo exato da "validade" nem eventual teto de valor.

### 4. Natureza dos Cofrinhos do Mercado Pago — EVIDÊNCIA CONFLITANTE
A fonte secundária (Seu Dinheiro, 04/03/2026) afirma que aplicam em Tesouro Selic, o que implicaria **ausência de FGC**. Mas o próprio blog do Mercado Pago mantém artigo intitulado "O que é investimento CDB e como funciona nos Cofrinhos?", que **não consegui abrir (HTTP 403)**. É possível que coexistam duas modalidades (fundo e CDB). **Não trate a ausência de FGC como confirmada.**

### 5. Quais instituições zeram a taxa de agente de custódia no Tesouro Direto
Não consultei o ranking de agentes de custódia da B3. **Nenhum nome é citado neste dossiê** como praticante de taxa zero.

### 6. Condições do PicPay (102% do CDI)
Emissor, cobertura do FGC, teto e carência **não constam da página oficial**. Um número sem essas quatro informações não permite comparação de risco.

### 7. Prazo exato de liquidação do resgate no Tesouro Direto
O FAQ da B3 descreve um fluxo D+1 para o agente de custódia e D+2 para o investidor, com "prazo varia conforme instituição". **Não é o D+0 que se costuma afirmar.** Não obtive confirmação do horário de crédito ao investidor.

### 8. Desfecho da inspeção do TCU sobre a liquidação do Master
Há registro de que o BC desistiu de embargos e a inspeção foi autorizada. **O resultado não foi apurado.**

### 9. Ordem da fila de credores acima do limite do FGC na liquidação
Sabe-se que o excedente vira crédito contra a massa. **A ordem legal exata de habilitação e a expectativa de recuperação não foram confirmadas** em fonte primária.

### 10. Papel operacional detalhado do Will Bank no esquema e a oferta do Mubadala
A liquidação e o compartilhamento de limite FGC estão confirmados. **O papel operacional dentro do conglomerado e os termos da oferta do Mubadala não foram apurados.**

### 11. Poupança e CDI acumulados: CÁLCULO, NÃO LEITURA
Os **8,3144%** e **14,5707%** de 12 meses foram compostos por mim a partir das séries mensais do BCB. **As séries são primárias; a composição é derivação.** O mesmo vale para **toda a Seção 6**, que são projeções sob taxa constante.

### 12. Data de lançamento e eventual teto do Tesouro Reserva
A página oficial não menciona nenhum dos dois. A matéria da Agência Gov que poderia confirmar retornou **timeout de leitura**.

---

**Dossiê fechado em 31/08/2026.** Taxas de renda fixa mudam diariamente e as condições promocionais de fintechs mudam sem aviso — os percentuais da Seção 1 devem ser reconferidos antes de qualquer decisão. Este documento registra o que foi lido, onde e quando; não constitui recomendação de investimento.

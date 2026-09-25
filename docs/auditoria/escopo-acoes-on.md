# Escopo de análise por classe de ativo — Parte 2: Ações ON

**Emissão:** 02/09/2026. Sequência do documento de FII.
**Natureza:** escopo de engenharia. Define campos, fórmulas e força da evidência. **Não** é recomendação, não define limiares, não indica ativos.
**Fontes:** pesquisadas nesta sessão. Divergências registradas, não resolvidas.

---

## 1. Correção de pendência aberta

**PENDÊNCIA 13 — FECHADA, e a sua estava certa.** O `custos.yaml` registra "Lei 15.270/2025". Confirmado: (cite index="57-1">Lei nº 15.270, de 2025, disponível no Planalto em `_ato2023-2026/2025/lei/l15270.htm`</cite), (cite index="56-1">sancionada em 26 de novembro de 2025 e vigente desde 1º de janeiro de 2026</cite>. A fonte editorial que eu citei no documento de FII, grafando "15.570/25", está errada. Registro o erro: foi meu, por confiar em fonte secundária sem cruzar.

---

## 2. Por que a espécie é parâmetro, não detalhe

Ação ON é ação ordinária: um voto por ação. Isso importa por três motivos mensuráveis, e nenhum deles é o voto em si — um minoritário não derrota controlador em assembleia.

**Primeiro: tag along.** A Lei 6.404 assegura ao ON minoritário, em alienação de controle, no mínimo 80% do valor pago ao controlador. PN não tem esse direito por lei. É a diferença mais concreta entre as espécies e é campo binário.

**Segundo: o segmento de listagem.** O Novo Mercado admite apenas ON, com regra de uma ação, um voto. Portanto a espécie ON é pré-condição do segmento com a evidência mais favorável — ver §4.4.

**Terceiro: liquidez.** No Brasil, historicamente, muitas companhias concentraram liquidez na PN. Um ON pode ser a espécie "melhor" e a menos negociável da mesma companhia. Espécie e liquidez precisam ser campos separados, e o filtro de elegibilidade opera sobre o **par companhia × espécie**, não sobre a companhia.

**Consequência de modelo de dados:** a chave de análise não é `codeCVM`. É `codeCVM × especie × ticker`. Fundamento é da companhia; liquidez, tag along e preço são do papel. Misturar os dois produz um score de companhia atribuído a um papel que ninguém negocia.

Nota sobre o seu `politica.yaml`: `especies_permitidas: [ON, PN, UNIT]`. Manter as três é defensável — a auditoria já registrou que a justificativa foi não perder bancos —, mas então `tag_along` e `segmento` viram campos de score, e não consequência automática da espécie.

---

## 3. Regime tributário como parâmetro

Mudou em 2026 e a mudança é estrutural para a análise de dividendos.

**Ganho de capital.** 15% sobre o ganho em operação comum, 20% em day trade, com IRRF de 0,005% na fonte. Isenção de R$ 20 mil de alienações no mês — e esta **existe para ação**, ao contrário de ETF e FII. É o único ativo do seu universo com essa isenção, e isso é um parâmetro real de comparação entre rotas.

**Dividendos — o regime novo.** (cite index="62-1">A partir de 1º de janeiro de 2026 há tributação na fonte à alíquota de 10% sobre lucros e dividendos distribuídos a pessoas físicas residentes em montante superior a R$ 50.000,00 por mês pagos por uma mesma pessoa jurídica</cite>. (cite index="56-1">A retenção incide sobre o valor total distribuído, não apenas sobre o excedente</cite>, e (cite index="56-1">funciona como antecipação do IRPFM, podendo ser restituída se o contribuinte não atingir o limite anual</cite>.

**IRPFM.** (cite index="56-1">Tributação mínima anual para pessoas físicas com renda total acima de R$ 600.000: alíquota progressiva de 0% a 10% entre R$ 600.001 e R$ 1.200.000, e mínima fixa de 10% acima de R$ 1.200.000</cite>. (cite index="56-1">Há redutor que impede bitributação: a soma das alíquotas efetivas da pessoa jurídica e da pessoa física não pode superar 34% para empresas em geral</cite>. A base do IRPFM (cite index="56-1">considera a renda total — tributável, isenta e exclusiva</cite>.

**Transição.** (cite index="59-1">Lucros aprovados até o fim de 2025 podem ser pagos até o último dia útil de 2028 sem a incidência dos 10%</cite>.

**Regulamentação:** IN RFB 2.299/2025 e o Perguntas e Respostas divulgado em 16/12/2025.

### 3.1 O que isso significa para o sistema

O limiar de R$ 50 mil é **por pessoa jurídica pagadora, por mês**. Para carteira diversificada de varejo, praticamente nunca dispara — o que é uma boa notícia e uma armadilha de modelagem: a regra existe, é calculável, e vira relevante em concentração alta ou patrimônio elevado.

| Campo | Fórmula | Por que |
|---|---|---|
| T-01 `div_mensal_por_pagadora` | Provento por CNPJ por mês | Único agregador correto. Por ticker está errado: ON e PN da mesma companhia somam |
| T-02 `irrf_dividendo_projetado` | 10% do total se T-01 > 50.000 | Cliff, não marginal |
| T-03 `renda_total_anual_projetada` | Base do IRPFM, inclui isentos | Aqui entram os rendimentos de FII, que são isentos mas **contam na base** |
| T-04 `jcp_vs_dividendo` | JCP retém 15% na fonte; dividendo, 0% ou 10% no cliff | O regime novo **estreitou** a diferença. Uma empresa que paga por JCP entrega menos líquido em faixas baixas do que uma que paga dividendo |
| T-05 `isencao_20k_usada_no_mes` | Soma de alienações de ação no mês | Só ação. Consumir com ETF não é possível — não há isenção lá |

**T-04 é o campo com maior consequência analítica.** Todo comparativo de dividend yield entre companhias que existia até 2025 comparava dividendo isento com JCP a 15% líquido. A partir de 2026 há um terceiro estado. Qualquer série histórica de "DY líquido" que atravesse 01/01/2026 sem essa quebra está errada — e é exatamente o tipo de erro que o `dt_disponivel` não pega, porque não é defasagem de dado, é mudança de regime.

---

## 4. O que a evidência brasileira sustenta

Esta seção é desconfortável e é a razão de existir do documento.

### 4.1 Existe biblioteca de fatores brasileira, pública e gratuita

O NEFIN (Núcleo de Pesquisas em Economia Financeira da USP) publica séries de fatores de risco brasileiros — mercado, tamanho, book-to-market, momento e iliquidez —, usadas como padrão na literatura nacional. (cite index="65-1">O fator de iliquidez refere-se ao retorno de uma carteira comprada em ações não líquidas e vendida em ações líquidas</cite>.

**Consequência prática, e é grande:** você não precisa construir os fatores para ter benchmark. Já existem, são públicos, e permitem calcular alfa da sua política contra um modelo de fatores brasileiro em vez de contra o Ibovespa apenas. Isso torna o backtest muito mais forte por custo quase zero, e é um insumo que nenhum dos documentos anteriores do projeto mencionava.

**→ NOVA PENDÊNCIA 19: obter a documentação e as séries do NEFIN, verificar cobertura temporal e critério de construção das carteiras.**

### 4.2 Momento é forte no Brasil. Valor e tamanho, não.

Os prêmios médios mensais reportados a partir das séries do NEFIN são desconcertantes para quem espera o padrão americano: (cite index="65-1">a carteira long-short de momento (WML) apresentou prêmio médio mensal de 1,1% no Brasil, contra 0,74% nos EUA; os fatores de mercado, tamanho e book-to-market apresentaram prêmios mensais médios de 0,3%, −0,02% e 0,05%, respectivamente</cite>.

Leia de novo: **HML a 0,05% ao mês e SMB negativo.** O prêmio de valor, que é o alicerce da narrativa fundamentalista brasileira, é praticamente nulo no período medido. O de tamanho é negativo.

E a magnitude do momento: (cite index="66-1">nos dez anos anteriores a 2020, uma carteira formada pela estratégia de momento teve rentabilidade superior a 528%, enquanto o retorno de mercado foi de −16,32%</cite>.

`PARCIAL — os prêmios vêm de tabela descritiva de um artigo, e período e amostra não foram verificados no texto integral.`

### 4.3 Lucratividade e investimento: o modelo explica, mas não há prêmio

Este é o achado que contradiz diretamente o que eu especifiquei no escopo geral.

(cite index="67-1">Analisando o modelo de cinco fatores de Fama e French no mercado acionário brasileiro pela metodologia de Fama e MacBeth, as regressões do primeiro passo sugeriram que o modelo de cinco fatores tem o melhor desempenho na explicação dos retornos. No entanto, nas regressões do segundo passo, **não se verificaram prêmios de risco associados à lucratividade e ao investimento**</cite>.

Ou seja: no Brasil, os dois fatores que eu recomendei como campos de melhor evidência — lucratividade bruta (Novy-Marx) e crescimento de ativos (Cooper, Gulen & Schill) — **explicam** a variação dos retornos mas **não foram remunerados** como prêmio de risco no período estudado.

E há suporte para acrescentar momento ao modelo: (cite index="66-1">um modelo de seis fatores, com o fator momento adicionado ao de cinco, apresentou maior poder de explicação, em alfa e em R² ajustado, para o mercado brasileiro entre 1999 e 2016</cite>. (cite index="68-1">Outro trabalho, dissecando anomalias no mercado brasileiro, encontrou o modelo de seis fatores com melhor desempenho para portfólios tamanho-momento e tamanho-volatilidade, e o de cinco fatores para portfólios tamanho-emissões líquidas</cite>.

### 4.4 Governança tem evidência, e ela aponta para ON

(cite index="73-1">Empresas com melhor qualidade de governança corporativa tendem a apresentar desempenho financeiro estatisticamente superior às de qualidade inferior no mercado brasileiro</cite>.

E há um achado específico sobre o Novo Mercado: (cite index="72-1">investigando o retorno anormal de adquirentes em torno do anúncio de aquisições, encontrou-se relação positiva com a adesão ao Novo Mercado, mas não com as demais variáveis de governança testadas (Nível 2 e programas de ADR níveis II e III). As empresas do Novo Mercado são justamente as que não emitem ações sem direito a voto, o que limita a capacidade dos controladores de separar direitos de voto de direitos sobre fluxo de caixa</cite>.

Isso é o argumento mais direto a favor da espécie ON que a literatura brasileira oferece, e ele não é sobre o voto — é sobre a **ausência de separação entre controle e fluxo de caixa**, que reduz benefícios privados de controle.

Contexto estrutural que a literatura registra: (cite index="71-1">estudos brasileiros evidenciam elevada concentração da propriedade nas empresas listadas</cite>, e (cite index="75-1">a concentração acionária em empresas familiares é apontada como barreira à adoção de conselhos independentes</cite>. Sobre estatais, (cite index="71-1">sua natureza institucional e estrutura de controle tornam complexas a definição de objetivos operacionais e a avaliação de desempenho, já que a atuação está sujeita ao controlador imediato, o governo, e ao controlador indireto, a sociedade, além das expectativas de retorno dos sócios privados</cite>.

### 4.5 Síntese, e o que ela obriga a admitir

| Fator | Evidência **brasileira** | Uso |
|---|---|---|
| Momento | **A mais forte** | Catálogo de posição tática. **Não** é buy & hold |
| Governança / Novo Mercado | Moderada | Portão ou campo de score |
| Iliquidez | Fator estabelecido no NEFIN | Portão de elegibilidade |
| Book-to-market (valor) | **Muito fraca** — 0,05% a.m. | Campo, marcado |
| Tamanho | **Negativa** — −0,02% a.m. | Campo, marcado |
| Lucratividade | Explica, **sem prêmio** no 2º passo | Campo, marcado |
| Investimento / crescimento de ativos | Explica, **sem prêmio** no 2º passo | Campo, marcado |
| Accruals, qualidade do lucro | Não localizada evidência brasileira nesta busca | Campo de **exclusão**, não de seleção |

**A admissão honesta:** o fator com melhor evidência brasileira é um fator de negociação, não de posse. E os fatores fundamentalistas que sustentariam um catálogo de buy & hold têm evidência local fraca ou nula.

Isso **não** invalida o catálogo — muda o que ele é. Os campos fundamentalistas se justificam como **portão de exclusão** (evitar fraude, insolvência, diluição, iliquidez), onde a evidência é melhor e a lógica não depende de prêmio de risco, e como **descrição do negócio**, que é o objetivo de aprendizado que você declarou. Não se justificam, com a evidência disponível, como máquina de seleção.

E reforça a pergunta A-05, que segue aberta desde o laudo Rev. 03: se valor não paga, tamanho é negativo, lucratividade e investimento não têm prêmio, e o que sobra é momento — a hipótese nula do índice fica mais forte, não mais fraca.

---

## 5. Catálogo — ON de buy & hold

Os blocos abaixo herdam o escopo geral. O que muda aqui é a calibração à evidência brasileira e os campos específicos de ON.

### Bloco A · Elegibilidade do par companhia × espécie (portão)

| # | Campo | Fonte | Nota |
|---|---|---|---|
| A-01 | Liquidez média diária, 60 pregões | COTAHIST | Do **ticker**, não da companhia |
| A-02 | Pregões com negócio em 60 | COTAHIST | — |
| A-03 | Free float | FRE | — |
| A-04 | **Segmento de listagem** | B3 | Novo Mercado tem evidência específica (§4.4) |
| A-05 | **Tag along** | FRE / estatuto | 100% no Novo Mercado; mínimo legal de 80% para ON |
| A-06 | **Estrutura de controle** | FRE | Controle definido, difuso, familiar ou estatal |
| A-07 | **Separação voto × fluxo de caixa** | Composição do capital | O mecanismo que a evidência de §4.4 aponta. Companhia só-ON tem separação nula |
| A-08 | Anos de fundamento disponível | `fato_contabil` | < 3 anos ⇒ catálogo de aposta |
| A-09 | **Reapresentações** | `count(versao > 1)` | Depende da correção A-01 do laudo. Proxy de qualidade contábil que ninguém publica |
| A-10 | Opinião do auditor e ressalvas | Notas | `NÃO OBTIDO` sem extração de texto |

### Bloco B · Rentabilidade

Marcados `evidencia: sem_premio_local` conforme §4.3 — exibidos e usados como descrição, não como seleção.

ROIC · Lucro bruto / ativos · Margem bruta em série de 10 anos · Desvio-padrão e mínimo do ROIC · ROIC − custo de capital (estimativa, declarar premissas) · DuPont · Anos consecutivos com ROIC positivo.

### Bloco C · Solvência (portão)

Cobertura de juros (EBIT / despesa financeira líquida) · Dívida líquida / EBITDA · Perfil de vencimento · **Moeda da dívida × moeda da receita** · Caixa / dívida de curto prazo · Escore de insolvência como rastreio.

**Financeiras continuam sem bloco.** C-01 a C-03 são indefinidos para banco e seguradora, e o substituto — Basileia, imparidade, custo do crédito, eficiência — não está especificado em lugar nenhum do projeto desde o achado A-06. Com `especies_permitidas` incluindo PN para reter bancos, isto é lacuna ativa. **PENDÊNCIA 20.**

### Bloco D · Qualidade do lucro

Accruals de Sloan · FCO / lucro líquido em 5 anos · Capex / depreciação · Receita × recebíveis · Receita × estoque · Dias de capital de giro · Rastreio de manipulação · Partes relacionadas.

**É o bloco com melhor razão evidência/esforço no contexto brasileiro**, porque funciona como exclusão e não depende de prêmio de risco. Sem evidência local localizada, mas a lógica de exclusão não exige prêmio.

### Bloco E · Alocação de capital

Crescimento do ativo total · **Diluição** · ROIC incremental · Payout total, **separando JCP de dividendo** (§3.1) · Aquisições e impairment histórico · Recompras.

### Bloco F · Preço

EV/EBIT · EV/FCF · P/VP (financeiras) · Earnings yield × NTN-B real · Percentil histórico do múltiplo · DY, marcado.

**Calibração local:** com HML a 0,05% ao mês, "comprar barato" não teve prêmio no período medido. O bloco F é contexto de entrada, não tese.

### Bloco G · Risco brasileiro

Controle estatal ou golden share · Exposição regulatória e tarifária · Concentração de cliente e fornecedor · Exposição cambial líquida · ADR e dupla listagem · Litígio tributário e provisões.

---

## 6. Catálogo — ON de posição especulativa

### Bloco H · Sobrevivência

Queima mensal · Meses de pista · Emissões em 36 meses · **Diluição acumulada** · Vencimentos em 24 meses · Covenants.

### Bloco I · Qualidade do crescimento

Orgânico × por aquisição · Receita × recebíveis · **Trajetória da margem bruta na expansão** · Marketing / receita nova · Receita recorrente · Concentração de receita.

### Bloco J · Economia unitária

Margem de contribuição · Receita para o ponto de equilíbrio · Trajetória do FCO · Alavancagem operacional.

### Bloco K · Estrutura da posição — input do usuário

Perda máxima 100% · **Tese escrita e falsificável** · **Prazo, com data** · **Condição de falsificação** · Liquidez de saída · Insiders e lock-up.

### Bloco L · Sinais táticos, e onde eles pertencem

Aqui, e só aqui, entram os campos de momento — os de melhor evidência brasileira (§4.2), e que **não são de posse**: retorno acumulado 12 − 1 meses (definição padrão de WML) · retorno 6 meses · distância da máxima de 52 semanas · volume relativo.

**A regra que separa os dois catálogos:** um campo de momento **nunca** entra no score de buy & hold. Se ele entrar, o catálogo deixa de medir durabilidade e passa a medir preço recente, e o horizonte declarado vira ficção. Isso é código, não convenção.

### Bloco M · Teste de classificação e o que não se aplica

Roda os portões A e C, registra o que reprova, com data. Não impede a compra; impede a reclassificação retroativa.

Inaplicáveis: múltiplo de lucro sem lucro · DY em empresa que não distribui · ROIC com base de capital em mudança · qualquer média de 10 anos em série de 3 · e **crescimento de ativos com sinal negativo**, que aqui é a tese.

---

## 7. Fontes e disponibilidade

| Bloco | Fonte | Status |
|---|---|---|
| A-01, A-02 | COTAHIST | `COMPLETO` — depende do layout, pendência 1 |
| A-03 a A-07 | FRE (CVM) | `PARCIAL` — o FRE é anual e parcialmente não estruturado |
| A-08, A-09 | `fato_contabil` | `COMPLETO` após a correção da Silver |
| B, C, D, E | DFP e ITR | `COMPLETO` |
| F | DFP + COTAHIST + ANBIMA | `COMPLETO` |
| G-01, G-02, G-06 | FRE e notas | `NÃO OBTIDO` sem extração de texto |
| L | COTAHIST ajustado | `COMPLETO` |
| Fatores de referência | **NEFIN** | `NÃO OBTIDO` — pendência 19 |

**Comparado ao FII, a situação é muito melhor:** os blocos B, C, D, E, F e L saem inteiros de CVM e COTAHIST. Não há equivalente ao problema dos blocos C e D do FII, que exigem extração de PDF de relatório gerencial. **Ação ON é a classe mais construível do universo com a Fase 0 e a Fase 1.**

---

## 8. Estratégias validáveis

Cada uma com hipótese, sinal esperado e critério de rejeição escritos **antes** de rodar.

| # | Estratégia | Hipótese | Base | Rejeita se |
|---|---|---|---|---|
| A1 | **Portão de exclusão puro** | Excluir por iliquidez, insolvência, accruals altos e diluição melhora o retorno sem selecionar nada | Lógica de exclusão; não exige prêmio | Não superar o universo sem filtro |
| A2 | **Valor (B/M) — hipótese nula esperada** | Valor **não** paga no Brasil | (cite index="65-1">HML com prêmio médio mensal de 0,05%</cite> | **Espera-se que falhe.** Se "funcionar", há erro no pipeline |
| A3 | **Tamanho — hipótese nula esperada** | Small cap **não** paga | (cite index="65-1">SMB com prêmio médio mensal de −0,02%</cite> | Idem A2 |
| A4 | **Lucratividade** | Sem prêmio no Brasil | (cite index="67-1">sem prêmio de risco no segundo passo</cite> | Sinal positivo forte contraria a literatura — investigar antes de comemorar |
| A5 | **Momento (12−1)** | Sinal com melhor evidência local | (cite index="65-1">WML a 1,1% a.m.</cite> | Não bater o índice líquido de custo e imposto. **Atenção: gira, e o custo fiscal de 15% sobre ganho é real** |
| A6 | **Governança / Novo Mercado** | Restringir a Novo Mercado melhora o retorno ajustado | (cite index="72-1">relação positiva com adesão ao Novo Mercado</cite> | Não superar o universo irrestrito |
| A7 | **1/N do universo elegível** | Benchmark | DeMiguel et al. | — |
| A8 | **Índice puro, custo real** | **Hipótese nula verdadeira** | — | Se nada bate A8, a resposta é o índice |
| A9 | **Alfa contra fatores NEFIN** | A política tem retorno não explicado pelos fatores conhecidos | §4.1 | Alfa não distinguível de zero |

**A2, A3 e A4 são as mais valiosas da tabela, e as três devem falhar.** Três testes com resultado esperado negativo são o melhor controle de integridade que um backtest pode ter. Se qualquer uma "funcionar", investigue o look-ahead antes de investigar o mercado.

**A9 é a que muda o patamar do projeto.** Bater o Ibovespa pode ser exposição a fatores conhecidos. Alfa contra um modelo de fatores brasileiro é outra afirmação — e ela está a um download de distância.

**Sobre A5, uma ressalva que o backtest precisa incorporar:** momento exige giro; giro no Brasil gera ganho de capital tributável a 15%, com a isenção de R$ 20 mil/mês como amortecedor apenas em patrimônio pequeno. Um backtest de momento sem custo fiscal explícito superestima o resultado, e a magnitude do erro cresce com o patrimônio. Este é o único ponto do documento em que a tributação entra dentro do backtest, e não ao lado dele.

---

## 9. Pendências

**Fechada:** 13 (Lei 15.270/2025 confirmada; seu YAML estava certo).

**Novas:**

| # | Item | Bloqueia |
|---|---|---|
| 19 | Séries e documentação de fatores do NEFIN: cobertura, critério de construção, periodicidade | A9 — o teste de maior valor da tabela |
| 20 | Bloco de análise para instituições financeiras | Bloco C para bancos; lacuna aberta desde o achado A-06 |
| 21 | Texto integral dos artigos de §4.2 e §4.3: período, amostra, tratamento de sobrevivência | Toda a §4.5, que reorienta o catálogo |
| 22 | IN RFB 2.299/2025 e o Perguntas e Respostas de 16/12/2025 | T-01 a T-04 |
| 23 | Lei 6.404 art. 254-A (tag along) no original | A-05 |
| 24 | Layout do FRE e o que é estruturado nele | Blocos A-03 a A-07 e G |

**Limitações desta peça:** nenhuma norma foi lida no original; os artigos brasileiros foram lidos por resumo, não por texto integral, e período, amostra e tratamento de viés de sobrevivência não foram verificados — o que importa especialmente para os prêmios de §4.2, que são o achado mais consequente. Nenhum limiar aparece, de propósito.

---

## 10. O que muda no escopo geral por causa desta pesquisa

Três correções ao documento de escopo de campos, emitido antes destas buscas:

1. **A §2.2 daquele documento marcou lucratividade e crescimento de ativos como "evidência moderada-alta".** Isso vale para os EUA. No Brasil, (cite index="67-1">não se verificaram prêmios de risco associados à lucratividade e ao investimento</cite>. Rebaixe para `sem_premio_local` e mantenha como campo descritivo e de exclusão.

2. **Momento foi classificado como "não é métrica de buy & hold".** Continua verdade, mas é o fator com melhor evidência brasileira, e isso precisa aparecer — não como convite a virar trader, e sim como fato sobre o mercado que o backtest vai encontrar de qualquer forma.

3. **Faltava o benchmark de fatores.** Alfa contra um modelo de fatores local é qualitativamente diferente de "bateu o Ibovespa", e o insumo é público e gratuito. Deveria estar no pré-registro do backtest desde o início.

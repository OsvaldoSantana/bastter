# Estratégias de ações testadas no mercado brasileiro

**Emissão:** 02/09/2026. Sequência dos escopos de FII e de ações ON.
**Objeto:** levantar estratégias de seleção de ações que foram **testadas empiricamente no mercado brasileiro**, reportar o que os estudos encontraram, e submeter cada resultado à mesma auditoria metodológica que o projeto aplica a si mesmo.
**Natureza:** escopo de engenharia e revisão de literatura. **Não é recomendação de estratégia, de ativo ou de alocação.** Nenhum limiar é prescrito.
**Limitação declarada:** todos os artigos foram lidos por **resumo indexado**, não por texto integral. Período, amostra, tratamento de sobrevivência, custos e método de benchmark **não foram verificados**. Isso não é ressalva de rodapé — é o que separa "estratégia validada" de "estratégia com resultado publicado", e a §6 trata disso.

---

## 1. Critério de inclusão

Entrou nesta lista a estratégia que satisfaz três condições: **regra mecânica** (replicável sem julgamento), **testada com dados brasileiros**, e **resultado publicado com comparação a um benchmark**. Ficou de fora tudo que é discricionário, tudo que só tem evidência americana, e tudo que aparece apenas em material comercial.

---

## 2. Magic Formula (Greenblatt)

**Regra:** ordenar as ações por ROIC (qualidade) e por earnings yield — EBIT/EV — (preço), somar as duas posições no ranking, comprar as melhores. Rebalanceamento periódico.

### 2.1 O que os estudos encontraram

**UFRGS, 2000–2020.** (cite index="76-1">Os portfólios construídos a partir da Magic Formula e de seus componentes de valor e qualidade, testados isoladamente, apresentaram retornos superiores ao mercado. A carteira do fator valor apresentou os melhores resultados, com CAGR de 29,17% e Índice de Sharpe de 0,72, contra CAGR de 9,68% do Ibovespa no período. Por duplo ordenamento, obtiveram-se carteiras mais rentáveis e com melhor Sharpe do que ordenando por um fator apenas</cite>.

**Encontro Brasileiro de Finanças.** (cite index="80-1">Os resultados mostram que, quanto pior a classificação dos ativos no ranking, menor o retorno das carteiras, independentemente do período de permanência</cite>. Este é o achado mais importante da estratégia e o menos citado: **a monotonicidade do ranking**. Se o decil 1 rende mais que o 2, que rende mais que o 3, o sinal tem estrutura. Se só o topo funciona, é ruído no topo.

O mesmo trabalho documenta uma alteração relevante na implementação: (cite index="80-1">no lugar do NOPLAT, Greenblatt usa o EBIT — medida antes de impostos —, o que simplifica o procedimento; e há divergência na definição de capital investido</cite>. **Consequência de engenharia: "Magic Formula" não é uma especificação única.** Duas implementações honestas divergem no ROIC. O sistema precisa fixar a definição no `politica.yaml` e versioná-la.

**UERJ, 2007–2017.** (cite index="85-1">A carteira de Greenblatt obteve retorno anual de 11,06% e a de Piotroski 8,35%, contra 5,04% do Ibovespa</cite>.

**Estudo comparativo com modelo multifatorial.** (cite index="84-1">As carteiras de Piotroski, Graham e Greenblatt geraram rentabilidade anualizada de 30,06%, 36,14% e 21,92% respectivamente, superando a rentabilidade anualizada do Ibovespa</cite>.

**Backtest recente, não revisado por pares, 2012–2025.** (cite index="93-1">Usando base point-in-time livre de viés de sobrevivência, carteiras altamente concentradas (N=3) maximizaram retornos absolutos, acima de 1.500% no período, mas com máximo drawdown superior a 60%. A relação risco-retorno se otimizou em carteiras de 16 ativos com rebalanceamento trimestral, maximizando o Índice de Sortino</cite>. E, o que é mais útil: (cite index="93-1">observou-se subperformance em anos de forte alta de mercado, como 2021, quando a estratégia recuou 11,93% enquanto o benchmark avançou</cite>.

### 2.2 Leitura

A dispersão dos resultados é a informação. **11,06% ao ano (2007–2017), 21,92% (outro período), 29,17% no componente de valor (2000–2020), acima de 1.500% acumulado com N=3 (2012–2025).** São a mesma família de regra, e o resultado varia por fator de três ou mais conforme período, concentração e definição de ROIC. Isso não desqualifica a estratégia; **quantifica a sensibilidade a escolhas de implementação**, e é exatamente o que o pré-registro do seu backtest existe para conter.

O achado do drawdown de 60% com N=3 conversa diretamente com a Parte I do seu dossiê: concentração alta maximiza o resultado esperado do backtest e maximiza também a probabilidade de o investidor abandonar a regra no meio.

---

## 3. F-Score de Piotroski

**Regra:** dentro do universo de alto book-to-market, pontuar de 0 a 9 nove sinais contábeis binários — rentabilidade, alavancagem/liquidez, eficiência operacional. Comprar os de score alto.

**Insper, 2005–2015, com a adaptação brasileira de Lopes e Galdi (2007).** (cite index="83-1">O investidor poderia ter alterado os retornos médios ajustados ao mercado — diferença entre o retorno da carteira e o do IBrX-100 — de sua carteira de alto book-to-market de 6,8% em um ano e 16,2% em dois anos para 26,3% e 38,2% através deste método de seleção. Os testes estatísticos apresentaram que a estratégia foi significativa em distinguir firmas de boa performance das de má performance para todos os níveis de tamanho e diferentes níveis de liquidez e endividamento</cite>.

**Baldo (2016).** (cite index="82-1">O retorno médio executando long-short entre ações de score alto e score baixo aumenta em 48% o retorno, com significância estatística para diferentes níveis</cite>.

**Comparação com modelo de Ohlson.** (cite index="88-1">Uma pesquisa indica performance estatisticamente superior do portfólio de Ohlson: 46,97% de retorno anormal no primeiro ano contra 11,55% do portfólio Piotroski; no segundo ano, 67,54% contra 14,00%</cite>. `Nota: outro trabalho reporta, para o portfólio Ohlson,` (cite index="82-1">0,35 no primeiro ano e 0,50 no segundo, contra 0,10 e 0,17 do portfólio Piotroski</cite>`— escalas diferentes, provavelmente amostras diferentes. Divergência registrada.`

### 3.1 Por que o F-Score é o achado mais relevante deste levantamento

Três motivos, e nenhum é o retorno.

**Primeiro: é a única estratégia da lista que resolve a contradição do documento anterior.** A busca sobre fatores mostrou (cite index="65-1">HML com prêmio médio mensal de 0,05% no Brasil</cite> — valor praticamente não paga. Mas o F-Score não é uma estratégia de valor: é uma **estratégia de exclusão dentro do valor**. Ele parte do alto B/M e separa a empresa barata que se recupera da empresa barata que está morrendo. Se o prêmio de valor é nulo porque a média mistura as duas, um filtro que as separa pode produzir resultado onde o fator não produz. É uma hipótese testável e é o teste mais interessante que o seu backtest pode rodar.

**Segundo: é robusto a subamostras.** (cite index="83-1">Significativo para todos os níveis de tamanho e diferentes níveis de liquidez e endividamento</cite>. Robustez a corte é mais informativa que magnitude de retorno.

**Terceiro: é o que o escopo geral já classificou como bloco de exclusão.** Os nove sinais do F-Score são, em substância, os blocos C e D do catálogo de ON — solvência e qualidade do lucro. A evidência brasileira sustenta o uso desses campos como **portão**, que é precisamente onde eu os havia colocado, e não como score de seleção.

---

## 4. Graham

**Regra:** filtros de segurança e preço — endividamento, liquidez corrente, histórico de lucro, P/L e P/VP máximos.

Resultados divergem entre estudos. (cite index="84-1">Um trabalho reporta rentabilidade anualizada de 36,14% para a carteira de Graham</cite>; o mesmo levantamento registra que, em outra aplicação, (cite index="84-1">Graham não proporcionou retorno anormal</cite>. E a observação geral: (cite index="84-1">as aplicações no contexto brasileiro mostraram a necessidade de ajustar alguns dos limites dos filtros usados no processo de seleção</cite>.

**Leitura:** "ajustar os limites dos filtros" é, tecnicamente, calibrar parâmetros na mesma amostra em que se mede o resultado. Sem pré-registro do ajuste, o retorno reportado é in-sample. Graham fica marcado `evidencia: divergente, com risco de sobreajuste declarado pelos próprios autores`.

---

## 5. Momento

**Regra:** comprar as ações de melhor retorno passado num período de formação, manter por um período de permanência.

(cite index="97-1">Lacerda (2007) demonstrou rentabilidade anormal controlada pelo risco da estratégia de momentum no mercado brasileiro entre 1987 e 2006, para um portfólio com período de formação e de permanência de três meses</cite>. E, do documento anterior: (cite index="65-1">a carteira long-short de momento apresentou prêmio médio mensal de 1,1% no Brasil, contra 0,74% nos EUA</cite>; (cite index="66-1">nos dez anos anteriores a 2020, a carteira de momento rendeu mais de 528% enquanto o mercado caiu 16,32%</cite>.

Uma qualificação metodológica que a própria literatura levanta: (cite index="97-1">a diferença de evidências no Brasil em relação a outros mercados pode residir no fato de que as séries temporais brasileiras costumam incluir períodos com grande incidência de crises, que impactam significativamente o conjunto da série</cite>.

**Leitura:** é a estratégia com a evidência brasileira mais forte e a **menos compatível com o objetivo declarado do seu projeto**. Formação e permanência de três meses significa quatro rebalanceamentos por ano, cada venda com ganho de capital tributável a 15%, e a isenção de R$ 20 mil mensais só protege patrimônio pequeno. Nenhum dos retornos citados é líquido de imposto. **Um backtest de momento sem custo fiscal explícito não é comparável a um backtest de buy & hold**, e a diferença cresce com o patrimônio.

---

## 6. Dividend yield — a evidência é negativa

**SciELO, julho/1994 a dezembro/1999.** (cite index="91-1">Construíram-se mensalmente três carteiras — alto, baixo e zero dividend yield — e compararam-se risco, retorno e indicadores ajustados ao risco entre si e contra o Ibovespa. A evidência empírica é incapaz de sugerir que ações de alto dividend yield tendem a ter maiores ou menores taxas de retorno do que ações de baixo ou zero yield. As evidências sugerem que não é possível demonstrar uma clara associação entre dividend yield e taxas de retorno</cite>.

**Este é o terceiro achado independente na mesma direção**, e vale registrar a convergência: dividend yield não se sustentou como critério de seleção em ações brasileiras (aqui), em FIIs brasileiros (o estudo em que os fundos de maior DY mediano não estavam entre os de maior rentabilidade), nem no segmento de "ETF de renda" (a sua própria pesquisa sobre covered call). Três classes, três metodologias, mesma conclusão.

A amostra deste estudo é curta e antiga — cinco anos e meio, encerrando em 1999 — e precisa ser tratada como tal. Mas a direção é consistente com tudo o mais.

---

## 7. Baixa volatilidade

Não localizei estudo brasileiro revisado por pares nesta busca. O que existe é melhor que estudo, para efeito de validação: **um índice público, com metodologia divulgada e track record ao vivo**. (cite index="96-1">O S&P/B3 Baixa Volatilidade Altos Dividendos mede o desempenho das ações de menor volatilidade dentro de um grupo de componentes do S&P Brazil BMI com rendimento elevado de dividendos, sujeitos a requisitos de diversificação e negociabilidade, com componentes ponderados pelo rendimento dos dividendos</cite>.

**Por que isso vale mais que um backtest:** um índice publicado tem desempenho **out-of-sample a partir da data de lançamento**. Não há como sobreajustá-lo retroativamente. É o mesmo tipo de evidência que o SPIVA fornece, e é o padrão mais alto disponível sem rodar dinheiro real.

**→ PENDÊNCIA 25: obter a metodologia e a série do índice, e separar o período pré-lançamento (retroativo, sobreajustável) do pós-lançamento (out-of-sample).** É a distinção que decide o peso da evidência.

---

## 8. A tensão que este levantamento expõe

Duas literaturas brasileiras, sobre o mesmo mercado, dizem coisas incompatíveis.

| Literatura de **fatores** | Literatura de **estratégias** |
|---|---|
| (cite index="65-1">HML a 0,05% ao mês — valor praticamente não paga</cite> | (cite index="76-1">Carteira do fator valor com CAGR de 29,17% contra 9,68% do Ibovespa</cite> |
| (cite index="67-1">Sem prêmio de risco para lucratividade e investimento no segundo passo de Fama-MacBeth</cite> | (cite index="84-1">Greenblatt, que combina qualidade e valor, com alfa positivo e estatisticamente significativo</cite> |

Ambas não podem ser fatos simples sobre o mesmo mercado. **As reconciliações candidatas são quatro, e todas são testáveis no seu sistema:**

1. **A métrica não é a mesma.** HML usa book-to-market; a Magic Formula usa EBIT/EV. Empresa com muito ativo intangível ou muito ativo depreciado tem B/M que não representa preço. Se for isso, o earnings yield sobrevive e o B/M não — e a diferença é medível.
2. **A construção não é a mesma.** Fator é long-short ponderado sobre todo o universo; estratégia é carteira concentrada, igualmente ponderada, no topo do ranking. O prêmio pode estar concentrado no extremo e ser diluído na média.
3. **O tratamento de dados não é o mesmo.** Só um dos trabalhos localizados declara base point-in-time livre de sobrevivência, e é o não revisado por pares. Os demais não descrevem o tratamento no resumo.
4. **O período não é o mesmo.** 1994–1999, 2000–2020, 2005–2015, 2007–2017, 2012–2025. Cada um contém um regime macro distinto.

**Esta tensão é o conteúdo mais valioso do documento**, porque é uma pergunta que o seu backtest pode responder com os dados que a Fase 0 e a Fase 1 já entregam — e a resposta vale mais do que replicar qualquer uma das estratégias.

---

## 9. Auditoria das evidências — sete descontos obrigatórios

Aplicando ao material acima a mesma régua que os laudos aplicaram ao seu projeto.

**D-1 · O benchmark é quase sempre CAPM ou Ibovespa puro.** Os próprios autores flagram: (cite index="84-1">uma limitação importante dos estudos citados é a utilização do CAPM como modelo de referência risco-retorno; modelos multifatoriais têm o potencial de explicar melhor os retornos das metodologias de value investing</cite>. Bater o Ibovespa pode ser exposição a fatores conhecidos — e no Brasil o Ibovespa tem concentração setorial alta. **O teste correto é alfa contra os fatores do NEFIN**, e apenas o estudo com modelo multifatorial faz algo próximo.

**D-2 · Viés de sobrevivência não declarado.** Um único trabalho localizado declara base livre de sobrevivência, e é blog. Os demais não informam no resumo. Numa amostra de ~400 companhias com dezenas de deslistagens desde 2000, isso não é detalhe: é a diferença entre o resultado e o dobro dele.

**D-3 · Look-ahead contábil não descrito.** Nenhum resumo menciona o tratamento da data de disponibilidade dos fundamentos. Uma carteira montada em janeiro com o balanço de dezembro do mesmo ano usa dado que não existia. É o P1 do seu blueprint, e é o desconto mais provável de todos.

**D-4 · Custos e impostos ausentes.** Nenhum retorno citado é declarado líquido de corretagem, emolumentos, spread e ganho de capital a 15%. Magic Formula com 16 ativos e rebalanceamento trimestral implica dezenas de operações por ano. **A sua tabela de custos de agosto/2026 é exatamente o insumo que falta nesses estudos**, e você a tem.

**D-5 · Busca de parâmetros reportada como resultado.** (cite index="76-1">"diversas combinações de número de ativos e períodos de permanência"</cite> testadas, e a melhor reportada. (cite index="93-1">Concentração e periodicidade de rebalanceamento variadas até maximizar o Sortino</cite>. Graham com (cite index="84-1">limites de filtros ajustados ao contexto brasileiro</cite>. Nenhum reporta correção para testes múltiplos. Com uma dezena de configurações testadas, o t-crítico honesto sobe — é o argumento de Harvey, Liu e Zhu.

**D-6 · Dependência de período.** 2000–2020 começa perto de um piso e contém o superciclo de commodities. Cinco estudos, cinco janelas, resultados que variam por fator de três.

**D-7 · Decaimento pós-publicação.** Lopes e Galdi é de 2007; a adaptação brasileira do F-Score circula há quase vinte anos. A literatura americana documenta queda substancial de anomalias após a publicação. Nenhum dos trabalhos testa o período pós-divulgação separadamente.

**Efeito líquido:** nenhuma das estratégias está **validada** no sentido estrito. Todas estão **documentadas com resultado publicado**, o que é diferente e ainda assim é muito mais do que o Bastter oferece — que é o ponto que a Parte I do seu dossiê estabeleceu.

---

## 10. Especificação para o backtest

Cada estratégia vira uma entrada versionada em `politica.yaml`, com pré-registro datado antes de rodar.

```yaml
estrategias_pre_registradas:
  greenblatt_v1:
    universo: elegivel_apos_portoes_A_C
    ranking: [roic_ebit_sobre_capital_investido, ebit_sobre_ev]
    combinacao: soma_de_posicoes
    n_ativos: 16
    rebalanceamento: trimestral
    definicao_roic: EBIT/(capital_de_giro + ativo_imobilizado_liquido)  # fixar, é ambíguo
    hipotese: "supera o índice líquido de custo e imposto"
    rejeita_se: "alfa contra fatores NEFIN não distinguível de zero"
    variantes_permitidas: 3        # limite de busca, declarado ANTES

  piotroski_v1:
    universo: quartil_superior_book_to_market
    score: f_score_9_sinais
    corte: score >= 8
    rebalanceamento: anual
    hipotese: "separa recuperação de deterioração dentro do valor"
    rejeita_se: "não distingue os extremos com significância"

  hml_puro_v1:
    hipotese_nula_esperada: "NÃO supera"     # HML a 0,05% a.m.
    rejeita_se: "resultado positivo forte ⇒ investigar look-ahead ANTES de comemorar"

  dy_alto_v1:
    hipotese_nula_esperada: "NÃO supera"     # três evidências convergentes
    rejeita_se: idem

  momento_12_1_v1:
    obrigatorio: custo_fiscal_explicito       # 15% sobre ganho, a cada giro
    hipotese: "melhor evidência local, mas o líquido é a pergunta"

  indice_puro:
    papel: hipotese_nula_verdadeira
```

**Três regras de execução que valem mais que as estratégias:**

1. **`hml_puro_v1` e `dy_alto_v1` devem falhar.** Duas estratégias com resultado esperado negativo são o controle de integridade do pipeline. Se qualquer uma "funcionar", o defeito está no seu código, não no mercado. Rode-as **primeiro**.
2. **Toda estratégia é medida líquida de custo e imposto**, com a sua própria tabela de custos como insumo. É o único diferencial estrutural do seu backtest frente a toda a literatura acima.
3. **`variantes_permitidas` é declarado antes.** Sem teto de busca, o resultado reportado é o máximo de uma amostra de tentativas, e a §9 D-5 mostra que é assim que a literatura foi construída.

---

## 11. Pendências

| # | Item | Bloqueia |
|---|---|---|
| 19 | Séries e documentação de fatores do NEFIN | D-1 — o benchmark correto de toda a §9 |
| 21 | Texto integral dos artigos de fatores | A tensão da §8 |
| 25 | Metodologia e série do índice S&P/B3 Baixa Volatilidade Altos Dividendos, separando pré e pós-lançamento | §7 |
| 26 | Texto integral dos estudos de Magic Formula (UFRGS, EBFin) e Piotroski (Insper, Lopes e Galdi 2007): amostra, sobrevivência, defasagem contábil, custos | D-2, D-3, D-4 |
| 27 | Definição exata de ROIC e de capital investido em cada estudo | §2.1 — as implementações divergem |
| 28 | Verificar se algum estudo testa o período pós-publicação separadamente | D-7 |

**Nota final de escopo.** Nenhuma estratégia deste documento deve ser implementada antes de a decisão A-05 estar resolvida — núcleo indexado ou seleção ativa —, que segue aberta desde o laudo Rev. 03. O que muda com esta pesquisa é que a decisão ficou **mais fácil de tomar empiricamente**: as seis entradas do bloco de pré-registro acima, rodadas contra o índice puro e contra os fatores do NEFIN, respondem a pergunta com dados seus, e não com literatura de terceiros.

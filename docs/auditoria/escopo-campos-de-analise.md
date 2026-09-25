# Laudo de escopo — campos de análise de ativos

**Objeto:** especificação dos campos que o sistema deve calcular para avaliar ativos, separados por finalidade: posição de longo prazo (buy & hold) e posição especulativa.
**Emissão:** 02/09/2026.
**Natureza:** documento de escopo de engenharia. Define **o que o sistema mede**, com que fonte e com que validade empírica. **Não** define o que comprar, não emite recomendação e não estabelece limiares "corretos" — limiar é parâmetro do `politica.yaml`, e a decisão sobre ele é sua.

**Advertência metodológica que governa o documento inteiro.** As referências citadas na §2 estão marcadas com grau de confiança da minha memória. **Nenhuma foi aberta nesta sessão.** Pelo achado C-10 do manual — a Parte I do dossiê foi produzida pelo mesmo tipo de sistema que a auditou —, toda referência que virar parâmetro de política precisa ser verificada na fonte primária antes de ser usada como justificativa. As que sustentam decisão estão marcadas `VERIFICAR`.

---

## 1. O que "análise" significa como campo de sistema

O erro que este documento existe para evitar: tratar análise como opinião estruturada. Num sistema, análise é um conjunto de campos com quatro propriedades obrigatórias por campo:

| Propriedade | Por que é obrigatória |
|---|---|
| **Fórmula explícita** | "Boa margem" não é campo. `lucro_bruto / ativo_total` é |
| **Fonte e disponibilidade point-in-time** | Um campo que só existe hoje não pode entrar em backtest. `dt_disponivel` vale para indicador como vale para fato |
| **Modo de falha declarado** | Toda métrica quebra em algum lugar. Dívida líquida/EBITDA é indefinida para banco. ROE é alavancável. Se o modo de falha não está escrito, ele aparece como resultado plausível e errado |
| **Força da evidência** | Se a métrica prevê retorno fora da amostra, se apenas descreve o passado, ou se é convenção sem lastro |

Um campo sem as quatro não entra no catálogo. Vira lacuna registrada, com motivo — o mesmo vocabulário das suas pesquisas.

**Consequência de escopo:** o sistema calcula e exibe. Ele **não** produz nota única de qualidade até que o backtest com pré-registro justifique — que é o que o `politica.yaml` já declara em `permite_score: false`. Este documento especifica os insumos daquele score, não o score.

---

## 2. O que a evidência sustenta, e com que força

Esta seção é a que separa campo com lastro de campo por convenção. Ela é curta de propósito: a lista de métricas com evidência decente é muito menor que a lista de métricas em uso.

### 2.1 Os quatro achados que enquadram tudo o mais

**A maioria dos fatores publicados não sobrevive a teste honesto.** Harvey, Liu & Zhu (2016) catalogaram centenas de fatores publicados e argumentam que, corrigindo para testes múltiplos, o limiar de significância deveria ser em torno de t ≈ 3,0, não 2,0 — o que elimina boa parte da literatura. Hou, Xue & Zhang (2020) tentaram replicar um grande número de anomalias e a maioria não sobreviveu com tratamento adequado de ponderação e microcaps. `VERIFICAR — sustenta o desenho inteiro.`

**O que sobrevive à publicação decai.** McLean & Pontiff (2016) mediram o retorno de anomalias antes e depois da publicação acadêmica e encontraram queda substancial no período pós-publicação. Consequência direta: um fator descoberto em 2013 e testado no seu backtest a partir de 2010 está sendo medido majoritariamente no período em que ele já era conhecido. `VERIFICAR.`

**A distribuição de retornos de ações é extremamente assimétrica.** Bessembinder (2018): uma minoria pequena de empresas responde por toda a criação de riqueza líquida acima de letras do Tesouro; a mediana das ações tem retorno de longo prazo negativo. Isso já está na Parte I do seu dossiê e é o achado que torna a seleção concentrada estruturalmente difícil. `VERIFICAR.`

**Amostra brasileira é pequena.** Cerca de 400 companhias listadas, fundamentos estruturados desde 2010, subsetores com 3 a 6 empresas, presença relevante de controle estatal e concentração de liquidez em poucos papéis. Qualquer fator estimado aqui tem erro-padrão muito maior que a versão americana. **Este é o motivo pelo qual o catálogo abaixo prioriza portões de exclusão sobre escores de seleção.**

### 2.2 Métricas com evidência relativamente robusta

| Métrica | Achado | Confiança | Uso no sistema |
|---|---|---|---|
| **Lucratividade bruta / ativos** | Novy-Marx (2013): lucro bruto sobre ativos prevê retorno melhor que medidas de lucro mais "limpas", e é complementar a valor | Moderada-alta `VERIFICAR` | Campo B-02 |
| **Crescimento de ativos** | Cooper, Gulen & Schill (2008): crescimento alto do ativo total associado a retorno futuro **menor**. Um dos achados mais replicados | Moderada-alta `VERIFICAR` | Campo E-01 — e é o campo mais contraintuitivo do catálogo |
| **Accruals** | Sloan (1996): a parcela do lucro que vem de accruals, e não de caixa, reverte; preços não incorporam isso na formação | Alta `VERIFICAR` | Campo D-01 |
| **Qualidade composta** | Asness, Frazzini & Pedersen ("Quality minus junk"): lucratividade, crescimento, segurança e payout combinados | Moderada `VERIFICAR` | Estrutura do bloco B |
| **Valor, condicionado a qualidade** | Fama & French (1992, 1993) para o prêmio de valor; Novy-Marx (2013) para o argumento de que valor isolado captura muita empresa em deterioração | Moderada | Bloco F — sempre condicionado, nunca isolado |
| **Distress NÃO é compensado** | Dichev (1998) e Campbell, Hilscher & Szilagyi (2008): ações com alto risco de falência tiveram retorno **baixo**, não alto | Moderada-alta `VERIFICAR` | Justifica o bloco C ser **portão**, não fator |
| **Momento** | Jegadeesh & Titman (1993) e vasta literatura posterior | Alta, mas **não é métrica de buy & hold** | Bloco especulativo, §5 |

### 2.3 Métricas de uso corrente sem evidência independente

Estas continuam no catálogo — como **campo exibido**, não como critério —, porque você precisa vê-las e porque a ausência delas seria notada. O que muda é que ficam marcadas.

| Métrica | Situação |
|---|---|
| **Dividend yield como sinal de qualidade** | Sem evidência independente de que preveja retorno total superior depois de controlar por lucratividade e valor. E no Brasil o JCP distorce a comparação, porque tem retenção de 15% na fonte e tratamento contábil distinto |
| **P/L isolado** | Fraco. Captura tanto empresa barata quanto empresa em deterioração. Só tem uso condicionado a qualidade |
| **ROE** | Alavancável por construção: sobe com dívida sem que nada melhore. É por isso que o catálogo usa ROIC |
| **Payout alto como virtude** | Miller & Modigliani (1961) e a literatura de política de dividendos: sem fricções, a forma de devolver capital é irrelevante. Com fricções, o que importa é o retorno sobre o capital retido — que é o campo E-03 |
| **"Lucro consistente há N anos"** | Descreve o passado. A lucratividade tem reversão à média documentada. É filtro de exclusão razoável, não previsor |
| **Média histórica de múltiplo como âncora** | Assume estacionariedade que não se observa. Útil como contexto, não como sinal |

**Como isso entra no sistema:** cada campo carrega `evidencia: robusta | fraca | convencao | ausente`, e o `politica.yaml` só pode usar campos de evidência `robusta` como portão, salvo declaração explícita em contrário registrada no `DECISIONS.md`.

---

## 3. As duas finalidades exigem catálogos diferentes

A separação que você pediu não é de grau. É de **objeto de medição**.

| | Buy & hold | Posição especulativa |
|---|---|---|
| **A pergunta** | Este negócio continua gerando caixa em 10 anos? | Esta tese se confirma antes de o dinheiro acabar? |
| **O que se mede** | Durabilidade | Sobrevivência e velocidade |
| **Horizonte da evidência** | 10 anos de histórico | 4 a 8 trimestres de trajetória |
| **Perda máxima aceita** | Limitada por diversificação e portão de solvência | **Total, declarada de antemão** |
| **Critério de saída** | Deterioração da tese estrutural | **Prazo**, definido antes da entrada |
| **Peso na carteira** | Fração de crescimento, 1/N dentro do bloco | Teto duro de função APOSTA |
| **Falha mais comum** | Comprar deterioração barata | Confundir tração com crescimento financiado |
| **Função no `politica.yaml`** | `CRESCIMENTO` | `APOSTA` |

**A regra estrutural que decorre disso, e que deve ser código:** um ativo entra num dos dois catálogos, nunca nos dois. Se falha em qualquer portão de solvência do buy & hold e mesmo assim é comprado, ele é **automaticamente** classificado como APOSTA e passa a obedecer ao teto da função — sem exceção, sem reclassificação posterior. Isso fecha o modo de falha mais caro do varejo: a aposta que vira "longo prazo" depois que cai.

---

## 4. Catálogo — ativos de buy & hold

Sete blocos, na ordem de avaliação. Os blocos A e C são **portões binários**: reprova elimina. Os blocos B, D, E e F são **campos exibidos**, que só viram escore depois do backtest com pré-registro.

### Bloco A — Elegibilidade estrutural (portão)

O que determina se o ativo é sequer analisável, antes de qualquer juízo sobre o negócio.

| # | Campo | Fórmula / fonte | Modo de falha |
|---|---|---|---|
| A-01 | Liquidez média diária | Média de volume financeiro em 60 pregões, do COTAHIST | Média esconde concentração; use com A-02 |
| A-02 | Pregões com negócio | Contagem em 60 pregões | Sua pesquisa de ETFs já mostrou o valor deste campo — ECOO11 sem negócio em 4 de 20 |
| A-03 | Free float | Ações em circulação / total, do FRE | Divulgação anual; defasagem alta |
| A-04 | Segmento de listagem | Novo Mercado / N2 / N1 / tradicional, da B3 | É proxy de governança, não medida dela |
| A-05 | Tag along | % do FRE | Campo legal, não econômico |
| A-06 | Anos de fundamento disponível | Contagem em `fato_contabil` | Empresa recém-listada não tem histórico — e é um bom motivo para ir ao catálogo especulativo |
| A-07 | Opinião do auditor | Tipo de parecer; ressalvas | Não estruturado na CVM — provável `NÃO OBTIDO` |
| A-08 | Histórico de reapresentação | Contagem de `versao > 1` por período | **Campo original e barato.** Você já preserva versões (correção A-01 do laudo); reapresentação frequente é sinal de qualidade contábil, e ninguém publica isso |
| A-09 | Continuidade operacional | Menção de dúvida em notas | Texto livre; `NÃO OBTIDO` sem NLP |

### Bloco B — Rentabilidade e sua durabilidade

| # | Campo | Fórmula | Nota |
|---|---|---|---|
| B-01 | ROIC | NOPAT / capital investido | Preferido a ROE: não é inflável por alavancagem |
| B-02 | **Lucratividade bruta / ativos** | Lucro bruto / ativo total | Novy-Marx. É o campo de melhor razão evidência/simplicidade do catálogo |
| B-03 | Margem bruta, série de 10 anos | Lucro bruto / receita | A **tendência** importa mais que o nível |
| B-04 | Estabilidade do ROIC | Desvio-padrão e mínimo em 10 anos | Durabilidade é o objeto; um ROIC médio alto com dois anos negativos é outra coisa |
| B-05 | ROIC − custo de capital | B-01 menos WACC estimado | WACC é **estimativa**, não fato. Marque como derivado e exponha as premissas |
| B-06 | Decomposição DuPont | Margem × giro × alavancagem | Diagnóstico: mostra de onde vem o retorno |
| B-07 | Anos consecutivos com ROIC > 0 | Contagem | Filtro de exclusão, não previsor (§2.3) |

### Bloco C — Solvência (portão)

Bloco de exclusão, e a evidência é clara sobre por quê: risco de falência não foi historicamente compensado por retorno maior. Não é fator; é portão.

| # | Campo | Fórmula | Modo de falha |
|---|---|---|---|
| C-01 | Cobertura de juros | EBIT / despesa financeira líquida | **Preferido a dívida/EBITDA:** não depende de EBITDA como proxy de caixa |
| C-02 | Dívida líquida / EBITDA | Padrão | **Indefinido para bancos e seguradoras** — é o achado A-06 do laudo consolidado. Exige bloco de política separado para financeiras |
| C-03 | Perfil de vencimento | Dívida < 12 m / dívida total | Risco de rolagem é o que mata, não o nível |
| C-04 | Moeda da dívida × moeda da receita | Da nota de instrumentos financeiros | **Campo crítico no Brasil** e frequentemente ausente dos sistemas. Dívida em dólar com receita em real é risco cambial estrutural |
| C-05 | Caixa / dívida de curto prazo | Padrão | — |
| C-06 | Escore de insolvência | Altman Z ou Ohlson O | Ambos calibrados em amostra americana antiga. Use como **rastreio**, nunca como veredito |
| C-07 | Covenants e garantias | Notas | Texto livre; provável `NÃO OBTIDO` |

**Para instituições financeiras**, C-01 a C-03 são inaplicáveis. O bloco substituto — índice de Basileia, índice de imparidade, custo do crédito, índice de eficiência, ROE ajustado a risco — é escopo próprio e hoje **não está especificado em lugar nenhum do projeto**. Registre como lacuna.

### Bloco D — Qualidade do lucro

O bloco mais negligenciado e com a melhor evidência isolada do catálogo.

| # | Campo | Fórmula | Sinal |
|---|---|---|---|
| D-01 | **Accruals** | (Lucro líquido − FCO) / ativo médio | Sloan (1996). Accrual alto sugere lucro que ainda não virou caixa |
| D-02 | Conversão de caixa, 5 anos | Σ FCO / Σ lucro líquido | Persistentemente < 1 é sinal de que o lucro não se materializa |
| D-03 | Capex / depreciação | Padrão | < 1 por anos seguidos sugere subinvestimento que aparece depois |
| D-04 | Receita × contas a receber | Taxas de crescimento comparadas | Recebível crescendo acima da receita é o sinal clássico de venda empurrada |
| D-05 | Receita × estoque | Idem | Análogo |
| D-06 | Dias de capital de giro | DSO, DIO, DPO em série | Tendência importa mais que nível |
| D-07 | Rastreio de manipulação | Beneish M-score ou equivalente | **Rastreio, não acusação.** Falso positivo é comum. Marque como sinalizador |
| D-08 | Partes relacionadas / receita | Das notas | Difícil de estruturar; provável `PARCIAL` |
| D-09 | Mudanças de política contábil | Das notas | Idem |

### Bloco E — Alocação de capital

O que a administração faz com o dinheiro. Contém o campo mais contraintuitivo do catálogo.

| # | Campo | Fórmula | Nota |
|---|---|---|---|
| E-01 | **Crescimento do ativo total** | Variação anual | Cooper/Gulen/Schill: crescimento alto associado a retorno futuro **menor**. Sinal invertido em relação à intuição |
| E-02 | Diluição | Variação do número de ações | Retorno por ação é o que importa, não retorno da empresa |
| E-03 | ROIC incremental | Δ NOPAT / Δ capital investido | **O campo que decide se reter lucro cria valor.** Substitui o debate sobre payout |
| E-04 | Payout total | (Dividendos + JCP + recompra) / lucro | No Brasil, separe JCP: retenção de 15% na fonte |
| E-05 | Aquisições e baixas | Ágio reconhecido, impairment histórico | Histórico de write-off é histórico de alocação ruim |
| E-06 | Capex de manutenção × expansão | Estimado de D-03 e das notas | Estimativa; marque como derivado |

### Bloco F — Preço

Último bloco, e por construção. Um ativo que reprova em A ou C não chega aqui.

| # | Campo | Nota |
|---|---|---|
| F-01 | EV / EBIT | Preferido a P/L: neutro à estrutura de capital |
| F-02 | EV / FCF | Mais difícil de manipular que EBIT |
| F-03 | P/VP | Só faz sentido para financeiras e ativos de balanço |
| F-04 | Earnings yield × NTN-B real | O único prêmio observável com um comparador honesto |
| F-05 | Percentil histórico do próprio múltiplo | Contexto. **Não** sinal (§2.3) |
| F-06 | Dividend yield | Exibido, marcado `evidencia: convencao` |

### Bloco G — Risco específico do Brasil

Nenhum sistema estrangeiro tem estes, e eles explicam boa parte da variância local.

| # | Campo |
|---|---|
| G-01 | Controle estatal ou golden share |
| G-02 | Exposição regulatória e ciclo tarifário (energia, saneamento, telecom, saúde) |
| G-03 | Concentração de cliente ou fornecedor |
| G-04 | Exposição cambial líquida: receita × custo × dívida (integra C-04) |
| G-05 | Dupla listagem / ADR e a base de preço a usar |
| G-06 | Litígio tributário e provisões |

---

## 5. Catálogo — posição especulativa

A distinção que faz este catálogo existir: **você não está medindo se o negócio é bom. Está medindo se a tese tem tempo de se confirmar, e quanto da tese o preço já contém.**

### Bloco H — Pista de sobrevivência (portão)

Se este bloco reprova, não há tese: há corrida contra o caixa.

| # | Campo | Fórmula |
|---|---|---|
| H-01 | Queima mensal | FCO + capex, média de 4 trimestres |
| H-02 | **Meses de pista** | Caixa e equivalentes / H-01 |
| H-03 | Dependência de captação | Número de emissões nos últimos 36 meses |
| H-04 | Diluição acumulada | Variação do número de ações em 36 meses |
| H-05 | Vencimentos nos próximos 24 meses | Dívida a vencer / caixa |
| H-06 | Covenants em risco | Das notas |

**H-02 é o campo mais importante do catálogo inteiro.** Pista menor que o prazo da tese significa diluição certa antes da confirmação — e o seu retorno se dá por ação, não pela empresa.

### Bloco I — Qualidade do crescimento

Distingue tração de crescimento comprado. Todos os campos comparam **taxas**, não níveis.

| # | Campo | O que revela |
|---|---|---|
| I-01 | Crescimento orgânico × por aquisição | Receita comprada não é tração |
| I-02 | Crescimento de receita × de recebíveis | Recebível correndo à frente = venda empurrada. Mesmo campo D-04, com peso maior aqui |
| I-03 | Trajetória da margem bruta na expansão | **Sobe:** ganho de escala real. **Cai:** o crescimento está sendo comprado com desconto |
| I-04 | Marketing / receita nova | Proxy de CAC quando não há divulgação |
| I-05 | Receita recorrente / total | Se divulgado |
| I-06 | Retenção ou churn | Raramente divulgado; `NÃO OBTIDO` na maioria |
| I-07 | Concentração de receita | Um cliente grande transforma tese em aposta binária |

### Bloco J — Economia unitária

| # | Campo |
|---|---|
| J-01 | Margem de contribuição, se apurável |
| J-02 | Receita necessária para o ponto de equilíbrio, à estrutura de custo atual |
| J-03 | Trajetória do FCO: negativo estável, melhorando ou piorando |
| J-04 | Alavancagem operacional: Δ resultado / Δ receita |

### Bloco K — Estrutura da posição

Este bloco não é sobre a empresa. É sobre você, e nenhum dado público o preenche.

| # | Campo | Origem |
|---|---|---|
| K-01 | Perda máxima aceita | **Input do usuário.** Sempre 100% do valor alocado |
| K-02 | **Tese, escrita** | Input. Uma frase falsificável: "X vai acontecer até a data D" |
| K-03 | **Prazo da tese** | Input. Data. Não "longo prazo" |
| K-04 | **Condição de falsificação** | Input. O que, se acontecer, encerra a posição |
| K-05 | Liquidez de saída | Calculado: dias para sair sem mover o preço, de A-01 e A-02 |
| K-06 | Participação de insiders e vencimento de lock-up | Do FRE e de fatos relevantes |
| K-07 | Quanto da tese o preço já contém | Derivado; marque como estimativa e exponha as premissas |

**K-02 a K-04 são a razão de ser deste catálogo.** São os únicos campos que nenhum dado fornece e sem os quais a posição não é especulação — é esperança sem prazo. E são a aplicação direta do princípio de pré-registro que o `politica.yaml` já adotou para o backtest: escreva a condição antes de ver o resultado.

### Bloco L — Teste de classificação (obrigatório)

Roda os portões do buy & hold (A e C) contra o ativo especulativo e **registra quantos ele reprova**. Não impede a compra. Torna impossível a reclassificação retroativa.

```
ativo XYZ · classificado como APOSTA em 2026-09-02
reprova: A-06 (2 anos de fundamento), C-01 (EBIT negativo), C-05 (caixa < dívida CP)
tese: [K-02] · prazo: [K-03] · falsificação: [K-04]
teto de função APOSTA: 3% · perda máxima aceita: 100%
```

### Bloco M — O que NÃO se aplica, e por quê

Campo tão importante quanto os anteriores, porque a métrica aplicada fora do domínio produz número plausível e sem sentido.

| Métrica do buy & hold | Por que não se aplica |
|---|---|
| P/L, EV/EBIT | Não há lucro. O múltiplo fica negativo ou absurdo, e ambos são ilegíveis |
| Dividend yield | Empresa em crescimento que distribui está financiando dividendo com captação |
| ROIC, ROE | Base de capital muda rápido demais para a média significar algo |
| Estabilidade em 10 anos | A série não existe |
| Percentil histórico de múltiplo | Idem |
| Crescimento de ativos como sinal negativo | E-01 tem sinal **invertido** aqui: crescer o ativo é a tese. Aplicar o fator do buy & hold produziria a conclusão oposta à pretendida |

Esta última linha é o exemplo mais claro de por que os dois catálogos precisam ser separados no modelo de dados, e não apenas no relatório.

---

## 6. Consequências para o modelo de dados

O que este escopo exige do sistema, e o que ele já tem.

**Já existe ou está especificado:** `fato_contabil` com bitemporalidade, plano de contas setorial, séries de preço ajustadas, `entidade` com setor e subsetor.

**Falta, e é obrigatório:**

| Necessidade | Onde |
|---|---|
| `dt_disponivel` no **indicador**, não só no fato | Um indicador derivado de dois fatos com disponibilidades diferentes tem a **maior** das duas. Sem isso, o backtest tem look-ahead pela porta dos fundos |
| Tabela de **classificação de tese** | `ativo_id`, `catalogo` (BH ou APOSTA), `dt_classificacao`, K-02, K-03, K-04, e o resultado do bloco L. É a tabela que impede reclassificação retroativa |
| Metadados por campo | `evidencia`, `fonte`, `modo_de_falha`, `aplicavel_a` (BH / APOSTA / ambos), `status` |
| Bloco de política para **financeiras** | Achado A-06 do laudo, ainda aberto. C-01 a C-03 são inaplicáveis e o substituto não existe |
| Contagem de reapresentações (A-08) | Depende da correção A-01: Silver preserva todas as versões. Se aquela correção não for feita, este campo é impossível |

**Campos que hoje são `NÃO OBTIDO` e devem nascer assim:** A-07, A-09, C-07, D-08, D-09, I-05, I-06, G-06 — todos dependem de texto livre em notas explicativas. Registre com motivo, não com valor vazio. É a regra K-07 das suas pesquisas, aplicada aos indicadores.

---

## 7. O que este catálogo não resolve

Seção obrigatória, e é a que dá crédito ao resto.

**Nenhum conjunto destes campos foi demonstrado, fora da amostra e no mercado brasileiro, capaz de identificar vencedores futuros.** A evidência da §2 é majoritariamente americana, majoritariamente anterior à publicação, e sujeita ao decaimento de McLean & Pontiff. O que o catálogo faz melhor é **excluir**: fraude contábil, insolvência, diluição, iliquidez. A evidência para exclusão é mais forte que para seleção, e o desenho reflete isso — blocos A e C são portões, os demais são campos.

**A questão A-05 continua aberta e este documento não a resolve.** A Parte I do seu dossiê julgou contraditados os pilares de diversificação concentrada e de rejeição a ETFs. Um catálogo de análise de ativos individuais é útil se a resposta for seleção ativa; se for núcleo indexado, boa parte dele vira ferramenta de estudo, não de decisão — o que continua compatível com o seu objetivo declarado de aprendizado, mas muda o que precisa ser construído. **A decisão deve preceder a implementação dos blocos B, D, E e F.** Os blocos A, C e o catálogo especulativo inteiro valem em qualquer cenário.

**Nenhum limiar aparece neste documento.** "ROIC acima de X", "dívida abaixo de Y" — nada disso está aqui, de propósito. Limiar é escolha declarada, vai para o `politica.yaml`, e é exatamente o que o backtest com pré-registro deve atacar. Colocar limiar num documento de escopo o transformaria em recomendação.

**As referências não foram verificadas.** Ver a advertência de abertura.

---

## 8. Escopo por fase

Considerando o orçamento real (3–4 h efetivas por semana) e o escopo reduzido do laudo Rev. 03.

**Fase A — computável de CVM + COTAHIST, point-in-time, sem input do usuário.** A-01, A-02, A-06, A-08, B-01 a B-04, B-06, B-07, C-01 a C-03, C-05, D-01 a D-06, E-01 a E-04, F-01 a F-05. São **30 campos**, todos derivados de dado que a Fase 0 e a Fase 1 já entregam. É o corpo da enciclopédia consultável, e cobre a maior parte do valor.

**Fase B — exige o FRE ou dado adicional.** A-03, A-04, A-05, C-04, E-05, G-01 a G-06. Fonte nova, esforço próprio.

**Fase C — catálogo especulativo.** Blocos H, I, J, L e M. Note que quase todos derivam dos mesmos fatos da Fase A, com fórmulas diferentes — o custo marginal é baixo depois da Fase A. **Exceção: o bloco K é input, não cálculo, e pode ser construído hoje**, em qualquer estágio do sistema, porque é uma tabela e um formulário.

**Fase D — depende de texto não estruturado.** A-07, A-09, C-07, D-08, D-09, G-06. Deixe como `NÃO OBTIDO` registrado. É a última fronteira e a de pior razão esforço/retorno.

**Sugestão de sequência:** bloco K primeiro — antes de qualquer campo calculado. É a tabela de tese com prazo e condição de falsificação, custa um dia, não depende de dado nenhum, e é o único elemento do documento inteiro que muda comportamento sem depender de o sistema estar pronto.

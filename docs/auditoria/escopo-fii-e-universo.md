# Escopo de análise por classe de ativo — Parte 1: universo e FII

**Emissão:** 02/09/2026.
**Natureza:** documento de escopo de engenharia. Define o universo de ativos acessíveis, e especifica os campos de análise da primeira classe. **Não** é recomendação de investimento, não define limiares e não indica ativos.
**Fontes:** pesquisadas nesta sessão, com URL e data. Onde a evidência é editorial ou comercial, está marcado. Onde as fontes divergem, a divergência é registrada, não resolvida.

---

# Parte I — Universo de ativos acessíveis a pessoa física no Brasil

Inventário do que **existe e é acessível**, não do que deve ser comprado. Serve para que uma classe ausente do sistema seja ausência declarada, e não omissão — o achado §6.4 da auditoria da camada de alocação.

## 1. Renda fixa soberana — Tesouro Direto

| Ativo | Indexador | Nota |
|---|---|---|
| Tesouro Selic | Selic | Sem marcação relevante a mercado |
| Tesouro Reserva | Selic | Produto recente, aporte mínimo de R$ 1,00 |
| Tesouro Prefixado (LTN) | Nominal fixo | Marcação a mercado |
| Tesouro Prefixado com juros semestrais (NTN-F) | Nominal fixo | Cupom |
| Tesouro IPCA+ (NTN-B Principal) | IPCA + juro real | Marcação a mercado forte em prazos longos |
| Tesouro IPCA+ com juros semestrais (NTN-B) | IPCA + juro real | Cupom |
| Tesouro Renda+ | IPCA + juro real | Fase de conversão em renda mensal por 20 anos |
| Tesouro Educa+ | IPCA + juro real | Análogo, 5 anos |

## 2. Renda fixa bancária — cobertura do FGC

| Ativo | Tributação | Nota |
|---|---|---|
| CDB | Tabela regressiva | Emissor bancário |
| RDB | Tabela regressiva | Não negociável, sem resgate antecipado por padrão |
| Letra de Câmbio (LC) | Tabela regressiva | Emissor: financeira |
| LCI / LCA | **Isentas para PF** | Combinação FGC + isenção |
| LIG (Letra Imobiliária Garantida) | Isenta para PF | Carteira de cobertura própria, **sem FGC** |
| Poupança | Isenta | 0,5% a.m. + TR quando Selic > 8,5% |
| Conta remunerada / "cofrinho" | Depende do lastro | Verificar se é conta de pagamento (sem FGC) ou RDB (com) |

## 3. Renda fixa privada — sem FGC

Debêntures comuns · Debêntures incentivadas (Lei 12.431, isentas para PF) · CRI · CRA · Notas comerciais · Letra Financeira (aplicação mínima elevada) · FIDC (varejo destravado pela Resolução CVM 175).

## 4. Renda variável listada na B3

Ações ON, PN e UNIT · BDR patrocinado e não patrocinado · ETF de ações (BR e internacional, como IVVB11) · ETF de renda fixa · ETF de criptoativos · **FII** · Fiagro · FI-Infra e FIP-IE · FIP listado · Fundos de Fundos.

## 5. Derivativos e estruturados

Opções sobre ações e índice · Mercado a termo · Futuros (índice, dólar, DI, commodities) · COE · Aluguel de ativos (BTC).

## 6. Fundos não listados

FIF (renda fixa, ações, multimercado, cambial) sob o novo marco da Resolução CVM 175 · Fundos de previdência PGBL e VGBL · Fundos exclusivos.

## 7. Exterior

Conta em corretora estrangeira (ações, ETFs, bonds, REITs) · Plataformas brasileiras com conta internacional · BDR e ETF de índice estrangeiro como via doméstica.

## 8. Criptoativos

Compra direta em exchange com custódia própria ou da exchange · ETF de cripto na B3 · ETN.

## 9. Outros

Ouro (contrato OZ1D na B3, e ETF) · Moeda estrangeira em espécie ou conta · Crowdfunding de investimento (Resolução CVM 88) · Precatórios e ativos judiciais (mercado privado, sem regulação de valores mobiliários) · Imóvel direto.

**Fora do universo de investimento, apesar de vendido como tal:** consórcio (é sistema de compra) e capitalização (é sorteio com poupança forçada). Registre-os como exclusão declarada.

---

# Parte II — FII: especificação completa

## 10. Definição operante e base normativa

<cite index="16-1">O FII é regido pelo Anexo Normativo III da Resolução CVM 175, destinado à aplicação em empreendimentos imobiliários, com as classes de cotas constituídas em regime fechado</cite>. <cite index="20-1">A Resolução CVM 175 foi editada em 23/12/2022</cite> e <cite index="21-1">entrou em vigor em 02/10/2023, junto com a Resolução 184, que trouxe os anexos normativos</cite>. <cite index="22-1">A norma reconhece criptoativos como ativos financeiros e destravou a distribuição de FIDC ao varejo</cite> — mudanças que afetam o universo da Parte I.

A base legal anterior permanece: Lei 8.668/1993 (constituição) e Lei 9.779/1999 (regime tributário do patrimônio).

**Consequência de engenharia, e é a primeira:** o regime mudou em outubro de 2023. Um backtest de FII que atravesse essa data compara fundos sob regimes distintos de classes, subclasses e responsabilidade de cotista. Isso precisa ser uma variável de controle, não um detalhe.

## 11. O regime tributário como parâmetro do sistema

A isenção do rendimento distribuído é **condicional**, e as condições são campos calculáveis — não notas de rodapé.

<cite index="41-1">São condições cumulativas: cotas admitidas à negociação exclusivamente em bolsa ou mercado de balcão organizado; número mínimo de cotistas; e o cotista pessoa física não pode deter 10% ou mais das cotas nem ter direito a mais de 10% dos rendimentos distribuídos</cite>. <cite index="41-1">Se qualquer trava de concentração for ultrapassada, o cotista perde integralmente a isenção sobre os proventos daquele fundo</cite>.

**Divergência registrada — não resolvida aqui.** As fontes discordam sobre o número mínimo de cotistas. Várias, datadas de 2026, afirmam que <cite index="41-1">a Lei 14.754/2023 elevou o piso de 50 para 100 cotistas, e que um fundo que caia abaixo de 100 perde a isenção até recompor a base</cite>. Outras, mais antigas, registram <cite index="39-1">o mínimo de 50 cotistas estabelecido pela Lei 11.196/2005</cite>. Ambas são secundárias.
→ **PENDÊNCIA 12: ler Lei 11.033/2004 art. 3º, II, com as alterações da Lei 14.754/2023, no Planalto.** O parâmetro entra no `politica.yaml` como `NAO_CONFIRMADO` até lá, e bloqueia o portão de isenção.

**Confirmado e relevante:** <cite index="38-1">a isenção segue vigente em 2026, e permaneceu intacta após a queda da MP 1.303/2025, derrubada pela Câmara em outubro de 2025</cite> — o que corrobora a sua pesquisa. A MP propunha <cite index="43-1">retenção de 5% sobre rendimentos distribuídos a pessoas físicas por FII e Fiagro negociados em bolsa com no mínimo cem cotistas</cite>. <cite index="40-1">A Lei 15.570/2025 passou a tributar dividendos acima de R$ 50 mil mensais em 10% e instituiu imposto mínimo para rendas anuais acima de R$ 600 mil; FII e FI-Infra permanecem fora da base de cálculo do imposto mínimo</cite>.

**Segunda divergência, e é sua.** O seu `custos.yaml` registra "Lei 15.270/2025 (dividendos)". A fonte acima diz **15.570/25**. Um dos dois números está errado. → **PENDÊNCIA 13.**

**Campos derivados obrigatórios:**

| Campo | Fórmula | Efeito |
|---|---|---|
| T-01 `isencao_elegivel` | Booleano das três condições | Se falso, o rendimento é tributado e todo DY comparado a outra classe está errado |
| T-02 `n_cotistas` | Do informe mensal | Série. Fundo perdendo cotistas caminha para o desenquadramento |
| T-03 `margem_ate_desenquadramento` | `n_cotistas − piso` | **Campo original.** Ninguém publica distância até a perda da isenção |
| T-04 `ganho_capital_aliquota` | 20%, **sem** isenção mensal | O achado §B.1 da sua pesquisa de ETFs vale aqui: a isenção de R$ 20 mil é lista fechada e não alcança FII |
| T-05 `dy_liquido_equivalente` | DY isento convertido para bruto comparável | Um DY de 9% isento equivale a ~11,3% bruto na faixa de 20%. Sem este campo, comparar FII com CDB é comparar coisas diferentes |

## 12. A segmentação decide o catálogo

Um "FII" não é uma classe. São pelo menos cinco negócios distintos sob a mesma sigla, e **aplicar os campos de tijolo a um fundo de papel produz número plausível e sem sentido** — o mesmo erro do bloco M do escopo anterior.

| Segmento | Objeto | Campos que dominam | Campos inaplicáveis |
|---|---|---|---|
| **Tijolo — renda** (lajes, galpões, shoppings, agências, hospitais) | Imóvel alugado | Vacância, WAULT, cap rate, inadimplência, tipo de contrato | — |
| **Papel** (CRI) | Crédito imobiliário | Indexador, LTV, garantias, inadimplência, duration, MTM | Vacância, cap rate, WAULT |
| **FOF** | Cotas de outros FII | Taxa em duas camadas, P/VP look-through | Vacância, cap rate |
| **Desenvolvimento** | Obra para venda | VGV, cronograma, permuta, risco de execução | DY estável, vacância |
| **Híbrido** | Mistura | Todos, ponderados pela composição | — |

**Campo estrutural S-00 · `segmento`** — obrigatório, e determina quais campos são aplicáveis. Sem ele, o sistema calcula vacância para fundo de CRI.

**Alerta específico do P/VP em fundo de papel:** <cite index="51-1">em FII de papel o índice pode ser influenciado pela metodologia de marcação a mercado, prejudicando a comparação com outros fundos</cite>. O P/VP de tijolo compara preço com laudo de avaliação; o de papel compara preço com carteira marcada. Não são a mesma métrica e não devem entrar na mesma ordenação.

## 13. O que a evidência sustenta

Esta é a seção que separa campo com lastro de campo por convenção. É curta, e o resultado é desconfortável.

### 13.1 P/VP — a métrica mais usada, com evidência estrangeira e nenhuma brasileira

Nas fontes brasileiras consultadas, o P/VP aparece exclusivamente em material **comercial e editorial** — corretoras, casas de análise, portais. Nenhuma valida a métrica empiricamente. <cite index="47-1">O tratamento típico é descritivo: P/VP acima de 1 indica ágio, abaixo de 1 indica desconto</cite>, com a ressalva genérica de que <cite index="53-1">um P/VP muito baixo pode indicar problemas estruturais, como perda de locatários, vacância elevada ou gestão ineficiente</cite>.

A evidência real vem da literatura de REIT, sobre o análogo P/NAV, e ela é substantiva:

- **Reversão à média confirmada.** <cite index="23-1">Ações de REIT com P/NAV alto apresentam retornos subsequentes baixos, e as de P/NAV baixo, retornos altos — resultado que os autores associam a mispricing, e que é análogo ao encontrado em fundos fechados</cite>.
- **E a decomposição, que é o achado mais útil.** <cite index="29-1">Mais da metade da variação transversal do prêmio sobre NAV é explicada por características observáveis: tamanho, tipo de propriedade, localização, alavancagem e lucratividade. Decompondo o prêmio em componente explicado por características e componente residual de sentimento, o componente de sentimento é fortemente e negativamente relacionado a retornos futuros, enquanto o componente de características é um previsor positivo muito fraco</cite>.

**Consequência direta de engenharia, e é a mais valiosa deste documento:** *P/VP bruto é o sinal errado.* O campo que vale calcular é o **resíduo** — o P/VP que sobra depois de controlar por segmento, tamanho, alavancagem e rentabilidade. Isso é uma regressão transversal simples, roda em segundos, e é a diferença entre replicar o que todo portal já mostra e produzir algo que a evidência sustenta. Fica como campo P-03.

### 13.2 Dividend yield — a evidência brasileira é contrária ao uso corrente

Este é o achado mais contraintuitivo para o mercado local, e ele é brasileiro.

<cite index="32-1">Um estudo empírico sobre o DY de FIIs constatou que os fundos com maior mediana de dividend yield no período, em sua maioria, **não** estavam entre os que apresentaram maior rentabilidade aos cotistas; que os DY altos tendem a persistir ao longo do tempo; e que esses fundos apresentaram retornos negativos calculados sobre a variabilidade do valor das cotas no mercado secundário</cite>. O mesmo estudo observa <cite index="32-1">que os fundos com maior volume de negociação têm, em sua maioria, DY acima da mediana, em decorrência do efeito clientela</cite>.

Ou seja: **DY alto persiste, atrai fluxo, e não se converte em retorno total superior.** É o mesmo padrão que a literatura de ações mostra para dividend yield isolado, e o mesmo mecanismo que a sua pesquisa de ETFs identificou no segmento de covered call — cupom alto convivendo com retorno total menor.

**Mas o nível não é a única forma de usar DY.** <cite index="31-1">Um estudo publicado na Revista Contabilidade & Finanças usou a **variação** do dividend yield como critério de seleção de FIIs brasileiros em estratégias de momento, medindo o desempenho por índice de Sharpe, alfa do modelo de três fatores de Fama-French e retorno excedente ao índice do setor; as estratégias apresentaram resultados acima dos índices setoriais</cite>.

**Consequência:** o sistema deve calcular `dy_nivel` (marcado `evidencia: contraria`) e `dy_variacao` (marcado `evidencia: moderada, momento`) como campos **distintos**, e o segundo pertence ao catálogo de posição tática, não ao de buy & hold.

### 13.3 Investimento e lucratividade — o que funciona em ações também funciona em REIT

<cite index="27-1">Investimento e lucratividade têm poder preditivo substancial sobre retornos de REIT, não subsumido por modelos convencionais; um modelo de fatores baseado em investimento supera modelos convencionais na captura de padrões transversais. Book-to-market tem poder preditivo muito mais fraco sobre retornos de REIT depois de 1990</cite>. A literatura citada inclui <cite index="29-1">Ling, Ooi & Xu (2019) sobre crescimento de ativos e desempenho em REITs</cite> e <cite index="27-1">Vincent (1999) sobre o conteúdo informacional do FFO</cite>.

**Duas consequências:**
1. O campo de crescimento de patrimônio — emissões seguidas, aquisições agressivas — tem **sinal negativo esperado**, como no bloco E do escopo geral. É o campo mais contraintuitivo do catálogo e o que o mercado de FII trata como virtude.
2. B/M fraco em REIT pós-1990 reforça a §13.1: P/VP bruto não basta.

### 13.4 O prêmio sobre a NTN-B — o comparador correto

<cite index="35-1">O prêmio de risco de FII é normalmente medido pela diferença entre o dividend yield dos fundos e o cupom da NTN-B longa; quando a curva de juros real abre, o prêmio comprime e os FIIs tendem a cair — e a lógica inversa vale no fechamento</cite>. Material de gestora atribui à pesquisa da Citi <cite index="37-1">correlação positiva de 0,79 entre a mediana do DY e a taxa da NTN-B, com prêmio médio de longo prazo em torno de 3,2 p.p. e tendência de reversão à média</cite>. `PARCIAL — fonte de casa de análise citada em blog; o dado original da Citi não foi obtido.`

**Consequência:** `dy_menos_ntnb` é campo obrigatório, e é o único comparador honesto de nível de preço da classe. DY isolado, sem a taxa real de referência da data, não significa nada. E ele deve ser **point-in-time**: a NTN-B da data da observação, não a de hoje.

### 13.5 Síntese da força da evidência

| Métrica | Evidência | Origem | Uso |
|---|---|---|---|
| Resíduo do P/VP após controles | Moderada | REIT, EUA | **Campo de seleção** |
| P/VP bruto | Fraca | REIT, EUA | Contexto |
| Crescimento de patrimônio (sinal negativo) | Moderada | REIT, EUA | Campo, sinal invertido |
| Lucratividade | Moderada | REIT, EUA | Campo |
| Variação do DY | Moderada | **Brasil, revisada por pares** | Catálogo tático |
| DY nível | **Contrária** | **Brasil** | Exibido, marcado |
| Prêmio sobre NTN-B | Moderada | Prática de mercado, `PARCIAL` | Comparador obrigatório |
| Vacância, WAULT, cap rate | Sem validação preditiva encontrada | Prática | Campos descritivos e de portão |

**Nenhuma métrica de FII foi validada preditivamente no Brasil, fora da amostra, com pré-registro.** Isso não as torna inúteis: torna-as **descritivas e de exclusão**, que é o uso defensável, exatamente como no escopo geral.

---

## 14. Catálogo — FII de buy & hold

### Bloco A · Elegibilidade e portões (binário)

| # | Campo | Fonte | Nota |
|---|---|---|---|
| A-01 | Liquidez média diária (60 pregões) | COTAHIST | — |
| A-02 | Pregões com negócio em 60 | COTAHIST | Mesmo campo que salvou a sua análise de ETF |
| A-03 | Patrimônio líquido | Informe mensal | Fundo pequeno concentra risco de gestão |
| A-04 | Número de cotistas | Informe mensal | Alimenta T-02 |
| A-05 | **Isenção elegível** | Derivado de T-01 | **Portão.** Reprova ⇒ DY não é comparável |
| A-06 | Anos desde a constituição | CVM | < 3 anos ⇒ vai ao catálogo de aposta |
| A-07 | Segmento | Classificação | Determina quais blocos se aplicam |
| A-08 | Fundo com prazo determinado? | Regulamento | <cite index="16-1">Classes de FII podem ter prazo de duração</cite>. Um fundo com prazo **não é buy & hold** — é operação com data |

### Bloco B · Geração de caixa (tijolo)

| # | Campo | Fórmula |
|---|---|---|
| B-01 | Resultado caixa por cota | Informe trimestral |
| B-02 | **Distribuído ÷ resultado caixa** | Acima de 1 sustentado = distribuição financiada por reserva, venda ou capital |
| B-03 | Reserva de lucro caixa acumulada | Informe. Mede por quantos meses B-02 > 1 é sustentável |
| B-04 | Resultado recorrente vs. não recorrente | Ganho de venda de imóvel não se repete |
| B-05 | Cap rate implícito | NOI / valor de mercado do fundo |
| B-06 | NOI por m² | Série. A tendência importa mais que o nível |

**B-02 corrige o critério do blueprint original.** A auditoria de 01/09 (achado A-19) apontou que comparar distribuído com **resultado contábil** é erro de grandeza: <cite index="48-1">a obrigação legal é distribuir no mínimo 95% do lucro apurado em regime de caixa</cite>. A comparação correta é contra o resultado caixa do informe, e a reserva acumulada é o contexto que decide se um mês acima de 1 é problema ou não.

### Bloco C · Ativos e contratos (tijolo)

| # | Campo | Por que importa |
|---|---|---|
| C-01 | Vacância física (% de área) | — |
| C-02 | **Vacância financeira** (% de receita) | Diverge da física quando o que vaga é o contrato caro. É a que importa |
| C-03 | WAULT — prazo médio remanescente ponderado | Mede quando o risco de renovação chega |
| C-04 | % vencendo em 12 e 24 meses | O perfil, não a média |
| C-05 | Típico vs. atípico (built to suit) | Contrato atípico tem multa cheia — proteção real |
| C-06 | Concentração por inquilino | Um inquilino grande transforma o fundo em aposta de crédito |
| C-07 | Concentração por imóvel e por região | — |
| C-08 | Inadimplência | — |
| C-09 | Reajuste: índice e data-base | IPCA vs. IGP-M muda a trajetória real |
| C-10 | Idade e estado dos ativos; capex de retrofit previsto | Capex futuro reduz distribuição futura |

**C-02 e C-05 são os campos que os portais não publicam de forma estruturada** e que exigem leitura do relatório gerencial. São, provavelmente, `PARCIAL` no primeiro ciclo.

### Bloco D · Carteira de crédito (papel)

| # | Campo |
|---|---|
| D-01 | Composição por indexador (IPCA, CDI, prefixado) |
| D-02 | Spread médio sobre o indexador |
| D-03 | LTV médio e distribuição |
| D-04 | Tipo de garantia: alienação fiduciária, cessão fiduciária, aval |
| D-05 | Inadimplência e CRI em recuperação |
| D-06 | Concentração por devedor e por operação |
| D-07 | Duration da carteira |
| D-08 | Metodologia de marcação: curva ou mercado |
| D-09 | % de CRI *high yield* vs. *high grade* |

**D-08 é o campo que torna o P/VP de papel comparável ou não.** Fundo marcado na curva não reflete stress; fundo marcado a mercado reflete. Sem o campo, a ordenação por P/VP mistura os dois.

### Bloco E · Estrutura, gestão e alocação de capital

| # | Campo | Nota |
|---|---|---|
| E-01 | Taxa de administração e de gestão | Sobre PL ou sobre valor de mercado — muda o incentivo |
| E-02 | Taxa de performance: existe, sobre qual referência | Referência mal escolhida gera taxa sem desempenho |
| E-03 | Custo total (taxas ÷ PL) | Comparável entre fundos |
| E-04 | **Crescimento do PL em 36 meses** | Sinal **negativo** esperado (§13.3) |
| E-05 | Emissões: número, preço vs. VP, diluição | Emitir abaixo do VP dilui quem fica |
| E-06 | Alavancagem (papel e obrigações a pagar) | <cite index="49-1">Fundos sem alavancagem são tratados como atributo de qualidade no mercado</cite>, sem validação empírica local |
| E-07 | Histórico do gestor: outros fundos, desempenho | — |
| E-08 | Conflito: gestor comprando de parte relacionada | — |

### Bloco F · Preço

| # | Campo | Evidência |
|---|---|---|
| F-01 | P/VP bruto | Fraca — contexto |
| F-02 | **Resíduo do P/VP** após controlar segmento, PL, alavancagem, rentabilidade | **Moderada — é o campo de seleção** (§13.1) |
| F-03 | DY 12 meses | Contrária — exibido, marcado |
| F-04 | **DY − NTN-B longa, point-in-time** | Comparador obrigatório (§13.4) |
| F-05 | Percentil do próprio P/VP no histórico | Contexto |
| F-06 | Cap rate implícito vs. cap rate de mercado do segmento | — |

**Contexto de nível, para calibrar:** <cite index="49-1">o IFIX encerrou 2024 com P/VP de 0,78, contra 0,86 no primeiro semestre de 2025</cite>. `PARCIAL — fonte editorial.`

---

## 15. Catálogo — FII de posição especulativa

Aplica-se a fundo de desenvolvimento, fundo em recuperação de vacância, fundo novo sem histórico, fundo de papel *high yield* e fundo com prazo determinado. A pergunta muda: não é se o fundo é bom, é **se a tese se confirma antes de o desconto virar realidade**.

### Bloco G · Sobrevivência da tese

| # | Campo |
|---|---|
| G-01 | Caixa e aplicações ÷ obrigações de 12 meses |
| G-02 | Compromissos de capex e aquisições já assumidos |
| G-03 | Dependência de nova emissão para cumpri-los |
| G-04 | Diluição em 36 meses: cotas emitidas ÷ cotas iniciais |
| G-05 | Preço médio das emissões vs. VP na data |
| G-06 | Vencimento de dívida e obrigações do fundo |

### Bloco H · Qualidade do desconto

O campo central: **por que este fundo está barato?**

| # | Campo | O que separa |
|---|---|---|
| H-01 | Decomposição do P/VP (§13.1) | Desconto explicado por característica ≠ desconto de sentimento. <cite index="29-1">Só o componente de sentimento previu retorno futuro, e negativamente ao prêmio</cite> |
| H-02 | Trajetória da vacância: piorando, estabilizada, melhorando | Desconto de fundo que ainda piora não é oportunidade |
| H-03 | Data do último laudo de avaliação | VP defasado torna o P/VP ficção |
| H-04 | Ativo problemático identificado e isolável? | Desconto localizado ≠ desconto estrutural |
| H-05 | Distribuição atual é sustentável sem reserva? | Se depende de reserva, o DY que atraiu vai cair |

### Bloco I · Estrutura da posição — input do usuário

| # | Campo |
|---|---|
| I-01 | Perda máxima aceita — sempre 100% |
| I-02 | **Tese escrita, falsificável** — "vacância cai abaixo de X% até a data D" |
| I-03 | **Prazo.** Data, não "longo prazo" |
| I-04 | **Condição de falsificação** — o que encerra a posição |
| I-05 | Liquidez de saída em dias, derivada de A-01 e A-02 |
| I-06 | Se o fundo tem prazo determinado (A-08), a data dele é um teto ao prazo da tese |

### Bloco J · Teste de classificação (obrigatório)

Roda os portões do bloco A contra o fundo e registra o que reprova, com data. Impede reclassificação retroativa — a aposta que vira "longo prazo" depois de cair.

### Bloco K · O que não se aplica

DY estável em fundo de desenvolvimento (não há renda). Vacância em fundo de papel. Cap rate em FOF. Média histórica de qualquer coisa em fundo com menos de 3 anos. WAULT em papel.

---

## 16. Fontes de dado e disponibilidade

| Bloco | Fonte | Estruturado? | Status |
|---|---|---|---|
| A-01, A-02 | COTAHIST | Sim | `COMPLETO` |
| A-03, A-04, B-01 a B-03 | Informe mensal e trimestral, CVM/Fnet | Parcial — colunas voláteis | `PARCIAL` — a sua auditoria já registrou ~60 colunas instáveis |
| C-01 a C-10 | Relatório gerencial (PDF) | **Não** | `NÃO OBTIDO` sem extração |
| D-01 a D-09 | Relatório gerencial e anexos | **Não** | `NÃO OBTIDO` |
| E-01 a E-03 | Regulamento e informe | Parcial | `PARCIAL` |
| E-04, E-05 | Informe + histórico de emissões | Sim | `COMPLETO` após ingestão |
| F-01, F-02, F-05 | Informe (VP) + COTAHIST (preço) | Sim | `COMPLETO` |
| F-04 | ANBIMA ETTJ / Tesouro | Sim | `COMPLETO` |
| T-01 a T-05 | Informe + norma | Sim, exceto o piso de cotistas | **`NÃO_CONFIRMADO`** — pendência 12 |

**Conclusão de escopo:** os blocos A, B, E e F são construíveis com CVM + COTAHIST + ANBIMA — tudo que a Fase 0 e a Fase 1 já entregam. **Os blocos C e D exigem extração de PDF de relatório gerencial, que é um projeto próprio.** Registre como fase separada e não a subestime: é a mesma classe de esforço do parser do COTAHIST.

---

## 17. Estratégias validáveis — o que o backtest deve testar

Cada uma com hipótese, sinal esperado e critério de rejeição escrito **antes** de rodar, conforme o pré-registro que o `politica.yaml` já adota.

| # | Estratégia | Hipótese | Base | Rejeita se |
|---|---|---|---|---|
| E1 | **Resíduo do P/VP** | Fundos com desconto não explicado por características superam o IFIX | <cite index="29-1">componente de sentimento do prêmio sobre NAV negativamente relacionado a retornos futuros</cite> | Não superar em X% das janelas por bootstrap em blocos |
| E2 | **DY nível (hipótese nula esperada)** | Fundos de DY alto **não** superam em retorno total | <cite index="32-1">os de maior mediana de DY não estavam entre os de maior rentabilidade</cite> | **Espera-se que falhe.** É o teste que valida o pipeline: se E2 "funcionar", há erro de look-ahead |
| E3 | **Variação do DY** | Variação do DY seleciona momento | <cite index="31-1">estratégias de momento com esse critério ficaram acima dos índices setoriais</cite> | Não bater IFIX líquido de custo |
| E4 | **Crescimento do PL, sinal negativo** | Fundos que mais emitiram têm retorno futuro menor | <cite index="27-1">investimento prevê retorno de REIT</cite> | Sinal positivo ou nulo |
| E5 | **1/N do IFIX** | Benchmark de referência | DeMiguel et al., já no seu YAML | — |
| E6 | **IFIX puro, custo real** | **Hipótese nula verdadeira** | — | Se nenhuma estratégia bate E6, a resposta é o índice |

**E2 é a estratégia mais valiosa da tabela, e ela deve falhar.** Uma estratégia com resultado esperado negativo é o melhor teste de integridade do backtest que existe: se ela produzir resultado positivo, o problema é o seu pipeline, não o mercado.

**E6 é a hipótese nula.** É a mesma pergunta A-05 do laudo Rev. 03, aplicada a FII. Se o índice vencer, você economizou o catálogo inteiro como ferramenta de decisão — e ele continua valendo como ferramenta de estudo, que é o seu objetivo declarado.

---

## 18. Pendências e limitações

**Limitações desta peça:**
1. Nenhuma norma foi lida no original. Resolução CVM 175 e Anexo III, Lei 11.033, Lei 14.754 e Lei 15.570 vieram de citação secundária ou de trecho indexado.
2. Os papers de REIT foram lidos por resumo, não por texto integral. Metodologia, amostra e período não foram verificados.
3. Não há literatura brasileira revisada por pares sobre P/VP de FII nas buscas realizadas. Isso é ausência de evidência, não evidência de ausência — mas o campo entra marcado.
4. Nenhum limiar aparece neste documento, de propósito.

**Pendências abertas:**

| # | Item | Bloqueia |
|---|---|---|
| 12 | Piso de cotistas para a isenção: 50 ou 100? Ler Lei 11.033 art. 3º com alterações da Lei 14.754 no Planalto | T-01, A-05 — **portão inteiro** |
| 13 | Lei de dividendos: 15.270 (seu YAML) ou 15.570 (fonte de hoje)? | Consistência do `custos.yaml` |
| 14 | Resolução CVM 175, Anexo III, texto integral | A-08 (prazo), regras de emissão, alavancagem |
| 15 | Dicionário do informe mensal e trimestral de FII (CVM/Fnet) | Blocos A, B, E — a fase construível |
| 16 | Papers de REIT em texto integral: NAV premium sentiment; investimento e lucratividade | Sinal e magnitude de F-02 e E-04 |
| 17 | Papers brasileiros em texto integral: DY variação (RCF) e DY empírico (UNIFESP) | E2 e E3 |
| 18 | Dado original da Citi sobre prêmio DY − NTN-B | F-04 |

---

## 19. Próximas classes

Ordem sugerida, por razão valor/esforço e por reuso do que já existe:

1. **Ação individual** — o catálogo geral já está escrito; falta só o bloco de financeiras, que é lacuna aberta desde o achado A-06.
2. **ETF de índice** — poucos campos, e é a hipótese nula de todas as demais.
3. **Renda fixa bancária (CDB/RDB/LCI/LCA)** — a pesquisa já está feita; falta o campo de risco de emissor por conglomerado, que o `politica.yaml` declara e o código não lê.
4. **Tesouro Direto** — trivial em campos, não trivial em marcação a mercado.
5. **Crédito privado (CRI, CRA, debêntures)** — reusa o bloco D deste documento.
6. **Exterior** — depende da pendência do expense ratio, ainda aberta desde a lista de download.
7. **Cripto** — menor prioridade: 3% de teto e o pior esforço/impacto do plano.

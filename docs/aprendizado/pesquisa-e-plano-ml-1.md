# Aprendizado de máquina no sistema — pesquisa e plano

*Escrito em 19/09/2026, no chat do projeto dedicado a aprendizado de máquina, com o PC dele
desligado. Nada aqui foi executado: é pesquisa com fonte, desenho e ordem de trabalho. O
pré-registro que sai deste documento está em `preregistro-ml-v1.md`, ao lado.*

> **Status deste documento:** `ESPECIFICACAO`. Nenhuma chave de YAML, nenhum módulo e
> nenhum teste nasceu dele ainda. Se o `PLANO.md` discordar sobre ordem, **o `PLANO.md`
> ganha** — este arquivo propõe a inserção do aprendizado de máquina na fila, não a
> reordena.

---

## 1. Objetivo e fronteira

**Objetivo:** ordenar, a cada mês, as ações elegíveis pela chance de superar as demais, para
decidir o destino do aporte e das trocas; e sinalizar risco contábil antes que ele vire preço.

**Fronteira (§1 do `CLAUDE.md`):** o aprendizado de máquina **não define pesos**. O sistema
"não é um otimizador" — DeMiguel, Garlappi e Uppal (2009). O modelo responde *qual primeiro*,
nunca *quanto*. A única estimativa que vira percentual é a fração de renda variável, e ela é
**um** número (o prêmio da estratégia), descontado pela incerteza — ver §7.

---

## 2. O achado que organiza a pesquisa: M5 contra M6

As competições Makridakis são o maior teste público de métodos de previsão.

| competição | domínio | resultado para aprendizado de máquina |
|---|---|---|
| M4 (2018) | 100 mil séries, vários domínios | métodos puros foram mal; venceu um híbrido rede neural + estatística; o topo foi de combinações |
| M5 (2020) | vendas do Walmart, 42.840 séries | primeira vitória clara: LightGBM em 1º |
| **M6 (2022–2023)** | **100 ativos financeiros, avaliação ao vivo** | 23,3% das equipes previram melhor que o benchmark; 28,8% montaram carteira melhor; **6,7% as duas coisas**; menos de 25% bateram a probabilidade uniforme por quintil |

> **A regra que sai daqui:** a mesma ferramenta que vence em varejo quase não passa do acaso
> em ações. Quem decide é a relação sinal-ruído do domínio, não a técnica. Portanto:
>
> 1. o que se importa de fora é principalmente **disciplina e arquitetura**;
> 2. as camadas cujo valor **não depende de bater o mercado** vêm primeiro (§6).

---

## 3. O que cada campo ensina, e como volta para o projeto

### 3.1 Dados tabulares pequenos (biomedicina) → modelo desafiante

O TabPFN (Hollmann et al., *Nature* 637, 2025) é um modelo de fundação para tabelas,
pré-treinado em milhões de conjuntos sintéticos, que supera os métodos anteriores em
conjuntos de até 10 mil amostras. A versão 2.5 foi desenhada para até 50 mil linhas.

**No projeto:** desafiante do LightGBM, dentro do mesmo pré-registro (é variante e consome
`m`). **Limite declarado:** o pré-treino supõe dados sem ordem temporal; não há evidência
pública em retornos de ações, cuja relação sinal-ruído é muito menor que a dos conjuntos de
teste dele.

### 3.2 Busca na web → o objetivo certo

O objetivo `lambdarank` do LightGBM vem dos sistemas de ranking de buscadores: otimiza a
**ordem** do topo, não o valor de cada previsão. É a pergunta do aporte.

### 3.3 Meteorologia → previsão como distribuição

O GenCast (DeepMind, *Nature* 2024) supera o ENS europeu em 97,2% de 1.320 alvos, com treino
até 2018 e teste em 2019, e o artigo discute explicitamente se algum dado de entrada
carregaria informação do futuro. A métrica é o CRPS, regra de pontuação própria para
distribuições.

**No projeto:** saída em **probabilidade por quintil** (como no M6), pontuada por RPS contra
a probabilidade uniforme; e **conjunto de modelos** avaliado como sistema.

### 3.4 Diagnóstico médico → o direito de dizer "não sei"

Predição conformal (Angelopoulos e Bates) dá conjuntos de previsão com cobertura garantida
sem supor distribuição. A variante seletiva só responde quando atinge a precisão exigida.

**No projeto:** é o `NAO_CONFIRMADO` com matemática. Previsão incerta demais → o modelo se
abstém, e a ação é ordenada pela regra do déficit. **Limite (P5):** em série temporal, a
dependência viola a trocabilidade da garantia; usa-se a versão adaptativa e a cobertura é
**medida** na sombra, nunca presumida.

### 3.5 Regulação de dispositivos médicos → pré-registro da manutenção

A FDA publicou em 12/2024 a guia final do PCCP (*Predetermined Change Control Plan*): o
fabricante declara de antemão quais modificações virão do aprendizado contínuo, como serão
validadas, e a avaliação de impacto; as mudanças previstas dispensam nova autorização.

**No projeto:** o retreino não pode virar escolha depois do resultado. O plano de mudanças
predeterminado separa o que muda sozinho do que exige novo pré-registro
(`preregistro-ml-v1.md`, §9). É a P4 estendida do teste para a manutenção.

### 3.6 Ensaios clínicos e testes A/B → espiar tem custo

Olhar o resultado todo mês e parar quando dá significância infla falso positivo. A medicina
usa desenhos sequenciais com gasto de alfa (O'Brien-Fleming); a indústria de testes A/B
chegou aos valores-p "sempre válidos".

**No projeto:** 55 meses de sombra são 55 espiadas. As análises confirmatórias são
**anuais**, com fronteira sequencial pré-registrada; o mensal é só monitoramento (§3.7).

### 3.7 Controle estatístico de processo → a regra de desligamento

O CUSUM (Page, 1954), padrão em linha de produção, detecta desvio da média com o menor
atraso para uma taxa de falso alarme escolhida.

**No projeto:** CUSUM sobre o IC mensal da sombra. Limites calibrados por simulação para um
tempo médio até falso alarme declarado.

### 3.8 Manutenção preditiva → "a empresa boa virou ruim" é vida útil remanescente

Vida útil remanescente (engenharia) e análise de sobrevivência (medicina) são o mesmo
problema, e os dois tratam **censura**: ignorar quem ainda não falhou superestima o risco.
Florestas de sobrevivência já foram aplicadas a falência de empresas.

**No projeto:** o motivo 2 de venda vira um **modelo de risco de deterioração**, com as
empresas que nunca pioraram entrando como censuradas — o mesmo cuidado do viés de
sobrevivência, pelo outro lado.

### 3.9 Detecção de fraude → módulo defensivo, com alerta embutido

Bao et al. (*Journal of Accounting Research*, 2020): conjunto de modelos (RUSBoost) sobre
**dados contábeis brutos**, guiado por teoria contábil, supera a regressão logística clássica
por larga margem. Um estudo com 33.544 observações chinesas confirma que métodos próprios para
classes desbalanceadas vencem. **Walker (2021) replicou Bao e questionou a suposição que
sustentava o resultado.**

**No projeto:** rótulos já disponíveis (reapresentação de balanço, recuperação judicial,
cancelamento de registro), dados brutos da CVM, validação **sem a mesma empresa em treino e
teste**. A replicação é a régua §5-B em campo alheio.

### 3.10 Sistemas em produção → o F-02 com outro nome

Breck et al. (Google, SysML 2019) descrevem uma pane real: uma chamada passou a devolver −1
como código de erro; −1 era valor válido para a variável; o dado virou treino e o modelo
aprendeu a prever −1. A resposta foi validação por esquema **e por distribuição**, antes do
modelo.

**No projeto:** o esquema já existe (`docs/schemas/`). Falta a camada que aprende a
distribuição esperada de cada campo. C-03 (quebra de 1994: desvio no mercado inteiro num dia)
e A-01 (outra empresa com HTTP 200: desvio de escala numa emissora) são exatamente o que ela
pega. **É a aplicação de maior valor imediato, e não precisa bater mercado nenhum.**

### 3.11 Modelos de linguagem → extração, não previsão

Kim, Muhn e Nikolaev (Chicago Booth, 2024): o GPT-4, com demonstrações anonimizadas, previu a
direção dos lucros melhor que analistas. **A página do arXiv registra que uma versão
posterior foi retirada pelo autor** — resultado não consolidado.

**No projeto:** o uso sólido é **extrair** o que o X-01 diz não existir nos CSVs (VSO,
distratos, dívida SFH), lendo notas explicativas **com o trecho citado** — o
`trecho_conferido` da P1. Tira o Osvaldo do caminho crítico (P7).

> **Regra não opcional:** um modelo de linguagem treinado até uma data "sabe" o que aconteceu
> antes dela. Usá-lo em backtest anterior ao fim do treino é informação do futuro. **Modelo de
> linguagem entra só para frente** — sombra e extração datada.

### 3.12 Peso zero — visível, não excluído (P6)

| técnica | por que peso zero | o que reabre |
|---|---|---|
| aprendizado por reforço | ~200 decisões mensais em 16 anos; o ambiente não se reinicia | ambiente simulado validado, ou decisão sequencial que otimização não resolve |
| redes em grafo (cadeia de fornecedores) | relações entre empresas brasileiras não estão em dado estruturado medido | uma fonte de relações com procedência |
| modelos de fundação de séries temporais para retorno | retorno é quase ruído; o M6 dá o teto | evidência publicada em finanças |

---

## 4. Os dois conflitos com a doutrina, e como ficaram

**P3 (portões, não pontuação).** O aprendizado de máquina **nunca elimina**; atua numa etapa
nova, **ordenação**, depois dos portões. Cada ordenação sai decomposta por variável
(`pred_contrib=True` do LightGBM, sem dependência nova). *Decisão delegada, 19/09.*

**G7 (sem tese, sem peso).** O modelo passa a contar como **tese sistemática** registrada em
`teses.yaml`, com `impressao()` e validadores próprios — opção B. Motivo: ele declarou que não
quer estar no caminho crítico nem afirmar percentuais (P7, U-01). É redesenho do sentido de
"tese", registrado como tal. *Decisão delegada, 19/09, reversível.*

---

## 5. Pré-requisitos de dados (camada 0)

| insumo | fonte | limitação a declarar (P5) |
|---|---|---|
| preço ajustado | COTAHIST + `ajustar.py` | antes de 04/07/1994 há quebra de moeda (C-03): usar 2010+ |
| fundamentos por data de disponibilidade | DFP (2010+) / ITR (2011+), `DT_RECEB` | **valores reapresentados**: a data está certa, o valor pode ser o corrigido depois; viés otimista até o acervo semanal cobrir o período |
| universo mensal | COTAHIST (liquidez) | nunca composição do Ibovespa: a B3 só publica a do dia (V-01) |
| troca de código | A-03/A-04/P-93 | uma empresa não pode virar duas nem sumir |
| fatores | NEFIN + `fatores.py` | — |

**Duas regras de desenho:** toda variável carrega a data em que ficou disponível e a montagem
**recusa** (`InsumoBloqueado`) data posterior à decisão; e **ausente fica ausente** — preencher
com zero é o F-02 na forma mais tentadora (endividamento zero parece empresa saudável).

---

## 6. Arquitetura por camadas — ordenadas por valor que independe de alfa

| camada | o que é | vale sem alfa? |
|---|---|---|
| **C0 · guarda de dados** | anomalia por distribuição no pipeline (§3.10) | **sim** — protege tudo |
| **C1 · motor de avaliação** | walk-forward com purga, IC com n, multiplicidade, fronteira sequencial, CUSUM, conformal | sim — impede autoengano |
| **C2 · defensivo** | sobrevivência + fraude com dados brutos (§3.8, §3.9) | **sim** — evitar uma Americanas não depende de achar uma Magalu |
| **C3 · extração por modelo de linguagem** | dossiê X-01 com trecho citado | sim — tira o humano do caminho crítico |
| **C4 · ranking** | multifator → LightGBM `lambdarank` → TabPFN → conjunto; probabilidade por quintil; abstenção | só se passar no pré-registro |
| **C5 · governança** | plano de mudanças, registro de modelos com `impressao()`, sombra | sim |

```
camada 0 ─► C0 guarda ─► montagem PIT ─► portões G0–G8 ─► ORDENAÇÃO ─► motor de aporte
                                               │               ▲
                                               ├─► C4 ranking ─┘
                                               └─► C2 defensivo ─► alerta (portão só se validado)
```

---

## 7. Decisões tomadas neste chat (19/09/2026)

Todas precisam entrar no projeto pelo protocolo §9 — ver §9 abaixo.

| id | decisão | fundamento |
|---|---|---|
| D-ML1 | aprendizado de máquina é **ordenação**, fora de portões e de pesos | delegada |
| D-ML2 | modelo como **tese sistemática** (opção B do G7) | delegada |
| D-ML3 | o sistema **recomenda vendas**, por dois motivos separados no relatório: **1** — existe alternativa melhor, líquida de custo e IR (ordenação, com bandas); **2** — a empresa piorou (portões reaplicados à carteira; nunca preço) | **dele** |
| D-ML4 | defensivo começa como **alerta**; vira portão só se H-ML6 rejeitar | delegada |
| D-ML5 | horizonte do alvo: **1 mês** | delegada |
| D-ML6 | o motivo 1 **pode quebrar carrego**, com margem maior que a de uma troca comum | **dele** |
| D-ML7 | **preço médio só é lido pelo cálculo de IR**, nunca por sinal; o gatilho "subiu X% sobre o meu custo" é recusado | delegada |
| D-ML8 | **motivo 3 — concentração:** acima de 1,5× o peso-alvo deixa de receber aporte; acima de 2× (ou 15% absoluto) vende até o teto, fatiando no limite de isenção | delegada |
| D-ML9 | fração de renda variável = meia-Kelly sobre o prêmio **da estratégia** medido fora da amostra, descontado em direção ao prêmio do índice — **nunca o do índice sozinho** | delegada |
| D-RES | G2: exclusividade da reserva até **metade do alvo**; depois **80% reserva / 20% investimento** | delegada |
| — | o usuário segue o sistema integralmente e **não afirma percentuais** | **dele** |

> **Retratação registrada no chat, 19/09:** eu calculei ~15% de renda variável por Kelly com o
> prêmio **do índice** (0,96% a.a., t = 0,74) para decidir sobre uma carteira **selecionada**.
> Medi uma coisa e concluí sobre outra — régua §5-B, pergunta 1, e a crítica ao Bessembinder
> (§6, item 4) na direção oposta. Corrigido por D-ML9.

---

## 8. Fases

| fase | entrega | depende de | classe | desktop? |
|---|---|---|---|---|
| **ML-0** | `preregistro-ml-v1.md` commitado | nada | `DECISAO_DE_DESENHO` | commit, sim |
| **ML-1** | C1 provada **só com dado sintético** | ML-0 | `BLOQUEIA_O_SISTEMA` | não |
| **ML-2** | C0 sobre o acervo real; aceite: detecta C-03 e um A-01 injetado sem ter sido programada para eles | camada 0 | `BLOQUEIA_O_SISTEMA` | **sim** |
| **ML-3** | base de variáveis PIT 2010–2026 | ML-2, CVM | `BLOQUEIA_O_SISTEMA` | **sim** |
| **ML-4** | C2 avaliado | ML-3 + acervo semanal CVM | — | não |
| **ML-5** | C4 avaliado **uma vez** no teste | ML-3 | — | não |
| **ML-6** | sombra no Actions | ML-4 ou ML-5 | — | configuração inicial |
| **ML-7** | C3, só para frente | ML-6 | — | não |

**A inversão em relação ao pré-projeto anterior:** a guarda de dados passa à frente de
qualquer modelo de retorno. Pelo histórico (C-03, A-01, P-99, F-02), o risco maior não é o
modelo fraco — é o dado errado em silêncio. Modelo bom sobre dado errado aprende o erro: o −1
do Google.

---

## 9. Ao voltar ao desktop

Nada abaixo foi aplicado. Regra §5-B.12: **arquivo que duas mãos editam não se entrega
inteiro** — por isso nenhum `politica.yaml`, `PENDENCIAS.md` ou `CLAUDE.md` vai junto.

1. `git add docs/aprendizado/` e commit **antes de qualquer variável da ML-3 existir** — o
   pré-registro só vale com data anterior ao dado (P4, `PREREGISTRO-EVIDENCIA.md`).
2. Registrar a impressão do `preregistro-ml-v1.md` (sha256, 16 primeiros caracteres) no
   `preregistro.py` quando a família `aprendizado` for criada.
3. Pendências novas para o `PENDENCIAS.md`, cada uma com dono, gatilho e classe:

| pendência | dono | gatilho | classe |
|---|---|---|---|
| modelar IR de renda variável (isenção R$ 20 mil/mês sobre vendas, degrau não progressivo, compensação, FII 20% sem isenção) — hoje em `limitacoes_declaradas`; **nenhuma venda sai do motor antes disto** | Claude | antes do primeiro sinal de venda | `BLOQUEIA_O_SISTEMA` |
| G2: `exclusividade` absoluta → limiar (metade do alvo) + divisão 80/20, no YAML (D-RES) | Claude | próxima sessão local | `DECISAO_DE_DESENHO` (tomada) |
| registrar D-ML1…D-ML9 em `perfil.yaml → decisoes` com fundamento de decisão delegada e o critério dele (crescimento composto do patrimônio) | Claude | próxima sessão local | `DECISAO_DE_DESENHO` (tomada) |
| novo tipo de tese: `SISTEMATICA` em `teses.yaml`, com validadores (D-ML2) | Claude | antes da ML-5 | `BLOQUEIA_O_SISTEMA` |
| P-15: medir compatibilidade de `lightgbm` e `tabpfn` com `numpy==2.4.4` / `pandas==3.0.2` / Python 3.11 **antes** de pinar | Claude | antes da ML-1 usar dado real | `BLOQUEIA_O_SISTEMA` |
| guarda de teste: nenhuma variável derivada de custo de aquisição entra em ranking ou portão (D-ML7) | Claude | junto da ML-1 | `BLOQUEIA_O_SISTEMA` |

---

## Fontes (acesso em 19/09/2026)

- M4/M5: Makridakis et al.; síntese em arxiv.org/pdf/2401.13912 e arxiv.org/pdf/2504.00059.
- M6: arxiv.org/pdf/2310.13357; percentuais em arxiv.org/pdf/2410.08009; "menos de 25%" em
  ideas.repec.org/a/eee/intfor/v41y2025i4p1395-1403.html.
- TabPFN: nature.com/articles/s41586-024-08328-6; TabPFN-2.5: arxiv.org/abs/2511.08667.
- GenCast: arxiv.org/pdf/2312.15796; deepmind.google (blog de 04/12/2024).
- Conformal: Angelopoulos e Bates, arxiv.org/pdf/2107.07511.
- FDA PCCP: guia final de 03–04/12/2024 (resumos Foley, Jones Day, Akin).
- Sobrevivência / vida útil: arxiv.org/abs/2405.01614; Ishwaran et al. (2008), *Annals of
  Applied Statistics*.
- Fraude: Bao et al. (2020), *JAR* 58(1):199–235; Walker (2021), *Econ Journal Watch*;
  Rahman e Zhu (2023), *Accounting & Finance*.
- Validação de dados: Breck et al., SysML 2019, research.google/pubs/pub47967.
- Modelos de linguagem: Kim, Muhn e Nikolaev, arxiv.org/abs/2407.17866 (nota de retirada na
  página do arXiv).
- Status `NAO_CONFIRMADO` neste documento: nenhuma das fontes foi lida em texto integral nesta
  sessão; as afirmações vêm de resumos e das páginas indicadas. Antes de qualquer número daqui
  entrar em `custos.yaml` ou `politica.yaml`, vale `trecho_conferido`.

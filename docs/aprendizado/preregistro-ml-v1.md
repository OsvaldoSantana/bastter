# Pré-registro — família `aprendizado`, versão 1

*Escrito em 19/09/2026, antes de qualquer variável da base PIT existir. É a fase ML-0 de
`pesquisa-e-plano-ml-1.md`. Corrigido em 21/09/2026, **antes do primeiro commit** (§13).*

*Vale a partir do commit **empurrado ao `origin`** que o contém: o hash desse commit e a data
pública dele são a prova (`auditoria/PREREGISTRO-EVIDENCIA.md`). Commit só local não vale — é
a lição da P-116, em que um critério escrito antes entrou no mesmo commit que os resultados e
ficou impossível de distinguir deles.*

> **O que este documento faz:** fixa hipóteses, dados, variáveis, modelos, espaço de busca,
> métricas, critérios de veredito e a regra de manutenção **antes** de ver o resultado.
> **O que ele não faz:** escolher depois. Toda mudança nele depois do commit gera `v2`, com
> nova impressão, e tudo que foi medido sob a `v1` continua reportado sob a `v1`.

---

## 1. Família e orçamento de multiplicidade

A família `aprendizado` é **separada** das estratégias de 05/09 (m = 13), porque testa outra
pergunta: ordenação relativa dentro do universo, e não prêmio de fator. **Por conservadorismo,
todo veredito é reportado duas vezes:** no `m` da família e no `m` somado às 13 anteriores. Se
os dois divergirem, vale a decisão 4 de 13/09: **divergência bloqueia**, e o operativo é o
mais conservador.

| id | hipótese nula (H0) | variantes |
|---|---|---|
| H-ML1 | multifator ingênuo: IC médio ≤ 0 | 1 |
| H-ML2 | LightGBM: IC ≤ IC do multifator | 4 (grade da §5) |
| H-ML3 | TabPFN: IC ≤ IC do multifator | 1 |
| H-ML4 | conjunto: IC ≤ IC do multifator | 1 |
| H-ML5 | carteira operacional (topo, líquida de custo e IR simulado) rende ≤ regra do déficit | 1 |
| H-ML6 | ações sinalizadas pelo defensivo rendem ≥ universo nos 12 meses seguintes | 1 |
| H-ML7 | a variável de reversão 36–60 meses não acrescenta IC ao LightGBM | 1 |
| H-ML8 | regra de concentração com teto compõe ≥ regra sem teto | 1 |
| | **m da família** | **11** |

A grade da H-ML2 é escolhida **dentro** das dobras de desenvolvimento (§4) e só a configuração
vencedora vai ao teste. Ela conta 4 no orçamento mesmo assim: a regra é conservadora de
propósito.

---

## 2. Dados

- **Período:** jan/2010 a **dez/2025** (fundamentos DFP desde 2010; COTAHIST inteiro em R$,
  fora da quebra de 1994 — C-03). **2026 fica fora:** o `COTAHIST_A2026.ZIP` do acervo chegou
  truncado (P-100) e a série do NEFIN termina em 07/2026. Estender o período exige `v2`,
  escrita antes de o arquivo de 2026 ser lido — o fim do teste não pode ser escolhido depois
  de ver quantos meses "ajudam".
- **Data de decisão:** último pregão de cada mês `t`.
- **Universo em `t`:**
  - mercado à vista, lote padrão, no COTAHIST;
  - negociada em ≥ 90% dos pregões dos 3 meses anteriores;
  - volume financeiro médio dos 3 meses no percentil ≥ 50 entre as que passaram no filtro
    anterior — percentil, não valor em reais, para não depender da inflação;
  - **uma classe por empresa** (a mais líquida em `t`): ON e PN da mesma empresa não podem
    contar como dois acertos;
  - identidade da empresa pelo `codeCVM`, não pelo ticker (A-03).
- **Disponibilidade:** variável contábil só entra se `DT_RECEB` ≤ data de decisão. A montagem
  **recusa** (`InsumoBloqueado`) qualquer violação — é o canário de vazamento (§8).
- **Deslistagem:** retorno medido até o último pregão negociado, como no estudo da Economatica
  de 16/09/2026. A ação não some do mês em que saiu.

### Limitações declaradas desta seção (P5)

| limitação | direção do viés | quando deixa de importar |
|---|---|---|
| valores contábeis reapresentados antes de 09/2026 | **otimista** — o modelo vê balanços já corrigidos | à medida que o acervo semanal da CVM cobrir o período |
| execução no fechamento do dia da decisão | otimista (custo de impacto ignorado) | universo filtrado por liquidez reduz; medido na sombra |
| universo pequeno (~100 empresas/mês) | variância alta das métricas | não se resolve; se mede e se publica o n |
| **série ajustada com eventos de quantidade faltando antes de 2024** (A-11: o COTAHIST marca bonificação que o silver não tem; CMIG3/4 −27% num dia) | **indeterminada** — um degrau não removido entra como retorno falso no alvo e no momento | quando a P-112 medir a lacuna em 2010–2025; **a ML-5 não roda antes disso** (é a C0 da ML-2 aplicada ao alvo) |
| séries `INCOMPLETO` por provento sem preço de véspera (P-113) | indeterminada | quando a P-113 for implementada e o número de séries incompletas publicado |

---

## 3. Alvo

Retorno total do mês `t+1` (ajustado por proventos via `ajustar.py`), menos a mediana do
universo em `t+1`, convertido em posição relativa. Para a saída probabilística, o quintil desse
retorno. Horizonte de um mês: D-ML5.

---

## 4. Particionamento

- **Desenvolvimento:** jan/2010 a dez/2019. Escolha de hiperparâmetros por walk-forward interno
  com janela expansiva, retreino anual.
- **Teste:** jan/2020 a **dez/2025 — 72 meses**. Os modelos são retreinados anualmente com
  dados até o ano anterior e **hiperparâmetros congelados em dez/2019**. **O teste é executado
  uma vez.**
- **Purga:** 1 mês (o horizonte do alvo). **Embargo:** 1 mês entre o fim do treino e o início
  da previsão.
- **Defensivo (H-ML6):** dobras agrupadas por empresa — nenhuma empresa aparece em treino e
  teste da mesma dobra (a lição da replicação de Bao et al.).

---

## 5. Variáveis e modelos

### 5.1 Variáveis

Todas convertidas em posição relativa dentro do mês; **ausente fica ausente**; bancos entram
com as variáveis inaplicáveis ausentes e um indicador de regime (P6).

| grupo | variáveis |
|---|---|
| valuation | lucro/preço, patrimônio/preço, EBITDA/valor da firma, dividend yield 12m, caixa operacional/preço |
| qualidade | ROE, margem bruta, desvio da margem em 12 trimestres, (lucro − caixa operacional)/ativo, dívida líquida/EBITDA, crescimento da receita em 3 anos |
| momento | retorno 12 meses excluindo o último; retorno do último mês |
| reversão (só H-ML7) | retorno de 36 a 60 meses atrás |
| risco | volatilidade 12m, log do volume financeiro, log do valor de mercado |
| defensivo (só C2) | resultado financeiro / lucro, crescimento de fornecedores − crescimento da receita, reapresentações nos últimos 36 meses |

**Proibido, com guarda de teste:** qualquer variável derivada do custo de aquisição de um
usuário (D-ML7).

### 5.2 Modelos

| modelo | configuração |
|---|---|
| multifator (H-ML1) | média simples das posições de valuation, qualidade e momento |
| LightGBM (H-ML2) | `objective=lambdarank`; `num_leaves ∈ {7, 15}` × `min_data_in_leaf ∈ {50, 200}`; `learning_rate=0.03`; `feature_fraction=0.7`; número de árvores por parada antecipada nas dobras internas; `deterministic=True`, `num_threads=1`, semente fixa |
| TabPFN (H-ML3) | configuração padrão da versão pinada, **sem ajuste** |
| conjunto (H-ML4) | média das posições dos três acima |
| defensivo (H-ML6) | sobrevivência (floresta de sobrevivência) para deterioração; conjunto para classes raras para reapresentação/fraude |

---

## 6. Métricas

**Primária:** IC mensal (correlação de postos entre previsão e alvo), média no teste, com o
**n de meses** e o **n médio de empresas por mês** ao lado (§5-B.14).

**Inferência:** bootstrap em blocos, com **corte operativo = o MAIOR entre os cortes de
`L ∈ {1, 2, 3}`**, cada um pelo mesmo procedimento de `multiplicidade.py`. Margens menores que
o ruído de semente são `NAO_CONFIRMADO`, com a mesma régua do m = 8.

> **Por que não um L só.** A faixa informativa da P-88 (L = 2 a 8) foi definida por ≥ 39
> blocos distintos por replicação, com n = 306. Com n = 72, L = 2 dá 36 blocos e L = 3 dá 24:
> os dois ficam abaixo do limiar que definiu a faixa. Medido em 21/09 sobre 80 meses do NEFIN,
> o controle sem dependência (SMB) perde **−9,1% do corte em L = 2 e −11,3% em L = 3** — a
> degeneração do reamostrador abaixa o corte, e isso é anticonservador. O máximo entre
> L ∈ {1, 2, 3} cobre as duas direções sem olhar o dado de teste: se houver dependência serial,
> um L maior sobe o corte; se não houver, o L = 1 é o maior. É a lógica da decisão 4 — entre
> leituras que podem divergir, vale a mais conservadora. O custo é poder, declarado no 9º
> teste da §8. Detalhe: `auditoria/AUDITORIA-PREREGISTRO-ML-V1.md` §2.

**Secundárias:**
- RPS da probabilidade por quintil contra a probabilidade uniforme (a métrica do M6);
- diferença entre o topo e a mediana; giro mensal;
- retorno líquido: custos lidos por `val()`. Se algum insumo estiver `NAO_CONFIRMADO`, o
  líquido **não é calculado** e o relatório diz isso (F-02);
- alfa contra os quatro fatores do NEFIN via `alfa_contra_fatores()`.

**Robustez (todas pré-registradas, nenhuma escolhida depois):** sem o quintil menos líquido;
sem bancos; subperíodos 2020–2022 e 2023–2025. **Robustez que inverte o sinal rebaixa o
veredito para `NAO_CONFIRMADO`.**

---

## 7. Critério de decisão operacional

O modo `ordenacao.modo: deficit_e_score` só liga se **todas** valerem:

0. **H-ML1 rejeitada, no `m` conservador.** Sem isso, as condições seguintes medem vitória
   sobre uma linha de base que pode não ter sinal nenhum — vencer um multifator de IC ≤ 0 é
   trivial. **Não acrescenta hipótese:** a H-ML1 já está no orçamento. O custo é poder: o
   modo só liga se o multifator **e** o modelo tiverem sinal detectável;
1. H-ML2, H-ML3 **ou** H-ML4 rejeitada, no `m` conservador;
2. H-ML5 rejeitada (o ganho sobrevive a custo e IR simulado);
3. nenhum teste de robustez inverte o sinal.

Qualquer outro desfecho: o modo fica `deficit`, o modelo fica com **peso zero, visível**, e a
sombra continua medindo (P6). O defensivo vira portão só se H-ML6 for rejeitada (D-ML4).

---

## 8. Testes exigidos antes de qualquer dado real (ML-1)

| teste | passa se |
|---|---|
| sinal plantado | o pipeline recupera um sinal sintético conhecido |
| ruído puro | em ≥ 200 sementes, a taxa de rejeição fica dentro do intervalo do α nominal |
| canário de vazamento | variável igual ao alvo futuro é **recusada**; removida a guarda, o canário passa (mutação) |
| rótulos embaralhados | o IC colapsa para o intervalo do ruído |
| determinismo | duas execuções, mesmo hash de modelo e de saída |
| ausente não vira zero | variável ausente chega ausente ao modelo |
| cobertura conformal | em dado sintético com dependência serial, a cobertura adaptativa fica dentro da tolerância declarada |
| preço médio | nenhuma variável derivada de custo de aquisição chega ao ranking |
| **poder com sinal plantado** | o módulo calcula e publica o **efeito mínimo detectável**: o IC médio, em desvios do IC mensal, que o pipeline rejeita com 80% de probabilidade, com n = 72, m = 24 e a regra de corte da §6, em dado sintético com e sem dependência serial |

**O nono teste não tem limiar de aprovação — tem obrigação de publicação.** O efeito mínimo
detectável vai para o relatório final **ao lado do veredito**. A ordem de grandeza esperada,
só pela aritmética (`c / √72`): com corte 3,1, o IC médio precisa chegar a **0,37 do desvio
mensal**; com 4,1, a **0,48**. Se o poder medido for baixo, um "não rejeita" será lido como
*"o teste não tinha como ver"*, e não como *"o modelo não funciona"* — as duas conclusões têm a
mesma saída e são opostas, e só o número de poder as separa.

---

## 9. Plano de mudanças predeterminado

Inspirado no PCCP da FDA (12/2024).

**Pode mudar sem novo pré-registro** — desde que passe na validação abaixo:
- retreino anual com a mesma configuração;
- novos meses de dado;
- universo recalculado pela regra da §2.

**Validação de toda mudança automática:** os **nove** testes da §8 verdes; IC fora da amostra
do modelo novo, no último ano, não inferior ao do anterior além do ruído de semente; instantâneo
dourado da saída comparado campo a campo.

**Exige `v2` deste documento:** variável nova ou removida; grade de hiperparâmetros; família de
modelo; alvo ou horizonte; **período de teste**; qualquer limiar da §6, da §7 ou da §10.

---

## 10. Modo sombra (a partir da ML-6)

- **Mensal:** o job grava `sombra/AAAA-MM.csv` (ordenação, probabilidade por quintil,
  abstenção, contribuições por variável, vendas sugeridas com motivo 1/2/3) e faz o commit. O
  histórico público é o verificador externo.
- **Confirmatório, anual:** até 5 análises (uma por ano até 2031), com fronteira sequencial do
  tipo O'Brien-Fleming, α total de 5% bilateral. Valores de referência para 5 análises:
  z ≈ 4,56 · 3,23 · 2,63 · 2,28 · 2,04 — **`NAO_CONFIRMADO`: o módulo recalcula, e vale o
  número calculado.**
- **Desligamento:** CUSUM sobre o IC mensal. Limites calibrados por simulação na ML-1 para um
  tempo médio até falso alarme de **120 meses** sob a hipótese de sinal constante. Disparou →
  peso zero e relatório com a data.
- **Abstenção:** cobertura-alvo de 80% (conformal adaptativo); cobertura realizada publicada
  todo ano, com n.
- **Motivos de venda:** medidos separadamente — motivo 1, retorno do comprado contra o vendido,
  líquido; motivo 2, retorno do sinalizado contra o universo; motivo 3, efeito no crescimento
  composto.

---

## 11. Dependências (P-15)

`lightgbm` e `tabpfn`: versões **`NAO_CONFIRMADO`** até a compatibilidade com
`numpy==2.4.4`, `pandas==3.0.2` e Python 3.11 ser medida (`pip install --dry-run` na máquina
dele; a consulta ao PyPI daqui foi recusada por `robots.txt` e não foi contornada). Se o
TabPFN não couber na faixa fechada, H-ML3 fica com peso zero e a variante **continua contada no
`m`** — orçamento não encolhe por conveniência.

**As duas entram num grupo opcional** (`[project.optional-dependencies] aprendizado`), com
**impressão de ambiente própria** para a família. A impressão do motor (`7565df1381e2c1ed`)
**não muda**: se mudasse, todo resultado pré-registrado de 05/09 deixaria de ser conferência e
passaria a ser número novo (`CLAUDE.md` §3). O TabPFN pode trazer `torch` — `NAO_CONFIRMADO` —,
e é mais uma razão para isolar.

---

## 12. O que este pré-registro NÃO protege (P5)

- **Um erro de sinal como o E-06.** Nenhum contador de variantes pega; o que segura são os
  testes da §8 e a leitura da vizinhança.
- **A qualidade da camada 0.** Pré-registro sobre dado errado mede o erro com rigor. Por isso a
  ML-2 (guarda de dados) vem antes da ML-5 — e a lacuna de eventos de quantidade (A-11, P-112)
  é o primeiro caso concreto dela.
- **Mudança de regime depois de 2025.** É o que a sombra e o CUSUM existem para detectar, não
  para evitar. A retenção de 10% sobre dividendos acima de R$ 50 mil/mês (Lei 15.270/2025,
  a partir de 2026) é uma mudança de regime conhecida no dado de preço do dia ex.

---

## 13. Correções antes do commit (21/09/2026)

Feitas por decisão dele (P-107), a partir de `auditoria/AUDITORIA-PREREGISTRO-ML-V1.md`.
Nenhuma é `v2`: o documento ainda não tinha sido commitado, e pela regra do próprio cabeçalho
ele só vale a partir do commit.

| § | antes | agora | por quê |
|---|---|---|---|
| cabeçalho | "vale a partir do commit" | vale a partir do commit **empurrado** | P-116 |
| cabeçalho | `pesquisa-e-plano-ml.md` | `pesquisa-e-plano-ml-1.md` | a referência não resolvia |
| 2, 4 | período até ago/2026; teste de 80 meses | até **dez/2025**; teste de **72 meses** | 2026 truncado (P-100); NEFIN até 07/2026 |
| 2 | — | limitações da série ajustada (A-11, P-112, P-113) | medidas em 21/09 na janela 2021–2025 |
| 6 | `L = 3` | **máximo entre L ∈ {1, 2, 3}** | com n = 72, L = 3 degenera e abaixa o corte |
| 6 | subperíodo 2023–2026 | 2023–2025 | segue o período |
| 7 | — | **condição 0: H-ML1 rejeitada** | vencer multifator sem sinal é trivial |
| 8 | oito testes | **nove** — poder com sinal plantado | "não rejeita" sem poder é ilegível |
| 9 | "os oito testes"; período não listado | "os nove"; período exige `v2` | consistência |
| 11 | — | grupo opcional com impressão própria | impressão do motor intocada |
| 12 | — | Lei 15.270/2025 como regime conhecido | dividendo tributado a partir de 2026 |

**O `m` não mudou** (11 na família, 24 no conservador).

# Manual de desenvolvimento assistido por IA

**Projeto:** sistema de ingestão, indicadores e backtest sobre dados públicos de mercado (escopo reduzido do laudo Rev. 03, §7).
**Contexto operacional:** um desenvolvedor, 3–4 h efetivas por semana, fragmentadas. Limite real de ritmo: cota de uso do assistente.
**Emissão:** 31/08/2026.

Este documento substitui os três guias auditados (C-01 a C-10 do laudo). Ele parte de duas correções que aqueles guias erravam:

1. **Cowork e Claude Code rodam o mesmo motor agêntico.** A escolha entre eles é de superfície, não de segurança. O portão de revisão é seu, e o mecanismo é git.
2. **CLAUDE.md é contexto, não imposição.** A documentação oficial diz isso explicitamente: para bloquear uma ação independentemente do que o modelo decida, use hook ou CI. Regras que *precisam* valer sempre não moram em prosa.

---

## 1. Os cinco princípios

**D1 · O repositório é a especificação.** Nada que importa vive numa conversa. Se uma regra só existe no chat, ela não existe.

**D2 · A especificação é o blueprint corrigido, nunca o original.** O achado C-07 do laudo: colar as sete armadilhas da CVM sem colar as correções congelaria quatro defeitos críticos por trinta semanas. O `CLAUDE.md` carrega as regras **substituídas** marcadas como proibidas.

**D3 · Você fornece o domínio; o assistente fornece a implementação.** Layout do COTAHIST, campos da CVM, regra fiscal, fator de ajuste — nada disso sai da cabeça do modelo. Se o spec não foi colado, o código é pseudocódigo.

**D4 · O teste é a especificação executável.** Código que parece certo não é verificável. Teste que passa é. Isto vale duplamente aqui, porque os erros que matam o projeto (escala, sinal, período, ajuste aditivo) não aparecem na leitura.

**D5 · O que precisa valer sempre vira hook ou CI.** Prosa em `CLAUDE.md` é seguida com alta frequência, não com garantia. Três regras deste projeto são invioláveis e por isso não ficam só em prosa: não escrever em `data/bronze/`, não usar data corrente em transformação, não commitar `data/` ou `.env`.

---

## 2. Arquivos a criar

Sete arquivos na raiz, mais o diretório `.claude/`. Não são cinco arquivos de gestão — são dois de contexto e cinco de projeto. `PROGRESS.md`, `TASKS.md` e `VALIDATION.md` dos guias antigos foram removidos: são estado que já existe em git e em issues, e que diverge em três semanas. Um arquivo de progresso desatualizado é pior que nenhum, porque as sessões seguintes o leem como verdade.

### 2.1 `CLAUDE.md` — o único arquivo que o assistente lê sozinho

Carregado automaticamente no início de toda sessão. Hierárquico: o modelo caminha da pasta atual até a raiz do repositório e concatena todos os `CLAUDE.md` encontrados. Suporta importação por `@caminho`, com profundidade máxima de cinco saltos.

**Regra de ouro:** se uma linha não muda o comportamento do agente, apague-a. Não é documentação; é contrato. Mantenha abaixo de ~200 linhas; acima disso, mova o específico para `.claude/rules/`.

```markdown
# Projeto — laboratório de dados de mercado

## O que é
Ingestão de dados públicos (CVM, B3), séries de preço ajustadas,
indicadores fundamentalistas e backtest point-in-time.
Objetivo: aprendizado + enciclopédia consultável. NÃO gerencia carteira.

## Escopo — o que NÃO existe neste projeto
Não implemente, não sugira, não crie arquivo para:
- motor de aporte, carteira, movimentações, Postgres, FastAPI
- módulo de Imposto de Renda
- FIIs, renda fixa, exterior, cripto, opções
- score de qualidade composto (bloqueado até a decisão D-004)
Se uma tarefa parecer exigir qualquer um destes, PARE e pergunte.

## Pilha — não acrescente tecnologia sem me perguntar
Python 3.12 · uv · DuckDB · dbt-duckdb · Streamlit · make
Deliberadamente FORA: Postgres, FastAPI, Prefect, Docker, Polars, Spark, Kafka.
Polars só entra se for demonstrado que SQL não resolve. Justifique antes.

## Regras invioláveis
1. `data/bronze/` é imutável. Nunca edite, nunca sobrescreva, nunca delete.
2. NUNCA use `now()`, `current_date`, `current_timestamp` ou `date.today()`
   em camada de transformação (dbt/, src/parsers/, src/indicadores/).
   Toda lógica as-of recebe a data como parâmetro explícito.
3. Nunca commite `data/`, `.env`, ou qualquer arquivo com e-mail pessoal.
4. Encoding latin-1 em tudo que vem de CVM, B3 e ANBIMA. Nunca assuma UTF-8.
5. Leitura de Parquet é por nome de coluna, nunca por posição.

## Correções ao blueprint — a versão antiga está PROIBIDA
| Tema | Regra vigente | Proibido |
|---|---|---|
| Versões CVM | Silver preserva TODAS as versões. `max(versao)` é seleção de query com `dt_disponivel <= :as_of` | Deduplicar por `max(versao)` na carga |
| `dt_disponivel` | Vem de fonte declarada + coluna `dt_disponivel_origem` (observada/inferida/estimada) | Usar timestamp de coleta |
| Ajuste de série | Multiplicativo: fator = (P_com − D)/P_com aplicado a toda a série anterior | Ajuste aditivo (P − D) |
| Datas de evento | Fator se aplica no `dt_ex`. `dt_com` é o último pregão COM direito | Aplicar o fator em `dt_com` |
| Janelas de backtest | 5 e 10 anos apenas (fundamentos CVM começam em 2010) | Janelas de 15 ou 20 anos |
| Universo | Inclui empresas deslistadas desde 2010 | Só as ~400 listadas hoje |
| Validação de ajuste | Invariante interna (ex-date, FATCOT↔grupamento, retorno vs. índice) | Yahoo ou brapi como oráculo |
| FATCOT | Fator de cotação (unidade vs. lote). É INSUMO do ajuste | Tratar como fator de proventos |

## Como trabalhamos
- Antes de implementar, preencha a Ficha de Insumos (@docs/ficha-insumos.md)
  e PARE. Não escreva código antes de eu responder.
- Uma tarefa por sessão. Uma tarefa = um contrato testável.
- Teste primeiro, implementação depois.
- Nunca marque tarefa como concluída. Eu marco, depois de rodar.
- Toda decisão minha vai para DECISIONS.md, formato do próprio arquivo.

## Comandos
make setup · make bronze · make silver · make gold · make test · make ui
make rebuild  # reconstrói tudo a partir de bronze. Deve funcionar sempre.
```

**Verificação:** `/memory` lista os arquivos de instrução carregados; `/context` mostra o que efetivamente entrou na sessão. Use quando o modelo ignorar uma regra que você acha que está ativa.

### 2.2 `DECISIONS.md` — append-only, nunca editado

O único registro que não apodrece, porque nada é reescrito. Uma entrada por decisão sua.

```markdown
# Registro de decisões

## D-001 · 2026-08-31 · Pilha mínima
**Decisão:** Python + uv + DuckDB + dbt-duckdb + Streamlit + make.
**Justificativa:** 8 tecnologias excediam 3–4 h/semana de manutenção (laudo E-02).
Postgres e FastAPI sem função no escopo reduzido (E-03).
**Alternativas:** pilha completa do blueprint II.2. Rejeitada por superfície operacional.
**Reverte quando:** houver conta em corretora (Postgres) ou segundo consumidor (FastAPI).

## D-002 · 2026-08-31 · Pré-registro do backtest
**Decisão:** [limiar], métrica = bootstrap em blocos, máximo de [N] variantes de política
testáveis antes de reportar.
**Justificativa:** janelas móveis sobrepostas não são observações independentes (A-15).
**Não expira.** Alterar depois de ver o resultado anula o instrumento.

## D-003 · 2026-08-31 · Ajuste multiplicativo
**Decisão:** fator = (P_com − D)/P_com, aplicado a toda a série anterior, no dt_ex.
**Justificativa:** aditivo quebra a composição do retorno e gera preço negativo em
séries longas (laudo C-04).
**Oráculo dos testes:** Aviso aos Acionistas da empresa + arquivo de proventos B3.

## D-004 · PENDENTE · Núcleo indexado vs. seleção ativa
**Status:** bloqueia o score composto (II.5). Será resolvida pelo backtest reduzido,
não por argumento. Ver laudo §7.
```

### 2.3 `docs/ficha-insumos.md` — o protocolo de input

Detalhado na §5. É o arquivo que o `CLAUDE.md` importa e que governa o começo de toda tarefa.

### 2.4 `docs/fontes/` — os specs colados

Um arquivo por fonte, com o trecho oficial copiado e a data de acesso. **É a diferença entre implementação e pseudocódigo.**

```
docs/fontes/
├── cvm-dfp-layout.md          # colunas, tipos, ORDEM_EXERC, ESCALA_MOEDA, VERSAO
├── cvm-cadastro-layout.md     # situação de registro, datas
├── cotahist-layout.md         # layout posicional 245c, FATCOT, TPMERC
├── b3-proventos-endpoint.md   # payload, formato, exemplo de resposta real
└── README.md                  # o que já foi coletado e o que falta
```

Cada arquivo abre com o mesmo cabeçalho:

```markdown
# COTAHIST — layout de série histórica
Fonte: [URL] · Acesso: 2026-09-XX · Versão do documento: [se houver]
Status: [COMPLETO | PARCIAL — falta X | NÃO OBTIDO]
---
[trecho colado, verbatim]
```

O campo `Status` importa: um spec parcial explicitamente marcado é seguro. Um spec parcial que parece completo produz código plausível e errado.

### 2.5 `README.md` — cinco linhas, escrito no primeiro dia

Responde "como eu rodo isso". Com 3–4 h semanais fragmentadas, retomabilidade vale mais que arquitetura.

### 2.6 `Makefile` — reconstrução com um comando

```makefile
setup:    ## instala dependências a partir do lock
	uv sync

bronze:   ## coleta e grava bruto (idempotente via manifesto)
	uv run python -m src.coletores.cvm
	uv run python -m src.coletores.b3

silver gold:  ## transformações
	uv run dbt build --project-dir dbt --select $@

test:     ## pirâmide completa sobre fixtures
	uv run pytest tests/ -v
	uv run dbt test --project-dir dbt

rebuild:  ## reconstrói TUDO a partir de bronze. Deve funcionar sempre.
	uv run dbt build --project-dir dbt --full-refresh

check-determinismo:  ## E-06 — falha se houver data corrente em transformação
	@! grep -rEn "now\(\)|current_date|current_timestamp|date\.today\(\)" \
	    dbt/models/ src/parsers/ src/indicadores/ \
	  || (echo "ERRO: data corrente em camada de transformação" && exit 1)

ui:
	uv run streamlit run src/ui/app.py
```

`make rebuild` não é conveniência. É o teste de que P2 (reprodutibilidade a partir de Bronze) é verdade. Se ele quebrar, quebrou a propriedade central do sistema.

### 2.7 `.gitignore` e `.env.example` — no commit inicial

```gitignore
data/
*.duckdb
*.duckdb.wal
.env
.venv/
__pycache__/
dbt/target/
dbt/logs/
CLAUDE.local.md
```

```bash
# .env.example — copie para .env, que é gitignored
SEC_USER_AGENT="Nome Sobrenome email@exemplo.com"
DATA_DIR="./data"
```

O e-mail do User-Agent exigido pela SEC é dado pessoal e tende a ser hard-coded no coletor por descuido (laudo E-12).

### 2.8 `.claude/` — regras específicas e imposições

```
.claude/
├── settings.json          # hooks: o que precisa valer sempre
├── rules/
│   ├── coletores.md       # carrega quando o modelo toca src/coletores/
│   ├── parsers.md         # as 7 armadilhas da CVM, em detalhe
│   ├── dbt.md             # on_schema_change, convenções, testes obrigatórios
│   └── testes.md          # a pirâmide da §4, e o que cada camada cobre
└── commands/
    ├── nova-tarefa.md     # o protocolo da §5, como slash command
    └── revisar.md         # o prompt de revisão da §6.3
```

As regras com escopo de caminho carregam sob demanda, quando o modelo entra naquela subárvore. Isso mantém o `CLAUDE.md` raiz curto — que é o que o faz ser seguido.

**Distinção que os guias antigos não faziam.** Três categorias, três mecanismos:

| Tipo de regra | Onde vive | Por quê |
|---|---|---|
| Preferência, convenção, contexto | `CLAUDE.md` / `.claude/rules/` | Alta aderência, sem garantia. Suficiente |
| Regra que precisa valer **sempre** | hook em `.claude/settings.json` | A doc oficial é explícita: para bloquear uma ação, use hook, não prosa |
| Propriedade verificável do repositório | alvo de `make` + CI | Falha ruidosa, independe de quem escreveu |

As três invioláveis deste projeto (bronze imutável, sem data corrente, sem commit de `data/`) têm as três formas: escritas no `CLAUDE.md`, bloqueadas por hook, verificadas em CI. Redundância deliberada.

---

## 3. Estrutura de pastas

```
projeto/
├── CLAUDE.md
├── DECISIONS.md
├── README.md
├── Makefile
├── pyproject.toml
├── uv.lock                     # versionado — reprodutibilidade (E-11)
├── .python-version
├── .gitignore
├── .env.example
├── .claude/
│   ├── settings.json
│   ├── rules/
│   └── commands/
├── .github/workflows/ci.yml
│
├── docs/
│   ├── blueprint-corrigido.md  # a especificação vigente
│   ├── ficha-insumos.md
│   ├── pre-registro-backtest.md
│   └── fontes/
│
├── src/
│   ├── coletores/              # baixar e gravar bruto. Um arquivo por fonte.
│   │   ├── cvm.py
│   │   ├── b3.py
│   │   └── manifesto.py        # idempotência (E-04)
│   ├── parsers/                # bruto → estruturado. As 7 armadilhas moram aqui.
│   │   ├── dfp.py
│   │   ├── cotahist.py
│   │   └── eventos.py
│   ├── schemas/                # Pydantic. NÃO chamar de models (colide com dbt)
│   ├── politica/               # carga e validação do YAML (P3)
│   ├── indicadores/
│   ├── backtest/
│   ├── ui/                     # Streamlit
│   └── comum/
│       ├── log.py              # log estruturado com run_id (E-08)
│       └── tempo.py            # ÚNICO lugar autorizado a ler data corrente
│
├── dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── staging/
│   │   ├── silver/             # preserva TODAS as versões
│   │   └── gold/               # seleção as-of parametrizada
│   └── tests/
│
├── config/
│   └── politica.yaml
│
├── tests/                      # ver §4
│
├── scripts/
│
└── data/                       # gitignored
    ├── bronze/                 # imutável
    ├── silver/
    └── gold/
```

**Três decisões que corrigem os guias antigos.** `src/schemas/` em vez de `src/models/`, porque dbt já chama de *models* os arquivos SQL e a colisão de vocabulário confunde tanto você quanto o assistente. `src/politica/` existe, porque o P3 não tinha casa na árvore proposta. E `src/comum/tempo.py` é o único módulo autorizado a ler a data corrente — o que torna a regra E-06 verificável por `grep`, não por disciplina.

---

## 4. Estrutura de testes

Cinco camadas. As duas primeiras são o que os guias antigos propunham; as três seguintes são o que pega os erros que efetivamente matam este projeto.

```
tests/
├── fixtures/                   # amostras congeladas, pequenas, versionadas
│   ├── cvm_dfp_amostra.csv     # ~200 linhas, latin-1, com ORDEM_EXERC
│   ├── cotahist_amostra.txt    # ~200 linhas posicionais, com FATCOT ≠ 1
│   └── proventos_b3.json
├── unit/                       # 1. funções puras
├── contrato/                   # 2. layout de fonte não mudou
├── canonicos/                  # 3. casos com oráculo externo
├── invariantes/                # 4. propriedades que sempre valem
└── golden/                     # 5. registros conferidos à mão
```

### Camada 1 — unitários

Funções puras, sobre fixtures. Rápidos, determinísticos, sem rede.

### Camada 2 — contrato de fonte

Rodam contra a fonte real, uma vez por dia, e alertam quando o layout muda. Endpoints da B3 não são documentados e mudam sem aviso (Q-07 do laudo). São os únicos testes que tocam a rede.

```python
def test_cotahist_largura_de_linha():
    """Se a B3 mudar o layout, isto falha antes de corromper Bronze."""
    linha = baixar_primeira_linha_do_dia()
    assert len(linha) == 245
```

### Camada 3 — canônicos, com oráculo externo

**Esta é a camada que os guias antigos erraram.** Os exemplos que eles davam usavam ajuste aditivo e fabricavam o valor esperado — codificando o mesmo palpite em dois lugares. Um caso canônico só vale se o valor esperado vier de fora.

```python
def test_ajuste_dividendo_multiplicativo():
    """Oráculo: Aviso aos Acionistas de [EMPRESA], [DATA], + arquivo de
    proventos da B3. Ver docs/fontes/b3-proventos-endpoint.md.

    Fator = (P_com − D) / P_com, aplicado a TODA a série anterior ao ex.
    Aditivo (P − D) está PROIBIDO: quebra a composição do retorno e
    produz preço negativo em séries longas. Ver DECISIONS.md D-003.
    """
    serie = carregar_fixture("serie_pre_evento")
    evento = EventoCorp(tipo=DIVIDENDO, dt_com=DT_COM, dt_ex=DT_EX, valor=D)

    fator = (P_COM - D) / P_COM
    ajustada = ajustar(serie, [evento])

    assert ajustada[DT_COM] == pytest.approx(P_COM * fator, rel=1e-6)
    assert ajustada[DT_EX] == pytest.approx(P_EX, rel=1e-6)  # ex não se ajusta
```

Casos canônicos mínimos antes de confiar no ajuste: dividendo, **JCP** (retenção de 15% na fonte — decida e registre se a série ajusta pelo bruto ou pelo líquido), desdobramento, **grupamento com mudança de FATCOT** (é onde a série ganha três ordens de grandeza em silêncio), bonificação e subscrição. Subscrição é o mais difícil e o que fontes de terceiros erram com mais frequência: não a deixe como `TODO`.

### Camada 4 — invariantes

Propriedades que valem sempre, sem oráculo externo. É a camada de maior retorno por hora, e nenhum dos guias a propunha.

```python
def test_balanco_fecha():
    """Ativo = Passivo + PL. Pega ESCALA_MOEDA e sinal invertido."""

def test_itr_reconcilia_com_dfp():
    """Soma dos trimestres = anual. Pega Q4 derivado errado e ORDEM_EXERC."""

def test_gap_no_ex_bate_com_provento():
    """No ex, o gap de preço BRUTO ≈ provento, dentro de banda.
    Detecta evento não tratado sem depender de Yahoo ou brapi (A-14)."""

def test_fatcot_coincide_com_grupamento():
    """Toda mudança de FATCOT tem evento correspondente em evento_corp."""

def test_retorno_total_reproduz_indice():
    """Cesta de constituintes ajustada ≈ retorno total do índice publicado.
    É o teste mais forte do ajuste, e o oráculo é a própria B3."""

def test_reconstrucao_determinista():
    """Rodar `make rebuild` duas vezes produz hash idêntico em Gold.
    Falha se houver data corrente em transformação (E-06)."""

def test_pontualidade_temporal():
    """Nenhuma linha de Gold com dt_disponivel > data de referência da consulta.
    O smoke test do laudo, automatizado."""
```

### Camada 5 — golden records

Dez empresas × cinco anos, conferidas à mão contra o DFP publicado, congeladas como esperado. Caras de produzir, imbatíveis para detectar deriva silenciosa. Produza depois da camada 4, não antes.

### CI

Camadas 1, 3, 4 e 5 sobre fixtures, mais `make check-determinismo`, mais `dbt build` sobre a amostra. Camada 2 em agendamento diário separado, porque toca a rede. Em projeto solo, CI não coordena equipe — detecta que o ambiente derivou desde a última sessão.

---

## 5. Procedimento de inputs

O problema real: o modelo produz código plausível para specs que não recebeu, e o erro é de semântica de domínio, não de sintaxe. A defesa é procedimental.

### 5.1 A Ficha de Insumos

Toda tarefa começa com isto, e **o modelo para aqui**. `docs/ficha-insumos.md`:

```markdown
# Ficha de Insumos — preencher ANTES de qualquer código

## Tarefa
[uma frase]

## Contrato
Entrada: [tipo, formato, origem]
Saída: [tipo, formato, destino]
Critério de aceite: [verificável, não "funciona"]

## 1. Specs que preciso e não tenho
Liste cada documento oficial necessário. Para cada um: qual campo/regra,
e o que acontece se eu prosseguir sem ele.

## 2. Suposições que estou fazendo
Liste TODA suposição, inclusive as que parecem óbvias.
Formato: "Suponho X. Se for Y, o efeito é Z."

## 3. Constantes cuja procedência não sei
Todo número mágico que eu precisaria escrever. Para cada um, de onde deveria vir.

## 4. Decisões que são suas, não minhas
Escolhas de domínio, política ou tributação que não me cabem.

## 5. O que já existe no repositório e devo reusar
Arquivos que li e que esta tarefa deve estender em vez de duplicar.

## 6. Regras do CLAUDE.md que esta tarefa toca
Cite as que se aplicam e como pretendo respeitá-las.

## Veredito
[ ] Tenho tudo. Posso implementar.
[ ] Falta o item N. NÃO vou implementar até receber.
```

### 5.2 Sinais de que falta insumo

Se o modelo produzir código sem ter pedido spec, e o código fizer parsing de dado externo, desconfie por padrão.

| Sinal | Significado | Ação |
|---|---|---|
| Constante mágica sem procedência (`largura = 245`) | Assumiu o layout | Buscar o documento oficial e colar em `docs/fontes/` |
| "Assumindo que...", "tipicamente...", "geralmente..." | Está supondo | Não aceite. Converta em item da seção 2 da ficha |
| Alíquota, isenção ou limite sem citação | Inventou regra fiscal | Validar contra fonte primária. Este é o pior modo de falha |
| `# TODO: adicionar regra X` | Sabe que falta | Buscar antes de continuar |
| Nenhuma pergunta e código completo | Pode ter inventado sem saber | **Sinal mais perigoso.** Validar com dado real imediatamente |
| Propôs tecnologia fora da pilha | Não leu ou ignorou o `CLAUDE.md` | Rodar `/context` e verificar o que carregou |

### 5.3 Insumo obrigatório por tipo de tarefa

| Tarefa | Insumo obrigatório | Consequência de prosseguir sem |
|---|---|---|
| Coletor | URL exata, formato, encoding, cadência, política de rate limit | Bloqueio por abuso ou coleta parcial silenciosa |
| Parser CVM | Layout de colunas + as 7 armadilhas + exemplo real | Escala em 3 ordens de grandeza, linhas duplicadas |
| Parser COTAHIST | Layout posicional completo + `FATCOT` + `TPMERC` | Layout inventado; falha silenciosa |
| Ajuste de série | Fórmula (multiplicativa), `dt_ex` vs. `dt_com`, tratamento de JCP | O bug mais caro do projeto |
| Indicador | Definição exata + fonte de cada componente | Número plausível e errado |
| Modelo dbt | Se preserva versões, e qual a chave as-of | Quebra a bitemporalidade |
| Backtest | Pré-registro (D-002) já escrito | Overfitting com aparência de prova |

### 5.4 O que nunca delegar

- **Decisão de política de investimento.** Pesos, filtros, tetos. Vão para `politica.yaml` com justificativa em `DECISIONS.md`.
- **Validação do próprio design.** O modelo tende a concordar com você. Use-o como implementador, não como validador.
- **Regra fiscal escrita do zero.** Cole a regra da fonte e peça implementação dela.
- **Interpretação do backtest.** O código pode ser gerado; a leitura do resultado é sua, contra o pré-registro.
- **Refatoração grande sem testes verdes antes e depois.**
- **Verificação dos quatro pilares que viram parâmetro** (diversificação, lucro/dívida, múltiplos, ETFs). A Parte I foi produzida por um sistema da mesma classe; validá-la com outro não é verificação. 4–8 h de leitura humana.

---

## 6. Fluxo por sessão

### 6.1 Abertura

```
Leia CLAUDE.md e DECISIONS.md.
Rode `git log --oneline -10` e me diga onde paramos.
Próxima tarefa: [T-XXX].
Preencha a Ficha de Insumos. NÃO implemente.
```

Sem `PROGRESS.md`: o histórico de commits é o registro que não diverge, porque é gerado pelo próprio trabalho.

### 6.2 Implementação

Depois de responder a ficha e colar os specs faltantes:

```
Insumos completos. Specs colados em docs/fontes/.

Implemente nesta ordem:
1. Os testes das camadas 1, 3 e 4 para este contrato.
2. Mostre os testes. PARE. Vou revisar antes de você escrever a implementação.
3. Só depois, a implementação que os satisfaz.
```

Teste antes de código não é preferência de estilo aqui — é o que dá ao modelo uma especificação verificável em vez de uma descrição, e é o que consome menos cota, porque evita a iteração conversacional até o código sair certo.

### 6.3 Revisão

Sessão separada. `.claude/commands/revisar.md`:

```
REVISE [arquivo]. Busque especificamente:
1. Violação de regra inviolável do CLAUDE.md (bronze, data corrente, segredos)
2. Data corrente implícita em transformação
3. Leitura de Parquet por posição em vez de nome
4. Idempotência: rodar duas vezes duplica algo?
5. Edge cases: arquivo vazio, ZIP corrompido, encoding errado, coluna ausente
6. Constantes cuja procedência não está em docs/fontes/
7. Erro silencioso — algo que falha sem alertar

Para cada problema: explique, mostre o trecho, mostre a correção.
NÃO corrija ainda. Apenas liste.
```

O "não corrija ainda" força a revisão a ser explícita e te dá a chance de julgar se ela procede.

### 6.4 Fechamento

Você roda os testes. Você faz o commit, com mensagem que diz o porquê. Se houve decisão, você acrescenta entrada em `DECISIONS.md`. O modelo nunca marca tarefa como concluída.

### 6.5 Quando o modelo errar

1. Não peça "corrija" sem especificar o erro — corrige o sintoma, não a causa.
2. Converta o erro em caso de teste, imediatamente.
3. Se a causa foi contexto faltante, acrescente a regra ao `CLAUDE.md` ou a `.claude/rules/`.
4. Se o erro repetir mesmo com a regra escrita, ela precisa virar hook ou verificação de CI. Prosa não estava bastando.

---

## 7. Cota como recurso de projeto

O limite real de ritmo é a cota de uso, e trabalho agêntico multi-passo consome cota substancialmente mais rápido que chat. Consulte os limites vigentes do seu plano em `https://support.claude.com`.

**O que gasta muito:** iterar em conversa até o código sair certo; pedir a fase inteira de uma vez; deixar o agente explorar o repositório sem alvo; refatoração ampla.

**O que gasta pouco:** ficha de insumos preenchida antes; specs colados de uma vez em vez de descobertos por tentativa; teste como especificação; tarefa com contrato fechado; `.claude/rules/` com escopo de caminho, que carrega só o relevante.

**Unidade de tarefa.** O critério "50–200 linhas" dos guias antigos está errado — um parser de COTAHIST correto é naturalmente 150–300 linhas e quebrá-lo piora. O critério certo é **um contrato testável**, e que caiba entre dois resets de cota sem perder o fio. Se perder o fio no meio, o `CLAUDE.md` e o `DECISIONS.md` te devolvem ao ponto sem custo.

---

## 8. Ordem de execução

**Sessão 1 — sem código.** `CLAUDE.md`, `DECISIONS.md` com D-001 a D-004, `.gitignore`, `.env.example`, `README.md`, `Makefile` com os alvos vazios, `pyproject.toml` + lock, CI mínima, `docs/fontes/README.md` listando o que falta obter. Commit inicial.

**Sessão 2 — sem código.** Escreva D-002 (pré-registro do backtest) com data. Defina o evento externo com data que não depende de nenhuma fase estar pronta — mitigação do risco R-01 do laudo. Colete os specs de CVM e COTAHIST para `docs/fontes/`.

**Sessão 3 — primeiro código, deliberadamente trivial.** `make setup` funciona, DuckDB abre, um teste passa, CI verde. Comprova a pilha antes de qualquer domínio.

**Sessão 4 em diante.** Coletor CVM → parser DFP com as sete armadilhas → modelos dbt com preservação de versões → smoke test point-in-time. O smoke test na semana 2, não na 16: é o que transforma a decisão mais arriscada do projeto em algo com retorno rápido.

**Marco.** Quando a fase 0 fechar, pare e meça as horas reais. O fator de erro observado recalibra todas as estimativas do laudo, e é a única falsificação empírica barata que o projeto oferece.

# Laudo de auditoria técnica — consolidado

**Objeto:** *Engenharia Reversa do Bastter* — dossiê técnico, Rev. 01, 28/08/2026, Parte II (blueprint e roadmap); documentos derivados de auditoria e de método de desenvolvimento.
**Cliente:** Osvaldo Santana Jr., pessoa física.
**Emissão:** 31/08/2026. Rev. 03 — consolida e substitui as Rev. 01 e Rev. 02.
**Auditor:** sistema de IA. Ver §9 (independência e conflitos).

---

## 1. Parecer

### 1.1 Opinião

> O blueprint projeta um gestor de patrimônio para quem ainda não tem patrimônio: dois terços do escopo não têm insumo hoje. O terço restante — ingestão, séries ajustadas, indicadores e um backtest reduzido — atende integralmente ao objetivo declarado, mas depende de cinco decisões que vencem nas primeiras semanas e que o roadmap não agenda. A camada de engenharia de dados é bem projetada; a camada de engenharia de software não foi projetada.

### 1.2 As três conclusões estruturantes

**Primeira — escopo sem insumo.** O cliente não tem patrimônio, conta em corretora nem aporte mensal. O motor de decisão de II.6 calcula `D_i = w*_i · (V + A) − v_i` com `V = 0` e `A = 0`; o nível 1 da hierarquia divide por `V`. Não produz recomendação ruim: não tem entrada. Em cadeia caem o freio de concentração, o gatilho de deriva, a banda morta, o módulo de IR e os módulos de FII, renda fixa, exterior, cripto e opções. Entre 60% e 70% da Parte II está suspensa por ausência de insumo, não por defeito.

**Segunda — a ordem do roadmap não é a ordem do custo.** Os cinco achados de maior impacto (A-05, A-03, A-01, C-04, A-02) vencem nas semanas 1 a 4; três só produzem sintoma na semana 12 ou depois; um nunca é agendado. O roadmap está ordenado por dependência técnica, não por custo de erro tardio.

**Terceira — a engenharia de software está ausente do documento.** O dossiê especifica arquitetura de dados com rigor e não especifica: concorrência, evolução de schema, idempotência, determinismo temporal, estratégia de teste, integração contínua, gestão de dependências, segredos, observabilidade ou orçamento de operação. São dezenove achados na §5, e a maioria é barata agora e cara depois.

### 1.3 Escopo excluído nominalmente

1. Validade empírica dos treze pilares da Parte I. Nenhuma fonte acadêmica foi aberta. A Parte I é tratada como declaração do cliente.
2. Exatidão das URLs e layouts declarados em II.4 como verificados em 28/08/2026. Nenhum endpoint foi acessado.
3. Correção das regras tributárias citadas. Exigem profissional habilitado.
4. Qualquer juízo sobre mérito de investimento, alocação ou o método Bastter como estratégia financeira.
5. Conformidade LGPD e segurança de infraestrutura além do apontado em E-12.

### 1.4 Método

Leitura integral do dossiê. Verificação de consistência interna seção contra seção — para esses achados o dossiê é a própria fonte, e são reproduzíveis por leitura. Duas buscas web em 31/08/2026 sobre fatos de produto Anthropic (§10). Nenhuma outra fonte externa consultada. Achados rotulados **FATO** (verificável na fonte), **INFERÊNCIA** (derivação) e **OPINIÃO** (juízo).

---

## 2. Qualidades — o que deve ser preservado

Registrado antes dos defeitos porque parte do que segue seria perdido numa simplificação apressada.

### 2.1 Engenharia de dados

| ID | Qualidade | Por que preservar |
|---|---|---|
| Q-01 | Bronze imutável com hash e timestamp de coleta | Permite reprocessar toda a história quando um bug de transformação for descoberto. É a decisão mais valiosa do blueprint |
| Q-02 | Medalhão bronze/silver/gold sobre Parquet + DuckDB | Dimensionamento correto para 8 GB. Colunar, embarcado, sem operação |
| Q-03 | Recusa explícita a Spark, Kafka e warehouse gerenciado | O dossiê nomeia esse excesso como o modo de morte mais comum de projetos assim. Está certo |
| Q-04 | dbt-duckdb com testes declarativos e linhagem | SQL versionado é o que torna P2 executável em vez de aspiracional |
| Q-05 | As sete armadilhas da CVM documentadas | `VERSAO`, `ESCALA_MOEDA`, consolidado × individual, `ORDEM_EXERC`, Q4 derivado, plano setorial, COTAHIST não ajustado. É conhecimento tácito que custa meses a quem descobre sozinho |
| Q-06 | Ponte `codeCVM ↔ issuingCompany ↔ ticker ↔ CNPJ` priorizada | O ponto onde a maioria das tentativas caseiras trava, corretamente colocado no início |
| Q-07 | Teste de contrato diário para endpoints não documentados da B3 | Detecta mudança de layout no primeiro desvio, não três meses depois |
| Q-08 | Cruzamento de fontes de preço como detector de bug | "Divergência revela evento corporativo não tratado" é a inversão certa: o cruzamento não é redundância, é instrumento |
| Q-09 | Rejeição de StatusInvest por proibição contratual | Decisão correta, tomada por antecipação |

### 2.2 Projeto do sistema

| ID | Qualidade | Por que preservar |
|---|---|---|
| Q-10 | P3 — regras como dados, em YAML versionado | Trocar política vira commit, não deploy. Habilita o teste que o Bastter não permite |
| Q-11 | P4 — `recomendacao` com `snapshot_entrada` e `politica_hash` | Reconstruir em 2030 por que o sistema decidiu o que decidiu. Engenharia de qualidade real |
| Q-12 | `posicao_alvo` versionada, nunca sobrescrita | Consistente com a bitemporalidade do resto |
| Q-13 | Gatilho de deriva que apresenta cenários fiscais e não vende sozinho | A melhor ideia do blueprint. Suspensa por falta de insumo, não descartada |
| Q-14 | Streamlit primeiro, Next.js depois | Existe para impedir que o projeto morra antes de dar valor. O motivo está certo |
| Q-15 | As três travas do módulo de opções | Perda máxima conhecida, proibição estrutural de descoberto no código, P&L segregado. Condicionamento correto |
| Q-16 | `fii_informe` em formato longo | Escolha defensável para informes com ~60 colunas voláteis. Ver ressalva em E-18 |

---

## 3. Achados de consistência do dossiê

Legenda: **CONTRADITADO** (o dossiê nega em uma seção o que afirma em outra) · **DEFEITO** (erro de projeto) · **AUSENTE** (elemento necessário inexistente) · **INSUFICIENTE** (evidência não permite veredito).

| ID | Afirmação | Evidência | Localização | Veredito | Conf. |
|---|---|---|---|---|---|
| A-01 | Silver deduplica por `max(versao)` | II.8 req. 3 exige a versão vigente na data; deduplicar na carga destrói a informação | Diagrama II.2 vs. II.8 | CONTRADITADO | Forte |
| A-02 | Backtest com janelas de 5/10/15/20 anos | II.4 declara CVM DFP desde 2010, ITR desde 2011 | II.4 vs. II.8 req. 5 | CONTRADITADO | Forte |
| A-03 | `dt_disponivel` obrigatório em todo fato | Nenhuma linha de II.4 declara fonte para o campo | II.3 vs. II.4 | AUSENTE | Forte |
| A-04 | `dt_deslistagem` na dimensão entidade | Sem fonte declarada; II.8 req. 1 depende dele | II.3 vs. II.4 | AUSENTE | Forte |
| A-05 | "Cada linha da Parte I vira requisito na Parte II" | Pilares 4 e 11 julgados Contraditado; a Parte II constrói seleção de 20–30 ações, sem ETF em `especies_permitidas`, sem benchmark 100% índice | I.6, I.7 vs. II.5, II.8 | CONTRADITADO | Forte |
| A-06 | `divida_liq_ebitda_max` como portão duro | `excluir_setores: []` vazio; PN incluída para reter bancos; EBITDA indefinido para instituição financeira | II.5 | CONTRADITADO | Forte |
| A-07 | Portão de dívida "por setor" | Comentário diz dicionário; o YAML traz escalar | II.5 | DEFEITO | Forte |
| A-08 | Caixa não é classe do sistema | `CLASSES` não o inclui; I.2 exige reserva ≥ 6 meses; o PI sempre deixa sobra sem destino | I.2, II.3, II.6 | AUSENTE | Forte |
| A-09 | Sem vínculo recomendação → execução | `movimentacao` não referencia `rec_id`, embora I.7 conclua que o valor está na arquitetura de decisão | II.3 vs. I.7 | AUSENTE | Forte |
| A-10 | "Custo da pilha de dados: R$ 0/mês" | II.2 declara VPS de R$ 30–60/mês | Capa vs. II.2 | CONTRADITADO | Forte |
| A-11 | Robustez como requisito | Backup e recuperação não aparecem em nenhuma seção | II.2, II.10 | AUSENTE | Forte |
| A-12 | Motor decide classe, depois ativo | O PI de II.6 é formulado globalmente sobre todo *i*; o contrato de saída traz `classe_mais_atrasada` | II.6 | DEFEITO | Moderada |
| A-13 | Modelo suporta tudo que vem depois | Sem calendário de negociação, sem tipo decimal, `custos` agregado, sem `dt_ex` | II.3 | AUSENTE | Forte |
| A-14 | Mitigar risco de ajuste com Yahoo e brapi | II.4 classifica Yahoo com ToS restritivo; II.10 lista sua quebra como risco médio; brapi é compra opcional | II.4, II.10 | DEFEITO | Forte |
| A-15 | Reportar distribuição sobre janelas móveis | Janelas de 10 anos em 16 de história são ~1,6 observações independentes | II.8 req. 5 (INFERÊNCIA estatística) | DEFEITO | Forte |
| A-16 | Sistema cobre a sequência do método | Sem módulo de dívidas, reserva ou marco de 24 meses, apesar de I.2 defini-los e I.6 sustentá-los | I.2 vs. II.7 | AUSENTE | Forte |
| A-17 | Roadmap de 16 semanas | Fase 1 dá 2 semanas ao componente que o próprio dossiê chama de mais propenso a erro; fase 4 dá 3 semanas a quatro domínios de ingestão | II.9 (INFERÊNCIA) | DEFEITO | Moderada |
| A-18 | Z-score dentro do setor | Subsetores B3 com poucas empresas tornam σ instável e a winsorização inoperante; μ e σ point-in-time não especificados | II.5 | DEFEITO | Moderada |
| A-19 | FII: distribuído ≤ resultado gerado | Compara regime caixa com resultado contábil | II.7 (pendência #3) | INSUFICIENTE | Moderada |

---

## 4. Achados sobre os documentos derivados

### 4.1 Segunda auditoria

| ID | Afirmação | Evidência | Veredito | Conf. |
|---|---|---|---|---|
| B-01 | FATCOT é "o próprio ajuste da B3" | FATCOT é fator de cotação (unidade ou lote), não fator de proventos | DEFEITO | Moderada |
| B-02 | Cadastro CVM traz datas de deslistagem | O campo disponível é cancelamento de registro na CVM, evento distinto da saída de negociação na B3 | DEFEITO | Moderada |
| B-03 | Rejeitar se não superar o CDI em ≥60% das janelas | Percentual sobre janelas sobrepostas não é taxa de sucesso (ver A-15) | DEFEITO | Forte |
| B-04 | Na banda morta, desempatar por maior gap | Com preços contínuos não há empate exato: a banda deixaria de existir e o sistema voltaria a perseguir ruído | DEFEITO | Forte |
| B-05 | Sobra do aporte vai para renda fixa | Empurra a RF acima do alvo — a deriva que o sistema combate | DEFEITO | Forte |
| B-06 | Documento intitulado "Versão Completa" | Inicia na §21; cita seções ausentes; duas das cinco correções críticas apontam para elas | DEFEITO | Forte |
| B-07 | §33 (venda escalonada na isenção mensal) | Achado válido e original, texto renderizado corrompido e ilegível | DEFEITO | Forte |
| B-08 | Justificativa do valor absoluto no PI | Diferenciabilidade é irrelevante em MILP; e recomenda objetivo quadrático com solver CP-SAT, que são incompatíveis | DEFEITO | Forte |

### 4.2 Guias de desenvolvimento

| ID | Afirmação | Evidência | Veredito | Conf. |
|---|---|---|---|---|
| C-01 | Cowork: "nada é feito sem você copiar", risco baixo | Cowork é modo agêntico que lê, cria e edita arquivos e executa tarefas multi-passo com autonomia | CONTRADITADO | Moderada |
| C-02 | Claude Code roda no terminal e esconde o raciocínio | Roda em terminal, IDE, app desktop e web; pede permissão e exibe diff antes de aplicar | CONTRADITADO | Forte |
| C-03 | "Cowork por mensagem / Claude Code por sessão" | Em assinatura ambos consomem a mesma cota; cobrança por token é o caminho Console/API | DEFEITO | Moderada |
| C-04 | Teste canônico: ajustado = 30,00 − 0,50 | Ajuste aditivo. O padrão é multiplicativo por `(P−D)/P`; aditivo quebra a composição do retorno e gera preços negativos em séries longas | DEFEITO | Forte |
| C-05 | `dt_com=15/03` descrito como ex-date | `dt_com` é o último pregão com direito; o fator se aplica no ex | DEFEITO | Forte |
| C-06 | Casos canônicos como especificação | Valores esperados fabricados para casar com a premissa; sem oráculo externo | DEFEITO | Forte |
| C-07 | CONTEXT.md com as armadilhas "coladas do blueprint" | Congelaria A-01, A-03, A-04 e A-05 como especificação canônica por 30 semanas | DEFEITO | Forte |
| C-08 | Fase 0 em tarefas 0.1–0.5 | Omite origem de `dt_disponivel`, ponte `codeCVM↔ticker`, universo com deslistadas e smoke test point-in-time | AUSENTE | Forte |
| C-09 | `data/` dentro do repositório | Sem `.gitignore`, sem tratamento de segredos, sem decisão sobre qual pasta o agente enxerga | AUSENTE | Forte |
| C-10 | "Você é o especialista em domínio, não o Claude" | A Parte I — obras, pilares, citações — foi produzida pelo mesmo tipo de sistema. O domínio já foi terceirizado | DEFEITO | Forte |

**Efeito consolidado de C-01 a C-03.** O eixo Cowork ↔ Claude Code não é supervisionado ↔ autônomo; é superfície sobre o mesmo motor. A recomendação "fique no Cowork por segurança" não entrega a segurança que promete — o prompt final do próprio guia manda o agente criar `docker-compose.yml`, `src/`, `tests/` e cinco arquivos. O argumento defensável que sobra: **o portão de revisão é seu, e o mecanismo é git** — branch por tarefa, commit antes, diff lido antes do merge. Funciona em qualquer superfície e não depende de fato de produto que muda a cada trimestre.

---

## 5. Auditoria de engenharia de software

Esta seção não existia nas revisões anteriores. O dossiê especifica arquitetura de dados; não especifica engenharia de software. Os dezenove achados abaixo são desse recorte.

### 5.1 Achados críticos

**E-01 · DuckDB é single-writer e a arquitetura assume o contrário.** *FATO parcial, ver pendência #6.*
O diagrama de II.2 tem Prefect (dbt), FastAPI e Streamlit tocando o mesmo arquivo `.duckdb`. DuckDB admite um único processo escritor; leitores concorrentes exigem abertura `read_only`. O sintoma aparece na fase 2, quando a UI passa a consultar enquanto o pipeline transforma, e se manifesta como falha de lock intermitente — o pior tipo para depurar em sessões de fim de semana.
*Correção:* transformar para arquivo temporário e fazer swap atômico ao final; leitores sempre `read_only=True`; ou manter Gold como Parquet e abrir DuckDB efêmero por consulta. **Decidir na fase 0 — muda o layout de diretórios.**

**E-02 · A superfície operacional da pilha excede o orçamento de manutenção.** *INFERÊNCIA, confiança forte.*
São oito tecnologias — Polars, DuckDB, Parquet, dbt, Prefect, Postgres, FastAPI, Streamlit, sobre Docker Compose — para um desenvolvedor com 3 a 4 horas efetivas por semana. Cada uma tem versão, incompatibilidade e modo de falha próprios. A justificativa de Polars no dossiê é comparativa ("5–20× mais rápido que pandas"), não dimensional: sobre 8 GB e uma execução semanal, a diferença é irrelevante e o custo de aprender uma segunda API não é.
*Correção — pilha mínima para o escopo revisado:* Python 3.12 + gerenciador com lockfile + DuckDB + dbt-duckdb + Streamlit + `make`/cron. Polars entra quando SQL comprovadamente não bastar, não por antecipação. Docker entra quando houver segundo ambiente.

**E-03 · Postgres e FastAPI não têm propósito no escopo revisado.** *INFERÊNCIA, confiança forte.*
Postgres existe para carteira, movimentações e recomendações — nenhuma das três existe sem conta em corretora. FastAPI existe como contrato entre motor e UI; com Streamlit lendo DuckDB direto, não há segundo consumidor. Mantê-los agora custa dois serviços, duas estratégias de migração e dois pontos de falha, por zero função.
*Correção:* remover ambos do escopo atual, com gatilho de reativação declarado (§11). Isso também resolve E-05 parcialmente e rebaixa A-11.

**E-04 · Idempotência é declarada e não especificada.** *FATO.*
II.2 diz "1 coletor por fonte, idempotente" e o guia repete "rodar duas vezes não duplica nada". Nenhum documento define a chave de idempotência. O caso real: a CVM republica ZIPs anuais; o hash muda, o conteúdo pode ou não ter mudado, e o coletor não tem como decidir se grava nova partição ou ignora.
*Correção:* tabela `manifesto_coleta(fonte, url, hash_conteudo, dt_coleta, status, bytes)` como fonte de verdade da idempotência; armazenamento endereçado por conteúdo em Bronze; hash igual ⇒ registra a tentativa e não grava partição nova; hash diferente ⇒ grava nova partição e **emite alerta**, porque republicação é sinal, não ruído — é exatamente o evento que A-01 precisa preservar.

**E-05 · Não há estratégia de evolução de schema em nenhuma das três camadas.** *AUSENTE.*
Parquet em Bronze: acrescentar coluna a partições históricas exige política de leitura tolerante a schema. dbt: sem `on_schema_change` definido, modelos incrementais quebram silenciosamente. Postgres (se voltar): sem ferramenta de migração declarada.
*Correção:* Bronze grava schema junto ao dado e a leitura é por nome, nunca por posição; dbt com `on_schema_change: fail` em incrementais, para que a quebra seja ruidosa; migração de Postgres decidida junto com sua reativação.

**E-06 · Determinismo temporal não é tratado, e é fatal num sistema bitemporal.** *INFERÊNCIA, confiança forte.*
P2 promete "reprocessa 18 anos de história em uma noite". Isso só é verdade se nenhuma transformação depender da data corrente. Qualquer `current_date`, `now()` ou `today()` dentro de um modelo dbt ou de um parser torna o reprocessamento não reprodutível — e num sistema cuja tese é o point-in-time, isso destrói a propriedade central sem produzir erro visível.
*Correção:* proibir data corrente implícita em toda a camada de transformação; toda lógica as-of recebe a data como parâmetro; um teste de CI que falha se `now()`, `current_date` ou `current_timestamp` aparecerem em `models/`. Regra de uma linha, valor desproporcional.

**E-07 · P7 não tem contrato operacional.** *AUSENTE.*
"Degrada, não quebra; usa o último dado bom e marca como `stale`." Não há definição de: quanto tempo torna um dado stale, por fonte; o que a camada seguinte faz ao receber stale; se o consumidor pode recusar. Sem isso, "degrada" na prática significa "usa dado velho em silêncio", que é o oposto da intenção.
*Correção:* tabela `fonte_status(fonte, ultima_execucao_ok, cadencia_esperada, limite_stale)`; propagação de flag até a UI; e uma inversão importante — **P7 não deve valer para nada que alimente decisão monetária**. Preço stale num gráfico é aceitável; preço stale numa recomendação de aporte é falha, e deve interromper, não degradar.

**E-08 · Não há rastreio de proveniência por execução.** *AUSENTE.*
P4 guarda o vetor de entrada da decisão. Não há equivalente para o pipeline: nada correlaciona uma linha de Gold à execução que a produziu, nem à partição de Bronze de origem. Quando o número estiver errado, não há como responder "de qual arquivo isso veio".
*Correção:* `run_id` gerado por execução, gravado em toda linha de Silver e Gold e emitido em log estruturado. Custa pouco e é a diferença entre depurar em minutos e em horas.

### 5.2 Achados de teste e integração

**E-09 · A pirâmide de teste está ausente; os testes existentes são sintáticos.** *FATO.*
O dossiê cita `unique`, `not_null` e `accepted_values` do dbt. Nenhum deles detecta os erros que matam este projeto: escala errada (`ESCALA_MOEDA`), sinal invertido, período errado (Q4 derivado), ajuste aditivo (C-04). Falta também estratégia de fixture: não há como testar um parser sem baixar gigabytes.
*Correção, três camadas:*
1. **Fixtures versionadas** — amostras congeladas e pequenas commitadas no repositório: um CSV de DFP truncado, 200 linhas de COTAHIST, um informe de FII. Tornam o teste rápido e determinístico.
2. **Golden records** — 10 empresas × 5 anos conferidas à mão contra o DFP publicado, congeladas como esperado.
3. **Invariantes contábeis** — Ativo = Passivo + PL dentro de tolerância; subtotais da DRE fecham; acumulados de ITR reconciliam com o DFP anual. São o que pega escala e sinal.

**E-10 · Não há integração contínua.** *AUSENTE.*
Em projeto solo com sessões espaçadas, CI não serve para coordenar equipe — serve para detectar que o ambiente derivou desde a última sessão. É o antídoto mais barato para o modo de falha "funcionava há três semanas".
*Correção:* um workflow que roda `pytest` sobre as fixtures, `dbt build` sobre a amostra, e a checagem de determinismo temporal de E-06. Dez minutos de configuração.

**E-11 · Dependências sem lockfile.** *FATO.*
O guia menciona `requirements.txt`. O dossiê recomenda fixar a versão do `yfinance` e de mais nada. Reprodutibilidade prometida em P2 é incompatível com dependências flutuantes.
*Correção:* gerenciador com lock (`uv` ou equivalente), lockfile versionado, versão de Python fixada no repositório.

### 5.3 Achados de segurança e operação

**E-12 · Segredos e dados pessoais sem estratégia.** *AUSENTE.*
O guia propõe `data/bronze|silver|gold` dentro da árvore do projeto. Quando o Postgres voltar, conterá movimentações, patrimônio e dados fiscais. Adicionalmente, a SEC exige User-Agent identificável com e-mail — dado pessoal que tende a ser hard-coded em coletor e versionado por descuido.
*Correção:* `data/`, `.env` e credenciais fora do versionamento no commit inicial; e-mail do User-Agent em variável de ambiente; decisão explícita e registrada sobre qual diretório um agente de código enxerga.

**E-13 · Docker sem definição de estado.** *AUSENTE.*
Onde vive o arquivo `.duckdb` — bind mount ou volume nomeado? O que entra no backup? Sem isso, `docker compose down -v` apaga meses de coleta sem aviso.
*Correção:* já resolvido em boa parte por E-02 (adiar Docker). Quando entrar: dados sempre em bind mount explícito, nunca em volume anônimo.

**E-14 · Não há orçamento de operação.** *AUSENTE.*
Os documentos orçam construção. Endpoints não documentados da B3 exigem manutenção perpétua — estimativa de 2 a 5 horas por mês em regime, com picos. Sobre 3 a 4 horas efetivas semanais, isso consome entre 15% e 30% da capacidade permanentemente, e nenhuma projeção de prazo desconta isso.

### 5.4 Achados de modelo e código

**E-15 · Chaves primárias não declaradas em `cotacao` e `evento_corp`.** *FATO.* `fato_contabil` tem PK explícita; as outras duas não. `evento_corp` não tem chave natural óbvia, e recoleta produzirá duplicatas silenciosas — que corromperão o ajuste de série, que é o risco "alto e caro" do próprio dossiê. *Correção:* unicidade explícita em `(instrumento_id, tipo, dt_com, valor_por_acao)` ou equivalente, com teste dbt.

**E-16 · `snapshot_entrada jsonb` sem versão de schema.** *FATO.* JSON sem campo de versão apodrece: em 2030 não se saberá qual formato ler. *Correção:* `schema_versao` no próprio documento.

**E-17 · `politica_hash` sem definição de canonicalização.** *FATO.* Hash dos bytes do YAML muda com espaço em branco e reordenação de chaves, produzindo falsa diferença de política. *Correção:* hash da serialização canônica do conteúdo já parseado e validado por Pydantic.

**E-18 · `fii_informe` em EAV sem camada tipada.** *INFERÊNCIA.* Formato longo é escolha defensável para ~60 colunas voláteis, mas transfere a tipagem para o consumidor. Sem uma view tipada por cima, todo consumidor reimplementa a conversão e diverge. *Correção:* views tipadas em Gold, uma por informe.

**E-19 · Nomenclatura mista e `models/` ambíguo.** *FATO, severidade baixa.* O modelo mistura português (`fato_contabil`, `conta_contabil`) e inglês (`Revenue`, `Net Income`, `FCF`). E a estrutura proposta usa `src/models/` para schemas Pydantic enquanto dbt chama de models os arquivos SQL — colisão garantida de vocabulário num projeto que vai durar anos. Além disso, a política (P3) não tem casa na árvore proposta. *Correção:* uma língua para identificadores de banco; `src/schemas/` para Pydantic; `src/policy/` para carga e validação do YAML.

### 5.5 A prática de engenharia mais importante para este contexto

*OPINIÃO.* Dadas 3 a 4 horas efetivas semanais, fragmentadas, a propriedade de maior valor não é arquitetura — é **retomabilidade**. Concretamente, três coisas valem mais que qualquer escolha de tecnologia:

1. Um `Makefile` com alvos que reconstroem tudo a partir de Bronze com um comando. Se retomar exige lembrar sete passos, o projeto morre na terceira interrupção.
2. Um README que responde "como eu rodo isso" em cinco linhas, escrito no primeiro dia e atualizado a cada quebra.
3. Commit por tarefa, com mensagem que diz o porquê. É o único registro de progresso que não diverge, porque é gerado pelo próprio trabalho — motivo pelo qual os cinco arquivos de gestão propostos no guia devem colapsar para dois (contexto durável + `DECISIONS.md` append-only).

---

## 6. Riscos

| ID | Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|---|
| R-01 | **O artefato substitui a ação.** Oito anos acompanhando o método sem conta aberta; agora um projeto de 200–400 h que precisa terminar antes de qualquer decisão. Cada fase fornece razão legítima para ainda não ser hora | Alta | Alto | Definir por escrito, com data, um evento externo que **não** depende de nenhuma fase estar pronta. Se depender, a mitigação é nula |
| R-02 | Escopo explode e o projeto morre na fase de infraestrutura | Alta | Alto | Escopo reduzido da §7; nada avança sem entregável utilizável |
| R-03 | Ajuste de série errado corrompe todo o histórico em silêncio | Alta | Alto | C-04, C-06, E-09 e A-14 combinados: forma multiplicativa, oráculo externo, invariante contra índice |
| R-04 | Teto de uso do assistente vira o limite real de ritmo | Alta | Médio | Escrever especificação e testes primeiro consome muito menos cota que iterar em conversa até o código sair certo |
| R-05 | Bitemporalidade mal implementada só aparece na fase de backtest | Média | Alto | Smoke test point-in-time na semana 2 (§8, item 11) |
| R-06 | Overfitting do backtest | Média | Médio | Pré-registro datado antes do código existir, com número máximo de variantes testáveis |
| R-07 | Endpoints da B3 mudam sem aviso | Alta | Médio | Teste de contrato diário (Q-07) + Bronze imutável permite reprocessar |
| R-08 | Deriva de ambiente entre sessões espaçadas | Média | Médio | E-10 (CI) + E-11 (lockfile) |

---

## 7. Escopo revisado e orçamento

**Horas.** ~6 h/semana nominais, fragmentadas, majoritariamente sob atenção dividida. Estimativa efetiva: 3–4 h/semana em tarefas de depuração de dados, que é a natureza das fases 0 e 1. Escopo completo (30–40 semanas a 15 h/semana) ⇒ 18–30 meses neste orçamento: inviável.

**Dentro — 60 a 110 h, 20 a 35 semanas:**

| # | Módulo | Horas |
|---|---|---|
| 1 | Fase 0 — CVM DFP/ITR → Parquet → DuckDB, sete armadilhas tratadas | 20–35 |
| 2 | Fase 1 — COTAHIST, eventos, ponte `codeCVM↔ticker`, ajuste de série | 25–40 |
| 3 | Fase 2 reduzida — indicadores em curva, Lucro × Cotação, página de ativo em Streamlit. Sem score composto até A-05 | 15–25 |
| 4 | Backtest reduzido — ações BR, universo com deslistadas, benchmarks CDI, IBOV TR, 1/n e **100% índice**; janelas de 5 e 10 anos | 15–25 |
| 5 | Estado financeiro — dívidas, reserva em meses, marco de 24 meses. Único módulo que descreve a posição real hoje | 8–16 |

**Fora, com gatilho de reativação:**

| Módulo | Reativa quando |
|---|---|
| Motor de aporte (II.6), Postgres, FastAPI | Existir conta em corretora e primeira posição |
| Módulo de IR, backup do Postgres | Existirem operações no ano-calendário |
| FIIs, renda fixa, exterior, cripto | Existir posição na classe |
| Score composto (II.5) | A-05 resolvido a favor de seleção ativa |
| Gatilho de deriva (Q-13) | Aporte anual < 5% do patrimônio |
| Opções | Mudança declarada, e com as três travas de Q-15 |

**Sobre A-05.** Não decida por argumento. Construa 0, 1 e o backtest reduzido, e faça a primeira pergunta ser: *uma carteira 1/n e uma carteira 100% índice teriam batido a política com score?* Se índice vencer, o score inteiro foi economizado e a resposta foi aprendida em vez de recebida. Se perder, existe uma afirmação falsificável — que é o que o dossiê declara querer.

**Sobre C-10.** No escopo reduzido, só quatro pilares viram parâmetro: 4 (diversificação), 5 (lucro e dívida), 6 (múltiplos) e 11 (ETFs). São os que determinam A-05. Verificar esses quatro contra as fontes primárias — 4 a 8 horas — e marcar os outros nove como não verificados no arquivo de contexto.

---

## 8. Custo por achado

Premissas: horas do cliente como custo de oportunidade; "tardio" é o custo se o defeito só produzir sintoma na fase correspondente; faixas amplas onde a base é fraca.

| Ordem | ID | Agora | Tardio | Premissa |
|---|---|---|---|---|
| 1 | A-05 | 1 dia de decisão | 11–20 semanas de fases construídas para tese que a Parte I contradiz | Assume que núcleo indexado tornaria fases 2 e 4 dispensáveis |
| 2 | A-03 | 4–8 h | Perda integral do backtest; não recuperável sem recoletar | Assume que o parser preencheria com a data de coleta |
| 3 | A-01 | ~2 h | 40–80 h para reescrever Silver e Gold | Assume 3–5 modelos dbt já sobre a regra errada |
| 4 | C-04 | 2–4 h | Série corrompida em silêncio; 3–6 semanas | Detecção só quando nenhum benchmark bater |
| 5 | E-06 | 1 h (regra + teste de CI) | Reprocessamento não reprodutível; a propriedade central perdida sem erro visível | — |
| 6 | E-01 | 2–3 h | Falhas de lock intermitentes na fase 2 | — |
| 7 | A-02 | 30 min | Semanas tentando rodar janelas inexistentes | — |
| 8 | E-02/E-03 | Economia imediata | 2 serviços mantidos por zero função durante todo o projeto | — |
| 9 | A-17 | 1 h de reorçamento | Abandono na fase 4 | Três estimativas independentes convergem |
| 10 | E-04 | 3–5 h | Bronze com partições duplicadas ou republicações perdidas | — |
| 11 | E-09 | 6–10 h | Os erros de escala, sinal e período passam por todos os testes existentes | — |
| 12 | A-13 | 2–4 h | Erro de centavo em apuração; contagem de dias úteis errada | Adiado com o módulo de IR |
| 13 | A-14/B-01 | 6–10 h | Falsa confiança no ajuste de série | — |
| 14 | E-15 | 1 h | Duplicatas silenciosas corrompem o ajuste | — |
| 15 | E-10/E-11 | 1–2 h | Deriva de ambiente entre sessões | — |
| 16 | A-15/B-03 | 4–8 h | Não quantificável. Custo epistêmico: um número que parece prova | — |
| 17 | E-07/E-08 | 4–6 h | Depuração em horas onde seriam minutos | — |
| 18 | E-12 | 1 h | Não quantificável. Exposição de dados pessoais | — |
| 19 | A-18 | 3–5 h | Score ruidoso; efeito não quantificável sem backtest válido | Suspenso com o score |
| 20 | C-01/C-02/C-03 | 15 min | Escolha de ferramenta sobre premissa falsa; magnitude baixa | — |
| — | C-07/C-08 | 2–3 h | Multiplicador: amplifica A-01, A-03, A-04 e A-05 por toda a duração | — |
| — | E-14 | — | Consome 15–30% da capacidade permanentemente, e nenhuma projeção desconta | — |

Os seis primeiros somam **cerca de 15 horas agora** contra algo entre 20 e 45 semanas depois.

---

## 9. Backlog

**Bloco 0 — esta semana, sem código**

1. Pré-registro do backtest: limiar, métrica com bootstrap em blocos, número máximo de variantes testáveis, data. → A-15, B-03
2. Evento externo com data, independente de qualquer fase. → R-01
3. Nomear qual tarefa concreta a "ferramenta" executa hoje. → pendência #11
4. Arquivo de contexto = blueprint **corrigido**, com fases 3–5 marcadas fora de escopo e as regras substituídas marcadas como proibidas. → C-07
5. Verificar os quatro pilares que viram parâmetro. → C-10
6. Decidir a pilha mínima e registrar o que ficou de fora e por quê. → E-02, E-03

**Bloco 1 — fundação, antes da primeira carga**

7. Origem de `dt_disponivel` + enum de procedência. → A-03
8. Silver preserva versões; `max(versao)` como seleção as-of. → A-01
9. Derivação de `dt_deslistagem`; universo com deslistadas. → A-04, B-02
10. Estratégia de concorrência do DuckDB. → E-01
11. Proibição de data corrente em transformação + teste de CI. → E-06
12. `manifesto_coleta` e chave de idempotência. → E-04
13. `run_id` e log estruturado. → E-08
14. `.gitignore`, segredos, e-mail do User-Agent em variável de ambiente. → C-09, E-12
15. Lockfile e versão de Python fixada. → E-11
16. CI mínima: pytest + dbt build sobre fixtures + checagem de E-06. → E-10
17. `Makefile` com alvo de reconstrução total; README de cinco linhas. → §5.5
18. Smoke test point-in-time na semana 2. → A-03, R-05
19. `dt_ex`, calendário de negociação, tipo decimal. → A-13 (parcial)

**Bloco 2 — testes e execução**

20. Casos canônicos em forma multiplicativa, com oráculo externo (Aviso aos Acionistas + arquivo de proventos B3) e invariante de retorno total contra índice; incluir JCP e grupamento com FATCOT. → C-04, C-05, C-06, B-01
21. Fixtures versionadas, golden records, invariantes contábeis. → E-09
22. Harness por invariante interna no lugar de Yahoo/brapi. → A-14
23. Unicidade explícita em `cotacao` e `evento_corp`. → E-15
24. `on_schema_change` e leitura de Parquet por nome. → E-05
25. `fonte_status` e contrato de staleness; decisão monetária não degrada, interrompe. → E-07
26. Execução das cinco entregas da §7.

**Suspensos com seus módulos:** A-06, A-07, A-08, A-09, A-11, A-12, A-16, A-18, A-19, B-04, B-05, B-08, E-13, E-16, E-17, E-18.

---

## 10. Independência e conflitos

**Respostas do cliente, 31/08/2026.** Nunca foi assinante do Bastter Blue; acompanhou o método entre 2010 e 2018. Nunca teve conta moderada, suspensa ou banida; nunca foi ativo na comunidade. Sem interesse comercial no sistema em momento inicial. Sem posição em ativo ou fornecedor citado. Sem relação pessoal ou profissional com nomeados. Não pretende publicar a Parte I.

**Efeito.** Nenhum conflito material. A ausência de atrito com a comunidade neutraliza a hipótese de que a Parte I seja motivada por ressentimento. A não publicação suspende as exposições regulatórias de redistribuição de dados da B3 e de cláusula share-alike da ODbL.

**Exposição registrada, não conflito.** Oito anos de acompanhamento são enquadramento. O risco correspondente não é defender o método — é que suas categorias permaneçam como estrutura depois de os pilares serem contraditados. A-05 é exatamente esse padrão, e isso reforça sua prioridade.

**Conflito estrutural do auditor.** Sou um sistema de IA. O objeto auditado — e explicitamente os três guias — apresenta características de produção assistida ou gerada por sistema da mesma classe. Audito artefatos possivelmente produzidos pelo mesmo tipo de processo que me produz. Duas consequências concretas: a Parte I foi excluída do escopo em vez de validada, porque validá-la com o mesmo tipo de sistema que a escreveu não é verificação; e o achado C-10 existe porque um dos guias afirma que o cliente é o especialista de domínio, quando o domínio já havia sido terceirizado. Sem interesse financeiro, sem remuneração de qualquer parte, sem relação com a Bastter.com ou fornecedores citados.

---

## 11. Limites do parecer e reauditoria

Parecer de engenharia de software e consistência documental. **Não é recomendação de compra, venda, manutenção ou alocação de qualquer ativo**, e nenhum trecho deve ser lido como tal. Não avalio o mérito financeiro do método Bastter nem de qualquer política descrita no dossiê. Não sou advogado, contador nem consultor de investimentos; as regras tributárias citadas não foram verificadas e exigem profissional habilitado antes de virarem código — em especial o custo de aquisição sob eventos societários.

| Elemento | Gatilho de reauditoria |
|---|---|
| Todo o pacote | Abertura de conta em corretora — devolve dois terços do escopo ao jogo |
| §10 | Surgimento de interesse comercial ou decisão de publicar a Parte I |
| §7 | Primeiro aporte ou mudança material de patrimônio |
| Prazo (A-17) | Fim da fase 0: medir horas reais e recalibrar com o fator observado |
| A-05 | Primeiro resultado do backtest reduzido |
| R-01 | Data do evento externo do item 2 do backlog |
| Fatos de produto (C-01 a C-03) | 30–60 dias, ou qualquer mudança de plano, superfície ou preço |
| Endpoints B3 (II.4) | 90 dias, ou primeiro alerta do teste de contrato |
| Pré-registro do backtest | Não expira. Alterá-lo depois de ver o resultado anula o instrumento |
| Exposições regulatórias | Suspensas. Reativam com publicação ou compartilhamento |

---

## 12. Pendências

**Fechadas:** as seis perguntas de conflito de interesse; os sete inputs de perfil.

**Abertas — localização pendente**

| # | Item | Sustenta |
|---|---|---|
| 1 | Definição de FATCOT no layout oficial da série histórica da B3 | B-01 |
| 2 | Campos de situação e data no cadastro CVM, e correspondência com saída de negociação na B3 | B-02 |
| 6 | Comportamento de escrita concorrente do DuckDB nas versões atuais | E-01 |
| 7 | **Política de sobrescrita dos arquivos anuais da CVM** — se versões anteriores são recuperáveis. Determina se o req. 3 de II.8 é exequível retroativamente. Maior impacto da lista | A-01, II.8 |
| 8 | Quatro referências acadêmicas (pilares 4, 5, 6, 11): DOI, ano, e verificação de que o número citado consta do texto | A-05, C-10 |
| 9 | Página primária da Anthropic sobre Cowork | C-01 |
| 10 | Documento anterior à segunda auditoria (suas seções 1, 2, 5, 8, 21, 23) | B-06 |

**Suspensas:** #3 (regra de distribuição de FII), #4 e #5 (termos da B3 e share-alike ODbL).

**Aberta — só o cliente responde**

11. **Qual tarefa concreta a "ferramenta" executa hoje?** Sem carteira, sem operações e sem aporte, a resposta determina se o escopo da §7 acerta o alvo. A leitura mais provável é *estudar empresas* — uma enciclopédia consultável — e não gerir posição; se for isso, a §7 atende integralmente. Se for outra coisa, precisa ser nomeada, porque muda o alvo.

---

## 13. Conformidade do próprio pacote

Dos quatro critérios de aceite: condição de falsificação declarada para todo veredito — **atendido**; nenhuma citação, DOI ou página inventada — **atendido**; o cliente reordena o roadmap só com a §8 — **atendido**; "um terceiro abre as fontes e chega ao mesmo veredito" — **atendido nos achados A-xx e na maioria dos E-xx** (o dossiê é a própria fonte, reproduzíveis por leitura) e **não atendido** nos achados B-xx, C-xx e nos que dependem das sete pendências abertas.

Registro como falha conhecida, não como ressalva de rodapé.

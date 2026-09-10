# Pendências

Registro único e vivo. Atualizado a cada sessão, **antes** de encerrar.
Regra da casa: pendência sem dono e sem gatilho não é pendência, é desabafo.

**Estado em 06/09/2026 (2ª sessão do dia) · política 1.17.0 · custos 2.1 · perfil 1.0 · catálogo 1.0 · 269 testes**

**Classes:** 34 `BLOQUEIA_O_SISTEMA` · 10 `DECISAO_DE_DESENHO` · 2 `DADO_DE_UM_USUARIO`
(P-55 fechada no mesmo dia; P-57 a P-67 abertas)

---


## Achado U-01 — o roteiro misturava o sistema com a carteira de uma pessoa

**Correção do Osvaldo, 06/09/2026:**

> *"eu não ter reserva ou aporte ser uma barreira de desenvolvimento me parece estranho.
> imagina que fosse uma ferramenta para ser vendida: eu não teria informações sobre o
> aporte e a reserva do cliente porque ele não existiria. então o sistema tem que
> existir e funcionar independente do input do usuário."*

Ele está certo, e **o sistema já funciona** — `test_usuario_novo.py` mede: patrimônio
zero, nada assinado, nada registrado, e a resposta vem completa e acionável (*"R$800/mês
para o Tesouro Reserva até R$10 mil, depois RDB; 23 meses até o alvo"*). Com a reserva
pronta, sai uma carteira de 7 rotas sem nada assinado.

**O defeito era do ROTEIRO, não do motor.** Eu vinha listando "aporte realizado = zero"
e "as duas teses não assinadas" como bloqueios de desenvolvimento. Não são: são o estado
de **um** usuário.

É o achado **L-01 num nível acima**. A L-01 separou `politica.yaml` (motor) de
`perfil.yaml` (usuário) na *configuração*. O *plano* nunca recebeu essa separação — e
por isso o caminho crítico tinha, no meio dele, coisas que só dizem respeito à carteira
do Osvaldo.

### As três classes, e a proporção é o achado

| classe | quantas | o que significa |
|---|---|---|
| **BLOQUEIA_O_SISTEMA** | 34 | o sistema não faz o trabalho dele. Prioridade real. |
| **DECISAO_DE_DESENHO** | 10 | precisa de *um* humano decidindo sobre o sistema — qualquer dono de produto responderia |
| **DADO_DE_UM_USUARIO** | **2** | P-01 e P-02. **Nunca** são bloqueio de desenvolvimento |

**Só duas de 46 são dado seu, e eu pus as duas no caminho crítico.** Toda pendência
nova nasce com a classe declarada; sem ela, não dá para saber se está no caminho
crítico ou na lista de outra pessoa.

---

> **As pendências fechadas migraram para `ACHADOS.md` em 06/09/2026.** Eram 39% deste
> arquivo — ~4 mil tokens de história de coisa já resolvida, relidos toda sessão. A
> tabela `## Fechadas` no fim continua aqui, porque ela é o que impede uma sessão nova
> de reabrir tarefa pronta; o que saiu foi a narrativa longa de cada uma.

---

## P-44 · O próximo passo não pode ser de engenharia duas vezes seguidas

**Regra de processo, criada em 06/09 depois de medir o próprio ritmo.** Sete rodadas
seguidas de qualidade de engenharia, zero de propósito — e **eu propus todas**, uma no
fim de cada resposta.

É o M-01 aplicado a nós: trocar o destino do aporte move 3 meses, trocar o valor move
33, e o sistema trabalhava na alavanca de 3. **A alavanca da engenharia move 0.**
Nenhum teste aproxima a reserva de existir.

Se a sessão anterior fechou uma pendência de engenharia, a próxima proposta é de
**produto, dado, ou uma pergunta a você**. Engenharia entra quando **destrava** algo.

---

## P-45 · Migrar o trabalho de repositório para o Claude Code — **decisão sua**

O plano Pro inclui Claude Code no terminal, com **limite compartilhado** com o app. O
ritual de zip que fazemos toda sessão existe **só** porque seu computador fica
desligado; no Claude Code o arquivo é editado onde mora, e `git commit` é direto.

**A divisão proposta:** Claude Code para refatoração, teste, lint e git; este ambiente
para pesquisa, download da CVM/B3 e processamento pesado — que é do que a Fase 0
precisa.

**Gatilho:** terça, depois do push. Não antes — o primeiro passo é ter o repositório
no GitHub.

---

## P-46 · Usar subagentes na leitura de fonte primária

Ler os 32 arquivos de `docs/fontes` custou o texto **inteiro** de cada um dentro do
contexto. Um subagente lê e devolve só a conclusão.

Para a Fase 0 deixa de ser detalhe: os layouts da CVM e do COTAHIST têm centenas de
páginas. **Um subagente por documento** é a diferença entre caber e não caber.

**Gatilho:** a primeira sessão da Fase 0.

---

## P-01 · Assinatura dos dois registros · `DADO_DE_UM_USUARIO`

Os dois rascunhos estão prontos em `alocacao/teses.yaml` e passam em todas as
verificações de conteúdo. Faltam três edições, e nenhuma delas eu posso fazer.

**HASH11** — apagar `exemplo: true` e colar `impressao: 31a31607f3c60e62`.
**Tesouro IPCA+** — apagar `exemplo: true`, trocar `C06_reconhecimento` para `true`
e colar `impressao: 942c75bae248327b`.

> Antes de assinar o HASH11, responda a pergunta anterior: **você quer a posição?**
> Ela reprova ou é inaplicável em todos os portões do catálogo buy & hold, custa
> 1,30% a.a. e a perda máxima aceita é 100%. "Não compro" é uma resolução completa
> e custa zero. Assinar o rascunho porque ele está pronto é o erro que o
> pré-registro existe para impedir.

**Gatilho:** nenhum. Depende só de você decidir.

> **Não bloqueia desenvolvimento** (U-01). O sistema aloca sem nenhuma tese assinada —
> as rotas que exigem registro viram pendência com o motivo escrito, e as outras
> recebem peso. Isto bloqueia **a sua carteira**, não o projeto.

---

## P-02 · Aporte realizado · `DADO_DE_UM_USUARIO`

Piso planejado R$500/mês; realizado hoje **zero**. É o único número do projeto que
nenhuma linha de código substitui. Enquanto for zero, a data da reserva completa
(**~mai/2031**, recalculada em 05/09) é projeção de um aporte que não começou.

E o achado M-01 põe isto em escala: o aporte é a alavanca de **33 meses**; o destino,
onde o sistema inteiro trabalha hoje, é a de **3**.

> **Não bloqueia desenvolvimento** (U-01). Um cliente novo de um produto tem aporte
> zero, e o sistema responde. `test_usuario_novo.py` garante isso.

---

## P-04 · `b3.quem_paga_custodia` fura a P1 — **decisão sua**

É `NAO_CONFIRMADO` e **não declara `bloqueia` nada**, ao contrário das outras
quatro. Insumo não confirmado que nenhum cálculo recusa não está protegido: não
bloqueia porque ninguém o lê, e se um dia alguém ler, lerá `None`.

Ou ele bloqueia algo e precisa dizer o quê, ou sai do `custos.yaml`.

---

## P-05 · Quatro `NAO_CONFIRMADO` esperando download

| chave | bloqueia | o que fecha |
|---|---|---|
| `etf.BOVV11` | `tabela_etf_rv_completa` | site do gestor bloqueia robô — visita manual |
| ~~`etf.IMAB11`~~ | **fechada 05/09** — 0,25% a.a. (página do gestor, PARCIAL). Falta o regulamento para virar COMPLETO |
| `etf.ACWI11` | `comparacao_global_amplo` | regulamento / página do produto |
| `exterior.vest_stablecoin.iof` | `ordenacao_rotas_exterior` | tratamento de IOF em stablecoin |

O `IMAB11` é o mais valioso: é o único concorrente conhecido do Tesouro IPCA+ na
função `PROTECAO_REAL` que não paga a custódia de 0,20% a.a. da B3.

---

## P-06 · `Fonte: NAO_REGISTRADA` no layout do COTAHIST

O `SeriesHistoricas_Layout.md` não registra de onde veio o PDF. Pesa porque o
achado central daquele arquivo é que as tabelas anexas da **revisão 02 (05/10/2020)**
estão desatualizadas — `TPMERC=021` e seis `CODBDI` aparecem em 2023 e não constam.
Sem a URL não dá para checar se existe revisão 03.

**Gatilho:** antes de escrever o parser do COTAHIST.

---

## P-08 · Constantes vencendo — macro renovadas em 05/09

`cdi_aa` e `selic_aa` reconferidos na API do BCB: **13,90%** (SGS 4389, 03/09) e meta
**14,00%** (SGS 432). **Os dois valores estavam certos** — era prazo vencido, não número
errado. Novo `expira`: 04/12/2026. Falta `poupanca_am`, que vence em 28/09.

| constante | `expira` |
|---|---|
| `macro.cdi_aa` | **04/09/2026 — já venceu** |
| `macro.selic_aa` | 07/09/2026 |
| `macro.poupanca_am` | 28/09/2026 |
| tarifas B3 e Tesouro (9) | 04/12/2026 |
| tabelas comerciais (11) | 04/12/2026 |
| taxas de fundo (19) | 05/09/2027 |

`motor.val()` avisa em stderr quando passa da data. Leis usam `expira: null` +
`revisar_se`, porque lei não vence no aniversário.

---

## P-09 · Fase 0 virou o único caminho — **prioridade máxima**

Depois de H1/H3 (05/09), os três testes pré-registrados terminam no mesmo lugar:

- **H1 (valor)** — o alfa medido é de um long-short cuja perna vendida não existe
  para pessoa física. O NEFIN publica só o spread, nunca as pernas. Medir a carteira
  investível exige montar os tercis a partir do dado de ação.
- **H2 (dividendo)** — não há fator de DY na série. A carteira precisa ser montada.
- **H3 (tamanho)** — fechada, e fechada sem precisar da Fase 0.

Dois de três terminam nela. Somado ao prazo que já existia (a CVM sobrescreve os
arquivos anuais e `dt_disponivel` não se reconstrói), a Fase 0 deixou de ser "a maior
peça restante" e passou a ser **a única que destrava alguma coisa**.

**Gatilho:** próxima sessão no desktop.

---

## P-10 · `alfa_contra_fatores()` tem uma armadilha viva

Ela **subtrai o Risk_Free**, porque foi escrita para carteira comprada. Aplicada a um
fator long-short, troca o alfa do HML de +0,766% (t=+2,94) para −0,178% (t=−0,68):
inverte sinal e veredito, sem levantar erro.

Hoje há um teste que prende a diferença, e o `backtest_h1_h3.py` não a usa. Mas a
função continua com o nome que convida ao erro.

**Duas saídas:** renomear para `alfa_de_carteira_contra_fatores()`, ou aceitar um
parâmetro `auto_financiado=False` que dispensa a subtração.
**Gatilho:** antes de escrever a próxima estratégia do pré-registro.

---

## P-20 · Opções voltaram a ser pendência, não exclusão

Correção dele em 05/09: *"quando você me perguntou se operava opções eu disse que não,
mas além do meu cofrinho no PicPay eu não opero mais nada — isso não foi uma
autorização de exclusão."*

Ele está certo, e a falha é a mesma do banco com outra roupa: converti resposta
factual em decisão de escopo. Numa carteira vazia, "não opero X" é verdade para todo
X. `opcoes` perdeu o `fundamento` e voltou a ser pendência.

**O que falta é régua, e há um problema real de modelagem:** opção tem propriedades que
o catálogo não representa. No lançamento a descoberto a **perda pode exceder o capital
aplicado**, e a escala `perda_maxima` não tem degrau acima de `total`. E a posição tem
vencimento próprio, que interage com o teto de 10 anos.

**Gatilho:** nenhum urgente — ele não opera hoje. Mas a exclusão saiu do arquivo.

---

## P-27 · Separação motor/usuário ainda é parcial

Achado L-01. `compromissos` e `decisoes` foram para `perfil.yaml`; a fusão é na carga,
então nenhum consumidor mudou. **Quatro seções continuam mistas por dentro:**

- `corretora` — metodologia do ranking junto com os **pesos** que você escolheu
- `aporte_extraordinario` — regra junto com o seu padrão de bônus
- `sleeves`
- `custos.yaml → cofrinho` — termos de um produto de mercado junto com o estado da
  **sua** conta

Dividi-las exige decidir a granularidade, e isso é desenho, não arrumação.

**Gatilho:** antes de existir um segundo usuário — não antes disso.

---

## P-28 · `revisao` está declarada e nunca é lida — **o guarda foi consertado, a dívida não**

Nenhum `.py` referencia a seção `revisao` do `politica.yaml`. Ou vira comportamento
(cadência de revisão implementada), ou sai do arquivo.

**Em 05/09 o defeito de fundo foi fechado.** O `test_cobertura_yaml` varria **seis** das
dezenove seções lendo **três** dos onze módulos — media o próprio escopo, não a
cobertura. Foi por esse vão que `revisao` entrou e ficou. Agora são quatro testes:
toda seção precisa de um **regime declarado com motivo escrito** (`OPERACIONAL`,
`REGISTRO`, `ESPECIFICAÇÃO`), seção nova sem regime **quebra a suíte**, e a dívida
conhecida vive num inventário que **não pode apodrecer** — entrada já paga ou de chave
removida faz o teste falhar.

As três chaves de `revisao` continuam na dívida. O que mudou é que agora elas são
contadas, e o próximo `revisao` não tem por onde entrar.

---

## P-29 · `estrategias_pre_registradas` — o pré-registro não é lido pelo motor

121 chaves. Nenhum módulo do motor as referencia; quem lê são os testes e o
`backtest_h1_h3.py`. É defensável — o pré-registro descreve o que **será testado**, não
o que o alocador faz hoje. Mas até que o backtest completo exista, é uma especificação,
e especificação sem número some.

---

## P-30 · `bloco_C_solvencia` — especificado em 05/09, nenhum módulo aplica

48 chaves escritas na mesma sessão em que a régua de solvência foi desenhada. Só
`test_alocacao.py` as menciona: os testes verificam que o **texto** existe, não que
algum comportamento derive dele. A régua de banco (P-16) depende dela.

---

## P-31 · `regime_instituicao_financeira` — mesma situação, 46 chaves

Nasceu da sua correção sobre bancos: *"não faz o menor sentido excluir Itaú e Bradesco
— não deve ser excluído, deve ser encontrado o critério"*. O critério foi **escrito**.
Ele ainda não **roda**.

---

## P-32 · O que sobrou de prosa na seção `corretora`

Depois do achado N-01, três regras saíram do Python e foram para o YAML. Restam
declarações sem consequência: `promocional` (peso negativo para promoção — argumento
escrito, nunca aplicado), `cobertura_e_penalidade` e `nota_cobertura` (o código
implementa a penalidade por dimensão ausente, mas com números próprios) e
`fora_do_ranking`.

---

## P-34 · `sleeves` — seis chaves que o `sleeve.py` não lê

`exige_selecao`, `n_ativos_efetivo`, `bloqueado_por`, `meses_para_montar`. O
`bloqueado_por: A05_nucleo_indexado_vs_selecao_ativa` é o mais grave: ele afirma que a
sleeve de seleção ativa está **travada por uma decisão em aberto**, e nada a trava.

---

| item | valor |
|---|---|
| depositado | R$ 7.671,01 |
| limite extra obtido | R$ 530,00 |
| razão | **14,5 para 1** — 6,9% vira limite |

Ou o vínculo tem teto, ou a maior parte do saldo está parada sem comprar limite nenhum.
**A pergunta:** com quanto de depósito você mantém o limite de que precisa? Se R$1.000
bastarem, sobram R$6.671 livres — e aí eles têm destino, que é constituir a reserva que
hoje é zero.

---

| saldo | ganho extra a.a. | mensalidade a.a. | saldo liquido |
|---|---|---|---|
| R$ 7.671 | R$ 162,07 | R$ 287,88 | **−R$ 125,81** |
| R$ 10.000 *(teto)* | R$ 211,28 | R$ 287,88 | **−R$ 76,60** |
| R$ 13.625 | R$ 287,87 | R$ 287,88 | R$ 0,00 *(empate)* |

**O empate está 1,4× acima do teto do produto.** Pagando a mensalidade, o Turbinado
nunca se paga. Só vale com a isenção — e a isenção é mensal.

As duas condições escritas: **R$20 mil investidos** para liberar um produto que aceita
no máximo R$10 mil; ou **R$2.500 em 3 meses no cartão**, que só é grátis se você
gastaria isso de qualquer forma. Induzir R$100/mês de gasto extra custa R$1.200/ano
para economizar R$287,88.

### As duas perguntas que sobraram — **só você**

1. **O que exatamente te isenta hoje, e isso se repete todo mês?** A tela diz "Tarefas
   concluídas — ativo **este mês**", o que sugere requalificação mensal e não status
   permanente. Se depender de tarefa mensal, é um custo de atenção recorrente que a
   conta acima não captura.
2. **O saldo do cofrinho do cartão pode migrar para o Turbinado, ou está preso
   enquanto garantir o limite?** Se estiver preso, a decisão passa a ser sobre o
   **aporte novo**, não sobre os R$7.671.

Com a isenção valendo, o Turbinado rende **13,88% a.a. líquido** contra 11,70% do
cofrinho atual — **R$167,14/ano** sobre o saldo de hoje, e com liquidez.

---

## P-25 · Reserva e dívida não são independentes — **estrutural**

Achado J-02, e é o mais sério do dia. O cofrinho garante a **fatura do cartão**. Sua
reserva de emergência é colateral de uma dívida de **consumo sua**.

No cenário para o qual a reserva existe — perda do contrato único, com estabilidade de
renda medida como **baixa, 6 de 6** — você teria ao mesmo tempo: renda zero, fatura
aberta, e a reserva empenhada nessa fatura. **Ela não fica só indisponível: é consumida
pela dívida que a prendia.**

Iliquidez atrasa o acesso. Colateral destrói o ativo no cenário em que ele deveria ser
usado — reserva com correlação −1 com a própria necessidade.

O G1 (dívida) e o G2 (reserva) rodam em sequência como se os dois lados fossem
independentes. Neste arranjo não são: é o mesmo dinheiro contado duas vezes, uma como
segurança e outra como limite de gasto.

**Efeito no motor hoje: zero** — `reserva_disponivel: 0.00` já zera a contagem por
outro caminho. Mas o motivo registrado dizia "iliquidez" quando o problema é
"colateral", e a distinção decide o remédio.

---

## P-35 · A reserva é um número e o mundo tem baldes — **consequência do P-24**

Com teto por produto, "quanto há de reserva" deixou de bastar: para saber se a próxima
parcela cabe é preciso saber **onde** ela está. `Estado.reserva_por_rota` foi criado e é
**opcional**. Quando ausente, o G2 avisa que não sabe em vez de supor que a reserva foi
construída na ordem do plano.

**Hoje não morde** — a reserva é zero e o `estado.yaml` declara `reserva_por_rota: {}`,
que *afirma* que não há reserva em lugar nenhum, diferente de omitir a chave. Morde a
partir do primeiro depósito, e o viés aponta para **recomendar demais** a rota melhor.

---

## P-22 · Opções: duas famílias, não uma

Contexto que ele trouxe em 05/09 — no Bastter, opções e **aluguel de ações** eram
apresentados como forma de *rentabilizar* a carteira, não como aposta direcional.
Isso resolve metade do problema de modelagem da P-20.

**Coberta** (call sobre ação que já se tem; aluguel de ação detida): perda máxima é
custo de oportunidade acima do strike, mais risco de contraparte. Cabe em
`perda_maxima: limitada` — **o catálogo já representa.** Falta pesquisa de custo, e
o `Tarifacao_Equities_V5.0` item 1.3.1.4 (exercício de opções) já está em `docs/fontes`.

**Descoberta:** perda pode exceder o capital aplicado, e a escala não tem degrau
acima de `total`. Essa continua irrepresentável.

A exclusão genérica de "opções" era grossa demais: juntava duas coisas com perfis de
perda opostos.

---

## P-23 · Método Mille pré-registrado, com a crítica antes do teste

Mille é João Bosco Oliveira Junior, coautor do Bastter — **mesma casa**, não fonte
independente. Quatro pilares: governança, produtividade, geração de caixa,
endividamento. Dois cortes numéricos: **margem líquida > 20%** e FCL Capex não
negativo por muito tempo.

**Crítica registrada antes de rodar:** margem líquida acima de 20% é **filtro
setorial disfarçado de filtro de qualidade**. Banco, software e concessionária têm
margem estruturalmente alta; varejo, distribuição e construção têm baixa — e nenhuma
das duas coisas fala da administração. Se rodar, tem de ser com controle setorial.

**Três dos quatro pilares saem da CVM.** Governança não: "ligar para o RI" não vira
coluna. Quem rodar só os pilares 2–4 está rodando três quartos do método, e o
registro diz isso em vez de fingir cobertura.

---

---

## P-19 · Imóvel direto foi excluído por argumento geral, sem medição

Achado ao escrever a P6. A entrada `imovel_consorcio_COE_previdencia_sem_match` dizia
"fora por custo e iliquidez; **não avaliados individualmente**" — e essa segunda metade
não é fundamento legítimo.

Consórcio e COE têm custo estruturalmente alto e documentado, o que sustenta a exclusão
por `CRITERIO_MEDIDO`. "Previdência sem match" está resolvida por outro caminho (ele é
PJ e não tem previdência). **Imóvel direto é o elo fraco:** excluído por argumento
geral, sem medição.

**Gatilho:** nenhum urgente — ele não tem capital para imóvel na Fase A. Mas a exclusão
precisa de régua ou de reclassificação para pendência.

---

---

## P-17 · C-04 e C-05 não foram lidos — ⚙ **exige o desktop**

O regime do bloco C está escrito, mas a lista de campos vive em
`auditoria/escopo-campos-de-analise.md`, na sua máquina, e a ponte estava fora do ar.
C-01 a C-03 são conhecidos por referência cruzada dentro do próprio `politica.yaml`;
**C-04 e C-05 são citados como existentes e nunca nomeados ali.**

Não inventei os dois. Um bloco de exclusão com critério inventado excluiria empresa
por regra que ninguém escolheu — pior que bloco nenhum.

**Gatilho:** primeira sessão de desktop. Ler o arquivo e reconciliar.

---

## P-18 · `SETOR_ATIV` da CVM não foi contado

O bloco C recusa instituição financeira, e a identificação sai do campo `SETOR_ATIV`
do cadastro da CVM. O campo foi conferido, mas **só dois valores foram vistos** — a
enumeração nunca foi contada no dado real, como foi feito com `ORDEM_EXERC` e
`ESCALA_MOEDA`. Sem isso o corte automático não pode ser codificado.

**Gatilho:** antes de codificar a recusa. ⚙ exige o desktop.

---

## P-12 · `DATADO` cobra liquidez onde deveria cobrar vencimento — **decisão sua**

Achado H-01, ao catalogar LCI/LCA. A função `DATADO` exige `exige_liquidez_dias: 30`.
Isso trata um problema de **duração** com critério de **liquidez**.

Simulei a chegada da carência sem tocar no YAML: com 270 dias a rota perde **todas**
as funções; com 90, idem; com 30, só sobra `DATADO`. Uma LCI isenta de IR, coberta
pelo FGC e que **vence exatamente na data do objetivo** seria eliminada por uma
iliquidez que o objetivo não precisa.

A regra correta seria "vence até a data do objetivo **ou** é líquida em 30 dias" — o
mesmo padrão que o G8/CARREGO já usa para `PROTECAO_REAL`. Não mudei porque afrouxar
`exige_liquidez_dias` sozinho deixa entrar também coisa ilíquida que não vence em data
nenhuma; a mudança precisa vir com o casamento de vencimento junto.

**Efeito hoje: zero** — LCI/LCA estão bloqueadas no G5 e o G6 nem as vê. Morde no dia
em que a carência for confirmada. Há um teste que falha se alguém mexer no `DATADO`
sem atualizar este registro.

---

## P-43 · Há um TERCEIRO catálogo — achado T-01

`motor.montar_rotas` é paralelo ao `catalogo.yaml`: **22 rotas contra 25, com 13 nomes
que só existem lá**. A P-36 disse "os dois catálogos" e havia três. Nenhum módulo de
produção o chama — só o `test_motor.py`.

O ruff viu uma **variável** morta; o defeito era a **chamada**: `B3V = val(...)` era
cópia da função de baixo, e a chamada **abortaria** se o valor fosse `NAO_CONFIRMADO`,
dentro de uma função que promete *"capturar InsumoBloqueado como marcador em vez de
abortar"*. A linha saiu.

**O catálogo não foi apagado, e a decisão é sua.** Apagar código com teste próprio sem
medir o que os testes guardam é como se perde uma rede. As opções:

| | consequência |
|---|---|
| apagar `montar_rotas` + os testes dele | some a cobertura de K-06 e K-07 — precisa medir se `test_alocacao` já cobre |
| migrá-lo para YAML também | ele vira o catálogo da **camada de custo**, com procedência, e passa a poder discordar visivelmente do de alocação |
| deixar e declarar | duas fontes de verdade sobre os mesmos custos, sem nada as confrontando |

**Recomendo a segunda**, com um teste que confronte os dois onde eles se sobrepõem —
mas é decisão sua, e não é urgente.

---

## P-41 · Carregamento de YAML domina o custo multiusuário

`carregar_politica()` custa **82 ms** e `carregar()` **42 ms**, contra 2,75 ms do motor.
Para um usuário é irrelevante. Para N usuários × M chamadas, 124 ms de parse por chamada
domina tudo.

**Deliberadamente não feito.** Otimizar agora seria para um cenário que não existe — e o
S-02 é a prova de que cache mal dimensionado custa correção, não só tempo.
**Gatilho:** o segundo usuário.

---

## P-42 · O catálogo é quadrático em número de rotas

| rotas | `alocar()` |
|---|---|
| 25 | 12 ms |
| 400 | 728 ms |
| 800 | 2.810 ms |

Quatro `next(v[0] for v in vivos if v[0].id == rid)` dentro de laços sobre `pesos`.
**Limitado por desenho:** rota é um *tipo* de caminho, não um papel — ação individual é
uma sleeve dentro de `acao_zero`. Barato de consertar, não é o gargalo.
**Gatilho:** se o catálogo passar de ~100 rotas.

---

## P-47 · Eventos societários da B3 — o insumo que faltava no plano inteiro

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo (rodar) + Claude (processar).
**Gatilho:** terça, 08/09 — antes de qualquer download da CVM.

Sem proventos, desdobramento, grupamento e bonificação, **uma série de preços não serve
para backtest**. A PETR desdobrou 100:1 em 25/04/2008 — confirmado em primeira mão no
endpoint da B3, com `factor: 100,00000000000` e `lastDatePrior: 25/04/2008`. O preço cai
99% num dia. COTAHIST cru lê isso como um crash de 99%.

**Não havia uma linha sobre isso em lugar nenhum do plano.** O blueprint listava COTAHIST
e CVM e parava aí. Um backtest rodado sobre esse acervo teria produzido números e eles
teriam parecido plausíveis.

A fonte existe, é gratuita e é programática, mas **não é documentada**:
`sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedSupplementCompany/{base64}`.
Sem contrato, sem SLA, sem espelho conhecido. Por isso **vem antes da CVM**: DFP/ITR são
ZIP estático em portal oficial; isto pode sumir sem aviso.

`fase0/coletar_b3.py` está escrito, compila e teve a lógica testada (a rede não — ver
P-49). Ele grava snapshot datado imutável, com sha256 e manifesto JSONL.

**A armadilha embutida, e ela é o F-02 de novo:** a chave é texto, e chave errada devolve
HTTP 200 com listas vazias, **em silêncio**. Gravar isso como "empresa sem eventos" é
escrever ausência de dado no lugar de dado. O coletor acusa em voz alta; o parser, quando
existir, precisa recusar.

---

## P-48 · Viés de sobrevivência na composição de índice — declarado, não resolvido

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de rodar o backtest.

A carteira teórica do Ibovespa só existe publicamente **para o dia corrente**. O primeiro
snapshot do projeto foi capturado em 06/09/2026 (76 ativos, referência B3 08/09/26, lista
em `docs/fontes/pesquisa-bases-e-apis-2026-09.md`). O histórico de composição não é
publicado por ninguém, de graça.

Um backtest 1998–2026 que use a carteira de hoje **compra empresas que só entraram no
índice depois de darem certo**. Isso não se conserta coletando daqui para frente — só se
declara. Vai para `politica.yaml → limitacoes_declaradas` com a direção do viés
(otimista) e a condição em que deixa de importar (quando houver ≥1 ciclo de
rebalanceamento capturado, ou seja, ~2027).

Mesma família: **backtest anterior a 2026 é reconstrução, não observação.** O acervo
ponto-no-tempo começa no primeiro dia de captura. Isto também é limitação declarada, e é
a mais importante das duas.

---

## P-49 · `coletar_b3.py` nunca tocou a rede — e não pode tocar daqui

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo. **Gatilho:** terça, primeira coisa.

O script compila e a lógica pura foi testada (montagem do base64, derivação
`PETR4 → PETR`, recusa de sobrescrita). **O caminho de rede não rodou**, porque a máquina
de download é a dele — ver a correção da §11.2 do CLAUDE.md.

O que precisa ser conferido no primeiro uso:
- se `BPAC11 → BPAC`, `KLBN11 → KLBN`, `IGTI11 → IGTI` são de fato os códigos de
  emissora que o endpoint aceita. **Só `PETR` foi confirmado.** Unit e BDR podem ter
  outra regra, e a falha é silenciosa;
- se as 76 emissoras respondem, ou quantas voltam sem `tradingName`;
- se a pausa de 1,2 s é suficiente para não tomar bloqueio.

```powershell
cd C:\...astter
python fase0\coletar_b3.py --indice IBOV
python fase0\coletar_b3.py --eventos          # usa a carteira recém-capturada
```

---

## P-50 · P-05 estava mal formulada — não é número ausente, é campo errado

**Classe:** `BLOQUEIA_O_SISTEMA` (rebaixa a P-05, não a substitui). **Dono:** Claude.
**Gatilho:** antes de escrever qualquer taxa de ETF no `custos.yaml`.

Nas lâminas do Itaú, **"taxa de administração" é só um componente**: há também gestão,
custódia e estruturação. O BOVV11 tem adm 0,02% + custódia 0,01% + gestão 0,07% = **0,10%
total**. O PIBB11, 0,005 + 0,005 + 0,049 = **0,06% total**. A BlackRock, ao contrário,
publica número único (BOVA11 0,10%, SMAL11 0,50%, IVVB11 0,23%).

Guardar isso num campo `taxa_adm` e comparar rotas por ele **subestima sistematicamente o
custo do lado Itaú**. É o F-02 num disfarce novo: o número existe, está certo, e mede
outra coisa. `custos.yaml` precisa de `taxa_total_aa` + `composicao` + `fonte_url` +
`data_doc`.

Os valores acima são **PARCIAL** — vieram de subagente, não da minha leitura. Antes de
entrar no `custos.yaml` cada um precisa da conferência de trecho que a doutrina exige.

---

## P-51 · `ORDEM_EXERC = PENÚLTIMO` contamina o backtest

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** ao escrever o parser da CVM.

O projeto contou as duas enumerações em 12,8 milhões de linhas e registrou as duas como
válidas. Elas são — mas **`PENÚLTIMO` é o ano anterior já reapresentado**. Usar a linha
`PENÚLTIMO` do arquivo de 2025 para saber o que se sabia em 2024 é look-ahead puro: é
justamente o número corrigido depois.

Regra que sai daqui: o parser usa **só `ÚLTIMO`, do arquivo daquele ano**. E a partição é
o **ano do arquivo**, não o ano do dado — o DFP de 2025 corrige 2023.

---

## P-52 · ANBIMA — o segundo prazo real do projeto, e ele não estava registrado

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo. **Gatilho:** decidir se o projeto
quer série ANBIMA.

IMA-B, IRF-M, ETTJ e debêntures ficam públicos por **5 dias úteis**. O histórico só existe
no ANBIMA Feed — grátis para associado, pago para o resto. Ou o projeto começa a coletar
diariamente, ou aceita não ter a série.

A decisão é de desenho porque muda o escopo: sem IMA-B não há comparação direta de um ETF
de inflação com o índice que ele segue. Hoje o projeto usa Tesouro direto como referência,
e isso pode bastar. **Não decidi por ele.**

---

## P-53 · O acervo não pode depender de engine nenhum

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude. **Gatilho:** ao criar `data/bronze/`.

Recomendação da pesquisa: **Parquet imutável particionado por `dt_captura` como acervo, e
DuckDB como motor de consulta** — com o `.duckdb` sendo artefato reconstruível, nunca o
arquivo de registro. Segundo lugar: DuckLake (1.0 em abr/2026), com `AT (TIMESTAMP => …)`
nativo; perdeu por acoplar um acervo de década a um formato recente.

A consulta as-of e as sete armadilhas estão em
`docs/fontes/pesquisa-bases-e-apis-2026-09.md` §3. Duas que este projeto não sabia que
tinha, além da P-51: **`dt_captura` não é data de conhecimento do mercado** e **o
mapeamento ticker↔CNPJ↔CD_CVM também precisa ser bitemporal**, senão o join vaza futuro.

---

## P-54 · A rotina de snapshot da CVM é SEMANAL — e ainda não existe

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo (rodar) + Claude (escrever).
**Gatilho:** terça, junto do coletor da B3.

Confirmado na fonte em 06/09 (`docs/fontes/cvm-dfp-politica-atualizacao.md`, COMPLETO):
a CVM atualiza **semanalmente** os arquivos dos **últimos cinco anos**, com as
reapresentações. Os de 2010 a 2020 estão congelados.

**O que muda em relação ao que o projeto acreditava:**

| acreditava | é |
|---|---|
| o arquivo do ano corrente é reescrito | **os seis últimos** são, toda semana |
| o prazo vence em 31/12 | o prazo vence **toda semana** |
| são 1,5 GB correndo contra o tempo | são **6 arquivos**; os outros 11 podem esperar |

Última atualização registrada pela CVM: **31/08/2026, 08:01**. Entre ela e a terça
haverá pelo menos mais uma rodada — a primeira captura já nasce com uma semana perdida,
e isso não é recuperável.

O que falta: uma rotina que rode toda semana e grave
`data/bronze/cvm/dfp/dt_captura=AAAA-MM-DD/`, com sha256 e manifesto, **sem sobrescrever**.
O `coletar_b3.py` já tem a forma; falta o equivalente para a CVM, e ele pode reusar
`cvm_catalogo.py` para ler o `last_modified` de cada recurso e só baixar o que mudou.

---

## ~~P-55~~ · Política do ITR — **FECHADA em 06/09/2026, no mesmo dia**

Conferida na fonte (`docs/fontes/cvm-itr-politica-atualizacao.md`, COMPLETO). É
**idêntica** à do DFP: semanal, últimos cinco anos, histórico desde 2011.

Duas coisas vieram de brinde: os recursos do ITR **vêm rotulados por ano** (2021…2026),
o que converte a janela de inferência em observação; e o carimbo `31/08/2026 08:01` é
**o mesmo nos dois conjuntos, ao minuto** — é um único job semanal do portal, então uma
única rotina cobre os dois e um único `last_modified` decide se vale baixar.

---

## P-56 · `composicao_capital` só em 2024 — a explicação apareceu, e ela é uma regra

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude. **Gatilho:** ao escrever o parser.

`cvm-enumeracoes-observadas.md` registrou que `composicao_capital` só existe na safra de
2024, e deixou o porquê em aberto. A página do conjunto diz que ele "também disponibiliza
as seções Pareceres e Declarações e **Dados da Empresa/Composição do Capital**".

**Inferência (não leitura):** se só os últimos cinco anos são regerados, as safras
congeladas de 2012 e 2019 ficaram no formato anterior à inclusão dessa seção e **nunca
serão regeradas**.

Isso converte "a estrutura muda entre safras sem motivo" em **"a estrutura de uma safra
congelada é a do dia em que ela congelou"** — que é regra, e regra se testa. O parser
passa a poder afirmar: safra fora da janela tem estrutura estável para sempre; safra
dentro da janela pode ganhar coluna a qualquer semana.

NAO_CONFIRMADO: o ano exato de entrada da seção.

---

## P-57 · A captura semanal não pode depender do Osvaldo lembrar — achado W-01

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de considerar a
Fase 0 concluída.

**Correção dele, 06/09/2026.** Eu ofereci montar um lembrete semanal:

> *"o lembrete no caso seria exatamente para quê? uma das coisas do projeto é
> estabilidade, e um projeto escalável não deve depender de mim para funcionar."*

Está certo. Virou a **doutrina P7** do CLAUDE.md. E é a terceira vez que eu ponho ele no
caminho crítico de algo que é do sistema — U-01, P6, e agora esta.

### O problema real, sem disfarce

A captura precisa de três coisas ao mesmo tempo: **gatilho** (semanal), **rede**, e
**disco** que retenha os snapshots. A máquina dele fica desligada quase sempre; o Task
Scheduler do Windows não roda em máquina desligada, então ele não é solução — é o mesmo
lembrete com outro nome.

### A separação que torna o problema tratável

Os dois lados têm custo de armazenamento muito diferente, e tratá-los junto é o que faz
o problema parecer impossível:

| | tamanho | automatizável hoje |
|---|---|---|
| **eventos societários da B3 + carteira de índice** | JSON, poucos MB por captura | **sim** — cabe em repositório, cabe em runner gratuito |
| **metadado da CVM** (`last_modified` dos 2 conjuntos) | bytes | **sim** — e é o que decide se vale baixar |
| **os 6 ZIPs da CVM** | centenas de MB por captura | **não trivialmente** — é aqui que mora o custo |

**Ou seja: a parte irreplicável e perecível é a barata.** O que é caro de guardar (os
ZIPs) é justamente o que dá para reconstruir parcialmente, porque a CVM mantém a versão
corrente; o que não dá para reconstruir de jeito nenhum (eventos societários, composição
de índice, e o *histórico* de `last_modified`) é pequeno.

### O que investigar antes de decidir

- **GitHub Actions com `schedule`** — cron semanal, sem máquina ligada. Cobre B3 e
  metadado da CVM com folga. Limites de minuto e de armazenamento em repositório
  privado: **NAO_CONFIRMADO**, precisa ser lido antes de prometer.
- Onde guardar os ZIPs quando o metadado acusar mudança, e por quanto tempo. Talvez a
  resposta honesta seja: **não guardar todos**, e declarar isso.
- Se o próprio `last_modified` capturado semanalmente já entrega parte do valor
  point-in-time sem guardar o conteúdo — ele diz *quando* mudou, mesmo sem dizer *o quê*.

### A resposta, pesquisada no mesmo dia

`docs/fontes/executor-da-rotina-semanal.md`. **GitHub Actions em repositório privado.**
14 GB de disco efêmero, 6 h por job, 2.000 min/mês (a rotina usa 100–200), banda não
tarifada, e **sem pausa por inatividade** — a regra dos 60 dias só vale para repo público.

**Supabase está descartado como executor**, e o motivo é preciso: projeto Free **pausa
após 1 semana de inatividade**, com restauração manual. Uma rotina semanal vive em cima
desse limiar — seria a P7 violada pela própria infraestrutura. Edge Function ainda por
cima limita a 150 s, 256 MB e upload de 50 MB.

**E o armazenamento deixou de ser problema:** guarda-se o **delta**, não o snapshot.
Poucas centenas de MB por ano em vez de dezenas de GB, versionado no próprio git.

**O que falta para fechar:** escrever o workflow, e a primeira execução real. Página de
limite lida não é rotina rodando — até lá, a limitação vai declarada.

**A armadilha a embutir no desenho:** 404 + unzip vazio = "nenhuma mudança", que é
indistinguível de "a CVM não mudou nada". `set -euo pipefail`, conferência de sha256, e
notificação em `if: failure()`. Ausência de mudança se **afirma**, não se infere.

---

## P-58 a P-61 · Regimes de leitura de balanço — a pergunta que expôs o defeito

**Documento:** `auditoria/regimes-de-leitura-de-balanco.md`. **Classe:** todas
`BLOQUEIA_O_SISTEMA`. **Gatilho:** depois da P-18 (contar `SETOR_ATIV`), que bloqueia as
quatro.

**Pergunta do Osvaldo, 06/09/2026:** como o sistema lida com empresa que lucrou menos por
reinvestir, com dívida feita para capex, e com setores que funcionam com dívida alta —
construção civil, porque se realiza imóvel com financiamento.

**Resposta honesta: não estava desenhado.** E a pergunta expôs um defeito do projeto, não
uma lacuna de escopo.

O `bloco_C_solvencia` já escreve que dívida líquida/EBITDA aplicado a um banco *"devolve
um número, e esse é o perigo: métrica que não se aplica mas não falha é o modo de falha do
F-02"*. **O projeto reconheceu esse modo de falha para banco e não o generalizou.** Existe
um regime para instituição financeira e **um único regime para "todo o resto"** — que lê
uma incorporadora e uma WEG com a mesma régua.

| | |
|---|---|
| **P-58** | o portão de regime tem 2 saídas e precisa de N. Candidatos: incorporação, utilities/concessões, propriedades para renda, arrendamento pesado (IFRS 16) |
| **P-59** | **C-01 (cobertura de juros) exclui empresa em fase de investimento** — EBIT deprimido por depreciação nova E despesa financeira alta pela dívida do capex: as duas pontas pioram pelo mesmo motivo, que pode ser saudável. E cai no portão de **exclusão**, o pior lugar |
| **P-60** | **ROIC vs custo da dívida** não existe no sistema, e é o único critério que separa dívida que cria valor de dívida que destrói |
| **P-61** | capex de **manutenção** vs **expansão**: a CVM não separa, e a heurística "manutenção ≈ depreciação" é conhecidamente errada em empresa que cresce. **Limitação declarada**, com direção de viés: **o sistema subestima quem investe para crescer** |

**A correção que a pergunta dele também recebeu:** capex **não passa pela DRE**. O que
derruba o lucro são três causas distintas — depreciação do capex passado, juros da dívida
do capex, e opex não capitalizado — e elas têm leitura **oposta**. Consequência de
desenho: **a porta de entrada é a DFC, não a DRE.**

**P6 aplicada:** construção civil **não sai do universo**. A saída fácil seria excluir por
falta de régua, e foi exatamente essa a correção que criou a P6 — no caso do banco. Se eu
excluir agora, é a quarta vez.

**O que só ele responde** (§6 do documento): dívida SFH vs corporativa, receita a
apropriar, permuta, distratos, e qual número um planejador olha primeiro. Ele é engenheiro
civil e analista de planejamento; isso é procedência melhor que artigo, **desde que
registrada como decisão dele**.

---

## P-62 · Repositório público — **DECIDIDO em 06/09**, com pré-requisito duro

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo (decidiu) + Claude (executar).
**Gatilho:** antes do primeiro `git push`.

Ele disse não ter problema com repositório público. Isso **melhora** a automação: repo
público tem Actions sem consumo de cota e runner maior (4 vCPU/16 GB contra 2/8). A regra
dos 60 dias de auto-desativação do cron deixa de morder porque **o próprio workflow
commita o delta toda semana**, e commit é atividade.

**Mas há um pré-requisito que não é negociável:** `alocacao/estado.yaml` guarda a situação
financeira real dele — patrimônio, aporte, dívida. Em repositório público, isso **não
entra**, e a U-01 já provou que não precisa: `test_usuario_novo.py` mede que o sistema
funciona com estado vazio, e `estado.exemplo.yaml` existe para ocupar esse lugar.

A favor: nada foi empurrado ainda, então **não há histórico para reescrever** — a janela
limpa é agora. Se um commit com `estado.yaml` for para o GitHub público, a correção passa
a exigir reescrita de histórico, e a cópia já vazou.

**`perfil.yaml`: ele decidiu que pode ser público.** Perguntado na forma correta ("você
quer isso público, podendo não ter?"), respondeu que sim. Fica registrado como
`DECISAO_DO_USUARIO`, e sobrevive à carteira mudar.

**`estado.yaml` continua fora**, e isso não é preferência: é o único arquivo que carrega
patrimônio, aporte e dívida reais. O `.gitignore` precisa listá-lo **antes** do primeiro
`git add`, e o teste que guarda isso ainda não existe — ver P-67.

---

## P-63 · O híbrido nível/tendência é regra geral ou regra do bloco C?

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo. **Gatilho:** ao implementar qualquer
métrica com leitura temporal.

Em 05/09 ficou decidido, para solvência: **HÍBRIDO — o nível corta, a tendência marca sem
poder de veto.**

Em 06/09, sobre distratos, ele disse o contrário: `5% → 7% → 11% → 16%` preocupa **muito
mais** que `12% → 11% → 10% → 9%`, mesmo com o segundo em nível mais alto. **A tendência
domina.**

Os dois podem estar certos — mas então **o híbrido não é regra geral, é regra do bloco C**,
e isso precisa ser dito. Duas saídas, ambas defensáveis:

- **(a)** o híbrido é *por métrica*, e distrato é uma métrica cuja informação mora na
  direção;
- **(b)** o híbrido é geral, e o que muda é o que conta como "nível" — para distrato, o
  nível seria a **média móvel**, não o ponto.

Decidir por omissão aqui seria deixar o código escolher, que é exatamente o que a P2 proíbe.

---

## P-64 · Portão × dossiê — uma camada de desenho que o projeto não tem

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de implementar
qualquer regime.

Ele respondeu como analista lendo **uma** empresa. O sistema precisa varrer **centenas**.
Uma sequência manual de dez passos não é portão.

| | o que é | quando roda | fonte |
|---|---|---|---|
| **portão** | automático, todo o universo | sempre | dado estruturado |
| **dossiê** | leitura manual guiada, empresa a empresa | só na lista curta | notas, release, IPE |

Para incorporação **o portão não pode ser o regime** — o dado não existe (X-01). O portão só
pode dizer: *"esta empresa é do regime INCORPORACAO, exige dossiê, e até ter um permanece no
universo sem peso atribuído por este bloco."*

Coerente com P6 (nada sai), P1 (nada é inventado) e A05 (o sistema não nomeia empresa). E
transforma o painel de cinco camadas dele **no roteiro do dossiê** — que é o que ele é.

**Vale para todo regime, não só incorporação.**

---

## P-65 · Extração de nota explicativa e de IPE — a segunda esteira, nunca orçada

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** depois da Fase 0 rodar.

**Achado X-01.** Dos dez passos da sequência dele, **3 são obtíveis** no dado estruturado
(FCO, margem bruta, caixa) e **7 não são**. E os 3 obtíveis são os que ele não colocaria em
primeiro lugar.

O caminho existe: a página do conjunto DFP publica *"os endereços para download dos
Formulários DFP entregues"* (documento completo do Empresas.NET), e o **IPE** carrega
releases de resultados. Mas é **extração de documento**, não leitura de CSV — ordem de
grandeza diferente do que o projeto orçou.

**A investigar antes de prometer:** formato dos formulários do Empresas.NET; se as notas
vêm em XML estruturado ou em texto livre; volume do IPE; e se existe alguma padronização
que torne a extração determinística em vez de heurística. **Se for heurística, ela produz
número sem procedência — e aí a P1 manda não fazer.**

---

## P-66 · Os cortes de distrato entram no YAML como decisão declarada

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude (implementar). **Gatilho:** junto da P-64.

10% / 15% / 20% são os cortes dele. **Ele mesmo escreveu que "não existe percentual
universal"**, então são `DECISAO_DO_USUARIO`, **não** `CRITERIO_MEDIDO` — exatamente como o
bloco C já declara que "dívida líquida/EBITDA abaixo de 3 é costume de mercado, não norma".

Vão para o YAML com o **custo de discordar medido**: quantas empresas mudam de lado se o
corte for 10 em vez de 15.

---

## P-67 · Falta o teste que impede `estado.yaml` de ir para um repositório público

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** **antes** do primeiro
`git add`.

A decisão P-62 depende de uma linha de `.gitignore`, e uma linha de `.gitignore` é
exatamente o tipo de coisa que se perde numa refatoração sem ninguém notar. **Isso é o
padrão que o projeto inteiro existe para combater:** um arquivo declara um comportamento e
nada testa se ele acontece.

O teste: falha se `estado.yaml` estiver rastreado pelo git, ou se qualquer arquivo com o
padrão de estado real entrar no índice. Barato, e é a diferença entre uma decisão e uma
esperança.

---

## Fechadas

| # | o que era | fechada em |
|---|---|---|
| — | isenção de FII: 50 ou 100 cotistas | 04/09 — **100**, duas leis independentes |
| — | enumerações ORDEM_EXERC / ESCALA_MOEDA / MOEDA | 04/09 — `OBSERVADO`, 12,8M linhas |
| — | layout do COTAHIST conferido contra dado real | 04/09 — + fechamento ao byte em 05/09 |
| — | custódia interna dos ETF iShares não modelada (F-01) | 04/09 |
| — | rota bloqueada simulava com custo zero (F-02) | 04/09 |
| — | CRLF mudava o sha256 da série do NEFIN (F-04) | 04/09 |
| — | `.md` → constante do `custos.yaml` sem mapa | 05/09 — `MAPA-CONSTANTES.md` |
| 20 | regime de análise para bancos | 05/09 — **especificado**, 5 métricas, só Basileia com piso legal |
| — | LCI/LCA e FII fora do catálogo | 05/09 — viraram rotas, bloqueadas com motivo |
| P-03 | 6 citações apontando para trecho não transcrito | 05/09 — 5 transcritas, 1 corrigida |
| F-05 | `bloqueia` era prosa: nenhuma linha de código o lia | 05/09 — viaja na exceção + 3 testes |
| F-03 | IMAB11 como concorrente do Tesouro IPCA+ | 05/09 — **hipótese caiu**: 0,25% > 0,20%, Tesouro vence em todas as faixas |
| L-01 | escolhas do usuário misturadas com o motor | 05/09 — `perfil.yaml` + 3 testes de fronteira |
| J-03 | troca depósito/limite calculada em 14,5:1 | 05/09 — **refutada**: é 1:1 mais bônus |
| J-02 | reserva é colateral da própria fatura do cartão | 05/09 — registrado; motor já zerava por outro caminho |
| K-03 | isenção do Turbinado parecia gratuita | 05/09 — é paga em gasto no cartão e chave Pix |
| K-01 | Turbinado parecia melhor sem olhar a mensalidade | 05/09 — empate acima do teto: nunca se paga pagando |
| J-01 | reserva contada pela nominal, não pela disponível | 05/09 — `reserva_efetiva`; meses caíram de 1,9 para 0,0 |
| — | `opcoes` excluída por resposta factual | 05/09 — **revertida**, virou P-20 |
| P-16 | bloco C: nível ou tendência | 05/09 — **híbrido**, e admite empresa sem dado |
| P-14 | banco no universo | 05/09 — **construir a fonte do BCB**; banco não sai |
| P-07 | ordem dos portões no código, não no YAML | 05/09 — dado + achado I-01 |
| P-13 | `isento_ir` booleano não expressava o FII | 05/09 — dois campos |
| — | bloco C sem regime de exclusão | 05/09 — **regime especificado**, com a lacuna C-04/C-05 declarada |
| — | schema não sabia expressar "regra decidida, papel não comprado" (G-01) | 05/09 |
| H3 | `tamanho_smb_v1` — prêmio de tamanho no Brasil | 05/09 — **nula sobrevive**, t=0,28, P(rejeitar)=3% |
| P-24 | rota com teto de saldo não modelada | 05/09 — `teto_de_saldo` + G2 devolve composição |
| K-02 | teto do produto ignorado pelo G2 | 05/09 — era pior: prometia retorno sobre dinheiro recusado |
| O-01 | retorno médio no alvo inteiro escondia a isenção do Tesouro | 05/09 — critério virou marginal |
| N-01 | seção `corretora` declarava 3 regras que só o Python decidia | 05/09 — lidas do YAML + 5 testes |
| P-28 | guarda de cobertura media o próprio escopo | 05/09 — 19 seções, 11 módulos, regime declarado |
| P-33 | `aporte_extraordinario.registro` na dívida | 05/09 — **falso positivo**, é prosa |
| P-15 | ambiente de execução não registrado | 05/09 — `pyproject.toml` + `ambiente.py`, 8 testes |
| P-36 | catálogos eram dado de pesquisa dentro de código | 05/09 — 2 YAML, migração com **zero diferenças** |
| Q-01 | insumo bloqueado derrubava o catálogo inteiro | 05/09 — bloqueia a rota, nunca o catálogo |
| Q-02 | `confirmacao` era uma letra para cinco fontes | 05/09 — procedência por grupo, letra derivada |
| P-37 | `alocar()` com 300 linhas | 05/09 — 6 passos, **zero desvio** em 38 cenários |
| R-01 | ordem dos portões só aceitava 18 de 120 valores | 05/09 — contrato `consome`/`produz` declarado |
| P-38 | `deepcopy` por disciplina, não por garantia | 06/09 — `conftest.py` + guarda que nomeia o culpado |
| S-01 | 37% do motor era re-hashear o `custos.yaml` | 06/09 — memoizado por mtime |
| S-02 | cache de arrasto ignorava o `C` recebido | 06/09 — **testes que alteravam custo testavam nada** |
| P-39 | não havia mapa de dependências | 06/09 — `impacto.py`, com os pontos cegos declarados |
| P-40 | sem lint nem type-checker | 06/09 — ruff e mypy em **zero**, com cada dispensa justificada |
| T-01 | linha morta cuja chamada contradizia a docstring | 06/09 — removida; revelou o **terceiro catálogo** |
| — | cofrinho do PicPay fora do catálogo | 05/09 — 2 rotas; a dele entra **sem** LIQUIDEZ |

---

## Ao voltar ao desktop

*Reescrito em 06/09/2026. A versão anterior era de 05/09 e citava 149/158 testes — hoje
são 269. Fila desatualizada é pior que fila nenhuma: ela parece confiável.*

### 0. Antes de tudo — a ordem importa

1. Extrair o zip `bastter-06set2026.zip` por cima da pasta (ele traz **tudo** desde
   sexta 18h).
2. `cd alocacao ; python ambiente.py` — confere o ambiente **antes** de acreditar em
   qualquer número.
3. `python -m pytest -q` — esperado: **269 passed**.
4. `ruff check . && mypy .` — ambos em **zero**.

### 1. O que precisa ser gravado na pasta (4ª leva, tudo posterior a sexta 18h)

| arquivo | destino | o que é |
|---|---|---|
| `alocacao.py` | `alocacao\` | P-24 (`teto_de_saldo`, `compor_reserva`), P-36 (catálogo em YAML), P-37 (`alocar()` em 6 passos), S-01, S-02 |
| `catalogo.yaml` | `alocacao\` | **novo** — 25 rotas, valores por referência ao `custos.yaml` |
| `instituicoes.yaml` | `alocacao\` | **novo** — 24 instituições, procedência por grupo de campos |
| `ambiente.py` | `alocacao\` | **novo** — P-15 |
| `impacto.py` | `alocacao\` | **novo** — P-39, mapa de dependências |
| `conftest.py` | `alocacao\` | **novo** — P-38, guarda de estado compartilhado |
| `estado.exemplo.yaml` | `alocacao\` | **novo** — cadastro mínimo (U-01) |
| `test_usuario_novo.py` | `alocacao\` | **novo** — 13 testes, U-01 |
| `test_p40_lint.py` | `alocacao\` | **novo** — ruff/mypy como portão da suíte |
| `test_alocacao.py`, `test_motor.py`, `test_impacto.py`, `test_corretoras.py` | `alocacao\` | atualizados |
| `motor.py`, `politica.yaml`, `custos.yaml`, `corretoras.py`, `cenarios.py`, `demo_aporte.py`, `estado_io.py`, `fatores.py`, `reserva.py`, `aporte.py`, `tese.py` | `alocacao\` | lint/tipos em zero |
| `pyproject.toml` | raiz | **novo** — P-15 + P-40 |
| `CLAUDE.md` | raiz | §7 refeita (V-01), §11.2 **corrigida**, §11.3 reescrita |
| `PENDENCIAS.md` | raiz | este arquivo |
| `ACHADOS.md` | raiz | **novo** — a história, migrada para fora do CLAUDE.md |
| `pesquisa-bases-e-apis-2026-09.md` | `docs\fontes\` | **novo** — a pesquisa de 06/09 |
| `fase0\` (pasta inteira) | raiz | **novo** — `LEIA-PRIMEIRO.md`, `CELULAR-CVM.md`, `fase0.ps1`, `coletar_b3.py` |
| `gitignore-ATUALIZADO.txt` | vira `.gitignore` | acrescenta `.mypy_cache`, `.ruff_cache` |
| `dot-claude\` | renomear para `.claude\` | as 3 skills do projeto |

### 2. Comandos que só a sessão local pode dar

```powershell
# a) O dado PERECÍVEL primeiro. É o único item da lista que pode deixar de existir.
python fase0\coletar_b3.py --indice IBOV
python fase0\coletar_b3.py --eventos

# b) Só então a CVM, e SEM baixar nada ainda:
.\fase0.ps1 -SoConferir

# c) git — o repositório ainda não existe no GitHub
#    gh não está instalado: criar em github.com/new, PRIVADO, sem README/gitignore/licença
git add -A
git commit -m "P-15/24/36/37/38/39/40, U-01, V-01: pesquisa de bases e coletor da B3"
git remote add origin <url>
git push -u origin main
```

### 3. Contas pendentes de dado, que só rodam aí

- **P-17** — reconciliar C-04 e C-05 com `auditoria/escopo-campos-de-analise.md`.
- **P-18** — contar `SETOR_ATIV` nos ZIPs da CVM.
- **P-06** — registrar a URL do PDF do layout do COTAHIST.

### 4. O que o celular pode antecipar em dois dias

`fase0/CELULAR-CVM.md`. A Tarefa 1 leva 2 minutos e fecha o `NAO_CONFIRMADO` que decide
se a Fase 0 é urgente — a mesma pergunta que o `-SoConferir` responde na terça.

### 5. Vencimento a conferir

`macro.poupanca_am` vence em **28/09/2026**. `motor.val()` avisa em stderr. Ainda não
venceu; só não deixe passar.

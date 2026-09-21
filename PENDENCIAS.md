# Pendências

Registro único e vivo. Atualizado a cada sessão, **antes** de encerrar.
Regra da casa: pendência sem dono e sem gatilho não é pendência, é desabafo.

**Estado em 06/09/2026 (2ª sessão do dia) · política 1.17.0 · custos 2.1 · perfil 1.0 · catálogo 1.0 · 269 testes**

**Classes:** 42 `BLOQUEIA_O_SISTEMA` · 10 `DECISAO_DE_DESENHO` · 3 `DADO_DE_UM_USUARIO`
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

## P-06 · ~~`Fonte: NAO_REGISTRADA` no layout do COTAHIST~~ **FECHADA em 19/09**

O `SeriesHistoricas_Layout.md` não registra de onde veio o PDF. Pesa porque o
achado central daquele arquivo é que as tabelas anexas da **revisão 02 (05/10/2020)**
estão desatualizadas — `TPMERC=021` e seis `CODBDI` aparecem em 2023 e não constam.
Sem a URL não dá para checar se existe revisão 03.

**Gatilho:** antes de escrever o parser do COTAHIST.

> **18/09/2026 — medido, e reclassifica a pendência.** As duas páginas públicas da série
> histórica foram lidas nesta data (a atual da B3 e o formulário no host legado) e
> **nenhuma linka documento de leiaute** — não é "eu não procurei a URL", é *a página
> onde ela deveria estar não a tem*. Transcrição em
> `docs/fontes/b3-series-historicas-cotahist.md` §5.
>
> **RETIRADO em 19/09, no dia seguinte.** O leiaute EXISTE e tem URL:
> `www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf`
> — **revisão 02 de 05/10/2020**, a mesma que o projeto transcrevia. **Não há revisão 03**,
> que era a pergunta da pendência. Fonte em `docs/fontes/b3-cotahist-leiaute.md`.
>
> Ele está numa **terceira** página — *Cotações Históricas*, não *Séries Históricas*. Eu
> tinha lido duas e concluído sobre "a página onde ela deveria estar". §5-B.13 dois dias
> seguidos. **A pendência fecha, e o que sobra é a P-95:** o leiaute **não traz tabela de
> valores para `MODREF`** — não é tabela incompleta, é inexistente.
>
> ~~A P-06 deixa de ser *achar um link* e passa a ser *decidir o que fazer sem ele*, e a
> saída provável é limitação declarada:~~ o layout que o projeto usa é cópia sem fonte
> verificável, e a enumeração real tem de sair do **dado observado** com falha ruidosa
> fora dela — que é o que a P-95 já mandava, por outro motivo.

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

**11/09/2026: `promocional` saiu desta lista.** O `regras()` agora recusa peso diferente
de zero, no mesmo padrão de `reclame_aqui` e `facilidade`. Restam
`cobertura_e_penalidade` e `fora_do_ranking`.

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

## P-68 · O primeiro aporte existe — e a pergunta certa não é quanto, é se está livre

**Classe:** `DADO_DE_UM_USUARIO`. **Dono:** Osvaldo. **Gatilho:** antes de rodar qualquer
projeção de Fase A com número real.

**10/09/2026: R$500 depositados**, no cofrinho do PicPay a 121% do CDI, obtido *"por
completar as missões"*.

O projeto já mediu esse produto, e o registro é desconfortável (`custos.yaml`, seção
`cofrinho`, achados J-01/J-02/K-01):

- o Turbinado a 121% que foi analisado em 05/09 vem com **mensalidade de R$287,88/ano** e
  exige **R$2.500 de gasto no cartão em 3 meses**;
- o diferencial de 121% para 102% vale **2,113% a.a. líquido de IR** — e, no teto,
  **PERDE R$76,60 por ano** contra o cofrinho comum;
- e o principal: **o cofrinho que rende mais é caução do limite do cartão.** Dinheiro
  empenhado **não é reserva** — é garantia. O `Estado` já separa `reserva_atual` de
  `reserva_disponivel` exatamente por isso.

### RESPONDIDA em 10/09 pela tela do app — e a resposta contraria o que ele disse

`docs/fontes/picpay-cofrinhos-2026-09-10.md`, status OBSERVADO.

Ele escreveu *"os 500 reais é livre"*. **A tela do produto diz o contrário**, em duas
marcações independentes: *"O saldo deste cofrinho está ativo como limite do seu cartão"*
e a etiqueta `LIMITE DO CARTÃO` na lista.

A distinção por trás disso é real: o cofrinho é **líquido** (resgata quando quiser) e
**empenhado** (resgatar derruba o limite) ao mesmo tempo. É exatamente por isso que o
`Estado` separa `reserva_atual` de `reserva_disponivel` desde o J-01.

**E apareceu o número que faltava:** total guardado **R$ 8.181,71** — R$500 no Turbinado
(121%) e **R$ 7.681,71 no Cofrinho do Cartão (120%)**, os dois etiquetados
`LIMITE DO CARTÃO`.

> **O M-01 estava certo pelo motivo certo.** Ele registrou que "~mar/2030" fora calculado
> com **R$7.671 de reserva inicial** e que isso estava errado *"porque a reserva é zero"*.
> O saldo hoje é **R$7.681,71**. **O número existia** — o que estava errado era chamá-lo
> de reserva. Agora há evidência, com etiqueta do próprio app.

**O que ainda falta, e é o único número que define a Fase A:** quanto do limite está
**comprometido** hoje. `reserva_disponivel = 8.181,71 − limite usado`. Com limite zerado,
a reserva é R$8.181,71 e a Fase A está muito à frente do que o projeto supõe; com o limite
todo usado, é **zero**, e o dinheiro garante dívida que já existe.

### Decisão dele em 11/09, e o registro guarda as duas coisas separadas

> *"considerar 500 reais livres — devo ter clicado na hora de depositar para usar como
> limite"*

**Registrado assim, e a separação é o ponto:**

| campo | valor | status |
|---|---|---|
| estado observado do Turbinado | `LIMITE DO CARTAO` | **OBSERVADO** — etiqueta do app, 10/09 |
| `reserva_disponivel` dos R$500 | 500 | **DECISAO_DO_USUARIO**, `NAO_CONFIRMADO` na fonte |

Não é firula de modelagem: as duas afirmações podem ser verdadeiras ao mesmo tempo — o
app mostra o estado de hoje, ele descreve a intenção e o que pretende desfazer. Misturá-las
num campo só apagaria qual das duas o sistema está usando.

**A conferência que fecha isso leva 30 segundos:** no cofrinho Turbinado há a linha *"O
saldo deste cofrinho está ativo como limite do seu cartão"* com uma seta. Entrar, desligar,
e tirar outra captura. Aí `reserva_disponivel = 500` vira **OBSERVADO** e a decisão some do
caminho — que é sempre o desfecho melhor.

> **O risco real, e ele é uma hipótese, não um fato:** na lista, **os dois** cofrinhos
> aparecem com a etiqueta `LIMITE DO CARTAO` — inclusive o de 120%. Pode ser que, no
> PicPay, **taxa alta e caução sejam o mesmo produto**, e que desligar o limite jogue o
> saldo para o cofrinho comum de 102%. Se for o caso, não existe "R$500 livre a 121%": há
> uma escolha.
>
> **E o preço dessa escolha é pequeno e já está medido:** 121% × 102% sobre R$500 é
> **R$13,20/ano bruto**. Treze reais por ano é o que custa ter esse dinheiro solto — e num
> projeto cuja Fase A depende de reserva de verdade, é barato. Mas é decisão dele, não
> minha, e depende de a hipótese se confirmar. `NAO_CONFIRMADO`.

---

## P-74 · K-01 comparou contra a alternativa errada

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de reescrever a
seção `cofrinho` do `custos.yaml`.

O K-01 mediu **121% × 102%** e concluiu que a mensalidade de R$287,88/ano fazia o
Turbinado perder. **Mas a alternativa real não é o cofrinho comum de 102%** — é o
**Cofrinho do Cartão a 120%**, que ele já tem e onde já estão R$7.681,71.

Com CDI de 13,90% a.a.:

| comparação | diferencial | sobre R$8.181,71 |
|---|---|---|
| 121% × **120%** | **0,139 p.p. a.a.** | **R$ 11,37/ano bruto · R$ 8,81–9,67 líquido** |
| 121% × 102% | 2,641 p.p. a.a. | R$ 216,08/ano bruto |

**As missões valem ~R$9 por ano**, antes de contar o que custa gerá-las (o K-01 registrou
~R$2.500 de gasto no cartão em 3 meses). É o M-01 outra vez: o destino move pouco, o
aporte move tudo — R$50/mês a mais valem R$600/ano, **66 vezes** o prêmio das missões.

E é a **P7** aplicada a dinheiro: manter o 121% depende de lembrar de cumprir tarefa todo
mês. Uma rotina que depende de alguém lembrar não é uma rotina — e aqui ela vale R$9.

**NAO_CONFIRMADO antes de reescrever o K-01:** a tela de 10/09 diz apenas *"Tarefas
concluídas"*; o K-01 registrou R$287,88/ano a partir de capturas de **05/09**. As duas
leituras podem estar descrevendo **planos diferentes**, e isso precisa ser reconciliado —
não reescrever o achado antigo com o dado novo sem entender a diferença.

---

## P-75 · O ambiente instalado diverge dos pinos, e o Python é outro

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo. **Gatilho:** antes de acreditar em
qualquer número produzido na máquina dele.

Instalado em 10/09: **numpy 2.5.3, pandas 3.0.5**, em **Python 3.13**.
Declarado no `pyproject.toml`: **numpy==2.4.4, pandas==3.0.2**, `requires-python ==3.11.*`.

**As três divergem, e as duas primeiras são as que MUDAM NÚMERO** — `alfa_contra_fatores`
resolve por `numpy.linalg.lstsq`, `mensal()` compõe por `pandas.groupby`.

Isto é o P-15 fazendo exatamente o trabalho dele: a divergência virou evento visível em
vez de número silenciosamente diferente. **A saída não é afrouxar o pino.** Ou se instala
o declarado, ou se muda o declarado **com medição** e registro em `REGISTRO-vN.md`.

Enquanto isso vale a regra já escrita no CLAUDE.md §3: a suíte continua verde e **isso
está certo** — o que deixa de valer não é o código, é a *reprodução* de um resultado
pré-registrado.

---



- livres → `reserva_atual = 500`, `reserva_disponivel = 500`. A Fase A começou.
- empenhados → `reserva_atual = 500`, `reserva_disponivel = 0`. **A reserva continua zero**,
  e o que existe é uma caução que rende.

E uma segunda, que pode **melhorar** o registro do projeto: se os 121% vieram de **missões**
e **não** de mensalidade, então a aritmética do K-01 não se aplica a este caso — o custo de
R$287,88/ano some, e o Turbinado deixa de perder para o cofrinho comum. **Seria a primeira
vez que um achado do projeto é derrubado por um fato novo em vez de por um erro.** Não
presumi: o K-01 fica como está até a captura do app confirmar.

---

## P-69 a P-72 · Auditoria externa (DeepSeek), conferida contra o código em 10/09

**Documento:** `AUDITORIA-DEEPSEEK-CONFERIDA.md`. Auditoria de terceiro é **hipótese**, não
achado — cada item foi rodado antes de virar pendência. Os quatro críticos são verdadeiros.

| # | item | classe | veredito |
|---|---|---|---|
| ~~**P-69**~~ | `etf.IMAB11` duplicado em `custos.yaml` (achado **Y-01**) | `BLOQUEIA_O_SISTEMA` | **FECHADA 11/09/2026** — ver tabela `## Fechadas`; abriu a **P-76** |
| ~~**P-70**~~ | `HOJE = dt.date(2026,9,1)` fixo em `motor.py:20` | `BLOQUEIA_O_SISTEMA` | **FECHADA 11/09/2026** — ver tabela `## Fechadas` |
| ~~**P-71**~~ | `dividas`/`objetivos` voltam como `dict`, motor espera dataclass | `BLOQUEIA_O_SISTEMA` | **FECHADA 11/09/2026** — ver tabela `## Fechadas` |
| ~~**P-72**~~ | `aporte_mensal <= 0` bloqueia `carregar()` | `BLOQUEIA_O_SISTEMA` | **FECHADA 11/09/2026** — ver tabela `## Fechadas` |

### O que os quatro têm em comum, e isso vale mais que os quatro

**P-71 e P-72 moram na costura entre dois módulos que cada um testa sozinho.** Os testes do
G1 montam `Divida(...)` na mão; `test_usuario_novo.py` monta o cadastro em memória. Nenhum
passa por `estado_io.carregar()`. **269 testes, e a porta de entrada real do sistema não é
exercitada por nenhum.**

Isso não é um bug: é uma lacuna de cobertura com forma reconhecível. O próximo defeito real
provavelmente mora ali também.

**E morava — duas vezes.** O teste que fecha P-71/P-72 (`test_p71_p72_porta_de_entrada.py`)
escreve um estado sintético (`tmp_path`, nunca o real) com dívida, objetivo e
`aporte_mensal=0`, carrega pelo caminho real e roda `alocar()` até o fim. Ele bateu em
QUATRO exceções diferentes, cada uma só visível depois que a anterior foi corrigida:
`EstadoInvalido` (P-72) → `AttributeError` em `g1_divida` (P-71) → `TypeError:
Estado.__init__() got an unexpected keyword argument 'reserva_empenhada'` (achado lateral:
`d` carregava `reserva_empenhada` e `meses_cobertos`, nenhum campo de `Estado` — o primeiro
já apontado como campo morto pela própria auditoria externa, o segundo duplicava uma
`@property` que `Estado` já calcula) → `ValueError: pesos somam 0` (achado lateral em
`custo_entrada_fixo_pct`, que tratava `aporte==0` como custo infinito para QUALQUER rota,
inclusive as de tarifa zero). `Estado(**estado_io.carregar()[0])` nunca tinha sido
executado, nem uma vez, fora deste teste.

### Correção à auditoria, registrada porque o método exige

**A1 (bônus arredondado, `aporte.py:69`) é verdadeiro, mas a auditoria o descreve pela
metade.** Ela diz "projeção otimista". Medido: 5/ano → 6 disparos (**+20%**), 7/ano → 6
(**−14%**), 11/ano → 12 (**+9%**). **Erra nos dois sentidos.** Viés que troca de sinal
conforme o input é pior que viés constante: não dá para corrigir de cabeça.

### Onde a auditoria erra de forma que importa: a ordem

Ela propõe **quatro semanas de motor** e a Fase 0 depois. É a P-44 sendo violada por
escrito, e o **X-01** torna o argumento mais forte — o dado estruturado da CVM responde 3
dos 10 passos de uma leitura de incorporadora, e nenhuma refatoração do motor antecipa
essa descoberta. Some-se o prazo semanal declarado pela própria CVM.

**Ordem defendida:** P-69 a P-72 (horas, não semanas) → **Fase 0** → o resto **em paralelo**.

---

## P-73 · A máquina roda Python 3.13 e o projeto exige 3.11

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Osvaldo. **Gatilho:** antes de acreditar em
qualquer número produzido lá.

`pyproject.toml` fecha em `requires-python = "==3.11.*"`, e a faixa é fechada **de
propósito**: 3.12 mudou o comportamento de comparação de `datetime.date` em alguns
caminhos, e o projeto compara `expira` em quase todo `val()`.

Isto é o P-15 fazendo o trabalho dele — a divergência virou um evento visível em vez de um
número silenciosamente diferente. **A saída não é reabrir a faixa por conveniência**: ou se
instala o 3.11, ou se reabre **com medição** e se registra em `REGISTRO-vN.md`.

Enquanto isso, um resultado produzido no 3.13 é **número novo**, não conferência de um
antigo.

---

## P-76 · A F-03 se declarou refutada com um insumo que não autoriza refutação

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo decide a regra; Claude implementa.
**Gatilho:** quando o regulamento do IMAB11 for baixado (P-05/P-50) — ou antes, se
qualquer decisão sobre a rota de ETF de renda fixa for tomada.

Aberta ao fechar a P-69. A F-03 foi medida em 05/09 **à mão, com 0,25%** (está em
`politica.yaml → fora_de_escopo.ETF_renda_fixa`) e registrada como *"hipótese caiu,
Tesouro vence em todas as faixas"*. Mas o próprio insumo é `PARCIAL`, com
`bloqueia: comparacao_definitiva_imab11_vs_td_ipca`, e o `motivo` diz por quê: **a
página do gestor não diz se 0,25% é teto de regulamento ou taxa efetiva.**

Isso não é detalhe. Se 0,25% for o **teto**, a taxa cobrada pode ser menor que 0,20% —
e a comparação **inverte**. A conclusão saiu mais forte que o insumo que a sustenta: é a
P1 aplicada ao relato de uma medição, não ao dado.

**A decisão que falta:** uma conclusão medida herda o status do insumo mais fraco dela?
Se sim, a F-03 volta a "tendência medida, não refutação" até o regulamento chegar, e a
linha da F-03 em `## Fechadas` ganha a ressalva. Não mexi em nenhum dos dois registros.

---

---

## P-80 · A rotina mede um terço do projeto

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo decide; Claude implementa.
**Gatilho:** agora — as três suítes estão verdes ao mesmo tempo, e é a janela barata.

`pyproject.toml` declara `testpaths = ["alocacao"]`, e `test_p40_lint.py` roda
`ruff check .` com `cwd=alocacao/`. Consequência medida em 16/09: `py -3.11 -m pytest -q`
dava **verde** enquanto `pytest fase0` tinha **9 falhas** e `pytest auditoria` tinha
**2** — e `ruff` tinha **5 violações** em `fase0/refinar.py` que nenhum portão olhava.

Isto é a **P7 aplicada à própria rotina**: rodar as outras duas depende de alguém
lembrar, então não é rotina. E o preço já foi pago: o A-06 sobreviveu quatro dias e a
linha de base das órfãs apodreceu, as duas coisas dentro das pastas que o portão não vê.

**A mudança é de uma linha e meia,** e não a apliquei porque ela **redefine o que
"verde" significa** neste projeto — isso é decisão sua, não minha:

```toml
testpaths = ["alocacao", "auditoria", "fase0"]
```

e, no lado do lint, `ruff check .` a partir da RAIZ. Esse segundo pede uma decisão a
mais: a raiz tem **14 violações** em `pesquisa-custos-2026-08/calc/`, que é cópia
congelada de pesquisa. Ou ela entra em `[tool.ruff] exclude` com o motivo escrito ao
lado, ou o portão nasce com linha de base — e linha de base conhecida não é barreira
(é o próprio texto do `test_P40_ruff_esta_em_zero`).

---

## P-81 · O `chaves_orfas.py` não separa decisão registrada de parâmetro órfão

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude, com sua confirmação.
**Gatilho:** a próxima vez que a linha de base crescer.

Reconferindo a linha de base em 16/09, dez chaves entraram de uma vez — e não porque
alguém escreveu chave nova: o instrumento passou a contar **"LIDA SÓ POR TESTE"** como
órfã. A mudança é deliberada e vem da P-77 (*campo que só o teste toca é campo que o
motor não usa*).

Mas as dez **não são da mesma espécie**, e a diferença decide o que fazer com cada uma:

- **parâmetro órfão** — `portoes.G3_atrito.ativo` prometia comportamento e não
  entregava. É defeito, e foi o E-03.
- **decisão registrada** — `corretora.promocional.e_uma_decisao_nao_uma_omissao: true`
  não promete comportamento nenhum: ela **registra um julgamento**, e o teste a lê para
  fixar o registro. Isso é procedência, não dívida.

Cinco das dez são do segundo tipo. Hoje elas convivem na mesma lista, e uma lista que
mistura duas espécies faz a próxima pessoa tratar procedência como dívida — ou, pior,
tratar dívida como procedência. O instrumento precisa de um terceiro rótulo, ou o YAML
precisa de uma convenção que ele reconheça.

---

## ~~P-77~~ · Meia P-13 — **FECHADA 16/09/2026**, ver `## Fechadas`

**Classe:** `BLOQUEIA_O_SISTEMA`. **Dono:** Claude. **Gatilho:** antes de qualquer rota
com `aliquota_ganho` sair do bloqueio por insumo — hoje o FII está bloqueado, e é só
por isso que o número não sai errado.

Achado pela guarda de campos mortos (11/09). A P-13 trocou `isento_ir` por dois campos
porque o FII não cabia num booleano: rendimento isento, **ganho tributado a 20%**
(Lei 8.668/1993 art. 18). O catálogo preenche os dois, e três testes conferem o
valor de `aliquota_ganho`. **Nenhuma linha de produção o lê.** `retorno_liquido_aa`
calcula `ir = 0.0 if r.isento_ir else aliquota_ir_rf(...)`, e `isento_ir` devolve
`isento_ir_rendimento` — para o FII, IR zero sobre tudo. É exatamente o *"True
subestimava o imposto"* que o comentário da P-13 descreve como o erro que ela corrigiu.

Inventariado em `test_campos_mortos.py`; o teste do inventário quebra no dia em que ele
passar a ser lido, e a linha tem de sair.

---

## P-78 · Dado de pesquisa coletado e nunca consumido — oito campos de `Instituicao` e um utilitário

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo decide por campo; Claude executa.
**Gatilho:** a próxima vez que `corretoras.py` for tocado.

A guarda achou 10 além dos quatro da auditoria; um é a P-77. Os outros nove:

- `bc_procedentes`, `bc_clientes` — o numerador e o denominador do `bc_indice`, que é o
  que pontua. Guardar a origem de um número é procedência; a pergunta é se o lugar
  dela é o dataclass ou o `instituicoes.yaml`.
- `corretagem_fii`, `corretagem_etf_pct`, `exercicio_opcao_pct`, `mesa_minimo` — custo
  por operação coletado e fora de `pontuar()`, que só usa `corretagem_rv`. O
  `corretagem_etf_pct` é o 0,50% da XP em ETF: para quem compra ETF, é o custo que
  mais importa, e o ranking não o vê.
- `home_broker_web`, `exporta_csv` — a dimensão `facilidade`, que o `regras()` já
  recusa pontuar em voz alta. Decisão tomada; o campo pode ficar como dado exibido.
- `ambiente.PACOTE_PARA_IMPORT` — usado só pelo teste do P-15. **É ponto cego
  declarado da guarda**, não defeito do código: uso só em teste conta como morto de
  propósito (P-71), e para um utilitário isso pode ser rigor demais.

Nada foi removido: o LIMITE do prompt era parar acima de cinco e mostrar a lista.

---

## ~~P-79~~ · Três cópias do desembrulho — **FECHADA 16/09/2026** junto com o A-06

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Claude. **Gatilho:** a próxima vez que o
caminho `--eventos` do `coletar_b3.py` precisar mudar por outro motivo.

A esteira de proventos (11/09) precisou desembrulhar o acervo — string JSON contendo
lista (A-00, A-02) — e ganhou `desembrulhar()`. A mesma regra já vivia **inline** em
`coletar_eventos` e numa **cópia** em `test_coletar_b3.py` (`_normalizar`, com um teste
que confere o fonte). Três implementações da mesma conta é a N-01 na forma canônica.

Não unifiquei porque o LIMITE do prompt 5 proibia tocar o caminho `--eventos`: ele
funciona, e o acervo que ele produz não se recupera. Quando ele for tocado por outro
motivo, `coletar_eventos` passa a chamar `desembrulhar()` e o teste espelho morre.

---

---

## P-82 · O repositório guardou uma cópia de si mesmo, e a suíte continuou verde

**Classe:** `BLOQUEIA_O_SISTEMA`. **FECHADA em 16/09/2026**, no mesmo dia em que abriu —
mas ela tem seis minutos de vida que valem mais que o conserto.

Ao fechar as seis falhas herdadas, o `git rm` apagou os cinco `*-patch.py` e a guarda
duplicada. Fez o certo. O `git add -A` seguinte encontrou na raiz a pasta
`pacote_segunda/pacote_segunda/` — o zip de 14/09 descompactado ali por engano — e a
levou junto. O git então viu os mesmos bytes saindo de um lugar e aparecendo em outro, e
registrou **rename**: os arquivos não foram removidos, **foram mudados de lugar para
dentro da cópia**.

O commit `bebea75` passou a carregar uma cópia congelada do projeto de 14/09: um segundo
`CLAUDE.md`, um segundo `chaves_orfas.py`, um segundo `refinar.py`, um segundo
`test_chaves_orfas.py`. **E a suíte ficou verde**, porque nenhum portão olha para lá —
`testpaths = ["alocacao"]`, `campos_mortos.py` varre `alocacao/`, o `ruff` do P-40 roda
com `cwd=alocacao/`. **A P-80 cobrou a primeira conta em menos de uma hora.**

### O que é caro aqui não é o erro, é que a regra já estava escrita

O `.gitignore` ignora `Claude outputs/` com o motivo por extenso: *"ela contém uma CÓPIA
INTEIRA do projeto... não é só tamanho: é a armadilha do `pesquisa-custos-2026-08/calc/`
outra vez, e pior."* A armadilha tinha **nome**, tinha **precedente citado**, e tinha
**remédio** — e o remédio era uma **lista de nomes de pasta que alguém precisa lembrar de
estender**. `pacote_segunda/` não estava na lista. É a P7 na forma mais limpa que o
projeto já produziu: *rotina que depende de lembrar não é rotina*.

`alocacao/test_p82_copia_do_projeto.py` mede o **índice do git**, não o disco — como o
`test_p67_segredo.py` faz com o `estado.yaml`. Descompactar um zip na pasta é inofensivo;
o defeito nasce no `git add`. Duas regras: módulo com o mesmo nome de um módulo dos três
pacotes, e **pasta de pacote aninhada** — a segunda existe porque a primeira não pegaria
`pacote_segunda/pacote_segunda/alocacao/E02-patch.py`, cujo nome não colide com nada.

### O que fica aberto dentro dela

`pesquisa-custos-2026-08/calc/` tem `motor.py`, `test_motor.py` e `custos.yaml` — os
mesmos nomes do projeto vivo, congelados em 28/08. Entrou em `COPIAS_DECLARADAS` com o
motivo escrito, que é o terceiro caminho honesto do protocolo das órfãs. **Mas declarar
não é resolver:** quem abrir `calc/motor.py` continua lendo uma versão de três semanas
atrás sem nada no arquivo avisar. Mover para `docs/historico/` ou renomear os arquivos
resolveria de vez — e isso é decisão sua.

---

---

## P-83 · Nove casas não pesquisadas carregavam custo ZERO — e a decisão 1 ia acordá-lo

**Classe:** `BLOQUEIA_O_SISTEMA`. **FECHADA em 16/09/2026** na parte que é defeito.
A dimensão do ranking, que é a decisão, **continua aberta** — ver P-84.

Fui implementar a sua decisão de 13/09 (*"custo por operação entra no ranking: **sim**"*)
e medi os campos antes de escrever a dimensão. A medição derrubou a premissa e achou
outra coisa.

### O que a medição mostrou

| campo | declaram | valores distintos |
|---|---|---|
| `corretagem_fii` | 11 / 24 | **um só: 0,0** |
| `exercicio_opcao_pct` | 4 / 24 | **um só: 0,005** |
| `mesa_minimo` | 4 / 24 | 20 · 25 · 50 — o único que varia |
| `corretagem_etf_pct` | 24 / 24 | 0,0 em 23, **0,005 na XP** |

**Dois dos três campos que você autorizou são constantes.** Uma dimensão construída
sobre eles adiciona peso ao ranking e **não muda ordenação nenhuma** — é um número que
parece medir. É a forma do `pl_medio_3a`.

### E o que estava embaixo, que é o achado

`corretagem_etf_pct: 0.0` e `corretagem_pct: 0.0` estavam escritos em **nove casas cuja
própria `fonte` diz, com estas palavras, "custos NÃO OBTIDOS"** — Clear, BTG, Bradesco,
Mirae, Órama, Guide, Necton, Vitreo, Avenue. O `corretagem_rv` delas é `null`, ou seja
*"não sei"*, e o campo vizinho traz zero.

**Zero é o melhor valor possível.** É o F-02 na letra — o mesmo defeito da BOVV11, cuja
taxa `NAO_CONFIRMADO` virava `adm_aa = 0.0` e a punha como a rota mais barata do
catálogo. Não mordeu até hoje por um acidente: **os campos eram mortos.** A sua decisão
de pôr o custo por operação no ranking é exatamente o que os acordaria, e nove casas não
pesquisadas estreariam com custo zero de graça.

**E o zero tinha um segundo andar:** `corretagem_pct: float = 0.0` era o *default do
dataclass*. Limpar só o YAML deixaria o zero morando um nível acima, pronto para voltar
na primeira casa que não declarasse o campo.

### O que foi corrigido

Os 18 zeros viraram `null`; os dois defaults viraram `None`; e `pontuar()` passou a tirar
a dimensão quando **qualquer** das duas parcelas é desconhecida — meio custo conhecido não
é um custo, e somar a metade que se sabe com um zero inventado dá um número otimista por
construção.

**Instantâneo dourado: o ranking saiu byte a byte idêntico** (`ee59cd02…`). A correção é
inteiramente inerte hoje, que é exatamente o ponto — os zeros estavam dormindo.

Três guardas, as três provadas por mutação: nenhuma casa `NAO_CONFIRMADO` pode carregar
número de custo (guarda de **classe**, não dos dois campos); o default do dataclass não
pode voltar a ser zero; meio custo não pontua.

---

## P-84 · A dimensão de custo por operação — o que a decisão 1 ainda precisa

**Classe:** `DECISAO_DE_DESENHO`. **Dono:** Osvaldo. **Gatilho:** agora; nada trava.

Com a P-83 corrigida, sobra a pergunta de desenho, e ela é sua porque envolve **peso**,
que é política declarada:

- `corretagem_fii` e `exercicio_opcao_pct` são **constantes**. O projeto já tem o
  mecanismo certo para isso e o precedente escrito: `reclame_aqui` é **exibido e nunca
  pontuado** (`politica.yaml → pontua: false, exibe: true`). Eles saem de campo morto sem
  fingir que discriminam.
- `mesa_minimo` varia (20/25/50) mas só 4 de 24 declaram, e **não dá para separar "não
  tem mesa" de "não pesquisei"**. Pontuá-lo penalizaria 20 casas pela ausência de um
  produto, não pela falta de transparência.
- `corretagem_etf_pct` é o único com cobertura real depois da P-83 (15 casas) e com um
  valor que separa: **os 0,50% da XP em ETF.** É também o que mais importa para quem
  compra ETF — e ele **não estava** nos três que você autorizou.

**A pergunta:** a corretagem de ETF entra como segunda parcela da dimensão `corretagem`
que já existe (sem inventar peso novo), ou como dimensão própria com peso declarado por
você no `politica.yaml`?

---

## P-85 · O relatório do ranking mudava de texto entre execuções

**Classe:** `BLOQUEIA_O_SISTEMA`. **FECHADA em 16/09/2026.**

Peguei tentando usar a saída do `corretoras.py` como instantâneo dourado — que é
justamente para o que ela não servia. A linha *"vencedores distintos: N — <lista>"*
juntava um `set`, e `set` de string não tem ordem **entre processos**.

**O `refinar.py` já tinha aprendido a lição e escrito o motivo** — *"Ordem ESTÁVEL. Sem
isso o instantâneo dourado acusa diferença a cada rodada e para de servir como rede"* — e
ela não atravessou de módulo para módulo. É o A-07 (funções irmãs) com o irmão sendo um
**módulo**: regra aplicada num lugar só.

A guarda roda o relatório em **subprocesso**, com `PYTHONHASHSEED` diferente — dentro de
um processo só a ordem do `set` é estável e o defeito não aparece.

---

---

## P-86 · O `chaves_orfas.py` escondia 42 de 67 chaves, e emudecia por escolha de nome

**Classe:** `BLOQUEIA_O_SISTEMA`. **FECHADA em 16/09/2026.**

A ferramenta deduplicava por **nome de folha**: a segunda ocorrência de qualquer nome no
mesmo arquivo **sumia do relatório** — nem órfã, nem lida, invisível. `bc_procedentes`
aparecia para o Itaú e calava para as outras oito casas; `variantes_permitidas` aparecia
numa estratégia e sumia em sete.

**Peguei sem procurar**, e é isso que torna o defeito caro: batizei uma chave nova
(`custo_por_operacao.e_uma_decisao_nao_uma_omissao`) com o mesmo nome de folha de uma
existente, e a **existente desapareceu da auditoria**. Uma guarda que emudece porque
alguém escolheu um nome é pior que guarda nenhuma — e o sintoma é a linha de base
**encolher**, que é a direção que parece progresso.

Corrigido para dedupe por caminho: **17 órfãs + 8 lidas-só-por-teste viraram 35 + 32.**

### Zero espécies novas, e é isso que permitiu fechar barato

As 42 escondidas são **nove espécies**, e todas já tinham o porquê escrito na linha de
base — para *uma* instância. A linha de base declarava uma e cobria N em silêncio.
Listá-las uma a uma seria copiar o mesmo motivo 42 vezes, então entrou `ESPECIES`, com
glob e o motivo escrito na espécie (precedente na casa: `test_alocacao.py` já usa
`corretora.*.e_uma_decisao_nao_uma_omissao`).

E a guarda nova **me pegou na mesma rodada**: pus `instituicoes.*.facilidade.exporta_csv`
por simetria, e o teste de *"espécie declarada que não casa com órfã nenhuma"* reprovou —
nenhuma casa declara esse campo.

`test_a_ferramenta_NAO_deduplica_por_nome_de_folha` é a guarda da guarda, com prova por
mutação.

---

## P-87 · Existe uma SEGUNDA cópia do projeto na máquina, com `.git` próprio

**Dono:** Osvaldo · **Gatilho:** nenhum — antes do próximo pacote ou sessão de nuvem ·
**Classe:** `BLOQUEIA_O_SISTEMA`

O repositório vivo é `C:\Users\osvaldo.junior\Desktop\Bastter`. Existe **outro**, em
`C:\Users\osvaldo.junior\OneDrive - VOLGA …\Área de Trabalho\Bastter`, com `.git`
próprio cujo último `index` é de **09/09/2026**, `corretoras.py` de 18 KB contra os 28 KB
do vivo, e ainda com os cinco `*-patch.py` e a pasta `pacote_segunda/` que o P-82 removeu.

**Foi essa a pasta que a sessão da nuvem recebeu como pasta conectada em 18/09**, e eu
estive a um `device_commit_files` de escrever o trabalho de três dias dentro dela. O que
impediu foi conferir tamanho e `mtime` antes de gravar — não uma guarda.

> **É a armadilha do `pesquisa-custos-2026-08/calc/` e do `pacote_segunda/` num terceiro
> andar, e é o pior dos três:** os dois primeiros moram *dentro* do repositório e o
> `test_p82_copia_do_projeto.py` os mede pelo índice do git. Este mora **fora**, tem git
> próprio, e nenhum teste do projeto pode alcançá-lo — um teste mede o repositório em que
> roda, e o problema é justamente haver dois.

**Contexto, corrigido por ele em 18/09:** tirar o projeto do OneDrive **foi decisão
tomada e executada** — a pasta do servidor é o original abandonado, não um espelho vivo.
Isso explica a pasta e **não a torna inofensiva**: ela continua sendo um repositório
completo, com `.git` próprio, no caminho que a nuvem recebeu como pasta conectada.

**O que fazer (decisão dele, não minha):** ou a cópia do OneDrive é apagada, ou é renomeada
para algo que não se confunda (`Bastter-ARQUIVO-09set`), ou o `Desktop\Bastter` passa a ser
o único caminho aceito. Enquanto houver duas, toda sessão de nuvem precisa conferir qual
recebeu — e **P7: conferência que depende de alguém lembrar não é conferência.**

---

## P-88 · ~~Ninguém mediu a dependência serial~~ **MEDIDA em 19/09 — existe, e são ~8%**

**Dono:** próxima sessão (integrar no `multiplicidade.py`) · **Gatilho:** quando o
`multiplicidade.py` estiver em mãos · **Classe:** `DECISAO_DE_DESENHO` ·
*(laudo em `auditoria/P88-DEPENDENCIA-SERIAL.md`)*

> **A previsão desta pendência estava certa.** Ljung-Box(12) no **resíduo** — a série que o
> bootstrap de fato reamostra: **HML p = 0,031** (tem dependência), **SMB p = 0,166** (não
> tem). O SMB virou o **controle**, e ele não foi construído: estava ali, com a mesma `n`, a
> mesma `k` e o mesmo procedimento.
>
> | L | blocos | HML | vs iid | SMB (controle) | vs iid | líquido |
> |---|---|---|---|---|---|---|
> | 1 | 306 | 3,1099 | — | 2,8473 | — | — |
> | 2 | 153 | 3,2909 | +5,8% | 2,7736 | −2,6% | **+8,4%** |
> | 3 | 102 | 3,3133 | +6,5% | 2,7695 | −2,7% | **+9,3%** |
> | 6 | 51 | 3,2145 | +3,4% | 2,6991 | −5,2% | **+8,6%** |
> | 24 | **13** | 2,9624 | −4,7% | 2,7573 | −3,2% | −1,6% |
>
> **Sinais opostos na faixa informativa** (L = 2 a 8, ≥ 39 blocos). Corte iid 3,1099 →
> **~3,36**; folga do HML de −0,175 → **~−0,45**. O veredito **não muda**, e a conclusão
> **não exige escolher um L** — que era exatamente o que esta pendência pedia evitar.
>
> **Sem o controle, a leitura teria sido a oposta:** em L = 24 são 13 blocos distintos, o
> reamostrador degenera e o corte cai **por artefato**. Eu teria lido *"a dependência não
> importa"*, a conclusão errada pelo motivo errado.
>
> `auditoria/p88_block_bootstrap.py` + 18 testes. **`L=1` reproduz 3,1473**, o número
> registrado em 18/09 — sem essa calibração, um corte maior não provaria nada: poderia ser a
> minha implementação diferindo da registrada.

**O que continua aberto, e é pouco:**

1. **Romano-Wolf não entrou.** O container tinha a versão do `backtest_h1_h3.py` *anterior* a
   18/09, sem `bootstrap_conjunto`. Integrar `corte_*_por_bloco` no
   `alocacao/multiplicidade.py` é o passo, e só então o número absoluto vale para as duas
   correções.
2. **O "líquido" é inferência, não medição** — supõe que o artefato da degeneração é igual nas
   duas séries (plausível: mesma `n`, mesma `k`, mesmo procedimento). `NAO_CONFIRMADO` para os
   ~3,36; **MEDIDO** para o sinal, a faixa e o veredito.
3. ~~A última versão do teste não foi executada.~~ **Executada: 18 passed, ruff limpo** —
   mas o caminho até lá rendeu um achado de método, registrado na §6 do laudo: quando o shell
   voltou, a suíte falhou com o **nome antigo** do teste, e foi essa mensagem que revelou que
   **a chamada que aplicava a correção era justamente a que o shell havia derrubado.** Eu
   documentei como *"corrigido, sem rodar"* algo que estava *"não corrigido, sem rodar"* —
   e foi a nota de incerteza que fez o par ser conferido em vez de acreditado.

<details><summary>o texto original desta pendência, mantido</summary>

O corte de 18/09 sai de um bootstrap que sorteia **meses soltos**. Se os fatores tiverem
dependência serial, a distribuição da estatística é outra e o corte medido está
**subestimado** — na mesma direção do achado (o HML fica ainda mais longe de sobreviver),
o que torna a limitação conservadora e não convidativa.

Medir pede *block bootstrap* com blocos de comprimento declarado. O custo é baixo; o que
falta é escolher o comprimento do bloco **com medição de sensibilidade**, e não por
convenção — senão troca-se uma suposição tabelada por outra.

</details>

---

## P-89 · O corte de m = 8 é `NAO_CONFIRMADO`, e a margem é menor que o ruído

**Dono:** próxima sessão · **Gatilho:** se alguém quiser julgar as oito pré-registradas ·
**Classe:** `DECISAO_DE_DESENHO`

Em m = 8 o corte medido é 2,9337 e o `t` do HML é 2,9351: **0,0014 de diferença**, contra
um desvio de reamostragem de ~0,075. O veredito ali não é "rejeita" nem "não rejeita" — é
`NAO_CONFIRMADO`, e é assim que está escrito. Fechar exige mais repetições (100.000 já
estabilizam a terceira casa) ou aceitar que a família de interesse são os dois `m` que o
sistema calcula, e não o 8 que ninguém usa.


## P-90 · Obter os custos das casas que a coleta não alcançou

**Dono:** próxima sessão de pesquisa (nuvem, com subagentes) · **Gatilho:** nenhum —
está pronta para começar · **Classe:** `BLOQUEIA_O_SISTEMA`

Correção dele, 18/09: *"se a informação existe e você não conseguiu, o item não deve ser
excluído — mas o problema de conseguir a informação deve ser solucionado."*

A metade "não excluir" está feita (`auditoria/P90-INFORMACAO-NAO-OBTIDA.md`). **Esta
pendência é a outra metade**, e ela existe porque o campo `pegadinha` guardava um
fracasso do meu raspador como se fosse característica da instituição:

| casa | o que `pegadinha` diz | o que isso descreve |
|---|---|---|
| BTG Pactual digital | *site é SPA sem HTML servido* | o meu leitor, não o BTG |
| Bradesco / Ágora | *PDF de tarifas não pôde ser baixado* | idem |
| Mirae Asset | *HTTP 403; DNS não resolve* | idem |
| Órama, Guide, Necton, Vitreo | SPA / 404 / IPv6 / DNS | idem |

**A regra que sai disto, e ela é geral:** *"não consegui obter"* é um estado do
INSTRUMENTO e tem de ser registrado como tal — com a data da tentativa, o método usado e
o erro. Escrito no campo que descreve a instituição, ele vira, seis meses depois, um fato
sobre ela. É a mesma classe do C-01 (número plausível em prosa que ninguém precisa medir
para repetir).

**Primeira tarefa, e ela não é raspar de novo:** listar as fontes que **não dependem do
site da corretora**. O precedente já existe e é do próprio projeto — `solidez` e
`reclamacoes` dessas casas foram obtidas assim, de balanço e do Ranking de Reclamações do
BCB, e são justamente as que sobreviveram ao fracasso. Candidatos a verificar, nenhum
confirmado: tabela de tarifas na página institucional de RI, taxas de custódia
publicadas pelo Tesouro Direto por instituição habilitada, e a lista de participantes da
B3. **Não registrar nenhuma como fonte antes de abrir e ler.**

---

## P-91 · Comparar retrato de CVM por hash de arquivo produz falso positivo

**Dono:** próxima sessão · **Gatilho:** antes de escrever a rotina semanal automática ·
**Classe:** `DECISAO_DE_DESENHO`

Medido em 18/09 (`auditoria/CVM-PRIMEIRO-RETRATO.md`): o `dfp_cia_aberta_2024.zip` mudou
de sha256 em 14 dias **sem nenhuma mudança de dado** — a CVM regerou o arquivo e 8 linhas
de 94.517 trocaram de posição. `sorted(a) == sorted(b)`.

A estratégia do `CLAUDE.md` §11.6 — *"baixar, comparar, guardar o delta"* — declararia
uma reapresentação aqui e comitaria ruído toda semana. `fase0/manifesto_cvm.py --comparar`
já faz a comparação certa (normalizada por ordem, quatro vereditos nomeados). **O que
falta é a decisão de desenho:** a rotina semanal guarda o delta de *quê* — do ZIP, do CSV,
ou das linhas com chave `(CNPJ, DT_REFER, ORDEM_EXERC, conta)`? A terceira é a única que
sobrevive a uma mudança de separador ou de codificação, e é a mais cara.

---

## P-92 · O acervo tem UM ano de preço, e ele é a régua de todo o resto

**Dono:** Osvaldo (download) · **Gatilho:** antes de qualquer execução do pré-registro ·
**Classe:** `BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

`fase0/ajustar.py` existe e foi medido contra o mercado (`auditoria/C02-O-DEGRAU-MEDIDO.md`):
a série ajustada de **2023** está de pé, com 293 datas-ex medidas e controle em 86.736
pares. O módulo não tem mais nada a fazer — **o que falta é preço.**

Um ano não é backtest. E há um segundo ganho, que é o mais barato do projeto hoje:

| ano | eventos de QUANTIDADE que ele corrobora |
|---|---|
| 2025 | 31 |
| 2021 | 19 |
| 2023 (no acervo) | **1** |

A leitura percentual do campo `factor` — a decisão do C-01 — tem hoje **uma** corroboração
de preço. Com 2021 e 2025 ela passa a ter **51**, e são os casos **grandes**, que o preço
resolve com folga. Baixar dois arquivos fecha uma questão metodológica *e* amplia a
cobertura da data ex, sem uma linha de código nova: o `calendario.py` e o `ajustar.py` leem
o que estiver na pasta.

**A regra que vale a pena carregar:** ordem por evento de quantidade, não por
proximidade — 2025 antes de 2024.

---

## P-93 · Treze eventos de 2023 não encontram ticker, e o preço deles fica sem ajuste

**Dono:** próxima sessão · **Gatilho:** antes de usar a série ajustada em qualquer conta ·
**Classe:** `BLOQUEIA_O_SISTEMA`

O A-03/A-04 chegou ao preço. A emissora troca de código, o evento chega com o código
**novo** e o preço de 2023 está sob o **antigo**:

| emissora no evento | ticker de 2023 | eventos dentro da janela |
|---|---|---|
| AXIA (ON, PNA, PNB) | ELET3 / ELET5 / ELET6 | 3 |
| AZZA (ON) | ARZZ3 | 4 |
| ISAE (ON, PN) | TRPL3 / TRPL4 | 4 |
| MOTV (ON) | CCRO3 | 2 |

`ajustar.py` acusa os 13 e sai com código ≠ 0 — **e não remenda**, porque não há a quem
atribuir a marca: as séries de ELET3, ARZZ3, TRPL4 e CCRO3 saem `AJUSTADO` ou
`SEM_EVENTO_CAPTURADO` sem que nada nelas diga que falta um provento.

**O que resolve não é casar nome parecido** — seria o A-01 outra vez, dado do ativo errado
com aparência perfeita. É a ponte ticker↔`codeCVM`↔data, que o A-03 já pediu por outro
motivo: o `codeCVM` vem no mesmo objeto do suplemento e é **estável quando o ticker não é**.

---

## P-94 · O evento na borda desloca o nível e não aparece em teste nenhum — achado A-08

**Dono:** próxima sessão · **Gatilho:** quando o SEGUNDO ano de COTAHIST entrar no acervo ·
**Classe:** `BLOQUEIA_O_SISTEMA`

Oito eventos com `ultimo_dia_com_direito = 28/12/2023` — o **último pregão observado**. A
data ex é 02/01/2024, que o calendário não alcança, então não foi derivada, então o fator
não foi aplicado. Ele multiplicaria a série **inteira**: nenhum retorno de dentro de 2023
muda, e o **nível** fica deslocado.

**É o único defeito do módulo que não muda número nenhum hoje.** Não aparece no degrau, não
aparece no controle, não aparece na suíte. Aparece na hora de emendar 2023 com 2024 — com
um salto artificial exatamente na virada do ano. Sete tickers marcados `NIVEL_INCERTO`:
B3SA3, CMIN3, ENGI3, ENGI4, ENGI11, ITUB3, ITUB4.

**O que NÃO é isto**, e a distinção é o achado: 1.368 eventos têm data ex *posterior* à
janela e também não entraram. Isso é **propriedade** do ajuste retroativo — ele reescala o
passado a partir do fim da série, então todo ano novo reescala tudo. Contar os dois juntos
poria 1.368 linhas no relatório e ensinaria a ignorá-lo.

**Ao entrar o ano seguinte, a borda resolve sozinha** (o calendário passa a alcançar a data
ex). O que esta pendência guarda é a **conferência**: o número de `NIVEL_INCERTO` tem de
cair para zero na emenda, e se não cair é porque a borda mudou de lugar em vez de fechar.

---

## P-95 · O COTAHIST escreve a data ex, e o layout publicado não lista todas as marcas

**Dono:** próxima sessão · **Gatilho:** nenhum — vale como conferência barata a qualquer
momento · **Classe:** `DECISAO_DE_DESENHO`

Achado lateral de 18/09, e ele é gratuito: o campo **ESPECI** do COTAHIST não é só
`ON`/`PN` — carrega a marca de ex (`ON  ED  NM`, `PN  EJ  N1`, `ON  EB  NM`, `ON  EG`).
Medido: em **284 das 293** datas ex derivadas do calendário, o ESPECI muda exatamente
naquele dia, contra uma taxa de fundo de **1,59%** nos 86.736 pares sem evento; e em
**nenhuma** das 293 o dia ex vem sem marca. As 9 restantes são datas ex consecutivas, em
que a véspera já estava marcada — inconclusivas, não contrárias.

**É uma terceira fonte para a data ex, dentro do mesmo arquivo de preço, que não depende de
preço nenhum.** Hoje ela fica em bruto em duas colunas do `degrau_datas_ex_*.csv`, para
conferência humana, e não entra em conta nenhuma.

**O que impede usá-la, e é o mesmo padrão do A-05:** usar exige enumerar as marcas, e a
tabela ESPECI do layout publicado está **incompleta** — 2023 traz `EX`, `EC`, `EBG`, `ERC`,
`EDG`, `ERG`, `EDC` e `EDS`, que ela não lista. A enumeração tem de sair do **dado
observado**, com falha ruidosa no que estiver fora dela, e o `docs/fontes/SeriesHistoricas_Layout.md`
precisa registrar que a tabela dele não é exaustiva — hoje o arquivo diz que as tabelas
incompletas são as de CODBDI e TPMERC, e a de ESPECI foi transcrita como "integral".


## P-96 · ~~Ano fechado do COTAHIST muda?~~ **FECHADA em 18/09 — não muda, medido**

**Dono:** Osvaldo (download) · **Gatilho:** junto com o download dos quatro anos ·
**Classe:** `DECISAO_DE_DESENHO` · ⚙ **exige o desktop**

A limitação `captura_do_cotahist_passa_por_captcha` (política 1.21.0) diz que o custo do
portão manual é **um número fixo de cliques, uma vez** — e diz isso apoiada numa
suposição minha: *ano fechado não muda*. **A B3 não afirma isso em lugar nenhum**; as
duas páginas públicas não publicam política de atualização (lido em 18/09/2026).

> **18/09 — a medição aconteceu sozinha.** O download dos 41 anos rebaixou o
> `COTAHIST_A2023.ZIP` e ele veio com **70.216.090 bytes — exatamente o tamanho do que
> está no acervo desde 04/09.** Falta uma linha para fechar:
>
> ```powershell
> Get-FileHash "docs\fontes\series-historicas-cotahist\COTAHIST_A2023.ZIP" -Algorithm SHA256
> #   ad1603788d78aaa1de806498572277f1d9443f88ae116452751b5800cb23523e  -> congelado
> ```
>
> Tamanho igual é evidência forte e não é prova: dois arquivos do mesmo tamanho podem
> diferir. O hash decide.
>
> **FECHADA — o hash foi medido no arquivo rebaixado:**
>
> ```
> ad1603788d78aaa1de806498572277f1d9443f88ae116452751b5800cb23523e   rebaixado 18/09
> ad1603788d78aaa1de806498572277f1d9443f88ae116452751b5800cb23523e   acervo     04/09
> ```
>
> **Idênticos.** Ano fechado do COTAHIST é congelado — deixou de ser suposição minha e
> virou medição, com 14 dias de intervalo.

- **Igual** → congelado, medido em vez de suposto. A P7 encolhe para o ano corrente.
- **Diferente** → existe rotina periódica, ela é manual, e a limitação muda de peso.

E vale o aprendizado da CVM antes de concluir: **hash diferente não é reapresentação.**
`manifesto_cvm.py --comparar` separa `REORDENADO` de `REAPRESENTADO`; na CVM, comparar
por hash deu **100% de falso positivo** em 18/09.

---

## P-97 · A procedência do `COTAHIST_A2023.ZIP` que já está no acervo

**Dono:** Osvaldo · **Gatilho:** antes de escrever o `origem.csv` do b3 ·
**Classe:** `DADO_DE_UM_USUARIO`

O arquivo está em `data\bronze\b3\` desde 04/09/2026 e **não se sabe de onde veio**.
O manifesto conta isso: `P-06: 1 de 1 arquivo(s) tem sha256 e NAO tem de onde vieram`.

Não dá para supor que veio da página de séries anuais — inventar procedência no arquivo
cuja única função é não inventar procedência seria o pior lugar possível para um chute.
Duas saídas legítimas: ele confirma a origem, ou a linha do `origem.csv` registra origem
**desconhecida** e a contagem continua em 1 até alguém rebaixar o arquivo por um caminho
conhecido. A segunda é honesta; a primeira é melhor.

---

## P-98 · 507 MB entraram em `docs/fontes/` sem casar com nenhum padrão do `.gitignore`

**Dono:** próxima sessão (feito: guarda escrita) · **Gatilho:** **antes do próximo
`git add`** · **Classe:** `BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

O acervo COTAHIST (6,0 GB) foi baixado para `docs\fontes\series-historicas-cotahist\`
— **dentro do repositório, que é público.** O `.gitignore` cobria
`docs/fontes/**/*.zip` e `**/*.txt`, e por isso 65 dos 81 arquivos estavam cobertos.

**Os 16 de 1986–2001 não.** O ZIP da B3 muda de convenção no meio da série e esses anos
saem **sem extensão** (`COTAHIST.A1986`, `COTAHIST_A2001`). São **507 MB** que padrão
nenhum pegava, a um `git add -A` de virar histórico permanente — blob commitado não se
apaga com `git rm`, só com reescrita de histórico, e depois de um push nem isso.

**É a P-82 pela segunda vez em dois dias:** *regra escrita numa lista de nomes não é
regra, é lembrete.* Lá era uma lista de **pastas**; aqui é uma lista de **extensões**,
e estendê-la exigiria saber de antemão como um publicador nomeia o conteúdo de um ZIP
de 1986. Ninguém sabe.

**Fechado nesta sessão, nos dois níveis:** `.gitignore` ganhou a pasta, e
`alocacao/test_p98_acervo_fora_do_indice.py` mede **tamanho no índice do git** — bytes
não dependem de alguém ter acertado o nome. 5 testes, com prova por mutação usando os
números reais do incidente. **Falta rodar `git status` antes do próximo commit** para
confirmar que nada já entrou.

---

## P-99 · ~~O COTAHIST muda de convenção de nome~~ **CONSERTADA em 19/09, falta aplicar**

**Dono:** Osvaldo (copiar os arquivos) · **Gatilho:** segunda 21/09, passo 1 de
`SEGUNDA-21.md` · **Classe:** `BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

> **Consertada em 19/09, e eram TRÊS defeitos, não um.** Medido nos 9 ZIPs que estavam no
> container: **7 de 9 devolviam ZERO registros em silêncio**; `arquivos()` faria quinze anos
> disputarem a chave `COTAHIST`; e `pregoes()` **morria inteiro** num `BadZipFile` — o 2026
> truncado apagava o calendário do acervo todo.
>
> `fase0/calendario.py` + `fase0/test_calendario_p99.py` (24 testes). **Instantâneo dourado:
> 2023 em 248 pregões, sha256 `e4a9d81d…d551c`, idêntico ao de 18/09.**
>
> **Risco declarado:** eu não pude ver `test_calendario.py` nem `test_ajustar.py` — nunca
> passaram pelo container. Se algum falhar, é o contrato do `registros()`, que agora confere
> cabeçalho. Já reduzi: arquivo que começa direto em registro de cotação é aceito, e a
> primeira linha não se perde. Mas testei contra a minha suposição, não contra eles.

| faixa | nome dentro do ZIP |
|---|---|
| 1986–2000 | `COTAHIST.A1986` … `COTAHIST.A2000` — **ponto**, sem extensão |
| 2001 | `COTAHIST_A2001` — **sublinhado**, sem extensão |
| 2002–2025 | `COTAHIST_A2002.TXT` — sublinhado **e** `.TXT` |

> **18/09 — medido, e a notícia é boa: o problema é SÓ o nome.** Abri os três ZIPs e
> comparei o conteúdo. O layout é **idêntico** nos 41 anos — 245 posições, CRLF,
> `TIPREG=01`, `DATA` em 3–10, `CODNEG` em 13–24, `MOEDA` em 53–56:
>
> ```
> COTAHIST_A1986.ZIP -> 'COTAHIST.A1986'      245 pos.  '00COTAHIST.1986BOVESPA 19991210'
> COTAHIST_A2001.ZIP -> 'COTAHIST_A2001'      245 pos.  '00COTAHIST.2001BOVESPA 20060331'
> COTAHIST_A2023.ZIP -> 'COTAHIST_A2023.TXT'  245 pos.  '00COTAHIST.2023BOVESPA 20231228'
> ```
>
> **A correção certa não é uma lista de nomes** — seria o mesmo erro da P-98 e da P-82
> pela terceira vez. É ler o **membro único do ZIP** (`namelist()[0]`) e validar pelo
> conteúdo: cabeçalho `00COTAHIST.<ANO>` e registros de 245 posições. Nome é a
> propriedade que varia; o layout é a que identifica.

`fase0/calendario.py` varre ZIP **ou** TXT; `ajustar.py` lê o que estiver na pasta.
**Nenhum dos dois encontra os 16 primeiros**, e o modo de falha é o mais caro do
projeto: eles não quebram — **não veem o ano.** A série passaria a começar em 2002 sem
ninguém ter decidido isso, e nenhum teste de "veio número?" notaria.

A correção é a do A-05: enumeração vinda do **dado observado**, com falha ruidosa fora
dela. E um teste que liste os anos efetivamente lidos e compare com os anos presentes
na pasta — **contagem que decai**, não suposição.

---

## P-100 · O `COTAHIST_A2026.ZIP` não é um ZIP completo

**Dono:** Osvaldo (rebaixar) · **Gatilho:** quando o ano corrente for necessário ·
**Classe:** `DECISAO_DE_DESENHO` · ⚙ **exige o desktop**

> **21/09 — agora bloqueia a família ML.** O teste do `preregistro-ml-v1.md` vai de
> jan/2020 até o fim do COTAHIST; sem 2026 íntegro, ou o período termina em dez/2025 escrito
> no §2, ou a família espera este arquivo. Ver P-107.

38.328.935 bytes baixados; a extração falha com *"O registro Final de Diretório Central
não foi localizado"* — o fim do arquivo não chegou.

> **18/09 — medido o que o arquivo é.** Não é página de erro nem HTML: o cabeçalho é
> `PK\x03\x04`, com o membro `COTAHIST_A2026.TXT` declarado e **flag 0x0808** — bit 3
> ligado, isto é, **ZIP em streaming**, com os tamanhos num descritor no fim. É a forma
> de quem **gera o arquivo na hora**, coerente com o ano corrente ainda estar aberto. O
> download foi **cortado**, não recusado.
>
> Consequência para a rotina automática: um ZIP em streaming **não dá para validar pelo
> tamanho esperado**, porque não há tamanho esperado. O coletor tem de **abrir o ZIP e
> ler o membro até o fim** antes de aceitar o arquivo — conferir depois de gravar é
> conferir tarde.

**É a armadilha do `CLAUDE.md` §11.6, e desta vez ela gritou por sorte do formato:**
*"um download que devolve 404 mais um unzip vazio produzem 'nenhuma mudança',
indistinguível de 'a B3 não mudou nada'"*. Um ZIP truncado quebra alto; um TXT truncado
teria entrado calado. **Ausência de mudança precisa ser afirmada, nunca inferida da
ausência de erro** — e isso vale agora para o coletor que a rotina automática vai usar:
ele tem de conferir o ZIP antes de aceitar o arquivo, não depois.

---

## P-101 · Quatro moedas no acervo, e uma quebra de 2,75x que nenhum evento societário explica

**Dono:** próxima sessão · **Gatilho:** **só quando a janela do `ajustar.py` passar de
04/07/1994** · **Classe:** `BLOQUEIA_O_SISTEMA` · *(achado C-03)*

> **19/09 — MEDIDA e instrumentada, ainda NÃO aplicada.** Nasceu `fase0/moeda.py`: varre o
> acervo, acha as fronteiras de `MODREF`, mede o fator pela razão do mesmo `CODNEG` com o
> controle do dia anterior ao lado, e devolve `QUEBRA_MEDIDA` / `SEM_QUEBRA` /
> `NAO_CONFIRMADO`. 19 testes.
>
> ```
> COTAHIST_A1986  19860227->19860304  CR$->CZ$    274  1.1973  ctrl 1.0000 (n=339)      --  SEM_QUEBRA
> COTAHIST_A1989  19890113->19890118  CZ$->NCZ$   198  0.9677  ctrl 1.0000 (n=307)      --  SEM_QUEBRA
> COTAHIST_A1990  19900313->19900319  NCZ$->CR$     2  0.7142  ctrl 1.0000 (n=238)      --  NAO_CONFIRMADO
> COTAHIST_A1994  19940630->19940704  CR$->R$     136  0.3644  ctrl 1.0106 (n=251)  2.7440  QUEBRA_MEDIDA
> ```
>
> **Ele NÃO aplica a reexpressão, e há um teste que prende isso.** Escolher a base —
> reexpressar tudo para R$? manter cada ano na moeda dele? — é **decisão de desenho sua**,
> e a P6 manda deixar a lacuna declarada em vez de inventar critério. Mesmo desenho do
> `refinar.py` com o `FACTOR_AMBIGUO`.
>
> **Achado lateral, e ele veio de imprimir o `n` do controle:** nas fronteiras de 1986,
> 1989 e 1990 o controle mede **1,0000 exato** com 339, 307 e 238 pares — em plena
> hiperinflação. Não é mercado estável: é a **maioria dos papéis repetindo o preço** do dia
> anterior, mercado raso. Isso *fortalece* a leitura — se o dia comum de 1986 mede 1,0000,
> a fronteira medindo 1,1973 teve mais movimento que o normal, e ainda assim nada perto de
> 1.000x.

> **19/09 — NÃO está no caminho crítico hoje, e isso é decisão de ordem, não de mérito.** O
> próximo passo é `ajustar.py` sobre **2021–2025**, e essa janela está **inteira em `R$`**.
> Pôr a P-101 na frente por ser o achado mais novo seria escolher tarefa pelo frescor — o
> erro que a P-44 registra.
>
> E a explicação do achado avançou: o header mostra que 1986–1995 foram **todos gerados em
> 19991210**. `MODREF` é **rótulo histórico**, não a unidade gravada — ver
> `docs/fontes/b3-cotahist-leiaute.md` §4.

A série agora começa em 02/01/1986 e atravessa seis planos econômicos. O campo `MOEDA`
(posições 53–56) muda **dentro do mesmo arquivo anual**: `CR$`, `CZ$`, `NCZ$`, `R$`.

**Medido — razão do mesmo ticker, mercado à vista, com controle do dia anterior:**

| troca | pares | mediana | |
|---|---|---|---|
| 1986 Cruzado (1.000:1) | 274 | 1,197 | **sem quebra** — já reexpresso |
| 1989 Verão (1.000:1) | 198 | 0,968 | **sem quebra** |
| 1993 Cruzeiro Real (1.000:1) | 182 | 0,998 | **sem quebra** — e a `MOEDA` nem distingue as duas |
| 1990 Collor | **2** | — | `NAO_CONFIRMADO` — o mercado parou |
| **1994 Real (CR$ 2.750 = R$ 1)** | 136 | **0,364** | **QUEBRA**, contra controle de 1,011 |

**Três das quatro trocas não deixam quebra.** A suposição natural — *"toda troca de moeda
é uma quebra"* — erra em 3 de 4, e só a medição diz qual. A tabela de planos econômicos
teria acusado quatro e acertado uma.

**A do Real é real:** 1/0,364 = **2,744**, consistente com os 2,750 da lei, com o resto
sendo variação de um pregão. E ela entra na série ajustada como **−63,6% no mercado
inteiro, em um dia, sem causa** — porque troca de moeda não é evento societário, não tem
`factor`, não tem data-ex e não existe no silver.

**É o F-02 na forma mais cara:** não é insumo ausente virando zero — é insumo
**presente, correto e anunciado** que ninguém lê. E é o C-01 em escala de mercado.

**O que falta, e é pouco:** varrer os 33 arquivos não abertos para fechar a enumeração
`OBSERVADO` de `MOEDA`; medir o fator de cada quebra encontrada (nunca tabelar); e decidir
se a série utilizável começa em **04/07/1994** ou em **02/01/1986** — decisão que entra em
`limitacoes_declaradas` ou vira trabalho, mas não fica em silêncio.

---

## P-103 · O `CLAUDE.md` afirmava tokens sem conta, e um plano externo calibrou nele

**Dono:** próxima sessão · **Gatilho:** nenhum — fechada no que dava para fechar ·
**Classe:** `DECISAO_DE_DESENHO` · *(retratação na §11.4; laudo em
`auditoria/AUDITORIA-PLANO-DE-TOKENS.md`)*

A §11.4 declarava a leitura de sessão em **"~26 mil"** antes do corte de 06/09 e
**"~13 mil"** depois. Medido em 19/09 com `tiktoken`: a razão real deste repositório é
**19,0 tokens/linha**, logo os valores são **~38.400** e **~19.900** — erros de **+48%** e
**+53%**, os dois na direção que faz o projeto parecer mais enxuto.

**O custo não foi interno.** Três planos de otimização de tokens foram escritos em 19/09, e
um deles declarou ter **calibrado a própria razão empírica** nos "~13 mil" da §11.4. Ele
errou a leitura inicial por **90%** — e a conta dele estava certa; a fonte é que não
estava. **Número plausível em prosa, citado por terceiro como fonte: C-01 na camada do
token.**

**Fechado no processo, não na tabela:** `auditoria/tamanho_do_contexto.py` + 8 testes, com
prova por mutação. A §11.4 não afirma mais valor — aponta para o comando.

**O que a medição abriu e continua aberto:**

| # | o que | classe |
|---|---|---|
| 1 | ~~O cache não foi medido~~ **FECHADO em 19/09 na fonte oficial, e ele me derrubou.** O write é **2,0x** e o read 0,1x; como o fator incide sobre todo o prefixo, **cortar X% corta X% do custo, com cache ou sem** — medido, **−25%**. A inversão de prioridade que eu anunciei não existe. O risco do split é a **janela de 20 blocos**, não o prefixo. `auditoria/CACHE-E-O-CORTE.md` | — |
| 2 | **O variável não tem instrumento.** Resposta, saída de ferramenta e arquivo reescrito são o que custa integral em todo turno, e eu não os meço | `DECISAO_DE_DESENHO` |
| 3 | **A §11.5 está `NAO_CONFIRMADO`** — ordenação sem número, e o título dizia "medido" | — |
| 4 | **`## Fechadas` = 7.457 tokens** (7,7% da leitura). Mover para `FECHADAS.md` é o único item de tamanho com número verificado | `DECISAO_DE_DESENHO` |
| 5 | ~~49% do `CLAUDE.md` são blocos `>`~~ **DECISÃO C EXECUTADA em 19/09.** Critério dele: *otimização sem perder contexto* → triagem por **função**, não por percentual. Saíram 962 linhas e **20.085 tokens** (os 30 achados de 06/09–18/09); ficou um **índice** com a regra de cada um. **−17.816 tok, −33,7% do arquivo**, e **26/26 achados com endereço, medido** | — |
| 6 | **P-45, P-46 e P-53 têm gatilho vencido há 13 dias** (push, Fase 0, `data/bronze/`). Os três "pilares" de um dos planos são essas três pendências. **O problema não é falta de plano: é que nada dispara o gatilho** — P7 | `BLOQUEIA_O_SISTEMA` |

> **O achado de método, e vale para além de token:** a regra do C-01 (*"achado só entra com
> a conta escrita"*) é de 12/09; a §11.4 é de 06/09. **Regra nova não audita o passado
> sozinha.** Nenhum instrumento do projeto varre prosa antiga procurando número sem
> procedência — e a §11.4 sobreviveu treze dias por isso, com a regra que a condenava
> escrita dezoito parágrafos acima.

---

## P-104 · Vinte e quatro achados são citados só em código, e podem não ser achados

**Dono:** próxima sessão · **Gatilho:** quando o `ACHADOS.md` estiver em mãos ·
**Classe:** `DECISAO_DE_DESENHO` · *(levantado por `auditoria/achados_ancorados.py`)*

A guarda que nasceu com a Decisão C varreu o repositório e achou **45 códigos citados sem
definição em `.md` nenhum**. Vinte e um caem quando o `ACHADOS.md` entrar na árvore — ele
não estava. **Os outros 24 são citados SÓ em código:**

```
B-05  B-06  B-07  B-08  D-1   H-02  K-04  K-05  K-08  K-11
V-02  V-03  V-04  V-05  V-06  V-07  V-08  V-09  V-10  V-12
V-13  V-14  V-15  Z-01
```

**E parte deles provavelmente não é achado.** `K-04` aparece com as teses (`teses.yaml`,
`tese.py`), e os `V-*` aparecem no changelog do `politica.yaml` como itens de um laudo de
agosto. **Namespaces diferentes com a mesma forma.**

**Não os pus na linha de base, e a razão é a régua §5-B:** *medir levanta o candidato; quem
o promove é a leitura* — e eu não tenho o `ACHADOS.md` nem os laudos de agosto para ler.
Jogá-los na exclusão sem motivo seria pior que deixá-los acusados: viraria **cobertura
falsa**. Ficam nomeados em `CANDIDATOS_19_09`, com um teste que impede que virem linha de
base sem o motivo escrito.

**O que decidir:** para cada um, ou o motivo (*"é tese"*, *"é item do laudo de agosto"*) e a
saída para `NAO_SAO_ACHADOS`, ou a constatação de que é achado de verdade — e aí **é um nome
que o código cita e ninguém pode consultar**, que é o defeito que esta guarda existe para
pegar.

---

## P-105 · ~~O leiaute do COTAHIST estava em Python~~ **FECHADA em 19/09 — defeito meu**

**Dono:** — · **Gatilho:** — · **Classe:** `BLOQUEIA_O_SISTEMA` · *(P2 violada)*

O `fase0/calendario.py` nasceu em 19/09 com `POS_DATA = (2, 10)`, `POS_MODREF = (52, 56)`,
`LARGURA = 245` e `MODREF_OBSERVADOS = (...)` **escritos em Python**, com a procedência num
comentário. São valores de **fonte externa** — o leiaute publicado pela B3 — e a P2 é
explícita: *"todo parâmetro vive em YAML versionado, nunca em código."*

**E eu os escrevi no mesmo dia em que auditei três planos de otimização por falta de
rigor.** A procedência ficou num comentário, que é o lugar onde ela não pode ser conferida
por teste nenhum.

**Fechada:** `docs/schemas/cotahist-v02.yaml` — revisão, URL, data de acesso e o status de
cada enumeração ao lado dos valores. O `calendario.py` lê de lá e **recusa rodar sem o
arquivo** (`LeiauteAusente`), sem fallback: um fallback silencioso reintroduziria o defeito
e **funcionaria**, que é o pior resultado possível.

E a conversão 1-baseada → Python mora num lugar só, porque ela é a fonte clássica de erro
de um: o documento diz 53–56, Python quer `[52:56]`.

> **A ideia não é minha.** Veio do **terceiro plano de otimização de tokens** que você mandou
> auditar — *"schema estruturado, Knowledge Registry"* —, e era o melhor item dos três. O
> ganho dele não é token: **é a P2.** Registro a origem porque conclusão sem procedência é o
> que este projeto persegue.

---

## P-106 · ~~`modref_de()` era lida só por teste~~ **FECHADA em 19/09 — P-77 recriada por mim**

**Dono:** — · **Gatilho:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

`calendario.modref_de()` e `conferir_modref()` nasceram em 19/09 e **nenhum módulo do motor
as chamava** — só o teste. É a **P-77 na letra**: *campo que só o teste toca é campo que o
motor não usa*, e é categoria pior que órfã pura, porque tem testemunha — o teste prova o
esquema e ninguém prova o comportamento. Foi assim que a P-13 anunciou correção com a suíte
verde.

**Menos de 24 horas entre a P-77 estar escrita no `CLAUDE.md` e eu recriá-la.**

**Fechada:** `fase0/moeda.py` é o consumidor que faltava, e ele não é enfeite — é o
instrumento do C-03.

---

## P-107 · O pré-registro de ML herdou `L = 3` de uma amostra quatro vezes maior — e não tem teste de poder

**Dono:** Osvaldo (decidir) · **Gatilho:** **antes do primeiro commit de
`preregistro-ml-v1.md`** — ele vale *"a partir do commit que o contém"*; depois disso, cada
correção é uma v2 · **Classe:** `DECISAO_DE_DESENHO`

Auditoria completa em `auditoria/AUDITORIA-PREREGISTRO-ML-V1.md`. Medido com o instrumento
da P-88 sobre o NEFIN recortado a n = 80 (o tamanho do teste do ML, jan/2020 em diante):

| L | blocos | HML | SMB (controle) |
|---|---|---|---|
| 1 | 80 | 3,1045 | 4,1399 |
| **3** | **27** | 3,4598 (+11,4%) | 3,6704 (**−11,3%**) |

A faixa L = 2 a 8 da P-88 foi definida por **≥ 39 blocos** com n = 306. Com n = 80, `L = 3`
dá 27 — está **fora** da faixa pelo próprio critério que a definiu, e o controle mostra o
artefato: o corte **cai** 11% onde não há dependência. Anticonservador, na direção de
aceitar um modelo que não funciona.

**Recomendação (decisão sua):** corte operativo = **máximo entre L ∈ {1, 2, 3}**, com o motivo
escrito no §6; e um **nono teste** no §8 — poder com sinal plantado, reportado ao lado do
veredito (com c ≈ 3,1–4,1, o IC médio precisa ser ≥ 0,35–0,46 × sd para ser detectável).
Mais quatro menores na tabela §5 da auditoria. **P-100 passa a bloquear a família ML.**

**Também retratado aqui:** a minha recusa do ML em 19/09 (`AUDITORIA-PLANO-DE-TOKENS.md`
§4.5) citou DeMiguel fora do alcance dele.

---

## P-108 · ~~O `origem.csv` com BOM zerava a procedência em silêncio~~ **FECHADA em 21/09 — e o roteiro que causou era meu**

**Dono:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

O `SEGUNDA-21.md` mandava criar o `origem.csv` com `Out-File -Encoding utf8`. No Windows
PowerShell 5.1 isso grava `EF BB BF` na frente — **medido no arquivo dele: 26 bytes, os três
primeiros o BOM**. O leitor abria com `utf-8`, a primeira coluna virava `'\ufeffcaminho'`,
e o filtro `r.get("caminho")` descartava **todas** as linhas sem erro nem aviso. Ele
declararia as 41 origens e o contador continuaria em 42. É o F-02 na camada do registro.

**Fechada:** `origem_declarada()` lê com `utf-8-sig`, e cabeçalho sem a coluna `caminho`
**levanta** em vez de zerar (*origem ilegível não é origem ausente*).
`fase0/test_origem_bom.py`, 5 testes, um deles reproduzindo o leitor antigo para provar que
o defeito existia. O `origem.csv` foi escrito com as 41 linhas, sem BOM, a partir do
manifesto dele de 21/09 e da `$baseUrl` do script de download que ele colou em 18/09.

---

## P-109 · ~~O `calendario.py` de 19/09 reprovava 19 testes que eu não rodei~~ **FECHADA em 21/09**

**Dono:** — · **Classe:** `BLOQUEIA_O_SISTEMA`

O `calendario.py` de 19/09 confere o header do COTAHIST (`00COTAHIST.AAAABOVESPA …`) — é o
que pegou a P-99. Os sintéticos do `test_ajustar.py` (sem header) e do `test_calendario.py`
(header `00` + oito zeros) não existem no acervo real, e **14 + 5 testes** reprovaram. Eu
tinha declarado em 19/09 que não rodara esses testes; não tinha tentado — o repositório é
público (§5-B.15).

**E o roteiro mentia sobre o código.** O `SEGUNDA-21.md` de 19/09 dizia que *"arquivo que
começa direto num registro de cotação é aceito, e a primeira linha não se perde"*. O
`registros()` entregue não faz isso: ele exige o header e levanta. É o defeito recorrente da
casa — *um arquivo declara um comportamento que o código não tem* —, escrito por mim no
roteiro do dia em que você ia confiar nele.

**Fechada** corrigindo o **sintético**, não o leitor: os dois `_cotahist()` agora escrevem o
header real. O `calendario` continua recusando arquivo sem header, com aviso em stderr —
recusar é o que protege a P-99. Medido sobre clone do `origin/main` + entrega.

---

## P-110 · ~~Treze `.md` da raiz sem papel, e o teto de órfãos medido na árvore errada~~ **FECHADA em 21/09**

**Dono:** — · **Classe:** `DECISAO_DE_DESENHO`

`test_todo_md_da_raiz_tem_PAPEL_declarado` reprovou no repositório real: `LEIA-AGORA.md`,
`LEIA-NA-SEGUNDA.md`, `LEIA-NA-TERCA.md`, dois de prompts, `RECRIAR-REPOSITORIO.md` e sete
laudos de agosto. **Fechada:** os treze classificados `SOB_DEMANDA`, cada um com o motivo,
lido o título de cada um. **Nenhum entra na leitura de sessão.**

O teto de 46 órfãos do `achados_ancorados.py` foi medido em 19/09 numa árvore **sem** o
`ACHADOS.md`. No repositório real, com o `ACHADOS.md` já colado, também dá **46 — mas com
outros 24 códigos** (os da árvore de entrega ganharam definição; entraram os `E-10`…`E-19`
do laudo consolidado, os `T-02`…`T-05` dos escopos, `D-2`…`D-7`). O teto continua valendo,
agora **por medição no lugar certo**, e a coincidência fica escrita aqui para ninguém ler
como calibração.

**Sobra (aberta, sem prazo):** os três `LEIA-*` são roteiros vencidos. Movê-los para
`docs/historico/` limpa a raiz; é decisão sua, porque são arquivos seus.

---

## Fechadas

| # | o que era | fechada em |
|---|---|---|
| C-01, a corroboração de preço | a regra do `factor` tinha sido fechada pela **distribuição**, com UM caso de preço, e a data ex derivada também tinha UM. A série de preços ajustada não existia | 18/09 — `fase0/ajustar.py` + `fase0/test_ajustar.py` (32 testes, 8 contra o acervo). **O degrau do dia ex cai de −1,6263% (t = −9,88) para −0,0360% (t = −0,29) em 293 datas-ex**, com controle em 86.736 pares de pregões sem evento (pior divergência 1e-27, arredondamento de `Decimal`). Duas mutações presas na suíte: data ex deslocada deixa o degrau **inteiro** e cria um **falso** na véspera (+1,91%, t = +11,20); fator invertido **dobra** o degrau (−3,16%). Ver `auditoria/C02-O-DEGRAU-MEDIDO.md` |
| — | `calendario.py` era o único leitor de COTAHIST; o segundo (`ajustar.py`) ia redigitar a descoberta de arquivo e a posição da data | 18/09 — extraídos `arquivos()`, `registros()` e `data_de()`. Um fato, um dono. Instantâneo dourado de `pregoes()` antes e depois: **248 pregões, `sha256 e4a9d81d…` idêntico** |
| manifesto da CVM | gravado em `data/bronze/cvm/manifesto/` — dentro do caminho que o `.gitignore` ignora na linha 12. **Não entrou no commit `64a5c97`**, e o `CVM-PRIMEIRO-RETRATO.md` afirmava que entrava | 18/09 — destino padrão passou a ser `docs/acervo/cvm/`, achado pela raiz do repositório; `gravar()` **recusa** qualquer caminho sob `data/`. 3 testes, um provado por mutação. Encontrado lendo a lista de `create mode` do commit dele e não achando o manifesto lá |
| P-87 | uma segunda cópia do projeto na máquina, no OneDrive, com `.git` próprio parado em 09/09 — e foi a pasta que a sessão de nuvem recebeu conectada | 18/09 — **apagada por ele.** `Desktop\Bastter` é o caminho único |
| passo 1 do `PLANO.md` | CVM não baixada — o bloqueio de que os outros três marcos dependiam | 18/09 — **33 ZIPs**, DFP 2010–2026 e ITR 2011–2026, em `data\bronze\cvm\`. Acervo completo, cauda congelada incluída. Falta o manifesto (`fase0/manifesto_cvm.py --manifesto`), e sem ele o acervo é um conjunto de arquivos, não um retrato datado |
| decisão 2 de 13/09 | o corte do backtest era **1,96 por omissão** — e 1,96 é a NORMAL, num teste com 301 graus de liberdade | 18/09 — `alocacao/multiplicidade.py`: t de Student implementada em casa (sem acrescentar scipy, que mudaria a impressão do ambiente e tornaria todo resultado registrado um número novo), Bonferroni, Bonferroni sobre marginal medida e Romano-Wolf com bootstrap **conjunto**. 69 testes, com oráculo externo: tabela publicada de Student, identidade de ida-e-volta, e amostragem pelo numpy |
| decisão 3 de 13/09 | o `m` era afirmado por quem registra, e o `pesquisa_id` era renomeável | 18/09 — `alocacao/preregistro.py`: `m_executado` sai do **diário**, `m_orcado` da **soma** dos `variantes_permitidas`, `pesquisa_id` do sha256 da fonte + regra de amostra. Renomear não reinicia contador; trocar a série levanta `FonteTrocada` |
| decisão 4 de 13/09 | divergência de veredito não tinha regra, e "preservar tudo" viraria "escolha o que preferir" | 18/09 — portão em `preregistro.operativo()`, sobre **vereditos divergentes venham de onde vierem**, não só R1×Rn. Primeiro caso no mesmo dia: o HML diverge entre os dois lados do `m`. Operativo = **orçado**. `leitura` com menos de 120 caracteres não destrava |
| P-29 | `estrategias_pre_registradas` declarada ESPECIFICACAO — escrito e não ligado a nada | 18/09 — reclassificada para **REGISTRO** (67 das suas chaves são testemunho e nunca serão lidas; inventariá-las como dívida seria registrar 67 promessas falsas). O papel de ESPECIFICACAO virou **número**: `m_orcado − m_executado` = **11** testes pré-registrados que nunca foram ao dado, com teste que o prende |
| — | `politica.yaml` sem bump desde 16/09 | 18/09 — **1.19.0 → 1.20.0**, changelog com o corte medido e a retificação do HML |
| — | `ruff` acusava 1 erro em `auditoria/pares_irmaos.py` (E501), fora do portão da P-40 | 18/09 — corrigido; `ruff check alocacao fase0 auditoria` passa limpo. Um passo da **P-80**, que continua aberta (o `testpaths` ainda cobre um terço) |
| P-84 | a decisão dele de 13/09 — custo por operação no ranking — sem implementação | 16/09 — `corretagem_etf_pct` entrou como **segunda parcela** da dimensão `corretagem` (pior caso entre ação e ETF), sem inventar peso. Os outros três são **exibidos e nunca pontuados** (`politica.yaml → corretora.custo_por_operacao`), porque medidos são constantes entre quem os declara. **A tabela do ranking não mudou**, e o motivo está preso num teste: a única casa com ETF ≠ 0 é a XP, cuja dimensão já estava `None` pelo E-08 |
| P-86 | o `chaves_orfas.py` deduplicava por NOME DE FOLHA e escondia **42 de 67** chaves — a segunda ocorrência de um nome sumia do relatório | 16/09 — dedupe por caminho; linha de base recortada por **espécie** (glob + motivo), porque as 42 são nove espécies já declaradas para uma instância. Guarda da guarda com prova por mutação |
| — | `politica.yaml` sem bump de versão desde 11/09 (passo 9 do protocolo, sete commits) | 16/09 — **1.18.0 → 1.19.0**, com o changelog registrando a decisão do custo por operação e a lacuna acumulada |
| P-83 | nove casas com `procedencia: NAO_CONFIRMADO` — cuja própria fonte diz *"custos NÃO OBTIDOS"* — carregavam `corretagem_pct: 0.0` e `corretagem_etf_pct: 0.0`, e o default do dataclass também era `0.0` | 16/09 — 18 zeros viraram `null`, os dois defaults viraram `None`, e `pontuar()` tira a dimensão quando qualquer parcela é desconhecida. **Ranking byte a byte idêntico** (`ee59cd02…`): a correção é inerte hoje, e é esse o ponto — os zeros estavam dormindo até a decisão 1 acordá-los. 3 guardas provadas por mutação |
| P-85 | a saída do `corretoras.py` mudava de TEXTO entre execuções (um `set` impresso sem ordenar) e não servia como instantâneo dourado | 16/09 — ordenado; guarda roda o relatório em subprocesso com `PYTHONHASHSEED` diferente. O `refinar.py` já tinha a lição escrita e ela não atravessou de módulo para módulo |
| C-01 | `factor` dos eventos de quantidade: percentual ou multiplicador? As duas leituras produzem número e diferem por até 50x; 180 das 738 linhas do silver ficavam sem fator | 16/09 — **medido pela DISTRIBUIÇÃO**, não por um caso: os 65 desdobramentos usam 11 valores distintos que, lidos como percentual, caem em cima de razões canônicas (100→2x, 400→5x, 9900→100x). E a regra é **dupla**: no GRUPAMENTO `factor` já é o multiplicador, e é < 1. FACTOR_AMBIGUO 180 → CALCULADO 178 + FACTOR_FORA_DA_REGRA 2 (as incorporações). Instantâneo dourado: nenhuma coluna herdada mudou de valor |
| — | a coluna `data_ex` do silver guardava `lastDatePrior`, que é o **último dia COM direito** — o degrau de preço cai no pregão seguinte, e quem ajustasse por ela deslocaria tudo em um pregão | 16/09 — renomeada para `ultimo_dia_com_direito`; entraram `data_ex` derivada e `data_ex_status`. `fase0/calendario.py` tira o calendário do próprio COTAHIST do acervo (**dia com negociação é pregão**) e **recusa** fora da cobertura em vez de chutar dia útil — Carnaval e feriado estadual não estão em regra genérica nenhuma. Hoje: 1 derivada, 737 `FORA_DA_COBERTURA`; a cobertura cresce sozinha a cada ano de COTAHIST |
| P-82 | `git add -A` levou `pacote_segunda/pacote_segunda/` junto, e o git registrou as deleções como **rename para dentro da cópia** — o repositório passou a guardar uma cópia congelada de si mesmo, com um segundo `CLAUDE.md`, e a suíte continuou verde porque nenhum portão olha para fora de `alocacao/` | 16/09 — cópia removida e `test_p82_copia_do_projeto.py` mede o **índice**, não o disco. A regra já existia no `.gitignore` e era uma lista de nomes de pasta a lembrar; agora é medição |
| A-06 | `desembrulhar` não existia em `coletar_b3.py` — a lógica estava EMBUTIDA em `coletar_eventos`, e `refinar.py` importava um nome que só existia em cópia de teste | 16/09 — extraída, devolve `(dados, n_registros)` (A-07), e `coletar_eventos` a CHAMA. **Instantâneo dourado sobre os 74 arquivos do acervo real: `2127cad3…` idêntico antes e depois.** `pytest fase0` 9 falhas → 0, e `refinar.py` rodou até o fim pela primeira vez: 738 linhas |
| P-79 | três cópias da normalização (embutida, `desembrulhar`, `_normalizar` no teste) | 16/09 — uma só. O teste que comparava o TEXTO DO FONTE das duas primeiras saiu: comparar fonte é o instrumento que sobra quando não dá para comparar comportamento, e não dar era **consequência** da duplicata |
| P-77 | `aliquota_ganho` declarado e nunca lido pelo motor | 16/09 — `regime_tributario` lê; a linha saiu do `INVENTARIO` de `test_campos_mortos.py`, acusada pelo próprio teste do inventário |
| — | `alocacao.py:PONTAS_DIVERGENTES` | 16/09 — **removida**. Constante decorativa que eu criei no P-77 e nunca referenciei; os motivos são frases inteiras. A guarda de campos mortos pegou o meu próprio lixo um commit depois de nascer |
| — | DUAS guardas para o mesmo defeito Y-01/E-09 (`test_y01_yaml_duplicata.py` e `test_chaves_duplicadas.py` + `auditoria/chaves_duplicadas.py`), escritas em paralelo no mesmo fim de semana — o N-01 dentro da própria suíte | 16/09 — **fundidas**. Ficou a que usa `yaml.compose` e já estava no `testpaths`; da outra vieram os três testes que ela não tinha: a prova de que a guarda PEGA, o caso do merge, e o caso concreto do IMAB11. Fechou também a falha do P-15, sem precisar afrouxar o P-15 |
| — | `test_E08b_a_referencia_HERDA_o_relogio` adiantava o relógio escrevendo em `motor.HOJE` — **apoiava-se no defeito que a P-70 removeu** | 16/09 — **o teste estava errado, não o P-70**. Agora troca o `val` que `corretoras` usa por um espião que injeta `hoje`: prova que o aviso saiu POR ALI, não só que alguém avisou |
| — | `tributacao.ir_jcp_fonte` COMPLETO sem `fonte` no nível do nó | 16/09 — `fonte` escrita **e** a guarda `test_toda_constante_tem_procedencia` aprendeu a olhar dentro da série: se ALGUMA faixa declara fonte, todas precisam. Série meio declarada é pior que série não declarada, porque quem lê supõe que a faixa calada herda a de cima — e aqui herdar é o erro, a faixa de 18% vem de uma MP que caducou |
| — | os cinco `*-patch.py` ainda no repositório, 5 violações de ruff | 16/09 — apagados. Remendo de uma vez não é ferramenta; deixá-lo convida a rodá-lo de novo |
| — | `conferir-pacote.ps1` não rodou: política de execução + travessão `—` lido como CP1252, onde `0x94` é aspa tipográfica de fechamento e o parser do PowerShell a trata como delimitador de string | 16/09 — apagado, sem substituto. **O remédio não é um `.ps1` melhor**: `py -3.11` já funciona, não tem política de execução e aceita `encoding` explícito. E, sem zip, o script não tem função. Regra, se algum dia voltar a existir um `.ps1`: **7-bit ASCII, sem exceção** |
| — | linha de base das órfãs apodrecida (10 novas, 2 já resolvidas na lista) | 16/09 — reconferida **na máquina real**, com o porquê ao lado de cada uma; `corretagem_fii` e `exercicio_opcao_pct` saíram porque o código passa a lê-las. Abriu a P-81 |
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
| P-70 | `HOJE` fixo em `motor.py`, resolvido no import — aviso de expiração mudo desde 02/09 | 11/09 — `val()` recebe `hoje` opcional, resolvido em `dt.date.today()` NO MOMENTO DA CHAMADA; 2 testes injetam data (nunca o relógio real). **Segunda metade, no mesmo dia:** 4 de 43 `expira` estavam ENTRE ASPAS — texto, e `val()` só avisa em `dt.date`. Duas eram `cdi_aa` e `selic_aa`, reconferidas em 05/09 e reescritas com aspas: o mecanismo que o `CLAUDE.md` cita como prova estava mudo para elas. Aspas removidas (mesma data, não é renovação) + `test_P70_toda_expira_e_data_e_nunca_texto` |
| P-71 | `dividas`/`objetivos` voltavam como `dict`, motor espera dataclass | 11/09 — `estado_io.validar()` converte para `Divida`/`Objetivo` na carga; `test_p71_p72_porta_de_entrada.py` é o primeiro teste que passa por `estado_io.carregar()` de verdade. **Segunda metade, no mesmo dia:** a conversão era `classe(**x)` cru e aceitava o que o módulo existe para recusar — `taxa_am: "14,5"` entrava como TEXTO sem problema (e estourava no G1), campo faltando virava `TypeError`, chave errada sumia. E `match_empregador`/`match_verificado`, pedidos pelo `estado.exemplo.yaml`, **nunca eram lidos**. Agora cada registro passa pelo `_num()`, e os dois de match chegam ao `Estado`; 5 testes, todos falhavam antes |
| P-72 | `aporte_mensal <= 0` bloqueava `carregar()`, contradizendo a U-01 | 11/09 — só NEGATIVO bloqueia; zero vira AVISO |
| — | achado lateral: `Estado(**estado_io.carregar()[0])` nunca funcionou — `d` carregava `reserva_empenhada`/`meses_cobertos`, nenhum campo de `Estado` | 11/09 — os dois removidos de `d` (eram campo morto e formula duplicada; a validação de `reserva_empenhada` continua) |
| — | achado lateral: `custo_entrada_fixo_pct` tratava `aporte==0` como custo infinito para toda rota, mesmo as de tarifa zero — zerava o universo e violava `_conferir_invariantes` | 11/09 — `r.corr_fix == 0` agora é custo zero para qualquer aporte; sem mudança para aporte>0 |
| P-69 | `etf.IMAB11` duas vezes no `custos.yaml` — o PyYAML ficava com o placeholder `null` e a entrada de 05/09 estava morta (Y-01) | 11/09 — entradas **fundidas** (valor/fonte de 05/09, base legal e `bloqueia` da outra); `test_y01_yaml_duplicata.py` varre os seis YAML pela árvore de nós. A F-03 foi medida à mão com 0,25%, nunca por `val()` — não foi contaminada. Abriu a P-76 |
| — | guarda de campos mortos do lado Python (auditoria de 10/09: o P-28 protegia só o YAML) | 11/09 — `campos_mortos.py` (AST; referência = `Attribute`, `keyword`, `Name` ou chave de `Dict`, só em produção) + `test_campos_mortos.py` com inventário que não apodrece e os pontos cegos declarados. Achou 10 além dos quatro — P-77 e P-78 |
| — | `Aporte.status_do_variavel` | 11/09 — **removido**. Ninguém o preenchia e ninguém o lia: um status que parece gate e não é. A desconfiança do extraordinário já está no desenho (piso × extraordinário) |
| — | `tese.DIFERIDOS_K` | 11/09 — **removido**. O G-01 nasceu do C02, que depende do juro travado na compra; o K02 não depende de compra. Diferir a tese selaria na impressão um texto vazio |
| — | `estado_io.reserva_empenhada` | 11/09 — **usado**, como conferência: se declarado, tem de bater com `reserva_atual − reserva_disponivel`, no padrão de `reserva_por_rota`. O motor segue usando só `reserva_disponivel` |
| — | `corretora.promocional` (P-32) | 11/09 — **usado**: `regras()` recusa peso ≠ 0, como faz com `reclame_aqui` e `facilidade` |
| B-02 | 3 de 74 emissoras com `totalRecords: 0` na esteira de proventos (ABEV, CURY, KLBN) | 11/09 — **não era truncamento** (o código supunha; a hipótese foi medida e caiu): a tabela de proventos guarda o nome **sem** o sufixo `S/A`. O coletor tenta o nome como veio e, **só depois de um zero**, sem o sufixo; a forma usada vai para o manifesto. As 71 gravadas não foram tocadas; recoletar as 3 é decisão do Osvaldo |
| B-03 | CURY falhou nas duas formas do B-02 | 11/09 — `'CURY S.A.'` → 20: o sufixo não some, é **reescrito** (barra vira ponto). As bases divergem sem regra, então virou **cascata**: como veio → sem sufixo → `S.A.` → `SA`, só avançando depois de zero; a trilha inteira vai para o manifesto. 73 de 74 gravadas; recoletar a CURY é decisão do Osvaldo |

---

## P-102 · ~~Uma guarda acessória derrubou o manifesto~~ **CONSERTADA, falta aplicar**

**Dono:** Osvaldo (aplicar os arquivos) · **Gatilho:** **antes de qualquer outro commit** ·
**Classe:** `BLOQUEIA_O_SISTEMA` · ⚙ **exige o desktop**

Liguei `acervos_sem_regime()` ao `main()` do `manifesto_cvm.py` sem guarda. Em `tmp_path` o
`raiz_do_repositorio` acha o `pyproject.toml` que o próprio teste cria, a política não existe
ali, e o `FileNotFoundError` subiu — derrubando **três testes do `test_manifesto_cvm.py` que
não tinham nada a ver com P7 nenhuma**. Eles foram commitados e **empurrados vermelhos, no
primeiro push da história do repositório** (`3ee5e97`).

**Dois erros meus, e o segundo vale mais:** rodei só o meu teste novo, não a suíte de `fase0`
(passo 5 do §9, *"pytest, o júri"*, pulado na mesma resposta em que citei o protocolo); e uma
guarda **acessória** derrubou o **trabalho principal** — o comando grava o retrato de
procedência, conferir a P7 é um extra que eu pendurei nele.

**A correção fica entre dois extremos:** `PoliticaAusente` **levanta** na função (engolir
seria o E-02 — arquivo ausente virando *"nada declarado"*) e o `main()` **avisa que a
conferência não rodou** e deixa o retrato de pé. *"Conferi e está certo"* e *"não consegui
conferir"* não podem ter a mesma saída.

**Medido com o PC desligado**, reconstruindo os três testes a partir do diff:

```
1 test_sem_origem_declarada_o_manifesto_CONTA_em_vez_de_calar   VERDE
2 test_com_origem_declarada_o_numero_CAI                       VERDE
3 test_a_origem_NAO_e_reescrita_pelo_manifesto                 VERDE
4 politica ausente LEVANTA (nao vira "nada declarado")          VERDE
```

**O que NÃO foi medido (P5):** a suíte `fase0` inteira. O container não tem `ajustar.py`,
`test_ajustar.py`, `test_calendario.py` nem o `coletar_b3.py` atual — o mirror é parcial.
O que está provado é a causa raiz, que era **uma** e local ao `main()`. **Rodar a suíte na
máquina é o que fecha.**

---

## Ao voltar ao desktop

> # ▶ O roteiro completo está em **`SEGUNDA-21.md`**, na raiz.
>
> *Reescrito em 19/09. Ele é autossuficiente: abrir e seguir de cima para baixo. Esta seção
> só resume, para não haver duas listas discordando — foi assim que a versão de 06/09 ficou
> doze dias mandando criar um repositório que já existia.*

**Em uma linha:** copiar 7 arquivos do chat → as três suítes verdes → commit e push →
`ajustar.py` sobre 2021–2025 no Claude Code.

| passo | o que | tempo |
|---|---|---|
| 1 | copiar os 7 arquivos do chat (lista em `SEGUNDA-21.md`) | 5 min |
| 2 | **as três suítes verdes** — `origin/main` está VERMELHO (P-102) | 5 min |
| 3 | commit + push | 2 min |
| 4 | **`ajustar.py` sobre 2021–2025 contíguos** ⚙ Claude Code | o trabalho |

**Duas coisas com data:** `macro.poupanca_am` vence **28/09**; e a CVM reescreve DFP/ITR
toda semana — cada semana sem captura é uma rodada de reapresentações que **não volta**.

**Uma coisa que eu não fiz:** não atualizei o `ACHADOS.md` — ele nunca passou pelo
container, e manter atualizado um arquivo que eu não li seria escrever sobre o que suponho
que ele diz. O bloco pronto está em `ACHADOS-19-09-PARA-COLAR.md`.

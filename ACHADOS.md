# ACHADOS.md — o registro histórico

Todo defeito encontrado neste projeto, com a medição que o provou e o teste que o
prende. **Este arquivo não é instrução: é memória.**

## Por que ele foi separado do CLAUDE.md — 06/09/2026

O `CLAUDE.md` chegou a **1.112 linhas (~15 mil tokens)** e estava fazendo dois trabalhos
incompatíveis ao mesmo tempo:

| trabalho | quando precisa ser lido |
|---|---|
| **instruções** — doutrinas, convenções, como trabalhar, próximo passo | **toda sessão**, antes de tocar em qualquer coisa |
| **história** — os 25 achados, com narrativa completa | **só quando a tarefa toca aquela área** |

Misturados, os dois custavam ~15 mil tokens em toda sessão, e ~10 mil deles eram
narrativa que a tarefa do dia normalmente não precisava. Somados aos ~11 mil do
`PENDENCIAS.md`, davam **26 mil tokens gastos antes de qualquer trabalho começar** —
num plano com limite compartilhado entre o app e o Claude Code.

**Nada foi apagado.** A auditabilidade é o ponto do projeto inteiro; o que mudou é
*quando* se paga por ela. O `CLAUDE.md` ficou com 449 linhas de instrução e aponta para
cá quando o assunto exige.

## Como usar

Procure pela letra do achado (`F-02`, `N-01`, `S-02`…). Cada um tem: o que era, como
foi medido, o que mudou, e o teste que impede a volta. Se você vai mexer numa área,
leia os achados dela **antes** — vários destes defeitos são reincidências de um mesmo
padrão, e reconhecer o padrão vale mais que decorar os casos.

**O padrão que mais se repetiu**, e que já apareceu quatro vezes com roupas
diferentes — F-05, N-01, R-01, S-02: *um arquivo declara um comportamento que o código
não tem, e os dois concordam por acaso, então ninguém descobre.*

---

### J-01 / K-01 — a reserva que nunca existiu, e o pedágio do Turbinado

**A resolução veio dele, e ela desfaz um erro meu de modelagem.** Eu vinha tratando os
R$7.671 do cofrinho como "reserva que por acaso está empenhada", e inventei
`reserva_disponivel` para descrever isso. Ele corrigiu:

> *"Não tenho problemas em a reserva não estar no cofrinho de limite de cartão. Eu
> deposito lá porque não tinha um cartão com bom limite e uso o cartão como meio de
> pagamento. É só considerar que aquele valor não é uma reserva."*

O modelo certo é mais simples: **aquele dinheiro nunca foi reserva.** É caução de um
meio de pagamento, com propósito próprio. Os 102% do CDI são consolo, não objetivo.

`estado.yaml` tem hoje `reserva_atual: 0.00` e um bloco `deposito_garantia` separado,
que não compete no G2, não conta meses de despesa e não entra em patrimônio investido.
**A reserva de emergência dele é zero — não "zero porque travada", mas zero porque
nunca foi constituída.** A Fase A começa do começo, e isso é o dado.

**Onde eu errei, e vale como aviso.** Escrevi que a reserva seria "consumida pela
dívida que a prendia" e falei em "correlação −1 com a própria necessidade". Com o
propósito declarado, isso cai: o cartão é **garantido**, e uma dívida coberta 14,5× pelo
próprio depósito não é risco de crédito, é pagamento antecipado. **Deduzi risco de uma
estrutura sem perguntar o propósito dela.** A limitação do motor continua registrada
(G1 e G2 tratam dívida e reserva como independentes, e isso é um defeito real), mas com
`aplica_se_ao_caso_do_usuario: false`.

**J-03, e ele foi REFUTADO no mesmo dia.** Eu escrevi que o depósito comprava limite
a 14,5 para 1 e que havia "capital ocioso". Errado, e o erro foi de método: li "limite
**extra** de R$530" como se fosse o retorno inteiro do depósito, sem perguntar o limite
**total**. Ele informou: R$9.551. A conta fecha ao centavo — base R$1.349,99 (sem
cofrinho) + R$7.671,01 (cofrinho, **1 para 1**) + R$530,00 (bônus de 6,9%). O cofrinho
vira limite 1:1 e ainda paga bônus. **Não há capital ocioso e não há o que liberar sem
perder limite na mesma medida.**

**K-01, o pedágio do Turbinado.** 121% do CDI e resgate livre, mas R$23,99/mês. A
vantagem de 19 p.p. do CDI vale 2,113% a.a. líquido e só cobre os R$287,88/ano a partir
de **R$13.625** — e o **teto do produto é R$10.000**. Pagando, nunca se paga: no teto
ainda perde R$76,60/ano. Só vale com a isenção.

**K-03: a isenção é paga em outra moeda.** As missões deste mês foram **gasto no cartão**
e **trazer uma chave Pix** — uma terceira via, por tarefas que o banco escolhe e que
mudam todo mês. Os R$287,88/ano são o **piso**: falta o gasto marginal induzido pela
missão. Condição rebaixada a `PARCIAL` — a do mês seguinte é desconhecida por construção.

**K-02:** a reserva-alvo de R$36.000 não cabe num produto de teto R$10.000, e `RotaAloc`
não tem campo para teto de saldo (P-24).

### L-01 — a fronteira entre o motor e um usuário

Ele lembrou em 05/09 que **escalabilidade inclui servir mais pessoas**, e que o
projeto estava construído sobre as preferências dele. Medi antes de opinar: **109
chaves de motor contra 13 de usuário, no mesmo arquivo**.

O problema não era o tamanho — era que **um segundo usuário não teria onde pôr as
escolhas dele sem editar o `politica.yaml`, e ao editar apagaria as do primeiro.**

`compromissos` e `decisoes` foram para `perfil.yaml`. A fusão acontece na carga, então
**nenhum consumidor mudou**: os seis arquivos que liam essas seções continuam lendo
igual. Trocar de usuário é passar outro `perfil` a `carregar_politica()`.

Três testes guardam a fronteira: seção de perfil dentro da política falha; perfil que
redefina `portoes` ou `funcoes` é recusado (dois usuários com motores diferentes não
produzem nada comparável); e o perfil tem hash próprio, porque procedência de saída
precisa dizer **qual** perfil a gerou.

**Por que agora e não depois:** eram 13 chaves. Depois da Fase 0 e dos blocos de
análise seriam muitas mais, e cada decisão nova escrita no lugar errado aprofunda o
acoplamento. Separar cedo custou uma função de carga; separar tarde custaria uma
migração.

**Continua parcial (P-27).** Quatro seções são mistas *por dentro* — `corretora` junta
metodologia com os pesos que ele escolheu, e `custos.yaml → cofrinho` junta termos de
produto com o estado da conta dele. Dividi-las sem decidir a granularidade criaria
bagunça pior que a atual.

### O-01 / K-02 — o G2 media a média, e a média não descreve nenhum real

Fui fechar a P-24 (`teto_de_saldo`) e encontrei um defeito maior debaixo dela.

O G2 avaliava cada rota de liquidez **no alvo inteiro**, ordenava pela média e mandava
100% do aporte para a primeira. O Tesouro Selic é isento de custódia até R$10.000 e paga
0,20% a.a. acima disso — então o retorno **depende do saldo**, e a média em R$36.000 não
descreve nenhum real: os dez mil primeiros rendem mais do que ela diz, os vinte e seis
mil seguintes, menos. Avaliado em R$10.000 o Tesouro ganha do RDB; avaliado em R$36.000,
perde. Os dois números são verdadeiros e nenhum é o critério.

Com retorno dependente de saldo, **ordenar pela média e encher a primeira não dá o
melhor resultado.** O critério é o marginal — quanto rende o *próximo* real.

| | destino | R$/ano | em emissor privado |
|---|---|---|---|
| rota única | RDB 100% CDI | 3.878,10 | R$ 36.000 |
| composição | Tesouro 10k + RDB 26k | 3.885,85 | R$ 26.000 |

**O ganho em reais é R$7,75 por ano, e inflar isso seria repetir o erro do J-02.** O que
muda de verdade é outra coisa: a rota única **obrigava a escolher** entre o melhor
retorno e o melhor crédito. A composição não escolhe — os R$10.000 saem do emissor
privado sem custar retorno.

E aí o K-02 fica pior do que estava escrito. Não é que o portão "para de funcionar"
quando o produto enche. Com a isenção do Turbinado confirmada, o G2 antigo o elegeria
avaliando no alvo inteiro: R$36.000 a 13,03% = **R$4.692/ano**. O produto aceita
R$10.000. O número não era otimista — era retorno **sobre dinheiro que o produto
recusa**, e o portão continuaria mandando aporte para lá. Mesma família do F-02: resposta
bem formada sobre premissa que deixou de valer.

O `teto_de_saldo` não é o teto do FGC, e confundi-los inverte a consequência: o FGC
limita a **garantia** — passar dele é um risco que se pode aceitar; o teto de saldo
limita o que o produto **aceita** — passar dele não é arriscado, é impossível.

**Duas rotas entraram no catálogo, e uma delas é a única posição que ele tem.** O
cofrinho do PicPay não existia no catálogo: o sistema opinava sobre onde pôr dinheiro sem
enxergar onde o dinheiro está — o pior caso da P6. Entra **sem** a função LIQUIDEZ, que é
o achado J-01 inteiro (0 a 29 dias de espera conforme o dia da emergência), e rendendo
102% do CDI. Rende acima do CDI e ainda assim não serve para a função que ele precisa
preencher primeiro.

### N-01 — a seção `corretora` prometia três regras que o Python decidia sozinho

`multiplicador_de_confirmacao: {C: 1.00, P: 0.75, N: 0.00}` estava no `politica.yaml`,
com uma `regra:` explicando o porquê. E estava também em `corretoras.py`, como o literal
`mult = {"C": 1.0, "P": 0.75, "N": 0.0}`. **Os dois concordavam.**

Concordar é pior que discordar. Discordância aparece; concordância faz o arquivo parecer
governar o sistema quando não governa. Editar o YAML não mudava o ranking — e o ranking
de corretoras é a decisão de **onde o dinheiro fica guardado por dez anos**.

Eram três, e a terceira mostra o padrão:

| declarado no YAML | onde de fato vivia | agora |
|---|---|---|
| `multiplicador_de_confirmacao` | literal em `pontuar()` | lido do YAML |
| `reclamacoes.escala: "índice 0 = 100 pontos"` | `1 - bc_indice/100` | `escala_indice_para_nota_zero` |
| corretagem: nenhum campo | `0.01` com um comentário ao lado | `custo_do_aporte_para_nota_zero` |
| `reclame_aqui.pontua: false` / `exibe: true` | ninguém lia nenhum dos dois | `pontua: true` levanta exceção; `exibe` exibe |

O terceiro caso é o mais instrutivo: **o YAML não dizia nada** sobre a escala de
corretagem. A escolha de que 1% do aporte zera a dimensão — R$5 numa ordem de R$500 —
é o que separa "caro" de "inviável", e estava num comentário de código.

O quarto fecha uma mentira menor e mais teimosa: `exibe: true` mandava mostrar o Reclame
Aqui sem pontuá-lo, e a saída não o mostrava. Exibir **é** o ponto: o Itaú tem 8,1 no
Reclame Aqui e é o 3º mais reclamado do Brasil no ranking do BC. Esconder a fonte que
discorda é escolher a que agrada.

É o mesmo achado do **F-05** (`bloqueia` era prosa), em outra seção. Duas ocorrências do
mesmo defeito em dois dias significam que ele não é acidente — é o modo de falha padrão
deste projeto, e a P2 existe justamente contra ele.

### P-28 — o guarda media o próprio escopo

O `test_cobertura_yaml` existia desde 02/09 para pegar exatamente esse defeito. Ele
varria **6 das 19 seções**, lendo **3 dos 11 módulos**, com as duas listas escritas à
mão. Um teste de cobertura com escopo manual mede o escopo, não a cobertura — e foi por
esse vão que `revisao` entrou, foi declarada e nunca lida.

Agora são quatro testes, e o que importa é o terceiro:

1. varre todas as seções e todos os módulos (a lista de módulos vem do `listdir`);
2. toda seção precisa de **regime declarado com motivo escrito** — `OPERACIONAL` (o
   motor lê), `REGISTRO` (testemunho), `ESPECIFICAÇÃO` (escrito e não ligado);
3. **seção nova sem regime quebra a suíte.** Não há default. Esquecer virou barulho;
4. a dívida conhecida vive num inventário que **não pode apodrecer**: entrada já paga,
   ou de chave removida, faz o teste falhar.

O item 4 se provou na hora — a correção do N-01 pagou quatro entradas do inventário e o
teste mandou apagá-las. Um inventário que só cresce é decoração.

O que a varredura completa encontrou: **três seções inteiras especificadas e não
ligadas** (`bloco_C_solvencia`, `regime_instituicao_financeira`,
`estrategias_pre_registradas` — P-29 a P-31), e mais três blocos de dívida menor
(P-32 a P-34). Nenhuma delas era visível antes.

### Bloqueado nele, não em código

- **Tese do HASH11** (K02/K03/K04) e **compromisso do IPCA+** (C02–C06). Sem
  eles os dois ativos ficam em zero. Só passam a importar na Fase B.
- **O aporte realizado.** R$500 é o piso planejado; o realizado é zero. É o único
  número do projeto que nenhuma linha de código substitui.
- **Onde constituir a reserva** — ela é zero e começa agora. Os candidatos são
  `td_reserva` (Selic, isento de custódia até R$10 mil) e o Turbinado com isenção; o
  G2 sabe escolher entre eles assim que o destino existir.
- ~~**Se o empenho do cofrinho é obrigatório**~~ — resolvido: não importa, o valor não é reserva.

---


---

## 9. Armadilhas de repositório já encontradas

### F-04 — CRLF corrompe a série do NEFIN

`git` no Windows converte LF em CRLF no checkout (`core.autocrlf=true`). Para
código é inofensivo. Para `alocacao/dados/nefin_factors.csv` não é: são **6.322
bytes a mais** (um por pregão), e o sha256 que `fatores.hash_fonte()` publica muda
de `619991c2192c` para `421b3b3b753e`.

Isso quebraria a única coisa que o pré-registro promete — que um resultado de
backtest é reproduzível. Um clone novo em outra máquina Windows produziria números
iguais com procedência diferente, e ninguém perceberia.

Protegido em três camadas: `.gitattributes` marca o arquivo como binário;
`test_fonte_e_exatamente_a_serie_pre_registrada` fixa o hash; e
`test_serie_nao_tem_fim_de_linha_do_windows` procura `\r\n` direto nos bytes.
**Nunca "conserte" o hash esperado para fazer o teste passar** — se ele falhou, ou
a fonte mudou de propósito (então atualize e registre em `REGISTRO-vN.md`) ou algo
corrompeu o arquivo.

### Identidade do commit

O primeiro commit saiu como `osvaldo.junior@volga.local` — e-mail derivado do
hostname, que o GitHub não consegue atribuir a ninguém. Confira com
`git log -1 --format='%an <%ae>'` antes de assumir que a autoria está certa.

### G-01 — o schema não sabia dizer "regra decidida, papel não comprado"

`teses.yaml` só admitia um estado: compromisso pronto. Ele presume uma posição que
existe ou vai existir já. Mas a Fase A vai até ~2031 e não há conta em corretora —
e `C02_compromisso` exige o **juro real travado**, que só existe no dia da compra.

Preencher C02 hoje não seria pré-registro: seria ficção com hash. Deixar em branco
também não serve, porque as **regras** (prazo, condição de venda, teto,
reconhecimento) são decidíveis hoje — e hoje é exatamente quando pré-registrá-las
tem valor, antes de a posição existir.

Daí dois estados. `REGRA_DECIDIDA` sela o decidível e exige que os campos que
esperam a compra valham `AGUARDA_COMPRA` **em voz alta** — campo vazio não
distingue "ainda não sei" de "esqueci". `COMPROMISSO_ATIVO` exige tudo. A migração
acontece na compra, recalcula a impressão e manda a antiga para `historico`.

**O G8 não libera peso em `REGRA_DECIDIDA`.** Regra seleada não é posição.

### Git dentro do OneDrive

Este repositório fica numa pasta sincronizada pelo OneDrive corporativo. Isso
funciona na maioria dos dias, mas o modo de falha existe: o OneDrive trava um
arquivo dentro de `.git` durante um commit e o índice fica inconsistente.

Se acontecer: `rm -f .git/index.lock` e `git status`. Se o índice em si
corromper, `rm .git/index && git reset` reconstrói a partir do HEAD — os commits
já feitos não se perdem. Pausar a sincronização antes de operações grandes
(rebase, filter-branch) evita o problema.

---

## 10. Auditoria de engenharia — 05/09/2026

O Osvaldo perguntou se o projeto usa boas práticas e se é fácil de auditar e manter.
A resposta medida é: **auditável sim, e por um motivo incomum; manutenível não, e por
motivos comuns.** Esta seção existe para que nenhuma sessão futura confunda as duas.

### Onde ele é genuinamente bom, e não é opinião

| prática | evidência |
|---|---|
| todo defeito vira teste que falha na versão anterior | 216 testes, cada docstring nomeia o achado |
| rastreabilidade de decisão | `changelog` com 12 entradas; todo achado tem letra e data |
| procedência de dado | `status` + `fonte` + `acesso` + `expira` em 55 constantes |
| limitações declaradas | 8 entradas com **direção do viés** — raro até em código profissional |
| guarda contra config morta | 4 testes; regime obrigatório por seção; inventário de dívida que não apodrece |
| reprodutibilidade da série | hash fixado em teste + `.gitattributes` |

O item das **limitações com direção do viés** é o que mais distingue este projeto de
código comum. Quase nenhum sistema declara "esta simplificação favorece o ETF contra a
ação, e a decisão A05 é exatamente entre os dois".

### Onde ele falha, medido

**1. ~~A doutrina P2 é violada pelas duas maiores estruturas de dado do projeto.~~ —
FECHADA em 05/09.** `alocacao.catalogo()` (183 linhas, 25 rotas) virou `catalogo.yaml`
com um carregador de **39 linhas**; `corretoras.catalogo_instituicoes()` (136 linhas,
24 casas) virou `instituicoes.yaml` com um de **32**. Ver P-36 e os achados Q-01/Q-02
abaixo.

**2. ~~Funções grandes demais em pontos concentrados.~~ — FECHADA em 05/09.**
`alocar()` tinha **300 linhas** e virou seis passos de 16 a 51. A maior função do
motor hoje é `g2_reserva`, com 102. Ver P-37 e o achado R-01 abaixo.

**3. ~~Ferramental de projeto: não existe.~~ — FECHADA em 05/09, e o conserto tem uma
forma que vale registrar.** Havia um furo real: as versões de `numpy` e `pandas` que
produziram os números pré-registrados não existiam em lugar nenhum do repositório. O
dado estava selado (sha256 + `.gitattributes`); o ambiente não. Ver P-15 e a seção
sobre `ambiente.py` abaixo.

~~Continua faltando lint, type-checker e CI~~ — **ruff e mypy fechados em 06/09
(P-40), ambos em zero e ligados à suíte.** Continua sem CI, porque não há para onde
apontar enquanto o repositório não estiver no GitHub.

**4. Dinheiro é `float`.** Zero uso de `Decimal`. Para as contas atuais (percentuais,
projeções) é aceitável e o erro é irrelevante. Deixa de ser quando existirem
lançamentos, saldos e conciliação — e aí a migração é global.

**5. Cerca de um terço dos testes não exercita o motor.** Eles afirmam o conteúdo do
YAML. Não são inúteis — o P-28 e as limitações declaradas *são* esse tipo de teste, e
foi um deles que pegou o N-01. Mas eles inflam a contagem: "216 testes" não significa
216 comportamentos verificados. Ao citar o número, dizer o que ele mede.

**6. ~~Estado global carregado no import.~~ — FECHADA em 05/09.** O `conftest.py`
tem fixtures `custos`/`politica` e uma guarda que acusa o teste que suja estado
compartilhado. E o S-02 mostrou que o problema era maior do que a pendência descrevia
— ver abaixo.

**7. Nenhuma camada de persistência.** O blueprint prevê DuckDB + Postgres + Parquet.
Existe: YAML e um CSV. Isso é adequado à fase — mas quem ler o blueprint e depois o
código vai achar que falta código, e não é isso: **a Fase 0 nunca rodou.**

### O veredito, sem enfeite

Auditável **por um humano**, e muito. Um leitor cuidadoso reconstrói toda decisão a
partir dos arquivos, o que quase nenhum código permite. Auditável **por ferramenta**,
não: não há tipos, lint, CI ou lockfile.

Manutenível por quem escreveu, no mês em que escreveu. **Não manutenível por um
terceiro** — e a razão não é o tamanho, é que os dois catálogos exigem editar Python
para mudar um número de pesquisa, e nada testa se esse número tem procedência.

**A prioridade honesta de engenharia:** ~~P-15~~, ~~P-36~~, ~~P-37~~, ~~P-38~~ e
~~P-40~~ feitas. A fila de engenharia acabou. O que resta é P-43 (o terceiro catálogo)
e CI — e CI só faz sentido depois do push.

**O que NÃO fazer:** adicionar tipos e lint antes disso. Melhoram a leitura e não
fecham nenhum furo de veracidade, que é o que este projeto promete.

### P-15 fechada — `ambiente.py`, e a assimetria é a decisão de desenho

O projeto já sabia dizer de onde veio cada **número** (`status`/`fonte`/`acesso`/
`expira` em 55 constantes) e cada **dado** (sha256 da série do NEFIN, fixado em teste).
Não sabia dizer de onde veio o **resultado** — em qual ambiente foi calculado. E
`alfa_contra_fatores()` sai de `numpy.linalg.lstsq`, que é uma *implementação*, não um
teorema. Mesmo modo de falha do F-04, deslocado do dado para a máquina.

Três regras, e elas têm severidades **diferentes de propósito**:

| | severidade | por quê |
|---|---|---|
| toda dependência importada está declarada, e vice-versa | **erro duro** | é o "funciona na minha máquina" em forma testável |
| a impressão em `politica.yaml` bate com o `pyproject` | **erro duro** | trocar de `numpy` vira decisão visível, não efeito colateral de um `pip install -U` |
| a versão instalada é a registrada | **aviso** | quem carrega o alarme é o **resultado**, não a suíte |

A assimetria não é conveniência. Um teste que ficasse vermelho porque a máquina dele
tem outro `numpy` puniria trabalho legítimo com um alarme que não é sobre o código.
Um backtest que não dissesse em que ambiente rodou seria meio pré-registro. O
mecanismo do aviso é o mesmo do `expira`: `motor.val()` avisa em `stderr` e devolve o
valor.

**As versões vivem só no `pyproject.toml`.** O `politica.yaml` guarda apenas a
impressão digital calculada a partir dele — repetir os números nos dois arquivos seria
o N-01 outra vez. Não há `requirements.txt`, pelo mesmo motivo; o comando de instalação
se deriva da lista (`python ambiente.py --instalar`).

Dependências classificadas por **consequência**, não por importância: `numpy` e
`pandas` são *numéricas* (mudam número registrado); `PyYAML` e `pytest` são
*ferramentas* (um parser ou entrega os mesmos floats, ou erro). Divergência numérica
avisa; divergência de ferramenta não diz nada sobre a validade de nenhum número.

**O que a impressão NÃO promete,** e está escrito no registro: sistema operacional,
BLAS ligada ao `numpy` e arquitetura de CPU continuam fora, e podem mover a última casa
decimal de uma regressão. Ela cobre o que dá para cobrir com o repositório.

### P-36 fechada — o catálogo saiu do Python, e trouxe dois achados

| | antes | depois |
|---|---|---|
| `alocacao.catalogo()` | 183 linhas, 25 rotas em literais | **39 linhas** + `catalogo.yaml` |
| `corretoras.catalogo_instituicoes()` | 136 linhas, 24 casas em literais | **32 linhas** + `instituicoes.yaml` |

**A garantia da migração foi conferida campo a campo contra o objeto anterior: zero
diferenças, nas duas metades.** Isso não é detalhe de processo — é o único jeito de
migrar 39 registros com ~15 campos cada sem introduzir um erro silencioso. O snapshot
foi comparado, não relido.

**Regra central: valor que vem do `custos.yaml` fica como referência, nunca cópia.**
`adm_aa: {de: etf.PIBB11}` e não `adm_aa: 0.0059`. Copiar o número criaria dois lugares
que concordam — o N-01 em escala de catálogo — e mataria `expira`, `status` e `bloqueia`
da constante. Um teste prova pelo comportamento: mexer na constante *tem* de mexer na
rota.

O vocabulário de referência é pequeno de propósito: `{de:}`, `{soma:}`,
`{de_se_na_lista:}`, `{de_campo:}`. As três **estratégias de bloqueio** continuam em
Python — são lógica, não dado. O YAML diz *qual* se aplica e a *que* fonte; o Python diz
*como*. Acrescentar uma rota não exige tocar em Python; acrescentar um **tipo novo de
regra** exige, e deve exigir.

#### Q-01 — insumo bloqueado derrubava o catálogo inteiro

O tratamento era **inconsistente**, e as duas metades nunca se encontravam no mesmo
teste:

- rotas de ETF **degradavam**: `val()` levantava, a rota entrava sem a taxa e com o
  motivo escrito — foi assim que o BOVV11 ficou visível;
- todas as outras **explodiam**: `val()` levantava dentro de `catalogo()` e o catálogo
  inteiro morria.

Uma constante `NAO_CONFIRMADO` em `corretagem.safra_terra` apagaria as 25 rotas,
**inclusive as 24 que não dependem dela** — o oposto exato da doutrina P6. Regra única
agora: insumo bloqueado bloqueia **a rota**, com o motivo escrito, e a mensagem aponta
para a *constante* e não para o campo, porque quem lê precisa saber que número ir buscar.

#### Q-02 — a letra sempre falou de custos, e o registro não sabia dizer

`confirmacao` era uma letra por instituição, e `pontuar()` a aplica como **multiplicador
de tudo**: `N` zera a nota inteira. Mas ela nunca significou "este registro é confiável".
Sempre significou "os **custos** podem ser lidos em fonte oficial" — a própria `regra` do
multiplicador, em `politica.yaml`, diz isso com todas as letras.

As fontes provam: BTG, Bradesco, Mirae e Avenue têm `N` e `fonte` dizendo *"BCB IF.data
03/2026 (porte) — custos NÃO OBTIDOS"*. O balanço deles vem do **Banco Central**; o
índice de reclamações do BTG e do Bradesco vem do **ranking do BC**. Duas fontes
primárias, ambas completas.

**O comportamento estava certo** — não publicar custo tira da ordenação, por decisão
declarada. **O registro é que não sabia dizer**: um leitor do arquivo antigo concluiria
que o dado de balanço do BTG é duvidoso, quando ele veio do regulador.

A procedência passou a ser **por grupo de campos** — custos, balanço, reclamações,
Reclame Aqui, societário, facilidade —, porque é assim que as fontes de fato se agrupam.
E `confirmacao` deixou de ser campo próprio: é **derivada** de
`custos.procedencia.status`. Dois campos que podiam discordar viraram um; é o N-01
prevenido em vez de encontrado.

**O que isso não conserta, declarado:** a granularidade é por grupo, não por campo.
Procedência por campo daria 24 × 15 = 360 blocos para registrar cinco fontes reais, e
registro que ninguém lê é pior que registro nenhum. Se um campo um dia vier de fonte
diferente da do grupo, ele precisa de grupo próprio.

### P-37 fechada — e o achado que só apareceu depois da quebra

`alocar()` tinha 300 linhas e orquestrava nove portões. Virou seis passos:

| | linhas |
|---|---|
| `_preparar` | 16 |
| `fase_aporte` | 43 |
| `fase_universo` | 17 |
| `distribuir_por_funcao` | 46 |
| `alocar` | 51 |

A quebra segue **as fases que já existiam no YAML**, não um critério novo. A maior
função do motor hoje é `g2_reserva`, com 102 linhas, e um teste novo
(`test_P37_nenhuma_funcao_do_motor_passa_de_120_linhas`) impede que a próxima apareça
sem alguém decidir que deve aparecer.

**A garantia:** 38 cenários de estado foram serializados campo a campo antes da quebra
— pesos, **cada string de alerta**, cada pendência, cada rota em cada lista de rejeição
— e comparados depois. A única diferença em toda a matriz é o próprio `politica_hash`,
que mudou porque o `politica.yaml` mudou. Isso é o sistema de procedência funcionando,
não desvio.

#### R-01 — a ordem dos portões era um dado que só aceitava 18 de 120 valores

Este achado **só foi possível depois da quebra**, e é o argumento inteiro da P-37: com
`fase_universo` isolada, dá para permutar a ordem no YAML e observar o resultado sem
rodar a alocação completa. Com 300 linhas, não dava.

A P-07 declarou a ordem dos portões como dado e afirmou que trocá-la é um commit no
YAML. **Isso é falso para 102 das 120 ordens.**

A causa: os portões mudam a **forma** do que trafega. O `G3_atrito` é o único que
transforma — entra rota, sai `(rota, custo)` — e `G4`, `G7` e `G8` consomem pares.
Qualquer um deles antes do G3 estourava com `TypeError: cannot unpack non-iterable
RotaAloc object` disparado no fundo de uma função de portão, nunca com uma mensagem
dizendo que a **ordem** era o problema.

Declarar a ordem como dado sem declarar o contrato é declarar uma liberdade que não
existe — mesma família do F-05 (`bloqueia` era prosa) e do N-01.

Cada portão da fase `universo` passou a declarar `consome`/`produz`, e
`conferir_ordem_do_universo` recusa antes de rodar. O quadro medido:

| | ordens | |
|---|---|---|
| rodam | 18 | |
| recusadas com mensagem clara | 90 | novo |
| `InsumoBloqueado` | 12 | **não é defeito** — é o guarda do F-02 disparando |

As 12 são as ordens que põem o `G5_status` depois de um portão que calcula custo, e aí
uma rota bloqueada chega a uma conta. A mensagem já nomeia a rota e a constante.
Transformar isso num erro de ordem esconderia que a causa é outra.

**O `G5_status` é polimórfico de propósito** — aceita rota nua ou par e devolve o que
recebeu. Foi isso que permitiu corrigir o F-02 movendo-o para a frente sem quebrar nada,
e está declarado como `produz: mesma_forma`.

#### A cadeia de `elif` virou tabela

A fase `universo` era uma cadeia de `elif nome == ...`, e a consequência não era
estética: **a lista de portões implementados só existia escondida naqueles ramos**. Duas
validações precisavam dela — "este portão existe?" e "esta ordem é executável?" — e
nenhuma podia enxergá-la. Agora é `PORTOES_DO_UNIVERSO`, e o G6 aparece nela como um
não-faz-nada **nomeado, com o motivo escrito**, em vez de um `continue` que não
distingue "já rodou" de "esqueceram de implementar".

---

## 11. Como rastrear o alcance de uma alteração — 06/09/2026

O Osvaldo perguntou como eu rastreio, a cada mudança, onde o que foi alterado interage
com os outros arquivos. **A resposta honesta era: três ferramentas e nenhum mapa.**

| ferramenta | o que responde | limite |
|---|---|---|
| a suíte (265 testes) | *"quebrou?"* | responde **depois** |
| `grep` | *"onde aparece este nome?"* | depende de eu lembrar do nome certo |
| instantâneo dourado | *"mudou algum número?"* | caro; só vale para mudança grande |

Nenhuma delas responde, **antes** de editar: *"se eu mexer em `etf.BOVA11`, o que
alcança esse valor?"*. Foi assim que o **N-01** quase passou — procurei
`multiplicador_de_confirmacao` no Python, achei zero, e só não concluí "ninguém lê"
porque desconfiei do número repetido.

**`impacto.py` responde.** Ele não substitui a suíte: a suíte julga, ele orienta.

```bash
python impacto.py etf.BOVA11        # constante
python impacto.py simular_custo     # função
python impacto.py teto_de_saldo     # campo de dataclass
```

O que ele enxerga: `catalogo.yaml → custos.yaml` (46 arestas — e esse grafo é **dado**,
não inferência, desde a P-36), chave de YAML → módulo, o grafo de imports, o grafo de
chamadas com **fecho transitivo inverso**, e acesso a atributo.

**O que ele NÃO enxerga é a parte que importa mais**, e ele reporta junto: 14 leituras
com chave montada em tempo de execução (`P["funcoes"][f]`), `getattr` dinâmico, e
despacho por dicionário de funções. Toda conclusão de "ninguém lê isto" passa por essa
lista antes de virar decisão. **Um mapa que finge completude é pior que grep, porque
grep ninguém confunde com garantia.**

Três testes impedem o mapa de mentir: toda referência do catálogo aparece no grafo;
toda aresta aponta para constante que existe; e — o que separa mapa de desenho —
**alterar a constante que o mapa aponta tem de mudar exatamente as rotas que ele diz**.

### O protocolo, na prática

1. `python impacto.py <alvo>` — antes de editar, ver o que alcança.
2. Ler os pontos cegos. Se o alvo for lido por chave dinâmica, o mapa não basta.
3. Para mudança de contrato (dataclass, retorno de função, YAML estrutural):
   **instantâneo dourado antes**, comparar campo a campo depois. Foi o que garantiu a
   P-36 (39 registros) e a P-37 (38 cenários).
4. Rodar a suíte. Ela é o júri, não o guia.

---

## 12. Performance e escalabilidade — medido em 06/09/2026

O Osvaldo perguntou se estamos bem nas duas. **Estávamos mal na primeira, por um
motivo que também era um defeito de correção.**

### S-01 e S-02 — o cache que existia para acelerar era o defeito

**S-01.** `hash_custos()` era chamada **73 vezes por `alocar()`** — uma por consulta ao
cache de arrasto, que a usava na chave — e cada chamada **relia e re-hasheava os 33 KB**
do `custos.yaml`. **37% do tempo do motor** era gasto hasheando um arquivo para decidir
se podia usar um valor já calculado.

**S-02, e este é pior.** O cache global de `arrasto_anualizado` tinha na chave o hash do
**arquivo**. Mas o custo que a função usa vem do **`C` que chega como parâmetro**. Passar
um `C` alterado em memória — que é o que **todo teste faz**, via `deepcopy` — devolvia,
em silêncio, o valor calculado com o `C` original.

> Medido: com o CDI alterado de 13,9% para 50%, o arrasto voltava **idêntico**.
> Qualquer teste que alterasse um custo e conferisse arrasto ou dominância estava
> testando nada.

É a mesma família do F-02 e do N-01: um mecanismo que parecia funcionar e não
funcionava. E ensinou uma distinção que faltava:

| | do quê | serve a |
|---|---|---|
| `hash_custos()` | do **arquivo** em disco | **procedência** — de qual `custos.yaml` a saída nasceu |
| `impressao_de_custos(C)` | do **conteúdo** em memória | **correção de cache** — se dois cálculos podem compartilhar |

São iguais enquanto ninguém altera o `C` em memória. Todo teste altera. **Um cache cuja
chave não inclui a entrada não é um cache: é uma resposta errada guardada.**

`alocar()`: **9,79 ms → 2,75 ms**, e agora correto, que antes não era.

### Escalabilidade, por eixo — e os três eixos são diferentes

**Rotas do catálogo: quadrático, e não urgente.** Medido inflando o catálogo:

| rotas | `alocar()` | ms/rota |
|---|---|---|
| 25 | 12 ms | 0,48 |
| 100 | 68 ms | 0,68 |
| 400 | 728 ms | 1,82 |
| 800 | 2.810 ms | 3,51 |

A causa são quatro `next(v[0] for v in vivos if v[0].id == rid)` dentro de laços sobre
`pesos`. **Mas o input é limitado por desenho**: rota é um *tipo* de caminho, não um
papel — ação individual é uma *sleeve* dentro de `acao_zero`, não 400 rotas. O catálogo
realisticamente fica na casa das dezenas. É barato de consertar e não é o gargalo.

**Multiusuário: o gargalo é o carregamento, não o motor.** `carregar_politica()` custa
**82 ms** e `carregar()` **42 ms**. Para um usuário, irrelevante — são pagos uma vez.
Para N usuários × M chamadas, 124 ms de parse de YAML por chamada domina os 2,75 ms do
motor. É trivialmente cacheável **e ainda não foi feito** (P-41): fazer agora seria
otimizar para um cenário que não existe, e o S-02 é a prova de que cache mal
dimensionado custa correção.

**Fase 0 (dados da CVM): não existe.** O blueprint prevê DuckDB + Postgres + Parquet;
existe YAML e um CSV. Isso é adequado à fase — mas quem ler o blueprint e depois o
código vai achar que falta código, e não é isso: **a Fase 0 nunca rodou.**

### O veredito

**Performance: boa agora, e não era.** O que estava ruim não era lentidão — era um cache
que respondia errado, e a lentidão era o sintoma que fez olhar.

**Escalabilidade: boa no eixo que existe, não testada no que não existe.** A separação
motor/usuário (`perfil.yaml`) está feita e é o que importa para o segundo usuário. O
quadrático no catálogo é real e limitado por desenho. E não dá para afirmar nada sobre
o eixo de dados enquanto a Fase 0 não rodar — qualquer número aqui seria invenção.

---

## 13. P-40 fechada — lint e tipos, com cada dispensa justificada

**Zero, e não "poucos".** Uma barreira com baseline conhecida não é barreira: com 33
violações aceitas, a 34ª se esconde no ruído. Por isso a P-40 zerou antes de ligar a
guarda.

**A regra da casa vale para o próprio lint: toda dispensa tem motivo escrito**, e um
teste conta as linhas de justificativa — não dá para acrescentar um código de regra em
silêncio.

| dispensada | por quê |
|---|---|
| `E701`/`E702` | convenção da casa, 228 ocorrências, **nenhuma descuido**. Este código tem docstrings longas de propósito — elas carregam o achado, a fonte e o porquê. Espalhar o corpo afastaria o código da explicação que o justifica. |
| `E401` | `import os, sys, math` no topo; a lista é curta o bastante. |
| `E402` | `sys.path.insert` **antes** dos imports. Necessidade, não estilo — a alternativa é empacotar de verdade, que é mudança de estrutura. |
| `E731` | dois adaptadores de uma linha, usados logo abaixo. |
| `I001` | **incoerente com `E401`**: ele quer quebrar `import os, sys` em três linhas para poder ordená-las. Ligar uma regra que exige o que a outra dispensa é pedir para o lint brigar consigo mesmo. |

**`E501` ficou ligado**, ao contrário. As 39 linhas longas foram medidas antes de
decidir, e **seis delas eu mesmo criei na P-37** ao passar `P`, `pesos` e `alertas`
explicitamente para `espalhar` — viraram a tabela `BLOCOS_A_ESPALHAR`, que é melhor
código e cabe. Linha longa aqui costuma ser sintoma de assinatura que cresceu.

**As ferramentas ficam no grupo `lint` do pyproject, fora da impressão do ambiente.**
Não mudam número, então não pertencem à impressão que serve à reprodução (P-15); e
exigi-las instaladas deixaria vermelha a máquina de quem só quer rodar o motor.
**Vermelho que não é sobre o código ensina a ignorar vermelho.** Os testes pulam com o
comando que as liga.

### O que o lint achou de verdade

Pouco, e foi bom: 25 imports mortos, 5 f-strings sem placeholder, 2 nomes ambíguos, e
dois achados que valem por si:

**Um `None * float`** que o mypy não conseguia descartar em `pontuar()`. **Não era bug
em execução** — era um tipo que não dava para provar. Reescrito para calcular num local
e atribuir uma vez, ficou melhor e verificável em vez de argumentável.

**T-01 — há um terceiro catálogo.** `motor.montar_rotas` é paralelo ao `catalogo.yaml`:
**22 rotas contra 25, com 13 nomes que só existem lá**. A P-36 disse "os dois catálogos"
e havia três. Nenhum módulo de produção o chama — só o `test_motor.py`.

> O ruff viu uma **variável** morta; o defeito era a **chamada**. `B3V = val(C["b3"]
> ["vista_total_pct"])` era cópia da função de baixo, e a chamada **abortaria** se o
> valor fosse `NAO_CONFIRMADO` — dentro de uma função cuja docstring promete *"capturar
> InsumoBloqueado como marcador em vez de abortar"*.

Não foi apagado (P-43). **Apagar código com teste próprio sem medir o que os testes
guardam é como se perde uma rede.**

---

# Pendências fechadas — a narrativa completa

Migradas do `PENDENCIAS.md` em 06/09/2026. A tabela-resumo continua lá; aqui
está o texto inteiro de cada uma, para quem precisar reconstituir por que uma
decisão foi tomada daquele jeito.

---

## ~~P-03~~ · FECHADA em 05/09 — as seis citações conferidas

Cinco transcritas da fonte pública, uma **corrigida**: `ir_fii` citava a IN 1.585
art. 56, que está transcrito e não diz 20%. A base real é a **Lei 8.668/1993 art. 18
(red. Lei 9.779/1999)**. Era o único dos seis em que a fonte apontava para o lugar
errado — os outros cinco eram lacuna de leitura.

Teste novo impede que a categoria volte em silêncio.

---

## ~~P-07~~ · FECHADA em 05/09 — ordem dos portões virou dado

`politica.yaml → portoes.*.ordem` é iterado pelo motor. Portão sem `ordem` é erro
duro; portão declarado numa fase sem execução no motor também.

**Achado I-01 no caminho:** a ordem real **nunca foi G0→G8**. Sempre foi G6, G0, G1,
G2, G5, G3, G7, G8, G4 — G6 primeiro, G4 por último. A numeração sugeria uma sequência
que o código não executa, e a tabela do `CLAUDE.md` ensinava o modelo errado. Corrigida.

Um teste inverte a ordem no YAML e exige que o comportamento mude — se fosse
decorativa, ele passaria com qualquer sequência.

---

## ~~P-16~~ · RESOLVIDA em 05/09 — híbrido, e admite sem dado

**P-16a: híbrido.** O nível corta, a tendência marca sem poder de veto. A metade que
corta roda hoje; a que marca fica em `AGUARDA_SERIE` até a Fase 0 — mesmo padrão do
`REGRA_DECIDIDA`. O bloco não fica travado esperando: roda cego à direção e **diz que
está cego**.

**P-16b: admitir com marcação.** Contra a minha recomendação, e ele está certo:
admitir não inventa número nenhum, logo não fere a P1. Excluir por falta de dado seria
viés de sobrevivência pela porta dos fundos.

Registrei por que isso **não** contradiz o caso BOVV11: lá o custo era insumo de
**ordenação** e sem ele só dava para ranquear inventando zero. Solvência é critério de
**exclusão** — deixar de excluir não produz número falso.

**Falta decidir**, só quando a série existir: quantos trimestres a tendência olha, e o
que fazer com empresa jovem sem histórico.

---

## ~~P-21~~ · RESOLVIDA — aquele dinheiro não é reserva

*"É só considerar que aquele valor não é uma reserva."* Isso desfez o nó e um erro meu:
eu modelava os R$7.671 como reserva-empenhada e inventei `reserva_disponivel`. O modelo
certo é mais simples — é **caução de um meio de pagamento**.

`estado.yaml`: `reserva_atual: 0.00` e um bloco `deposito_garantia` à parte, fora do
G2 e fora do patrimônio. **Sua reserva de emergência é zero porque nunca foi
constituída**, não porque está travada.

**Rebaixei o J-02.** Eu havia escrito que a reserva seria "consumida pela dívida" e
falei em "correlação −1". Com o propósito declarado isso cai: o cartão é garantido, e
dívida coberta 14,5× pelo próprio depósito é pagamento antecipado, não risco. Deduzi
risco de uma estrutura sem perguntar o propósito dela.

---

## ~~P-26~~ · REFUTADA — o depósito compra limite 1 para 1

Eu havia calculado 14,5:1 e falado em "capital ocioso". **Errado.** Li "limite extra de
R$530" como se fosse o retorno inteiro, sem perguntar o limite total.

| | |
|---|---|
| limite base, sem cofrinho | R$ 1.349,99 |
| cofrinho, convertido **1:1** | R$ 7.671,01 |
| bônus por guardar (6,9%) | R$ 530,00 |
| **total** | **R$ 9.551,00** |

Fecha ao centavo com o que você informou. Não há capital ocioso, e não há o que
liberar sem perder limite na mesma medida.

---

## ~~P-33~~ · FALSO POSITIVO, retirada em 05/09

`aporte_extraordinario.registro` é uma **instrução ao humano** de 244 caracteres, não um
parâmetro. O primeiro inventário de dívida a listou porque eu classifiquei prosa à mão.
O guarda ganhou uma segunda porta — valor de 120 caracteres ou mais é parágrafo, não
configuração — e mandou apagar a linha. Um teste novo cobra o preço dessa regra: se
algum dia um valor longo virar comportamento, ele quebra.

---

## ~~P-24~~ · FECHADA em 05/09 — o G2 devolve composição, e apareceu um segundo achado

`RotaAloc.teto_de_saldo` existe, e o G2 passou a compor a reserva em vez de eleger uma
rota. O que o conserto encontrou pelo caminho vale mais que o conserto:

**K-02 é pior do que estava escrito.** Não é só que o portão "para de funcionar" quando
o produto enche. Com a isenção do Turbinado confirmada, o G2 antigo o elegeria avaliando
no alvo inteiro: **R$36.000 a 13,03% = R$4.692/ano**. O produto aceita **R$10.000**. O
número não era otimista — era **retorno sobre dinheiro que o produto recusa**. A
composição devolve R$4.112, que é o que existe. R$580/ano de ficção, 14%.

**O-01, achado novo.** O retorno de algumas rotas **depende do saldo**: o Tesouro Selic
é isento de custódia até R$10.000 e paga 0,20% a.a. acima disso. O G2 avaliava tudo no
alvo inteiro, e a média não descreve nenhum real — os dez mil primeiros rendem mais do
que ela diz, os vinte e seis mil seguintes, menos. Com retorno dependente de saldo,
**ordenar pela média e encher a primeira não dá o melhor resultado.** O critério certo é
o marginal.

| | destino | R$/ano | em emissor privado |
|---|---|---|---|
| rota única (antes) | RDB 100% CDI | 3.878,10 | R$ 36.000 |
| composição (agora) | Tesouro 10k + RDB 26k | 3.885,85 | R$ 26.000 |

**O ganho em reais é pequeno — R$7,75/ano — e dizer o contrário seria inflar o achado.**
O que muda de verdade é outra coisa: a rota única **obrigava a escolher** entre o melhor
retorno e o melhor crédito. A composição não escolhe: os R$10.000 do Tesouro saem do
emissor privado **sem custar retorno**.

`criterio_escolha_rota` passou de `retorno_liquido` para `retorno_liquido_marginal`, e o
valor antigo agora **levanta erro** em vez de ser aceito em silêncio — ele nomeia um
comportamento que o motor não faz mais.

**Duas rotas entraram no catálogo** (doutrina P6): `picpay_cofrinho` e
`picpay_turbinado`. A primeira é a única posição que você possui e **não existia no
catálogo** — o pior caso da P6: o sistema opinava sobre onde pôr dinheiro sem enxergar
onde o dinheiro está. Ela entra **sem a função LIQUIDEZ**, que é o achado J-01 inteiro:
0 a 29 dias de espera conforme o dia em que a emergência cair. O Turbinado entra
**bloqueado** — a isenção depende de missões que mudam todo mês e que o banco escolhe.

---

## ~~P-13~~ · FECHADA em 05/09 — `isento_ir` virou dois campos

`isento_ir_rendimento` (bool) e `aliquota_ganho` (float ou `None`). `None` significa
"usa a tabela geral", **não** zero — confundir os dois seria o F-02 outra vez, com
ausência virando o número mais favorável.

O campo antigo virou propriedade que lê o novo: ele **sempre** se referiu ao
rendimento, e o rename só tornou isso explícito. Um teste garante que nenhum chamador
antigo mudou de resposta.

---

## ~~P-14~~ · RESOLVIDA em 05/09 — construir a fonte do BCB

**Banco não sai do universo.** Eu havia oferecido três variantes de excluir e
recomendado uma; isso contradiz a regra fundadora do projeto, agora escrita como
doutrina P6.

Meu argumento — "se a A05 der núcleo indexado, o bloco nunca roda" — é verdadeiro e
**irrelevante**: ele justifica *adiar a construção*, nunca *excluir o ativo*. Confundi
ordem de trabalho com escopo.

**Consequência:** a Fase 0 passa a ter duas esteiras — CVM (societária → bloco C) e BCB
(prudencial → bloco de banco). Aumento de escopo decidido **antes** de construir, que
era exatamente o ponto do achado H-02.

**Continua aberto:** a ordem entre as duas esteiras. Aí o argumento da A05 vale — a
esteira da CVM serve aos dois caminhos, a do BCB só a um.

---

---

## ~~P-15~~ · FECHADA em 05/09 — `pyproject.toml` + `ambiente.py`

Não era higiene: era um furo na promessa central. O pré-registro afirma que um
resultado de backtest é reproduzível, e o `.gitattributes` + o hash da série protegiam
*o dado*. As versões de `numpy` e `pandas` que produziram os números **não estavam
registradas em lugar nenhum** — e `alfa_contra_fatores` passa por
`numpy.linalg.lstsq`, que é uma implementação, não um teorema.

**Três regras, com severidades diferentes de propósito:**

| | severidade |
|---|---|
| toda dependência importada está declarada, e vice-versa | **erro duro** |
| a impressão em `politica.yaml` bate com o `pyproject` | **erro duro** |
| a versão instalada é a registrada | **aviso** |

A assimetria é a decisão de desenho. Um teste vermelho porque a sua máquina tem outro
`numpy` puniria trabalho legítimo com um alarme que não é sobre o código. Quem carrega
o alarme é o **resultado** — `alfa_contra_fatores()["ambiente"]` traz
`reproduz_o_registrado` —, não a suíte. Mesmo mecanismo do `expira`.

**As versões vivem só no `pyproject.toml`.** O `politica.yaml` guarda a impressão
digital (`7565df1381e2c1ed`) calculada a partir dele. Não há `requirements.txt` de
propósito: duas listas concordando é o N-01. O comando sai da lista:

```powershell
python ambiente.py --instalar
```

Dependências classificadas por **consequência**: `numpy` e `pandas` são *numéricas*;
`PyYAML` e `pytest` são *ferramentas*.

**O que não cobre, declarado:** sistema operacional, BLAS e arquitetura de CPU
continuam fora e podem mover a última casa de uma regressão.

**Na terça:** se `python ambiente.py` acusar versões diferentes, isso é informação
correta e não um problema a consertar às pressas. Rode o comando de instalação se
quiser reproduzir os números registrados; se preferir suas versões, os 224 testes
continuam válidos e o backtest passa a produzir número novo em vez de conferir o
antigo. **A decisão é sua e agora ela é visível** — que era exatamente o que faltava.

---

## ~~P-36~~ · FECHADA em 05/09 — o catálogo saiu do Python, e trouxe dois achados

| | antes | depois |
|---|---|---|
| `alocacao.catalogo()` | 183 linhas, 25 rotas em literais | **39 linhas** + `catalogo.yaml` |
| `corretoras.catalogo_instituicoes()` | 136 linhas, 24 casas em literais | **32 linhas** + `instituicoes.yaml` |

**As duas migrações foram conferidas campo a campo contra o objeto anterior: zero
diferenças.** Não é detalhe de processo — é o único jeito de mover 39 registros com ~15
campos cada sem introduzir um erro silencioso.

**Valor que vem do `custos.yaml` ficou como referência, nunca cópia:**
`adm_aa: {de: etf.PIBB11}`. Copiar o número seria o N-01 em escala de catálogo, e
mataria `expira`, `status` e `bloqueia` da constante. Um teste prova pelo comportamento:
mexer na constante *tem* de mexer na rota.

### Q-01 · insumo bloqueado derrubava o catálogo inteiro

O tratamento era **inconsistente**, e as duas metades nunca se encontravam no mesmo
teste: rotas de ETF **degradavam** (entravam sem a taxa e com o motivo escrito — foi
assim que o BOVV11 ficou visível); todas as outras **explodiam** dentro de `catalogo()`.

Uma constante `NAO_CONFIRMADO` em `corretagem.safra_terra` apagaria as 25 rotas,
**inclusive as 24 que não dependem dela** — o oposto exato da P6. Regra única agora:
insumo bloqueado bloqueia **a rota**.

### Q-02 · a letra sempre falou de custos, e o registro não sabia dizer

`confirmacao` era uma letra por instituição, aplicada como **multiplicador de tudo**.
Mas sempre significou *"os **custos** podem ser lidos em fonte oficial"* — a própria
`regra` do multiplicador diz isso. BTG, Bradesco, Mirae e Avenue têm `N` com `fonte`
dizendo *"BCB IF.data 03/2026 (porte) — custos NÃO OBTIDOS"*: o balanço vem do **Banco
Central** e o índice de reclamações, do **ranking do BC**.

**O comportamento estava certo. O registro é que não sabia dizer** — um leitor
concluiria que o dado de balanço do BTG é duvidoso, quando veio do regulador.

Procedência passou a ser **por grupo de campos**, e `confirmacao` virou **derivada** de
`custos.procedencia.status`. Dois campos que podiam discordar viraram um.

**Declarado, não consertado:** a granularidade é por grupo, não por campo. Por campo
seriam 24 × 15 = 360 blocos para cinco fontes reais, e registro que ninguém lê é pior
que registro nenhum.

---

## ~~P-37~~ · FECHADA em 05/09 — e o achado só apareceu depois da quebra

`alocar()` virou seis passos: `_preparar` (16), `fase_aporte` (43), `fase_universo`
(17), `distribuir_por_funcao` (46), `alocar` (51). A quebra segue **as fases que já
existiam no YAML**, não um critério novo. Maior função do motor hoje: `g2_reserva`, 102
linhas — e um teste novo impede que a próxima passe de 120 sem alguém decidir.

**A garantia:** 38 cenários serializados campo a campo antes — pesos, **cada string de
alerta**, cada pendência, cada rota em cada lista de rejeição. A única diferença em toda
a matriz é o próprio `politica_hash`, que mudou porque o `politica.yaml` mudou.

### R-01 · a ordem dos portões era um dado que só aceitava 18 de 120 valores

**Só foi possível encontrar depois da quebra** — é o argumento inteiro da P-37. Com
`fase_universo` isolada dá para permutar a ordem e observar o resultado sem rodar a
alocação inteira; com 300 linhas, não dava.

A P-07 declarou a ordem como dado e afirmou que trocá-la é um commit no YAML. **Falso
para 102 das 120 ordens.** Os portões mudam a **forma** do que trafega: o `G3_atrito` é
o único que transforma (entra rota, sai `(rota, custo)`) e `G4`, `G7` e `G8` consomem
pares. Qualquer um antes do G3 estourava com `TypeError` no fundo de uma função de
portão, nunca dizendo que a ordem era o problema.

| | ordens | |
|---|---|---|
| rodam | 18 | |
| recusadas com mensagem clara | 90 | novo |
| `InsumoBloqueado` | 12 | **não é defeito** — guarda do F-02 disparando |

Cada portão passou a declarar `consome`/`produz`. Declarar a ordem como dado sem
declarar o contrato era declarar uma liberdade que não existe — mesma família do F-05.

---

## ~~P-38~~ · FECHADA em 06/09 — e o problema era maior que a pendência

`conftest.py` com fixtures `custos`/`politica` e uma guarda que **acusa o teste que
suja estado compartilhado, nomeia o objeto e restaura** para que só o culpado fique
vermelho.

**A escolha de desenho:** copiar sempre custaria 0,23 s e *esconderia* o defeito;
detectar custa 0,38 s e o *reporta*. Este projeto detecta — esconder defeito atrás de
cópia é o padrão que ele passou a semana rejeitando. Declarado no arquivo: a guarda
mora no teardown, então o pytest rotula **ERROR**, não FAILED. Dá para relabelar com um
hook; não foi feito, porque seriam dez linhas de esperteza para mudar uma palavra.

---

## ~~S-01~~ e ~~S-02~~ · FECHADOS em 06/09 — o cache que acelerava era o defeito

**S-01:** `hash_custos()` era chamada **73 vezes por `alocar()`** e cada chamada relia e
re-hasheava os 33 KB do `custos.yaml`. **37% do tempo do motor.**

**S-02, pior:** o cache global de `arrasto_anualizado` tinha na chave o hash do
**arquivo**, mas o custo vem do **`C` que chega como parâmetro**. Passar um `C` alterado
em memória — o que **todo teste faz** — devolvia o valor do original, em silêncio.
Medido: com o CDI de 13,9% para 50%, o arrasto voltava idêntico. **Qualquer teste que
alterasse um custo e conferisse arrasto ou dominância estava testando nada.**

Nasceu a distinção que faltava: `hash_custos()` é do **arquivo** e serve à
**procedência**; `impressao_de_custos()` é do **conteúdo** e serve à **correção de
cache**. `alocar()`: 9,79 ms → **2,75 ms**, e correto.

---

## ~~P-39~~ · FECHADA em 06/09 — `impacto.py`, o mapa que não existia

Pergunta do Osvaldo: *como você rastreia onde o que foi alterado interage com os outros
arquivos?* A resposta honesta era **suíte + grep + instantâneo dourado, e nenhum mapa**.

`python impacto.py <constante | função | campo>` responde antes de editar. Reporta os
**14 pontos cegos** junto — chave montada em tempo de execução, `getattr` dinâmico,
despacho por dicionário. Três testes impedem o mapa de mentir, e o terceiro é o que
separa mapa de desenho: **alterar a constante que o mapa aponta tem de mudar exatamente
as rotas que ele diz.**

---

## ~~P-40~~ · FECHADA em 06/09 — ruff e mypy em zero, ligados à suíte

**Zero, e não "poucos".** Barreira com baseline conhecida não é barreira: com 33
violações aceitas, a 34ª se esconde no ruído.

**Toda dispensa tem motivo escrito no `pyproject.toml`**, e um teste conta as linhas de
justificativa — não dá para acrescentar um código de regra em silêncio. `E701`/`E702`
são convenção da casa (228 ocorrências, nenhuma descuido); `I001` saiu por ser
**incoerente com `E401`**; `E501` ficou **ligado**, porque seis das linhas longas eu
criei na P-37 e viraram uma tabela.

As ferramentas ficam no grupo `lint`, **fora da impressão do ambiente** — não mudam
número, e exigi-las instaladas deixaria vermelha a máquina de quem só quer rodar o
motor. Os testes **pulam** com o comando que as liga. **Na terça isso vai pular, e está
certo.**

**O que achou:** 25 imports mortos, 5 f-strings vazias, 2 nomes ambíguos, 1 `None *
float` que não era bug em execução (era tipo não provável — o código ficou melhor), e o
T-01 abaixo.

---


# CLAUDE.md

Instruções para qualquer sessão do Claude que trabalhe neste repositório.
Leia inteiro antes de tocar em código. Se algo aqui contradisser o que você acha
razoável, o arquivo ganha — ou você argumenta contra ele explicitamente, e nesse
caso a conversa é sobre mudar o arquivo, não sobre ignorá-lo.

---

## 1. O que é este projeto

Um sistema pessoal de análise e aporte de investimentos, do Osvaldo. Ele é
engenheiro civil, analista de planejamento, PJ sem previdência, com um contrato
único. O sistema é **inspirado no Bastter.com e existe para corrigi-lo**: a
premissa é que o método do Bastter acerta na disciplina e erra ao apresentar
como derivado o que é escolha, e como regra o que é preferência.

O objetivo não é replicar um método. É construir um em que **toda decisão tenha
procedência**: de onde veio o número, quem escolheu a regra, e o que aconteceria
se a escolha fosse outra.

### O que este sistema NÃO é

- Não é um robô de recomendação. Ele **recusa-se a nomear empresas** enquanto a
  decisão A05 (núcleo indexado × seleção ativa) estiver pendente.
- Não é um otimizador. DeMiguel, Garlappi & Uppal (2009): 14 modelos de
  otimização, nenhum bateu 1/N fora da amostra. Para 25 ativos seriam necessários
  ~3.000 meses de dados. Regra declarada e testável, nunca ótimo derivado.
- Não é um backtest rodando atrás de um resultado. As nove estratégias estão
  **pré-registradas com ordem de execução** antes de qualquer dado ser tocado.

---

## 2. As sete doutrinas

Estas são o projeto. Código que as viola está errado mesmo que os testes passem.

### P1 — Procedência por valor, não por bloco

Cada constante em `custos.yaml` carrega `status` (`COMPLETO` / `PARCIAL` /
`NAO_CONFIRMADO` / `OBSERVADO`), `fonte`, `acesso`, e o que ela `bloqueia`.
**Um cálculo que dependa de valor bloqueado recusa-se a rodar** — levanta
`InsumoBloqueado`, não devolve zero, não devolve um padrão, não avisa e segue.

> Isto já foi violado uma vez, e do jeito mais caro possível. `simular_custo` não
> olhava `bloqueios`, então a rota BOVV11 (taxa `NAO_CONFIRMADO`) simulava com
> custo zero — e **zero ganha de todo mundo**, então ela aparecia como a rota mais
> barata do catálogo. Achado F-02. Se você criar qualquer caminho novo em que um
> insumo ausente vire um número, é o mesmo erro outra vez.

`OBSERVADO` é uma quarta categoria de propósito: valor **contado no dado real**,
não documentado pela fonte. As enumerações da CVM são assim. Um parser que
encontre valor fora de uma lista `OBSERVADO` deve **falhar ruidosamente**.

### P2 — Regras como dados

Todo parâmetro vive em YAML versionado, nunca em código. Trocar política é um
commit no `.yaml`, jamais um deploy.

Dois testes protegem isso, e eles são complementares:
- `test_cobertura_yaml_secoes_operacionais` falha se uma chave declarada nunca
  for lida. **Chave não lida é mentira documental** — quem lê o YAML acredita
  que o sistema faz algo que ele não faz.
- O teste inverso varre literais numéricos no módulo.

Já pegou dois casos reais: `conta_como_liquidez` e `exclusividade`, ambos
declarados e nunca implementados.

**Fechada em 05/09:** a ordem dos portões era a dívida mais antiga da P2 — cada um
tinha `ativo` como dado e a sequência vivia no código. Agora `politica.yaml →
portoes.*.ordem` é iterado pelo motor. Portão sem `ordem` é erro duro, e portão
declarado numa fase sem execução no motor também: declarar sem implementar é o erro
que a P2 existe para pegar, e ele vale nos dois sentidos.

### P3 — Portões, não pontuação

**A numeração NÃO é a ordem.** Isso enganou por semanas e é o achado I-01. A
sequência real, agora declarada em `politica.yaml → portoes.*.ordem` e **iterada**
pelo motor, é:

| # | portão | fase | o que decide |
|---|---|---|---|
| 1 | G6 coerência função-rota | universo | rota incoerente perde a **função**, não o catálogo. Roda antes de tudo: é pré-condição do catálogo |
| 2 | G0 match empregador | aporte | desligado (`ativo: false`) — ele é PJ, não existe match |
| 3 | G1 dívida | aporte | líquido × líquido, nunca dívida efetiva × retorno bruto |
| 4 | G2 reserva | aporte | com `exclusividade`; escolhe por retorno líquido, não por ordem alfabética |
| 5 | G5 status | universo | **antes do G3** — status é pré-condição de comparação de custo (F-02) |
| 6 | G3 atrito | universo | separa custo FIXO (dilui, calcula o aporte de reentrada) de PERCENTUAL (não dilui, a rota nunca volta) |
| 7 | G7 tese registrada | universo | sem tese, sem peso |
| 8 | G8 compromisso de carrego | universo | a duração vem do papel que o usuário se compromete a carregar, nunca do catálogo |
| 9 | G4 dominância | universo | só elimina se a rota perder em **todos** os horizontes; se inverte com o horizonte, sai como `PREFERENCIA_DE_HORIZONTE` |

Cada portão elimina por um motivo nomeado, e a eliminação é reportada com o motivo.
Nada de score agregado que esconde qual critério matou o quê.

**Duas fases, porque são dois tipos de decisão.** `aporte` decide *quanto* dinheiro
segue e pode encerrar o pipeline; `universo` decide *quais* rotas seguem e nunca
encerra. Trocar a ordem dentro de uma fase é um commit no YAML. Trocar um portão de
fase não é reordenação, é redesenho — o motor recusa.

### P4 — Pré-registro com impressão digital

Teses (K02/K03/K04) e carregos (C01–C06) em `teses.yaml`, cada um com um hash
`impressao()` de 16 caracteres. Reescrever uma tese depois do fato é possível —
mas deixa rastro. Validadores rejeitam condição de **preço** em K04 e C03: "se
cair 30%" não é evento que invalida uma tese, é o preço machucando a posição.

O pré-registro do backtest já foi corrigido uma vez, e essa correção só foi
legítima porque aconteceu **antes** de qualquer dado ser tocado: a premissa
"valor não paga no Brasil" estava errada — HML paga 0,688%/mês, t = 2,60 na
série primária do NEFIN.

### P5 — Limitações declaradas

`politica.yaml → limitacoes_declaradas` lista o que o motor **sabe que não
modela**, com a *direção do viés* e a condição em que deixa de importar. Três
hoje: IR na venda de renda variável, periodicidade da custódia do Tesouro, e a
ordem dos portões.

Um limite escrito não vira surpresa depois. Se você descobrir algo que o motor
não modela e não puder modelar agora, o lugar dele é aqui — não num comentário.

### P6 — Ausência de critério não é critério de exclusão

Ativo, classe ou empresa **não sai do universo** por o projeto ainda não ter régua
para ele. Falta de critério é tarefa aberta, não veredito. O que sai por falta de
dado é o **peso**, nunca a presença no catálogo: a rota fica visível, bloqueada e
com o motivo escrito, para que não considerar seja uma decisão e não uma omissão.

> Esta é a regra fundadora do projeto, e ela virou doutrina em 05/09/2026 **depois
> de a mesma correção ser necessária três vezes** — todas contra mim:
>
> 1. Tirei Tesouro IPCA+ e cripto do catálogo por não haver regra. Nasceram a função
>    `PROTECAO_REAL` e o registro `CARREGO`.
> 2. LCI, LCA e FII estavam em `fora_de_escopo`. Viraram rotas bloqueadas por insumo.
> 3. Ofereci três variantes de excluir banco e **recomendei uma**. Correção dele:
>    *"as maiores ações do Brasil de empresas privadas são Itaú, Bradesco e Ambev,
>    duas delas são bancos... não deve ser excluído, deve ser encontrado o critério."*
>
> Se for necessária uma quarta vez, o problema não é dele.

**Só há dois fundamentos legítimos para exclusão permanente**, e ambos precisam estar
declarados no campo `fundamento`:

- `DECISAO_DO_USUARIO` — ele decidiu que **não quer** aquilo, podendo ter. É
  preferência declarada, e sobrevive à carteira mudar.
- `CRITERIO_MEDIDO` — a régua existe, foi aplicada, o ativo reprovou (fundos DI e
  multimercado, por custo).

Não são fundamento: "ainda não temos régua", "não avaliados individualmente",
"complexo demais" — descrevem o estado do **projeto**. E, por correção dele em 05/09,
**"o usuário não opera aquilo"** — isso descreve o estado da **carteira**, que hoje é
um cofrinho no PicPay e mais nada. Numa carteira vazia, "não opero X" é verdade para
todo X, e portanto não distingue nada.

> **A armadilha da pergunta factual.** Eu perguntei "você opera opções?", ele
> respondeu "não", e eu tratei isso como decisão de escopo. A pergunta media um
> **fato** e eu li como **preferência**. A forma certa é *"você quer que X fique fora,
> podendo tê-lo?"* — essa tem resposta que sobrevive à carteira mudar.
>
> Vale para toda sessão: **resposta factual não autoriza exclusão.** Se a régua não
> existe, a pergunta certa não é se o ativo fica, é quanto custa construí-la.

Dois testes guardam isso: `test_nada_sai_do_universo_por_falta_de_regua` recusa
exclusão permanente sem fundamento — foi ele que encontrou imóvel/consórcio/COE,
excluído por argumento geral sem medição (P-19) — e
`test_nao_operar_nao_e_fundamento_de_exclusao` recusa fundamento apoiado em estado.

**O que a P6 não proíbe:** peso zero. Uma rota pode ficar em zero indefinidamente por
insumo bloqueado ou tese ausente — isso é o sistema funcionando. A diferença entre
peso zero e exclusão é que o primeiro é visível, contável e reversível por um número
que chega.

### P7 — Uma rotina que depende de alguém lembrar não é uma rotina

Doutrina nova, **06/09/2026, e ela é dele** (achado W-01). Eu ofereci montar um lembrete
semanal para a captura da CVM. A resposta:

> *"o lembrete no caso seria exatamente para quê? uma das coisas do projeto é
> estabilidade, e um projeto escalável não deve depender de mim para funcionar."*

Está certo, e é **a terceira vez que eu cometo o mesmo erro** — pôr o Osvaldo no caminho
crítico de algo que é do sistema. Foi a U-01 (reserva e aporte como bloqueio de
desenvolvimento), foi a P6 (falta de régua virando ausência de ativo), e agora isto.

**A regra:** todo processo periódico do sistema tem que rodar **sem intervenção humana**,
ou ser **declarado como limitação** com a mesma seriedade de `limitacoes_declaradas`. Não
existe terceira opção chamada "eu lembro".

O teste, e ele é simples de aplicar: *se esta ferramenta fosse vendida, o cliente teria
que lembrar disso?* Se a resposta é não, o lembrete é dívida disfarçada de solução.

**O que isso proíbe na prática:** lembrete, alarme, tarefa agendada que só notifica, item
de checklist manual, "toda terça eu rodo". **O que isso exige:** gatilho automático,
verificação idempotente, e um registro que diga quando a rotina rodou pela última vez —
para que a falha seja *visível*, e não descoberta seis meses depois por um buraco na
série.

> **Onde a doutrina dói — e a resposta apareceu no mesmo dia.** A máquina dele fica
> desligada quase sempre, e a captura semanal precisa de rede e disco. O executor é
> **GitHub Actions em repositório privado**: cron nativo, 14 GB de disco efêmero, 6 h por
> job, 2.000 min/mês, e — o detalhe que decide — a regra que desativa cron por inatividade
> **só vale para repositório público**. Ver `docs/fontes/executor-da-rotina-semanal.md` e
> a P-57.
>
> Até a primeira execução real existir, a P7 continua mandando **declarar a limitação**.
> Página de limite lida não é rotina rodando.

---

## 3. Como rodar

```bash
cd alocacao
python ambiente.py           # confere o ambiente ANTES de acreditar num número
python -m pytest -q          # 269 testes, ~7,8 s
ruff check . && mypy .       # ambos em ZERO (P-40); pulam se não instalados
python impacto.py <alvo>     # o que alcança uma constante, função ou campo
python demo_aporte.py        # motor de aporte
python cenarios.py           # varredura de cenários
```

**Dependências: só no `pyproject.toml`, com pino exato (`==`), e em lugar nenhum
mais.** Não existe `requirements.txt` de propósito — duas listas de versões que
concordam é o achado N-01: editar uma não muda nada e ninguém descobre. O comando de
instalação se deriva da lista:

```bash
python ambiente.py --instalar    # imprime o pip install exato
```

**Se `ambiente.py` disser que o `numpy` ou o `pandas` são diferentes, a suíte continua
verde e isso está certo.** O que deixa de valer não é o código: é a *reprodução* de um
resultado pré-registrado, que passa a ser um número novo em vez da conferência de um
antigo. Quem carrega esse aviso é o resultado (`alfa_contra_fatores()["ambiente"]`),
não a suíte. Ver seção 10.

---

## 4. Mapa dos arquivos

```
alocacao/
  motor.py         val(), InsumoBloqueado, custodia_rv_aa(). A porta de entrada
                   de todo insumo. Se algo lê custos.yaml sem passar por val(),
                   está furando a P1.
  custos.yaml      constantes com procedência por valor
  politica.yaml    o MOTOR: funções, portões, doutrinas, regimes, pré-registro.
                   Vale independente de quem usa.
  perfil.yaml      UM usuário: `compromissos` e `decisoes`. Um segundo usuário é um
                   segundo arquivo destes, nunca uma edição no politica.yaml.
                   `carregar_politica()` funde os dois na carga — achado L-01.
  alocacao.py      catálogo de rotas, portões G0–G8, motor de aporte
  tese.py          validadores de tese e carrego + impressao()
  teses.yaml       registros K e C. Dois estados: REGRA_DECIDIDA (regras seladas,
                   posicao nao existe, G8 NAO libera peso) e COMPROMISSO_ATIVO
                   (tudo preenchido). Achado G-01 — ver secao 9.
  estado.yaml      situação financeira real — PRIVADO
  estado_io.py     validação do estado; bloqueia status != REAL, data futura, aporte <= 0
  reserva.py       simulação da fase de reserva
  aporte.py        piso + extraordinário
  fatores.py       fatores NEFIN; alfa contra 4 fatores
  corretoras.py    ranking de corretoras + teste de robustez
  sleeve.py        fração de RV
  cenarios.py      varredura
  dados/nefin_factors.csv    6.321 sessões, 2001-01-02 a 2026-07-03
docs/fontes/       32 .md de fonte primária + README.md com o índice de extração
auditoria/         laudos de escopo e definições
  regimes-de-leitura-de-balanco.md   por que uma régua só não serve (06/09)
  regime-incorporacao.md             o regime de construção, decidido POR ELE (06/09)
pesquisa-custos-2026-08/   pesquisa de custos de agosto/2026
```

**Armadilha:** `pesquisa-custos-2026-08/calc/` contém um `motor.py` e um
`custos.yaml` **antigos e diferentes** dos de `alocacao/`. São a versão de
agosto. Nunca importe de lá.

---

## 5. Convenções

- **Código e YAML em ASCII.** Comentários, docstrings e valores de `.py` e
  `.yaml` sem acento (`alocacao`, `portoes`, `funcao`). Markdown usa acento
  normal. Não "conserte" isso.
- **Comentário explica o porquê, não o quê.** O estilo da casa é nomear o achado
  que motivou a linha: `# A-02: custo percentual nao dilui`. Um comentário que
  parafraseia o código é ruído.
- **Um achado, um teste que falha na versão anterior.** Teste que passaria antes
  e depois não documenta nada. O teste do F-01 não checa se o campo existe — ele
  compara **duas simulações** e exige diferença > 1% do custo total, porque um
  campo declarado e nunca lido passaria num teste de atributo.
- **`REGISTRO-vN.md`** por rodada de mudança, com o achado, o número, o efeito
  medido e o que quebrou.

---

## 5-A. Três regras permanentes de sessão

Decididas por ele em 05/09/2026. Valem em **toda** sessão, sem ele precisar pedir.

### Sempre registrar as pendências

`PENDENCIAS.md`, na raiz, é o registro único e vivo. Atualize-o **antes de
encerrar a sessão**, não durante — o que sobrou só se sabe no fim.

Cada pendência precisa de **dono**, **gatilho** e **classe**. Sem os três não é
pendência, é desabafo. Gatilho é o evento que a torna acionável ("antes de escrever
o parser"), e "nenhum" é resposta válida.

**A classe é obrigatória desde 06/09 (achado U-01)**, e existe porque sem ela eu
coloquei dado pessoal do Osvaldo no caminho crítico do projeto:

| classe | o que significa |
|---|---|
| `BLOQUEIA_O_SISTEMA` | o sistema não faz o trabalho dele. **É o caminho crítico.** |
| `DECISAO_DE_DESENHO` | precisa de *um* humano decidindo sobre o sistema — qualquer dono de produto responderia |
| `DADO_DE_UM_USUARIO` | o estado de **uma** carteira. **Nunca** bloqueia desenvolvimento |

Hoje são 22 / 5 / **2**. As duas da última classe são P-01 e P-02, e eu tinha as
duas no caminho crítico. Antes de chamar algo de bloqueio, pergunte: **um cliente
novo desta ferramenta teria isso?** Se não teria, o sistema precisa funcionar sem.

Pendência fechada não some: vai para a tabela do fim, com a data. O histórico do
que já foi resolvido é o que impede a sessão seguinte de reabrir tarefa pronta —
o que já aconteceu três vezes neste projeto.

### Sempre terminar indicando o próximo passo

Toda sessão fecha nomeando **qual é o próximo passo do planejamento**. Não uma
lista do que dá para fazer — *o* próximo passo, escolhido e justificado.

Se não houver planejamento que cubra o momento, **elabore um** em vez de
devolver a pergunta. Um plano aqui é: o que vem primeiro, por que ele antes dos
outros, o que ele destrava, e o que o impede hoje. Sem essas quatro coisas é
lista de desejos.

Duas obrigações que a experiência deste projeto impôs:

- **Marque o que exige o desktop.** Metade dos passos precisa de comando na
  máquina dele; misturar os dois na mesma fila fez com que tarefas já concluídas
  fossem reabertas três vezes.
- **Revise a fila da seção 7 quando ela mudar.** Em 05/09 ela listava três itens
  já concluídos naquele mesmo dia. Fila desatualizada é pior que fila nenhuma:
  ela parece confiável.

### Sempre registrar o que fazer quando a sessão voltar ao desktop

Este projeto roda em duas sessões com poderes diferentes, e confundi-las custa caro:

- **Cowork (nuvem, esta aqui).** Lê e escreve arquivos, roda Python, publica
  artefatos. Grava na pasta dele pela ponte — que só existe com o desktop ligado.
  **Não executa comando na máquina dele.**
- **Claude Code (local, no desktop).** Tem shell na máquina: PowerShell, git,
  download, e os 1,5 GB de dado bruto de `data\`.

Toda sessão Cowork termina com a seção `## Ao voltar ao desktop` no fim do
`PENDENCIAS.md`: o que ficou pendente de gravação, e o que precisa da sessão local
porque exige comando. Sem isso o trabalho fica no chat e se perde.

**Regra de encaminhamento:** tarefa que precisa de PowerShell, git, download ou do
dado bruto **é para a sessão local**. Diga isso em vez de simular. Já houve duas
tarefas assim; cumpri-las daqui teria produzido contagem inventada ou script que
nunca rodou — num projeto cuja doutrina inteira é procedência, esse é o pior
resultado possível, pior que não fazer.

---

## 6. Como trabalhar com o Osvaldo

Instruções permanentes dele, que valem em toda sessão:

- **Mostre onde ele está errado.** Ele pede isso explicitamente e ele leva a
  sério. Concordar por educação é a pior coisa que se pode entregar aqui.
- **Não concorde com o Bastter por afinidade.** O projeto existe porque o método
  tem defeitos. Repetir os defeitos com sotaque técnico é falha.
- **Traga coisas que ele não sabe que existem.** Ele valoriza o achado lateral
  mais que a confirmação.
- **Análise profunda, nunca superficial.** É a preferência declarada dele.
- **Pergunte antes quando a resposta muda o resultado.** Não pergunte por
  cortesia; pergunte quando o caminho bifurca de verdade.
- **Pergunte o número inteiro antes de calcular uma razão.** Três vezes em dois dias
  eu deduzi a situação dele de um fragmento: excluí banco por falta de régua, li "não
  opero opções" como preferência, e calculei 14,5:1 de troca depósito-limite sem
  perguntar o limite total — que era 1:1. O padrão é sempre o mesmo: um dado parcial
  sustenta uma conclusão que o dado completo derruba.
- **Não confunda o que ele faz com o que ele quer.** A carteira dele hoje é um
  cofrinho no PicPay e nada mais. Toda pergunta do tipo "você opera X?" tem a mesma
  resposta, e nenhuma delas é uma preferência. Pergunte por decisão, não por estado —
  ver a armadilha registrada na doutrina P6.
- **O processo é orgânico e sem pressa.** Não force conclusão. Ele tem plano
  limitado do Claude — não gaste turno reexplicando o que já está escrito aqui.

### As críticas dele que mudaram o sistema

Registradas porque cada uma foi um erro meu que ele pegou:

1. *"os investimentos não devem sair por não ter regras"* — eu tinha feito
   ausência-de-regra produzir ausência-de-ativo. Um default silencioso na
   direção oposta. Virou a função `PROTECAO_REAL` e o registro `CARREGO`.
2. *"nenhum compromisso maior que 10 anos"* — uma quarta postura, melhor que as
   três que a fonte oferecia, porque não depende de um horizonte revisável.
3. *"o aporte mensal não é verdade em pedra"* — falha real de modelagem. Aporte
   virou piso + extraordinário.
4. A crítica ao Bessembinder: estatística **incondicional** não responde uma
   pergunta **condicional**. "55% das ações perdem da T-bill" é sobre todas as
   ações; investir por critério é uma subamostra. Levou a elevar o
   `portao_de_exclusao_v1` no pré-registro e a registrar `criterio_nao_e_previsao`.
5. *"alguns aspectos ficaram de fora"* (corretoras) — três eram mensuráveis e eu
   não tinha buscado. O Ranking de Reclamações do BCB é fonte **primária e
   oficial** e eu havia ignorado.

---

## 7. Onde o projeto está

**Fase A — formar a reserva.** Até **~mai/2031**, recalculado em 05/09 (achado M-01).
O projeto dizia "~mar/2030", número calculado com R$7.671 de reserva inicial — e a
reserva é **zero**. São 56 meses, não 42.

> **M-01, e vale mais que a data.** Trocar o *destino* do aporte move o prazo em
> **3 meses** (56 no cofrinho de 102%, 56 no `td_reserva`, 54 no Turbinado, 62 na
> poupança). Trocar o *aporte* move **33** (56 meses a R$500, 32 a R$1.000, 17 a
> R$2.000). O G2 é o único portão com trabalho a fazer na Fase A, e decide a alavanca
> de 3 meses; a de 33 — quanto entra — não passa por portão nenhum.
>
> Isso **não** é argumento para desligar o G2: na Fase B e C os valores são maiores e
> a diferença de custo compõe. Vale para a Fase A especificamente. Se ele perguntar
> "onde ponho a reserva", a resposta honesta começa por: quase qualquer lugar serve; o
> que muda o prazo é começar a aportar.

| camada | estado |
|---|---|
| 0 · pipeline de dados (CVM DFP/ITR, COTAHIST, bitemporalidade) | **não iniciada** — maior peça restante |
| 1 · motor de custo | completa |
| 2 · portões G0–G8 | completa |
| 3 · alocação alvo | completa |
| 4 · custo de discordar | completa |
| 5 · motor de aporte | completa, ociosa até a reserva fechar |
| 6 · catálogo de campos (blocos A–M) | especificada. **Regimes** dos blocos C (solvência) e de instituição financeira escritos em 05/09 — a execução depende da Fase 0 |
| 7 · backtest | pré-registrado, não executado |
| — · fatores NEFIN, fase de reserva | completas, **fora do plano original** |

As duas camadas fora do plano são as que mais mudaram decisões. O blueprint foi
escrito sem conhecer o estado financeiro real e otimizou a parte do sistema que
só será usada em 2031.

> **X-01 — o dado estruturado não alcança a decisão. 06/09/2026, e é o achado mais caro
> desta sessão.**
>
> O Osvaldo respondeu como se lê uma incorporadora (`auditoria/regime-incorporacao.md`).
> A sequência dele tem dez passos. **Três são obtíveis nas 8 demonstrações estruturadas da
> CVM.** VSO, vendas líquidas, distratos, receita a apropriar, unidades em estoque, e a
> separação entre dívida SFH e corporativa **não existem** nos CSVs — vivem em **nota
> explicativa** e em **release de resultados** (protocolado como IPE).
>
> E os três obtíveis são justamente os que ele **não** colocaria em primeiro lugar.
>
> A Fase 0 inteira foi desenhada em cima dos CSVs de DFP/ITR. **Isto não invalida a Fase 0
> — ela continua necessária. Mostra que ela não é suficiente**, e que existe uma segunda
> esteira (extração de documento) de ordem de grandeza diferente, que nunca foi orçada.
> Não há razão para supor que construção seja exceção: banco já era, e agora são dois.
>
> **O que a doutrina obriga:** P6 — construção não sai do universo. `empresa_sem_dado` —
> admitir com marcação. Então empresa de regime `INCORPORACAO` entra marcada, com o motivo
> escrito e **contável**. E nasce uma camada de desenho que o projeto não tinha:
> **portão** (automático, todo o universo, dado estruturado) × **dossiê** (manual, lista
> curta, notas e release). Para incorporação o portão só pode dizer *"esta empresa exige
> dossiê"* — P-64.

### Próximo passo, em ordem de valor

*Revisado em 06/09/2026 pela pesquisa de bases e APIs (`docs/fontes/pesquisa-bases-e-apis-2026-09.md`).
A fila **mudou de primeiro lugar**, e a razão está no achado V-01 abaixo.*

> **V-01 — o insumo que faltava, e ele é mais perecível que a CVM.**
> O projeto tratava a Fase 0 como "baixar DFP/ITR antes que sobrescrevam". A pesquisa
> achou três fontes que expiram mais rápido, e uma delas **decide se o backtest é
> possível**:
>
> | fonte | janela pública | o que se perde por dia |
> |---|---|---|
> | eventos societários da B3 (provento, desdobramento, grupamento) | endpoint **não documentado**, sem contrato, sem SLA | pode sumir sem aviso; não há espelho |
> | ANBIMA — IMA-B, IRF-M, ETTJ, debêntures | **5 dias úteis** | o dia; o histórico é pago |
> | carteira teórica dos índices da B3 | **só o dia corrente** | a composição daquele dia |
>
> Sem eventos societários **uma série de preços é inutilizável**: a PETR desdobrou 100:1
> em 25/04/2008 (confirmado no endpoint, em primeira mão) e o preço cai 99% num dia sem
> nada ter acontecido com a empresa. COTAHIST cru lê isso como um crash. Não havia linha
> nenhuma no plano sobre isso.

1. **Coletar o dado perecível da B3.** ⚙ **exige o desktop.** `fase0/coletar_b3.py`
   (stdlib apenas, compila e tem a lógica testada; a rede não). Captura eventos
   societários e carteira de índice em snapshot datado e imutável, com sha256 e
   manifesto. **Vem antes da CVM** porque DFP/ITR são ZIP estático em portal oficial com
   dicionário publicado — não evaporam; este endpoint pode.
2. **Fase 0 da CVM — o prazo é SEMANAL, e são 6 arquivos, não 1,5 GB.** ⚙ **exige o
   desktop.** O `NAO_CONFIRMADO` **fechou em 06/09** pela própria CVM
   (`docs/fontes/cvm-dfp-politica-atualizacao.md`, status COMPLETO):
   *"Os arquivos serão atualizados semanalmente com as eventuais reapresentações"*,
   sobre *"os últimos cinco anos"*, com *"histórico desde 2010 (incluindo arquivos não
   sujeitos à política de atualização)"*.
   O acervo se parte: **2021–2026 = 6 arquivos reescritos toda semana; o resto congelado,
   sem urgência nenhuma.** O ITR foi conferido em seguida e é **idêntico** — mesma
   política, mesma janela, e os recursos vêm rotulados por ano (2021…2026), o que
   transforma a janela de inferência em observação. Os dois carregam o mesmo carimbo
   `31/08/2026 08:01`: é **um único job semanal** do portal, então **uma** rotina cobre
   os dois. Histórico: DFP desde 2010, ITR desde **2011**. Corolário que não estava em lugar
   nenhum: **o `dfp_cia_aberta_2022.zip` de hoje não é o de 2023** — um ano de cinco
   atrás ainda está na janela de reapresentação.
3. **Segunda fonte: BCB.** **Ficou mais barata.** O IF.data **tem API OData**
   (`olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/`) — o projeto supunha
   download por navegador. P-14 continua resolvida como "construir"; o custo caiu.
4. **P-05 (taxa de ETF) — a pendência estava mal formulada.** Não é um número ausente,
   é um **campo errado**: nas lâminas do Itaú "taxa de administração" é só um componente
   (há gestão, custódia, estruturação), enquanto a BlackRock publica número único.
   Comparar rotas por `taxa_adm` subestima o custo de um lado. `custos.yaml` precisa de
   `taxa_total_aa` + `composicao` + `fonte_url` + `data_doc`.
5. Reconciliar C-04/C-05 com `auditoria/escopo-campos-de-analise.md` — ⚙ **exige o
   desktop**. E a decisão *nível ou tendência* (P-16).

**Concluídos em 05/09:** hipóteses nulas H1/H3 (H2 sem dado); pendência 20 (regime de
instituição financeira); **regime do bloco C**; LCI/LCA e FII como rotas de catálogo;
`bloqueia` deixou de ser prosa (F-05); MAPA-CONSTANTES e as 6 citações fechadas;
**ordem dos portões como dado (P-07/I-01)**; **`isento_ir` virou dois campos (P-13)**;
estado `REGRA_DECIDIDA` (G-01); F-03 medida e **refutada** (IMAB11 perde do Tesouro).

**Concluídos em 06/09:** P-24, P-15, P-36, P-37, P-38, P-39, P-40; achados O-01, Q-01,
Q-02, R-01, S-01, S-02, T-01, **U-01**; e a pesquisa de bases e APIs (**V-01**).

## 8. Números que envelhecem

Não os repita de memória — leia do YAML.

- `custos.yaml → macro.*` tem campo `expira`. `motor.val()` avisa em stderr
  quando passa da data. Em 05/09/2026 `cdi_aa` e `selic_aa` foram reconferidos na
  API do BCB e **os dois valores estavam certos** — era prazo vencido, não número
  errado. É assim que o mecanismo deve funcionar: ele manda reconferir, não
  presume erro. Próximo a vencer: `poupanca_am`, em 28/09/2026.
- **Procedência de trecho.** Toda constante cuja fonte cita documento e artigo
  carrega `trecho_conferido`. Constante nova com `false` faz o suite falhar
  (`test_nenhuma_constante_fica_com_trecho_nao_conferido`). Em 05/09 as seis que
  estavam abertas foram fechadas — cinco transcritas, uma **corrigida**: `ir_fii`
  citava a IN 1.585 art. 56, e a base real é a Lei 8.668/1993 art. 18.
- Ranking de corretoras: Itaú vence em 10 de 11 configurações de peso. A
  exceção **não é bug** — apareceu quando a dimensão de reclamações entrou, e
  está reportada em vez de escondida.
- Prêmio de ações brasileiro 2001–2026: **0,96% a.a., t = 0,74**. Não
  distinguível de zero. A fração em renda variável é aposta declarada com preço
  medido, não um dado.

---


---

## 9. O protocolo de mudança — leia antes de editar qualquer coisa

Isto substitui "eu me viro": é o método que a semana produziu, e ele existe porque
**cada passo aqui pegou pelo menos um defeito real** que o passo anterior deixou passar.

| # | passo | pegou |
|---|---|---|
| 1 | `python impacto.py <alvo>` — o que alcança o que você vai mexer | o N-01 quase passou por falta disto |
| 2 | ler os **pontos cegos** do relatório | chave dinâmica não aparece no mapa |
| 3 | mudança de contrato? **instantâneo dourado antes** | garantiu P-36 (39 registros) e P-37 (38 cenários) |
| 4 | editar |  |
| 5 | `python -m pytest` — o júri, nunca o guia | |
| 6 | `ruff check . && mypy .` — ambos em zero | T-01 |
| 7 | comparar o instantâneo — **campo a campo, não só os números** | |
| 8 | registrar em `PENDENCIAS.md` e, se for achado, em `ACHADOS.md` | |
| 9 | subir a versão do `politica.yaml` + changelog | |

**O passo 3 não é opcional em refatoração.** Refatorar sem rede é reescrever e torcer,
e as duas maiores mudanças da semana só foram defensáveis porque a rede existia.

---

## 10. Onde a história ficou

Os achados (`F-01` … `W-01`), com medição e teste, estão em **`ACHADOS.md`**.
Não estão aqui de propósito: misturar instrução com história custava ~10 mil tokens
por sessão em narrativa que a tarefa do dia normalmente não precisa.

**Leia os achados da área que você vai tocar, antes de tocar.** Vários são reincidência
do mesmo padrão, e reconhecer o padrão vale mais que decorar os casos.

---

## 11. Como trabalhar — método, ferramenta e ritmo (revisto em 06/09/2026)

O Osvaldo pediu para revisitar como o projeto está sendo construído. Esta seção é a
resposta, e ela começa pelo que dói.

### 11.1 O achado que vale mais que os outros — a alavanca errada, de novo

**Nas últimas sete rodadas de trabalho, sete foram de qualidade de engenharia. Nenhuma
foi do propósito do projeto.** P-24, P-15, P-36, P-37, P-38, P-39, P-40, mais S-01/S-02.
Tudo isso era real — o S-02 invalidava silenciosamente qualquer teste que alterasse um
custo. Mas **eu propus todas elas**, uma no fim de cada resposta, e é assim que se
chega aqui.

Enquanto isso: a **Fase 0 não começou** e tem prazo (a CVM sobrescreve os arquivos
anuais e `DT_RECEB` não se reconstrói), e o sistema ainda **não pode nomear uma
empresa** — bloqueado na decisão A05, que precisa do backtest da Fase 0.

> **Correção de 06/09, e ela é dele (achado U-01).** Eu tinha escrito aqui que "o
> aporte realizado é zero" e "a reserva é zero" como se fossem bloqueios de
> desenvolvimento. **Não são.** Ele apontou: *"imagina que fosse uma ferramenta para
> ser vendida — eu não teria informações sobre o aporte e a reserva do cliente porque
> ele não existiria."*
>
> Está certo, e o sistema já se comporta assim: `test_usuario_novo.py` mede que alguém
> com patrimônio zero e nada assinado recebe resposta completa e acionável. **O
> defeito era do roteiro, não do motor** — e é a L-01 num nível acima: a configuração
> separou motor de usuário, o plano nunca separou.

Isto é o achado M-01 aplicado a nós mesmos:

> M-01 mediu que trocar o **destino** do aporte move 3 meses e trocar o **valor** move
> 33 — e que o sistema inteiro trabalhava na alavanca de 3.
>
> **A alavanca da engenharia move 0.** Nenhum teste, nenhuma refatoração e nenhum lint
> aproxima a reserva de existir. O motor está pronto para uma carteira que não existe.

**Regra nova, e ela é permanente:** ao terminar uma sessão, o próximo passo proposto
**não pode ser de engenharia duas vezes seguidas**. Se o anterior foi, o próximo é de
produto ou de dado — ou é uma pergunta ao Osvaldo. Engenharia entra quando ela
**destrava** algo, não quando ela é o que sobrou de mais fácil de fazer.

### 11.2 Duas ferramentas, e elas não são substitutas

O plano Pro inclui **Claude Code no terminal**, com **limite compartilhado** com o app —
é a mesma cota, gasta de forma diferente. A divisão que faz sentido aqui:

| | **Claude Code** (terminal, na pasta) | **Cowork** (aqui, container na nuvem) |
|---|---|---|
| refatoração, testes, lint | **sim** — sem ritual de zip | não |
| git: commit, branch, push | **sim**, direto | não alcança |
| **baixar dado em massa** | **sim** | **não — ver a correção abaixo** |
| pesquisa com fonte primária, subagentes | não | **sim** |
| processar dado pesado que ele já baixou | não | **sim** — o container tem disco |
| trabalhar com o computador desligado | não | **sim** |

> **Correção de 06/09/2026, e ela desmente o que esta seção dizia antes.** Estava escrito
> aqui que baixar CVM/B3 era papel do container, "porque ele tem rede e disco". **Está
> errado, duas vezes:**
>
> 1. `dados.cvm.gov.br` responde `ROBOTS_DISALLOWED` às minhas ferramentas de busca. Já
>    aconteceu em duas sessões, com dois agentes diferentes. **E eu não contorno** — é
>    regra de operação minha, e burlá-la num projeto cuja doutrina inteira é procedência
>    seria a contradição mais cara possível.
> 2. Mesmo para domínios que respondem (a B3 responde), **eu não roteirizo download em
>    massa daqui.** A ferramenta de busca é para ler página, não para ser um `wget` com
>    outro nome.
>
> **Consequência:** a máquina de download é a dele, sempre. O container é máquina de
> **pesquisa** e de **processamento do que ele já baixou**. Foi por isso que
> `coletar_b3.py` saiu daqui como script para rodar lá, e não como dado coletado — e é
> por isso que os dois dias até terça são perda real, não evitável.

**O ritual do zip é puro desperdício, e ele existe só porque o computador fica
desligado.** Empacotar, conferir, enviar, extrair, reconferir — toda sessão. No Claude
Code isso não existe: o arquivo é editado onde ele mora.

**Consequência prática:** a partir de terça, refatoração e teste vão para o Claude Code.
Este ambiente fica para pesquisa e para processar o dado bruto depois que ele existir.

### 11.3 Subagentes — usados de verdade em 06/09, e o resultado justifica

Deixou de ser proposta. A pesquisa de bases e APIs rodou com **quatro subagentes em
paralelo** — armazenamento ponto-no-tempo, BCB, CVM/B3/Tesouro/ANBIMA, e taxas de ETF —
cada um devolvendo **só a conclusão**.

Custou ~329 mil tokens **no contexto deles**, 186 chamadas de ferramenta, ~5 min de
relógio. No meu contexto entraram quatro blocos de conclusão. Sequencialmente, o texto
das páginas teria entrado inteiro e a sessão não caberia.

**A regra que sai disso:** trabalho de leitura larga (catálogo, layout, documentação de
API, comparação de ferramenta) vai para subagente. Trabalho que decide o projeto fica
aqui. E o subagente herda a doutrina: **o prompt dele carrega a proibição de inventar
URL, número e versão, e a ordem de marcar `NAO_CONFIRMADO`** — sem isso ele devolve
plausibilidade, que é pior que ausência, porque passa.

**O que a prática mostrou e a teoria não previa:** dois dos quatro voltaram com o mesmo
bloqueio (`ROBOTS_DISALLOWED` na CVM) e **os dois o respeitaram**. Conclusão que só vale
porque nenhum contornou: a CVM não é alcançável de nenhum agente na nuvem, e a pergunta
que ela responde tem que sair do desktop ou do celular.

### 11.4 O que se lê toda sessão — cortado pela metade em 06/09

| | antes | depois |
|---|---|---|
| `CLAUDE.md` | 1.112 linhas | **482** |
| `PENDENCIAS.md` | 911 linhas | **565** |
| `ACHADOS.md` | — | 1.066 (lido **só** quando a tarefa toca a área) |
| **total por sessão** | **~26 mil tokens** | **~13 mil** |

Nada foi apagado. O que mudou é **quando** se paga: instrução toda sessão, história sob
demanda. Os dois arquivos estavam fazendo dois trabalhos incompatíveis ao mesmo tempo.

### 11.5 Onde os tokens vão embora, medido

Fora a leitura inicial, os três maiores gastos desta semana, em ordem:

1. **Respostas longas minhas.** São o maior item isolado. Parte é o que ele pediu
   (análise profunda, nunca superficial) e parte é excesso meu — repetir na resposta o
   que já está no arquivo que acabei de escrever.
2. **Rodar a suíte inteira depois de cada passo.** 269 testes, ~8 s. Barato em tempo,
   caro em token quando a saída volta inteira. `pytest -q | tail -3` resolve, e eu já
   faço isso — mas nem sempre.
3. **Reler arquivo que acabei de escrever.** Desnecessário: a ferramenta de edição
   falha se a edição não colou.

### 11.6 Onde a automação vai morar — decidido em 06/09/2026

A pergunta foi dele: *"subir o projeto para um servidor não resolveria isso? tipo
supabase?"* A resposta é **não para o Supabase, sim para a ideia**.

| | serve? | por quê |
|---|---|---|
| **GitHub Actions, repo privado** | **sim** | cron nativo · 14 GB de disco efêmero · 6 h/job · 2.000 min/mês · sem pausa por inatividade |
| Supabase Free | **não** como executor | **pausa após 1 semana de inatividade**, e a rotina é semanal — fica em cima do limiar. Edge Function: 150 s, 256 MB, upload de 50 MB |
| Vercel Hobby (ele tem conta) | não | cron 1×/dia, função de 300 s, sem disco |
| Cloudflare Workers | não | 10 ms de CPU por cron |
| Cloudflare R2 | **sim**, como depósito | 10 GB grátis, egress zero — se um dia for preciso guardar ZIP bruto |

**Duas inversões que valem mais que a tabela:**

1. ~~Repositório privado é mais confiável.~~ **DECIDIDO EM 06/09: o repositório é
   PÚBLICO** — escolha dele, e ela é melhor. Público tem Actions sem consumo de cota e
   runner maior (4 vCPU/16 GB contra 2/8). A regra dos 60 dias de auto-desativação **não
   morde**, porque o próprio workflow commita o delta toda semana e commit é atividade.
   **O pré-requisito é duro e não é negociável:** `alocacao/estado.yaml` **não entra no
   repositório**. A U-01 já provou que não precisa — `test_usuario_novo.py` mede o sistema
   funcionando com estado vazio, e `estado.exemplo.yaml` ocupa o lugar. `perfil.yaml`
   **entra**, por decisão explícita dele. Nada foi empurrado ainda, então não há histórico
   para reescrever: a janela limpa é agora.
2. **Não é preciso guardar snapshot semanal.** A reapresentação é uma fração mínima do
   arquivo; o que o backtest precisa é o **histórico de mudanças**, não o arquivo. Baixar,
   comparar, guardar o delta, descartar o resto: de dezenas de GB/ano para poucas centenas
   de MB — e **o próprio git vira o armazenamento**.

**A armadilha a carregar para o desenho, e é o F-02 outra vez:** um download que devolve
404 mais um unzip vazio produzem *"nenhuma mudança"*, indistinguível de *"a CVM não mudou
nada"*. **Ausência de mudança precisa ser afirmada, nunca inferida da ausência de erro.**

**O que NÃO é desperdício, e não deve ser cortado:** o instantâneo dourado. Ele custou
caro em duas ocasiões e foi o que permitiu afirmar "zero desvio" em vez de "acho que
está tudo bem". Medir antes de mexer é o método, não o excesso.

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

> **11/09/2026 — Python 3.11.9 instalado, e o `ambiente.py` disse, pela primeira vez:**
> `python: requer ==3.11.* · rodando 3.11.9`. Desde que o P-15 foi escrito, nenhuma
> máquina havia rodado o interpretador declarado.
>
> **Como instalar as dependências — e NÃO é `pip install -e .`:**
>
> ```powershell
> py -3.11 -m pip install "PyYAML==6.0.3" "numpy==2.4.4" "pandas==3.0.2" "pytest==9.1.1" ruff mypy types-PyYAML
> ```
>
> É o comando que o próprio `ambiente.py --instalar` imprime. Use-o.
>
> **B-04 — `pip install -e .` NÃO funciona, e o motivo é o padrão da casa outra vez.**
> O `pyproject.toml` declara `[build-system]` com setuptools, e o build **falha**:
> *"Multiple top-level packages discovered in a flat-layout: ['data', 'fase0',
> 'alocacao', 'auditoria']"*. Nunca houve declaração de `packages`, porque **este projeto
> nunca foi um pacote instalável** — é um conjunto de scripts, e o `pyproject.toml` existe
> para **declarar versões**, não para construir distribuição.
>
> O arquivo promete um build que não existe. É inofensivo hoje, e é exatamente a forma de
> defeito que o projeto persegue: **declaração sem execução.** Ou o `[build-system]` sai,
> ou ganha `[tool.setuptools] packages = []` e passa a ser verdade. Pendência, não urgência.

**Na máquina do Osvaldo, até 11/09/2026: Python 3.13, e o `pyproject.toml` exige
`==3.11.*`.** Não é detalhe de instalação — é o P-15 funcionando: a faixa foi fechada de
propósito (3.12 mudou comparação de `datetime.date`, e o projeto compara `expira` em quase
todo `val()`). Ou instala-se o 3.11, ou a faixa é reaberta **com medição**, nunca por
conveniência. Enquanto isso, um resultado produzido no 3.13 é número novo, não conferência
de um antigo.

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

### Teste em toda etapa — sem exceção

Regra dele, 11/09/2026: *"nunca deixar de implementar testes unitários em todas as etapas."*

Ela não é redundante com o "um achado, um teste": aquela é **reativa** (achou defeito,
escreve teste), esta é **preventiva** (escreveu código, escreve teste). O `coletar_b3.py`
mostrou a diferença da pior forma — foi entregue em 06/09 com *"compila e a lógica foi
testada"*, e na primeira corrida real quebrou **três vezes seguidas**, em A-00, A-01 e
A-02.

**Os três eram função pura. Nenhum precisava de rede.** O que faltou não foi teste de
integração: foi teste de `empresa_de` e de `normalizar` — as duas funções onde morava
todo o risco, e as duas que ficaram sem.

**Consequência operacional:** arquivo novo em `fase0/` ou em `alocacao/` nasce com
`test_<nome>.py` ao lado. Script utilitário também — foi um script utilitário que trouxe
dado do ativo errado com HTTP 200.

### Escalável, auditável, manutenível — nesta ordem de conferência

Regra dele, 11/09/2026. Não é slogan; são três perguntas com resposta verificável, e o
projeto já tem a ferramenta de cada uma:

| | a pergunta | onde já se responde |
|---|---|---|
| **escalável** | funciona com 400 empresas, não só com 76? com dois usuários? | P-41/P-42 mediram; `catalogo.yaml` é quadrático **por desenho declarado** |
| **auditável** | de onde veio este número, e o que muda se a escolha for outra? | P1, `impacto.py`, o acervo em bruto com sha256 |
| **manutenível** | a próxima sessão entende sem reler tudo? o teste pega a volta? | `CLAUDE.md`, `ACHADOS.md`, um teste por achado |

**O que isto proíbe na prática:** script de uma vez só que ninguém consegue rodar de
novo; número no código em vez de no YAML; e correção sem teste — as três coisas que
fazem o projeto parecer pronto e não ser.

### Achado retirado fica como retratação — nunca some

**Decisão dele, 12/09/2026**, tomada sobre o E-05: quando um achado é derrubado, ele
**permanece escrito**, marcado como retirado, com o motivo e a causa raiz do erro.
Não se apaga.

**Por quê, e a razão é medível:** o valor de um achado derrubado não está no achado —
está em **como ele passou**. O E-05 sobreviveu a uma auditoria inteira, entrou neste
arquivo, entrou na fila de segunda e entrou numa resposta com tabela e recomendação. O
que o matou foi o Osvaldo responder *"portão"* e eu ir escrever o código que já existia.
Apagar o E-05 apagaria junto a única coisa que ele ensinou: **auditar um projeto que põe
regra em YAML varrendo só o Python é medir metade do sistema e chamar de conclusão.**

Um arquivo que só guarda os acertos descreve um projeto que nunca errou, e esse projeto
não existe. Pior: ele volta a cometer o mesmo erro, porque não há onde ler que já o
cometeu.

**O custo é real e aceito.** Este arquivo passa de 1.300 linhas e cresce a cada
retratação. A troca está declarada: **tamanho em troca de não repetir**. Se um dia o
custo virar impeditivo, a saída é mover o histórico para um arquivo de achados — não
deletá-lo.

**Como se escreve uma retratação, e a forma importa:**

1. o achado original **citado**, não parafraseado — o leitor tem de ver o que foi dito;
2. a **evidência** que o derruba, medida e não argumentada;
3. a **causa raiz do erro de método**, que é a parte que vale;
4. o que foi **corrigido na ferramenta ou no processo** para que a classe não repita.

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

## 5-B. A régua da medição — onze erros meus em uma semana, e a forma que eles têm

*Escrita em 13/09/2026, a pedido dele: **régua de método, não lista de incidentes.***

Entre 11 e 13/09 eu errei onze vezes. Publiquei dois dos erros e retirei os dois. A
lista dos nove está nas retratações espalhadas por este arquivo; o que vale é que
**eles têm uma forma só**, e a forma tem conserto.

### A forma

> **Em todos os onze, a medição estava certa. Errada era a pergunta que eu achei que
> ela tinha respondido.**

O instrumento respondeu exatamente o que sabia responder — e eu li a resposta como se
ela cobrisse uma pergunta maior. Não é falta de rigor na medição: **é excesso de
confiança no alcance dela.**

| o que eu media | o que eu concluía | a distância |
|---|---|---|
| `r.desembrulhar is c.desembrulhar` | "não há duplicata" | identidade da referência ≠ uso pelo coletor (**A-06**) |
| chaves lidas nos `.py` | "ninguém lê esta chave" | o `catalogo.yaml` lia por `{de_campo:}` (**E-05**) |
| leituras por índice **literal** | "campo órfão" | o código lia por índice **variável** (`ajuste_estabilidade`) |
| leituras fora do módulo de definição | "campo morto" | o consumidor morava no próprio módulo (**P-78**) |
| a string `[build-system]` no arquivo | "patch não aplicado" | a nota inserida continha a string (**B-04**) |
| art. 14, I, "b" da LC 224 | "vigora em 01/04/2026" | a alínea cobria **outros artigos** (**JCP**) |
| 0,25% > 0,20% | "F-03 refutada" | o insumo não existia no `custos.yaml` (**P-76**) |
| `(08/03 − 01/01).days` | "67 dias" | 2016 é bissexto, e o intervalo é inclusivo — **68** |
| — | "o catálogo duplica o literal" | eu não tinha aberto o `catalogo.yaml` (**E-08**) |
| `C['etf']['IMAB11']` carregado | "a taxa nunca entrou no arquivo" | entrou — uma **chave duplicada** a apagava (**E-09**) |
| chaves duplicadas nos `.py`… digo, nos YAML | "`catalogo.yaml` é ilegível" | ele usa **merge** (`<<:`), e meu loader não construía a tag |

### A régua — cinco perguntas antes de promover uma medição a achado

**1. Escreva em uma frase o que a medição mediu.** Se essa frase for mais estreita que
a sua conclusão, pare. Não reescreva a frase: **reescreva a conclusão.**

**2. Que parte do sistema ficou fora do instrumento?** Linguagens (este projeto põe
regra em YAML: varrer só `.py` é medir metade), caminhos de leitura não-literais
(`d[k]` com `k` variável), módulos que o filtro excluiu, testes que você contou como
motor — ou como não-motor.

**3. Abra os arquivos em volta antes de escrever.** Quatro dos onze morreram na primeira
leitura de vizinhança, e um deles tinha **um comentário em português, uma convenção e
dois testes** dizendo exatamente o que eu ia "descobrir". *Medir levanta o candidato;
quem o promove a achado é a leitura.*

**4. A guarda falha quando deveria?** Guarda que nunca falhou é guarda que ninguém sabe
se funciona. Os três modos de provar, e cada um pegou um erro diferente:
- **mutação** — reintroduza o defeito e veja a guarda reprovar;
- **duas execuções** — a única forma de testar idempotência;
- **adiantar o relógio** — `motor.HOJE = 2027-01-01` provou que o aviso de `expira`
  passou a sair.

**5. Numa fonte, a cláusula que você citou cobre o item de que você está falando?**
*"Fonte primária ganha"* não é passe livre. Ela ganha **depois** de se verificar qual
dispositivo a cláusula alcança. Usei a autoridade de uma fonte primária para descartar
uma secundária **correta** — pior do que não ter consultado nenhuma das duas, porque
veio com confiança.

### O que a régua NÃO diz

Não diz "meça menos". Os onze erros não vieram de medir demais — vieram de **concluir
antes de ler**. Os achados que sobreviveram à semana (**E-01**, **E-03**, **P-77**,
**E-08**, a série do JCP) foram todos confirmados com as cinco perguntas acima, e
quatro deles nasceram exatamente das mesmas ferramentas que produziram os falsos
positivos.

E não diz "desconfie de ferramenta". Diz **declare o alcance dela**: o
`chaves_orfas.py` imprime, antes de qualquer resultado, quantas leituras cegas existem
e quantos nomes vêm de YAML — é a P5 aplicada ao próprio instrumento. **Ferramenta que
anuncia o próprio limite é ferramenta; ferramenta que só imprime achados é opinião com
sotaque de máquina.**

### A regra de uma linha, para quando não der tempo de ler as cinco

> **Medir → ler a vizinhança → concluir.** O passo do meio é o que eu pulava.

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
**A data vale** — o M-01 a calculou com reserva inicial ZERO, e a reserva **é** zero
(U-02, abaixo). Cheguei a declará-la inválida em 12/09 e estava errado.

> **10/09/2026 — o aporte deixou de ser zero.** Primeiro depósito de **R$500**, no cofrinho
> do PicPay. A P-02 sai de `DADO_DE_UM_USUARIO` pendente e passa a ter valor — e o M-01 diz
> que esta é a alavanca de **33 meses**, não a de 3.
>
> **U-02 — eu transformei o dinheiro dele em reserva, e ele já tinha decidido que não
> era. Correção dele, 12/09/2026.**
>
> Escrevi, vinte linhas acima do lugar onde este mesmo arquivo diz o contrário:
>
> ```
> reserva_atual       8.181,71
> reserva_disponivel  4.702,12   (4.202,12 + 500,00)
> reserva_empenhada   3.479,59
> ```
>
> **Está errado em duas contas, e as duas na mesma direção — a que faz o projeto parecer
> mais adiantado do que está.**
>
> 1. **Os R$500 são o aporte mensal prometido, não reserva.** Foram para um cofrinho
>    diferente, e são a P-02 saindo de zero. Contá-los como reserva **conta o mesmo
>    dinheiro duas vezes**: ele é a alavanca de 33 meses do M-01 *e*, na minha conta,
>    parte do alvo que essa alavanca existe para construir.
> 2. **O Cofrinho do Cartão não é reserva, e isso já estava decidido.** Este arquivo
>    diz, na seção seguinte: *"o número existia — errado era chamá-lo de reserva."* Eu
>    escrevi a frase certa e depois escrevi a tabela errada. **A reserva é ZERO.**
>
> **A consequência concreta, e ela ia para a fila de segunda:** eu declarei inválido o
> ~mai/2031 do M-01 *"porque a reserva não é zero"*. A reserva **é** zero, então o
> número do M-01 **vale** — e ele ia gastar a segunda recalculando uma data que estava
> certa, a partir de um `estado.yaml` com três números errados.
>
> **E o pior é o terceiro erro, que é de doutrina.** A U-01 é dele: *"imagina que fosse
> uma ferramenta para ser vendida — eu não teria informações sobre o aporte e a reserva
> do cliente"*. No mesmo dia em que reescrevi a U-01 neste arquivo, ancorei um achado da
> auditoria (o E-05, que ainda por cima era falso) em **quanto dinheiro ele tem e onde**
> — dando a um defeito de desenho um peso emprestado de um dado de usuário. **Achado de
> desenho que precisa do saldo de alguém para parecer grave não é achado de desenho.**
>
> **O que vale como regra daqui:** número que descreve o dinheiro dele entra em
> `estado.yaml` e em lugar nenhum mais — nem como ilustração, nem como argumento. E a
> classificação (o que é reserva, o que é aporte, o que é caução) é **decisão declarada
> dele**, não leitura minha do extrato.

> **P-68 FECHADA em 12/09** — no que ela de fato mediu: do Cofrinho do Cartão
> (R$7.681,71), **R$4.202,12 estão disponíveis para retirada**, logo o limite
> comprometido é **R$3.479,59**; e **dá para desligar** o limite sobre o Turbinado.
> Isso responde *"quanto sai"*, que era a pergunta. **Não responde "quanto é reserva"** —
> e a resposta dessa, dele, é **zero**: o saldo do cartão não é reserva por decisão
> declarada, e os R$500 são aporte.
>
> E caiu uma hipótese: como o limite pode ser desligado, **taxa alta e caução não são o
> mesmo produto** no PicPay. Dá para ter 121% sem dar o dinheiro em garantia —
> `OBSERVADO`.

> **O quadro completo apareceu em 10/09** (`docs/fontes/picpay-cofrinhos-2026-09-10.md`):
> total guardado **R$ 8.181,71** — R$500 no Turbinado (121%) e **R$7.681,71 no Cofrinho do
> Cartão (120%)** —, e **os dois etiquetados `LIMITE DO CARTÃO`** pelo próprio app.
>
> **O M-01 estava certo pelo motivo certo.** Ele dizia que "~mar/2030" fora calculado com
> R$7.671 de reserva e que isso estava errado *"porque a reserva é zero"*. O saldo é
> R$7.681,71: **o número existia — errado era chamá-lo de reserva.**
>
> **E era aí que estava a armadilha, que eu caí dentro em 12/09.** Eu li a P-68 como
> *"descubra quanto da reserva está livre"*. A pergunta certa nunca foi essa: quanto sai
> do cofrinho é uma medida de **liquidez do produto**, não uma medida de **reserva**.
> Saber que R$4.202,12 saem não torna esse dinheiro reserva — a classificação é decisão
> dele, e a decisão já estava tomada: **não é**. Ver U-02.
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

*Tabela revista em 13/09/2026 — a camada 0 deixou de ser "não iniciada".*

| camada | estado |
|---|---|
| 0 · pipeline de dados | **em andamento.** B3: acervo de eventos completo (74 emissoras, ~8 mil proventos, `dt_captura=2026-09-11`) e o primeiro **silver** escrito (`refinar.py`, 41 testes). CVM: política **confirmada na fonte**, download **manual pendente** (robots). COTAHIST: **não localizado**. Bitemporalidade: desenhada, não implementada |
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

> **Y-01 — chave YAML duplicada é sobrescrita em silêncio. 10/09/2026.**
>
> `custos.yaml` tem **duas** entradas `etf.IMAB11` (linhas 171 e 253). O PyYAML **não
> reclama**: fica com a última. O que o motor lê hoje é `valor: null,
> status: NAO_CONFIRMADO` — a entrada de 05/09, com valor 0,25%, fonte e data de acesso,
> **está morta desde que foi escrita**.
>
> É o F-02 numa camada nova: lá insumo ausente virava zero; aqui **insumo presente é
> sobrescrito por um ausente**. O erro é na direção conservadora (a rota fica bloqueada),
> o que é sorte, não desenho.
>
> **Pergunta aberta:** o registro diz "F-03 medida e refutada (IMAB11 perde do Tesouro)".
> Se o motor lê `None`, **com que número essa medição foi feita?** Responder antes de
> apagar qualquer das duas entradas.
>
> **O teste que falta não é sobre IMAB11** — é uma varredura do YAML cru procurando chave
> repetida em qualquer mapping. Um teste do IMAB11 seria patch.

> **A-01 e A-02 — 11/09/2026, a primeira corrida real da Fase 0, e ela rendeu dois
> achados que nenhuma leitura teria dado.**
>
> **A-01 — `B3SA3` virou `BSA`, e a B3 respondeu 200.** O coletor derivava a emissora
> filtrando dígitos do ticker. Funciona em 73 dos 74 ativos do Ibovespa e erra em
> **B3SA3**, cujo código de emissora é `B3SA` — tem dígito no meio. O endpoint **casou
> com outra empresa** e devolveu capital social de R$9,61 bi datado de 1981.
>
> Este é o modo de falha mais caro do projeto inteiro: **não é ausência de dado, é dado
> do ativo errado, com aparência perfeita.** Nenhum teste de "veio resposta?" o pega. A
> regra certa é posicional — ticker da B3 é 4 caracteres de emissora + dígitos —, e o
> coletor agora imprime o nome da empresa em cada linha, para que a divergência seja
> visível a olho.
>
> **A-02 — eu registrei o formato do endpoint errado.** `docs/fontes/pesquisa-bases-e-apis-2026-09.md`
> diz que `GetListedSupplementCompany` devolve um **objeto**. Devolve uma **lista**. As 74
> emissoras vieram como lista, sem exceção. A leitura original passou por uma ferramenta
> de resumo, que desembrulhou a lista de um elemento **sem avisar**, e eu transcrevi a
> conclusão dela como se fosse o dado.
>
> É a mesma classe do F-05/N-01 com um intermediário novo: **um resumo não é uma
> observação.** Quando a fonte é máquina, o que vale é o byte que ela devolve, e a única
> prova é o arquivo bruto gravado no acervo.
>
> **O acerto de desenho, e vale registrar porque foi barato:** a guarda escrita em 10/09
> — *"resposta estranha é evidência, não lixo: grave o bruto e acuse no fim"* — fez o
> coletor sobreviver às 74 e trazer a forma real de volta, em vez de morrer na primeira.
> A versão anterior perdia 75 ativos por causa de um.

> **A-03 — o código da emissora muda, e a história não vem junto. 11/09/2026.**
>
> `MBRF` voltou com `tradingName: MARFRIG`, `codeCVM: 20788`, e **as três listas de
> eventos vazias**. Não é falha de rede nem chave errada: o código mudou (`MRFG` → `MBRF`,
> na fusão com a BRF) e o histórico **ficou sob o código antigo**.
>
> Zero numa lista é comum e legítimo — há empresa que nunca desdobrou. **Zero nas três,
> numa empresa do Ibovespa, é quase sempre troca de código.** Das 74 emissoras, só a MBRF
> caiu nesse caso, o que torna a guarda barata e precisa.
>
> É a confirmação concreta do que a pesquisa de 06/09 tinha previsto em abstrato: **o
> mapeamento ticker ↔ CNPJ ↔ CD_CVM também precisa ser bitemporal**, senão o join vaza
> futuro. Aqui ele não vaza futuro — ele **apaga passado**, que é o outro lado da mesma
> moeda. Série de preços sem ajuste de proventos é série inútil.
>
> Note o que salvou: `codeCVM` vem no mesmo objeto. **O CNPJ/CD_CVM é estável quando o
> ticker não é** — é por ele que a ponte para o código antigo se faz.

> **11/09/2026 — cinco rodadas no Claude Code, e o saldo real.**
>
> Fechadas e commitadas: **P-69/Y-01** (`258ca3b`), **P-70** (`9e1aa8a` + `e15d205`),
> **P-71/P-72** (`4f54f31` + `c989ac6`), **campos mortos** (`fb8ce78`), e a esteira
> `--proventos-completos` escrita com testes sem rede.
>
> **A pergunta do Y-01 foi respondida:** a F-03 foi medida **à mão, com 0,25%, fora do
> motor** — está em `politica.yaml → fora_de_escopo.ETF_renda_fixa`. O valor nunca passou
> por `val()`, então a duplicata não a contaminou. Mas abriu a **P-76**: a conclusão foi
> registrada como *"refutada"* e o insumo que a sustenta é `PARCIAL`. Se 0,25% for o
> **teto** do regulamento, a taxa efetiva pode ficar abaixo de 0,20% e **a comparação
> inverte**. *Uma conclusão medida herda o status do insumo mais fraco dela?* — é a P1
> aplicada ao relato de uma medição, e ainda não tem resposta.
>
> **O achado de maior valor não estava em nenhum prompt: P-77.** `retorno_liquido_aa` faz
> `ir = 0.0 if r.isento_ir else ...`, e `isento_ir` resolve por `isento_ir_rendimento` —
> então, para o FII, **o IR de ganho de capital vira zero**. É exatamente o defeito que a
> P-13 foi criada para corrigir, vivo, no código. Hoje não produz número errado **só
> porque o FII está bloqueado por falta de insumo** — o bloqueio está *escondendo* o bug.
> É o F-02 ao contrário: lá a ausência virava zero; aqui a ausência **esconde** um zero
> que já está errado.
>
> **O portão da P-40, instalado em 11/09:** `ruff check .` → **All checks passed**.
> `mypy` **não rodou**: parou nos stubs do numpy com *"Type statement is only supported in
> Python 3.12 and greater"*.
>
> **Isso não é dívida de código — é a P-73 pela terceira vez.** O `pyproject.toml` declara
> `python_version = "3.11"`, a máquina roda **3.13**, e o numpy instalado traz stubs com
> sintaxe de 3.12+. O mypy **nunca vai passar nessa máquina** enquanto a divergência
> existir. Instalar o Python 3.11 deixou de ser preferência de reprodutibilidade e virou
> **requisito operacional**: sem ele, metade do portão está permanentemente desligada.
>
> E nenhum commit fez o bump de versão do `politica.yaml` nem o changelog — passo 9 do
> protocolo, cinco commits seguidos.

> **B-02 — a causa do TOTAL-ZERO não era truncamento. Medida em 11/09/2026.**
>
> A esteira de proventos fechou **71 de 74** emissoras — mais de **8 mil registros**, com
> ITUB em 956, BBDC em 902, ITSA em 506 e PETR em 343. Falharam três: **ABEV, CURY,
> KLBN**, todas com `totalRecords: 0`.
>
> O código supunha **truncamento no campo de 12 posições**. Nenhuma das três estava
> truncada: `AMBEV S/A` tem 9 caracteres, `CURY S/A` tem 8, `KLABIN S/A` tem 10.
>
> **O que elas têm em comum é a barra.** Chamei o endpoint com os nomes sem o sufixo e ele
> respondeu: **`AMBEV` → 134 registros. `KLABIN` → 18.** Com `S/A`, zero. E os nomes com
> `S.A.` **de ponto** — SUZANO, RUMO, VIVARA, IGUATEMI — passaram todos.
>
> **A causa real: os dois endpoints da B3 guardam o nome comercial de formas diferentes.**
> O suplemento devolve `AMBEV S/A`; a tabela de proventos guarda `AMBEV`. Não é bug de
> codificação nosso — é divergência entre duas bases da mesma casa.
>
> **E o teste que importava mais deu a resposta tranquilizadora:** chamei com `ITAU`
> (prefixo de `ITAUUNIBANCO`) e voltou **zero**. Ou seja, **o match é exato, não por
> prefixo nem por conteúdo.** Isso fecha a dúvida que eu tinha e que valia mais que as
> três falhas: **não existe match parcial silencioso.** Ou o nome bate e vem tudo, ou não
> bate e vem zero — e zero é visível. **O acervo das 71 está íntegro**, e `ITAUUNIBANCO`,
> com exatamente 12 caracteres, é o nome real e não um nome cortado.
>
> **Corrigido e commitado (`b02b789`), 13 testes novos.** O coletor tenta o nome como veio
> e, **só depois de um zero**, sem o sufixo societário; a forma usada vai para o manifesto,
> porque **a forma é procedência, não detalhe de implementação** — quem reprocessar precisa
> saber qual nome trouxe o dado.
>
> Dois testes valem por si: um garante que a segunda tentativa **nunca acontece antes** de
> um zero (resposta fora do formato não é culpa do nome, e trocar o nome mascararia o
> defeito); outro garante que zero **nas duas formas** continua sendo `TOTAL-ZERO`, e não
> vira "empresa sem proventos". As duas respostas ficam no acervo como evidência, com a
> forma no nome do arquivo.
>
> E os comentários do código que culpavam o truncamento foram corrigidos. **Uma hipótese
> errada deixada num comentário engana a próxima sessão com a autoridade de um fato.**

> **A suíte deixou de ficar verde nesta máquina — e isso agora é o caminho crítico.**
>
> Enquanto `ruff` e `mypy` não estavam instalados, o `test_p40_lint.py` **pulava** e a
> suíte fechava verde. Instalados em 11/09, o ruff passou em `alocacao/` e em `fase0/`
> (zero), e o **mypy falha em toda rodada** — nos stubs do numpy, que exigem Python 3.12+.
>
> **Não é dívida de código. É a P-73**, e ela mudou de natureza: deixou de ser uma questão
> de reprodutibilidade de backtest e virou operacional. **Uma suíte permanentemente
> vermelha deixa de ser sinal** — em duas semanas ninguém olha mais, e o dia em que um
> teste de verdade quebrar, ele vai entrar no meio do vermelho de sempre.
>
> Instalar o Python 3.11 é o que devolve o verde. Não é preferência.
>
> *(O ruff na raiz acusa 20 erros, **14 deles em `pesquisa-custos-2026-08/calc/`** — a
> cópia congelada de agosto que o §4 marca como armadilha. Corretamente não tocada.)*

> **B-03 — não há regra única, e isso muda a estratégia. Medido em 11/09/2026.**
>
> A correção do B-02 fechou **ABEV (134)** e **KLBN (18)**, exatamente os números previstos.
> **CURY falhou nas duas formas.** Fui atrás e achei:
>
> | emissora | suplemento guarda | tabela de proventos guarda | o que aconteceu |
> |---|---|---|---|
> | ABEV | `AMBEV S/A` | `AMBEV` | sufixo **removido** |
> | KLBN | `KLABIN S/A` | `KLABIN` | sufixo **removido** |
> | **CURY** | `CURY S/A` | **`CURY S.A.`** → **20 registros** | sufixo **reescrito**: barra vira ponto |
>
> **As duas bases da B3 divergem sem regra.** Às vezes o sufixo societário some, às vezes
> ele muda de grafia. Uma normalização determinística — "tire o sufixo" — **não cobre os
> três casos**, e foi exatamente por isso que a correção do B-02, que estava certa, ainda
> deixou uma de fora.
>
> A estratégia certa não é uma regra: é uma **cascata de candidatos** — como veio, sem
> sufixo, sufixo com pontos, sufixo sem pontuação — parando no primeiro que responder, e
> **registrando qual funcionou**. O acervo precisa guardar a forma, não a regra.
>
> **O que NÃO está em risco, e vale dizer:** o match é exato (`ITAU` → 0), então as 73 que
> bateram bateram **exatamente**. Divergência de grafia produz zero, nunca dado parcial.
> **O acervo é íntegro ou visivelmente incompleto — nunca silenciosamente errado.**

> **12/09/2026 — três marcos no mesmo dia, e um deles é inédito.**
>
> **1. O ambiente reproduz o registrado.** `ambiente.py` no Python 3.11.9, com numpy
> 2.4.4, pandas 3.0.2, PyYAML 6.0.3 e pytest 9.1.1: *"O ambiente instalado E o
> registrado."* **Desde que o P-15 foi escrito em 05/09, nenhuma máquina havia rodado o
> que o projeto declara.** A impressão é `7565df1381e2c1ed`.
>
> **2. A suíte fechou verde sem nenhum `s`.** Antes havia dois skips — ruff e mypy
> ausentes. O portão da P-40 **rodou de verdade** e passou. **P-73 fechada.**
>
> **3. O acervo de eventos fechou em 74/74.** A CURY veio pela terceira forma da cascata
> (`CURY S/A` → `CURY` → **`CURY S.A.` → 20 registros**), exatamente como o B-03 previa.
>
> **A Fase 0 mudou de estado: deixou de ser coleta e virou refino.** O desenho está em
> `DESENHO-PIPELINE.md`, e o achado que o organiza é este: **cada registro de provento
> traz `closingPricePriorExDate`**, o fechamento na véspera do ex. **A série de fatores
> de ajuste pode ser construída inteira sem tocar no COTAHIST** — o preço só entra depois,
> para aplicar. As duas metades do problema se separam, e a metade difícil já está no disco.

> **C-01 — eu errei um número e ele se propagou por três arquivos. 12/09/2026.**
>
> Escrevi, aqui e em dois documentos de fonte, que a PETR *"desdobrou 100:1"* e que *"o
> preço cai 99% num dia"*. O registro traz `factor: "100,00000000000"` com
> `label: DESDOBRAMENTO`.
>
> **`factor` quase certamente é percentual, não multiplicador.** Um desdobramento de 100%
> faz cada ação virar duas e o preço cair **pela metade** — não 99%.
>
> ```
> leitura percentual     fator = 1/(1 + 100/100) = 0,5
> leitura multiplicador  fator = 1/100           = 0,01
> ```
>
> **As duas produzem número, e diferem por cinquenta vezes.** Nenhum teste de "veio
> número?" distingue. Não há documentação da B3 sobre o campo, e o suplemento não traz
> preço de véspera para desempatar.
>
> **`refinar.py` não escolhe.** Grava `ratio` cru e devolve `FACTOR_AMBIGUO`. A
> desambiguação é **medição**: com o COTAHIST, a razão entre o fechamento de 24/04/2008 e
> o de 25/04/2008 responde em uma consulta.
>
> **O que me incomoda mais que o erro:** ele durou seis dias e apareceu em três arquivos
> porque era uma afirmação *plausível* que ninguém precisava medir para repetir. O projeto
> tem doutrina contra número sem procedência **em YAML**; não tinha nada contra número sem
> procedência **em prosa**. Agora tem: achado só entra no `CLAUDE.md` com a conta escrita
> ou com o `NAO_CONFIRMADO` explícito.

> **D-01 — a guarda do segredo mede o arquivo, e o dado sai pela prosa. 12/09/2026.**
>
> A P-62 decidiu que `estado.yaml` não entra no repositório, e o `test_p67_segredo.py`
> garante isso medindo o **índice do git**. Funciona.
>
> **Só que eu escrevi os mesmos números na prosa deste arquivo e do `PENDENCIAS.md`** —
> saldo dos cofrinhos, aporte, reserva — e esses dois **entram**. O repositório é público
> desde 11/09.
>
> É o padrão do projeto contra ele mesmo: um guarda que checa nome de arquivo não vê
> conteúdo, e quem escreveu o guarda escreveu o vazamento na mesma semana.
>
> **Decisão dele, 12/09: `DECISAO_DO_USUARIO` — pode ficar.** *"Não me incomoda."* Fica
> registrado como escolha declarada, não como descuido.
>
> **O que a decisão NÃO cobre:** ela vale para o que existe hoje, com a ordem de grandeza
> de hoje. Se o patrimônio crescer, ou se entrar dado de outra natureza — corretora, conta,
> valor de posição —, **a decisão precisa ser revisitada, não herdada.** Uma escolha feita
> sobre R$8 mil não se estende sozinha a R$800 mil.

> **A-04 — "a história está sob o código antigo" era uma suposição minha, e ela é falsa
> como regra. 12/09/2026.**
>
> O A-03 acima termina com uma frase que eu escrevi sem medir: *"o histórico ficou sob o
> código antigo"*. Fui medir. **Não há regra.**
>
> | código antigo | o endpoint responde? |
> |---|---|
> | `MRFG` (Marfrig) | **vazio** — nem `tradingName`, nem conteúdo |
> | `BRFS` (BRF) | **responde** — `BRF SA`, `codeCVM 16292`, 2 `cashDividends`, 2 `stockDividends` |
>
> Duas empresas da **mesma fusão**, dois comportamentos opostos. E há um detalhe que
> fecha o círculo: entre os `stockDividends` que o `BRFS` devolve está **a própria
> incorporação**. O evento que apagou o código está registrado sob o código que ele
> apagou.
>
> **O que isso corrige na fila:** "buscar pelo código antigo" não é um passo do pipeline
> — é uma tentativa, que às vezes funciona. Um ativo cujo emissor mudou de código tem a
> **lacuna declarada por ativo**, com status, e não uma correção presumida. A P5 na veia:
> limitação declarada vale mais que remendo silencioso.
>
> **O que continua aberto:** a MBRF. A história da Marfrig não está sob `MRFG` nem sob
> `MBRF`. Ou ela vem de outra fonte — CVM, que é por `CD_CVM` e imune a troca de ticker —
> ou o ativo entra com a lacuna escrita.

> **A-05 — o `refinar.py` violava uma regra que o próprio projeto tinha escrito.
> 12/09/2026.**
>
> `docs/fontes/cvm-enumeracoes-observadas.md` diz, com todas as letras: *"um parser que
> encontre valor fora de uma lista OBSERVADO deve falhar ruidosamente — nunca tratar como
> um dos valores conhecidos por padrão, nunca ignorar a linha em silêncio."*
>
> O `refinar.py` aceitava **qualquer** `label` calado. Só apareceu porque o `BRFS` do
> A-04 devolveu um tipo que eu nunca tinha visto: **`INCORPORACAO`**.
>
> **E `INCORPORACAO` não é mais um tipo na lista.** Os outros eventos de quantidade mudam
> o *preço* de um ativo. A incorporação troca ações de uma empresa por ações de **outra**,
> numa relação de troca: é mudança de **identidade** do ativo, não de escala. Tratá-la
> como evento comum **junta duas séries diferentes** e o gráfico fica lindo.
>
> **A correção:** `TIPOS_OBSERVADOS` (caixa, quantidade, direito), `conferir_tipo()` que
> **acumula** o desconhecido, marca a linha com `fator_status = TIPO_DESCONHECIDO`,
> **não descarta** (descartar perderia dado) e **não adivinha** (adivinhar seria o F-02).
> No fim, relatório em voz alta e **código de saída ≠ 0**.
>
> **A regra que fica:** regra escrita num documento de fonte não é regra até existir um
> teste que a meça. O projeto tinha a frase desde 06/09 e o parser que a violava desde
> 12/09 — e os dois conviviam sem se ver.

> **A-06 — a guarda contra duplicação passou um dia inteiro medindo o sintoma errado.
> 12/09/2026. É o pior achado da semana.**
>
> O `refinar.py` importa `desembrulhar` de `coletar_b3` em vez de reimplementá-la, porque
> duas leituras da mesma regra concordam por acidente até o dia em que não concordam
> (N-01). Havia teste para isso, e ele era verde:
>
> ```python
> assert r.desembrulhar is coletar_b3.desembrulhar
> ```
>
> **`desembrulhar` não existia no `coletar_b3.py` de produção.** A lógica estava
> **embutida** dentro de `coletar_eventos`. O nome só existia numa **cópia de teste** que
> eu mesmo escrevi aqui, com o comentário *"réplica local para teste; a versão de produção
> está no repositório dele"* — uma afirmação que eu nunca conferi.
>
> Ou seja: **existiam exatamente as duas implementações que a guarda existia para
> proibir, e a guarda dizia que não.**
>
> O defeito não era o código — era a **medição**. `is` mede se duas variáveis apontam
> para o mesmo objeto. Apontavam. O que ninguém media era se o **coletor usava a própria
> função que exporta**.
>
> **É o padrão recorrente do projeto na sua forma mais cara** — *um arquivo declara um
> comportamento que o código não tem, e os dois concordam por acidente* — com um
> agravante: aqui o arquivo que declarava era **o teste**. Teste verde é a coisa que a
> gente não volta a ler.
>
> **Como teria aparecido sem mim:** na segunda-feira, na primeira execução real. O
> `refinar.py` não falha em silêncio — o `try/except ImportError` levanta `SystemExit`
> com o texto do N-01. O desenho segurou; a **entrega** é que não.
>
> **A correção, e ela é dupla:**
> 1. `desembrulhar(texto) -> (dados, n_registros)` extraída de verdade para o
>    `coletar_b3.py`, com `coletar_eventos` **chamando-a**;
> 2. o teste reescrito para medir a **ausência de duplicata**: lê o código-fonte de
>    `coletar_eventos` e exige que ele chame `desembrulhar` e **não** contenha
>    `json.loads(texto)` nem `isinstance(dados, list)`.
>
> A guarda nova foi **testada contra a mutação**: reintroduzi o desembrulho embutido e ela
> falhou. Guarda que nunca falhou é guarda que ninguém sabe se funciona — foi essa a
> lição inteira.

> **A-07 — a mesma falha era barulhenta numa função e muda na vizinha. 12/09/2026.**
>
> Dois silêncios, achados ao arrumar o A-06:
>
> **1. Mais de um registro para a mesma emissora.** `desembrulhar` já contava quantos
> vinham, e o coletor imprimia o número. O `refinar.py` **descartava a contagem e usava o
> primeiro**. Mais de um registro não é erro — é informação. Mas escolher um deles sem
> dizer é escrever **ausência de critério no lugar de critério**, que é a P6 ao contrário.
> A contagem agora sobe até o relatório final, com o texto que importa: *"o silver usou o
> primeiro; isso não é uma regra, é a ordem em que a B3 devolveu."*
>
> **2. Página que não desembrulha para objeto.** No `linhas_do_suplemento`, esse caso
> devolve **aviso**. No `linhas_do_paginado`, era `continue` **mudo** — a página sumia do
> silver sem deixar rastro. **A mesma condição, o mesmo módulo, duas leituras que
> discordam — e a muda vencia, porque é a que roda oito mil vezes.**
>
> **A pergunta que isso deixa como método:** quando a mesma condição aparece em dois
> lugares do mesmo módulo, elas concordam? Não é uma pergunta de revisão de código — é
> uma pergunta de auditoria, e vale para todo par de funções irmãs do projeto.

> **A auditoria do A-07 — seis achados, quatro medidos. 12/09/2026.**
> *Documento inteiro em `auditoria/AUDITORIA-A07-FUNCOES-IRMAS.md`. Status `PARCIAL`:
> medida sobre o instantâneo de 06/09, não sobre o repositório real. Reconferir.*
>
> **E-01 — o `simular` de um módulo recusa rota bloqueada; o do outro devolve número.**
> `alocacao.simular_custo` levanta `InsumoBloqueado` se `not r.confiavel` (é o F-02
> escrito na docstring). `motor.simular` **não tem a guarda** — e o `motor.Rota` tem a
> propriedade `confiavel` e o `montar_rotas` preenche `bloqueios`. O dado está lá; a
> função não olha. Medido: BOVV11 bloqueada devolve **custo R$1.329,68, empatada com a
> rota que de fato não cobra nada**, e `alertas` vazio — porque a taxa desconhecida vira
> `adm_aa = 0.0` no default do dataclass. **É o K-07/F-02 literal, vivo no módulo irmão.**
> O teste que existia afirma `not bovv.confiavel`: confere que a bandeira está
> levantada, não que alguém a honra. **O A-06 outra vez, em outro arquivo.**
>
> **E-02 — arquivo ausente virou "nada registrado".** `tese.carregar_registros` faz
> `if not os.path.exists(p): return {}, {}`. O irmão `ambiente.declarado` faz o oposto,
> e escreveu a doutrina na própria docstring: *"NÃO tem valores de reserva: se o arquivo
> sumir, é erro, porque sem ele não há nada a conferir."* G7/G8 falham para o lado
> seguro, então o sistema não fica perigoso — fica **mentiroso**: você lê *"nenhuma tese
> registrada para esta rota"* quando o fato é *"o teses.yaml não foi encontrado"*.
> Rodando da pasta errada com vinte teses, você lê a mensagem errada vinte vezes. E
> `teses.yaml` **é** o pré-registro: a P4 existe justamente para que não se confunda
> *"nunca me comprometi"* com *"o registro sumiu"*. Oito carregadores, **três
> tratamentos** para a mesma condição — e os dois que acertam são os dois que
> escreveram a consequência na mensagem. Não é coincidência: quem escreve a
> consequência descobre que precisa levantar.
>
> **E-02 RESOLVIDO em 12/09, e a decisão de desenho é dele.** Perguntei se arquivo
> ausente e arquivo vazio deviam ser a mesma coisa — porque a U-01 manda não quebrar o
> primeiro dia de um usuário. Resposta: **são coisas diferentes.** Ficaram três estados,
> com três mensagens: **ausente** levanta `RegistroAusente`; **vazio** (em branco, `{}`,
> só `meta:`, seções nulas) devolve `({}, {})` e isso é legítimo — é o estado do
> primeiro dia; **ilegível** levanta `RegistroIlegivel`, porque YAML quebrado pode ter
> o registro inteiro dentro, ilegível por um caractere, e chamar isso de "nenhuma tese"
> seria dizer que não há registro quando há.
>
> A U-01 virou **parâmetro**, não padrão: `permitir_ausente=True`. Quem simula um
> usuário novo **pede** a ausência em vez de recebê-la calado e nunca saber a diferença.
> E o caminho do usuário novo nem passa por ali — `alocar()` aceita `teses={}` injetado,
> que é o que o `test_usuario_novo.py` já fazia.
>
> 13 testes, e o que dá nome ao achado é `test_a_diferenca_entre_ausente_e_vazio_e_
> OBSERVAVEL`: antes, os dois devolviam `({}, {})` e eram **indistinguíveis de fora** —
> e era exatamente essa indistinguibilidade o defeito.

> **E-03 — o `politica.yaml` declara nove interruptores e dois não estão ligados em
> nada.** Sete portões leem `g["ativo"]`. `g3_atrito` e `g4_dominancia` **não**. Medido:
> `G3_atrito.ativo = false` barra **os mesmos 5 ativos de 25**. Hoje os nove estão
> `true`, então **arquivo e código concordam por acidente** — a frase do defeito
> recorrente, literal. O custo não é erro: é **conclusão errada sobre o próprio
> sistema**. O dia em que você perguntar *"quanto do resultado vem do atrito?"* — que é
> para isso que o sistema foi feito — a resposta será "nada", e será falsa. Nenhum teste
> pega, porque nada está quebrado. P2 violada em 2 de 9 consumidores.
>
> **E-04 — o `impacto.py` só responde quando você já desconfia.** `quem_le`,
> `leituras_de_yaml`, `quem_usa_campo` são boas ferramentas e todas exigem que você
> **nomeie a chave**. Ninguém ia perguntar por `portoes.G3_atrito.ativo` — justamente
> porque ninguém suspeitava. Faltava a pergunta inversa, que não precisa de suspeita:
> **quais chaves o YAML declara que código nenhum lê?** Agora existe:
> `auditoria/chaves_orfas.py`.
>
> **E-05 — RETIRADO em 12/09, no mesmo dia em que foi escrito. Era falso positivo
> meu, e é o maior erro da auditoria.** Eu escrevi que `liquidez_media_dias: 15` e
> `liquidez_pior_caso_dias: 29` não tinham leitor e que o G2 escolhia a rota da reserva
> sem termo de liquidez. **As três afirmações são falsas.** O `catalogo.yaml` lê a
> chave por `{de_campo: "cofrinho.picpay_garantia_de_limite.liquidez_pior_caso_dias"}`;
> o portão existe (`exige_liquidez_dias`, em `g6_coerencia_funcao`); ele está declarado
> por função (`LIQUIDEZ: 1`, `LASTRO: 5`, `DATADO: 30`); e roda **ordem 1**, antes do
> G1 e do G2, tirando a função da rota lenta — então ela nem chega ao G2. Medido: o
> `picpay_cofrinho` de 29 dias **nunca teve LIQUIDEZ**, declara LASTRO e perde até isso;
> as três rotas da reserva resgatam em **zero dias**.
>
> **A causa raiz, e ela é sobre método:** minha ferramenta varria **só os `.py`**, num
> projeto que põe regra em YAML de propósito e cujo `impacto.py` **já mapeia** as
> arestas YAML→YAML. Auditei metade do sistema e chamei o resultado de conclusão.
> É o A-06 do meu lado da mesa: a ferramenta mediu o lugar errado e o verde dela me
> convenceu. `chaves_orfas.py` agora conta `{de:}/{de_campo:}/{soma:}` como leitura.
>
> **E o que o derrubou não foi eu conferir:** foi ele responder *"portão"* e eu ir
> escrever o código que já existia. Um achado pode sobreviver a uma revisão e morrer
> na primeira tentativa de agir sobre ele.

> **E-06 — o pré-registro declara as próprias guardas e nada as executa.**
> `hml_puro_v1.variantes_permitidas: 1` é o **limite anti-p-hacking**: os graus de
> liberdade que ele se autorizou antes de olhar o resultado. Zero leituras. Nada conta,
> nada compara, nada falha na décima variante. `greenblatt_v1.verificar_monotonicidade:
> true` idem. **Um pré-registro que declara a guarda e não a executa vira documento
> sobre intenções** — a P4 entrega a impressão digital e o compromisso fica em prosa.
>
> **E-06 — as duas medições que mudaram a pergunta. 12/09/2026.**
> *Documento em `auditoria/E06-O-QUE-CONTA-COMO-VARIANTE.md`. Decisão de desenho aberta.*
>
> Antes de contar variantes é preciso saber o que se conta. Fui procurar, no próprio
> pré-registro, um grau de liberdade não declarado. Achei dois candidatos, **e nenhum
> dos dois é o que eu esperava.**
>
> **O filtro de pregões não era p-hacking, e a medição é que diz.** O pré-registro fala
> em 307 meses; a execução registra 306, *"filtro n_dias >= 15"* — e o 15 é um **default
> em Python** (`fatores.premios(minimo_dias=15)`), invisível ao registro. Variando só o
> filtro: **de 5 a 18 o alfa é idêntico ao quinto decimal** (0,00766, t = 2,94), porque
> qualquer corte razoável corta o mesmo mês — o último, de 3 pregões. Hipótese minha,
> medida e **caída**. Registro porque a conclusão importa nos dois sentidos: uma escolha
> não declarada pode ser inofensiva, e a única forma de saber é medir a sensibilidade.
>
> **O grau de liberdade que existe inverte o SINAL, e nenhum contador o pegaria.**
> `alfa_contra_fatores` faz `y = retorno − Risk_Free`, porque foi escrita para
> estratégia long-only. HML é long-short, de custo zero: já é excesso. Subtrair o CDI
> brasileiro (0,938% ao mês na amostra) leva o alfa de **+0,00766 (t = 2,94, rejeita)**
> para **−0,00178 (t = −0,68, não rejeita)**. Mesmo dado, mesma regressão, mesma
> amostra, **veredito invertido** — e não é parâmetro, nem amostra, nem campo do
> registro: é como se monta a variável dependente.
>
> **E o projeto já sabia.** Eu ia publicar isto como achado e parei ao ler em volta:
> `backtest_h1_h3.py` linha 9 avisa em português para não usar aquela função ali; o
> idioma correto (`alfa_contra_fatores(m.HML + m.Risk_Free, m)`) está nos testes;
> `test_h1_h3_reproduzem_o_resultado_registrado` afirma 0,00766 e t = 2,94; e
> `test_subtrair_risk_free_de_um_fator_inverte_o_veredito` **prende a armadilha num
> teste**, com a docstring dizendo que existe para o dia em que alguém "consertar" o
> código. É o projeto no seu melhor.
>
> **A consequência de desenho, e ela governa a decisão:** o grau de liberdade mais
> perigoso do pré-registro **não é contável** por nenhuma definição de variante. O que o
> segura é uma convenção escrita e um teste. Qualquer desenho que trate
> `variantes_permitidas` como defesa principal protege o flanco errado — e por isso a
> recomendação é **rebaixar o contador a alarme**: estourar o limite não bloqueia a
> execução, exige justificativa escrita. **O que protege contra p-hacking não é o número
> de tentativas; é o registro de todas elas.** Um limite de 1 sem registro da tentativa 2
> é mais fraco que um limite de 5 com as cinco escritas.
>
> **E há uma régua de sizing que ele já usa sem ter escrito:** o Greenblatt tem 3 porque
> a especificação publicada é ambígua (`nota_definicao`: implementações honestas divergem
> por um fator de três); o `hml_puro_v1` tem 1 porque é regressão sobre série publicada,
> sem espaço. **O número segue a ambiguidade da fonte.**

> **E-06 decidido por ele em 12/09/2026 — e a decisão corrigiu o meu desenho em três
> pontos.** *Modelo de dados em `auditoria/PRE-REGISTRO-MODELO-DE-DADOS.md`.*
>
> **1. Dado novo, mesma spec = EXTENSÃO**, não variante. A razão dele é de incentivo e
> é decisiva: transformar atualização temporal em variante ensina *"não atualize o
> estudo, isso gasta a sua única bala"* — e é o mesmo defeito que derrubou o D1, onde
> corrigir um erro consumia a mesma bala que uma escolha metodológica.
>
> > **Meu acréscimo:** a extensão não precisa de regra própria se a amostra for
> > registrada como **regra** e não como data — `fim: ULTIMA_DISPONIVEL`. Aí a data
> > literal vira **saída** da execução e não entrada do registro, e toda a tabela de
> > classificação dele (`2001→2005` é variante, novo filtro é variante, novo fim é
> > extensão) passa a ser **consequência do formato** em vez de lista a decorar.
> > Cláusula de exceção é a superfície por onde o contorno entra.
>
> **2. O controle é do CONJUNTO**, com o limite por estratégia como camada auxiliar —
> multiplicidade é problema da família, ambiguidade metodológica é local.
>
> > **E o conjunto tem um NÚMERO, que nem ele nem eu tínhamos.** Se cada estratégia
> > rejeita a t > 1,96, oito testes dão **1 − 0,95⁸ ≈ 34%** de ao menos uma rejeição
> > falsa sob a nula. Medido, com Bonferroni: m=2 (as executadas) → corte **2,253**;
> > m=8 (as pré-registradas) → **2,754**; m=13 (o orçamento inteiro, soma dos
> > `variantes_permitidas`) → **2,913**.
> >
> > **O HML (t = 2,94) sobrevive até o corte mais severo — por 0,027 de um t.** Não o
> > invalida; recoloca. "t = 2,94" soa como p ≈ 0,003; corrigido pela família que o
> > próprio projeto pré-registrou, é significância **na margem** — coerente com as
> > quatro razões que o registro já dava para não agir sobre ele. Ressalva contra mim:
> > Bonferroni **superestima** a correção com testes correlacionados, e estes são (mesma
> > série, mesmos cinco fatores). O corte verdadeiro fica entre 1,96 e 2,891.
>
> > **E `pesquisa_id` não pode ser declarado.** Ele viu o buraco — *"alguém cria
> > Conjunto A, B, C e reseta o contador"* — e fechou com julgamento. Julgamento é
> > contornável por quem está de boa-fé e com pressa, que é o caso perigoso. **Ancorar
> > no dado:** `pesquisa_id` derivado de `hash_fonte()` + regra de amostra, os dois já
> > existentes. Renomear não reseta, porque o nome não é a chave — e `m` passa a ser
> > **calculável** a partir do diário, não afirmado por quem registra.
>
> **3. Erro factual é isento de variante, mas auditável e com fonte primária quando
> material** — e a distinção dele é a que importa: erro de fato **não tem alternativa
> defensável do outro lado**; grau de liberdade tem duas leituras e você escolheu uma. O
> `tratamento_rf` é o caso puro de grau de liberdade disfarçado de correção.
>
> > E ele acrescentou o quarto tipo, que fecha a porta: quando há duas leituras e
> > **nenhuma fonte desempata**, não se declara erro factual — declara-se
> > `NAO_CONFIRMADO` e para. É o C-01 virando regra de processo.
>
> **4. A regra dele que vale mais que as três:** extensão nunca sobrescreve, correção
> nunca apaga, variante nunca apaga a especificação anterior. O sistema vira uma
> sequência de estados auditáveis em vez de uma planilha melhorada até dar o resultado
> desejado — e é a mesma doutrina do *achado retirado fica como retratação*.
>
> > **O que falta nela, e o sistema precisa agir:** se R1 rejeita e R2 (extensão) não,
> > **o que o portão lê?** Sem regra, "preservar tudo" vira "escolha o que preferir" —
> > p-hacking com auditoria completa. Proposta: a extensão mais recente é o **operativo**,
> > e divergência de veredito entre R1 e Rn é **bloqueante** até estar escrita. Um alfa
> > que morre ao estender é o evento mais informativo que este projeto pode produzir;
> > merece uma parada, não uma linha de log.
>
> **E o que este aparato NÃO protege, declarado de propósito (P5):** nada nele teria
> pego o Risk_Free invertido. Especificação congelada, graus de liberdade, diário e
> contador passariam por aquilo sem piscar, porque `tratamento_rf` só entra na lista se
> alguém **souber que ele existe**. O que pegou foi um comentário em português e dois
> testes. **A limitação declarada vale mais que a proteção presumida** — e é por isso que
> o contador é alarme, não defesa.

> **Correção dos meus próprios números do E-06, e ela aperta a margem. 13/09/2026.**
> Calculei os cortes com a **normal**; o certo para 306 meses e 5 parâmetros é a **t de
> Student com 301 gl**, que é um pouco mais alta. Recalculado: m=2 → **2,253**; m=8 →
> **2,754**; m=13 → **2,913**. **A folga do HML cai de 0,049 para 0,027.** O sinal da
> conclusão não muda — ele sobrevive — mas a margem é ainda mais fina do que escrevi.

> **P-77 FECHADA em 13/09/2026 — e a pendência estava descrevendo o sintoma errado.**
> *Documento em `auditoria/P77-CAMPO-MORTO.md`.*
>
> A pendência dizia que *"`retorno_liquido_aa` zera o IR de ganho do FII"*. **Não zera:
> devolve `None`** — o FII é `indexador: rv` e a função sai antes da linha do imposto.
> Procurar pelo sintoma descrito não achava nada, e é por isso que ficou aberta.
>
> **O defeito real:** `aliquota_ganho` tem **zero leituras no motor**. As quatro únicas
> estão em `test_alocacao.py`. A P-13 partiu `isento_ir` em dois campos pela razão certa
> (rendimento isento por Lei 11.033/2004; ganho a 20% por Lei 8.668/1993), criou o
> campo, o catálogo preencheu com a lei citada — **e nenhuma linha consumiu**. Mudança
> de ESQUEMA anunciada como correção de COMPORTAMENTO.
>
> **Três coincidências o esconderam:** o FII é `rv`; o FII está bloqueado; e as únicas
> outras rotas com `aliquota_ganho` são LCI/LCA, **com 0,0**, onde a diferença não
> aparece.
>
> **O número, medido, com a rota que vai existir amanhã:** uma debênture incentivada
> (`isento_ir_rendimento: true`, `aliquota_ganho: 0.20`, `indexador: cdi`) devolvia
> **0,13900** — o imposto inteiro zerado, e **exatamente o número da LCI/LCA**. O motor
> a trataria como isenta nas duas pontas. Errado **para menos**: a rota apareceria mais
> rentável do que é e competiria melhor no G2.
>
> **A correção recusa em vez de chutar.** `regime_tributario()` devolve a alíquota
> quando há uma só, e **um motivo** quando há duas. `retorno_liquido_aa` não inventa um
> modelo de duas pontas — ela modela instrumento que ACUMULA rendimento, onde o ganho é
> o rendimento. P6: lacuna declarada, não critério inventado. E o motivo **não some
> junto com o `None`** — foi um `None` calado que escondeu isto por oito dias.
>
> **A guarda que impede a próxima:** *todo campo que o `catalogo.yaml` preenche tem de
> ser lido por um módulo que não é teste*. Rodada contra o código de antes, ela acusa
> `aliquota_ganho` pelo nome. Teria pegado a P-77 no dia em que nasceu.
>
> **E a lição é sobre o meu instrumento, pela quarta vez no mesmo tema.** O
> `chaves_orfas.py` que escrevi ontem **não** pegou este campo. Fui ver por quê
> esperando um problema de dataclass; era outra coisa: ele varre **todos** os `.py`,
> testes inclusive. **Campo que só o teste toca é campo que o motor não usa** — e é
> categoria pior que órfã pura, porque tem uma testemunha: o teste prova o esquema e
> ninguém prova o comportamento. Foi assim que a P-13 anunciou correção com a suíte
> verde. A ferramenta agora separa leitor do motor de leitor de teste e reporta
> **"LIDA SÓ POR TESTE"** como categoria própria.

> **A terceira vez no mesmo padrão, e agora é regra de método. 12/09/2026.**
>
> Nesta auditoria eu **publiquei** o E-05 (retirado: a chave era lida por outro YAML),
> **quase publiquei** o multiplicador de estabilidade (era leitura por índice variável) e
> **quase publiquei** o Risk_Free acima — com o projeto já tendo um comentário, uma
> convenção e dois testes sobre ele.
>
> Os três têm a mesma forma: **medi, e conclui antes de ler em volta.** Os dois achados
> que sobreviveram — E-01 e E-03 — foram confirmados **lendo**, não medindo.
>
> **A ordem é: medir → ler a vizinhança → concluir.** Numa auditoria a medição levanta o
> candidato; quem o promove a achado é a leitura. Eu vinha fazendo medir → concluir, e
> lendo só quando alguma coisa me obrigava.

> **O falso positivo, e ele ensina mais que dois achados.** A ferramenta acusou
> `G2_reserva.ajuste_estabilidade.{alta,media,baixa}` — o multiplicador da reserva por
> estabilidade de renda. **Falso:** é lido quatro vezes, com índice **variável**
> (`g["ajuste_estabilidade"][estado.estabilidade_renda]`), e por isso o nome da folha
> nunca aparece literal. O que pegou não foi a ferramenta — foi **ler**. Virou regra no
> código (`pais_varridos()`: quem alcança os filhos por variável lê todos os filhos) e
> derrubou 23 candidatos para 19 **sem derrubar nenhum achado**, que é o teste certo de
> um filtro. E virou a razão de os dois scripts imprimirem *"candidatos"*, nunca
> *"achados"*: **P3 aplicada à própria auditoria.**
>
> **Uma convenção que existe e ninguém escreveu.** Sete impressões digitais, dois
> cortes de `sha256` — e não é inconsistência: **arquivo → `[:12]`, conteúdo →
> `[:16]`**, os sete obedecem. Só que a regra não está escrita, então a oitava é
> cara-ou-coroa, e comparar um `[:12]` com um `[:16]` nunca bate, em silêncio.

> **P-76, P-78 e B-04 — fechadas em 13/09/2026, e duas mudaram de forma ao serem
> medidas.** *Documento em `auditoria/P76-P78-B04.md`.*
>
> **P-76 — a doutrina, e ela vale sozinha:** uma conclusão **não herda** o status do
> insumo mais fraco. Ela herda o resultado de uma **medição de sensibilidade** —
> sobrevive a toda a faixa que a incerteza admite → `COMPLETO` com a faixa declarada;
> inverte dentro da faixa → `PARCIAL` com a fronteira declarada; faixa desconhecida →
> `NAO_CONFIRMADO`. Herdar o mais fraco enterraria conclusões robustas junto com as
> frágeis e ensinaria a não medir. **O status de uma conclusão é uma medição, não uma
> herança.**
>
> > **Mas o caso F-03 não é exemplo disso — é vazamento.** `custos.yaml` diz
> > `etf.IMAB11: valor None, status NAO_CONFIRMADO, motivo "taxa nao obtida"`. E a
> > conclusão cita **0,25%**, que existe em **três** documentos (`PENDENCIAS.md:152`,
> > `politica.yaml:859`, `pesquisa-bases-e-apis:293`, decomposto em adm 0,04 +
> > custódia 0,03 + gestão 0,18) **e não existe no arquivo que o código lê**. Quem roda
> > o motor hoje recebe o IMAB11 bloqueado enquanto os documentos dizem que a questão
> > está resolvida. É o C-01 no lugar mais caro.
> >
> > **E medida, a conclusão é frágil:** 0,25% contra 0,20% são **5 pontos-base**, com o
> > lado incerto sendo soma de três componentes de fonte secundária. A F-03 é
> > **`PARCIAL`**, com fronteira declarável: inverte se o IMAB11 ficar abaixo de 0,20%.
> > Não ponho o valor no `custos.yaml` sozinho — é entrada de valor com fonte, e eu não
> > abri a página do gestor; registrar citando documento interno seria citar a mim mesmo.
>
> **P-78 — os oito campos existem (a contagem estava certa), mas são TRÊS naturezas:**
>
> - **procedência, e está certo (2):** `bc_procedentes`/`bc_clientes` são lidos por
>   `test_corretoras.py:90-91`, que **recalcula o índice a partir das partes**. São o
>   insumo que prova o número derivado. **Reclassificar, não consertar.**
> - **ausência de critério declarada, e está certo (3):** `home_broker_web`,
>   `exporta_csv` e os `ra_*` — e `regras()` **levanta `NotImplementedError`** se
>   alguém ligar `facilidade.pontua`. **P6 executada corretamente**, o oposto do E-03:
>   aqui o interruptor falha alto em vez de não fazer nada.
> - **defeito de verdade (3):** `mesa_minimo`, `corretagem_fii`, `exercicio_opcao_pct`
>   — custos por operação que `pontuar()` não considera.
>
> > **E o `corretagem_etf_pct` — o 0,50% da XP — é N-01, não campo ignorado.** ⚠️
> > **RETIFICADO em 13/09, ver o bloco E-08 abaixo:** eu escrevi que o `catalogo.yaml`
> > tinha `corr_pct: 0.005` literal. **Não tem.** Ele faz
> > `corr_pct: {de: "corretagem.xp_etf_pct"}` — referencia, exatamente como o próprio
> > cabeçalho dele manda. O catálogo é o **contraexemplo**, não o culpado. A duplicata
> > está em outro lugar, e são seis, não uma.
>
> **B-04 — a correção é apagar, não construir.** `pip install -e .` falha por
> descoberta automática com vários diretórios de topo. Declarar os pacotes seria a
> correção óbvia e **errada**: ninguém instala este projeto —
> `comando_de_instalacao()` monta `pip install "numpy==..."`, instala as
> **dependências**, e nenhuma linha faz `import bastter`. `[build-system]` era uma
> promessa que o código não usa; o `pyproject.toml` daqui é **manifesto**, lido por
> `ambiente.declarado()` via tomllib, e é disso que a P-15 depende. **Medido antes de
> apagar: a impressão do ambiente é `7565df1381e2c1ed` com e sem a seção** — idêntica à
> registrada, então a remoção não invalida resultado pré-registrado nenhum.
>
> > **E um erro meu, pego rodando duas vezes.** A primeira guarda de idempotência do
> > `B04-patch.py` era `if "[build-system]" not in s: sair` — e a nota que o patch
> > **insere** menciona `[build-system]` em prosa, então a segunda execução casava com
> > o próprio comentário e aplicava de novo. **Guarda de idempotência também precisa
> > ser testada rodando duas vezes.** Agora a marca é do patch, não da string removida.

> **A série histórica do JCP FECHOU — e o fechamento corrige um erro meu. 13/09/2026.**
> *Transcrições em `docs/fontes/lei-9249-1995-jcp-planalto.md`, todas do Planalto.*
>
> | de | até | alíquota | norma |
> |---|---|---|---|
> | 01/01/1996 | 31/12/2015 | **15%** | Lei 9.249/1995 art. 9º §2º, redação original |
> | **01/01/2016** | **08/03/2016** | **18%** | MP 694/2015 art. 1º, efeitos por art. 4º, I; encerrada pelo Ato Declaratório nº 5/2016 |
> | 09/03/2016 | 31/12/2025 | **15%** | redação original restabelecida |
> | 01/01/2026 | — | **17,5%** | LC 224/2025 art. 8º, vigência pelo art. 14, **III** |
>
> **A janela do meio tem 68 dias** — 31 de janeiro + 29 de fevereiro (bissexto) + 8 de
> março. Todo JCP pago nela sofreu 18%, e **o imposto permanece devido**: a CF art. 62
> §11 mantém as relações regidas pela MP quando o Congresso não edita decreto
> legislativo, e não editou. **Caducar não devolve imposto pago.**
>
> **A CORREÇÃO, e ela é contra mim.** Em 12/09 escrevi aqui que a LC 224 vigora em
> **01/04/2026** pelo art. 14, I, "b", e que a fonte secundária que dizia 01/01/2026
> estava contradita pelo Planalto — *"fonte primária ganha"*. **Estava errado, e a
> secundária estava certa.** A alínea "b" cobre **os arts. 7º e 9º**; o art. 8º — o do
> JCP — cai no **inciso III**, *"a partir de 1º de janeiro de 2026"*.
>
> > **O erro não foi de fonte, foi de ENDEREÇAMENTO:** li a cláusula certa e a apliquei
> > ao artigo errado. Ler um artigo de vigência sem checar **qual item ele nomeia** é
> > ler metade dele. E é pior que não ter consultado: usei a autoridade da fonte
> > primária para descartar uma secundária correta, **com confiança**.
> >
> > **Regra que fica: "fonte primária ganha" não é passe livre.** Ela ganha depois de
> > se verificar qual dispositivo a cláusula alcança. Procedência é sobre **verificar**,
> > não sobre hierarquia.
>
> **E a mesma fonte secundária errava a primeira faixa ao contrário** — dizia 18% até
> 2015 e 15% pela MP 694, quando a original é 15% e a MP **subiu** para 18%. Duas
> fontes secundárias, dois erros em direções opostas, e num deles ela estava certa.
>
> **MP 1.303/2025 não entra:** o Planalto não a lista entre as que deram redação ao
> §2º, e ela caducou em outubro/2025 (retirada de pauta na Câmara) antes de produzir
> efeito.
>
> **O que foi entregue:** `tributacao.ir_jcp_fonte` no `custos.yaml` com as quatro
> vigências e a norma ao lado de cada número; `alocacao/jcp.py` com `aliquota_jcp(data,
> C)` e `jcp_liquido()`; **16 testes**, e os que importam são os de **fronteira** — no
> meio de uma faixa qualquer implementação acerta.
>
> **Uma coisa declarada de propósito (lição da P-77):** `jcp.py` **não tem chamador no
> motor hoje**, porque a série de retorno total líquida ainda não existe. Isso está
> escrito no topo do módulo, junto com a consequência: **se a série líquida nascer sem
> chamar esta função, é defeito.**
>
> **E um erro que o próprio teste pegou:** eu tinha escrito "67 dias" — 2016 é
> bissexto, e são **68**.

> **E-08 — o `bloqueia` que nomeia o consumidor, e o consumidor que não pergunta.
> 13/09/2026.** *Testes em `alocacao/test_e08_bloqueio_e_copia.py`.*
>
> **Primeiro a retratação, porque ela vem antes do achado.** Em `P76-P78-B04.md` e aqui
> eu escrevi que o `catalogo.yaml` carregava `corr_pct: 0.005` literal, duplicando a
> constante. **Fui ler o arquivo e ele faz o contrário:**
>
> ```yaml
> bova11_xp:
>   corr_pct:    {de: "corretagem.xp_etf_pct"}
>   saida_extra: {de: "corretagem.xp_etf_pct"}
> ```
>
> Referencia, duas vezes, e por isso herda status, procedência e `expira` de graça. **O
> catálogo é o contraexemplo do defeito, não o defeito.** Foi a sexta vez nesta semana
> que concluí antes de ler o arquivo — e a segunda que a conclusão chegou a ser
> publicada.
>
> **O achado de verdade, medido:** `custos.yaml -> corretagem.xp_swing` é `PARCIAL` e
> declara **`bloqueia: ["ranking_corretoras"]`** — nomeia **este** consumidor, não um
> genérico. E o ranking **roda**: `pontuar()` devolve **46,0** para a XP, com
> multiplicador **0,8**. Porque `pontuar()` lê `inst.corretagem_rv` do
> `instituicoes.yaml` e **nunca chama `val()`** — então a consequência declarada não
> chega até ele.
>
> A mesma incerteza, sobre o mesmo número, tratada de dois jeitos: **bloqueio duro** no
> `custos.yaml`, **multiplicador 0,8** no `instituicoes.yaml`. E o macio vence, porque é
> o do caminho que executa.
>
> > **E o ponto não é que alguém escolheu o multiplicador: é que ninguém escolheu.** Os
> > dois mecanismos são deliberados, moram em arquivos diferentes e não se conhecem —
> > **o layout dos arquivos decidiu qual vence.** É o F-05 pela metade: `bloqueia`
> > deixou de ser prosa para quem passa por `val()`; para quem não passa, continua prosa.
>
> **E-08b — a cópia não herda o relógio, e são SEIS.** Medindo o mesmo fato nos dois
> arquivos (e descartando as quatro coincidências de valor — `exercicio_opcao_pct:
> 0.005` bate com `xp_etf_pct` por acaso, 0,5% é taxa comum):
>
> | `instituicoes.yaml` | `custos.yaml` |
> |---|---|
> | `xp.corretagem_rv` 4,9 | `corretagem.xp_swing` (PARCIAL) |
> | `xp.corretagem_etf_pct` 0,005 | `corretagem.xp_etf_pct` (COMPLETO) |
> | `caixa.corretagem_rv` 4,49 | `corretagem.caixa_fixa` |
> | `caixa.corretagem_pct` 0,0002 | `corretagem.caixa_pct` |
> | `safra.corretagem_rv` 4,5 | `corretagem.safra_terra` |
> | `terra.corretagem_rv` 4,5 | `corretagem.safra_terra` |
>
> **As cinco constantes têm `expira: 2026-12-04`. As seis cópias não têm campo de
> validade nenhum.** Em 05/12/2026 o `val()` começa a avisar para quem **referencia** — e
> as cópias continuam caladas, para sempre. **O projeto construiu um relógio e metade
> dos números não está ligada nele.**
>
> Note também que o `xp_etf_pct` é `COMPLETO` no `custos.yaml` e o bloco que o copia
> declara `PARCIAL`: **o mesmo número com dois status.**
>
> **A causa raiz não é de quem escreveu o número:** o `instituicoes.yaml` **não tem
> resolvedor de referência**. O `catalogo.yaml` tem `{de:}` e por isso acerta. Enquanto
> o formato não oferecer a alternativa, copiar é a única coisa que se pode fazer.
>
> **14 testes**, 7 verdes e **7 `xfail(strict=True)`** — os sete medem defeito aberto, e
> o `strict` obriga a tirar o marcador no dia do conserto.

> **E-08 FECHADO em 13/09/2026 — o `instituicoes.yaml` ganhou resolvedor de
> referência.** *Decisão dele: resolvedor, não remoção. Documento em
> `auditoria/E08-RESOLVEDOR.md`.*
>
> `{de: "corretagem.xp_etf_pct"}` passa a valer em qualquer campo de custo, e a
> resolução **passa por `val()`** — é isso que faz status, procedência, `expira` e
> `bloqueia` caírem de graça. As seis cópias viraram referência.
>
> **Três regras, e cada uma responde a um erro anterior:** constante `COMPLETO` devolve
> o valor; constante que **bloqueia o contexto declarado** devolve `None` com o motivo;
> `NAO_CONFIRMADO` devolve `None` sempre. **O contexto é opcional de propósito** — *um
> consumidor que não se nomeia não pode reivindicar um bloqueio dirigido a outro*.
>
> E o `None` **não é um buraco**: é o valor que `pontuar()` já sabia tratar, marcando a
> dimensão como não avaliada e deixando a `cobertura` penalizar. *"Dimensão ausente é
> penalidade, não neutralidade"* já estava escrito lá dentro. **O resolvedor não
> inventou tratamento nenhum — fez o dado chegar ao tratamento que existia.**
>
> O ranking passou a **se nomear**: `catalogo_instituicoes(contexto=RANKING)`. Uma
> linha, e é ela que transforma a frase do YAML em comportamento.
>
> **Medido — e o número engana:**
>
> ```
> XP antes:   total 46,0   corretagem = 2,0     multiplicador 0,80
> XP depois:  total 45,9   corretagem = None    "corretagem NÃO CONFIRMADA"
> ```
>
> > **A nota praticamente não mudou** — perder a dimensão tira um peso de 12 que valia
> > 2,0, e os efeitos quase se cancelam. **E isso não torna a correção menor.** O que
> > mudou não foi *quanto*, foi **o que o sistema afirma**: antes ele dizia *"a
> > corretagem da XP é ruim, nota 2,0"*, uma asserção sobre um número que o próprio
> > projeto declarava não conseguir ler; agora diz *"não sei ler, e isso custa
> > cobertura"*. **Uma correção de honestidade pode não mexer no resultado e continuar
> > sendo correção.** Chamar isso de "sem impacto" seria medir a coisa errada.
>
> **Prova de inércia:** os conjuntos de falha da suíte são **idênticos** com e sem o
> patch — 12 nos dois, nenhuma nova, nenhuma sumiu (as 12 são P-15 e P-40 do meu
> ambiente). `test_corretoras.py` segue com 26 verdes. As seis referências, sem
> contexto, devolvem exatamente os valores de antes.
>
> **17 testes novos, zero `xfail`** — os sete que documentavam defeito aberto agora
> medem o conserto. O melhor deles **adianta o relógio** (`motor.HOJE = 2027-01-01`) e
> confirma que o aviso de expiração passou a sair também para o `instituicoes.yaml`.
> **O relógio existia; faltava ligar o outro lado nele.**

> **E-09 — a chave duplicada que apagou oito dias de trabalho. 13/09/2026, e é o
> achado mais silencioso do projeto.** *Documento em `auditoria/F03-IMAB11-E09.md`.*
>
> `custos.yaml -> etf:` tinha **`IMAB11:` duas vezes**: a de cima (05/09) com
> `valor: 0.0025, status: PARCIAL` e a página do gestor como fonte; a de baixo, oitenta
> linhas abaixo, com `valor: null, NAO_CONFIRMADO`. **PyYAML fica com a última, sem
> aviso nenhum.** O `PENDENCIAS.md` dizia *"fechada 05/09 — 0,25%"*, o motor via
> `NAO_CONFIRMADO`, e **os dois discordaram em silêncio por oito dias**.
>
> **E eu errei sobre isto ontem:** escrevi que *"a taxa nunca entrou no arquivo que o
> código lê"*. Entrou. Medi `C['etf']['IMAB11']` — o valor **carregado** — e concluí
> sobre o **arquivo**. É a décima linha da régua §5-B.
>
> **A guarda é da classe:** `auditoria/chaves_duplicadas.py`, um `SafeLoader` que
> **recusa** duplicata em vez de escolher. Varrido sobre os sete YAMLs: **exatamente
> uma no projeto inteiro**, e era a que importava. 10 testes, com prova por mutação — e
> o teste mostra que o `yaml.safe_load` padrão **não reclama** da duplicata sintética.
>
> > **E a ferramenta errou antes de acertar, na mesma manhã em que escrevi a régua.** A
> > primeira versão reprovava o `catalogo.yaml` inteiro, porque ele usa âncora e merge
> > (`<<: *base`) e meu loader não construía a tag. **Sobrescrever chave da âncora é o
> > propósito do merge.** Alcance do instrumento menor que o sistema, outra vez.

> **F-03 e P-05 FECHADAS — ele mandou a lâmina do gestor. 13/09/2026.**
>
> Lâmina It Now ID ETF IMA-B, Itaú Asset, **31/08/2026**: administração **0,04%** +
> custódia **0,03%** + gestão **0,18%** = **0,25% a.a.**, e a linha *"taxa cobrada"* é
> **igual** à *"taxa máxima"* nas três colunas — o que responde exatamente a dúvida
> registrada (*"é teto de regulamento ou taxa efetiva?"*) sem precisar do regulamento.
>
> **A P-05 estava certa ao dizer que a pendência era mal formulada:** não era número
> ausente, era **campo errado**. "Taxa de administração" é um componente, e aqui é o
> **menor dos três** — comparar por `taxa_adm` subestimaria em **seis vezes**.
>
> **F-03 remedida, e a conclusão ficou mais forte:** incluindo a custódia de RV da B3
> que o ETF paga acima de R$26.471,77 e o Tesouro não, o Tesouro IPCA+ vence em **todas**
> as faixas, e a margem **abre** de +0,05 pp (R$5 mil) para **+0,09 pp** (R$100 mil).
> Pela régua da P-76, isso é `COMPLETO` com a faixa declarada — **a fragilidade que eu
> apontei era do insumo, não da conclusão.**

> **A evidência sobre pré-registro — e ela contraria a MINHA recomendação. 13/09/2026.**
> *Documentos em `auditoria/PREREGISTRO-EVIDENCIA.md` e o relatório completo, 25 fontes.*
>
> Ele confirmou o desenho e pediu evidência. A evidência apoia duas camadas, é ambígua
> numa e **contraria a quarta — o contador como alarme, que fui eu quem recomendou.**
>
> - **Lerner & Tetlock (1999):** *accountability* **piora** o julgamento quando a escolha
>   envolve *"options easiest to justify"* — e "rodar mais uma variante" é sempre a mais
>   fácil de justificar. Pior: audiência de visões **conhecidas** (ele mesmo) produz
>   **conformidade**, não autocrítica. **A justificativa escrita pode virar máquina de
>   licenças.**
> - **Sharon et al. (2022)**, meta-análise: em tarefas **complexas**, *accountability* de
>   **resultado** é superior à de processo — **d ≈ −0,48**. Backtest de 8 estratégias é
>   tarefa configural por qualquer definição.
> - **E a trava mais dura que existe — a revisão Stage 1 dos Registered Reports — é a
>   que tem os maiores efeitos medidos:** 43,7% de hipóteses apoiadas contra 96,1% da
>   literatura padrão.
> - **Brodeur et al. (2024)**, 15.992 estatísticas: *"no evidence that pre-registration
>   in itself reduces p-hacking"*. **O que funciona é o plano de análise detalhado**, não
>   o ato de registrar.
>
> **O problema estrutural:** todo benefício demonstrado vem de arranjos com **verificador
> externo**. Auto-registro sem leitor é o caso em que os estudos não acham efeito.
>
> > **Mas ele tem um verificador e talvez não tenha percebido: o repositório é público,
> > com commits datados.** Um pré-registro commitado antes da execução, num histórico que
> > não se reescreve sem rastro, é muito mais perto do `clinicaltrials.gov` do que de uma
> > anotação privada. **Regra concreta que sai daí:** o commit da especificação precisa
> > ser anterior ao commit do resultado, e isso é verificável por qualquer pessoa.
>
> **Recomendação revista: trava, com uma saída nomeada.** Exceder o orçado não se
> resolve com um parágrafo — cria-se um **`v2`**, com especificação e `m` próprios, e o
> `v1` fica de pé com o resultado dele. O custo de exceder deixa de ser escrever e passa
> a ser **admitir que é outro experimento**. E entra uma **camada zero**: o plano de
> análise detalhado, que é o que Brodeur mede como sendo o que funciona — hoje só o
> `hml_puro_v1` o tem de fato.

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
> Sem eventos societários **uma série de preços é inutilizável**: a PETR tem um desdobramento registrado
> em 25/04/2008 (confirmado no endpoint, em primeira mão) e o preço cai de forma ainda não medida (C-01) sem
> nada ter acontecido com a empresa. COTAHIST cru lê isso como um crash. Não havia linha
> nenhuma no plano sobre isso.

1. ~~Coletar o dado perecível da B3.~~ **FEITO em 11/09/2026 — o acervo existe.**
   Carteira do Ibovespa (76 ativos) e eventos societários de **74 emissoras**, todas com
   nome conferido contra o ticker. `dt_captura=2026-09-11`.
   **O acervo ponto-no-tempo do projeto começa nesta data** — vai para
   `limitacoes_declaradas`: não há PIT anterior a 11/09/2026, e backtest antes disso é
   reconstrução, não observação.

   **Duas lacunas declaradas do que foi capturado, e nenhuma é bloqueio:**
   - `GetListedSupplementCompany` devolve uma **janela recente**, não a série completa —
     a PETR veio com 24 proventos, e o endpoint paginado
     (`GetListedCashDividends`) reportou **343** desde 2010. Os desdobramentos parecem ir
     bem mais longe (BBAS com 18, BBDC com 10). **Falta a esteira do histórico longo.**
   - **MBRF sem evento nenhum** — achado A-03 acima.
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
  presume erro. Próximo a vencer: `poupanca_am` em **28/09/2026**, e
  `cofrinho.turbinado_condicao_de_isencao` em **05/10/2026**.

  > **B-01, 11/09/2026 — e este parágrafo estava mentindo.** O aviso só dispara quando
  > `expira` é `dt.date`. **Quatro das 43 constantes datadas tinham a data entre aspas**
  > (`expira: '2026-12-04'`), e YAML entre aspas é **texto** — o `val()` fica mudo, sem
  > erro nenhum.
  >
  > **Duas delas eram exatamente `cdi_aa` e `selic_aa`**: reconferidas em 05/09 e
  > reescritas com aspas **na mesma sessão que as reconferiu**. O parágrafo acima citava
  > as duas como prova de que o mecanismo funciona, enquanto o mecanismo estava desligado
  > **para elas**.
  >
  > A culpa é minha, e o padrão é o de sempre: o arquivo declarava um comportamento que o
  > código não tinha, e os dois concordavam por acidente porque ninguém checou o **tipo**
  > do valor carregado. Corrigido com `test_P70_toda_expira_e_data_e_nunca_texto`, que
  > mede o tipo **depois** do `safe_load` — porque o defeito só existe lá.
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

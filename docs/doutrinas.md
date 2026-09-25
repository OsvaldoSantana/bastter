# As sete doutrinas

*Fonte única desde 25/09/2026. Até ali elas moravam no §2 do `CLAUDE.md`, e o texto veio de
lá sem mudança de conteúdo. O `CLAUDE.md` e o README apontam para cá. Uma cópia em outro
lugar seria a P2 violada por quem a escreveu.*

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
modela**, com a *direção do viés* e a condição em que deixa de importar. ~~Três
hoje: IR na venda de renda variável, periodicidade da custódia do Tesouro, e a
ordem dos portões.~~ *(Corrigido em 23/09: eram onze, e a ordem dos portões estava
consertada desde 05/09.)*

**Desde 23/09 toda entrada diz de quem é o limite** (§5-B.16): `tipo: FISICA` — o mundo
não fornece — ou `tipo: NAO_CONSERTADA` — daria para consertar —, e a segunda só entra com
`o_que_resolveria` e `pendencia` aberta. Uma falha técnica escrita como limitação encerra a
investigação; foi assim que 2026 ficou fora de um pré-registro com o arquivo bom no disco.

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

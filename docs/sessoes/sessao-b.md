# Sessão B — 24/09/2026

Worktree `sessao-b`, só em `alocacao/`. Nada aqui foi escrito em `CLAUDE.md`, `ACHADOS.md`
ou `PENDENCIAS.md`: a numeração **B-n é provisória** e se resolve no merge.

> ⚠ **Colisão de numeração a resolver no merge.** O projeto já tem **B-01 a B-04** (expira
> entre aspas, nome societário da B3, cascata de nomes, `[build-system]`). O
> `achados_ancorados.py` trata `B-2` e `B-02` como códigos **distintos** — a máquina não
> confunde, mas um leitor confunde. Ao promover estes achados, renumerar (ex.: para a
> próxima letra livre) e trocar os comentários de código junto, no mesmo commit.

Itens de uma auditoria externa, já conferidos contra o código antes desta sessão. Cada
um tem o teste que **falha antes e passa depois** — e o "falha antes" foi **medido**, não
argumentado: por mutação, ou rodando o teste novo contra o arquivo de `HEAD`.

## Estado da árvore

- Worktree criada nesta sessão a partir de `main` (`6526669`); ela não existia.
- `alocacao/`: **535 passed, 2 failed**, estável em 3 execuções. `ruff` e `mypy` em zero.
- **As 2 falhas não são desta sessão e não são do código:** `test_estado_real_nao_tem_mais_reserva_empenhada_a_denunciar`
  e `test_reserva_e_zero_e_o_deposito_esta_fora_dela` leem o `alocacao/estado.yaml` real,
  que é privado e gitignored (P-67) e portanto **não existe numa worktree nova**. Na árvore
  principal elas rodam. Não copiei o arquivo.
- `auditoria/`: rodada depois deste documento existir — ver o fim.

---

### B-1 — `estado_io._registro` só reconhecia campo de texto por causa de um `__future__` alheio

**O defeito.** `f.type == "str"`. `dataclasses.fields()` devolve a anotação **crua**: ela só
é a string `"str"` porque `alocacao.py` tem `from __future__ import annotations`. Um
dataclass de um módulo sem o `__future__` tem `f.type is str`, a comparação dá `False`, e
o campo de texto vai para `_num()`, que o reprova com *"'corrente' nao e numero"* — um erro
que não aponta para a causa.

**O conserto.** `typing.get_type_hints(classe)` resolve os dois casos para o tipo real, e a
comparação passa a ser `tipos[f.name] is str`.

**O teste.** `alocacao/test_b1_registro_sem_future.py`, 3 testes. O dataclass é escrito em
disco e **importado de verdade**, sem `__future__`, e o primeiro teste prende essa
pré-condição (sem ela o segundo provaria nada). O terceiro é o espelho: texto em branco
continua reprovado.

**Falha antes:** com o `estado_io.py` de `HEAD`, 2 dos 3 reprovam —
`["contas[0].nome: 'corrente' nao e numero", ...]` e `["c.nome: '  ' nao e numero"]`.

### B-2 — as fixtures de sessão eram protegidas por docstring

**O defeito.** `custos_originais` e `politica_original` (escopo `session`) tinham como
única proteção *"NAO altere"*. É disciplina — o que a P-38 recusa — e no pior lugar: vivem a
suíte inteira e alimentam `custos`/`politica`, a **porta sancionada** de todo teste seguinte.

**O conserto.** No mesmo desenho da guarda existente (detectar, acusar, restaurar no lugar):
a fixture registra impressão e cópia pristina ao nascer (`_vigiar`); a guarda autouse
confere, depois de cada teste que **recebeu** a fixture (direta ou transitivamente, via
`request.fixturenames`), e restaura com `clear()/update()`.

**O que NÃO foi feito, de propósito:** limpar cache ou recarregar entre testes. É a opção
COPIAR SEMPRE que o próprio `conftest.py` rejeita — esconderia a classe do S-02 em vez de
acusá-la. Está escrito no comentário, ao lado do código.

**O teste.** `test_B2_a_guarda_vigia_as_fixtures_de_sessao`, por subprocesso como o da P-38:
quatro testes, dois sujam (`politica_original`, `custos_originais`) e dois herdariam — um
deles pela **cópia** `custos`, que é feita a partir da original.

**Falha antes:** com o `conftest.py` de `HEAD`, a saída é `2 failed, 2 passed` — **os dois
culpados ficam verdes e as duas vítimas ficam vermelhas**, longe da causa. É o cenário
exato que a P-38 descreve. Depois: `4 passed, 2 errors`, só os culpados acusados, com o nome
da fixture na mensagem.

**Limite declarado (herdado):** a impressão é de `repr()`; vale para `dict`/`list`/escalares,
que é do que `C` e `P` são feitos.

### B-3 — a guarda do `carregar` escapava por alias e por `import *`

**O defeito.** `test_usuario_novo` registrava `a.asname or a.name`. Com
`from estado_io import carregar as c`, entrava `"c"`; a chamada `c()` é `ast.Name`, não
`ast.Attribute` — escapava pelas duas pontas. E `from estado_io import *` traz o `carregar`
sem nomeá-lo.

**O conserto.** A lógica saiu para `_nomes_do_carregar(fonte)`, que registra `a.name` (o nome
original) e trata `*` como alcance — sem saber o que entrou, a guarda recusa. O teste que
protege o arquivo passou a chamar essa função sobre o próprio fonte.

**O teste.** `test_B3_a_guarda_do_carregar_ve_alias_e_import_estrela`, 5 fontes sintéticas:
três que têm de ser pegas e **dois controles** (`validar({})`, e `carregar` de `motor` com
alias) — uma guarda que recusasse tudo também passaria nas três primeiras.

**Falha antes:** mutando a função de volta para `asname or name` e `{"carregar"}`, os dois
casos novos reprovam (alias e estrela); os demais passam.

**Achado lateral, não mexido:** a função antiga calculava um conjunto `importados` e nunca o
usava. Saiu junto com a extração, porque ficou sem lugar.

**O que continua fora do alcance (P5):** referência sem chamada (`f = estado_io.carregar`) e
`getattr(estado_io, "carregar")`. A guarda é sobre este arquivo; se um dia precisar ser
sobre o projeto, o instrumento é outro.

### B-4 — `test_P72_aporte_mensal_negativo_continua_bloqueando` não testava o bloqueio

**O defeito.** O teste só chamava `carregar(..., exigir_real=False)` e conferia a lista de
problemas. *"Bloqueando"* é o que a porta faz no modo padrão: levantar `EstadoInvalido`.

**O conserto.** `pytest.raises(EstadoInvalido, match="aporte_mensal = -100")` com
`exigir_real=True`.

**Falha antes:** mutando `carregar()` para não honrar `exigir_real`, o teste antigo passa e
o novo reprova com `DID NOT RAISE EstadoInvalido`.

### B-5 — o teste do E-03 media a bandeira, não quem a honra

**O defeito.** `test_E03_todo_portao_que_declara_ativo_le_o_proprio_interruptor` procurava a
palavra `ativo` em `inspect.getsource(fn)` — a forma do **A-06**.

**O conserto.** Comportamento. `_cenarios_E03()` dá a cada um dos nove portões um cenário em
que ele, **ligado**, reprova algo (G0 com match declarado; G1 com dívida a 10% a.m.; G2 com
reserva zero; G3–G8 sobre o catálogo real). O teste força `ativo: true` e `ativo: false` no
mesmo cenário e exige: ligado reprova alguma coisa (senão o cenário é fraco e desligar não
provaria nada); desligado não reprova nada e deixa passar **todos** os itens. Na fase
`aporte`, "reprovar" é emitir diretiva ou pendência. Portão com `ativo` no YAML e sem cenário
reprova — o décimo portão tem de trazer o seu, que era o propósito de fechar a classe.

**Falha antes — a medição que decide:** troquei no G7 `if not g["ativo"]: return pares, []`
por `if not g["ativo"]: pass`. O teste **de `HEAD` passa** (a palavra está lá). O novo reprova
com `desliga-lo NAO desliga a eliminacao: G7_tese_registrada`.

Os quatro testes E-03 que já mediam comportamento (G3, G4, aridade, inércia) não mudaram.

### B-6 — `motor.simular` × `alocacao.simular_custo`: só medido, nada mudado

**Como foi medido.** As 19 rotas confiáveis do `catalogo.yaml`, espelhadas campo a campo num
`motor.Rota` e simuladas pelas duas funções em três configurações (R$500 × 10 anos, R$500 ×
25, R$5.000 × 25): **57 pares**. Script fora do repositório, no scratchpad da sessão.

**A aritmética do laço é a mesma.** Com o espelho alimentando `adm_aa` com `interno_aa`
(adm + custódia interna), **0 de 57** pares divergem acima de 1e-6.

**Com o espelho honesto (`adm_aa` ← `adm_aa`, que é o que o `motor.Rota` consegue
representar), 9 de 57 divergem** — as três rotas com `custodia_interna_aa = 0,00025`:

| rota | R$500 × 10a | R$500 × 25a | R$5.000 × 25a |
|---|---|---|---|
| `bova11` | +15,1% | +15,7% | **+17,4%** |
| `bova11_xp` | +5,1% | +7,6% | +8,0% |
| `smal11` | +4,3% | +4,2% | +4,3% |

(diferença relativa do custo total; `alocacao` maior em todos). No `bova11` a custódia
interna de 0,025% a.a. é um quarto da adm de 0,10%, daí o peso.

**Todas as divergências, e quais parecem intencionais:**

| # | divergência | intencional? |
|---|---|---|
| 1 | **custódia interna (F-01)**: `simular_custo` usa `interno_aa`; o `motor.Rota` **não tem o campo** | **não parece.** O F-01 foi corrigido só do lado da alocação; `motor.py` não cita o F-01. É o **A-07** (a mesma condição em dois lugares, e o irmão ficou para trás). Hoje inerte: `motor.simular` não tem chamador de produção |
| 2 | `custodia_rv_interpretacao`: `motor.simular` lê do `custos.yaml`; `simular_custo` usa o **default** `"deducao"` da função | **não.** Concordam **por acidente**, porque o YAML diz `deducao`. Ver o candidato abaixo |
| 3 | `anos` fracionário: `motor` faz `range(anos*12)` e levanta `TypeError` com 2,5; `alocacao` faz `int(anos*12)` | não declarado; o `motor` simplesmente nunca recebeu float |
| 4 | custo de entrada ≥ aporte: `motor` **alerta** (K-08.3); `alocacao` faz `min()` **em silêncio** | parcial: no pipeline o G3 barra antes; quem chama `custo_pct_aportado`/`arrasto_anualizado` direto não é avisado |
| 5 | `bruto` e `custodia_absorvida` são parâmetros no `motor`; na alocação o bruto é o CDI fixo e não existe custódia absorvida | **sim** — são cenários da camada de custo (K-04), e o docstring do `motor` os declara |
| 6 | retorno: `(pat, custo, alertas)` × `(pat, custo, aportado)` | sim, contratos de consumidores diferentes |
| 7 | rota de entrada: `motor.Rota.entrada_pct/saida_pct` × `RotaAloc.entrada_extra/saida_extra` | declarado nos docstrings de `custo_entrada_pct` das duas pontas: *"juntar e outra tarefa"* |

**Candidato a achado, não promovido — B-6a.** A única leitura de
`b3.custodia_rv_interpretacao` no projeto é `motor.py:233`, dentro de `motor.simular`, que
**só testes chamam** (mesma situação do `montar_rotas`, P-43). O caminho de produção,
`simular_custo`, **não lê a chave**. Isso tem a forma da **P-77** (*campo que só o teste toca
é campo que o motor não usa*), e um instrumento que conte leituras por arquivo `.py` a veria
como lida — **não conferi** se é o caso do `test_cobertura_yaml_secoes_operacionais` ou do
`chaves_orfas.py`. Se alguém trocar o valor no YAML, o `motor.simular` muda e a alocação não.
**Não promovido** porque falta a pergunta 3 da régua §5-B: não li o laudo da P-43 nem o
inventário do `chaves_orfas.py` para saber se isto já está declarado.

**Sobre a P-43** (decisão dele, aberta): esta medição é o insumo que a opção 2 da P-43 pedia
— *"um teste que confronte os dois onde eles se sobrepõem"*. Ela diz que o confronto teria
achado uma divergência real (F-01) em três rotas, e uma concordância por acidente (a chave).

### B-7 — o P-38 falhava de vez em quando, e não era a guarda

**Observado:** na primeira execução da suíte na worktree,
`test_P38_a_guarda_restaura_para_que_so_o_culpado_falhe` reprovou; nas cinco seguintes, não.

**Medido:** o subprocesso não desligava o cache do pytest. No Windows o rename da pasta de
cache às vezes falha (`WinError 5, Acesso negado`), sai um `PytestCacheWarning`, e a linha de
contagem vira `2 passed, 1 warning, 1 error` — a substring `"2 passed, 1 error"` reprova por
um aviso alheio à guarda. Reproduzido fora da suíte, com o aviso transcrito.

**O conserto:** `-p no:cacheprovider` nos dois subprocessos da P-38 (o do B-2 já nasceu com
ele). Suíte verde em 3 execuções seguidas depois disso.

---

## O que NÃO foi aplicado

**C2, C3 e C5 da auditoria externa — não aplicados, por instrução.** C2 + C3 juntos
reabririam o **J-01** (reserva empenhada não é reserva). Não os li nesta sessão, então não
registro o conteúdo deles aqui — o motivo está nas notas da auditoria.

## Próximo passo

**Decidir a P-43 com a medição do B-6 na mão — é decisão dele, e é a única coisa desta
sessão que precisa de um humano.** As três saídas da P-43 agora têm número:

- **apagar** `montar_rotas` + `motor.simular`: some a única leitura de
  `custodia_rv_interpretacao` — e com ela a chave vira órfã de verdade (o B-6a sai do
  esconderijo e tem de ser resolvido: ou `simular_custo` passa a ler, ou a chave sai);
- **migrar e confrontar**: o confronto já sabe o que acharia (F-01 em 3 rotas, até 17,4%);
- **deixar**: duas simulações que hoje divergem até 17% sem nada as confrontando.

**Por que antes do resto:** as outras seis coisas desta sessão fecharam; esta é a que muda o
que o sistema calcula. **O que destrava:** o B-6a, que depende de qual lado sobrevive.
**O que impede hoje:** só a decisão. **Não exige o desktop.**

A regra da §11.1 conta a favor: esta sessão foi inteira de engenharia de teste. O passo
seguinte a este não pode ser engenharia outra vez.

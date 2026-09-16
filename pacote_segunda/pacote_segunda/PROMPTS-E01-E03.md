# Prompts de Claude Code — E-01, E-02 e E-03

Três remendos pequenos, independentes entre si, **nesta ordem** — E-01 tem número
errado saindo, E-03 produz conclusão errada, E-02 produz mensagem errada.

**O E-02 já vem com o código pronto** (`E02-patch.py` e `test_e02_registros.py`, 13
testes verdes aqui). Se quiser uma vitória rápida antes das outras duas, comece por
ele: é `python E02-patch.py fase0\..\alocacao\tese.py` e rodar a suíte.

**Antes dos dois, o de sempre:**

```powershell
cd C:\Users\osvaldo.junior\Desktop\Bastter
git status --short
py -3.11 -m pytest -q          # tem de estar verde ANTES. Remendo sobre suíte
                               # vermelha não se distingue de remendo que quebrou.
```

**Um commit por prompt.** Se o segundo falhar, o primeiro não volta junto.

---

## Prompt 1 — E-01

```
Correcao de defeito com teste que mede a coisa certa. Arquivo: alocacao/motor.py

CONTEXTO, e confira antes de mudar qualquer coisa
`alocacao/alocacao.py` tem `simular_custo`, que comeca assim:

    if not r.confiavel:
        raise InsumoBloqueado(f"rota {r.id} bloqueada: {'; '.join(r.bloqueios)}")

A docstring dela explica: achado F-02 -- uma rota BLOQUEADA nao simula, porque a
BOVV11, cuja taxa de administracao e NAO_CONFIRMADO, devolvia custo como se a taxa
fosse ZERO e por isso aparecia como a rota MAIS BARATA do catalogo.

`motor.simular` faz o MESMO trabalho e NAO tem essa guarda. O `motor.Rota` TEM a
propriedade `confiavel` e o `montar_rotas` PREENCHE `bloqueios` -- o dado esta la, a
funcao nao olha. Reproduza antes de corrigir:

    C = motor.carregar()
    bovv = [r for r in motor.montar_rotas(C) if "BOVV11" in r.nome][0]
    print(bovv.confiavel)                      # False
    print(motor.simular(bovv, C, 500.0, 20))   # devolve numero, alertas VAZIO

Esperado, medido em 12/09 sobre o instantaneo de 06/09:

    bovv.confiavel = False
    custo  BOVV11 (bloqueada)      = R$1329.68     alertas = []
    custo  "Corretora taxa zero"   = R$1329.68     <- empate EXATO

Empatam porque a taxa desconhecida virou `adm_aa = 0.0` no default do dataclass: o
insumo ausente foi renderizado como zero, e zero e o melhor valor possivel.
Se o seu numero for outro, PARE e me diga -- a base mudou desde 06/09 e a auditoria
inteira precisa ser remedida antes deste remendo.

TAREFA 1 -- a guarda
Em `motor.simular`, antes de qualquer calculo:

    if not r.confiavel:
        raise InsumoBloqueado(f"rota {r.nome} bloqueada: {'; '.join(r.bloqueios)}")

Use `InsumoBloqueado`, que ja existe no modulo. NAO devolva pelo canal `alertas`:
alerta e para problema que ainda deixa o numero valer, e aqui o numero NAO vale.
Escreva no codigo um comentario curto dizendo que isto e o F-02 e que a guarda gemea
mora em `alocacao.simular_custo`.

TAREFA 2 -- a divisao por zero, e ela e outro defeito
`motor.custo_entrada_pct` faz `r.corr_fix/aporte` sem proteger. Com `aporte=0` levanta
ZeroDivisionError. A irma `alocacao.custo_entrada_fixo_pct` devolve `math.inf` no mesmo
caso -- que e a resposta certa: com aporte zero o custo fixo e infinitamente diluido ao
contrario. Iguale ao comportamento da irma.

NAO TENTE unificar as duas funcoes nem os dois dataclasses. `motor.Rota` usa
`entrada_pct`/`saida_pct` e `alocacao.RotaAloc` usa `entrada_extra`/`saida_extra`; sao
classes diferentes e juntar isso e outra tarefa. Apenas deixe um comentario em CADA uma
das duas dizendo que a outra existe e em que diferem.

TESTES -- em alocacao/test_motor.py, e o primeiro e o que importa
 a) GUARDA HONRADA, nao guarda levantada. Ja existe
    `test_rota_com_insumo_nao_confirmado_nao_entra_na_ordenacao`, que afirma
    `not bovv.confiavel`. Ele confere que a BANDEIRA esta levantada; ninguem conferia
    que alguem a HONRA -- foi exatamente assim que este defeito sobreviveu. O teste
    novo tem de afirmar que `motor.simular(rota_bloqueada, ...)` LEVANTA
    InsumoBloqueado. Escreva na docstring essa distincao, com estas palavras:
    "medir a bandeira nao e medir quem a honra".
 b) o numero falso, nomeado: antes da correcao a BOVV11 bloqueada empatava em custo com
    a "Corretora taxa zero". Teste que as duas NAO podem mais ser comparadas, porque a
    bloqueada se recusa a produzir numero.
 c) rota confiavel continua simulando igual: pegue "BOVA11 — corretora zero", rode
    `simular` e compare com o valor de antes da mudanca (rode uma vez, anote, use o
    numero literal no teste com tolerancia de 1e-9). Isto e o instantaneo dourado: a
    correcao nao pode mexer em quem nao estava quebrado.
 d) `custo_entrada_pct(r, 0, b3v)` devolve `math.inf` e NAO levanta.

VERIFICACAO -- nao encerre sem
 - `py -3.11 -m pytest -q` verde, e me diga quantos testes rodaram antes e depois;
 - prove que (a) pega o defeito: reverta a guarda numa copia temporaria, rode so esse
   teste, mostre a falha, desfaca. Guarda que nunca falhou e guarda que ninguem sabe
   se funciona;
 - rode `py -3.11 alocacao/ambiente.py` e confirme o selo do ambiente.

RESTRICOES
 - nao mude `montar_rotas`, nem o catalogo, nem custos.yaml;
 - nao mexa em nenhuma rota que nao esteja bloqueada;
 - se algum teste existente passar a falhar, PARE e me mostre qual -- nao ajuste o
   teste para acomodar a mudanca sem me perguntar.

COMMIT
 Mensagem comecando com "E-01:" e dizendo, em uma linha, que a guarda do F-02 faltava
 no modulo irmao e que o teste novo mede a honra da bandeira, nao a bandeira.
```

---

## Prompt 2 — E-03

```
Correcao de interruptor morto. Arquivo: alocacao/alocacao.py

CONTEXTO, e reproduza antes
`alocacao/politica.yaml` declara `ativo` para os NOVE portoes. Sete funcoes leem o
campo (`if not g["ativo"]: return ...`). `g3_atrito` e `g4_dominancia` NAO leem.

Como os nove estao `true`, arquivo e codigo concordam -- por acidente. Reproduza:

    import copy, alocacao as A
    from motor import carregar as carregar_custos
    C = carregar_custos(); P = A.carregar_politica(); rotas = A.catalogo(C)
    P2 = copy.deepcopy(P); P2["portoes"]["G3_atrito"]["ativo"] = False
    print(len(A.g3_atrito(rotas, C, P, 500.0)[1]))    # 5 rotas fora
    print(len(A.g3_atrito(rotas, C, P2, 500.0)[1]))   # 5 tambem -- desligado nao desliga

ATENCAO ao montar o teste do G4: NAO o alimente com a saida crua de `catalogo(C)`.
No pipeline real o G5 roda ANTES (ordem G6, G0, G1, G2, G5, G3, G7, G8, G4) e tira as
rotas bloqueadas; o G4 calcula arrasto, e arrasto de rota bloqueada LEVANTA
InsumoBloqueado -- corretamente, e o F-02 fazendo o trabalho dele. Passe por
`g6_coerencia_funcao` e `g5_status` antes. Com o pipeline real sao 18 rotas e o G3 tira
4; com o catalogo cru sao 25 e ele tira 5. Os dois numeros estao certos, para entradas
diferentes -- confira qual voce esta medindo antes de comparar.

POR QUE ISSO IMPORTA, e nao e um bug comum
Um interruptor morto nao produz ERRO: produz CONCLUSAO ERRADA sobre o proprio sistema.
No dia em que alguem perguntar "quanto do resultado vem do portao de atrito?" -- uma
analise de sensibilidade, que e para isso que este projeto existe -- a resposta sera
"nada muda", e sera falsa. Nenhum teste pega, porque nada esta quebrado.

A ARMADILHA, e ela e o centro da tarefa
"Desligado" NAO pode ser `return rotas, []`. Os dois portoes fazem duas coisas ao mesmo
tempo: CALCULAM um numero e ELIMINAM com base nele. Desligar o portao desliga a
ELIMINACAO, nunca o calculo -- porque quem vem depois consome o numero.

  g3_atrito(rotas, C, P, aporte) -> (dentro, fora)
      `dentro` e lista de PARES (rota, e). Devolver `rotas` cru entrega rotas nuas
      onde o resto espera pares, e o G4 quebra.
      DESLIGADO = calcula `e` de todas, poe TODAS em `dentro`, `fora` vazia.

  g4_dominancia(pares, C, aporte, P, anos, memo) -> (vivos, dominados, preferencia)
      `vivos` e lista de QUADRAS (rota, e, arrasto_no_horizonte, motivo).
      DESLIGADO = calcula o arrasto de todas, poe TODAS em `vivos` com motivo None,
      `dominados` e `preferencia` vazias. Sim, o arrasto continua sendo calculado --
      e o preco de preservar o contrato, e esta escrito aqui de proposito.

TAREFA
1. Nos dois, ler `ativo` no inicio e implementar o desligado como descrito acima.
2. Comentario curto em cada um: desligar suspende a ELIMINACAO, nao o CALCULO, e o
   motivo (o contrato de tupla de quem consome).

TESTES -- em alocacao/test_alocacao.py
 a) o portao generico, e ele e o que fecha a classe inteira: para CADA portao de
    `politica.yaml` que declara `ativo`, se existir funcao de mesmo nome em minusculas
    (`G3_atrito` -> `g3_atrito`), o codigo-fonte dessa funcao TEM de mencionar "ativo".
    Use `inspect.getsource`. Sem isto, o decimo portao repete o defeito.
 b) G3 desligado nao elimina ninguem: `len(dentro) == len(rotas)` e `fora == []`.
 c) G4 desligado nao elimina ninguem: `len(vivos) == len(pares)`, `dominados == []`,
    `preferencia == []`.
 d) CONTRATO PRESERVADO, e nao pule este: com cada um desligado, as tuplas continuam
    com a mesma aridade de quando ligado -- pares em `dentro`, quadras em `vivos`.
    Este e o teste que pega a correcao ingenua. Medido em 12/09: `dentro` traz tuplas
    de 2 e `vivos` tuplas de 4. Afirme os numeros, nao "e uma tupla".
 e) INSTANTANEO DOURADO: com os nove `ativo: true` (a configuracao real), a saida de
    `alocar()` para um estado fixo tem de ser IDENTICA a de antes da mudanca. Serialize
    o resultado ANTES de mexer no codigo, guarde, compare depois. Se divergir em
    qualquer campo, PARE: a mudanca deveria ser inerte na configuracao padrao.

DEPOIS -- ha um xfail para remover
`auditoria/test_chaves_orfas.py` tem
`test_E03_todo_portao_declarado_le_o_proprio_interruptor` marcado
`@pytest.mark.xfail(strict=True)`. Corrigido o defeito, ele PASSA, e o `strict`
transforma isso em FALHA -- de proposito, para obrigar a limpeza. Remova o decorador e
as seis linhas de comentario acima dele. Se a suite ficar verde sem voce remover nada,
PARE: significa que o teste nao esta medindo o que diz medir.

VERIFICACAO
 - `py -3.11 -m pytest -q` verde, com o xfail JA removido;
 - prove que (a) pega: remova a leitura de `ativo` de um dos dois numa copia temporaria,
   rode so esse teste, mostre a falha, desfaca.

RESTRICOES
 - nao mude politica.yaml;
 - nao mude a ordem dos portoes;
 - nenhuma diferenca de saida com a configuracao padrao -- se houver, e defeito da
   correcao, nao efeito dela.

COMMIT
 Mensagem comecando com "E-03:" e dizendo que dois de nove portoes ignoravam o proprio
 interruptor e que o custo era conclusao errada em analise de sensibilidade, nao erro.
```

---

## Prompt 3 — E-02

> **Este tem código pronto.** `E02-patch.py` aplica o remendo e `test_e02_registros.py`
> traz os 13 testes. O prompt abaixo é para o Claude Code **conferir e integrar**, não
> para reescrever — pedir que ele redescubra o desenho é convidar uma terceira leitura
> de uma regra que já tem duas.

```
Integracao de remendo pronto + conferencia adversarial.
Arquivos: alocacao/tese.py (patch), alocacao/test_e02_registros.py (novo)

CONTEXTO
`tese.carregar_registros` fazia `if not os.path.exists(p): return {}, {}`. G7 e G8
falham para o lado seguro (sem tese, a rota e barrada), entao o sistema nunca ficou
perigoso -- ficou MENTIROSO:

    o que se lia   "nenhuma tese registrada para esta rota"
    o que era      "o teses.yaml nao foi encontrado"

As duas pedem acoes opostas: registre a tese x ache o arquivo, todas as suas teses
sumiram. E `teses.yaml` E o pre-registro: a P4 existe para separar "nunca me
comprometi" de "o registro sumiu".

DECISAO DO USUARIO, 12/09/2026, e ela governa o desenho:
**arquivo ausente e arquivo vazio sao coisas diferentes.** Tres estados:

    AUSENTE    levanta RegistroAusente
    VAZIO      devolve ({}, {}) -- legitimo, e o estado do primeiro dia
    ILEGIVEL   levanta RegistroIlegivel (YAML quebrado nao e "nenhuma tese")

E `permitir_ausente=True` devolve ({}, {}) tambem no ausente: e a U-01 escrita como
parametro -- quem simula usuario novo PEDE a ausencia em vez de recebe-la calado.

TAREFA
1. Copie `E02-patch.py` e `test_e02_registros.py` para `alocacao/`.
2. Rode `py -3.11 E02-patch.py tese.py` a partir de `alocacao/`. O script e idempotente:
   se `RegistroAusente` ja existir no arquivo, ele recusa em vez de aplicar duas vezes.
   Se ele abortar com "regiao de carga nao encontrada", PARE e me diga -- significa que
   o `tese.py` da maquina divergiu do que eu li, e o remendo tem de ser refeito a mao.
3. Apague o `E02-patch.py` depois de aplicado. Ele e um remendo de uma vez, nao
   ferramenta -- deixa-lo no repositorio convida alguem a roda-lo de novo.

CONFERENCIA ADVERSARIAL -- e e por isto que voce esta nesta tarefa
Nao aceite o remendo porque os testes passam. Confira, e me diga o que achar:
 a) `git diff tese.py` -- a mudanca e SO na regiao de carga? Se tocou em
    `validar_tese`, `validar_carrego` ou nas impressoes, algo saiu errado.
 b) todo chamador de `carregar_registros` e `carregar_teses` continua funcionando?
    Sei de: `alocacao._preparar` (linha ~1137), `tese.__main__`, `test_tese.py`.
    O `_preparar` so chama quando `teses is None or carregos is None`, e o
    `test_usuario_novo.py` passa `teses={}` explicito -- entao o caminho do usuario
    novo NAO passa por aqui. CONFIRME isso, nao acredite em mim.
 c) existe algum caminho em que `alocar()` roda sem `teses.yaml` no disco e que agora
    passaria a levantar? Se existir, me mostre ANTES de mudar qualquer coisa.
 d) a suite inteira: `py -3.11 -m pytest -q`. Diga quantos testes antes e depois.

E UMA COISA QUE EU NAO FIZ, e quero sua opiniao
Os outros seis carregadores do projeto (`motor.carregar`, `alocacao.carregar_politica`,
`alocacao.carregar_catalogo`, `corretoras.carregar_instituicoes_cru`,
`estado_io.carregar`) levantam `FileNotFoundError` cru, sem dizer o que se perde. Nao
mexi neles nesta tarefa. Me diga se algum deles tem o mesmo modo de falha do E-02 --
ausencia virando "vazio" em vez de erro -- ou se todos ja falham alto. NAO corrija
agora; so me diga.

RESTRICOES
 - nao mude teses.yaml;
 - nao mude G7 nem G8 -- o comportamento deles ja esta certo, o defeito era a mensagem;
 - se algum teste existente falhar, PARE e me mostre qual.

COMMIT
 Mensagem comecando com "E-02:" dizendo que ausencia de arquivo virava ausencia de
 registro, e que ausente, vazio e ilegivel agora sao tres estados com tres mensagens.
```

---

## O que me mandar de volta

Da execução dos dois, o que muda a sessão seguinte:

1. **quantos testes** antes e depois de cada prompt;
2. a **saída das duas reproduções** — o número da BOVV11 e o `5 / 5` do G3. Se
   qualquer um vier diferente, algum dos oito commits desde 06/09 já mexeu ali, e a
   auditoria inteira precisa ser remedida antes de qualquer outra coisa;
3. do E-02: a resposta do Claude Code sobre os **outros seis carregadores** — se algum
   tem o mesmo modo de falha, ele vira o próximo remendo e eu não preciso adivinhar
   qual;
4. se o **instantâneo dourado do E-03 divergiu** em algum campo — isso é mais
   importante que os dois remendos juntos, porque significa que "desligado" e "ligado"
   nunca foram a mesma coisa e o padrão já estava mentindo.

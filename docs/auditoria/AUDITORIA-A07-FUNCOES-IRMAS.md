# Auditoria A-07 — funções irmãs, e o que elas discordam

**Data:** 12/09/2026 · **Escopo:** `alocacao/` (17 módulos) + `fase0/`
**Status da auditoria: `PARCIAL`, e a limitação é grande — leia a seção 0 antes de tudo.**

A pergunta, herdada do achado A-07:

> quando a **mesma condição** aparece em dois lugares do projeto, os dois a tratam igual?

Não é pergunta de revisão de código. É de auditoria: ninguém está procurando um bug
específico — está procurando **pares que discordam sem que ninguém tenha decidido que
deviam discordar**.

Cinco achados confirmados, **três deles medidos** — e um sexto que eu publiquei e **retirei** (§5), que é o que mais ensinou e não lidos. Um falso positivo meu,
registrado porque a lição dele vale mais que o achado.

---

## 0. A limitação, e ela vem antes dos achados

**Tudo abaixo foi medido sobre o instantâneo de 06/09 que está no meu ambiente, não
sobre o repositório da sua máquina.** Entre os dois há pelo menos oito commits:
P-69/Y-01, P-70, P-71/P-72, campos mortos, B-01, B-02, B-03.

Então: **nenhum achado aqui é `COMPLETO`.** Todos são `NAO_CONFIRMADO` até rodarem
contra os arquivos de verdade — e é por isso que a entrega inclui **duas ferramentas**
em vez de só uma lista. A lista envelhece; a ferramenta você roda de novo.

```powershell
py -3.11 auditoria\pares_irmaos.py alocacao fase0
py -3.11 auditoria\chaves_orfas.py alocacao alocacao\politica.yaml alocacao\custos.yaml alocacao\catalogo.yaml alocacao\instituicoes.yaml
```

---

## 1. E-01 — o `simular` de um módulo recusa a rota bloqueada; o do outro devolve número

**O par:** `alocacao.simular_custo` × `motor.simular`. Mesmo trabalho, módulos
diferentes.

`alocacao.simular_custo` abre assim, e a docstring dele conta a história inteira:

```python
if not r.confiavel:
    raise InsumoBloqueado(f"rota {r.id} bloqueada: {'; '.join(r.bloqueios)}")
```

> *"Achado F-02: uma rota BLOQUEADA não simula. Antes, `bovv11` — cuja taxa de
> administração é NAO_CONFIRMADO — devolvia custo como se a taxa fosse ZERO, o que a
> fazia parecer a rota MAIS BARATA do catálogo."*

**`motor.simular` não tem essa guarda.** E o `motor.Rota` **tem** a propriedade
`confiavel`, e o `montar_rotas` **preenche** `bloqueios`. O dado está lá. A função não
olha.

### Medido, não deduzido

```
rota: BOVV11 — corretora zero
confiavel? False | bloqueios: ['etf.BOVV11: site do gestor bloqueia acesso
                               automatizado  BLOQUEIA: tabela_etf_rv_completa']

motor.simular -> patrimonio R$576.768,55 | custo R$1.329,68 | alertas (nenhum)

ordenacao por custo, com a bloqueada dentro:
   R$     0,00  Cofrinho / RDB 100% CDI (FGC)
   R$ 1.329,68  BOVV11 — corretora zero        <-- bloqueada
   R$ 1.329,68  Corretora taxa zero
   R$ 2.400,52  Safra / Terra — R$4,50 por ordem
```

**R$1.329,68, empatada com a rota que de fato não cobra nada** — porque a taxa
desconhecida virou `adm_aa = 0.0` no default do dataclass. E `alertas` veio **vazio**.

É o K-07/F-02 **literal**, vivo, no módulo irmão. O irmão levanta exceção; este devolve
o número — e o número é o **lisonjeiro**.

### Por que o teste não pegou

`test_rota_com_insumo_nao_confirmado_nao_entra_na_ordenacao` afirma:

```python
assert bovv and not bovv[0].confiavel
```

Ele confere que **a bandeira está levantada**. Ninguém confere que **alguém a honra.**
É o A-06 de novo, em outro arquivo: *a guarda mede o sintoma errado*.

### E-01b — as duas funções de custo também divergem

`custo_entrada_pct` e `custo_saida_pct` existem **nos dois módulos**, com o mesmo nome:

| | `alocacao.py` | `motor.py` |
|---|---|---|
| `aporte == 0` | `math.inf` (protegido) | **`ZeroDivisionError`** |
| campo do extra | `r.entrada_extra` / `r.saida_extra` | `r.entrada_pct` / `r.saida_pct` |
| decomposição A-02 (fixo × percentual) | **sim** | não |

Duas implementações da mesma regra, e o refinamento do A-02 só chegou em uma. **É o
N-01 outra vez** — e note que o A-06 acabou de mostrar que este projeto é vulnerável a
exatamente isso.

**Quem é o vivo hoje:** só `test_motor.py` importa `motor.simular`, e ele simula a
"BOVA11 — corretora zero", que não é bloqueada. Então **hoje nenhum número errado sai
para você.** O defeito é a distância de uma linha: qualquer chamada futura a
`motor.simular` com rota bloqueada recebe o número falso, sem alerta.

---

## 2. E-02 — arquivo ausente virou "nada registrado"

**O par:** `ambiente.declarado` × `tese.carregar_registros`. Os dois carregam um arquivo
**de pré-registro**.

```python
# ambiente.py -- e a docstring é doutrina escrita
def declarado(path=None):
    """... NAO tem valores de reserva: se o arquivo sumir, e erro, porque sem ele
    nao ha nada a conferir."""
    if not os.path.exists(p):
        raise AmbienteIndeclarado(f"{p} nao encontrado. Sem ele o projeto nao sabe
            dizer em que ambiente os resultados pre-registrados foram produzidos —
            e a P-15 volta a estar aberta.")
```

```python
# tese.py
def carregar_registros(path=None, ...):
    p = path or os.path.join(AQUI, "teses.yaml")
    if not os.path.exists(p): return {}, {}          # <-- calado
```

### A consequência exata

G7 e G8 **falham para o lado seguro** — sem tese, a rota vai para `sem` e é barrada.
Isso é bom e vale registrar: **o sistema não fica perigoso.** Fica **mentiroso**.

A mensagem que você lê é:

> `nenhuma tese registrada para esta rota`

quando o fato é:

> `o teses.yaml não foi encontrado`

São duas coisas diferentes, com ações opostas:

| o que o sistema diz | o que você faria |
|---|---|
| "você não registrou tese para esta rota" | registre a tese |
| "o arquivo de teses sumiu" | **ache o arquivo — todas as suas teses sumiram** |

Rodando da pasta errada, com vinte teses registradas, você lê vinte vezes *"nenhuma
tese registrada"* — e a leitura certa era *"seu arquivo de pré-registro desapareceu"*.
**Ausência de arquivo escrita no lugar de ausência de registro:** é a forma do F-02.

E há um agravante de doutrina. `teses.yaml` **é** o pré-registro. A P4 existe para que
não seja possível confundir *"eu nunca me comprometi com uma tese"* com *"o registro
sumiu"* — e é exatamente essa confusão que o `return {}, {}` produz.

### Os oito irmãos, e o mapa completo

| carregador | arquivo ausente | a mensagem diz o que se perde? |
|---|---|---|
| `ambiente.declarado` | `AmbienteIndeclarado` (própria) | **sim** |
| `fatores.carregar_diario` / `hash_fonte` | `FonteAusente` (própria) | **sim** |
| `tese.carregar_registros` | **`return {}, {}`** | **não — e some** |
| `motor.carregar` | `FileNotFoundError` cru | não |
| `alocacao.carregar_politica` | `FileNotFoundError` cru (×2 arquivos) | não |
| `alocacao.carregar_catalogo` | `FileNotFoundError` cru | não |
| `corretoras.carregar_instituicoes_cru` | `FileNotFoundError` cru | não |
| `estado_io.carregar` | `FileNotFoundError` cru | não |

**Três tratamentos para a mesma condição, em oito funções que fazem a mesma coisa.**
Os dois que acertam são os dois que **escreveram a razão na mensagem** — e não é
coincidência: quem escreve a consequência descobre que precisa levantar.

---

## 3. E-03 — o `politica.yaml` declara nove interruptores; dois não estão ligados em nada

Os nove portões declaram `ativo` no YAML. **Sete funções leem o campo. `g3_atrito` e
`g4_dominancia` não.**

```python
if not g["ativo"]: return ...      # G0, G1, G2, G5, G6, G7, G8
```

### Medido

```
rotas no catalogo: 25
G3 ativo=True   -> dentro 20 / fora 5
G3 ativo=False  -> dentro 20 / fora 5
MESMO RESULTADO? True
```

**Desligar o G3 no arquivo não desliga o G3.** Os cinco mesmos ativos continuam
barrados por atrito.

### Por que isso é pior do que parece

Hoje os nove estão `true`, então **o arquivo e o código concordam — por acidente.** É a
frase que este projeto usa para descrever o próprio defeito recorrente, e aqui ela é
literal.

O dia em que isso custa é o dia em que você faz a pergunta certa: *"quanto do resultado
vem do portão de atrito?"* — uma análise de sensibilidade, que é para isso que o sistema
foi construído. Você põe `ativo: false`, roda, e recebe **resultado idêntico**. A
conclusão natural é *"o G3 não muda nada"*, e ela é **falsa**.

**Um interruptor que não faz nada não produz erro. Produz conclusão errada sobre o
próprio sistema** — e essa não aparece em teste nenhum, porque não há nada quebrado.

É P2 (regras como dados) violada em dois de nove consumidores.

---

## 4. E-04 — o `impacto.py` só responde quando você já desconfia

O projeto **já tem** ferramenta de mapa: `quem_le(chave)`, `leituras_de_yaml`,
`leituras_cegas`, `quem_usa_campo`. São boas. E o E-03 passou por baixo delas durante
semanas.

**O motivo é estrutural, não de qualidade:** todas respondem *"quem lê ESTA chave?"* —
você precisa **nomear a chave**. Ninguém ia pensar em perguntar por
`portoes.G3_atrito.ativo`, justamente porque ninguém suspeitava.

Falta a pergunta inversa, que não precisa de suspeita:

> **quais chaves o YAML declara que código nenhum lê?**

Está implementada em `chaves_orfas.py`, nesta entrega.

---

## 5. E-05 — **RETIRADO.** Era falso positivo meu, e é o maior erro desta auditoria

Eu escrevi que `custos.yaml` declara a liquidez do Cofrinho (15 dias na média, 29 no
pior caso), que ninguém a lê, e que o G2 escolhe a rota da reserva sem termo de
liquidez. **As três afirmações estão erradas, e a terceira é a pior.**

### 1. A chave é lida — por outro YAML

```yaml
# catalogo.yaml, linha 146
liquidez_dias: {de_campo: "cofrinho.picpay_garantia_de_limite.liquidez_pior_caso_dias"}
```

Minha ferramenta varria **só os `.py`**. Este projeto põe regra em YAML **de propósito**
e resolve arestas YAML→YAML — e o `impacto.py` já mapeia exatamente essas arestas
(`referencias_do_catalogo`), descritas lá como *"a parte do mapa em que dá para confiar
sem ressalva"*. Eu não a usei.

**Auditar metade do sistema e chamar o resultado de conclusão.** É o A-06 outra vez, do
meu lado da mesa: a ferramenta media o lugar errado, e o verde dela me convenceu.

### 2. O portão de liquidez já existe, e já está declarado

```python
# alocacao.py, g6_coerencia_funcao
lim_d = spec.get("exige_liquidez_dias")
if lim_d is not None and lim_d is not False and r.liquidez_dias > lim_d:
    falhas.append(f"resgate em {r.liquidez_dias}d > exige_liquidez_dias={lim_d}")
```

```yaml
# politica.yaml
LIQUIDEZ:  exige_liquidez_dias: 1
LASTRO:    exige_liquidez_dias: 5
DATADO:    exige_liquidez_dias: 30
```

**Portão, exatamente como você respondeu que devia ser** — e implementado, com a régua
por função, antes desta conversa.

### 3. E ele roda primeiro, e o resultado propaga

`fase_aporte` executa **G6 antes de G0, G1 e G2** (ordem 1 no YAML), e G6 **tira a função
da rota** (`replace(r, funcoes=mantidas)`). Como `rotas_de_liquidez` exige
`"LIQUIDEZ" in r.funcoes`, a rota lenta já não chega ao G2. Medido:

```
rotas com LIQUIDEZ e liquidez_dias > 1:   (nenhuma)

rotas_de_liquidez, antes e depois do G6:  td_reserva 0d · rdb_100 0d · poupanca 0d

G6 tirou a funcao de:
   picpay_cofrinho   perde LASTRO   resgate em 29d > exige_liquidez_dias=5
   lci               perde LASTRO   resgate em 9999d > exige_liquidez_dias=5
   lca               perde DATADO   resgate em 9999d > exige_liquidez_dias=30
```

O cofrinho de 29 dias **nunca teve `LIQUIDEZ`** — declara LASTRO, e perde até isso. As
três rotas da reserva resgatam em **zero dias**. A defesa é dupla e as duas camadas
funcionam.

### O que sobra, e é pequeno

`cofrinho.picpay_garantia_de_limite.liquidez_media_dias = 15` continua sem leitor — e
isso está **certo**: o catálogo usa o **pior caso**, não a média, que é a escolha
conservadora e a que a P6 pede.

### A ferramenta foi corrigida

`lidas_por_yaml()` agora conta `{de:}`, `{de_campo:}`, `{soma:}` e `{de_se_na_lista:}`
como leitura. A lista caiu de 19 para **18** e o falso positivo sumiu — sem derrubar
nenhum dos achados que ficaram de pé.

> **Dois falsos positivos numa auditoria de seis achados.** O primeiro (§7) eu peguei
> lendo. O segundo eu **não peguei** — ele foi para o `CLAUDE.md`, para a fila de
> segunda e para a minha resposta, com uma tabela e uma recomendação. O que o derrubou
> foi ele me responder *"portão"* e eu ir escrever o código que já existia.
>
> A lição não é "conferir mais". É que **o número de leitores de uma chave não é
> mensurável varrendo uma linguagem só**, e eu tratei um resultado parcial como
> conclusão — a P1 inteira, cometida por quem escreveu a P1.

## 6. E-06 — o pré-registro declara as próprias guardas, e nada as executa

Duas chaves órfãs dentro de `estrategias_pre_registradas`:

| chave | valor | leituras |
|---|---|---|
| `greenblatt_v1.verificar_monotonicidade` | `true` | **0** |
| `hml_puro_v1.variantes_permitidas` | `1` | **0** |

A segunda é a mais séria. **`variantes_permitidas: 1` é o limite anti-p-hacking** — o
número de graus de liberdade que você se autorizou antes de olhar o resultado. É
literalmente a razão de existir do pré-registro.

Está declarado. Nada o conta. Nada o compara. Nada falha se você rodar a décima
variante.

**Um pré-registro que declara a própria guarda e não a executa vira um documento sobre
intenções.** A P4 promete impressão digital *e* compromisso; hoje a impressão digital
existe (e funciona), o compromisso é prosa.

Outras sete órfãs de valor numérico/booleano, sem nenhuma leitura, com consequência
menor mas do mesmo tipo:

```
tributacao.fii_isencao_rendimento.cotistas_minimos    = 100    (liga-se à P-77)
tributacao.ir_etf_rf_faixas.valor.prazo_medio_ate     = 180
tributacao.irrf_dedo_duro.e_custo_liquido             = False
b3.vista_total_pct.divergencia.valor_alternativo      = 0.000274
corretora.cobertura_e_penalidade                      = True
corretora.multiplicador_de_confirmacao.N              = 0.0
instituicoes.itau.custos.corretagem_fii               = 0.0
```

---

## 7. O falso positivo, e ele ensina mais que dois achados

`chaves_orfas.py` acusou `portoes.G2_reserva.ajuste_estabilidade.{alta,media,baixa}`
— o multiplicador da reserva por estabilidade de renda. Pareceu grave.

**É falso positivo.** O campo é lido, três vezes:

```python
alocacao.py:754   meses = g["meses_base"] * g["ajuste_estabilidade"][estado.estabilidade_renda]
alocacao.py:1048  f += c["ajuste_estabilidade"][estado.estabilidade_renda]
reserva.py:88     meses_alvo = min(g["meses_base"]*g["ajuste_estabilidade"][e["estabilidade_renda"]] ...
```

O índice é **variável**, não literal. É uma das **375 leituras cegas** que a própria
ferramenta conta e anuncia no cabeçalho antes de imprimir qualquer coisa.

### E a ferramenta melhorou por causa disso

O falso positivo tem uma causa **estrutural**, não de sorte: quando o código alcança as
folhas por variável (`g["ajuste_estabilidade"][estado.estabilidade_renda]`), o nome da
folha **nunca aparece literal em lugar nenhum** — e nenhuma busca por literal a acharia.

A regra que fecha a classe inteira: **quem alcança os filhos por variável lê todos os
filhos.** Se o pai é lido literalmente e logo indexado por não-constante, as folhas dele
não são órfãs — por construção, não por suposição. Está em `pais_varridos()`.

O filtro derrubou **23 candidatos para 19**, e não derrubou nenhum achado: o
`cofrinho.picpay_garantia_de_limite` do E-05 **não aparece no código em nível nenhum**,
nem pai nem folha, então sobrevive ao filtro. Que é o teste certo para um filtro: ele
tem de matar o ruído **e** deixar o sinal em pé.

**O que salvou não foi a ferramenta — foi ler.** E é por isso que os dois scripts
imprimem *"candidatos"* e não *"achados"*, e terminam dizendo que nada ali é achado até
alguém abrir os dois lados. É a P3 aplicada à própria auditoria: **portão, não
pontuação.** Uma ferramenta que despejasse 203 linhas como se fossem defeitos teria me
feito escrever três parágrafos errados sobre a reserva dele.

---

## 8. Uma convenção que existe e ninguém escreveu

Sete impressões digitais, dois cortes de `sha256`:

| corte | funções |
|---|---|
| `[:12]` | `carregar_politica` (`_hash`, `_hash_perfil`), `hash_custos_sem_cache`, `fatores.hash_fonte` |
| `[:16]` | `impressao_de_custos`, `ambiente.impressao`, `tese._hash`, `conftest` |

Parece inconsistência. **Não é:** o corte segue uma regra perfeita —
**hash de ARQUIVO → 12; hash de CONTEÚDO → 16.** Os sete obedecem, sem exceção.

**Só que a regra não está escrita em lugar nenhum.** Então a oitava impressão digital
é cara-ou-coroa, e o dia em que alguém comparar um `[:12]` com um `[:16]` o resultado
é "nunca bate", silenciosamente.

Não é defeito. É **convenção sem dono** — e o barato é escrevê-la agora, enquanto ela
ainda é verdade.

---

## 9. O que fazer, em ordem de valor

| # | o quê | por quê primeiro |
|---|---|---|
| 1 | **E-01**: a guarda `if not r.confiavel: raise` no `motor.simular` | é o F-02 vivo; uma linha; e o teste que falta é o que mede a HONRA da bandeira, não a bandeira |
| 2 | **E-03**: `g3_atrito` e `g4_dominancia` lendo `ativo` | interruptor morto produz conclusão errada, e conclusão errada não aparece em teste |
| 3 | **E-02**: `carregar_registros` levantando `RegistroAusente` | a mensagem certa vale mais que o comportamento, que já é seguro |
| 4 | **E-06**: `variantes_permitidas` contado de verdade | sem isso o pré-registro é intenção |
| 5 | **E-04**: `chaves_orfas.py` na suíte, falhando em órfã nova | P7: auditoria que depende de alguém lembrar não é auditoria |
| 6 | a convenção de corte de hash, escrita | dois minutos, enquanto ainda é verdade |
| — | ~~E-05~~ | **retirado** — falso positivo; o portão já existe e funciona (§5) |

**O 5 é o que fecha o resto.** Os cinco primeiros são defeitos de hoje; o sexto é o que
impede que o sétimo apareça — e ele cabe num teste que roda junto com os outros.


---

## 10. O que ficou de pé como ferramenta, e por quê

| arquivo | o que faz |
|---|---|
| `auditoria/pares_irmaos.py` | levanta pares (condição, tratamento) que discordam dentro do mesmo módulo |
| `auditoria/chaves_orfas.py` | a pergunta inversa do `impacto.py`: chave declarada que ninguém lê |
| `auditoria/test_chaves_orfas.py` | três portões, e um deles reproduz o E-03 |

O teste tem três partes, e a terceira é a que importa:

1. **nenhuma órfã NOVA** — contra uma linha de base de 19, cada uma com o porquê escrito
   ao lado. Fechar uma órfã tem dois caminhos honestos: ou o código passa a lê-la, ou
   ela sai do YAML. Pôr na linha de base é o terceiro, e exige escrever a razão.
2. **a linha de base não guarda chave já resolvida** — o inverso, para que a lista não
   vire depósito. Uma pendência falsa é pior que pendência nenhuma: a próxima pessoa
   acredita nela.
3. **todo portão que declara `ativo` lê `ativo`** — o E-03 direto, sem depender do
   script.

O terceiro está marcado **`xfail(strict=True)`**, e a escolha merece uma linha. O
defeito existe hoje: o teste reprova de verdade. Suíte cronicamente vermelha é suíte que
ninguém lê — foi exatamente assim que o A-06 sobreviveu um dia inteiro. Com `strict`, a
suíte fica **verde com o defeito registrado**, e no instante em que o G3/G4 for corrigido
o teste passa, o `strict` converte isso em **falha**, e alguém é obrigado a vir tirar o
marcador. O defeito fica escrito na suíte, e o conserto não passa despercebido.

Estado hoje: **2 passed, 1 xfailed.**

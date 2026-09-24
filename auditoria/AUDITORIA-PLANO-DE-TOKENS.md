# Auditoria dos três planos de otimização de token

**19/09/2026.** Três documentos auditados: o **Plano 1** (camadas/regras A–M), o
**Plano 2** (AI4SE, 5 pilares) e o **Plano 3** (a crítica ao Plano 2, com Knowledge
Registry e Context Budget).

**Instrumento:** `tiktoken` `cl100k_base` sobre os arquivos reais do repositório em
19/09. É o tokenizador da OpenAI, não o do Claude — **declarado**. As conclusões abaixo
são sobre **erro relativo** e **ordem de grandeza**, que não dependem do tokenizador
exato; qualquer número absoluto aqui carrega ±10%.

---

## 1. O veredito

| | Plano 1 | Plano 2 | Plano 3 |
|---|---|---|---|
| ancoragem no projeto | **alta** — cita seções reais | **alta** — cita P-45/46/53, que existem e dizem o que ele diz | média |
| medição | **nenhuma**, e declara | nenhuma, **não** declara | nenhuma, não declara |
| procedência das afirmações externas | n/a | **zero fontes** para "estudos demonstram" | zero fontes |
| novidade real | 1 item | **nenhuma** — os pilares 1, 2 e 4 são P-46, P-45 e P-53 | **2 itens, e são os melhores dos três** |
| risco de doutrina | **alto** (§4.3, §4.4) | baixo | **alto** (§4.5) |

**A frase que resume:** os três propõem reestruturar 91 mil tokens de arquivo a partir de
uma estimativa que erra **47%** — e o projeto tem uma régua contra exatamente isso.

---

## 2. O que a medição derrubou

### 2.1 O problema é 90% maior do que o Plano 1 calculou

| arquivo | Plano 1 estimou | **medido** | erro |
|---|---|---|---|
| `CLAUDE.md` | ~1.900 linhas, **~26.000 tok** | 2.609 linhas, **50.994 tok** | **+96%** |
| `PENDENCIAS.md` | ~1.750 linhas, **~22.000 tok** | 2.128 linhas, **40.169 tok** | **+83%** |
| `PLANO.md` | "?" | 318 linhas, 5.972 tok | — |
| **leitura inicial** | **~51.000** | **97.135** | **+90%** |

**A razão de 14 tokens/linha está errada: o real é 19,0** (±0,6 nos sete arquivos
medidos), e `chars/token` fica em **2,96** — português com acentuação e tabelas custa
mais que o inglês de onde essa razão vem. **O erro é de 36%, e na direção confortável.**

### 2.2 E a régua foi calibrada num número errado — que é meu

O Plano 1 §0.1 diz, com honestidade, que calibrou os 14 t/linha pela **§11.4 do
`CLAUDE.md`**, que declara `1.112 linhas = ~13k tokens`.

**A §11.4 está errada.** Medido a 19,0 t/linha:

| §11.4 declara | linhas | tokens declarados | **tokens reais** |
|---|---|---|---|
| antes do corte de 06/09 | 2.023 | "~26 mil" | **~38.400** |
| depois do corte | 1.047 | "~13 mil" | **~19.900** |

**Eu escrevi a §11.4 em 06/09 sem escrever a conta.** É o **C-01 na camada do token**:
número plausível em prosa, sem procedência, que sobreviveu treze dias e foi **citado por
um terceiro como fonte de calibração**. O próprio `CLAUDE.md` tem a regra contra isso
desde 12/09: *"achado só entra no `CLAUDE.md` com a conta escrita ou com o
`NAO_CONFIRMADO` explícito."* A §11.4 é mais velha que a regra e nunca foi reconferida.

> **Consequência que vale mais que a correção:** o corte de 06/09 nunca levou o projeto a
> 13k. Ele levou a ~20k. O que se sabia sobre o custo de contexto deste projeto estava
> errado desde o dia em que foi medido, e os três planos herdaram o erro.

### 2.3 O "passo 1, 30 minutos, parte de 40% do ganho" vale 0,4%

O Plano 1 §5 abre com *"criar `SESSION.md` e apagar a seção Ao voltar ao desktop"*,
alegando **−2k/sessão**, e diz que os passos 1+2 entregam ~40% do ganho total.

**Medido: a seção `## Ao voltar ao desktop` tem 25 linhas e 411 tokens.** Ela foi
reescrita em 18/09 justamente para apontar para o `docs/historico/entregas/SEGUNDA-21.md` em vez de duplicá-lo.
**O Plano 1 auditou a versão de antes** — a de ~120 linhas.

Apagá-la rende **0,42%** da leitura inicial. A duplicação que ele aponta é real e vale
consertar por **clareza**; não por token.

### 2.4 O que de fato é grande, medido

| bloco | linhas | tokens | % da leitura inicial |
|---|---|---|---|
| **`CLAUDE.md`, blocos de citação `>`** (retratações e achados) | 1.161 | **25.113** | **25,9%** |
| `CLAUDE.md`, resto | 1.448 | 25.888 | 26,7% |
| `PENDENCIAS.md`, corpo antes de `## Fechadas` | 1.971 | 32.303 | 33,3% |
| `PENDENCIAS.md`, `## Fechadas` | 131 | **7.457** | **7,7%** |
| `PENDENCIAS.md`, `## Ao voltar` | 25 | 411 | 0,4% |

**Metade do `CLAUDE.md` — 49% dos tokens — são blocos `>`.** Essa é a Decisão C do
`PLANO.md` quantificada, e é o único alvo do tamanho que os planos alegam.

**E o `PENDENCIAS.md` tem 71 pendências abertas.** O corpo delas, 32,3k tokens, é o maior
bloco único da leitura inicial — e **nenhum dos três planos o ataca**: os três miram na
`## Fechadas`, que é 4 vezes menor.

---

## 3. ⚠ Nenhum dos três mediu o cache — e nem eu

> ### RETRATAÇÃO desta seção — 19/09/2026, algumas horas depois
>
> Esta seção afirmava: *"Cortar arquivo estável rende ~10% do que o plano calcula"* e
> *"o split em 6 arquivos lidos sob demanda **destrói o cache**"*. **As duas são falsas**,
> e a primeira erra por **20 vezes**.
>
> Fui à fonte: o cache **write** é **2,0x** o token de entrada (TTL 1 h), o **read** é
> 0,1x. **Eu medi o read e concluí sobre o cache.** Como o multiplicador incide sobre
> **todo** o prefixo, cortar X% dele corta X% do custo — **com cache ou sem**. Medido:
> **−25% da leitura de sessão, em qualquer número de turnos.** A "inversão de prioridade"
> que eu anunciei não existe.
>
> E o split não quebra o prefixo (se o estável for lido primeiro): quebra a **janela de
> lookback de 20 blocos**, que é um risco diferente e menor.
>
> **O que sobrevive desta seção:** que nenhum dos três planos mediu o cache — e agora, que
> eu também não tinha. Laudo com as contas em `auditoria/CACHE-E-O-CORTE.md`.

### O texto original, mantido como retratação

### Nenhum dos três menciona *prompt caching*

Este ambiente declara **TTL de cache de 1 hora**. Um prefixo estável de contexto é pago
integral **na primeira** chamada e a ~10% do custo nas seguintes. Isso muda a aritmética
inteira:

| | sem cache | **com cache** |
|---|---|---|
| leitura inicial, 1ª chamada | 97k | 97k |
| leitura inicial, chamadas 2…N | 97k cada | **~9,7k cada** |
| o que custa integral em toda chamada | — | **o que MUDA: resposta, saída de ferramenta, arquivo reescrito** |

**Numa sessão de 20 turnos**, a leitura inicial cacheada custa ~97k + 19×9,7k ≈ **281k**,
contra 1.940k sem cache. O restante do gasto — respostas, `pytest`, arquivos — é **sempre
integral**.

> **Isso não derruba o plano; ele inverte a ORDEM dele.** Cortar arquivo estável rende
> ~10% do que o plano calcula. **Reduzir o que varia por turno rende 100%.** O único
> item dos três planos que ataca o variável é a regra de tamanho de resposta (§2.1 do
> Plano 1) — que ele coloca em segundo lugar e sustenta com um número inventado.

### E há um efeito perverso que nenhum viu

**O split em 6 arquivos "lidos sob demanda" destrói o cache.** Cada combinação diferente
de anexos é um prefixo diferente, e prefixo diferente é *cache miss*. Um projeto com
`CLAUDE.md` estável de 51k em cache pode sair **mais barato** que um com 7k + três anexos
que mudam de sessão para sessão.

Isso é medível e não está medido — **por mim inclusive**. Fica `NAO_CONFIRMADO`, e é a
pergunta que decide se o split vale a pena.

---

## 4. Cinco riscos de doutrina, em ordem de gravidade

### 4.1 `REGUA.md` "sob demanda" é a P7 contra si mesma — e é o pior item dos três planos

Plano 1 §1.1: `REGUA.md` é lido *"sob demanda, mas obrigatória quando a tarefa envolve
medição"*.

**Quem decide se a tarefa envolve medição?** A sessão. Que é exatamente quem erra.

Os treze casos da régua têm **uma forma só**: eu não percebi que estava concluindo além
do que medi. Nos treze, se eu soubesse que estava medindo, teria olhado. **Uma régua que
depende de a sessão reconhecer o próprio erro para ser carregada não tem função.** É a
P7 na letra: *rotina que depende de alguém lembrar não é rotina.*

E o custo é pequeno. A régua inteira cabe em ~2.500 tokens; em cache, ~250 por chamada.
**Tirar o airbag porque ele ocupa espaço no porta-malas.**

### 4.2 Split multiplica o defeito que o projeto mais comete

O projeto mediu **quatro vezes** que duas cópias da mesma regra concordam por acidente
até o dia em que não concordam: **N-01** (duas listas de versões), **A-06** (duas
implementações de `desembrulhar`), **E-08b** (seis cópias de constante sem relógio),
**Y-01/E-09** (chave duplicada apagando a de cima).

Seis arquivos em vez de dois é **mais pares que podem discordar**, e o par
`CLAUDE.md` × `DOUTRINA.md` é o pior possível: prosa contra prosa, sem teste que leia
nenhum dos dois. A regra 12 da §5-B já diz isso — *"prosa e registro não são exceção: são
justamente onde o conflito não estoura"*.

**Split é trade-off medido, não ganho puro.** Se for feito, precisa de um teste que meça
a divergência — e nenhum dos três planos propõe um.

### 4.3 Regra A/B/C troca uma instrução dele por economia, e admite

Plano 1 §2.1 propõe resposta ≤400 palavras (≤150 na entrega) e escreve: *"Isso é o
oposto do que o `CLAUDE.md` §6 pede hoje (análise profunda, nunca superficial)."*

A §6 é **instrução permanente do Osvaldo**, não preferência minha. Um plano não revoga
instrução do dono do projeto por argumento de custo — isso é decisão dele.

**Mas há um núcleo correto, e ele não é sobre tamanho: é sobre DESTINO.** Laudo no chat é
desperdício porque laudo é arquivo. A regra honesta seria: *análise longa vai para
arquivo; a resposta diz o que mudou, onde está, o que quebrou e o próximo passo.* Isso
**não reduz profundidade** — muda onde ela mora, e é o que a §11.5 já apontava sem
formalizar.

### 4.4 O número que sustenta a regra mais importante é inventado

*"Respostas longas minhas: 25–35% do gasto"* (Plano 1 §0.3) cita a §11.5. **A §11.5 não
tem número** — ela diz *"são o maior item isolado"*, e ordinal não é percentual.

A tabela §0.3 inteira é inferência apresentada em formato de medição. **Seis linhas com
percentuais, zero medições.** É a forma exata do defeito recorrente da casa, e o Plano 1
a declara na §6.2 — o que o torna honesto, não correto.

### 4.5 O Plano 3 empurra o projeto para o que ele declarou não ser

> **RETRATADA em 21/09/2026 — a metade que cita DeMiguel.** DeMiguel, Garlappi & Uppal
> medem **otimização de pesos** (média-variância contra 1/N) e não dizem nada sobre
> **ordenar** ativos. O plano de ML do projeto (`pesquisa-e-plano-ml-1.md` §1) declara
> *"o modelo responde qual primeiro, nunca quanto"* — fora do alcance da fonte que eu usei
> contra ele. É a régua §5-B.5: a cláusula citada não cobre o item. **O que sobrevive:**
> um plano de custo de token não é a porta para mudar escopo — e o ML não entrou por ela,
> entrou por pré-registro próprio (`docs/aprendizado/preregistro-ml-v1.md`). Detalhe em
> `auditoria/AUDITORIA-PREREGISTRO-ML-V1.md` §0. O texto original fica abaixo, riscado
> pela nota e não apagado.


Plano 3 propõe `BRONZE → SILVER → GOLD → FEATURE STORE → BACKTEST ENGINE`, com "variáveis
para ML".

**`CLAUDE.md` §1, primeira linha do "O que este sistema NÃO é":** *"Não é um otimizador.
DeMiguel, Garlappi & Uppal (2009): 14 modelos de otimização, nenhum bateu 1/N fora da
amostra."*

Feature store para ML não é otimização de token — é **mudança de escopo**, e o escopo tem
evidência contra. Bronze→Silver→Gold já está declarado; **Feature Store e ML não**, e
entrar por um plano de custo seria a pior porta possível.

---

## 5. O Plano 2 está correto e é redundante — e a redundância é o achado

Conferi as três pendências que ele cita. **Existem, e dizem o que ele diz:**

| pilar do Plano 2 | pendência | criada em | gatilho declarado |
|---|---|---|---|
| 1 · subagentes para fonte primária | **P-46** | 06/09 | *"a primeira sessão da Fase 0"* |
| 2 · divisão Cowork × Claude Code | **P-45** | 06/09 | *"terça, depois do push"* |
| 4 · Parquet + DuckDB | **P-53** | 06/09 | *"ao criar `data/bronze/`"* |

**Eu ia acusar o Plano 2 de inventar numeração. Medi e estava errado** — ele está melhor
ancorado que o Plano 1.

> **Mas é por isso que ele não entrega nada: os três pilares são decisões de 06/09 com
> gatilho escrito, e OS TRÊS GATILHOS VENCERAM.** O push foi em 18/09 (P-45). A Fase 0
> começou em 11/09 (P-46). `data/bronze/` existe desde 11/09 (P-53). **Treze dias, três
> gatilhos vencidos, nenhum puxado.**
>
> **Esse é o achado que os três planos não têm, e ele não é sobre token: é P7.** O
> problema não é falta de plano — é que o projeto tem as decisões registradas com gatilho
> e **nada as dispara**. Escrever um quarto plano sobre as mesmas três decisões é a
> quarta cópia da mesma regra: N-01 na camada do planejamento.

E o Plano 2 tem um defeito de casa próprio: *"estudos demonstram"*, *"pesquisas
recentes"*, *"reduz substancialmente as taxas de erro"* — **zero referências**. O projeto
tem o precedente em `auditoria/PREREGISTRO-EVIDENCIA.md`: 25 fontes, e a evidência
**contrariou** a minha própria recomendação. Afirmação sem fonte que soa técnica é pior
que ausência, porque passa.

---

## 6. O que os três trazem de real — quatro itens, e dois são bons

**(a) `## Fechadas` para arquivo separado.** 7.457 tokens medidos, 7,7% da leitura
inicial. Consulta é `grep` por número, não leitura. **Aceito, e é o único item de
tamanho com número verificado.**

**(b) Knowledge Registry / schema como dado — o melhor item dos três, e é novo.**
Plano 3 propõe `schemas/cotahist.yaml` com as posições dos campos, em vez de reler o
leiaute.

Isso **não é** economia de token: é a **P2 aplicada a leiaute**. E ele tem um alvo
concreto **hoje**: o `fase0/calendario.py` que escrevi nesta sessão carrega
`POS_DATA = (2, 10)`, `POS_MODREF = (52, 56)`, `LARGURA = 245` **em código**, com a
procedência num comentário. São constantes de fonte externa em Python — exatamente o que
a P2 proíbe, e eu acabei de fazer.

**(c) Context Manifest por tarefa.** É a forma executável da P-46, melhor que "use
subagente": declara o que entra, o que é opcional e o que é **proibido** entrar. O
`excluded: data/**` é um `.gitignore` para contexto, e o projeto já aprendeu, com a
P-98, que a lista tem de ser medida e não lembrada.

**(d) Traceback em vez de prosa.** Já é a prática, funciona, e vale escrever: o
`pytest` como júri vale também para a **entrada** do prompt, não só para o veredito.

**Descartado: telemetria de contexto (Plano 3, pilar 6).** Boa em princípio e
**inexequível daqui**: eu não meço tokens da minha própria sessão, não vejo cache hit, e
não tenho como saber quantos tokens "foram usados" contra "foram enviados". O `CER` e o
`R` que ele propõe não têm instrumento. Registrar como desejo, não como pilar.

---

## 7. O que eu faria, em ordem de token medido

| # | ação | ganho medido | risco |
|---|---|---|---|
| 1 | **Corrigir a §11.4** com os números reais e marcar a retratação | 0 tok, **mas todo plano futuro deixa de herdar erro de 47%** | nenhum |
| 2 | `## Fechadas` → `FECHADAS.md` | **−7.457** (−7,7%) | nenhum |
| 3 | **Os 25.113 tok de bloco `>` do `CLAUDE.md` → `ACHADOS.md`** (é a Decisão C, já no `PLANO.md`) | **−25.113** (−25,9%) | **médio** — ver §4.2; precisa de teste de divergência |
| 4 | **Medir se o split derruba o cache** antes de fazer o item 3 | decide se 2 e 3 valem | — |
| 5 | Laudo vai para arquivo; a resposta diz o que mudou, onde, o que quebrou, o próximo passo | ataca o **variável**, que é o que não cacheia | **baixo**, e não mexe na §6 |
| 6 | `docs/schemas/cotahist-v02.yaml` e o `calendario.py` lendo dele | 0 tok, **fecha a P2 num lugar que eu violei hoje** | nenhum |
| 7 | **Puxar P-45, P-46 e P-53** — gatilhos vencidos há 13 dias | o que os três planos prometem | nenhum |
| — | ~~`SESSION.md` + apagar "Ao voltar"~~ | **−411 (0,4%)** — vale por clareza, não por token | nenhum |
| — | ~~`REGUA.md` sob demanda~~ | **recusado**, §4.1 | — |
| — | ~~Feature Store / ML~~ | recusado em 19/09, **recusa retratada em 21/09** (§4.5) | — |

**O item 1 vem primeiro porque é o mais barato e o mais caro de não fazer:** enquanto a
§11.4 disser 13k, todo plano que a citar vai errar por 47% na direção confortável — e
este ciclo acabou de acontecer.

---

## 8. O que esta auditoria NÃO mediu (P5)

1. **O tokenizador é o `cl100k_base`, da OpenAI**, não o do Claude. Conclusões sobre erro
   relativo e ordem de grandeza sobrevivem; números absolutos carregam ±10%.
2. **Não medi o efeito do cache.** A §3 é aritmética sobre um TTL declarado pelo ambiente,
   não uma medição de faturamento. **É a pergunta que decide os itens 2 e 3 da §7**, e
   está aberta.
3. **Não medi resposta minha nem saída de ferramenta.** A afirmação de que o variável
   domina o gasto com cache ligado é dedução, não observação — não tenho o instrumento
   (§6, item descartado).
4. **Não li o `ACHADOS.md`.** Todo item que mande "mover para o `ACHADOS.md`" supõe um
   arquivo que eu nunca abri. Mesma limitação declarada em 19/09.
5. **Não medi `PLANO.md`, `teses.yaml`, `catalogo.yaml` nem `instituicoes.yaml`** além do
   tamanho bruto, e não sei quais entram na leitura de uma sessão típica — o que é, ele
   mesmo, um buraco: **o projeto não declara em nenhum lugar qual é o conjunto de leitura
   inicial.** Sem isso, "leitura inicial = 97k" é a minha suposição de três arquivos.

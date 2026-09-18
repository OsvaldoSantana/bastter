# PLANO.md — onde queremos chegar, o que já existe, e o que vem antes de quê

*Criado em 18/09/2026, por pergunta dele: **"você tem um arquivo de planejamento onde
você tem listado tudo que foi feito e tudo que precisa ser feito e onde queremos
chegar?"*** A resposta honesta era **não**.

O projeto tinha três registros e nenhum plano. `CLAUDE.md` mistura doutrina com história
e cresceu para 2.270 linhas; `PENDENCIAS.md` tem **64 entradas sem ordem entre si**;
`ACHADOS.md` guarda o passado. **Nenhum dos três responde "onde queremos chegar"**, e a
"fila" da §7 do `CLAUDE.md` é um retrato do próximo passo, não um plano — foi reescrita
quatro vezes e ficou desatualizada em três delas.

> **A divisão de trabalho, daqui em diante.** Este arquivo tem **destino e ordem**.
> `PENDENCIAS.md` tem o detalhe de cada item. `ACHADOS.md` tem a história. `CLAUDE.md` tem
> a doutrina. Se este arquivo discordar dos outros sobre **o que vem primeiro**, ele ganha
> — e a divergência é um defeito a corrigir, não um empate a tolerar.

---

## 1. Onde queremos chegar

**Decisão dele, 18/09/2026**, ao retirar do `CLAUDE.md` as duas linhas que diziam que o
sistema *"recusa-se a nomear empresas"*:

> *"o projeto talvez hoje não consiga fazer isso, mas o objetivo dele é tomar decisões
> sobre alocação de investimento — por isso as linhas foram tiradas."*

**E ele está certo contra mim.** Eu tinha escrito a incapacidade de hoje como se fosse
identidade permanente. **É a P6 virada contra o próprio projeto:** ausência de régua não é
critério de exclusão — nem de um ativo, nem do escopo. O certo é declarar o **objetivo**
(o que se quer fazer) e declarar a **limitação** (o que ainda não se sabe fazer), que é a
P5. "Não faz" vira prazo; "recusa-se" vira doutrina, e doutrina não se revoga com dado.

### O destino, em uma frase

> A cada aporte, o sistema diz **quanto** vai **para onde** — e, quando a régua existir,
> **para qual papel** —, com **procedência em cada número**: de onde ele veio, quem
> escolheu a regra, e o que aconteceria se a escolha fosse outra.

### A limitação declarada de hoje (P5)

O sistema decide **classe e rota**. Ele ainda **não decide papel**: não há régua de
seleção de empresa, porque ela depende do dado da Fase 0 e do backtest que a Fase 0
destrava. Isso é uma **lacuna com caminho**, não uma recusa — e o caminho está na §3.

### Os quatro marcos, e o que separa um do outro

| marco | o sistema passa a | estado |
|---|---|---|
| **M1 · decidir o aporte** | dizer quanto entra, para qual classe e por qual rota, com custo e imposto medidos e nove portões nomeados | **pronto**, e ocioso até a reserva existir |
| **M2 · decidir com dado próprio** | ler balanço e evento societário do acervo dele, sem depender de terceiro nem de tela | **em andamento** — B3 e CVM no disco; falta ler |
| **M3 · decidir o papel** | aplicar uma régua de empresa **pré-registrada** e medida, com o corte que a família de testes exige | **bloqueado** em M2 |
| **M4 · fazer isso sozinho** | rodar a captura semanal sem ninguém lembrar, e acusar a falha em vez de a esconder | **desenhado**, não executado (P7 / §11.6) |

**A ordem não é negociável e a razão é de dado, não de gosto:** M3 sem M2 é backtest sobre
o dado de outra pessoa, que é o desconto D3 da literatura (*look-ahead* contábil) entrando
pela porta da frente. E M4 sem M2 é automatizar uma esteira que ainda não existe.

---

## 2. O que já está feito

### As camadas do blueprint

| camada | estado |
|---|---|
| 0 · pipeline de dados | **em andamento** — ver o detalhe abaixo |
| 1 · motor de custo | completa |
| 2 · portões G0–G8 | completa, com a ordem como **dado** (`politica.yaml`), não como código |
| 3 · alocação alvo | completa |
| 4 · custo de discordar | completa |
| 5 · motor de aporte | completa, ociosa até a reserva fechar |
| 6 · catálogo de campos (blocos A–M) | **especificada**; os regimes de solvência e de instituição financeira escritos, a execução depende da camada 0 |
| 7 · backtest | **pré-registrado e agora com mecanismo** — ver abaixo |
| — · fatores NEFIN | completa, fora do plano original |
| — · fase de reserva | completa, fora do plano original |

### A camada 0, em detalhe — é onde o projeto está

| fonte | estado |
|---|---|
| **B3 — eventos societários** | **completo.** 74/74 emissoras, ~8 mil proventos, `dt_captura=2026-09-11`. Acervo bruto com sha256 |
| **B3 — silver** | **escrito.** `refinar.py`, 9.272 linhas, `factor` desambiguado (C-01), `data_ex` derivada por calendário real de pregão |
| **COTAHIST** | **1 ano (2023)**, e já virou produto: a série **ajustada** de 2023, medida contra 293 datas-ex (C-02). Um ano não é backtest — e a janela isolada tem **duas bordas**, ver passo 3 |
| **CVM — DFP/ITR** | **baixada em 18/09.** 33 ZIPs: DFP 2010–2026, ITR 2011–2026. Falta o manifesto com sha256 |
| **CVM — cadastro** | **obtido em 03/09**, status COMPLETO. É por ele que a ponte ticker↔CD_CVM se faz |
| **bitemporalidade** | desenhada (`DESENHO-PIPELINE.md`), **não implementada** |

### O aparato de pré-registro (fechado em 18/09)

As quatro decisões de 13/09 estão implementadas. O que era documento sobre intenções virou
mecanismo: o `m` é **calculado** dos dois lados, o `pesquisa_id` é **derivado** do dado, o
corte sai da **distribuição medida** e não da tabela, e divergência de veredito **bloqueia**
até estar escrita. Isso não aproxima nenhum marco sozinho — **mas é o que torna o M3
defensável quando ele chegar.** Ver `auditoria/ROMANO-WOLF.md`.

### O estado financeiro real (é dado de um usuário e nunca bloqueia desenvolvimento)

Fase A — formar a reserva, até **~mai/2031**. Reserva **zero** por decisão declarada dele;
o aporte deixou de ser zero em 10/09. O M-01 mediu que o **destino** do aporte move 3 meses
e o **valor** move 33 — e nenhum portão decide o segundo.

---

## 3. O que falta, em ordem — e o que cada passo destrava

### ~~1 · Baixar a CVM~~ — **FEITO em 18/09/2026.** 33 ZIPs, acervo completo

> Manifesto gravado em 18/09 — **39 arquivos, 716 MB** —, mas no lugar errado
> (`data/`, que o git ignora) e por defeito meu; corrigido para `docs/acervo/cvm/`, e
> precisa ser regravado uma vez. E o download
> rendeu um achado que muda o desenho da rotina semanal — ver `auditoria/CVM-PRIMEIRO-RETRATO.md`
> e a **P-91**: comparar por hash de arquivo declara reapresentação onde houve só
> reordenação de linhas.

<details><summary>o registro do passo, como estava</summary>

### 1 · Baixar a CVM · **escolhido em 18/09** · ⚙ desktop

**O que destrava:** o M2 inteiro. Sem DFP/ITR não há balanço, sem balanço não há bloco C,
sem bloco C não há portão de exclusão, e sem portão não há backtest — é o único item da
lista de que os outros três marcos dependem.

**Por que agora e não depois:** os arquivos de 2021–2026 são **reescritos toda semana** com
reapresentações, sob o mesmo nome. Cada semana sem retrato é uma rodada de correções que
deixou de ser observável — e é exatamente o número **entregue na época** que um backtest
honesto precisa, porque a decisão de compra teria sido tomada com ele.

**Como:** `auditoria/CVM-DOWNLOAD-MANUAL.md`, revisado em 18/09. 12 ZIPs com prazo (6 DFP +
6 ITR), `data\bronze\cvm\`, **sem descompactar**, e o `sha256` + a hora do download
registrados junto — *um retrato sem hash não é um retrato: é um arquivo*.

**O que impede hoje:** nada além de estar na máquina. `dados.cvm.gov.br` me responde
`ROBOTS_DISALLOWED` e eu não contorno.

</details>

### ~~2 · A série ajustada de 2023~~ — **FEITO em 18/09/2026**

```
O DEGRAU DO DIA DA DATA EX -- 293 casos
  retorno BRUTO     media -1.6265%   t  -9.88
  retorno AJUSTADO  media -0.0360%   t  -0.29
  CONTROLE: 86.736 pares sem evento; divergencia maxima 1.0e-27 (arredondamento)
```

`fase0/ajustar.py` + 32 testes (8 contra o acervo). Duas mutações presas na suíte: data-ex
deslocada devolve o degrau inteiro (−1,63%, t −9,88) **e cria um falso na véspera**
(+1,91%, t +11,20); fator invertido **dobra** o degrau (−3,16%, t −12,98). *Nenhuma
leitura errada de fator encolhe um degrau* — é isso que faz da medição uma prova.

> **CORREÇÃO DA MINHA ESPECIFICAÇÃO, e ela é o ponto desta rodada.** Eu escrevi aqui que
> o teste *"responde se o degrau desaparece quando o fator é aplicado; se não desaparecer,
> o C-01 está errado"*. **A população não dá esse poder ao teste.** Das 293 datas-ex de
> 2023, **292 são provento em dinheiro e apenas UMA é evento de quantidade** (a bonificação
> da FLRY). O C-01 é sobre o campo `factor` dos eventos de **quantidade** — e a leitura
> percentual continua apoiada na **distribuição** dos 180 valores mais **um** caso de preço,
> que é exatamente o que já era.
>
> **O que a medição DE FATO confirmou, e não é pouco — são três coisas, em 293 casos:**
> a **data-ex derivada do calendário observado** (que tinha 1 caso em 16/09), o **sentido
> do fator** (multiplicador de preço, e não o inverso) e a **fórmula do fator de provento**.
>
> A régua §5-B pegou isto antes da publicação, do lado de lá: *a conclusão que eu ia
> imprimir é mais larga que a medição*. O relatório do módulo agora imprime as duas
> metades separadas — o que confirma e o que não confirma. Ver `auditoria/C02-O-DEGRAU-MEDIDO.md`.

<details><summary>a especificação, como estava</summary>

### 2 · A série ajustada de 2023 — o primeiro produto ponta a ponta · ⚙ Claude Code

**O que destrava:** a confiança no pipeline, antes de investir mais dado nele. Junta as duas
metades que nunca se encontraram — o silver de eventos e o COTAHIST 2023 — e responde se o
degrau de preço **desaparece** quando o fator é aplicado. Se não desaparecer, o C-01 está
errado e é melhor descobrir com um ano do que com vinte.

**O que impede hoje:** nada. Os dois insumos já estão no disco.

**A especificação, para a sessão do Claude Code abrir com ela na mão:**

| | |
|---|---|
| **entra** | `fase0/refinar.py` (silver de eventos, 9.272 linhas) + `data\…\COTAHIST_A2023.TXT` (557 MB, layout de 245 posições) |
| **sai** | `fase0/ajustar.py` + `test_ajustar.py`, e uma série ajustada por ticker para 2023 |
| **a regra** | fator acumulado **de trás para frente**: o preço de antes da data-ex é multiplicado pelo produto dos fatores de todos os eventos posteriores. `data_ex` já é o **primeiro dia SEM** o direito (corrigido em 16/09) |
| **o teste que decide** | pegar os eventos de 2023 com fator calculado e medir o retorno do dia da data-ex **antes e depois** do ajuste. Se o degrau não encolher, o C-01 está errado |
| **o controle** | dias **sem** evento não podem mudar de retorno. Se mudarem, o ajuste vazou para onde não devia |
| **o que NÃO fazer** | não recalcular `factor`; não inventar preço para `SEM_PRECO`; não ajustar linha com `fator_status != CALCULADO` — essas entram na série com a lacuna declarada, nunca corrigidas por interpolação |
| **o parser do COTAHIST JÁ EXISTE** | `fase0/calendario.py` tem `TIPO_COTACAO = "01"`, `POS_DATA`, e a varredura que abre ZIP **ou** TXT. **Extrair de lá, nunca reescrever** — duas leituras do mesmo layout de 245 posições concordam por acidente até o dia em que não concordam, e foi exatamente isso o A-06. O que falta é só acrescentar as posições de papel e de fechamento, no mesmo lugar |

> **Um aviso para quem abrir esta especificação:** o degrau de preço **não é prova sozinho**.
> Um provento em dinheiro também derruba o preço na data-ex, e a queda medida é a soma dos
> dois efeitos. O teste tem de separar: use os eventos de **quantidade** (desdobramento,
> grupamento, bonificação) para medir o ajuste de fator, e trate os de **caixa** à parte —
> senão o resultado mistura duas coisas e "o degrau encolheu" deixa de significar algo.

**Por que o teste decide alguma coisa:** o C-01 foi fechado por **assinatura aritmética**
(onze valores caindo em razões canônicas), não por preço. Esta é a primeira vez que a
regra encosta em preço de verdade — e um ano de COTAHIST é amostra suficiente para
derrubá-la se ela estiver errada.

</details>

### 3 · COTAHIST 2021 a 2025 — **contíguos**, e não só 2021 e 2025 · ⚙ desktop

**O que destrava:** duas coisas ao mesmo tempo, e a segunda não estava na proposta.

**(a) A corroboração por preço sai de 1 para ~51 eventos de quantidade.** É o único
caminho para o C-01 deixar de se apoiar em distribuição mais um caso — e 2025 traz 31
dos eventos, incluindo os grandes, que o preço resolve com folga.

**(b) A CONTIGUIDADE elimina bordas, e isso não é detalhe.** O ajuste é retroativo: ele
reescala o passado a partir do **fim** da série, então todo evento cuja data-ex caia
depois do fim da janela **não entra**, e desloca o nível *sem produzir degrau visível* —
é a P-94, e ela é invisível no controle e na suíte.

| acervo | blocos | **bordas** |
|---|---|---|
| só 2023 | 1 | 2 |
| 2021 + 2023 + 2025 | **3** | **6** |
| **2021…2025** | **1** | **2** |

**Baixar os cinco anos custa o mesmo trabalho manual que baixar dois** — é a mesma página,
três cliques a mais, ~350 MB — e **elimina quatro das seis bordas.** Anos salteados não
formam série: o ajuste retroativo só atravessa um bloco contíguo, e 2022 e 2024 são a
emenda. **2024 em particular é o que fecha a borda de 2023**, o bloco que já está medido.

**O que impede hoje:** nada além de estar na máquina.

### 4 · Bitemporalidade — `dt_captura` × `DT_REFER` · ⚙ Claude Code

**O que destrava:** o direito de dizer que o backtest não vaza futuro. Está desenhada e não
existe em código; o acervo já guarda `dt_captura` no caminho, então o custo é de leitura, não
de coleta.

### 5 · O bloco C sobre dado real — o primeiro portão que olha empresa

**O que destrava:** o M3. É o primeiro momento em que o sistema aplica régua a uma empresa,
e ele é de **exclusão**, não de ordenação — a evidência local sustenta excluir as ruins e
não sustenta ordenar as boas (`criterio_nao_e_previsao`).

**O que impede hoje:** o passo 1.

### 6 · A rotina semanal sem humano · ⚙ decisão + Claude Code

**O que destrava:** o M4, e a honestidade do acervo. Enquanto o download for manual, a P7
manda **declarar a limitação** — e ela está declarada. GitHub Actions em repositório público
é a escolha registrada (§11.6).

### Fora da fila, mas com custo em toda sessão

- **`CLAUDE.md` tem 2.270 linhas / ~40 mil tokens**, e `PENDENCIAS.md` outros ~29 mil. A
  §11.4 registrou em 06/09 que o corte tinha levado o custo por sessão a ~13 mil; hoje é
  **cinco vezes isso**. A doutrina da retratação declarou a troca e nomeou a saída: *"se um
  dia o custo virar impeditivo, a saída é mover o histórico para um arquivo de achados — não
  deletá-lo."* **Virou.** Alvo: `CLAUDE.md` ≤ 600 linhas de instrução; todo bloco datado vai
  para `ACHADOS.md`.
- **Trabalho de repositório pertence ao Claude Code.** A tabela §11.2 já diz isso e as
  rodadas de 16 e 18/09 foram feitas da nuvem mesmo assim — pagando transferência de arquivo
  e sem alcançar o git. A nuvem é para **pesquisa com fonte primária, subagentes e
  processamento de dado pesado**.
- **16 commits nunca empurrados.** O `PREREGISTRO-EVIDENCIA.md` conclui que todo benefício
  medido de pré-registro vem de arranjo com **verificador externo**, e que o que salva este
  desenho é o repositório público com commits datados. **Sem push, esse verificador não
  existe.**

---

## 4. Os bloqueios reais, e quantos são

| # | bloqueio | classe | o que o levanta |
|---|---|---|---|
| 1 | ~~CVM não baixada~~ — **levantado em 18/09** | — | o acervo existe; falta o manifesto |
| 2 | COTAHIST cobre 1 ano, e a janela isolada tem duas bordas | `BLOQUEIA_O_SISTEMA` | baixar **2021 a 2025 contíguos** — ver passo 3 |
| 3 | bitemporalidade não implementada | `BLOQUEIA_O_SISTEMA` | passo 3 |
| 4 | a segunda esteira — nota explicativa e IPE — **nunca orçada** (X-01) | `BLOQUEIA_O_SISTEMA` | precisa de decisão de escopo antes de código |
| 5 | ~~duas cópias do projeto na máquina (P-87)~~ — **apagada por ele em 18/09** | — | resolvido |

**E um defeito do próprio registro:** das 64 entradas do `PENDENCIAS.md`, **só 34 declaram
classe** — a regra que exige dono, gatilho e classe é de 06/09, e as 30 anteriores nunca
foram classificadas. *Pendência sem classe é desabafo*, pela regra dele.

---

## 5. Decisões que são dele, e o plano não anda sem elas

| # | decisão | por que é dele | custo de adiar |
|---|---|---|---|
| ~~A~~ | ~~destino da cópia do OneDrive~~ | — | **decidida em 18/09: apagada** |
| B | a segunda esteira (X-01) entra no escopo, e quando? | é orçamento de esforço, não questão técnica | o M3 nasce cobrindo só parte do universo, e sem isso escrito |
| C | `CLAUDE.md` cortado agora ou depois do passo 1? | é o tempo dele que paga os dois lados | ~40 mil tokens por sessão, toda sessão |
| D | nível ou tendência nos blocos de balanço (P-16/P-63) | é escolha de método, não de dado | trava o bloco C no passo 4 |

---

## 6. O que NÃO está no plano, de propósito

- **Otimizador de carteira.** DeMiguel, Garlappi & Uppal: 14 modelos, nenhum bateu 1/N fora
  da amostra. Regra declarada e testável, nunca ótimo derivado.
- **Robô que opera.** O sistema decide e registra; a ordem é dele.
- **Mais engenharia de qualidade sem destravar nada.** A regra da §11.1 é permanente: o
  próximo passo proposto não pode ser de engenharia duas vezes seguidas, e engenharia entra
  quando **destrava**, não quando é o que sobrou de mais fácil.

---

## 7. Como este arquivo se mantém honesto

1. **Um passo concluído sai da §3 e entra na §2, com a data.** A fila não guarda item pronto
   — isso já aconteceu três vezes neste projeto e fila desatualizada parece confiável.
2. **Todo passo declara o que destrava e o que o impede hoje.** Sem as duas coisas é lista
   de desejos.
3. **Todo passo declara onde roda:** ⚙ desktop (PowerShell, git, download, dado bruto) ou
   nuvem (pesquisa, subagente, processamento).
4. **Este arquivo não guarda história.** Quando um passo fecha, a medição vai para
   `auditoria/` e a narrativa para `ACHADOS.md`. Se ele começar a crescer como o
   `CLAUDE.md`, está errado.

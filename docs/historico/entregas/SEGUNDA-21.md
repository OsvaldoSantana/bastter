> VENCIDO — executado em 21/09/2026 (b54787b). Não é instrução vigente.

# Segunda, 21/09/2026 — o roteiro

> **ROTEIRO VENCIDO.** Os Passos 1 a 3 foram feitos em 21/09; o Passo 3 é o commit `b54787b`.
> O que sobrou não mora mais aqui: a fila é o `PLANO.md`, as pendências são o `PENDENCIAS.md`.
> Este arquivo fica como registro do dia, não como instrução.

*Escrito em 19/09 com o seu PC desligado e **reescrito em 21/09 depois da auditoria do que
você rodou ao ligar o PC.** Este arquivo é a lista completa: seguindo de cima para baixo,
nada fica para trás.*

---

## O que a auditoria de 21/09 encontrou

Você rodou os Passos 2 e 4 **sem o Passo 1**. Nenhum arquivo da entrega chegou à pasta, e a
prova está no próprio transcript: os mesmos 3 testes vermelhos de 18/09, `auditoria` com 4
testes em vez de 42, e `nothing to commit`. **O `nothing to commit` foi sorte:** a mensagem
de commit dizia *"P-06 fechada"* sobre um repositório em que o manifesto acabara de contar
**42 arquivos sem origem**.

E a auditoria achou **três defeitos meus** que o Passo 1 teria posto no repositório:

| | o que era | como ficou |
|---|---|---|
| **P-109** | o `calendario.py` de 19/09 reprovava **19 testes** seus (`test_ajustar`, `test_calendario`) que eu não tinha rodado — e o roteiro dizia que arquivo sem header era *aceito*, o que o código não fazia | sintéticos com header real; medido sobre clone do `origin/main` |
| **P-110** | a `auditoria` reprovava **2** no repositório real: 13 `.md` antigos sem papel, e o teto de órfãos calibrado na árvore errada | classificados; teto re-medido no lugar certo |
| **P-108** | o `Out-File -Encoding utf8` **que eu mandei você usar** grava BOM no PowerShell 5.1, e o leitor descartava **todas** as origens em silêncio | leitor tolerante + `origem.csv` escrito com as 41 linhas |

Regra nova na régua: **§5-B.15 — suíte verde na árvore de entrega não é suíte verde no
repositório.**

---

## Passo 1 · ~~Copiar os arquivos~~ **FEITO por mim em 21/09, direto na pasta**

Com a sua autorização, gravei os arquivos em `Desktop\Bastter` com trava de data: nenhum
arquivo que você tivesse mexido desde a minha leitura seria sobrescrito. A lista, com
sha256, está no `ENTREGA-19-09.md`. **Conferência opcional:**

```powershell
cd C:\Users\osvaldo.junior\Desktop\Bastter
Get-FileHash CLAUDE.md, PENDENCIAS.md, ACHADOS.md, fase0\calendario.py -Algorithm SHA256 |
  Format-Table Hash, Path -AutoSize
```

**Os dois apêndices já estão colados no `ACHADOS.md`** (54 KB → 124 KB). Os arquivos
temporários não existem mais.

---

## Passo 2 · ~~Ficar verde~~ **FEITO em 21/09 — commit `c6ccf2a`, empurrado**

> **Medido no transcript dele:** `fase0` 212 passed · `alocacao` 516 passed · `auditoria`
> 41 passed + 1 skipped (`tiktoken` ausente, esperado) · `ruff` limpo · manifesto
> `P-06: 1 de 42` · o `origin/main` voltou a ficar verde. Os três avisos de marca `slow`
> viraram a P-111, fechada no mesmo dia. **Próximo: Passo 3.**

<details><summary>O roteiro original deste passo</summary>


```powershell
cd C:\Users\osvaldo.junior\Desktop\Bastter
py -3.11 -m pytest fase0 -q
py -3.11 -m pytest alocacao -q
py -3.11 -m pytest auditoria -q
py -3.11 -m ruff check alocacao fase0 auditoria
```

**O que esperar**, medido sobre clone do `origin/main` com a entrega aplicada:

| suíte | no clone | na sua máquina deve dar |
|---|---|---|
| `fase0` | 196 passed, 16 skipped | **mais passed e menos skipped** — os skips são o acervo, que só existe aí |
| `auditoria` | 42 passed | 42 passed |
| `alocacao` | 514 passed, **2 failed** | **516 passed** — os 2 leem `estado.yaml`, que nunca vai ao git (P-62) |
| `ruff` | limpo | limpo |

**Se qualquer coisa fora disso aparecer, me mande a saída e não commite.** Foi commitando
por cima do vermelho que a P-102 chegou ao `origin`.

### Com as três verdes: o manifesto de hoje, e o commit

```powershell
py -3.11 fase0\manifesto_cvm.py --manifesto data\bronze\b3
```

Deve dizer **`P-06: 1 de 42`** — só o `COTAHIST_A2023.ZIP` de 04/09, na raiz de
`data\bronze\b3`, cuja origem só você sabe (P-97, Passo 4). Vai aparecer também um
**AVISO de manifesto do mesmo dia com conteúdo diferente**: é o retrato de hoje cedo, sem
as origens, sendo **preservado** com o hash no nome. É o comportamento certo, não erro.

```powershell
git add -A
git status
git commit -m "P-102/P-99/P-105/P-106 e C-03; P-108 a P-110 da auditoria de 21/09; ACHADOS com a Decisao C; origem do COTAHIST declarada (41 de 42)"
git push
```

**Leia o `git status` antes do commit.** Tem de aparecer código, testes, docs e
`docs\acervo\b3\` — **nenhum arquivo de `data\`** e **nenhum `estado.yaml`**. A guarda
P-98 reprova se um ZIP escapar, mas olhar custa dez segundos.

---

</details>

---

## Passo 3 · ~~O PRÓXIMO PASSO do projeto~~ **FEITO em 21/09 — commit `b54787b`** (ver `docs/auditoria/C02-JANELA-2021-2025.md`)

### `ajustar.py` sobre 2021–2025 contíguos

**Classe: `BLOQUEIA_O_SISTEMA`.** É o passo 3 do `PLANO.md`, e ele estava esperando
arquivo. **Agora tem 41 anos no disco e o leitor enxerga todos.**

**Por que este, e não a quebra de moeda que eu achei sexta:** a janela 2021–2025 está
**inteira em `R$`**. A quebra do Real é de 04/07/1994. **O C-03 não bloqueia este passo** —
e dizer isso vale mais do que empilhar a P-101 na frente por ser o achado mais novo.

**O que ele destrava, medido:**

| | hoje | com 2021–2025 |
|---|---|---|
| eventos de quantidade corroborados por preço (C-01) | **1** | **~51** |
| bordas da janela (P-94) | 6, se anos salteados | **2** |
| anos de série ajustada | 1 (2023) | **5 contíguos** |

⚙ **É trabalho de Claude Code**, na sua máquina: 5,6 GB de arquivo e a suíte inteira ao
lado. Daqui eu não alcanço.

**Prompt para o Claude Code:**

> Leia `CLAUDE.md`, `PLANO.md` §3 (passo 3) e `docs/auditoria/C02-O-DEGRAU-MEDIDO.md`.
> Estenda `fase0/ajustar.py` para a janela contígua **2021 a 2025**, usando
> `fase0/calendario.py` (não reescreva a descoberta de arquivo nem o parser — N-01).
> Meça o degrau bruto e ajustado por ano, com o controle dos pares sem evento ao lado,
> como o C-02 fez para 2023. Escreva testes antes de rodar. Instantâneo dourado do 2023
> **antes de mexer**: `pregoes()` tem de continuar em 248 pregões,
> sha256 `e4a9d81d3d6d4cb8810b86322de3d08415f7a3fed23b32d923b4291c13bd551c`.
> Não commite sem as três suítes verdes.

---

## Passo 4 · O que sobrou, em ordem, para quando o passo 3 fechar

| # | o que | classe | por que não é agora |
|---|---|---|---|
| 1 | **P-101** — reexpressar a moeda pré-04/07/1994 | `BLOQUEIA_O_SISTEMA` | só morde se a janela passar de 1994. A de hoje não passa |
| 2 | **P-100** — rebaixar o `COTAHIST_A2026.ZIP` (chegou truncado) | `DECISAO_DE_DESENHO` | é o ano corrente; o backtest termina em período fechado. **Desde 21/09 bloqueia a família ML** (P-107) |
| 3 | **P-97** — a origem do `COTAHIST_A2023.ZIP` de 04/09 | `DADO_DE_UM_USUARIO` | **veja a nota abaixo, tem resposta nova** |
| 4 | ~~Decisão C~~ — **executada em 19/09**, ver §5 | — | — |
| 5 | P-17, P-18 | — | contas de dado, sem prazo |
| **6** | **P-107 — corrigir o `preregistro-ml-v1.md` ANTES de commitá-lo** | `DECISAO_DE_DESENHO` | **tem janela:** ele vale a partir do commit. Leia `auditoria\AUDITORIA-PREREGISTRO-ML-V1.md` §5 (sete linhas), decida, e só então baixe os dois documentos de ML do projeto *Bastter* no claude.ai para `docs\aprendizado\` e faça o commit |

**P-97 — só falta você.** O `COTAHIST_A2023.ZIP` da raiz de `data\bronze\b3` (de 04/09)
tem o **mesmo sha256** (`ad1603788d78…`) do que está em `cotahist\` desde 18/09 — medido no
manifesto de hoje. É o mesmo arquivo, byte a byte. As 41 origens de `cotahist\` já estão
declaradas (P-108); este é o único que fica contando, **porque eu não sei de onde ele veio**
e a regra do `origem.csv` é não inventar procedência. Duas saídas, as duas suas:

- você lembra de onde veio → acrescente a linha no `docs\acervo\b3\origem.csv`;
- é duplicata e não importa de onde veio → mova-o para fora do acervo. **Antes, confira**
  que nenhum módulo lê a raiz: `Select-String -Path fase0\*.py -Pattern 'bronze.*b3'`. Os
  que eu conheço leem `cotahist\`; o `ajustar.py` eu não li inteiro.

**Decisão C — EXECUTADA em 19/09, com o seu critério.** Você deu a régua: *otimização sem
perder contexto*. A resposta **não** foi cortar 25% por percentual — foi triar por
**função**: a regra que impede a repetição fica, a narrativa que a explica sai.

| | |
|---|---|
| saíram | 962 linhas, **20.085 tokens** — os 30 achados de 06/09 a 18/09, que moravam na §7 |
| ficou | um **índice**: uma linha por achado, com a regra que ele deixou |
| medido | `CLAUDE.md` **−17.816 tok (−33,7%)**; leitura de sessão de 100.059 → **83.101** |
| **contexto perdido** | **zero, e é medido: 26/26 achados com endereço** |

**O argumento que decidiu não foi token.** A §10 do `CLAUDE.md` diz desde 06/09 que achado
mora no `ACHADOS.md` — *"não estão aqui de propósito"* — e a §7 acumulou trinta depois
disso. O corte foi fazer o arquivo **cumprir a própria regra**, não inventar uma nova.

E a guarda nova pegou o próprio índice **duas vezes** no dia em que nasceu: a tabela estava
dentro de um blockquote (invisível ao instrumento) e `| **A-03 / A-04** |` deixava o A-04
sem endereço. **Índice tem de ser legível pela máquina, senão é lista de nomes.**

---

## Passo 5 · Duas coisas com data

- **`macro.poupanca_am` vence 28/09/2026** — sete dias depois de segunda. `motor.val()`
  avisa em stderr. Reconferir na fonte, não presumir erro: em 05/09 o `cdi_aa` e o
  `selic_aa` estavam **certos**, era só prazo vencido.
- **A CVM reescreve DFP/ITR toda semana.** O acervo é de 18/09. Cada semana sem captura é
  uma rodada de reapresentações que deixou de ser observável, e **não volta**. Está
  declarado em `politica.yaml → limitacoes_declaradas.captura_da_cvm_e_manual_e_o_dado_e_perecivel`,
  e a saída é GitHub Actions (P-57). Enquanto não existir, é manual — e a P7 diz que isso
  tem de estar escrito, não lembrado. Está.

---

## Uma coisa que eu não consegui fazer e você precisa saber

**Não atualizei o `ACHADOS.md`.** Ele nunca passou pelo container — eu nunca o li — e
manter atualizado um arquivo que não li seria escrever sobre o que eu suponho que ele diz.
É o defeito recorrente deste projeto na forma mais boba.

O bloco pronto está em **`ACHADOS-19-09-PARA-COLAR.md`**, também no chat: cole o conteúdo
dele no `ACHADOS.md` e apague o arquivo temporário. Se preferir, me mande o `ACHADOS.md`
na próxima sessão e eu o mantenho direito daí em diante.

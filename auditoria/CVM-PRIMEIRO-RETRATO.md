# O primeiro retrato da CVM — e a reapresentação que não houve

**18/09/2026.** Os arquivos chegaram: **39 arquivos, 716 MB** — DFP 2010–2026 (17 anos)
e ITR 2011–2026 (16 anos), mais **6 cópias duplicadas** de 2012, 2019 e 2024. O acervo está
**completo** na faixa que a CVM publica, e a cauda congelada veio junto — ela não tinha
prazo e não custou nada esperar.

E o acervo trouxe, sem ninguém planejar, **o par que o projeto precisava desde 06/09.**

---

## 1. Três anos foram baixados duas vezes, com 14 dias de intervalo

2012, 2019 e 2024 (DFP e ITR) existem em duas cópias: a de **04/09/2026** e a de
**18/09/2026**, esta última como `... (1).zip`. **Não apague nenhuma das duas.** São a
única evidência ponto-no-tempo que o projeto tem, e o `.gitignore` já mantém `data\` fora
do repositório.

| par | sha256 do ZIP | veredito |
|---|---|---|
| DFP **2012** | idêntico | `IDENTICO` |
| DFP **2019** | idêntico | `IDENTICO` |
| ITR **2012** | idêntico | `IDENTICO` |
| ITR **2019** | idêntico | `IDENTICO` |
| **DFP 2024** | **mudou** | `REORDENADO` — e não é o que parece |
| **ITR 2024** | **mudou** | `REORDENADO` — idem |

**Seis pares, dois com hash diferente, e ZERO reapresentações.** Os dois que mudaram são
exatamente os do ano em curso na janela de reapresentação; os quatro congelados não se
mexeram, como a política da CVM promete.

---

## 2. O sha256 mudou e o dado não

No `dfp_cia_aberta_2024.zip`, **dois** dos dezoito CSVs diferem. Neles:

- mesmo número de linhas (94.517 e 59.744);
- mesmo número de bytes;
- **zero linhas exclusivas de qualquer um dos lados** — `sorted(a) == sorted(b)`;
- 8 e 12 linhas fora de posição, respectivamente.

**A CVM regerou o arquivo e a ordem das linhas mudou. Não houve reapresentação.**

> **A estratégia registrada no `CLAUDE.md` §11.6 — *"baixar, comparar, guardar o delta"* —
> teria declarado uma reapresentação aqui.** E comitaria ruído no git toda semana, para
> sempre, enquanto o evento de verdade ficaria escondido no meio dele.
>
> É o **F-02 espelhado**: lá a ausência virava zero; aqui **o ruído vira evento**. O mesmo
> parágrafo do §11.6 já avisava do lado oposto — *"ausência de mudança precisa ser
> afirmada, nunca inferida da ausência de erro"* — e o que faltava era a outra metade:
> **presença de mudança também precisa ser afirmada, nunca inferida da mudança de hash.**

O **ITR 2024** repete o padrão com mais força: **quatro** CSVs alterados, **128 linhas
fora de posição em ~2,2 milhões**, e de novo `sorted(a) == sorted(b)` em todos.

### A taxa medida, e ela recalibra a urgência

Somando os dois anos: **seis CSVs com bytes diferentes, e nenhuma linha trocada.**

| | medido |
|---|---|
| pares com hash diferente | 2 de 6 |
| CSVs com bytes diferentes | 6 |
| linhas efetivamente reapresentadas | **0** |
| falso positivo se a comparação fosse por hash | **100%** |

> Isso **não** derruba a doutrina — reapresentação existe e destrói o retrato de época. O
> que ele diz é que, **na única janela observada, o sinal era todo ruído**, e uma rotina
> que compara por hash teria comitado dois "deltas" que não são deltas.

**O que esta medição NÃO mede (§5-B, pergunta 1):** dois anos, uma janela de 14 dias,
entre 04/09 e 18/09/2026. Não é taxa anual, não cobre 2021–2023, 2025 e 2026 — que só têm
um retrato —, e não diz nada sobre quanto uma reapresentação real muda quando ela vem.

---

## 3. O que foi entregue

`fase0/manifesto_cvm.py`, com 10 testes sem rede e sem os 700 MB do acervo, e **duas
operações que respondem perguntas diferentes** — porque confundi-las foi o defeito:

| operação | responde | não responde |
|---|---|---|
| `--manifesto` | *qual* arquivo eu tenho (sha256, bytes, `dt_captura`) | se mudou |
| `--comparar` | *a CVM reapresentou alguma coisa?* | qual arquivo é qual |

Quatro vereditos nomeados, nunca um booleano: `IDENTICO`, `REORDENADO`,
`REAPRESENTADO`, `ESTRUTURA`. Só `REAPRESENTADO` sai com código ≠ 0 — é o único que
exige ação humana, e é o insumo que a rotina semanal automática (P7) vai consumir.

Rodado sobre o acervo real:

```
dfp_cia_aberta_2024.zip  x  (1).zip   -> REORDENADO
    BPA_ind_2024.csv: 8 fora de posicao em 94.517 linhas
    DVA_ind_2024.csv: 12 fora de posicao em 59.744 linhas
dfp_cia_aberta_2019.zip  x  (1).zip   -> IDENTICO
```

---

## 4. O que falta, e é de você

```powershell
cd $HOME\Desktop\Bastter
Remove-Item -Recurse data\bronze\cvm\manifesto    # o lugar errado, ignorado pelo git
py -3.11 fase0\manifesto_cvm.py --manifesto data\bronze\cvm
```

Agora grava em **`docs\acervo\cvm\dt_captura=AAAA-MM-DD.csv`**, com sha256, tamanho e
data dos 39 arquivos. **Até entrar num commit, o acervo é um conjunto de arquivos e não um
retrato datado** — e `dfp_cia_aberta_2022.zip` de hoje não é o de semana que vem, sob o
mesmo nome.

Confira que ele entrou, porque foi exatamente isso que faltou da primeira vez:

```powershell
git status --short docs\acervo
```

> **CORREÇÃO DE 18/09, e o defeito é meu — no mesmo dia em que o instrumento nasceu.**
>
> Esta seção dizia que *"o manifesto entra no repositório (o `data\` não entra, o
> manifesto sim)"*. **A primeira versão gravava em `data\bronze\cvm\manifesto\`, e o
> `.gitignore` ignora `data/` inteiro na linha 12.** O arquivo foi gravado, o
> `git commit` passou com 20 arquivos, e o manifesto **não entrou** — justamente o
> arquivo cujo único propósito é ser verificável por terceiro.
>
> É o defeito recorrente do projeto na forma mais crua: **o documento declarava um
> comportamento que o sistema não tinha, e os dois concordaram porque ninguém leu a saída
> do `git commit`.** O que denunciou foi ler a lista de `create mode` do commit dele e
> não achar o manifesto lá.
>
> **Corrigido:** o destino padrão passou a ser `docs/acervo/cvm/`, achado pela raiz do
> repositório (`pyproject.toml`), e `gravar()` **recusa** qualquer caminho que passe por
> `data/`, com o motivo na mensagem. Três testes novos, um deles provado por mutação.
>
> O manifesto de 18/09 está em `data\bronze\cvm\manifesto\` e precisa ser regravado —
> ver a §4.

---

## 5. Declarado de propósito (P5)

- **A normalização é por linha inteira.** Se a CVM mudar o separador, a codificação ou o
  espaçamento, tudo vira `REAPRESENTADO` — falso positivo na direção conservadora, que é
  a direção certa para um alarme, e está escrito.
- **`dfp_cia_aberta_2026.zip` tem 218 KB** contra ~13 MB dos outros anos, e
  `itr_cia_aberta_2026.zip` tem 19,6 MB contra ~32 MB. É **coerente com ano em curso** e
  não foi conferido contra a página do conjunto: `OBSERVADO`, não `COMPLETO`.
- **Três anos foram descompactados na pasta** (2012, 2019, 2024). Inofensivo — o
  `test_p82_copia_do_projeto.py` mede o índice do git, não o disco —, mas o ZIP continua
  sendo a evidência, e é dele que o manifesto tira o hash.

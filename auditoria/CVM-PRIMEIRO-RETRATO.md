# O primeiro retrato da CVM — e a reapresentação que não houve

**18/09/2026.** Os arquivos chegaram: **33 ZIPs**, DFP 2010–2026 (17 anos) e ITR
2011–2026 (16 anos), em `data\bronze\cvm\`. O acervo está **completo** na faixa que a CVM
publica, e a cauda congelada veio junto — ela não tinha prazo e não custou nada esperar.

E o acervo trouxe, sem ninguém planejar, **o par que o projeto precisava desde 06/09.**

---

## 1. Três anos foram baixados duas vezes, com 14 dias de intervalo

2012, 2019 e 2024 (DFP e ITR) existem em duas cópias: a de **04/09/2026** e a de
**18/09/2026**, esta última como `... (1).zip`. **Não apague nenhuma das duas.** São a
única evidência ponto-no-tempo que o projeto tem, e o `.gitignore` já mantém `data\` fora
do repositório.

| par | sha256 do ZIP | veredito |
|---|---|---|
| DFP **2019** | **idêntico** nos 14 dias | `IDENTICO` |
| DFP **2024** | **mudou** | `REORDENADO` — e não é o que parece |

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

E o 2019 foi a testemunha do outro lado: **byte a byte idêntico**, exatamente como a
política da CVM promete para os anos fora da janela de reapresentação. A promessa deixou
de ser citada e passou a ser **medida**.

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
py -3.11 fase0\manifesto_cvm.py --manifesto data\bronze\cvm
```

Grava `data\bronze\cvm\manifesto\dt_captura=AAAA-MM-DD.csv` com sha256, tamanho e data de
cada um dos 33 ZIPs. **Até isso rodar, o acervo é um conjunto de arquivos e não um retrato
datado** — e `dfp_cia_aberta_2022.zip` de hoje não é o de semana que vem, sob o mesmo nome.

O manifesto é pequeno e **entra no repositório** (o `data\` não entra, o manifesto sim):
é ele que torna a procedência verificável por terceiro sem os 700 MB.

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

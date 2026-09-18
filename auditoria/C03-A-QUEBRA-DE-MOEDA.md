# C-03 — quatro moedas no acervo, e só uma delas deixou quebra no arquivo

**Medido em 18/09/2026**, sobre os ZIPs recém-baixados, em primeira mão. Instrumento:
razão `PREULT(depois)/PREULT(antes)` do **mesmo `CODNEG`**, só mercado à vista
(`TPMERC=010`), nos pregões que cercam cada troca de moeda — o mesmo método dos 86.736
pares do C-02.

---

## 1. O que apareceu, e ninguém tinha olhado

O acervo passou de 1 ano para 41. A série agora começa em **02/01/1986** e atravessa
**seis planos econômicos**. O campo `MOEDA` (posições 53–56) declara a unidade, e ele
muda **dentro do mesmo arquivo anual**:

| ano | faixa de cada moeda | plano |
|---|---|---|
| 1986 | `CR$` 02/01→27/02 · `CZ$` 04/03→30/12 | Cruzado — CR$ 1.000 = CZ$ 1 |
| 1989 | `CZ$` 02/01→13/01 · `NCZ$` 18/01→28/12 | Verão — CZ$ 1.000 = NCZ$ 1 |
| 1990 | `NCZ$` 02/01→13/03 · `CR$` 19/03→28/12 | Collor — paridade |
| 1993 | `CR$` o ano inteiro | **Cruzeiro Real, 1.000:1 — a MOEDA não distingue** |
| 1994 | `CR$` 03/01→30/06 · `R$` 04/07→29/12 | **Real — CR$ 2.750 = R$ 1** |

> **O 1993 é o caso que assusta antes de medir:** em 01/08/1993 o cruzeiro virou cruzeiro
> real a 1.000:1, e **as duas moedas se abreviam `CR$`**. Um campo que anuncia a unidade e
> não distingue duas unidades separadas por três casas decimais é pior que um campo
> ausente — ele afirma continuidade onde pode não haver.

## 2. A medição, e ela derruba a suposição óbvia nos dois sentidos

```
razão preço(depois)/preço(antes), mesmo ticker, mercado à vista

  1994  30/06 -> 04/07  (Real)          pares=136   mediana=0,36443   p10=0,343  p90=0,396
  1994  controle 29->30/06              pares=251   mediana=1,01064   p10=0,945  p90=1,096
  1993  30/07 -> 02/08  (Cruzeiro Real) pares=182   mediana=0,99792   p10=0,936  p90=1,038
  1986  27/02 -> 04/03  (Cruzado)       pares=274   mediana=1,19729   p10=1,000  p90=1,477
  1989  13/01 -> 18/01  (Verão)         pares=198   mediana=0,96774   p10=0,866  p90=1,032
  1990  13/03 -> 19/03  (Collor)        pares=  2   mediana=0,71416
```

**Três das quatro trocas NÃO produzem quebra.** 1986, 1989 e 1993 ficam dentro do ruído
diário — a B3 **já reexpressou** o ano inteiro numa unidade só, e o `MOEDA` ali é rótulo
histórico, não fator. A suposição natural — *"toda troca de moeda é uma quebra"* — está
errada em 3 de 4 casos, e só a medição diz qual.

**A do Real é real, e é grande.** 0,36443 contra um controle de 1,01064 no dia anterior,
com a dispersão apertada (p10–p90 de 0,343 a 0,396, a mesma largura do ruído de um dia
comum). O inverso é **2,744** — consistente com os **2,750** do Plano Real, com o resto
sendo variação de um pregão.

> **O que isso diz sobre a escala do arquivo, e é um achado embutido:** a conversão legal
> é CR$ 2.750 = R$ 1, e a quebra medida é de **2,750**, não de 2.750. As três casas de
> diferença significam que a coluna de preço antes de 04/07/1994 está em **milhares** de
> cruzeiros reais. `NAO_CONFIRMADO` — é a leitura que reconcilia a lei com a medição, e
> não há documento da B3 em mãos que a confirme.

**O 1990 não foi medido, e a ausência é a informação.** Só **2** tickers têm preço nos
dois lados de 13→19/03/1990: o Plano Collor bloqueou os haveres e o mercado praticamente
parou. Dois pares não decidem nada — fica `NAO_CONFIRMADO`, e o número de pares é o que
declara isso, em vez de uma mediana com cara de resposta.

## 3. Por que isto é caro exatamente aqui

`fase0/ajustar.py` constrói a série ajustada a partir de **eventos societários**. Uma
troca de moeda **não é evento societário** — não há `factor`, não há data-ex, não há linha
no silver. Então a quebra de 04/07/1994 entra na série como uma queda de **−63,6% em um
pregão, no mercado inteiro, sem causa**.

É a forma do **F-02** outra vez, e da pior maneira: não é um insumo ausente virando zero,
é um insumo **presente, correto e anunciado** — o campo `MOEDA` está lá, preenchido — que
ninguém lê. O arquivo declara o comportamento; o código não tem.

E é o **C-01** em escala de mercado: lá um `factor` mal lido movia um papel por até 50x;
aqui uma unidade não lida move **todos** por 2,75x, num dia, e o gráfico fica plausível.

## 4. O que a doutrina obriga

- **`MOEDA` é enumeração `OBSERVADO`** (A-05): a lista sai do dado, não de um documento —
  o layout publicado já é sabidamente incompleto (P-95) e não temos a URL dele (P-06).
  Valor fora da lista **falha ruidosamente**, nunca é tratado como um dos conhecidos.
- **Quatro valores observados até agora:** `CR$`, `CZ$`, `NCZ$`, `R$`. Medidos em 1986,
  1989, 1990, 1993, 1994, 1995, 2001 e 2023. **Faltam 33 arquivos** — a varredura
  completa é barata e tem de rodar antes de a enumeração ser fechada.
- **O fator de reexpressão é MEDIDO, nunca tabelado.** A conversão legal acerta 1 de 4
  casos; a tabela de planos econômicos teria dito "quebra" quatro vezes e acertado uma.
  A régua é a razão do mesmo ticker, com o controle do dia anterior ao lado.
- **A cobertura do backtest é decisão, não consequência.** Enquanto a reexpressão não
  existir, a série utilizável começa em **04/07/1994**; com ela, em 02/01/1986. Isso não
  se resolve em silêncio: entra em `limitacoes_declaradas` ou vira trabalho.

## 5. O que este documento NÃO mediu (P5)

- **1987, 1988, 1991, 1992** e os 29 arquivos restantes — não abertos. A enumeração de
  `MOEDA` e a lista de quebras estão **incompletas por construção**, não fechadas.
- **A escala em milhares** antes de 04/07/1994 é leitura que reconcilia lei e medição,
  sem documento que a confirme.
- **Nada sobre 1990.** Dois pares.
- **Só `PREULT` e só `TPMERC=010`.** Se a quebra atinge opção, termo ou leilão de forma
  diferente, este instrumento não veria.

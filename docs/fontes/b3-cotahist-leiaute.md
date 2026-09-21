# COTAHIST — o leiaute, e a fonte que fechou a P-06

**Status:** `COMPLETO` · **Acesso:** 19/09/2026 · Fecha a **P-06**, aberta desde 05/09.

```
https://www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf
```

**Revisão 02, de 05/10/2020** — a **mesma** que o projeto já tinha transcrito em
`docs/fontes/SeriesHistoricas_Layout.md`. A P-06 perguntava *"sem a URL não dá para
checar se existe revisão 03"*. Agora dá: **não existe.** A rev. 02 é a corrente.

---

## 1. Onde ela estava, e por que eu não tinha achado

A P-06 estava aberta porque eu concluí, em 18/09, que *"nenhuma das duas páginas
públicas linka documento de leiaute"*. As duas páginas que eu li foram a de **Séries
Históricas** e o formulário no host legado.

**O leiaute está numa terceira página, que eu não abri:**

```
https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/cotacoes-historicas/
```

*Cotações Históricas*, não *Séries Históricas*. São duas páginas irmãs, com nomes quase
iguais, e a documentação mora na que não tem o formulário de download.

> **É a régua §5-B outra vez, e é a segunda vez em dois dias com o mesmo arquivo.** Medi
> *"duas páginas não linkam o leiaute"*; escrevi *"a página onde ela deveria estar não a
> tem"* — uma afirmação sobre onde o documento **deveria** estar, feita sem procurar
> onde ele **está**. Uma busca resolveu. Registro porque o padrão é idêntico ao da
> §5-B.13: **a conclusão saiu mais larga que a medição, e a diferença era um passo de
> procura que eu não dei.**

## 2. O que a página declara sobre o preço — e é fonte primária para o C-03

Transcrição literal:

> *"A série histórica de cotações traz todo o histórico de preços dos títulos negociados
> na Bolsa desde 1986. As cotações são fornecidas **na moeda e forma de cotação da
> época, sem nenhum ajuste para a inflação ou proventos**."*

Duas consequências, e a segunda é uma tensão aberta:

1. **Ajuste de proventos é nosso** — a B3 diz que não faz. É o que o `ajustar.py` existe
   para fazer, e agora está escrito na fonte em vez de presumido.
2. **"Na moeda da época" e a medição do C-03 discordam em 3 de 4 casos.** A frase prevê
   quebra em toda troca de moeda; o dado mostra quebra **só** na do Real. Ver §4.

## 3. O registro de cotação — TIPREG 01, 245 posições

Posições do leiaute (1-indexadas; em Python, menos 1 no início):

| campo | início | fim | tam. | tipo |
|---|---|---|---|---|
| TIPREG | 01 | 02 | 2 | N(02) |
| DATA DO PREGÃO | 03 | 10 | 8 | N(08) |
| CODBDI | 11 | 12 | 2 | X(02) |
| CODNEG | 13 | 24 | 12 | X(12) |
| TPMERC | 25 | 27 | 3 | N(03) |
| NOMRES | 28 | 39 | 12 | X(12) |
| ESPECI | 40 | 49 | 10 | X(10) |
| PRAZOT | 50 | 52 | 3 | X(03) |
| **MODREF** | **53** | **56** | **4** | X(04) |
| PREABE | 57 | 69 | 13 | (11)V99 |
| PREMAX | 70 | 82 | 13 | (11)V99 |
| PREMIN | 83 | 95 | 13 | (11)V99 |
| PREMED | 96 | 108 | 13 | (11)V99 |
| PREULT | 109 | 121 | 13 | (11)V99 |

> **Correção de nome:** o campo 53–56 chama-se **MODREF — "moeda de referência"**. Eu o
> vinha chamando de `MOEDA` no C-03 e no código. Nome errado em campo de posição fixa é
> barato hoje e caro no dia em que alguém procurar `MOEDA` no leiaute e não achar.

**E o leiaute NÃO traz tabela de valores para MODREF.** Não é omissão minha: o documento
lista o campo e não enumera o conteúdo. Então a enumeração **tem** de sair do dado
observado, com falha ruidosa fora dela — A-05, e desta vez não por a tabela estar
incompleta (P-95, o caso do `ESPECI`), mas por **não existir tabela nenhuma**.

Observados no acervo, em 8 dos 41 arquivos: **`CR$` · `CZ$` · `NCZ$` · `R$`**.
Os outros 33 não foram abertos — a lista está incompleta por construção.

## 4. O header diz quando o arquivo foi GERADO, e isso explica o C-03

`00COTAHIST.AAAABOVESPA AAAAMMDD`. Medido:

| arquivos | gerados em |
|---|---|
| 1986, 1989, 1990, 1993, 1994, 1995 | **19991210** — todos no mesmo dia |
| 2001 | 20060331 |
| 2023 | 20231228 |

**Os arquivos antigos foram gerados num lote único, em 10/12/1999** — treze anos depois
do primeiro pregão e cinco anos depois do Plano Real.

Isso reconcilia a frase da B3 com a medição do C-03, e a leitura é esta:

> **`MODREF` é rótulo histórico, não a unidade em que o número está gravado.** A B3
> reexpressou a série pré-Real numa base única ao regerá-la em 1999, e deixou a
> fronteira do Real (04/07/1994) como está. Por isso 1986, 1989 e 1993 não têm quebra —
> e 1994 tem, de **2,744**.

**`NAO_CONFIRMADO`, e a distinção importa:** isto é a leitura que reconcilia cinco
medições e a data de geração. Não há documento da B3 afirmando a reexpressão.

> **O perigo prático, e ele é o C-01 em outra roupa:** um leitor que confie em `MODREF`
> para converter aplicaria **três conversões falsas** (1986, 1989, 1990) e erraria a
> única verdadeira, porque o rótulo muda onde o número não muda e o número muda onde o
> rótulo também muda. *Campo que parece dizer o fator e não diz* — exatamente o que o
> `factor` da B3 fez no C-01.

## 5. O que este documento NÃO cobre (P5)

- **A tabela de `CODBDI`, `TPMERC` e `ESPECI`** não foi transcrita aqui — ela já está em
  `docs/fontes/SeriesHistoricas_Layout.md`, e a **P-95** registra que a de `ESPECI` está
  incompleta contra o dado de 2023. Esta fonte confirma a revisão, não corrige a P-95.
- **Existe uma segunda URL** para o mesmo nome de arquivo
  (`.../C8/F3/08/B4/297BE410.../SeriesHistoricas_Layout.pdf`), não aberta. Se for outra
  revisão, a conclusão do §1 muda — e é por isso que ela está escrita aqui em vez de
  omitida.
- **A versão em inglês** (`HistoricalQuotations_B3.pdf`) não foi comparada com a
  portuguesa. Duas traduções do mesmo leiaute que discordam seria um achado.

---

## Fontes

- [Cotações históricas — B3](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/cotacoes-historicas/) — lida 19/09/2026
- [LAYOUT DO ARQUIVO – COTAÇÕES HISTÓRICAS, rev. 02 de 05/10/2020](https://www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf) — lido 19/09/2026

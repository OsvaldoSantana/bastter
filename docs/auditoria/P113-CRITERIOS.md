# P-113 — critérios de aceitação, escritos ANTES da corrida

**23/09/2026.** Este arquivo existe por causa da **P-116**: em 21/09 os critérios do
`test_ajustar_janela.py` foram escritos antes da primeira corrida e entraram no **mesmo
commit** que os números, e um leitor externo não tem como distinguir critério de resultado.
*"Pré-registrado" não é verificável pela P4 se o histórico não puder prová-lo.*

> **O processo, e ele é a única coisa que torna o "antes" verificável:** este arquivo é
> commitado e **empurrado**; o hash do commit é a impressão digital; só então a mudança roda.
> A medição vai num arquivo separado, num commit posterior.

**Nada aqui foi medido depois.** Os números da linha de base saem do acervo **como ele está**
— nenhum deles depende da mudança. As previsões são aritmética sobre essa base, e estão
escritas como números exatos de propósito: previsão com faixa larga não reprova nada.

---

## 1. A decisão dele

> Usar o fechamento do COTAHIST quando a B3 não traz `closingPricePriorExDate`, com uma
> coluna nova dizendo de onde veio cada preço de véspera (B3 ou COTAHIST), e **a B3 ganhando
> quando existe**. Sem segundo leitor de COTAHIST (N-01).

**Trocar a fonte de um insumo é P1, não conveniência** — é por isso que a P-113 era
`DECISAO_DE_DESENHO` e não tarefa. O que a torna defensável é que as duas fontes já foram
medidas uma contra a outra: **352 de 352 ao centavo em 2023**, e ≥ 1.000 casos sem uma única
divergência na janela 2021–2025. A substituição não é um palpite de que elas concordam; é o
uso de uma concordância medida.

**Onde a mudança mora, e por que não é no `refinar.py`:** a substituição precisa de duas
coisas que o `refinar.py` não tem — o casamento evento↔ticker (ISIN, depois
`(prefixo, ESPECI)` com vigência) e a série de preços. As duas moram no `ajustar.py`. Pôr o
leitor de preço no `refinar.py` seria o terceiro leitor de COTAHIST do projeto, e o
`refinar.py` já é importado pelo `ajustar.py` — a dependência ficaria circular. **Um fato, um
dono** (N-01): `calendario.py` acha arquivo e data, `ajustar.py` lê preço.

---

## 2. A linha de base — medida hoje, sem a mudança

Janela **2021–2025**, silver `eventos_silver_2026-09-11_cal-1986-2026.csv`.

| | |
|---|---|
| eventos casados | 8.514 |
| eventos com data ex **dentro** da janela de preços | **2.218** |
| séries `INCOMPLETO` | **78** |
| degraus medidos | **1.586** |

**Os 2.218, por `fator_status`:**

| status | n | o que é |
|---|---|---|
| `CALCULADO` | 2.020 | tem fator |
| **`SEM_PRECO`** | **173** | provento do suplemento, sem `closingPricePriorExDate` — **o alvo** |
| `TIPO_DESCONHECIDO` | 14 | rótulo fora da enumeração observada (A-05) |
| `SEM_FATOR` | 9 | **subscrição** — ver §5 |
| `PRECO_INVALIDO` | 2 | preço zero ou negativo |

**Dos 173 `SEM_PRECO`, o COTAHIST tem o fechamento da véspera em 172.** O que falta em um é
véspera dentro da janela de preços, não preço.

---

## 3. O que tem de acontecer — previsão exata

| # | grandeza | hoje | **previsto** |
|---|---|---|---|
| **C1** | `SEM_PRECO` resolvidos pelo COTAHIST | 0 | **172** |
| **C2** | séries `INCOMPLETO` | 78 | **18** |
| **C3** | degraus contaminados (par com fator e irmão sem fator no mesmo dia) | 138 | **8** |
| **C4** | …desses, presentes na tabela de degraus | 137 | **7** |
| **C5** | pares `(ticker, data_ex)` que ganham fator do zero | — | **7** |
| **C6** | pares já existentes que ganham uma parcela nova | — | **131** |
| **C7** | total de degraus medidos | 1.586 | **1.593** |

**C2 não vai a zero, e isso está previsto:** dos 18 que sobram, **9 são causados só por
`SEM_FATOR`** (subscrição) e os outros 9 por `TIPO_DESCONHECIDO`, `PRECO_INVALIDO` e o único
`SEM_PRECO` sem véspera. Previsão que fosse a zero estaria escondendo a §5.

---

## 4. O que REPROVA a mudança

Qualquer um destes, sozinho, e a mudança não entra:

**R1 — as duas fontes divergirem onde ambas existem.** A premissa inteira é a concordância
medida. Todo evento do paginado tem `closingPricePriorExDate` **e** tem fechamento no
COTAHIST: se algum par divergir além de um centavo, a substituição perde o fundamento e o
achado passa a ser a divergência. **Tolerância: R$ 0,01. Divergências aceitas: 0.**

**R2 — a B3 não ganhar.** Nenhum evento que tenha `closingPricePriorExDate` pode sair marcado
`COTAHIST`, e nenhum valor de preço de véspera de origem `B3` pode mudar. A regra é
*substituir ausência*, nunca *preferir a nossa fonte*.

**R3 — o degrau não encolher.** O critério do C-02, e ele é o portão: `|média ajustada|`
tem de continuar menor que `|média bruta|`, no agregado e nos cinco anos. Aplicar 172 fatores
novos que pioram o degrau significa que a substituição está errada — leitura, sentido ou dia.

**R4 — o controle se mover.** Os pares de pregões **sem evento** não podem mudar: a pior
divergência tem de continuar em **1e-27** (arredondamento de `Decimal`). Se um par sem evento
se mexer, a mudança tocou preço que não devia tocar.

**R5 — série perder qualidade.** Nenhuma série pode sair de `AJUSTADO` para `INCOMPLETO` ou
`NIVEL_INCERTO`. A mudança só pode acrescentar informação.

**R6 — o instantâneo dourado de 2023 se mover por motivo não explicado.** Ele **vai** mudar,
ao contrário das corridas anteriores, porque 2023 tem eventos `SEM_PRECO` que agora ganham
fator. O que se exige é que **toda** diferença no CSV de 2023 seja atribuível a um par
`(ticker, data_ex)` da lista C5/C6 — nenhuma linha pode mudar sem estar nessa lista.

**R7 — o número de duplicatas se mover.** A-12: 206, e 206 independentemente do calendário.
A substituição de preço não toca identidade de evento.

---

## 5. O que esta mudança NÃO faz, e é decisão dele

A P-113 diz, no fim: *"Conferir junto: `diagnostico()` conta `SEM_FATOR` (subscrição, que por
desenho não ajusta preço) como insumo ausente."*

**Conferido, e é verdade.** `diagnostico()` marca a série `INCOMPLETO` quando qualquer evento
casado não tem `fator_status == CALCULADO`, e subscrição entra nessa conta. Mas subscrição
**não é evento de ajuste de preço por desenho** — o próprio `refinar.py` a marca `SEM_FATOR`
com esse motivo escrito. Contá-la como insumo ausente faz a série parecer incompleta quando
não falta nada.

**O tamanho disso muda com esta mudança, e é por isso que ele está aqui e não depois:**

| | INCOMPLETO |
|---|---|
| hoje | 78 — subscrição é 1 |
| depois da substituição de preço | **18 — subscrição vira 9, isto é, metade** |
| se `SEM_FATOR` deixasse de contar | **9** |

Hoje a subscrição está escondida atrás de 172 `SEM_PRECO`. Removidos eles, ela passa a
responder por **metade das séries `INCOMPLETO` que sobram** — e `INCOMPLETO` é um status
publicado, que diz *"o retorno desta série está errado"*. Dizer isso de 9 séries porque houve
uma subscrição é dizer algo falso sobre elas.

**Não mudo isso nesta rodada**, porque reclassificar um status publicado é decisão dele e não
estava no que ele pediu. Fica registrado com o número, para a decisão ser tomada sabendo
quanto vale.

---

## 6. Como cada critério é conferido

Todos em `fase0/test_p113_preco_de_vespera.py`, contra o acervo real, e cada um pela
**medição**, nunca pela presença do campo:

- **R1** compara, evento a evento, `closingPricePriorExDate` com o fechamento do COTAHIST na
  véspera — é o teste que pode derrubar a premissa, e ele roda sobre todos os pares em que as
  duas fontes existem;
- **R2** tem prova por **mutação**: inverter a precedência (COTAHIST ganhando) tem de fazer o
  teste reprovar. Guarda que nunca falhou é guarda que ninguém sabe se funciona;
- **R3/R4** são o `medir()` inteiro, com o controle ao lado — os mesmos instrumentos do C-02;
- **C1–C7** são números exatos, e cada um entra como `assert` com o valor deste documento.

**Se um critério reprovar, o resultado é o achado** — não o motivo para afrouxar o critério.
O C-02 por ano já reprovou em 4 de 5 e ficou em `xfail` estrito (P-115) em vez de ser
relaxado; a régua é a mesma aqui.

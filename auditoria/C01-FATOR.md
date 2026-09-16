# C-01 — como se lê o `factor` dos eventos de quantidade da B3

**Medido em 16/09/2026**, sobre o silver de `dt_captura=2026-09-11` (738 linhas, 74
emissoras) e sobre o `COTAHIST_A2023`. Status: **MEDIDO, REGRA PROPOSTA — aguarda a sua
confirmação.** Nada em `refinar.py` foi alterado.

## A pergunta

`refinar.py` marca 180 eventos como `FACTOR_AMBIGUO` e recusa calcular o fator de ajuste.
O motivo está escrito no próprio relatório: *"a leitura de `factor` — percentual ou
multiplicador — muda o resultado por até 50x e não há fonte que desempate."* Enquanto ela
não for respondida, a série de preços não pode ser ajustada, e sem preço ajustado não há
backtest.

## O instrumento que eu ia usar, e por que ele era o instrumento errado

O plano era desempatar pelo COTAHIST: comparar o fechamento da véspera com o do dia ex e
medir o fator real. Duas coisas quebraram esse plano, e as duas são mensuráveis:

1. **O acervo tem um ano só.** `COTAHIST_A2023.ZIP` (70 MB) e o `.TXT` extraído (557 MB).
   Eu tinha registrado "três arquivos COTAHIST" lendo a coluna truncada do PowerShell —
   eram o ZIP, a pasta e o TXT. Corrigido.
2. **Dos 180 eventos ambíguos, exatamente UM tem data-ex em 2023.** A distribuição por
   ano é: 2025 com 31, 2021 com 19, 1996 com 14, 2024 com 9, 2009 com 9, e uma cauda
   longa. 2023 tem 1 — o FLRY.

Um caso não decide uma regra, e a doutrina do projeto diz isso. **Então o COTAHIST não é
o árbitro. Ele é a testemunha de corroboração.** O árbitro é a distribuição.

## O árbitro: a distribuição dos 180 valores, separada por tipo de evento

### DESDOBRAMENTO — 65 eventos

| `factor` | ocorrências | lido como **%** → fator | lido como **multiplicador** → fator |
|---|---|---|---|
| 50 | 2 | 1,5 | 51 |
| 70 | 2 | 1,7 | 71 |
| **100** | **19** | **2** | 101 |
| 200 | 11 | 3 | 201 |
| 300 | 7 | 4 | 301 |
| 400 | 13 | 5 | 401 |
| 900 | 6 | 10 | 901 |
| 1900 | 1 | 20 | 1901 |
| 4900 | 2 | 50 | 4901 |
| 7900 | 1 | 80 | 7901 |
| 9900 | 1 | 100 | 9901 |

Lido como percentual, a coluna inteira cai em cima das razões canônicas de desdobramento:
**1:2, 1:3, 1:4, 1:5, 1:10, 1:20, 1:50, 1:80, 1:100**. Lido como multiplicador, produz
101, 201, 301, 401, 901 — e o padrão `…01` é a própria denúncia: são `(fator−1)×100`.

Não é uma comparação de plausibilidade. É uma **assinatura aritmética**: a probabilidade
de onze valores distintos caírem todos, por acaso, a exatamente um centésimo de uma razão
inteira é desprezível.

### GRUPAMENTO — 41 eventos, e aqui a regra é OUTRA

| `factor` | ocorrências | lido como **multiplicador direto** |
|---|---|---|
| 0,001 | 12 | 1000:1 |
| 0,01 | 6 | 100:1 |
| 0,1 | 6 | 10:1 |
| 0,02 | 2 | 50:1 |
| 0,005 | 2 | 200:1 |
| 0,0181818 | 2 | 55:1 |
| 0,2 / 0,333333 / 0,0666667 / 0,025 / 0,008 / 0,004 / 0,00395 | 1 cada | 5:1, 3:1, 15:1, 40:1, 125:1, 250:1, 253:1 |
| 0,00002 | 2 | 50000:1 |

**No grupamento o campo JÁ É o multiplicador de quantidade**, e ele é menor que 1.
Aplicar `1 + factor/100` aqui daria 1,00001 — ou seja, *nenhum ajuste* num evento que
multiplica o preço por mil. O erro seria silencioso e na direção pior: a série passaria
por um grupamento de 1000:1 sem degrau.

### BONIFICAÇÃO — 72 eventos

Valores entre 0,16 e 900, com concentração em 10, 20, 25, 30, 50, 100. Lidos como
percentual: 1,10 · 1,20 · 1,25 · 1,30 · 1,50 · 2,00. São percentuais de bonificação
usuais. Lidos como multiplicador, seriam bonificações de 1000% a 90000%.

### INCORPORAÇÃO — 2 eventos

`20,5` e `100`. Dois casos não sustentam regra. **Fica fora da regra**, marcado, e não
adivinhado — P6.

## A testemunha: FLRY, COTAHIST 2023

Evento no bruto da B3 (`FLRY.json → stockDividends`):

```
{ "label": "BONIFICACAO",    "factor": "5,00000000000",   "lastDatePrior": "12/06/2023" }
{ "label": "DESDOBRAMENTO",  "factor": "100,00000000000", "lastDatePrior": "26/06/2017" }
```

O mesmo campo, na mesma emissora, vale 5 e 100. Como multiplicador, seriam um evento de
5:1 e outro de 100:1 na mesma ação. Como percentual: bonificação de 5% e desdobramento
de 100% (isto é, 1:2). A segunda leitura é a única que sobrevive ao par.

Preços de FLRY3 no COTAHIST 2023, lote padrão, mercado à vista, sem ajuste:

| pregão | fechamento | variação |
|---|---|---|
| 09/06 | 15,89 | |
| **12/06** | **16,32** | último dia COM direito |
| 13/06 | 15,05 | **−7,78 %** |

**−7,78 % é a maior queda de fechamento do FLRY3 no ano inteiro**, num papel cujo
desvio-padrão diário em 2023 foi 1,87 %. É 4,2 σ, e a segunda maior queda do ano foi
−4,97 %.

Duas coisas saem daí, e uma delas eu não estava procurando:

1. **A ordem de grandeza confirma o percentual.** Uma bonificação de 5% pede −4,76 %; o
   observado é −7,78 %, com resíduo de ~3 % (1,7 σ) que o ruído do dia explica. A leitura
   como multiplicador pediria **−83 %**. O COTAHIST não resolve 5 % na casa decimal — um
   evento dessa magnitude está dentro do ruído diário —, mas resolve 50× sem esforço, e
   50× é exatamente a pergunta.
2. **`lastDatePrior` é o último dia COM direito, não o primeiro dia ex.** O degrau cai no
   pregão *seguinte*. A coluna do silver se chama `data_ex` e guarda `lastDatePrior`: quem
   ajustar preço usando essa data como dia ex vai deslocar todo ajuste em um pregão. Isso
   não estava na pergunta e é achado à parte.

## A regra proposta

```
GRUPAMENTO                    ->  fator = factor            (exige 0 < factor < 1)
DESDOBRAMENTO, BONIFICACAO    ->  fator = 1 + factor/100    (exige factor >= 0)
qualquer outro rotulo         ->  FACTOR_FORA_DA_REGRA, e a linha entra marcada
factor fora da faixa do rotulo ->  FACTOR_FORA_DA_REGRA
```

E o ajuste de preço usa **o pregão seguinte a `lastDatePrior`**, não `lastDatePrior`.

A recusa faz parte da regra, e é o ponto dela: a regra cobre o que foi **observado** nos
180, e qualquer coisa fora disso continua acusada em vez de estimada.

## Limitações declaradas (P5)

- **INCORPORAÇÃO: 2 observações.** Fora da regra por enquanto.
- **Corroboração de preço: um caso.** O COTAHIST cobre 2023 e só o FLRY cai lá. Baixar
  **2021** (19 eventos) e **2025** (31) levaria a corroboração de 1 para 51 casos, e daria
  os casos GRANDES — que são os que o preço resolve bem. É o item de download manual mais
  barato que existe hoje no projeto.
- **A regra do grupamento vem só da distribuição**, sem nenhuma confirmação de preço: os
  41 grupamentos são todos fora de 2023.
- **Os `factor` quebrados** (2,50757 · 2,9647 · 26,2838 · 30,9685 · 12,9477 …) são
  bonificações com percentual não redondo, coisa comum. Eles não contradizem a regra, mas
  também não a confirmam — quem confirma são os redondos.

## O que ainda não foi feito

`refinar.py` **não foi alterado**. A regra acima é proposta, não implementada: quem
escolhe regra neste projeto é você. Implementá-la muda 180 das 738 linhas do silver e
`FACTOR_AMBIGUO` deve cair a ~2 (as incorporações).

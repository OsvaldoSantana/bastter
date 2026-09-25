# Pré-registro `aprendizado` v2 — emenda 1: quando começa o desenvolvimento

*Escrita em 25/09/2026, antes de qualquer resultado e **antes de medir o mês que ela produz**.
Decisão dele sobre a P-132, opção (a). Emenda a `preregistro-ml-v2.md`, que **não foi tocado**:
o sha256 dele continua `2e2c46d4de72057f…` (commit `2c608c9`).*

*Vale a partir do commit **empurrado ao `origin`** que a contém, pela mesma regra do cabeçalho
da v2 (P-116). O mês que a regra produz é medido **depois** desse commit e registrado em outro.*

---

## 1. A regra

> O período de **desenvolvimento** começa no primeiro mês `t` em que **pelo menos 90%** das
> empresas do universo do ML em `t` (definido na §2 da v2) têm **ao menos um documento** com
> `DT_RECEB` ≤ data de decisão de `t`.

Os termos são os da v2: **data de decisão** = último pregão do mês `t`; **universo** = a lista
da §2 (à vista, lote padrão, ≥ 90% dos pregões em 3 meses, volume no percentil ≥ 50, uma classe
por empresa, identidade pelo `codeCVM`).

## 2. O limiar é um grau de liberdade, e está declarado

**90%** foi escolhido por ele em **25/09/2026**, antes de qualquer resultado da família e antes
de medir o mês que o limiar produz. Outro limiar produziria outro mês. Isto fica escrito para
que ninguém o leia como derivado: é escolha, com data.

## 3. Como a medição lê a regra — escrito antes de medir

Três pontos que a §2 da v2 não fixa e que mudariam o mês. **Operacionalização escrita por
Claude em 25/09, antes da medição**, pela mesma razão do limiar: escolhida depois, seria
escolhida olhando.

1. **Documento** = uma linha do índice DFP ou ITR da CVM (`dfp_cia_aberta_AAAA.csv`,
   `itr_cia_aberta_AAAA.csv`), qualquer versão, com o `CD_CVM` da empresa. Não importa se o
   documento traz a variável: a regra é de **cobertura**, não de completude.
2. **Empresa do universo sem `CD_CVM` identificável** conta como **sem documento**. É o lado
   conservador: atrasa o início em vez de adiantá-lo. O número dessas empresas sai ao lado
   do resultado, com o n de cada mês (§5-B.14).
3. **O primeiro mês fecha a questão.** Se a cobertura passar de 90% em `t` e cair abaixo
   depois, o desenvolvimento **não** recomeça: a regra escolhe um início, não um filtro mensal.
   A cobertura mês a mês é publicada assim mesmo.

## 4. O que NÃO muda

- **Teste:** jan/2020 a ago/2026, 80 meses, executado uma vez.
- **Hiperparâmetros congelados em dez/2019.** O fim do desenvolvimento não se move.
- **Orçamento de testes:** `m` = 11 na família e 24 no conservador. A emenda não acrescenta
  hipótese nem variante.
- Hipóteses, variáveis, modelos, grade, métricas, critério da §7, os nove testes da §8, o plano
  de mudanças e o modo sombra.

Por isso é **emenda**, e não `v3`: a §9 da v2 exige nova versão para mudança de período de
**teste**, variável, grade, família de modelo, alvo ou limiar; o início do desenvolvimento não
está na lista. O que ele encurta é a janela de onde os hiperparâmetros são escolhidos, e é essa
a razão de registrá-la antes de medir.

## 5. Motivo: CV-04

A v2 declara período desde jan/2010 *"com fundamentos DFP desde 2010"*, e a regra de
disponibilidade (`DT_RECEB` ≤ data de decisão) deixa **zero empresas** com fundamento de jan a
dez/2010. O menor `DT_RECEB` do `dfp_cia_aberta_2010` é **27/01/2011**, e não existe ITR de 2010.

| mês | empresas com documento (todas, não só o universo) |
|---|---|
| jan/2010 … dez/2010 | 0 |
| jan/2011 | 3 |
| fev/2011 | 82 |
| mar/2011 | 510 |

Medição completa em `ACHADOS.md` → CV-04. Esses números são do mercado inteiro; a regra é sobre
o **universo** do ML, e é esse mês que a medição vai dizer.

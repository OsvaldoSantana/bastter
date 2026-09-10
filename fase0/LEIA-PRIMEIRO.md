# Fase 0 — o que tem prazo, e por quê

## A afirmação que eu vinha repetindo, e ela estava imprecisa

Eu escrevi várias vezes: *"a CVM sobrescreve os arquivos anuais e `DT_RECEB` não se
reconstrói"*. A conclusão está certa, o motivo não.

`DT_RECEB` é a data em que a CVM **recebeu** o documento, e ela viaja **dentro do
dado**. Se um registro sobrevive, um download feito em 2030 ainda diz quando ele
chegou. Então `DT_RECEB` *se* reconstrói — para os registros que sobrevivem.

**O que não se reconstrói é o que foi substituído.** O `dfp_cia_aberta_2026.zip` é um
arquivo **mutável**: enquanto o ano corre, empresas entregam, e quem entrega errado
entrega de novo com `VERSAO` incrementada. A versão antiga, muito provavelmente, deixa
de existir no arquivo publicado.

Isso importa exatamente para o que a Fase 0 existe para permitir:

> Um backtest ponto-no-tempo precisa responder **"o que era possível saber no dia X"**.
> Se em 15/03 a empresa publicou um lucro e em 20/05 corrigiu, um backtest que rodasse
> com o arquivo de hoje usaria o número corrigido para decidir uma compra de abril.
> Isso é **look-ahead bias**, e é a forma mais comum de um backtest mentir.

`DT_RECEB` diz quando o registro **sobrevivente** chegou. Não diz o que o registro
**substituído** dizia, nem que ele existiu.

## A consequência, e ela muda a urgência

O prazo não é "o arquivo do ano vira em 31/12". É contínuo:

> **Cada dia sem snapshot é um dia de história ponto-no-tempo que nunca mais existe.**

Você não recupera o que o arquivo dizia em março de 2026. Recupera a partir do primeiro
dia em que começar a guardar — e só isso. Não há como comprar esse dado depois.

## CONFIRMADO em 06/09/2026 — e a urgência ficou mais estreita e mais aguda

O `NAO_CONFIRMADO` que estava aqui **fechou**. A CVM declara o próprio comportamento na
página do conjunto (`docs/fontes/cvm-dfp-politica-atualizacao.md`), e a resposta é:

> *"Os arquivos serão **atualizados semanalmente** com as eventuais **reapresentações**."*
> *"...demonstrações financeiras entregues **nos últimos cinco anos**"*
> *"**Histórico desde 2010** (incluindo arquivos **não sujeitos à política de atualização**)"*

O acervo se parte em dois:

| faixa | arquivos | comportamento | urgência |
|---|---|---|---|
| **2021–2026** | **6** | reescritos **toda semana** | **alta e contínua** |
| 2010–2020 | 11 | congelados | nenhuma |

**O prazo não é anual — é semanal. E o que corre não são 1,5 GB, são 6 arquivos.**
Última atualização registrada: **31/08/2026, 08:01**. Na terça já terá passado pelo
menos mais uma rodada.

Corolário que o projeto não tinha: **`dfp_cia_aberta_2022.zip` de hoje não é o de 2023**.
Um ano de cinco atrás ainda está na janela de reapresentação.

---

## O que o projeto já sabe (não refazer)

Fechado em 03–04/09/2026, está em `docs/fontes/`:

| | |
|---|---|
| URLs | `dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/` e `.../ITR/DADOS/` |
| nome do arquivo | `dfp_cia_aberta_AAAA.zip`, `itr_cia_aberta_AAAA.zip` |
| encoding | **ISO-8859-1** — confirmado, `PENÚLTIMO` íntegro |
| separador | `;` |
| subconjuntos | BPA, BPP, DFC_MD, DFC_MI, DMPL, DRA, DRE, DVA × `_con`/`_ind` |
| enumerações | `ORDEM_EXERC` ∈ {ÚLTIMO, PENÚLTIMO}; `ESCALA_MOEDA` ∈ {MIL, UNIDADE}; `MOEDA` = REAL — **OBSERVADO**, contado em 12,8 M linhas |

**A regra que veio junto e que o script respeita:** o conjunto de arquivos **muda entre
safras** (`composicao_capital` só aparece em 2024). Descubra os arquivos **varrendo o
ZIP**, nunca por lista escrita no código.

## Como usar

```powershell
# 1. Reconhecimento — não baixa nada pesado, responde as perguntas abertas
.\fase0.ps1 -SoConferir

# 2. Download com snapshot datado e imutável
.\fase0.ps1 -Anos 2010..2026

# 3. Depois, periodicamente (o ano corrente muda o tempo todo)
.\fase0.ps1 -Anos 2026
```

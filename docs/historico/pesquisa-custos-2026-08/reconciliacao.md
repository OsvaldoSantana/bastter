# Tabela de reconciliação — a quinta peça

**Emissão:** 01/09/2026. Responde ao achado §5.3 do relatório por peça e a K-01/K-02/R-03 do laudo consolidado.
**Regra:** uma linha por número que aparece em mais de um relatório. O status vencedor é o de maior
evidência, não o do arquivo mais recente. Quem perde é **corrigido no arquivo de origem**, não ignorado.

| # | Número | `cofrinhos` | `corretoras` | `etfs` | `internacional` | **Vencedor** | Onde venceu | Ação |
|---|---|---|---|---|---|---|---|---|
| 1 | **Taxa do IVVB11 = 0,23% a.a.** | — | — | **COMPLETO** (BlackRock, fonte G3) | NÃO CONFIRMADO — "premissa do pedido" | **0,23% · COMPLETO** | `etfs`, tabela "Internacional listado na B3", nota 7 | Corrigir `internacional` §4.1 e §4.4 |
| 2 | **Expense ratio do IVV = 0,03% a.a.** | — | — | **COMPLETO** (ishares.com, fonte G16, net assets US$ 886,7 bi) | NÃO CONFIRMADO — "página do iShares não foi aberta" | **0,03% · COMPLETO** | `etfs`, §6, tabela de comparação | Corrigir `internacional` §4.4 e a pendência 1 do laudo |
| 3 | **Expense ratio do VOO = 0,03% a.a.** | — | — | **PARCIAL** (Vanguard — taxa e AUM sim, inception não) | — | **0,03% · PARCIAL** | `etfs`, fonte G17 | Usável; marcar PARCIAL no ponto de uso |
| 4 | **VTI** | — | — | **NÃO OBTIDO** | — | **bloqueado** | — | Não entra em cálculo. Não é usado em nenhuma rota |
| 5 | **Isenção de R$ 20 mil/mês alcança ETF?** | — | — | **NÃO** — COMPLETO, base legal dupla (Lei 11.033 art. 3º I + IN 1.585 art. 59, lista fechada) | "decisivo… **deixo em aberto**" | **NÃO alcança · COMPLETO** | `etfs` §B.1 | Reescrever `internacional` §4.3–4.4 e a lacuna 1 |
| 6 | **IOF na remessa via stablecoin (Vest)** | — | — | — | "não se aplica (declarado)" — **posição da plataforma** | **NÃO CONFIRMADO** | — | Rota fora da ordenação. Se o IOF de 1,10% valer, vai a 2,50% e fica pior que a Avenue |
| 7 | **Faixas de IR regressivo da renda fixa** | texto §6.1 diz 22,5 / 22,5 / 20 / 15 — **ERRADO**; as tabelas usam o correto | — | — | — | **22,5 / 20 / 17,5 / 15** · COMPLETO | Lei 11.033/2004 art. 1º | Corrigir o texto de §6.1. As tabelas ficam |
| 8 | **Taxa do HASH11** | — | — | **0,3% (camada BR) e 1,3% (máxima global)** | — | **1,3% · COMPLETO** | `etfs`, nota do gestor | 1,3% é o número comparável. Ficha deve trazer os dois |
| 9 | **Corretagem da XP no swing trade** | — | R$ 4,90 — **PARCIAL, "confirmar"** | — | — | **PARCIAL** | — | Não sustenta veredito nominal. Fora da ordenação |
| 10 | **Taxa do ACWI11** | — | — | 0,30% numa seção e 0,75–0,95% em outra, **na mesma página do gestor** | — | **NÃO CONFIRMADO** | — | Bloqueia comparação de global amplo |
| 11 | **Taxa do BOVV11** | — | — | **NÃO CONFIRMADO** (site bloqueia) | — | **bloqueado** | — | 3º maior ETF do país. Prioridade 1 da 3ª passada |
| 12 | **Custódia da B3 em RV** | — | **COMPLETO** — 10 faixas progressivas, isenção R$ 26.471,77 | — | — | **10 faixas · COMPLETO** | `corretoras` §B.4 | Era o insumo que o script v1 truncou em uma faixa |
| 13 | **Quem paga a custódia da B3** | — | **NÃO CONFIRMADO** — a página não diz | — | — | **NÃO CONFIRMADO** | — | Cenário `custodia_absorvida` no motor |
| 14 | **Retenção de 30% em dividendos nos EUA** | — | — | — | **PARCIAL** — ausência de tratado confirmada, percentual não | **PARCIAL** | — | Marca deve acompanhar o uso, não ficar na lista de lacunas |
| 15 | **Periodicidade da custódia do Tesouro** | — | B3 diz provisão diária; Safra diz semestral | — | — | **NÃO CONFIRMADO** | — | Afeta precisão, não direção. `OC 014-2024-VPC` não obtido |

---

## O padrão que a tabela expõe

Cinco das quinze linhas são o **mesmo defeito**: a marca de status ficou na seção que a criou e não
acompanhou o dado até o ponto de uso. Linhas 1, 2, 5, 6, 14.

E duas linhas são o inverso — um arquivo declarou não confirmado algo que o arquivo irmão já tinha
confirmado (linhas 1 e 2). Os quatro relatórios foram produzidos em paralelo, sem se lerem.

**Correção estrutural, não editorial:** o status é propriedade do **dado**, não da seção. No repositório
isso é o campo `status` no YAML de procedência, com o campo `bloqueia` que impede o cálculo de rodar.
No texto, é repetir a marca em cada tabela que usa o número, mesmo parecendo redundante.
A redundância aqui é a função, não o defeito.

## Correção sobre o próprio laudo

O laudo consolidado afirma, em K-01, que o valor `0,0003` (expense ratio do ETF americano) *"não tem
nenhuma fonte confirmada em nenhum dos quatro relatórios"*. **Isso está incorreto.** Ele tem — em
`pesquisa-etfs.md`, seção 6, fonte G16, status COMPLETO, com URL e net assets. O auditor leu a declaração
de não-confirmado em `internacional` §4.4 e a lacuna 10 de `etfs` (que é do **VTI**, não do IVV) e
concluiu ausência de fonte.

O achado **estrutural** de K-01 continua inteiramente válido, e é o mais importante do laudo: dois
arquivos divergiram sobre o mesmo número e nada os reconciliou. Só a premissa factual da acusação
específica não procede. Registrado aqui porque a mesma disciplina que o laudo exige de mim eu devo
exigir dele.

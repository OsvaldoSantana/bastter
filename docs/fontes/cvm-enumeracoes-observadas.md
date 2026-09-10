# Enumerações observadas — ORDEM_EXERC, ESCALA_MOEDA, MOEDA (CVM DFP/ITR)
Fonte: https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/ e https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/
Acesso: 04/09/2026
Status: OBSERVADO — enumeração contada no dado real, NÃO documentada no dicionário de dados da CVM (ver `cvm-dfp-dicionario-dados.md`, que confirma tipo/tamanho mas não os valores)
Vigencia: VIGENTE — mas leia a advertência ao final antes de codificar contra esta lista
Fecha: item 10 da seção "Itens do projeto ainda sem fonte" de `docs/fontes/README.md`
Original: ZIPs `dfp_cia_aberta_{2012,2019,2024}.zip` e `itr_cia_aberta_{2012,2019,2024}.zip`, gravados em `data\bronze\cvm\dfp\` e `data\bronze\cvm\itr\` (pasta `data\` no `.gitignore`, não versionada)
---

## Método

Não é leitura de dicionário — é `DISTINCT` contado por streaming linha a linha sobre o dado real, porque o dicionário da CVM (`meta_dfp_cia_aberta*.txt`) declara tipo/tamanho de `ORDEM_EXERC` e `ESCALA_MOEDA` mas não a lista de valores válidos.

**Amostra:** 3 safras afastadas entre si — **2012, 2019, 2024** — para os dois formulários (DFP e ITR), escolhidas deliberadamente não-contíguas porque o risco real não é "o valor é desconhecido", é "o valor muda de safra para safra sem aviso".

**Cobertura por safra:** os 8 subconjuntos de demonstração que o dicionário confirma conterem `ORDEM_EXERC`/`ESCALA_MOEDA`/`MOEDA` — BPA, BPP, DFC_MD, DFC_MI, DMPL, DRA, DRE, DVA — cada um nas duas variantes `_con` (consolidado) e `_ind` (individual). 2 formulários × 8 subconjuntos × 2 variantes × 3 anos = **96 arquivos CSV**, todos localizados e processados; nenhum arquivo esperado ficou ausente e nenhum arquivo ficou sem as três colunas.

**Execução:** PowerShell, leitura por streaming via `[System.IO.File]::ReadLines($path, [System.Text.Encoding]::GetEncoding("ISO-8859-1"))` — nunca carrega o arquivo inteiro em memória, e o encoding ISO-8859-1 explícito evita corrupção de acentos (`PENÚLTIMO` confirmado íntegro na saída, com Ú acentuado). Cada linha é dividida por `;` (delimitador confirmado no cabeçalho de todos os arquivos), e os valores das 3 colunas-alvo são acumulados em tabela hash: contagem total + conjunto de contextos (`formulário|subconjunto|variante|ano`) em que o valor aparece. Nenhum CSV foi lido para o contexto da conversa — só o agregado final (poucas dezenas de linhas) foi trazido.

**Volume total percorrido:** 12.803.440 linhas de dados (excluindo cabeçalhos), 96 arquivos, em 6 min 26 s.

**Script:** gerado nesta sessão em `%TEMP%\...\scratchpad\count_enums.ps1`, não commitado (é ferramenta de contagem, não parser do projeto — regra da tarefa: não escrever parser).

---

## ORDEM_EXERC — 2 valores distintos, em TODOS os 96 arquivos

| Valor | Contagem (linhas) | Anos em que aparece | Subconjuntos/variantes em que aparece |
|---|---|---|---|
| `ÚLTIMO` | 6.418.033 | 2012, 2019, 2024 | Todos: BPA, BPP, DFC_MD, DFC_MI, DMPL, DRA, DRE, DVA — `_con` e `_ind` — DFP e ITR |
| `PENÚLTIMO` | 6.385.407 | 2012, 2019, 2024 | Idem — todos os 96 contextos |

Nenhum terceiro valor (ex.: "ANTEPENÚLTIMO", numérico, vazio) apareceu em nenhuma das 12,8 milhões de linhas percorridas.

## ESCALA_MOEDA — 2 valores distintos, em TODOS os 96 arquivos

| Valor | Contagem (linhas) | Anos em que aparece | Subconjuntos/variantes em que aparece |
|---|---|---|---|
| `MIL` | 12.079.420 | 2012, 2019, 2024 | Todos os 96 contextos |
| `UNIDADE` | 724.020 | 2012, 2019, 2024 | Todos os 96 contextos |

Nenhum terceiro valor (ex.: "MILHÃO", "CENTAVO") apareceu. Confirma o risco descrito no enunciado: tratar tudo como `MIL` sem checar a coluna erraria por 3 ordens de grandeza exatamente nas 724.020 linhas marcadas `UNIDADE` — presentes em todos os subconjuntos e anos, não um caso raro isolado.

## MOEDA — 1 único valor, em TODOS os 96 arquivos

| Valor | Contagem (linhas) | Anos em que aparece | Subconjuntos/variantes em que aparece |
|---|---|---|---|
| `REAL` | 12.803.440 (100% das linhas) | 2012, 2019, 2024 | Todos os 96 contextos |

Nenhuma outra moeda observada nas 3 safras amostradas.

---

## Diferença entre subconjuntos e entre `_con`/`_ind`

**Nenhuma diferença encontrada.** Os três campos existem com a mesma estrutura nos 8 subconjuntos (BPA, BPP, DFC_MD, DFC_MI, DMPL, DRA, DRE, DVA), nas duas variantes (`_con`, `_ind`), nos dois formulários (DFP, ITR), nas 3 safras amostradas — e o conjunto de valores observados é idêntico em todos os 96 contextos (cada valor de cada coluna tem `contexts=96`, ou seja, aparece em literalmente todo arquivo processado, não em um subconjunto de arquivos). Não há valor exclusivo de um subconjunto, de uma variante, de um formulário ou de uma safra dentro da amostra observada.

---

## Diferença entre SAFRAS no conjunto de arquivos — achado adicional (04/09/2026)

Verificação posterior, feita conferindo a listagem de diretório contra a alegação
de "96 arquivos" deste documento. A contagem de 96 está **exata** — 8 subconjuntos
× 2 variantes × 2 formulários × 3 safras. Mas ao conferi-la apareceu uma diferença
que a contagem por coluna não podia enxergar, porque está fora das três colunas.

**O conjunto de arquivos MUDA entre safras.** `composicao_capital` existe apenas
nas safras de 2024:

| safra | formulário | arquivos no ZIP | tem `composicao_capital`? |
|---|---|---|---|
| 2012 | DFP | 18 | não |
| 2012 | ITR | 18 | não |
| 2019 | DFP | 18 | não |
| 2019 | ITR | 18 | não |
| 2024 | DFP | **19** | **sim** |
| 2024 | ITR | **19** | **sim** |

Isso **não afeta nenhuma contagem acima**: o dicionário confirma que
`composicao_capital` não carrega `ORDEM_EXERC`, `ESCALA_MOEDA` nem `MOEDA`, e por
isso ele nunca entrou nos 96. As três enumerações continuam válidas como contadas.

**Mas é o mesmo risco, num eixo diferente.** A hipótese que este documento foi
escrito para testar era "a enumeração muda de safra para safra sem aviso". A
enumeração não mudou — a **estrutura** mudou. Um parser que descubra os arquivos
por lista fixa, ou que assuma que toda safra traz o mesmo conjunto, quebra em 2012
procurando um arquivo que só passou a existir depois; ou, pior, processa 2024 e
2012 como se fossem comparáveis sem notar que um tem uma demonstração a mais.

Implicação para o parser, do mesmo tipo da advertência abaixo: **descubra os
arquivos por varredura do ZIP, nunca por lista escrita no código**, e registre
quando o conjunto de uma safra diferir do da anterior. Conjunto de arquivos
observado tem exatamente o mesmo status que enumeração observada — vale para as
safras vistas, não é promessa da CVM.

NAO_CONFIRMADO: em qual safra exatamente `composicao_capital` passou a existir.
Só três safras foram baixadas; o corte está em algum ponto entre 2019 e 2024, e
determiná-lo exigiria baixar as safras intermediárias. Não presumi o ano.

---

## Advertência — leia antes de codificar

**Enumeração observada não é enumeração documentada.** Este arquivo registra o que foi CONTADO em 12,8 milhões de linhas de 3 safras (2012, 2019, 2024) de DFP e ITR — não uma garantia da CVM de que só esses valores existirão. Um valor novo pode aparecer em safra futura (2025, 2026, ou qualquer trimestre ainda não amostrado) sem aviso, exatamente como o dicionário de dados da CVM não impede.

**Implicação obrigatória para o parser (quando ele for escrito, fora do escopo desta tarefa):** ao encontrar um valor de `ORDEM_EXERC`, `ESCALA_MOEDA` ou `MOEDA` fora desta lista, o parser precisa **falhar ruidosamente** (exceção, linha rejeitada com log, teste de contrato quebrando) — nunca tratar como um dos valores conhecidos por padrão, nunca ignorar a linha em silêncio. Esse é exatamente o modo de falha que o enunciado da tarefa descreve como o mais caro do projeto: linha duplicada (ORDEM_EXERC mal tratado) ou valor errado por três ordens de grandeza (ESCALA_MOEDA mal tratado).

Se uma safra futura introduzir um novo valor, o achado correto é atualizar este arquivo com nova contagem — não alargar silenciosamente o parser para engolir o valor desconhecido sem entender o que ele significa.

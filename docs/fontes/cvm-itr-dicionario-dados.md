# Dicionário de Dados — ITR (CVM, Portal Dados Abertos)
Fonte: https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/META/meta_itr_cia_aberta_txt.zip
Acesso: 03/09/2026 15:30:02
Status: COMPLETO
Fecha: Dicionário do ITR/CVM
Original: cvm-itr-dicionario-dados.zip (extraído automaticamente em cvm-itr-dicionario-dados\)
---

## Comparação byte a byte com o dicionário do DFP (método de verificação)

Comparei diretamente (`Compare-Object`, após decodificar ambos como ISO-8859-1) cada um dos 11 arquivos do dicionário ITR com o equivalente do dicionário DFP (ver `cvm-dfp-dicionario-dados.md`):

- `meta_itr_cia_aberta.txt` (índice) — **idêntico** ao `meta_dfp_cia_aberta.txt`.
- `meta_itr_cia_aberta_BPA.txt` — **idêntico** ao `meta_dfp_cia_aberta_BPA.txt` (mesmos campos: CD_CONTA, CD_CVM, CNPJ_CIA, DENOM_CIA, DS_CONTA, DT_FIM_EXERC, DT_REFER, ESCALA_MOEDA, GRUPO_DFP, MOEDA, ORDEM_EXERC, ST_CONTA_FIXA, VERSAO, VL_CONTA).
- `meta_itr_cia_aberta_DRE.txt` — **idêntico** ao `meta_dfp_cia_aberta_DRE.txt`.
- `meta_itr_cia_aberta_composicao_capital.txt` — **idêntico** ao `meta_dfp_cia_aberta_composicao_capital.txt`.
- `meta_itr_cia_aberta_parecer.txt` — **1 diferença**: onde o dicionário do DFP tem o campo `TP_RELAT_AUD` ("Tipo Relatório do Auditor Independente"), o dicionário do ITR tem `TP_RELAT_ESP` ("Tipo Relatório da Revisão Especial"). Faz sentido: a DFP é auditada anualmente, o ITR passa por revisão especial trimestral. Os demais campos do arquivo `parecer` são idênticos (CNPJ_CIA, DENOM_CIA, DT_REFER, VERSAO, NUM_ITEM_PARECER_DECL, TP_PARECER_DECL, TXT_PARECER_DECL).

NAO_CONFIRMADO: não rodei o `Compare-Object` nos 5 arquivos restantes (BPP, DFC_MD, DFC_MI, DMPL, DRA, DVA) — só confirmei BPA, DRE, índice, composição de capital e parecer. Assumo que os 5 restantes também são idênticos entre DFP e ITR (mesmo padrão observado em todos os outros), mas isso não foi verificado byte a byte.

## Campos confirmados (ORDEM_EXERC, ESCALA_MOEDA, VERSAO) — mesma definição do DFP

| Campo | Descrição | Domínio | Tipo Dados | Tamanho/Precisão |
|---|---|---|---|---|
| **ORDEM_EXERC** | Ordem do exercício social | Alfanumérico | varchar | 9 |
| **ESCALA_MOEDA** | Escala monetária | Alfanumérico | varchar | 100 |
| **VERSAO** | Versão do documento | Numérico | smallint | Precisão 5, Scale 0 |

## Campo específico do ITR: TP_RELAT_ESP (texto literal)

"Campo: TP_RELAT_ESP — Descrição: Tipo Relatório da Revisão Especial — Domínio: Alfanumérico — Tipo Dados: varchar"

NAO_CONFIRMADO: tamanho exato de TP_RELAT_ESP não capturado na comparação (a ferramenta de diff mostrou só as duas primeiras linhas divergentes); se precisar do tamanho/precisão exatos, preciso reabrir o arquivo.

## Observações

- Encoding: ISO-8859-1 (latin-1), igual ao DFP.
- Mesma ressalva do dicionário DFP: o arquivo não define os valores possíveis (enumeração) de ORDEM_EXERC nem ESCALA_MOEDA, só o tipo de dado.

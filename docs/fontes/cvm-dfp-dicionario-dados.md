# Dicionário de Dados — DFP (CVM, Portal Dados Abertos)
Fonte: https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/META/meta_dfp_cia_aberta_txt.zip
Acesso: 03/09/2026 15:30:02
Status: COMPLETO — para os campos pedidos (ORDEM_EXERC, ESCALA_MOEDA, VERSAO); PARCIAL para o dicionário como um todo (11 arquivos no zip, resumidos abaixo, só 3 lidos por completo)
Fecha: Dicionário de dados do DFP/CVM (ORDEM_EXERC, ESCALA_MOEDA, VERSAO)
Original: cvm-dfp-dicionario-dados.zip (extraído automaticamente em cvm-dfp-dicionario-dados\)
---

## Estrutura do ZIP (texto literal, 11 arquivos de dicionário)

meta_dfp_cia_aberta.txt (arquivo principal — índice de documentos); meta_dfp_cia_aberta_BPA.txt (Balanço Patrimonial Ativo); meta_dfp_cia_aberta_BPP.txt (Balanço Patrimonial Passivo); meta_dfp_cia_aberta_composicao_capital.txt; meta_dfp_cia_aberta_DFC_MD.txt (Demonstração de Fluxo de Caixa — Método Direto); meta_dfp_cia_aberta_DFC_MI.txt (Método Indireto); meta_dfp_cia_aberta_DMPL.txt (Demonstração das Mutações do Patrimônio Líquido); meta_dfp_cia_aberta_DRA.txt (Demonstração de Resultado Abrangente); meta_dfp_cia_aberta_DRE.txt (Demonstração de Resultado); meta_dfp_cia_aberta_DVA.txt (Demonstração de Valor Adicionado); meta_dfp_cia_aberta_parecer.txt (Parecer do Auditor/Declaração).

Confirmei que os campos **ORDEM_EXERC** e **ESCALA_MOEDA** aparecem nos 8 arquivos de demonstrações contábeis (BPA, BPP, DFC_MD, DFC_MI, DMPL, DRA, DRE, DVA) — todos com a mesma estrutura de campos comuns. Não aparecem em `meta_dfp_cia_aberta.txt` (índice), `composicao_capital.txt` nem `parecer.txt`.

## Campos comuns às 8 demonstrações (texto literal — extraído de BPA e DRE, idênticos entre si)

| Campo | Descrição | Domínio | Tipo Dados | Tamanho/Precisão |
|---|---|---|---|---|
| CD_CONTA | Código da conta | Numérico | varchar | 18 |
| CD_CVM | Código CVM | Numérico | char | 6 |
| CNPJ_CIA | CNPJ da companhia | Alfanumérico | varchar | 18 |
| DENOM_CIA | Nome empresarial da companhia | Alfanumérico | varchar | 100 |
| DS_CONTA | Descrição da conta | Alfanumérico | varchar | 100 |
| DT_FIM_EXERC | Data fim do exercício social | AAAA-MM-DD | date | 10 |
| DT_INI_EXERC | Data início do exercício social | AAAA-MM-DD | date | 10 |
| DT_REFER | Data de referência do documento | AAAA-MM-DD | date | 10 |
| **ESCALA_MOEDA** | **Escala monetária** | Alfanumérico | varchar | 100 |
| GRUPO_DFP | Nome e nível de agregação da demonstração | Alfanumérico | varchar | 206 |
| MOEDA | Moeda | Alfanumérico | varchar | 100 |
| **ORDEM_EXERC** | **Ordem do exercício social** | Alfanumérico | varchar | 9 |
| ST_CONTA_FIXA | Indica se é conta fixa ou não | S/N | varchar | 1 |
| **VERSAO** | **Versão do documento** | Numérico | smallint | Precisão 5, Scale 0 |
| VL_CONTA | Valor da conta | Numérico | decimal | Precisão 29, Scale 10 |

NAO_CONFIRMADO: o campo **DT_INI_EXERC** aparece em DRE mas **não aparece em BPA** (balanço é foto de um instante, não tem início de período — confirmado pela ausência do campo no arquivo BPA.txt). Não testei se ele existe nos outros 6 arquivos (BPP, DFC_MD, DFC_MI, DMPL, DRA, DVA) individualmente — assumi por semelhança de nome de conta que DFC/DRA/DVA (fluxos/resultados) o têm e BPP (balanço) não, mas isso é inferência, não leitura direta de cada um dos 6 arquivos restantes.

**Importante — o dicionário NÃO define os valores possíveis (enumeração) de ORDEM_EXERC e ESCALA_MOEDA.** Ele só diz o tipo de dado (varchar) e tamanho. O arquivo não contém, por exemplo, uma lista tipo "ÚLTIMO / PENÚLTIMO" para ORDEM_EXERC nem "MIL / UNIDADE" para ESCALA_MOEDA — isso teria que vir de outro documento (manual do usuário do sistema DFP/CVM) ou ser inferido dos próprios dados no CSV. NAO_CONFIRMADO: valores possíveis de ORDEM_EXERC e ESCALA_MOEDA — não presumi.

## meta_dfp_cia_aberta.txt — arquivo índice (texto literal, campos completos)

| Campo | Descrição | Domínio | Tipo Dados | Tamanho |
|---|---|---|---|---|
| CATEG_DOC | Categoria do documento | Alfanumérico | varchar | 20 |
| CD_CVM | Código CVM | Numérico | char | 6 |
| CNPJ_CIA | CNPJ da companhia | Alfanumérico | varchar | 20 |
| DENOM_CIA | Nome empresarial da companhia | Alfanumérico | varchar | 100 |
| DT_RECEB | Data da recebimento do documento | AAAA-MM-DD | date | 10 |
| DT_REFER | Data de referência do documento | AAAA-MM-DD | date | 10 |
| ID_DOC | Identificador do documento | Numérico | int | Precisão 10 |
| LINK_DOC | Endereço para download do documento | Alfanumérico | varchar | 121 |
| VERSAO | Versão do documento | Numérico | smallint | Precisão 5 |

## meta_dfp_cia_aberta_composicao_capital.txt (texto literal, campos completos)

CNPJ_CIA, DENOM_CIA, DT_REFER, VERSAO (mesmos padrões acima) + campos sem descrição preenchida no dicionário (Descrição e Domínio em branco no arquivo original): QT_ACAO_ORDIN_TESOURO, QT_ACAO_TOTAL_TESOURO, QT_ACAO_TOTAL_CAP_INTEGR, QT_ACAO_PREF_TESOURO, QT_ACAO_PREF_CAP_INTEGR, QT_ACAO_ORDIN_CAP_INTEGR (todos bigint, Precisão 19, Scale 0).

NAO_CONFIRMADO: o próprio dicionário da CVM não preenche "Descrição" nem "Domínio" para os campos QT_ACAO_*. O nome da coluna sugere quantidade de ações ordinárias/preferenciais em tesouraria/capital integralizado, mas isso é leitura do nome do campo, não texto explicativo do arquivo — registrado aqui como interpretação do nome, não como definição confirmada pela fonte.

## meta_dfp_cia_aberta_parecer.txt (texto literal, campos completos)

CNPJ_CIA, DENOM_CIA, DT_REFER, VERSAO (padrão) + NUM_ITEM_PARECER_DECL (Numérico, smallint, Precisão 5) "Número da linha do texto do Parecer/Declaração"; TP_PARECER_DECL (Alfanumérico, varchar 101) "Tipo do Parecer/Declaração"; TP_RELAT_AUD (Alfanumérico, varchar 19) "Tipo Relatório do Auditor Independente"; TXT_PARECER_DECL (Alfanumérico, varchar 8000) "Texto do Parecer/Declaração".

## Observações

- Encoding: os arquivos .txt vieram em ISO-8859-1 (latin-1) — não é UTF-8 nem Windows-1252 exatamente (testei latin-1/ISO-8859-1 e os acentos ficaram corretos). Gravado aqui em UTF-8, conforme regra 5.
- Não li por completo os 6 arquivos restantes (BPP, DFC_MD, DFC_MI, DMPL, DRA, DVA) — assumo estrutura idêntica a BPA/DRE por já ter confirmado ORDEM_EXERC/ESCALA_MOEDA/VERSAO presentes neles via busca de texto, mas não abri cada um individualmente para conferir se têm alguma variação de campo. Se precisar da lista exata de campos de algum desses 6, aponte que abro.

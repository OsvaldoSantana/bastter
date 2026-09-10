# Cadastro de Companhias Abertas — CVM (dicionário + dados)
Fonte: https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/META/meta_cad_cia_aberta.txt (dicionário) e https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv (dados)
Acesso: 03/09/2026 15:30:44 (dicionário) / 15:29:58 (CSV)
Status: COMPLETO
Fecha: Cadastro de companhias abertas da CVM (situação e datas de registro)
Original: cvm-cadastro-dicionario-dados.txt e cvm-cadastro-companhias-abertas.csv
---

## Dicionário de dados (texto literal, campos completos — 44 campos)

| Campo | Descrição | Domínio | Tipo Dados | Tamanho/Precisão |
|---|---|---|---|---|
| AUDITOR | Nome do Auditor | Alfanumérico | varchar | 100 |
| BAIRRO | Bairro | Alfanumérico | varchar | 100 |
| BAIRRO_RESP | Bairro do responsável | Alfanumérico | varchar | 100 |
| CATEG_REG | Categoria do registro | Alfanumérico | varchar | 20 |
| CD_CVM | Código CVM | Numérico | numeric | Precisão 7 |
| CEP | CEP | Numérico | numeric | Precisão 8 |
| CEP_RESP | CEP do responsável | Numérico | numeric | Precisão 8 |
| CNPJ_AUDITOR | CNPJ do Auditor | Alfanumérico | varchar | 18 |
| CNPJ_CIA | CNPJ da companhia | Alfanumérico | varchar | 18 |
| COMPL | Complemento de endereço | Alfanumérico | varchar | 100 |
| COMPL_RESP | Complemento de endereço do responsável | Alfanumérico | varchar | 100 |
| CONTROLE_ACIONARIO | Controle Acionário | Alfanumérico | varchar | 30 |
| DDD_FAX | Código de DDD (FAX) | Numérico | varchar | 4 |
| DDD_FAX_RESP | Código de DDD (FAX) do responsável | Numérico | varchar | 4 |
| DDD_TEL | Código de DDD (Telefone) | Numérico | varchar | 4 |
| DDD_TEL_RESP | Código de DDD (Telefone) do responsável | Numérico | varchar | 4 |
| DENOM_COMERC | Denominação Comercial | Alfanumérico | varchar | 100 |
| DENOM_SOCIAL | Denominação Social | Alfanumérico | varchar | 100 |
| **DT_CANCEL** | **Data de cancelamento** | AAAA-MM-DD | date | 10 |
| DT_CONST | Data de constituição | AAAA-MM-DD | date | 10 |
| DT_INI_CATEG | Data início da categoria do registro | AAAA-MM-DD | date | 10 |
| DT_INI_RESP | Data início de atuação do responsável | AAAA-MM-DD | date | 10 |
| **DT_INI_SIT** | **Data início da situação** | AAAA-MM-DD | date | 10 |
| DT_INI_SIT_EMISSOR | Data início da situação do emissor | AAAA-MM-DD | date | 10 |
| **DT_REG** | **Data de registro** | AAAA-MM-DD | date | 10 |
| EMAIL | Endereço de e-mail | Alfanumérico | varchar | 100 |
| EMAIL_RESP | Endereço de e-mail do responsável | Alfanumérico | varchar | 100 |
| FAX | FAX | Numérico | numeric | Precisão 15 |
| FAX_RESP | FAX do responsável | Numérico | numeric | Precisão 15 |
| LOGRADOURO | Logradouro | Alfanumérico | varchar | 100 |
| LOGRADOURO_RESP | Logradouro do responsável | Alfanumérico | varchar | 100 |
| MOTIVO_CANCEL | Motivo de cancelamento | Alfanumérico | varchar | 100 |
| MUN | Nome do município | Alfanumérico | varchar | 100 |
| MUN_RESP | Nome do município do responsável | Alfanumérico | varchar | 100 |
| PAIS | País | Alfanumérico | varchar | 100 |
| PAIS_RESP | País do responsável | Alfanumérico | varchar | 100 |
| RESP | Nome do Responsável | Alfanumérico | varchar | 100 |
| SETOR_ATIV | Setor de atividade | Alfanumérico | varchar | 100 |
| **SIT** | **Situação** | Alfanumérico | varchar | 40 |
| SIT_EMISSOR | Descrição da situação do emissor | Alfanumérico | char | 80 |
| TEL | Telefone | Numérico | numeric | Precisão 15 |
| TEL_RESP | Telefone do responsável | Numérico | numeric | Precisão 15 |
| TP_ENDER | Tipo de endereço | Alfanumérico | char | 30 |
| TP_MERC | Tipo de mercado | Alfanumérico | varchar | 50 |
| TP_RESP | Tipo de responsável | Alfanumérico | varchar | 100 |
| UF | Unidade da Federação | Alfanumérico | char | 2 |
| UF_RESP | Unidade da Federação do responsável | Alfanumérico | char | 2 |

NAO_CONFIRMADO: assim como no dicionário do DFP/ITR, o dicionário não lista os valores possíveis de SIT (Situação) nem de SIT_EMISSOR — só o tipo/tamanho do campo. Os valores reais observados na coluna SIT do CSV (ver abaixo) foram vistos diretamente nos dados, não no dicionário.

## Estrutura real do CSV (confirmada por leitura direta do arquivo de dados)

Cabeçalho literal (separador `;`):

```
CNPJ_CIA;DENOM_SOCIAL;DENOM_COMERC;DT_REG;DT_CONST;DT_CANCEL;MOTIVO_CANCEL;SIT;DT_INI_SIT;CD_CVM;SETOR_ATIV;TP_MERC;CATEG_REG;DT_INI_CATEG;SIT_EMISSOR;DT_INI_SIT_EMISSOR;CONTROLE_ACIONARIO;TP_ENDER;LOGRADOURO;COMPL;BAIRRO;MUN;UF;PAIS;CEP;DDD_TEL;TEL;DDD_FAX;FAX;EMAIL;TP_RESP;RESP;DT_INI_RESP;LOGRADOURO_RESP;COMPL_RESP;BAIRRO_RESP;MUN_RESP;UF_RESP;PAIS_RESP;CEP_RESP;DDD_TEL_RESP;TEL_RESP;DDD_FAX_RESP;FAX_RESP;EMAIL_RESP;CNPJ_AUDITOR;AUDITOR
```

Duas linhas de exemplo reais, literais (primeiras do arquivo):

```
08.773.135/0001-00;2W ECOBANK S.A. - EM RECUPERAÇÃO JUDICIAL;2W ECOBANK S.A.;2020-10-29;2007-03-23;;;SUSPENSO(A) - DECISÃO ADM;2026-05-19;25224;Energia Elétrica;;Categoria A;2020-10-29;EM RECUPERAÇÃO JUDICIAL OU EQUIVALENTE;2025-04-23;PRIVADO;SEDE;Avenida Dr. Chucri Zaidan, 1550;8 and-conj 815-sl 1;Chacara Santo Antoni;SÃO PAULO;SP;BRASIL;4711130;11;39579400;11;39579499;ri@2wecobank.com.br;DIRETOR DE RELAÇÕES COM INVESTIDORES;FERNANDO GUEDES VIEIRA;2026-04-22;AV DR. CHUCRI ZAIDAN, 1550;8 AND-CONJ815-SL1;CHÁCARA STO. ANTÔNIO;SÃO PAULO;SP;;4711130;11;39579400;;;juridico@2wecobank.com.br;10.830.108/0001-65;GRANT THORNTON AUDITORES INDEPENDENTES LTDA.

11.396.633/0001-87;3A COMPANHIA SECURITIZADORA;TRIPLO A  COMPANHIA SECURITIZADORA;2010-03-08;2009-11-03;2015-12-18;CANCELAMENTO VOLUNTÁRIO;CANCELADA;2015-12-18;21954;Securitização de Recebíveis;;Categoria B;2010-03-08;FASE PRÉ-OPERACIONAL;2010-03-08;PRIVADO;SEDE;Avenida Erasmo Braga, nº. 299;sala 703;Centro;RIO DE JANEIRO;RJ;BRASIL;20020000;21;22338867;21;22338867;dri@3asec.com.br;DIRETOR DE RELAÇÕES COM INVESTIDORES;FELIPE MARQUES DA FONSECA;2011-06-16;AVENIDA ERASMO BRAGA, Nº. 299;SALA 703;CENTRO;RIO DE JANEIRO;RJ;;20020000;21;22338867;21;22338867;juridico@triploasec.com.br;60.525.706/0001-07;MOORE STEPHENS LIMA LUCCHESI AUDITORES INDEPENDENTES
```

Valores de SIT observados diretamente nestas duas linhas: `SUSPENSO(A) - DECISÃO ADM` e `CANCELADA`. NAO_CONFIRMADO: lista completa e exaustiva de todos os valores possíveis de SIT — só vi estes dois exemplos, o arquivo tem milhares de linhas que não li por completo (seria dado bruto, não spec).

## Observações

- Encoding do dicionário (.txt): ISO-8859-1 (latin-1). O CSV de dados, por outro lado, já veio corretamente acentuado ao ser lido — parece estar em UTF-8 ou o PowerShell/Read tool já tratou corretamente (confirmado visualmente: "SÃO PAULO", "RECUPERAÇÃO JUDICIAL" aparecem corretos).
- O CSV inteiro tem 1.493.174 bytes (milhares de companhias) — não li o arquivo inteiro, apenas o cabeçalho e as duas primeiras linhas de dados, suficiente para confirmar a estrutura de colunas. Isso está de acordo com a doutrina do projeto (dado bruto não é spec).

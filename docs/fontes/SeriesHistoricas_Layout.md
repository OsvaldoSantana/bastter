# Layout do Arquivo — Cotações Históricas (COTAHIST)
Fonte: NAO_REGISTRADA
Acesso: 03/09/2026 10:56:24
Status: COMPLETO — posições/larguras verificadas contra COTAHIST_A2023.TXT em 04/09/2026, com fechamento aritmético ao byte (registro fisico = 247 bytes, CRLF); tabelas de domínio CODBDI e TPMERC INCOMPLETAS; posição de INDOPC NAO verificavel neste arquivo (ver "Verificacao contra dado real")
Fecha: Layout posicional do COTAHIST (245 caracteres, FATCOT, TPMERC, CODNEG)
Original: SeriesHistoricas_Layout.pdf
---

## 1. Conceitos básicos (texto literal)

"O arquivo COTAHIST.AAAA.TXT contém as informações das cotações históricas relativas à negociação de todos os papéis-mercado no período de um ano, classificado pelos campos Tipo de registro, Data do pregão, Código de BDI, Nome da empresa e Código de Negociação. Esta divisão não impede que o usuário o classifique de acordo com as suas necessidades, segundo o equipamento e software a serem usados."

"O nome do arquivo identifica o ano correspondente. Ex.: COTAHIST.1990.TXT, COTAHIST.1991.TXT, Etc."

## 2. Estrutura do arquivo (texto literal)

Nome do Arquivo: COTAHIST.AAAA.TXT

Tipos de Registros: Cada arquivo é composto por três tipos de registros.
- Registro - 00 - Header
- Registro - 01 - Cotações dos papéis por dia
- Registro - 99 - Trailer

Tamanho dos Registros: 245 bytes.

## 3. Layout do arquivo

### 3.1 Registro - 00 - Header

| NOME DO CAMPO / DESCRIÇÃO | CONTEÚDO | TIPO E TAMANHO | POS. INIC. | POS. FINAL |
|---|---|---|---|---|
| TIPO DE REGISTRO | FIXO "00" | N(02) | 01 | 02 |
| NOME DO ARQUIVO | FIXO "COTAHIST.AAAA" | X(13) | 03 | 15 |
| CÓDIGO DA ORIGEM | FIXO "BOVESPA" | X(08) | 16 | 23 |
| DATA DA GERAÇÃO DO ARQUIVO | FORMATO "AAAAMMDD" | N(08) | 24 | 31 |
| RESERVA | PREENCHER COM BRANCOS | X(214) | 32 | 245 |

### 3.2 Registro - 01 - Cotações históricas por papel-mercado

| NOME DO CAMPO / DESCRIÇÃO | CONTEÚDO | TIPO E TAMANHO | POS. INIC. | POS. FINAL |
|---|---|---|---|---|
| TIPREG - TIPO DE REGISTRO | FIXO "01" | N(02) | 01 | 02 |
| DATA DO PREGÃO | FORMATO "AAAAMMDD" | N(08) | 03 | 10 |
| CODBDI - CÓDIGO BDI UTILIZADO PARA CLASSIFICAR OS PAPÉIS NA EMISSÃO DO BOLETIM DIÁRIO DE INFORMAÇÕES | VER TABELA ANEXA | X(02) | 11 | 12 |
| CODNEG - CÓDIGO DE NEGOCIAÇÃO DO PAPEL | (sem conteúdo adicional no arquivo) | X(12) | 13 | 24 |
| TPMERC - TIPO DE MERCADO — CÓD. DO MERCADO EM QUE O PAPEL ESTÁ CADASTRADO | VER TABELA ANEXA | N(03) | 25 | 27 |
| NOMRES - NOME RESUMIDO DA EMPRESA EMISSORA DO PAPEL | (sem conteúdo adicional no arquivo) | X(12) | 28 | 39 |
| ESPECI - ESPECIFICAÇÃO DO PAPEL | VER TABELA ANEXA | X(10) | 40 | 49 |
| PRAZOT - PRAZO EM DIAS DO MERCADO A TERMO | (sem conteúdo adicional no arquivo) | X(03) | 50 | 52 |
| MODREF - MOEDA DE REFERÊNCIA | MOEDA USADA NA DATA DO PREGÃO | X(04) | 53 | 56 |
| PREABE - PREÇO DE ABERTURA DO PAPEL-MERCADO NO PREGÃO | (sem conteúdo adicional no arquivo) | (11)V99 | 57 | 69 |
| PREMAX - PREÇO MÁXIMO DO PAPEL-MERCADO NO PREGÃO | (sem conteúdo adicional no arquivo) | (11)V99 | 70 | 82 |
| PREMIN - PREÇO MÍNIMO DO PAPEL-MERCADO NO PREGÃO | (sem conteúdo adicional no arquivo) | (11)V99 | 83 | 95 |
| PREMED - PREÇO MÉDIO DO PAPEL-MERCADO NO PREGÃO | (sem conteúdo adicional no arquivo) | (11)V99 | 96 | 108 |
| PREULT - PREÇO DO ÚLTIMO NEGÓCIO DO PAPEL-MERCADO NO PREGÃO | (sem conteúdo adicional no arquivo) | (11)V99 | 109 | 121 |
| PREOFC - PREÇO DA MELHOR OFERTA DE COMPRA DO PAPEL-MERCADO | (sem conteúdo adicional no arquivo) | (11)V99 | 122 | 134 |
| PREOFV - PREÇO DA MELHOR OFERTA DE VENDA DO PAPEL-MERCADO | (sem conteúdo adicional no arquivo) | (11)V99 | 135 | 147 |
| TOTNEG - NEG. - NÚMERO DE NEGÓCIOS EFETUADOS COM O PAPEL-MERCADO NO PREGÃO | (sem conteúdo adicional no arquivo) | N(05) | 148 | 152 |
| QUATOT - QUANTIDADE TOTAL DE TÍTULOS NEGOCIADOS NESTE PAPEL-MERCADO | (sem conteúdo adicional no arquivo) | N(18) | 153 | 170 |
| VOLTOT - VOLUME TOTAL DE TÍTULOS NEGOCIADOS NESTE PAPEL-MERCADO | (sem conteúdo adicional no arquivo) | (16)V99 | 171 | 188 |
| PREEXE - PREÇO DE EXERCÍCIO PARA O MERCADO DE OPÇÕES OU VALOR DO CONTRATO PARA O MERCADO DE TERMO SECUNDÁRIO | (sem conteúdo adicional no arquivo) | (11)V99 | 189 | 201 |
| INDOPC - INDICADOR DE CORREÇÃO DE PREÇOS DE EXERCÍCIOS OU VALORES DE CONTRATO PARA OS MERCADOS DE OPÇÕES OU TERMO SECUNDÁRIO | VER TABELA ANEXA | N(01) | 202 | 202 |
| DATVEN - DATA DO VENCIMENTO PARA OS MERCADOS DE OPÇÕES OU TERMO SECUNDÁRIO | FORMATO "AAAAMMDD" | N(08) | 203 | 210 |
| FATCOT - FATOR DE COTAÇÃO DO PAPEL | '1' = COTAÇÃO UNITÁRIA; '1000' = COTAÇÃO POR LOTE DE MIL AÇÕES | N(07) | 211 | 217 |
| PTOEXE - PREÇO DE EXERCÍCIO EM PONTOS PARA OPÇÕES REFERENCIADAS EM DÓLAR OU VALOR DE CONTRATO EM PONTOS PARA TERMO SECUNDÁRIO | PARA OS REFERENCIADOS EM DÓLAR, CADA PONTO EQUIVALE AO VALOR, NA MOEDA CORRENTE, DE UM CENTÉSIMO DA TAXA MÉDIA DO DÓLAR COMERCIAL INTERBANCÁRIO DE FECHAMENTO DO DIA ANTERIOR, OU SEJA, 1 PONTO = 1/100 US$ | (07)V06 | 218 | 230 |
| CODISI - CÓDIGO DO PAPEL NO SISTEMA ISIN OU CÓDIGO INTERNO DO PAPEL | CÓDIGO DO PAPEL NO SISTEMA ISIN A PARTIR DE 15-05-1995 | X(12) | 231 | 242 |
| DISMES - NÚMERO DE DISTRIBUIÇÃO DO PAPEL | NÚMERO DE SEQÜÊNCIA DO PAPEL CORRESPONDENTE AO ESTADO DE DIREITO VIGENTE | 9(03) | 243 | 245 |

### 3.3 Registro - 99 - Trailer

| DESCRIÇÃO DO CAMPO | CONTEÚDO | TIPO E TAMANHO | POS. INIC. | POS. FINAL |
|---|---|---|---|---|
| TIPO DE REGISTRO | FIXO "99" | N(02) | 01 | 02 |
| NOME DO ARQUIVO | FIXO "COTAHIST.AAAA" | X(13) | 03 | 15 |
| CÓDIGO DA ORIGEM | FIXO "BOVESPA" | X(08) | 16 | 23 |
| DATA DA GERAÇÃO DO ARQUIVO | FORMATO "AAAAMMDD" | N(08) | 24 | 31 |
| TOTAL DE REGISTROS | INCLUIR TAMBÉM OS REGISTROS HEADER E TRAILER. | N(11) | 32 | 42 |
| RESERVA | PREENCHER COM BRANCOS | X(203) | 43 | 245 |

## 4. Tabelas anexas (texto literal)

### Tabela de CODBDI - Relação dos valores para códigos de BDI

```
02  LOTE PADRAO
05  SANCIONADAS PELOS REGULAMENTOS BMFBOVESPA
06  CONCORDATARIAS
07  RECUPERACAO EXTRAJUDICIAL
08  RECUPERAÇÃO JUDICIAL
09  RAET - REGIME DE ADMINISTRACAO ESPECIAL TEMPORARIA
10  DIREITOS E RECIBOS
11  INTERVENCAO
12  FUNDOS IMOBILIARIOS
14  CERT.INVEST/TIT.DIV.PUBLICA
18  OBRIGACÕES
22  BÔNUS (PRIVADOS)
26  APOLICES/BÔNUS/TITULOS PUBLICOS
32  EXERCICIO DE OPCOES DE COMPRA DE INDICES
33  EXERCICIO DE OPCOES DE VENDA DE INDICES
38  EXERCICIO DE OPCOES DE COMPRA
42  EXERCICIO DE OPCOES DE VENDA
46  LEILAO DE NAO COTADOS
48  LEILAO DE PRIVATIZACAO
49  LEILAO DO FUNDO RECUPERACAO ECONOMICA ESPIRITO SANTO
50  LEILAO
51  LEILAO FINOR
52  LEILAO FINAM
53  LEILAO FISET
54  LEILAO DE ACÕES EM MORA
56  VENDAS POR ALVARA JUDICIAL
58  OUTROS
60  PERMUTA POR ACÕES
61  META
62  MERCADO A TERMO
66  DEBENTURES COM DATA DE VENCIMENTO ATE 3 ANOS
68  DEBENTURES COM DATA DE VENCIMENTO MAIOR QUE 3 ANOS
70  FUTURO COM RETENCAO DE GANHOS
71  MERCADO DE FUTURO
74  OPCOES DE COMPRA DE INDICES
75  OPCOES DE VENDA DE INDICES
78  OPCOES DE COMPRA
82  OPCOES DE VENDA
83  BOVESPAFIX
84  SOMA FIX
90  TERMO VISTA REGISTRADO
96  MERCADO FRACIONARIO
99  TOTAL GERAL
```

### Tabela de ESPECI - Relação de valores para especificação (texto literal, integral)

```
BDR       BDR
BNS       BÔNUS DE SUBSCRIÇÃO EM ACÕES MISCELÂNEA
BNS B/A   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
BNS ORD   BÔNUS DE SUBSCRIÇÃO EM ACÕES ORDINÁRIAS
BNS P/A   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
BNS P/B   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
BNS P/C   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
BNS P/D   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
BNS P/E   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
BNS P/F   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
BNS P/G   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
BNS P/H   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
BNS PRE   BÔNUS DE SUBSCRIÇÃO EM ACÕES PREFERÊNCIA
CDA       CERTIFICADO DE DEPÓSITO DE ACÕES ORDINÁRIAS
CI        FUNDO DE INVESTIMENTO
CI ATZ    Fundo de Investimento Atualização
CI EA     Fundo de Investimento Ex-Atualização
CI EBA    Fundo de Investimento Ex-Bonificação e Ex-Atualização
CI ED     Fundo de Investimento Ex-dividendo
CI ER     Fundo de Investimento Ex-Rendimento
CI ERA    Fundo de Investimento Ex-rendimento e Ex-Atualização
CI ERB    Fundo de Investimento Ex-rendimento e Ex-Bonificação
CI ERS    Fundo de Investimento Ex-Rendimento e Ex-Subscrição
CI ES     Fundo de Investimento Ex-Subscrição
CPA       CERTIF. DE POTENCIAL ADIC. DE CONSTRUÇÃO
DIR       DIREITOS DE SUBSCRIÇÃO MISCELÂNEA (BÔNUS)
DIR DEB   Direito de Debênture
DIR ORD   DIREITOS DE SUBSCRIÇÃO EM ACÕES ORDINÁRIAS
DIR P/A   DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
DIR P/B   DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
DIR P/C   DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
DIR P/D   DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
DIR P/E   DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
DIR P/F   DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
DIR P/G   DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
DIR P/H   DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
DIR PR    DIREITOS DE SUBSCRIÇÃO EM ACÕES RESGATÁVEIS
DIR PRA   DIREITOS DE SUBSCRIÇÃO EM ACÕES RESGATÁVEIS
DIR PRB   DIREITOS DE SUBSCRIÇÃO EM ACÕES RESGATÁVEIS
DIR PRC   DIREITOS DE SUBSCRIÇÃO EM ACÕES RESGATÁVEIS
DIR PRE   DIREITOS DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
FIDC      Fundo de Investimento em Direitos Creditórios
LFT       LETRA FINANCEIRA DO TESOURO
M1 REC    RECIBO DE SUBSCRIÇÃO DE MISCELÂNEAS
ON        ACÕES ORDINÁRIAS NOMINATIVAS
ON ATZ    Ações Ordinárias Atualização
ON EB     Ações Ordinárias Ex-Bonificação
ON ED     Ações Ordinárias Ex-Dividendo
ON EDB    Ações Ordinárias Ex-Dividendo e Ex-Bonificação
ON EDJ    Ações Ordinárias Ex-dividendo e Ex-Juros
ON EDR    Ações Ordinárias Ex-Dividendo e Ex-Rendimento
ON EG     Ações Ordinárias Ex-Grupamento
ON EJ     Ações Ordinárias Ex-juros
ON EJB    Ações Ordinárias Ex-juros e Ex-bonificação
ON EJS    Ações Ordinárias Ex-Juros e Ex-Subscrição
ON ER     Ações Ordinárias Ex-Rendimento
ON ERJ    Ações Ordinárias Ex-Rendimento e Ex-Juros
ON ES     Ações Ordinárias Ex-Subscrição
ON P      ACÕES ORDINÁRIAS NOMINATIVAS COM DIREITO
ON REC    RECIBO DE SUBSCRIÇÃO EM ACÕES ORDINÁRIAS
OR        ACÕES ORDINÁRIAS NOMINATIVAS RESGATÁVEIS
OR P      ACÕES ORDINÁRIAS NOMINATIVAS RESGATÁVEIS
PCD       POSIÇÃO CONSOLIDADA DA DIVIDA
PN        ACÕES PREFERÊNCIAIS NOMINATIVAS
PN EB     Ações Preferenciais Ex-Bonificação
PN ED     Ações Preferenciais Ex-Dividendo
PN EDB    Ações Preferenciais Ex-Dividendo e Ex-Bonificação
PN EDJ    Ações Preferenciais Ex-dividendo e Ex-Juros
PN EDR    Ações Preferenciais Ex-Dividendo e Ex-Rendimento
PN EJ     Ações Preferenciais Ex-Juros
PN EJB    Ações Preferenciais Ex-juros e Ex-bonificação
PN EJS    Ações Preferenciais Ex-Juros e Ex-Subscrição
PN ES     Ações Preferenciais Ex-Subscrição
PN P      ACÕES PREFERÊNCIAIS NOMINATIVAS COM DIREITO
PN REC    RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
PNA       ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE A
PNA EB    Ações Preferenciais Classe A Ex-BonificaçãoPreferencial
PNA EDR   Ações Preferenciais Classe A Ex-Dividendo e Ex-Rendimento
PNA EJ    Ações Preferenciais Classe A Ex-Juros
PNA ES    Ações Preferenciais Classe A Preferencial Ex-Subscrição
PNA P     ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE A
PNA REC   RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
PNB       ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE B
PNB EB    Ações Preferenciais Classe B Ex-Bonificação
PNB ED    Ações Preferenciais Classe B Ex-Dividendo
PNB EDR   Ações Preferenciais Classe B Ex-Dividendo e Ex-Rendimento
PNB EJ    Ações Preferenciais Classe B Ex-Juros
PNB P     ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE B
PNB REC   RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
PNC       ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE C
PNC ED    Ações Preferenciais Classe C Preferencial Classe C Ex-Dividendo
PNC P     ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE C
PNC REC   RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
PND       ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE D
PND ED    Ações Preferenciais Classe D Ex-Dividendo
PND P     ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE D
PND REC   RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
PNE       ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE E
PNE ED    Ações Preferenciais Classe E Ex-Dividendo
PNE P     ACÕES PREFERÊNCIAIS NOMINATIVAS CLASSE E
PNE REC   RECIBO DE SUBSCRIÇÃO EM ACÕES PREFERENCIAIS
```

### Tabela de INDOPC - Relação dos valores para correção de contratos

```
1   US$   CORREÇÃO PELA TAXA DO DÓLAR
2   TJLP  CORREÇÃO PELA TJLP
8   IGPM  CORREÇÃO PELO IGP-M - OPÇÕES PROTEGIDAS
9   URV   CORREÇÃO PELA URV
```

### Tabela de TPMERC - Relação dos valores para tipo de mercado

```
010  VISTA
012  EXERCÍCIO DE OPÇÕES DE COMPRA
013  EXERCÍCIO DE OPÇÕES DE VENDA
017  LEILÃO
020  FRACIONÁRIO
030  TERMO
050  FUTURO COM RETENÇÃO DE GANHO
060  FUTURO COM MOVIMENTAÇÃO CONTÍNUA
070  OPÇÕES DE COMPRA
080  OPÇÕES DE VENDA
```

## Observações

- Documento tem revisão 02, datado de 05/10/2020 (10 páginas), com histórico de alteração de 05/10/2020 (v2.0: "Atualização de itens na TABELA DE ESPECI - RELAÇÃO DE VALORES PARA ESPECIFICAÇÃO").
- FATCOT (posição 211-217, N(07)) e TPMERC (posição 25-27, N(03)) e CODNEG (posição 13-24, X(12)) — os três campos citados no item do inventário — estão todos CONFIRMADOS acima, com posição exata extraída literalmente do arquivo.

## Verificacao contra dado real

**Data:** 04/09/2026
**Arquivo usado:** `COTAHIST_A2023.ZIP` → `COTAHIST_A2023.TXT`, baixado de `https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2023.ZIP` (download automatizado funcionou de primeira, sem bloqueio Cloudflare). 557.584.222 bytes, 2.257.426 linhas. Gravado em `data\bronze\b3\` (gitignored, não commitado).
**Método:** streaming por `[System.IO.File]::ReadLines($path, [System.Text.Encoding]::GetEncoding("ISO-8859-1"))`, uma passada completa do arquivo (~8 s), sem carregar o arquivo inteiro em memória e sem trazer nenhuma linha crua para o contexto além das amostras impressas abaixo. Não escrevi parser — só extração posicional pontual para checagem.

### a) Toda linha tem exatamente 245 caracteres?

**SIM — CONFIRMADO.** As 2.257.426 linhas (header + 2.257.424 registros `01` + trailer) têm exatamente 245 caracteres, sem exceção.

### b) Header (00) e trailer (99) existem e batem com o layout?

**SIM — CONFIRMADO**, campo a campo:

- Header (linha 1): `00` + `COTAHIST.2023` (13c) + `BOVESPA ` (8c) + `20231228` (8c) + 214 brancos. Todas as posições batem com a tabela 3.1.
- Trailer (última linha): `99` + `COTAHIST.2023` (13c) + `BOVESPA ` (8c) + `20231228` (8c) + `00002257426` (11c) + 203 brancos. Todas as posições batem com a tabela 3.3.
- **Checagem cruzada:** o campo TOTAL DE REGISTROS do trailer (`2257426`) é **idêntico** à contagem real de linhas do arquivo (`2257426`), incluindo header e trailer — exatamente como a descrição do campo promete ("incluir também os registros header e trailer").

### c) Amostra de 20 linhas TIPREG=01 (CODNEG, TPMERC, PREULT, FATCOT, PRAZOT por posição)

20 linhas amostradas a intervalos de 100.000 registros `01` ao longo do arquivo inteiro (não só o início). Todos os valores fazem sentido de domínio:

- **CODNEG** — tickers reais e reconhecíveis: `NEOE3`, `LOGN3`, `XPLG11` (mercado à vista); `HOOT4F`, `BRSR6F` (sufixo `F` = fracionário, TPMERC 020); `MRFGP105`, `PETRD198`, `ITSAP864`, `VIIAP590`, `BBASG413` etc. (códigos de opções, TPMERC 070/080).
- **PREULT** — formato `(11)V99` (2 decimais implícitos) decodifica para preços plausíveis: `NEOE3` → `0000000001503` = R$ 15,03 (Neoenergia, jan/2023, condiz com o preço real da época).
- **FATCOT** — `0000001` em todas as 20 amostras (cotação unitária), consistente com o fato de nenhuma delas ser um fundo/ativo de lote-1000.
- **PRAZOT** — em branco (`"   "`) para TPMERC 010 (vista) e 070/080 (opções), como esperado, já que o campo só se aplica a termo. Verifiquei adicionalmente 8 linhas TPMERC=030 (termo) fora da amostra dos 20: `PRAZOT` aparece populado com prazos plausíveis em dias corridos (`016`, `022`, `030`, `045`, `061`, `091`, `182`) em tickers com sufixo `T` (`ABCB4T`, `ABEV3T`, `MRVE3T`) — confirma a posição do campo e o domínio.

### d) Existe alguma linha com FATCOT diferente de 1?

**SIM.** Domínio observado bate exatamente com o documentado (`1` ou `1000`), sem terceiro valor:

| FATCOT | Contagem | Papéis (exemplos) |
|---|---|---|
| `0000001` | 2.256.922 (99,98%) | (a grande maioria dos papéis) |
| `0001000` | 502 (0,02%) | `FNAM11` (248), `FNOR11` (248), `BCEE3L` (1), `BCEE5L` (1), `INGA4L` (2), `VLRA5L` (1), `XING5L` (1) — 7 tickers distintos |

### e) Distribuição de TPMERC — ACHADO: valor fora da tabela documentada

| TPMERC | Contagem | Na tabela do `.md`? |
|---|---|---|
| 010 VISTA | 307.936 | Sim |
| 012 EXERC. OPÇÕES DE COMPRA | 15.186 | Sim |
| 013 EXERC. OPÇÕES DE VENDA | 16.312 | Sim |
| 017 LEILÃO | 29 | Sim |
| 020 FRACIONÁRIO | 103.396 | Sim |
| **021** | **30** | **NÃO — ausente da tabela do `.md`** |
| 030 TERMO | 67.950 | Sim |
| 070 OPÇÕES DE COMPRA | 886.777 | Sim |
| 080 OPÇÕES DE VENDA | 859.808 | Sim |
| 050, 060 (documentados) | 0 | Sim, mas zero ocorrências em 2023 |

**ACHADO (sobre o LAYOUT, não sobre o dado):** `TPMERC=021` ocorre 30 vezes em 2023 e não está na "Tabela de TPMERC" do documento (revisão 02, 05/10/2020). Investiguei as 30 linhas: todas em `CODBDI` 92 ou 93 (também ausentes da "Tabela de CODBDI" do mesmo documento), concentradas entre 27/11/2023 e 22/12/2023, com tickers no formato `<ticker-base><M ou Q>` (ex.: `RENT3M`, `ENEV3M`, `RDOR3Q`, `WEGE3Q`, `INBR32M`). Isso é consistente com sessões especiais de leilão de reorganização de carteira (rebalanceamento de índice, ex. revisão quadrienal do Ibovespa em dez/2023) — mas essa é uma inferência do padrão dos dados, **não confirmada por texto do documento**, que simplesmente não cobre esse código.

**Achado adicional (mesma natureza, fora do escopo original mas encontrado na mesma verificação):** a distribuição completa de `CODBDI` nas 2.257.424 linhas `01` de 2023 contém 6 valores ausentes da "Tabela de CODBDI" do `.md`: **13** (6.644 linhas), **34** (89.876), **35** (2.045), **36** (19.998), **92** (18), **93** (12). Os demais 23 valores observados batem com a tabela documentada.

**Não verificado por falta de exemplo distintivo no arquivo:** `INDOPC` teve um único valor (`0`) em 100% das 2.257.424 linhas — nenhuma linha do COTAHIST_A2023 carrega os valores `1`/`2`/`8`/`9` da tabela documentada (esperado: só se aplica a opções/termo referenciadas em moeda/índice específicos, aparentemente raros ou ausentes em 2023). Não pude, portanto, confirmar a tabela de INDOPC contra dado real — nem confirmar nem refutar. Da mesma forma, `MODREF` teve um único valor (`R$  `) em 100% das linhas — não há exemplo de moeda de referência diferente de Real no arquivo de 2023 para testar. `PTOEXE`, `PREEXE`, `DATVEN`, `CODISI`, `DISMES` e as tabelas completas de `ESPECI` não foram checadas campo a campo contra valores reais nesta sessão (fora do escopo pedido pelo item c, que especificou CODNEG/TPMERC/PREULT/FATCOT/PRAZOT).

### Fechamento aritmético do arquivo — conferência de 04/09/2026 (sessão Cowork)

Auditoria posterior da verificação acima, feita **sem reabrir o arquivo** — só com os
três números que a própria verificação registrou. Eles se fecham exatamente, e o
resto que sobra tem significado:

```
tamanho do .TXT            557.584.222 bytes
2.257.426 linhas x 245     553.069.370 bytes de conteudo
sobra                        4.514.852 bytes
sobra / linha                        2,0   exatamente
```

**Três conclusões, nenhuma delas registrada antes:**

1. **O terminador tem 2 bytes: CRLF.** O registro FÍSICO é de **247 bytes**, não 245.
   A verificação (a) usou `ReadLines`, que descarta o terminador — por isso mediu 245
   e acertou. Mas um parser que leia por blocos de tamanho fixo (`f.read(245)` num
   laço, abordagem natural para largura fixa) **desalinha na segunda linha** e produz
   lixo a partir dali. Quem ler por bytes tem de usar 247, ou abrir em modo texto.

2. **A sobra é exatamente 2×n, não 2×(n−1)** — logo o arquivo **termina com quebra de
   linha depois do trailer**. Um `split` ingênuo por CRLF devolve 2.257.427 elementos,
   sendo o último vazio. É a diferença entre um parser que roda e um que estoura ao
   fatiar uma string de zero caractere.

3. **A aritmética é uma verificação independente das outras duas.** Ela só fecha ao
   byte se as 245 posições E a contagem de 2.257.426 linhas estiverem ambas corretas.
   Um arquivo com uma única linha de largura diferente deixaria resto. Não deixou.

**Duas somas de controle, pelo mesmo raciocínio:**

| distribuição | soma | registros `01` | fecha? |
|---|---|---|---|
| TPMERC (9 valores observados) | 2.257.424 | 2.257.424 | sim |
| FATCOT (2 valores observados) | 2.257.424 | 2.257.424 | sim |

As duas distribuições são **exaustivas** — nenhuma linha ficou fora de categoria, e
portanto nenhum valor adicional escapou da contagem. Sem essa conferência, uma tabela
de distribuição é uma lista de valores vistos; com ela, é a lista completa.

### Correção do escopo do "não verificado"

A seção acima agrupa `INDOPC` e `MODREF` como "sem exemplo distintivo". Os dois casos
não são equivalentes, e a diferença importa:

- **`INDOPC` — posição NÃO verificada.** Valor único `0` em 100% das linhas, um único
  dígito cercado de outros campos numéricos. Se o offset estivesse errado por uma ou
  duas casas, leríamos um `0` de um campo vizinho e nada denunciaria o erro. Aqui a
  ausência de variedade impede verificar **a posição**, não só a tabela de domínio.
- **`MODREF` — posição verificada, tabela não.** Valor único `R$  `, mas o conteúdo é
  **distintivo**: um offset errado devolveria dígitos, não `R$`. A posição está
  confirmada pelo próprio formato; o que falta é exemplo de moeda diferente de Real
  para testar a tabela.

Mesma distinção vale como regra geral: **campo constante e não-distintivo é campo cuja
posição o dado não consegue confirmar.** Só um arquivo de outra safra, ou um registro
de opção referenciada em índice, resolveria `INDOPC`.

### Lacuna de procedência no próprio documento

O cabeçalho deste `.md` traz `Fonte: NAO_REGISTRADA`. É um buraco que importa mais do
que o normal: o achado central desta verificação é que as tabelas anexas da **revisão
02, de 05/10/2020**, estão desatualizadas frente ao dado de 2023. Sem a URL de origem
não dá para checar se a B3 publicou uma revisão 03 que já cubra `TPMERC=021` e os seis
`CODBDI` órfãos. **Ação:** registrar a URL de download do PDF, e conferir a revisão
vigente antes de escrever o parser.

### Veredito da verificação

**Estrutura posicional (larguras, offsets, header, trailer) — CONFIRMADA, sem divergência.** Todas as 2.257.426 linhas têm 245 caracteres; header e trailer batem campo a campo, incluindo a contagem de registros do trailer contra a contagem real do arquivo; os 5 campos pedidos (CODNEG, TPMERC, PREULT, FATCOT, PRAZOT) decodificam para valores com sentido de domínio em todas as amostras.

**Tabelas de domínio (CODBDI, TPMERC) — INCOMPLETAS.** `TPMERC=021` e 6 valores de `CODBDI` (13, 34, 35, 36, 92, 93) ocorrem no dado real de 2023 e não estão na revisão 02 (05/10/2020) do documento-fonte. Isso não invalida o posicionamento dos campos — invalida a premissa de que as "tabelas anexas" são exaustivas. Um parser que valide `TPMERC`/`CODBDI` contra essas tabelas e rejeite/ignore valores desconhecidos silenciosamente vai descartar essas 30 + ~118.000 linhas sem aviso. Se o parser precisar validar esses domínios, ele precisa falhar ruidosamente em valor desconhecido (mesma regra já aplicada às enumerações da CVM em `cvm-enumeracoes-observadas.md`), não assumir a tabela do PDF de 2020 como completa.

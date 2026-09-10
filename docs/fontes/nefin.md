# NEFIN — Séries de Fatores de Risco (CSV) + Metodologia
Fonte: https://nefin.com.br/resources/risk_factors/nefin_factors.csv (dados) e https://nefin.com.br/resources/NEFIN_methodology.pdf (metodologia)
Acesso: 03/09/2026 14:18:30 (CSV) / 14:18:38 (metodologia)
Status: COMPLETO
Fecha: Séries de fatores do NEFIN
Original: nefin_factors.csv e NEFIN_methodology.pdf
---

## Estrutura do CSV (texto literal, cabeçalho + 2 linhas de exemplo)

```
"","Date","Rm_minus_Rf","SMB","HML","WML","IML","Risk_Free"
"1",2001-01-02,0.00660063299326548,0.115836998553672,0.0601153507912085,-0.00491699156244864,0.00787837722397337,0.000578516538294771
"2",2001-01-03,0.0624274996096267,0.0383097794477492,0.00844817019052758,-0.03709321416758,0.018070335041524,0.00057714347804283
```

Colunas: índice de linha (sem nome), Date (AAAA-MM-DD), Rm_minus_Rf (fator de mercado), SMB, HML, WML, IML, Risk_Free. Série diária começando em 02/01/2001.

## Metodologia (texto literal, traduzido do inglês apenas quando indicado — o documento é em inglês)

Fonte do documento: NEFIN — FEA-USP, "Methodology", atualizado em 13 de janeiro de 2017 ("Updated on January 13 2017").

### 5.1 Market Factor (texto literal, em inglês)

"The Market Factor is the difference between the value-weighted daily return of the market portfolio (using all the eligible stocks as defined in Section 3) and the daily risk-free rate. The daily risk-free rate is computed from the 30-day DI Swap."

### 5.2 Small Minus Big (SMB) (texto literal)

"The Small Minus Big Factor (SMB) is the return of a portfolio long on stocks with low market capitalization ('Small') and short on stocks with high market capitalization ('Big'). Every January of year t, we (ascending) sort the eligible stocks according to their December of year t-1 market capitalization, and separate them into 3 quantiles. Then, we compute the equal-weighted returns of the first portfolio ('Small') and the third portfolio ('Big'). The SMB Factor is the return of the 'Small' portfolio minus the return of the 'Big' portfolio."

### 5.3 High Minus Low (HML) (texto literal)

"The High Minus Low Factor (HML) is the return of a portfolio long on stocks with high book-to-market ratio ('High') and short on stocks with low book-to-market ratio ('Low'). Every January of year t, we (ascending) sort the eligible stocks into 3 quantiles (portfolios) according to the book-to-market ratio of the firms in June of year t-1. [...] The HML Factor is the return of the 'High' portfolio minus the return of the 'Low' portfolio."

### 5.4 Winners Minus Losers (WML) (texto literal)

"The Winners Minus Losers Factor (WML) is the return of a portfolio long on stocks with high past returns ('Winners') and short on firms with low past returns ('Losers'). Every month t, we (ascending) sort the eligible stocks into 3 quantiles (portfolios) according to their cumulative returns between month t-12 and t-2. [...] The WML Factor is the return of the 'Winners' portfolio minus the return of the 'Losers' portfolio."

### 5.5 Illiquid Minus Liquid (IML) (texto literal)

"The Illiquid Minus Liquid Factor (IML) is the return of a portfolio long on stocks with high illiquidity ('Illiquid') and short on stocks with low illiquidity ('Liquid'). Every month t, we (ascending) sort the eligible stocks into 3 quantiles (portfolios) according to their previous twelve month illiquidity moving average (stock illiquidity is computed as in Acharya and Pedersen 2005). [...] The IML Factor is the return of the 'Illiquid' portfolio minus the return of the 'Liquid' portfolio."

### 3. Eligibility criteria (texto literal) — quais ações entram nos cálculos

"A stock traded in BOVESPA is considered eligible for year t if it meets 3 criteria:
- The stock is the most traded stock of the firm (the one with the highest traded volume during last year);
- The stock was traded in more than 80% of the days in year t-1 with volume greater than R$ 500.000,00 per day. In case the stock was listed in year t-1, the period considered goes from the listing day to the last day of the year;
- The stock was initially listed prior to December of year t-1."

### Risk-free rate usada nos fatores (texto literal, ver 5.1 acima)

"The daily risk-free rate is computed from the 30-day DI Swap."

### Fórmula de retorno individual (texto literal, Seção 2.1)

"r_i,t = 0 if there is no trade of i in t, or (P^i_t / P^i_t-1) − 1 otherwise" — onde P^i_t é o preço da ação i no dia t ajustado por dividendos e desdobramentos ("adjusted for dividends and splits").

## Observações

- O documento de metodologia está inteiramente em inglês; não traduzi o texto literal (regra 1 pede transcrição literal, não tradução).
- Não transcrevi as seções 6 a 9 (Illiquidity Index, Cost of Equity, Volatility Index IVol-Br, Dividend Yield, Short Interest) porque o item do inventário pede apenas "Séries de fatores do NEFIN" — os 5 fatores (Rm-Rf, SMB, HML, WML, IML) presentes no CSV baixado, que são exatamente as seções 5.1 a 5.5 acima. Se precisar da metodologia do IVol-Br ou do Illiquidity Index, aponte que extraio.
- Encoding: ambos os arquivos já vieram legíveis em UTF-8/ASCII, sem necessidade de redecodificação.

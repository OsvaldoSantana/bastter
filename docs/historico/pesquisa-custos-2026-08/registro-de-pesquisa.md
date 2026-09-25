# Registro de pesquisa — custos de investimento no Brasil

**Emissão:** 31/08–01/09/2026
**Objeto:** levantamento de custos por rota de investimento, insumo da camada de alocação
**Formato:** conforme `docs/fontes/` do manual de desenvolvimento assistido, §2.4
**Destino no repositório:** `docs/fontes/custos-2026-08/`

---

## Regra de evidência aplicada

Só há número nestes arquivos se ele foi lido na fonte citada, na data indicada.
Nada estimado, arredondado por conveniência ou preenchido de memória.

**Vocabulário de status, normalizado entre as quatro frentes:**

| Marcador | Onde aparece | Significado |
|---|---|---|
| `NÃO CONFIRMADO` | no campo de dado | o valor não foi lido em fonte; o campo fica vazio, não estimado |
| `NÃO OBTIDO` | na linha do registro de fontes | a fonte não pôde ser acessada, **com o motivo técnico** |
| `PARCIAL` | na linha do registro de fontes | fonte acessada, mas incompleta ou datada |
| `COMPLETO` | na linha do registro de fontes | fonte acessada e transcrita |

**Cálculos são identificados como cálculo, não leitura**, e trazem fórmula e insumos abertos.

---

## Arquivos

| Arquivo | Linhas | Status | Cobre |
|---|---:|---|---|
| `pesquisa-corretoras.md` | 905 | 1ª e 2ª passada | Tarifas B3 (à vista, opções, custódia, Tesouro), 25 instituições, solidez via API do BCB, MRP, consolidação societária 2020–2026 |
| `pesquisa-cofrinhos.md` | 898 | completa | Cofrinhos e contas remuneradas, FGC, caso Banco Master, Tesouro Direto, poupança, comparação líquida |
| `pesquisa-etfs.md` | 457 | completa | 222 ETFs do registro da CVM, liquidez calculada do COTAHIST, tributação com base legal, BDRs, segmento de "ETF de renda" |
| `pesquisa-internacional.md` | 1.236 | parcial declarada | IOF, 15 plataformas, Lei 14.754/2023 artigo por artigo, ponto de equilíbrio |
| `calc/custos.py` | — | executável | Tabelas de custo de entrada por aporte (seção 4 do documento) |
| `calc/vinte_anos.py` | — | executável | Simulação de custo acumulado em 20 anos (seção 5) |

**Total:** 3.496 linhas, ~300 KB, 390 chamadas de apuração, 150+ fontes com status.

---

## Insumos macro — a serem reconferidos a cada uso

| Indicador | Valor | Série | Data |
|---|---:|---|---|
| Selic meta | 14,00% a.a. | BCB/SGS 432 | 31/08/2026 |
| CDI anualizado | 13,90% a.a. | BCB/SGS 4389 | 28/08/2026 |
| CDI diário | 0,051660% a.d. | BCB/SGS 12 | 28/08/2026 |
| Poupança | 0,6455% a.m. | BCB/SGS 25 | 28/08/2026 |
| TR | 0,1448% a.m. | BCB/SGS 226 | 28/08/2026 |

`https://api.bcb.gov.br/dados/serie/bcdata.sgs.<n>/dados/ultimos/1?formato=json`

Consistência conferida: (1+0,1390)^(1/252) − 1 = 0,051658% a.d. ≈ série 12.

---

## Constantes extraídas — candidatas a `config/politica.yaml`

Nenhuma destas deve ser escrita em código. Todas têm data de coleta e expiram.

```yaml
# custos-b3 — fonte: b3.com.br, acesso 31/08/2026
b3_vista_total_pct:        0.000300   # ADTV < R$3mi (Negociacao+CCP+TTA)
b3_vista_acima_3mi_pct:    0.000225
b3_custodia_rv_isencao:    26471.77   # R$
b3_custodia_rv_faixa1_aa:  0.000500
b3_inatividade_mes:        3.82       # R$, apos 60 meses sem movimentacao
td_custodia_aa:            0.002000
td_isencao_selic:          10000.00   # R$ por CPF, so Tesouro Selic/Reserva
b3_opcoes_pf_total_pct:    0.001340   # sobre o premio

# fgc — fonte: fgc.org.br, acesso 31/08/2026
fgc_limite_conglomerado:   250000.00
fgc_teto_4_anos:           1000000.00
# unidade de exposicao e o CONGLOMERADO, nao a marca

# iof-cambio — fonte: Decreto 6.306/2007 red. 12.499/2025, acesso 31/08/2026
iof_remessa_investimento:  0.0110     # art. 15-B, XXI-A
iof_conta_titularidade:    0.0350     # art. 15-B, XXI
iof_repatriacao:           0.0038     # art. 15-B, XXV
# o cronograma de reducao do Decreto 10.997/2022 FOI REVOGADO

# tributacao — fonte: Planalto e IN RFB 1.585/2015, acesso 31/08/2026
ir_acao_comum:             0.15
ir_day_trade:              0.20
isencao_mensal_acao:       20000.00   # SO acao/ouro/PME — ETF e BDR NAO tem
ir_fii_ganho:              0.20       # sem isencao
ir_etf_rf:                 [0.25, 0.20, 0.15]   # <=180d / 180-720d / >720d
ir_exterior:               0.15       # Lei 14.754/2023, apuracao ANUAL
# a isencao de R$35 mil/mes NAO se aplica mais a aplicacoes financeiras no exterior
come_cotas_etf:            false      # Lei 14.754 art. 18, II e art. 24, §1º
```

---

## Lacunas — o que reabrir numa 3ª passada

| # | Lacuna | Motivo técnico | Prioridade |
|---|---|---|---|
| 1 | BTG Pactual — nenhuma tarifa | SPA sem HTML servido | alta |
| 2 | Liquidez dos ETFs de renda fixa | Ausentes do COTAHIST à vista 2026 | alta |
| 3 | Taxa de adm. de ~20 dos 26 ETFs | Sites de gestor bloqueiam acesso automatizado | alta |
| 4 | Distribuição de covered call é retorno de capital? | Não há divulgação clara | alta |
| 5 | Texto oficial das Resoluções CMN 5.238 e 5.295 | API de normativos do BCB devolveu vazio | média |
| 6 | 11 fintechs — %CDI, emissor, FGC, teto | Dados vivem dentro do app | estrutural |
| 7 | Bradesco, Órama, Mercado Pago, PicPay, Genial | SPA, 403, 404, timeout | média |
| 8 | Retenção de 30% em dividendos nos EUA | Confirmada a ausência de tratado, não o percentual | média |
| 9 | Spread de RF, rebate de fundos, float | **Nenhuma instituição publica** | não fechável |
| 10 | Plano Collor — Lei 8.024/1990 | Texto não obtido | baixa |

**Dados descartados por suspeita:**
- Tabela atribuída ao BTG: idêntica valor por valor à da Terra em cinco faixas. Coincidência exata não é plausível.
- Spreads do C6: artigo de 2024, anterior aos decretos de IOF de 2025.

**Fontes datadas, marcadas:** o "0,99%" do Inter vem de tabela com nota de rodapé de setembro de 2022.

---

## Método — o que funcionou e o que não

**Funcionou:** `curl` via shell contra fontes públicas foi mais eficaz que a ferramenta de
leitura de páginas em quase todos os casos — foi assim que se obteve a tabela de custódia da
B3 (49.524 bytes, HTTP 200) que a outra via não conseguia. Liquidez de ETF calculada do
COTAHIST da própria B3, não copiada de agregador.

**Não funcionou:** Cloudflare em b3.com.br (para curl), StatusInvest, bb.com.br, sites de
gestor de ETF. SPAs sem HTML servido (BTG, Órama, Bradesco). API de normativos do BCB.

**Regra para a próxima:** começar por `curl`, não pela ferramenta de fetch. E registrar o
bloqueio como resultado, não como falha — saber que uma instituição não publica seus custos
de forma acessível **é** um dado sobre ela.

---

## Gatilhos de reauditoria

| Elemento | Reauditar quando |
|---|---|
| Insumos macro (Selic, CDI, poupança) | A cada uso — são séries diárias |
| Tarifas B3 | 90 dias, ou ao primeiro alerta do teste de contrato |
| Corretagem por instituição | 90 dias, ou ao abrir conta |
| %CDI de cofrinhos | 30 dias — são promoções com validade |
| IOF e tributação | A cada decreto ou lei nova; a MP 1.303/2025 já caiu |
| Taxas de ETF | Anual, na lâmina |
| Lista de instituições existentes | Anual — 7 das 25 sumiram em 6 anos |

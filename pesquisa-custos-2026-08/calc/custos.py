# -*- coding: utf-8 -*-
"""
Custo líquido por rota de investimento — Brasil, agosto/2026.
TODOS os insumos vêm dos quatro relatórios de pesquisa (procedência em cada linha).
Nada estimado. Onde falta dado, a rota é marcada.
"""
import json

# ── INSUMOS MACRO (BCB/SGS, 28-31/08/2026) ────────────────────────────────────
CDI_AA      = 0.1390     # série 4389
SELIC_AA    = 0.1400     # série 432
POUP_MES    = 0.006455   # série 25 (período 28/08→28/09/2026)

# ── CUSTOS B3 (fonte primária B3, 31/08/2026) ─────────────────────────────────
B3_VISTA        = 0.000300   # 0,0300% por operação, ADTV < R$3mi (Negociação+CCP+TTA)
B3_CUST_RV_ISEN = 26471.77   # isenção de custódia RV
B3_CUST_RV_F1   = 0.000500   # 0,0500% a.a. primeira faixa
TD_CUSTODIA     = 0.002000   # 0,20% a.a.
TD_ISENCAO_SELIC= 10000.00   # isento até R$10k em Tesouro Selic/Reserva

# ── ROTAS ─────────────────────────────────────────────────────────────────────
# corr_fix = corretagem fixa por ordem (R$) | corr_pct = corretagem percentual
# entrada_pct = custo percentual de entrada adicional (spread+IOF no exterior)
# adm_aa = taxa de administração anual | cust_aa = custódia anual aplicável
ROTAS = [
 # ─ Renda fixa / caixa ─
 dict(g="Caixa e renda fixa", n="Tesouro Reserva / Selic ate R$10k", corr_fix=0, corr_pct=0,
      b3=0, entrada=0, adm=0, cust=0, nota="isento de custodia ate R$10k por CPF"),
 dict(g="Caixa e renda fixa", n="Tesouro Selic acima de R$10k", corr_fix=0, corr_pct=0,
      b3=0, entrada=0, adm=0, cust=TD_CUSTODIA, nota="0,20% a.a. so sobre o excedente"),
 dict(g="Caixa e renda fixa", n="Tesouro IPCA+ / Prefixado", corr_fix=0, corr_pct=0,
      b3=0, entrada=0, adm=0, cust=TD_CUSTODIA, nota="0,20% a.a. desde o primeiro real"),
 dict(g="Caixa e renda fixa", n="Cofrinho / RDB 100% CDI (FGC)", corr_fix=0, corr_pct=0,
      b3=0, entrada=0, adm=0, cust=0, nota="sem taxa; risco de credito do emissor"),
 dict(g="Caixa e renda fixa", n="Poupanca", corr_fix=0, corr_pct=0,
      b3=0, entrada=0, adm=0, cust=0, nota="isenta de IR, mas rende 57% do CDI"),

 # ─ ETF Brasil ─
 dict(g="ETF na B3", n="PIBB11 — corretora taxa zero", corr_fix=0, corr_pct=0,
      b3=B3_VISTA, entrada=0, adm=0.00059, cust=None, nota="ETF mais barato da B3"),
 dict(g="ETF na B3", n="DIVO11 / IMAB11 / B5P211 — corretora zero", corr_fix=0, corr_pct=0,
      b3=B3_VISTA, entrada=0, adm=0.00040, cust=None, nota="0,04% a.a."),
 dict(g="ETF na B3", n="BOVA11 — corretora taxa zero", corr_fix=0, corr_pct=0,
      b3=B3_VISTA, entrada=0, adm=0.00100, cust=None, nota="o mais liquido da B3"),
 dict(g="ETF na B3", n="BOVA11 — XP (corretagem 0,50% em ETF)", corr_fix=0, corr_pct=0.0050,
      b3=B3_VISTA, entrada=0, adm=0.00100, cust=None, nota="0,50% na entrada E na saida"),
 dict(g="ETF na B3", n="IVVB11 (S&P 500 em BRL)", corr_fix=0, corr_pct=0,
      b3=B3_VISTA, entrada=0, adm=0.00230, cust=None, nota="sem obrigacao acessoria"),
 dict(g="ETF na B3", n="SMAL11", corr_fix=0, corr_pct=0,
      b3=B3_VISTA, entrada=0, adm=0.00500, cust=None, nota="0,50% a.a."),
 dict(g="ETF na B3", n="HASH11 (cripto)", corr_fix=0, corr_pct=0,
      b3=B3_VISTA, entrada=0, adm=0.01300, cust=None, nota="1,3% taxa maxima global"),

 # ─ Ação individual ─
 dict(g="Acao individual", n="Corretora taxa zero (Itau, C6, Inter, Rico...)", corr_fix=0, corr_pct=0,
      b3=B3_VISTA, entrada=0, adm=0, cust=None, nota="isencao de R$20 mil/mes na venda"),
 dict(g="Acao individual", n="Safra / Terra (R$ 4,50 por ordem)", corr_fix=4.50, corr_pct=0,
      b3=B3_VISTA, entrada=0, adm=0, cust=None, nota="+PIS/COFINS/ISS sobre a corretagem"),
 dict(g="Acao individual", n="XP swing trade (R$ 4,90 por ordem)", corr_fix=4.90, corr_pct=0,
      b3=B3_VISTA, entrada=0, adm=0, cust=None, nota="leitura PARCIAL — confirmar"),
 dict(g="Acao individual", n="Caixa (R$ 4,49 + 0,02%)", corr_fix=4.49, corr_pct=0.0002,
      b3=B3_VISTA, entrada=0, adm=0, cust=None, nota="FII e isento na Caixa"),

 # ─ Exterior ─
 dict(g="Exterior", n="ETF EUA — Avenue melhor degrau (0,50% + IOF 1,1%)", corr_fix=0, corr_pct=0,
      b3=0, entrada=0.0160, adm=0.00030, cust=None, nota="degrau exige volume; controlador Itau"),
 dict(g="Exterior", n="ETF EUA — Vest stablecoin (1,40%, sem IOF declarado)", corr_fix=0, corr_pct=0,
      b3=0, entrada=0.0140, adm=0.00030, cust=None, nota="custodia Northbound; corretagem US$0"),
 dict(g="Exterior", n="ETF EUA — Nomad nivel 1 (2,00% + IOF 1,1%)", corr_fix=0, corr_pct=0,
      b3=0, entrada=0.0310, adm=0.00030, cust=None, nota="custodia Apex; corretagem US$0"),
 dict(g="Exterior", n="ETF EUA — Avenue degrau inicial (1,95% + IOF 1,1%)", corr_fix=0, corr_pct=0,
      b3=0, entrada=0.0305, adm=0.00030, cust=None, nota="degrau de entrada"),
 dict(g="Exterior", n="Rota Wise como conta (0,73% + IOF 3,5%)", corr_fix=0, corr_pct=0,
      b3=0, entrada=0.0423, adm=0.00030, cust=None, nota="IOF de conta, nao de investimento"),
]

APORTES = [200, 500, 1000]

def entrada_pct(r, a):
    return (r["corr_fix"]/a) + r["corr_pct"] + r["b3"] + r["entrada"]

def meses_para_pagar(pct, taxa_aa=CDI_AA):
    """Quantos meses de rendimento bruto o custo de entrada consome."""
    if pct <= 0: return 0.0
    m = (1+taxa_aa)**(1/12) - 1
    return pct / m

print("="*100)
print("TABELA 1 — CUSTO DE ENTRADA POR APORTE (% do aporte consumido no ato da compra)")
print("="*100)
print(f"{'Rota':<52}{'R$200':>13}{'R$500':>13}{'R$1.000':>13}")
print("-"*100)
gr = None
linhas1 = []
for r in ROTAS:
    if r["g"] != gr:
        gr = r["g"]; print(f"\n[{gr}]")
    cells=[]
    for a in APORTES:
        p = entrada_pct(r,a)
        cells.append(f"{p*100:>12.3f}%")
    print(f"{r['n']:<52}" + "".join(cells))
    linhas1.append(dict(grupo=r["g"], rota=r["n"], nota=r["nota"],
        adm_aa=r["adm"], cust_aa=r["cust"],
        **{f"e{a}": entrada_pct(r,a) for a in APORTES}))

print("\n"+"="*100)
print("TABELA 2 — QUANTOS MESES DE RENDIMENTO (a 13,90% a.a.) O CUSTO DE ENTRADA CONSOME")
print("="*100)
print(f"{'Rota':<52}{'R$200':>13}{'R$500':>13}{'R$1.000':>13}")
print("-"*100)
gr=None
for r in ROTAS:
    if r["g"]!=gr: gr=r["g"]; print(f"\n[{gr}]")
    cells=[f"{meses_para_pagar(entrada_pct(r,a)):>12.1f}m" for a in APORTES]
    print(f"{r['n']:<52}" + "".join(cells))

json.dump(linhas1, open("/tmp/bastter/calc/tabela_entrada.json","w"), ensure_ascii=False, indent=1)
print("\nOK -> tabela_entrada.json")

# -*- coding: utf-8 -*-
"""Custo acumulado em 20 anos, aporte mensal. Retorno bruto identico em todas
as rotas de mesma classe — o objetivo e isolar o CUSTO, nao prever retorno."""
CDI=0.1390; B3V=0.000300; ISEN_RV=26471.77; CUST_RV=0.000500
TD_C=0.002000; TD_ISEN=10000.0

def sim(aporte, anos, corr_fix=0.0, corr_pct=0.0, b3=0.0, entrada=0.0,
        adm=0.0, cust_rv=False, cust_td=False, td_isen=False, bruto=CDI):
    """Retorna (patrimonio_final, custo_total_pago)."""
    m_bruto=(1+bruto)**(1/12)-1
    pat=0.0; custo=0.0
    for i in range(anos*12):
        liq=aporte
        c=corr_fix + aporte*(corr_pct+b3+entrada)
        c=min(c,aporte); liq-=c; custo+=c
        pat+=liq
        pat*=(1+m_bruto)
        # taxa de administracao do fundo/ETF
        if adm:
            t=pat*((1+adm)**(1/12)-1); pat-=t; custo+=t
        # custodia B3 renda variavel (progressiva, isenta ate 26.471,77)
        if cust_rv and pat>ISEN_RV:
            base=pat-ISEN_RV
            t=base*((1+CUST_RV)**(1/12)-1); pat-=t; custo+=t
        # custodia Tesouro Direto
        if cust_td:
            base=max(0.0,pat-TD_ISEN) if td_isen else pat
            t=base*((1+TD_C)**(1/12)-1); pat-=t; custo+=t
    return pat,custo

ANOS=20
CEN=[
 ("Tesouro Reserva / Selic (isencao ate R$10k)", dict(cust_td=True, td_isen=True)),
 ("Tesouro IPCA+ (0,20% desde o 1o real)",       dict(cust_td=True, td_isen=False)),
 ("Cofrinho / RDB 100% CDI",                     dict()),
 ("PIBB11 — corretora zero",                     dict(b3=B3V, adm=0.00059, cust_rv=True)),
 ("BOVA11 — corretora zero",                     dict(b3=B3V, adm=0.00100, cust_rv=True)),
 ("BOVA11 — XP (0,50% de corretagem em ETF)",    dict(b3=B3V, corr_pct=0.0050, adm=0.00100, cust_rv=True)),
 ("IVVB11 — corretora zero",                     dict(b3=B3V, adm=0.00230, cust_rv=True)),
 ("SMAL11 — corretora zero",                     dict(b3=B3V, adm=0.00500, cust_rv=True)),
 ("HASH11 — corretora zero",                     dict(b3=B3V, adm=0.01300, cust_rv=True)),
 ("Acao — corretora zero",                       dict(b3=B3V, cust_rv=True)),
 ("Acao — R$4,50 por ordem",                     dict(b3=B3V, corr_fix=4.50, cust_rv=True)),
 ("ETF EUA — Avenue melhor degrau (E=1,60%)",    dict(entrada=0.0160, adm=0.00030)),
 ("ETF EUA — Nomad nivel 1 (E=3,10%)",           dict(entrada=0.0310, adm=0.00030)),
]

for AP in (200,500,1000):
    ref,_=sim(AP,ANOS)                      # rota sem custo nenhum
    print("="*104)
    print(f"APORTE R$ {AP}/mes · {ANOS} anos · aportado R$ {AP*12*ANOS:,.0f} · "
          f"rendimento bruto 13,90% a.a. em todas as rotas")
    print(f"{'(referencia sem custo algum)':<46}{ref:>16,.0f}")
    print("-"*104)
    print(f"{'Rota':<46}{'Patrimonio':>16}{'Custo total':>15}{'% do aportado':>15}{'vs. sem custo':>13}")
    print("-"*104)
    for nome,kw in CEN:
        pat,cst=sim(AP,ANOS,**kw)
        print(f"{nome:<46}{pat:>16,.0f}{cst:>15,.0f}{cst/(AP*12*ANOS)*100:>14.1f}%{(pat-ref):>13,.0f}")
    print()

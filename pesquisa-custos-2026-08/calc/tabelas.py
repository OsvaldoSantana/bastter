# -*- coding: utf-8 -*-
"""Gera as tabelas de custo. Rotas com insumo NAO_CONFIRMADO saem da ordenacao (K-07)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import carregar, val, montar_rotas, simular, custo_entrada_pct, custo_saida_pct

C   = carregar()
B3V = val(C["b3"]["vista_total_pct"], contexto="b3")
CDI = val(C["macro"]["cdi_aa"], contexto="cdi")
ROT = montar_rotas(C)
APORTES = [200, 500, 1000]
ANOS = 20
SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(SAIDA, exist_ok=True)

def marca(r): return " " if r.confiavel else "†"

print("="*118)
print("TABELA 1 — CUSTO DE ENTRADA E SAIDA, COM A TAXA ANUAL AO LADO  (K-05, K-06)")
print("="*118)
print(f"{'Rota':<44}{'entr.200':>10}{'entr.500':>10}{'entr.1k':>10}{'saida':>10}{'adm a.a.':>11}{'':>3}")
print("-"*118)
g=None
for r in ROT:
    if r.grupo!=g: g=r.grupo; print(f"\n[{g}]")
    e=[custo_entrada_pct(r,a,B3V) for a in APORTES]
    s=custo_saida_pct(r,B3V)
    adm = f"{r.adm_aa*100:.3f}%" if r.adm_aa or not r.bloqueios else "  n/c"
    print(f"{r.nome:<44}"+"".join(f"{x*100:>9.3f}%" for x in e)+f"{s*100:>9.3f}%{adm:>11}{marca(r):>3}")
print("\n† rota com insumo NAO CONFIRMADO — fora de qualquer ordenacao. Motivos:")
for r in ROT:
    for b in r.bloqueios: print(f"   {r.nome}: {b}")

print("\n"+"="*118)
print(f"TABELA 2 — CUSTO EM {ANOS} ANOS  ·  custodia da B3 com as 10 faixas progressivas (K-03)")
print("Nao inclui IR. Os tratamentos diferem: RF regressiva 22,5→15%; ETF 15% sem isencao;")
print("acao 15% COM isencao de R$20 mil/mes na venda. (K-09)")
print("="*118)
linhas=[]
for AP in APORTES:
    ref,_,_ = simular(ROT[3], C, AP, ANOS)   # cofrinho: rota sem custo algum
    print(f"\nAPORTE R$ {AP}/mes · aportado R$ {AP*12*ANOS:,} · referencia sem custo R$ {ref:,.0f}")
    print(f"{'Rota':<44}{'Patrimonio':>15}{'Custo total':>14}{'% aportado':>12}{'vs. ref':>13}{'':>3}")
    print("-"*118)
    res=[]
    for r in ROT:
        try:
            pat,cst,al = simular(r,C,AP,ANOS)
        except Exception as e:
            print(f"{r.nome:<44}{'BLOQUEADA — '+str(e)[:55]:>60}"); continue
        res.append((r,pat,cst,al))
    conf   = sorted([x for x in res if x[0].confiavel], key=lambda x:-x[1])
    bloq   = [x for x in res if not x[0].confiavel]
    for r,pat,cst,al in conf+bloq:
        if not r.confiavel and (r,pat,cst,al)==bloq[0] if bloq else False: pass
        print(f"{r.nome:<44}{pat:>15,.0f}{cst:>14,.0f}{cst/(AP*12*ANOS)*100:>11.1f}%{pat-ref:>13,.0f}{marca(r):>3}")
        linhas.append(dict(aporte=AP, rota=r.nome, grupo=r.grupo, patrimonio=round(pat,2),
                           custo=round(cst,2), confiavel=r.confiavel, adm_aa=r.adm_aa))
    if bloq: print("   " + "-"*40 + " abaixo da linha: insumo nao confirmado")

with open(os.path.join(SAIDA,"tabelas.json"),"w",encoding="utf-8") as f:
    json.dump(linhas,f,ensure_ascii=False,indent=1)
print(f"\nOK -> {os.path.join(SAIDA,'tabelas.json')}")

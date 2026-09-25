# -*- coding: utf-8 -*-
"""Testes das camadas 1, 3 e 4 do manual: unitario, canonico com oraculo, invariante."""
import os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from motor import carregar, val, custodia_rv_aa, montar_rotas, simular, InsumoBloqueado

C = carregar()
FX   = C["b3"]["custodia_rv_faixas"]["valor"]
ISEN = C["b3"]["custodia_rv_isencao"]["valor"]

# ── camada 3 — canonicos com oraculo externo (tabela literal da B3) ───────────
def test_custodia_abaixo_da_isencao_e_zero():
    """Oraculo: B3, texto literal 'posicoes ate R$ 26.471,77 sao isentos desta taxa'."""
    assert custodia_rv_aa(26_471.77, FX, ISEN) == 0.0
    assert custodia_rv_aa(10_000.00, FX, ISEN) == 0.0

def test_custodia_primeira_faixa():
    """R$100 mil: excedente R$73.528,23, todo na faixa 1 (0,0500% a.a.)."""
    esperado = (100_000 - ISEN) * 0.000500
    assert custodia_rv_aa(100_000, FX, ISEN) == pytest.approx(esperado, rel=1e-9)

def test_custodia_atravessa_faixas():
    """R$300 mil: 115.000-26.471,77 a 0,05% + 115.000 a 0,04% + resto a 0,02%.
    Este teste teria pego K-03 — o v1 cobrava 0,05% sobre TODO o excedente."""
    esperado = (115_000-ISEN)*0.000500 + 115_000*0.000400 + (300_000-230_000)*0.000200
    assert custodia_rv_aa(300_000, FX, ISEN) == pytest.approx(esperado, rel=1e-9)
    assert custodia_rv_aa(300_000, FX, ISEN) < (300_000-ISEN)*0.000500   # < que o v1

# ── camada 4 — invariantes ────────────────────────────────────────────────────
def test_faixas_de_custodia_sao_monotonicas():
    """Nenhuma faixa e mais cara que a anterior, e os tetos sao crescentes."""
    tx = [f["taxa_aa"] for f in FX]
    assert tx == sorted(tx, reverse=True)
    tetos = [f["ate"] for f in FX if f["ate"] is not None]
    assert tetos == sorted(tetos)
    assert FX[-1]["ate"] is None          # ultima faixa e aberta

def test_invariante_cdi_diario():
    """(1+CDI_aa)^(1/252)-1 deve bater com a serie 12 do BCB (0,051660%).
    A pesquisa conferiu isto a mao uma vez; aqui roda sozinho."""
    cdi = val(C["macro"]["cdi_aa"], contexto="cdi")
    assert (1+cdi)**(1/252)-1 == pytest.approx(0.00051660, abs=1e-7)

def test_invariante_poupanca_legal():
    """Lei 12.703/2012: com Selic > 8,5%, poupanca = 0,5% a.m. + TR.
    TR de 0,1448% e poupanca de 0,6455% (series 226 e 25) devem fechar."""
    assert (1.005*1.001448)-1 == pytest.approx(0.006455, abs=1e-6)

def test_rota_com_insumo_nao_confirmado_nao_entra_na_ordenacao():
    """Teria pego K-07: a rota Vest aparecia como a mais barata do exterior
    porque um NAO CONFIRMADO estava sendo renderizado como zero."""
    rotas = montar_rotas(C)
    vest = [r for r in rotas if "Vest" in r.nome]
    assert vest and not vest[0].confiavel
    bovv = [r for r in rotas if "BOVV11" in r.nome]
    assert bovv and not bovv[0].confiavel

def test_valor_bloqueado_levanta_excecao():
    """Um calculo que depende de NAO_CONFIRMADO recusa-se a rodar, em vez de rodar com premissa."""
    with pytest.raises(InsumoBloqueado):
        val(C["etf"]["ACWI11"], contexto="acwi")
    with pytest.raises(InsumoBloqueado):
        val(C["etf"]["BOVV11"], contexto="bovv")

def test_status_parcial_pode_ser_recusado():
    with pytest.raises(InsumoBloqueado):
        val(C["corretagem"]["xp_swing"], permitir_parcial=False, contexto="xp")
    assert val(C["corretagem"]["xp_swing"], permitir_parcial=True, contexto="xp") == 4.90

def test_toda_constante_tem_procedencia():
    """Nenhum valor COMPLETO sem fonte."""
    faltando = []
    def anda(no, cam=""):
        if isinstance(no, dict):
            if "valor" in no and no.get("status") == "COMPLETO" and not no.get("fonte"):
                faltando.append(cam)
            for k, v in no.items():
                if k not in ("valor","status","fonte","acesso","expira","nota","motivo","bloqueia"):
                    anda(v, f"{cam}.{k}")
    anda(C)
    assert not faltando, f"sem fonte: {faltando}"

def test_perna_de_saida_e_contabilizada():
    """Teria pego K-06: a rota XP cobra 0,50% na entrada E na saida."""
    rotas = {r.nome: r for r in montar_rotas(C)}
    xp = rotas["BOVA11 — via XP (0,50% em ETF)"]
    assert xp.saida_pct > 0
    ext = rotas["ETF EUA (IVV) — Avenue — melhor degrau"]
    assert ext.saida_pct == pytest.approx(0.0038)   # IOF de repatriacao

def test_custodia_absorvida_zera_a_linha():
    """Itau, Safra, Caixa e outras declaram absorver a custodia da B3."""
    r = [x for x in montar_rotas(C) if x.nome == "BOVA11 — corretora zero"][0]
    p1,c1,_ = simular(r, C, 1000, 20, custodia_absorvida=False)
    p2,c2,_ = simular(r, C, 1000, 20, custodia_absorvida=True)
    assert c2 < c1 and p2 > p1

# -*- coding: utf-8 -*-
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from motor import carregar as carregar_custos
from alocacao import catalogo, carregar_politica
from sleeve import expandir_sleeve, premio_de_diversificacao, verificar_decisao, DecisaoPendente

C, P = carregar_custos(), carregar_politica()
R = {r.id: r for r in catalogo(C)}

def test_decisao_pendente_bloqueia_selecao_de_empresas():
    """O motor aloca para a sleeve mas RECUSA-SE a nomear empresas enquanto A-05 estiver aberta."""
    with pytest.raises(DecisaoPendente):
        verificar_decisao(P, "A05_nucleo_indexado_vs_selecao_ativa")
    e = expandir_sleeve(R["acao_zero"], 0.105, P, C, 500, 20)
    assert e["bloqueado"] is True
    assert e["exige_selecao"] is True

def test_etf_nao_exige_selecao():
    e = expandir_sleeve(R["bova11"], 0.105, P, C, 500, 20)
    assert e["exige_selecao"] is False
    assert e["bloqueado"] is False

def test_n_minimo_vem_do_teto_por_papel():
    for peso in (0.05, 0.105, 0.129, 0.30):
        e = expandir_sleeve(R["acao_zero"], peso, P, C, 500, 20)
        assert e["n_minimo_pelo_teto"] == math.ceil(peso/P["tetos"]["por_ativo_pct_patrimonio"])

def test_acao_e_mais_barata_que_qualquer_etf():
    """O achado que torna A-05 uma decisao real e nao retorica."""
    d = premio_de_diversificacao(C, P, 500, 20)
    assert d["arrasto_acao"] < d["arrasto_etf"]
    assert d["custo_extra_reais"] > 0

def test_premio_e_proporcional_ao_aporte():
    """Como os dois custos sao percentuais, o premio em % do aportado nao muda com o tamanho."""
    a = premio_de_diversificacao(C, P, 200, 20)["pct_do_aportado"]
    b = premio_de_diversificacao(C, P, 2000, 20)["pct_do_aportado"]
    assert abs(a-b) < 0.05

def test_decisao_resolvida_desbloqueia():
    P2 = {**P, "decisoes": {**P["decisoes"],
        "A05_nucleo_indexado_vs_selecao_ativa": {
            **P["decisoes"]["A05_nucleo_indexado_vs_selecao_ativa"], "status": "RESOLVIDA"}}}
    e = expandir_sleeve(R["acao_zero"], 0.105, P2, C, 500, 20)
    assert e["bloqueado"] is False

# -*- coding: utf-8 -*-
"""A medicao da P-145 sem rede: classificacao, leituras fixadas e o que a saida nao carrega."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p145_ponte_2013_2019 as M  # noqa: E402

CNPJ_A, CNPJ_B, CNPJ_C = "11.111.111/0001-11", "22.222.222/0001-22", "33.333.333/0001-33"


def _d(c):
    return "".join(x for x in c if x.isdigit())


def test_as_duas_leituras_da_secao_2_estao_fixadas():
    """Decisao dele de 25/09. Se alguem trocar a janela, a medicao deixa de ser a
    pre-registrada -- e o teste diz isso em vez de medir outra coisa em silencio."""
    assert M.JANELA == "t-2..t"
    assert M.U.JANELAS[M.JANELA] == (2, 0)
    # >= mediana inclusiva: com volumes 1, 2, 3 a mediana e 2 e o 2 fica
    dias = [M.U.dt.date(2013, 1, d) for d in (2, 3)]
    vol = {"AAAA3": {d: 1.0 for d in dias}, "BBBB3": {d: 2.0 for d in dias},
           "CCCC3": {d: 3.0 for d in dias}}
    ident = {k: (f"BR{k[:4]}ACNOR1", k) for k in vol}
    u = M.U.universo((2013, 1), vol, ident, set(dias), M.JANELA)
    assert set(u) == {"BBBB", "CCCC"}


def test_classificar_as_cinco_categorias():
    isin = {"MANU": CNPJ_A, "BOAS": CNPJ_A, "RENO": CNPJ_B, "REAP": CNPJ_C}
    manual = {"MANU": CNPJ_A}
    cdcvm = {_d(CNPJ_A): "1", _d(CNPJ_B): "2"}
    nomes = {_d(CNPJ_A): "BOA SORTE S.A. BOA SORTE", _d(CNPJ_B): "NOVO NOME S.A."}
    nomres = {"BOAS": "BOA SORTE", "RENO": "ANTIGA MARCA", "REAP": "X", "SUMI": "Y"}
    c = M.classificar(["MANU", "BOAS", "RENO", "REAP", "SUMI"], isin, manual, cdcvm, nomes,
                      nomres)
    assert c == {"MANU": "MANUAL", "BOAS": "LIGADO_NOME_CONFERE",
                 "RENO": "LIGADO_NOME_DIVERGE", "REAP": "CNPJ_SEM_CVM",
                 "SUMI": "AUSENTE_DO_ISIN"}
    assert set(c.values()) == set(M.CATEGORIAS)


def test_palavra_generica_nao_casa_nome():
    """Sem a lista de genericas, "CIA" e "SA" fariam quase todo par "conferir"."""
    assert M.tokens("CIA BRASILEIRA DE DISTRIB S.A.") == {"DISTRIB"}
    assert not (M.tokens("CIA HERING") & M.tokens("CIA SIDERURGICA NACIONAL"))


def test_a_saida_nao_carrega_preco_nem_volume():
    """A saida vai para um repositorio publico (P-136). O relatorio so recebe contagens e
    rotulos; este teste prende o que ele imprime."""
    serie = {(2013, 1): (3, 2, 1, ["SUMI"])}
    classe = {"BOAS": "LIGADO_NOME_CONFERE", "SUMI": "AUSENTE_DO_ISIN"}
    txt = M.relatorio(serie, classe, {"BOAS": "BOA SORTE", "SUMI": "Y"},
                      {"BOAS": 1, "SUMI": 1}, {"isin isinp.zip": "ab" * 32})
    assert "RESUMO: 2 emissores" in txt and "pior mes 2013-01, 2/3" in txt
    for proibido in ("VOLTOT", "PREULT", "PREMED", "QUATOT", "R$"):
        assert proibido not in txt


def test_conferir_insumos_acusa_o_que_o_acervo_nao_conhece(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    pins = {"cotahist": {a: {"arquivo": f"COTAHIST_A{a}.ZIP", "sha256": "0" * 64}
                         for a in M.ANOS_COTAHIST if a != 2015}}
    faltas = M.conferir_insumos(repo=str(tmp_path), pins=pins)
    assert any("isin/isinp.zip" in f for f in faltas)
    assert any(f.startswith("COTAHIST 2015: sem pin") for f in faltas)
    assert len(faltas) == len(M.INSUMOS) + len(M.ANOS_COTAHIST)

# -*- coding: utf-8 -*-
"""O n do JCP por ano sai do silver sem ler preco (P-115, secao 9 do criterio v2).

O QUE MEDE (P5): (1) com as colunas de valor, preco e fator ENVENENADAS -- qualquer leitura
levanta erro --, a contagem sai certa; (2) a unidade e o papel-dia "so JCP, dia limpo", e a
mesma linha pelas duas esteiras conta uma vez (A-13); (3) a regra da janela escolhe a menor
candidata com n >= 1.648, e cai em 2016-2020 quando nenhuma atende; (4) o texto cita o mesmo
limiar. NAO mede o silver real: ele mora no disco dele, e o script nao roda aqui.
"""
from __future__ import annotations

import csv
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import c02_contar_n as N  # noqa: E402

TEXTO = os.path.join(os.path.dirname(AQUI), "docs", "auditoria",
                     "C02-CRITERIO-V2-PREREGISTRO.md")


class PrecoLido(AssertionError):
    pass


class Envenenada(dict):
    """Uma linha do silver em que so as colunas permitidas se deixam ler."""

    def __getitem__(self, k):
        if k not in N.LIDAS:
            raise PrecoLido(k)
        return super().__getitem__(k)

    def get(self, k, padrao=None):
        if k not in N.LIDAS:
            raise PrecoLido(k)
        return super().get(k, padrao)

    def items(self):
        raise PrecoLido("items")

    def values(self):
        raise PrecoLido("values")


def _linha(cod, ts, tipo, data_ex, ultimo="", origem="paginado"):
    return Envenenada(origem=origem, cod=cod, type_stock=ts, tipo=tipo, data_ex=data_ex,
                      ultimo_dia_com_direito=ultimo or data_ex, valor="VENENO",
                      preco_vespera="VENENO", fator="VENENO", ratio="VENENO")


LINHAS = [
    # 2016: dois so-JCP limpos (PETR ON e PN sao papeis diferentes)
    _linha("PETR", "ON", "JRS CAP PROPRIO", "2016-05-02"),
    _linha("PETR", "PN", "JRS CAP PROPRIO", "2016-05-02"),
    # a mesma linha pelas duas esteiras: conta uma vez (A-13)
    _linha("PETR", "PN", "JRS CAP PROPRIO", "2016-05-02", origem="suplemento"),
    # JCP com dividendo no mesmo papel-dia: nao e "so JCP"; nem "so dividendo"
    _linha("VALE", "ON", "JRS CAP PROPRIO", "2016-06-01"),
    _linha("VALE", "ON", "DIVIDENDO", "2016-06-01"),
    # JCP com desdobramento no mesmo dia: dia sujo
    _linha("ITUB", "PN", "JRS CAP PROPRIO", "2016-07-01"),
    _linha("ITUB", "PN", "DESDOBRAMENTO", "2016-07-01"),
    # dividendo limpo
    _linha("BBAS", "ON", "DIVIDENDO", "2016-08-01"),
    # 2013 sem data_ex (calendario nao cobria): o ano sai do ultimo dia com direito
    _linha("ABEV", "ON", "JRS CAP PROPRIO", "", ultimo="2013-12-27"),
    # rendimento de FII nao e JCP nem dividendo
    _linha("HGLG", "CI", "RENDIMENTO", "2016-09-01"),
]


def test_o_veneno_funciona():
    """Vacuidade: se a linha envenenada deixasse ler o preco, o teste abaixo nao provaria
    nada."""
    with pytest.raises(PrecoLido):
        LINHAS[0]["valor"]
    with pytest.raises(PrecoLido):
        LINHAS[0].get("preco_vespera")


def test_conta_certo_sem_ler_preco():
    c = N.contar(LINHAS)
    assert c[2016] == dict(jcp=4, so_jcp_limpo=2, div=2, so_div_limpo=1, pela_data_com=0)
    assert c[2013] == dict(jcp=1, so_jcp_limpo=1, div=0, so_div_limpo=0, pela_data_com=1)


def test_ler_devolve_so_as_colunas_permitidas(tmp_path):
    p = tmp_path / "silver.csv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["origem", "cod", "type_stock", "tipo", "ultimo_dia_com_direito",
                    "data_ex", "valor", "preco_vespera", "fator"])
        w.writerow(["paginado", "PETR", "PN", "JRS CAP PROPRIO", "2016-04-29", "2016-05-02",
                    "VENENO", "VENENO", "VENENO"])
    linhas = list(N.ler(str(p)))
    assert linhas == [dict(cod="PETR", type_stock="PN", tipo="JRS CAP PROPRIO",
                           data_ex="2016-05-02", ultimo_dia_com_direito="2016-04-29")]


def test_silver_sem_coluna_obrigatoria_recusa(tmp_path):
    p = tmp_path / "silver.csv"
    p.write_text("cod,tipo\nPETR,DIVIDENDO\n", encoding="utf-8")
    with pytest.raises(N.SilverIncompleto):
        list(N.ler(str(p)))


def test_limiar_da_regra():
    assert N.N_MIN == 1648


def _cont(por_ano):
    return {a: dict(jcp=n, so_jcp_limpo=n, div=0, so_div_limpo=0, pela_data_com=0)
            for a, n in por_ano.items()}


def test_regra_escolhe_a_menor_janela_que_atende():
    c = _cont({2013: 300, 2014: 300, 2015: 300, 2016: 250, 2017: 250, 2018: 250,
               2019: 250, 2020: 250})
    # 2016-2020 = 1250; 2015-2020 = 1550; 2014-2020 = 1850 -> atende
    assert N.janela(c) == dict(ini=2014, fim=2020, n=1850, atende=True)


def test_regra_sem_candidata_que_atenda_cai_em_2016_2020():
    c = _cont({a: 100 for a in range(2013, 2021)})
    assert N.janela(c) == dict(ini=2016, fim=2020, n=500, atende=False)


def test_regra_a_original_ja_basta():
    c = _cont({a: 400 for a in range(2013, 2021)})
    assert N.janela(c) == dict(ini=2016, fim=2020, n=2000, atende=True)


def test_o_texto_cita_o_mesmo_limiar_e_as_mesmas_candidatas():
    with open(TEXTO, encoding="utf-8") as f:
        s = f.read()
    assert "n_JCP ≥ 1.648" in s
    assert "2016–2020, 2015–2020, 2014–2020 e 2013–2020" in s
    assert N.CANDIDATAS == ((2016, 2020), (2015, 2020), (2014, 2020), (2013, 2020))

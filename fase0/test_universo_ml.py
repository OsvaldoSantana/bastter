# -*- coding: utf-8 -*-
"""P-143 / P-132: o universo da secao 2 e a cobertura da emenda 1. Dado sintetico para as
regras; um teste REAL para a ponte manual contra o cadastro da CVM."""
import csv
import datetime as dt
import os
import sys
import zipfile

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import universo_ml as U  # noqa: E402
from acervo_de_teste import exigir_acervo  # noqa: E402

D = dt.date


def test_emissor_e_posicional_no_ISIN():
    assert U.emissor_do_isin("BRPETRACNPR6") == "PETR"
    assert U.emissor_do_isin("US0378331005") is None       # nao brasileiro
    assert U.emissor_do_isin("BRPETR") is None              # cortado
    assert U.emissor_do_isin("") is None


def _dias(ano, mes, n):
    return [D(ano, mes, d) for d in range(1, n + 1)]


def _mercado():
    """3 meses (out-dez/2010), 10 pregoes cada. AAAA3 negocia tudo e muito; BBBB3 negocia
    tudo e pouco; CCCC3 negocia 80%; AAAA4 e a outra classe da mesma empresa."""
    dias = _dias(2010, 10, 10) + _dias(2010, 11, 10) + _dias(2010, 12, 10)
    vol = {"AAAA3": {d: 100.0 for d in dias}, "AAAA4": {d: 50.0 for d in dias},
           "BBBB3": {d: 1.0 for d in dias}, "CCCC3": {d: 500.0 for d in dias[:24]}}
    ident = {"AAAA3": ("BRAAAAACNOR1", "A"), "AAAA4": ("BRAAAAACNPR1", "A"),
             "BBBB3": ("BRBBBBACNOR1", "B"), "CCCC3": ("BRCCCCACNOR1", "C")}
    return vol, ident, set(dias)


def test_universo_filtra_pregoes_volume_e_uma_classe_por_empresa():
    vol, ident, dias = _mercado()
    u = U.universo((2010, 12), vol, ident, dias, "t-2..t")
    # CCCC3 sai pelos 90% (24 de 30); BBBB3 sai pela mediana; AAAA fica UMA vez, na classe
    # mais liquida
    assert u == {"AAAA": "AAAA3"}


def test_as_duas_janelas_olham_meses_diferentes():
    """CCCC3 nao negocia em dezembro. Na janela que termina em t (out-dez) ela sai pelos
    90%; na que termina em t-1 (set-nov, sem pregao em set neste mercado) ela entra."""
    vol, ident, dias = _mercado()
    assert U.universo((2010, 12), vol, ident, dias, "t-3..t-1") == {"AAAA": "AAAA3",
                                                                     "CCCC": "CCCC3"}
    assert U.universo((2011, 1), vol, ident, dias, "t-3..t-1") == {"AAAA": "AAAA3"}


def test_sem_ponte_conta_como_SEM_documento():
    univ = {"AAAA": "AAAA3", "ZZZZ": "ZZZZ3"}
    ponte = {"AAAA": "11.111.111/0001-11"}
    n, com_id, com_doc, sem = U.cobertura((2011, 3), univ, D(2011, 3, 31), ponte,
                                          {"11111111000111": D(2011, 2, 1)},
                                          {"11111111000111": "1"})
    assert (n, com_id, com_doc, sem) == (2, 1, 1, ["ZZZZ"])


def test_documento_depois_da_decisao_nao_conta():
    n, _i, doc, _s = U.cobertura((2011, 3), {"AAAA": "AAAA3"}, D(2011, 3, 31),
                                 {"AAAA": "1"}, {"1": D(2011, 4, 1)}, {"1": "9"})
    assert (n, doc) == (1, 0)


def test_mes_da_emenda_e_o_PRIMEIRO_que_passa_e_nao_volta_atras():
    serie = {(2011, 2): (10, 10, 8, []), (2011, 3): (10, 10, 9, []),
             (2011, 4): (10, 10, 8, [])}
    assert U.mes_da_emenda(serie) == (2011, 3)
    assert U.mes_da_emenda({(2011, 2): (10, 10, 8, [])}) is None


def test_a_ponte_MANUAL_vence_o_EMISSOR_txt(tmp_path):
    """O caso do codigo reaproveitado: EMBR no EMISSOR.TXT de hoje e a Embrast Ltda."""
    z = tmp_path / "isinp.zip"
    with zipfile.ZipFile(z, "w") as f:
        f.writestr("EMISSOR.TXT", '"EMBR","EMBRAST LTDA","04310364000129","20180628"\n'
                                  '"PETR","PETROBRAS","33000167000101","20180628"\n')
    m = tmp_path / "ponte.yaml"
    m.write_text(yaml.safe_dump({"ponte": {"EMBR": {"cnpj": "07.689.002/0001-89",
                                                    "cd_cvm": 20087, "motivo": "x"}}}),
                 encoding="utf-8")
    p = U.ponte_emissor_cnpj(str(z), str(m))
    assert p["EMBR"] == "07.689.002/0001-89" and p["PETR"] == "33000167000101"


@pytest.mark.slow
def test_REAL_toda_linha_da_ponte_manual_existe_no_cadastro_da_CVM():
    """Cada (cnpj, cd_cvm) escrito a mao tem de existir no cad_cia_aberta. Foi assim que os
    CNPJs digitados de memoria foram conferidos em 25/09 -- 42 de 42."""
    cad_csv = os.path.join(U.CVM, "cad", "cad_cia_aberta.csv")
    exigir_acervo(cad_csv)
    pares = set()
    with open(cad_csv, encoding="latin-1") as f:
        for r in csv.DictReader(f, delimiter=";"):
            pares.add((r["CNPJ_CIA"], r["CD_CVM"]))
    with open(U.PONTE_MANUAL, encoding="utf-8") as f:
        ponte = yaml.safe_load(f)["ponte"]
    fora = [em for em, v in ponte.items() if (v["cnpj"], str(v["cd_cvm"])) not in pares]
    assert not fora, fora

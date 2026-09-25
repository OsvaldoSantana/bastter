# -*- coding: utf-8 -*-
"""O verificador de vencimento do job semanal (P7)."""
import datetime as dt
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expira_proxima as E  # noqa: E402

HOJE = dt.date(2026, 9, 25)


def test_pega_o_que_vence_na_janela_e_ignora_o_resto():
    dados = {"macro": {
        "poupanca_am": {"valor": 0.006, "expira": dt.date(2026, 9, 28)},
        "cdi_aa": {"valor": 0.14, "expira": dt.date(2026, 12, 4)},
        "lei": {"valor": 0.15, "expira": None},
        "velha": {"valor": 1, "expira": dt.date(2026, 9, 1)}}}
    assert E.vencendo(dados, HOJE, 7) == [("macro.velha", dt.date(2026, 9, 1)),
                                          ("macro.poupanca_am", dt.date(2026, 9, 28))]


def test_expira_em_TEXTO_nao_e_lido_como_data():
    """O P-70 ja reprova texto; aqui ele nao vira falso vencimento nem cai calado no meio."""
    assert E.vencendo({"x": {"valor": 1, "expira": "2026-09-26"}}, HOJE, 7) == []


def test_no_repositorio_a_poupanca_de_28_09_aparece_em_25_09():
    r = subprocess.run([sys.executable, E.__file__, "--hoje", "2026-09-25"],
                       capture_output=True, text=True, check=True)
    assert "poupanca_am" in r.stdout and "2026-09-28" in r.stdout

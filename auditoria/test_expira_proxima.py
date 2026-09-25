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


def test_no_repositorio_a_poupanca_aparece_tres_dias_antes_de_vencer():
    """Era "a de 28/09 aparece em 25/09" -- e quebrou no dia em que a poupanca foi
    renovada (25/09, vence 24/10), sem a ferramenta mudar. O `expira` e lido do arquivo:
    o teste mede a ferramenta, nao a data de hoje."""
    import yaml
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(raiz, "alocacao", "custos.yaml"), encoding="utf-8") as f:
        expira = yaml.safe_load(f)["macro"]["poupanca_am"]["expira"]
    hoje = expira - dt.timedelta(days=3)
    r = subprocess.run([sys.executable, E.__file__, "--hoje", hoje.isoformat()],
                       capture_output=True, text=True, check=True)
    assert "poupanca_am" in r.stdout and expira.isoformat() in r.stdout

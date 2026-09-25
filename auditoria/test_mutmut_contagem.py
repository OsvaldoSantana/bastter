#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A contagem do mutmut e o portao "nada testado -> vermelho" (F-02 na mutacao)."""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutmut_contagem as mc  # noqa: E402

# Recorte da tabela do mutmut 3.8 (mutmut/stats.py), so para o teste. O main usa a dele.
STATUS = {1: "killed", 3: "killed", 0: "survived", None: "not checked", 33: "no tests",
          34: "skipped", 36: "timeout"}.__getitem__


def _meta(pasta, rel, codigos):
    p = pasta / (rel + ".meta")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"exit_code_by_key": codigos, "durations_by_key": {}}),
                 encoding="utf-8")


def test_conta_por_status_em_todos_os_meta(tmp_path):
    _meta(tmp_path, "fase0/ajustar.py", {"a__mutmut_1": 1, "a__mutmut_2": 0, "a__mutmut_3": 3})
    _meta(tmp_path, "alocacao/estado_io.py", {"e__mutmut_1": 36, "e__mutmut_2": None})
    c = mc.contar(str(tmp_path), STATUS)
    assert (c["gerados"], c["testados"], c["killed"], c["survived"], c["timeout"],
            c["not checked"]) == (5, 4, 2, 1, 1, 1)


def test_nada_testado_e_vermelho_mesmo_com_mutantes_gerados(tmp_path, capsys):
    _meta(tmp_path, "fase0/ajustar.py", {"a__mutmut_1": None, "a__mutmut_2": 33})
    assert mc.main(["--pasta", str(tmp_path)], status_de=STATUS) == 1
    saida = capsys.readouterr().out
    assert "::notice title=Mutacao::gerados=2 testados=0" in saida
    assert "::error" in saida


def test_sem_pasta_de_mutantes_e_vermelho(tmp_path, capsys):
    """O caso dos 46 s: o mutmut sai antes de gerar. Zero gerados nao e zero sobreviventes."""
    assert mc.main(["--pasta", str(tmp_path / "mutants")], status_de=STATUS) == 1
    assert "gerados=0" in capsys.readouterr().out


def test_com_algo_testado_e_verde_e_publica_a_contagem(tmp_path, capsys):
    _meta(tmp_path, "x.py", {"m1": 1, "m2": 0})
    assert mc.main(["--pasta", str(tmp_path), "--saida-mutmut", "0"], status_de=STATUS) == 0
    out = capsys.readouterr().out
    assert "killed=1 survived=1" in out and "mutmut_run_saiu=0" in out
    assert "::error" not in out

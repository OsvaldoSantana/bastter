# -*- coding: utf-8 -*-
"""P-149: o `cenarios.py` e comando do CLAUDE.md, secao 3, e caia no `main` sem teste nenhum
que o rodasse -- a P-80 (a rotina mede um terco) na forma de um script de exemplo."""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def test_P149_cenarios_roda_ate_o_fim():
    r = subprocess.run([sys.executable, "cenarios.py"], cwd=AQUI, capture_output=True,
                       text=True, timeout=120)
    assert r.returncode == 0, r.stderr[-2000:]
    # os seis cenarios ate o fim, nao so o primeiro; os dois primeiros encerram na fase de
    # APORTE (reserva, divida) e nao chegam a alocacao -- por isso a conta e pelo titulo
    assert all(f"CENARIO {i} " in r.stdout for i in range(1, 7)), r.stdout[-1500:]

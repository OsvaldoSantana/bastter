# -*- coding: utf-8 -*-
"""P-125 -- `calendario.conferir_cabecalho` devolvia `'.202'` como ano de 2026.

O header e `00COTAHIST.AAAABOVESPA AAAAMMDD`: `00` em 0-1, `COTAHIST` em 2-9, o PONTO em
10, o ano em 11-14. A fatia era [10:14] -- pegava o ponto e perdia o ultimo digito. A
docstring prometia devolver o ano, e ninguem lia o retorno: `registros()` so usa a funcao
para levantar. E o arquivo declarando o que o codigo nao faz, mudo porque o retorno nao
tinha consumidor (P-77/P-106). O primeiro consumidor e o `nomear_extracoes.py`, que
compara o ano do cabecalho com o do nome: com o defeito, TODA copia seria recusada.
"""
from __future__ import annotations
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendario as C    # noqa: E402


@pytest.mark.parametrize("ano, gerado", [
    ("2026", "20260918"),
    ("1986", "19991210"),
    ("2001", "20060331"),
    ("2023", "20231228"),
])
def test_P125_o_ano_e_o_ano_e_nao_o_ponto_antes_dele(ano, gerado):
    """O portao. Reprova contra a versao anterior, que devolvia ('.202', ...)."""
    cab = ("00COTAHIST.%sBOVESPA %s" % (ano, gerado)).ljust(245)
    assert C.conferir_cabecalho(cab, "x") == (ano, gerado)


def test_P125_o_ano_devolvido_e_quatro_digitos():
    """A forma, alem do valor: um ano com ponto nao e ano, seja qual for o digito."""
    ano, _ = C.conferir_cabecalho("00COTAHIST.1994BOVESPA 19991210".ljust(245), "x")
    assert len(ano) == 4 and ano.isdigit()


def test_P125_header_do_zip_sintetico_devolve_o_ano(tmp_path):
    """Pelo caminho que o leitor usa: o header lido do membro do ZIP."""
    import zipfile
    z = tmp_path / "COTAHIST_A2026.ZIP"
    with zipfile.ZipFile(z, "w") as f:
        f.writestr("COTAHIST_A2026.TXT",
                   "00COTAHIST.2026BOVESPA 20260918".ljust(245) + "\r\n")
    with zipfile.ZipFile(z) as f:
        with f.open(C.membro_do_zip(f)) as m:
            primeira = m.readline().decode("latin-1")
    assert C.conferir_cabecalho(primeira, str(z))[0] == "2026"

# -*- coding: utf-8 -*-
"""P-121 -- `calendario.arquivos()` aceitava PASTA com nome de ano como arquivo de COTAHIST.

O filtro era so o NOME (`ano_de`), e o nome e a propriedade que qualquer coisa pode ter.
Desde 21/09/2026 o acervo tem `COTAHIST_A2026/` -- a extracao do ZIP rebaixado -- ao lado
do `COTAHIST_A2026.ZIP`. Ela nao entrava por acidente: `sorted()` poe a pasta antes do ZIP,
e o ZIP de mesmo ano sobrescreve. Um ano com so a pasta devolveria um DIRETORIO, e o
`registros()` quebraria longe daqui, com um erro que nao diz qual regra falhou.

Mesma licao da P-99, um nivel abaixo: la *"nome e a propriedade que varia; leiaute e a que
identifica"*; aqui, antes do leiaute, *o nome nem diz se e arquivo*.
"""
from __future__ import annotations
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendario as C    # noqa: E402

RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACERVO_REAL = os.path.join(RAIZ_REPO, "data", "bronze", "b3", "cotahist")


def test_P121_pasta_so_com_nome_de_ano_NAO_entra(tmp_path):
    """O portao. Reprova contra a versao de 23/09 manha, que devolvia
    `{"COTAHIST_A2027": ".../COTAHIST_A2027"}` -- um diretorio."""
    (tmp_path / "COTAHIST_A2027").mkdir()
    (tmp_path / "COTAHIST_A2027" / "COTAHIST_A2027.TXT").write_bytes(b"")
    assert C.arquivos(str(tmp_path)) == {}


def test_P121_pasta_com_nome_de_ZIP_nao_desbanca_o_arquivo_de_verdade(tmp_path):
    """A forma que reprovava com um arquivo presente: o `.TXT` entra primeiro, e a pasta
    `COTAHIST_A2027.ZIP/` -- ordenada depois e com cara de ZIP -- tomava o lugar dele."""
    txt = tmp_path / "COTAHIST_A2027.TXT"
    txt.write_bytes(b"")
    (tmp_path / "COTAHIST_A2027.ZIP").mkdir()
    assert C.arquivos(str(tmp_path)) == {"COTAHIST_A2027": str(txt)}


def test_P121_a_pasta_ao_lado_do_ZIP_continua_perdendo_para_o_ZIP(tmp_path):
    """O estado real do acervo. Passava antes por acidente de ordenacao; tem de continuar
    passando pelo motivo certo."""
    (tmp_path / "COTAHIST_A2026").mkdir()
    zp = tmp_path / "COTAHIST_A2026.ZIP"
    zp.write_bytes(b"")
    assert C.arquivos(str(tmp_path)) == {"COTAHIST_A2026": str(zp)}


@pytest.mark.skipif(not os.path.isdir(ACERVO_REAL),
                    reason="acervo COTAHIST ausente nesta maquina")
def test_P121_no_acervo_real_todo_caminho_devolvido_e_arquivo():
    achados = C.arquivos(ACERVO_REAL)
    assert achados, "acervo presente e nenhum COTAHIST achado -- vacuidade"
    assert [c for c in achados.values() if not os.path.isfile(c)] == []

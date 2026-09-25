# -*- coding: utf-8 -*-
"""P-142: o helper que decide quando um teste de acervo real pode pular, e a guarda que
impede o `skipif` de voltar aos arquivos com `test_REAL_*`."""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from acervo_de_teste import exigir_acervo  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))


def test_sem_pasta_de_acervo_PULA(tmp_path):
    with pytest.raises(pytest.skip.Exception, match="NAO RODOU"):
        exigir_acervo(str(tmp_path / "data" / "x.csv"), raiz=str(tmp_path / "data"))


def test_pasta_presente_e_arquivo_ausente_FALHA(tmp_path):
    """O caso da P-142: o acervo esta na maquina, o teste procura no lugar errado."""
    (tmp_path / "data").mkdir()
    with pytest.raises(pytest.fail.Exception, match="P-142"):
        exigir_acervo(str(tmp_path / "data" / "bronze" / "b3" / "COTAHIST_A2023.ZIP"),
                      raiz=str(tmp_path / "data"))


def test_tudo_presente_segue(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "x.csv").write_text("a\n", encoding="utf-8")
    exigir_acervo(str(tmp_path / "data" / "x.csv"), raiz=str(tmp_path / "data"))


def test_todo_arquivo_com_test_REAL_usa_o_helper_e_nenhum_skip():
    """A guarda da classe. Um `skipif(not os.path.isfile(...))` num arquivo de testes REAL e
    a forma exata da P-142: pula na maquina que tem o acervo, e ninguem le o motivo."""
    ruins = {}
    for nome in sorted(os.listdir(AQUI)):
        if not (nome.startswith("test_") and nome.endswith(".py")) or \
                nome == os.path.basename(__file__):
            continue
        with open(os.path.join(AQUI, nome), encoding="utf-8") as f:
            texto = f.read()
        if not re.search(r"^def test_\w*REAL", texto, re.M):
            continue
        motivos = []
        if "exigir_acervo(" not in texto:
            motivos.append("nao chama exigir_acervo")
        if re.search(r"pytest\.mark\.skipif\(|pytest\.skip\(", texto):
            motivos.append("usa skipif/skip")
        if motivos:
            ruins[nome] = motivos
    assert not ruins, ruins

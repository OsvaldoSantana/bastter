# -*- coding: utf-8 -*-
"""P-141 (25/09/2026): o executor paralelo da suite NAO entra na impressao do ambiente.

O pedido foi "pytest-xdist no grupo de desenvolvimento". O grupo `dev` e lido por
`ambiente.declarado()`, e a impressao que ele produz (7565df1381e2c1ed) esta gravada em
resultados pre-registrados. Um executor de teste nao muda numero nenhum; se mudasse a
impressao, o resultado passaria a acusar "ambiente diferente" sem que nada nele mudasse
-- um alarme falso no instrumento que existe para acusar a mudanca verdadeira."""
import os
import shutil
import tomllib

import ambiente

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def _pyproject():
    with open(os.path.join(RAIZ, "pyproject.toml"), "rb") as f:
        return tomllib.load(f)


def test_P141_xdist_mora_no_grupo_paralelo_com_pino_exato():
    grupo = _pyproject()["project"]["optional-dependencies"]["paralelo"]
    assert any(x.startswith("pytest-xdist==") for x in grupo), grupo
    assert all("==" in x for x in grupo), "sem pino, um pip install amanha muda o executor"


def test_P141_xdist_fora_da_impressao_do_ambiente():
    assert "pytest-xdist" not in ambiente.declarado()["versoes"], (
        "pytest-xdist entrou em dependencies/dev e mudou a impressao do ambiente. O lugar "
        "dele e o grupo `paralelo`.")


def test_P141_MUTACAO_xdist_em_dev_mudaria_a_impressao(tmp_path):
    """A razao da guarda, medida: o mesmo pyproject com o xdist em `dev` imprime outro."""
    copia = tmp_path / "pyproject.toml"
    shutil.copy(os.path.join(RAIZ, "pyproject.toml"), copia)
    texto = copia.read_text(encoding="utf-8")
    alvo = '"pytest==9.1.1",'
    assert texto.count(alvo) == 1
    copia.write_text(texto.replace(alvo, alvo + ' "pytest-xdist==3.8.0",'), encoding="utf-8")
    assert ambiente.impressao(str(copia)) != ambiente.impressao()

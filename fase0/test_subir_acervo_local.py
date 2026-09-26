# -*- coding: utf-8 -*-
"""Testes da carga inicial -- um acervo falso em `tmp_path` e o `ArmazemMemoria`."""
from __future__ import annotations

import hashlib
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import acervo as V  # noqa: E402
import armazem as A  # noqa: E402
import subir_acervo_local as S  # noqa: E402


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _acervo(tmp_path, snapshot_mente=False):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    b = tmp_path / "data" / "bronze"
    dfp = b / "cvm" / "dfp"
    (dfp / "_snapshots").mkdir(parents=True)
    (dfp / "dfp_cia_aberta_2024.zip").write_bytes(b"vigente")
    velho = b"de 13/09"
    sha12 = ("0" * 12) if snapshot_mente else _sha(velho)[:12]
    (dfp / "_snapshots" / f"dfp_cia_aberta_2024__v20260913__{sha12}.zip").write_bytes(velho)
    (b / "cvm" / "cad").mkdir(parents=True)
    (b / "cvm" / "cad" / "cad_cia_aberta.csv").write_bytes(b"CNPJ;X\n")
    (b / "cvm" / "_manifest").mkdir()                 # fora de dfp/itr/cad: ignorado
    (b / "b3" / "cotahist").mkdir(parents=True)
    (b / "b3" / "cotahist" / "COTAHIST_A1986.ZIP").write_bytes(b"1986")
    (b / "b3" / "cotahist" / "notas.txt").write_bytes(b"?")
    return str(tmp_path)


def test_plano_nao_envia_nada_e_da_chave_de_conteudo_a_cada_versao(tmp_path):
    repo = _acervo(tmp_path)
    arm = A.ArmazemMemoria()
    assert S.main([], armazem=arm, repo=repo) == 0
    assert arm.objetos == {}
    assert not os.path.exists(S.inventario(repo, "cvm"))
    itens = {(x["recurso"], x["papel"]): x for x in S.plano(repo) if x["acao"] == S.SUBIR}
    snap = itens[("dfp", "snapshot")]
    assert snap["arquivo"] == "dfp_cia_aberta_2024.zip", "o snapshot volta ao nome canonico"
    assert snap["chave"] == A.chave("cvm", "dfp", "dfp_cia_aberta_2024.zip", _sha(b"de 13/09"))
    assert itens[("cotahist", "canonico")]["chave"].startswith("b3/cotahist/COTAHIST_A1986.ZIP/")


def test_arquivo_fora_da_convencao_e_desconhecido_e_nao_sobe(tmp_path):
    repo = _acervo(tmp_path)
    desc = [x for x in S.plano(repo) if x["acao"] == S.DESCONHECIDO]
    assert [os.path.basename(x["caminho"]) for x in desc] == ["notas.txt"]


def test_aplicar_sobe_grava_inventario_e_repetir_nao_muda_nada(tmp_path):
    repo = _acervo(tmp_path)
    arm = A.ArmazemMemoria()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 0
    assert arm.envios == 4
    inv_cvm = V._ler(S.inventario(repo, "cvm"))
    assert {x["papel"] for x in inv_cvm} == {"canonico", "snapshot"} and len(inv_cvm) == 3
    assert len(V._ler(S.inventario(repo, "b3"))) == 1
    antes = open(S.inventario(repo, "cvm"), "rb").read()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 0
    assert arm.envios == 4, "a segunda carga nao escreve nada no armazem"
    assert open(S.inventario(repo, "cvm"), "rb").read() == antes, "nem no inventario"


def test_o_inventario_torna_a_versao_abrivel(tmp_path):
    repo = _acervo(tmp_path)
    arm = A.ArmazemMemoria()
    S.main(["--aplicar"], armazem=arm, repo=repo)
    import shutil
    shutil.rmtree(os.path.join(repo, "data", "bronze"))      # a maquina perdeu o disco
    p = V.abrir("dfp", "dfp_cia_aberta_2024.zip", _sha(b"de 13/09")[:8], armazem=arm,
                repo=repo)
    assert open(p, "rb").read() == b"de 13/09"


def test_snapshot_cujo_nome_mente_para_o_plano_inteiro(tmp_path):
    repo = _acervo(tmp_path, snapshot_mente=True)
    arm = A.ArmazemMemoria()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 1
    assert arm.objetos == {} and not os.path.exists(S.inventario(repo, "cvm"))
    with pytest.raises(SystemExit):
        S.aplicar(S.plano(repo), arm, repo)


def test_P145_o_banco_de_ISIN_sobe_e_a_captura_mais_recente_e_a_canonica(tmp_path):
    """Sem o isinp.zip no armazem, a ponte da P-145 so roda no desktop. Duas capturas: a
    mais nova e a vigente, a outra fica como versao anterior; pasta fora da convencao nao
    sobe."""
    repo = _acervo(tmp_path)
    isin = tmp_path / "data" / "bronze" / "b3" / "isin"
    for d, b in (("dt_captura=2026-09-25", b"isin 25"), ("dt_captura=2026-10-01", b"isin 01")):
        (isin / d).mkdir(parents=True)
        (isin / d / "isinp.zip").write_bytes(b)
    (isin / "rascunho").mkdir()
    itens = [x for x in S.plano(repo) if x["recurso"] == "isin"]
    subir = {x["papel"]: x for x in itens if x["acao"] == S.SUBIR}
    assert subir["canonico"]["sha256"] == _sha(b"isin 01")
    assert subir["snapshot"]["sha256"] == _sha(b"isin 25")
    assert subir["canonico"]["chave"].startswith("b3/isin/isinp.zip/")
    assert [x["arquivo"] for x in itens if x["acao"] == S.DESCONHECIDO] == ["rascunho"]
    arm = A.ArmazemMemoria()
    assert S.main(["--aplicar"], armazem=arm, repo=repo) == 0
    caminho = V.abrir("isin", "isinp.zip", repo=repo, armazem=arm,
                      cache=str(tmp_path / "cache"))
    with open(caminho, "rb") as f:
        assert f.read() == b"isin 01"

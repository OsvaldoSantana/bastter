# -*- coding: utf-8 -*-
"""O backend local do armazem e a conferencia de quem reproduz de fora (25/09/2026)."""
from __future__ import annotations

import hashlib
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import armazem as A  # noqa: E402
import conferir_reproducao as R  # noqa: E402


def _arquivo(tmp_path, nome, corpo):
    p = tmp_path / nome
    p.write_bytes(corpo)
    return str(p), hashlib.sha256(corpo).hexdigest()


def test_local_tem_o_contrato_do_armazem(tmp_path):
    arm = A.ArmazemLocal(tmp_path / "arm")
    c, sha = _arquivo(tmp_path, "x.csv", b"conteudo")
    k = A.chave("nefin", "risk_factors", "x.csv", sha)
    assert arm.enviar_se_ausente(k, c) is True
    assert arm.enviar_se_ausente(k, c) is False, "nunca sobrescreve"
    assert arm.listar("nefin/") == [k] and arm.ocupado() == len(b"conteudo")
    destino = arm.baixar(k, str(tmp_path / "volta.csv"))
    assert open(destino, "rb").read() == b"conteudo"


def test_local_recusa_byte_que_nao_e_o_da_chave(tmp_path):
    arm = A.ArmazemLocal(tmp_path / "arm")
    c, _ = _arquivo(tmp_path, "x.csv", b"conteudo")
    with pytest.raises(A.ConteudoDivergente):
        arm.enviar_se_ausente(A.chave("nefin", "r", "x.csv", "0" * 64), c)


def test_do_ambiente_local_usa_a_pasta_da_variavel_e_tem_teto(tmp_path):
    repo = tmp_path / "repo"
    (repo / "alocacao").mkdir(parents=True)
    (repo / "alocacao" / "politica.yaml").write_text("armazem:\n  aviso_gb: 7\n  teto_gb: 9\n",
                                                     encoding="utf-8")
    arm = A.do_ambiente("local", env={"ARMAZEM_LOCAL": str(tmp_path / "p")}, raiz_repo=str(repo))
    assert isinstance(arm, A.ArmazemLocal) and arm.pasta == str(tmp_path / "p")
    assert arm.teto == 9 * A.GB
    with pytest.raises(ValueError):
        A.do_ambiente("disco", raiz_repo=str(repo))


def test_as_quatro_situacoes():
    nossos = {("cvm", "dfp", "a.zip"): {"1"}, ("cvm", "dfp", "b.zip"): {"2", "3"},
              ("cvm", "itr", "c.zip"): {"4"}}
    seus = {("cvm", "dfp", "a.zip"): {"1"}, ("cvm", "dfp", "b.zip"): {"9"},
            ("b3", "cotahist", "d.zip"): {"5"}}
    assert R.comparar(nossos, seus) == [
        ("SO_SEU", ("b3", "cotahist", "d.zip")), ("IGUAL", ("cvm", "dfp", "a.zip")),
        ("DIFERENTE", ("cvm", "dfp", "b.zip")), ("SO_NOSSO", ("cvm", "itr", "c.zip"))]


def test_capturados_le_o_sha_da_chave_e_ignora_o_log(tmp_path):
    arm = A.ArmazemLocal(tmp_path / "arm")
    c, sha = _arquivo(tmp_path, "a.zip", b"zip")
    arm.enviar_se_ausente(A.chave("cvm", "dfp", "a.zip", sha), c)
    log, _ = _arquivo(tmp_path, "log.csv", b"log")
    arm.enviar_se_ausente("logs/capturas/2026-09-25.csv", log)
    assert dict(R.capturados(arm)) == {("cvm", "dfp", "a.zip"): {sha}}


def test_o_nefin_de_hoje_bate_com_o_registrado():
    """Contra o registro real: a versao que o projeto fixou e a que o NEFIN serve em 25/09."""
    reg = R.registrados(R.acervo.raiz_repo())
    assert "619991c2192c958ae5f508ca4b9eae2d679d0a87b9c19ee4a21325b1981855f2" in \
        reg[("nefin", "risk_factors", "nefin_factors.csv")]

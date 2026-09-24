# -*- coding: utf-8 -*-
"""Testes do `armazem.py` -- sem rede e sem boto3.

O que se prova aqui, e cada um tem o espelho que impede o teste de passar por acaso:
  - a mesma chave enviada duas vezes nao altera nada (o pedido literal da P-57);
  - chave de conteudo com o byte errado e recusada na subida e na descida;
  - o `ArmazemS3` fala o dialeto do boto3 (com um cliente falso) e nao vaza credencial.
"""
import hashlib
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import armazem as A  # noqa: E402


def _arquivo(tmp_path, nome, conteudo):
    p = tmp_path / nome
    p.write_bytes(conteudo)
    return str(p), hashlib.sha256(conteudo).hexdigest()


# ── a chave ───────────────────────────────────────────────────────────────────

def test_a_chave_tem_a_forma_prometida():
    d = "a" * 64
    assert A.chave("cvm", "dfp", "dfp_cia_aberta_2024.zip", d) == \
        f"cvm/dfp/dfp_cia_aberta_2024.zip/{d}.zip"
    assert A.chave("b3", "cotahist", "COTAHIST_A2023.ZIP", d).endswith(f"/{d}.zip")
    assert A.sha_da_chave(f"cvm/dfp/x.zip/{d}.zip") == d
    assert A.sha_da_chave("logs/capturas/2026-09-24.csv") is None


@pytest.mark.parametrize("args", [
    ("xyz", "dfp", "a.zip", "a" * 64),        # fonte fora da lista
    ("cvm", "d/fp", "a.zip", "a" * 64),       # barra no segmento
    ("cvm", "dfp", "..", "a" * 64),
    ("cvm", "dfp", "a.zip", "A" * 64),        # sha maiusculo nao e o que sha256() devolve
    ("cvm", "dfp", "a.zip", "a" * 63),
    ("cvm", "dfp", "semextensao", "a" * 64),
])
def test_chave_malformada_e_recusada(args):
    with pytest.raises(A.ChaveInvalida):
        A.chave(*args)


# ── nunca sobrescrever ────────────────────────────────────────────────────────

def test_enviar_a_mesma_chave_duas_vezes_nao_altera_nada(tmp_path):
    arm = A.ArmazemMemoria()
    p, d = _arquivo(tmp_path, "a.zip", b"conteudo")
    k = A.chave("cvm", "dfp", "a.zip", d)
    assert arm.enviar_se_ausente(k, p) is True
    antes = dict(arm.objetos)
    assert arm.enviar_se_ausente(k, p) is False
    assert arm.objetos == antes and arm.envios == 1


def test_chave_de_log_ja_existente_nao_e_sobrescrita_por_outro_conteudo(tmp_path):
    """O espelho: a chave de log nao e de conteudo, e ainda assim nao se reescreve."""
    arm = A.ArmazemMemoria()
    p1, _ = _arquivo(tmp_path, "1.csv", b"primeiro")
    p2, _ = _arquivo(tmp_path, "2.csv", b"segundo")
    assert arm.enviar_se_ausente("logs/capturas/2026-09-24.csv", p1)
    assert not arm.enviar_se_ausente("logs/capturas/2026-09-24.csv", p2)
    assert arm.objetos["logs/capturas/2026-09-24.csv"] == b"primeiro"


def test_subir_byte_que_nao_bate_com_a_chave_e_recusado(tmp_path):
    arm = A.ArmazemMemoria()
    p, _ = _arquivo(tmp_path, "a.zip", b"conteudo")
    k = A.chave("cvm", "dfp", "a.zip", "b" * 64)
    with pytest.raises(A.ConteudoDivergente):
        arm.enviar_se_ausente(k, p)
    assert arm.objetos == {}


def test_descer_byte_que_nao_bate_com_a_chave_e_recusado_e_nao_deixa_arquivo(tmp_path):
    arm = A.ArmazemMemoria()
    k = A.chave("cvm", "dfp", "a.zip", "c" * 64)
    arm.objetos[k] = b"corrompido no armazem"
    destino = str(tmp_path / "saida" / "a.zip")
    with pytest.raises(A.ConteudoDivergente):
        arm.baixar(k, destino)
    assert not os.path.exists(destino) and not os.path.exists(destino + ".part")


def test_baixar_e_listar(tmp_path):
    arm = A.ArmazemMemoria()
    p, d = _arquivo(tmp_path, "a.zip", b"x")
    k = A.chave("cvm", "dfp", "a.zip", d)
    arm.enviar_se_ausente(k, p)
    arm.objetos["logs/capturas/2026-09-24.csv"] = b"l"
    destino = arm.baixar(k, str(tmp_path / "b" / "a.zip"))
    assert open(destino, "rb").read() == b"x"
    assert arm.listar("cvm/") == [k]
    assert arm.listar() == sorted([k, "logs/capturas/2026-09-24.csv"])


@pytest.mark.parametrize("k", ["", "/abs", "a//b", "a/../b", "a\\b"])
def test_chave_crua_invalida_e_recusada_em_toda_operacao(k, tmp_path):
    arm = A.ArmazemMemoria()
    with pytest.raises(A.ChaveInvalida):
        arm.existe(k)
    with pytest.raises(A.ChaveInvalida):
        arm.baixar(k, str(tmp_path / "x"))


# ── ArmazemS3, com um cliente falso ──────────────────────────────────────────

class _Erro404(Exception):
    response = {"Error": {"Code": "404"}}


class _Erro403(Exception):
    response = {"Error": {"Code": "403"}}


class _ClienteFalso:
    """O pedaco do boto3 que o ArmazemS3 usa: head_object, upload_file, download_file e
    o paginador de list_objects_v2."""

    def __init__(self, negar=False):
        self.objetos, self.chamadas, self.negar = {}, [], negar

    def head_object(self, Bucket, Key):
        self.chamadas.append(("head", Bucket, Key))
        if self.negar:
            raise _Erro403()
        if Key not in self.objetos:
            raise _Erro404()
        return {}

    def upload_file(self, caminho, bucket, key):
        self.chamadas.append(("upload", bucket, key))
        self.objetos[key] = open(caminho, "rb").read()

    def download_file(self, bucket, key, destino):
        open(destino, "wb").write(self.objetos[key])

    def get_paginator(self, nome):
        assert nome == "list_objects_v2"
        cli = self

        class P:
            def paginate(self, Bucket, Prefix):
                ks = [k for k in sorted(cli.objetos) if k.startswith(Prefix)]
                yield {"Contents": [{"Key": k} for k in ks[:1]]}
                yield {"Contents": [{"Key": k} for k in ks[1:]]}
                yield {}
        return P()


ENV = {"R2_ACCOUNT_ID": "conta-secreta-123", "R2_ACCESS_KEY_ID": "chave-secreta-456",
       "R2_SECRET_ACCESS_KEY": "segredo-789", "R2_BUCKET": "acervo"}


def test_s3_nunca_sobrescreve_e_pagina_a_listagem(tmp_path):
    cli = _ClienteFalso()
    arm = A.ArmazemS3.de_ambiente(ENV, cliente=cli)
    p, d = _arquivo(tmp_path, "a.zip", b"conteudo")
    k = A.chave("cvm", "dfp", "a.zip", d)
    assert arm.enviar_se_ausente(k, p) and not arm.enviar_se_ausente(k, p)
    assert [c[0] for c in cli.chamadas].count("upload") == 1
    assert all(c[1] == "acervo" for c in cli.chamadas)
    cli.objetos["cvm/dfp/b.zip/" + "d" * 64 + ".zip"] = b""
    assert len(arm.listar("cvm/")) == 2          # veio de duas paginas
    assert open(arm.baixar(k, str(tmp_path / "o.zip")), "rb").read() == b"conteudo"


def test_s3_erro_que_nao_e_404_sobe_em_vez_de_virar_ausente(tmp_path):
    """403 lido como "nao existe" faria o envio seguinte tentar escrever -- e um
    armazem sem permissao pareceria vazio (o F-02 no transporte)."""
    arm = A.ArmazemS3.de_ambiente(ENV, cliente=_ClienteFalso(negar=True))
    with pytest.raises(_Erro403):
        arm.existe("cvm/dfp/a.zip/" + "a" * 64 + ".zip")


def test_s3_endpoint_vem_da_conta_ou_do_R2_ENDPOINT():
    assert A.ArmazemS3.de_ambiente(ENV, cliente=_ClienteFalso()).endpoint_url == \
        "https://conta-secreta-123.r2.cloudflarestorage.com"
    outro = dict(ENV, R2_ENDPOINT="https://s3.exemplo")
    assert A.ArmazemS3.de_ambiente(outro, cliente=_ClienteFalso()).endpoint_url == \
        "https://s3.exemplo"


def test_credencial_ausente_diz_o_NOME_e_nunca_um_valor():
    env = dict(ENV)
    del env["R2_SECRET_ACCESS_KEY"]
    with pytest.raises(A.ArmazemIndisponivel) as e:
        A.ArmazemS3.de_ambiente(env, cliente=_ClienteFalso())
    msg = str(e.value)
    assert "R2_SECRET_ACCESS_KEY" in msg
    assert not any(v in msg for v in ENV.values())


def test_repr_nao_carrega_credencial_nem_conta():
    arm = A.ArmazemS3.de_ambiente(ENV, cliente=_ClienteFalso())
    r = repr(arm)
    assert "acervo" in r
    assert not any(v in r for v in ("conta-secreta-123", "chave-secreta-456", "segredo-789"))


def test_o_modulo_carrega_sem_boto3(monkeypatch):
    """A suite nao depende do boto3 (pyproject: optional-dependencies.captura). Sem ele,
    so o ArmazemS3 sem cliente injetado falha -- e falha dizendo como instalar."""
    monkeypatch.setitem(sys.modules, "boto3", None)
    with pytest.raises(A.ArmazemIndisponivel, match="captura"):
        A.ArmazemS3("acervo")
    assert A.ArmazemMemoria() is not None

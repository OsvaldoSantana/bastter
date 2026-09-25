# -*- coding: utf-8 -*-
"""P-139: o leitor da familia ML abre a versao FIXADA e confere a impressao de conteudo.

O defeito que ele fecha (CH-01): o pre-registro fixa `fb3546ed...`, o acervo marca
`4f2cf2aa...` como vigente, e o `calendario` lia o que estivesse no disco. Cada teste
abaixo reprova numa versao plausivel do leitor que "abre o vigente" ou "confia no hash
do ZIP".
"""
from __future__ import annotations

import datetime as dt
import hashlib
import os
import re
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import acervo  # noqa: E402
import insumo_ml as M  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATE = dt.date(2026, 8, 31)


def _linha(data, codneg):
    return ("01" + data + "02" + codneg.ljust(12) + "010" + "EMPRESA     "
            + "ON        " + "   " + "R$  ").ljust(245)


def _zip(caminho, linhas, gerado="20260918"):
    corpo = ("00COTAHIST.2026BOVESPA " + gerado).ljust(245) + "\r\n"
    corpo += "".join(ln + "\r\n" for ln in linhas)
    corpo += ("99COTAHIST.2026BOVESPA " + gerado).ljust(245) + "\r\n"
    with zipfile.ZipFile(caminho, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("COTAHIST_A2026.TXT", corpo.encode("latin-1"))
    return str(caminho)


LINHAS = [_linha("20260102", "PETR4"), _linha("20260102", "VALE3"),
          _linha("20260831", "PETR4"), _linha("20260901", "PETR4")]


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def _pins(caminho, **imp):
    sha, n, d = M.impressao(caminho, ATE)
    base = dict(ate=ATE, registros=n, pregoes=d, sha256=sha)
    base.update(imp)
    return {"preregistro": "pre.md", "cotahist": {2026: dict(
        arquivo="COTAHIST_A2026.ZIP", sha256=_sha(caminho),
        bytes=os.path.getsize(caminho), impressao=base)}}


def _abrir_de(mapa, chamadas):
    """Um acervo falso: (arquivo, versao) -> caminho. Registra cada chamada."""
    def abrir(recurso, arquivo, versao=None, conferir=False):
        chamadas.append((recurso, arquivo, versao, conferir))
        return mapa[(arquivo, versao)]
    return abrir


@pytest.fixture(autouse=True)
def _limpar_cache():
    M._CONFERIDAS.clear()
    yield
    M._CONFERIDAS.clear()


# ── a impressao: independe da ordem, depende do conteudo e da janela ──────────
def test_impressao_nao_depende_da_ORDEM_das_linhas(tmp_path):
    """CH-01: a B3 regera reordenando. Um leitor que confiasse no hash do ZIP acusaria."""
    a = _zip(tmp_path / "a.zip", LINHAS)
    b = _zip(tmp_path / "b.zip", list(reversed(LINHAS)), gerado="20260923")
    assert _sha(a) != _sha(b)
    assert M.impressao(a, ATE) == M.impressao(b, ATE)


def test_impressao_MUDA_com_um_campo_dentro_da_janela(tmp_path):
    a = _zip(tmp_path / "a.zip", LINHAS)
    mexido = [LINHAS[0][:60] + "X" + LINHAS[0][61:]] + LINHAS[1:]
    b = _zip(tmp_path / "b.zip", mexido)
    assert M.impressao(a, ATE)[0] != M.impressao(b, ATE)[0]


def test_impressao_ignora_o_que_esta_DEPOIS_da_janela(tmp_path):
    """E declarado no modulo (P5): o teste do pre-registro termina em `ate`."""
    a = _zip(tmp_path / "a.zip", LINHAS)
    b = _zip(tmp_path / "b.zip", LINHAS + [_linha("20260923", "ITUB4")])
    assert M.impressao(a, ATE) == M.impressao(b, ATE)
    assert M.impressao(a, ATE)[1:] == (3, 2)


# ── o leitor: a versao fixada, nunca a vigente ────────────────────────────────
def test_ano_fixado_abre_pela_VERSAO_e_nao_pela_vigente(tmp_path):
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    pins = _pins(fixado)
    sha = pins["cotahist"][2026]["sha256"]
    chamadas: list = []
    lt = M.abrir_cotahist(2026, pins=pins, abrir=_abrir_de(
        {("COTAHIST_A2026.ZIP", sha): str(fixado)}, chamadas))
    assert lt.fixado and lt.sha256 == sha and lt.caminho == str(fixado)
    assert chamadas == [("cotahist", "COTAHIST_A2026.ZIP", sha, True)], \
        "abriu sem a versao, ou sem conferir o sha256"


def test_versao_fixada_indisponivel_BLOQUEIA_e_nao_cai_para_a_vigente(tmp_path):
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    pins = _pins(fixado)

    def abrir(recurso, arquivo, versao=None, conferir=False):
        if versao is None:
            return str(fixado)          # a vigente esta ali, e nao pode ser usada
        raise acervo.VersaoDesconhecida(versao)
    with pytest.raises(M.InsumoBloqueado, match="NAO a substitui"):
        M.abrir_cotahist(2026, pins=pins, abrir=abrir)


def test_impressao_diferente_da_fixada_BLOQUEIA(tmp_path):
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    pins = _pins(fixado, sha256="0" * 64)
    sha = pins["cotahist"][2026]["sha256"]
    with pytest.raises(M.InsumoBloqueado, match="impressao"):
        M.abrir_cotahist(2026, pins=pins, abrir=_abrir_de(
            {("COTAHIST_A2026.ZIP", sha): str(fixado)}, []))


def test_contagem_diferente_da_fixada_BLOQUEIA(tmp_path):
    """O hash sozinho nao basta como declaracao: o n viaja com ele (regua 5-B.14)."""
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    pins = _pins(fixado, registros=4)
    sha = pins["cotahist"][2026]["sha256"]
    with pytest.raises(M.InsumoBloqueado):
        M.abrir_cotahist(2026, pins=pins, abrir=_abrir_de(
            {("COTAHIST_A2026.ZIP", sha): str(fixado)}, []))


def test_tamanho_diferente_do_fixado_BLOQUEIA(tmp_path):
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    pins = _pins(fixado)
    pins["cotahist"][2026]["bytes"] += 1
    sha = pins["cotahist"][2026]["sha256"]
    with pytest.raises(M.InsumoBloqueado, match="bytes"):
        M.abrir_cotahist(2026, pins=pins, abrir=_abrir_de(
            {("COTAHIST_A2026.ZIP", sha): str(fixado)}, []))


def test_ano_SEM_pin_le_a_vigente_e_diz_que_nao_e_fixado(tmp_path, monkeypatch):
    """O pre-registro nao fixou 2025. Bloquear seria inventar regra; esconder seria pior."""
    p = _zip(tmp_path / "v.zip", LINHAS)
    monkeypatch.setattr(acervo, "versoes", lambda r, a: [
        dict(sha256="ab" * 32, vigente=True), dict(sha256="cd" * 32, vigente=False)])
    lt = M.abrir_cotahist(2025, pins={"preregistro": "pre.md", "cotahist": {}},
                          abrir=_abrir_de({("COTAHIST_A2025.ZIP", None): str(p)}, []))
    assert not lt.fixado and lt.sha256 == "ab" * 32


# ── o pins.yaml do repositorio ────────────────────────────────────────────────
def test_o_pin_do_yaml_e_o_do_PRE_REGISTRO():
    """N-01: duas declaracoes da mesma coisa. O .md e o que foi empurrado; o yaml e o
    que o codigo le. Reprova se um andar sem o outro."""
    pins = M.carregar_pins()
    md = open(os.path.join(REPO, pins["preregistro"]), encoding="utf-8").read()
    pin = pins["cotahist"][2026]
    assert f"sha256 {pin['sha256'][:12]}" in md
    assert f"{pin['bytes']:,}".replace(",", ".") in md
    assert re.search(r"COTAHIST_A2026\.ZIP", md)


@pytest.mark.slow
def test_a_impressao_do_yaml_e_a_do_BYTE_FIXADO_quando_ele_esta_no_disco():
    """A medida do CH-01 reproduzida pelo leitor, sobre o arquivo real. Lento (~700 MB)."""
    pins = M.carregar_pins()
    pin = pins["cotahist"][2026]
    local = os.path.join(REPO, "data", "bronze", "b3", "cotahist", pin["arquivo"])
    if not os.path.exists(local) or os.path.getsize(local) != pin["bytes"]:
        pytest.skip("o byte fixado nao esta no disco desta maquina")
    imp = pin["impressao"]
    assert M.impressao(local, imp["ate"]) == (imp["sha256"], imp["registros"],
                                              imp["pregoes"])

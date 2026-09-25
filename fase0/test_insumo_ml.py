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
from acervo_de_teste import exigir_acervo  # noqa: E402

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


def _so_a_vigente(caminho):
    """Um acervo em que o byte observado sumiu e so a vigente abre."""
    def abrir(recurso, arquivo, versao=None, conferir=False):
        if versao is None:
            return str(caminho)
        raise acervo.VersaoDesconhecida(versao)
    return abrir


# P-140 (25/09): substitui o teste da P-139 "versao fixada indisponivel BLOQUEIA e nao cai
# para a vigente". A regra mudou por decisao registrada: a impressao e o pino principal, e
# a vigente com a MESMA impressao e o mesmo conteudo (CH-01) -- bloquear seria recusar o
# dado certo por causa da compressao.
def test_P140_sha_DIFERENTE_e_impressao_IGUAL_segue_com_AVISO(tmp_path):
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    pins = _pins(fixado)
    recomprimido = _zip(tmp_path / "vigente.zip", list(reversed(LINHAS)), gerado="20260923")
    assert _sha(recomprimido) != pins["cotahist"][2026]["sha256"]
    with pytest.warns(M.AvisoRecompressao, match="IGUAL"):
        lt = M.abrir_cotahist(2026, pins=pins, abrir=_so_a_vigente(recomprimido))
    assert lt.fixado and lt.sha256 == _sha(recomprimido) and "IGUAL" in lt.aviso


def test_P140_impressao_DIFERENTE_na_vigente_BLOQUEIA(tmp_path):
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    pins = _pins(fixado)
    outro = _zip(tmp_path / "vigente.zip", LINHAS[:1] + LINHAS[2:])     # uma linha a menos
    with pytest.raises(M.InsumoBloqueado, match="impressao"):
        M.abrir_cotahist(2026, pins=pins, abrir=_so_a_vigente(outro))


def test_P140_byte_observado_disponivel_nao_avisa(tmp_path, recwarn):
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    pins = _pins(fixado)
    sha = pins["cotahist"][2026]["sha256"]
    lt = M.abrir_cotahist(2026, pins=pins, abrir=_abrir_de(
        {("COTAHIST_A2026.ZIP", sha): str(fixado)}, []))
    assert lt.aviso == "" and not [w for w in recwarn if w.category is M.AvisoRecompressao]


def test_P140_nada_abre_BLOQUEIA(tmp_path):
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    pins = _pins(fixado)

    def abrir(recurso, arquivo, versao=None, conferir=False):
        raise acervo.VersaoDesconhecida(versao)
    with pytest.raises(M.InsumoBloqueado, match="nem o byte observado"):
        M.abrir_cotahist(2026, pins=pins, abrir=abrir)


def test_P140_medir_pin_e_a_mesma_medida_que_o_leitor_confere(tmp_path):
    """Quem escreve o pin e quem o confere usam uma funcao so (N-01)."""
    fixado = _zip(tmp_path / "fixado.zip", LINHAS)
    p = M.medir_pin(fixado, 2026, ATE)
    assert p == _pins(fixado)["cotahist"][2026]
    assert M.medir_pin(fixado, 2026)["impressao"]["ate"] == dt.date(2026, 12, 31)


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


def _meses_da_maior_janela_de_preco(md):
    """A maior janela em MESES da tabela de variaveis (secao 5.1), lida do texto."""
    secao = md.split("### 5.1", 1)[1].split("### 5.2", 1)[0]
    meses = [int(x) for x in re.findall(r"(\d+) meses", secao)]
    meses += [int(x) for x in re.findall(r"(\d+)m\b", secao)]
    return max(meses)


def test_P140_os_anos_fixados_cobrem_a_maior_janela_do_preregistro():
    """3.1 medido, nao suposto: a maior janela de preco do pre-registro (a reversao, 60
    meses) contada do primeiro mes de decisao (secao 2) define o primeiro ano que o ML le.
    O ultimo negocio ate o fim daquele mes pode estar no ano anterior -- por isso -1."""
    pins = M.carregar_pins()
    md = open(os.path.join(REPO, pins["preregistro"]), encoding="utf-8").read()
    ano0 = int(re.search(r"\*\*Per[ií]odo:\*\* jan/(\d{4})", md).group(1))
    n = _meses_da_maior_janela_de_preco(md)
    assert n == 60, "a maior janela mudou -- e o conjunto de anos fixados tem de mudar junto"
    primeiro = ano0 - (n + 11) // 12 - 1        # jan/2010 - 60 meses = jan/2005; -1 = 2004
    faltando = set(range(primeiro, 2026)) - set(pins["cotahist"])
    assert primeiro == 2004 and not faltando, sorted(faltando)


@pytest.mark.slow
def test_REAL_todo_ano_fixado_confere_nesta_maquina():
    """3.4: todo pin do pins.yaml abre e confere no acervo real, pelo leitor do ML."""
    exigir_acervo(os.path.join(REPO, "data", "bronze", "b3", "cotahist"))
    pins = M.carregar_pins()
    lidos = [M.abrir_cotahist(a, pins=pins) for a in sorted(pins["cotahist"])]
    assert all(lt.fixado for lt in lidos) and len(lidos) == len(pins["cotahist"])


@pytest.mark.slow
def test_REAL_a_impressao_do_yaml_e_a_do_arquivo_no_disco_2026():
    """A medida do CH-01 reproduzida pelo leitor, sobre o arquivo real. Lento (~700 MB).
    P-140: a impressao e o pino principal, entao ela vale para QUALQUER versao no disco --
    o fixado ou a vigente recomprimida. Antes pulava quando o disco tinha a vigente."""
    pins = M.carregar_pins()
    pin = pins["cotahist"][2026]
    local = os.path.join(REPO, "data", "bronze", "b3", "cotahist", pin["arquivo"])
    exigir_acervo(local)
    imp = pin["impressao"]
    assert M.impressao(local, imp["ate"]) == (imp["sha256"], imp["registros"],
                                              imp["pregoes"])

# -*- coding: utf-8 -*-
"""A sonda da P-135 transcreve o que a B3 responde -- inclusive a recusa."""
from __future__ import annotations

import datetime as dt
import email.message
import io
import os
import sys
import urllib.error

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import sondar_cotahist as sc  # noqa: E402


class _Resp(io.BytesIO):
    def __init__(self, status, headers):
        super().__init__(b"")
        self.status = status
        self.headers = email.message.Message()
        for k, v in headers.items():
            self.headers[k] = v

    def getcode(self):
        return self.status


def test_urls_anual_do_ano_corrente_e_diarios_so_de_dia_util():
    # quinta 24/09/2026: para tras ate quinta 17/09, pulando sabado e domingo
    u = sc.urls(dt.date(2026, 9, 24))
    assert u[0].endswith("COTAHIST_A2026.ZIP")
    diarios = [x.rsplit("_D", 1)[1] for x in u[1:]]
    assert diarios == ["23092026.ZIP", "22092026.ZIP", "21092026.ZIP",
                       "18092026.ZIP", "17092026.ZIP"]


def test_resposta_200_traz_os_cabecalhos():
    def abrir(req, timeout):
        assert req.get_method() == "HEAD"
        return _Resp(200, {"Content-Length": "84469516",
                           "Last-Modified": "Wed, 23 Sep 2026 23:43:07 GMT",
                           "Server": "cloudflare"})
    ln = sc.sondar(sc.BASE + "COTAHIST_A2026.ZIP", abrir)
    assert ln["status"] == "200" and ln["Content-Length"] == "84469516"
    assert ln["Last-Modified"].startswith("Wed") and ln["erro"] == ""


def test_recusa_e_transcrita_e_nao_retentada():
    chamadas = []

    def abrir(req, timeout):
        chamadas.append(req)
        h = email.message.Message()
        h["Server"] = "cloudflare"
        raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", h, None)
    ln = sc.sondar(sc.BASE + "COTAHIST_A2026.ZIP", abrir)
    assert ln["status"] == "403" and ln["erro"] == "HTTPError 403 Forbidden"
    assert ln["Server"] == "cloudflare"
    # 403 nao e retentavel, mas 503 seria: a sonda nao retenta nenhum
    chamadas.clear()

    def abrir503(req, timeout):
        chamadas.append(req)
        raise urllib.error.HTTPError(req.full_url, 503, "Unavailable", None, None)
    assert sc.sondar(sc.BASE + "x.ZIP", abrir503)["status"] == "503"
    assert len(chamadas) == 1


def test_falha_de_rede_vira_linha_e_nao_excecao():
    def abrir(req, timeout):
        raise urllib.error.URLError("timed out")
    ln = sc.sondar(sc.BASE + "x.ZIP", abrir)
    assert ln["status"] == "" and "timed out" in ln["erro"]


def test_main_sai_zero_mesmo_com_recusa_e_escreve_no_resumo(tmp_path, monkeypatch, capsys):
    resumo = tmp_path / "resumo.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(resumo))

    def abrir(req, timeout):
        raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", None, None)
    assert sc.main([], abrir=abrir, hoje=dt.date(2026, 9, 24)) == 0
    texto = resumo.read_text(encoding="utf-8")
    assert "COTAHIST_A2026.ZIP | 403" in texto and "HTTPError 403 Forbidden" in texto

# -*- coding: utf-8 -*-
"""A captura do NEFIN: sobe com a chave da fonte, o portao HEAD fecha a segunda rodada, 404
e erro, e o log nao se mistura. Sem rede e sem boto3."""
from __future__ import annotations

import csv
import os
import sys
import urllib.error

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import armazem as A  # noqa: E402
import capturar_nefin as N  # noqa: E402
from test_capturar_cvm import _Resp  # noqa: E402

LM = "Thu, 17 Sep 2026 14:48:15 GMT"
CORPO = b'"","Date","Rm_minus_Rf"\n"1",2001-01-02,0.01\n'


class Nefin:
    def __init__(self, corpo=CORPO, publicado=True):
        self.corpo, self.publicado, self.chamadas = corpo, publicado, []

    def __call__(self, req, timeout=None):
        self.chamadas.append((req.get_method(), req.full_url))
        if not self.publicado or req.full_url != N.URL:
            raise urllib.error.HTTPError(req.full_url, 404, "Not Found", {}, None)
        cab = {"Content-Length": str(len(self.corpo)), "Last-Modified": LM, "ETag": '"x"'}
        return _Resp(b"" if req.get_method() == "HEAD" else self.corpo, cab)


def _rodar(tmp_path, srv, arm):
    repo = tmp_path / "repo"
    (repo / "alocacao").mkdir(parents=True, exist_ok=True)
    (repo / "alocacao" / "politica.yaml").write_text(
        "armazem:\n  aviso_gb: 7\n  teto_gb: 9\n", encoding="utf-8")
    reg = str(tmp_path / "docs" / "acervo" / "nefin" / "capturas.csv")
    rc = N.main(["--armazem", "s3", "--raiz", str(tmp_path / "data" / "bronze" / "nefin"),
                 "--registro", reg, "--raiz-repo", str(repo)],
                abrir=srv, dormir=lambda s: None, armazem=arm)
    return rc, reg


def _linhas(reg):
    return list(csv.DictReader(open(reg, encoding="utf-8"), delimiter=";"))


def test_primeira_rodada_sobe_com_a_chave_do_nefin(tmp_path):
    arm = A.ArmazemMemoria()
    rc, reg = _rodar(tmp_path, Nefin(), arm)
    assert rc == 0
    ks = [k for k in arm.objetos if not k.startswith("logs/")]
    assert len(ks) == 1 and ks[0].startswith("nefin/risk_factors/nefin_factors.csv/")
    (ln,) = _linhas(reg)
    assert ln["situacao"] == "novo" and ln["url"] == N.URL and ln["sha256"]


def test_segunda_rodada_o_portao_fecha_e_nao_ha_GET(tmp_path):
    srv, arm = Nefin(), A.ArmazemMemoria()
    _rodar(tmp_path, srv, arm)
    srv.chamadas.clear()
    rc, reg = _rodar(tmp_path, srv, arm)
    assert rc == 0 and [m for m, _ in srv.chamadas] == ["HEAD"]
    assert len(_linhas(reg)) == 1, "inalterado pelo portao vai so para o log"


def test_404_e_erro_e_fica_vermelho(tmp_path):
    """Uma URL so: se ela sumir, a fonte inteira sumiu. Foi o que aconteceu com o endereco
    antigo (`/resources/risk_factors/`), medido em 25/09."""
    rc, reg = _rodar(tmp_path, Nefin(publicado=False), A.ArmazemMemoria())
    assert rc == 1 and _linhas(reg)[0]["situacao"] == "erro"


def test_o_log_e_do_nefin(tmp_path):
    arm = A.ArmazemMemoria()
    _rodar(tmp_path, Nefin(), arm)
    logs = [k for k in arm.objetos if k.startswith("logs/")]
    assert logs and all(k.startswith("logs/capturas_nefin/") for k in logs)

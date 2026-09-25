# -*- coding: utf-8 -*-
"""Testes do modo `--armazem` do `capturar_cvm.py` (P-57) -- sem rede e sem boto3.

O servidor falso e o do `test_capturar_cvm.py`; o armazem e o `ArmazemMemoria`. O que se
prova, e a razao de cada um:
  - o registro versionado recebe so o que muda o estado, e o log recebe a rodada inteira
    (2.2 da P-57: sem isso seriam 365 commits de ruido por ano);
  - o `inalterado` por "hash coincide" vai ao registro, e e o que impede o portao HEAD de
    baixar o mesmo arquivo todo dia;
  - a regra 2.5 continua valendo sem disco: download cortado nao sobe;
  - os dois modos compartilham o portao, porque o `caminho` do registro e o mesmo.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import armazem as A  # noqa: E402
import capturar_cvm as C  # noqa: E402
from test_capturar_cvm import LM2, N_BASICO, _servidor_basico, _zip  # noqa: E402


def _rodar(tmp_path, srv, arm, *extra):
    raiz = str(tmp_path / "data" / "bronze" / "cvm")
    reg = str(tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv")
    rc = C.main(["--raiz", raiz, "--registro", reg, "--pausa", "0", "--armazem", "s3",
                 *extra], abrir=srv, dormir=lambda s: None, armazem=arm,
                manifestar=lambda r: pytest.fail("o modo armazem nao roda o manifesto"))
    return rc, raiz, reg


def _conteudo(arm):
    return sorted(k for k in arm.objetos if not k.startswith(C.LOGS))


def _logs(arm):
    return sorted(k for k in arm.objetos if k.startswith(C.LOGS))


def _log(arm, k):
    return list(csv.DictReader(io.StringIO(arm.objetos[k].decode("utf-8")), delimiter=";"))


def test_primeira_rodada_sobe_cada_arquivo_pela_chave_de_conteudo(tmp_path):
    srv, arm = _servidor_basico(), A.ArmazemMemoria()
    rc, raiz, reg = _rodar(tmp_path, srv, arm)
    assert rc == 0
    ks = _conteudo(arm)
    assert len(ks) == N_BASICO
    for k in ks:
        assert A.sha_da_chave(k) is not None, "toda chave de conteudo carrega o sha256"
    linhas = C.ler_registro(reg)
    assert [x["situacao"] for x in linhas] == ["novo"] * N_BASICO
    for x in linhas:
        assert A.chave("cvm", x["recurso"], x["arquivo"], x["sha256"]) in ks, \
            "a chave se deriva do registro: recurso, arquivo e sha256"
    assert not os.path.exists(raiz), "sem --cache, o disco local nao e tocado"
    assert len(_logs(arm)) == 1


def test_rodada_sem_mudanca_vai_so_para_o_log(tmp_path):
    srv, arm = _servidor_basico(), A.ArmazemMemoria()
    _rodar(tmp_path, srv, arm)
    reg = str(tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv")
    antes, gets, envios = open(reg, "rb").read(), len(srv.gets()), arm.envios
    rc, _, _ = _rodar(tmp_path, srv, arm)
    assert rc == 0
    assert open(reg, "rb").read() == antes, "inalterado pelo portao nao muda o registro"
    assert len(srv.gets()) == gets, "o portao HEAD nao baixa de novo"
    logs = _logs(arm)
    assert len(logs) == 2 and arm.envios == envios + 1, "so o log novo foi escrito"
    segundo = _log(arm, logs[-1])            # "<dia>.csv" ordena antes de "<dia>__<hora>Z.csv"
    assert {x["situacao"] for x in segundo} == {"inalterado"} and len(segundo) == N_BASICO


def test_hash_coincide_vai_ao_registro_e_fecha_o_portao_na_rodada_seguinte(tmp_path):
    """A CVM regera o arquivo com Last-Modified novo e o mesmo byte. Se esta linha fosse
    so para o log, o registro guardaria o Last-Modified velho e o portao abriria todo
    dia -- o mesmo arquivo baixado para sempre."""
    srv, arm = _servidor_basico(), A.ArmazemMemoria()
    _rodar(tmp_path, srv, arm)
    url = [u for u in srv.arquivos if "dfp_cia_aberta_2012" in u][0]
    srv.arquivos[url]["lm"] = LM2
    _rodar(tmp_path, srv, arm)
    reg = str(tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv")
    ult = C.ler_registro(reg)[-1]
    assert (ult["situacao"], ult["motivo"], ult["http_last_modified"]) == \
        ("inalterado", "hash coincide", LM2)
    gets = srv.gets().count(url)
    _rodar(tmp_path, srv, arm)
    assert srv.gets().count(url) == gets, "com o Last-Modified novo no registro, o portao fecha"


def test_versao_nova_e_outra_chave_e_a_anterior_fica(tmp_path):
    srv, arm = _servidor_basico(), A.ArmazemMemoria()
    _rodar(tmp_path, srv, arm)
    antes = set(_conteudo(arm))
    srv.publicar("dfp", 2012, _zip({"dfp_cia_aberta_2012.csv": "a;b\n9;9\n"}), lm=LM2)
    rc, _, reg = _rodar(tmp_path, srv, arm)
    assert rc == 0
    depois = set(_conteudo(arm))
    assert antes < depois and len(depois - antes) == 1, "nada sobrescrito, uma chave nova"
    sit = [x["situacao"] for x in C.ler_registro(reg)]
    assert sit[-1] == "atualizado" and "deslocado" not in sit


def test_download_cortado_nao_sobe_e_o_log_sobe_mesmo_assim(tmp_path):
    srv, arm = _servidor_basico(), A.ArmazemMemoria()
    _rodar(tmp_path, srv, arm)
    antes = set(_conteudo(arm))
    url = srv.publicar("dfp", 2012, _zip({"dfp_cia_aberta_2012.csv": "x" * 5000}), lm=LM2)
    srv.cortar[url] = 40
    rc, _, reg = _rodar(tmp_path, srv, arm)
    assert rc == 1
    assert set(_conteudo(arm)) == antes
    rej = [x for x in C.ler_registro(reg) if x["situacao"] == "rejeitado"]
    assert len(rej) == 1 and "Content-Length" in rej[0]["motivo"]
    assert any(x["situacao"] == "rejeitado" for x in _log(arm, _logs(arm)[-1]))


def test_indice_vazio_e_erro_no_registro_e_no_log(tmp_path):
    srv, arm = _servidor_basico(), A.ArmazemMemoria()
    srv.indices[C.INDICES["itr"]] = []
    rc, _, reg = _rodar(tmp_path, srv, arm)
    assert rc == 1
    assert C.ler_registro(reg)[-1]["situacao"] == "erro"
    assert _log(arm, _logs(arm)[0])[0]["situacao"] == "erro"


def test_cache_guarda_copia_no_endereco_da_chave(tmp_path):
    srv, arm = _servidor_basico(), A.ArmazemMemoria()
    cache = str(tmp_path / "cache")
    _rodar(tmp_path, srv, arm, "--cache", cache)
    for k in _conteudo(arm):
        p = os.path.join(cache, *k.split("/"))
        assert open(p, "rb").read() == arm.objetos[k]


def test_os_dois_modos_compartilham_o_portao(tmp_path):
    """Uma rodada no disco (a maquina dele) e depois uma na nuvem: a nuvem nao baixa o
    que o disco ja registrou -- o `caminho` e o mesmo nos dois."""
    srv, arm = _servidor_basico(), A.ArmazemMemoria()
    raiz = str(tmp_path / "data" / "bronze" / "cvm")
    reg = str(tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv")
    C.main(["--raiz", raiz, "--registro", reg, "--pausa", "0"], abrir=srv,
           dormir=lambda s: None, manifestar=lambda r: None)
    gets = len(srv.gets())
    rc, _, _ = _rodar(tmp_path, srv, arm)
    assert rc == 0 and len(srv.gets()) == gets and _conteudo(arm) == []


def test_sem_armazem_o_modo_disco_nao_toca_o_armazem(tmp_path):
    srv, arm = _servidor_basico(), A.ArmazemMemoria()
    raiz = str(tmp_path / "data" / "bronze" / "cvm")
    reg = str(tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv")
    rc = C.main(["--raiz", raiz, "--registro", reg, "--pausa", "0"], abrir=srv,
                dormir=lambda s: None, manifestar=lambda r: None, armazem=arm)
    assert rc == 0 and arm.objetos == {}
    assert os.path.exists(os.path.join(raiz, "dfp", "dfp_cia_aberta_2012.zip"))


@pytest.mark.parametrize("args", [["--armazem", "s3", "--dry-run"], ["--cache", "x"]])
def test_combinacao_sem_sentido_e_recusada(tmp_path, args):
    with pytest.raises(SystemExit):
        C.main(["--raiz", str(tmp_path), *args], abrir=_servidor_basico(),
               dormir=lambda s: None, armazem=A.ArmazemMemoria())


def test_segundo_log_do_dia_nao_sobrescreve_o_primeiro():
    arm = A.ArmazemMemoria()
    t = dt.datetime(2026, 9, 25, 9, 15, 7, tzinfo=dt.timezone.utc)
    k1 = C.enviar_diario(arm, [dict(situacao="inalterado")], momento=t)
    k2 = C.enviar_diario(arm, [dict(situacao="novo")], momento=t)
    assert k1 == "logs/capturas/2026-09-25.csv"
    assert k2 == "logs/capturas/2026-09-25__091507Z.csv"
    assert b"inalterado" in arm.objetos[k1] and b"novo" in arm.objetos[k2]
    assert C.enviar_diario(arm, [], momento=t) == "logs/capturas/2026-09-25__091507Z_2.csv"
    assert len(arm.objetos) == 3


def test_sem_credencial_a_mensagem_nomeia_a_variavel(tmp_path, monkeypatch):
    for v in A.VARIAVEIS:
        monkeypatch.delenv(v, raising=False)
    with pytest.raises(A.ArmazemIndisponivel, match="R2_BUCKET"):
        C.main(["--raiz", str(tmp_path), "--armazem", "s3"], abrir=_servidor_basico(),
               dormir=lambda s: None)


# ── o teto (politica.yaml -> armazem) ─────────────────────────────────────────
# A politica dos testes declara aviso 1 KB e teto 1 MB, em GB: os tres niveis cabem
# em bytes de teste. `_ocupar` poe o que ja esta no bucket antes da rodada.

def _politica_de_teste(tmp_path):
    raiz = tmp_path / "repo"
    (raiz / "alocacao").mkdir(parents=True)
    (raiz / "alocacao" / "politica.yaml").write_text(
        "armazem:\n  aviso_gb: 0.000001\n  teto_gb: 0.001\n", encoding="utf-8")
    return str(raiz)


def _ocupar(arm, n):
    arm.objetos["b3/x/ja.zip/" + "0" * 64 + ".zip"] = b"z" * n


def _rodar_com_teto(tmp_path, arm, monkeypatch):
    saida = tmp_path / "github_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(saida))
    rc, raiz, reg = _rodar(tmp_path, _servidor_basico(), arm,
                           "--raiz-repo", _politica_de_teste(tmp_path))
    return rc, reg, dict(ln.split("=", 1) for ln in saida.read_text().splitlines())


def test_teto_abaixo_do_aviso_captura_e_o_nivel_e_abaixo(tmp_path, monkeypatch):
    arm = A.ArmazemMemoria().limitar(10 ** 6)
    rc, reg, out = _rodar_com_teto(tmp_path, arm, monkeypatch)
    assert rc == 0 and out["armazem_nivel"] == "abaixo"
    assert [x["situacao"] for x in C.ler_registro(reg)] == ["novo"] * N_BASICO


def test_teto_entre_aviso_e_teto_captura_e_o_nivel_e_aviso(tmp_path, monkeypatch):
    arm = A.ArmazemMemoria().limitar(10 ** 6)
    _ocupar(arm, 5_000)
    rc, reg, out = _rodar_com_teto(tmp_path, arm, monkeypatch)
    assert rc == 0 and out["armazem_nivel"] == "aviso" and out["armazem_gb"] == "0.00"
    assert [x["situacao"] for x in C.ler_registro(reg)] == ["novo"] * N_BASICO


def test_teto_acima_recusa_registra_e_fica_vermelho(tmp_path, monkeypatch):
    """Nada de conteudo sobe; o registro ganha `recusado_por_teto` com o sha256 do que
    teria subido; o log sobe (e a prova); o estado nao avanca, entao a proxima rodada
    tenta de novo em vez de achar que ja tem."""
    arm = A.ArmazemMemoria().limitar(10 ** 6)
    _ocupar(arm, 10 ** 6)
    rc, reg, out = _rodar_com_teto(tmp_path, arm, monkeypatch)
    assert rc == 1 and out["armazem_nivel"] == "teto"
    assert _conteudo(arm) == ["b3/x/ja.zip/" + "0" * 64 + ".zip"]
    linhas = C.ler_registro(reg)
    assert [x["situacao"] for x in linhas] == ["recusado_por_teto"] * N_BASICO
    assert all(x["sha256"] and "teto" in x["motivo"] for x in linhas)
    assert C.estado_do_registro(linhas) == {}
    assert {x["situacao"] for x in _log(arm, _logs(arm)[-1])} == {"recusado_por_teto"}

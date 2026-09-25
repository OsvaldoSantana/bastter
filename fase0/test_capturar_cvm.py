# -*- coding: utf-8 -*-
"""Testes de `capturar_cvm.py` -- sem rede: o HTTP e um servidor falso injetado.

Cada correcao da auditoria de 24/09 (2.1 a 2.9) tem pelo menos um teste aqui, e o nome
do teste diz qual. O `tools/baixar_cvm.py` original reprovaria em todos: caminho absoluto,
`requests`, `range(2021, 2027)`, nenhum portao de integridade, snapshot com a hora da
captura, registro so de novo/atualizado, e nenhum --dry-run que se pudesse medir.
"""
from __future__ import annotations

import csv
import io
import json
import os
import sys
import urllib.error
import zipfile

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import capturar_cvm as C  # noqa: E402

DFP = C.INDICES["dfp"]
ITR = C.INDICES["itr"]
LM1 = "Mon, 05 Aug 2024 20:48:19 GMT"
LM2 = "Sun, 20 Sep 2026 10:33:49 GMT"


def _zip(membros, quando=(2024, 8, 5, 20, 45, 0)):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, texto in membros.items():
            z.writestr(zipfile.ZipInfo(nome, date_time=quando), texto)
    return buf.getvalue()


class _Resp:
    def __init__(self, corpo, cab):
        self._b = io.BytesIO(corpo)
        self.headers = cab

    def read(self, n=-1):
        return self._b.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class Servidor:
    """Um dados.cvm.gov.br de mentira. `cortar[url] = n` entrega so n bytes e declara o
    tamanho inteiro -- a forma exata do COTAHIST_A2026 de 18/09."""

    def __init__(self):
        self.arquivos = {}
        self.indices = {u: [] for u in C.INDICES.values()}
        self.falhas = {}
        self.cortar = {}
        self.chamadas = []
        self.sem_head = False

    def publicar(self, recurso, ano, corpo, lm=LM1, etag='"e1"'):
        url = f"{C.INDICES[recurso]}{recurso}_cia_aberta_{ano}.zip"
        self.arquivos[url] = dict(corpo=corpo, lm=lm, etag=etag)
        if ano not in self.indices[C.INDICES[recurso]]:
            self.indices[C.INDICES[recurso]].append(ano)
        return url

    def publicar_cad(self, corpo, lm=LM2):
        self.arquivos[C.CAD_URL] = dict(corpo=corpo, lm=lm, etag='"c"')

    def gets(self):
        return [u for m, u in self.chamadas if m == "GET" and u not in self.indices]

    def __call__(self, req, timeout=None):
        url, metodo = req.full_url, req.get_method()
        self.chamadas.append((metodo, url))
        self.ultimo_cabecalho = dict(req.header_items())
        fila = self.falhas.get(url)
        if fila:
            raise urllib.error.HTTPError(url, fila.pop(0), "falso", {}, None)
        if url in self.indices:
            rec = next(k for k, v in C.INDICES.items() if v == url)
            html = "".join(f'<a href="{rec}_cia_aberta_{a}.zip">x</a>'
                           for a in self.indices[url])
            return _Resp(html.encode(), {})
        a = self.arquivos[url]
        cab = {"Content-Length": str(len(a["corpo"])), "Last-Modified": a["lm"],
               "ETag": a["etag"]}
        if metodo == "HEAD":
            if self.sem_head:
                raise urllib.error.HTTPError(url, 405, "sem HEAD", {}, None)
            return _Resp(b"", cab)
        if "Range" in self.ultimo_cabecalho:
            return _Resp(a["corpo"][:1], dict(cab, **{
                "Content-Length": "1", "Content-Range": f"bytes 0-0/{len(a['corpo'])}"}))
        corpo = a["corpo"][:self.cortar[url]] if url in self.cortar else a["corpo"]
        return _Resp(corpo, cab)


def _rodar(tmp_path, srv, *extra, manifestar=None):
    raiz = str(tmp_path / "data" / "bronze" / "cvm")
    reg = str(tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv")
    chamadas = []
    rc = C.main(["--raiz", raiz, "--registro", reg, "--pausa", "0", *extra],
                abrir=srv, dormir=lambda s: None,
                manifestar=manifestar or (lambda r: chamadas.append(r)))
    return rc, raiz, reg, chamadas


def _linhas(reg):
    return C.ler_registro(reg)


def _servidor_basico():
    srv = Servidor()
    srv.publicar("dfp", 2012, _zip({"dfp_cia_aberta_2012.csv": "a;b\n1;2\n"}))
    srv.publicar("itr", 2012, _zip({"itr_cia_aberta_2012.csv": "a;b\n3;4\n"}))
    srv.publicar("fca", 2012, _zip({"fca_cia_aberta_2012.csv": "a;b\n5;6\n"}))
    srv.publicar_cad(b"CNPJ;DENOM\n1;X\n")
    return srv


# Quantos arquivos o servidor basico publica: um por recurso de INDICES, mais o cad.
# Derivado, nao escrito: era `3` em seis testes, e o FCA (P-132) fez 4 (N-01).
N_BASICO = len(_servidor_basico().arquivos)


# ── 2.1 ───────────────────────────────────────────────────────────────────────

def test_2_1_raiz_padrao_e_relativa_ao_repositorio():
    assert C.raiz_padrao() == os.path.join(C.raiz_repo(), "data", "bronze", "cvm")
    with open(C.__file__, encoding="utf-8") as f:
        fonte = f.read()
    assert "C:\\" not in fonte and "Users" not in fonte, "caminho absoluto no modulo"


def test_2_1_registro_padrao_fica_em_docs_acervo_fora_de_data():
    reg = C.registro_padrao(C.raiz_padrao())
    partes = reg.replace("\\", "/").split("/")
    assert partes[-3:] == ["acervo", "cvm", "capturas.csv"] and "data" not in partes


# ── 2.2 ───────────────────────────────────────────────────────────────────────

def test_2_2_sem_requests():
    with open(C.__file__, encoding="utf-8") as f:
        fonte = f.read()
    assert "import requests" not in fonte and "from requests" not in fonte
    assert "requests" not in sys.modules or C.__dict__.get("requests") is None


def test_2_2_retenta_em_503_e_429_e_pede_identity():
    srv = Servidor()
    url = srv.publicar("dfp", 2012, b"x")
    srv.falhas[url] = [503, 429]
    esperas = []
    with C.requisitar(url, srv, esperas.append) as r:
        assert r.read() == b"x"
    assert len(esperas) == 2
    assert srv.ultimo_cabecalho.get("Accept-encoding") == "identity"


def test_2_2_nao_retenta_em_404():
    srv = Servidor()
    url = srv.publicar("dfp", 2012, b"x")
    srv.falhas[url] = [404]
    with pytest.raises(urllib.error.HTTPError):
        C.requisitar(url, srv, lambda s: None)
    assert len(srv.chamadas) == 1


def test_2_2_servidor_sem_HEAD_da_o_tamanho_pelo_Content_Range():
    """O original caia para GET de 1 byte e lia o Content-Length da FAIXA (1): o portao
    compararia o arquivo inteiro com 1 byte para sempre."""
    srv = Servidor()
    url = srv.publicar("dfp", 2012, b"0123456789")
    srv.sem_head = True
    assert C.metadados(url, srv, lambda s: None)["tamanho"] == 10


# ── 2.3 ───────────────────────────────────────────────────────────────────────

def test_2_3_os_anos_vem_do_indice_e_2027_e_capturado(tmp_path):
    srv = _servidor_basico()
    srv.publicar("dfp", 2027, _zip({"dfp_cia_aberta_2027.csv": "a\n"}))
    rc, raiz, reg, _ = _rodar(tmp_path, srv)
    assert rc == 0
    assert os.path.exists(os.path.join(raiz, "dfp", "dfp_cia_aberta_2027.zip"))


def test_2_3_indice_vazio_e_erro_nao_nada_a_capturar(tmp_path):
    srv = Servidor()
    rc, *_ = _rodar(tmp_path, srv)
    assert rc == 1


# ── 2.4 ───────────────────────────────────────────────────────────────────────

def test_2_4_padrao_captura_todos_os_anos_inclusive_os_congelados(tmp_path):
    srv = _servidor_basico()
    for ano in (2020, 2021, 2022, 2023, 2024):
        srv.publicar("dfp", ano, _zip({f"dfp_cia_aberta_{ano}.csv": "a\n"}))
    rc, raiz, *_ = _rodar(tmp_path, srv)
    assert rc == 0
    assert os.path.exists(os.path.join(raiz, "dfp", "dfp_cia_aberta_2012.zip"))


def test_2_4_escopo_e_so_filtro(tmp_path):
    srv = _servidor_basico()
    for ano in range(2020, 2025):
        srv.publicar("dfp", ano, _zip({f"dfp_cia_aberta_{ano}.csv": "a\n"}))
    rc, raiz, *_ = _rodar(tmp_path, srv, "--escopo", "recentes")
    assert rc == 0
    assert not os.path.exists(os.path.join(raiz, "dfp", "dfp_cia_aberta_2012.zip"))
    assert os.path.exists(os.path.join(raiz, "dfp", "dfp_cia_aberta_2020.zip"))
    assert not os.path.exists(os.path.join(raiz, "cad"))


def test_2_4_portao_HEAD_nao_baixa_de_novo(tmp_path):
    srv = _servidor_basico()
    _rodar(tmp_path, srv)
    antes = len(srv.gets())
    rc, _, reg, _ = _rodar(tmp_path, srv)
    assert rc == 0 and len(srv.gets()) == antes, "segunda rodada sem mudanca nao baixa"


def test_2_4_congelado_regenerado_e_capturado(tmp_path):
    """CV-02: 2010-2019 foram regerados em 08/2024. Last-Modified novo -> baixa."""
    srv = _servidor_basico()
    _rodar(tmp_path, srv)
    srv.publicar("dfp", 2012, _zip({"dfp_cia_aberta_2012.csv": "a;b\n1;9\n"},
                                   quando=(2026, 9, 20, 10, 0, 0)), lm=LM2)
    rc, raiz, reg, _ = _rodar(tmp_path, srv)
    assert rc == 0
    sit = [x["situacao"] for x in _linhas(reg) if x["arquivo"] == "dfp_cia_aberta_2012.zip"]
    assert sit[-2:] == ["deslocado", "atualizado"]


# ── 2.5 ───────────────────────────────────────────────────────────────────────

def _versao_anterior(tmp_path):
    srv = _servidor_basico()
    _rodar(tmp_path, srv)
    raiz = str(tmp_path / "data" / "bronze" / "cvm")
    alvo = os.path.join(raiz, "dfp", "dfp_cia_aberta_2012.zip")
    with open(alvo, "rb") as f:
        return srv, alvo, f.read()


def test_2_5_download_cortado_e_rejeitado_e_a_anterior_fica(tmp_path):
    srv, alvo, antes = _versao_anterior(tmp_path)
    url = srv.publicar("dfp", 2012, _zip({"dfp_cia_aberta_2012.csv": "x" * 5000}), lm=LM2)
    srv.cortar[url] = 40
    rc, raiz, reg, manif = _rodar(tmp_path, srv)
    assert rc == 1
    with open(alvo, "rb") as f:
        assert f.read() == antes, "a versao anterior tem de ficar intacta"
    assert not os.path.exists(alvo + ".part")
    rej = [x for x in _linhas(reg) if x["situacao"] == "rejeitado"]
    assert len(rej) == 1 and "Content-Length" in rej[0]["motivo"]
    assert rej[0]["arquivo"] == "dfp_cia_aberta_2012.zip"
    assert not os.path.isdir(os.path.join(raiz, "dfp", "_snapshots"))
    assert manif == [], "captura com falha nao regrava o manifesto"


def test_2_5_zip_corrompido_e_rejeitado(tmp_path):
    srv, alvo, antes = _versao_anterior(tmp_path)
    bom = _zip({"dfp_cia_aberta_2012.csv": "y" * 5000})
    ruim = bytearray(bom)
    meio = len(ruim) // 3
    ruim[meio:meio + 20] = b"\x00" * 20                    # mesmo tamanho, CRC quebrado
    srv.publicar("dfp", 2012, bytes(ruim), lm=LM2)
    rc, raiz, reg, _ = _rodar(tmp_path, srv)
    assert rc == 1
    with open(alvo, "rb") as f:
        assert f.read() == antes
    rej = [x for x in _linhas(reg) if x["situacao"] == "rejeitado"]
    assert len(rej) == 1 and "zip" in rej[0]["motivo"]


# ── 2.6 ───────────────────────────────────────────────────────────────────────

def test_2_6_snapshot_tem_a_data_da_versao_e_o_sha_dos_bytes(tmp_path):
    srv, alvo, antes = _versao_anterior(tmp_path)
    srv.publicar("dfp", 2012, _zip({"dfp_cia_aberta_2012.csv": "novo\n"},
                                   quando=(2026, 9, 20, 10, 0, 0)), lm=LM2)
    _rodar(tmp_path, srv)
    snaps = os.listdir(os.path.join(os.path.dirname(alvo), "_snapshots"))
    import hashlib
    assert snaps == [f"dfp_cia_aberta_2012__v20240805__"
                     f"{hashlib.sha256(antes).hexdigest()[:12]}.zip"]


def test_2_6_data_da_versao_e_o_maior_membro_nao_o_primeiro(tmp_path):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(zipfile.ZipInfo("a.csv", date_time=(2024, 8, 5, 20, 45, 0)), "a")
        z.writestr(zipfile.ZipInfo("b.csv", date_time=(2024, 8, 6, 1, 0, 0)), "b")
    p = tmp_path / "x.zip"
    p.write_bytes(buf.getvalue())
    assert C.data_da_versao(str(p)) == "20240806"


def test_2_6_csv_usa_o_Last_Modified_e_sem_ele_DESCONHECIDA(tmp_path):
    p = tmp_path / "cad_cia_aberta.csv"
    p.write_bytes(b"a\n")
    assert C.data_da_versao(str(p), "Thu, 24 Sep 2026 04:12:17 GMT") == "20260924"
    assert C.data_da_versao(str(p), "") == "DESCONHECIDA"
    assert "__vDESCONHECIDA__" in C.nome_do_snapshot(str(p))


def test_2_6_plano_renomeia_snapshot_antigo_e_so_com_aplicar(tmp_path):
    raiz = tmp_path / "cvm"
    snaps = raiz / "dfp" / "_snapshots"
    snaps.mkdir(parents=True)
    corpo = _zip({"m.csv": "1"})
    antigo = snaps / "dfp_cia_aberta_2022__20260924T121630Z__0938723d8459.zip"
    antigo.write_bytes(corpo)
    plano = C.plano_de_snapshots(str(raiz))
    assert [x["acao"] for x in plano] == ["RENOMEAR"]
    assert antigo.exists(), "o plano nao muda nada"
    import hashlib
    esperado = f"dfp_cia_aberta_2022__v20240805__{hashlib.sha256(corpo).hexdigest()[:12]}.zip"
    assert os.path.basename(plano[0]["destino"]) == esperado
    C.aplicar(plano)
    assert os.listdir(snaps) == [esperado]
    assert C.plano_de_snapshots(str(raiz)) == [], "idempotente"


# ── 2.7 ───────────────────────────────────────────────────────────────────────

def test_2_7_toda_observacao_vira_linha_com_caminho_relativo(tmp_path):
    srv = _servidor_basico()
    _rodar(tmp_path, srv)
    _rodar(tmp_path, srv)
    linhas = _linhas(tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv")
    sit = [x["situacao"] for x in linhas]
    assert sit.count("novo") == N_BASICO and sit.count("inalterado") == N_BASICO
    for x in linhas:
        assert not os.path.isabs(x["caminho"]) and "\\" not in x["caminho"]
        assert x["caminho"].startswith("cvm/") or x["caminho"].startswith("data/")


def test_2_7_inalterado_pelo_portao_nao_repete_o_hash_do_disco(tmp_path):
    """N-01: o registro e o diario do HTTP. Sem bytes recebidos, sem sha256."""
    srv = _servidor_basico()
    _rodar(tmp_path, srv)
    _rodar(tmp_path, srv)
    inal = [x for x in _linhas(tmp_path / "docs" / "acervo" / "cvm" / "capturas.csv")
            if x["situacao"] == "inalterado"]
    assert inal and all(x["sha256"] == "" and x["motivo"] == "portao HEAD" for x in inal)


def test_2_7_estado_e_derivavel_do_registro(tmp_path):
    srv = _servidor_basico()
    _, raiz, reg, _ = _rodar(tmp_path, srv)
    p = os.path.join(raiz, "_manifest", "estado.json")
    with open(p, encoding="utf-8") as f:
        salvo = json.load(f)
    assert C.estado_do_registro(_linhas(reg)) == salvo
    os.remove(p)
    antes = len(srv.gets())
    _rodar(tmp_path, srv)
    assert len(srv.gets()) == antes, "sem estado.json o portao funciona igual"


# ── 2.8 ───────────────────────────────────────────────────────────────────────

def test_2_8_manifesto_roda_ao_fim_da_captura_sem_erro(tmp_path):
    srv = _servidor_basico()
    rc, raiz, _, manif = _rodar(tmp_path, srv)
    assert rc == 0 and manif == [raiz]


def test_2_8_manifesto_de_verdade_grava_fora_de_data(tmp_path):
    srv = _servidor_basico()
    raiz = str(tmp_path / "cvm")
    rc = C.main(["--raiz", raiz, "--registro", str(tmp_path / "reg.csv"), "--pausa", "0"],
                abrir=srv, dormir=lambda s: None)
    assert rc == 0
    gravados = [os.path.join(d, a) for d, _, fs in os.walk(tmp_path) for a in fs]
    assert any(os.path.basename(g).startswith("dt_captura=") for g in gravados)


# ── 2.9 ───────────────────────────────────────────────────────────────────────

def _retrato(pasta):
    out = {}
    for d, _, fs in os.walk(pasta):
        for a in fs:
            p = os.path.join(d, a)
            with open(p, "rb") as f:
                out[os.path.relpath(p, pasta)] = f.read()
    return out


def test_2_9_dry_run_nao_muda_byte_nenhum(tmp_path):
    srv = _servidor_basico()
    _rodar(tmp_path, srv)
    srv.publicar("dfp", 2012, _zip({"dfp_cia_aberta_2012.csv": "outro\n"}), lm=LM2)
    srv.publicar("dfp", 2027, _zip({"dfp_cia_aberta_2027.csv": "a\n"}))
    antes = _retrato(tmp_path)
    rc, _, _, manif = _rodar(tmp_path, srv, "--dry-run")
    assert rc == 0 and manif == []
    assert _retrato(tmp_path) == antes


def test_2_9_dry_run_num_acervo_vazio_nao_cria_pasta(tmp_path):
    srv = _servidor_basico()
    _rodar(tmp_path, srv, "--dry-run")
    assert _retrato(tmp_path) == {} and os.listdir(tmp_path) == []


# ── Tarefa 3: limpeza ─────────────────────────────────────────────────────────

def _acervo_sujo(tmp_path):
    raiz = tmp_path / "cvm"
    dfp = raiz / "dfp"
    dfp.mkdir(parents=True)
    igual = _zip({"dfp_cia_aberta_2012.csv": "a\n"})
    (dfp / "dfp_cia_aberta_2012.zip").write_bytes(igual)
    (dfp / "dfp_cia_aberta_2012 (1).zip").write_bytes(igual)
    (dfp / "dfp_cia_aberta_2024.zip").write_bytes(_zip({"dfp_cia_aberta_2024.csv": "b\n"}))
    unica = _zip({"dfp_cia_aberta_2024.csv": "c\n"}, quando=(2026, 9, 13, 9, 0, 0))
    (dfp / "dfp_cia_aberta_2024 (1).zip").write_bytes(unica)
    ext = dfp / "dfp_cia_aberta_2012"
    ext.mkdir()
    (ext / "dfp_cia_aberta_2012.csv").write_bytes(b"a\n")
    (dfp / "pagina.html").write_bytes(b"<html>")
    return raiz, dfp, unica


def test_3_copia_identica_sai_e_copia_unica_vira_snapshot(tmp_path):
    raiz, dfp, unica = _acervo_sujo(tmp_path)
    plano = {os.path.basename(x["origem"]): x for x in C.plano_de_limpeza(str(raiz))}
    assert plano["dfp_cia_aberta_2012 (1).zip"]["acao"] == "APAGAR"
    assert plano["dfp_cia_aberta_2024 (1).zip"]["acao"] == "RENOMEAR"
    assert "__v20260913__" in plano["dfp_cia_aberta_2024 (1).zip"]["destino"]
    assert plano["dfp_cia_aberta_2012"]["acao"] == "APAGAR"
    assert plano["pagina.html"]["acao"] == "DESCONHECIDO"
    C.aplicar(list(plano.values()))
    restantes = sorted(os.listdir(dfp))
    assert restantes == ["_snapshots", "dfp_cia_aberta_2012.zip", "dfp_cia_aberta_2024.zip",
                         "pagina.html"]
    [snap] = os.listdir(dfp / "_snapshots")
    assert (dfp / "_snapshots" / snap).read_bytes() == unica


def test_3_extracao_que_nao_bate_com_ZIP_nenhum_para_tudo(tmp_path):
    raiz, dfp, _ = _acervo_sujo(tmp_path)
    (dfp / "dfp_cia_aberta_2012" / "dfp_cia_aberta_2012.csv").write_bytes(b"editado\n")
    plano = C.plano_de_limpeza(str(raiz))
    assert any(x["acao"] == "PARAR" for x in plano)
    with pytest.raises(SystemExit):
        C.aplicar(plano)
    assert (dfp / "dfp_cia_aberta_2012 (1).zip").exists(), "PARAR nao aplica nada"


def test_3_main_arrumar_sem_aplicar_nao_muda_nada(tmp_path):
    raiz, _, _ = _acervo_sujo(tmp_path)
    antes = _retrato(raiz)
    assert C.main(["--raiz", str(raiz), "--arrumar", "limpeza"]) == 0
    assert _retrato(raiz) == antes


def test_registro_le_o_proprio_formato(tmp_path):
    reg = str(tmp_path / "r.csv")
    C.anotar(reg, dict(dt_captura="t", situacao="inalterado", etag='"a-b"'))
    with open(reg, encoding="utf-8") as f:
        assert next(csv.reader(f, delimiter=";")) == list(C.COLUNAS)
    assert C.ler_registro(reg)[0]["etag"] == '"a-b"'


def test_3_pasta_somente_leitura_sai_inteira(tmp_path):
    """24/09: `rmtree` apagou os CSVs de `dfp_cia_aberta_2012` e o Windows negou o `rmdir`
    da pasta, que tinha atributo ReadOnly. A pasta ficou vazia e o plano seguinte virou
    PARAR ("pasta vazia")."""
    import stat
    raiz, dfp, _ = _acervo_sujo(tmp_path)
    ext = dfp / "dfp_cia_aberta_2012"
    os.chmod(ext, stat.S_IREAD | stat.S_IEXEC)
    try:
        C.aplicar(C.plano_de_limpeza(str(raiz)))
        assert not ext.exists()
    finally:
        if ext.exists():
            os.chmod(ext, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)


def test_P132_o_FCA_entra_na_rotina_como_os_outros_recursos():
    """O universo do pre-registro ML identifica empresa pelo CD_CVM, e o COTAHIST so tem
    ticker. A ponte e o FCA (`valor_mobiliario`); se ele saisse da captura, a montagem do
    universo voltaria a depender de alguem baixar a mao (P7)."""
    urls = [u for u, rec in C.alvos(abrir=_servidor_basico(), dormir=lambda s: None)
            if rec == "fca"]
    assert urls == [C.INDICES["fca"] + "fca_cia_aberta_2012.zip"]

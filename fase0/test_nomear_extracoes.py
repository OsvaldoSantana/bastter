# -*- coding: utf-8 -*-
"""
test_nomear_extracoes.py -- as copias extraidas do COTAHIST com o nome certo (23/09/2026).

Sinteticos com a cara do acervo real: os tres jeitos de o membro vir nomeado (1986-2000,
2001, 2002+), a subpasta de ano do 2026, e cada recusa do modulo provada por um caso em
que ela tem de disparar.
"""
import os
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendario as C                                                  # noqa: E402
import nomear_extracoes as N                                            # noqa: E402


def _texto(ano, datas=("0102",)):
    linhas = [("00COTAHIST.%s" % ano + "BOVESPA " + "%s1228" % ano).ljust(245)]
    linhas += [("01" + ano + d).ljust(245) for d in datas]
    linhas += [("99COTAHIST.%s" % ano).ljust(245)]
    return "\r\n".join(linhas) + "\r\n"


def _par(pasta, ano, membro, extraido=None, texto=None):
    """Um ZIP do ano com `membro` dentro e, se pedido, a copia extraida ao lado."""
    texto = texto or _texto(ano)
    with zipfile.ZipFile(os.path.join(pasta, "COTAHIST_A%s.ZIP" % ano), "w",
                         zipfile.ZIP_DEFLATED) as z:
        z.writestr(membro, texto)
    if extraido:
        destino = os.path.join(pasta, extraido)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "w", encoding="latin-1", newline="") as f:
            f.write(texto)
    return texto


@pytest.fixture
def acervo(tmp_path):
    """Os quatro casos do disco dele, em miniatura."""
    p = str(tmp_path)
    _par(p, "1986", "COTAHIST.A1986", "COTAHIST.A1986")
    _par(p, "2001", "COTAHIST_A2001", "COTAHIST_A2001")
    _par(p, "2002", "COTAHIST_A2002.TXT", "COTAHIST_A2002.TXT")
    _par(p, "2026", "COTAHIST_A2026.TXT", os.path.join("COTAHIST_A2026", "COTAHIST_A2026.TXT"))
    return p


def _por_ano(linhas):
    return {ln["ano"]: ln for ln in linhas}


# ── o plano ───────────────────────────────────────────────────────────────────

def test_o_ano_do_cabecalho_e_o_ano_e_nao_o_ponto_antes_dele():
    """PRE-REQUISITO. `conferir_cabecalho` promete devolver o ano, e ate 23/09 devolvia
    `'.202'` -- a fatia [10:14] pega o ponto de `COTAHIST.` e perde o ultimo digito.
    Ninguem lia o retorno, por isso nada quebrou: e o arquivo declarando o que o codigo
    nao faz. Este modulo e o primeiro consumidor, e compara o ano do cabecalho com o do
    nome -- com o defeito, TODA copia seria recusada."""
    cab = ("00COTAHIST.2026BOVESPA 20260918").ljust(245)
    assert C.conferir_cabecalho(cab, "x") == ("2026", "20260918")
    cab = ("00COTAHIST.1986BOVESPA 19991210").ljust(245)
    assert C.conferir_cabecalho(cab, "x") == ("1986", "19991210")


def test_os_tres_nomes_da_B3_e_a_pasta_do_2026_viram_o_nome_certo(acervo):
    pa = _por_ano(N.plano(acervo))
    assert pa["1986"]["status"] == N.RENOMEAR
    assert pa["2001"]["status"] == N.RENOMEAR
    assert pa["2026"]["status"] == N.RENOMEAR
    assert pa["2002"]["status"] == N.JA_CORRETO
    for ln in pa.values():
        assert os.path.basename(ln["destino"]) == "COTAHIST_A%s.TXT" % ln["ano"]
        assert os.path.dirname(ln["destino"]) == acervo


def test_sem_aplicar_NADA_muda_no_disco(acervo):
    antes = sorted(os.walk(acervo))
    assert N.main(["--pasta", acervo]) == 0
    assert sorted(os.walk(acervo)) == antes


def test_aplicar_renomeia_tira_a_pasta_vazia_e_nao_toca_nos_ZIPs(acervo):
    zips = {n: os.path.getsize(os.path.join(acervo, n))
            for n in os.listdir(acervo) if n.endswith(".ZIP")}
    assert N.main(["--pasta", acervo, "--aplicar"]) == 0
    nomes = set(os.listdir(acervo))
    assert {"COTAHIST_A1986.TXT", "COTAHIST_A2001.TXT", "COTAHIST_A2002.TXT",
            "COTAHIST_A2026.TXT"} <= nomes
    assert not {"COTAHIST.A1986", "COTAHIST_A2001", "COTAHIST_A2026"} & nomes
    assert {n: os.path.getsize(os.path.join(acervo, n)) for n in zips} == zips


def test_depois_de_aplicar_o_calendario_continua_o_mesmo(acervo):
    """O leitor prefere o ZIP; renomear as copias nao pode mudar um pregao."""
    antes = C.pregoes(acervo)
    N.main(["--pasta", acervo, "--aplicar"])
    assert C.pregoes(acervo) == antes


def test_rodar_de_novo_nao_faz_nada(acervo):
    N.main(["--pasta", acervo, "--aplicar"])
    linhas = N.plano(acervo)
    assert {ln["status"] for ln in linhas} == {N.JA_CORRETO}


# ── as recusas -- cada uma com o caso que a dispara ──────────────────────────

def test_RECUSA_copia_diferente_do_ZIP(tmp_path):
    """Mesmo tamanho, um byte trocado: so o CRC pega. E o caso que importa -- uma copia
    editada a mao que ninguem sabe que foi editada."""
    p = str(tmp_path)
    texto = _par(p, "1990", "COTAHIST.A1990")
    with open(os.path.join(p, "COTAHIST.A1990"), "w", encoding="latin-1", newline="") as f:
        f.write(texto[:300] + ("9" if texto[300] != "9" else "8") + texto[301:])
    [ln] = N.plano(p)
    assert ln["status"] == N.RECUSADO and "CRC" in ln["motivo"]
    assert N.main(["--pasta", p, "--aplicar"]) == 1
    assert os.path.exists(os.path.join(p, "COTAHIST.A1990"))


def test_RECUSA_copia_cortada(tmp_path):
    p = str(tmp_path)
    texto = _par(p, "1991", "COTAHIST.A1991")
    with open(os.path.join(p, "COTAHIST.A1991"), "w", encoding="latin-1", newline="") as f:
        f.write(texto[:-10])
    [ln] = N.plano(p)
    assert ln["status"] == N.RECUSADO and "tamanho" in ln["motivo"]


def test_RECUSA_nome_de_um_ano_com_conteudo_de_outro(tmp_path):
    p = str(tmp_path)
    _par(p, "1992", "COTAHIST.A1992", texto=_texto("1993"))
    with open(os.path.join(p, "COTAHIST.A1992"), "w", encoding="latin-1", newline="") as f:
        f.write(_texto("1993"))
    [ln] = N.plano(p)
    assert ln["status"] == N.RECUSADO and "cabecalho diz" in ln["motivo"]


def test_RECUSA_sem_ZIP_ao_lado(tmp_path):
    p = str(tmp_path)
    with open(os.path.join(p, "COTAHIST.A1994"), "w", encoding="latin-1", newline="") as f:
        f.write(_texto("1994"))
    [ln] = N.plano(p)
    assert ln["status"] == N.RECUSADO and "sem COTAHIST_A1994.ZIP" in ln["motivo"]


def test_NAO_sobrescreve_quando_o_nome_certo_ja_existe(tmp_path):
    p = str(tmp_path)
    texto = _par(p, "1995", "COTAHIST.A1995", "COTAHIST.A1995")
    with open(os.path.join(p, "COTAHIST_A1995.TXT"), "w", encoding="latin-1", newline="") as f:
        f.write(texto)
    pa = _por_ano(N.plano(p))
    velho = [ln for ln in N.plano(p) if ln["origem"].endswith("COTAHIST.A1995")]
    assert velho[0]["status"] == N.DESTINO_EXISTE
    N.main(["--pasta", p, "--aplicar"])
    assert os.path.exists(os.path.join(p, "COTAHIST.A1995"))
    assert pa["1995"]


def test_pasta_que_nao_e_de_ano_fica_intacta(tmp_path):
    p = str(tmp_path)
    _par(p, "2026", "COTAHIST_A2026.TXT",
         os.path.join("COTAHIST_A2026", "COTAHIST_A2026.TXT"))
    with open(os.path.join(p, "COTAHIST_A2026", "LEIA.txt"), "w") as f:
        f.write("nota dele")
    N.main(["--pasta", p, "--aplicar"])
    assert os.path.isdir(os.path.join(p, "COTAHIST_A2026")), "pasta com outro arquivo nao some"
    assert os.path.exists(os.path.join(p, "COTAHIST_A2026.TXT"))


# ── P-131: nome certo nao e conteudo certo ────────────────────────────────────

def test_P131_nome_certo_com_conteudo_cortado_e_RECUSADO(tmp_path):
    """P-131. `JA_CORRETO` saia pelo `continue` antes de `conferir()`: dizia "o nome e o
    certo" e era lido como "a copia e o conteudo do ZIP". Uma copia truncada com o nome
    certo saia JA_CORRETO -- status com cara de medicao sem ter medido (F-02). Reprova
    contra a versao de 23/09."""
    p = str(tmp_path)
    texto = _par(p, "2003", "COTAHIST_A2003.TXT")
    with open(os.path.join(p, "COTAHIST_A2003.TXT"), "w", encoding="latin-1", newline="") as f:
        f.write(texto[:-10])
    [ln] = N.plano(p)
    assert ln["status"] == N.RECUSADO and "tamanho" in ln["motivo"]
    assert N.main(["--pasta", p]) == 1


def test_P131_nome_certo_com_conteudo_do_ZIP_continua_JA_CORRETO(tmp_path):
    """O outro lado: a conferencia nao pode transformar toda copia de nome certo em recusa."""
    p = str(tmp_path)
    _par(p, "2004", "COTAHIST_A2004.TXT", "COTAHIST_A2004.TXT")
    [ln] = N.plano(p)
    assert ln["status"] == N.JA_CORRETO and ln["motivo"] == ""

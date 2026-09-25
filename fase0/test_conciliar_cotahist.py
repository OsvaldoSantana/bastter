# -*- coding: utf-8 -*-
"""P-137: a conciliacao dos diarios do COTAHIST contra o anual (25/09/2026).

Os ZIPs sao sinteticos, com o leiaute MEDIDO no diario real de 24/09 (header
`00COTAHIST.<ano>BOVESPA <data>`, registros de 245 posicoes, trailer). Linha real da B3 nao
entra no repositorio: os termos vedam publicar dado de mercado (docs/fontes/b3-termos-de-uso.md).
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import os
import sys
import warnings
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import armazem as armazem_mod  # noqa: E402
import conciliar_cotahist as cc  # noqa: E402


def _linha(d, codneg, preco=100):
    corpo = f"01{d:%Y%m%d}02{codneg:<12}010EMPRESA     ON      NM   R$  {preco:013d}"
    return corpo.ljust(245)


def _zip(caminho, ano, linhas, gerado="20260930"):
    head = f"00COTAHIST.{ano}BOVESPA {gerado}".ljust(245)
    trail = f"99COTAHIST.{ano}BOVESPA {gerado}{len(linhas):011d}".ljust(245)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with zipfile.ZipFile(caminho, "w") as z:
        z.writestr(os.path.basename(caminho).replace(".ZIP", ".TXT"),
                   "\r\n".join([head, *linhas, trail]) + "\r\n")
    with open(caminho, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


D = dt.date


# ── as funcoes puras ─────────────────────────────────────────────────────────

def test_impressao_e_do_multiconjunto_e_nao_da_ordem():
    """CH-01: 4 dos 5 diarios de 17-23/09 tem outra ordem que o anual e o mesmo conteudo."""
    a, b = _linha(D(2026, 9, 24), "PETR4"), _linha(D(2026, 9, 24), "VALE3")
    assert cc.impressao([a, b]) == cc.impressao([b + "\r\n", a])
    assert cc.impressao([a, b]) != cc.impressao([a, a])       # multiconjunto, nao conjunto
    assert cc.impressao([a]) != cc.impressao([_linha(D(2026, 9, 24), "PETR4", 101)])


def test_data_do_diario_pelo_nome():
    assert cc.data_do_diario("COTAHIST_D24092026.ZIP") == D(2026, 9, 24)
    assert cc.data_do_diario("b3/cotahist_diario/COTAHIST_D01102026.ZIP") == D(2026, 10, 1)
    assert cc.data_do_diario("COTAHIST_A2026.ZIP") is None
    assert cc.data_do_diario("COTAHIST_D32132026.ZIP") is None


def test_conciliar_separa_as_cinco_situacoes():
    d1, d2, d3, d4, d5 = (D(2026, 9, x) for x in (15, 22, 23, 24, 25))
    x = lambda d, c="PETR4", p=100: _linha(d, c, p)  # noqa: E731
    anual = {d1: [x(d1)], d2: [x(d2), x(d2, "VALE3")], d3: [x(d3)], d4: [x(d4)]}
    diarios = {d2: [x(d2, "VALE3"), x(d2)],            # mesma coisa, outra ordem
               d3: [x(d3, p=999)],                     # conteudo diferente
               d5: [x(d5)]}                            # dia que o anual nao tem
    r = {x["data"]: x["situacao"] for x in cc.conciliar(anual, diarios, inicio_da_rotina=d2)}
    assert r == {d1: "ANTES_DA_ROTINA", d2: "CONFERE", d3: "DIVERGE",
                 d4: "SEM_DIARIO", d5: "DIARIO_SEM_PREGAO"}


def test_sem_diario_nenhum_a_ausencia_e_da_rotina_e_nao_perda():
    anual = {D(2026, 9, 1): [_linha(D(2026, 9, 1), "PETR4")]}
    assert cc.conciliar(anual, {}, None)[0]["situacao"] == "ANTES_DA_ROTINA"


def test_comparar_anuais_acha_o_dia_revisado_e_devolve_o_n():
    d1, d2, d3 = D(2026, 9, 1), D(2026, 9, 2), D(2026, 9, 3)
    antigo = {d1: [_linha(d1, "PETR4")], d2: [_linha(d2, "PETR4")]}
    novo = {d1: [_linha(d1, "PETR4")], d2: [_linha(d2, "PETR4", 555)], d3: [_linha(d3, "X")]}
    assert cc.comparar_anuais(novo, antigo) == (2, [d2])


def test_por_dia_le_o_leiaute_do_diario_real(tmp_path):
    d = D(2026, 9, 24)
    c = tmp_path / "COTAHIST_D24092026.ZIP"
    _zip(str(c), 2026, [_linha(d, "PETR4"), _linha(d, "VALE3")], gerado="20260924")
    out = cc.por_dia(str(c))
    assert list(out) == [d] and len(out[d]) == 2


# ── ponta a ponta, num repositorio falso ─────────────────────────────────────

REG_COLS = ("dt_captura", "recurso", "arquivo", "url", "http_last_modified", "etag",
            "sha256", "bytes", "caminho", "situacao", "motivo")


def _repo(tmp_path, entradas):
    """entradas: [(dt_captura, recurso, arquivo, sha)]. O byte fica no cache do acervo."""
    reg = tmp_path / "docs" / "acervo" / "b3" / "capturas.csv"
    reg.parent.mkdir(parents=True, exist_ok=True)
    with open(reg, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=REG_COLS, delimiter=";", lineterminator="\n")
        w.writeheader()
        for quando, rec, arq, sha in entradas:
            w.writerow(dict(dt_captura=quando, recurso=rec, arquivo=arq, sha256=sha,
                            situacao="novo"))
    return str(tmp_path)


def _no_cache(repo, recurso, arquivo, montar):
    tmp = os.path.join(repo, "_tmp", recurso, arquivo)
    sha = montar(tmp)
    k = armazem_mod.chave("b3", recurso, arquivo, sha)
    destino = os.path.join(repo, "data", "armazem", *k.split("/"))
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    os.replace(tmp, destino)
    return sha


def _cenario(tmp_path, anual_revisado=False):
    repo = str(tmp_path)
    d22, d23, d24 = D(2026, 9, 22), D(2026, 9, 23), D(2026, 9, 24)
    dias = {d: [_linha(d, "PETR4"), _linha(d, "VALE3")] for d in (d22, d23, d24)}
    sha_ant = _no_cache(repo, "cotahist", "COTAHIST_A2026.ZIP",
                        lambda p: _zip(p, 2026, dias[d22] + dias[d23], "20260923"))
    novo = dict(dias)
    if anual_revisado:
        novo[d22] = [_linha(d22, "PETR4", 777), _linha(d22, "VALE3")]
    sha_novo = _no_cache(repo, "cotahist", "COTAHIST_A2026.ZIP",
                         lambda p: _zip(p, 2026, [x for d in sorted(novo) for x in novo[d]]))
    diarios = []
    for d in (d23, d24):                                # 22 nunca foi capturado
        arq = f"COTAHIST_D{d:%d%m%Y}.ZIP"
        sha = _no_cache(repo, "cotahist_diario", arq,
                        lambda p, d=d: _zip(p, 2026, list(reversed(dias[d])), f"{d:%Y%m%d}"))
        diarios.append((f"{d:%Y-%m-%d}T23:00:00Z", "cotahist_diario", arq, sha))
    _repo(tmp_path, [("2026-09-24T19:00:00Z", "cotahist", "COTAHIST_A2026.ZIP", sha_ant),
                     *diarios,
                     ("2026-10-01T14:00:00Z", "cotahist", "COTAHIST_A2026.ZIP", sha_novo)])
    return repo


def _resultado(repo):
    with open(os.path.join(repo, cc.RESULTADO_RELATIVO), encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def _rodar(repo, *args):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")          # CapturaParada: o relogio do teste e fixo
        return cc.main(["--mes", "2026-09", *args], repo=repo, hoje=D(2026, 10, 1))


def test_ponta_a_ponta_confere_e_marca_o_antes_da_rotina(tmp_path):
    repo = _cenario(tmp_path)
    assert _rodar(repo) == 0
    r = {x["data"]: x["situacao"] for x in _resultado(repo)}
    assert r == {"2026-09-22": "ANTES_DA_ROTINA", "2026-09-23": "CONFERE",
                 "2026-09-24": "CONFERE"}


def test_ponta_a_ponta_e_idempotente(tmp_path):
    """Duas execucoes (regra 4 da 5-B): a segunda nao escreve linha nenhuma."""
    repo = _cenario(tmp_path)
    _rodar(repo)
    n = len(_resultado(repo))
    assert _rodar(repo) == 0 and len(_resultado(repo)) == n


def test_ponta_a_ponta_a_revisao_da_B3_sai_como_REVISADO_e_nao_como_falha(tmp_path):
    repo = _cenario(tmp_path, anual_revisado=True)
    assert _rodar(repo) == 0
    rev = [x for x in _resultado(repo) if x["situacao"] == "REVISADO"]
    assert [x["data"] for x in rev] == ["2026-09-22"]
    assert rev[0]["anual_anterior_sha256"] and "1 de 2" in rev[0]["detalhe"]


def test_ponta_a_ponta_diario_divergente_falha(tmp_path):
    """Mutacao: o diario de 24/09 passa a ter outro conteudo; o codigo de saida vira 1."""
    repo = _cenario(tmp_path)
    reg = os.path.join(repo, "docs", "acervo", "b3", "capturas.csv")
    d = D(2026, 9, 24)
    sha = _no_cache(repo, "cotahist_diario", "COTAHIST_D24092026.ZIP",
                    lambda p: _zip(p, 2026, [_linha(d, "PETR4", 1)], "20260924"))
    with open(reg, "a", encoding="utf-8", newline="") as f:
        f.write(f"2026-09-25T09:00:00Z;cotahist_diario;COTAHIST_D24092026.ZIP;;;;{sha};;;"
                f"atualizado;\n")
    assert _rodar(repo) == 1
    assert {x["data"]: x["situacao"] for x in _resultado(repo)}["2026-09-24"] == "DIVERGE"


def test_anual_anterior_ilegivel_avisa_e_nao_derruba(tmp_path, capsys):
    """P-102: a versao antiga cortada nao derruba a conciliacao do mes. A linha entra no
    MEIO do registro de proposito: a anterior e escolhida pelo instante, nao pela ordem."""
    repo = _cenario(tmp_path)
    ruim = _no_cache(repo, "cotahist", "COTAHIST_A2026.ZIP",
                     lambda p: (open(p, "wb").write(b"PK\x03\x04cortado") and None) or
                     hashlib.sha256(open(p, "rb").read()).hexdigest())
    reg = os.path.join(repo, "docs", "acervo", "b3", "capturas.csv")
    linhas = open(reg, encoding="utf-8").read().splitlines()
    linhas.insert(1, f"2026-09-28T10:00:00Z;cotahist;COTAHIST_A2026.ZIP;;;;{ruim};;;novo;")
    open(reg, "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    assert _rodar(repo) == 0
    assert "NAO rodou" in capsys.readouterr().err


def test_sem_o_anual_do_mes_seguinte_nao_faz_nada(tmp_path):
    repo = _cenario(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert cc.main(["--mes", "2026-10"], repo=repo, hoje=D(2026, 10, 2)) == 0
    assert not os.path.exists(os.path.join(repo, cc.RESULTADO_RELATIVO))


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

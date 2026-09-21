# -*- coding: utf-8 -*-
"""
test_moeda.py -- ACHADO C-03 com teste, e a P-77 que eu criei em 19/09 fechada.

DOIS DEFEITOS MEUS, do mesmo dia, consertados aqui e no `calendario.py`:

  1. **P2 violada.** `POS_DATA`, `POS_MODREF` e `LARGURA = 245` nasceram em Python, com a
     procedencia num comentario. Sao valores de FONTE EXTERNA, e a P2 e explicita: *todo
     parametro vive em YAML versionado, nunca em codigo*. Viraram
     `docs/schemas/cotahist-v02.yaml`, com revisao, URL, data de acesso e o status de cada
     enumeracao ao lado.

  2. **P-77 recriada.** `calendario.modref_de()` e `conferir_modref()` nasceram e
     **nenhum modulo do motor as chamava** -- so o teste. *Campo que so o teste toca e
     campo que o motor nao usa*, e e pior que orfao puro porque tem testemunha. Este modulo
     e o consumidor que faltava.

O QUE O C-03 MEDIU, e e a razao de o fator nao ser tabelado: das quatro trocas de moeda do
acervo, **tres NAO deixam quebra de preco**. Uma tabela de planos economicos teria acusado
as quatro e acertado uma. O fator sai da razao do mesmo `CODNEG`, com o controle do dia
anterior ao lado -- o instrumento do C-02.

O QUE ESTE MODULO NAO FAZ, e o teste prende isso: **nao aplica a reexpressao.** Escolher a
base e decisao de desenho do Osvaldo, e P6 manda deixar a lacuna declarada em vez de
inventar criterio. Mesmo desenho do `refinar.py` com `FACTOR_AMBIGUO`.
"""
from __future__ import annotations
import io
import os
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendario as C  # noqa: E402
import moeda as M  # noqa: E402

ACERVO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "data", "bronze", "b3", "cotahist")


def _lin(data, codneg="PETR4", preco=10.00, modref="R$", tpmerc="010"):
    return ("01" + data + "02" + codneg.ljust(12) + tpmerc + "PETROBRAS   "
            + "PN        " + "   " + modref.ljust(4)
            + "0" * 13 * 4 + f"{int(round(preco*100)):013d}").ljust(245) + "\r\n"


def _zip(caminho, ano, linhas):
    corpo = (("00COTAHIST." + ano + "BOVESPA 19991210").ljust(245) + "\r\n"
             + "".join(linhas))
    with zipfile.ZipFile(caminho, "w") as z:
        z.writestr(f"COTAHIST_A{ano}.TXT", corpo.encode("latin-1"))


# ── o leiaute vem do YAML (P2) ────────────────────────────────────────────────

def test_P2_as_posicoes_vem_do_YAML_e_nao_do_codigo():
    L = C.leiaute()
    assert L["campos"]["MODREF"] == (52, 56), "53-56 no documento, [52:56] em Python"
    assert L["campos"]["PREULT"] == (108, 121)
    assert L["largura"] == 245 and L["escala"] == 100
    assert L["revisao"] == "02"


def test_P2_sem_o_schema_o_modulo_RECUSA_em_vez_de_adivinhar():
    """P1: insumo ausente nao vira numero. Ler 245 posicoes com palpite devolve numero
    para tudo, e numero errado tem a cara de numero certo (F-02). E NAO ha fallback de
    constante em Python -- um fallback silencioso reintroduziria o defeito que a mudanca
    para YAML veio corrigir, e funcionaria, que e o pior resultado."""
    with pytest.raises(C.LeiauteAusente):
        C.carregar_leiaute("/caminho/que/nao/existe/cotahist.yaml")


def test_P2_a_enumeracao_de_MODREF_tambem_vem_do_YAML():
    assert set(C.modref_observados()) == {"CR$", "CZ$", "NCZ$", "R$"}


# ── fronteiras ────────────────────────────────────────────────────────────────

def test_a_fronteira_e_onde_o_MODREF_MAJORITARIO_muda(tmp_path):
    """Majoritario e nao unico: no dia da virada as duas moedas convivem no arquivo, e
    exigir unanimidade perderia a fronteira exatamente no dia em que ela acontece."""
    z = tmp_path / "COTAHIST_A1994.ZIP"
    _zip(z, "1994", [
        _lin("19940630", "AAA", 100.0, "CR$"), _lin("19940630", "BBB", 50.0, "CR$"),
        _lin("19940630", "CCC", 10.0, "R$"),                      # minoria no dia
        _lin("19940704", "AAA", 36.4, "R$"), _lin("19940704", "BBB", 18.2, "R$"),
    ])
    _p, moedas = M.por_dia(str(z))
    assert M.fronteiras(moedas) == [("19940630", "19940704", "CR$", "R$")]


def test_a_razao_e_do_MESMO_codneg_e_nao_de_populacoes(tmp_path):
    """O primeiro instrumento que eu tentei foi a mediana do dia, e ela nao distingue
    troca de escala de troca da composicao da amostra. Aqui o papel novo no dia seguinte
    NAO pode entrar na conta."""
    z = tmp_path / "COTAHIST_A1994.ZIP"
    _zip(z, "1994", [
        _lin("19940630", "AAA", 100.0, "CR$"), _lin("19940630", "BBB", 200.0, "CR$"),
        _lin("19940704", "AAA", 50.0, "R$"), _lin("19940704", "BBB", 100.0, "R$"),
        _lin("19940704", "ZZZ", 1.0, "R$"),          # so existe depois: nao e par
    ])
    precos, _m = M.por_dia(str(z))
    mediana, pares, _p10, _p90 = M.razao(precos, "19940630", "19940704")
    assert pares == 2 and mediana == pytest.approx(0.5)


def test_so_o_mercado_a_VISTA_entra(tmp_path):
    """Opcao e termo tem preco de outra natureza; misturar generos numa razao de precos
    produz um numero que nao mede nada."""
    z = tmp_path / "COTAHIST_A1994.ZIP"
    _zip(z, "1994", [
        _lin("19940630", "AAA", 100.0, "CR$"),
        _lin("19940630", "AAAT", 9.0, "CR$", tpmerc="030"),       # termo
        _lin("19940704", "AAA", 36.4, "R$"),
        _lin("19940704", "AAAT", 9.0, "R$", tpmerc="030"),
    ])
    precos, _m = M.por_dia(str(z))
    assert set(precos["19940630"]) == {"AAA"}


# ── os tres status ────────────────────────────────────────────────────────────

def _fronteira(tmp_path, n, fator, ano="1994"):
    z = tmp_path / f"COTAHIST_A{ano}.ZIP"
    linhas = []
    for i in range(n):
        linhas.append(_lin("19940629", f"T{i:03d}", 100.0, "CR$"))
        linhas.append(_lin("19940630", f"T{i:03d}", 100.0, "CR$"))
        linhas.append(_lin("19940704", f"T{i:03d}", 100.0 * fator, "R$"))
    _zip(z, ano, linhas)
    return M.medir(str(z))[0]


def test_status_QUEBRA_quando_a_razao_sai_da_faixa(tmp_path):
    r = _fronteira(tmp_path, 60, 1 / 2.75)
    assert r["status"] == M.QUEBRA
    assert r["fator"] == pytest.approx(2.75, rel=1e-3)
    assert r["controle"] == pytest.approx(1.0)


def test_status_SEM_QUEBRA_quando_a_razao_fica_na_faixa(tmp_path):
    """1986, 1989 e 1993 sao este caso no acervo real -- e sao TRES de quatro."""
    r = _fronteira(tmp_path, 60, 1.05)
    assert r["status"] == M.SEM_QUEBRA


def test_status_NAO_CONFIRMADO_com_poucos_pares(tmp_path):
    """O caso do Plano Collor: 2 pares, porque o mercado parou. **Uma mediana de 2 tem
    cara de resposta**, e e por isso que o corte existe."""
    r = _fronteira(tmp_path, 3, 1 / 2.75)
    assert r["status"] == M.NAO_CONFIRMADO and r["pares"] == 3


def test_o_FATOR_e_None_quando_o_status_nao_e_QUEBRA(tmp_path):
    """F-02 na camada do relato: numero de fator ao lado de um status que nao o autoriza e
    a coisa mais facil de alguem usar sem ler o status."""
    for n, f in ((60, 1.05), (3, 1 / 2.75)):
        assert _fronteira(tmp_path, n, f)["fator"] is None


def test_o_CONTROLE_vem_com_o_proprio_n(tmp_path):
    """Controle 1,0000 com um par tem a mesma cara de 1,0000 com 250, e so o segundo
    autoriza a conclusao. Foi o relatorio imprimindo 1,0000 exato em tres fronteiras que
    me mostrou que o controle sem n era decoracao."""
    r = _fronteira(tmp_path, 60, 1 / 2.75)
    assert r["pares_controle"] == 60


# ── A-05: enumeracao OBSERVADO com falha ruidosa ──────────────────────────────

def test_A05_modref_desconhecido_e_ACUSADO_e_o_comando_sai_diferente_de_zero(tmp_path,
                                                                            capsys):
    z = tmp_path / "COTAHIST_A1994.ZIP"
    _zip(z, "1994", [_lin("19940630", "AAA", 1.0, "UFIR")])
    assert M.main(["--acervo", str(tmp_path)]) == 2
    assert "FORA DA ENUMERACAO" in capsys.readouterr().err


def test_A05_o_desconhecido_NAO_e_descartado_nem_tratado_como_conhecido(tmp_path):
    z = tmp_path / "COTAHIST_A1994.ZIP"
    _zip(z, "1994", [_lin("19940630", "AAA", 1.0, "UFIR")])
    precos, moedas = M.por_dia(str(z))
    assert "UFIR" in moedas["19940630"], "a linha continua no dado"
    assert precos["19940630"]["AAA"] == 1.0
    assert C.conferir_modref({"UFIR"}) == {"UFIR"}


# ── o que ele NAO faz, e o teste prende ───────────────────────────────────────

def test_o_modulo_NAO_aplica_a_reexpressao(tmp_path):
    """P6: escolher a base e decisao de desenho, e ausencia de criterio e tarefa aberta,
    nao veredito. Se alguem acrescentar um `aplicar()` aqui sem a decisao escrita, este
    teste e o lugar onde a discussao volta."""
    r = _fronteira(tmp_path, 60, 1 / 2.75)
    assert set(r) == {"fronteira", "de", "para", "mediana", "pares", "p10", "p90",
                      "fator", "status", "controle", "pares_controle"}
    assert not hasattr(M, "aplicar"), \
        "aplicar a reexpressao exige decidir a base -- e isso e decisao dele"


# ── o acervo real, quando estiver na maquina ──────────────────────────────────

MEDIDO_19_09 = {
    "COTAHIST_A1986": ("19860227", "19860304", M.SEM_QUEBRA, 1.1973),
    "COTAHIST_A1989": ("19890113", "19890118", M.SEM_QUEBRA, 0.9677),
    "COTAHIST_A1990": ("19900313", "19900319", M.NAO_CONFIRMADO, 0.7142),
    "COTAHIST_A1994": ("19940630", "19940704", M.QUEBRA, 0.3644),
}


@pytest.mark.skipif(not os.path.isdir(ACERVO),
                    reason="acervo de COTAHIST ausente -- ESTE TESTE NAO RODOU")
def test_C03_o_acervo_real_reproduz_as_quatro_fronteiras_medidas():
    """O instantaneo do achado. Se um destes numeros mudar, ou o acervo mudou ou o
    instrumento mudou -- e as duas coisas exigem saber qual."""
    fora = io.StringIO()
    linhas, _desc, _ile = M.relatorio(ACERVO, saida=fora)
    por_arq = {r["arquivo"]: r for r in linhas}
    for arq, (a, b, status, mediana) in MEDIDO_19_09.items():
        if arq not in por_arq:
            continue
        r = por_arq[arq]
        assert r["fronteira"] == (a, b), arq
        assert r["status"] == status, arq
        assert r["mediana"] == pytest.approx(mediana, abs=5e-4), arq


@pytest.mark.skipif(not os.path.isdir(ACERVO),
                    reason="acervo de COTAHIST ausente -- ESTE TESTE NAO RODOU")
def test_C03_a_unica_quebra_do_acervo_mede_2_744_e_nao_2750():
    """A conversao legal e CR$ 2.750 = R$ 1, e a quebra medida e de **2,744**. As tres
    casas de diferenca sao o achado embutido: a coluna de preco antes de 04/07/1994 esta
    em MILHARES de cruzeiros reais. `NAO_CONFIRMADO` -- e a leitura que reconcilia a lei
    com a medicao, sem documento da B3 que a confirme."""
    fora = io.StringIO()
    linhas, _d, _i = M.relatorio(ACERVO, saida=fora)
    quebras = [r for r in linhas if r["status"] == M.QUEBRA]
    assert len(quebras) == 1, [r["arquivo"] for r in quebras]
    assert quebras[0]["fator"] == pytest.approx(2.744, abs=2e-3)
    assert 2.5 < quebras[0]["fator"] < 3.0, "nao e 2750: a escala ja esta em milhares"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

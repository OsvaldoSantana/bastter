# -*- coding: utf-8 -*-
"""A-12 -- a identidade de um evento nao pode ser montada com um campo DERIVADO.

O DEFEITO, e ele nao chegou a mim como defeito: chegou como um numero que mudou.

Ao fechar a P-114, o silver foi regerado com o calendario dos 41 anos e o `ajustar.py`
passou a colapsar **206** duplicatas onde antes colapsava **334**. Um numero que cai
128 unidades ao trocar o CALENDARIO e a denuncia: calendario nao cria nem destroi
evento, entao um dos dois numeros estava errado.

Estava o de cima. `_chave_de_evento` usava `data_ex`, que o projeto DERIVA -- e que no
silver de 11/09 estava VAZIO em 8.889 das 9.272 linhas, porque o calendario so cobria
2023. Duas linhas que diferiam apenas pela data colidiam na chave, e a colisao nao
aparecia como colisao: aparecia como *duplicata exata*, rotulo que o relatorio imprime
sem levantar suspeita.

O QUE FOI COLAPSADO DE VERDADE, medido linha a linha: das 334, **128 nao eram
duplicata**, e **as 128 se distinguiam pelo `ultimo_dia_com_direito`**. O BBDC pagou
R$0,01 em 30/04/1996, 30/08/1996, 30/12/1996, 28/02/1997 e 31/03/1997; para a chave
antiga, com `data_ex` vazio nas cinco, era um pagamento so.

A REGRA QUE SAI DAQUI, e ela e maior que este modulo:

    identidade se monta com o campo OBSERVADO, nunca com o DERIVADO.

`ultimo_dia_com_direito` vem da B3 e esta preenchido em 9.272 de 9.272. `data_ex` nos
calculamos, e o que nos calculamos pode faltar. **Campo vazio dentro de uma chave nao
distingue: ele UNE, e em silencio.** E o F-02 na camada da identidade -- ausencia de
insumo virando igualdade, em vez de virando zero.

E O PIOR ERA COMO ELE IA SUMIR. Com o calendario dos 41 anos a chave antiga tambem da
206, porque `data_ex` passa a estar preenchido. O defeito se auto-encobriria na proxima
corrida, e o unico vestigio seria a linha "334" no laudo de 21/09 -- que ninguem teria
motivo para reabrir. Por isso a correcao e da CHAVE, e nao do calendario: o teste abaixo
exige 206 nos DOIS silvers, isto e, exige que a contagem NAO dependa de quanto
calendario existe no disco.
"""
from __future__ import annotations
import csv
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ajustar as A  # noqa: E402

RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SILVER = os.path.join(RAIZ_REPO, "data", "silver")
SILVER_ESTREITO = os.path.join(SILVER, "eventos_silver_2026-09-11.csv")
SILVER_LARGO = os.path.join(SILVER, "eventos_silver_2026-09-11_cal-1986-2026.csv")

DUPLICATAS_REAIS = 206      # medido nos dois silvers, 23/09/2026
COLAPSO_ANTIGO = 334        # o que a chave com `data_ex` produzia no silver estreito


def _ev(**kw):
    """Uma linha de silver com so o que a chave le."""
    base = dict(origem="paginado", cod="BBDC", type_stock="PN", isin="BRBBDCACNPR8",
                ultimo_dia_com_direito="1996-04-30", data_ex="", tipo="DIVIDENDO",
                valor="0.01", ratio="", preco_vespera="",
                arquivo_origem="BBDC/pagina-001.json")
    base.update(kw)
    return base


# ── o portao: duas datas diferentes sao dois eventos ──────────────────────────

def test_A12_duas_datas_diferentes_com_data_ex_VAZIA_nao_colidem():
    """O caso real do BBDC, reduzido. Contra a versao anterior isto REPROVA: com
    `data_ex` vazio nos dois, a chave antiga devolvia a mesma tupla."""
    a = _ev(ultimo_dia_com_direito="1996-04-30")
    b = _ev(ultimo_dia_com_direito="1996-08-30")
    assert A._chave_de_evento(a) != A._chave_de_evento(b)


def test_A12_o_BBDC_de_1996_97_sao_CINCO_eventos_e_nao_um():
    """Os cinco pagamentos de R$0,01, todos com `data_ex` em branco."""
    dias = ["1996-04-30", "1996-08-30", "1996-12-30", "1997-02-28", "1997-03-31"]
    linhas = [_ev(ultimo_dia_com_direito=d) for d in dias]
    assert len({A._chave_de_evento(r) for r in linhas}) == 5


def test_A12_a_duplicata_EXATA_continua_sendo_colapsada():
    """O A-09 nao pode ter sido desfeito pela correcao. Mesmo dia, mesmo tudo: um so."""
    a, b = _ev(), _ev()
    assert A._chave_de_evento(a) == A._chave_de_evento(b)
    vistos, n = set(), 0
    for r in (a, b):
        k = A._chave_de_evento(r)
        if k in vistos:
            n += 1
        vistos.add(k)
    assert n == 1


def test_A12_a_chave_NAO_le_data_ex():
    """A regra escrita como teste: o campo derivado nao entra na identidade. Mudar
    `data_ex` sozinho nao pode mover a chave -- senao a identidade do evento passa a
    depender de quanto calendario existe no disco."""
    a = _ev(data_ex="")
    b = _ev(data_ex="1996-05-02")
    assert A._chave_de_evento(a) == A._chave_de_evento(b)


def test_A12_a_chave_le_o_campo_OBSERVADO():
    """O complemento do teste acima: se NENHUM campo de data entrasse na chave, os dois
    testes passariam e o defeito voltaria em outra forma."""
    a = _ev(ultimo_dia_com_direito="1996-04-30")
    b = _ev(ultimo_dia_com_direito="1996-04-29")
    assert A._chave_de_evento(a) != A._chave_de_evento(b)


# ── contra o acervo real: a contagem nao pode depender do calendario ──────────

def _colapsadas(caminho):
    with open(caminho, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    vistos, n = set(), 0
    for r in linhas:
        k = A._chave_de_evento(r)
        if k in vistos:
            n += 1
        else:
            vistos.add(k)
    return n, len(linhas)


@pytest.mark.skipif(not (os.path.isfile(SILVER_ESTREITO) and os.path.isfile(SILVER_LARGO)),
                    reason="os dois silvers de 11/09 ausentes -- ESTE TESTE NAO RODOU")
def test_A12_o_numero_de_duplicatas_NAO_depende_do_calendario():
    """O teste que nomeia o achado, e o unico que o pegaria de novo.

    Os dois arquivos tem as MESMAS 9.272 linhas e diferem so na coluna `data_ex`: um
    foi gravado com o calendario de 2023, o outro com o dos 41 anos. Duplicata e
    propriedade do DADO -- se a contagem muda, a chave esta lendo o que nao devia."""
    n_estreito, tot_e = _colapsadas(SILVER_ESTREITO)
    n_largo, tot_l = _colapsadas(SILVER_LARGO)
    assert tot_e == tot_l == 9272
    assert n_estreito == n_largo == DUPLICATAS_REAIS, (
        "a contagem de duplicatas mudou com o calendario: estreito=%d largo=%d. A chave "
        "voltou a ler um campo derivado." % (n_estreito, n_largo))


@pytest.mark.skipif(not os.path.isfile(SILVER_ESTREITO),
                    reason="silver de 11/09 ausente -- ESTE TESTE NAO RODOU")
def test_A12_a_chave_ANTIGA_colapsava_128_eventos_reais():
    """A prova por mutacao, com o numero do incidente. Reintroduz a chave de 21/09 e
    mede o estrago que ela fazia -- 334 contra 206, e as 128 distinguidas pelo campo
    observado. Um teste que so afirmasse o numero certo nao documentaria nada."""
    def chave_de_21_09(r):
        return (r["origem"], r["cod"], r["type_stock"], r["isin"], r["data_ex"],
                r["tipo"], r["valor"], r["ratio"], r["preco_vespera"],
                r["arquivo_origem"])

    with open(SILVER_ESTREITO, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))

    vistos, mortas_antiga = set(), []
    for r in linhas:
        k = chave_de_21_09(r)
        if k in vistos:
            mortas_antiga.append(r)
        else:
            vistos.add(k)
    assert len(mortas_antiga) == COLAPSO_ANTIGO

    vistos, mortas_nova = set(), []
    for r in linhas:
        k = A._chave_de_evento(r)
        if k in vistos:
            mortas_nova.append(r)
        else:
            vistos.add(k)
    assert len(mortas_nova) == DUPLICATAS_REAIS
    assert COLAPSO_ANTIGO - DUPLICATAS_REAIS == 128

    # e as 128 nao eram duplicata: o campo observado as distingue
    assert all(not r["data_ex"] for r in mortas_antiga if r not in mortas_nova), (
        "as linhas que so a chave antiga matou tinham `data_ex` PREENCHIDO -- entao a "
        "explicacao do achado (campo vazio unindo linhas) esta errada")


@pytest.mark.skipif(not os.path.isfile(SILVER_LARGO),
                    reason="silver largo ausente -- ESTE TESTE NAO RODOU")
def test_A12_o_campo_observado_nunca_falta_e_e_por_isso_que_ele_serve():
    """A premissa da correcao, medida em vez de suposta. Se `ultimo_dia_com_direito`
    pudesse faltar, trocar um campo vazio por outro nao consertaria nada."""
    with open(SILVER_LARGO, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    vazios = [r for r in linhas if not r["ultimo_dia_com_direito"]]
    assert not vazios, "%d linha(s) sem ultimo_dia_com_direito" % len(vazios)

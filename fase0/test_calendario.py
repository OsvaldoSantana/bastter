# -*- coding: utf-8 -*-
"""
test_calendario.py -- o calendario de pregoes (16/09/2026).

Modulo de PRODUCAO novo, e os portoes que pegariam um modulo sem teste vivem todos em
`alocacao/` -- `campos_mortos.py`, o P-15, o ruff do P-40. E a P-80 outra vez: a rotina
mede um terco do projeto. Enquanto ela nao for unificada, este arquivo e a rede.
"""

import datetime as dt
import os
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendario as C                                                   # noqa: E402

RAIZ_ACERVO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "bronze", "b3")


def _linha(data_aaaammdd, tipreg="01"):
    """Um registro COTAHIST: 245 posicoes, TIPREG em 1-2 e DATA em 3-10."""
    return (tipreg + data_aaaammdd).ljust(245)


def _cotahist(pasta, nome, datas, extra=()):
    linhas = [_linha("00000000", "00")]                      # header
    linhas += [_linha(d) for d in datas]
    linhas += list(extra)
    linhas += [_linha("99999999", "99")]                     # trailer
    caminho = os.path.join(pasta, nome)
    texto = "\n".join(linhas) + "\n"
    if nome.lower().endswith(".zip"):
        with zipfile.ZipFile(caminho, "w") as z:
            z.writestr(nome[:-4] + ".TXT", texto)
    else:
        with open(caminho, "w", encoding="latin-1") as f:
            f.write(texto)
    return caminho


def test_header_e_trailer_NAO_viram_pregao(tmp_path):
    """O header tem TIPREG 00 e o trailer 99, e os dois carregam data. Contar um deles
    como pregao poria 0000-00-00 no calendario -- ou, pior, uma data valida que nunca
    foi pregao."""
    _cotahist(str(tmp_path), "COTAHIST_A2023.TXT", ["20230102", "20230103"])
    datas, cob = C.pregoes(str(tmp_path))
    assert datas == {dt.date(2023, 1, 2), dt.date(2023, 1, 3)}
    assert cob == (dt.date(2023, 1, 2), dt.date(2023, 1, 3))


def test_o_calendario_pula_o_que_nao_e_pregao(tmp_path):
    """O ponto do modulo. 12/06/2023 e segunda; 13/06 e terca. Mas entre 21 e 26/02/2023
    esta o Carnaval, e NENHUMA regra generica de dia util sabe disso. O calendario sabe
    porque foi observado."""
    _cotahist(str(tmp_path), "COTAHIST_A2023.ZIP",
              ["20230217", "20230222", "20230223"])     # sexta, quarta de cinzas, quinta
    datas, cob = C.pregoes(str(tmp_path))
    # a vespera do Carnaval e 17/02; o proximo pregao NAO e 20 nem 21
    assert C.proximo_pregao(dt.date(2023, 2, 17), datas, cob) == dt.date(2023, 2, 22)


def test_fora_da_cobertura_devolve_NAO_SEI_e_nao_um_chute(tmp_path):
    """Tres recusas, e as tres sao "nao sei". Antes do inicio observado pode haver
    pregao que ninguem viu; no ultimo dia observado, o seguinte esta fora."""
    _cotahist(str(tmp_path), "COTAHIST_A2023.TXT", ["20230102", "20230103", "20231228"])
    datas, cob = C.pregoes(str(tmp_path))
    assert C.proximo_pregao(dt.date(2008, 4, 24), datas, cob) is None, "antes do inicio"
    assert C.proximo_pregao(dt.date(2023, 12, 28), datas, cob) is None, "o ultimo dia"
    assert C.proximo_pregao(dt.date(2026, 1, 1), datas, cob) is None, "depois do fim"
    assert C.proximo_pregao(None, datas, cob) is None
    assert C.proximo_pregao(dt.date(2023, 1, 2), datas, cob) == dt.date(2023, 1, 3)


def test_sem_COTAHIST_nenhum_o_calendario_e_vazio_e_DIZ_isso(tmp_path):
    """Nao levanta, nao inventa, e devolve cobertura (None, None) -- que e o que o
    `refinar.py` le para marcar a linha como SEM_CALENDARIO em vez de deixar em branco."""
    datas, cob = C.pregoes(str(tmp_path))
    assert datas == set() and cob == (None, None)
    assert C.pregoes(os.path.join(str(tmp_path), "nao-existe")) == (set(), (None, None))
    assert C.proximo_pregao(dt.date(2023, 6, 12), datas, cob) is None


def test_o_ZIP_ganha_do_TXT_do_mesmo_ano(tmp_path):
    """Sao o mesmo dado -- o `.TXT` e o `.ZIP` extraido, e o acervo guarda os dois. Ler
    os dois nao erra o resultado (e um `set`), mas le 557 MB a toa."""
    _cotahist(str(tmp_path), "COTAHIST_A2023.ZIP", ["20230102"])
    _cotahist(str(tmp_path), "COTAHIST_A2023.TXT", ["20230102", "20230103"])
    datas, _ = C.pregoes(str(tmp_path))
    assert datas == {dt.date(2023, 1, 2)}, "leu o TXT tambem, ou leu o TXT em vez do ZIP"


def test_anos_diferentes_SOMAM(tmp_path):
    _cotahist(str(tmp_path), "COTAHIST_A2023.TXT", ["20231228"])
    _cotahist(str(tmp_path), "COTAHIST_A2024.TXT", ["20240102"])
    datas, cob = C.pregoes(str(tmp_path))
    assert len(datas) == 2 and cob == (dt.date(2023, 12, 28), dt.date(2024, 1, 2))
    assert C.proximo_pregao(dt.date(2023, 12, 28), datas, cob) == dt.date(2024, 1, 2), \
        "a virada do ano so fecha porque os dois anos estao no acervo"


@pytest.mark.skipif(not os.path.isdir(RAIZ_ACERVO), reason="acervo nao esta neste ambiente")
def test_o_caso_REAL_do_FLRY_contra_o_acervo():
    """O caso que deu origem ao achado. Se nao houver COTAHIST no acervo, isto SKIPA --
    e o skip e honesto: sem o arquivo nao ha o que medir."""
    datas, cob = C.pregoes(RAIZ_ACERVO)
    if not datas:
        pytest.skip("nenhum COTAHIST no acervo -- ESTE TESTE NAO RODOU")
    if not (cob[0] <= dt.date(2023, 6, 12) < cob[1]):
        pytest.skip("o COTAHIST do acervo nao cobre 06/2023 -- ESTE TESTE NAO RODOU")
    assert C.proximo_pregao(dt.date(2023, 6, 12), datas, cob) == dt.date(2023, 6, 13), (
        "a BONIFICACAO da FLRY tem lastDatePrior 12/06/2023, e a maior queda do FLRY3 no "
        "ano inteiro (-7,78%) esta em 13/06 -- o pregao SEGUINTE")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

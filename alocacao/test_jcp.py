# -*- coding: utf-8 -*-
"""
test_jcp.py -- as quatro vigencias da aliquota do JCP, e as fronteiras entre elas.

As fronteiras sao o teste inteiro: no meio de uma faixa qualquer implementacao acerta.
E na virada -- e ha uma virada de SESSENTA E OITO DIAS em 2016 -- que se erra.
"""

import datetime as dt
import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jcp                                                              # noqa: E402

C = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "custos.yaml"), encoding="utf-8"))


@pytest.mark.parametrize("data,esperado,apelido", [
    ("1996-01-01", 0.15,  "primeiro dia do regime"),
    ("2010-06-15", 0.15,  "meio da faixa longa -- o comeco do acervo"),
    ("2015-12-31", 0.15,  "vespera da MP 694"),
    ("2016-01-01", 0.18,  "MP 694 comeca a produzir efeito"),
    ("2016-02-10", 0.18,  "dentro da janela de 68 dias"),
    ("2016-03-08", 0.18,  "ULTIMO dia de vigencia da MP 694"),
    ("2016-03-09", 0.15,  "MP caducou: a redacao original volta"),
    ("2020-07-01", 0.15,  "meio da segunda faixa de 15%"),
    ("2025-12-31", 0.15,  "vespera da LC 224"),
    ("2026-01-01", 0.175, "LC 224 art. 8o, vigencia pelo art. 14, III"),
    ("2026-09-13", 0.175, "hoje"),
])
def test_aliquota_por_data(data, esperado, apelido):
    a, _ = jcp.aliquota_jcp(data, C)
    assert a == esperado, apelido


def test_a_JANELA_DE_68_DIAS_existe_e_e_o_ponto_do_arquivo():
    """01/01/2016 a 08/03/2016: a MP 694 subiu a aliquota para 18% e caducou. O
    Ato Declaratorio no 5/2016 (09/03/2016) registra o encerramento em 08/03/2016.

    Sessenta e oito dias em que o JCP pagou 18%. Uma constante unica de 15% erra
    TODOS os proventos dessa janela -- e o erro e pequeno, plausivel e invisivel."""
    inicio = dt.date(2016, 1, 1)
    fim = dt.date(2016, 3, 8)
    assert (fim - inicio).days + 1 == 68
    dia = inicio
    while dia <= fim:
        assert jcp.aliquota_jcp(dia, C)[0] == 0.18, dia
        dia += dt.timedelta(days=1)
    assert jcp.aliquota_jcp(fim + dt.timedelta(days=1), C)[0] == 0.15


def test_antes_do_regime_RECUSA_em_vez_de_aproximar():
    """1995 e anterior ao instituto. Devolver 15% seria inventar imposto sobre um
    instituto que nao existia -- o F-02 na veia."""
    with pytest.raises(jcp.ForaDeVigencia):
        jcp.aliquota_jcp("1995-12-31", C)


def test_nao_ha_buraco_nem_sobreposicao_entre_as_vigencias():
    """A propriedade estrutural: as quatro faixas cobrem o tempo sem furo e sem
    sobrepor. Um furo devolveria ForaDeVigencia no meio da serie; uma sobreposicao
    faria a resposta depender da ORDEM da lista, que e acidente de edicao."""
    vs = C["tributacao"]["ir_jcp_fonte"]["valor"]
    for a, b in zip(vs, vs[1:]):
        fim_a = dt.date.fromisoformat(str(a["ate"]))
        ini_b = dt.date.fromisoformat(str(b["de"]))
        assert ini_b == fim_a + dt.timedelta(days=1), (
            "buraco ou sobreposicao entre %s e %s" % (a["ate"], b["de"]))
    assert vs[-1].get("ate") in (None, ""), "a ultima vigencia tem de ser aberta"


def test_liquido_de_PF_e_definitivo():
    """Par. 3o, II: para PF a tributacao na fonte e DEFINITIVA. O liquido e o liquido."""
    assert jcp.jcp_liquido(100.0, "2026-09-13", C) == pytest.approx(82.5)
    assert jcp.jcp_liquido(100.0, "2016-02-01", C) == pytest.approx(82.0)
    assert jcp.jcp_liquido(100.0, "2015-02-01", C) == pytest.approx(85.0)


def test_a_constante_declara_procedencia_e_nao_vence_por_prazo():
    no = C["tributacao"]["ir_jcp_fonte"]
    assert no["status"] == "COMPLETO"
    assert no["expira"] is None, "lei nao vence no aniversario"
    assert no["revisar_se"], "vence quando outra lei a altera -- e isso tem de estar escrito"
    for v in no["valor"]:
        assert v.get("fonte"), "cada vigencia carrega a norma que a criou: %r" % v


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

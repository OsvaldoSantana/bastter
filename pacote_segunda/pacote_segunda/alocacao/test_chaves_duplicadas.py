# -*- coding: utf-8 -*-
"""
test_chaves_duplicadas.py -- ACHADO E-09, e ele e o mais silencioso de todos.

`custos.yaml -> etf:` tinha `IMAB11:` DUAS vezes. A primeira (linha 171, escrita em
05/09) trazia `valor: 0.0025, status: PARCIAL`, com a pagina do gestor como fonte. A
segunda (linha 253) trazia `valor: null, status: NAO_CONFIRMADO`.

**PyYAML fica com a ULTIMA, sem aviso nenhum.** Resultado: o trabalho de 05/09 estava
no arquivo e nao tinha efeito. O `PENDENCIAS.md` dizia "fechada 05/09 — 0,25%", o motor
via NAO_CONFIRMADO, e os dois discordaram em silencio por oito dias.

E o defeito nao e do IMAB11 -- e do FORMATO: qualquer constante deste projeto pode ser
apagada por uma duplicata em outro ponto do mesmo arquivo, e nada acusa. Este teste e a
guarda da CLASSE, nao do caso.
"""

import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "auditoria"))

import chaves_duplicadas as D                                           # noqa: E402

YAMLS = ["custos.yaml", "politica.yaml", "catalogo.yaml", "instituicoes.yaml",
         "teses.yaml", "perfil.yaml", "estado.exemplo.yaml"]


@pytest.mark.parametrize("nome", YAMLS)
def test_nenhuma_chave_duplicada(nome):
    caminho = os.path.join(AQUI, nome)
    if not os.path.exists(caminho):
        pytest.skip("%s nao existe neste ambiente" % nome)
    D.carregar_estrito(caminho)      # levanta DuplicataProibida se houver


def test_a_guarda_PEGA_uma_duplicata_de_verdade(tmp_path):
    """Guarda que nunca falhou e guarda que ninguem sabe se funciona. Esta reproduz o
    E-09 em miniatura: o mesmo nome duas vezes, a segunda apagando a primeira."""
    f = tmp_path / "x.yaml"
    f.write_text("etf:\n  IMAB11:\n    valor: 0.0025\n  IMAB11:\n    valor: null\n",
                 encoding="utf-8")
    with pytest.raises(D.DuplicataProibida) as e:
        D.carregar_estrito(str(f))
    assert "IMAB11" in str(e.value)
    import yaml
    # e a prova de que o PyYAML padrao NAO reclama -- fica com a ultima, calado
    assert yaml.safe_load(open(f, encoding="utf-8"))["etf"]["IMAB11"]["valor"] is None


def test_merge_NAO_e_duplicata(tmp_path):
    """O `catalogo.yaml` usa ancora e merge (`<<: *base`). Sobrescrever uma chave da
    ancora e o PROPOSITO do merge, nao um defeito.

    A primeira versao desta ferramenta reprovava o catalogo.yaml inteiro por isso --
    o instrumento com alcance menor que o sistema, e desta vez em cima da regua que eu
    tinha escrito na mesma manha (§5-B). Por isso este teste existe."""
    f = tmp_path / "m.yaml"
    f.write_text("base: &b\n  a: 1\n  b: 2\nfilho:\n  <<: *b\n  b: 99\n", encoding="utf-8")
    d = D.carregar_estrito(str(f))
    assert d["filho"] == {"a": 1, "b": 99}


def test_a_taxa_do_IMAB11_esta_viva_no_arquivo():
    """O caso concreto, e a razao de o E-09 ter sido caro: nao basta o numero estar
    escrito, ele precisa ser o que o `yaml.safe_load` devolve."""
    import yaml
    caminho = os.path.join(AQUI, "custos.yaml")
    if not os.path.exists(caminho):
        pytest.skip("custos.yaml nao esta neste ambiente")
    C = yaml.safe_load(open(caminho, encoding="utf-8"))
    no = C["etf"]["IMAB11"]
    assert no["status"] == "COMPLETO", "a taxa do IMAB11 voltou a nao valer"
    assert no["valor"] == 0.0025
    comp = no["composicao"]
    assert abs(sum(v for v in comp.values() if v) - no["valor"]) < 1e-12, \
        "os componentes da taxa nao somam o total declarado"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

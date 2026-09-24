# -*- coding: utf-8 -*-
"""
B-11 (sessao-b, 24/09/2026): `estado_io._registro` decidia se um campo e texto com
`f.type == "str"`. `f.type` e a anotacao CRUA: so e a string "str" porque o
`alocacao.py` tem `from __future__ import annotations`. Um dataclass de um modulo sem o
__future__ tem `f.type is str`, a comparacao da False, e o campo de texto vai para
`_num()` -- que o reprova como "nao e numero". Nada no nome do erro aponta a causa.

O modulo sintetico abaixo e escrito em disco e importado de verdade, SEM o __future__:
e a condicao do defeito, e este arquivo de teste tambem nao tem o __future__ para que
nada aqui possa mascara-la.
"""
import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import estado_io

FONTE = (
    "import dataclasses\n"
    "@dataclasses.dataclass\n"
    "class Conta:\n"
    "    nome: str\n"
    "    saldo: float\n"
)


def _importar(tmp_path):
    p = tmp_path / "modulo_sem_future.py"
    p.write_text(FONTE, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("modulo_sem_future", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_B11_o_modulo_sintetico_de_fato_nao_tem_future(tmp_path):
    """Sem esta pre-condicao o teste de baixo provaria nada: se `f.type` fosse "str"
    aqui, a versao antiga tambem passaria."""
    import dataclasses
    Conta = _importar(tmp_path).Conta
    assert dataclasses.fields(Conta)[0].type is str


def test_B11_campo_str_de_modulo_sem_future_passa_pelo_registro(tmp_path):
    Conta = _importar(tmp_path).Conta
    problemas = []
    r = estado_io._registro({"nome": "corrente", "saldo": "1.234,50"}, Conta,
                            "contas[0]", problemas)
    assert r is not None, f"o registro tinha de se sustentar: {problemas}"
    assert r.nome == "corrente" and r.saldo == 1234.50
    assert not any("nome" in x for x in problemas), (
        f"o campo de texto foi tratado como numero: {problemas}")


def test_B11_campo_str_em_branco_continua_reprovado(tmp_path):
    """O espelho: a correcao nao pode ter afrouxado a guarda de texto em branco."""
    Conta = _importar(tmp_path).Conta
    problemas = []
    assert estado_io._registro({"nome": "  ", "saldo": 10}, Conta, "c", problemas) is None
    assert "c.nome: nao preenchido" in problemas

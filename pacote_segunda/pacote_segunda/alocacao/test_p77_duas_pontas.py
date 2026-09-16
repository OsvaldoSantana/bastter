# -*- coding: utf-8 -*-
"""
test_p77_duas_pontas.py -- o campo que a P-13 criou e ninguem leu.

A P-13 partiu `isento_ir` em dois campos porque o FII nao cabia num booleano: o
RENDIMENTO distribuido e isento e o GANHO e tributado a 20%. Ela criou
`aliquota_ganho`, o catalogo o preencheu com a lei citada ao lado -- e **nenhuma linha
do motor o leu**. Medido em 13/09/2026: as quatro unicas leituras estao em
`test_alocacao.py`.

Mudanca de ESQUEMA anunciada como correcao de COMPORTAMENTO. E o padrao recorrente do
projeto na forma mais enganosa: o teste provava o esquema, e ninguem provava o resto.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alocacao as A                                                    # noqa: E402
from motor import carregar as carregar_custos                           # noqa: E402

C = carregar_custos()
P = A.carregar_politica()


def _rota(**kw):
    base = dict(id="teste", nome="teste", funcoes=["LIQUIDEZ"], exposicao="caixa",
                indexador="cdi", rendimento_fator=1.0)
    base.update(kw)
    return A.RotaAloc(**base)


# ── o regime, caso a caso ────────────────────────────────────────────────────

def test_sem_aliquota_ganho_usa_a_tabela_geral():
    fixa, motivo = A.regime_tributario(_rota())
    assert fixa is None and motivo is None, "None = delega para aliquota_ir_rf"


def test_isento_sem_aliquota_ganho_continua_isento():
    """LCI/LCA antes da P-13, e o comportamento nao pode ter mudado."""
    fixa, motivo = A.regime_tributario(_rota(isento_ir_rendimento=True))
    assert fixa == 0.0 and motivo is None


def test_as_duas_pontas_isentas_e_um_caso_resolvido():
    """LCI/LCA depois da P-13: `aliquota_ganho: 0.0` nao muda nada, e nao deve."""
    fixa, motivo = A.regime_tributario(
        _rota(isento_ir_rendimento=True, aliquota_ganho=0.0))
    assert fixa == 0.0 and motivo is None


def test_P77_pontas_divergentes_RECUSAM_em_vez_de_chutar():
    """O caso do FII, e o coracao da P-77. Rendimento isento + ganho a 20% sao DUAS
    aliquotas; esta funcao modela UMA. A resposta honesta nao e um numero aproximado
    -- e recusar dizendo por que. Antes da correcao, `r.isento_ir` devolvia True e o
    imposto INTEIRO virava zero: errado para MENOS, que e a direcao lisonjeira."""
    fixa, motivo = A.regime_tributario(
        _rota(isento_ir_rendimento=True, aliquota_ganho=0.20))
    assert fixa is None
    assert motivo and "DUAS" in motivo and "20.0%" in motivo


def test_P77_o_motivo_NAO_some_com_o_None(  ):
    """Foi um `None` calado que escondeu a P-77 por oito dias. O motivo sobe."""
    r = _rota(isento_ir_rendimento=True, aliquota_ganho=0.20)
    motivos = {}
    assert A.retorno_liquido_aa(r, C, 180, 10000.0, motivos) is None
    assert "teste" in motivos and "20.0%" in motivos["teste"]


def test_P77_sem_o_dict_de_motivos_nao_quebra():
    """Todo chamador antigo passa quatro argumentos. O quinto e opcional."""
    r = _rota(isento_ir_rendimento=True, aliquota_ganho=0.20)
    assert A.retorno_liquido_aa(r, C, 180, 10000.0) is None


# ── o que NAO pode ter mudado ────────────────────────────────────────────────

@pytest.mark.parametrize("rid,esperado", [
    ("lci", 0.13900), ("lca", 0.13900), ("rdb_100", 0.10773),
    ("td_reserva", 0.10850), ("poupanca", 0.08027), ("picpay_cofrinho", 0.10988),
])
def test_instantaneo_dourado_das_rotas_de_caixa(rid, esperado):
    """Medido ANTES do patch, em 13/09/2026. Se qualquer um mudar, a correcao mexeu
    em quem nao estava quebrado."""
    r = [x for x in A.catalogo(C) if x.id == rid][0]
    assert A.retorno_liquido_aa(r, C, 180, 10000.0) == pytest.approx(esperado, abs=1e-5)


def test_nenhuma_rota_do_catalogo_e_recusada_hoje():
    """A P-77 e LATENTE: hoje nenhuma rota de renda fixa tem pontas divergentes. O
    unico `aliquota_ganho` nao-zero e o do FII, que e `indexador: rv` e ja devolvia
    None antes da linha do imposto. Este teste existe para o dia em que deixar de ser
    verdade -- ele avisa, em vez de deixar um numero errado passar."""
    motivos = {}
    for r in A.catalogo(C):
        A.retorno_liquido_aa(r, C, 180, 10000.0, motivos)
    assert motivos == {}, (
        "rota(s) com pontas tributarias divergentes entraram no catalogo: %s. Nao e "
        "erro -- e o dia em que a P-77 deixou de ser latente. Decida o modelo das "
        "duas pontas ANTES de deixar a rota competir." % motivos)


# ── a guarda estrutural: campo preenchido tem de ser LIDO pelo motor ─────────

def test_P77_todo_campo_que_o_catalogo_preenche_e_lido_pelo_MOTOR():
    """A generalizacao da P-77, e a unica parte deste arquivo que impede a PROXIMA.

    `aliquota_ganho` passou despercebido porque era lido -- por `test_alocacao.py`, e
    so por ele. **Campo que so o teste toca e campo que o motor nao usa:** o teste
    prova o esquema e ninguem prova o comportamento. Esta guarda mede o MOTOR, e de
    proposito ignora os proprios testes."""
    import ast

    import yaml

    aqui = os.path.dirname(os.path.abspath(__file__))
    cru = yaml.safe_load(open(os.path.join(aqui, "catalogo.yaml"), encoding="utf-8"))

    preenchidos = set()
    for _rid, spec in (cru.get("rotas") or {}).items():
        if isinstance(spec, dict):
            preenchidos.update(k for k in spec if not k.startswith("_"))

    lidos_pelo_motor = set()
    for f in sorted(os.listdir(aqui)):
        if not f.endswith(".py") or f.startswith("test_") or f == "conftest.py":
            continue
        try:
            arv = ast.parse(open(os.path.join(aqui, f), encoding="utf-8").read())
        except SyntaxError:
            continue
        for n in ast.walk(arv):
            if isinstance(n, ast.Attribute):
                lidos_pelo_motor.add(n.attr)
            elif isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) \
                    and isinstance(n.slice.value, str):
                lidos_pelo_motor.add(n.slice.value)
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                    and n.func.attr in ("get", "setdefault") and n.args \
                    and isinstance(n.args[0], ast.Constant):
                lidos_pelo_motor.add(n.args[0].value)

    # prosa e procedencia descrevem o dado, nao prometem comportamento
    META = {"nome", "nota", "procedencia", "status", "base", "decidido_em",
            "revisar_se", "fonte", "acesso", "motivo", "bloqueio", "regra", "fontes"}
    mortos = sorted(preenchidos - lidos_pelo_motor - META)
    assert not mortos, (
        "campo(s) que o catalogo PREENCHE e o motor nao le: " + ", ".join(mortos)
        + ". Ou o motor passa a ler, ou o campo sai do catalogo. Um campo preenchido "
          "e nao lido e uma promessa que o codigo nao cumpre -- foi a P-77 inteira.")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

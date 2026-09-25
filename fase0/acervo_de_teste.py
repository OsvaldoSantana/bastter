# -*- coding: utf-8 -*-
"""acervo_de_teste.py -- quando um teste contra o acervo real pode pular. P-142 (25/09/2026).

O DEFEITO: nove testes do C-02 pularam em TODA rodada desde a P-114, porque procuravam o
COTAHIST em `data/bronze/b3/` e ele mora em `data/bronze/b3/cotahist/`. A mensagem dizia
"ESTES TESTES NAO RODARAM" -- verdadeira, na maquina que TEM o acervo, e ninguem le a
lista de skips. Um `skipif(not os.path.isfile(...))` nao distingue "esta maquina nao tem
acervo" (CI, clone novo: pular e certo) de "o acervo esta aqui e o arquivo esperado nao"
(caminho errado, arquivo renomeado, silver nao gerado: e defeito).

A REGRA, uma so para todo `test_REAL_*`:
  a PASTA DO ACERVO do arquivo NAO existe -> pula, dizendo que nao rodou;
  a pasta existe e falta o arquivo          -> FALHA, nomeando o que falta.

A PASTA DO ACERVO (refinada na tarefa de metricas, 25/09): `data/bronze/<fonte>` para o bronze
e `data/<camada>` para o resto (`data/silver`). Antes era a raiz `data/`. O motivo e o job
semanal do GitHub: ele materializa do armazem o bronze que o R2 tem (COTAHIST, CVM), e o silver
nao esta no R2 -- com a raiz, os testes de silver FALHARIAM por um insumo que aquela maquina
nunca teve. O caso da P-142 continua falhando: `data/bronze/b3` existia e o arquivo nao.

`fase0/test_acervo_de_teste.py` reprova arquivo de teste com `test_REAL_*` que ainda use
`skipif`/`pytest.skip` em vez disto.
"""
import os

import pytest

RAIZ_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def pasta_do_acervo(caminho, raiz=RAIZ_DATA):
    """`data/bronze/<fonte>` para o bronze, `data/<camada>` para o resto."""
    partes = os.path.relpath(os.path.abspath(caminho), os.path.abspath(raiz)).split(os.sep)
    if partes[0] == os.pardir:
        return os.path.abspath(raiz)
    n = 2 if partes[0] == "bronze" else 1
    return os.path.join(os.path.abspath(raiz), *partes[:min(n, len(partes) - 1)])


def exigir_acervo(*caminhos, raiz=RAIZ_DATA):
    """Pula so quando a PASTA DO ACERVO nao existe; com ela, arquivo faltando e falha."""
    ausentes = sorted({pasta_do_acervo(c, raiz) for c in caminhos
                       if not os.path.isdir(pasta_do_acervo(c, raiz))})
    if ausentes:
        pytest.skip(f"sem acervo nesta maquina ({ausentes} nao existe) -- ESTE TESTE NAO RODOU")
    faltando = [c for c in caminhos if not os.path.exists(c)]
    if faltando:
        pytest.fail(f"o acervo existe e falta o que este teste le: {faltando}. Caminho "
                    f"errado ou arquivo nao gerado e defeito, nao ambiente (P-142).",
                    pytrace=False)

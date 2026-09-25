# -*- coding: utf-8 -*-
"""acervo_de_teste.py -- quando um teste contra o acervo real pode pular. P-142 (25/09/2026).

O DEFEITO: nove testes do C-02 pularam em TODA rodada desde a P-114, porque procuravam o
COTAHIST em `data/bronze/b3/` e ele mora em `data/bronze/b3/cotahist/`. A mensagem dizia
"ESTES TESTES NAO RODARAM" -- verdadeira, na maquina que TEM o acervo, e ninguem le a
lista de skips. Um `skipif(not os.path.isfile(...))` nao distingue "esta maquina nao tem
acervo" (CI, clone novo: pular e certo) de "o acervo esta aqui e o arquivo esperado nao"
(caminho errado, arquivo renomeado, silver nao gerado: e defeito).

A REGRA, uma so para todo `test_REAL_*`:
  a pasta do acervo (`data/`) NAO existe  -> pula, dizendo que nao rodou;
  a pasta existe e falta um arquivo       -> FALHA, nomeando o que falta.

`fase0/test_acervo_de_teste.py` reprova arquivo de teste com `test_REAL_*` que ainda use
`skipif`/`pytest.skip` em vez disto.
"""
import os

import pytest

RAIZ_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def exigir_acervo(*caminhos, raiz=RAIZ_DATA):
    """Pula so quando a maquina nao tem acervo; com acervo, arquivo faltando e falha."""
    if not os.path.isdir(raiz):
        pytest.skip(f"sem acervo nesta maquina ({raiz} nao existe) -- ESTE TESTE NAO RODOU")
    faltando = [c for c in caminhos if not os.path.exists(c)]
    if faltando:
        pytest.fail(f"o acervo existe ({raiz}) e falta o que este teste le: {faltando}. "
                    f"Caminho errado ou arquivo nao gerado e defeito, nao ambiente (P-142).",
                    pytrace=False)

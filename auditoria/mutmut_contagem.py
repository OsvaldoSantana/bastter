#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mutmut_contagem.py -- quantas alteracoes o mutmut GEROU, TESTOU, matou e deixou vivas.

POR QUE ELE EXISTE (25/09/2026, CI-03). A primeira execucao do workflow Mutacao ficou verde em
46 s, com quatro modulos-alvo. Verde nao dizia se alguma alteracao tinha sido testada, e o
log do job so abre com login. Mutacao verde sem mutante testado e o F-02: ausencia de
medicao com a cara de "nenhum sobrevivente".

A fonte e o que o mutmut grava, nao o texto que ele imprime: `mutants/<arquivo>.meta`, um
JSON com `exit_code_by_key` (mutante -> codigo de saida do pytest). O significado de cada
codigo vem do proprio mutmut (`mutmut.stats.status_by_exit_code`), injetado -- copiar a
tabela seria uma segunda lista que concorda por acidente (N-01).

Saida: uma linha `::notice` que a API publica le sem login, e codigo 1 quando NADA foi
testado (nenhum .meta, ou todo mutante em `not checked`/`no tests`/`skipped`/interrompido).
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter

# Estados em que o pytest NAO julgou o mutante: nao contam como teste.
NAO_TESTADO = ("not checked", "no tests", "skipped", "check was interrupted by user")


def contar(pasta, status_de):
    """Counter de status sobre todo `.meta` sob `pasta`, mais `gerados` e `testados`."""
    c = Counter()
    for raiz, _, nomes in os.walk(pasta):
        for n in nomes:
            if not n.endswith(".meta"):
                continue
            with open(os.path.join(raiz, n), encoding="utf-8") as f:
                meta = json.load(f)
            for codigo in meta.get("exit_code_by_key", {}).values():
                c[status_de(codigo)] += 1
    c["gerados"] = sum(v for k, v in c.items() if k != "gerados")
    c["testados"] = c["gerados"] - sum(c[s] for s in NAO_TESTADO)
    return c


def linha(c):
    ordem = ["gerados", "testados", "killed", "survived", "timeout", "suspicious",
             "segfault", "caught by type check"] + list(NAO_TESTADO)
    return " ".join(f"{k.replace(' ', '_')}={c[k]}" for k in ordem)


def main(argv=None, status_de=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasta", default="mutants")
    ap.add_argument("--saida-mutmut", type=int, default=None,
                    help="codigo de saida do `mutmut run`, so para constar na anotacao")
    a = ap.parse_args(argv)
    if status_de is None:
        from mutmut.stats import status_by_exit_code
        status_de = status_by_exit_code.__getitem__
    c = contar(a.pasta, status_de)
    extra = "" if a.saida_mutmut is None else f" mutmut_run_saiu={a.saida_mutmut}"
    print(f"::notice title=Mutacao::{linha(c)}{extra}")
    if c["testados"] == 0:
        print(f"::error title=Mutacao::nenhuma alteracao foi testada ({c['gerados']} "
              f"gerada(s)) -- verde aqui seria ausencia de medicao (F-02)")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

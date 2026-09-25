#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cobertura_csv.py -- cobertura de linhas por modulo, como MEDIDA, nao meta (25/09/2026).

Le o `coverage.json` do job semanal e escreve `docs/metricas/cobertura.csv`, uma linha por
modulo, ordenada por caminho. Imprime os modulos de PRODUCAO (nao `test_*`, nao `conftest`)
abaixo de 50%. Nao ha teto nem piso obrigatorio: o numero existe para ser lido, e um piso
ensinaria a escrever teste que executa linha sem afirmar nada -- a cobertura mede o que foi
EXECUTADO, nao o que foi VERIFICADO (a mutacao mede a segunda coisa).

Escreve o arquivo sempre com o mesmo conteudo para a mesma entrada: o bot so commita se o
`git diff` mostrar mudanca.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "docs", "metricas", "cobertura.csv")
LIMIAR_DE_LEITURA = 50.0      # so decide o que e LISTADO; nada reprova por ele
COLUNAS = ("modulo", "producao", "linhas", "executadas", "percentual")


def e_producao(caminho):
    nome = os.path.basename(caminho)
    return not (nome.startswith("test_") or nome == "conftest.py")


def linhas(cov):
    out = []
    for caminho, info in cov["files"].items():
        s = info["summary"]
        n, ex = s["num_statements"], s["covered_lines"]
        out.append(dict(modulo=caminho.replace("\\", "/"), producao=int(e_producao(caminho)),
                        linhas=n, executadas=ex,
                        percentual=f"{(100.0 * ex / n) if n else 100.0:.1f}"))
    return sorted(out, key=lambda r: r["modulo"])


def texto_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUNAS, delimiter=";", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def abaixo(rows, limiar=LIMIAR_DE_LEITURA):
    return [r for r in rows if r["producao"] and float(r["percentual"]) < limiar]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--saida", default=SAIDA)
    a = ap.parse_args(argv)
    with open(a.json, encoding="utf-8") as f:
        rows = linhas(json.load(f))
    os.makedirs(os.path.dirname(a.saida), exist_ok=True)
    with open(a.saida, "w", encoding="utf-8", newline="") as f:
        f.write(texto_csv(rows))
    baixos = abaixo(rows)
    print(f"{len(rows)} modulos; de producao abaixo de {LIMIAR_DE_LEITURA:.0f}%: {len(baixos)}")
    for r in baixos:
        print(f"  {r['percentual']:>5}%  {r['modulo']}  ({r['executadas']}/{r['linhas']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""expira_proxima.py -- as constantes cujo `expira` vence em ate N dias. P7 (25/09/2026).

O `motor.val()` avisa em stderr QUANDO uma constante vencida e LIDA. Isso depende de alguem
rodar o motor e ler o stderr -- e a P7 diz que rotina que depende de alguem lembrar nao e
rotina. O job semanal (`.github/workflows/testes.yml`) roda este comando e abre UMA issue
com a lista, antes do vencimento.

Le os YAML do motor pela mesma forma que o `test_P70`: no no com `valor`, o `expira` do no.
Nenhuma data esta escrita aqui. Sai 0 sempre; a lista e a saida.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVOS = [os.path.join(RAIZ, "alocacao", n) for n in ("custos.yaml", "politica.yaml")]


def vencendo(dados, hoje, dias, prefixo=""):
    """[(caminho, expira)] dos nos com `valor` e `expira` <= hoje + dias, ordenados."""
    limite = hoje + dt.timedelta(days=dias)
    out = []

    def anda(d, p):
        if isinstance(d, dict):
            if "valor" in d and isinstance(d.get("expira"), dt.date) and d["expira"] <= limite:
                out.append((p.lstrip("."), d["expira"]))
            for k, v in d.items():
                anda(v, f"{p}.{k}")
        elif isinstance(d, list):
            for i, v in enumerate(d):
                anda(v, f"{p}[{i}]")

    anda(dados, prefixo)
    return sorted(set(out), key=lambda x: (x[1], x[0]))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=7)
    ap.add_argument("--hoje", type=dt.date.fromisoformat, default=None)
    a = ap.parse_args(argv)
    hoje = a.hoje or dt.date.today()
    linhas = []
    for caminho in ARQUIVOS:
        with open(caminho, encoding="utf-8") as f:
            dados = yaml.safe_load(f)
        nome = os.path.basename(caminho)
        linhas += [f"- `{nome}` -> `{p}`: expira **{e.isoformat()}**"
                   + (" (JA VENCIDA)" if e < hoje else "")
                   for p, e in vencendo(dados, hoje, a.dias)]
    print("\n".join(linhas))
    return 0


if __name__ == "__main__":
    sys.exit(main())

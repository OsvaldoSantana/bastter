#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""metricas_processo.py -- o processo medido por semana (25/09/2026).

Duas fontes:
  docs/metricas/eventos.csv          uma linha por erro (achado, retratacao, reincidencia),
                                     versionado. Todo achado ou retratacao novo ganha a sua
                                     linha no MESMO commit que o registra.
  data/analise-sessoes/turnos.csv    tempo e tokens por pedido, de tools/analisar_sessoes.py.
                                     So existe na maquina que tem as sessoes (~/.claude); fora
                                     dela a secao sai vazia e DIZ que saiu vazia.

Por semana ISO: retratacoes por autor; reincidencias; % dos erros achados pelo Osvaldo (com o
n ao lado -- regua 5-B.14); pedidos, minutos por pedido, chamadas ao modelo e tokens de saida.

`validar()` reprova evento sem codigo, com tipo/autor/quem_achou fora das listas, ou com data
que nao e data. Valor desconhecido se escreve `desconhecido`, nunca vazio: vazio nao distingue
"nao sei" de "esqueci".
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTOS = os.path.join(RAIZ, "docs", "metricas", "eventos.csv")
TURNOS = os.path.join(RAIZ, "data", "analise-sessoes", "turnos.csv")
COLUNAS = ("data", "codigo", "tipo", "autor", "quem_achou", "regua", "commit_introduziu",
           "commit_corrigiu", "descricao")
TIPOS = ("achado", "retratacao", "reincidencia")
PESSOAS = ("claude-chat", "claude-code", "osvaldo", "outra-ia", "fonte", "desconhecido")


class EventoInvalido(ValueError):
    pass


def ler(caminho=EVENTOS):
    with open(caminho, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f, delimiter=";")
        if tuple(r.fieldnames or ()) != COLUNAS:
            raise EventoInvalido(f"colunas {r.fieldnames}, esperado {COLUNAS}")
        return list(r)


def validar(eventos):
    for i, e in enumerate(eventos, start=2):
        if not (e.get("codigo") or "").strip():
            raise EventoInvalido(f"linha {i}: evento sem codigo -- {e}")
        if e["tipo"] not in TIPOS:
            raise EventoInvalido(f"linha {i}: tipo {e['tipo']!r} fora de {TIPOS}")
        for campo in ("autor", "quem_achou"):
            if e[campo] not in PESSOAS:
                raise EventoInvalido(f"linha {i}: {campo} {e[campo]!r} fora de {PESSOAS}")
        try:
            dt.date.fromisoformat(e["data"])
        except ValueError as ex:
            raise EventoInvalido(f"linha {i}: data {e['data']!r}") from ex
        vazios = [c for c in COLUNAS if not (e.get(c) or "").strip()]
        if vazios:
            raise EventoInvalido(f"linha {i}: {vazios} vazio -- escreva 'desconhecido'")
    return eventos


def semana(data):
    a, s, _ = dt.date.fromisoformat(data[:10]).isocalendar()
    return f"{a}-S{s:02d}"


def por_semana(eventos):
    out = collections.defaultdict(lambda: dict(n=0, retratacoes=collections.Counter(),
                                               reincidencias=0, achados_osvaldo=0,
                                               quem_desconhecido=0))
    for e in eventos:
        s = out[semana(e["data"])]
        s["n"] += 1
        if e["tipo"] == "retratacao":
            s["retratacoes"][e["autor"]] += 1
        if e["tipo"] == "reincidencia":
            s["reincidencias"] += 1
        if e["quem_achou"] == "osvaldo":
            s["achados_osvaldo"] += 1
        if e["quem_achou"] == "desconhecido":
            s["quem_desconhecido"] += 1
    return dict(out)


def sessoes_por_semana(caminho=TURNOS):
    if not os.path.exists(caminho):
        return None
    out = collections.defaultdict(lambda: dict(pedidos=0, s=0.0, chamadas=0, saida_tok=0))
    with open(caminho, encoding="utf-8", newline="") as f:
        for t in csv.DictReader(f, delimiter=";"):
            s = out[semana(t["ini"])]
            s["pedidos"] += 1
            s["s"] += float(t["dur_s"])
            s["chamadas"] += int(t["chamadas"])
            s["saida_tok"] += int(t["saida_tok"])
    return dict(out)


def relatorio(eventos, sessoes):
    R = ["| semana | erros (n) | retratacoes por autor | reincidencias | achados pelo Osvaldo "
         "| quem achou: desconhecido |", "|---|---|---|---|---|---|"]
    for sem, s in sorted(por_semana(eventos).items()):
        ret = ", ".join(f"{k} {v}" for k, v in sorted(s["retratacoes"].items())) or "0"
        pct = 100.0 * s["achados_osvaldo"] / s["n"]
        R.append(f"| {sem} | {s['n']} | {ret} | {s['reincidencias']} | "
                 f"{pct:.0f}% ({s['achados_osvaldo']} de {s['n']}) | {s['quem_desconhecido']} |")
    R.append("")
    if sessoes is None:
        R.append("Sessoes: sem `data/analise-sessoes/turnos.csv` nesta maquina -- rode "
                 "`py -3.11 tools/analisar_sessoes.py`. Secao NAO medida aqui.")
    else:
        R += ["| semana | pedidos | min por pedido | chamadas ao modelo "
              "| tokens de saida por pedido |", "|---|---|---|---|---|"]
        for sem, s in sorted(sessoes.items()):
            n = max(s["pedidos"], 1)
            R.append(f"| {sem} | {s['pedidos']} | {s['s'] / 60 / n:.1f} | {s['chamadas']} | "
                     f"{s['saida_tok'] // n} |")
    return "\n".join(R) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--eventos", default=EVENTOS)
    ap.add_argument("--turnos", default=TURNOS)
    a = ap.parse_args(argv)
    ev = validar(ler(a.eventos))
    print(relatorio(ev, sessoes_por_semana(a.turnos)), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())

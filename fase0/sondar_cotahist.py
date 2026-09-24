#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sonda da P-135: a B3 responde ao runner do GitHub como responde a maquina dele?

O QUE MEDE, e so isso. Um HEAD, SEM retentativa, em `COTAHIST_A<ano>.ZIP` do ano corrente
e nos `COTAHIST_D<DDMMAAAA>.ZIP` dos dias uteis recentes. Para cada um: status,
Content-Length, Last-Modified, ETag e Server -- ou o erro, transcrito como veio.

POR QUE SEM RETENTATIVA. `requisitar` retenta 429/5xx, e uma retentativa que da certo
esconderia justamente o que se quer saber: se o primeiro contato de um IP de datacenter
e recusado. A sonda e medicao, nao captura.

POR QUE VARIOS DIAS. Um dia sem arquivo diario pode ser feriado, e a sonda nao conhece
feriado (o calendario do projeto vem do proprio COTAHIST -- `calendario.py`). Sondar os
dias uteis da ultima semana separa "o arquivo diario nao existe" de "hoje nao houve
pregao" sem escrever lista de feriado de cabeca.

A sonda NUNCA sai com erro por causa da resposta: um 403 e o dado que ela existe para
trazer. So sai 1 se ela mesma quebrar. Regua 5-B.13: "nao da" so se escreve com o erro
transcrito -- e e isso que ela imprime.

  python fase0/sondar_cotahist.py              # imprime; no Actions, tambem no resumo
"""
from __future__ import annotations

import datetime as dt
import os
import sys
import urllib.error
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import capturar_cvm  # noqa: E402

BASE = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/"
CABECALHOS = ("Content-Length", "Last-Modified", "ETag", "Server")
DIAS_PARA_TRAS = 7


def urls(hoje, dias=DIAS_PARA_TRAS):
    """O anual do ano corrente e os diarios dos dias uteis (seg-sex) anteriores a hoje."""
    out = [BASE + f"COTAHIST_A{hoje.year}.ZIP"]
    for i in range(1, dias + 1):
        d = hoje - dt.timedelta(days=i)
        if d.weekday() < 5:
            out.append(BASE + f"COTAHIST_D{d:%d%m%Y}.ZIP")
    return out


def sondar(url, abrir=urllib.request.urlopen):
    """{url, status, <cabecalhos>, erro}. O erro vai como veio: classe, codigo e razao."""
    linha = dict(url=url, status="", erro="", **{c: "" for c in CABECALHOS})
    try:
        with capturar_cvm.requisitar(url, abrir, lambda s: None, metodo="HEAD",
                                     tentativas=1, timeout=60) as r:
            linha["status"] = str(getattr(r, "status", "") or r.getcode())
            for c in CABECALHOS:
                linha[c] = r.headers.get(c) or ""
    except urllib.error.HTTPError as e:
        linha["status"] = str(e.code)
        linha["erro"] = f"HTTPError {e.code} {e.reason}"
        for c in CABECALHOS:
            linha[c] = (e.headers.get(c) if e.headers else "") or ""
    except (urllib.error.URLError, OSError) as e:
        linha["erro"] = f"{type(e).__name__}: {getattr(e, 'reason', e)}"
    return linha


def formatar(linhas):
    cols = ("url", "status") + CABECALHOS + ("erro",)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for ln in linhas:
        out.append("| " + " | ".join(str(ln[c]) for c in cols) + " |")
    return "\n".join(out)


def main(argv=None, abrir=urllib.request.urlopen, hoje=None):
    hoje = hoje or dt.datetime.now(dt.timezone.utc).date()
    linhas = [sondar(u, abrir) for u in urls(hoje)]
    tabela = f"P-135, sonda de {dt.datetime.now(dt.timezone.utc):%Y-%m-%dT%H:%M:%SZ}\n\n" \
             + formatar(linhas)
    print(tabela)
    resumo = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumo:
        with open(resumo, "a", encoding="utf-8") as f:
            f.write(tabela + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

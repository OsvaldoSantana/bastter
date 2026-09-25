#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""materializar_acervo.py -- poe em `data/bronze/` o que o armazem tem, pelo `acervo.abrir`.

POR QUE ELE EXISTE (metricas, 25/09/2026). Os testes contra o acervo real leem por caminho
(`data/bronze/b3/cotahist/...`), e o job semanal do GitHub nao tem o disco dele. Este
comando abre cada arquivo conhecido -- a versao VIGENTE, conferida pelo sha256 -- e o copia
para o caminho que os testes leem. O silver nao esta no armazem, e por isso fica fora: os
testes dele pulam no job, visivelmente (`exigir_acervo`, pasta por acervo).

O QUE ELE ACUSA, e e o motivo de existir tanto quanto a copia: arquivo que o registro ou o
inventario dizem existir e o armazem NAO entrega. A captura local sem `--armazem` produz
exatamente isso (CV-07): o registro anota a versao, o portao da rodada seguinte a da como
`inalterado`, e o byte nunca sobe. A lista vai para `--faltas`, e o job fica vermelho no fim,
depois de rodar os testes -- a falha e visivel e nao esconde o resto do resultado.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import acervo  # noqa: E402


def conhecidos(repo=None):
    """{(fonte, recurso, arquivo)} de todo inventario e registro de captura."""
    repo = repo or acervo.raiz_repo()
    out = set()
    for ln in acervo._inventarios(repo):
        out.add((ln["fonte"], ln["recurso"], ln["arquivo"]))
    for fonte, rel in acervo.REGISTROS.items():
        for ln in acervo._ler(os.path.join(repo, rel)):
            if ln.get("sha256") and ln.get("situacao") in acervo.VIGENTES:
                out.add((fonte, ln["recurso"], ln["arquivo"]))
    return out


def materializar(itens, repo, abrir=None):
    """Copia cada item para `data/bronze/<fonte>/<recurso>/<arquivo>`. Devolve (copiados,
    ja_estavam, faltas). Idempotente: o que ja esta no lugar nao e copiado de novo."""
    abrir = abrir or acervo.abrir
    copiados, ja, faltas = [], [], []
    for fonte, recurso, arquivo in sorted(itens):
        destino = os.path.join(repo, "data", "bronze", fonte, recurso, arquivo)
        try:
            origem = abrir(recurso, arquivo)
        except Exception as e:
            faltas.append(f"{fonte}/{recurso}/{arquivo}: {type(e).__name__}: {e}")
            continue
        if os.path.abspath(origem) == os.path.abspath(destino):
            ja.append(destino)
            continue
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy2(origem, destino)
        copiados.append(destino)
    return copiados, ja, faltas


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--faltas", help="grava aqui a lista do que o armazem nao entregou")
    a = ap.parse_args(argv)
    repo = acervo.raiz_repo()
    copiados, ja, faltas = materializar(conhecidos(repo), repo)
    print(f"materializados {len(copiados)}, ja no lugar {len(ja)}, FALTAS {len(faltas)}")
    for f in faltas:
        print(f"  FALTA  {f}")
    if a.faltas:
        with open(a.faltas, "w", encoding="utf-8") as fh:
            fh.write("".join(f + "\n" for f in faltas))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

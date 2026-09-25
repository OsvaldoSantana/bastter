#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""conferir_reproducao.py -- o que alguem de fora capturou bate com o que o projeto registrou?

POR QUE ELE EXISTE (25/09/2026). O armazem do projeto e privado (P-136), e quem reproduz de
fora captura na propria maquina, com `--armazem local` (docs/reproduzir.md). Este comando
compara o que ficou nessa pasta com o que o projeto declara ter visto -- os inventarios e os
registros de captura em docs/acervo/ -- pelo sha256, que esta na propria chave do armazem.

Cada (fonte, recurso, arquivo) cai em uma de quatro situacoes:
  IGUAL        o sha256 capturado e uma versao que o projeto registrou
  DIFERENTE    o arquivo existe dos dois lados, e nenhuma versao registrada tem este sha256.
               Na CVM isso e o esperado para o que a fonte reescreveu depois da nossa
               captura: ela serve so a versao corrente (limite declarado no documento).
  SO_NOSSO     o projeto registrou, a pasta nao tem (nao capturado, ou a fonte ja nao serve)
  SO_SEU       a pasta tem, o projeto nunca registrou

  python fase0/conferir_reproducao.py [--pasta data/armazem-local]
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import acervo  # noqa: E402
import armazem as armazem_mod  # noqa: E402

SITUACOES = ("IGUAL", "DIFERENTE", "SO_NOSSO", "SO_SEU")


def registrados(repo):
    """{(fonte, recurso, arquivo): {sha256}} de todo inventario e registro de captura."""
    out = defaultdict(set)
    for ln in acervo._inventarios(repo):
        if ln.get("sha256"):
            out[(ln["fonte"], ln["recurso"], ln["arquivo"])].add(ln["sha256"])
    for fonte, rel in acervo.REGISTROS.items():
        for ln in acervo._ler(os.path.join(repo, rel)):
            if ln.get("sha256"):
                out[(fonte, ln["recurso"], ln["arquivo"])].add(ln["sha256"])
    return out


def capturados(armazem):
    """{(fonte, recurso, arquivo): {sha256}} das chaves de conteudo da pasta (logs fora)."""
    out = defaultdict(set)
    for k in armazem.listar(""):
        sha = armazem_mod.sha_da_chave(k)
        if sha is None:
            continue
        fonte, recurso, arquivo, _ = k.split("/", 3)
        out[(fonte, recurso, arquivo)].add(sha)
    return out


def comparar(nossos, seus):
    """[(situacao, (fonte, recurso, arquivo))], ordenado."""
    out = []
    for item in sorted(set(nossos) | set(seus)):
        n, s = nossos.get(item, set()), seus.get(item, set())
        if not s:
            out.append(("SO_NOSSO", item))
        elif not n:
            out.append(("SO_SEU", item))
        elif s & n:
            out.append(("IGUAL", item))
        else:
            out.append(("DIFERENTE", item))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pasta", default=None, help="padrao: ARMAZEM_LOCAL ou data/armazem-local")
    a = ap.parse_args(argv)
    repo = acervo.raiz_repo()
    pasta = a.pasta or os.environ.get("ARMAZEM_LOCAL") or \
        os.path.join(repo, armazem_mod.PASTA_LOCAL_PADRAO)
    if not os.path.isdir(pasta):
        print(f"{pasta} nao existe: capture antes, com --armazem local", file=sys.stderr)
        return 2
    resultado = comparar(registrados(repo), capturados(armazem_mod.ArmazemLocal(pasta)))
    conta = {s: sum(1 for x, _ in resultado if x == s) for s in SITUACOES}
    for sit, (fonte, recurso, arquivo) in resultado:
        if sit != "IGUAL":
            print(f"{sit:10} {fonte}/{recurso}/{arquivo}")
    print("  ".join(f"{s} {conta[s]}" for s in SITUACOES) + f"  (n={len(resultado)})")
    return 0 if conta["IGUAL"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

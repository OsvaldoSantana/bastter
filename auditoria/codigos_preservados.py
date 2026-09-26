#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nenhum codigo do projeto some do repositorio -- a promessa do corte de 26/09 virada medicao.

POR QUE ELE EXISTE. Em 26/09/2026 o `CLAUDE.md` e o `PENDENCIAS.md` foram cortados para o que
muda o que uma sessao faz: a historia foi para `docs/historico/`. A regra da casa e que achado
retirado fica como retratacao e nada se apaga (secao 5-A). O `achados_ancorados.py` mede que
todo codigo CITADO tenha endereco; nao mede que um codigo que EXISTIA continue existindo --
um corte que levasse junto a citacao e a definicao passaria verde nele.

O QUE ELE MEDE (P5): o conjunto de codigos `LETRA-NUMERO` (P-57, A-06, CV-01...) e `5-B.n`
nos `.py`, `.md`, `.yaml` e `.yml` do repositorio, contra a linha de base gravada em
`auditoria/codigos_linha_de_base.txt`. Um codigo da linha de base que nao aparece em arquivo
nenhum reprova. NAO mede se o texto em volta chegou inteiro, nem quantas vezes o codigo
aparece: mover um bloco inteiro deixa o conjunto igual, e e isso que se quer provar.

A LINHA DE BASE SO CRESCE. Codigo novo entra com `--gravar`; codigo que sai da linha de base
e codigo apagado, e isso a secao 5-A nao permite.
"""
from __future__ import annotations
import argparse
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import achados_ancorados as A  # noqa: E402 -- mesma varredura, mesmas pastas ignoradas (N-01)

LINHA_DE_BASE = os.path.join(AQUI, "codigos_linha_de_base.txt")
REGUA = re.compile(r"5-B\.(\d{1,2})\b")


def codigos(raiz=RAIZ):
    """{codigo: ocorrencias} em toda a arvore, com a mesma exclusao do achados_ancorados."""
    out = {}
    for caminho in A.arquivos(raiz):
        with io.open(caminho, encoding="utf-8", errors="replace") as f:
            s = f.read()
        for m in A.REF.finditer(s):
            c = f"{m.group(1)}-{m.group(2)}"
            if c not in A.NAO_SAO_ACHADOS:
                out[c] = out.get(c, 0) + 1
        for m in REGUA.finditer(s):
            c = f"5-B.{m.group(1)}"
            out[c] = out.get(c, 0) + 1
    return out


def ler_base(caminho=LINHA_DE_BASE):
    with io.open(caminho, encoding="utf-8") as f:
        return {x.strip() for x in f if x.strip() and not x.startswith("#")}


def sumidos(base, atuais):
    return sorted(base - set(atuais))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gravar", action="store_true",
                    help="acrescenta os codigos novos a linha de base (nunca tira)")
    a = ap.parse_args(argv)
    atuais = codigos()
    base = ler_base() if os.path.exists(LINHA_DE_BASE) else set()
    falta = sumidos(base, atuais)
    print(f"{len(atuais)} codigos no repositorio, {sum(atuais.values())} ocorrencias; "
          f"linha de base {len(base)}; sumidos {len(falta)}")
    for c in falta:
        print(f"  SUMIU: {c}")
    if a.gravar:
        novo = sorted(base | set(atuais))
        with io.open(LINHA_DE_BASE, "w", encoding="utf-8", newline="\n") as f:
            f.write("# codigos do repositorio; so cresce -- ver auditoria/codigos_preservados.py\n")
            f.write("\n".join(novo) + "\n")
        print(f"linha de base gravada: {len(novo)}")
    return 1 if falta else 0


if __name__ == "__main__":
    raise SystemExit(main())

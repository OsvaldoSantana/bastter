#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Todo link relativo num `.md` rastreado aponta para um arquivo (ou pasta) que existe.

Estetica quebrada e link quebrado (25/09/2026): o repositorio passou a ser lido por quem e de
fora, e um link morto e a primeira coisa que essa pessoa encontra. O teste nasceu junto com a
mudanca dos laudos para `docs/auditoria/`, que mexeu em 46 caminhos.

ALCANCE (P5): mede links markdown inline (`[texto](alvo)`, imagem inclusive) e de referencia
(`[id]: alvo`). NAO mede: o texto entre crases (`caminho/em/crase.md`), que e mencao e nao
link; a ancora `#secao` (so o arquivo); link absoluto (`https://...`), que exigiria rede.
Bloco de codigo cercado por ``` fica de fora -- ali o colchete e codigo, nao link.
"""
from __future__ import annotations
import os
import re
import subprocess
from urllib.parse import unquote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INLINE = re.compile(r"!?\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
REFERENCIA = re.compile(r"^\s{0,3}\[[^\]]+\]:\s+<?(\S+?)>?(?:\s|$)", re.M)
CERCA = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)
EXTERNO = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", re.I)


def alvos(texto):
    """Os alvos de link do texto, na ordem, sem os de dentro de bloco de codigo."""
    texto = CERCA.sub("", texto)
    return INLINE.findall(texto) + REFERENCIA.findall(texto)


def quebrados(md, texto, existe=os.path.exists):
    """[(md, alvo)] dos links relativos de `md` cujo alvo nao existe."""
    out = []
    base = os.path.dirname(os.path.join(RAIZ, md))
    for alvo in alvos(texto):
        if EXTERNO.match(alvo):
            continue
        caminho = unquote(alvo.split("#", 1)[0].split("?", 1)[0])
        if not caminho:
            continue
        destino = os.path.normpath(os.path.join(RAIZ, caminho.lstrip("/")) if caminho.startswith("/")
                                   else os.path.join(base, caminho))
        if not existe(destino):
            out.append((md, alvo))
    return out


def _mds():
    r = subprocess.run(["git", "ls-files", "*.md"], cwd=RAIZ, capture_output=True, text=True,
                       check=True, encoding="utf-8")
    return [m for m in r.stdout.split("\n") if m and os.path.exists(os.path.join(RAIZ, m))]


def test_o_detector_pega_o_quebrado_e_ignora_o_resto():
    texto = ("[ok](README.md) [morto](nao-existe.md) [site](https://x.org) [ancora](#sec)\n"
             "![img](figs/nada.png)\n[ref]: outro-morto.md\n```\n[em codigo](ignorado.md)\n```\n")
    achados = [a for _, a in quebrados("README.md", texto)]
    assert achados == ["nao-existe.md", "figs/nada.png", "outro-morto.md"]


def test_todo_link_relativo_de_todo_md_rastreado_existe():
    mds = _mds()
    assert len(mds) > 50, "a lista de .md encolheu demais -- o git ls-files mudou?"
    ruins = []
    for md in mds:
        with open(os.path.join(RAIZ, md), encoding="utf-8") as f:
            ruins += quebrados(md, f.read())
    assert not ruins, f"{len(ruins)} link(s) quebrado(s):\n" + "\n".join(
        f"  {m}: {a}" for m, a in ruins)

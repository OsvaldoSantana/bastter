#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A regra de credencial (CLAUDE.md 5-A) como TRAVA, nao como prosa.

Reincidencia de 25/09/2026: a sessao local tentou disparar workflow pelo navegador
embutido e depois pelo Chrome dele, "que costuma ter a sessao aberta". Sessao logada e
credencial. A regra de 24/09 estava escrita e nao impediu; o que impede e a ferramenta
negada em `.claude/settings.json`, versionado. A pesquisa na web continua pelas
ferramentas de busca e leitura de pagina, que nao carregam a sessao dele.
"""
from __future__ import annotations
import json
import os
import subprocess

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS = os.path.join(RAIZ, ".claude", "settings.json")
NEGADAS = ("mcp__claude-in-chrome", "mcp__claude-in-chrome__*")


def _deny():
    with open(SETTINGS, encoding="utf-8") as f:
        return json.load(f).get("permissions", {}).get("deny", [])


def test_as_ferramentas_do_chrome_estao_negadas():
    faltam = [r for r in NEGADAS if r not in _deny()]
    assert not faltam, f"{SETTINGS}: permissions.deny perdeu {faltam} (5-A, 25/09)"


def test_nenhuma_permissao_libera_o_chrome_por_outro_lado():
    """Um `allow` do mesmo prefixo, aqui ou no settings.local.json, seria o contorno."""
    for nome in ("settings.json", "settings.local.json"):
        p = os.path.join(RAIZ, ".claude", nome)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            allow = json.load(f).get("permissions", {}).get("allow", [])
        assert not [r for r in allow if r.startswith("mcp__claude-in-chrome")], nome


def test_a_trava_esta_no_indice_do_git():
    """Mede o indice, como o P-67/P-82/P-98: a trava que so existe no disco dele nao
    viaja para o proximo clone."""
    r = subprocess.run(["git", "ls-files", "--error-unmatch", ".claude/settings.json"],
                       cwd=RAIZ, capture_output=True, text=True)
    assert r.returncode == 0, "`.claude/settings.json` nao esta versionado"

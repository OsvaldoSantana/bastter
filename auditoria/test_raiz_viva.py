# -*- coding: utf-8 -*-
"""A raiz so tem documentos vivos (24/09/2026). A lista e dado: `raiz_viva.yaml`.

Mede duas coisas, porque o defeito tem duas portas:
  - o INDICE do git (`git ls-files` na raiz) -- e onde o bilhete vira historia permanente,
    mesmo instrumento do test_p67_segredo e do test_p82_copia_do_projeto;
  - o DISCO, so para `.md` -- um bilhete novo e acusado antes do `git add`, que e quando
    ainda custa uma linha mover.
Arquivo nao rastreado que nao e `.md` (PDF, zip, HTML de trabalho) nao entra: nao e
documento do projeto, e o .gitignore decide se ele pode ser adicionado.
"""
from __future__ import annotations

import os
import subprocess

import pytest
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def _dado():
    with open(os.path.join(AQUI, "raiz_viva.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def _rastreados_na_raiz():
    r = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        pytest.skip("sem git: o indice nao pode ser medido")
    return {p for p in r.stdout.splitlines() if "/" not in p}


def fora_da_lista(rastreados, md_no_disco, vivos):
    """O que esta na raiz e nao e vivo. Funcao pura, para a mutacao nao precisar de git."""
    return sorted((set(rastreados) | set(md_no_disco)) - set(vivos))


def test_raiz_so_tem_documentos_vivos():
    vivos = _dado()["vivos"]
    md = {n for n in os.listdir(RAIZ)
          if n.endswith(".md") and os.path.isfile(os.path.join(RAIZ, n))}
    intrusos = fora_da_lista(_rastreados_na_raiz(), md, vivos)
    d = _dado()["destinos"]
    assert not intrusos, (
        "na raiz e fora de auditoria/raiz_viva.yaml: " + ", ".join(intrusos)
        + f". Bilhete de entrega vai para {d['bilhete']} (o prompt vive no chat); laudo "
        f"ou desenho, para {d['referencia']}. Se for vivo, entra na lista com o porque.")


def test_todo_vivo_existe_e_tem_porque():
    for nome, porque in _dado()["vivos"].items():
        assert os.path.isfile(os.path.join(RAIZ, nome)), f"vivo que nao existe: {nome}"
        assert isinstance(porque, str) and len(porque) > 10, nome


def test_os_destinos_existem():
    for destino in _dado()["destinos"].values():
        assert os.path.isdir(os.path.join(RAIZ, destino)), destino


def test_mutacao_md_novo_na_raiz_e_acusado():
    vivos = _dado()["vivos"]
    assert fora_da_lista(list(vivos), ["LEIA-NA-QUARTA.md"], vivos) == ["LEIA-NA-QUARTA.md"]
    assert fora_da_lista(list(vivos) + ["x.html"], [], vivos) == ["x.html"]
    assert fora_da_lista(list(vivos), [], vivos) == []            # controle

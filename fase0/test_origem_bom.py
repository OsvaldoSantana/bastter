#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-108: `origem.csv` escrito pelo Windows PowerShell 5.1 tem BOM, e isso nao pode
zerar a procedencia em silencio.

Achado em 21/09/2026 lendo o transcript dele: o roteiro
`docs/historico/entregas/SEGUNDA-21.md` mandava criar o arquivo com
`Out-File -Encoding utf8`, que no PowerShell 5.1 grava `EF BB BF` na frente.
O leitor abria com `utf-8`, a coluna virava '\\ufeffcaminho', e o filtro `r.get("caminho")`
descartava TODAS as linhas -- sem erro, sem aviso. O instrumento que conta origem ausente
teria contado 42 depois de ele declarar as 41.
"""
from __future__ import annotations
import codecs
import csv
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifesto_cvm as m  # noqa: E402

CORPO = ("caminho;origem;acesso\r\n"
         "cotahist/COTAHIST_A1986.ZIP;https://exemplo/SerHist;2026-09-18\r\n")


def _grava(pasta, bom):
    dados = CORPO.encode("utf-8")
    (pasta / m.ORIGEM).write_bytes((codecs.BOM_UTF8 if bom else b"") + dados)


@pytest.mark.parametrize("bom", [False, True], ids=["sem_bom", "com_bom_powershell51"])
def test_a_origem_e_lida_com_ou_sem_bom(tmp_path, bom):
    _grava(tmp_path, bom)
    lido = m.origem_declarada(str(tmp_path))
    assert list(lido) == ["cotahist/COTAHIST_A1986.ZIP"]
    assert lido["cotahist/COTAHIST_A1986.ZIP"]["origem"] == "https://exemplo/SerHist"


def test_prova_por_mutacao_o_leitor_antigo_perdia_tudo_em_silencio(tmp_path):
    """O defeito reproduzido com o leitor de antes: nenhuma excecao, zero linhas. Se um
    dia este teste falhar, o `csv` mudou de comportamento e o comentario em
    `origem_declarada` precisa ser reescrito -- nao apagado."""
    _grava(tmp_path, bom=True)
    with open(tmp_path / m.ORIGEM, encoding="utf-8", newline="") as f:
        antigo = {r["caminho"]: r for r in csv.DictReader(f, delimiter=";")
                  if r.get("caminho")}
    assert antigo == {}


def test_cabecalho_errado_levanta_em_vez_de_zerar(tmp_path):
    """Origem ilegivel nao e origem ausente: a primeira conta como 'sem origem' e
    esconde o problema; a segunda para e diz o nome da coluna que veio."""
    (tmp_path / m.ORIGEM).write_text("arquivo;origem;acesso\nx.zip;u;d\n", encoding="utf-8")
    with pytest.raises(ValueError, match="caminho"):
        m.origem_declarada(str(tmp_path))


def test_sem_arquivo_continua_vazio(tmp_path):
    assert m.origem_declarada(str(tmp_path)) == {}

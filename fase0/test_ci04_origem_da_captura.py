#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CI-04: o arquivo que a ROTINA captura tem a origem no registro de captura, e
`origem_declarada` so lia o `origem.csv` escrito a mao.

Achado em 25/09/2026 na execucao `Testes #9` (36164255949, 94c5348): o
`test_P97_nao_sobrou_ZIP_sem_origem_no_acervo` reprovou com os seis
`cotahist_diario/COTAHIST_D*.ZIP` que o workflow da P-135 captura desde 24/09. Na maquina
dele o teste passava porque esses arquivos nunca chegaram ao disco; so o job semanal, que
materializa o armazem, os tinha. A URL de cada um estava no `capturas.csv` desde a captura.

O conserto nao e acrescentar uma linha ao `origem.csv` por pregao: isso poe alguem no
caminho critico de uma rotina (P7), e duas listas com a mesma URL e o N-01.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifesto_cvm as m  # noqa: E402

CAB = ("dt_captura;recurso;arquivo;url;http_last_modified;etag;sha256;bytes;caminho;"
       "situacao;motivo\n")
URL = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D17092026.ZIP"


def _registro(pasta, *linhas):
    (pasta / m.REGISTRO_DE_CAPTURA).write_text(CAB + "".join(linhas), encoding="utf-8")


def _linha(arquivo="COTAHIST_D17092026.ZIP", situacao="novo", sha="c878bab7", url=URL):
    return (f"2026-09-24T19:01:22Z;cotahist_diario;{arquivo};{url};;;{sha};640513;"
            f"data/bronze/b3/cotahist_diario/{arquivo};{situacao};\n")


def test_arquivo_capturado_pela_rotina_tem_origem_declarada(tmp_path):
    """Falha na versao anterior: sem `origem.csv`, `origem_declarada` devolvia {}."""
    _registro(tmp_path, _linha())
    lido = m.origem_declarada(str(tmp_path))
    r = lido["cotahist_diario/COTAHIST_D17092026.ZIP"]
    assert URL in r["origem"]
    assert r["acesso"] == "2026-09-24"


def test_a_origem_escrita_a_mao_ganha_do_registro(tmp_path):
    (tmp_path / m.ORIGEM).write_text(
        "caminho;origem;acesso\ncotahist_diario/COTAHIST_D17092026.ZIP;a mao;2026-09-01\n",
        encoding="utf-8")
    _registro(tmp_path, _linha())
    assert m.origem_declarada(str(tmp_path))[
        "cotahist_diario/COTAHIST_D17092026.ZIP"]["origem"] == "a mao"


def test_404_erro_e_linha_sem_sha_nao_sao_origem_de_arquivo(tmp_path):
    """Um `ausente` (404 de feriado, P-137) e um `erro` nao trouxeram byte nenhum. Contar a
    URL deles como origem declararia a procedencia de um arquivo que nao existe -- e
    esconderia um ZIP de mesmo nome vindo de outro lugar."""
    _registro(tmp_path,
              _linha("COTAHIST_D19092026.ZIP", situacao="ausente", sha=""),
              _linha("COTAHIST_D20092026.ZIP", situacao="erro", sha=""),
              _linha("COTAHIST_D21092026.ZIP", situacao="novo", sha=""),
              _linha("COTAHIST_D22092026.ZIP", situacao="novo", url=""))
    assert m.origem_declarada(str(tmp_path)) == {}


def test_o_acervo_real_nao_tem_linha_vigente_sem_url():
    """As duas pastas de registro do projeto, lidas como o motor le."""
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fonte in ("b3", "cvm"):
        pasta = os.path.join(raiz, "docs", "acervo", fonte)
        for chave, r in m.origem_declarada(pasta).items():
            assert r["origem"].strip(), f"{fonte}: {chave} sem origem"


def test_as_situacoes_com_byte_sao_as_vigentes_do_acervo():
    """A lista mora em dois modulos (este nao importa o acervo); o teste as amarra (N-01)."""
    import acervo
    assert tuple(m.SITUACOES_COM_BYTE) == tuple(acervo.VIGENTES)

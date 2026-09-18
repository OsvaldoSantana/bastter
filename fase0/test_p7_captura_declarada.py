#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P7 com teste: nenhum acervo existe sem regime de captura escrito.

A P7 e de 06/09/2026 e e dele: *"rotina que depende de alguem lembrar nao e rotina"*.
Ela admite duas saidas e so duas -- rodar sem intervencao humana, ou ser declarada em
`limitacoes_declaradas` com a mesma seriedade das outras. Nao existe terceira chamada
"eu lembro".

E ate 18/09/2026 o projeto estava na terceira. Duas capturas manuais (CVM e COTAHIST)
alimentavam o acervo havia semanas e NENHUMA das duas estava declarada. A doutrina
existia, escrita em dois arquivos, e nada media. E o defeito recorrente da casa na sua
forma mais barata de cometer: *um arquivo declara um comportamento que o codigo nao
tem, e os dois concordam por acidente* -- aqui nem por acidente, por ausencia de
instrumento.

ALCANCE, declarado antes de qualquer resultado (P5 aplicada ao instrumento): este
arquivo mede que cada subpasta de `docs/acervo/` e nomeada por alguma entrada de
`limitacoes_declaradas.*.acervos`, e que nenhuma entrada nomeia pasta inexistente.
NAO mede que a captura seja manual, que alguem a tenha rodado, ou quando. Um acervo
que ganhe rotina automatica continua passando aqui ate alguem tirar o nome da lista --
e e por isso que `quando_deixa_de_importar` esta escrito em cada entrada.
"""
from __future__ import annotations
import io
import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifesto_cvm as m  # noqa: E402

RAIZ = m.raiz_do_repositorio(os.path.dirname(os.path.abspath(__file__)))


def _politica():
    with io.open(os.path.join(RAIZ, m.POLITICA), encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_o_repositorio_foi_encontrado():
    """Se a ancora falhar, todos os outros passam por vacuidade -- que e o modo de
    falha que o A-06 ensinou a temer: guarda verde porque nao mediu nada."""
    assert RAIZ and os.path.isdir(os.path.join(RAIZ, "alocacao"))


def test_existe_pelo_menos_um_acervo_para_medir():
    """Vacuidade outra vez, do outro lado: sem pasta em docs/acervo/ a diferenca de
    conjuntos e vazia e o teste principal passa sem ter visto nada."""
    base = os.path.join(RAIZ, m.ACERVO)
    assert os.path.isdir(base), f"{m.ACERVO} nao existe -- o manifesto grava ali"
    assert [n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n))]


def test_P7_todo_acervo_tem_regime_de_captura_declarado():
    sem, _ = m.acervos_sem_regime(RAIZ)
    assert not sem, (
        f"acervo(s) sem regime de captura declarado: {sorted(sem)}. "
        "P7: ou a captura roda sem humano, ou ela entra em "
        "limitacoes_declaradas com `acervos`, direcao do vies e condicao de saida."
    )


def test_P7_nenhuma_declaracao_aponta_para_acervo_que_nao_existe():
    """Declaracao apodrecida e pior que declaracao ausente: ela parece cobertura.
    Se um acervo for renomeado ou removido, o nome velho fica na politica dizendo que
    alguem pensou no regime de uma pasta que nao existe mais."""
    _, orfas = m.acervos_sem_regime(RAIZ)
    assert not orfas, f"declaracao sem acervo correspondente: {sorted(orfas)}"


def test_a_declaracao_carrega_o_que_a_P5_exige_e_nao_so_o_nome():
    """Nomear o acervo e barato. O que torna a limitacao util -- e o que
    `limitacoes_declaradas` exige das outras oito -- e a DIRECAO DO VIES e a condicao
    em que ela deixa de importar. Sem os dois, a entrada e um alibi: cumpre a letra da
    P7 e nao diz nada a quem ler o resultado."""
    faltando = {}
    for nome, lim in _politica()["limitacoes_declaradas"].items():
        if not isinstance(lim, dict) or "acervos" not in lim:
            continue
        ausentes = [c for c in ("direcao_do_vies", "quando_deixa_de_importar", "fonte")
                    if not lim.get(c)]
        if ausentes:
            faltando[nome] = ausentes
    assert not faltando, faltando


def test_o_campo_acervos_e_lista_de_texto_e_nao_um_texto_solto():
    """`acervos: cvm` em vez de `acervos: ["cvm"]` faria a uniao virar o conjunto das
    LETRAS -- e {'c','v','m'} nao casa com pasta nenhuma, entao o teste principal
    reprovaria com uma mensagem que nao explica nada. Falhar aqui explica."""
    for nome, lim in _politica()["limitacoes_declaradas"].items():
        if isinstance(lim, dict) and "acervos" in lim:
            a = lim["acervos"]
            assert isinstance(a, list) and a and all(isinstance(x, str) for x in a), \
                f"{nome}.acervos deve ser lista nao vazia de texto, veio {a!r}"


# ── prova por mutacao ─────────────────────────────────────────────────────────
# Guarda que nunca falhou e guarda que ninguem sabe se funciona (regra 4 da §5-B).

def _repo_falso(tmp_path, acervos, declarados):
    (tmp_path / "pyproject.toml").write_text("[tool.x]\n", encoding="utf-8")
    pol = tmp_path / "alocacao"
    pol.mkdir()
    corpo = {"limitacoes_declaradas": {
        f"lim_{i}": {"acervos": list(d), "direcao_do_vies": "x",
                     "quando_deixa_de_importar": "y", "fonte": "z"}
        for i, d in enumerate(declarados)}}
    (pol / "politica.yaml").write_text(yaml.safe_dump(corpo), encoding="utf-8")
    for a in acervos:
        (tmp_path / "docs" / "acervo" / a).mkdir(parents=True)
    return str(tmp_path)


def test_mutacao_acervo_novo_sem_declaracao_e_ACUSADO(tmp_path):
    raiz = _repo_falso(tmp_path, ["cvm", "b3", "anbima"], [["cvm", "b3"]])
    sem, orfas = m.acervos_sem_regime(raiz)
    assert sem == {"anbima"} and not orfas


def test_mutacao_declaracao_de_acervo_inexistente_e_ACUSADA(tmp_path):
    raiz = _repo_falso(tmp_path, ["cvm"], [["cvm", "tesouro"]])
    sem, orfas = m.acervos_sem_regime(raiz)
    assert orfas == {"tesouro"} and not sem


def test_mutacao_acervo_coberto_por_qualquer_entrada_serve(tmp_path):
    """A cobertura e por UNIAO: duas limitacoes diferentes podem cobrir um acervo cada,
    e e assim que a CVM e a B3 estao hoje -- regimes distintos, entradas distintas."""
    raiz = _repo_falso(tmp_path, ["cvm", "b3"], [["cvm"], ["b3"]])
    assert m.acervos_sem_regime(raiz) == (set(), set())


def test_mutacao_arquivo_no_lugar_de_pasta_nao_vira_acervo(tmp_path):
    """`docs/acervo/` guarda um CSV por captura DENTRO da pasta do acervo; um arquivo
    solto na raiz nao e acervo e nao deve exigir declaracao."""
    raiz = _repo_falso(tmp_path, ["cvm"], [["cvm"]])
    (tmp_path / "docs" / "acervo" / "LEIA.md").write_text("x", encoding="utf-8")
    assert m.acervos_sem_regime(raiz) == (set(), set())


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

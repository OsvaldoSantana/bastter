# -*- coding: utf-8 -*-
"""O `medir.yml` nao ganha poder: so `contents: write`, e o token de LEITURA em um passo so.

Por que (decisao dele, 26/09/2026): um script de medicao roda codigo da branch com o token
do armazem no ambiente. Se ele tivesse o token de escrita, poderia apagar uma versao da CVM
que a CVM nao guarda mais (CV-01); se tivesse mais permissao no GitHub, o disparo por push
viraria atalho para agir no repositorio. `defeitos()` e funcao pura para poder ser provada
por mutacao (regua 5-B, pergunta 4)."""
from __future__ import annotations

import copy
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_workflows import _wf  # noqa: E402

SEGREDO = re.compile(r"secrets\.([A-Za-z0-9_]+)")


def defeitos(d):
    """[o que o workflow faz alem do permitido] -- vazio e o unico resultado aceito."""
    out = []
    if d.get("permissions") != {"contents": "write"}:
        out.append(f"permissions do workflow = {d.get('permissions')!r}; so contents: write")
    if d.get("on") != {"push": {"branches": ["medir/**"]}}:
        out.append(f"gatilho = {d.get('on')!r}; so push em medir/**")
    if SEGREDO.search(str(d.get("env", ""))):
        out.append("segredo no env do workflow")
    passos_com_segredo = []
    for nome_job, job in d.get("jobs", {}).items():
        if "permissions" in job:
            out.append(f"job {nome_job} declara permissions proprias: {job['permissions']!r}")
        fora = {k: v for k, v in job.items() if k != "steps"}
        if SEGREDO.search(str(fora)):
            out.append(f"segredo no job {nome_job} fora de um passo")
        for p in job.get("steps", []):
            if SEGREDO.search(str({k: v for k, v in p.items() if k != "env"})):
                out.append(f"segredo fora do env do passo {p.get('name')!r}")
            usados = SEGREDO.findall(str(p.get("env", "")))
            if usados:
                passos_com_segredo.append(p.get("name"))
            out += [f"segredo {s} no passo {p.get('name')!r}: so R2_LEITURA_*"
                    for s in usados if not s.startswith("R2_LEITURA_")]
    if len(passos_com_segredo) > 1:
        out.append(f"segredo em mais de um passo: {passos_com_segredo}")
    return out


def test_o_medir_yml_so_tem_contents_write_e_o_token_de_leitura_num_passo():
    d = _wf("medir.yml")
    assert defeitos(d) == []
    com = [p["name"] for j in d["jobs"].values() for p in j["steps"]
           if SEGREDO.search(str(p.get("env", "")))]
    assert com == ["Medir (token de leitura)"], "vacuidade: o passo que mede tem de ter o token"


def _mutante(f):
    d = copy.deepcopy(_wf("medir.yml"))
    f(d)
    return defeitos(d)


def _passo(d, nome):
    return next(p for p in d["jobs"]["medir"]["steps"] if p.get("name") == nome)


def test_mutacao_permissao_a_mais_reprova():
    assert _mutante(lambda d: d["permissions"].update({"actions": "write"}))
    assert _mutante(lambda d: d.update(permissions="write-all"))
    assert _mutante(lambda d: d["jobs"]["medir"].update(permissions={"issues": "write"}))


def test_mutacao_token_de_escrita_reprova():
    def troca(d):
        _passo(d, "Medir (token de leitura)")["env"]["R2_ACCESS_KEY_ID"] = \
            "${{ secrets.R2_ACCESS_KEY_ID }}"
    assert any("so R2_LEITURA_" in x for x in _mutante(troca))


def test_mutacao_segredo_fora_do_passo_reprova():
    assert _mutante(lambda d: d["jobs"]["medir"].update(
        env={"R2_BUCKET": "${{ secrets.R2_LEITURA_BUCKET }}"}))
    assert _mutante(lambda d: d.update(env={"X": "${{ secrets.R2_LEITURA_BUCKET }}"}))
    assert _mutante(lambda d: _passo(d, "Conferir insumos").update(
        env={"R2_BUCKET": "${{ secrets.R2_LEITURA_BUCKET }}"}))
    assert _mutante(lambda d: _passo(d, "Resumo").update(
        run="echo ${{ secrets.R2_LEITURA_BUCKET }}"))


def test_mutacao_outro_gatilho_reprova():
    assert _mutante(lambda d: d["on"].update(workflow_dispatch=None))
    assert _mutante(lambda d: d["on"]["push"].update(branches=["**"]))

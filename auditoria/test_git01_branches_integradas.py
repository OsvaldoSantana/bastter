# -*- coding: utf-8 -*-
"""GIT-01 -- branch no origin que o HEAD nao contem.

Em 25/09/2026 uma sessao na nuvem empurrou a secao 6 da emenda 1 do pre-registro ML para
`claude/brave-gates-g4zm6k` (2f939ae, 15:11Z). Uma sessao local olhou so o `main`, achou que
nada tinha sido feito e publicou uma segunda redacao da mesma secao (53112d6, 16:54Z). Duas
versoes publicadas de um pre-registro, e ninguem viu, porque nada media branch fora do `main`.

A guarda: toda ref em `refs/remotes/origin/` tem de estar contida no HEAD. Branch nova de
outra sessao reprova aqui ate alguem integra-la ou apaga-la -- e e esse o ponto.

O QUE ELA NAO VE (P5): so enxerga as refs que este clone buscou. No CI o checkout busca so o
`main` (fetch-depth 1), entao la ela passa sem medir nada; o `git fetch` e dever de quem roda
na maquina. E nao distingue branch esquecida de branch em andamento: as duas reprovam.

GIT-02 (25/09/2026): `origin/dependabot/*` fica de fora. O `dependabot.yml` da Sessao B abriu
quatro branches na primeira rodada, e todo `git fetch` passou a reprovar esta guarda por eles.
Nao sao outra sessao fazendo a tarefa do projeto: sao propostas que so entram por PR, com o
portao do CI-05. Deixa-las reprovar seria o alarme que dispara sempre (A-08). O corte e pelo
PREFIXO que so o Dependabot usa, e `test_git02_...` prende que ele nao alarga.

`origin/medir/*` (26/09/2026, CLAUDE.md 5-A.11): a branch de medicao nunca e mesclada por
desenho -- o resultado vive nela, commitado pelo `medir.yml`. Mas ela so fica de fora ENQUANTO
o que ela tem a mais que o HEAD for so `medicoes/resultados/`: um script ou uma regra que more
so nela e trabalho de sessao, e reprova como qualquer outra branch.
"""
from __future__ import annotations

import os
import shutil
import subprocess

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORA = ("origin/dependabot/",)   # GIT-02


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True,
                          check=True).stdout


MEDIR, RESULTADOS = "origin/medir/", "medicoes/resultados/"


def so_resultado_de_medicao(arquivos: list[str]) -> bool:
    """O que a branch de medicao tem a mais e so a saida que o workflow commita."""
    return bool(arquivos) and all(a.startswith(RESULTADOS) for a in arquivos)


def nao_integradas(alvo: str = "HEAD") -> list[str]:
    """Refs de origin/ que `alvo` nao contem. `origin/HEAD` e apelido, nao branch."""
    saida = _git("branch", "-r", "--no-merged", alvo, "--format=%(refname:short)")
    out = []
    for r in saida.split():
        if not r.startswith("origin/") or r == "origin/HEAD" or r.startswith(FORA):
            continue
        if r.startswith(MEDIR) and so_resultado_de_medicao(
                _git("log", f"{alvo}..{r}", "--name-only", "--format=").split()):
            continue
        out.append(r)
    return sorted(out)


def _repositorio_git() -> bool:
    if shutil.which("git") is None:
        return False
    try:
        return _git("rev-parse", "--is-inside-work-tree").strip() == "true"
    except subprocess.CalledProcessError:
        return False


pytestmark = pytest.mark.skipif(not _repositorio_git(), reason="fora de um clone git")


def test_git01_toda_branch_do_origin_esta_no_head():
    pendentes = nao_integradas()
    assert not pendentes, (
        f"GIT-01: {pendentes} tem commits que o HEAD nao contem. Leia antes de trabalhar "
        "(`git log HEAD..<branch>`), integre ou apague -- outra sessao pode ter feito a tarefa.")


def test_git01_a_guarda_ve_um_commit_fora_do_head():
    # Controle (B-13): a guarda tem de reprovar quando ha o que reprovar. O pai do HEAD nao
    # contem o HEAD; se ha branch remota apontando para o HEAD, ela aparece como pendente.
    if _git("rev-list", "--count", "HEAD").strip() == "1":
        pytest.skip("historico de um commit so")
    no_head = [r for r in _git("branch", "-r", "--points-at", "HEAD",
                               "--format=%(refname:short)").split()
               if r.startswith("origin/") and r != "origin/HEAD"]
    if not no_head:
        pytest.skip("nenhuma branch remota aponta para o HEAD; controle sem objeto")
    assert set(no_head) <= set(nao_integradas("HEAD~1"))


def test_git02_so_o_dependabot_fica_de_fora():
    # Controle do corte: um prefixo mais largo (`origin/d`, `origin/`) calaria a GIT-01 inteira.
    assert FORA == ("origin/dependabot/",)
    assert "origin/dependabot/pip/numpy-2.4.6".startswith(FORA)
    for r in ("origin/main", "origin/claude/x", "origin/wip/sessao-b", "origin/dependabotx"):
        assert not r.startswith(FORA), r


def test_medir_so_fica_de_fora_com_resultado_e_nada_mais():
    """A branch de medicao carrega a saida, e so ela. Um script que more so na branch
    reprova: e trabalho que outra sessao nao veria."""
    assert so_resultado_de_medicao(["medicoes/resultados/p145.txt"])
    assert not so_resultado_de_medicao(["medicoes/resultados/p145.txt", "medicoes/p145.py"])
    assert not so_resultado_de_medicao(["CLAUDE.md"])
    assert not so_resultado_de_medicao([]), "sem arquivo nenhum nao e resultado"

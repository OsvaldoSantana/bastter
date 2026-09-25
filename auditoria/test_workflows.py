# -*- coding: utf-8 -*-
"""As regras dos workflows, presas: acao por SHA, imagem fixa, segredo so onde precisa (P7)."""
import os
import re

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF = os.path.join(RAIZ, ".github", "workflows")


def _wf(nome):
    with open(os.path.join(WF, nome), encoding="utf-8") as f:
        d = yaml.safe_load(f)
    d["on"] = d.pop(True, d.get("on"))      # PyYAML le a chave `on` como booleano
    return d


def _passos(d):
    return [p for j in d["jobs"].values() for p in j["steps"]]


def test_toda_acao_de_todo_workflow_e_fixada_por_SHA():
    for nome in sorted(os.listdir(WF)):
        for p in _passos(_wf(nome)):
            if "uses" in p:
                assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", p["uses"]), (nome, p["uses"])


def test_toda_maquina_e_ubuntu_24_04():
    for nome in sorted(os.listdir(WF)):
        for j in _wf(nome)["jobs"].values():
            assert j["runs-on"] == "ubuntu-24.04", nome


def test_segredo_do_R2_so_no_passo_que_materializa_o_acervo():
    d = _wf("testes.yml")
    com = [p["name"] for p in _passos(d) if "secrets." in str(p.get("env", ""))]
    assert com == ["Materializar o acervo do armazem"], com
    assert "secrets." not in str(d["jobs"]["rapido"])


def test_push_roda_sem_slow_e_o_semanal_roda_tudo():
    d = _wf("testes.yml")
    assert d["on"]["push"]["branches"] == ["main"] and d["on"]["schedule"]
    rapido = " ".join(p.get("run", "") for p in d["jobs"]["rapido"]["steps"])
    completo = " ".join(p.get("run", "") for p in d["jobs"]["completo"]["steps"])
    assert '-m "not slow and not privado and not acervo"' in rapido and "-n auto" in rapido
    assert "ruff" in rapido
    assert "not slow" not in completo and "--cov" in completo and "expira_proxima" in completo
    assert '-m "not privado"' in completo, "o estado.yaml nao esta no runner (secao 11.6)"


def test_mutacao_e_so_manual():
    assert list(_wf("mutacao.yml")["on"]) == ["workflow_dispatch"]


def test_testes_clona_com_historico_e_tags():
    """As tags de marco (prereg-*) so chegam ao runner com fetch-depth: 0."""
    for job in ("rapido", "completo"):
        co = [p for p in _wf("testes.yml")["jobs"][job]["steps"]
              if str(p.get("uses", "")).startswith("actions/checkout@")]
        assert co and co[0].get("with", {}).get("fetch-depth") == 0, job


def test_pr_roda_o_rapido_e_nunca_o_completo():
    """PR (contribuidor, Dependabot) ganha portao, mas nao segredo: so o rapido."""
    d = _wf("testes.yml")
    assert d["on"]["pull_request"]["branches"] == ["main"]
    assert "pull_request" in d["jobs"]["rapido"]["if"]
    assert "pull_request" not in d["jobs"]["completo"]["if"]
    assert "push" not in d["jobs"]["completo"]["if"]


def test_P148_dependabot_ignora_exatamente_as_dependencias_numericas():
    """P-148: o Dependabot nao propoe o que muda numero pre-registrado (P-15), e so isso.

    Derivado de pyproject -> tool.meol.dependencias.numericas, a mesma lista que o
    `ambiente.py` usa para dizer MUDA NUMERO: uma lista so (N-01). Numerica nova sem ignore
    volta o PR vermelho semanal; ignore numa ferramenta (ruff, mypy) cala atualizacao que
    nao muda numero nenhum."""
    import tomllib
    with open(os.path.join(RAIZ, "pyproject.toml"), "rb") as f:
        numericas = set(tomllib.load(f)["tool"]["meol"]["dependencias"]["numericas"])
    with open(os.path.join(RAIZ, ".github", "dependabot.yml"), encoding="utf-8") as f:
        d = yaml.safe_load(f)
    pip = [u for u in d["updates"] if u["package-ecosystem"] == "pip"]
    assert len(pip) == 1
    ignorados = {i["dependency-name"] for i in pip[0].get("ignore", [])}
    assert numericas, "a lista de numericas sumiu do pyproject"
    assert ignorados == numericas, (sorted(ignorados), sorted(numericas))
    acoes = [u for u in d["updates"] if u["package-ecosystem"] == "github-actions"]
    assert acoes and not acoes[0].get("ignore"), "as acoes nao mudam numero: nada a ignorar"

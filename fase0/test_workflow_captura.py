# -*- coding: utf-8 -*-
"""O workflow da captura (P-57) diz o que a decisao promete?

O workflow nao roda na suite -- roda no GitHub. O que se mede aqui e a DECLARACAO: um
arquivo de workflow que perdesse o `concurrency`, o `if: always()` do commit ou o
`--armazem s3` continuaria verde no GitHub, e o defeito so apareceria como um registro que
nunca muda ou duas capturas brigando. Mesmo desenho do teste do `pyproject`: o arquivo e
dado, e dado se confere.
"""
from __future__ import annotations

import os
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import manifesto_cvm  # noqa: E402

REPO = manifesto_cvm.raiz_do_repositorio(AQUI)
WF = os.path.join(REPO, ".github", "workflows", "captura_cvm.yml")


def _wf():
    with open(WF, encoding="utf-8") as f:
        d = yaml.safe_load(f)
    # YAML 1.1: a chave `on` carrega como o booleano True
    d["on"] = d.pop(True, d.get("on"))
    return d


def _passos():
    return _wf()["jobs"]["captura"]["steps"]


def _passo(nome):
    return next(p for p in _passos() if p.get("name") == nome or p.get("id") == nome)


def test_gatilho_diario_e_manual():
    on = _wf()["on"]
    assert on["schedule"] == [{"cron": "15 9 * * *"}]
    assert "workflow_dispatch" in on


def test_sem_sobreposicao_e_com_permissao_de_escrever_o_registro():
    d = _wf()
    assert d["concurrency"]["cancel-in-progress"] is False
    assert d["concurrency"]["group"]
    assert d["permissions"] == {"contents": "write", "issues": "write"}


def test_python_do_projeto_e_instalacao_pelo_extra_captura():
    passos = _passos()
    py = next(p for p in passos if "setup-python" in p.get("uses", ""))
    assert str(py["with"]["python-version"]) == "3.11"
    assert any('pip install ".[captura]"' in p.get("run", "") for p in passos)


def test_captura_vai_para_o_armazem_e_credencial_so_por_segredo():
    p = _passo("captura")
    assert "fase0/capturar_cvm.py --armazem s3" in p["run"]
    for v in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET"):
        assert p["env"][v] == "${{ secrets.%s }}" % v
    texto = open(WF, encoding="utf-8").read()
    assert "echo $R2" not in texto and "echo \"$R2" not in texto


def test_registro_commitado_mesmo_com_falha_e_so_se_mudou():
    p = _passo("Commitar o registro, se mudou")
    assert p["if"] == "always()"
    assert "git status --porcelain" in p["run"] and "github-actions[bot]" in p["run"]
    assert "docs/acervo/cvm/capturas.csv" in p["run"]
    # o registro da B3 nasce na rotina: `git diff` nao ve arquivo novo, e ele nunca subiria
    assert "docs/acervo/b3/capturas.csv" in p["run"] and "git diff --quiet" not in p["run"]


def test_falha_da_captura_deixa_o_job_vermelho_depois_do_commit():
    passos = _passos()
    nomes = [p.get("name") for p in passos]
    falha = passos[nomes.index("Falhar se a captura falhou")]
    assert nomes.index("Falhar se a captura falhou") > nomes.index("Commitar o registro, se mudou")
    assert "steps.captura.outputs.codigo != '0'" in falha["if"] and "exit 1" in falha["run"]
    assert "set +e" in _passo("captura")["run"], \
        "sem set +e o passo morre antes de gravar o codigo, e o commit perde a linha"


def test_o_extra_captura_existe_e_o_projeto_constroi():
    """`pip install .[captura]` exige as duas coisas: o extra declarado com pino, e o
    build nao morrer no flat-layout (B-04). Medido em 24/09: sem `packages = []`, o
    setuptools recusa ('Multiple top-level packages discovered')."""
    import tomllib
    with open(os.path.join(REPO, "pyproject.toml"), "rb") as f:
        pp = tomllib.load(f)
    captura = pp["project"]["optional-dependencies"]["captura"]
    assert any(d.startswith("boto3==") for d in captura)
    assert pp["tool"]["setuptools"]["packages"] == []


def test_cotahist_no_mesmo_workflow_pelo_mesmo_armazem_e_com_vermelho_proprio():
    """P-135: a B3 respondeu 200 ao runner, e o COTAHIST entrou. Uma falha dele deixa o
    job vermelho igual a da CVM -- e a CVM ter falhado nao impede o COTAHIST de rodar
    (`set +e`: o passo grava o codigo em vez de morrer)."""
    nomes = [p.get("name") for p in _passos()]
    b3 = _passo("captura_b3")
    assert "fase0/capturar_cotahist.py --armazem s3" in b3["run"] and "set +e" in b3["run"]
    for v in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET"):
        assert b3["env"][v] == "${{ secrets.%s }}" % v
    assert nomes.index("Capturar COTAHIST") < nomes.index("Commitar o registro, se mudou")
    falha = _passo("Falhar se a captura falhou")["if"]
    assert "steps.captura_b3.outputs.codigo != '0'" in falha


def test_aviso_do_armazem_abre_uma_issue_so_e_antes_do_vermelho():
    """Acima do aviso: uma issue, a mesma atualizada (edit), nunca uma por rodada. E o
    passo vem antes do `Falhar`, senao o teto -- que deixa a captura vermelha -- nunca
    chegaria a avisar."""
    nomes = [p.get("name") for p in _passos()]
    av = _passo("Avisar se o armazem passou do aviso")
    assert "always()" in av["if"] and "== 'aviso'" in av["if"] and "== 'teto'" in av["if"]
    # vale a medida da B3, que roda depois da CVM e ja ve o que ela enviou
    assert av["env"]["NIVEL"].startswith("${{ steps.captura_b3.outputs.armazem_nivel ||")
    assert "gh issue list" in av["run"] and "gh issue edit" in av["run"]
    assert 'titulo="Armazem em ${GB} GB"' in av["run"]
    assert av["env"]["GH_TOKEN"] == "${{ github.token }}"
    assert nomes.index("Avisar se o armazem passou do aviso") < \
        nomes.index("Falhar se a captura falhou")


def test_imagem_do_runner_e_fixa():
    """`ubuntu-latest` troca de imagem sem commit nenhum (19/10/2026): o ambiente do
    job mudaria sem que o repositorio registrasse -- a P-15 do lado do executor."""
    assert _wf()["jobs"]["captura"]["runs-on"] == "ubuntu-24.04"

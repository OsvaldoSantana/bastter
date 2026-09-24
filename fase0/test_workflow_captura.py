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
    assert d["permissions"] == {"contents": "write"}


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
    assert "git diff --quiet" in p["run"] and "github-actions[bot]" in p["run"]
    assert "docs/acervo/cvm/capturas.csv" in p["run"]


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


def test_sonda_da_p135_roda_e_nao_derruba_a_captura():
    """A sonda mede a resposta da B3 ao runner. Se ela deixasse o job vermelho, uma recusa
    da B3 -- que e dado, nao defeito -- impediria a captura da CVM de rodar."""
    nomes = [p.get("name") for p in _passos()]
    sonda = _passo("Sondar o COTAHIST (P-135)")
    assert sonda["continue-on-error"] is True
    assert "fase0/sondar_cotahist.py" in sonda["run"]
    assert nomes.index("Sondar o COTAHIST (P-135)") < nomes.index("Capturar")

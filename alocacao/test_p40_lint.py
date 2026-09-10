# -*- coding: utf-8 -*-
"""
Lint e tipos como GUARDA, nao como decoracao. Pendencia P-40.

Lint que ninguem roda e um arquivo de configuracao com opiniao. O valor de uma
barreira dessas e ela estar em ZERO: com uma baseline de 33 violacoes conhecidas, a
34a se esconde no ruido e ninguem percebe. Por isso a P-40 zerou antes de ligar a
barreira — as 33 linhas longas foram medidas, e seis delas eram assinatura que
cresceu demais na P-37, nao estilo.

POR QUE ESTES TESTES PULAM EM VEZ DE FALHAR quando a ferramenta falta:
  `ruff` e `mypy` estao no grupo `lint` do pyproject, FORA da impressao do ambiente
  (ver P-15). Exigi-las instaladas deixaria a suite vermelha na maquina de quem so
  quer rodar o motor — e vermelho que nao e sobre o codigo ensina a ignorar vermelho.
  O pulo diz, em voz alta, o comando que liga a barreira.
"""
import os
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def _rodar(ferramenta, *args):
    try:
        return subprocess.run([sys.executable, "-m", ferramenta, *args],
                              capture_output=True, text=True, cwd=AQUI, timeout=180)
    except FileNotFoundError:
        return None


def _precisa(ferramenta):
    r = _rodar(ferramenta, "--version")
    if r is None or r.returncode != 0:
        pytest.skip(f"{ferramenta} nao instalado. Para ligar esta guarda: "
                    f"pip install {ferramenta}  (grupo `lint` do pyproject.toml)")


def test_P40_ruff_esta_em_zero():
    """Zero, e nao "poucos". Uma barreira com baseline conhecida nao e barreira.

    As dispensas estao no pyproject com o MOTIVO ESCRITO ao lado de cada uma — E701 e
    E702 sao convencao da casa (228 ocorrencias, nenhuma descuido: este codigo tem
    docstrings longas de proposito e espalhar o corpo afastaria o codigo da explicacao
    que o justifica); E402 e `sys.path.insert` antes dos imports, que e necessidade e
    nao estilo. E501 ficou LIGADO, ao contrario, porque linha longa aqui costumava ser
    sintoma de assinatura que cresceu."""
    _precisa("ruff")
    r = _rodar("ruff", "check", ".")
    assert r.returncode == 0, f"ruff encontrou violacoes:\n{r.stdout[-3000:]}"


def test_P40_mypy_nao_encontra_erro_real():
    """Nao e `strict`, e isso esta declarado no pyproject: tipagem completa custaria um
    diff enorme para um ganho que este projeto ja tem de outra forma (dataclasses
    tipadas, 265 testes, guardas de contrato). O nivel escolhido pega o que importa —
    variavel sem tipo que vira `Any` e se espalha, e operacao impossivel entre tipos.

    Foi ele que achou o `None * float` em `pontuar()`. Nao era bug em execucao: era um
    tipo que nao dava para provar, e o codigo ficou melhor ao ser reescrito."""
    _precisa("mypy")
    r = _rodar("mypy", "--ignore-missing-imports", ".")
    reais = [l for l in r.stdout.splitlines()
             if ": error:" in l and "Library stubs not installed" not in l]
    assert not reais, "mypy encontrou erro real:\n" + "\n".join(reais[:20])


def test_P40_toda_dispensa_de_regra_tem_motivo_escrito():
    """A regra da casa aplicada ao proprio lint: exclusao sem justificativa e uma
    decisao que ninguem consegue revisar depois. Vale para o .gitignore e vale aqui.

    O teste conta LINHAS DE COMENTARIO no bloco `ignore` — nao adivinha qualidade, mas
    torna impossivel acrescentar um codigo de regra em silencio."""
    import tomllib
    bruto = open(os.path.join(RAIZ, "pyproject.toml"), encoding="utf-8").read()
    d = tomllib.loads(bruto)
    dispensadas = d["tool"]["ruff"]["lint"]["ignore"]
    assert dispensadas, "se nao ha dispensa, este teste perdeu o proposito"

    # o fecho e o `]` NO INICIO DE LINHA: um `]` qualquer aparece dentro dos proprios
    # comentarios (`return []`), e cortar nele daria um bloco truncado — o teste
    # passaria a medir a primeira frase em vez do bloco inteiro.
    bloco = bruto.split("ignore = [")[1].split("\n]")[0]
    comentarios = [l for l in bloco.splitlines() if l.strip().startswith("#")]
    assert len(comentarios) >= 2 * len(dispensadas), (
        f"{len(dispensadas)} regras dispensadas e so {len(comentarios)} linhas de "
        f"motivo. Cada dispensa precisa dizer POR QUE, nao so QUAL.")
    for regra in dispensadas:
        assert regra in bloco, f"{regra} dispensada fora do bloco justificado"


def test_P40_as_ferramentas_de_lint_estao_fora_da_impressao_do_ambiente():
    """Elas nao mudam numero nenhum, entao nao pertencem a impressao que serve a
    reproducao de um resultado pre-registrado (P-15). E, na pratica: inclui-las faria
    a suite ficar vermelha em qualquer maquina que nao as tenha."""
    import ambiente
    declarado = ambiente.declarado()
    for ferramenta in ("ruff", "mypy", "types-PyYAML"):
        assert ferramenta not in declarado["versoes"], (
            f"{ferramenta} entrou na impressao do ambiente. Ferramenta de lint nao "
            f"muda numero: o lugar dela e o grupo `lint`, nao `dependencies`/`dev`.")

    import tomllib
    d = tomllib.load(open(os.path.join(RAIZ, "pyproject.toml"), "rb"))
    grupo = d["project"]["optional-dependencies"]["lint"]
    assert any("ruff" in x for x in grupo) and any("mypy" in x for x in grupo)

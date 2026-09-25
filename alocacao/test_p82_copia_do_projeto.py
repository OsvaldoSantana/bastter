# -*- coding: utf-8 -*-
"""
test_p82_copia_do_projeto.py -- ACHADO P-82, 16/09/2026.

O QUE ACONTECEU, e ele durou seis minutos entre a correcao e a recaida.

As seis falhas herdadas foram fechadas apagando, entre outros, os cinco `*-patch.py`
e a guarda duplicada. O `git rm` fez o certo. Mas a raiz do projeto tinha uma pasta
`pacote_segunda/pacote_segunda/` -- o zip de 14/09 descompactado ali por engano -- e o
`git add -A` a levou junto. O git entao viu os arquivos apagados de um lado e os
mesmos bytes do outro, e registrou **RENAME**: eles nao foram removidos, foram
MUDADOS DE LUGAR para dentro da copia.

Resultado: o repositorio passou a conter uma COPIA CONGELADA do projeto de 14/09 --
um segundo `CLAUDE.md`, um segundo `chaves_orfas.py`, um segundo `refinar.py`, um
segundo `test_chaves_orfas.py`. E a suite continuou VERDE, porque nenhum portao olha
para la: `testpaths = ["alocacao"]`, o `campos_mortos.py` varre `alocacao/`, e o
`ruff` do P-40 roda com `cwd=alocacao/`. **A P-80 cobrou a primeira conta em menos de
uma hora.**

E o mais caro: a regra ja estava escrita. O `.gitignore` ignora `Claude outputs/` com
o motivo por extenso -- *"ela contem uma COPIA INTEIRA do projeto... e a armadilha do
`docs/historico/pesquisa-custos-2026-08/calc/` outra vez"*. A armadilha tinha nome, e o remedio era
uma LISTA DE PASTAS que alguem precisa lembrar de estender. `pacote_segunda/` nao
estava na lista. **Isso e a P7: rotina que depende de lembrar nao e rotina.**

O QUE ESTE TESTE MEDE, e por que mede o INDICE e nao o disco: descompactar um zip na
pasta do projeto e inofensivo ate ser COMMITADO. O defeito nasce no `git add`. Mesmo
instrumento do `test_p67_segredo.py`, que mede o indice para o `estado.yaml`.

O QUE ELE NAO ENXERGA, declarado:
  - prosa duplicada. `escopo-campos-de-analise.md` existiu na raiz e em `auditoria/`,
    byte a byte igual, ate 24/09/2026 (a da raiz saiu na limpeza da raiz), e nao entrava
    aqui: dois textos iguais confundem, dois MODULOS iguais fazem o motor responder duas
    coisas. O risco nao e o mesmo e o remedio tambem nao;
  - copia com os arquivos RENOMEADOS. Se alguem copiar `motor.py` como `motor2.py`,
    a regra do nome nao pega -- pega a regra da pasta, se a pasta se chamar como um
    pacote; fora disso, passa;
  - copia FORA do indice. De proposito.
"""

import os
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

PACOTES = ("alocacao", "auditoria", "fase0")
REGISTROS = ("CLAUDE.md", "PENDENCIAS.md")
EXTENSOES = (".py", ".yaml")

# ── LINHA DE BASE. Copia que existe de PROPOSITO, com o porque escrito ao lado.
COPIAS_DECLARADAS = {
    # Congelado de 28/08/2026: e o ANCESTRAL do motor atual, guardado como registro da
    # pesquisa de custos, nao como codigo vivo. O proprio `.gitignore` o chama de
    # "armadilha" -- quem abrir `calc/motor.py` esta lendo uma versao de tres semanas
    # atras e nada no arquivo avisa. Fica, mas VISIVEL: tirar daqui exige mover a pasta
    # para `docs/historico/` ou renomear os arquivos, e isso e decisao do Osvaldo.
    "docs/historico/pesquisa-custos-2026-08/calc/motor.py",
    "docs/historico/pesquisa-custos-2026-08/calc/test_motor.py",
    "docs/historico/pesquisa-custos-2026-08/calc/custos.yaml",
}


def copias(rastreados):
    """Caminhos rastreados que duplicam o projeto. `rastreados` como `git ls-files`.

    Duas regras, e a segunda existe porque a primeira nao basta: um `E02-patch.py`
    dentro da copia nao colide com nome nenhum do projeto vivo, mas a PASTA que o
    contem se chama `alocacao/`, e e isso que denuncia a arvore inteira."""
    donos = {p.split("/")[1] for p in rastreados
             if len(p.split("/")) == 2 and p.split("/")[0] in PACOTES
             and p.endswith(EXTENSOES)}
    achados = set()
    for p in rastreados:
        partes = p.split("/")
        if len(partes) == 2 and partes[0] in PACOTES:
            continue                                   # o proprio projeto
        if any(x in PACOTES for x in partes[1:-1]) and p.endswith(EXTENSOES):
            # regra 2: pasta de pacote ANINHADA -- com CODIGO. 25/09/2026: os laudos foram
            # para `docs/auditoria/`, e prosa numa pasta de mesmo nome nao responde pergunta
            # nenhuma com outro numero. Copia de verdade leva .py e .yaml, e continua pega.
            achados.add(p)
            # `partes[1:-1]` e nao `partes[:-1]`: `alocacao/dados/nefin_factors.csv` tem
            # `alocacao` na posicao 0 e e o projeto vivo; copia e quando o nome do pacote
            # aparece DEPOIS de outra pasta.
        elif partes[-1] in donos and p.endswith(EXTENSOES):
            achados.add(p)                             # regra 1: modulo com o mesmo nome
        elif len(partes) > 1 and partes[-1] in REGISTROS:
            achados.add(p)                             # um registro so, e ele mora na raiz
    return sorted(achados - COPIAS_DECLARADAS)


def _rastreados():
    r = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        pytest.skip("nao e um repositorio git -- ESTE TESTE NAO RODOU")
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def test_P82_o_repositorio_nao_guarda_copia_de_si_mesmo():
    """O portao. Falha contra o commit bebea75, que trouxe 37 arquivos de
    `pacote_segunda/pacote_segunda/` -- inclusive um segundo `CLAUDE.md`."""
    achados = copias(_rastreados())
    assert not achados, (
        "o repositorio rastreia uma COPIA de si mesmo:\n  - " + "\n  - ".join(achados)
        + "\n\nUma copia congelada responde a mesma pergunta com outro numero, e nenhum "
          "portao olha para dentro dela. Apague, ou declare em COPIAS_DECLARADAS com o "
          "motivo escrito ao lado.")


def test_P82_a_guarda_PEGA_a_copia_que_de_fato_aconteceu():
    """Guarda que nunca falhou e guarda que ninguem sabe se funciona. Estes sao os
    caminhos REAIS do commit bebea75, e cada um cai por uma regra diferente."""
    real = [
        "alocacao/motor.py", "auditoria/chaves_orfas.py", "fase0/refinar.py",
        "CLAUDE.md", "PENDENCIAS.md",
        "pacote_segunda/pacote_segunda/CLAUDE.md",                     # registro fora da raiz
        "pacote_segunda/pacote_segunda/auditoria/chaves_orfas.py",     # pasta de pacote aninhada
        "pacote_segunda/pacote_segunda/alocacao/E02-patch.py",         # idem, e o nome NAO colide
        "pacote_segunda/pacote_segunda/B04-patch.py",                  # nao cai: nome nem pasta
    ]
    achados = copias(real)
    assert "pacote_segunda/pacote_segunda/CLAUDE.md" in achados
    assert "pacote_segunda/pacote_segunda/auditoria/chaves_orfas.py" in achados
    assert "pacote_segunda/pacote_segunda/alocacao/E02-patch.py" in achados, \
        "a regra da PASTA e o que pega o arquivo cujo nome nao colide com nada"
    assert "alocacao/motor.py" not in achados and "CLAUDE.md" not in achados


def test_P82_o_projeto_vivo_NAO_e_acusado_de_ser_copia_de_si_mesmo():
    """O espelho. Sem ele a guarda passaria igual se `copias()` devolvesse tudo."""
    vivos = ["alocacao/motor.py", "alocacao/custos.yaml", "auditoria/chaves_orfas.py",
             "fase0/coletar_b3.py", "alocacao/dados/nefin_factors.csv",
             "docs/fontes/nefin.md", "CLAUDE.md", "PENDENCIAS.md", "pyproject.toml"]
    assert copias(vivos) == []


def test_P82_a_linha_de_base_nao_guarda_copia_que_ja_saiu():
    """O inverso, no desenho do `test_chaves_orfas.py`: declaracao que nao encolhe vira
    deposito, e a proxima pessoa acredita que ainda ha copia onde nao ha."""
    rastreados = set(_rastreados())
    fantasmas = sorted(c for c in COPIAS_DECLARADAS if c not in rastreados)
    assert not fantasmas, (
        "declarada em COPIAS_DECLARADAS e ja nao existe no indice -- apague a linha:\n  - "
        + "\n  - ".join(fantasmas))


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))


def test_P82_laudo_em_docs_auditoria_nao_e_copia_e_codigo_la_dentro_e():
    """25/09/2026: `docs/auditoria/` recebeu os laudos. Os dois lados da regra 2."""
    assert copias(["auditoria/chaves_orfas.py", "docs/auditoria/C01-FATOR.md"]) == []
    assert copias(["auditoria/chaves_orfas.py", "docs/auditoria/chaves_orfas.py"]) ==         ["docs/auditoria/chaves_orfas.py"]
    assert copias(["alocacao/motor.py", "pacote/alocacao/E02-patch.py"]) ==         ["pacote/alocacao/E02-patch.py"]

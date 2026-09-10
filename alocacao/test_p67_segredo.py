# -*- coding: utf-8 -*-
"""
test_p67_segredo.py -- P-67. O teste que faltava, escrito depois do erro que ele
teria pego.

O QUE ACONTECEU.

Em 06/09/2026 o Osvaldo decidiu que o repositorio pode ser publico, e eu registrei
o pre-requisito: `alocacao/estado.yaml` nao entra. Abri a P-67 dizendo, com todas
as letras, que a decisao dependia de UMA LINHA de `.gitignore` e que uma linha de
`.gitignore` e exatamente o tipo de coisa que se perde sem ninguem notar.

Em 08/09 o repositorio foi criado e empurrado **com o estado.yaml dentro**.

Nao foi descuido de ninguem: a P-67 foi ABERTA e o teste nao foi ESCRITO, e entre
uma coisa e outra houve um `git add -A`. Isso e a tese do projeto inteiro aplicada
contra ele mesmo -- um arquivo declarava um comportamento e nada media se ele
acontecia (F-05, N-01, R-01, S-02). A pendencia era a documentacao do risco; o
teste e a unica coisa que o impede.

O QUE ESTE TESTE MEDE, e por que ele mede o INDICE e nao o disco.

Nao adianta conferir se o arquivo existe na pasta -- ele DEVE existir, e o motor
o le. O que nao pode e ele estar **rastreado pelo git**. Por isso o teste pergunta
ao proprio git (`git ls-files`), que e a fonte da verdade sobre o que vai junto no
proximo push.

Ele PULA quando nao ha git (container de CI sem historico, copia solta da pasta),
e diz isso em voz alta -- pular em silencio seria repetir o defeito que ele existe
para pegar.
"""

import os, subprocess, sys
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Nomes que NUNCA podem estar no indice. Nao e lista de arquivos do usuario: e a
# lista dos que carregam estado financeiro real.
PROIBIDOS = ("estado.yaml",)

# Excecoes explicitas. `estado.exemplo.yaml` e o cadastro minimo do achado U-01 --
# tudo nulo, `meta.status: MODELO` -- e ele PRECISA ser versionado: e o que prova
# que o sistema funciona sem dado de usuario.
PERMITIDOS = ("estado.exemplo.yaml",)

# Pastas que nao podem ser versionadas por carregarem copia congelada do projeto.
# `Claude outputs/` guarda o que o Cowork entrega -- projeto inteiro mais o zip.
# E a armadilha do `pesquisa-custos-2026-08/calc/` outra vez, e pior: la a copia
# velha ao menos tem nome diferente.
PASTAS_PROIBIDAS = ("claude outputs/", "dot-claude/")


def _git(*args):
    try:
        r = subprocess.run(("git",) + args, cwd=RAIZ, capture_output=True,
                           text=True, timeout=30)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        pytest.skip("git indisponivel (%s) -- ESTE TESTE NAO RODOU, e ele e o "
                    "unico que protege o estado financeiro real." % type(e).__name__)
    if r.returncode != 0:
        pytest.skip("nao e um repositorio git -- ESTE TESTE NAO RODOU. Se voce "
                    "esta prestes a rodar `git init`, rode a suite DEPOIS.")
    return r.stdout


@pytest.fixture(scope="module")
def indice():
    """Tudo que o git rastreia hoje. E o que vai no proximo push."""
    return [l.strip() for l in _git("ls-files").splitlines() if l.strip()]


def test_P67_estado_financeiro_real_nao_esta_rastreado(indice):
    achados = []
    for caminho in indice:
        base = os.path.basename(caminho)
        if base in PERMITIDOS: continue
        if base in PROIBIDOS: achados.append(caminho)

    assert not achados, (
        "ESTADO FINANCEIRO REAL RASTREADO PELO GIT:\n  " + "\n  ".join(achados) +
        "\n\nIsto NAO se corrige apagando o arquivo num commit novo: se ja houve "
        "push, o conteudo continua no historico.\n"
        "Passos, nesta ordem:\n"
        "  1. git rm --cached " + " ".join('"%s"' % c for c in achados) + "\n"
        "  2. confirmar que o .gitignore cobre o caminho\n"
        "  3. se ja foi empurrado: reescrever o historico ANTES de tornar o "
        "repositorio publico\n"
        "Ver o bloco SEGREDO do .gitignore e a P-67 do PENDENCIAS.md."
    )


def test_P67_copia_congelada_do_projeto_nao_esta_rastreada(indice):
    achados = [c for c in indice
               if any(c.lower().startswith(p) or ("/" + p) in c.lower()
                      for p in PASTAS_PROIBIDAS)]
    assert not achados, (
        "COPIA CONGELADA DO PROJETO RASTREADA (%d arquivos). Primeiros:\n  " % len(achados)
        + "\n  ".join(achados[:12]) +
        "\n\nUma sessao futura que abrir um destes le uma versao antiga sem nenhum "
        "aviso no arquivo. E a armadilha do `pesquisa-custos-2026-08/calc/`, e ali "
        "ao menos o nome era diferente.\n"
        "Corrija com: git rm -r --cached \"Claude outputs\" dot-claude"
    )


def test_P67_o_gitignore_cobre_o_estado_antes_de_alguem_esquecer():
    """Guarda do guarda. Os dois testes acima medem o INDICE; este mede a REGRA.

    Sem ele, `git rm --cached` faria a suite passar de novo e o proximo
    `git add -A` recolocaria tudo -- verde, e errado.
    """
    caminho = os.path.join(RAIZ, ".gitignore")
    assert os.path.exists(caminho), ".gitignore nao existe na raiz do projeto"
    with open(caminho, encoding="utf-8") as f:
        linhas = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

    def cobre(*padroes):
        return any(l in padroes for l in linhas)

    assert cobre("alocacao/estado.yaml", "**/estado.yaml", "estado.yaml"), (
        "o .gitignore NAO ignora estado.yaml. Os outros testes desta suite "
        "passariam mesmo assim, ate o proximo `git add -A`.")
    assert cobre("Claude outputs/", "Claude Outputs/"), (
        "o .gitignore NAO ignora a pasta de entrega do Cowork.")
    assert cobre("!alocacao/estado.exemplo.yaml", "!**/estado.exemplo.yaml"), (
        "falta a excecao do estado.exemplo.yaml. Sem ela o padrao `**/estado.yaml` "
        "nao o pega, mas a intencao precisa estar escrita: ele DEVE ser versionado, "
        "porque e a prova do achado U-01.")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

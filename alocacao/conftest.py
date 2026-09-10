# -*- coding: utf-8 -*-
"""
Fixtures e guarda de estado compartilhado. Fecha a pendencia P-38.

O PROBLEMA, como estava escrito na pendencia:
  Seis arquivos carregam `C, P = carregar_custos(), carregar_politica()` no import, e
  os testes usam `copy.deepcopy` POR DISCIPLINA, NAO POR GARANTIA. Uma mutacao vazada
  cruzaria testes em silencio: o teste que vazou passa, e outro qualquer falha depois,
  longe da causa.

A ESCOLHA DE DESENHO, e ela nao e obvia — as duas saidas custam quase o mesmo:
  COPIAR SEMPRE     dar a cada teste um `C` e um `P` proprios. Custa 0,23 s na suite.
                    Remove o risco. E ESCONDE O DEFEITO: o teste que muta estado
                    compartilhado continua passando e ninguem aprende.
  DETECTAR E NOMEAR conferir depois de cada teste se o compartilhado mudou, e falhar
                    O TESTE QUE MUDOU. Custa 0,38 s. Nao previne — REPORTA.

  Este projeto escolhe DETECTAR, e a razao vem das doutrinas: esconder um defeito
  atras de uma copia e o padrao que ele passou a semana inteira encontrando e
  rejeitando. O F-02 transformava insumo faltante em zero; a correcao foi RECUSAR,
  nao adotar um default melhor.

  Detectar sozinho tem um problema: se o teste A muta e ninguem restaura, todos os
  testes seguintes falham por causa do A. Entao a guarda tambem RESTAURA depois de
  acusar — so o culpado fica vermelho.

COMO ELA APARECE NA SAIDA, e isto e uma limitacao real e nao um detalhe:
  A guarda mora no TEARDOWN de uma fixture, entao o pytest rotula o resultado como
  ERROR e nao como FAILED. A linha final diz algo como "2 passed, 1 error", e o teste
  culpado aparece nas DUAS contagens — passou a fase de execucao e errou a de
  limpeza. O `returncode` e diferente de zero, entao CI e `pytest` local ficam
  vermelhos do mesmo jeito.

  Da para relabelar isso com um hook `pytest_runtest_makereport`. Nao foi feito de
  proposito: seriam dez linhas de esperteza para mudar uma PALAVRA na saida, e quem
  encontrasse o hook depois teria de entender por que o pytest esta mentindo sobre a
  fase em que o erro aconteceu. A mensagem nomeia o objeto e cita a P-38 — isso
  resolve o problema de verdade, que e saber o que fazer.

O QUE ELA NAO COBRE, declarado:
  A impressao e de `repr()`. Objeto cujo `repr` nao reflete o estado interno passaria
  batido. Para `dict`/`list`/`float`/`str`, que e do que `C` e `P` sao feitos, reflete.

  E ela nao cobre mutacao que o teste DESFAZ antes de terminar. Isso e correto: o
  contrato e sobre o estado no fim, nao sobre o caminho.

RELACAO COM O ACHADO S-02:
  A P-38 pedia protecao contra mutacao vazada. O S-02 mostrou algo pior no mesmo
  terreno: havia um cache GLOBAL cuja chave era o hash do ARQUIVO, entao um teste que
  copiava o `C` e o alterava recebia, em silencio, o valor calculado com o original.
  Copiar nao adiantava. Isolar teste nao adiantava. So a chave do cache adiantava.
  A licao: estado compartilhado nao e so o objeto que voce passa — e todo cache que
  alguem guardou por fora dele.
"""
import copy
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from alocacao import carregar_politica
from motor import carregar as carregar_custos

# Nomes de modulo que a guarda vigia. Sao os objetos que os testes recebem prontos e
# que NENHUM deles deveria alterar.
COMPARTILHADOS = ("C", "P", "PESOS", "AP", "INST", "BASE", "TETO_COMP")


def _impressao(o):
    return hashlib.sha256(repr(o).encode("utf-8")).hexdigest()[:16]


# ── Fixtures: o jeito SANCIONADO de alterar politica ─────────────────────────
@pytest.fixture(scope="session")
def custos_originais():
    """Carregado uma vez. NAO altere — use `custos` se precisar alterar."""
    return carregar_custos()


@pytest.fixture(scope="session")
def politica_original():
    """Carregada uma vez. NAO altere — use `politica` se precisar alterar."""
    return carregar_politica()


@pytest.fixture
def custos(custos_originais):
    """Copia fresca por teste. Altere a vontade: ninguem mais a ve."""
    return copy.deepcopy(custos_originais)


@pytest.fixture
def politica(politica_original):
    """Copia fresca por teste. Altere a vontade: ninguem mais a ve."""
    return copy.deepcopy(politica_original)


# ── A guarda ─────────────────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def guarda_de_estado_compartilhado(request):
    """Acusa o teste que alterou um objeto compartilhado, e restaura o objeto.

    P-38. Antes disso a suite dependia de disciplina: todo teste que precisava mexer
    na politica fazia `copy.deepcopy` de proprio acordo. Funcionava — e "funcionava"
    e a palavra que descreve tambem o F-05, o N-01 e o S-02 antes de alguem medir.

    A guarda transforma a disciplina em garantia SEM tirar a disciplina do caminho:
    quem esquecer o deepcopy descobre no mesmo teste, com o nome do objeto."""
    mod = request.module
    antes = {}
    for nome in COMPARTILHADOS:
        if hasattr(mod, nome):
            obj = getattr(mod, nome)
            antes[nome] = (_impressao(obj), copy.deepcopy(obj))

    yield

    sujos = []
    for nome, (impressao, pristino) in antes.items():
        atual = getattr(mod, nome, None)
        if atual is None or _impressao(atual) == impressao:
            continue
        sujos.append(nome)
        # restaura NO LUGAR, para nao invalidar quem guardou a referencia
        if isinstance(atual, dict):
            atual.clear(); atual.update(copy.deepcopy(pristino))
        elif isinstance(atual, list):
            atual[:] = copy.deepcopy(pristino)
        else:
            setattr(mod, nome, copy.deepcopy(pristino))

    assert not sujos, (
        f"este teste alterou objeto(s) compartilhado(s) do modulo: {', '.join(sujos)}. "
        f"O estado ja foi restaurado, entao os proximos testes nao herdam a sujeira — "
        f"mas o defeito e aqui. Use as fixtures `custos` / `politica`, que entregam "
        f"copia fresca, ou faca `copy.deepcopy` antes de alterar. (P-38)")

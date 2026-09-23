# -*- coding: utf-8 -*-
"""P-113 e A-13 -- o preco de vespera do COTAHIST, e a duplicata que ele acordou.

A DECISAO (dele, 23/09/2026): usar o fechamento do COTAHIST quando a B3 nao traz
`closingPricePriorExDate`, com uma coluna dizendo de onde veio cada preco, e **a B3
ganhando quando existe**. Criterios em `auditoria/P113-CRITERIOS.md`, commitados e
EMPURRADOS antes da corrida (commit `9a08a55`) -- e por isso o "antes" e verificavel
pela P4, que e o que a P-116 cobrava.

O QUE A CORRIDA ACHOU, E NAO ESTAVA PREVISTO -- achado A-13.

Dos 173 eventos `SEM_PRECO` da janela, **161 nao eram fatores faltando: eram o mesmo
pagamento chegando pela segunda porta.** As duas esteiras da B3 se sobrepoem na janela
recente -- o suplemento devolve os ultimos meses, o paginado devolve o historico longo --
e `_chave_de_evento` NAO as colapsa, porque `origem` entra nela de proposito (A-09: dois
registros iguais em PAGINAS diferentes seriam outro julgamento).

Ate 23/09 isso era inofensivo **por acidente**: a copia do suplemento vinha sem preco,
logo sem fator, logo nao era aplicada. **Dar preco a ela e que a acordaria** -- e o preco
cairia DUAS vezes o valor do provento.

    E o P-83 na letra: *insumo ausente adormecido num campo morto continua sendo insumo
    ausente; o campo morto nao e o defeito, e o anestesico.*

A PROVA E A MESMA DO A-09 -- o residuo, no ano em que a sobreposicao mora:

    2025, n=388     ajustado          t
    colapsando      +0,0330%      +0,39     <- indistinguivel de zero
    sem colapsar    +0,7377%      +6,31     <- o provento subtraido duas vezes

E A ARMADILHA QUE ISTO DEIXA ESCRITA: **o AGREGADO melhorava enquanto o ano quebrava.**
Sem colapsar, a media agregada dos cinco anos e -0,0192% (t -0,24); colapsando, -0,1909%
(t -2,53). O numero que parece melhor e o da versao errada -- o +0,74% de 2025 cancelava
o residuo negativo dos outros anos. O laudo do C-02 ja dizia por que a tabela e por ano:
*"um agregado de cinco anos esconderia um ano ruim atras de quatro bons"*. Aqui ele
escondeu um ano QUEBRADO atras de quatro certos.

E O CRITERIO PRE-REGISTRADO NAO TERIA PEGO. O R3 exigia que `|ajustado| < |bruto|` no
agregado e nos cinco anos, e a versao errada passa nos seis. Quem pegou foi a coluna de
origem -- `B3+COTAHIST=131` num degrau e uma pergunta, nao um dado. Fica registrado como
limite da propria regua: *criterio de encolhimento nao detecta super-ajuste.*
"""
from __future__ import annotations
import datetime as dt
import os
import sys
from decimal import Decimal

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ajustar as A  # noqa: E402

RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACERVO = os.path.join(RAIZ_REPO, "data", "bronze", "b3", "cotahist")
SILVER = os.path.join(RAIZ_REPO, "data", "silver",
                      "eventos_silver_2026-09-11_cal-1986-2026.csv")
ANOS = set(range(2021, 2026))

acervo = pytest.mark.skipif(
    not (os.path.isdir(ACERVO) and os.path.isfile(SILVER)),
    reason="acervo ou silver ausente -- ESTE TESTE NAO RODOU")


# ── numeros medidos em 23/09/2026, janela 2021-2025 ──────────────────────────
DO_COTAHIST = 11        # eventos que REALMENTE faltavam preco
REPETIDOS = 162         # o mesmo pagamento, ja contado pela outra esteira
INCOMPLETO = 74         # series (era 78)
DEGRAUS = 1593          # era 1586


def _ev(**kw):
    base = dict(_ticker="PETR4", data_ex="2023-06-15", data_ex_status=A.DERIVADA,
                tipo="DIVIDENDO", valor="1.00", preco_vespera="", origem="suplemento",
                fator="", fator_status=A.SEM_PRECO)
    base.update(kw)
    return base


def _serie(vespera=Decimal("25.00")):
    return {dt.date(2023, 6, 13): Decimal("20.00"),
            dt.date(2023, 6, 14): vespera,
            dt.date(2023, 6, 15): Decimal("24.00")}


# ── a substituicao em si ─────────────────────────────────────────────────────

def test_P113_sem_preco_da_B3_o_fator_sai_do_COTAHIST():
    """O portao. Contra a versao de 21/09 isto reprova: la a linha ficava `SEM_PRECO`."""
    fora, n, rep = A.completar_preco_de_vespera([_ev()], {"PETR4": _serie()})
    assert n == 1 and rep == 0
    r = fora[0]
    assert r["fator_status"] == A.CALCULADO
    assert r["_origem_preco"] == A.ORIGEM_COTAHIST
    # a vespera e o pregao anterior DA SERIE: 14/06, nao 13/06
    assert Decimal(r["preco_vespera"]) == Decimal("25.00")
    assert Decimal(r["fator"]) == (Decimal("25.00") - Decimal(1)) / Decimal("25.00")


def test_P113_a_B3_GANHA_quando_existe():
    """R2, e com prova por mutacao logo abaixo. O preco da B3 nao pode ser trocado pelo
    nosso, mesmo que o nosso exista e mesmo que os dois concordem."""
    r = _ev(preco_vespera="30.00", fator="0.9666", fator_status=A.CALCULADO)
    fora, n, rep = A.completar_preco_de_vespera([r], {"PETR4": _serie()})
    assert n == 0
    assert Decimal(fora[0]["preco_vespera"]) == Decimal("30.00")
    assert fora[0]["_origem_preco"] == A.ORIGEM_B3
    assert fora[0]["fator"] == "0.9666"


def test_P113_a_precedencia_INVERTIDA_seria_pega():
    """A mutacao do teste acima: se alguem fizer o COTAHIST ganhar, o preco da B3 muda.
    Guarda que nunca falhou e guarda que ninguem sabe se funciona."""
    r = _ev(preco_vespera="30.00", fator="0.9666", fator_status=A.CALCULADO)
    p, origem = A.preco_de_vespera(r, _serie())
    assert (p, origem) == (Decimal("30.00"), A.ORIGEM_B3), (
        "a B3 deixou de ganhar: preco_de_vespera preferiu a nossa fonte")
    # e sem o campo da B3 a mesma funcao devolve o COTAHIST -- as duas metades da regra
    p2, origem2 = A.preco_de_vespera(_ev(), _serie())
    assert (p2, origem2) == (Decimal("25.00"), A.ORIGEM_COTAHIST)


def test_P113_falta_REGRA_nao_e_falta_de_PRECO():
    """Subscricao e tipo desconhecido nao ganham preco. Ali nao falta insumo, falta
    criterio -- e preencher preco onde falta criterio produz numero para uma pergunta
    que ninguem respondeu (F-02 na forma mais cara)."""
    for st in ("SEM_FATOR", "TIPO_DESCONHECIDO"):
        fora, n, _ = A.completar_preco_de_vespera([_ev(fator_status=st)],
                                                  {"PETR4": _serie()})
        assert n == 0 and fora[0]["fator_status"] == st
        assert fora[0]["_origem_preco"] == A.ORIGEM_NENHUMA


def test_P113_sem_vespera_na_janela_continua_SEM_PRECO():
    """Nao inventa vespera. O primeiro pregao da serie nao tem dia anterior, e "nao sei"
    e uma resposta."""
    fora, n, _ = A.completar_preco_de_vespera(
        [_ev(data_ex="2023-06-13")], {"PETR4": _serie()})
    assert n == 0 and fora[0]["fator_status"] == A.SEM_PRECO


def test_P113_preco_zero_no_acervo_NAO_vira_fator():
    """Preco invalido nao e preco. A linha leva o status que o `refinar.py` define."""
    fora, n, _ = A.completar_preco_de_vespera(
        [_ev()], {"PETR4": _serie(vespera=Decimal(0))})
    assert n == 0 and fora[0]["fator_status"] != A.CALCULADO


# ── A-13: o mesmo pagamento pelas duas portas ────────────────────────────────

def test_A13_o_mesmo_provento_nas_duas_esteiras_ganha_UM_fator():
    """O achado. Contra a versao que eu ia entregar isto reprova, e reprova produzindo
    numero -- o provento subtraido duas vezes."""
    pag = _ev(origem="paginado", preco_vespera="25.00", fator="0.96",
              fator_status=A.CALCULADO)
    sup = _ev(origem="suplemento")          # mesmo ticker, dia, tipo e valor
    fora, n, rep = A.completar_preco_de_vespera([pag, sup], {"PETR4": _serie()})
    assert n == 0, "o suplemento ganhou fator para um pagamento ja contado"
    assert rep == 1
    assert fora[1]["fator_status"] == A.SEM_PRECO
    assert fora[1]["_repetido_na_outra_esteira"] is True


def test_A13_a_linha_repetida_FICA_na_tabela():
    """Ela nao e lixo: e a segunda testemunha do mesmo pagamento, e o projeto guarda
    testemunha (A-02). O que ela nao ganha e fator."""
    pag = _ev(origem="paginado", preco_vespera="25.00", fator="0.96",
              fator_status=A.CALCULADO)
    fora, _n, _r = A.completar_preco_de_vespera([pag, _ev()], {"PETR4": _serie()})
    assert len(fora) == 2


def test_A13_valor_diferente_no_mesmo_dia_sao_DOIS_pagamentos():
    """O outro lado, e sem ele a correcao apagaria evento real: a ALOS pagou dois
    dividendos diferentes em 19/11/2025, e os dois valem."""
    pag = _ev(origem="paginado", valor="0.10", preco_vespera="25.00", fator="0.996",
              fator_status=A.CALCULADO)
    sup = _ev(origem="suplemento", valor="0.19")
    _fora, n, rep = A.completar_preco_de_vespera([pag, sup], {"PETR4": _serie()})
    assert n == 1 and rep == 0


def test_A13_a_identidade_do_provento_IGNORA_a_esteira_e_o_arquivo():
    """A diferenca entre `_provento` e `_chave_de_evento`, escrita como teste. A segunda
    inclui `origem`/`arquivo_origem` de proposito (A-09); a primeira nao pode, senao ela
    nao responde a pergunta *este pagamento ja esta contado?*"""
    a = _ev(origem="suplemento", arquivo_origem="PETR.json")
    b = _ev(origem="paginado", arquivo_origem="PETR/pagina-003.json")
    assert A._provento(a) == A._provento(b)


def test_A13_zeros_a_direita_nao_criam_pagamento_novo():
    """`0.10216531400` e `0.102165314` sao o MESMO valor, e vieram assim das duas
    esteiras. Comparar por string os trataria como pagamentos diferentes e a duplicata
    passaria -- foi o que quase aconteceu na primeira medicao."""
    assert A._provento(_ev(valor="0.10216531400")) == A._provento(_ev(valor="0.102165314"))


# ── contra o acervo real: os numeros do laudo ────────────────────────────────

@pytest.fixture(scope="module")
def med():
    return A.medir(ACERVO, SILVER, ANOS)


@acervo
@pytest.mark.slow
def test_P113_REAL_os_numeros_da_corrida(med):
    """C1 e C7 do pre-registro, corrigidos pela A-13. A previsao de C1 era **172** e
    saiu **11**: os outros 161 eram duplicata. O criterio reprovou, e reprovar foi o
    resultado -- ver auditoria/P113-MEDIDO.md."""
    assert med.do_cotahist == DO_COTAHIST
    assert med.repetidos == REPETIDOS
    assert len(med.degraus) == DEGRAUS


@acervo
@pytest.mark.slow
def test_P113_REAL_nenhum_evento_do_paginado_usa_preco_nosso(med):
    """R2 contra o acervo: a B3 ganha em todos os 7.765 casos em que ela tem preco."""
    maus = [r for r in med.casados
            if r.get("_origem_preco") == A.ORIGEM_COTAHIST and r["origem"] == "paginado"]
    assert not maus, maus[:5]


@acervo
@pytest.mark.slow
def test_A13_REAL_o_residuo_de_2025_prova_o_colapso(med):
    """A prova do A-13 pelo mesmo instrumento do A-09. 2025 e o ano em que as duas
    esteiras se sobrepoem; colapsando, o residuo ajustado la fica indistinguivel de
    zero. Sem colapsar mede +0,74% com t +6,31 -- medido, nao suposto."""
    pa = A.degraus_por_ano(med.degraus)
    assert abs(pa[2025]["t_ajustado"]) < 2.0, (
        "o residuo de 2025 ficou significativo: %s" % pa[2025])


@acervo
@pytest.mark.slow
def test_A13_REAL_sem_colapsar_o_ano_quebra_e_o_AGREGADO_melhora(med):
    """A mutacao, e ela carrega a armadilha junto: reintroduzir a duplicata piora 2025
    (t +0,39 -> +6,31) **e melhora a media agregada**. Um criterio de agregado teria
    aprovado a versao errada -- e o R3 pre-registrado era exatamente isso."""
    orig = A._provento
    try:
        A._provento = lambda r: (r["_ticker"], r["data_ex"], r["tipo"], r["valor"],
                                 r["origem"])
        mau = A.medir(ACERVO, SILVER, ANOS)
    finally:
        A._provento = orig
    assert mau.repetidos == 0 and mau.do_cotahist == 172
    pa_mau = A.degraus_por_ano(mau.degraus)
    assert pa_mau[2025]["t_ajustado"] > 5, "a mutacao nao reproduziu o super-ajuste"

    _n, ma_bom, _t = A.resumo([g.retorno_ajustado for g in med.degraus])
    _n, ma_mau, _t = A.resumo([g.retorno_ajustado for g in mau.degraus])
    assert abs(ma_mau) < abs(ma_bom), (
        "a armadilha nao se reproduziu: o agregado da versao ERRADA deveria parecer "
        "melhor que o da certa (%s vs %s)" % (ma_mau, ma_bom))


@acervo
@pytest.mark.slow
def test_P113_REAL_as_duas_fontes_concordam_onde_ambas_existem(med):
    """R1 -- a premissa da decisao, remedida a cada corrida. Concordancia medida uma vez
    e concordancia daquela vez. Só compara onde o preco veio DA B3: incluir os
    substituidos seria comparar o COTAHIST com ele mesmo (E-01)."""
    bate = difere = 0
    exemplos = []
    for r in med.casados:
        if r.get("_origem_preco") != A.ORIGEM_B3 or r["data_ex_status"] != A.DERIVADA:
            continue
        serie = med.acervo.precos.get(r["_ticker"])
        d = A._data(r["data_ex"])
        antes = [x for x in serie if x < d] if serie else []
        if not antes:
            continue
        cot = serie[max(antes)]
        if abs(cot - Decimal(r["preco_vespera"])) <= Decimal("0.01"):
            bate += 1
        else:
            difere += 1
            exemplos.append((r["_ticker"], r["data_ex"], r["preco_vespera"], str(cot)))
    assert bate >= 1000 and difere == 0, (bate, difere, exemplos[:10])


@acervo
@pytest.mark.slow
def test_P113_REAL_a_coluna_de_origem_cobre_todo_degrau_com_fator(med):
    """A coluna nao pode ficar vazia onde ha fator de provento: vazia significa "nenhum
    preco entrou nesta conta", que e verdade so para evento de quantidade."""
    for g in med.degraus:
        if g.origem_preco:
            assert set(g.origem_preco.split("+")) <= {A.ORIGEM_B3, A.ORIGEM_COTAHIST}
        else:
            assert A.e_de_quantidade(g.tipos), (
                "degrau de provento sem origem de preco: %s %s" % (g.ticker, g.data_ex))

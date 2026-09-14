# -*- coding: utf-8 -*-
"""
test_e08_bloqueio_e_copia.py -- o `bloqueia` que ninguem honra, e as copias sem relogio.

ACHADO E-08, 13/09/2026. Sao dois defeitos com a mesma raiz: um numero vive em dois
arquivos, e so um dos dois passa pelo aparato que o projeto construiu.
"""

import os
import sys

import pytest
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

C = yaml.safe_load(open(os.path.join(AQUI, "custos.yaml"), encoding="utf-8"))
I = yaml.safe_load(open(os.path.join(AQUI, "instituicoes.yaml"), encoding="utf-8"))
P = yaml.safe_load(open(os.path.join(AQUI, "politica.yaml"), encoding="utf-8"))


# ── E-08a: o bloqueio declarado e o consumidor que nao pergunta ──────────────

def test_E08a_o_ranking_HONRA_o_bloqueia_que_o_nomeia():
    """`custos.yaml -> corretagem.xp_swing` e PARCIAL e declara
    `bloqueia: ["ranking_corretoras"]` -- nomeia ESTE consumidor.

    Ate 13/09/2026 o ranking rodava assim mesmo: `pontuar()` lia `inst.corretagem_rv`
    do instituicoes.yaml e **nunca chamava `val()`**, entao a consequencia declarada
    nao chegava nele. A incerteza era tratada por um multiplicador de 0,8, que
    DESCONTA em vez de barrar -- e ninguem tinha escolhido entre os dois mecanismos:
    o layout dos arquivos e que decidia.

    Agora o ranking se NOMEIA ao carregar o catalogo, e o campo volta `None`.

    ATENCAO AO QUE ESTE TESTE MEDE, e ao que NAO mede. Ele nao mede que a nota da XP
    caiu: ela praticamente nao mudou (46,0 -> 45,9), porque perder a dimensao tira um
    peso de 12 que estava valendo 2,0 -- os dois efeitos quase se cancelam. **O que
    mudou nao foi quanto, foi O QUE O SISTEMA AFIRMA.** Antes ele dizia "a corretagem
    da XP e ruim, nota 2,0". Agora diz "nao sei ler a corretagem da XP, e isso custa
    cobertura". Uma correcao de honestidade pode nao mexer no numero -- e continua
    sendo correcao."""
    import corretoras as K

    no = C["corretagem"]["xp_swing"]
    assert no["status"] == "PARCIAL" and "ranking_corretoras" in no["bloqueia"]

    INST = {i.id: i for i in K.catalogo_instituicoes(contexto=K.RANKING)}
    xp = INST["xp"]
    assert xp.corretagem_rv is None, "o bloqueio nomeado nao alcancou o ranking"
    assert any("ranking_corretoras" in b for b in xp.bloqueios), \
        "o campo foi zerado sem dizer por que -- pior que nao bloquear"

    r = K.pontuar(xp, P["corretora"]["pesos"], 500.0, 20.0, P)
    assert r["dim"]["corretagem"] is None
    assert any("NÃO CONFIRMADA" in n for n in r["notas"])


def test_E08a_SEM_contexto_o_bloqueio_dirigido_NAO_se_aplica():
    """O contexto e opcional de proposito: um consumidor que nao se nomeia nao pode
    reivindicar um bloqueio dirigido a outro. `bloqueia: [ranking_corretoras]` fala
    do ranking, nao de quem so quer ler o cadastro."""
    import corretoras as K

    INST = {i.id: i for i in K.catalogo_instituicoes()}
    assert INST["xp"].corretagem_rv == 4.9
    assert INST["xp"].bloqueios == []


def test_E08a_NAO_CONFIRMADO_barra_com_ou_sem_contexto():
    """Bloqueio dirigido e uma coisa; ausencia de valor e outra. Sem `valor` nao ha o
    que devolver a consumidor nenhum."""
    import corretoras as K
    from motor import InsumoBloqueado

    C2 = {"corretagem": {"fake": {"valor": None, "status": "NAO_CONFIRMADO",
                                  "motivo": "teste"}}}
    bl = []
    assert K._resolver({"de": "corretagem.fake"}, C2, "corretagem_rv", "x", None, bl) is None
    assert bl and "teste" in bl[0]


# ── E-08b: a copia nao herda o relogio ──────────────────────────────────────

# Os pares onde o MESMO FATO aparece nos dois arquivos. Coincidencia de VALOR nao
# entra: quatro casas tem `exercicio_opcao_pct: 0.005`, que bate com o `xp_etf_pct`
# por acaso -- 0,5% e uma taxa comum. Listar aquilo como duplicata seria o falso
# positivo que esta auditoria ja cometeu vezes demais.
PARES = [
    ("xp",    "corretagem_rv",      "xp_swing"),
    ("xp",    "corretagem_etf_pct", "xp_etf_pct"),
    ("caixa", "corretagem_rv",      "caixa_fixa"),
    ("caixa", "corretagem_pct",     "caixa_pct"),
    ("safra", "corretagem_rv",      "safra_terra"),
    ("terra", "corretagem_rv",      "safra_terra"),
]


@pytest.mark.parametrize("iid,campo,constante", PARES)
def test_E08b_o_literal_virou_REFERENCIA(iid, campo, constante):
    """As seis copias sairam. O numero mora num lugar so, e o instituicoes.yaml
    aponta para ele."""
    v = I["instituicoes"][iid]["custos"][campo]
    assert isinstance(v, dict) and v.get("de") == "corretagem." + constante, (
        "%s.%s voltou a ser literal (%r) -- e o N-01 reentrando pelo instituicoes.yaml"
        % (iid, campo, v))


@pytest.mark.parametrize("iid,campo,constante", PARES)
def test_E08b_a_referencia_devolve_o_mesmo_numero_de_antes(iid, campo, constante):
    """INSTANTANEO DOURADO. Os valores medidos ANTES do resolvedor, com o literal.
    Se algum mudar, o resolvedor nao preservou comportamento -- e a mudanca era para
    ser inerte fora do caso bloqueado."""
    import corretoras as K

    ANTES = {("xp", "corretagem_rv"): 4.9, ("xp", "corretagem_etf_pct"): 0.005,
             ("caixa", "corretagem_rv"): 4.49, ("caixa", "corretagem_pct"): 0.0002,
             ("safra", "corretagem_rv"): 4.5, ("terra", "corretagem_rv"): 4.5}
    INST = {i.id: i for i in K.catalogo_instituicoes()}      # sem contexto
    assert getattr(INST[iid], campo) == ANTES[(iid, campo)]


def test_E08b_a_referencia_HERDA_o_relogio(capsys):
    """O ponto estrutural. As constantes de `corretagem` expiram em 04/12/2026. A
    copia crua nao tinha campo de validade nenhum e continuaria valendo em silencio
    para sempre; a referencia passa por `val()`, que avisa em stderr quando vence.

    O projeto construiu um relogio -- agora os dois lados estao ligados nele."""
    import datetime as dt

    import motor
    for c in ("xp_swing", "xp_etf_pct", "caixa_fixa", "caixa_pct", "safra_terra"):
        assert C["corretagem"][c].get("expira"), "%s perdeu o expira" % c

    hoje_real = motor.HOJE
    try:
        motor.HOJE = dt.date(2027, 1, 1)                 # depois do vencimento
        import corretoras as K
        K._INSTITUICOES_CRU.clear()
        K.catalogo_instituicoes()
        err = capsys.readouterr().err
    finally:
        motor.HOJE = hoje_real
    assert "expirou" in err, (
        "nenhum aviso de expiracao saiu: a referencia nao esta passando por val()")


def test_E08_o_catalogo_NAO_copia_e_isso_e_o_contraexemplo():
    """O `catalogo.yaml` faz CERTO, e vale medir para saber como e o certo:

        bova11_xp:
          corr_pct:    {de: "corretagem.xp_etf_pct"}
          saida_extra: {de: "corretagem.xp_etf_pct"}

    Referencia, nao copia -- e por isso herda status, procedencia e `expira` de graca.
    O instituicoes.yaml nao tem resolvedor de referencia, e e por isso que copia.
    **O defeito nao e de quem escreveu o numero: e do formato que nao oferece a
    alternativa.**"""
    cat = yaml.safe_load(open(os.path.join(AQUI, "catalogo.yaml"), encoding="utf-8"))
    rota = cat["rotas"]["bova11_xp"]
    for campo in ("corr_pct", "saida_extra"):
        v = rota[campo]
        assert isinstance(v, dict) and v.get("de") == "corretagem.xp_etf_pct", (
            "bova11_xp.%s deixou de ser referencia e virou literal %r -- e o N-01 "
            "entrando pelo catalogo, que o proprio cabecalho dele proibe." % (campo, v))


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

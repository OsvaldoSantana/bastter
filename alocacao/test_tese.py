# -*- coding: utf-8 -*-
"""Testes dos dois registros do usuario: tese (bloco K) e carrego.

Cada teste nomeia o achado que o motivou, como o manual pede.
"""
import os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alocacao import carregar_politica
from tese import (validar_tese, validar_carrego, impressao, impressao_carrego,
                  carregar_registros)

P = carregar_politica()
TETO = P["compromissos"]["maximo_anos"]
HOJE = dt.date(2026, 9, 3)


def tese_base(**kw):
    t = dict(ativo_id="hash11", funcao="APOSTA", catalogo="ESPECULATIVO",
             dt_classificacao=dt.date(2026, 9, 3), K01_perda_maxima_aceita=1.0,
             K02_tese="ate 31/12/2031 existe na B3 um ETF de cripto com taxa abaixo de 0,5% ao ano",
             K03_prazo=dt.date(2031, 12, 31),
             K04_falsificacao="a taxa de administracao do veiculo subir acima de 1,5% ao ano",
             K05_liquidez_saida_dias=2,
             L_teste_de_classificacao=dict(rodado_em=dt.date(2026, 9, 3),
                                           reprova=["A-06", "C-01"]))
    t.update(kw)
    t["impressao"] = impressao(t)
    return t


def carrego_base(**kw):
    c = dict(ativo_id="td_ipca", funcao="PROTECAO_REAL", catalogo="BUY_AND_HOLD",
             dt_registro=dt.date(2026, 9, 3),
             C01_horizonte_de_carrego=dt.date(2035, 5, 15),
             C02_compromisso="carrego o NTN-B Principal 2035 ate o vencimento, travando "
                             "juro real de 6,8% ao ano na data da compra",
             C03_condicao_de_venda_antecipada="necessidade de caixa que a reserva de "
                             "emergencia nao cobre, comprovada por despesa efetiva",
             C04_custo_de_quebrar=dict(cenario="+2 p.p. de juro real",
                                       perda_estimada_pct=0.16,
                                       fonte_da_estimativa="duration modificada x choque"),
             C05_teto_da_funcao=0.15, C06_reconhecimento=True)
    c.update(kw)
    c["impressao"] = impressao_carrego(c)
    return c


# ══ V-04 · falso positivo por substring ══════════════════════════════════════
def test_tese_com_atende_a_nao_e_recusada_por_conter_tende_a():
    """V-04, demonstrado por execucao no laudo: `if v in texto` recusava
    'a empresa atende a 3 milhoes de clientes ate 31/12/2030' porque 'atende a'
    contem 'tende a'. Uma tese com metrica e data era rejeitada por casamento de
    substring, e o bloco K e o unico componente que exige esforco criativo do
    usuario — um validador que recusa a primeira tentativa correta e o caminho mais
    rapido para o arquivo nunca ser preenchido."""
    t = tese_base(K02_tese="a empresa atende a 3 milhoes de clientes ate 31/12/2030")
    ok, probs, _ = validar_tese(t, HOJE, TETO)
    assert ok, probs


def test_tende_a_isolado_continua_recusado():
    t = tese_base(K02_tese="o setor tende a crescer 20% ate 31/12/2030")
    ok, probs, _ = validar_tese(t, HOJE, TETO)
    assert not ok and any("nao falsificavel" in p for p in probs)


def test_potencial_e_aviso_e_nao_rejeicao():
    """Nenhuma regex separa 'capacidade potencial instalada' de 'ativo promissor'.
    Rebaixado a aviso; a regra dura que sobrevive e estrutural, nao lexical."""
    t = tese_base(K02_tese="a capacidade potencial instalada atinge 500 MW ate 31/12/2029")
    ok, probs, avisos = validar_tese(t, HOJE, TETO)
    assert ok, probs
    assert any("potencial" in a for a in avisos)


def test_tese_sem_numero_e_recusada():
    """O teste estrutural que substitui a lista lexical: uma tese falsificavel
    afirma QUANTO ou QUANDO, nao apenas o que."""
    t = tese_base(K02_tese="a adocao institucional do ativo se consolida no mercado brasileiro")
    ok, probs, _ = validar_tese(t, HOJE, TETO)
    assert not ok and any("sem nenhum numero" in p for p in probs)


# ══ V-10 · PENDENTE tratado como ausente ═════════════════════════════════════
def test_impressao_pendente_diz_ausente_e_nao_alterada():
    """V-10: `impressao: PENDENTE` caia no ramo `elif imp != calc` e imprimia
    'tese ALTERADA apos o registro' para algo que nunca foi registrado."""
    t = tese_base(); t["impressao"] = "PENDENTE"
    ok, probs, _ = validar_tese(t, HOJE, TETO)
    assert not ok
    assert any("impressao ausente" in p for p in probs)
    assert not any("ALTERADA" in p for p in probs)


def test_tese_alterada_apos_registro_continua_invalida():
    t = tese_base()
    t["K03_prazo"] = dt.date(2033, 1, 1)          # esticou o prazo sem re-registrar
    ok, probs, _ = validar_tese(t, HOJE, TETO)
    assert not ok and any("ALTERADA" in p for p in probs)


# ══ K-04 nao pode ser condicao de preco ══════════════════════════════════════
def test_k04_de_preco_e_recusada():
    """Com K01 = 100%, a queda ja esta dentro da perda aceita: uma condicao de preco
    encerraria a posicao exatamente quando a tese exigiria paciencia, e a perda
    maxima aceita de 100% vira ficcao."""
    t = tese_base(K04_falsificacao="o preco cair abaixo de R$ 30,00")
    ok, probs, _ = validar_tese(t, HOJE, TETO)
    assert not ok and any("condicao de PRECO" in p for p in probs)


def test_k04_de_disciplina_e_aceita():
    """O tipo menos obvio e mais util: encerra a posicao quando ela da certo demais."""
    t = tese_base(K04_falsificacao="a exposicao passar de 6% do patrimonio por 2 revisoes "
                                   "anuais seguidas sem novo aporte")
    ok, probs, _ = validar_tese(t, HOJE, TETO)
    assert ok, probs


# ══ teto de compromisso de 10 anos ═══════════════════════════════════════════
def test_k03_acima_do_teto_de_compromisso_e_recusada():
    """Decisao do usuario em 03/09/2026: nenhum compromisso maior que 10 anos."""
    t = tese_base(K03_prazo=dt.date(2045, 1, 1))
    ok, probs, _ = validar_tese(t, HOJE, TETO)
    assert not ok and any("acima do teto declarado" in p for p in probs)


def test_carrego_acima_do_teto_e_recusado_e_diz_ate_quando():
    """E o caso do NTN-B Principal 2060 — o papel que a versao 1.0.0 alocava com 17%
    sob DATADO sem prazo nenhum a casar. Agora ele fica fora por REGRA declarada, e a
    mensagem diz ate qual vencimento o teto permite ir."""
    c = carrego_base(C01_horizonte_de_carrego=dt.date(2060, 8, 15))
    ok, probs, _, dur = validar_carrego(c, HOJE, TETO)
    assert not ok
    assert dur > 30
    msg = " ".join(probs)
    assert "acima do teto declarado" in msg and "2036" in msg


def test_carrego_dentro_do_teto_e_valido_e_devolve_a_duracao():
    """A duracao NAO e constante de catalogo: vem do papel que voce se compromete a
    carregar. E por isso que o registro precede a alocacao."""
    ok, probs, _, dur = validar_carrego(carrego_base(), HOJE, TETO)
    assert ok, probs
    assert 8.5 < dur < 8.8


# ══ C-03 e o modo de falha da funcao PROTECAO_REAL ═══════════════════════════
def test_c03_de_preco_e_recusada():
    """O modo de falha desta funcao e vender quando a marcacao abre. Uma condicao de
    preco em C03 AUTORIZA exatamente o erro que o registro existe para impedir."""
    c = carrego_base(C03_condicao_de_venda_antecipada="se o titulo cair mais de 20%")
    ok, probs, _, _ = validar_carrego(c, HOJE, TETO)
    assert not ok and any("condicao de PRECO" in p for p in probs)


def test_c06_reconhecimento_falso_invalida():
    c = carrego_base(C06_reconhecimento=False)
    ok, probs, _, _ = validar_carrego(c, HOJE, TETO)
    assert not ok and any("C06_reconhecimento" in p for p in probs)


def test_c04_sem_perda_estimada_invalida():
    """Escrever o numero ANTES e o que muda o comportamento depois."""
    c = carrego_base(C04_custo_de_quebrar=dict(cenario="+2 p.p.", perda_estimada_pct=None))
    ok, probs, _, _ = validar_carrego(c, HOJE, TETO)
    assert not ok and any("perda_estimada_pct" in p for p in probs)


def test_c02_sem_numero_invalida():
    c = carrego_base(C02_compromisso="carrego o titulo ate o vencimento")
    ok, probs, _, _ = validar_carrego(c, HOJE, TETO)
    assert not ok and any("C02 sem numero" in p for p in probs)


# ══ o arquivo do repositorio ═════════════════════════════════════════════════
def test_repositorio_assinado_libera_so_o_que_a_assinatura_diz():
    """Ate 26/09/2026 este teste exigia que o repositorio trouxesse so modelos invalidos.
    A P-01 (decisao `01b`) assinou os dois registros. O que ele guarda agora: as duas
    assinaturas validas, com as impressoes que ele aprovou, e o td_ipca em REGRA_DECIDIDA
    -- valido, mas sem peso ate a compra (G-07). Se alguem editar o texto sem reassinar, a
    impressao nao bate e o registro deixa de valer; se o estado virar COMPROMISSO_ATIVO sem
    a compra, o `estado` abaixo cai."""
    import alocacao as A
    from motor import carregar as cc
    teses, carregos = carregar_registros(compromisso_maximo_anos=TETO)
    assert set(teses) == {"hash11"} and set(carregos) == {"td_ipca"}
    assert teses["hash11"]["valida"], teses["hash11"]["motivo"]
    assert carregos["td_ipca"]["valida"], carregos["td_ipca"]["motivo"]
    assert teses["hash11"]["tese"]["impressao"] == "ea8c8769bbf021e2"
    assert carregos["td_ipca"]["carrego"]["impressao"] == "942c75bae248327b"
    assert carregos["td_ipca"]["carrego"]["estado"] == "REGRA_DECIDIDA"
    P = A.carregar_politica()
    e = A.Estado(despesa_mensal=4500, reserva_atual=40500, aporte_mensal=500,
                 horizonte_anos=25, estabilidade_renda="baixa")
    r = A.alocar(e, cc(), P, teses=teses, carregos=carregos)
    assert r["alvo"]["pesos"].get("hash11", 0) > 0
    assert "td_ipca" not in r["alvo"]["pesos"]
    assert not [p for p in r["pendencias"] if p.id.startswith("reassinar:")], \
        "com a meta de 9 meses o C03 assinado nao pode pedir reassinatura"


def test_o_modelo_do_repositorio_cabe_no_teto_de_compromisso():
    """O modelo nao pode ensinar um vencimento que a propria politica proibe."""
    _, carregos = carregar_registros(compromisso_maximo_anos=TETO)
    d = carregos["td_ipca"]["duracao_anos"]
    assert d is not None and d <= TETO
    assert not any("acima do teto" in m for m in carregos["td_ipca"]["motivo"].split("; "))


# ── G-01: estado REGRA_DECIDIDA ──────────────────────────────────────────────
def _carrego_regra():
    return dict(ativo_id="td_ipca", funcao="PROTECAO_REAL", catalogo="BUY_AND_HOLD",
                dt_registro=dt.date(2026, 9, 5), estado="REGRA_DECIDIDA",
                C01_horizonte_de_carrego=dt.date(2035, 5, 15),
                C02_compromisso="AGUARDA_COMPRA",
                C03_condicao_de_venda_antecipada=(
                    "venda autorizada apenas por necessidade de caixa por despesa ja "
                    "incorrida que a reserva de emergencia nao cobrir, esgotada a reserva"),
                C04_custo_de_quebrar={"estado": "AGUARDA_COMPRA"},
                C05_teto_da_funcao=0.15, C06_reconhecimento=True)

def test_regra_decidida_aceita_c02_e_c04_adiados():
    """Antes do G-01 este registro era invalido por 'C02 ausente' — e a unica forma
    de valida-lo era inventar um juro real que o usuario nao contratou."""
    c = _carrego_regra()
    c["impressao"] = impressao_carrego(c)
    ok, pr, av, dur = validar_carrego(c, hoje=dt.date(2026,9,5), compromisso_maximo_anos=10)
    assert ok, pr
    assert any("REGRA_DECIDIDA" in a for a in av), "o estado tem de aparecer no aviso"

def test_regra_decidida_exige_o_adiamento_em_voz_alta():
    """Campo vazio nao vale: 'ainda nao sei' e 'esqueci' precisam ser distinguiveis."""
    c = _carrego_regra(); c["C02_compromisso"] = ""
    c["impressao"] = impressao_carrego(c)
    ok, pr, _, _ = validar_carrego(c, hoje=dt.date(2026,9,5), compromisso_maximo_anos=10)
    assert not ok and any("AGUARDA_COMPRA" in x for x in pr)

def test_compromisso_ativo_continua_exigindo_tudo():
    """A porta nova nao pode afrouxar a antiga."""
    c = _carrego_regra(); c["estado"] = "COMPROMISSO_ATIVO"
    c["impressao"] = impressao_carrego(c)
    ok, pr, _, _ = validar_carrego(c, hoje=dt.date(2026,9,5), compromisso_maximo_anos=10)
    assert not ok
    assert any("C02" in x for x in pr) and any("C04" in x for x in pr)

def test_estado_desconhecido_e_rejeitado():
    c = _carrego_regra(); c["estado"] = "MAIS_OU_MENOS"
    c["impressao"] = impressao_carrego(c)
    ok, pr, _, _ = validar_carrego(c, hoje=dt.date(2026,9,5), compromisso_maximo_anos=10)
    assert not ok and any("desconhecido" in x for x in pr)


def test_P01_o_comando_que_calcula_a_impressao_roda(capsys):
    """`python tese.py` e o que o teses.yaml manda rodar antes de assinar, e ele caia com
    KeyError desde a L-01: `compromissos` mora no perfil.yaml, e so `carregar_politica`
    funde os dois. Sem este teste, a P-01 ficaria sem o instrumento da propria assinatura."""
    import tese as _t
    _t.main()
    out = capsys.readouterr().out
    assert "teto de compromisso declarado:" in out
    assert "impressao a registrar: " in out and "hash11" in out and "td_ipca" in out

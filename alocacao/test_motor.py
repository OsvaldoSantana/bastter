# -*- coding: utf-8 -*-
"""Testes das camadas 1, 3 e 4 do manual: unitario, canonico com oraculo, invariante."""
import os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from motor import carregar, val, custodia_rv_aa, InsumoBloqueado

C = carregar()
FX   = C["b3"]["custodia_rv_faixas"]["valor"]
ISEN = C["b3"]["custodia_rv_isencao"]["valor"]

# ── camada 3 — canonicos com oraculo externo (tabela literal da B3) ───────────
def test_custodia_abaixo_da_isencao_e_zero():
    """Oraculo: B3, texto literal 'posicoes ate R$ 26.471,77 sao isentos desta taxa'."""
    assert custodia_rv_aa(26_471.77, FX, ISEN) == 0.0
    assert custodia_rv_aa(10_000.00, FX, ISEN) == 0.0

def test_custodia_primeira_faixa():
    """R$100 mil: excedente R$73.528,23, todo na faixa 1 (0,0500% a.a.)."""
    esperado = (100_000 - ISEN) * 0.000500
    assert custodia_rv_aa(100_000, FX, ISEN) == pytest.approx(esperado, rel=1e-9)

def test_custodia_atravessa_faixas():
    """R$300 mil: 115.000-26.471,77 a 0,05% + 115.000 a 0,04% + resto a 0,02%.
    Este teste teria pego K-03 — o v1 cobrava 0,05% sobre TODO o excedente."""
    esperado = (115_000-ISEN)*0.000500 + 115_000*0.000400 + (300_000-230_000)*0.000200
    assert custodia_rv_aa(300_000, FX, ISEN) == pytest.approx(esperado, rel=1e-9)
    assert custodia_rv_aa(300_000, FX, ISEN) < (300_000-ISEN)*0.000500   # < que o v1

# ── camada 4 — invariantes ────────────────────────────────────────────────────
def test_faixas_de_custodia_sao_monotonicas():
    """Nenhuma faixa e mais cara que a anterior, e os tetos sao crescentes."""
    tx = [f["taxa_aa"] for f in FX]
    assert tx == sorted(tx, reverse=True)
    tetos = [f["ate"] for f in FX if f["ate"] is not None]
    assert tetos == sorted(tetos)
    assert FX[-1]["ate"] is None          # ultima faixa e aberta

def test_invariante_cdi_diario():
    """(1+CDI_aa)^(1/252)-1 deve bater com a serie 12 do BCB (0,051660%).
    A pesquisa conferiu isto a mao uma vez; aqui roda sozinho."""
    cdi = val(C["macro"]["cdi_aa"], contexto="cdi")
    assert (1+cdi)**(1/252)-1 == pytest.approx(0.00051660, abs=1e-7)

def test_invariante_poupanca_legal():
    """Lei 12.703/2012: com Selic > 8,5%, poupanca = 0,5% a.m. + TR.
    TR de 0,1448% e poupanca de 0,6455% (series 226 e 25) devem fechar."""
    assert (1.005*1.001448)-1 == pytest.approx(0.006455, abs=1e-6)


# ══ E-01 · a guarda do F-02 faltava no modulo irmao ══════════════════════════
# P-43 (24/09/2026): os quatro testes do E-01 e os de K-06, K-07 e custodia absorvida
# mediam `motor.simular`/`montar_rotas`, que sairam. K-06 e K-07 foram medidos e
# trazidos para o test_alocacao (test_K06_*, test_K07_*); a recusa da rota bloqueada
# (F-02/E-01) e o aporte zero ja estavam la. A custodia absorvida nao tem par na
# alocacao -- vive como dimensao do ranking em `corretoras.py`.


def test_valor_bloqueado_levanta_excecao():
    """Um calculo que depende de NAO_CONFIRMADO recusa-se a rodar, em vez de rodar com premissa."""
    with pytest.raises(InsumoBloqueado):
        val(C["etf"]["ACWI11"], contexto="acwi")
    with pytest.raises(InsumoBloqueado):
        val(C["etf"]["BOVV11"], contexto="bovv")

def test_status_parcial_pode_ser_recusado():
    with pytest.raises(InsumoBloqueado):
        val(C["corretagem"]["xp_swing"], permitir_parcial=False, contexto="xp")
    assert val(C["corretagem"]["xp_swing"], permitir_parcial=True, contexto="xp") == 4.90

def test_toda_constante_tem_procedencia():
    """Nenhum valor COMPLETO sem fonte -- e, quando o `valor` e uma SERIE, nenhuma
    faixa da serie sem a dela.

    16/09/2026. A guarda parava no `valor` e nunca olhava dentro. `tributacao.
    ir_jcp_fonte` tem quatro vigencias vindas de QUATRO normas diferentes, e uma
    unica frase no topo do no teria satisfeito esta guarda dizendo quase nada sobre
    o que o motor de fato le.

    A regra acrescentada e DE PROPOSITO mais estreita que "toda faixa precisa de
    fonte", que reprovaria `ir_rf_faixas` (uma lei so, quatro prazos) sem que houvesse
    defeito: se ALGUMA faixa declara fonte, TODAS precisam. Serie meio declarada e
    pior que serie nao declarada, porque quem le supoe que a faixa calada herda a
    fonte da de cima -- e nesta serie herdar e exatamente o erro: a faixa de 18% vem
    de uma MP que caducou, e as vizinhas nao."""
    faltando = []
    def anda(no, cam=""):
        if isinstance(no, dict):
            if "valor" in no and no.get("status") == "COMPLETO":
                if not no.get("fonte"): faltando.append(cam)
                faixas = [f for f in (no["valor"] if isinstance(no["valor"], list) else [])
                          if isinstance(f, dict)]
                if any(f.get("fonte") for f in faixas):
                    faltando.extend(f"{cam}.valor[{i}]" for i, f in enumerate(faixas)
                                    if not f.get("fonte"))
            for k, v in no.items():
                if k not in ("valor","status","fonte","acesso","expira","nota","motivo","bloqueia"):
                    anda(v, f"{cam}.{k}")
    anda(C)
    assert not faltando, f"sem fonte: {faltando}"


# ── F-05: `bloqueia` deixou de ser prosa ─────────────────────────────────────
def test_bloqueia_viaja_na_excecao():
    """Ate 05/09/2026 o campo existia no YAML e NENHUMA linha o lia. A excecao
    dizia o motivo e nunca a consequencia."""
    C = carregar()
    with pytest.raises(InsumoBloqueado) as e:
        val(C["etf"]["BOVV11"], contexto="etf.BOVV11")
    assert "BLOQUEIA" in str(e.value) and "tabela_etf_rv_completa" in str(e.value)

def test_todo_insumo_nao_completo_declara_o_que_bloqueia():
    """Cobertura que o test_cobertura_yaml nao dava: ele varre politica.yaml, nunca
    custos.yaml. Um valor PARCIAL ou NAO_CONFIRMADO sem `bloqueia` e um insumo cujo
    custo de faltar ninguem escreveu."""
    C = carregar()
    nus = []
    def anda(d, p=""):
        if isinstance(d, dict):
            if "valor" in d:
                if d.get("status") in ("NAO_CONFIRMADO", "PARCIAL") and not d.get("bloqueia"):
                    nus.append(p.lstrip("."))
                return
            for k, v in d.items(): anda(v, f"{p}.{k}")
    anda(C)
    assert not nus, "status nao-COMPLETO sem `bloqueia`: " + ", ".join(nus)

def test_bloqueia_so_aparece_onde_faz_sentido():
    """O inverso: COMPLETO com `bloqueia` e contradicao — nada esta bloqueado."""
    C = carregar()
    erro = []
    def anda(d, p=""):
        if isinstance(d, dict):
            if "valor" in d:
                if d.get("status") == "COMPLETO" and d.get("bloqueia"):
                    erro.append(p.lstrip("."))
                return
            for k, v in d.items(): anda(v, f"{p}.{k}")
    anda(C)
    assert not erro, "COMPLETO declarando bloqueia: " + ", ".join(erro)


def test_nenhuma_constante_fica_com_trecho_nao_conferido():
    """MAPA-CONSTANTES achou 6 citacoes que apontavam para trecho ausente do corpo de
    fontes; todas foram transcritas ou corrigidas em 05/09/2026. Constante nova que
    entre com `trecho_conferido: false` falha aqui — a divida nao volta em silencio."""
    C = carregar()
    faltam = []
    def anda(d, p=""):
        if isinstance(d, dict):
            if "valor" in d:
                if d.get("trecho_conferido") is False: faltam.append(p.lstrip("."))
                return
            for k, v in d.items(): anda(v, f"{p}.{k}")
    anda(C)
    assert not faltam, "citacao sem trecho conferido: " + ", ".join(faltam)


# ── P-70: HOJE fixo em 2026-09-01, resolvido no import, deixava o aviso mudo ──
def test_P70_val_avisa_quando_a_data_injetada_passa_da_expiracao(capsys):
    """`hoje` e injetado por parametro -- o teste nao depende do relogio real e
    nao muda de resultado sozinho conforme os dias passam, ao contrario do que
    a antiga constante `HOJE` fazia com o aviso em producao."""
    no = {"valor": 1.0, "status": "COMPLETO", "fonte": "teste",
          "expira": dt.date(2026, 9, 28)}
    r = val(no, contexto="teste.expira", hoje=dt.date(2026, 9, 29))
    assert r == 1.0
    err = capsys.readouterr().err
    assert "[AVISO]" in err and "teste.expira" in err and "2026-09-28" in err

def test_P70_val_fica_em_silencio_antes_da_expiracao(capsys):
    """O espelho do teste acima, com a MESMA constante. Sem ele o teste anterior
    nao provaria nada: passaria igual se `val` avisasse sempre, cega para a
    data injetada."""
    no = {"valor": 1.0, "status": "COMPLETO", "fonte": "teste",
          "expira": dt.date(2026, 9, 28)}
    r = val(no, contexto="teste.expira", hoje=dt.date(2026, 9, 27))
    assert r == 1.0
    err = capsys.readouterr().err
    assert err == ""

def test_P70_toda_expira_e_data_e_nunca_texto():
    """P-70, segunda metade (11/09/2026). Destravar `HOJE` nao bastava: `val()` so avisa
    quando `expira` e `dt.date`, e `expira: '2026-12-04'` ENTRE ASPAS carrega como texto
    -- o aviso fica mudo sem erro nenhum. Eram quatro, e duas eram `cdi_aa` e `selic_aa`,
    as constantes que o CLAUDE.md cita como prova de que o mecanismo funciona: foram
    reconferidas em 05/09 e a data nova foi escrita com aspas. Medido no tipo CARREGADO,
    porque o defeito so existe depois do `safe_load`."""
    texto = []
    def anda(d, p=""):
        if isinstance(d, dict):
            if "valor" in d:
                e = d.get("expira")
                if e is not None and not isinstance(e, dt.date):
                    texto.append(f"{p.lstrip('.')} = {e!r}")
                return
            for k, v in d.items(): anda(v, f"{p}.{k}")
    anda(carregar())
    assert not texto, ("`expira` que nao e data -- val() nunca avisa nestas. Tire as "
                       "aspas (AAAA-MM-DD sem aspas e data em YAML): " + "; ".join(texto))

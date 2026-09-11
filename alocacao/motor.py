# -*- coding: utf-8 -*-
"""
Motor de custo v2 — corrige os achados K-01 a K-11 do laudo de 01/09/2026.

Mudancas em relacao a v1:
  K-01/K-07  status viaja com o dado; rota com insumo NAO_CONFIRMADO nao entra na ordenacao
  K-03       custodia da B3 com as 10 faixas progressivas (v1 usava so a faixa 1, a mais cara)
  K-04       interpretacao da isencao declarada e parametrizavel; cenario de custodia absorvida
  K-05       taxa de administracao aparece na tabela de entrada
  K-06       perna de saida modelada (corretagem, B3 na venda, IOF de repatriacao)
  K-08       premissas de modelagem declaradas; c>aporte emite alerta em vez de truncar em silencio
  K-11       constantes vem do YAML com procedencia; caminhos relativos; roda com -m; testes
"""
from __future__ import annotations
import os, sys, datetime as dt
from dataclasses import dataclass, field
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))

class InsumoBloqueado(Exception):
    """Levantada quando um calculo depende de valor NAO_CONFIRMADO."""

# ── carga com verificacao de status e validade ────────────────────────────────
def carregar(path=None):
    with open(path or os.path.join(AQUI, "custos.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

def _consequencia(no):
    """Achado F-05: `bloqueia` era prosa. Agora viaja na excecao.

    A P1 promete que um insumo bloqueado diz O QUE ele bloqueia. Ate 05/09/2026 o
    campo existia no custos.yaml e NENHUMA linha de codigo o lia — a excecao dizia
    so o motivo, nunca a consequencia. Quem via `InsumoBloqueado: etf.BOVV11` nao
    sabia que o que morria era a tabela completa de ETF de renda variavel.
    """
    b = no.get("bloqueia") or []
    if isinstance(b, str): b = [b]
    return f"  BLOQUEIA: {', '.join(b)}" if b else \
           "  (sem `bloqueia` declarado — o custo de nao ter este valor nao esta escrito)"

def val(no, *, permitir_parcial=True, contexto="", hoje=None):
    """Extrai o valor de um no do YAML, recusando NAO_CONFIRMADO.

    P-70: `HOJE` era uma constante fixa (2026-09-01) resolvida no IMPORT do
    modulo — o aviso de expiracao ficava mudo a partir do primeiro dia
    seguinte e ninguem via. `hoje` agora e parametro; quando omitido, resolve
    para `dt.date.today()` NO MOMENTO DA CHAMADA, nao no import."""
    if not isinstance(no, dict) or "valor" not in no:
        return no
    st = no.get("status", "COMPLETO")
    if st == "NAO_CONFIRMADO" or no["valor"] is None:
        raise InsumoBloqueado(f"{contexto}: {no.get('motivo','valor nao confirmado')}"
                              + _consequencia(no))
    if st == "PARCIAL" and not permitir_parcial:
        raise InsumoBloqueado(f"{contexto}: status PARCIAL — {no.get('motivo','')}"
                              + _consequencia(no))
    exp = no.get("expira")
    if exp and isinstance(exp, dt.date):
        agora = hoje if hoje is not None else dt.date.today()
        if agora > exp:
            print(f"  [AVISO] {contexto}: valor expirou em {exp} "
                  f"(fonte: {no.get('fonte','?')})", file=sys.stderr)
    return no["valor"]

# ── K-03: custodia progressiva de verdade ─────────────────────────────────────
def custodia_rv_aa(patrimonio, faixas, isencao, interpretacao="deducao"):
    """Taxa anual EM REAIS da custodia de renda variavel da B3.

    As faixas da B3 sao definidas sobre o VALOR EM CUSTODIA (absoluto), nao sobre
    o excedente. A isencao apenas retira os primeiros `isencao` reais da base.
    Confundir os dois sistemas de coordenadas foi o bug que o teste canonico pegou.
    """
    if patrimonio <= isencao:
        return 0.0
    isento_restante = isencao if interpretacao == "deducao" else 0.0
    total, piso = 0.0, 0.0
    for fx in faixas:
        teto = fx["ate"] if fx["ate"] is not None else float("inf")
        if patrimonio <= piso:
            break
        largura = min(patrimonio, teto) - piso          # parte do patrimonio nesta faixa
        isenta_aqui = min(isento_restante, largura)     # consome a isencao das faixas baixas
        isento_restante -= isenta_aqui
        total += (largura - isenta_aqui) * fx["taxa_aa"]
        piso = teto
    return total

# ── rotas ─────────────────────────────────────────────────────────────────────
@dataclass
class Rota:
    grupo: str
    nome: str
    corr_fix: float = 0.0
    corr_pct: float = 0.0
    b3_vista: bool = False          # paga tarifa da B3 na compra E na venda
    entrada_pct: float = 0.0        # spread + IOF (exterior)
    saida_pct: float = 0.0          # IOF de repatriacao + spread de volta
    adm_aa: float = 0.0
    custodia_rv: bool = False
    custodia_td: bool = False
    td_isento: bool = False
    bloqueios: list = field(default_factory=list)   # motivos que a tiram da ordenacao
    nota: str = ""

    @property
    def confiavel(self): return not self.bloqueios

def montar_rotas(C):
    """Monta as rotas da CAMADA DE CUSTO, capturando InsumoBloqueado como marcador em
    vez de abortar.

    ACHADO T-01 (06/09/2026), encontrado pelo ruff e confirmado pelo `impacto.py`.
    Este e um SEGUNDO CATALOGO, paralelo ao `catalogo.yaml`: 22 rotas contra 25, com
    13 nomes que so existem aqui. A P-36 tirou o catalogo de alocacao do Python e
    deixou este — havia tres catalogos e eu contei dois.

    Nenhum modulo de producao o chama; so o `test_motor.py`. Nao foi apagado: apagar
    codigo com teste proprio sem medir o que os testes guardam e como se perde uma
    rede. A pendencia P-43 registra a decisao a tomar.

    A linha `B3V = val(...)` foi removida daqui: a atribuicao era morta (copia da
    funcao de baixo) e a CHAMADA contradizia a propria docstring — ela ABORTARIA se
    `b3.vista_total_pct` fosse NAO_CONFIRMADO, numa funcao que promete capturar o
    bloqueio como marcador. O ruff viu a variavel; o defeito era a chamada."""
    IOF_I = val(C["exterior"]["iof_investimento"], contexto="iof.investimento")
    IOF_R = val(C["exterior"]["iof_repatriacao"], contexto="iof.repatriacao")
    R = []
    def add(**kw): R.append(Rota(**kw))

    # renda fixa / caixa
    add(grupo="Caixa e renda fixa", nome="Tesouro Reserva / Selic ate R$10k",
        custodia_td=True, td_isento=True, nota="isento de custodia ate R$10k por CPF")
    add(grupo="Caixa e renda fixa", nome="Tesouro Selic acima de R$10k",
        custodia_td=True, td_isento=True, nota="0,20% a.a. so sobre o excedente")
    add(grupo="Caixa e renda fixa", nome="Tesouro IPCA+ / Prefixado",
        custodia_td=True, td_isento=False, nota="0,20% a.a. desde o primeiro real")
    add(grupo="Caixa e renda fixa", nome="Cofrinho / RDB 100% CDI (FGC)",
        nota="sem taxa; o custo e risco de credito do emissor")

    # ETF Brasil
    for tk in ("PIBB11","DIVO11","BOVA11","IVVB11","SMAL11","HASH11"):
        try:
            adm = val(C["etf"][tk], contexto=f"etf.{tk}")
            add(grupo="ETF na B3", nome=f"{tk} — corretora zero", b3_vista=True,
                adm_aa=adm, custodia_rv=True)
        except InsumoBloqueado as e:
            add(grupo="ETF na B3", nome=f"{tk} — corretora zero", b3_vista=True,
                custodia_rv=True, bloqueios=[str(e)])
    try:
        adm = val(C["etf"]["BOVV11"], contexto="etf.BOVV11")
        add(grupo="ETF na B3", nome="BOVV11 — corretora zero", b3_vista=True,
            adm_aa=adm, custodia_rv=True)
    except InsumoBloqueado as e:
        add(grupo="ETF na B3", nome="BOVV11 — corretora zero", b3_vista=True,
            custodia_rv=True, bloqueios=[str(e)])
    add(grupo="ETF na B3", nome="BOVA11 — via XP (0,50% em ETF)", b3_vista=True,
        corr_pct=val(C["corretagem"]["xp_etf_pct"], contexto="xp.etf"),
        saida_pct=val(C["corretagem"]["xp_etf_pct"], contexto="xp.etf"),
        adm_aa=val(C["etf"]["BOVA11"], contexto="etf.BOVA11"), custodia_rv=True,
        nota="0,50% na entrada E na saida")

    # acao individual
    add(grupo="Acao individual", nome="Corretora taxa zero", b3_vista=True, custodia_rv=True,
        nota="tem a isencao de R$20 mil/mes na venda")
    add(grupo="Acao individual", nome="Safra / Terra — R$4,50 por ordem", b3_vista=True,
        corr_fix=val(C["corretagem"]["safra_terra"], contexto="corr.safra"), custodia_rv=True)
    add(grupo="Acao individual", nome="Caixa — R$4,49 + 0,02%", b3_vista=True,
        corr_fix=val(C["corretagem"]["caixa_fixa"], contexto="corr.caixa"),
        corr_pct=val(C["corretagem"]["caixa_pct"], contexto="corr.caixa"), custodia_rv=True)
    try:
        xp = val(C["corretagem"]["xp_swing"], permitir_parcial=False, contexto="corr.xp_swing")
        add(grupo="Acao individual", nome="XP swing trade", b3_vista=True,
            corr_fix=xp, custodia_rv=True)
    except InsumoBloqueado as e:
        add(grupo="Acao individual", nome="XP swing trade — R$4,90", b3_vista=True,
            corr_fix=4.90, custodia_rv=True, bloqueios=[str(e)])

    # exterior
    IVV = val(C["etf"]["IVV"], contexto="etf.IVV")
    for nome, spread in (("Avenue — melhor degrau", C["exterior"]["spread_avenue_melhor"]),
                         ("Avenue — degrau inicial", C["exterior"]["spread_avenue_inicial"]),
                         ("Nomad — nivel 5",        C["exterior"]["spread_nomad_n5"]),
                         ("Nomad — nivel 1",        C["exterior"]["spread_nomad_n1"])):
        s = val(spread, contexto=f"spread.{nome}")
        add(grupo="Exterior", nome=f"ETF EUA (IVV) — {nome}",
            entrada_pct=s+IOF_I, saida_pct=IOF_R, adm_aa=IVV,
            nota=f"spread {s*100:.2f}% + IOF 1,10%; saida 0,38%")
    # Vest — BLOQUEADA: o "sem IOF" e posicao da plataforma, nao fato confirmado
    vs = val(C["exterior"]["vest_stablecoin"]["spread"], contexto="vest.spread")
    add(grupo="Exterior", nome="ETF EUA (IVV) — Vest stablecoin",
        entrada_pct=vs, saida_pct=IOF_R, adm_aa=IVV,
        bloqueios=[C["exterior"]["vest_stablecoin"]["iof"]["motivo"]],
        nota="se o IOF de 1,10% se aplicar, vai a 2,50% e fica PIOR que a Avenue")
    add(grupo="Exterior", nome="Rota Wise como conta",
        entrada_pct=(val(C["exterior"]["spread_wise"], contexto="wise")
                     + val(C["exterior"]["iof_conta"], contexto="iof.conta")),
        saida_pct=IOF_R, adm_aa=IVV, nota="IOF de conta (3,5%), nao de investimento")
    return R

# ── simulacao ─────────────────────────────────────────────────────────────────
def custo_entrada_pct(r, aporte, b3v):
    return (r.corr_fix/aporte) + r.corr_pct + (b3v if r.b3_vista else 0.0) + r.entrada_pct

def custo_saida_pct(r, b3v):
    return r.corr_pct + (b3v if r.b3_vista else 0.0) + r.saida_pct

def simular(r, C, aporte, anos, bruto=None, custodia_absorvida=False, verbose=False):
    """Retorna (patrimonio, custo_total, alertas). Rendimento bruto identico em todas as rotas:
    o objetivo e ISOLAR O CUSTO, nao prever retorno."""
    bruto = bruto if bruto is not None else val(C["macro"]["cdi_aa"], contexto="cdi")
    B3V   = val(C["b3"]["vista_total_pct"], contexto="b3.vista")
    ISEN  = val(C["b3"]["custodia_rv_isencao"], contexto="b3.isencao")
    FX    = C["b3"]["custodia_rv_faixas"]["valor"]
    INTERP= val(C["b3"]["custodia_rv_interpretacao"], contexto="b3.interp")
    TD_C  = val(C["tesouro"]["custodia_aa"], contexto="td.custodia")
    TD_I  = val(C["tesouro"]["isencao_selic"], contexto="td.isencao")

    m_bruto = (1+bruto)**(1/12) - 1
    pat = custo = 0.0
    alertas = []
    e_pct = custo_entrada_pct(r, aporte, B3V)
    for _ in range(anos*12):
        c = e_pct * aporte
        if c >= aporte:                                  # K-08.3
            alertas.append(f"custo de entrada >= aporte: rota inviavel a R${aporte}")
            c = aporte
        pat += aporte - c; custo += c
        pat *= (1 + m_bruto)
        if r.adm_aa:
            t = pat*((1+r.adm_aa)**(1/12)-1); pat -= t; custo += t
        if r.custodia_rv and not custodia_absorvida:
            t = custodia_rv_aa(pat, FX, ISEN, INTERP)/12; pat -= t; custo += t
        if r.custodia_td:
            base = max(0.0, pat-TD_I) if r.td_isento else pat
            t = base*((1+TD_C)**(1/12)-1); pat -= t; custo += t
    # K-06: perna de saida, cobrada uma vez sobre o patrimonio final
    s_pct = custo_saida_pct(r, B3V)
    saida = pat * s_pct
    return pat - saida, custo + saida, alertas

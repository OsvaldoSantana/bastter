# -*- coding: utf-8 -*-
"""
Fatores de risco brasileiros — NEFIN/FEA-USP. Fecha a pendencia 19.

Por que este modulo existe:
  Bater o Ibovespa nao e evidencia de nada. O Ibovespa e um indice por VOLUME, com
  concentracao setorial alta, e superar um indice concentrado pode ser apenas
  exposicao a fatores conhecidos — tamanho, valor, momento, iliquidez. A afirmacao
  que importa e ALFA CONTRA UM MODELO DE FATORES LOCAL, e ela e qualitativamente
  diferente. Sem isto, todo backtest deste projeto herda o defeito D-1 que a
  auditoria da literatura apontou: benchmark CAPM ou Ibovespa puro.

METODOLOGIA DA FONTE (NEFIN_methodology.pdf, lida em 04/09/2026):
  elegibilidade  acao mais negociada da firma; negociada em >80% dos pregoes do ano
                 t-1 com volume > R$500.000/dia; listada antes de dezembro de t-1.
                 E um filtro de LIQUIDEZ forte: os fatores nao sao contaminados por
                 microcaps que ninguem consegue negociar. Isso os torna mais
                 realistas que os fatores americanos padrao, e menos extremos.
  construcao     tercis EXTREMOS, retorno IGUALMENTE PONDERADO, long-short.
                 SMB e HML: reordenados em JANEIRO, com dados de dezembro e de JUNHO
                 de t-1 — ou seja, a defasagem contabil ja esta embutida na fonte.
                 WML e IML: reordenados TODO MES.
  mercado        value-weighted de todas as elegiveis, menos o CDI.
  livre de risco Swap DI de 30 dias.

CONSEQUENCIA DE ENGENHARIA que o numero sozinho nao mostra:
  WML gira 12 vezes por ano; HML, uma. Comparar os premios brutos dos dois e
  comparar coisas com custo de execucao completamente diferente — e nenhum dos dois
  e liquido de nada. E por isso que `momento_12_1_v1` no pre-registro tem
  `obrigatorio: custo_fiscal_explicito`.
"""
from __future__ import annotations
import os, hashlib
import numpy as np, pandas as pd
import ambiente

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(AQUI, "dados", "nefin_factors.csv")
FATORES = ["Rm_minus_Rf", "SMB", "HML", "WML", "IML"]

class FonteAusente(Exception):
    """A fonte de fatores nao esta disponivel. O backtest NAO roda sem benchmark."""

def hash_fonte(path=None):
    p = path or ARQUIVO
    if not os.path.exists(p): raise FonteAusente(p)
    with open(p, "rb") as f: return hashlib.sha256(f.read()).hexdigest()[:12]

def carregar_diario(path=None):
    p = path or ARQUIVO
    if not os.path.exists(p):
        raise FonteAusente(
            f"{p} nao encontrado. Sem os fatores do NEFIN nao ha benchmark valido: "
            f"alfa contra o Ibovespa puro e o achado D-1 da auditoria da literatura.")
    d = pd.read_csv(p, index_col=0, parse_dates=["Date"])
    faltando = [c for c in FATORES + ["Risk_Free"] if c not in d.columns]
    if faltando: raise FonteAusente(f"colunas ausentes na fonte: {faltando}")
    return d.sort_values("Date").reset_index(drop=True)

def mensal(d=None):
    """Compoe os retornos diarios em mensais. Meses PARCIAIS nas pontas sao mantidos
    e marcados — o ultimo mes da serie quase sempre e incompleto."""
    d = carregar_diario() if d is None else d
    d = d.copy(); d["ym"] = d.Date.dt.to_period("M")
    m = d.groupby("ym")[FATORES + ["Risk_Free"]].apply(lambda g: (1 + g).prod() - 1)
    m["n_dias"] = d.groupby("ym").size()
    return m

def premios(m=None, minimo_dias=15):
    """Media, desvio e t de cada fator. Meses com menos de `minimo_dias` pregoes
    saem: um mes de 2 dias nao e uma observacao mensal."""
    m = mensal() if m is None else m
    m = m[m.n_dias >= minimo_dias]
    out = {}
    for f in FATORES:
        x = m[f]
        t = x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
        out[f] = dict(media_am=x.mean(), dp_am=x.std(ddof=1), t=t, n=len(x),
                      anualizado=(1 + x.mean())**12 - 1, pct_positivos=(x > 0).mean())
    return out

def premio_de_mercado(m=None, minimo_dias=15):
    """O premio de risco de ACOES no Brasil — mercado menos CDI, composto.

    Este numero e o mais importante que a fonte entrega, e nao aparece em nenhum
    dos documentos de escopo: ele calibra a fracao em renda variavel, que hoje e
    uma PREFERENCIA DECLARADA e nao uma consequencia de dado nenhum."""
    m = mensal() if m is None else m
    m = m[m.n_dias >= minimo_dias]
    rm = m.Rm_minus_Rf + m.Risk_Free
    anos = len(m) / 12
    cagr_acoes = (1 + rm).prod()**(1/anos) - 1
    cagr_cdi   = (1 + m.Risk_Free).prod()**(1/anos) - 1
    t = m.Rm_minus_Rf.mean() / (m.Rm_minus_Rf.std(ddof=1) / np.sqrt(len(m)))
    return dict(cagr_acoes=cagr_acoes, cagr_cdi=cagr_cdi,
                premio_aa=cagr_acoes - cagr_cdi, t=t, meses=len(m), anos=anos)

def janelas_moveis(anos=10, m=None, minimo_dias=15):
    """Em quantas janelas de N anos a bolsa perdeu do CDI.

    Uma media de 25 anos esconde o que o investidor de fato viveu. Esta funcao
    responde a pergunta que o aporte mensal faz: se eu tivesse comecado em qualquer
    ano, o que teria acontecido?"""
    m = mensal() if m is None else m
    m = m[m.n_dias >= minimo_dias].copy()
    m.index = m.index.to_timestamp()
    rm = m.Rm_minus_Rf + m.Risk_Free
    out = []
    for y in range(m.index.year.min(), m.index.year.max() - anos + 2):
        sl = slice(str(y), str(y + anos - 1))
        if len(m[sl]) < anos * 12 * 0.9: continue
        a = (1 + rm[sl]).prod()**(1/anos) - 1
        b = (1 + m.Risk_Free[sl]).prod()**(1/anos) - 1
        out.append(dict(inicio=y, fim=y+anos-1, acoes_aa=a, cdi_aa=b, acoes_venceu=a > b))
    return out

def alfa_contra_fatores(retornos_mensais, m=None, modelo=("Rm_minus_Rf","SMB","HML","WML","IML")):
    """Regressao do excesso de retorno da estrategia sobre os fatores. `alfa` e o
    que sobra — e e a unica afirmacao que vale a pena fazer sobre uma estrategia.

    retornos_mensais: Series indexada por Period('M') com o retorno BRUTO mensal da
    estrategia. O excesso e calculado aqui, contra o Risk_Free da propria fonte."""
    m = mensal() if m is None else m
    df = pd.DataFrame({"r": retornos_mensais}).join(m, how="inner")
    if len(df) < 24:
        raise ValueError(f"{len(df)} meses em comum: poucos para estimar alfa")
    y = (df.r - df.Risk_Free).values
    X = np.column_stack([np.ones(len(df))] + [df[f].values for f in modelo])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    gl = len(y) - X.shape[1]
    s2 = resid @ resid / gl
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - (resid @ resid) / (((y - y.mean())**2).sum())
    nomes = ["alfa"] + list(modelo)
    return dict(
        coef=dict(zip(nomes, beta)), erro_padrao=dict(zip(nomes, se)),
        t=dict(zip(nomes, beta/se)), r2=r2, meses=len(df), gl=gl,
        alfa_am=beta[0], alfa_aa=(1+beta[0])**12 - 1, t_alfa=beta[0]/se[0],
        fonte_hash=hash_fonte(),
        # P-15. O sha256 da serie diz de que DADO o numero saiu; o selo diz em que
        # AMBIENTE ele foi calculado. Sem os dois, "reproduzivel" e meia afirmacao:
        # este alfa vem de numpy.linalg.lstsq, e lstsq e uma implementacao, nao um
        # teorema. `reproduz_o_registrado` False nao invalida o numero — diz que ele
        # e um numero NOVO, e nao a conferencia de um antigo.
        ambiente=ambiente.selo(),
        nota="alfa NAO significativo e o resultado esperado. A hipotese nula e que a "
             "estrategia e exposicao a fatores conhecidos, nao habilidade.")

if __name__ == "__main__":
    d = carregar_diario(); m = mensal(d)
    print("="*88)
    print("FATORES NEFIN — VERIFICACAO CONTRA A FONTE PRIMARIA")
    print("="*88)
    print(f"arquivo: dados/nefin_factors.csv (sha256 {hash_fonte()})")
    print(f"periodo: {d.Date.min().date()} a {d.Date.max().date()} · {len(d)} pregoes\n")
    pr = premios(m)
    print(f"{'fator':<14}{'media a.m.':>12}{'t':>7}{'dp a.m.':>10}"
          f"{'anualizado':>12}{'meses>0':>10}")
    for f, v in pr.items():
        print(f"{f:<14}{v['media_am']*100:>11.3f}%{v['t']:>7.2f}{v['dp_am']*100:>9.2f}%"
              f"{v['anualizado']*100:>11.2f}%{v['pct_positivos']*100:>9.1f}%")
    pm = premio_de_mercado(m)
    print(f"\nPREMIO DE RISCO DE ACOES ({pm['anos']:.1f} anos)")
    print(f"   acoes {pm['cagr_acoes']:.2%} a.a. · CDI {pm['cagr_cdi']:.2%} a.a. "
          f"· premio {pm['premio_aa']:.2%} a.a. · t = {pm['t']:.2f}")
    jm = janelas_moveis(10, m)
    perdeu = [j for j in jm if not j["acoes_venceu"]]
    print(f"\nJANELAS MOVEIS DE 10 ANOS: {len(perdeu)} de {len(jm)} em que a bolsa PERDEU do CDI")
    for j in jm:
        marca = "  <- perdeu do CDI" if not j["acoes_venceu"] else ""
        print(f"   {j['inicio']}-{j['fim']}: acoes {j['acoes_aa']:+6.2%} a.a. "
              f"x CDI {j['cdi_aa']:+6.2%} a.a.{marca}")

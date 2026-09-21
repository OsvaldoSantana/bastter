#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-88 -- a dependencia serial que o bootstrap de 18/09 supunha nao existir.

A LIMITACAO QUE ELE FECHA, citada do `CLAUDE.md` (18/09/2026):

    "Entra um limite novo: o bootstrap reamostra **meses independentes** -- se houver
     dependencia serial, o corte medido esta **subestimado**, na mesma direcao do achado.
     Medir isso pede *block bootstrap*, e nao esta feito."

Esta medido. **A previsao estava certa**, e o instrumento que a confirma tem um controle
embutido, sem o qual ela nao teria sido confirmada -- ver DEGENERACAO abaixo.

O QUE E MEDIDO, em tres partes:

  1. **Existe dependencia?** Autocorrelacao e Ljung-Box(12) do fator bruto e do RESIDUO da
     regressao -- o residuo e o que importa, porque e a serie que o bootstrap reamostra.
     HML: LB p = **0,031**. SMB: p = **0,166**. *Um tem, o outro nao* -- e e isso que da o
     controle.
  2. **O corte muda?** Moving block bootstrap circular, com L de 1 a 24, quatro sementes
     cada. `L=1` reproduz o bootstrap registrado (e o teste exige que reproduza **3,1473**,
     o numero do `CLAUDE.md`).
  3. **A mudanca e sinal ou ruido?** O desvio entre sementes vai ao lado de cada corte.
     Diferenca menor que o desvio nao e achado -- foi assim que o m=8 ficou
     `NAO_CONFIRMADO` em 18/09.

A DEGENERACAO, e ela e a razao de o controle existir. Com n=306, `L=24` da **13 blocos
distintos** por replicacao. O bootstrap perde poder de reamostragem e o corte CAI -- e cai
por artefato do metodo, nao por menos dependencia. Sem o controle eu teria lido a queda em
L>=12 como "a dependencia nao importa", que e a conclusao errada pelo motivo errado.

    **O SMB e o controle certo porque ele tem a mesma n, a mesma k e o mesmo procedimento,
    e NAO tem dependencia serial.** O que sobrar de diferenca entre os dois e a dependencia.
    Medido: o corte do SMB CAI com L (-2,6% a -7,0%) e o do HML SOBE (+5,8% a +3,4%).
    **Sinais opostos** -- e e por isso que a limitacao fecha em vez de ficar ambigua.

O QUE ESTE MODULO NAO FAZ (P5):
  - **nao escolhe um L.** A P-88 e explicita: *"o que falta e escolher o comprimento do
    bloco com medicao de sensibilidade, e nao por convencao -- senao troca-se uma suposicao
    tabelada por outra"*. Ele devolve a FAIXA, e a conclusao nao depende de um L;
  - **nao usa Romano-Wolf.** So a marginal com Bonferroni medido, porque o
    `alocacao/multiplicidade.py` nao estava disponivel na sessao em que isto foi escrito.
    Integrar `corte_*_por_bloco` ali e o passo seguinte, e ai o numero absoluto passa a
    valer para as duas correcoes;
  - **nao corrige a degeneracao dentro do numero.** O efeito liquido estimado pela diferenca
    HML-SMB supoe que o artefato e o mesmo nas duas series -- plausivel (mesma n, mesma k,
    mesmo procedimento) e NAO medido. `NAO_CONFIRMADO` para o numero corrigido; MEDIDO para
    o sinal e para a faixa bruta.
"""
from __future__ import annotations
import argparse
import os
import sys
from math import erfc, sqrt

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "alocacao"))
import backtest_h1_h3 as B  # noqa: E402

M_ORCADO, ALFA = 13, 0.05
REPETICOES = 10_000
# Quatro sementes por L. Em 18/09 doze sementes deram 3,107 +- 0,075 para o iid; quatro
# bastam para separar as diferencas medidas aqui (0,08 a 0,20) do ruido (~0,05).
SEMENTES = tuple(B.SEMENTE + i for i in range(4))
# Faixa INFORMATIVA: >= 51 blocos distintos por replicacao com n=306. Acima de L=8 a
# contagem cai para <=38 e o corte passa a se mover por degeneracao -- ver o docstring.
L_INFORMATIVO = (2, 3, 4, 6, 8)
CORTE_IID_REGISTRADO = 3.1473      # CLAUDE.md, 18/09, m=13


def desenho(alvo, d):
    """(y, X) com a MESMA construcao de `alfa_contra_os_demais` -- a assinatura
    pre-registrada. Nao reimplementa a regressao: o teste exige que o t observado
    reproduza o registrado, e e isso que prende as duas na mesma conta."""
    outros = [f for f in B.FATORES if f != alvo]
    y = d[alvo].values.astype(float)
    X = np.column_stack([np.ones(len(d))] + [d[c].values.astype(float) for c in outros])
    return y, X


def alfa_se(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    gl = len(y) - X.shape[1]
    return b[0], float(np.sqrt(np.diag((r @ r / gl) * np.linalg.inv(X.T @ X)))[0])


def residuo(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ b


def autocorrelacao(s, ate=12):
    s = s - s.mean()
    return [float(np.corrcoef(s[:-h], s[h:])[0, 1]) for h in range(1, ate + 1)]


def ljung_box(rho, n):
    """(Q, p). Chi2 por Wilson-Hilferty, para nao trazer o scipy -- a P-15 fecha a faixa
    de versoes e a impressao do ambiente e `7565df1381e2c1ed`. Mesma decisao da
    `multiplicidade.py`, que implementou a t de Student a mao pelo mesmo motivo."""
    k = len(rho)
    q = n * (n + 2) * sum(rho[h - 1] ** 2 / (n - h) for h in range(1, k + 1))
    z = ((q / k) ** (1 / 3) - (1 - 2 / (9 * k))) / sqrt(2 / (9 * k))
    return q, 0.5 * erfc(z / sqrt(2))


def indices(rng, n, L):
    """Moving block bootstrap CIRCULAR. `L=1` e o iid do `bootstrap_t` registrado.

    Circular e nao truncado porque so assim `n` fica constante: descartar as pontas mudaria
    o tamanho da amostra junto com o comprimento do bloco, e ai duas coisas variam ao mesmo
    tempo e nenhuma e medida."""
    if L == 1:
        return rng.integers(0, n, n)
    nb = -(-n // L)
    ini = rng.integers(0, n, nb)
    return ((ini[:, None] + np.arange(L)[None, :]).ravel() % n)[:n]


def corte(y, X, L, semente, m=M_ORCADO, n_rep=REPETICOES):
    """Quantile 1-alfa/m de |t| CENTRADO. Centrado = distribuicao sob a nula."""
    a_obs, _ = alfa_se(y, X)
    rng = np.random.default_rng(semente)
    n = len(y)
    t = np.empty(n_rep)
    for i in range(n_rep):
        ix = indices(rng, n, L)
        a, se = alfa_se(y[ix], X[ix])
        t[i] = (a - a_obs) / se
    return float(np.quantile(np.abs(t), 1 - ALFA / m))


def dispersao(y, X, L, semente, n_rep=REPETICOES):
    """Desvio padrao do |t| CENTRADO reamostrado -- o estimador DIRETO do que a dependencia
    serial faz, e o unico estavel com poucas repeticoes.

    POR QUE ELE EXISTE, e e um defeito do meu primeiro teste. Eu afiro o SINAL do achado com
    1.500 repeticoes, para o teste rodar em segundos -- e usei o quantile `1-alfa/13`, que
    vive a 0,385% da ponta: com 1.500 amostras sao ~6 observacoes decidindo o numero, e ele
    oscila o bastante para o teste falhar com o achado correto.

    **O `CLAUDE.md` ja dizia isso em 18/09** -- *"com 10.000 repeticoes o quantil 1 - alfa/13
    vive na ponta da reamostragem"* -- e eu reintroduzi o problema no teste que escrevi para
    guardar o achado. Regra escrita nao impede a reincidencia; o que impede e medir.

    Dependencia serial infla a VARIANCIA da estatistica; o quantil e consequencia. Aferir a
    causa com 1.500 e estavel, e o quantil registrado fica no teste que usa 10.000."""
    a_obs, _ = alfa_se(y, X)
    rng = np.random.default_rng(semente)
    m = len(y)
    t = np.empty(n_rep)
    for i in range(n_rep):
        ix = indices(rng, m, L)
        aa, se = alfa_se(y[ix], X[ix])
        t[i] = (aa - a_obs) / se
    return float(np.std(t))


def blocos_distintos(n, L):
    return n if L == 1 else -(-n // L)


def medir(alvo, d, Ls, n_rep=REPETICOES):
    y, X = desenho(alvo, d)
    fora = {}
    for L in Ls:
        cs = [corte(y, X, L, s, n_rep=n_rep) for s in SEMENTES]
        fora[L] = {"media": float(np.mean(cs)), "desvio": float(np.std(cs)),
                   "min": min(cs), "max": max(cs),
                   "blocos": blocos_distintos(len(d), L)}
    return fora


def relatorio(Ls=(1, 2, 3, 4, 6, 8, 12, 18, 24), n_rep=REPETICOES, saida=sys.stdout):
    d = B.amostra()
    n = len(d)
    print(f"P-88 · block bootstrap · {n} meses · m={M_ORCADO} · {n_rep:,} repeticoes · "
          f"{len(SEMENTES)} sementes\n", file=saida)

    print("1. EXISTE DEPENDENCIA SERIAL?  (erro padrao de cada rho = "
          f"{1/sqrt(n):.4f})", file=saida)
    lb = {}
    for alvo in ("HML", "SMB"):
        y, X = desenho(alvo, d)
        for nome, s in ((f"{alvo} bruto", y), (f"{alvo} residuo", residuo(y, X))):
            rho = autocorrelacao(s)
            _q, p = ljung_box(rho, n)
            lb[nome] = p
            print(f"   {nome:16} rho1={rho[0]:+.3f} rho2={rho[1]:+.3f} "
                  f"rho3={rho[2]:+.3f}   Ljung-Box(12) p={p:.3f}", file=saida)
    print("   O RESIDUO e o que importa: e a serie que o bootstrap reamostra.\n", file=saida)

    res = {a: medir(a, d, Ls, n_rep) for a in ("HML", "SMB")}
    base = {a: res[a][1]["media"] for a in res}
    t_hml = B.alfa_contra_os_demais("HML", d)[1]
    print("2. O CORTE MUDA?   HML tem dependencia · SMB e o CONTROLE (nao tem)",
          file=saida)
    print(f"   {'L':>3} {'blocos':>7} | {'HML':>8} {'sd':>6} {'vs iid':>8} "
          f"{'folga':>8} | {'SMB':>8} {'vs iid':>8} | {'liquido':>8}", file=saida)
    for L in Ls:
        h, s = res["HML"][L], res["SMB"][L]
        vh, vs = h["media"] / base["HML"] - 1, s["media"] / base["SMB"] - 1
        marca = " *" if L in L_INFORMATIVO else ""
        print(f"   {L:>3} {h['blocos']:>7} | {h['media']:>8.4f} {h['desvio']:>6.4f} "
              f"{vh:>+7.1%} {t_hml-h['media']:>+8.4f} | {s['media']:>8.4f} {vs:>+7.1%} "
              f"| {vh-vs:>+7.1%}{marca}", file=saida)
    print("   * faixa informativa: >= 38 blocos distintos. Abaixo disso o corte cai por\n"
          "     DEGENERACAO do reamostrador, nao por menos dependencia -- e o controle e o\n"
          "     que separa as duas coisas.", file=saida)
    return res, lb, t_hml


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--repeticoes", type=int, default=REPETICOES)
    p.add_argument("--rapido", action="store_true", help="L reduzido, para conferir")
    a = p.parse_args(argv)
    Ls = (1, 3, 6) if a.rapido else (1, 2, 3, 4, 6, 8, 12, 18, 24)
    relatorio(Ls, a.repeticoes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

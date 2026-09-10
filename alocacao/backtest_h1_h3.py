# -*- coding: utf-8 -*-
"""H1 (hml_puro_v1), H2 (dy_alto_v1) e H3 (tamanho_smb_v1) contra os fatores NEFIN.

Executa o que o pre-registro de politica.yaml define, e SO isso. Rodar de novo tem
de dar o mesmo numero: a semente do bootstrap e fixa e a fonte tem hash publicado.

DUAS ARMADILHAS, ambas capazes de inverter o veredito sem levantar erro:

  1. NAO usar fatores.alfa_contra_fatores() aqui. Ela subtrai o Risk_Free, porque
     foi escrita para uma carteira COMPRADA. Os fatores do NEFIN sao long-short
     auto-financiados: descontar o CDI de um spread cobra um custo que a carteira
     nao tem. No HML isso troca +0,766% (t=+2,94) por -0,178% (t=-0,68).

  2. "Alfa contra os DEMAIS fatores" exclui o proprio fator. Incluir-se da R2 = 1
     por construcao — tautologia, nao teste.
"""
from __future__ import annotations
import numpy as np
import fatores as F

FATORES = ["Rm_minus_Rf", "SMB", "HML", "WML", "IML"]
SEMENTE = 20260905
MIN_DIAS = 15          # mes com menos pregoes que isso nao e observacao mensal

def amostra():
    m = F.mensal()
    return m[m.n_dias >= MIN_DIAS]

def alfa_contra_os_demais(alvo, d):
    """(alfa_mensal, t). Sem subtrair Risk_Free — ver armadilha 1 no docstring."""
    outros = [f for f in FATORES if f != alvo]
    y = d[alvo].values
    X = np.column_stack([np.ones(len(d))] + [d[c].values for c in outros])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    gl = len(y) - X.shape[1]
    se = np.sqrt(np.diag((r @ r / gl) * np.linalg.inv(X.T @ X)))
    return b[0], b[0] / se[0]

def meses_que_carregam(alvo, d, k=12):
    """Alfa depois de remover os k meses de maior influencia positiva.

    Um alfa que morre ao perder 4% da amostra e uma aposta em poucos meses, nao um
    premio. O CONTROLE importa tanto quanto o teste: se todo fator morresse igual,
    a medida nao diria nada. O WML nao morre."""
    a0, _ = alfa_contra_os_demais(alvo, d)
    infl = np.array([alfa_contra_os_demais(alvo, d.drop(d.index[i]))[0] - a0
                     for i in range(len(d))])
    return alfa_contra_os_demais(alvo, d.drop(d.index[np.argsort(infl)[:k]]))

def bootstrap_t(alvo, d, n=10_000, semente=SEMENTE):
    rng = np.random.default_rng(semente)
    idx = np.arange(len(d))
    ts = [alfa_contra_os_demais(alvo, d.iloc[rng.choice(idx, len(idx), replace=True)])[1]
          for _ in range(n)]
    return np.array(ts)

if __name__ == "__main__":
    d = amostra()
    print(f"fonte sha256[:12] = {F.hash_fonte()} | {len(d)} meses "
          f"({d.index.min()} a {d.index.max()})\n")
    for alvo in ("HML", "SMB"):
        a, t = alfa_contra_os_demais(alvo, d)
        ak, tk = meses_que_carregam(alvo, d)
        ts = bootstrap_t(alvo, d)
        print(f"{alvo}: alfa={a*100:+.3f}% a.m. ({(1+a)**12-1:+.2%} a.a.) t={t:+.2f}")
        print(f"     sem os 12 meses de maior influencia: alfa={ak*100:+.3f}% t={tk:+.2f}")
        print(f"     bootstrap P(t>1,96) = {100*(ts>1.96).mean():.0f}%\n")
    print("H2 (dy_alto_v1): NAO EXECUTAVEL — a serie nao tem fator de dividend yield.")
    print("  colunas:", [c for c in d.columns if c != "n_dias"])

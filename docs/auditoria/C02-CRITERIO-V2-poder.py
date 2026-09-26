# -*- coding: utf-8 -*-
"""P-115: probabilidade de o IC 95% NAO caber na faixa de equivalencia, aproximacao normal.
Da o sigma_max de cada faixa (reprovar ajuste perfeito <= 10%) e a tabela da secao 4.1."""
from math import erf, sqrt

Z = 1.959963985


def phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def nao_cabe(k, s, lo, hi):
    a, b = lo + Z * s, hi - Z * s
    return 1.0 if a > b else 1 - (phi((b - k) / s) - phi((a - k) / s))


def sigma_max(ks, lo, hi, alvo=0.10):
    L, H = 1e-6, 1.0
    for _ in range(200):
        m = (L + H) / 2
        L, H = (m, H) if max(nao_cabe(k, m, lo, hi) for k in ks) <= alvo else (L, m)
    return L


S21 = {"jcp": (1.044 - 0.859) / 2 / Z, "div": (1.240 - 1.092) / 2 / Z}  # iid, 2021-2025
for nome, ks, lo, hi, s in [("JCP [0.90,1.10]", [1.0], .90, 1.10, S21["jcp"]),
                            ("JCP [0.85,1.15]", [1.0], .85, 1.15, S21["jcp"]),
                            ("DIV [0.85,1.35]", [1.0, 1.176], .85, 1.35, S21["div"])]:
    sm = sigma_max(ks, lo, hi)
    print(nome, "sigma_max=%.4f" % sm,
          "| nao cabe @s21:", ["%.4f" % nao_cabe(k, s, lo, hi) for k in ks],
          "| @sigma_max:", ["%.4f" % nao_cabe(k, sm, lo, hi) for k in ks],
          "| M4 (1,15) cabe @sigma_max: %.4f" % (1 - nao_cabe(1.15, sm, lo, hi)))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conta JCP e dividendo por ano no silver, sem ler preco -- e aplica a regra da janela.

POR QUE (P-115, secao 9 do `docs/auditoria/C02-CRITERIO-V2-PREREGISTRO.md`, revisao 4). O
K2 do JCP provavelmente sai sem poder em 2016-2020. A janela pode crescer para tras
(2013-2020 no maximo), e o tamanho so pode ser escolhido pelo n, nunca pelo preco: escolher
olhando o preco seria escolher pelo resultado.

O QUE LE: do silver, SO `cod`, `type_stock`, `tipo`, `data_ex` e `ultimo_dia_com_direito`.
Valor, preco de vespera, ratio e fator nao sao lidos -- `ler()` projeta a linha nessas cinco
colunas antes de qualquer outra coisa, e o teste envenena as outras.

A UNIDADE e a dos 819 de 2021-2025 (`docs/auditoria/C02-JANELA-2021-2025.md`), ate onde o
silver sozinho diz: o PAPEL-DIA (`cod` + `type_stock` + data) com `JRS CAP PROPRIO` e sem
`DIVIDENDO` nem evento de quantidade no mesmo papel e dia ("so JCP", "dia limpo"). O papel-dia
junta a mesma linha vinda das duas esteiras (A-13). A data e a `data_ex`; sem ela, o ano sai
do `ultimo_dia_com_direito`, e `pela_data_com` conta quantos.

O QUE NAO MEDE (P5): se o papel tem preco no dia e na vespera -- isso exige o COTAHIST. O n
daqui e um TETO do n que entra no K2, e a regra e otimista por isso.

A SAIDA e so contagem (P-136): nenhum preco, nenhum valor.

  py -3.11 auditoria/c02_contar_n.py data/silver/eventos_silver_<...>.csv
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
import os
import sys
from collections import defaultdict
from typing import Iterable, Iterator, Mapping

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "fase0"))
import refinar  # noqa: E402  -- a lista de tipos e uma so (N-01)

LIDAS = ("cod", "type_stock", "tipo", "data_ex", "ultimo_dia_com_direito")
JCP = "JRS CAP PROPRIO"
DIVIDENDO = "DIVIDENDO"
QUANTIDADE = frozenset(refinar.TIPOS_DE_QUANTIDADE)

# a regra da secao 9: os numeros sao os da secao 4 (2021-2025 e sigma_max do K2)
SIGMA_2021_2025 = 0.0472
N_2021_2025 = 819
SIGMA_MAX_K2 = 0.0416
FOLGA = 0.8
N_MIN = math.ceil(N_2021_2025 * (SIGMA_2021_2025 / (FOLGA * SIGMA_MAX_K2)) ** 2)
CANDIDATAS = ((2016, 2020), (2015, 2020), (2014, 2020), (2013, 2020))
PADRAO = CANDIDATAS[0]


class SilverIncompleto(ValueError):
    pass


def ler(caminho: str) -> Iterator[dict[str, str]]:
    """Cada linha do silver projetada nas cinco colunas de `LIDAS`, e so nelas."""
    with open(caminho, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        cab = next(r)
        falta = [c for c in LIDAS if c not in cab]
        if falta:
            raise SilverIncompleto(f"{caminho}: faltam as colunas {falta}")
        idx = [cab.index(c) for c in LIDAS]
        for row in r:
            yield {c: row[i] for c, i in zip(LIDAS, idx)}


def contar(linhas: Iterable[Mapping[str, str]]) -> dict[int, dict[str, int]]:
    """{ano: {jcp, so_jcp_limpo, div, so_div_limpo, pela_data_com}}, por papel-dia."""
    tipos: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    ano_de: dict[tuple[str, str, str], tuple[int, bool]] = {}
    for ln in linhas:
        data = ln["data_ex"]
        pela_data_com = not data
        data = data or ln["ultimo_dia_com_direito"]
        k = (ln["cod"], ln["type_stock"], data)
        tipos[k].add(ln["tipo"])
        ano_de[k] = (int(data[:4]), pela_data_com)
    out: dict[int, dict[str, int]] = {}
    for k, ts in tipos.items():
        ano, pela = ano_de[k]
        c = out.setdefault(ano, dict(jcp=0, so_jcp_limpo=0, div=0, so_div_limpo=0,
                                     pela_data_com=0))
        limpo = not (ts & QUANTIDADE)
        if JCP in ts:
            c["jcp"] += 1
            c["so_jcp_limpo"] += int(limpo and DIVIDENDO not in ts)
        if DIVIDENDO in ts:
            c["div"] += 1
            c["so_div_limpo"] += int(limpo and JCP not in ts)
        if ts & {JCP, DIVIDENDO}:
            c["pela_data_com"] += int(pela)
    return out


def janela(contagem: Mapping[int, Mapping[str, int]]) -> dict[str, object]:
    """A menor candidata com n_JCP >= N_MIN; sem nenhuma, 2016-2020 com `atende=False`."""
    def n(ini, fim):
        return sum(contagem.get(a, {}).get("so_jcp_limpo", 0) for a in range(ini, fim + 1))
    for ini, fim in CANDIDATAS:
        if n(ini, fim) >= N_MIN:
            return dict(ini=ini, fim=fim, n=n(ini, fim), atende=True)
    return dict(ini=PADRAO[0], fim=PADRAO[1], n=n(*PADRAO), atende=False)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("silver")
    a = ap.parse_args(argv)
    with open(a.silver, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    c = contar(ler(a.silver))
    print(f"silver {os.path.basename(a.silver)} sha256 {sha}")
    print(f"{'ano':>6}{'jcp':>8}{'so_jcp_limpo':>14}{'div':>8}{'so_div_limpo':>14}"
          f"{'pela_data_com':>15}")
    for ano in sorted(c):
        x = c[ano]
        print(f"{ano:>6}{x['jcp']:>8}{x['so_jcp_limpo']:>14}{x['div']:>8}"
              f"{x['so_div_limpo']:>14}{x['pela_data_com']:>15}")
    j = janela(c)
    print(f"RESUMO regra da secao 9: n_min {N_MIN}; janela {j['ini']}-{j['fim']}, "
          f"n {j['n']}, " + ("atende" if j["atende"] else
                              "NENHUMA atende: NAO_CONFIRMADO provavel no K2, declarado"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

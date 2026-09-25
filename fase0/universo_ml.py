#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""universo_ml.py -- o universo da secao 2 do pre-registro ML, mes a mes, e a cobertura de
documentos da emenda 1. P-143 e P-132 (25/09/2026).

A PONTE, e por que ela e esta (CV-05, P-143). O COTAHIST fala ticker; os documentos da CVM
falam `CD_CVM`. O FCA so traz codigo de negociacao a partir de 2018. A ponte medida aqui:

    CODISI do COTAHIST  --[4 caracteres depois de "BR"]-->  codigo do emissor
    codigo do emissor   --[EMISSOR.TXT do banco de ISIN da B3]-->  CNPJ
    CNPJ                --[indices DFP/ITR da CVM, cad_cia_aberta]-->  CD_CVM e DT_RECEB

O banco de ISIN veio da pagina `sistemaswebb3-listados.b3.com.br/isinPage/` (o endereco do
download esta no JS dela: `GetTextDownload/` lista, `GetFileDownload/<btoa(id)>` entrega).

O UNIVERSO, lido da secao 2 da v2: mercado a vista (TPMERC 010), lote padrao (CODBDI 02);
negociado em >= 90% dos pregoes da janela; volume financeiro medio da janela no percentil
>= 50 entre os que passaram; uma classe por empresa. A EMPRESA aqui e o codigo do emissor
do ISIN -- a regra posicional do A-01, que distingue emissora sem nome.

"OS 3 MESES ANTERIORES" TEM DUAS LEITURAS, e a secao 2 nao escolhe: os 3 meses que terminam
na data de decisao (t-2, t-1, t) ou os 3 antes do mes t (t-3, t-2, t-1). Este modulo NAO
escolhe -- mede as duas (`JANELAS`) e o relatorio mostra as duas. Se o mes da emenda
coincidir nas duas, a escolha nao importa para ela; se divergir, e decisao de desenho.

O QUE ELE NAO FAZ (P5): nao casa por nome sozinho. A ponte manual
(`docs/aprendizado/ponte-emissor-cvm.yaml`) foi conferida a mao, linha a linha, pela
sucessao societaria; empresa sem ponte fica listada, com o NOMRES do COTAHIST, e conta como
SEM documento (emenda 1, secao 3, item 2).
"""
from __future__ import annotations

import collections
import csv
import datetime as dt
import io
import os
import statistics
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import calendario  # noqa: E402
import insumo_ml  # noqa: E402

REPO = os.path.dirname(AQUI)
ISINP = os.path.join(REPO, "data", "bronze", "b3", "isin", "dt_captura=2026-09-25", "isinp.zip")
CVM = os.path.join(REPO, "data", "bronze", "cvm")
PONTE_MANUAL = os.path.join(REPO, "docs", "aprendizado", "ponte-emissor-cvm.yaml")
CODBDI_LOTE_PADRAO, TPMERC_A_VISTA = "02", "010"
FRACAO_DE_PREGOES = 0.90         # secao 2: "negociada em >= 90% dos pregoes"
PERCENTIL_DE_VOLUME = 50         # secao 2: "percentil >= 50"
LIMIAR_DA_EMENDA = 0.90          # emenda 1, secao 2 -- escolhido por ele em 25/09
JANELAS = {"t-2..t": (2, 0), "t-3..t-1": (3, 1)}   # (inicio, fim) em meses antes de t


def _mes(d):
    return (d.year, d.month)


def _mes_menos(m, k):
    a, mm = m[0], m[1] - k
    while mm <= 0:
        a, mm = a - 1, mm + 12
    return (a, mm)


def emissor_do_isin(isin):
    """`BRPETRACNPR6` -> `PETR`. None se nao for ISIN brasileiro de 12 posicoes."""
    isin = (isin or "").strip()
    return isin[2:6] if len(isin) == 12 and isin[:2] == "BR" else None


def ler_negocios(registros):
    """{ticker: {data: volume}}, {ticker: (isin, nomres)}, pregoes -- de linhas COTAHIST."""
    p = {k: calendario.pos(k) for k in ("CODBDI", "TPMERC", "CODNEG", "VOLTOT", "CODISI",
                                        "NOMRES")}
    vol, ident, dias = collections.defaultdict(dict), {}, set()
    for raw in registros:
        d = calendario.data_de(raw)
        if d is None:
            continue
        dias.add(d)
        if raw[slice(*p["CODBDI"])] != CODBDI_LOTE_PADRAO or \
                raw[slice(*p["TPMERC"])] != TPMERC_A_VISTA:
            continue
        tk = raw[slice(*p["CODNEG"])].strip()
        vol[tk][d] = int(raw[slice(*p["VOLTOT"])]) / 100
        ident.setdefault(tk, (raw[slice(*p["CODISI"])].strip(),
                              raw[slice(*p["NOMRES"])].strip()))
    return dict(vol), ident, dias


def universo(mes, vol, ident, dias, janela):
    """Os EMISSORES do universo no mes `mes`, pela `janela` de JANELAS."""
    ini, fim = JANELAS[janela]
    meses = {_mes_menos(mes, k) for k in range(fim, ini + 1)}
    pregoes = sorted(d for d in dias if _mes(d) in meses)
    if not pregoes:
        return {}
    ok = {}
    for tk, serie in vol.items():
        n = sum(1 for d in pregoes if d in serie)
        if n >= FRACAO_DE_PREGOES * len(pregoes):
            ok[tk] = sum(serie.get(d, 0.0) for d in pregoes) / len(pregoes)
    if not ok:
        return {}
    corte = statistics.median(ok.values()) if PERCENTIL_DE_VOLUME == 50 else None
    por_emissor = {}
    for tk, v in ok.items():
        if v < corte:
            continue
        em = emissor_do_isin(ident[tk][0]) or f"?{tk}"
        if em not in por_emissor or v > por_emissor[em][1]:
            por_emissor[em] = (tk, v)          # a classe mais liquida da empresa
    return {em: tk for em, (tk, _v) in por_emissor.items()}


def ponte_emissor_cnpj(caminho=ISINP, manual=PONTE_MANUAL):
    """{emissor: cnpj}. O EMISSOR.TXT da B3, e por cima a ponte MANUAL conferida a mao --
    ela vence, porque existe justamente para os codigos trocados ou REAPROVEITADOS depois
    de 2010, em que o EMISSOR.TXT (dono atual do codigo) aponta para outra entidade."""
    with zipfile.ZipFile(caminho) as z:
        texto = z.read("EMISSOR.TXT").decode("utf-8", "replace")
    ponte = {r[0]: r[2] for r in csv.reader(io.StringIO(texto)) if len(r) >= 3 and r[2]}
    if manual:
        import yaml
        with open(manual, encoding="utf-8") as f:
            m = yaml.safe_load(f)
        ponte.update({em: v["cnpj"] for em, v in m["ponte"].items()})
    return ponte


def _digitos(cnpj):
    return "".join(c for c in cnpj if c.isdigit())


def documentos(indices):
    """{cnpj (digitos): menor DT_RECEB} e {cnpj: CD_CVM}, dos indices DFP/ITR."""
    primeiro, cdcvm = {}, {}
    for caminho, membro in indices:
        with zipfile.ZipFile(caminho) as z, z.open(membro) as f:
            for r in csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"), delimiter=";"):
                c = _digitos(r["CNPJ_CIA"])
                d = dt.date.fromisoformat(r["DT_RECEB"])
                if c not in primeiro or d < primeiro[c]:
                    primeiro[c] = d
                cdcvm.setdefault(c, r["CD_CVM"])
    return primeiro, cdcvm


def cadastro(caminho=os.path.join(CVM, "cad", "cad_cia_aberta.csv")):
    """{cnpj (digitos): CD_CVM} do cadastro, canceladas inclusive."""
    with open(caminho, encoding="latin-1") as f:
        return {_digitos(r["CNPJ_CIA"]): r["CD_CVM"]
                for r in csv.DictReader(f, delimiter=";") if r["CD_CVM"]}


def cobertura(mes, univ, decisao, ponte, primeiro_doc, cdcvm):
    """(n, com_cd_cvm, com_documento, sem_ponte[]) no mes."""
    com_id = com_doc = 0
    sem = []
    for em in sorted(univ):
        cnpj = _digitos(ponte.get(em, ""))
        if not cnpj or cnpj not in cdcvm:
            sem.append(em)
            continue
        com_id += 1
        d = primeiro_doc.get(cnpj)
        if d is not None and d <= decisao:
            com_doc += 1
    return len(univ), com_id, com_doc, sem


def mes_da_emenda(serie, limiar=LIMIAR_DA_EMENDA):
    """O primeiro mes com com_documento/n >= limiar (emenda 1, secao 3, item 3)."""
    for mes, (n, _i, doc, _s) in sorted(serie.items()):
        if n and doc / n >= limiar:
            return mes
    return None


def main(argv=None):
    anos = range(2009, 2013)
    t0 = dt.datetime.now()
    regs = []
    for a in anos:
        regs.extend(calendario.registros(insumo_ml.abrir_cotahist(a).caminho))
    vol, ident, dias = ler_negocios(regs)
    ponte = ponte_emissor_cnpj()
    cad = cadastro()
    idx = [(os.path.join(CVM, "dfp", f"dfp_cia_aberta_{a}.zip"), f"dfp_cia_aberta_{a}.csv")
           for a in (2010, 2011, 2012)]
    idx += [(os.path.join(CVM, "itr", f"itr_cia_aberta_{a}.zip"), f"itr_cia_aberta_{a}.csv")
            for a in (2011, 2012)]
    primeiro_doc, cdcvm = documentos(idx)
    cdcvm = {**cad, **cdcvm}
    ultimo = {}
    for d in dias:
        ultimo[_mes(d)] = max(ultimo.get(_mes(d), d), d)
    meses = [(a, m) for a in (2010, 2011, 2012) for m in range(1, 13)]
    sem_ponte = collections.Counter()
    for janela in JANELAS:
        serie = {}
        print(f"\n== janela {janela}")
        print("mes      n  com_CD_CVM  com_doc  cobertura  sem_ponte")
        for mes in meses:
            u = universo(mes, vol, ident, dias, janela)
            serie[mes] = cobertura(mes, u, ultimo[mes], ponte, primeiro_doc, cdcvm)
            n, i, doc, sem = serie[mes]
            for em in sem:
                sem_ponte[(em, ident[u[em]][1] if em in u else "")] += 1
            print(f"{mes[0]}-{mes[1]:02d}  {n:4d}  {i:10d}  {doc:7d}  "
                  f"{(doc / n if n else 0):9.3f}  {len(sem):9d}")
        m = mes_da_emenda(serie)
        print(f"MES DA EMENDA ({janela}): {m[0]}-{m[1]:02d}" if m else
              f"MES DA EMENDA ({janela}): nenhum em 2010-2012")
    print("\nemissores do universo SEM ponte (emissor, NOMRES, meses-janela):")
    for (em, nome), k in sorted(sem_ponte.items()):
        print(f"  {em}  {nome:12s}  {k}")
    print(f"\n# {(dt.datetime.now() - t0).total_seconds():.1f} s", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

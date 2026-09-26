#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-145: a ponte ticker -> CD_CVM para o universo do ML de 2013 a 2019.

A P-143 fechou a ponte de 2010-2012 (190 emissores; 136 ligados pelo EMISSOR.TXT, 50
ausentes dele, 4 codigos reaproveitados -- CV-06) e a ponte manual cobriu 42. O
desenvolvimento do ML vai ate 2019: esta medicao diz quantos emissores de 2013-2019 a ponte
ja liga, quantos precisam de conferencia a mao, e quais.

AS DUAS LEITURAS DA SECAO 2, FIXADAS (decididas por ele em 25/09, `preregistro-ml-v2-emenda-1.md`
secao 6, sha256 publicado `71621ba64c899281`): janela "t-2..t" e volume ">= mediana",
inclusiva -- que e o que `universo_ml.universo` ja faz (so descarta `v < corte`).

OS INSUMOS saem do acervo por `acervo.abrir`, nunca pelo caminho do disco: COTAHIST 2012-2019
pelas versoes FIXADAS do pre-registro (`insumo_ml`), o banco de ISIN na captura de 25/09 (a
mesma da P-143), o cadastro e os indices DFP/ITR na versao vigente, com o sha256 de cada um
impresso na saida (P1). `--conferir-insumos` diz, sem rede e sem segredo, o que falta.

O QUE A SAIDA NAO TEM, de proposito (P-136): preco, volume ou qualquer dado de negociacao da
B3. So contagens, codigos de emissor e o nome resumido -- a saida e commitada num
repositorio publico pelo `medir.yml`.

O QUE ELE NAO FAZ (P5): nao decide a ponte. "Nome diverge" e candidato a conferencia a mao
(20 dos 136 de 2010-2012 divergiam e estavam TODOS certos); "CNPJ sem registro na CVM" e a
forma dos 4 reaproveitados, e so a sucessao conferida a mao diz se e isso.
"""
from __future__ import annotations

import argparse
import collections
import csv
import io
import os
import re
import sys
import unicodedata
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASE0 = os.path.join(RAIZ, "fase0")
if FASE0 not in sys.path:
    sys.path.insert(0, FASE0)
import acervo  # noqa: E402
import calendario  # noqa: E402
import insumo_ml  # noqa: E402
import universo_ml as U  # noqa: E402

ANOS_COTAHIST = tuple(range(2012, 2020))      # t-2 de jan/2013 cai em nov/2012
MESES = tuple((a, m) for a in range(2013, 2020) for m in range(1, 13))
JANELA = "t-2..t"                             # emenda 1, secao 6 -- decisao dele, 25/09
ISIN_VERSAO = "c4654dbd"                      # a captura de 25/09 que a P-143 usou
INSUMOS = (
    [("isin", "isinp.zip", ISIN_VERSAO), ("cad", "cad_cia_aberta.csv", None)]
    + [("dfp", f"dfp_cia_aberta_{a}.zip", None) for a in range(2010, 2020)]
    + [("itr", f"itr_cia_aberta_{a}.zip", None) for a in range(2011, 2020)]
)
# Palavras que nao identificam empresa: sem isto, "CIA" e "SA" casariam quase tudo.
GENERICAS = {"SA", "CIA", "COMPANHIA", "PART", "PARTICIPACOES", "HOLDING", "BRASIL", "BRASILEIRA",
             "DO", "DA", "DE", "DOS", "DAS", "E", "ON", "PN", "NM", "N1", "N2", "EM", "INDUSTRIA",
             "COMERCIO", "S", "A", "LTDA", "GRUPO", "EMPREENDIMENTOS"}
CATEGORIAS = ("MANUAL", "LIGADO_NOME_CONFERE", "LIGADO_NOME_DIVERGE", "CNPJ_SEM_CVM",
              "AUSENTE_DO_ISIN")


def conferir_insumos(repo=None, pins=None):
    """[faltas] -- o que o acervo nao sabe entregar, sem rede: registro e inventario."""
    repo = repo or acervo.raiz_repo()
    faltas = []
    for rec, arq, ver in INSUMOS:
        try:
            acervo._escolher(acervo.versoes(rec, arq, repo), rec, arq, ver)
        except acervo.VersaoDesconhecida as e:
            faltas.append(str(e))
    pins = pins if pins is not None else insumo_ml.carregar_pins()
    for ano in ANOS_COTAHIST:
        pin = (pins.get("cotahist") or {}).get(ano)
        if pin is None:
            faltas.append(f"COTAHIST {ano}: sem pin no pre-registro")
            continue
        vs = acervo.versoes(insumo_ml.RECURSO, pin["arquivo"], repo)
        if not any(v["sha256"] == pin["sha256"] for v in vs):
            faltas.append(f"COTAHIST {ano}: a versao fixada {pin['sha256'][:12]} nao esta "
                          f"no registro nem no inventario")
    return faltas


def tokens(nome):
    """Palavras que identificam a empresa: maiusculas, sem acento, sem as genericas."""
    s = unicodedata.normalize("NFKD", nome or "").encode("ascii", "ignore").decode().upper()
    return {t for t in re.split(r"[^A-Z0-9]+", s) if len(t) >= 3 and t not in GENERICAS}


def classificar(emissores, isin, manual, cdcvm, nomes_cvm, nomres):
    """{emissor: categoria}. `isin` e o EMISSOR.TXT puro ({emissor: cnpj}); `manual` a ponte
    conferida a mao, que vence; `cdcvm` e `nomes_cvm` sao por CNPJ (so digitos)."""
    out = {}
    for em in emissores:
        if em in manual:
            out[em] = "MANUAL"
        elif em not in isin:
            out[em] = "AUSENTE_DO_ISIN"
        else:
            cnpj = U._digitos(isin[em])
            if cnpj not in cdcvm:
                out[em] = "CNPJ_SEM_CVM"
            elif tokens(nomres.get(em, "")) & tokens(nomes_cvm.get(cnpj, "")):
                out[em] = "LIGADO_NOME_CONFERE"
            else:
                out[em] = "LIGADO_NOME_DIVERGE"
    return out


def _ponte_isin(caminho):
    with zipfile.ZipFile(caminho) as z:
        texto = z.read("EMISSOR.TXT").decode("utf-8", "replace")
    return {r[0]: r[2] for r in csv.reader(io.StringIO(texto)) if len(r) >= 3 and r[2]}


def _manual(caminho=U.PONTE_MANUAL):
    import yaml
    with open(caminho, encoding="utf-8") as f:
        return {em: v["cnpj"] for em, v in yaml.safe_load(f)["ponte"].items()}


def _cadastro(caminho):
    """({cnpj: CD_CVM}, {cnpj: 'DENOM_SOCIAL DENOM_COMERC'})."""
    cd, nomes = {}, {}
    with open(caminho, encoding="latin-1") as f:
        for r in csv.DictReader(f, delimiter=";"):
            c = U._digitos(r.get("CNPJ_CIA", ""))
            if r.get("CD_CVM"):
                cd[c] = r["CD_CVM"]
            nomes[c] = f"{r.get('DENOM_SOCIAL', '')} {r.get('DENOM_COMERC', '')}"
    return cd, nomes


def relatorio(serie, classe, nomres, meses_por_emissor, shas):
    """O texto da saida. Recebe contagens e rotulos -- nunca preco nem volume (P-136)."""
    li = ["# P-145 -- ponte ticker -> CD_CVM, universo do ML de 2013 a 2019",
          f"# janela {JANELA}; volume >= mediana (inclusiva); emenda 1, secao 6", "",
          "## insumos (sha256)"]
    li += [f"  {k}  {v}" for k, v in sorted(shas.items())]
    li += ["", "## por mes", "mes      n  com_CD_CVM  com_doc  cobertura  sem_ponte"]
    for mes in sorted(serie):
        n, i, doc, sem = serie[mes]
        li.append(f"{mes[0]}-{mes[1]:02d}  {n:4d}  {i:10d}  {doc:7d}  "
                  f"{(doc / n if n else 0):9.3f}  {len(sem):9d}")
    cont = collections.Counter(classe.values())
    li += ["", "## emissores do universo em algum mes de 2013-2019, por categoria"]
    li += [f"  {c:22s} {cont.get(c, 0):4d}" for c in CATEGORIAS]
    li += ["", "## a conferir a mao (emissor, NOMRES, meses no universo)"]
    for c in ("AUSENTE_DO_ISIN", "CNPJ_SEM_CVM", "LIGADO_NOME_DIVERGE"):
        li.append(f"### {c}")
        li += [f"  {em}  {nomres.get(em, ''):12s}  {meses_por_emissor[em]}"
               for em in sorted(e for e, k in classe.items() if k == c)]
    pior = min(serie, key=lambda m: (serie[m][1] / serie[m][0]) if serie[m][0] else 1)
    n, i, _d, _s = serie[pior]
    li += ["",
           f"RESUMO: {len(classe)} emissores em 2013-2019; "
           f"{cont.get('MANUAL', 0) + cont.get('LIGADO_NOME_CONFERE', 0)} ligados sem conferencia "
           f"pendente; {cont.get('LIGADO_NOME_DIVERGE', 0)} com nome divergente; "
           f"{cont.get('AUSENTE_DO_ISIN', 0) + cont.get('CNPJ_SEM_CVM', 0)} sem ponte automatica",
           f"RESUMO: pior mes {pior[0]}-{pior[1]:02d}, {i}/{n} com CD_CVM "
           f"({(i / n if n else 0):.3f})"]
    return "\n".join(li) + "\n"


def medir():
    shas = {}
    regs = []
    for a in ANOS_COTAHIST:
        leitura = insumo_ml.abrir_cotahist(a)
        shas[f"cotahist {a}"] = leitura.sha256
        regs.extend(calendario.registros(leitura.caminho))
    vol, ident, dias = U.ler_negocios(regs)
    caminhos = {}
    for rec, arq, ver in INSUMOS:
        caminhos[arq] = acervo.abrir(rec, arq, ver, conferir=True)
        shas[f"{rec} {arq}"] = acervo.armazem_mod.sha256(caminhos[arq])
    isin, manual = _ponte_isin(caminhos["isinp.zip"]), _manual()
    ponte = {**isin, **manual}
    cd_cad, nomes_cvm = _cadastro(caminhos["cad_cia_aberta.csv"])
    idx = [(caminhos[arq], arq.replace(".zip", ".csv")) for rec, arq, _v in INSUMOS
           if rec in ("dfp", "itr")]
    primeiro_doc, cdcvm = U.documentos(idx)
    cdcvm = {**cd_cad, **cdcvm}
    ultimo = {}
    for d in dias:
        ultimo[U._mes(d)] = max(ultimo.get(U._mes(d), d), d)
    serie, meses_por_emissor, nomres = {}, collections.Counter(), {}
    for mes in MESES:
        u = U.universo(mes, vol, ident, dias, JANELA)
        serie[mes] = U.cobertura(mes, u, ultimo[mes], ponte, primeiro_doc, cdcvm)
        for em, tk in u.items():
            meses_por_emissor[em] += 1
            nomres[em] = ident[tk][1]
    classe = classificar(sorted(meses_por_emissor), isin, manual, cdcvm, nomes_cvm, nomres)
    return relatorio(serie, classe, nomres, meses_por_emissor, shas)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--conferir-insumos", action="store_true",
                    help="so diz o que falta no acervo, sem rede e sem segredo")
    a = ap.parse_args(argv)
    faltas = conferir_insumos()
    if faltas:
        print("INSUMO AUSENTE do registro e do inventario do acervo:", file=sys.stderr)
        for f in faltas:
            print(f"  {f}", file=sys.stderr)
            if os.environ.get("GITHUB_ACTIONS"):      # vira anotacao na pagina da execucao
                print(f"::error title=insumo ausente::{f}")
        return 1
    if a.conferir_insumos:
        print(f"insumos: {len(INSUMOS) + len(ANOS_COTAHIST)} conhecidos pelo acervo")
        return 0
    sys.stdout.write(medir())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

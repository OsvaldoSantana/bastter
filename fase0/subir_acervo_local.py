#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carga inicial do armazem: o acervo que so existe no disco dele sobe uma vez (P-57).

O QUE SOBE. Tudo o que o acervo bruto tem de versao:
  - CVM: `data/bronze/cvm/<recurso>/<arquivo>` (a versao vigente) e
    `data/bronze/cvm/<recurso>/_snapshots/<stem>__v<AAAAMMDD>__<sha12>.<ext>` (as
    deslocadas -- inclusive as duas de 2024 de 13/09, que vieram dos `(1).zip` do
    navegador e sao a UNICA copia daquela versao, CV-01);
  - B3: `data/bronze/b3/cotahist/COTAHIST_A<ANO>.ZIP`.
Cada uma vira `<fonte>/<recurso>/<arquivo>/<sha256>.<ext>`, e o snapshot volta ao nome
canonico: a versao e o sha256, o nome do disco era so onde ele cabia.

PLANO POR PADRAO (como o `nomear_extracoes.py` e o `--arrumar`). Sem `--aplicar` nada sai
da maquina: o plano diz o que subiria, com o sha256 de cada arquivo. Com `--aplicar`, sobe
com `enviar_se_ausente` -- rodar duas vezes nao muda nada -- e grava o inventario em
`docs/acervo/<fonte>/inventario-armazem.csv` (versionado, so metadado). O inventario so e
escrito depois do envio: inventario de objeto que nao subiu seria o registro mentindo.

PARAR. Snapshot cujo nome promete um sha12 que os bytes nao tem para o plano inteiro --
o nome e procedencia, e procedencia que nao bate nao sobe. Arquivo fora das convencoes sai
DESCONHECIDO e nao e tocado: decidir o que e lixo e de quem olhou o arquivo.

USO (na maquina dele, com as credenciais R2_* no ambiente):
  py -3.11 fase0/subir_acervo_local.py            # plano
  py -3.11 fase0/subir_acervo_local.py --aplicar  # sobe e grava o inventario
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import acervo as acervo_mod  # noqa: E402
import armazem as armazem_mod  # noqa: E402
import manifesto_cvm  # noqa: E402

SUBIR, PARAR, DESCONHECIDO = "SUBIR", "PARAR", "DESCONHECIDO"
SNAPSHOT = re.compile(r"^(?P<stem>.+)__v(?P<versao>\d{8}|DESCONHECIDA)__(?P<sha12>[0-9a-f]{12})"
                      r"(?P<ext>\.\w+)$")
COTAHIST = re.compile(r"^COTAHIST_A\d{4}\.ZIP$", re.IGNORECASE)
RECURSOS_CVM = ("dfp", "itr", "fca", "cad")   # fca: P-132, 25/09


def _item(fonte, recurso, arquivo, caminho, papel, versao=""):
    return dict(acao=SUBIR, fonte=fonte, recurso=recurso, arquivo=arquivo, caminho=caminho,
                papel=papel, versao=versao, sha256="", bytes=0, chave="", motivo="")


def plano(repo):
    """Lista do que subiria. Calcula o sha256 de cada arquivo -- e o custo de a chave
    ser o conteudo, e o plano nao pode prometer uma chave sem ter medido."""
    out = []
    base = os.path.join(repo, "data", "bronze")
    for recurso in RECURSOS_CVM:
        pasta = os.path.join(base, "cvm", recurso)
        if not os.path.isdir(pasta):
            continue
        for a in sorted(os.listdir(pasta)):
            p = os.path.join(pasta, a)
            if a == "_snapshots" and os.path.isdir(p):
                for s in sorted(os.listdir(p)):
                    m = SNAPSHOT.match(s)
                    it = _item("cvm", recurso, (m["stem"] + m["ext"]) if m else s,
                               os.path.join(p, s), "snapshot", m["versao"] if m else "")
                    if not m:
                        it.update(acao=DESCONHECIDO, motivo="nome fora da convencao 2.6")
                    else:
                        it["sha12"] = m["sha12"]
                    out.append(it)
            elif os.path.isfile(p) and a.lower().endswith((".zip", ".csv")):
                out.append(_item("cvm", recurso, a, p, "canonico"))
            else:
                out.append(dict(_item("cvm", recurso, a, p, ""), acao=DESCONHECIDO,
                                motivo="nao e ZIP, CSV nem _snapshots"))
    pasta = os.path.join(base, "b3", "cotahist")
    if os.path.isdir(pasta):
        for a in sorted(os.listdir(pasta)):
            p = os.path.join(pasta, a)
            if os.path.isfile(p) and COTAHIST.match(a):
                out.append(_item("b3", "cotahist", a, p, "canonico"))
            else:
                out.append(dict(_item("b3", "cotahist", a, p, ""), acao=DESCONHECIDO,
                                motivo="nao e COTAHIST_A<ANO>.ZIP"))
    for it in out:
        if it["acao"] != SUBIR:
            continue
        it["sha256"] = armazem_mod.sha256(it["caminho"])
        it["bytes"] = os.path.getsize(it["caminho"])
        if it.get("sha12") and not it["sha256"].startswith(it["sha12"]):
            it.update(acao=PARAR, motivo=f"o nome promete sha12 {it['sha12']} e os bytes "
                                         f"dao {it['sha256'][:12]}")
            continue
        it["chave"] = armazem_mod.chave(it["fonte"], it["recurso"], it["arquivo"],
                                        it["sha256"])
    return out


def inventario(repo, fonte):
    return os.path.join(repo, "docs", "acervo", fonte, acervo_mod.INVENTARIO)


def aplicar(itens, armazem, repo, agora=None):
    """Sobe e grava o inventario. Com um PARAR no plano, nada sobe."""
    if any(x["acao"] == PARAR for x in itens):
        raise SystemExit("ha PARAR no plano: nada foi enviado")
    agora = agora or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    enviados = 0
    por_fonte = {}                                # fonte -> linhas do inventario
    for x in itens:
        if x["acao"] != SUBIR:
            continue
        enviados += armazem.enviar_se_ausente(x["chave"], x["caminho"])
        por_fonte.setdefault(x["fonte"], []).append(dict(
            fonte=x["fonte"], recurso=x["recurso"], arquivo=x["arquivo"],
            sha256=x["sha256"], bytes=x["bytes"], chave=x["chave"], papel=x["papel"],
            versao=x["versao"], origem=os.path.relpath(x["caminho"], repo).replace("\\", "/"),
            dt_envio=agora))
    for fonte, linhas in por_fonte.items():
        _gravar_inventario(inventario(repo, fonte), linhas)
    return enviados


def _gravar_inventario(caminho, novas):
    """Acrescenta sem repetir chave: rodar de novo nao duplica linha, e a data do primeiro
    envio de cada chave fica."""
    existentes = acervo_mod._ler(caminho)
    vistas = {ln["chave"] for ln in existentes}
    linhas = existentes + [ln for ln in novas if ln["chave"] not in vistas]
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=acervo_mod.COLUNAS_INVENTARIO, delimiter=";")
        w.writeheader()
        for ln in sorted(linhas, key=lambda ln: ln["chave"]):
            w.writerow({c: ln.get(c, "") for c in acervo_mod.COLUNAS_INVENTARIO})


def main(argv=None, armazem=None, repo=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--aplicar", action="store_true", help="sobe e grava o inventario")
    p.add_argument("--armazem", choices=["s3"], default="s3")
    a = p.parse_args(argv)
    repo = repo or manifesto_cvm.raiz_do_repositorio(AQUI)
    itens = plano(repo)
    for x in itens:
        print(f"{x['acao']:12s} {os.path.relpath(x['caminho'], repo)}"
              + (f"\n{'':12s} -> {x['chave']}" if x["chave"] else "")
              + (f"\n{'':12s} {x['motivo']}" if x["motivo"] else ""))
    cont = {k: sum(x["acao"] == k for x in itens) for k in (SUBIR, PARAR, DESCONHECIDO)}
    total = sum(x["bytes"] for x in itens if x["acao"] == SUBIR)
    print("  ".join(f"{k} {v}" for k, v in cont.items()) + f"  ({total / 2**20:,.0f} MiB)")
    if cont[PARAR]:
        return 1
    if not a.aplicar:
        print("plano apenas: nada saiu da maquina. --aplicar para enviar.")
        return 0
    n = aplicar(itens, armazem or armazem_mod.do_ambiente(a.armazem), repo)
    print(f"enviados {n}; ja estavam no armazem {cont[SUBIR] - n}. Inventario gravado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

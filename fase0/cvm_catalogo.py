#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cvm_catalogo.py -- interroga a API do portal de dados abertos da CVM.

POR QUE ESTE ARQUIVO EXISTE.

Em 06/09/2026 o Osvaldo abriu `dados.cvm.gov.br/dataset` no celular e no rodape estava
escrito, em letra pequena:

    "Voce tambem pode ter acesso a esses registros usando a API (veja Documentacao da
     API)."  --  "Impulsionado por CKAN"

O portal e um **CKAN**. Isso muda duas coisas de uma vez:

1. O catalogo inteiro (54 conjuntos) e legivel por maquina. Nao precisa raspar HTML.
2. **CKAN publica `last_modified` por RECURSO.** Ou seja: a pergunta que esta aberta ha
   tres sessoes -- *"a CVM reescreve o `dfp_cia_aberta_2026.zip`?"* -- tem resposta
   exata, sem baixar 1,5 GB, e sem depender de cabecalho HTTP.

A pagina de listagem tambem respondeu, e a resposta foi um DESVIO:

    "Os arquivos de dados serao atualizados conforme a politica publicada na pagina do
     respectivo conjunto de dados."

Ou seja: nao ha politica global; ha uma por conjunto. E a politica de cada conjunto e um
campo do CKAN. Este script vai busca-la.

ADVERTENCIA DE PROCEDENCIA -- leia antes de confiar na saida.

Os caminhos `/api/3/action/*` abaixo sao o padrao do CKAN e **nao foram conferidos neste
portal**: `dados.cvm.gov.br` responde ROBOTS_DISALLOWED as minhas ferramentas e eu nao
contorno bloqueio de robots.txt. O que e OBSERVADO e que o portal roda CKAN (o proprio
rodape diz) e que ele anuncia ter API. Que a API esteja em `/api/3/action/` e
**inferencia forte, nao leitura**. Se o script falhar em `package_list`, o defeito
provavel e o caminho, nao a rede -- e ai a saida diz isso em voz alta em vez de fingir
catalogo vazio.

USO
    python cvm_catalogo.py --listar               # os 54 conjuntos, so nome e titulo
    python cvm_catalogo.py --detalhar cia_aberta-doc-dfp
    python cvm_catalogo.py --procurar dfp         # acha o slug sem adivinhar
    python cvm_catalogo.py --tudo                 # snapshot completo do catalogo

So biblioteca padrao. Nao entra na impressao do ambiente (`ambiente.py`): nao produz
numero, so grava bytes.
"""

import argparse, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

BASE = "https://dados.cvm.gov.br/api/3/action"
RAIZ_PADRAO = os.path.join("data", "bronze", "cvm", "catalogo")
PAUSA_S = 0.8
TEMPO_LIMITE_S = 45

# Campos de recurso que interessam. `last_modified` e o motivo deste arquivo existir.
CAMPOS = ("name", "format", "size", "created", "last_modified", "url", "hash")


def chamar(acao, **params):
    url = BASE + "/" + acao
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "User-Agent": "bastter-fase0/1.0 (coleta pessoal de dado publico)",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=TEMPO_LIMITE_S) as r:
            corpo = r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise RuntimeError(
            "HTTP %s em %s\n"
            "Se for 404, o caminho da API nao e este -- ele era INFERENCIA, nao leitura.\n"
            "Abra %s/dataset no navegador, clique em 'Documentacao da API' e me diga o\n"
            "caminho real. Nada foi gravado." % (e.code, url, BASE.split("/api")[0]))
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise RuntimeError("falha de rede em %s -- %s" % (url, e))

    dados = json.loads(corpo)
    if not dados.get("success"):
        raise RuntimeError("a API respondeu success=false em %s: %s" % (url, dados.get("error")))
    return dados["result"]


def agora():
    return datetime.now(timezone.utc).astimezone()


def gravar(raiz, nome, obj):
    dia = agora().strftime("%Y-%m-%d")
    destino = os.path.join(raiz, "dt_captura=" + dia, nome)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    if os.path.exists(destino):
        print("  (ja existia, nao reescrito: %s)" % destino)
        return destino
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    return destino


def linha_recurso(r):
    return "    %-46s %-6s %12s  mod=%s" % (
        (r.get("name") or "?")[:46], (r.get("format") or "?")[:6],
        r.get("size") if r.get("size") is not None else "?",
        r.get("last_modified") or r.get("created") or "SEM DATA")


def detalhar(slug, raiz, gravar_arquivo=True):
    p = chamar("package_show", id=slug)
    recursos = p.get("resources") or []
    print("\n%s" % p.get("title") or slug)
    print("  slug: %s" % p.get("name"))
    print("  atualizado no catalogo: %s" % p.get("metadata_modified"))
    # A politica de atualizacao que a pagina de listagem prometeu vive aqui.
    for chave in ("notes", "update_frequency", "frequency"):
        if p.get(chave):
            txt = str(p[chave]).replace("\r", " ").replace("\n", " ")
            print("  %s: %s%s" % (chave, txt[:300], "..." if len(txt) > 300 else ""))
    for e in (p.get("extras") or []):
        print("  extra %s: %s" % (e.get("key"), str(e.get("value"))[:200]))
    print("  %d recursos:" % len(recursos))
    for r in recursos[:400]:
        print(linha_recurso(r))
    if gravar_arquivo:
        print("  -> %s" % gravar(raiz, slug.replace("/", "_") + ".json", p))
    return p


def main(argv=None):
    a = argparse.ArgumentParser(description="Interroga a API CKAN do portal de dados abertos da CVM.")
    a.add_argument("--raiz", default=RAIZ_PADRAO)
    a.add_argument("--listar", action="store_true", help="nomes de todos os conjuntos")
    a.add_argument("--procurar", metavar="TERMO", help="acha o slug sem adivinhar")
    a.add_argument("--detalhar", metavar="SLUG", help="recursos e datas de um conjunto")
    a.add_argument("--tudo", action="store_true", help="snapshot completo do catalogo")
    n = a.parse_args(argv)
    if not (n.listar or n.procurar or n.detalhar or n.tudo):
        a.error("escolha --listar, --procurar, --detalhar ou --tudo")

    if n.listar or n.tudo:
        nomes = chamar("package_list")
        print("%d conjuntos no catalogo." % len(nomes))
        if n.listar and not n.tudo:
            for x in nomes: print("  " + x)
        gravar(n.raiz, "package_list.json", nomes)

    if n.procurar:
        r = chamar("package_search", q=n.procurar, rows=50)
        print("%d resultados para %r:" % (r.get("count", 0), n.procurar))
        for p in r.get("results", []):
            print("  %-46s %s" % (p.get("name"), (p.get("title") or "")[:70]))

    if n.detalhar:
        detalhar(n.detalhar, n.raiz)

    if n.tudo:
        falhas = []
        for i, slug in enumerate(nomes, 1):
            print("[%d/%d]" % (i, len(nomes)), end="")
            try:
                detalhar(slug, n.raiz)
            except Exception as e:                      # noqa: BLE001
                falhas.append((slug, str(e)[:90]))
                print("  ERRO em %s: %s" % (slug, str(e)[:90]))
            time.sleep(PAUSA_S)
        if falhas:
            print("\n%d conjuntos falharam: %s" % (len(falhas), ", ".join(s for s, _ in falhas)))
            return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        print("\n" + str(e), file=sys.stderr)
        sys.exit(2)

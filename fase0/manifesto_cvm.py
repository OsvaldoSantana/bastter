#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manifesto do acervo da CVM -- e a comparacao que NAO produz falso positivo.

POR QUE ELE EXISTE. O guia de download diz, com todas as letras: *um retrato sem hash
nao e um retrato, e sim um arquivo*. Os 33 ZIPs chegaram em 18/09/2026 e nenhum tinha
sha256 registrado -- a rotina existia como comando para alguem lembrar de rodar, e a P7
diz que rotina que depende de lembrar nao e rotina.

O ACHADO QUE MUDA O DESENHO, medido em 18/09 sobre o unico par que o acervo tinha.

Tres anos (2012, 2019, 2024) foram baixados duas vezes, com 14 dias de intervalo. O
`dfp_cia_aberta_2024.zip` de 04/09 e o de 18/09 tem sha256 DIFERENTE. E o dado e o
MESMO: dois dos dezoito CSVs mudaram, e neles

    mesmo numero de linhas, mesmo numero de bytes, e ZERO linhas exclusivas de
    qualquer um dos lados -- `sorted(a) == sorted(b)`.

Sao 8 linhas fora de posicao em 94.517, e 12 em 59.744. **A CVM regerou o arquivo e a
ordem das linhas mudou. Nao houve reapresentacao.**

    A estrategia registrada no CLAUDE.md §11.6 -- *"baixar, comparar, guardar o delta"* --
    teria declarado uma reapresentacao aqui, e commitado ruido no git toda semana. E o
    F-02 espelhado: la a ausencia virava zero; aqui o RUIDO VIRA EVENTO.

Por isso este modulo tem duas operacoes e elas respondem perguntas diferentes:

    --manifesto   sha256 do BYTE que a CVM entregou. E procedencia: prova QUAL arquivo
                  voce tem. Nunca serve para responder "mudou?".
    --comparar    diferenca de CONTEUDO entre dois ZIPs, normalizada por ordem. E a
                  unica que responde "a CVM reapresentou alguma coisa?".

E o 2019 foi a testemunha do outro lado: byte a byte identico nos 14 dias, exatamente
como a politica da CVM promete para os anos fora da janela de reapresentacao. A promessa
deixou de ser citada e passou a ser medida.

USO
    python fase0/manifesto_cvm.py --manifesto data/bronze/cvm
        grava em docs/acervo/cvm/dt_captura=AAAA-MM-DD.csv -- FORA do `data/`, que o
        .gitignore ignora. Manifesto ignorado pelo git nao prova nada a terceiro.
    python fase0/manifesto_cvm.py --comparar a.zip b.zip
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import hashlib
import io
import os
import sys
import zipfile

BLOCO = 1 << 20
COLUNAS = ("caminho", "bytes", "sha256", "mtime_utc", "dt_captura")


def sha256(caminho, bloco=BLOCO):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for p in iter(lambda: f.read(bloco), b""):
            h.update(p)
    return h.hexdigest()


def zips(raiz):
    """Todo .zip sob a raiz, em ordem estavel.

    Ordenar nao e estetica: e a licao do P-85, em que a saida de um relatorio mudava de
    texto entre execucoes por causa de um `set` impresso sem ordem, e o instantaneo
    dourado deixou de servir de rede."""
    out = []
    for pasta, _, arquivos in os.walk(raiz):
        for a in arquivos:
            if a.lower().endswith(".zip"):
                out.append(os.path.join(pasta, a))
    return sorted(out)


def manifesto(raiz, quando=None):
    """Uma linha por ZIP: o que se tem, e desde quando se sabe que se tem."""
    quando = quando or dt.datetime.now(dt.timezone.utc)
    linhas = []
    for caminho in zips(raiz):
        st = os.stat(caminho)
        linhas.append({
            "caminho": os.path.relpath(caminho, raiz).replace("\\", "/"),
            "bytes": st.st_size,
            "sha256": sha256(caminho),
            "mtime_utc": dt.datetime.fromtimestamp(
                st.st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "dt_captura": quando.strftime("%Y-%m-%d"),
        })
    return linhas


def raiz_do_repositorio(partida):
    """Sobe ate achar o `pyproject.toml`. E o mesmo ancoradouro que o `ambiente.py` usa,
    e nao o `.git`: o manifesto tem de saber onde fica o repositorio mesmo num clone
    sem historico."""
    d = os.path.abspath(partida)
    while True:
        if os.path.exists(os.path.join(d, "pyproject.toml")): return d
        pai = os.path.dirname(d)
        if pai == d: return None
        d = pai


def destino_padrao(raiz_acervo, hoje):
    """`docs/acervo/<nome>/dt_captura=AAAA-MM-DD.csv`, e NAO dentro do acervo.

    18/09/2026, e o defeito e meu. A primeira versao gravava em
    `data/bronze/cvm/manifesto/`, o `CVM-PRIMEIRO-RETRATO.md` afirmava que *"o manifesto
    entra no repositorio"*, e o `.gitignore` ignora `data/` inteiro desde sempre. O
    arquivo foi gravado, o commit passou, e o manifesto **nao entrou** -- justamente o
    arquivo cujo unico proposito e tornar a procedencia verificavel por terceiro.

    O documento declarava um comportamento que o sistema nao tinha, e os dois
    concordaram porque ninguem olhou a saida do `git commit`. E o defeito recorrente do
    projeto, desta vez cometido no mesmo dia em que o instrumento nasceu."""
    base = raiz_do_repositorio(raiz_acervo) or os.path.abspath(raiz_acervo)
    nome = os.path.basename(os.path.abspath(raiz_acervo).rstrip(os.sep)) or "acervo"
    return os.path.join(base, "docs", "acervo", nome, f"dt_captura={hoje}.csv")


def gravar(linhas, destino):
    partes = os.path.abspath(destino).replace("\\", "/").split("/")
    if "data" in partes:
        raise ValueError(
            f"recusando gravar o manifesto em {destino}: o caminho passa por `data/`, e "
            f"`data/` esta no .gitignore. Manifesto que nao entra no repositorio nao e "
            f"procedencia de ninguem -- e o unico proposito dele e ser verificavel sem "
            f"os 700 MB do acervo.")
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    novo = io.StringIO()
    w = csv.DictWriter(novo, fieldnames=COLUNAS, delimiter=";")
    w.writeheader()
    w.writerows(linhas)
    texto = novo.getvalue()

    # 18/09, e o caso apareceu na primeira hora de uso: o manifesto do acervo da B3 foi
    # gravado com UM arquivo (so o COTAHIST de 2023), e os outros quatro anos seriam
    # baixados em seguida -- no MESMO dia. O nome e `dt_captura=AAAA-MM-DD.csv`, entao a
    # segunda gravacao apagaria a primeira sem dizer nada.
    #
    # E o retrato apagado seria justamente a prova de que, as 14h, o acervo tinha so 2023.
    # O manifesto existe porque a CVM sobrescreve arquivo sob o mesmo nome -- e ele estava
    # fazendo exatamente isso consigo. O instrumento com o defeito que ele mede.
    #
    # A saida NAO e travar (o fluxo legitimo e baixar mais e regravar) nem versionar tudo
    # (rodar duas vezes sem mudanca criaria lixo). E: identico nao reescreve, diferente
    # PRESERVA o anterior com a impressao do proprio conteudo no nome.
    anterior = None
    if os.path.exists(destino):
        with open(destino, encoding="utf-8", newline="") as f:
            velho = f.read()
        if velho == texto:
            return destino                      # idempotente: duas execucoes, um arquivo
        raiz, ext = os.path.splitext(destino)
        anterior = f"{raiz}.{hashlib.sha256(velho.encode('utf-8')).hexdigest()[:12]}{ext}"
        os.replace(destino, anterior)
        print(f"AVISO: ja havia manifesto para hoje, com CONTEUDO DIFERENTE -- o acervo "
              f"mudou dentro do mesmo dia.\n  o retrato anterior foi PRESERVADO em "
              f"{os.path.basename(anterior)}", file=sys.stderr)
    with open(destino, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
    return destino


def comparar(a, b):
    """Diferenca de CONTEUDO entre dois ZIPs, insensivel a ordem de linha.

    Devolve (veredito, detalhe). O veredito e um NOME, nunca um booleano solto:

      IDENTICO      byte a byte
      REORDENADO    o conjunto de linhas e o mesmo em todos os membros -- a CVM regerou
                    o arquivo. **Nao e reapresentacao.**
      REAPRESENTADO ha linha que existe de um lado e nao do outro. E o evento que o
                    projeto quer capturar, e so ele.
      ESTRUTURA     os ZIPs nao tem os mesmos membros
    """
    if sha256(a) == sha256(b):
        return "IDENTICO", {}
    za, zb = zipfile.ZipFile(a), zipfile.ZipFile(b)
    na = {i.filename for i in za.infolist()}
    nb = {i.filename for i in zb.infolist()}
    if na != nb:
        return "ESTRUTURA", {"so_em_a": sorted(na - nb), "so_em_b": sorted(nb - na)}
    detalhe = {}
    veredito = "IDENTICO"
    for nome in sorted(na):
        da, db = za.read(nome), zb.read(nome)
        if da == db: continue
        la, lb = da.split(b"\n"), db.split(b"\n")
        sa, sb = set(la), set(lb)
        so_a, so_b = sa - sb, sb - sa
        if not so_a and not so_b:
            detalhe[nome] = {"tipo": "REORDENADO",
                             "fora_de_posicao": sum(1 for x, y in zip(la, lb) if x != y),
                             "linhas": len(la)}
            veredito = "REORDENADO" if veredito == "IDENTICO" else veredito
        else:
            detalhe[nome] = {"tipo": "REAPRESENTADO", "saiu": len(so_a),
                             "entrou": len(so_b), "linhas": len(lb),
                             "exemplo_entrou": [x.decode("latin-1")[:160] for x in list(so_b)[:2]],
                             "exemplo_saiu": [x.decode("latin-1")[:160] for x in list(so_a)[:2]]}
            veredito = "REAPRESENTADO"
    return veredito, detalhe


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--manifesto", metavar="RAIZ")
    p.add_argument("--saida", default=None)
    p.add_argument("--comparar", nargs=2, metavar=("A", "B"))
    a = p.parse_args(argv)
    if a.comparar:
        v, d = comparar(*a.comparar)
        print(f"veredito: {v}")
        for nome, info in d.items():
            print(f"  {nome}: {info}")
        # REAPRESENTADO e o unico que exige acao humana; sair != 0 para o chamador saber
        return 2 if v == "REAPRESENTADO" else 0
    if a.manifesto:
        linhas = manifesto(a.manifesto)
        if not linhas:
            print(f"nenhum .zip sob {a.manifesto} -- e isso NAO e 'nada mudou': e "
                  f"'nao ha acervo'. Confira o caminho antes de concluir.", file=sys.stderr)
            return 1
        hoje = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
        destino = a.saida or destino_padrao(a.manifesto, hoje)
        gravar(linhas, destino)
        print(f"{len(linhas)} arquivos, {sum(x['bytes'] for x in linhas)/1e6:.0f} MB")
        print(f"manifesto: {destino}")
        for x in linhas:
            print(f"  {x['sha256'][:16]}  {x['bytes']:>12,}  {x['caminho']}")
        return 0
    p.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

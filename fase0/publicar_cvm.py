#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica as versoes da CVM como arquivos de release do GitHub (P-136, decisao 2).

POR QUE ELE EXISTE (25/09/2026). A CVM serve so a versao corrente e reescreve toda semana os
cinco anos mais recentes do DFP e do ITR; as versoes substituidas que o projeto capturou so
existiam no R2, privado. A licenca e ODbL (docs/fontes/cvm-dados-abertos-licenca.md): pode
redistribuir, com atribuicao e aviso. Decisao dele: pode ser publico. Desenho, alternativas e
riscos em docs/decisoes/P-136-cvm-publica.md.

POR QUE RELEASE E NAO O R2. O acesso publico do R2 e do BUCKET inteiro (docs da Cloudflare,
lidas em 25/09), e o bucket guarda a B3, que os termos vedam publicar. A release usa o
GITHUB_TOKEN do proprio workflow: nenhuma conta nem credencial nova.

A GUARDA QUE MAIS IMPORTA: so sai o que e da CVM. `publicavel()` recusa com
`PublicacaoRecusada` qualquer versao cuja fonte nao seja `cvm`, cujo recurso nao seja um dos
quatro da CVM, ou cuja chave no armazem nao comece por `cvm/`. Release publicada nao se
despublica sem rastro: quem baixou, baixou.

  - uma release por ano de observacao: `cvm-acervo-<ano>`;
  - arquivo = versao: `<nome>__<sha256[:12]>.<ext>`, nunca sobrescrito;
  - notas com a atribuicao que a CVM exige, a licenca e a tabela de sha256 -- e a tabela que
    `fase0/conferir_reproducao.py` compara;
  - idempotente: so envia o que a release ainda nao tem.

  python fase0/publicar_cvm.py                       # plano: o que enviaria; nao toca nada
  python fase0/publicar_cvm.py --armazem s3 --aplicar   # o que o workflow roda
"""
from __future__ import annotations

import argparse
import csv
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import acervo  # noqa: E402
import armazem as armazem_mod  # noqa: E402

FONTE = "cvm"
RECURSOS = ("dfp", "itr", "fca", "cad")
PREFIXO_TAG = "cvm-acervo-"
REGISTRO = os.path.join("docs", "acervo", "cvm", "capturas.csv")
INVENTARIO = os.path.join("docs", "acervo", "cvm", "inventario-armazem.csv")
# So estas situacoes do registro tem o byte no armazem; `deslocado` aponta uma versao que ja
# entrou por outra linha, e `erro`/`rejeitado` nao tem byte.
COM_BYTE = ("novo", "atualizado")
ATRIBUICAO = ("Dados acessados pelo Portal de Dados Abertos da CVM, disponível em "
              "https://dados.cvm.gov.br/")
# Limite do corpo de release no GitHub; a tabela e compacta para caber com folga (P5).
LIMITE_NOTAS = 120_000


class PublicacaoRecusada(Exception):
    """Uma versao que nao e da CVM chegou ao publicador. Nunca deve acontecer, e por isso
    derruba em vez de pular: pular esconderia o defeito que a trouxe ate aqui."""


def _ler(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def versoes(repo):
    """[{fonte, recurso, arquivo, sha256, bytes, ano}] -- toda versao da CVM com byte no
    armazem, uma vez cada: o inventario da carga inicial e as capturas `novo`/`atualizado`."""
    vistas = {}
    for ln in _ler(os.path.join(repo, INVENTARIO)):
        vistas.setdefault(ln["sha256"], dict(
            fonte=ln.get("fonte", ""), recurso=ln["recurso"], arquivo=ln["arquivo"],
            sha256=ln["sha256"], bytes=ln.get("bytes", ""),
            ano=(ln.get("versao") or ln.get("dt_envio") or "")[:4]))
    for ln in _ler(os.path.join(repo, REGISTRO)):
        if ln.get("situacao") in COM_BYTE and ln.get("sha256"):
            vistas.setdefault(ln["sha256"], dict(
                fonte=FONTE, recurso=ln["recurso"], arquivo=ln["arquivo"],
                sha256=ln["sha256"], bytes=ln.get("bytes", ""),
                ano=(ln.get("dt_captura") or "")[:4]))
    return sorted(vistas.values(), key=lambda v: (v["ano"], v["recurso"], v["arquivo"],
                                                   v["sha256"]))


def publicavel(v):
    """A chave do armazem da versao, ou `PublicacaoRecusada`."""
    if v.get("fonte") != FONTE or v.get("recurso") not in RECURSOS:
        raise PublicacaoRecusada(
            f"{v.get('fonte')}/{v.get('recurso')}/{v.get('arquivo')}: so a CVM e publicavel "
            f"(ODbL); B3 e NEFIN nao (docs/decisoes/P-136-cvm-publica.md)")
    k = armazem_mod.chave(FONTE, v["recurso"], v["arquivo"], v["sha256"])
    if not k.startswith(FONTE + "/"):
        raise PublicacaoRecusada(f"chave fora de {FONTE}/: {k}")
    if not (len(v.get("ano", "")) == 4 and v["ano"].isdigit()):
        raise PublicacaoRecusada(f"{v['arquivo']}: sem ano de observacao ({v.get('ano')!r})")
    return k


def nome_do_arquivo(v):
    """`dfp_cia_aberta_2024.zip` -> `dfp_cia_aberta_2024__0dd854dc1a2b.zip`."""
    base, ext = os.path.splitext(v["arquivo"])
    return f"{base}__{v['sha256'][:12]}{ext.lower()}"


def plano(vs, existentes):
    """{tag: [versao]} do que falta enviar. `existentes` e {tag: set(nomes)} -- a release
    que nao existe entra com o conjunto vazio."""
    out = {}
    for v in vs:
        publicavel(v)
        tag = PREFIXO_TAG + v["ano"]
        if nome_do_arquivo(v) not in existentes.get(tag, set()):
            out.setdefault(tag, []).append(v)
    return out


def notas(tag, vs):
    """O corpo da release: atribuicao, licenca, e a tabela de sha256 de TODAS as versoes do
    ano (as ja publicadas e as novas)."""
    linhas = [
        f"# Acervo da CVM observado pelo MEOL — {tag[len(PREFIXO_TAG):]}",
        "",
        ATRIBUICAO + ".",
        "",
        "Licença dos dados: **Open Database License (ODbL) 1.0** — "
        "http://www.opendefinition.org/licenses/odc-odbl . Os arquivos são reproduzidos sem "
        "alteração; cada nome carrega o prefixo do sha256 da versão. Como conferir: "
        "`docs/reproduzir.md` no repositório.",
        "",
        "| arquivo | sha256 |",
        "|---|---|",
    ]
    linhas += [f"| `{nome_do_arquivo(v)}` | `{v['sha256']}` |" for v in vs]
    corpo = "\n".join(linhas) + "\n"
    if len(corpo) > LIMITE_NOTAS:
        raise ValueError(f"{tag}: notas com {len(corpo)} caracteres passam de {LIMITE_NOTAS}; "
                         f"partir a release (P5)")
    return corpo


def _gh(args, rodar):
    return rodar(["gh", *args])


def existentes_de(tags, rodar):
    """{tag: set(nomes)} das releases que ja existem; tag sem release fica de fora."""
    out = {}
    for tag in tags:
        try:
            r = _gh(["release", "view", tag, "--json", "assets", "--jq", ".assets[].name"],
                    rodar)
        except FileNotFoundError:
            return None                              # sem `gh`: nao ha como saber
        if r.returncode == 0:
            out[tag] = {n for n in r.stdout.split() if n}
    return out


def main(argv=None, rodar=None, abrir=None, repo=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--armazem", choices=["s3", "local"], default=None,
                   help="de onde abrir o byte que nao estiver no cache (acervo.abrir)")
    p.add_argument("--aplicar", action="store_true",
                   help="cria/edita a release e envia; sem ela, so imprime o plano")
    a = p.parse_args(argv)
    repo = repo or acervo.raiz_repo()
    rodar = rodar or (lambda cmd: subprocess.run(cmd, capture_output=True, text=True))
    if abrir is None:
        arm = armazem_mod.do_ambiente(a.armazem) if a.armazem else None

        def abrir(v):
            return acervo.abrir(v["recurso"], v["arquivo"], v["sha256"][:16],
                                armazem=arm, repo=repo)

    vs = versoes(repo)
    for v in vs:
        publicavel(v)                                 # tudo ou nada: recusa antes de enviar
    por_tag = {}
    for v in vs:
        por_tag.setdefault(PREFIXO_TAG + v["ano"], []).append(v)
    existentes = existentes_de(sorted(por_tag), rodar)
    if existentes is None:
        if a.aplicar:
            print("[!] `gh` nao encontrado: sem ele nao ha como publicar", file=sys.stderr)
            return 1
        print("AVISO: `gh` nao encontrado -- o plano abaixo SUPOE que nenhuma release existe")
        existentes = {}
    falta = plano(vs, existentes)
    total = sum(len(x) for x in falta.values())
    print(f"{len(vs)} versao(oes) da CVM; {total} a enviar em {len(falta)} release(s)")
    for tag, lista in sorted(falta.items()):
        print(f"  {tag}: {len(lista)} " + ("(release nova)" if tag not in existentes else ""))
    if not a.aplicar or not falta:
        return 0

    indisponiveis = []
    with tempfile.TemporaryDirectory(prefix="publicar_cvm_") as tmp:
        for tag, lista in sorted(falta.items()):
            publicados = set(existentes.get(tag, set()))
            arq_notas = os.path.join(tmp, f"{tag}.md")
            # As notas so listam o que ESTA na release: tabela com versao que nao subiu seria
            # afirmar um arquivo que nao existe.
            with open(arq_notas, "w", encoding="utf-8") as f:
                f.write(notas(tag, [v for v in por_tag[tag]
                                    if nome_do_arquivo(v) in publicados]))
            if tag not in existentes:
                r = _gh(["release", "create", tag, "--title", f"Acervo CVM {tag[-4:]}",
                         "--notes-file", arq_notas, "--latest=false"], rodar)
                if r.returncode != 0:
                    print(f"[!] {tag}: release nao criada: {r.stderr.strip()}", file=sys.stderr)
                    return 1
            for v in lista:
                try:
                    origem = abrir(v)
                except (KeyError, OSError, acervo.VersaoDesconhecida) as e:
                    indisponiveis.append(f"{nome_do_arquivo(v)}: {e}")
                    continue
                destino = os.path.join(tmp, nome_do_arquivo(v))
                shutil.copyfile(origem, destino)
                if armazem_mod.sha256(destino) != v["sha256"]:
                    raise armazem_mod.ConteudoDivergente(f"{destino}: sha256 nao confere")
                r = _gh(["release", "upload", tag, destino], rodar)
                os.remove(destino)
                if r.returncode != 0:
                    print(f"[!] {nome_do_arquivo(v)}: {r.stderr.strip()}", file=sys.stderr)
                    return 1
                publicados.add(nome_do_arquivo(v))
                print(f"[+] {tag} {nome_do_arquivo(v)}")
            with open(arq_notas, "w", encoding="utf-8") as f:
                f.write(notas(tag, [v for v in por_tag[tag]
                                    if nome_do_arquivo(v) in publicados]))
            r = _gh(["release", "edit", tag, "--notes-file", arq_notas], rodar)
            if r.returncode != 0:
                print(f"[!] {tag}: notas nao atualizadas: {r.stderr.strip()}", file=sys.stderr)
                return 1
    if indisponiveis:
        # Versao que o registro conhece e o armazem nao tem: nao e falha de publicacao, e
        # lacuna do acervo -- escrita, com o numero, e nao calada (5-B.14).
        print(f"AVISO: {len(indisponiveis)} versao(oes) sem byte no armazem, nao publicadas:\n  "
              + "\n  ".join(indisponiveis), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

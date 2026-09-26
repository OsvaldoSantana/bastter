#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Todo achado CITADO tem onde ser lido -- a promessa "nada some" virada medicao.

POR QUE ELE EXISTE. Em 19/09/2026 saiu do `CLAUDE.md` para o `ACHADOS.md` um intervalo
contiguo de 962 linhas e 20.085 tokens: os trinta achados de 06/09 a 18/09, que a secao 7
tinha acumulado. A secao 10 do proprio arquivo dizia, desde 06/09, que achado mora no
`ACHADOS.md` -- *"nao estao aqui de proposito"* --, e a 7 fez o contrario por treze dias.

O RISCO DO CORTE, e e ele que este modulo mede. O codigo do projeto cita achado em
comentario -- `# A-02: custo percentual nao dilui`, `# P-99: a chave e NORMALIZADA` -- e a
convencao da casa e justamente essa: *nomear o achado que motivou a linha*. Se um achado
for citado e nao existir em lugar nenhum, a proxima sessao le o nome e **nao tem onde ler
o achado**. Ai o corte deixou de mover contexto e passou a perde-lo.

    "Achado retirado fica como retratacao -- nunca some" e uma regra sobre APAGAR. Nao
    protege contra MOVER errado, que e mais facil de fazer e mais dificil de ver. Uma
    promessa que nenhum instrumento mede e uma promessa.

O QUE ELE MEDE, e o alcance e mais estreito que o nome (P5): que cada referencia
`LETRA-NUMERO` tenha, em algum `.md` do repositorio, uma **definicao** -- cabecalho
(`## A-06 ...`) ou linha de indice (`| **A-06** | ...`). NAO mede se a definicao esta
correta, nem se ela e suficiente, nem se o texto movido chegou inteiro. Mede uma coisa so:
que o nome tem endereco.

O QUE ELE NAO ENXERGA, declarado:
  - achado citado sem o formato `LETRA-NUMERO` (um "o defeito do zip", por exemplo);
  - definicao que existe e esta VAZIA -- um cabecalho sem corpo passa;
  - o `ACHADOS.md` quando ele nao esta na arvore. O relatorio DIZ que ele faltou, em vez de
    fechar verde por ausencia -- que seria o F-02 nesta camada.
"""
from __future__ import annotations
import argparse
import collections
import io
import os
import re
import sys

REF = re.compile(r"\b([A-Z]{1,2})-(\d{1,3})\b")
# O `>?\s*` nao e zelo: a primeira versao do indice de achados nasceu DENTRO de um
# blockquote, e o instrumento nao a via -- acusou como orfaos os 23 achados que ele
# mesmo acabara de ancorar. Ferramenta que mede o lugar errado, no dia em que nasceu.
DEF_CABECALHO = re.compile(r"^>?\s*#{2,4}\s+~*\**\s*([A-Z]{1,2})-(\d{1,3})\b", re.M)
DEF_INDICE = re.compile(r"^>?\s*\|\s*\**\s*([A-Z]{1,2})-(\d{1,3})[\s/*]*\|", re.M)
# Uma linha por achado, sempre. `| **A-03 / A-04** |` deixava o A-04 sem endereco --
# e foi este instrumento que pegou o proprio indice que acabara de nascer.
# Indice tem de ser legivel pela MAQUINA, senao e lista de nomes.
IGNORAR_DIR = {"__pycache__", ".git", ".mypy_cache", ".ruff_cache", "data",
               "pesquisa-custos-2026-08", "node_modules"}
EXTENSOES = (".py", ".md", ".yaml", ".yml")

# ── LINHA DE BASE. O que casa com o padrao e NAO e achado deste projeto.
# Cada entrada precisa do motivo ao lado -- lista sem motivo e lembrete, nao regra (P-82).
NAO_SAO_ACHADOS = {
    "UTF-8": "codificacao, nao achado",
    "UTF-16": "idem",
    "SHA-256": "algoritmo",
    "ISO-8601": "formato de data",
    "IMA-B": "indice ANBIMA",
    "IRF-M": "indice ANBIMA",
    "CDI-1": "indexador",
    "IPCA-15": "indice do IBGE",
    "Z-99": "codigo ficticio da prova por mutacao deste proprio modulo",
}



# ── PREFIXOS DE OUTRO DOMINIO: a mesma forma `LETRA-NUMERO`, numeracao propria, e nenhum
# e achado. Decisao dele, 26/09/2026: a pesquisa de marca chegou com prefixos C (01 a 29) e R (01 a
# 21), e os achados de fator, proventos, moeda e ordem dos portoes ja usavam esses numeros. Os
# documentos foram renomeados, e os prefixos novos entram aqui com o motivo, prefixo INTEIRO
# (`MC-02` sai, `C-02` fica). Guardado por `test_codigos_de_marca.py`.
PREFIXOS_DE_OUTRO_DOMINIO = {
    "MC": "livro de codigos de marca (docs/marca/, pesquisa de marcas)",
    "RI": "requisito de interface (docs/marca/requisitos-interface-v1.md)",
}


def conta_como_codigo(cod, ignorar=None):
    """O codigo `LETRA-NUMERO` e um nome deste projeto? Regra unica para este modulo e para o
    `codigos_preservados`, que antes repetiam o filtro cada um a seu modo."""
    ignorar = NAO_SAO_ACHADOS if ignorar is None else ignorar
    return cod not in ignorar and cod.split("-", 1)[0] not in PREFIXOS_DE_OUTRO_DOMINIO


# ── CANDIDATOS, nao achados (P3 aplicada a propria auditoria).
# Em 19/09 o modulo acusou 25 codigos citados SO em codigo, sem nenhum `.md`. Parte deles
# provavelmente NAO e achado -- `K-04` aparece com as teses (`teses.yaml`, `tese.py`), e os
# `V-*` aparecem no changelog do `politica.yaml` como itens de um laudo. Namespaces
# diferentes com a mesma forma.
#
# NAO os coloquei na linha de base, e a razao e a regua §5-B: **medir levanta o candidato;
# quem o promove e a leitura**, e eu nao tenho o `ACHADOS.md` nem os laudos de agosto para
# ler. Cada um que for tese ou item de laudo entra em NAO_SAO_ACHADOS com o motivo; cada um
# que for achado de verdade e um nome que o codigo cita e ninguem pode consultar.
CANDIDATOS_19_09 = (
    "B-05", "B-06", "B-07", "B-08", "D-1", "H-02", "K-04", "K-05", "K-08", "K-11",
    "V-02", "V-03", "V-04", "V-05", "V-06", "V-07", "V-08", "V-09", "V-10", "V-12",
    "V-13", "V-14", "V-15", "Z-01",
)


def arquivos(raiz):
    for base, dirs, arqs in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIR]
        for a in sorted(arqs):
            if a.endswith(EXTENSOES):
                yield os.path.join(base, a)


def varrer(raiz, ignorar=None):
    """(referencias, definicoes, achados_md_faltando).

    `referencias` e {codigo: {arquivo: n}}; `definicoes` e {codigo: [arquivo]}.

    `ignorar` e PARAMETRO e nao global capturado, pela licao do E-02: quem quer a linha de
    base **pede** por ela. Foi o proprio teste de mutacao que cobrou -- ele usa um codigo
    ficticio que precisa estar na exclusao da arvore real e FORA dela dentro do teste, e
    com a global isso era impossivel sem mascarar um dos dois lados."""
    ignorar = NAO_SAO_ACHADOS if ignorar is None else ignorar
    refs = collections.defaultdict(collections.Counter)
    defs = collections.defaultdict(list)
    tem_achados = False
    for caminho in arquivos(raiz):
        nome = os.path.relpath(caminho, raiz).replace("\\", "/")
        if nome.upper().endswith("ACHADOS.MD"):
            tem_achados = True
        with io.open(caminho, encoding="utf-8", errors="replace") as f:
            s = f.read()
        for m in REF.finditer(s):
            cod = f"{m.group(1)}-{m.group(2)}"
            if not conta_como_codigo(cod, ignorar):
                continue
            refs[cod][nome] += 1
        if nome.endswith(".md"):
            for p in (DEF_CABECALHO, DEF_INDICE):
                for m in p.finditer(s):
                    defs[f"{m.group(1)}-{m.group(2)}"].append(nome)
    return refs, defs, not tem_achados


def orfaos(refs, defs):
    """Achado citado e sem endereco. A contagem que DECAI: ela so encolhe quando alguem
    escreve a definicao, e sobe no minuto em que um corte leva o texto sem deixar ancora."""
    return {c: dict(onde) for c, onde in refs.items() if c not in defs}


def relatorio(raiz=".", saida=sys.stdout):
    refs, defs, falta_achados = varrer(raiz)
    orf = orfaos(refs, defs)
    print(f"{len(refs)} achados citados · {len(defs)} com definicao · "
          f"{len(orf)} SEM ENDERECO", file=saida)
    if falta_achados:
        print("\nAVISO: nao ha ACHADOS.md nesta arvore. A lista abaixo esta INCOMPLETA por\n"
              "  ausencia de arquivo, nao por estar tudo ancorado -- fechar verde aqui\n"
              "  seria o F-02 nesta camada.", file=saida)
    for cod in sorted(orf, key=lambda c: (c[0], int(c.split("-")[1]))):
        citacoes = ", ".join(f"{a}×{n}" for a, n in sorted(orf[cod].items())[:4])
        print(f"  {cod:<7} citado em {citacoes}", file=saida)
    if orf:
        print("\n  Cada um destes e um nome que a proxima sessao le e nao pode consultar.\n"
              "  Ou ele ganha definicao (cabecalho ou linha de indice) num .md, ou entra em\n"
              "  NAO_SAO_ACHADOS com o motivo ao lado.", file=saida)
    return orf, falta_achados


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--raiz", default=os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    a = p.parse_args(argv)
    orf, _falta = relatorio(a.raiz)
    return 1 if orf else 0


if __name__ == "__main__":
    raise SystemExit(main())

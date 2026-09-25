#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""materializar_acervo.py -- poe em `data/bronze/` o que o armazem tem, pelo `acervo.abrir`.

POR QUE ELE EXISTE (metricas, 25/09/2026). Os testes contra o acervo real leem por caminho
(`data/bronze/b3/cotahist/...`), e o job semanal do GitHub nao tem o disco dele. Este
comando abre cada arquivo conhecido -- a versao VIGENTE, conferida pelo sha256 -- e o copia
para o caminho que os testes leem. O silver nao esta no armazem, e por isso fica fora: os
testes dele pulam no job, visivelmente (`exigir_acervo`, pasta por acervo).

O QUE ELE ACUSA, e e o motivo de existir tanto quanto a copia: arquivo que o registro ou o
inventario dizem existir e o armazem NAO entrega. A captura local sem `--armazem` produz
exatamente isso (CV-07): o registro anota a versao, o portao da rodada seguinte a da como
`inalterado`, e o byte nunca sobe. A lista vai para `--faltas`, e o job fica vermelho no fim,
depois de rodar os testes -- a falha e visivel e nao esconde o resto do resultado.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import acervo  # noqa: E402
import insumo_ml  # noqa: E402


def conhecidos(repo=None):
    """{(fonte, recurso, arquivo)} de todo inventario e registro de captura."""
    repo = repo or acervo.raiz_repo()
    out = set()
    for ln in acervo._inventarios(repo):
        out.add((ln["fonte"], ln["recurso"], ln["arquivo"]))
    for fonte, rel in acervo.REGISTROS.items():
        for ln in acervo._ler(os.path.join(repo, rel)):
            if ln.get("sha256") and ln.get("situacao") in acervo.VIGENTES:
                out.add((fonte, ln["recurso"], ln["arquivo"]))
    return out


def materializar(itens, repo, abrir=None):
    """Copia cada item para `data/bronze/<fonte>/<recurso>/<arquivo>`. Devolve (copiados,
    ja_estavam, faltas). Idempotente: o que ja esta no lugar nao e copiado de novo."""
    abrir = abrir or acervo.abrir
    copiados, ja, faltas = [], [], []
    for fonte, recurso, arquivo in sorted(itens):
        destino = os.path.join(repo, "data", "bronze", fonte, recurso, arquivo)
        try:
            origem = abrir(recurso, arquivo)
        except Exception as e:
            faltas.append(f"{fonte}/{recurso}/{arquivo}: {type(e).__name__}: {e}")
            continue
        if os.path.abspath(origem) == os.path.abspath(destino):
            ja.append(destino)
            continue
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy2(origem, destino)
        copiados.append(destino)
    return copiados, ja, faltas


def fixados(repo=None):
    """{(recurso, arquivo, sha256)} de toda versao FIXADA pelo pre-registro do ML (P-139).

    CI-04: o leitor do ML abre a versao fixada, nao a vigente. Quando a captura traz outra
    versao (2026, em 24/09), a fixada deixa de estar em `data/bronze/`, e o leitor vai ao
    armazem -- e no passo dos testes nao ha segredo. Ela entra no cache `data/armazem/`
    aqui, no unico passo que tem as credenciais."""
    repo = repo or acervo.raiz_repo()
    pins = insumo_ml.carregar_pins(os.path.join(repo, insumo_ml.PINS_RELATIVO))
    return {(insumo_ml.RECURSO, p["arquivo"], p["sha256"])
            for p in (pins.get("cotahist") or {}).values()}


def materializar_fixados(itens, abrir=None):
    """Poe cada versao fixada onde o `acervo.abrir` a acha sem rede. Devolve (prontos,
    faltas). O que ja esta em disco com o mesmo sha256 nao e baixado."""
    abrir = abrir or acervo.abrir
    prontos, faltas = [], []
    for recurso, arquivo, sha in sorted(itens):
        try:
            prontos.append(abrir(recurso, arquivo, sha, conferir=True))
        except Exception as e:
            faltas.append(f"fixado {recurso}/{arquivo}@{sha[:12]}: {type(e).__name__}: {e}")
    return prontos, faltas


# Onde o motor le os fatores do NEFIN (alocacao/fatores.py -> ARQUIVO), e a chave da politica
# que fixa a versao que o pre-registro usou.
NEFIN_DESTINO = os.path.join("alocacao", "dados", "nefin_factors.csv")
NEFIN_RECURSO, NEFIN_ARQUIVO = "risk_factors", "nefin_factors.csv"


def nefin_fixado(repo=None):
    """O prefixo de sha256 da serie do NEFIN que o pre-registro usou:
    `politica.yaml -> pesquisa.fonte.sha256_12`. Sem ele, levanta: materializar a vigente
    no lugar da fixada trocaria o insumo do pre-registro em silencio (F-02)."""
    import yaml
    repo = repo or acervo.raiz_repo()
    with open(os.path.join(repo, "alocacao", "politica.yaml"), encoding="utf-8") as f:
        pol = yaml.safe_load(f)
    sha = ((pol.get("pesquisa") or {}).get("fonte") or {}).get("sha256_12")
    if not sha:
        raise KeyError("politica.yaml -> pesquisa.fonte.sha256_12 ausente")
    return str(sha)


def materializar_nefin(repo=None, abrir=None):
    """Poe a serie FIXADA do NEFIN onde o motor a le. Devolve (caminho ou None, faltas).

    O CSV saiu do git em 25/09/2026 (termos do NEFIN, docs/fontes/nefin.md): no clone ele
    nao existe, e este passo o traz do armazem pelo sha256 do pre-registro."""
    repo = repo or acervo.raiz_repo()
    abrir = abrir or acervo.abrir
    destino = os.path.join(repo, NEFIN_DESTINO)
    try:
        origem = abrir(NEFIN_RECURSO, NEFIN_ARQUIVO, nefin_fixado(repo), conferir=True)
    except Exception as e:
        return None, [f"nefin {NEFIN_ARQUIVO}: {type(e).__name__}: {e}"]
    if os.path.abspath(origem) != os.path.abspath(destino):
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy2(origem, destino)
    return destino, []


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--faltas", help="grava aqui a lista do que o armazem nao entregou")
    a = ap.parse_args(argv)
    repo = acervo.raiz_repo()
    copiados, ja, faltas = materializar(conhecidos(repo), repo)
    prontos, faltas_fix = materializar_fixados(fixados(repo))
    faltas += faltas_fix
    _nefin, faltas_nefin = materializar_nefin(repo)
    faltas += faltas_nefin
    print(f"materializados {len(copiados)}, ja no lugar {len(ja)}, "
          f"fixados prontos {len(prontos)}, FALTAS {len(faltas)}")
    for f in faltas:
        print(f"  FALTA  {f}")
    if a.faltas:
        with open(a.faltas, "w", encoding="utf-8") as fh:
            fh.write("".join(f + "\n" for f in faltas))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O COTAHIST que a familia ML le: a versao FIXADA pelo pre-registro, nunca a vigente.

POR QUE ELE EXISTE (P-139, CH-01). O `preregistro-ml-v2.md` fixa o `COTAHIST_A2026.ZIP`
em `fb3546ed...`. Desde a captura de 24/09 o `acervo.versoes()` marca `4f2cf2aa...` como
vigente, e o `calendario.arquivos()` le o que estiver no disco sem conferir hash nenhum.
Sem este modulo, o ML leria uma versao nesta maquina e outra numa que abrisse a vigente
pelo armazem -- e ninguem veria, porque as duas sao COTAHIST validos.

O QUE ELE FAZ, para um ano fixado em `docs/aprendizado/preregistro-ml-v2.pins.yaml`:
  1. abre pelo `acervo.abrir(..., versao=<sha256 fixado>, conferir=True)` -- o byte
     fixado, conferido, venha do cache, do disco ou do armazem;
  2. confere o tamanho declarado;
  3. mede a IMPRESSAO DE CONTEUDO da janela (sha256 das linhas TIPREG=01 ate a data,
     ORDENADAS) e compara com a declarada. Diferente levanta `InsumoBloqueado` (P1).
A impressao e o que sobrevive ao CH-01: a B3 regera o anual reordenando as linhas, o sha256
do ZIP muda e o conteudo nao. Ordenar antes do hash e o que torna a medida independente
da ordem -- e so dela.

ANO SEM PIN. O pre-registro so fixou 2026. Para os outros anos a leitura sai da versao
vigente, com o sha256 ao lado e `fixado=False`: a procedencia viaja com o resultado, e
bloquear aqui seria inventar uma regra que o pre-registro nao tem. Fixar 2010-2025 e
decisao (P-140).

O QUE ELE NAO MEDE (P5):
  - a impressao cobre a JANELA declarada, nao o arquivo: linhas depois de `ate` podem
    mudar sem que ela veja -- e e de proposito, o teste do pre-registro termina ali;
  - ela prova o mesmo MULTICONJUNTO de linhas. Codigo do ML que dependa da ORDEM das
    linhas (primeira ocorrencia vence, groupby sem ordenar) pode dar numero diferente
    entre duas versoes com a mesma impressao. Quem le tem de ordenar;
  - medir custa ler o membro inteiro (~700 MB, dezenas de segundos). E feito uma vez por
    processo e por (caminho, sha256).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import os
import sys
from dataclasses import dataclass

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import acervo  # noqa: E402
import calendario  # noqa: E402

PINS_RELATIVO = os.path.join("docs", "aprendizado", "preregistro-ml-v2.pins.yaml")
RECURSO = "cotahist"


class InsumoBloqueado(Exception):
    """P1: o insumo nao e o que o pre-registro fixou, e o calculo recusa-se a rodar."""


@dataclass(frozen=True)
class Leitura:
    caminho: str
    ano: int
    sha256: str
    fixado: bool          # True: a versao do pre-registro, conferida; False: a vigente


def carregar_pins(caminho=None):
    caminho = caminho or os.path.join(acervo.raiz_repo(), PINS_RELATIVO)
    with open(caminho, encoding="utf-8") as f:
        pins = yaml.safe_load(f)
    return pins


def impressao(caminho, ate):
    """(sha256, registros, pregoes) das linhas TIPREG=01 com DATA <= `ate`, ordenadas.

    As linhas entram sem terminador, em latin-1, unidas por CRLF -- a forma da medicao do
    CH-01, para que o numero seja o mesmo que esta no `pins.yaml`."""
    a, b = calendario.pos("DATA")
    limite = ate.strftime("%Y%m%d")
    linhas = []
    for raw in calendario.registros(caminho):
        if raw[a:b] <= limite:
            linhas.append(raw.rstrip("\r\n").encode("latin-1"))
    linhas.sort()
    dias = {ln[a:b] for ln in linhas}
    return hashlib.sha256(b"\r\n".join(linhas)).hexdigest(), len(linhas), len(dias)


_CONFERIDAS: set = set()


def _conferir(caminho, pin, ano):
    tam = os.path.getsize(caminho)
    if tam != pin["bytes"]:
        raise InsumoBloqueado(f"COTAHIST {ano}: {tam} bytes, o pre-registro fixou "
                              f"{pin['bytes']}")
    imp = pin["impressao"]
    chave = (caminho, pin["sha256"], str(imp["ate"]))
    if chave in _CONFERIDAS:
        return
    ate = imp["ate"] if isinstance(imp["ate"], dt.date) else dt.date.fromisoformat(
        str(imp["ate"]))
    medido = impressao(caminho, ate)
    declarado = (imp["sha256"], imp["registros"], imp["pregoes"])
    if medido != declarado:
        raise InsumoBloqueado(
            f"COTAHIST {ano}: impressao da janela ate {ate} medida {medido}, fixada "
            f"{declarado}. O byte e o fixado (sha256 conferido) e o conteudo nao e o "
            f"declarado: o pins.yaml ou o leitor mudou. Nao se le ate explicar qual.")
    _CONFERIDAS.add(chave)


def abrir_cotahist(ano, *, pins=None, abrir=None):
    """A `Leitura` do COTAHIST de `ano` para a familia ML. `abrir` e injetavel para teste
    (assinatura do `acervo.abrir`)."""
    pins = pins if pins is not None else carregar_pins()
    abrir = abrir or acervo.abrir
    arquivo = f"COTAHIST_A{int(ano)}.ZIP"
    pin = (pins.get("cotahist") or {}).get(int(ano))
    if pin is None:
        caminho = abrir(RECURSO, arquivo)
        vigente = [v for v in acervo.versoes(RECURSO, arquivo) if v["vigente"]]
        sha = vigente[0]["sha256"] if vigente else acervo.armazem_mod.sha256(caminho)
        return Leitura(caminho, int(ano), sha, fixado=False)
    if pin["arquivo"] != arquivo:
        raise InsumoBloqueado(f"pins.yaml: o ano {ano} aponta para {pin['arquivo']!r}")
    try:
        caminho = abrir(RECURSO, arquivo, pin["sha256"], conferir=True)
    except (acervo.VersaoDesconhecida, OSError) as e:
        raise InsumoBloqueado(
            f"COTAHIST {ano}: a versao fixada por {pins['preregistro']} "
            f"({pin['sha256'][:12]}) nao pode ser aberta: {type(e).__name__}: {e}. "
            f"A vigente NAO a substitui.") from e
    _conferir(caminho, pin, ano)
    return Leitura(caminho, int(ano), pin["sha256"], fixado=True)


def main(argv=None):
    """Confere os anos fixados. Sai 0 se todos conferem, 1 se algum esta bloqueado."""
    pins = carregar_pins()
    ruim = 0
    for ano in sorted(pins["cotahist"]):
        try:
            lt = abrir_cotahist(ano, pins=pins)
            print(f"{ano}  FIXADO  {lt.sha256[:12]}  {lt.caminho}")
        except InsumoBloqueado as e:
            ruim = 1
            print(f"{ano}  BLOQUEADO  {e}")
    return ruim


if __name__ == "__main__":
    raise SystemExit(main())

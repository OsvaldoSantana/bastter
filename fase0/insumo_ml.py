#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O COTAHIST que a familia ML le: a versao FIXADA pelo pre-registro, nunca a vigente.

POR QUE ELE EXISTE (P-139, CH-01). O `preregistro-ml-v2.md` fixa o `COTAHIST_A2026.ZIP`
em `fb3546ed...`. Desde a captura de 24/09 o `acervo.versoes()` marca `4f2cf2aa...` como
vigente, e o `calendario.arquivos()` le o que estiver no disco sem conferir hash nenhum.
Sem este modulo, o ML leria uma versao nesta maquina e outra numa que abrisse a vigente
pelo armazem -- e ninguem veria, porque as duas sao COTAHIST validos.

O QUE ELE FAZ, para um ano fixado em `docs/aprendizado/preregistro-ml-v2.pins.yaml`
(2004 a 2026 desde a P-140; a hierarquia mudou ali):
  1. tenta o byte OBSERVADO: `acervo.abrir(..., versao=<sha256 do pin>, conferir=True)`,
     venha do cache, do disco ou do armazem, e confere o tamanho (secundario);
  2. se ele nao abre, abre a VIGENTE -- e quem decide e o passo 3;
  3. mede a IMPRESSAO DE CONTEUDO da janela (sha256 das linhas TIPREG=01 ate a data,
     ORDENADAS) e compara com a declarada -- o PINO PRINCIPAL. Diferente levanta
     `InsumoBloqueado` (P1). Igual com sha256 diferente (caminho 2): `AvisoRecompressao`,
     registrado na `Leitura`, e segue.
A impressao e o que sobrevive ao CH-01: a B3 regera o anual reordenando as linhas, o sha256
do ZIP muda e o conteudo nao. Ordenar antes do hash e o que torna a medida independente
da ordem -- e so dela.

ANO SEM PIN. A leitura sai da versao vigente, com o sha256 ao lado e `fixado=False`: a
procedencia viaja com o resultado. `--medir A-B` produz o pin de um ano novo.

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
import time
import warnings
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


class AvisoRecompressao(UserWarning):
    """P-140: o byte observado nao esta disponivel, e a versao lida tem OUTRO sha256 com a
    MESMA impressao de conteudo (CH-01). Segue -- e fica registrado na `Leitura`."""


@dataclass(frozen=True)
class Leitura:
    caminho: str
    ano: int
    sha256: str           # o sha256 do byte efetivamente lido
    fixado: bool          # True: impressao do pre-registro conferida; False: sem pin
    aviso: str = ""       # nao vazio: sha256 diferente do observado, impressao igual


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


def _ate(imp):
    a = imp["ate"]
    return a if isinstance(a, dt.date) else dt.date.fromisoformat(str(a))


def medir_pin(caminho, ano, ate=None):
    """O pin de um ano, MEDIDO no byte em `caminho` (P-140). `ate` padrao: 31/12 do ano.
    E a mesma medida que `_conferir_impressao` refaz -- quem escreve o pin e quem o
    confere usam uma funcao so (N-01)."""
    ate = ate or dt.date(int(ano), 12, 31)
    sha, n, dias = impressao(caminho, ate)
    return dict(arquivo=f"COTAHIST_A{int(ano)}.ZIP",
                sha256=acervo.armazem_mod.sha256(caminho),
                bytes=os.path.getsize(caminho),
                impressao=dict(ate=ate, registros=n, pregoes=dias, sha256=sha))


def _conferir_tamanho(caminho, pin, ano):
    """Secundario: so vale quando o byte aberto E o observado (mesmo sha256)."""
    tam = os.path.getsize(caminho)
    if tam != pin["bytes"]:
        raise InsumoBloqueado(f"COTAHIST {ano}: {tam} bytes, o pre-registro fixou "
                              f"{pin['bytes']}")


def _conferir_impressao(caminho, pin, ano):
    """O pino PRINCIPAL. Diferente levanta, venha o byte de onde vier."""
    imp = pin["impressao"]
    chave = (caminho, pin["sha256"], str(imp["ate"]))
    if chave in _CONFERIDAS:
        return
    ate = _ate(imp)
    medido = impressao(caminho, ate)
    declarado = (imp["sha256"], imp["registros"], imp["pregoes"])
    if medido != declarado:
        raise InsumoBloqueado(
            f"COTAHIST {ano}: impressao da janela ate {ate} medida {medido}, fixada "
            f"{declarado}. O conteudo lido nao e o declarado: o dado, o pins.yaml ou o "
            f"leitor mudou. Nao se le ate explicar qual.")
    _CONFERIDAS.add(chave)


def abrir_cotahist(ano, *, pins=None, abrir=None):
    """A `Leitura` do COTAHIST de `ano` para a familia ML. `abrir` e injetavel para teste
    (assinatura do `acervo.abrir`).

    P-140, a hierarquia do pin: a IMPRESSAO de conteudo e o pino principal; o sha256 e os
    bytes sao o observado, secundario. O leitor tenta primeiro o byte observado -- e o
    unico que garante tambem a ORDEM das linhas (ver P5 no topo). Se ele nao pode ser
    aberto, abre a vigente e deixa a impressao decidir: igual, segue com `AvisoRecompressao`
    (a B3 recomprime sem mudar conteudo, CH-01); diferente, `InsumoBloqueado`."""
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
        motivo = f"{type(e).__name__}: {e}"
    else:
        _conferir_tamanho(caminho, pin, ano)
        _conferir_impressao(caminho, pin, ano)
        return Leitura(caminho, int(ano), pin["sha256"], fixado=True)
    try:
        caminho = abrir(RECURSO, arquivo)
    except (acervo.VersaoDesconhecida, OSError) as e:
        raise InsumoBloqueado(
            f"COTAHIST {ano}: nem o byte observado ({pin['sha256'][:12]}: {motivo}) nem a "
            f"vigente ({type(e).__name__}: {e}) podem ser abertos.") from e
    sha = acervo.armazem_mod.sha256(caminho)
    _conferir_impressao(caminho, pin, ano)
    aviso = ""
    if sha != pin["sha256"]:
        aviso = (f"COTAHIST {ano}: lido {sha[:12]}, observado no pin {pin['sha256'][:12]} "
                 f"({motivo}); impressao de conteudo IGUAL, segue (CH-01). Codigo que "
                 f"dependa da ordem das linhas tem de ordenar.")
        warnings.warn(aviso, AvisoRecompressao, stacklevel=2)
    return Leitura(caminho, int(ano), sha, fixado=True, aviso=aviso)


def main(argv=None):
    """Confere os anos fixados. Sai 0 se todos conferem, 1 se algum esta bloqueado.

    `--medir A-B` mede os pins de A a B na versao VIGENTE e imprime o bloco YAML, com o
    tempo de cada leitura. Nao escreve no pins.yaml: fixar e um commit, nao um efeito
    colateral de rodar o comando."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["--medir"]:
        a, b = (int(x) for x in argv[1].split("-"))
        total = time.perf_counter()
        for ano in range(a, b + 1):
            t0 = time.perf_counter()
            p = medir_pin(acervo.abrir(RECURSO, f"COTAHIST_A{ano}.ZIP"), ano)
            imp = p["impressao"]
            print(f"  {ano}:\n    arquivo: {p['arquivo']}\n    sha256: {p['sha256']}\n"
                  f"    bytes: {p['bytes']}\n    impressao:\n      ate: {imp['ate']}\n"
                  f"      registros: {imp['registros']}\n      pregoes: {imp['pregoes']}\n"
                  f"      sha256: {imp['sha256']}\n"
                  f"    # medido em {time.perf_counter() - t0:.1f} s")
        print(f"# total {time.perf_counter() - total:.1f} s", file=sys.stderr)
        return 0
    pins = carregar_pins()
    ruim = 0
    for ano in sorted(pins["cotahist"]):
        try:
            lt = abrir_cotahist(ano, pins=pins)
            print(f"{ano}  FIXADO  {lt.sha256[:12]}  {lt.caminho}"
                  + (f"  AVISO {lt.aviso}" if lt.aviso else ""))
        except InsumoBloqueado as e:
            ruim = 1
            print(f"{ano}  BLOQUEADO  {e}")
    return ruim


if __name__ == "__main__":
    raise SystemExit(main())

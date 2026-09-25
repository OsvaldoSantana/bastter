#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Captura dos fatores de risco do NEFIN -- o mesmo armazem, portao e teto da CVM e da B3.

POR QUE ELE EXISTE (25/09/2026). O `alocacao/dados/nefin_factors.csv` estava no git. Os
termos do NEFIN, lidos na fonte em 25/09 (`docs/fontes/nefin.md`), dizem que o dado e livre
para uso, pedem citacao em trabalho publicado e reservam todos os direitos -- nao autorizam
redistribuir. O arquivo saiu do git (mesma logica da P-136) e passou a morar no armazem, e
esta rotina o observa como a da CVM observa a DFP: HEAD, e GET so quando o portao abre.

MEDIDO ANTES DE ESCREVER (25/09/2026):
    https://nefin.com.br/nefindata/risk-factors/nefin_factors.csv
    200, 882.144 bytes, text/csv, Last-Modified 17/09/2026 14:48:15 GMT,
    sha256 619991c2192c... -- o MESMO arquivo que o pre-registro usa.
    O endereco antigo (`/resources/risk_factors/nefin_factors.csv`) responde 404.

A versao que o motor le NAO e a vigente: e a fixada em `politica.yaml -> pesquisa.fonte`,
posta no lugar pelo `materializar_acervo.py`. Quando o NEFIN publicar adiante, a nova versao
entra no registro e no armazem, e o pre-registro continua lendo a sua.

  python fase0/capturar_nefin.py --armazem s3          # o que o workflow roda
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.error
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import armazem as armazem_mod  # noqa: E402
import capturar_cvm as C  # noqa: E402

URL = "https://nefin.com.br/nefindata/risk-factors/nefin_factors.csv"
FONTE = "nefin"
RECURSO = "risk_factors"
LOGS = "logs/capturas_nefin"   # separado: o frescor le o ultimo log de cada fonte
RAIZ_RELATIVA = os.path.join("data", "bronze", "nefin")
REGISTRO_RELATIVO = os.path.join("docs", "acervo", "nefin", "capturas.csv")


def main(argv=None, abrir=urllib.request.urlopen, dormir=time.sleep, armazem=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--armazem", choices=["s3"], required=True,
                   help="credenciais so por variavel de ambiente R2_*")
    p.add_argument("--raiz", default=None, help=f"padrao: {RAIZ_RELATIVA}")
    p.add_argument("--registro", default=None, help=f"padrao: {REGISTRO_RELATIVO}")
    p.add_argument("--cache", default=None, help="guarda tambem uma copia em <cache>/<chave>")
    p.add_argument("--raiz-repo", default=None, help=argparse.SUPPRESS)  # testes
    a = p.parse_args(argv)
    base = a.raiz_repo or C.raiz_repo()
    raiz = os.path.abspath(a.raiz or os.path.join(base, RAIZ_RELATIVA))
    registro = a.registro or os.path.join(base, REGISTRO_RELATIVO)
    armazem = armazem or armazem_mod.do_ambiente(a.armazem)

    estado = C.estado_do_registro(C.ler_registro(registro))
    C.relatar_ocupacao(armazem, raiz=a.raiz_repo)
    diario = []
    nome = URL.rsplit("/", 1)[-1]
    try:
        s = C.capturar_para_armazem(URL, RECURSO, raiz, registro, estado, armazem,
                                    abrir=abrir, dormir=dormir, cache=a.cache,
                                    diario=diario, fonte=FONTE)
    except urllib.error.HTTPError as e:
        s = _erro(registro, diario, nome, f"HTTP {e.code} {e.reason}")
    except (urllib.error.URLError, OSError) as e:
        s = _erro(registro, diario, nome, str(e))
    print(f"{s}")
    print(f"log: {C.enviar_diario(armazem, diario, prefixo=LOGS)}")
    return 1 if s in (C.ERRO, C.REJEITADO, C.RECUSADO_POR_TETO) else 0


def _erro(registro, diario, nome, motivo):
    """Uma URL so, e ela e a fonte inteira: 404 aqui e erro, nunca 'ausente'."""
    print(f"[!] {URL}  ERRO: {motivo}", file=sys.stderr)
    linha = dict(dt_captura=C.agora(), recurso=RECURSO, url=URL, arquivo=nome,
                 situacao=C.ERRO, motivo=motivo)
    C.anotar(registro, linha)
    diario.append(linha)
    return C.ERRO


if __name__ == "__main__":
    raise SystemExit(main())

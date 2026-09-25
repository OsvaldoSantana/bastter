#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Captura do COTAHIST na nuvem (P-135) -- o mesmo armazem, o mesmo portao e o mesmo teto
da captura da CVM.

MEDIDO ANTES DE ESCREVER (24/09/2026). Do runner do GitHub e da maquina dele, identico
(`fase0/sondar_cotahist.py`, execucao 36043565046):

    COTAHIST_A2026.ZIP     200   84.469.516 bytes
    COTAHIST_D<dia>.ZIP    200   463.627 a 652.381 bytes (os 5 pregoes de 17 a 23/09)
    D07092026 feriado, D20092026 domingo, D24092026 ainda nao publicado:
                           404 nos tres, Content-Type text/html -- a MESMA resposta

O QUE ELE CAPTURA:
  - o DIARIO de cada dia util (seg-sex) dos ultimos DIAS_PARA_TRAS dias antes de hoje,
    toda rodada. O portao HEAD fecha os que ja estao no registro; a janela maior que um
    dia e para que uma rodada perdida (runner fora, cron atrasado) nao perca pregao.
  - o ANUAL uma vez por mes: na primeira rodada do mes, o `A<ano>` do mes que acabou,
    que ja traz o ultimo pregao dele. E o arquivo de CONCILIACAO: tem todo pregao, e so
    ele separa "feriado" de "diario que nao foi publicado". A primeira rodada de todas o
    captura tambem -- e a linha de base dessa conciliacao.
  - NAO o anual todo dia: ~85 MB x ~250 pregoes/ano passaria dos 10 GB gratis do R2 em
    poucos meses (e o teto do armazem recusaria antes). O diario mede ~0,5 MB.

O 404 DO DIARIO NAO E ERRO, e tambem nao e "nada mudou". A B3 responde igual para feriado,
fim de semana e dia ainda nao publicado, entao o 404 vira a linha `ausente` no LOG da
rodada, com o motivo escrito -- e o job nao fica vermelho por um feriado. Este modulo NAO
conhece feriado e nao inventa lista (o calendario do projeto vem do proprio COTAHIST,
`calendario.py`). Quem distingue e a conciliacao contra o anual, que ainda nao existe
(P-137). No ANUAL, 404 e erro.

  python fase0/capturar_cotahist.py --armazem s3          # o que o workflow roda
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
import time
import urllib.error
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import armazem as armazem_mod  # noqa: E402
import capturar_cvm as C  # noqa: E402

BASE = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/"
FONTE = "b3"
ANUAL, DIARIO = "cotahist", "cotahist_diario"   # ANUAL e o recurso da carga inicial
DIAS_PARA_TRAS = 7
AUSENTE = "ausente"
LOGS = "logs/capturas_b3"      # separado do da CVM: o frescor le o ultimo log de cada um
RAIZ_RELATIVA = os.path.join("data", "bronze", "b3")
REGISTRO_RELATIVO = os.path.join("docs", "acervo", "b3", "capturas.csv")
MOTIVO_404 = ("HTTP 404: feriado, fim de semana ou ainda nao publicado -- a B3 responde "
              "igual aos tres; quem distingue e a conciliacao com o anual")


def diarios(hoje, dias=DIAS_PARA_TRAS):
    """[(url, DIARIO)] dos dias uteis de `hoje - dias` a ontem, do mais antigo ao mais novo."""
    out = []
    for i in range(dias, 0, -1):
        d = hoje - dt.timedelta(days=i)
        if d.weekday() < 5:
            out.append((BASE + f"COTAHIST_D{d:%d%m%Y}.ZIP", DIARIO))
    return out


def anual_do_mes(hoje, linhas):
    """(url, ANUAL) se o registro nao tem o anual observado neste mes; senao None. O ano e
    o do mes que acabou: em janeiro, o anual de dezembro e o do ano anterior."""
    mes = f"{hoje:%Y-%m}"
    if any(ln.get("recurso") == ANUAL and (ln.get("dt_captura") or "").startswith(mes)
           for ln in linhas):
        return None
    ano = (hoje.replace(day=1) - dt.timedelta(days=1)).year
    return (BASE + f"COTAHIST_A{ano}.ZIP", ANUAL)


def main(argv=None, abrir=urllib.request.urlopen, dormir=time.sleep, armazem=None,
         hoje=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--armazem", choices=["s3", "local"], required=True,
                   help="s3: o R2 do projeto, credenciais so por R2_*; "
                        "local: uma pasta (ARMAZEM_LOCAL)")
    p.add_argument("--raiz", default=None, help=f"padrao: {RAIZ_RELATIVA}")
    p.add_argument("--registro", default=None, help=f"padrao: {REGISTRO_RELATIVO}")
    p.add_argument("--cache", default=None, help="guarda tambem uma copia em <cache>/<chave>")
    p.add_argument("--pausa", type=float, default=1.0, help="segundos entre requisicoes")
    p.add_argument("--raiz-repo", default=None, help=argparse.SUPPRESS)  # testes
    a = p.parse_args(argv)
    base = a.raiz_repo or C.raiz_repo()
    raiz = os.path.abspath(a.raiz or os.path.join(base, RAIZ_RELATIVA))
    registro = a.registro or os.path.join(base, REGISTRO_RELATIVO)
    armazem = armazem or armazem_mod.do_ambiente(a.armazem)
    hoje = hoje or dt.datetime.now(dt.timezone.utc).date()

    linhas = C.ler_registro(registro)
    estado = C.estado_do_registro(linhas)
    C.relatar_ocupacao(armazem, raiz=a.raiz_repo)
    alvos = diarios(hoje)
    anual = anual_do_mes(hoje, linhas)
    if anual:
        alvos.append(anual)

    diario, resumo = [], {}
    for url, recurso in alvos:
        nome = url.rsplit("/", 1)[-1]
        try:
            s = C.capturar_para_armazem(url, recurso, raiz, registro, estado, armazem,
                                        abrir=abrir, dormir=dormir, cache=a.cache,
                                        diario=diario, fonte=FONTE)
        except urllib.error.HTTPError as e:
            if e.code == 404 and recurso == DIARIO:
                s = AUSENTE
                diario.append(dict(dt_captura=C.agora(), recurso=recurso, arquivo=nome,
                                   url=url, situacao=AUSENTE, motivo=MOTIVO_404))
                print(f"[-] {nome}  ausente (404)")
            else:
                s = C.ERRO
                _erro(registro, diario, recurso, url, nome, f"HTTP {e.code} {e.reason}")
        except (urllib.error.URLError, OSError) as e:
            s = C.ERRO
            _erro(registro, diario, recurso, url, nome, str(e))
        resumo[s] = resumo.get(s, 0) + 1
        if a.pausa:
            dormir(a.pausa)
    print("  ".join(f"{k} {v}" for k, v in sorted(resumo.items())))
    print(f"log: {C.enviar_diario(armazem, diario, prefixo=LOGS)}")
    falhou = sum(resumo.get(k, 0) for k in (C.ERRO, C.REJEITADO, C.RECUSADO_POR_TETO))
    if falhou:
        print(f"{falhou} falha(s)", file=sys.stderr)
        return 1
    return 0


def _erro(registro, diario, recurso, url, nome, motivo):
    print(f"[!] {url}  ERRO: {motivo}", file=sys.stderr)
    linha = dict(dt_captura=C.agora(), recurso=recurso, url=url, arquivo=nome,
                 situacao=C.ERRO, motivo=motivo)
    C.anotar(registro, linha)
    diario.append(linha)


if __name__ == "__main__":
    raise SystemExit(main())

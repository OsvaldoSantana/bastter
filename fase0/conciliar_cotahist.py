#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conciliacao dos diarios do COTAHIST contra o anual do mes (P-137).

POR QUE ELE EXISTE. A B3 responde o MESMO 404 para feriado, fim de semana e diario ainda nao
publicado (medido em 24/09/2026), e a captura registra `ausente` sem saber qual dos tres foi.
Sem conciliar, um diario perdido vira buraco calado na serie -- a forma do F-02, em que
ausencia de arquivo parece ausencia de pregao. O anual do mes tem todo pregao: e ele que
separa uma coisa da outra.

MEDIDO ANTES DE ESCREVER (25/09/2026): o diario tem o MESMO leiaute do anual -- header
`00COTAHIST.2026BOVESPA 20260924`, registros de 245 posicoes, trailer contando so os `01`
(15.903 em COTAHIST_D24092026.ZIP, sha256 7ef9fb0e...). Por isso a leitura e a do
`calendario.registros()`, a unica do projeto (N-01).

AS DUAS COMPARACOES, e as duas por MULTICONJUNTO de linhas do dia (CH-01: 4 dos 5 diarios de
17-23/09 tem outra ORDEM que o anual e o mesmo conteudo -- comparar na ordem do arquivo daria
divergencia falsa):
  1. diario x anual, pregao a pregao do mes;
  2. anual novo x anual anterior, nos pregoes em comum. E o que transforma o CH-01 (n = 1 par)
     numa serie: um dia que muda ali e REVISAO da B3.

SITUACOES (uma linha por pregao em `docs/acervo/b3/conciliacoes.csv`):
  CONFERE            diario e anual tem o mesmo multiconjunto
  DIVERGE            os dois existem e diferem                         -> falha
  SEM_DIARIO         pregao no anual, nenhum diario capturado          -> falha (P7)
  DIARIO_SEM_PREGAO  diario capturado de um dia que o anual nao tem    -> falha
  ANTES_DA_ROTINA    pregao anterior ao primeiro diario ja capturado -- a rotina nao existia,
                     e a ausencia e esperada, nao perda
  REVISADO           dia em comum cujo conteudo mudou entre dois anuais (informacao, nao
                     falha: a B3 revisar e o mundo, nao defeito nosso)

IDEMPOTENTE: se o CSV ja tem a conciliacao deste mes contra esta versao do anual, nao refaz.
Se o anual do mes ainda nao foi capturado (a captura o traz na primeira rodada do mes
seguinte), diz isso e sai 0.

  python fase0/conciliar_cotahist.py --armazem s3               # o mes anterior a hoje
  python fase0/conciliar_cotahist.py --armazem s3 --mes 2026-09
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import acervo  # noqa: E402
import calendario  # noqa: E402

ANUAL, DIARIO = "cotahist", "cotahist_diario"      # os recursos do capturar_cotahist.py
REGISTRO_RELATIVO = os.path.join("docs", "acervo", "b3", "capturas.csv")
RESULTADO_RELATIVO = os.path.join("docs", "acervo", "b3", "conciliacoes.csv")
COLUNAS = ("dt_conciliacao", "competencia", "data", "situacao", "anual_sha256",
           "anual_anterior_sha256", "n_linhas_anual", "n_linhas_outro", "detalhe")
FALHAS = ("DIVERGE", "SEM_DIARIO", "DIARIO_SEM_PREGAO")


def impressao(linhas):
    """sha256 do multiconjunto: as linhas ordenadas, sem o fim de linha."""
    corpo = "\n".join(sorted(ln.rstrip("\r\n") for ln in linhas))
    return hashlib.sha256(corpo.encode("latin-1")).hexdigest()


def por_dia(caminho):
    """{data: [linhas de cotacao]} de um COTAHIST, anual ou diario."""
    out = {}
    for raw in calendario.registros(caminho):
        d = calendario.data_de(raw)
        if d is not None:
            out.setdefault(d, []).append(raw)
    return out


def data_do_diario(arquivo):
    """`COTAHIST_D24092026.ZIP` -> date(2026, 9, 24); None se o nome nao e de diario."""
    nome = os.path.basename(arquivo).upper()
    if not (nome.startswith("COTAHIST_D") and len(nome) >= 18):
        return None
    try:
        return dt.datetime.strptime(nome[10:18], "%d%m%Y").date()
    except ValueError:
        return None


def conciliar(anual, diarios, inicio_da_rotina):
    """[{data, situacao, n_anual, n_diario}] do mes, em ordem de data. `anual` e `diarios` sao
    {data: [linhas]} ja restritos ao mes; `inicio_da_rotina` e o primeiro diario capturado."""
    out = []
    for d in sorted(set(anual) | set(diarios)):
        a, b = anual.get(d), diarios.get(d)
        if a is not None and b is not None:
            s = "CONFERE" if impressao(a) == impressao(b) else "DIVERGE"
        elif a is not None:
            s = ("ANTES_DA_ROTINA" if inicio_da_rotina is None or d < inicio_da_rotina
                 else "SEM_DIARIO")
        else:
            s = "DIARIO_SEM_PREGAO"
        out.append(dict(data=d, situacao=s, n_anual=len(a or ()), n_diario=len(b or ())))
    return out


def comparar_anuais(novo, antigo):
    """(n_dias_em_comum, [datas revisadas]) entre duas versoes do anual."""
    comuns = sorted(set(novo) & set(antigo))
    return len(comuns), [d for d in comuns if impressao(novo[d]) != impressao(antigo[d])]


def _ler_csv(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def _anotar(caminho, linhas):
    novo = not os.path.exists(caminho)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, delimiter=";", lineterminator="\n")
        if novo:
            w.writeheader()
        w.writerows(linhas)


def _mes_anterior(hoje):
    return (hoje.replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m")


def main(argv=None, armazem=None, hoje=None, repo=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--armazem", choices=["s3", "local"], default=None,
                   help="de onde abrir o byte que nao estiver no cache (acervo.abrir)")
    # o dest nao e o nome da opcao: `a.<nome>` casaria com `politica.yaml -> revisao.mes`
    # e esconderia a divida P-28 dos dois instrumentos de cobertura (a leitura e por nome)
    p.add_argument("--mes", dest="competencia", default=None,
                   help="AAAA-MM; padrao: o mes anterior a hoje")
    a = p.parse_args(argv)
    repo = repo or acervo.raiz_repo()
    hoje = hoje or dt.datetime.now(dt.timezone.utc).date()
    mes = a.competencia or _mes_anterior(hoje)
    ano, m = (int(x) for x in mes.split("-"))
    fim_do_mes = (dt.date(ano, m, 28) + dt.timedelta(days=4)).replace(day=1)
    if armazem is None and a.armazem:
        import armazem as armazem_mod
        armazem = armazem_mod.do_ambiente(a.armazem)

    registro = _ler_csv(os.path.join(repo, REGISTRO_RELATIVO))
    arquivo_anual = f"COTAHIST_A{ano}.ZIP"
    # o anual que CONTEM o mes inteiro e o observado depois do fim dele
    # ordenadas pelo INSTANTE da observacao, nao pela ordem das linhas do registro: "a
    # anterior" e a observada antes, e depender da ordem do arquivo e certo por acidente
    todas = sorted(acervo.versoes(ANUAL, arquivo_anual, repo), key=lambda v: v["visto_em"])
    versoes = [v for v in todas if v["visto_em"][:10] >= fim_do_mes.isoformat()]
    if not versoes:
        print(f"{mes}: o anual {arquivo_anual} observado depois de {fim_do_mes} ainda nao "
              f"existe -- a captura o traz na primeira rodada do mes seguinte. Nada a fazer.")
        return 0
    anual_v = versoes[-1]
    resultado = os.path.join(repo, RESULTADO_RELATIVO)
    if any(ln.get("competencia") == mes and ln.get("anual_sha256") == anual_v["sha256"]
           for ln in _ler_csv(resultado)):
        print(f"{mes}: ja conciliado contra {anual_v['sha256'][:12]}. Nada a fazer.")
        return 0
    anteriores = [v for v in todas if v["visto_em"] < anual_v["visto_em"]]

    def _abrir(recurso, arquivo, sha):
        return acervo.abrir(recurso, arquivo, sha[:16], armazem=armazem, repo=repo)

    anual_todo = por_dia(_abrir(ANUAL, arquivo_anual, anual_v["sha256"]))
    anual = {d: v for d, v in anual_todo.items() if d.strftime("%Y-%m") == mes}

    capturados = {}                                   # data -> sha256 do diario vigente
    for ln in registro:
        if ln.get("recurso") == DIARIO and ln.get("sha256") and \
                ln.get("situacao") in acervo.VIGENTES:
            d = data_do_diario(ln.get("arquivo", ""))
            if d is not None:
                capturados[d] = (ln["arquivo"], ln["sha256"])
    inicio = min(capturados) if capturados else None
    diarios = {}
    for d, (arq, sha) in sorted(capturados.items()):
        if d.strftime("%Y-%m") == mes:
            diarios.update({k: v for k, v in por_dia(_abrir(DIARIO, arq, sha)).items()
                            if k == d})

    agora = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    linhas = [dict(dt_conciliacao=agora, competencia=mes, data=r["data"].isoformat(),
                   situacao=r["situacao"], anual_sha256=anual_v["sha256"],
                   anual_anterior_sha256="", n_linhas_anual=r["n_anual"],
                   n_linhas_outro=r["n_diario"], detalhe="")
              for r in conciliar(anual, diarios, inicio)]
    if anteriores:
        ant = anteriores[-1]
        try:
            antigo = por_dia(_abrir(ANUAL, arquivo_anual, ant["sha256"]))
        except calendario.AcervoIlegivel as e:
            # P-102: a comparacao entre anuais e ACESSORIA. Uma versao antiga ilegivel (o
            # A2026 de 18/09 chegou cortado, P-100) nao derruba a conciliacao do mes -- mas
            # tambem nao passa calada: sai escrita, sem numero.
            antigo = None
            print(f"AVISO: anual anterior {ant['sha256'][:12]} ilegivel ({e}); a "
                  f"comparacao entre anuais NAO rodou", file=sys.stderr)
    if anteriores and antigo is not None:
        n, revisados = comparar_anuais(anual_todo, antigo)
        for d in revisados:
            linhas.append(dict(dt_conciliacao=agora, competencia=mes, data=d.isoformat(),
                               situacao="REVISADO", anual_sha256=anual_v["sha256"],
                               anual_anterior_sha256=ant["sha256"],
                               n_linhas_anual=len(anual_todo[d]),
                               n_linhas_outro=len(antigo[d]),
                               detalhe=f"{len(revisados)} de {n} dias em comum mudaram"))
        # O zero sai escrito (5-B.14): "nenhum dia revisado" com o n ao lado.
        print(f"anual novo x anterior: {len(revisados)} de {n} dia(s) em comum revisado(s)")
    _anotar(resultado, linhas)

    contagem = {}
    for ln in linhas:
        contagem[ln["situacao"]] = contagem.get(ln["situacao"], 0) + 1
    print(f"{mes}: " + "  ".join(f"{k} {v}" for k, v in sorted(contagem.items())))
    falhas = sum(contagem.get(k, 0) for k in FALHAS)
    if falhas:
        print(f"{falhas} falha(s) de conciliacao -- ver {RESULTADO_RELATIVO}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

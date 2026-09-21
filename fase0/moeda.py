#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""As trocas de moeda do COTAHIST -- MEDIDAS por ano, e NAO aplicadas. Achado C-03.

POR QUE ELE EXISTE, e sao duas razoes.

A PRIMEIRA e o achado. O acervo comeca em 02/01/1986 e atravessa seis planos economicos. O
campo `MODREF` muda DENTRO do mesmo arquivo anual, e a suposicao natural -- *toda troca de
moeda e uma quebra de preco* -- **erra em 3 de 4 casos**. Medido em 19/09/2026, razao do
mesmo `CODNEG` com o controle do dia anterior ao lado:

    1986 Cruzado     (1.000:1)   274 pares   1,197   SEM QUEBRA
    1989 Verao       (1.000:1)   198 pares   0,968   SEM QUEBRA
    1993 Cruzeiro Real (1.000:1) 182 pares   0,998   SEM QUEBRA -- e o MODREF nem distingue
    1990 Collor                    2 pares     --    NAO_CONFIRMADO: o mercado parou
    1994 Real  (CR$ 2.750 = R$ 1) 136 pares   0,364  **QUEBRA**, contra controle de 1,011

**Uma tabela de planos economicos teria acusado quatro e acertado uma.** Por isso o fator
aqui e MEDIDO, nunca tabelado -- e a explicacao esta no header dos arquivos: os de 1986 a
1995 foram TODOS gerados em `19991210`, o mesmo dia, cinco anos depois do Plano Real. A B3
reexpressou a serie pre-Real ao regera-la.

    **MODREF e rotulo historico, nao a unidade em que o numero esta gravado.** Quem
    converter por ele aplica tres conversoes falsas e erra a unica verdadeira.
    `NAO_CONFIRMADO` -- e a leitura que reconcilia cinco medicoes com a data de geracao,
    nao uma afirmacao da B3.

A SEGUNDA razao e um defeito meu de 19/09. `calendario.modref_de()` e `conferir_modref()`
nasceram e **nenhum modulo do motor as chamava** -- so o teste. E a **P-77** na letra:
*campo que so o teste toca e campo que o motor nao usa*, e e categoria pior que orfa pura,
porque tem testemunha: o teste prova o esquema e ninguem prova o comportamento. Foi assim
que a P-13 anunciou correcao com a suite verde. Este modulo e o consumidor que faltava.

O QUE ELE NAO FAZ, de proposito: **nao aplica a reexpressao.** Devolve a fronteira, o fator
medido, o numero de pares e o status. Aplicar exige escolher a base -- reexpressar para R$?
manter cada ano na moeda dele? -- e isso e decisao de desenho do Osvaldo, nao consequencia
de uma medicao. Mesmo desenho do `refinar.py` com o `FACTOR_AMBIGUO`: grava o cru e recusa
escolher (P6 -- ausencia de critério é tarefa aberta, nao veredito).
"""
from __future__ import annotations
import argparse
import collections
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendario as C  # noqa: E402

# Abaixo disto a mediana da razao nao decide nada -- o Collor deu 2 pares porque o mercado
# parou, e uma mediana de 2 tem cara de resposta. Medido nas quatro fronteiras: as que
# decidem tem 136 a 274 pares, a que nao decide tem 2. O corte e frouxo de proposito.
PARES_MINIMOS = 30

# Fora desta faixa em torno de 1,0 a fronteira e QUEBRA. A largura vem do controle medido:
# o dia comum tem p10-p90 de 0,945 a 1,096, e as tres fronteiras sem quebra caem em
# 0,968-1,197. A do Real da 0,364. Nao ha nada entre 1,2 e 0,36 no acervo -- a folga entre
# as duas classes e de ordens de grandeza, e e por isso que um corte unico separa.
FAIXA_SEM_QUEBRA = (0.75, 1.35)

QUEBRA, SEM_QUEBRA, NAO_CONFIRMADO = "QUEBRA_MEDIDA", "SEM_QUEBRA", "NAO_CONFIRMADO"

# ACHADO LATERAL de 19/09, e ele apareceu porque o relatorio passou a imprimir o n do
# controle: nas fronteiras de 1986, 1989 e 1990 o controle da mediana **1,0000 exato** com
# 339, 307 e 238 pares. Em plena hiperinflacao. Nao e mercado estavel -- e a MAIORIA DOS
# PAPEIS REPETINDO O PRECO do dia anterior, mercado raso.
#
# Isso FORTALECE a leitura das fronteiras: se o dia comum de 1986 mede 1,0000, a fronteira
# medindo 1,1973 tem mais movimento que o normal -- e ainda assim nada perto de 1.000x. E a
# de 1994 tem controle 1,0106 (mercado ja liquido em R$) contra 0,3644 na fronteira.
CONTROLE_UNITARIO_ATE = 1990   # so para documentar o fato; nenhuma decisao depende dele


def por_dia(caminho, campos=("MODREF", "CODNEG", "PREULT", "TPMERC")):
    """{data: {codneg: preco}} e {data: {modref: n}}, do mercado a vista.

    So `TPMERC=010`: opcao e termo tem preco de outra natureza, e misturar generos numa
    razao de precos e a forma de produzir um numero que nao mede nada."""
    L = C.leiaute()
    ia, ib = L["campos"]["DATA"]
    ma, mb = L["campos"]["MODREF"]
    ca, cb = L["campos"]["CODNEG"]
    pa, pb = L["campos"]["PREULT"]
    ta, tb = L["campos"]["TPMERC"]
    esc = L["escala"]
    precos = collections.defaultdict(dict)
    moedas = collections.defaultdict(collections.Counter)
    for raw in C.registros(caminho):
        dt = raw[ia:ib]
        moedas[dt][raw[ma:mb].strip()] += 1
        if raw[ta:tb] != "010":
            continue
        try:
            p = int(raw[pa:pb]) / esc
        except ValueError:
            continue
        if p > 0:
            precos[dt][raw[ca:cb].strip()] = p
    return precos, moedas


def fronteiras(moedas):
    """[(data_antes, data_depois, de, para)] -- onde o MODREF majoritario muda.

    Majoritario e nao unico: num dia de virada as duas moedas convivem no arquivo, e exigir
    unanimidade perderia a fronteira exatamente no dia em que ela acontece."""
    dias = sorted(moedas)
    fora, anterior = [], None
    for d in dias:
        m = moedas[d].most_common(1)[0][0]
        if anterior and m != anterior[1]:
            fora.append((anterior[0], d, anterior[1], m))
        anterior = (d, m)
    return fora


def razao(precos, antes, depois):
    """(mediana, n_pares, p10, p90) da razao do MESMO codneg. None se nao houver par.

    E o instrumento do C-02, reaproveitado: razao do mesmo papel, nunca mediana de
    populacoes diferentes -- que foi a primeira coisa que eu tentei e que nao distingue
    troca de escala de troca de composicao da amostra."""
    comuns = precos.get(antes, {}).keys() & precos.get(depois, {}).keys()
    r = sorted(precos[depois][t] / precos[antes][t] for t in comuns)
    if not r:
        return None
    return (statistics.median(r), len(r), r[len(r) // 10], r[-max(len(r) // 10, 1)])


def medir(caminho):
    """[{fronteira, de, para, mediana, pares, fator, status, controle}] de um COTAHIST.

    `fator` e `1/mediana` -- quanto multiplicar o preco ANTES para por na escala DEPOIS --
    e vem `None` quando o status nao e QUEBRA_MEDIDA: numero de fator num caso nao
    confirmado e a coisa mais facil de alguem usar sem ler o status ao lado (F-02)."""
    precos, moedas = por_dia(caminho)
    dias = sorted(precos)
    fora = []
    for antes, depois, de, para in fronteiras(moedas):
        r = razao(precos, antes, depois)
        # controle: o pregao anterior ao 'antes', que nao tem troca de moeda nenhuma
        i = dias.index(antes) if antes in dias else 0
        ctrl = razao(precos, dias[i - 1], antes) if i >= 1 else None
        if r is None or r[1] < PARES_MINIMOS:
            status, fator = NAO_CONFIRMADO, None
        elif FAIXA_SEM_QUEBRA[0] <= r[0] <= FAIXA_SEM_QUEBRA[1]:
            status, fator = SEM_QUEBRA, None
        else:
            status, fator = QUEBRA, 1.0 / r[0]
        fora.append({"fronteira": (antes, depois), "de": de, "para": para,
                     "mediana": r[0] if r else None, "pares": r[1] if r else 0,
                     "p10": r[2] if r else None, "p90": r[3] if r else None,
                     "fator": fator, "status": status,
                     "controle": ctrl[0] if ctrl else None,
                     "pares_controle": ctrl[1] if ctrl else 0})
    return fora


def relatorio(raiz, saida=sys.stdout):
    """Varre o acervo. Devolve (linhas, modref_desconhecidos, ilegiveis)."""
    linhas, vistos, ilegiveis = [], set(), []
    for chave, caminho in sorted(C.arquivos(raiz).items()):
        try:
            _p, moedas = por_dia(caminho)
        except C.AcervoIlegivel as e:
            ilegiveis.append(str(e))
            continue
        for c in moedas.values():
            vistos.update(c)
        for r in medir(caminho):
            r["arquivo"] = chave
            linhas.append(r)
    # O controle vem com o PROPRIO numero de pares: `controle 1,0000` com um par so tem a
    # mesma cara de `controle 1,0000` com 250, e a segunda e a que autoriza a conclusao.
    # Controle sem n e decoracao -- e foi este relatorio que me mostrou isso, imprimindo
    # 1,0000 exato em duas fronteiras e me deixando sem saber se era bom ou vazio.
    print(f"{'arquivo':18} {'fronteira':22} {'de->para':14} {'pares':>6} "
          f"{'mediana':>9} {'controle':>16} {'fator':>9}  status", file=saida)
    for r in linhas:
        a, b = r["fronteira"]
        fat = f"{r['fator']:.4f}" if r["fator"] else "--"
        ctl = (f"{r['controle']:.4f} (n={r['pares_controle']})"
               if r["controle"] else "--")
        med = f"{r['mediana']:.4f}" if r["mediana"] is not None else "--"
        print(f"{r['arquivo']:18} {a}->{b:14} {r['de']+'->'+r['para']:14} "
              f"{r['pares']:>6} {med:>9} {ctl:>16} {fat:>9}  {r['status']}", file=saida)
    desconhecidos = C.conferir_modref(vistos)
    print(f"\nMODREF observados: {sorted(v for v in vistos if v)}", file=saida)
    if desconhecidos:
        # A-05: acumula, nao descarta, nao adivinha, e sai != 0.
        print(f"MODREF FORA DA ENUMERACAO: {sorted(desconhecidos)}\n"
              f"  A lista de `docs/schemas/cotahist-v02.yaml` sai do DADO e esta incompleta\n"
              f"  por construcao. Acrescente o valor novo ALI, com o ano em que apareceu --\n"
              f"  nunca aqui, e nunca tratando como um dos conhecidos.", file=sys.stderr)
    if ilegiveis:
        print(f"\n{len(ilegiveis)} arquivo(s) ILEGIVEIS, nao medidos:\n  "
              + "\n  ".join(ilegiveis), file=sys.stderr)
    quebras = [r for r in linhas if r["status"] == QUEBRA]
    print(f"\n{len(linhas)} fronteira(s) de MODREF · {len(quebras)} com QUEBRA medida · "
          f"{sum(1 for r in linhas if r['status'] == NAO_CONFIRMADO)} NAO_CONFIRMADO",
          file=saida)
    if quebras:
        print("  A reexpressao NAO foi aplicada: isto e medicao, e escolher a base e\n"
              "  decisao de desenho (P6 -- ausencia de criterio e tarefa aberta, nao\n"
              "  veredito). Ver auditoria/C03-A-QUEBRA-DE-MOEDA.md", file=saida)
    return linhas, desconhecidos, ilegiveis


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--acervo", default=os.path.join("data", "bronze", "b3", "cotahist"))
    a = p.parse_args(argv)
    _l, desconhecidos, _i = relatorio(a.acervo)
    return 2 if desconhecidos else 0


if __name__ == "__main__":
    raise SystemExit(main())

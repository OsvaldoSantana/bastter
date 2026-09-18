#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ajustar.py -- silver de eventos + COTAHIST -> serie de precos AJUSTADA por evento.

O QUE ELE FAZ
Le os precos de fechamento do COTAHIST do acervo, le a tabela de eventos que o
`refinar.py` gravou, e produz uma serie em que o degrau de preco causado por provento,
desdobramento, grupamento e bonificacao esta removido:

    ajustado(t) = fechamento(t) * PRODUTO dos fatores dos eventos com data_ex > t

O ultimo dia da serie fica com o preco publicado, e o passado e reescalado -- a convencao
usual, e a unica que nao muda o numero de ontem toda vez que chega um evento novo.

O QUE ELE DECIDE, E EXATAMENTE O QUE ELE NAO DECIDE
Este modulo faz a pergunta que so o preco responde, e a faz em 293 datas ex de 2023:

    o degrau ENCOLHE depois do ajuste?

Se nao encolher, alguma coisa esta errada -- leitura do fator, sentido do fator, ou data.
Nao ha resposta intermediaria, e por isso o teste que decide nao mede um campo: mede DUAS
series.

MAS A POPULACAO MEDIDA NAO E UNIFORME, e a distincao vale mais que o resultado. Das 293
datas ex, 292 sao provento em dinheiro e UMA e evento de quantidade (a BONIFICACAO da
FLRY). Entao a medicao confirma, com 293 casos:

  - a DATA EX derivada do calendario observado -- que ate 16/09 tinha UM caso;
  - o SENTIDO do fator (multiplicador de PRECO, e nao o inverso dele);
  - a formula do fator de provento, (P_vespera - valor) / P_vespera.

E NAO confirma, porque ali a amostra e de um: a leitura PERCENTUAL do campo `factor` nos
178 eventos de QUANTIDADE. Essa continua sustentada pela DISTRIBUICAO dos valores (ver
`auditoria/C01-FATOR.md`) mais este unico caso de preco. Quem quiser fechar a ponta
precisa do COTAHIST de 2021 e 2025, onde estao 50 dos eventos de quantidade.

O QUE ELE RECUSA
  - inventar ticker: o par (emissora, tipo de acao) vira `CODNEG` pelo que o COTAHIST
    declara -- ISIN primeiro, `(prefixo, ESPECI)` depois. Nao casou, nao entra, e SAI NO
    RELATORIO: evento nao aplicado e serie silenciosamente errada, que e pior que serie
    ausente;
  - tratar evento sem fator como fator 1: a serie inteira antes dele fica marcada
    `INCOMPLETO`. Ausencia de insumo NAO vira numero (F-02);
  - aplicar evento cuja data ex nao foi derivada: nao se sabe onde o degrau cai, e supor
    "e no dia seguinte" reintroduziria exatamente o erro que o `calendario.py` corrigiu.

O LAYOUT MORA EM DOIS MODULOS, E ISSO E DELIBERADO
`calendario.py` e dono de DUAS coisas -- quais arquivos COTAHIST existem no acervo, e
onde fica a data. Este modulo e dono dos campos de PRECO. Um fato, um dono: as posicoes
da data nao sao redigitadas aqui, e a descoberta de arquivo nao e reimplementada la
(N-01). Ate 18/09/2026 so havia um leitor de COTAHIST no projeto e a pergunta nao
existia; hoje ha dois.

USO
    python ajustar.py                        # o silver mais recente, acervo padrao
    python ajustar.py --silver data/silver/eventos_silver_2026-09-11.csv
    python ajustar.py --raiz data/bronze/b3 --saida data/silver

So biblioteca padrao, como o resto da Fase 0.
"""

import argparse, collections, csv, datetime as dt, math, os, sys
from decimal import Decimal, InvalidOperation

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import calendario                                                       # noqa: E402

RAIZ_PADRAO = os.path.join("data", "bronze", "b3")
SAIDA_PADRAO = os.path.join("data", "silver")

# ── o layout posicional do COTAHIST, campos de PRECO ──────────────────────────
# Fonte: docs/fontes/SeriesHistoricas_Layout.md, registro tipo 01, 245 posicoes.
# As posicoes aqui sao de indice zero (a fonte conta a partir de 1).
POS_CODBDI = (10, 12)        # 11-12   classificacao do papel no boletim
POS_CODNEG = (12, 24)        # 13-24   codigo de negociacao (o ticker)
POS_TPMERC = (24, 27)        # 25-27   tipo de mercado
POS_ESPECI = (39, 49)        # 40-49   especificacao: ON / PN / UNT + marca de ex
POS_PREULT = (108, 121)      # 109-121 preco do ultimo negocio, (11)V99
POS_FATCOT = (210, 217)      # 211-217 fator de cotacao: 1 unitario, 1000 por lote
POS_CODISI = (230, 242)      # 231-242 ISIN

CODBDI_LOTE_PADRAO = "02"
TPMERC_A_VISTA = "010"
CENTAVOS = Decimal(100)

# ── status por TICKER, e nenhum deles e decorativo ────────────────────────────
AJUSTADO = "AJUSTADO"
INCOMPLETO = "INCOMPLETO"            # evento dentro da janela SEM fator: retorno errado
NIVEL_INCERTO = "NIVEL_INCERTO"      # evento na borda, sem data ex: NIVEL errado, nao o retorno
SEM_EVENTO = "SEM_EVENTO_CAPTURADO"  # nenhum evento CAPTURADO alcanca esta serie
# O nome tem "CAPTURADO" porque a alternativa mentiria. O acervo de eventos cobre as 74
# emissoras do IBOV; o COTAHIST cobre 454 papeis a vista. Um FII que pagou rendimento
# todo mes sai daqui como serie sem evento -- e "SEM_EVENTO" seria lido como uma
# afirmacao sobre a EMPRESA quando e uma afirmacao sobre o ACERVO. Nome que mente e o
# defeito recorrente deste projeto (C-01, A-06, data_ex).

Papel = collections.namedtuple("Papel", "ticker especi isin arquivo")
Acervo = collections.namedtuple("Acervo", "precos especi papeis fatcot_fora arquivos")
Degrau = collections.namedtuple(
    "Degrau", "ticker data_ex data_vespera tipos n_eventos fator preco_vespera preco_ex "
              "retorno_bruto retorno_ajustado especi_vespera especi_ex")


# ─────────────────────────────────────────────────────────── leitura do COTAHIST

def cotacoes(raiz):
    """Le todo COTAHIST do acervo e devolve um `Acervo`.

    SO o mercado a vista em lote padrao (CODBDI 02, TPMERC 010). O filtro nao e
    conveniencia: o mesmo prefixo de quatro letras aparece em opcao (`ALOSA250`), termo
    (`ALOS3T`) e fracionario (`ALOS3F`), e o fracionario NEGOCIA O MESMO PAPEL com preco
    proprio. Casar um evento com o ticker errado e o A-01 outra vez -- dado do ativo
    errado, com aparencia perfeita.

    `fatcot_fora` guarda os tickers cujo FATOR DE COTACAO nao e 1 em algum pregao. Um
    papel cotado por lote de mil tem preco em outra escala; se ela MUDAR no meio da
    serie, o degrau que aparece nao e evento societario e nao ha fator que o remova. Em
    2023 o campo e 1 em 100% dos 87.483 registros a vista -- a guarda nunca disparou, e e
    por isso que ela precisa de teste sintetico."""
    precos = collections.defaultdict(dict)
    espec = collections.defaultdict(dict)
    papeis, fatcot_fora, arqs = {}, collections.Counter(), {}
    for base, caminho in sorted(calendario.arquivos(raiz).items()):
        arqs[base] = caminho
        for raw in calendario.registros(caminho):
            if raw[POS_CODBDI[0]:POS_CODBDI[1]] != CODBDI_LOTE_PADRAO:
                continue
            if raw[POS_TPMERC[0]:POS_TPMERC[1]] != TPMERC_A_VISTA:
                continue
            data = calendario.data_de(raw)
            if data is None:
                continue
            tk = raw[POS_CODNEG[0]:POS_CODNEG[1]].strip()
            try:
                preco = Decimal(raw[POS_PREULT[0]:POS_PREULT[1]]) / CENTAVOS
            except InvalidOperation:
                continue
            fatcot = raw[POS_FATCOT[0]:POS_FATCOT[1]].strip().lstrip("0") or "0"
            if fatcot != "1":
                fatcot_fora[tk] += 1
            esp = raw[POS_ESPECI[0]:POS_ESPECI[1]].strip()
            precos[tk][data] = preco
            espec[tk][data] = esp
            if tk not in papeis:
                papeis[tk] = Papel(tk, esp.split()[0] if esp else "",
                                   raw[POS_CODISI[0]:POS_CODISI[1]].strip(), base)
    return Acervo(dict(precos), dict(espec), papeis, dict(fatcot_fora), arqs)


# ──────────────────────────────────────────────────────── leitura do silver

def _chave_de_evento(r):
    """Tudo o que identifica o evento, INCLUSIVE o arquivo de onde ele veio.

    Achado A-09 (18/09/2026): a B3 devolve o mesmo provento DUAS VEZES na mesma pagina,
    byte a byte -- `ALOS/pagina-001.json` traz o dividendo de 28/04/2023 repetido. Somar
    os dois subtrai o dividendo duas vezes do preco. Nao e hipotese: medido nos 13 casos
    do acervo, colapsar a duplicata leva o residuo medio de +0,28% para -0,62%, e e o
    unico dos dois que fica dentro do ruido do dia.

    O arquivo entra na chave DE PROPOSITO: dois registros iguais em PAGINAS diferentes
    sao sobreposicao de paginacao, e ai o julgamento seria outro. Hoje nao existe nenhum
    -- e no dia em que existir, a contagem aparece em vez de ser absorvida."""
    return (r["origem"], r["cod"], r["type_stock"], r["isin"], r["data_ex"], r["tipo"],
            r["valor"], r["ratio"], r["preco_vespera"], r["arquivo_origem"])


def eventos(caminho):
    """(linhas, duplicatas). Le o CSV do `refinar.py` inteiro -- inclusive as linhas SEM
    fator e SEM data ex, porque sao elas que dizem o que a serie NAO sabe."""
    with open(caminho, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    vistos, fora, dup = set(), [], 0
    for r in linhas:
        k = _chave_de_evento(r)
        if k in vistos:
            dup += 1
            continue
        vistos.add(k)
        fora.append(r)
    return fora, dup


def indice_de_papeis(papeis):
    """(por_isin, por_par). `por_par` e {(prefixo, ESPECI): [tickers]} -- lista, e nao
    ticker, porque ambiguidade tem de ser VISIVEL em vez de resolvida pela ordem."""
    por_isin, por_par = {}, collections.defaultdict(list)
    for tk, p in sorted(papeis.items()):
        if p.isin:
            por_isin.setdefault(p.isin, tk)
        por_par[(tk[:4], p.especi)].append(tk)
    return por_isin, dict(por_par)


def ticker_de(evento, por_isin, por_par):
    """(ticker, motivo). O ISIN vem primeiro porque e identidade, nao convencao.

    O par (prefixo de 4, ESPECI) e a segunda tentativa, e os dois lados dele sao
    OBSERVADOS: o prefixo e a regra posicional do A-01, e o ESPECI e o que o proprio
    COTAHIST declara -- ON, PN, PNA, PNB, UNT, os mesmos valores que o `type_stock` do
    silver usa. Nada aqui e tabela escrita de cabeca.

    O caso que obriga o ISIN a existir e o unico evento de QUANTIDADE de 2023: a
    BONIFICACAO da FLRY vem do suplemento, que NAO traz `type_stock` -- traz ISIN. Sem
    esta ordem, justamente o evento do C-01 ficaria de fora da medicao que decide o C-01."""
    if evento["isin"] and evento["isin"] in por_isin:
        return por_isin[evento["isin"]], "ISIN"
    cands = por_par.get((evento["cod"], evento["type_stock"]), [])
    if len(cands) == 1:
        return cands[0], "PREFIXO+ESPECI"
    if not cands:
        return None, "SEM_TICKER"
    return None, "AMBIGUO"


def casar(evs, papeis):
    """(casados, nao_casados). `casados` ganha as chaves `_ticker` e `_como`."""
    por_isin, por_par = indice_de_papeis(papeis)
    casados, fora = [], []
    for r in evs:
        tk, como = ticker_de(r, por_isin, por_par)
        if tk is None:
            fora.append(dict(r, _motivo=como))
            continue
        casados.append(dict(r, _ticker=tk, _como=como))
    return casados, fora


# ──────────────────────────────────────────────────────────────── os fatores

def _data(texto):
    return dt.date.fromisoformat(texto) if texto else None


def fatores(casados):
    """{(ticker, data_ex): (fator, [tipos])}. Eventos no MESMO dia MULTIPLICAM.

    Dividendo e juros sobre capital proprio com a mesma data ex acontecem o tempo todo
    (57 pares no acervo de 2023), e o degrau do dia e o dos dois juntos. Somar so um
    deixaria metade do degrau de pe -- e a metade que sobra parece ruido."""
    fora = {}
    for r in casados:
        if r["fator_status"] != "CALCULADO" or r["data_ex_status"] != "DERIVADA":
            continue
        d = _data(r["data_ex"])
        if d is None:
            continue
        f, tipos = fora.get((r["_ticker"], d), (Decimal(1), []))
        fora[(r["_ticker"], d)] = (f * Decimal(r["fator"]), tipos + [r["tipo"]])
    return fora


def serie_ajustada(serie, fatores_do_ticker):
    """{data: (ajustado, acumulado)}.

    A ORDEM DAS DUAS LINHAS DO LACO E O MODULO INTEIRO. O preco do PROPRIO dia ex ja
    nasce sem o provento -- ele e o primeiro preco depois do degrau. Multiplicar o
    acumulado ANTES de gravar aplicaria o fator ao dia ex tambem, e o degrau mudaria de
    lugar em vez de sumir: um teste que so olhasse "o numero mudou?" passaria."""
    acum, fora = Decimal(1), {}
    for d in sorted(serie, reverse=True):
        fora[d] = (serie[d] * acum, acum)
        f = fatores_do_ticker.get(d)
        if f is not None:
            acum *= f
    return fora


def ajustar_tudo(acervo, fat):
    """{ticker: {data: (ajustado, acumulado)}} para TODO papel a vista do acervo --
    inclusive os sem evento nenhum. Sumir com um papel por ele nao ter evento seria
    ausencia de criterio virando ausencia de ativo (P6)."""
    por_ticker = collections.defaultdict(dict)
    for (tk, d), (f, _tipos) in fat.items():
        por_ticker[tk][d] = f
    return {tk: serie_ajustada(s, por_ticker.get(tk, {})) for tk, s in acervo.precos.items()}


# ───────────────────────────────────────────── o que a serie NAO sabe (P5)

def diagnostico(acervo, casados, fat):
    """{ticker: dict(status, aplicados, sem_fator, na_borda)}.

    ACHADO A-08, 18/09/2026, e ele e silencioso pela pior razao: nao muda nenhum numero
    HOJE. Um evento cujo `ultimo_dia_com_direito` cai DENTRO da janela de precos mas cuja
    data ex nao foi derivada -- porque ela cai depois do ultimo pregao observado -- afeta
    TODOS os dias da serie por igual. Todo retorno de dentro continua certo, e o NIVEL
    fica errado. Oito eventos de 28/12/2023 estao nesse caso (B3SA, CMIN, ENGI, ITUB).

    Isso nao aparece em nenhum teste de retorno, nao aparece no controle, e nao aparece no
    degrau. Aparece no dia em que o COTAHIST de 2024 entrar no acervo e as duas pontas
    forem emendadas -- com um salto artificial exatamente na virada do ano.

    A recusa de aplicar e deliberada: sabe-se que a data ex e DEPOIS do ultimo pregao,
    nao se sabe QUANDO. Aplicar seria afirmar uma data que ninguem observou.

    O QUE NAO ENTRA NESTA CONTA, e a distincao e o achado: evento cujo ultimo dia com
    direito e POSTERIOR ao ultimo pregao observado. Esse tambem nao foi aplicado, e nao e
    defeito -- e propriedade do ajuste retroativo, que reescala o passado a partir do fim
    da janela. Todo ano novo de COTAHIST reescala a serie inteira, e e assim que tem de
    ser. O contador `posteriores` existe so para que a propriedade seja dita em voz alta
    em vez de descoberta na primeira emenda de anos."""
    fora = {}
    por_ticker = collections.defaultdict(list)
    for r in casados:
        por_ticker[r["_ticker"]].append(r)
    posteriores = 0
    for tk, serie in acervo.precos.items():
        if not serie:
            continue
        primeiro, ultimo = min(serie), max(serie)
        aplicados = sum(1 for (t, _d) in fat if t == tk)
        sem_fator = na_borda = 0
        for r in por_ticker.get(tk, []):
            d = _data(r["data_ex"])
            if d is not None and r["data_ex_status"] == "DERIVADA":
                if d > primeiro and r["fator_status"] != "CALCULADO":
                    sem_fator += 1
                continue
            ucd = _data(r["ultimo_dia_com_direito"])
            if ucd is None or ucd < primeiro:
                continue                      # data ex <= primeiro pregao: nao alcanca a serie
            if ucd > ultimo:
                posteriores += 1              # ex depois da janela: ver a nota abaixo
                continue
            na_borda += 1
        if sem_fator:
            st = INCOMPLETO
        elif na_borda:
            st = NIVEL_INCERTO
        elif aplicados:
            st = AJUSTADO
        else:
            st = SEM_EVENTO
        fora[tk] = dict(status=st, aplicados=aplicados, sem_fator=sem_fator,
                        na_borda=na_borda)
    return fora, posteriores


# ──────────────────────────────────────────── a medicao que decide (C-02)

def degraus(acervo, ajustadas, fat):
    """Um `Degrau` por data ex com pregao no dia E no dia anterior.

    `retorno_bruto` e o retorno do dia ex na serie publicada; `retorno_ajustado` e o
    mesmo dia na serie ajustada. O primeiro carrega o evento; o segundo nao deveria
    carregar nada. A diferenca entre os dois E o degrau.

    As duas colunas de ESPECI sao TESTEMUNHA INDEPENDENTE, e nao custam nada: o COTAHIST
    escreve a marca de ex na especificacao do papel (`ON  ED  NM`, `PN  EJ  N1`). Elas nao
    entram em nenhuma conta -- ficam no CSV em bruto, para que a data ex derivada do
    calendario possa ser conferida contra o que a B3 escreveu no mesmo arquivo de preco.
    Medido no acervo: 284 das 293 mudam exatamente no dia ex, contra 1,59% dos pares sem
    evento. As 9 restantes sao datas ex consecutivas, em que a vespera JA estava marcada."""
    fora = []
    for (tk, dex), (f, tipos) in sorted(fat.items()):
        serie = acervo.precos.get(tk)
        if not serie or dex not in serie:
            continue
        antes = [d for d in serie if d < dex]
        if not antes:
            continue
        vesp = max(antes)
        p0, p1 = serie[vesp], serie[dex]
        if p0 <= 0:
            continue
        a0 = ajustadas[tk][vesp][0]
        a1 = ajustadas[tk][dex][0]
        fora.append(Degrau(
            tk, dex, vesp, "+".join(sorted(tipos)), len(tipos), f, p0, p1,
            float(p1 / p0 - 1), float(a1 / a0 - 1),
            acervo.especi[tk].get(vesp, ""), acervo.especi[tk].get(dex, "")))
    return fora


def resumo(lista):
    """(n, media, t) de uma lista de retornos. `t` e a media sobre o erro padrao dela:
    a pergunta nao e se UM dia ex ficou limpo -- o ruido diario de uma acao brasileira
    (sigma ~1,9%) engole qualquer provento de 1% --, e sim se a MEDIA de todos eles
    deixou de ser distinguivel de zero.

    Float, e nao Decimal, de proposito: isto e um RESUMO da medicao, nao um valor
    guardado. Nada aqui volta para o silver."""
    n = len(lista)
    if n < 2:
        return n, (lista[0] if n else 0.0), 0.0
    media = sum(lista) / n
    var = sum((x - media) ** 2 for x in lista) / (n - 1)
    ep = math.sqrt(var / n)
    return n, media, (media / ep if ep else 0.0)


def controle(acervo, ajustadas, fat):
    """(pares, divergentes, pior). O CONTROLE do experimento: em todo par de pregoes
    consecutivos SEM evento no segundo dia, o retorno tem de ser o mesmo antes e depois
    do ajuste -- os dois precos foram multiplicados pelo mesmo acumulado.

    Sem isto, "o degrau encolheu" nao prova nada: uma funcao que multiplicasse a serie
    inteira por um numero qualquer tambem encolheria degraus, e estragaria todo o resto.

    A divergencia nao e exatamente zero e o motivo e aritmetico, nao conceitual: o
    acumulado e um Decimal de 28 digitos significativos, e (p*k)/(q*k) arredonda na
    ultima casa. O pior caso medido no acervo e 1e-27 -- trinta ordens de grandeza abaixo
    do centavo. O teste exige uma tolerancia, e a tolerancia esta escrita nele."""
    pares = divergentes = 0
    pior = 0.0
    for tk, serie in acervo.precos.items():
        dias = sorted(serie)
        for i in range(1, len(dias)):
            d0, d1 = dias[i - 1], dias[i]
            if (tk, d1) in fat:
                continue
            if serie[d0] <= 0 or ajustadas[tk][d0][0] <= 0:
                continue
            pares += 1
            r0 = serie[d1] / serie[d0]
            r1 = ajustadas[tk][d1][0] / ajustadas[tk][d0][0]
            if r0 != r1:
                divergentes += 1
                pior = max(pior, abs(float(r1 - r0)))
    return pares, divergentes, pior


# ──────────────────────────────────────────────────────────────── escrita

COLUNAS_PRECO = ("ticker", "isin", "especi", "data", "fechamento", "fator_do_dia",
                 "fator_acumulado", "fechamento_ajustado", "ajuste_status",
                 "eventos_aplicados", "eventos_sem_fator", "eventos_na_borda",
                 "arquivo_origem", "dt_captura")

COLUNAS_DEGRAU = ("ticker", "data_ex", "data_vespera", "tipos", "n_eventos", "fator",
                  "fechamento_vespera", "fechamento_data_ex", "retorno_bruto",
                  "retorno_ajustado", "especi_vespera", "especi_data_ex",
                  "especi_mudou", "dt_captura")


def _texto(v):
    if v is None: return ""
    if isinstance(v, Decimal): return format(v, "f")
    if isinstance(v, float): return repr(v)
    if isinstance(v, dt.date): return v.isoformat()
    return str(v)


def gravar_precos(acervo, ajustadas, fat, diag, caminho, captura):
    """Ordem estavel (ticker, data), como no `refinar.py`: sem ela o instantaneo dourado
    acusa diferenca a cada rodada e para de servir de rede."""
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS_PRECO, lineterminator="\n")
        w.writeheader()
        for tk in sorted(acervo.precos):
            p = acervo.papeis[tk]
            d = diag.get(tk, {})
            for data in sorted(acervo.precos[tk]):
                aj, acum = ajustadas[tk][data]
                fd = fat.get((tk, data))
                w.writerow({
                    "ticker": tk, "isin": p.isin, "especi": acervo.especi[tk][data],
                    "data": _texto(data), "fechamento": _texto(acervo.precos[tk][data]),
                    "fator_do_dia": _texto(fd[0]) if fd else "",
                    "fator_acumulado": _texto(acum), "fechamento_ajustado": _texto(aj),
                    "ajuste_status": d.get("status", ""),
                    "eventos_aplicados": d.get("aplicados", 0),
                    "eventos_sem_fator": d.get("sem_fator", 0),
                    "eventos_na_borda": d.get("na_borda", 0),
                    "arquivo_origem": p.arquivo, "dt_captura": captura})


def gravar_degraus(lista, caminho, captura):
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS_DEGRAU, lineterminator="\n")
        w.writeheader()
        for g in sorted(lista, key=lambda g: (g.ticker, g.data_ex)):
            w.writerow({
                "ticker": g.ticker, "data_ex": _texto(g.data_ex),
                "data_vespera": _texto(g.data_vespera), "tipos": g.tipos,
                "n_eventos": g.n_eventos, "fator": _texto(g.fator),
                "fechamento_vespera": _texto(g.preco_vespera),
                "fechamento_data_ex": _texto(g.preco_ex),
                "retorno_bruto": _texto(g.retorno_bruto),
                "retorno_ajustado": _texto(g.retorno_ajustado),
                "especi_vespera": g.especi_vespera, "especi_data_ex": g.especi_ex,
                "especi_mudou": "sim" if g.especi_vespera != g.especi_ex else "nao",
                "dt_captura": captura})


# ─────────────────────────────────────────────────────────────── a corrida

def ultimo_silver(saida):
    if not os.path.isdir(saida):
        return None
    nomes = sorted(n for n in os.listdir(saida)
                   if n.startswith("eventos_silver_") and n.endswith(".csv"))
    return os.path.join(saida, nomes[-1]) if nomes else None


def ajustar(raiz=RAIZ_PADRAO, silver=None, saida=SAIDA_PADRAO):
    silver = silver or ultimo_silver(saida)
    if not silver or not os.path.isfile(silver):
        print("nao ha silver de eventos em %s -- rode o refinar.py antes."
              % os.path.abspath(saida), file=sys.stderr)
        return 2

    acervo = cotacoes(raiz)
    if not acervo.precos:
        print("nenhum COTAHIST em %s -- sem preco nao ha o que ajustar."
              % os.path.abspath(raiz), file=sys.stderr)
        return 2

    evs, dup = eventos(silver)
    captura = (evs[0].get("dt_captura", "") if evs else "")
    casados, sem_ticker = casar(evs, acervo.papeis)
    fat = fatores(casados)
    ajustadas = ajustar_tudo(acervo, fat)
    diag, posteriores = diagnostico(acervo, casados, fat)
    gs = degraus(acervo, ajustadas, fat)

    cob = (min(min(s) for s in acervo.precos.values() if s),
           max(max(s) for s in acervo.precos.values() if s))
    # nao casado SO importa se a data ex dele cai dentro da janela de precos: fora dela
    # ele nao mudaria numero nenhum, e acusar tudo seria ruido que ensina a ignorar.
    orfaos = [r for r in sem_ticker
              if _data(r["data_ex"]) and cob[0] < _data(r["data_ex"]) <= cob[1]]

    destino = os.path.join(saida, "precos_ajustados_%s.csv" % captura)
    destino_g = os.path.join(saida, "degrau_datas_ex_%s.csv" % captura)
    gravar_precos(acervo, ajustadas, fat, diag, destino, captura)
    gravar_degraus(gs, destino_g, captura)

    n, mb, tb = resumo([g.retorno_bruto for g in gs])
    _n, ma, ta = resumo([g.retorno_ajustado for g in gs])
    pares, div, pior = controle(acervo, ajustadas, fat)
    porst = collections.Counter(d["status"] for d in diag.values())

    print("acervo %s -- %d papeis a vista, %s a %s"
          % (", ".join(sorted(acervo.arquivos)), len(acervo.precos), cob[0], cob[1]))
    print("eventos %s -- %d linhas, %d duplicata(s) exata(s) colapsada(s), %d casadas, "
          "%d aplicadas" % (os.path.basename(silver), len(evs) + dup, dup, len(casados),
                            len(fat)))
    print("  %d evento(s) com data ex POSTERIOR a janela nao entraram -- e propriedade,"
          "\n  nao defeito: o ajuste retroativo reescala o passado a partir do FIM da"
          "\n  serie, entao cada ano novo de COTAHIST reescala a serie inteira."
          % posteriores)
    print("  series por status:")
    for st in sorted(porst): print("    %-16s %5d" % (st, porst[st]))
    print("  -> %s" % os.path.abspath(destino))
    print("  -> %s" % os.path.abspath(destino_g))

    print("\nO DEGRAU DO DIA EX -- %d datas ex com pregao no dia e na vespera" % n)
    print("  retorno BRUTO    media %+8.4f%%   t %+7.2f" % (100 * mb, tb))
    print("  retorno AJUSTADO media %+8.4f%%   t %+7.2f" % (100 * ma, ta))
    print("  CONTROLE: %d pares de pregoes SEM evento; %d com retorno diferente "
          "(pior %.1e)" % (pares, div, pior))
    quant = sum(1 for g in gs if "BONIFICACAO" in g.tipos or "DESDOBRAMENTO" in g.tipos
                or "GRUPAMENTO" in g.tipos)
    if n and abs(ma) < abs(mb):
        print("  O degrau ENCOLHEU. Nenhuma leitura errada de fator encolhe um degrau --"
              "\n  ela o inverte ou o aumenta, e as duas mutacoes estao na suite.")
        print("  O QUE ISTO CONFIRMA, nos %d casos: a data ex derivada do calendario, o"
              "\n  SENTIDO do fator, e a formula do fator de provento."
              "\n  O QUE NAO CONFIRMA: a leitura PERCENTUAL do campo `factor` -- dos %d"
              "\n  casos, %d e evento de QUANTIDADE. Ver auditoria/C02-O-DEGRAU-MEDIDO.md."
              % (n, n, quant))
    elif n:
        print("  O DEGRAU NAO ENCOLHEU. Isto REPROVA o ajuste como esta escrito: leitura"
              "\n  do `factor`, sentido do fator, ou a data ex derivada. Nao siga para o"
              "\n  backtest com esta serie.")

    if acervo.fatcot_fora:
        print("\nFATOR DE COTACAO DIFERENTE DE 1 (%d ticker(s)):" % len(acervo.fatcot_fora))
        for tk in sorted(acervo.fatcot_fora):
            print("  %-12s %d registro(s)" % (tk, acervo.fatcot_fora[tk]))
        print("Preco em outra escala. Se o fator MUDAR no meio da serie, o degrau que\n"
              "aparecer nao e evento societario e nenhum fator daqui o remove.")

    if orfaos:
        print("\nEVENTO DENTRO DA JANELA E SEM TICKER (%d) -- A-03/A-04:" % len(orfaos))
        por = collections.Counter((r["cod"], r["type_stock"], r["_motivo"]) for r in orfaos)
        for (cod, tp, mot) in sorted(por):
            print("  %-6s %-4s %-14s %d evento(s)"
                  % (cod, tp or "(sem tipo)", mot, por[(cod, tp, mot)]))
        print("Estes eventos NAO foram aplicados a serie nenhuma. Quando a emissora troca\n"
              "de codigo, o evento chega com o codigo NOVO e o preco de 2023 esta sob o\n"
              "ANTIGO -- entao a serie do codigo antigo esta sem estes ajustes, e nada na\n"
              "tabela de precos diz isso, porque nao ha a quem atribuir. Limitacao\n"
              "declarada, nao remendo presumido.")

    borda = sorted(tk for tk, d in diag.items() if d["status"] == NIVEL_INCERTO)
    if borda:
        print("\nNIVEL INCERTO NA BORDA (%d ticker(s)) -- A-08: %s"
              % (len(borda), ", ".join(borda)))
        print("Evento com ultimo dia COM DIREITO dentro da janela e data ex depois do\n"
              "ultimo pregao observado. NENHUM retorno de dentro muda -- o nivel inteiro\n"
              "e que fica deslocado, e isso so aparece ao emendar com o ano seguinte.")

    incompletos = sorted(tk for tk, d in diag.items() if d["status"] == INCOMPLETO)
    if incompletos:
        print("\nSERIE INCOMPLETA (%d ticker(s)): %s" % (len(incompletos),
                                                         ", ".join(incompletos)))
        print("Ha evento DENTRO da janela sem fator calculado. O preco anterior a ele\n"
              "esta ajustado so pelo que se sabe -- e o retorno do dia ex esta errado.")

    return 1 if (orfaos or incompletos or acervo.fatcot_fora) else 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Silver de eventos + COTAHIST -> precos ajustados.")
    p.add_argument("--raiz", default=RAIZ_PADRAO)
    p.add_argument("--saida", default=SAIDA_PADRAO)
    p.add_argument("--silver", help="CSV do refinar.py (padrao: o mais recente em --saida)")
    a = p.parse_args(argv)
    return ajustar(a.raiz, a.silver, a.saida)


if __name__ == "__main__":
    sys.exit(main())

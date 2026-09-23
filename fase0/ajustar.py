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

A JANELA CONTIGUA (21/09/2026, PLANO passo 3)
`--anos 2021-2025` le so esses anos do acervo -- um FILTRO sobre `calendario.arquivos()`,
nunca uma segunda descoberta de arquivo. E a data ex e REDERIVADA com o calendario da
propria janela, pela mesma `calendario.proximo_pregao` que o `refinar.py` usa: o silver
de 11/09 foi gravado com o calendario de 2023 so, e para ele todo evento de outro ano e
`FORA_DA_COBERTURA`. Onde o silver ja tinha derivado, as duas derivacoes tem de
concordar -- se discordarem, os dois calendarios divergem sobre o que foi pregao, e o
modulo PARA em vez de escolher (`DataExDivergente`).

Janela com buraco e recusada: o ajuste retroativo so atravessa um bloco contiguo, e um
ano faltando no meio viraria "um pregao" entre dezembro e o janeiro de dois anos depois.

A RAIZ PADRAO E `data/bronze/b3/cotahist` (23/09/2026, P-114)
Ela era `data/bronze/b3`, e `calendario.arquivos()` NAO e recursivo: os 41 anos moram
em `cotahist/`, e a raiz antiga enxergava UM arquivo -- o `COTAHIST_A2023.ZIP` avulso
que estava solto ali desde 04/09. Rodar sem `--raiz` media 2023 e dizia, no relatorio,
"acervo COTAHIST_A2023". Nao era numero errado: era um recorte de um ano com cara de
acervo inteiro, e o unico jeito de descobrir era conferir o nome do arquivo na saida.

A raiz aponta para a pasta que TEM o dado. O avulso saiu do acervo na mesma decisao
(P-97) -- eram duas metades do mesmo defeito: um arquivo no lugar errado e um padrao
apontando para o lugar errado, que se escondiam um ao outro.

USO
    python ajustar.py                        # o silver mais recente, acervo padrao
    python ajustar.py --anos 2021-2025
    python ajustar.py --silver data/silver/eventos_silver_2026-09-11.csv
    python ajustar.py --raiz data/bronze/b3/cotahist --saida data/silver

So biblioteca padrao, como o resto da Fase 0.
"""

import argparse, collections, csv, datetime as dt, math, os, sys
from decimal import Decimal, InvalidOperation

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import calendario                                                       # noqa: E402
from refinar import (CALCULADO, DERIVADA, FORA_DA_COBERTURA,           # noqa: E402
                     SEM_CALENDARIO, SEM_PRECO, fator_de_provento)

# P-114: a pasta que TEM os 41 anos, e nao a pasta que os contem uma abaixo.
# `calendario.arquivos()` nao e recursivo de proposito -- descer sozinho na arvore
# faria o acervo depender de onde alguem deixou um arquivo, e nao de onde ele mora.
RAIZ_PADRAO = os.path.join("data", "bronze", "b3", "cotahist")
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
Medicao = collections.namedtuple(
    "Medicao", "acervo evs dup casados sem_ticker fat ajustadas diag posteriores degraus "
               "cobertura rederivadas concordantes do_cotahist repetidos")
Degrau = collections.namedtuple(
    "Degrau", "ticker data_ex data_vespera tipos n_eventos fator preco_vespera preco_ex "
              "retorno_bruto retorno_ajustado especi_vespera especi_ex origem_preco")


# ─────────────────────────────────────────────────────────── leitura do COTAHIST

# ─────────────────────────────────────────────────────────────── a janela

class JanelaComBuraco(ValueError):
    """A janela pedida nao e um bloco contiguo de anos presentes no acervo."""


class DataExDivergente(ValueError):
    """O silver derivou uma data ex e o calendario da janela deriva outra."""


def janela(texto):
    """`"2021-2025"` -> (2021, ..., 2025); `"2023"` -> (2023,). Quatro digitos, sempre:
    `21-25` seria um palpite sobre o seculo."""
    partes = texto.split("-")
    if len(partes) not in (1, 2) or not all(len(x) == 4 and x.isdigit() for x in partes):
        raise ValueError("janela e AAAA ou AAAA-AAAA, nao %r" % texto)
    ini, fim = int(partes[0]), int(partes[-1])
    if ini > fim:
        raise ValueError("janela ao contrario: %r" % texto)
    return tuple(range(ini, fim + 1))


def conferir_janela(raiz, anos):
    """Levanta `JanelaComBuraco` se os anos nao forem contiguos ou se algum faltar no
    acervo. Presenca, nao legibilidade: um arquivo ilegivel levanta `AcervoIlegivel` na
    leitura, que e onde se descobre."""
    anos = sorted(anos)
    if anos != list(range(anos[0], anos[-1] + 1)):
        raise JanelaComBuraco("anos salteados nao formam serie: %s" % anos)
    presentes = {int(k[-4:]) for k in calendario.arquivos(raiz, anos)}
    faltam = [a for a in anos if a not in presentes]
    if faltam:
        raise JanelaComBuraco("faltam no acervo %s: %s" % (os.path.abspath(raiz), faltam))


def cotacoes(raiz, anos=None):
    """Le todo COTAHIST do acervo -- ou so os `anos` -- e devolve um `Acervo`.

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
    for base, caminho in sorted(calendario.arquivos(raiz, anos).items()):
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
    -- e no dia em que existir, a contagem aparece em vez de ser absorvida.

    A-12 (23/09/2026) -- A CHAVE USAVA `data_ex`, QUE E DERIVADO E PODE SER VAZIO.
    No silver de 11/09, 8.889 das 9.272 linhas tinham `data_ex` em branco, porque o
    calendario so cobria 2023 (P-114). Duas linhas que diferiam SO pela data colidiam
    na chave -- e a colisao nao aparecia como colisao, aparecia como *duplicata exata*,
    que e um numero que o relatorio imprime com naturalidade.

    Medido: a corrida de 21/09 colapsou **334** linhas, e **128 delas nao eram
    duplicata** -- as quatro parcelas de R$0,01 do BBDC em 1996-97, cada uma no seu
    dia, viraram uma. Com a chave abaixo dao 206, e dao 206 nos DOIS silvers: o numero
    deixa de depender de quanto calendario existe no disco.

    A REGRA: identidade de evento se monta com o campo OBSERVADO -- o que a B3
    declarou --, nunca com o campo DERIVADO. `ultimo_dia_com_direito` vem da fonte e
    esta preenchido em 9.272 de 9.272; `data_ex` nos calculamos, e o que nos calculamos
    pode faltar. Campo vazio dentro de uma chave nao distingue: ele UNE, e em silencio.
    E o F-02 na camada da identidade -- ausencia de insumo virando igualdade."""
    return (r["origem"], r["cod"], r["type_stock"], r["isin"],
            r["ultimo_dia_com_direito"], r["tipo"],
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


def rederivar_data_ex(evs, datas, cobertura):
    """(linhas, rederivadas). A data ex de cada evento, pelo calendario da JANELA.

    A regra e uma so, e mora no `calendario.py`: o pregao observado seguinte ao ultimo
    dia com direito. O que muda e o calendario -- e ele tem de ser o dos precos que o
    ajuste vai tocar, porque o degrau cai num dia DESTA serie.

    Onde o silver ja trazia `DERIVADA`, a janela tem de dar o mesmo dia. Se der outro, os
    dois calendarios discordam sobre o que foi pregao, e escolher um em silencio seria
    decidir sem medir qual fonte errou. `rederivadas` conta so as linhas que GANHARAM
    data ex aqui."""
    fora, rederivadas, divergem = [], 0, []
    for r in evs:
        d = calendario.proximo_pregao(_data(r["ultimo_dia_com_direito"]), datas, cobertura)
        novo = d.isoformat() if d else ""
        if r["data_ex_status"] == DERIVADA and novo and novo != r["data_ex"]:
            divergem.append("%s %s: silver %s, janela %s"
                            % (r["cod"], r["tipo"], r["data_ex"], novo))
        elif novo and r["data_ex_status"] != DERIVADA:
            rederivadas += 1
        fora.append(dict(r, data_ex=novo, data_ex_status=(
            DERIVADA if d else (FORA_DA_COBERTURA if datas else SEM_CALENDARIO))))
    if divergem:
        raise DataExDivergente("%d evento(s) com data ex diferente entre o silver e o "
                               "calendario da janela:\n  %s"
                               % (len(divergem), "\n  ".join(divergem[:20])))
    return fora, rederivadas


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


def vigente(evento, cands, precos):
    """Os candidatos cuja serie OBSERVADA alcanca a data ex do evento.

    21/09/2026, na primeira corrida da janela: o BPAC13 -- uma UNT que so negociou em 2021
    -- passou a disputar o par (BPAC, UNT) com o BPAC11 nos cinco anos, e os JCPs do
    BPAC11 de 2023, que o ano isolado aplicava, viraram AMBIGUO. Uma janela mais larga nao
    pode casar PIOR que uma estreita. O criterio e observado, nao nome parecido: um papel
    que nao negociava entre o primeiro e o ultimo pregao em torno da data ex nao e o papel
    daquele evento. Quando os dois negociam, a ambiguidade continua de pe."""
    d = _data(evento["data_ex"])
    if d is None or precos is None:
        return cands
    return [tk for tk in cands if precos.get(tk) and min(precos[tk]) <= d <= max(precos[tk])]


def casar(evs, papeis, precos=None):
    """(casados, nao_casados). `casados` ganha as chaves `_ticker` e `_como`. Com `precos`,
    a ambiguidade de par e desfeita pela VIGENCIA (ver `vigente`)."""
    por_isin, por_par = indice_de_papeis(papeis)
    casados, fora = [], []
    for r in evs:
        tk, como = ticker_de(r, por_isin, por_par)
        if como == "AMBIGUO":
            v = vigente(r, por_par[(r["cod"], r["type_stock"])], precos)
            if len(v) == 1:
                tk, como = v[0], "PREFIXO+ESPECI+VIGENCIA"
        if tk is None:
            fora.append(dict(r, _motivo=como))
            continue
        casados.append(dict(r, _ticker=tk, _como=como))
    return casados, fora


# ──────────────────────────────────────────────────────────────── os fatores

def _data(texto):
    return dt.date.fromisoformat(texto) if texto else None


# ── P-113: o preco de vespera, e DE ONDE ele veio ─────────────────────────────
# Decisao dele, 23/09/2026. Criterios em auditoria/P113-CRITERIOS.md, commitados e
# EMPURRADOS antes desta corrida (P-116) -- o hash do commit e a impressao digital.

ORIGEM_B3 = "B3"                # closingPricePriorExDate, do endpoint paginado
ORIGEM_COTAHIST = "COTAHIST"    # fechamento da vespera, do acervo de precos
ORIGEM_NENHUMA = ""             # evento de quantidade, ou vespera fora da janela


def preco_de_vespera(r, serie):
    """(preco, origem) da vespera de um evento ja casado com ticker.

    A B3 GANHA QUANDO EXISTE, e a regra e *substituir ausencia*, nunca *preferir a nossa
    fonte*. Trocar a fonte de um insumo e P1 -- o que torna esta substituicao defensavel
    nao e conveniencia, e uma concordancia MEDIDA: `closingPricePriorExDate` bate com o
    fechamento do COTAHIST em **352 de 352** ao centavo em 2023, e em mais de mil casos
    da janela 2021-2025 sem uma divergencia. O teste R1 refaz essa medicao a cada
    corrida, porque concordancia medida uma vez e concordancia daquela vez.

    A vespera e o pregao anterior DESTA serie -- a mesma definicao que `degraus()` usa
    para medir o degrau. Usar o `ultimo_dia_com_direito` daria quase sempre o mesmo dia
    e erraria quando o papel nao negociou nele, que e exatamente o caso em que o degrau
    se desloca (C-01/calendario).

    NAO ha leitor de COTAHIST novo aqui: `serie` ja e `acervo.precos[ticker]`, lida uma
    vez por `cotacoes()`. Um segundo leitor seria o N-01, e este modulo ja nasceu como o
    segundo do projeto -- e foi por isso que `arquivos()` e `registros()` foram extraidos
    para o `calendario.py` em 18/09."""
    b3 = r.get("preco_vespera")
    if b3:
        try:
            return Decimal(b3), ORIGEM_B3
        except InvalidOperation:
            pass
    d = _data(r["data_ex"])
    if d is None or not serie:
        return None, ORIGEM_NENHUMA
    antes = [x for x in serie if x < d]
    if not antes:
        return None, ORIGEM_NENHUMA
    p = serie[max(antes)]
    return (p, ORIGEM_COTAHIST) if p > 0 else (None, ORIGEM_NENHUMA)


def _provento(r):
    """A identidade de um provento ATRAVES das esteiras: ticker, dia, rotulo e valor.

    NAO tem `origem` nem `arquivo_origem`, e e exatamente nisso que ela difere da
    `_chave_de_evento`. La o arquivo entra de proposito (A-09: duas paginas com o mesmo
    registro seriam sobreposicao de paginacao, e o julgamento seria outro); aqui a
    pergunta e outra -- *este pagamento ja esta contado?* -- e a resposta nao pode
    depender de por qual porta ele entrou."""
    try:
        v = format(Decimal(r["valor"]), "f").rstrip("0").rstrip(".")
    except (InvalidOperation, TypeError, KeyError):
        v = r.get("valor") or ""
    return (r["_ticker"], r["data_ex"], r["tipo"], v)


def completar_preco_de_vespera(casados, precos):
    """Preenche o fator dos eventos que so faltava preco. Devolve (linhas, quantos).

    A-13 -- O MESMO PROVENTO CHEGA PELAS DUAS ESTEIRAS, E DAR PRECO A ELE O APLICA DUAS
    VEZES. As duas esteiras se sobrepoem na janela recente: `GetListedSupplementCompany`
    devolve os ultimos meses, e o paginado devolve o historico longo, entao o dividendo de
    setembro de 2025 esta nas duas. `_chave_de_evento` NAO os colapsa, porque `origem`
    entra nela de proposito (A-09).

    Ate aqui isso era inofensivo **por acidente**: a copia do suplemento vinha sem preco,
    logo sem fator, logo nao era aplicada. Dar preco a ela acorda uma duplicata que estava
    dormindo -- e o preco cairia DUAS vezes o valor do provento.

    **E o P-83 na letra:** *insumo ausente adormecido num campo morto continua sendo
    insumo ausente; o campo morto nao e o defeito, e o anestesico.* La eram zeros dormindo
    num campo que ninguem lia, e a decisao 1 e que os acordaria. Aqui e uma duplicata
    dormindo atras de um `SEM_PRECO`, e esta mudanca e que a acordaria.

    Medido em 23/09/2026 na janela 2021-2025: dos 172 eventos que ganhariam preco, **161
    sao o mesmo pagamento que o paginado ja traz** -- mesmo ticker, mesmo dia, mesmo
    rotulo, mesmo valor ate a ultima casa. Sobram 11 novos de verdade.

    O QUE ELE RECUSA FAZER, e as recusas sao o modulo:
      - nao toca em evento que ja tem fator: a B3 ganha quando existe (R2);
      - nao toca em `SEM_FATOR` (subscricao) nem em `TIPO_DESCONHECIDO`: ali nao falta
        preco, falta REGRA. Preencher preco onde falta regra produziria numero para uma
        pergunta que ninguem respondeu -- o F-02 na forma mais cara;
      - nao inventa vespera: sem pregao anterior na janela, a linha continua `SEM_PRECO`.

    O `fator_status` continua sendo `CALCULADO`, e NAO ganha um valor novo. A procedencia
    mora em UM lugar so -- a coluna de origem --, porque um status `CALCULADO_COTAHIST` ao
    lado de uma coluna que ja diz `COTAHIST` seriam duas leituras do mesmo fato, e duas
    leituras do mesmo fato concordam por acidente ate o dia em que nao concordam (N-01)."""
    # Quem JA carrega fator reserva o pagamento: o paginado tem o preco da propria B3, e
    # a B3 ganha quando existe (R2). A reserva e feita ANTES do laco, senao a ordem das
    # linhas decidiria qual copia sobrevive -- e ordem de arquivo nao e criterio.
    contados = {_provento(r) for r in casados
                if r["fator_status"] == CALCULADO and r["data_ex_status"] == DERIVADA}

    fora, n, repetidos = [], 0, 0
    for r in casados:
        if r["fator_status"] != SEM_PRECO or r["data_ex_status"] != DERIVADA:
            ja = r["fator_status"] == CALCULADO and r.get("preco_vespera")
            fora.append(dict(r, _origem_preco=ORIGEM_B3 if ja else ORIGEM_NENHUMA))
            continue
        chave = _provento(r)
        if chave in contados:
            # A-13: ja contado pela outra esteira. A linha FICA na tabela, com o
            # `SEM_PRECO` intacto -- ela nao e lixo, e a segunda testemunha do mesmo
            # pagamento. O que ela nao ganha e fator.
            repetidos += 1
            fora.append(dict(r, _origem_preco=ORIGEM_NENHUMA, _repetido_na_outra_esteira=True))
            continue
        p, origem = preco_de_vespera(r, precos.get(r["_ticker"]))
        valor = r.get("valor")
        if p is None or not valor:
            fora.append(dict(r, _origem_preco=ORIGEM_NENHUMA))
            continue
        f, st = fator_de_provento(Decimal(valor), p)
        if st != CALCULADO:
            # preco zero ou negativo no acervo: o status do refinar.py diz qual foi, e a
            # linha NAO vira CALCULADO. Ausencia de insumo nao vira numero (F-02).
            fora.append(dict(r, fator_status=st, _origem_preco=ORIGEM_NENHUMA))
            continue
        contados.add(chave)      # duas copias no PROPRIO suplemento tambem contam uma vez
        n += 1
        fora.append(dict(r, fator=format(f, "f"), fator_status=CALCULADO,
                         preco_vespera=format(p, "f"), _origem_preco=origem))
    return fora, n, repetidos


def fatores(casados):
    """{(ticker, data_ex): (fator, [tipos])}. Eventos no MESMO dia MULTIPLICAM.

    Dividendo e juros sobre capital proprio com a mesma data ex acontecem o tempo todo
    (57 pares no acervo de 2023), e o degrau do dia e o dos dois juntos. Somar so um
    deixaria metade do degrau de pe -- e a metade que sobra parece ruido."""
    fora = {}
    for r in casados:
        if r["fator_status"] != CALCULADO or r["data_ex_status"] != DERIVADA:
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
                if d > primeiro and r["fator_status"] != CALCULADO:
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

def origem_por_data_ex(casados):
    """{(ticker, data_ex): "B3" | "COTAHIST" | "B3+COTAHIST" | ""} -- P-113.

    O grao e o do degrau, nao o do evento, porque um degrau pode juntar mais de um
    evento no mesmo dia (dividendo + JCP acontece o tempo todo). Quando as parcelas vem
    de fontes diferentes, a coluna diz **as duas**: escolher uma esconderia que o numero
    e misto, e a pergunta que esta coluna existe para responder e *de onde veio o preco
    que produziu este fator*."""
    por = collections.defaultdict(set)
    for r in casados:
        if r["fator_status"] != CALCULADO or r["data_ex_status"] != DERIVADA:
            continue
        d = _data(r["data_ex"])
        if d is None:
            continue
        o = r.get("_origem_preco") or ORIGEM_NENHUMA
        if o:
            por[(r["_ticker"], d)].add(o)
    return {k: "+".join(sorted(v)) for k, v in por.items()}


def degraus(acervo, ajustadas, fat, casados=()):
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
    origens = origem_por_data_ex(casados)
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
            acervo.especi[tk].get(vesp, ""), acervo.especi[tk].get(dex, ""),
            origens.get((tk, dex), ORIGEM_NENHUMA)))
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


def controle_por_ano(acervo, ajustadas, fat):
    """{ano: (pares, divergentes, pior)}, pelo ano do SEGUNDO pregao do par. E o
    `controle` fatiado -- o agregado sai daqui, para que as duas contas nao possam
    discordar."""
    fora = {}
    for tk, serie in acervo.precos.items():
        dias = sorted(serie)
        for i in range(1, len(dias)):
            d0, d1 = dias[i - 1], dias[i]
            if (tk, d1) in fat:
                continue
            if serie[d0] <= 0 or ajustadas[tk][d0][0] <= 0:
                continue
            p, dv, pr = fora.get(d1.year, (0, 0, 0.0))
            r0 = serie[d1] / serie[d0]
            r1 = ajustadas[tk][d1][0] / ajustadas[tk][d0][0]
            if r0 != r1:
                dv, pr = dv + 1, max(pr, abs(float(r1 - r0)))
            fora[d1.year] = (p + 1, dv, pr)
    return fora


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
    pa = controle_por_ano(acervo, ajustadas, fat).values()
    return (sum(v[0] for v in pa), sum(v[1] for v in pa),
            max((v[2] for v in pa), default=0.0))


# Os tres rotulos cujo `factor` o C-01 leu -- o fator deles muda a QUANTIDADE de acoes.
TIPOS_DE_QUANTIDADE = frozenset({"BONIFICACAO", "DESDOBRAMENTO", "GRUPAMENTO"})


def e_de_quantidade(tipos):
    """`tipos` e o campo do `Degrau`, "A+B". Compara rotulo inteiro, nao pedaco de texto:
    um rotulo novo que CONTIVESSE "GRUPAMENTO" entraria calado numa busca por substring."""
    return any(t in TIPOS_DE_QUANTIDADE for t in tipos.split("+") if t)


def degraus_por_ano(gs):
    """{ano da data ex: dict(n, media_bruta, t_bruto, media_ajustada, t_ajustado,
    quantidade)}. A pergunta do C-02, feita ano a ano: um agregado de cinco anos
    esconderia um ano ruim atras de quatro bons."""
    por = collections.defaultdict(list)
    for g in gs:
        por[g.data_ex.year].append(g)
    fora = {}
    for ano, lista in sorted(por.items()):
        n, mb, tb = resumo([g.retorno_bruto for g in lista])
        _n, ma, ta = resumo([g.retorno_ajustado for g in lista])
        fora[ano] = dict(n=n, media_bruta=mb, t_bruto=tb, media_ajustada=ma,
                         t_ajustado=ta,
                         quantidade=sum(1 for g in lista if e_de_quantidade(g.tipos)))
    return fora


# ──────────────────────────────────────────────────────────────── escrita

COLUNAS_PRECO = ("ticker", "isin", "especi", "data", "fechamento", "fator_do_dia",
                 "fator_acumulado", "fechamento_ajustado", "ajuste_status",
                 "eventos_aplicados", "eventos_sem_fator", "eventos_na_borda",
                 "arquivo_origem", "dt_captura")

COLUNAS_DEGRAU = ("ticker", "data_ex", "data_vespera", "tipos", "n_eventos", "fator",
                  "origem_preco_vespera",
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
                "origem_preco_vespera": g.origem_preco,
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


def medir(raiz, silver, anos=None):
    """A medicao inteira, sem gravar nada -- o que a corrida e a suite compartilham.

    `evs` sao as linhas do silver como vieram (depois do A-09); `casados` ja carregam a
    data ex REDERIVADA pelo calendario da janela."""
    if anos is not None:
        conferir_janela(raiz, anos)
    acervo = cotacoes(raiz, anos)
    datas, cobertura = calendario.pregoes(raiz, anos)
    evs, dup = eventos(silver)
    redev, rederivadas = rederivar_data_ex(evs, datas, cobertura)
    concordantes = sum(1 for a, b in zip(evs, redev)
                       if a["data_ex_status"] == DERIVADA and b["data_ex"] == a["data_ex"])
    casados, sem_ticker = casar(redev, acervo.papeis, acervo.precos)
    # P-113: o preco de vespera do COTAHIST entra ANTES de `fatores()`, porque e ali que
    # a linha vira fator. Depois seria tarde; antes de `casar()` seria impossivel, porque
    # sem ticker nao ha serie de precos onde procurar.
    casados, do_cotahist, repetidos = completar_preco_de_vespera(casados, acervo.precos)
    fat = fatores(casados)
    ajustadas = ajustar_tudo(acervo, fat)
    diag, posteriores = diagnostico(acervo, casados, fat)
    return Medicao(acervo, evs, dup, casados, sem_ticker, fat, ajustadas, diag,
                   posteriores, degraus(acervo, ajustadas, fat, casados), cobertura,
                   rederivadas, concordantes, do_cotahist, repetidos)


def _sufixo(anos):
    """A corrida padrao grava com o nome de sempre; a da janela carrega os anos no nome,
    para que as duas nao se sobrescrevam e nenhum CSV finja ser o outro."""
    return "" if anos is None else "_%d-%d" % (min(anos), max(anos))


def ajustar(raiz=RAIZ_PADRAO, silver=None, saida=SAIDA_PADRAO, anos=None):
    silver = silver or ultimo_silver(saida)
    if not silver or not os.path.isfile(silver):
        print("nao ha silver de eventos em %s -- rode o refinar.py antes."
              % os.path.abspath(saida), file=sys.stderr)
        return 2

    try:
        m = medir(raiz, silver, anos)
    except JanelaComBuraco as e:
        print("JANELA RECUSADA: %s" % e, file=sys.stderr)
        return 2
    acervo, evs, dup, casados, sem_ticker = m.acervo, m.evs, m.dup, m.casados, m.sem_ticker
    fat, ajustadas, diag, posteriores, gs = m.fat, m.ajustadas, m.diag, m.posteriores, m.degraus
    if not acervo.precos:
        print("nenhum COTAHIST em %s -- sem preco nao ha o que ajustar."
              % os.path.abspath(raiz), file=sys.stderr)
        return 2
    captura = (evs[0].get("dt_captura", "") if evs else "")

    cob = (min(min(s) for s in acervo.precos.values() if s),
           max(max(s) for s in acervo.precos.values() if s))
    # nao casado SO importa se a data ex dele cai dentro da janela de precos: fora dela
    # ele nao mudaria numero nenhum, e acusar tudo seria ruido que ensina a ignorar.
    orfaos = [r for r in sem_ticker
              if _data(r["data_ex"]) and cob[0] < _data(r["data_ex"]) <= cob[1]]

    destino = os.path.join(saida, "precos_ajustados_%s%s.csv" % (captura, _sufixo(anos)))
    destino_g = os.path.join(saida, "degrau_datas_ex_%s%s.csv" % (captura, _sufixo(anos)))
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
    print("  data ex pelo calendario da janela (%s a %s): %d ganharam data ex aqui, %d "
          "concordam com o silver" % (m.cobertura[0], m.cobertura[1], m.rederivadas,
                                      m.concordantes))
    # P-113: a substituicao de fonte e DITA, nunca silenciosa. Trocar a procedencia de um
    # insumo sem anunciar seria o oposto da P1, mesmo que o numero saia certo.
    por_origem = collections.Counter(g.origem_preco for g in gs)
    print("  preco de vespera: %d fator(es) vieram do COTAHIST porque a B3 nao trouxe"
          "\n  `closingPricePriorExDate`; a B3 ganha quando existe (P-113). Degraus por"
          "\n  origem do preco: %s"
          % (m.do_cotahist,
             ", ".join("%s=%d" % (o or "(sem preco)", n)
                       for o, n in sorted(por_origem.items()))))
    print("  %d provento(s) do suplemento NAO ganharam fator porque a OUTRA esteira ja"
          "\n  traz o mesmo pagamento (A-13). Dar preco aos dois subtrairia o provento"
          "\n  duas vezes -- a duplicata estava dormindo atras do SEM_PRECO."
          % m.repetidos)
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
    quant = sum(1 for g in gs if e_de_quantidade(g.tipos))
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

    _imprimir_por_ano(gs, controle_por_ano(acervo, ajustadas, fat))
    _imprimir_residuo(residuo_de_mercado(m))

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


# ─────────────────────── o residuo, descontado o mercado (POS-HOC, 21/09/2026)
#
# O criterio do C-02 -- "o retorno ajustado do dia ex e zero em media" -- passou em 2023 e
# reprovou em quatro dos cinco anos da janela. Medido depois de ver, e por isso POS-HOC:
# o nulo estava errado em duas coisas. O dia ex tem o retorno do MERCADO daquele dia (e
# as datas ex se amontoam em poucos dias), e o preco nao cai exatamente o provento -- no
# dividendo cai mais. Em 2023 o mercado subiu, em media, nos dias ex, e escondeu isso.

def marca_de_ex(especi):
    """O token de ex do ESPECI (`ON  EDB N1` -> `EDB`), ou "". Testemunha, nao insumo: a
    tabela ESPECI publicada esta incompleta (P-95), e a letra so e LIDA aqui para separar
    os dias em que o COTAHIST declara um evento que o silver nao tem."""
    return next((t for t in especi.split()[1:] if t.startswith("E") and len(t) <= 4), "")


def mercado_do_dia(acervo, fat, tickers, minimo=20):
    """{data: mediana do retorno BRUTO dos `tickers` sem evento naquele dia}. Mediana e nao
    media: um papel com evento nao capturado nao pode arrastar o mercado. Dia com menos de
    `minimo` papeis fica de fora -- um "mercado" de tres acoes nao e mercado."""
    por = collections.defaultdict(list)
    for tk in tickers:
        s = acervo.precos.get(tk, {})
        dias = sorted(s)
        for d0, d1 in zip(dias, dias[1:]):
            if (tk, d1) in fat or s[d0] <= 0:
                continue
            por[d1].append(float(s[d1] / s[d0] - 1))
    fora = {}
    for d, v in por.items():
        if len(v) >= minimo:
            v.sort()
            k = len(v) // 2
            fora[d] = v[k] if len(v) % 2 else (v[k - 1] + v[k]) / 2
    return fora


def classe_do_degrau(g, sem_fator):
    """QUANTIDADE, MARCA_SEM_EVENTO (o ESPECI declara bonificacao/grupamento e o silver
    nao traz evento de quantidade), CONTAMINADO (ha evento SEM fator no mesmo dia) ou
    LIMPO. So o LIMPO mede o ajuste de provento; os outros medem o acervo."""
    if e_de_quantidade(g.tipos):
        return "QUANTIDADE"
    mk = marca_de_ex(g.especi_ex)
    if "B" in mk[1:] or "G" in mk[1:]:
        return "MARCA_SEM_EVENTO"
    if (g.ticker, g.data_ex) in sem_fator:
        return "CONTAMINADO"
    return "LIMPO"


def residuo_de_mercado(m):
    """[(degrau, classe, excesso, rendimento)] para todo degrau cujo dia tem mercado.
    `rendimento` e 1 - fator: a fracao do preco que o evento declarou tirar."""
    sem_fator = {(r["_ticker"], _data(r["data_ex"])) for r in m.casados
                 if r["data_ex_status"] == DERIVADA and r["fator_status"] != CALCULADO}
    merc = mercado_do_dia(m.acervo, m.fat, {r["_ticker"] for r in m.casados})
    return [(g, classe_do_degrau(g, sem_fator), g.retorno_ajustado - merc[g.data_ex],
             float(1 - g.fator)) for g in m.degraus if g.data_ex in merc]


def queda_por_provento(pontos):
    """(n, razao). Razao entre a queda de preco e o provento, pela inclinacao do excesso
    sobre o rendimento, pela origem: 1 + excesso/rendimento. 1,0 e o que o ajuste supoe."""
    num = sum(e * y for e, y in pontos)
    den = sum(y * y for _e, y in pontos)
    return len(pontos), (1 - num / den if den else float("nan"))


def _so(tipos, rotulo):
    return set(tipos.split("+")) == {rotulo}


def _imprimir_residuo(res):
    print("\nO RESIDUO, DESCONTADO O MERCADO DO DIA (pos-hoc) -- so dias LIMPOS")
    print("  ano     n   excesso%       t | fora: quant  marca_B/G  contaminado")
    por = collections.defaultdict(list)
    fora = collections.defaultdict(collections.Counter)
    for g, c, e, _y in res:
        if c == "LIMPO":
            por[g.data_ex.year].append(e)
        else:
            fora[g.data_ex.year][c] += 1
    for ano in sorted(set(por) | set(fora)):
        n, me, t = resumo(por.get(ano, []))
        f = fora[ano]
        print("  %d %5d %+9.4f %+7.2f | %11d %10d %12d" % (ano, n, 100 * me, t,
              f["QUANTIDADE"], f["MARCA_SEM_EVENTO"], f["CONTAMINADO"]))
    for rotulo in ("DIVIDENDO", "JRS CAP PROPRIO"):
        n, q = queda_por_provento([(e, y) for g, c, e, y in res
                                   if c == "LIMPO" and _so(g.tipos, rotulo)])
        print("  queda do preco / provento, so %-16s n=%4d  %.3f" % (rotulo, n, q))
    marcados = sorted((g for g, c, _e, _y in res if c == "MARCA_SEM_EVENTO"),
                      key=lambda g: (g.data_ex, g.ticker))
    if marcados:
        print("  o COTAHIST declara bonificacao/grupamento que o silver NAO tem (%d):"
              % len(marcados))
        for g in marcados:
            print("    %-8s %s %-6s ajustado %+7.2f%%" % (g.ticker, g.data_ex,
                                                        marca_de_ex(g.especi_ex),
                                                        100 * g.retorno_ajustado))


def _imprimir_por_ano(gs, ctrl):
    """A tabela que o C-02 fez para 2023, uma linha por ano, com o controle ao lado -- e,
    embaixo, cada evento de QUANTIDADE, porque ali o caso e a evidencia: o degrau de um
    desdobramento e grande demais para o ruido do dia esconder."""
    pa = degraus_por_ano(gs)
    print("\nPOR ANO -- degrau do dia ex, bruto e ajustado, e o controle dos pares sem evento")
    print("  ano     n   bruto%       t  ajust.%       t  quant |  pares  difer.    pior")
    for ano in sorted(set(pa) | set(ctrl)):
        a = pa.get(ano)
        p, dv, pr = ctrl.get(ano, (0, 0, 0.0))
        if a:
            print("  %d %5d %+8.4f %+6.2f %+8.4f %+6.2f %5d | %6d %7d %7.1e"
                  % (ano, a["n"], 100 * a["media_bruta"], a["t_bruto"],
                     100 * a["media_ajustada"], a["t_ajustado"], a["quantidade"],
                     p, dv, pr))
        else:
            print("  %d %5d %45s | %6d %7d %7.1e" % (ano, 0, "", p, dv, pr))
    q = sorted((g for g in gs if e_de_quantidade(g.tipos)),
               key=lambda g: (g.data_ex, g.ticker))
    if q:
        print("\nEVENTOS DE QUANTIDADE (%d) -- a leitura do `factor` (C-01) contra o preco"
              % len(q))
        print("  %-8s %-10s %-26s %12s %9s %9s"
              % ("ticker", "data ex", "tipos", "fator", "bruto%", "ajust.%"))
        for g in q:
            print("  %-8s %-10s %-26s %12.6f %+9.2f %+9.2f"
                  % (g.ticker, g.data_ex, g.tipos[:26], float(g.fator),
                     100 * g.retorno_bruto, 100 * g.retorno_ajustado))
        enc = sum(1 for g in q if abs(g.retorno_ajustado) < abs(g.retorno_bruto))
        print("  encolheram %d de %d" % (enc, len(q)))


def main(argv=None):
    p = argparse.ArgumentParser(description="Silver de eventos + COTAHIST -> precos ajustados.")
    p.add_argument("--raiz", default=RAIZ_PADRAO)
    p.add_argument("--saida", default=SAIDA_PADRAO)
    p.add_argument("--silver", help="CSV do refinar.py (padrao: o mais recente em --saida)")
    p.add_argument("--anos", type=janela, metavar="AAAA-AAAA",
                   help="janela CONTIGUA de anos do acervo (padrao: todos os da --raiz)")
    a = p.parse_args(argv)
    return ajustar(a.raiz, a.silver, a.saida, a.anos)


if __name__ == "__main__":
    sys.exit(main())

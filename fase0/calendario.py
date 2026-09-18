# -*- coding: utf-8 -*-
"""
calendario.py -- o calendario de pregoes da B3, OBSERVADO e nunca presumido.

POR QUE ELE EXISTE, e a resposta e um achado de 16/09/2026.

O suplemento da B3 nao traz a data ex. Traz `lastDatePrior` -- o ULTIMO DIA COM
DIREITO. O degrau de preco cai no pregao SEGUINTE. Medido no COTAHIST: a BONIFICACAO
da FLRY tem `lastDatePrior: 12/06/2023`, e a maior queda do FLRY3 no ano inteiro
(-7,78%, 4,2 desvios-padrao) esta em **13/06**. Quem tratar `lastDatePrior` como data
ex desloca TODO ajuste de preco em um pregao.

E "o pregao seguinte" nao e "o proximo dia util". Carnaval, Corpus Christi, feriado
estadual de Sao Paulo e as vesperas de Ano Novo nao estao em nenhuma regra de dia util
generica, e um evento na vespera de um deles sairia errado em silencio. Escrever a
lista de feriados de cabeca seria inventar insumo -- exatamente o que a P1 proibe.

ENTAO A FONTE E O PROPRIO ACERVO: **dia em que o COTAHIST registra negociacao e
pregao.** Procedencia real, do mesmo arquivo que o projeto ja guarda, e a cobertura
cresce sozinha a cada ano de COTAHIST que entrar no bronze.

O QUE ELE RECUSA, de proposito: fora da janela coberta, `proximo_pregao` devolve None
em vez de chutar. Nao ha como saber se houve pregao entre uma data e a borda do que se
observou -- e "nao sei" e uma resposta, "provavelmente segunda-feira" nao e.
"""

import datetime as dt
import io
import os
import zipfile

TIPO_COTACAO = "01"          # TIPREG: 00=header, 01=cotacao, 99=trailer
POS_DATA = (2, 10)           # DATA, posicoes 3-10 no layout de 245 posicoes da B3


def data_de(raw):
    """A data de um registro de cotacao, ou None quando o campo nao e data."""
    t = raw[POS_DATA[0]:POS_DATA[1]]
    try:
        return dt.date(int(t[:4]), int(t[4:6]), int(t[6:8]))
    except ValueError:
        return None


def arquivos(raiz):
    """{base: caminho} dos COTAHIST do acervo. O `.ZIP` GANHA do `.TXT` de mesmo ano:
    sao o mesmo dado, e ler o comprimido e uma ordem de grandeza mais barato.

    Mora aqui, e nao em quem chama, porque em 18/09/2026 nasceu o segundo leitor de
    COTAHIST do projeto (`ajustar.py`). Duas leituras da mesma regra de descoberta
    concordam por acidente ate o dia em que o acervo ganha um ano so em `.TXT` -- e ai
    um modulo enxerga o ano e o outro nao, sem ninguem levantar a mao (N-01)."""
    if not os.path.isdir(raiz):
        return {}
    achados = {}
    for nome in sorted(os.listdir(raiz)):
        base, ext = os.path.splitext(nome)
        if not base.upper().startswith("COTAHIST") or ext.upper() not in (".ZIP", ".TXT"):
            continue
        if base in achados and achados[base].lower().endswith(".zip"):
            continue
        achados[base] = os.path.join(raiz, nome)
    return achados


def registros(caminho):
    """Itera as linhas de COTACAO (TIPREG=01) de um COTAHIST, `.zip` ou `.txt`.

    Header e trailer NAO saem daqui: os dois carregam data, e contar um deles como
    pregao poria no calendario um dia que nunca foi pregao. O filtro e unico, para os
    dois consumidores -- a data (aqui) e o preco (`ajustar.py`)."""
    if caminho.lower().endswith(".zip"):
        with zipfile.ZipFile(caminho) as z:
            for n in z.namelist():
                if not n.upper().endswith(".TXT"):
                    continue
                with z.open(n) as f:
                    for raw in io.TextIOWrapper(f, encoding="latin-1"):
                        if raw[:2] == TIPO_COTACAO:
                            yield raw
        return
    with open(caminho, encoding="latin-1") as f:
        for raw in f:
            if raw[:2] == TIPO_COTACAO:
                yield raw


def pregoes(raiz):
    """(datas, cobertura). `datas` e um set de `dt.date`; `cobertura` e (menor, maior)
    ou (None, None) quando nao ha COTAHIST nenhum no acervo."""
    datas = set()
    for caminho in arquivos(raiz).values():
        for raw in registros(caminho):
            d = data_de(raw)
            if d is not None:
                datas.add(d)
    if not datas:
        return set(), (None, None)
    return datas, (min(datas), max(datas))


def proximo_pregao(dia, datas, cobertura):
    """O primeiro pregao ESTRITAMENTE depois de `dia`, ou None.

    None em tres situacoes, e as tres sao "nao sei", nao "nao existe":
      - nao ha calendario nenhum;
      - `dia` e anterior ao inicio do observado -- pode haver pregao entre ele e a
        borda, e nao se observou;
      - `dia` e igual ou posterior ao ULTIMO dia observado -- o proximo esta fora."""
    if dia is None or not datas:
        return None
    menor, maior = cobertura
    if dia < menor or dia >= maior:
        return None
    candidatos = [d for d in datas if d > dia]
    return min(candidatos) if candidatos else None

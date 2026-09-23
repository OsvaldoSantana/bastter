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
import re
import sys
import zipfile

# ── O LEIAUTE VEM DO YAML, e isto e um conserto de defeito meu de 19/09 ──────
# Estas constantes estavam escritas em Python:
#     POS_DATA = (2, 10) · POS_MODREF = (52, 56) · LARGURA = 245
# Sao valores de FONTE EXTERNA -- o leiaute publicado pela B3 -- e a P2 e explicita:
# *"todo parametro vive em YAML versionado, nunca em codigo. Trocar politica e um commit
# no .yaml, jamais um deploy."* Eu as escrevi no mesmo dia em que auditei tres planos de
# otimizacao por falta de rigor, e a procedencia ficou num comentario, que e o lugar onde
# ela nao pode ser conferida por teste nenhum.
#
# Agora o schema e dado: `docs/schemas/cotahist-v02.yaml`, com a revisao, a URL, a data de
# acesso e o status de cada enumeracao. A ideia veio do terceiro plano que ele mandou
# auditar -- era o melhor item dos tres, e o ganho nao e token, e a P2.

SCHEMA = os.path.join("docs", "schemas", "cotahist-v02.yaml")


class LeiauteAusente(FileNotFoundError):
    """Sem o schema nao se le COTAHIST. Recusa em vez de usar posicao embutida.

    P1 na letra: *insumo ausente NAO vira um numero*. Ler 245 posicoes fixas com um
    palpite de onde cada campo comeca devolve numero para tudo -- e numero errado tem a
    mesma cara de numero certo (F-02). E NAO ha fallback de constante em Python de
    proposito: um fallback silencioso reintroduziria exatamente o defeito que a mudanca
    para YAML veio corrigir, e ninguem descobriria, porque funcionaria."""


def _raiz_do_schema():
    """A raiz do repositorio, IMPORTADA e nao reimplementada.

    Subir a arvore ate o `pyproject.toml` sao quatro linhas, e escreve-las aqui seria o
    N-01: *duas leituras da mesma regra concordam por acidente ate o dia em que nao
    concordam* -- e o dia seria aquele em que a ancora do projeto deixasse de ser o
    `pyproject.toml`. Mesmo desenho do `refinar.py` importando `desembrulhar` do
    `coletar_b3` desde o A-06, e do `manifesto_cvm` ancorando no mesmo arquivo em vez do
    `.git` (para funcionar em clone sem historico)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from manifesto_cvm import raiz_do_repositorio
    except ImportError as e:      # pragma: no cover
        raise ImportError(
            "fase0/manifesto_cvm.py e onde `raiz_do_repositorio` mora. Reimplementar aqui "
            "seria o N-01 -- duas copias da mesma regra, que concordam ate nao concordarem."
        ) from e
    aqui = os.path.dirname(os.path.abspath(__file__))
    return raiz_do_repositorio(aqui) or os.path.dirname(aqui)


def carregar_leiaute(caminho=None):
    """O leiaute, do YAML. Converte as posicoes 1-BASEADAS do documento para os indices
    de Python -- a conversao mora AQUI e em um lugar so, porque ela e a fonte classica de
    erro de um: o documento diz 53-56, Python quer [52:56]."""
    import yaml
    c = caminho or os.path.join(_raiz_do_schema(), SCHEMA)
    if not os.path.exists(c):
        raise LeiauteAusente(
            f"{c} nao existe. O leiaute do COTAHIST e insumo, nao detalhe de "
            f"implementacao -- ver docs/fontes/b3-cotahist-leiaute.md")
    with io.open(c, encoding="utf-8") as f:
        y = yaml.safe_load(f)
    campos = {k: (v["inicio"] - 1, v["fim"]) for k, v in y["campos"].items()}
    obs = y["enumeracoes"]["MODREF"]["valores"]
    return {
        "campos": campos,
        "largura": y["registro"]["largura"],
        "escala": y["escala_de_preco"],
        "tipos": {v: k for k, v in y["registro"]["tipos"].items()},
        "modref_observados": tuple(obs),
        "revisao": y["meta"]["revisao"],
    }


_LEIAUTE = None


def leiaute():
    """Carregado uma vez. Nao e cache de desempenho: e para que um schema trocado no meio
    de uma execucao nao produza duas leituras diferentes do mesmo arquivo."""
    global _LEIAUTE
    if _LEIAUTE is None:
        _LEIAUTE = carregar_leiaute()
    return _LEIAUTE


def pos(campo):
    """(inicio, fim) em indices de Python, do YAML."""
    return leiaute()["campos"][campo]


TIPO_COTACAO = "01"          # TIPREG: 00=header, 01=cotacao, 99=trailer
TIPO_HEADER = "00"

# MODREF OBSERVADO no acervo -- a lista sai do DADO, nunca de documento. O leiaute
# publicado NAO traz tabela de valores para este campo (conferido na rev. 02), entao
# nao existe lista oficial a copiar. A-05: valor fora daqui falha ruidosamente.
# Medidos em 18-19/09/2026 sobre 8 arquivos (1986, 1989, 1990, 1993, 1994, 1995, 2001,
# 2023). Os outros 33 do acervo NAO foram abertos -- esta lista esta incompleta por
# construcao, e e por isso que quem a estende tem de MEDIR, nao deduzir.
def modref_observados():
    """A enumeracao vem do YAML (`enumeracoes.MODREF.valores`), com o status OBSERVADO e o
    numero de arquivos lidos declarados ao lado dela. Estava em Python; era o mesmo defeito
    das posicoes, com o agravante de a lista ser INCOMPLETA por construcao -- 8 dos 41
    arquivos -- e esse fato precisar viajar junto com ela."""
    return leiaute()["modref_observados"]


class AcervoIlegivel(Exception):
    """Um arquivo do acervo nao pode ser lido. NAO e "nenhum pregao": e "nao sei".

    O `COTAHIST_A2026.ZIP` chegou truncado em 18/09 e derrubava `pregoes()` inteiro --
    um arquivo ruim e o calendario do acervo deixava de existir. O desenho certo ja
    estava escrito no `coletar_b3.py` desde 10/09 (*"resposta estranha e evidencia, nao
    lixo: grave o bruto e acuse no fim"*), e foi o que salvou as 74 emissoras. A licao
    nao tinha atravessado de modulo para modulo -- e o A-07/P-85 outra vez."""


class LeiauteInesperado(Exception):
    """O membro do ZIP nao tem a cara de um COTAHIST. Melhor parar do que ler lixo
    em posicoes fixas e devolver numero."""


def modref_de(raw):
    """A moeda de referencia de um registro, sem espacos. Ver a NOTA abaixo."""
    a, b = pos("MODREF")
    return raw[a:b].strip()


def conferir_modref(vistos):
    """A-05 aplicada ao MODREF: acumula o desconhecido e devolve o conjunto, para quem
    chama falhar alto. NAO descarta a linha (perderia dado) e NAO adivinha (seria o
    F-02). Mesmo desenho do `conferir_tipo()` do `refinar.py`."""
    conhecidos = modref_observados()
    return {v for v in vistos if v and v not in conhecidos}


def ano_de(nome):
    """O ano de um nome de arquivo ou membro do COTAHIST, ou None.

    Os tres formatos que o acervo tem de fato, medidos em 18/09/2026 nos 41 arquivos:
        COTAHIST.A1986       1986-2000, dentro do ZIP -- PONTO, sem extensao
        COTAHIST_A2001       2001,      dentro do ZIP -- SUBLINHADO, sem extensao
        COTAHIST_A2023.TXT   2002-2025, dentro do ZIP
        COTAHIST_A2023.ZIP   o proprio ZIP, em qualquer ano
    Um `re` em vez de `splitext`, porque `splitext("COTAHIST.A1986")` devolve
    `('COTAHIST', '.A1986')` -- a base colide entre TODOS os anos antigos."""
    m = re.match(r"^COTAHIST[._]A?(\d{4})(\.(TXT|ZIP))?$", os.path.basename(nome),
                 re.IGNORECASE)
    return m.group(1) if m else None


def membro_do_zip(z):
    """O membro de um COTAHIST.ZIP, achado pelo CONTEUDO e nao pela extensao.

    O DEFEITO QUE ISTO CONSERTA (P-99), e ele era mudo. `registros()` filtrava
    `n.upper().endswith(".TXT")`. Dos 41 anos do acervo, 16 tem o membro SEM extensao
    -- e para esses o laco nao produzia linha nenhuma, sem erro, sem aviso: o ano
    simplesmente nao existia. Medido: 7 dos 9 arquivos em maos devolviam ZERO.

    E a correcao NAO e uma lista de nomes -- seria a P-82/P-98 pela terceira vez. A
    regra e: **um membro so, e ele tem de comecar com um header de COTAHIST**. Nome e a
    propriedade que varia; leiaute e a que identifica."""
    nomes = [n for n in z.namelist() if not n.endswith("/")]
    if len(nomes) == 1:
        return nomes[0]
    candidatos = [n for n in nomes if ano_de(n)]
    if len(candidatos) == 1:
        return candidatos[0]
    raise LeiauteInesperado(
        f"esperava UM membro de COTAHIST, achei {len(nomes)}: {nomes[:5]}")


def conferir_cabecalho(primeira, origem):
    """O header (TIPREG=00) diz `00COTAHIST.AAAABOVESPA AAAAMMDD`. Devolve
    (ano, data_de_geracao). Levanta se a linha nao tiver a cara do leiaute.

    A DATA DE GERACAO NAO E DECORACAO -- ela e a peca que explica o C-03: os arquivos
    de 1986 a 1995 foram TODOS gerados em **19991210**, o mesmo dia, treze anos depois
    do primeiro pregao. 2001 em 20060331, 2023 em 20231228."""
    if primeira[:2] != TIPO_HEADER or "COTAHIST" not in primeira[:12].upper():
        raise LeiauteInesperado(f"{origem}: primeira linha nao e header COTAHIST: "
                                f"{primeira[:40]!r}")
    # P-125: o ano esta em 11-14; [10:14] pegava o ponto de `COTAHIST.` e devolvia '.202'
    return primeira[11:15], primeira[23:31]


def data_de(raw):
    """A data de um registro de cotacao, ou None quando o campo nao e data."""
    a, b = pos("DATA")
    t = raw[a:b]
    try:
        return dt.date(int(t[:4]), int(t[4:6]), int(t[6:8]))
    except ValueError:
        return None


def arquivos(raiz, anos=None):
    """{base: caminho} dos COTAHIST do acervo. O `.ZIP` GANHA do `.TXT` de mesmo ano:
    sao o mesmo dado, e ler o comprimido e uma ordem de grandeza mais barato.

    `anos` e um FILTRO, e so isso (21/09/2026, PLANO passo 3): a janela 2021-2025 do
    `ajustar.py` le cinco dos 41 anos, e a regra de descoberta continua uma so. `None`
    devolve tudo, como antes.

    Mora aqui, e nao em quem chama, porque em 18/09/2026 nasceu o segundo leitor de
    COTAHIST do projeto (`ajustar.py`). Duas leituras da mesma regra de descoberta
    concordam por acidente ate o dia em que o acervo ganha um ano so em `.TXT` -- e ai
    um modulo enxerga o ano e o outro nao, sem ninguem levantar a mao (N-01)."""
    if not os.path.isdir(raiz):
        return {}
    achados = {}
    for nome in sorted(os.listdir(raiz)):
        ano = ano_de(nome)
        if ano is None:
            continue
        # P-121: o nome casa, o conteudo pode ser uma PASTA. `COTAHIST_A2026/` (a
        # extracao dele) existe no acervo desde 21/09 e so nao entrava porque `sorted()`
        # a poe antes do `.ZIP` e o ZIP a sobrescreve -- certo por acidente. Um ano com
        # so a pasta devolveria um diretorio como arquivo de COTAHIST.
        if not os.path.isfile(os.path.join(raiz, nome)):
            continue
        if anos is not None and int(ano) not in anos:
            continue
        # P-99: a chave e NORMALIZADA para `COTAHIST_A<ANO>`. Antes ela saia de
        # `splitext`, e `COTAHIST.A1986` virava a chave `COTAHIST` -- a MESMA para
        # todos os anos de 1986 a 2000. Quinze anos disputando uma entrada de dict.
        chave = f"COTAHIST_A{ano}"
        if chave in achados and achados[chave].lower().endswith(".zip"):
            continue
        achados[chave] = os.path.join(raiz, nome)
    return achados


def registros(caminho):
    """Itera as linhas de COTACAO (TIPREG=01) de um COTAHIST, `.zip` ou `.txt`.

    Header e trailer NAO saem daqui: os dois carregam data, e contar um deles como
    pregao poria no calendario um dia que nunca foi pregao. O filtro e unico, para os
    dois consumidores -- a data (aqui) e o preco (`ajustar.py`)."""
    try:
        if caminho.lower().endswith(".zip"):
            with zipfile.ZipFile(caminho) as z:
                membro = membro_do_zip(z)
                with z.open(membro) as f:
                    linhas = io.TextIOWrapper(f, encoding="latin-1")
                    conferir_cabecalho(next(linhas, ""), membro)
                    for raw in linhas:
                        if raw[:2] == TIPO_COTACAO:
                            yield raw
            return
        with open(caminho, encoding="latin-1") as f:
            conferir_cabecalho(next(f, ""), caminho)
            for raw in f:
                if raw[:2] == TIPO_COTACAO:
                    yield raw
    except (zipfile.BadZipFile, OSError, LeiauteInesperado) as e:
        raise AcervoIlegivel(f"{os.path.basename(caminho)}: {type(e).__name__}: {e}") from e


def pregoes(raiz, anos=None):
    """(datas, cobertura). `datas` e um set de `dt.date`; `cobertura` e (menor, maior)
    ou (None, None) quando nao ha COTAHIST nenhum no acervo. `anos` filtra como em
    `arquivos()`."""
    datas, self_ilegiveis = set(), []
    for caminho in arquivos(raiz, anos).values():
        try:
            for raw in registros(caminho):
                d = data_de(raw)
                if d is not None:
                    datas.add(d)
        except AcervoIlegivel as e:
            # Um arquivo ruim NAO apaga o acervo. Mas tambem nao passa calado: o ano
            # dele fica FALTANDO no calendario, e quem consumir tem de saber disso.
            self_ilegiveis.append(str(e))
    if self_ilegiveis:
        print(f"AVISO: {len(self_ilegiveis)} arquivo(s) do acervo ILEGIVEIS -- o "
              f"calendario abaixo NAO os cobre:\n  " + "\n  ".join(self_ilegiveis),
              file=sys.stderr)
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

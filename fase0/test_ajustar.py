# -*- coding: utf-8 -*-
"""
test_ajustar.py -- a suite do ajuste de precos (18/09/2026).

Escrita JUNTO com o modulo: regra dele de 11/09, depois de o `coletar_b3` quebrar tres
vezes na primeira corrida real, todas em funcao pura.

A SUITE TEM DUAS METADES, E ELAS RESPONDEM PERGUNTAS DIFERENTES.

  sintetica -- roda em qualquer maquina, com precos inventados de proposito, e prova que
  o CODIGO faz o que diz: o fator nao toca o proprio dia ex, o degrau some quando o fator
  esta certo, e CRESCE quando esta errado. Aqui as igualdades sao exatas.

  contra o acervo -- pula so sem `data/` na maquina (P-142: com acervo, falta e falha), e
  prova o que nenhum dado sintetico pode provar: que a regra do C-01 esta certa CONTRA O
  MERCADO, em 293 datas ex de 2023. Dado inventado nunca refuta uma leitura de campo -- ele
  so confirma a aritmetica de quem o inventou.

O TESTE QUE DECIDE e `test_O_DEGRAU_ENCOLHE_*`, e o par dele e `test_CONTROLE_*`. Um
sozinho nao vale: uma funcao que multiplicasse a serie inteira por um numero qualquer
tambem encolheria degraus -- e estragaria todo o resto da serie sem ninguem ver.
"""

import csv
import datetime as dt
import os
import sys
from decimal import Decimal

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ajustar as A                                                     # noqa: E402
import refinar                                                          # noqa: E402
import calendario                                                       # noqa: E402
from acervo_de_teste import exigir_acervo                               # noqa: E402

# P-142: era `data/bronze/b3`, e o COTAHIST mora em `.../cotahist` desde a P-114 -- os oito
# test_REAL_ abaixo pularam em toda rodada. `ANO_REAL` e a populacao para a qual eles foram
# escritos em 18/09, quando o acervo tinha UM ano: 2023. Ler os 41 seria outra medicao.
RAIZ_ACERVO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "bronze", "b3", "cotahist")
ANO_REAL = 2023
SILVER_ACERVO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "data", "silver", "eventos_silver_2026-09-11.csv")

# O erro de arredondamento de um Decimal de 28 digitos significativos em (p*k)/(q*k).
# Nao e "quase igual" por conveniencia: o pior caso medido no acervo inteiro -- 86.736
# pares de pregoes -- e 1e-27, trinta ordens de grandeza abaixo do centavo.
TOLERANCIA = Decimal("1e-24")


# ─────────────────────────────────────────────────────── COTAHIST sintetico

def _registro(data, codneg, preco_centavos, especi="ON      NM", codbdi="02",
              tpmerc="010", fatcot=1, isin="", tipreg="01"):
    """Um registro COTAHIST de 245 posicoes, montado pelas posicoes da fonte.

    Montado POR POSICAO e nao por concatenacao: um campo a mais ou a menos no meio
    deslocaria todos os seguintes e o teste continuaria verde lendo lixo -- que e
    exatamente o modo de falha que um layout posicional tem."""
    buf = [" "] * 245

    def por(ini, fim, valor, num=False):
        v = str(valor)
        v = v.rjust(fim - ini, "0") if num else v.ljust(fim - ini)
        buf[ini:fim] = list(v[:fim - ini])

    por(0, 2, tipreg)
    por(2, 10, data)
    por(*A.POS_CODBDI, codbdi)
    por(*A.POS_CODNEG, codneg)
    por(*A.POS_TPMERC, tpmerc)
    por(*A.POS_ESPECI, especi)
    por(*A.POS_PREULT, preco_centavos, True)
    por(*A.POS_FATCOT, fatcot, True)
    por(*A.POS_CODISI, isin)
    return "".join(buf)


def _header(nome):
    """O header REAL de um COTAHIST: `00COTAHIST.AAAABOVESPA AAAAMMDD`.

    21/09/2026 (P-109). Ate aqui o sintetico nao tinha header, e passava porque o
    `calendario` de 16/09 nao conferia nada. O de 19/09 confere -- e e o que achou os 16
    anos que o filtro `.TXT` zerava em silencio (P-99) -- e reprovou 14 testes daqui.
    O defeito era do sintetico: um arquivo sem header nao existe no acervo real, e um
    teste que so passa com dado que nao existe esta medindo o dado errado."""
    ano = calendario.ano_de(nome) or "2023"
    return ("00COTAHIST." + ano + "BOVESPA " + ano + "1228").ljust(245)


def _cotahist(pasta, nome, linhas):
    caminho = os.path.join(str(pasta), nome)
    with open(caminho, "w", encoding="latin-1") as f:
        f.write("\n".join([_header(nome)] + list(linhas)) + "\n")
    return str(pasta)


def _serie_plana(pasta, ticker="TESTE3", isin="BRTESTACNOR1", dias=None, precos=None):
    """Uma serie de 5 pregoes. Plana por padrao: qualquer degrau que aparecer foi posto
    pelo teste, nunca pelo ruido."""
    dias = dias or ["20230102", "20230103", "20230104", "20230105", "20230106"]
    precos = precos or [1000] * len(dias)
    return _cotahist(pasta, "COTAHIST_A2023.TXT",
                     [_registro(d, ticker, p, isin=isin) for d, p in zip(dias, precos)])


# ──────────────────────────────────────────────────────── silver sintetico

def _evento(**campos):
    linha = {c: "" for c in refinar.COLUNAS}
    linha.update(origem="paginado", cod="TEST", type_stock="ON", tipo="DIVIDENDO",
                 fator_status="CALCULADO", data_ex_status="DERIVADA",
                 dt_captura="2026-09-11", arquivo_origem="TEST\\pagina-001.json")
    linha.update(campos)
    return linha


def _silver(pasta, linhas, nome="eventos_silver_2026-09-11.csv"):
    caminho = os.path.join(str(pasta), nome)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=refinar.COLUNAS, lineterminator="\n")
        w.writeheader()
        for ln in linhas:
            w.writerow(ln)
    return caminho


# ───────────────────────────────────────────────────────────── o layout

def test_o_preco_vem_de_PREULT_e_tem_duas_casas(tmp_path):
    """(11)V99: o campo nao traz separador, e as duas ultimas posicoes SAO os centavos.
    Ler sem dividir por 100 produz uma serie 100x maior -- que passa em qualquer teste
    de retorno, porque a escala se cancela na razao. So um valor conferido pega."""
    raiz = _serie_plana(tmp_path, precos=[1632, 1505, 1000, 1000, 1000])
    ac = A.cotacoes(raiz)
    assert ac.precos["TESTE3"][dt.date(2023, 1, 2)] == Decimal("16.32")
    assert ac.precos["TESTE3"][dt.date(2023, 1, 3)] == Decimal("15.05")


def test_so_o_mercado_a_vista_em_lote_padrao_entra(tmp_path):
    """O MESMO prefixo de quatro letras aparece em fracionario, termo e opcao. O
    fracionario negocia o mesmo papel com PRECO PROPRIO -- casar um evento com ele seria
    o A-01 outra vez: dado do ativo errado, com aparencia perfeita."""
    raiz = _cotahist(tmp_path, "COTAHIST_A2023.TXT", [
        _registro("20230102", "TESTE3", 1000),                            # a vista
        _registro("20230102", "TESTE3F", 999, codbdi="96", tpmerc="020"),  # fracionario
        _registro("20230102", "TESTE3T", 998, codbdi="62", tpmerc="030"),  # termo
        _registro("20230102", "TESTA250", 50, codbdi="78", tpmerc="070"),  # opcao
        _registro("20230103", "TESTE3", 1000),
    ])
    ac = A.cotacoes(raiz)
    assert sorted(ac.precos) == ["TESTE3"]


def test_FATCOT_diferente_de_1_e_ACUSADO(tmp_path):
    """No acervo de 2023 o fator de cotacao e 1 em 100% dos registros a vista -- entao
    esta guarda NUNCA disparou com dado real, e guarda que nunca falhou e guarda que
    ninguem sabe se funciona. Este teste e a unica prova de que ela funciona.

    Importa porque um papel cotado por lote de mil muda de escala: se o fator mudar NO
    MEIO da serie, aparece um degrau de 1000x que nenhum evento societario explica e
    nenhum fator daqui remove."""
    raiz = _cotahist(tmp_path, "COTAHIST_A2023.TXT", [
        _registro("20230102", "TESTE3", 1000),
        _registro("20230103", "TESTE3", 1000, fatcot=1000),
    ])
    ac = A.cotacoes(raiz)
    assert ac.fatcot_fora == {"TESTE3": 1}


def test_header_e_trailer_nao_viram_preco(tmp_path):
    """Os dois carregam data e passariam pelo `data_de`. O filtro e do `calendario`, e e
    UM SO para os dois leitores de COTAHIST do projeto."""
    raiz = _cotahist(tmp_path, "COTAHIST_A2023.TXT", [
        _registro("20230101", "COTAHIST.202", 1, tipreg="00"),
        _registro("20230102", "TESTE3", 1000),
        _registro("20231231", "COTAHIST.202", 1, tipreg="99"),
    ])
    ac = A.cotacoes(raiz)
    assert sorted(ac.precos) == ["TESTE3"]
    assert sorted(ac.precos["TESTE3"]) == [dt.date(2023, 1, 2)]


# ───────────────────────────────────── A-09: a duplicata que a B3 devolve

def test_A09_duplicata_exata_e_colapsada_e_CONTADA(tmp_path):
    """A B3 devolve o mesmo provento duas vezes na MESMA pagina, byte a byte. Somar os
    dois subtrai o dividendo duas vezes do preco. Colapsar e a decisao -- e ela e
    CONTADA, porque decisao que nao aparece no relatorio vira premissa."""
    ev = _evento(data_ex="2023-01-04", valor="0.50", preco_vespera="10.00", fator="0.95")
    caminho = _silver(tmp_path, [ev, dict(ev), ev])
    linhas, dup = A.eventos(caminho)
    assert len(linhas) == 1 and dup == 2


def test_A09_paginas_DIFERENTES_nao_sao_duplicata(tmp_path):
    """O arquivo entra na chave de proposito: dois registros iguais em paginas diferentes
    sao sobreposicao de paginacao, e ai o julgamento e outro. Hoje nao existe nenhum no
    acervo -- e no dia em que existir, a contagem aparece em vez de ser absorvida."""
    a = _evento(data_ex="2023-01-04", valor="0.50", fator="0.95",
                arquivo_origem="TEST\\pagina-001.json")
    b = dict(a, arquivo_origem="TEST\\pagina-002.json")
    linhas, dup = A.eventos(_silver(tmp_path, [a, b]))
    assert len(linhas) == 2 and dup == 0


# ──────────────────────────────────────────────────── casar evento e papel

def _papeis(*trios):
    return {tk: A.Papel(tk, esp, isin, "COTAHIST_A2023") for tk, esp, isin in trios}


def test_casa_por_ISIN_antes_do_par():
    """O ISIN vem primeiro porque e identidade, nao convencao. E o caso que OBRIGA a
    ordem e o unico evento de QUANTIDADE de 2023: a BONIFICACAO da FLRY vem do
    suplemento, que nao traz `type_stock` -- traz ISIN. Sem isto, justamente o evento
    que decide o C-01 ficaria fora da medicao que decide o C-01."""
    papeis = _papeis(("FLRY3", "ON", "BRFLRYACNOR5"))
    por_isin, por_par = A.indice_de_papeis(papeis)
    ev = _evento(cod="FLRY", type_stock="", isin="BRFLRYACNOR5", tipo="BONIFICACAO")
    assert A.ticker_de(ev, por_isin, por_par) == ("FLRY3", "ISIN")


def test_casa_por_prefixo_e_ESPECI():
    """Os dois lados sao OBSERVADOS: o prefixo e a regra posicional do A-01 (quatro
    CARACTERES, nao quatro letras -- B3SA3), e o ESPECI e o que o COTAHIST declara."""
    papeis = _papeis(("B3SA3", "ON", ""), ("ITUB3", "ON", ""), ("ITUB4", "PN", ""))
    por_isin, por_par = A.indice_de_papeis(papeis)
    assert A.ticker_de(_evento(cod="ITUB", type_stock="PN"), por_isin, por_par) \
        == ("ITUB4", "PREFIXO+ESPECI")
    assert A.ticker_de(_evento(cod="B3SA", type_stock="ON"), por_isin, por_par) \
        == ("B3SA3", "PREFIXO+ESPECI")


def test_ambiguo_NAO_casa_e_diz_que_e_ambiguo():
    """Dois tickers para o mesmo par e ambiguidade real. Escolher o primeiro seria
    escrever ausencia de criterio no lugar de criterio -- e a ordem de um dicionario
    viraria regra de negocio."""
    papeis = _papeis(("XPTO3", "ON", ""), ("XPTO5", "ON", ""))
    por_isin, por_par = A.indice_de_papeis(papeis)
    assert A.ticker_de(_evento(cod="XPTO", type_stock="ON"), por_isin, por_par) \
        == (None, "AMBIGUO")


def test_evento_sem_ticker_sai_na_lista_de_fora_e_nao_some():
    """A-03/A-04: a emissora troca de codigo e o preco antigo fica sob o ticker antigo.
    O evento nao casa com nada -- e um evento perdido em silencio deixa a serie do
    codigo ANTIGO sem o ajuste, o que e pior que serie ausente."""
    papeis = _papeis(("TRPL4", "PN", ""))
    casados, fora = A.casar([_evento(cod="ISAE", type_stock="PN")], papeis)
    assert casados == [] and len(fora) == 1 and fora[0]["_motivo"] == "SEM_TICKER"


# ─────────────────────────────────────────────────────────────── fatores

def test_eventos_no_MESMO_dia_multiplicam():
    """Dividendo e JCP com a mesma data ex acontecem o tempo todo -- 57 pares no acervo
    de 2023. O degrau do dia e o dos dois juntos: aplicar so um deixa metade do degrau
    de pe, e a metade que sobra parece ruido."""
    evs = [dict(_evento(data_ex="2023-03-28", fator="0.99", tipo="DIVIDENDO"),
                _ticker="CMIG3", _como="ISIN"),
           dict(_evento(data_ex="2023-03-28", fator="0.98", tipo="JRS CAP PROPRIO"),
                _ticker="CMIG3", _como="ISIN")]
    fat = A.fatores(evs)
    f, tipos = fat[("CMIG3", dt.date(2023, 3, 28))]
    assert f == Decimal("0.99") * Decimal("0.98")
    assert tipos == ["DIVIDENDO", "JRS CAP PROPRIO"]


def test_evento_sem_fator_ou_sem_data_ex_NAO_entra():
    """F-02 na veia: insumo ausente nao vira fator 1. Ele fica de fora e a serie e
    marcada -- ver o teste do INCOMPLETO."""
    evs = [dict(_evento(data_ex="2023-03-28", fator="", fator_status="SEM_PRECO"),
                _ticker="X3", _como="ISIN"),
           dict(_evento(data_ex="", fator="0.99", data_ex_status="FORA_DA_COBERTURA"),
                _ticker="X3", _como="ISIN")]
    assert A.fatores(evs) == {}


# ──────────────────────────────────────────────── o ajuste, e a ordem dele

def test_o_fator_NAO_toca_o_proprio_dia_ex():
    """A ORDEM DAS DUAS LINHAS DO LACO E O MODULO INTEIRO. O preco do dia ex ja nasce sem
    o provento -- ele e o primeiro preco DEPOIS do degrau. Aplicar o fator nele tambem
    mudaria o degrau de lugar em vez de remove-lo, e um teste de "o numero mudou?"
    passaria feliz."""
    serie = {dt.date(2023, 1, 2): Decimal("10"), dt.date(2023, 1, 3): Decimal("10"),
             dt.date(2023, 1, 4): Decimal("10")}
    aj = A.serie_ajustada(serie, {dt.date(2023, 1, 3): Decimal("0.5")})
    assert aj[dt.date(2023, 1, 2)][0] == Decimal("5"), "o dia ANTERIOR e reescalado"
    assert aj[dt.date(2023, 1, 3)][0] == Decimal("10"), "o dia EX nao"
    assert aj[dt.date(2023, 1, 4)][0] == Decimal("10")


def _retorno(aj, d0, d1):
    return aj[d1][0] / aj[d0][0] - 1


def test_O_DEGRAU_ENCOLHE_e_some_quando_o_fator_esta_certo(tmp_path):
    """O TESTE QUE DECIDE, na versao sintetica e exata.

    Serie plana de R$10,00. No dia 04 a empresa fica ex de um dividendo de R$0,50: o
    preco abre em 9,50 porque o dinheiro saiu da empresa, nao porque ela vale menos.
    Fator = (10,00 - 0,50)/10,00 = 0,95.

        bruto     9,50 / 10,00 - 1 = -5%      <- o degrau
        ajustado  9,50 / (10,00 * 0,95) - 1 = 0   EXATO

    Aqui a igualdade e exata porque o fator e exato. No acervo ela nao e -- o que se mede
    la e a MEDIA de 293 dias, e e por isso que as duas metades da suite existem."""
    raiz = _serie_plana(tmp_path, precos=[1000, 1000, 950, 950, 950])
    ac = A.cotacoes(raiz)
    dex = dt.date(2023, 1, 4)
    fat = {("TESTE3", dex): (Decimal("0.95"), ["DIVIDENDO"])}
    aj = A.ajustar_tudo(ac, fat)["TESTE3"]
    bruto = ac.precos["TESTE3"][dex] / ac.precos["TESTE3"][dt.date(2023, 1, 3)] - 1
    assert bruto == Decimal("-0.05")
    assert _retorno(aj, dt.date(2023, 1, 3), dex) == 0
    gs = A.degraus(ac, {"TESTE3": aj}, fat)
    assert len(gs) == 1
    assert abs(gs[0].retorno_ajustado) < abs(gs[0].retorno_bruto)


def test_C01_lido_como_MULTIPLICADOR_o_degrau_CRESCE(tmp_path):
    """A MUTACAO que da sentido ao teste acima.

    Bonificacao de 5% (`factor: 5`). A regra do C-01 le percentual: fator de preco
    1/1,05 = 0,952380..., e o preco cai de 10,00 para 9,52. Lido como MULTIPLICADOR o
    fator seria 1/5 = 0,20.

        certo    9,52 / (10,00 * 0,952380...) - 1 =  -0,04%
        errado   9,52 / (10,00 * 0,20)        - 1 = +376%

    O ponto nao e que o numero muda: e que ele muda de ORDEM DE GRANDEZA e de SINAL. Uma
    leitura errada de fator NAO tem como encolher um degrau -- ela cria um degrau maior
    no lugar. E isso que faz da medicao do acervo uma prova, e nao uma coincidencia."""
    raiz = _serie_plana(tmp_path, precos=[1000, 1000, 952, 952, 952])
    ac = A.cotacoes(raiz)
    dex = dt.date(2023, 1, 4)
    certo = Decimal(1) / (1 + Decimal(5) / 100)
    errado = Decimal(1) / Decimal(5)

    aj_certo = A.ajustar_tudo(ac, {("TESTE3", dex): (certo, ["BONIFICACAO"])})["TESTE3"]
    aj_errado = A.ajustar_tudo(ac, {("TESTE3", dex): (errado, ["BONIFICACAO"])})["TESTE3"]
    bruto = ac.precos["TESTE3"][dex] / ac.precos["TESTE3"][dt.date(2023, 1, 3)] - 1

    r_certo = _retorno(aj_certo, dt.date(2023, 1, 3), dex)
    r_errado = _retorno(aj_errado, dt.date(2023, 1, 3), dex)
    assert abs(r_certo) < abs(bruto), "a leitura certa ENCOLHE o degrau"
    assert abs(r_errado) > abs(bruto) * 10, "a leitura errada o multiplica"
    assert r_errado > 3, "e inverte o sinal: a queda de 4,8% vira uma alta de 376%"


def test_a_data_ex_DESLOCADA_nao_encolhe_o_degrau(tmp_path):
    """A segunda mutacao, e ela e a que o acervo nao tinha como provar em 16/09.

    `lastDatePrior` e o ULTIMO DIA COM DIREITO; o degrau cai no pregao SEGUINTE. Usar a
    data errada nao "erra um pouco": deixa o degrau de pe onde ele esta E cria um degrau
    artificial, do mesmo tamanho e de sinal contrario, um dia antes. Piora duas vezes."""
    raiz = _serie_plana(tmp_path, precos=[1000, 1000, 950, 950, 950])
    ac = A.cotacoes(raiz)
    d02, d03, d04 = dt.date(2023, 1, 2), dt.date(2023, 1, 3), dt.date(2023, 1, 4)
    f = Decimal("0.95")

    certo = A.ajustar_tudo(ac, {("TESTE3", d04): (f, ["DIVIDENDO"])})["TESTE3"]
    torto = A.ajustar_tudo(ac, {("TESTE3", d03): (f, ["DIVIDENDO"])})["TESTE3"]

    assert _retorno(certo, d03, d04) == 0
    assert _retorno(torto, d03, d04) == Decimal("-0.05"), "o degrau continua inteiro"
    assert _retorno(torto, d02, d03) > Decimal("0.05"), "e nasceu um degrau falso na vespera"


def test_CONTROLE_dia_sem_evento_NAO_muda_de_retorno(tmp_path):
    """O PAR do teste que decide, e sem ele o outro nao prova nada: uma funcao que
    multiplicasse a serie inteira por um numero qualquer tambem encolheria degraus.

    Em todo par de pregoes sem evento no segundo dia, os dois precos foram multiplicados
    pelo MESMO acumulado, e a razao entre eles nao pode ter mudado."""
    raiz = _serie_plana(tmp_path, precos=[1000, 1100, 1045, 1200, 900])
    ac = A.cotacoes(raiz)
    fat = {("TESTE3", dt.date(2023, 1, 4)): (Decimal("0.95"), ["DIVIDENDO"])}
    aj = A.ajustar_tudo(ac, fat)
    pares, div, pior = A.controle(ac, aj, fat)
    assert pares == 3, "4 pares consecutivos, menos o do dia ex"
    assert div == 0 and pior == 0.0
    # e o mesmo, medido pela tabela de saida e nao pela funcao de controle
    dias = sorted(ac.precos["TESTE3"])
    for d0, d1 in zip(dias, dias[1:]):
        if (("TESTE3", d1)) in fat:
            continue
        bruto = ac.precos["TESTE3"][d1] / ac.precos["TESTE3"][d0]
        assert abs(_retorno(aj["TESTE3"], d0, d1) + 1 - bruto) < TOLERANCIA


# ─────────────────────────────────────────── o que a serie NAO sabe (P5)

def _diag(tmp_path, evento_extra, precos=None):
    raiz = _serie_plana(tmp_path, precos=precos)
    ac = A.cotacoes(raiz)
    casados, _ = A.casar([evento_extra], ac.papeis)
    fat = A.fatores(casados)
    diag, post = A.diagnostico(ac, casados, fat)
    return diag["TESTE3"], post


def test_A08_evento_na_BORDA_marca_NIVEL_INCERTO(tmp_path):
    """O achado mais silencioso do modulo, porque nao muda numero nenhum HOJE.

    Evento com ultimo dia COM DIREITO em 06/01 -- o ultimo pregao observado. A data ex e
    07/01 ou depois, e o calendario nao alcanca: nao foi derivada. O fator multiplicaria
    a serie INTEIRA, entao nenhum retorno de dentro muda e o NIVEL fica deslocado.

    Isso nao aparece no degrau, nao aparece no controle e nao aparece na suite. Aparece
    no dia em que o COTAHIST de 2024 entrar e as duas pontas forem emendadas -- com um
    salto artificial exatamente na virada do ano."""
    d, _post = _diag(tmp_path, _evento(
        cod="TEST", type_stock="ON", isin="BRTESTACNOR1",
        ultimo_dia_com_direito="2023-01-06", data_ex="", data_ex_status="FORA_DA_COBERTURA",
        fator="0.99"))
    assert d["status"] == A.NIVEL_INCERTO and d["na_borda"] == 1


def test_A08_evento_POSTERIOR_a_janela_nao_e_defeito(tmp_path):
    """A distincao que da valor ao A-08. Ultimo dia com direito em 2024: o evento tambem
    nao foi aplicado, e isso e PROPRIEDADE do ajuste retroativo -- ele reescala o passado
    a partir do fim da janela, e todo ano novo reescala tudo. Marcar isto como defeito
    poria 1.368 eventos no relatorio e ensinaria a ignora-lo."""
    d, post = _diag(tmp_path, _evento(
        cod="TEST", type_stock="ON", isin="BRTESTACNOR1",
        ultimo_dia_com_direito="2024-05-10", data_ex="", data_ex_status="FORA_DA_COBERTURA",
        fator="0.99"))
    assert d["status"] == A.SEM_EVENTO and d["na_borda"] == 0 and post == 1


def test_evento_ANTERIOR_ao_primeiro_pregao_nao_alcanca_a_serie(tmp_path):
    """A outra ponta: data ex <= primeiro pregao observado. O fator so valeria para dias
    ANTES dele, e nao ha nenhum. Nao e borda, nao e defeito, nao e nada."""
    d, post = _diag(tmp_path, _evento(
        cod="TEST", type_stock="ON", isin="BRTESTACNOR1",
        ultimo_dia_com_direito="2022-12-29", data_ex="", data_ex_status="FORA_DA_COBERTURA",
        fator="0.99"))
    assert d["status"] == A.SEM_EVENTO and d["na_borda"] == 0 and post == 0


def test_evento_sem_fator_DENTRO_da_janela_marca_INCOMPLETO(tmp_path):
    """Este muda numero, e por isso e o unico dos tres que e defeito. O degrau do dia ex
    continua de pe na serie ajustada, e nada no numero denuncia. A marca e o que denuncia."""
    d, _post = _diag(tmp_path, _evento(
        cod="TEST", type_stock="ON", isin="BRTESTACNOR1",
        ultimo_dia_com_direito="2023-01-03", data_ex="2023-01-04",
        data_ex_status="DERIVADA", fator="", fator_status="SEM_PRECO"))
    assert d["status"] == A.INCOMPLETO and d["sem_fator"] == 1


def test_SEM_EVENTO_diz_CAPTURADO_porque_a_afirmacao_e_sobre_o_ACERVO():
    """O acervo de eventos cobre 74 emissoras; o COTAHIST cobre 454 papeis. Um FII que
    pagou rendimento todo mes sai daqui sem evento -- e "SEM_EVENTO" seria lido como uma
    afirmacao sobre a EMPRESA quando e uma afirmacao sobre o ACERVO. Nome que mente e o
    defeito recorrente deste projeto, e este teste existe para que ninguem o "encurte"."""
    assert A.SEM_EVENTO == "SEM_EVENTO_CAPTURADO"


# ──────────────────────────────────────────────────────────────── escrita

def test_o_csv_e_estavel_e_grava_Decimal_exato(tmp_path):
    """Instantaneo dourado so serve se duas rodadas do mesmo dado derem o mesmo byte --
    licao da P-85, em que um `set` impresso sem ordenar fazia o relatorio mudar de texto
    entre execucoes."""
    raiz = _serie_plana(tmp_path, precos=[1000, 1000, 950, 950, 950])
    ac = A.cotacoes(raiz)
    fat = {("TESTE3", dt.date(2023, 1, 4)): (Decimal("0.95"), ["DIVIDENDO"])}
    aj = A.ajustar_tudo(ac, fat)
    diag, _ = A.diagnostico(ac, [], fat)
    a = os.path.join(str(tmp_path), "a.csv")
    b = os.path.join(str(tmp_path), "b.csv")
    A.gravar_precos(ac, aj, fat, diag, a, "2026-09-11")
    A.gravar_precos(ac, aj, fat, diag, b, "2026-09-11")
    texto = open(a, encoding="utf-8").read()
    assert texto == open(b, encoding="utf-8").read()
    assert "9.50" in texto and "e+" not in texto and "E+" not in texto


def test_a_corrida_inteira_fecha_e_escreve_os_dois_csv(tmp_path):
    """Fim a fim, sem acervo: o `main` tem de sobreviver a um universo de um papel so."""
    raiz = _serie_plana(tmp_path, precos=[1000, 1000, 950, 950, 950])
    saida = os.path.join(str(tmp_path), "silver")
    os.makedirs(saida)
    _silver(saida, [_evento(cod="TEST", type_stock="ON", isin="BRTESTACNOR1",
                            ultimo_dia_com_direito="2023-01-03", data_ex="2023-01-04",
                            valor="0.50", preco_vespera="10.00", fator="0.95")])
    assert A.ajustar(raiz, None, saida) == 0
    with open(os.path.join(saida, "degrau_datas_ex_2026-09-11.csv"), encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 1
    assert linhas[0]["ticker"] == "TESTE3" and float(linhas[0]["retorno_ajustado"]) == 0.0


# ═══════════════════════════════════════════════ contra o acervo real ═══════

# P-141: a fixture de modulo que le o acervo e POR PROCESSO. Sob `--dist loadgroup`, sem
# este grupo cada trabalhador que recebe um teste daqui refaz a leitura inteira.
pytestmark = pytest.mark.xdist_group("ajustar_real")

@pytest.fixture(scope="module")
def real():
    """O COTAHIST tem 557 MB. Uma leitura por MODULO, nao uma por teste."""
    exigir_acervo(SILVER_ACERVO, os.path.join(RAIZ_ACERVO, f"COTAHIST_A{ANO_REAL}.ZIP"))
    ac = A.cotacoes(RAIZ_ACERVO, {ANO_REAL})
    assert ac.precos, "o COTAHIST existe e nao devolveu preco nenhum"
    evs, _dup = A.eventos(SILVER_ACERVO)
    casados, fora = A.casar(evs, ac.papeis)
    fat = A.fatores(casados)
    aj = A.ajustar_tudo(ac, fat)
    return ac, casados, fora, fat, aj, A.degraus(ac, aj, fat)


@pytest.mark.slow
def test_REAL_O_DEGRAU_ENCOLHE_e_e_isto_que_confirma_o_C01(real):
    """A MEDICAO QUE DECIDE, contra o mercado, em 293 datas ex de 2023.

    O C-01 foi fechado em 16/09 pela DISTRIBUICAO dos valores de `factor`, com UMA
    corroboracao de preco (FLRY). Esta e a corroboracao em 293 casos -- e ela cobre o
    fator de PROVENTO, que a distribuicao nao tocava.

    O que se mede e a MEDIA, nao o caso: o desvio-padrao diario de uma acao brasileira e
    ~1,9% e engole qualquer provento de 1%. A media de 293 dias ex nao engole nada."""
    _ac, _cas, _fora, _fat, _aj, gs = real
    n, mb, tb = A.resumo([g.retorno_bruto for g in gs])
    _n, ma, ta = A.resumo([g.retorno_ajustado for g in gs])
    assert n >= 290, "a populacao encolheu -- o acervo mudou?"
    assert mb < -0.010 and tb < -5, "o degrau bruto existe e e enorme: %.4f (t=%.2f)" % (mb, tb)
    assert abs(ma) < 0.002, "sobrou degrau na serie ajustada: %.4f" % ma
    assert abs(ta) < 2.0, "o residuo ajustado ainda e distinguivel de zero: t=%.2f" % ta
    assert abs(ma) < abs(mb) / 10


@pytest.mark.slow
def test_REAL_CONTROLE_o_dia_sem_evento_nao_mudou(real):
    """Sem este, o teste acima nao prova nada. 86 mil pares de pregoes, e a unica
    diferenca permitida e o arredondamento do Decimal na ultima casa."""
    ac, _cas, _fora, fat, aj, _gs = real
    pares, div, pior = A.controle(ac, aj, fat)
    assert pares > 80000
    assert pior < 1e-24, "%d de %d pares mudaram de retorno, pior %.1e" % (div, pares, pior)


@pytest.mark.slow
def test_REAL_o_caso_FLRY_o_unico_evento_de_QUANTIDADE_de_2023(real):
    """O caso que deu origem ao C-01, agora medido pelas duas pontas.

    BONIFICACAO de 5% com ultimo dia com direito em 12/06/2023. A maior queda do FLRY3 no
    ano inteiro (-7,78%, 4,2 sigma) esta em 13/06 -- o pregao seguinte. Ajustado pela
    regra do C-01, o residuo cai para ~-3,2%, que e ruido de um dia e meio."""
    _ac, _cas, _fora, _fat, _aj, gs = real
    g = next((x for x in gs if x.ticker == "FLRY3" and x.data_ex == dt.date(2023, 6, 13)),
             None)
    assert g is not None, "a bonificacao da FLRY sumiu da medicao"
    assert "BONIFICACAO" in g.tipos
    assert -0.079 < g.retorno_bruto < -0.077
    assert abs(g.retorno_ajustado) < abs(g.retorno_bruto) / 2
    assert abs(g.fator - Decimal(1) / Decimal("1.05")) < Decimal("1e-9")


@pytest.mark.slow
def test_REAL_o_preco_de_vespera_da_B3_bate_com_o_COTAHIST(real):
    """DUAS FONTES INDEPENDENTES, e este e o teste que prova que o casamento de ticker
    esta certo. `closingPricePriorExDate` vem do endpoint de proventos; o fechamento vem
    do arquivo de cotacoes. Um ticker errado daria outro preco -- e nao um preco parecido,
    um preco de outra empresa.

    Medido: 352 de 352 batem EXATAMENTE, ao centavo."""
    ac, casados, _fora, fat, _aj, _gs = real
    bate = difere = 0
    for r in casados:
        if r["fator_status"] != "CALCULADO" or r["data_ex_status"] != "DERIVADA":
            continue
        if not r["preco_vespera"]:
            continue
        tk, dex = r["_ticker"], dt.date.fromisoformat(r["data_ex"])
        antes = [d for d in ac.precos[tk] if d < dex]
        if not antes:
            continue
        if ac.precos[tk][max(antes)] == Decimal(r["preco_vespera"]):
            bate += 1
        else:
            difere += 1
    assert bate >= 350 and difere == 0, "%d batem, %d diferem" % (bate, difere)


@pytest.mark.slow
def test_REAL_o_ESPECI_do_COTAHIST_e_testemunha_da_data_ex(real):
    """O achado lateral, e ele nao custou nada: o COTAHIST escreve a marca de ex na
    ESPECIFICACAO do papel -- `ON  ED  NM`, `PN  EJ  N1`. Isso e uma TERCEIRA fonte para
    a data ex, dentro do mesmo arquivo de preco, e que nao depende de preco nenhum.

    Medido: em 284 das 293 datas ex derivadas do calendario, o ESPECI muda exatamente
    naquele dia. A taxa de fundo e 1,59% nos 86 mil pares sem evento. As 9 restantes sao
    datas ex consecutivas, em que a vespera JA estava marcada -- inconclusivas, nao
    contrarias.

    Ele NAO entra em nenhuma conta do modulo, e e proposital: seria preciso enumerar as
    marcas, e a tabela ESPECI do layout publicado esta INCOMPLETA -- 2023 traz EX, EC,
    EBG, ERC, EDG, ERG, EDC e EDS, que ela nao lista. As duas colunas ficam em bruto no
    CSV, para conferencia humana."""
    ac, _cas, _fora, fat, _aj, gs = real
    mudou = sum(1 for g in gs if g.especi_vespera != g.especi_ex)
    assert mudou / len(gs) > 0.9, "%d de %d" % (mudou, len(gs))

    pares = falsos = 0
    for tk, serie in ac.precos.items():
        dias = sorted(serie)
        for d0, d1 in zip(dias, dias[1:]):
            if (tk, d1) in fat:
                continue
            pares += 1
            if ac.especi[tk][d0] != ac.especi[tk][d1]:
                falsos += 1
    taxa = falsos / pares
    assert taxa < 0.05, "a marca muda demais sozinha (%.2f%%) para ser testemunha" % (100 * taxa)
    assert mudou / len(gs) > 20 * taxa, "o sinal precisa ser muito maior que o fundo"


@pytest.mark.slow
def test_REAL_a_data_ex_DESLOCADA_reprova_em_293_casos(real):
    """A PROVA POR MUTACAO da medicao que decide, e ela fecha uma pergunta que em 16/09
    tinha UM caso (o FLRY).

    Reconstroi os fatores usando `ultimo_dia_com_direito` como se fosse a data ex -- o
    erro que o `calendario.py` existe para impedir -- e remede os MESMOS 293 dias:

        data ex certa       media -0,04%   t  -0,29
        data ex deslocada   media -1,63%   t  -9,88   (o degrau inteiro, de pe)
        ... e na vespera    media +1,91%   t +11,20   (um degrau FALSO, que nao existia)

    Um dia de erro nao "erra um pouco": deixa o degrau onde estava e cria outro do mesmo
    tamanho e sinal contrario um pregao antes. Guarda que nunca falhou e guarda que
    ninguem sabe se funciona -- esta falha, e e por isso que ela esta aqui."""
    ac, casados, _fora, fat, _aj, _gs = real
    mut = {}
    for r in casados:
        if r["fator_status"] != "CALCULADO" or r["data_ex_status"] != "DERIVADA":
            continue
        d = dt.date.fromisoformat(r["ultimo_dia_com_direito"])
        f, t = mut.get((r["_ticker"], d), (Decimal(1), []))
        mut[(r["_ticker"], d)] = (f * Decimal(r["fator"]), t + [r["tipo"]])
    ajm = A.ajustar_tudo(ac, mut)

    no_dia_ex, na_vespera = [], []
    for (tk, dex) in fat:
        serie = ac.precos.get(tk)
        if not serie or dex not in serie:
            continue
        antes = [d for d in serie if d < dex]
        if not antes:
            continue
        v = max(antes)
        no_dia_ex.append(float(ajm[tk][dex][0] / ajm[tk][v][0] - 1))
        ant2 = [d for d in serie if d < v]
        if ant2:
            na_vespera.append(float(ajm[tk][v][0] / ajm[tk][max(ant2)][0] - 1))

    _n, m_ex, t_ex = A.resumo(no_dia_ex)
    _n2, m_v, t_v = A.resumo(na_vespera)
    assert m_ex < -0.010 and t_ex < -5, "o degrau tinha de continuar de pe: %.4f" % m_ex
    assert m_v > 0.010 and t_v > 5, "e um degrau falso tinha de nascer na vespera: %.4f" % m_v


@pytest.mark.slow
def test_REAL_o_fator_INVERTIDO_dobra_o_degrau(real):
    """A segunda mutacao: trocar o fator por 1/fator -- o erro de SENTIDO, que e o mais
    facil de cometer, porque o numero continua plausivel e perto de 1.

        fator certo      media -0,04%   t  -0,29
        fator invertido  media -3,16%   t -12,98

    Ele nao deixa o degrau de pe: DOBRA. Isto e o que torna a medicao uma prova e nao uma
    coincidencia -- nao existe leitura errada de fator que encolha um degrau."""
    ac, _cas, _fora, fat, _aj, _gs = real
    inv = {k: (Decimal(1) / f, t) for k, (f, t) in fat.items()}
    gi = A.degraus(ac, A.ajustar_tudo(ac, inv), inv)
    _n, m, t = A.resumo([g.retorno_ajustado for g in gi])
    assert m < -0.020 and t < -8, "o fator invertido tinha de PIORAR o degrau: %.4f" % m


@pytest.mark.slow
def test_REAL_a_populacao_medida_e_a_que_o_relatorio_diz(real):
    """Guarda de numero publicado: os numeros deste dia estao escritos em
    `docs/auditoria/C02-O-DEGRAU-MEDIDO.md` e no CLAUDE.md. Se o acervo mudar, isto reprova --
    e reprovar e o certo: o texto passa a descrever outra medicao."""
    ac, _cas, fora, fat, _aj, gs = real
    assert len(ac.precos) == 454
    assert len(gs) == 293
    orfaos = [r for r in fora if r["data_ex"] and "2023-01-02" < r["data_ex"] <= "2023-12-28"]
    assert len(orfaos) == 13, "os eventos sem ticker mudaram de numero"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))


# ── P-117 (117a, 26/09/2026): o nome carrega os dois insumos, e a escolha e regra ──
def test_P117_o_nome_do_silver_carrega_captura_e_calendario():
    import refinar as R
    c = (dt.date(1986, 1, 2), dt.date(2026, 9, 18))
    assert R.nome_do_silver("2026-09-11", c) == \
        "eventos_silver_2026-09-11_cal-19860102-20260918.csv"
    assert R.nome_do_silver("2026-09-11", (None, None)) == \
        "eventos_silver_2026-09-11_cal-nenhum.csv"


def test_P117_a_escolha_e_a_captura_mais_nova_e_o_maior_calendario(tmp_path):
    """O caso que a P-117 descreve: um `_antigo` ou qualquer nome que o sorted() pusesse
    por ultimo ja nao inverte a escolha -- a regra le o calendario no nome."""
    for n in ("eventos_silver_2026-09-11.csv",                        # legado, sem calendario
              "eventos_silver_2026-09-11_cal-1986-2026.csv",           # legado do P-114
              "eventos_silver_2026-09-11_cal-20230102-20231228.csv",   # so 2023
              "eventos_silver_2026-09-10_cal-19860102-20260918.csv"):  # captura mais velha
        (tmp_path / n).write_text("x\n")
    assert os.path.basename(A.ultimo_silver(str(tmp_path))) == \
        "eventos_silver_2026-09-11_cal-1986-2026.csv"
    (tmp_path / "eventos_silver_2026-09-11_zzz_antigo.csv").write_text("x\n")
    assert os.path.basename(A.ultimo_silver(str(tmp_path))) == \
        "eventos_silver_2026-09-11_cal-1986-2026.csv", "nome fora do padrao nao conta"


def test_P117_empate_levanta_em_vez_de_escolher(tmp_path):
    for n in ("eventos_silver_2026-09-11_cal-19860102-20231228.csv",
              "eventos_silver_2026-09-11_cal-19890102-20261228.csv"):
        (tmp_path / n).write_text("x\n")
    with pytest.raises(A.SilverAmbiguo):
        A.ultimo_silver(str(tmp_path))


def test_P117_so_o_legado_sem_calendario_ainda_vale_se_for_o_unico(tmp_path):
    (tmp_path / "eventos_silver_2026-09-11.csv").write_text("x\n")
    assert A.ultimo_silver(str(tmp_path)).endswith("eventos_silver_2026-09-11.csv")

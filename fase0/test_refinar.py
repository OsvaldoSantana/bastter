# -*- coding: utf-8 -*-
"""
test_refinar.py -- a suite do bronze -> silver.

Escrita JUNTO com o modulo, nao depois: e a regra que ele deu em 11/09 depois de o
coletar_b3 quebrar tres vezes na primeira corrida real, todas em funcao pura.

As tres funcoes onde mora o risco aqui sao `dec_br`, `data_br` e os dois fatores. As
quatro sao puras. Nao ha desculpa para nenhuma chegar sem teste.
"""

import datetime as dt
import os
import sys
from decimal import Decimal

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refinar as r                                                     # noqa: E402


# ─────────────────────────────────────────────────── formato brasileiro

@pytest.mark.parametrize("texto,esperado", [
    ("0,65", Decimal("0.65")),
    ("0,04490000000", Decimal("0.04490000000")),
    ("84,49", Decimal("84.49")),
    ("15.468.781.313,18", Decimal("15468781313.18")),   # milhar E decimal
    ("1.380.439.543", Decimal("1380439543")),           # so milhar
    ("100,00000000000", Decimal("100")),
    ("", None), ("   ", None), (None, None),
    ("nao e numero", None),
])
def test_dec_br(texto, esperado):
    assert r.dec_br(texto) == esperado


def test_dec_br_a_ordem_das_trocas_importa():
    """Trocar a virgula ANTES de remover o ponto transformaria '0,65' em '0.65' e
    depois em '065'. O teste existe para que a ordem nao seja 'arrumada'."""
    assert r.dec_br("0,65") == Decimal("0.65")
    assert r.dec_br("1.234,56") == Decimal("1234.56")


def test_dec_br_devolve_Decimal_e_nunca_float():
    """8 mil somas em float acumulam erro. O tipo e parte do contrato."""
    assert isinstance(r.dec_br("0,1"), Decimal)
    assert r.dec_br("0,1") + r.dec_br("0,2") == Decimal("0.3")   # falha com float


@pytest.mark.parametrize("texto,esperado", [
    ("25/04/2008", dt.date(2008, 4, 25)),      # dia > 12: so uma leitura possivel
    ("22/06/2026", dt.date(2026, 6, 22)),
    ("13/09/2013", dt.date(2013, 9, 13)),
    ("", None), (None, None), ("30/02/2020", None), ("xx/yy/zzzz", None),
])
def test_data_br(texto, esperado):
    assert r.data_br(texto) == esperado


def test_data_br_o_caso_AMBIGUO_e_o_que_importa():
    """A LINHA MAIS PERIGOSA DO MODULO.

    '05/09/2026' e 5 de SETEMBRO. Lido como ISO seria 9 de MAIO -- e as DUAS sao datas
    validas, entao o parser errado nao levanta excecao: produz uma serie deslocada em
    meses, silenciosamente, so nos dias <= 12.

    Um teste que so usasse '25/04/2008' passaria com o parser errado."""
    assert r.data_br("05/09/2026") == dt.date(2026, 9, 5)
    assert r.data_br("01/12/2020") == dt.date(2020, 12, 1)
    assert r.data_br("12/11/2019") == dt.date(2019, 11, 12)
    # e o contraprova: nenhuma delas pode virar a leitura trocada
    assert r.data_br("05/09/2026") != dt.date(2026, 5, 9)


def test_data_br_aceita_timestamp_e_corta_a_hora():
    assert r.data_br("13/09/2013 00:00:00") == dt.date(2013, 9, 13)


# ──────────────────────────────────────────────────────────── os fatores

def test_fator_de_provento_o_caso_medido():
    """Do acervo real: PETR, provento de 0,65 com fechamento de 84,49 na vespera."""
    f, st = r.fator_de_provento(Decimal("0.65"), Decimal("84.49"))
    assert st == r.CALCULADO
    assert abs(f - Decimal("0.992306")) < Decimal("0.000001")
    assert f < 1, "provento sempre reduz o preco ajustado"


def test_fator_de_provento_sem_preco_nao_vira_numero():
    """O suplemento nao traz preco de vespera. A ausencia tem de virar ausencia
    DECLARADA, nunca 1.0 nem 0.0 -- e o F-02 numa tabela."""
    f, st = r.fator_de_provento(Decimal("0.65"), None)
    assert f is None and st == r.SEM_PRECO


def test_fator_de_provento_preco_zero_nao_divide():
    f, st = r.fator_de_provento(Decimal("0.65"), Decimal("0"))
    assert f is None and st == r.PRECO_INVALIDO


def test_C01_a_regra_e_DUPLA_e_o_rotulo_e_que_separa():
    """ACHADO C-01, medido e fechado em 16/09/2026.

    Ate 16/09 esta funcao RECUSAVA escolher (`FACTOR_AMBIGUO`), e a recusa estava certa:
    nao havia medicao. A medicao veio da DISTRIBUICAO dos 180 eventos do acervo, nao de
    um caso: lidos como percentual, os onze valores distintos de `factor` dos
    desdobramentos caem em cima de razoes canonicas (100->2x, 400->5x, 9900->100x); lidos
    como multiplicador dariam 101, 401, 9901.

    E a regra NAO e uma so. No GRUPAMENTO o campo ja e o multiplicador de quantidade, e
    e menor que 1. Este teste guarda as duas, porque confundi-las e o erro caro: aplicar
    a regra do desdobramento num grupamento de 1000:1 daria fator 1,00001 -- a serie
    passaria pelo degrau SEM DEGRAU, em silencio."""
    # desdobramento e bonificacao: `factor` e PERCENTUAL de novas por 100 existentes
    assert r.fator_de_quantidade(Decimal("100"), "DESDOBRAMENTO") == (Decimal("0.5"), r.CALCULADO)
    assert r.fator_de_quantidade(Decimal("400"), "DESDOBRAMENTO")[0] == Decimal("0.2")
    assert r.fator_de_quantidade(Decimal("9900"), "DESDOBRAMENTO")[0] == Decimal("0.01")
    f, st = r.fator_de_quantidade(Decimal("5"), "BONIFICACAO")
    assert st == r.CALCULADO and abs(f - Decimal("0.952380952")) < Decimal("1e-9")

    # grupamento: `factor` JA E o multiplicador de quantidade, e e < 1
    assert r.fator_de_quantidade(Decimal("0.001"), "GRUPAMENTO") == (Decimal("1000"), r.CALCULADO)
    assert r.fator_de_quantidade(Decimal("0.1"), "GRUPAMENTO")[0] == Decimal("10")


def test_C01_confundir_as_duas_regras_seria_o_erro_CARO():
    """O numero que o defeito produziria, escrito para nao se esquecer dele. Um
    grupamento de 1000:1 lido pela regra do desdobramento da 1,00001 -- indistinguivel
    de "nada aconteceu" para qualquer teste de "veio numero?"."""
    correto, _ = r.fator_de_quantidade(Decimal("0.001"), "GRUPAMENTO")
    errado = Decimal(1)/(1 + Decimal("0.001")/100)          # a regra do desdobramento
    assert correto == Decimal("1000")
    assert abs(errado - 1) < Decimal("0.0001"), "o erro seria INVISIVEL, e e esse o ponto"


def test_C01_o_que_a_regra_RECUSA():
    """A recusa e parte da regra. INCORPORACAO tem 2 observacoes no acervo -- duas nao
    sustentam regra, e ela e relacao de troca entre DUAS empresas, que pode nao ser a
    mesma aritmetica. Valor fora da faixa do rotulo tambem recusa: grupamento com
    `factor >= 1` seria desdobramento com etiqueta errada, e escolher qual dos dois esta
    errado seria escrever ausencia de criterio no lugar de criterio."""
    for factor, tipo in ((Decimal("100"), "INCORPORACAO"), (Decimal("2"), "CISAO"),
                         (Decimal("1"), "GRUPAMENTO"), (Decimal("2"), "GRUPAMENTO"),
                         (Decimal("0"), "GRUPAMENTO"), (Decimal("-1"), "DESDOBRAMENTO"),
                         (Decimal("0"), "BONIFICACAO"), (None, "DESDOBRAMENTO")):
        f, st = r.fator_de_quantidade(factor, tipo)
        assert f is None and st == r.FACTOR_FORA_DA_REGRA, (factor, tipo)


def test_C01_o_fator_e_multiplicador_de_PRECO_como_no_provento():
    """A convencao tem de ser UMA. `fator_de_provento` devolve `(P-valor)/P`, que e o
    que multiplica o preco historico. Se o de quantidade devolvesse multiplicador de
    QUANTIDADE, as duas colunas `fator` do mesmo CSV significariam coisas diferentes --
    e nada no arquivo avisaria."""
    # desdobramento 1:2 -> a acao vale metade, e o preco historico se multiplica por 0,5
    assert r.fator_de_quantidade(Decimal("100"), "DESDOBRAMENTO")[0] < 1
    # grupamento 10:1 -> a acao vale dez vezes mais
    assert r.fator_de_quantidade(Decimal("0.1"), "GRUPAMENTO")[0] > 1
    # provento: preco cai, fator < 1 -- mesma direcao
    assert r.fator_de_provento(Decimal("1"), Decimal("10"))[0] < 1


# ──────────────────────────────────────────────── leitura do bronze real

def _bronze(tmp_path, emissora, corpo, dia="2026-09-11"):
    """Grava no formato REAL do acervo: string JSON contendo lista (A-00 + A-02)."""
    import json
    pasta = tmp_path / "eventos" / ("dt_captura=" + dia)
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / (emissora + ".json")).write_text(json.dumps(json.dumps([corpo])),
                                              encoding="utf-8")
    return str(tmp_path)


ABEV = {
    "tradingName": "AMBEV S/A   ", "code": "ABEV", "codeCVM": "23264",
    "cashDividends": [{"assetIssued": "BRABEVACNOR1", "paymentDate": "31/12/2026",
                       "rate": "0,04490000000", "approvedOn": "04/05/2026",
                       "isinCode": "BRABEVACNOR1", "label": "JRS CAP PROPRIO",
                       "lastDatePrior": "22/06/2026"}],
    "stockDividends": [],
    "subscriptions": [{"assetIssued": "BRABEVACNOR1", "percentage": "0,13994090200",
                       "priceUnit": "16,09000000000", "subscriptionDate": "29/05/2014",
                       "approvedOn": "28/04/2014", "isinCode": "BRABEVACNOR1",
                       "label": "SUBSCRICAO", "lastDatePrior": "28/04/2014"}],
}


def test_suplemento_le_o_formato_real_do_acervo(tmp_path):
    raiz = _bronze(tmp_path, "ABEV", ABEV)
    caminho = os.path.join(raiz, "eventos", "dt_captura=2026-09-11", "ABEV.json")
    linhas, aviso = r.linhas_do_suplemento(caminho, "2026-09-11")
    assert aviso is None and len(linhas) == 2

    jcp = next(l for l in linhas if l["tipo"] == "JRS CAP PROPRIO")
    assert jcp["trading_name"] == "AMBEV S/A", "o padding da B3 tem de ser removido"
    assert jcp["code_cvm"] == "23264", "a chave estavel (A-03) viaja para o silver"
    assert jcp["ultimo_dia_com_direito"] == dt.date(2026, 6, 22), \
        "a coluna guarda lastDatePrior, e o NOME dela passou a dizer isso (16/09)"
    assert jcp["data_pagamento"] == dt.date(2026, 12, 31)
    assert jcp["valor"] == Decimal("0.04490000000")
    assert jcp["fator_status"] == r.SEM_PRECO
    assert jcp["isin"] == "BRABEVACNOR1"

    sub = next(l for l in linhas if l["tipo"] == "SUBSCRICAO")
    assert sub["fator_status"] == r.SEM_FATOR, \
        "subscricao e direito, nao ajuste de preco -- nao pode entrar num produtorio"


def test_MBRF_com_as_tres_listas_vazias_nao_quebra(tmp_path):
    """A-03: o codigo de emissora mudou (MRFG -> MBRF) e a historia ficou sob o antigo.
    Zero linhas e o resultado CERTO aqui; o alarme e do coletor, nao do refinador."""
    raiz = _bronze(tmp_path, "MBRF", {"tradingName": "MARFRIG     ", "code": "MBRF",
                                      "codeCVM": "20788", "cashDividends": [],
                                      "stockDividends": [], "subscriptions": []})
    caminho = os.path.join(raiz, "eventos", "dt_captura=2026-09-11", "MBRF.json")
    linhas, aviso = r.linhas_do_suplemento(caminho, "2026-09-11")
    assert linhas == [] and aviso is None


def test_paginado_calcula_o_fator_e_preserva_a_classe(tmp_path):
    import json
    pasta = tmp_path / "proventos" / "dt_captura=2026-09-11" / "PETR"
    pasta.mkdir(parents=True)
    (pasta / "pagina-001.json").write_text(json.dumps(json.dumps({
        "page": {"pageNumber": 1, "totalRecords": 2, "totalPages": 1},
        "results": [
            {"typeStock": "ON", "dateApproval": "30/08/2013", "valueCash": "0,65",
             "corporateAction": "DIVIDENDO", "lastDatePriorEx": "13/09/2013",
             "closingPricePriorExDate": "84,49", "ratio": "1"},
            {"typeStock": "PN", "dateApproval": "30/08/2013", "valueCash": "0,72",
             "corporateAction": "JRS CAP PROPRIO", "lastDatePriorEx": "13/09/2013",
             "closingPricePriorExDate": "80,00", "ratio": "1"},
        ]})), encoding="utf-8")
    cab = dict(cod="PETR", code_cvm="9512", trading_name="PETROBRAS",
               dt_captura="2026-09-11")
    linhas = r.linhas_do_paginado(str(pasta), "2026-09-11", cab)
    assert len(linhas) == 2
    assert {l["type_stock"] for l in linhas} == {"ON", "PN"}, \
        "o evento e por CLASSE: agregar por emissora mistura duas series"
    on = next(l for l in linhas if l["type_stock"] == "ON")
    assert on["fator_status"] == r.CALCULADO
    assert on["origem"] == "paginado"
    assert on["preco_vespera"] == Decimal("84.49")


# ────────────────────────────────────────────────── escrita determinista

def test_csv_e_deterministico_e_a_ordem_e_estavel(tmp_path):
    """Sem ordem estavel o instantaneo dourado acusa diferenca a cada rodada e deixa de
    servir como rede -- e uma rede que grita sempre e pior que nenhuma."""
    linhas = [
        dict(origem="paginado", cod="VALE", code_cvm="4170", trading_name="VALE",
             isin="", type_stock="ON", tipo="DIVIDENDO", ultimo_dia_com_direito=dt.date(2020, 3, 1),
             data_aprovacao=None, data_pagamento=None, valor=Decimal("1.5"),
             ratio=None, preco_vespera=Decimal("50"), fator=Decimal("0.97"),
             fator_status=r.CALCULADO, dt_captura="2026-09-11",
             arquivo_origem="a", sha256_origem="x"),
        dict(origem="suplemento", cod="ABEV", code_cvm="23264", trading_name="AMBEV S/A",
             isin="BRABEVACNOR1", type_stock="", tipo="JRS CAP PROPRIO",
             ultimo_dia_com_direito=dt.date(2026, 6, 22), data_aprovacao=None, data_pagamento=None,
             valor=Decimal("0.0449"), ratio=None, preco_vespera=None, fator=None,
             fator_status=r.SEM_PRECO, dt_captura="2026-09-11",
             arquivo_origem="b", sha256_origem="y"),
    ]
    a, b = str(tmp_path / "a.csv"), str(tmp_path / "b.csv")
    r.gravar_csv(linhas, a)
    r.gravar_csv(list(reversed(linhas)), b)
    texto = open(a, encoding="utf-8").read()
    assert texto == open(b, encoding="utf-8").read(), "a ordem de entrada nao pode vazar"
    assert texto.splitlines()[0] == ",".join(r.COLUNAS)
    assert texto.splitlines()[1].startswith("suplemento,ABEV"), "ordenado por cod"


def test_csv_grava_Decimal_exato_e_nunca_notacao_de_float(tmp_path):
    linhas = [dict(origem="p", cod="X", code_cvm="", trading_name="", isin="",
                   type_stock="", tipo="DIVIDENDO", ultimo_dia_com_direito=dt.date(2020, 1, 2),
                   data_aprovacao=None, data_pagamento=None,
                   valor=Decimal("0.04490000000"), ratio=None, preco_vespera=None,
                   fator=None, fator_status=r.SEM_PRECO, dt_captura="2026-09-11",
                   arquivo_origem="a", sha256_origem="x")]
    caminho = str(tmp_path / "c.csv")
    r.gravar_csv(linhas, caminho)
    texto = open(caminho, encoding="utf-8").read()
    assert "0.04490000000" in texto, "o Decimal perdeu casas ou virou float"
    assert "E-" not in texto and "e-" not in texto, "notacao cientifica no acervo"
    assert ",2020-01-02," in texto, "data em ISO no silver, sempre"


def test_a_normalizacao_vem_do_coletor_e_nao_e_reimplementada():
    """N-01 preventivo: se `refinar` reimplementasse `desembrulhar`, as duas versoes
    concordariam por acidente ate o dia em que o formato da B3 mudasse."""
    import coletar_b3
    assert r.desembrulhar is coletar_b3.desembrulhar
    assert r.sha256 is coletar_b3.sha256


def test_A06_a_guarda_anterior_media_o_sintoma_errado():
    """ACHADO A-06, 12/09/2026 -- e ele e sobre ESTE arquivo.

    O teste acima passou durante um dia inteiro contra um `desembrulhar` que so existia
    numa copia de teste. `coletar_b3.py` de producao nao tinha esse nome: a logica
    estava EMBUTIDA dentro de `coletar_eventos`. Ou seja, havia exatamente as duas
    implementacoes que a guarda existia para proibir, e ela dizia que nao.

    O defeito nao era o codigo -- era a MEDICAO. `r.desembrulhar is c.desembrulhar` mede
    se as duas variaveis apontam para o mesmo objeto. Elas apontavam. O que ninguem
    media era se o COLETOR usava a propria funcao que exporta.

    E o padrao recorrente do projeto na sua forma mais cara: um arquivo declara um
    comportamento que o codigo nao tem, e os dois concordam por acidente. Aqui o arquivo
    que declarava era o TESTE, e foi por isso que passou despercebido -- teste verde e
    a coisa que a gente nao volta a ler.

    Esta versao mede a ausencia de duplicata: `coletar_eventos` tem de CHAMAR
    `desembrulhar` e nao pode carregar uma segunda copia do desembrulho."""
    import inspect

    import coletar_b3

    fonte = inspect.getsource(coletar_b3.coletar_eventos)
    assert "desembrulhar(" in fonte, (
        "coletar_eventos nao chama desembrulhar -- ha (ou voltou a haver) uma segunda "
        "implementacao do desembrulho. Foi exatamente assim que o A-06 aconteceu.")

    # As duas linhas que FORMAM o desembrulho. Se qualquer uma reaparecer aqui, alguem
    # reimplementou -- mesmo que a chamada acima continue existindo.
    for marca in ("json.loads(texto)", "isinstance(dados, list)"):
        assert marca not in fonte, (
            "coletar_eventos voltou a desembrulhar por conta propria (%r). A leitura de "
            "formato mora em desembrulhar(), e em lugar nenhum mais." % marca)


def test_A06_desembrulhar_e_os_tres_formatos_observados():
    """Os tres formatos que a B3 devolveu de verdade, e o quarto que ela devolve quando
    da errado. A funcao nao julga nenhum deles -- so normaliza e conta."""
    import json

    import coletar_b3 as c

    # 1. objeto -- o unico que eu esperava quando escrevi a primeira versao
    assert c.desembrulhar('{"tradingName":"X"}') == ({"tradingName": "X"}, 1)
    # 2. JSON dentro de string (duplamente codificado)
    assert c.desembrulhar(json.dumps(json.dumps({"b": 3}))) == ({"b": 3}, 1)
    # 3. lista -- o formato NORMAL deste endpoint, achado A-02
    assert c.desembrulhar('[{"a":1}]') == ({"a": 1}, 1)
    # 3-b. mais de um registro: devolve o primeiro E diz quantos vieram
    assert c.desembrulhar('[{"a":1},{"a":2}]') == ({"a": 1}, 2)
    # 4. string curta de erro da propria B3 -- sai como chegou, para quem chamou tratar
    assert c.desembrulhar(json.dumps("erro")) == ("erro", 1)
    # 4-b. lista vazia nao vira dict nenhum: nao ha o que escolher
    assert c.desembrulhar("[]") == ([], 1)


# ───────────────────────── A-07: o que o silver escolhia em silencio

def test_A07_mais_de_um_registro_e_ACUSADO(tmp_path):
    """Escolher o primeiro de dois registros e uma decisao. Toma-la sem dizer e
    escrever ausencia de criterio no lugar de criterio -- o F-02 na veia."""
    caminho = tmp_path / "XPTO.json"
    caminho.write_text(
        '[{"code":"XPTO","codeCVM":"1","tradingName":"PRIMEIRO","cashDividends":[]},'
        ' {"code":"XPTO","codeCVM":"1","tradingName":"SEGUNDO","cashDividends":[]}]',
        encoding="utf-8")
    multiplos = {}
    linhas, aviso = r.linhas_do_suplemento(str(caminho), "2026-09-11", None, multiplos)
    assert multiplos == {"XPTO.json": 2}, "a contagem sumiu antes do relatorio"


def test_A07_registro_unico_nao_polui_o_relatorio(tmp_path):
    caminho = tmp_path / "UNO.json"
    caminho.write_text('[{"code":"UNO","codeCVM":"2","tradingName":"UNO SA"}]',
                       encoding="utf-8")
    multiplos = {}
    r.linhas_do_suplemento(str(caminho), "2026-09-11", None, multiplos)
    assert multiplos == {}, "aviso para o caso normal vira ruido, e ruido se ignora"


def test_A07_pagina_que_nao_e_objeto_nao_some_calada(tmp_path):
    """A MESMA condicao era aviso no suplemento e `continue` mudo no paginado. A muda
    vencia, porque e a que roda 8 mil vezes."""
    pasta = tmp_path / "XPTO"
    pasta.mkdir()
    (pasta / "pagina-1.json").write_text('"Servico indisponivel"', encoding="utf-8")
    (pasta / "pagina-2.json").write_text(
        '{"results":[{"corporateAction":"DIVIDENDO","valueCash":"1,00",'
        '"closingPricePriorExDate":"10,00","lastDatePriorEx":"02/01/2020",'
        '"dateApproval":"02/01/2020","ratio":"","typeStock":"ON"}]}', encoding="utf-8")
    cab = dict(cod="XPTO", code_cvm="1", trading_name="XPTO SA", dt_captura="2026-09-11")
    perdidas = []
    linhas = r.linhas_do_paginado(str(pasta), "2026-09-11", cab, None, None, perdidas)
    assert perdidas == [os.path.join("XPTO", "pagina-1.json")]
    assert len(linhas) == 1, "a pagina boa tem de entrar mesmo com a vizinha quebrada"


# ───────────────────────────────────────── A-05: enumeracao observada

def test_A05_tipo_conhecido_passa():
    d = {}
    for t in ("DIVIDENDO", "JRS CAP PROPRIO", "DESDOBRAMENTO", "INCORPORACAO",
              "SUBSCRICAO", "dividendo", "  BONIFICACAO  "):
        assert r.conferir_tipo(t, d) is True, t
    assert d == {}, "tipo conhecido nao pode virar desconhecido"


def test_A05_tipo_fora_da_lista_e_ACUSADO_e_nao_descartado():
    """A regra que o projeto escreveu para a CVM e nao tinha aqui: valor fora da
    enumeracao OBSERVADA falha ruidosamente. Nem descarta a linha (perderia dado), nem
    adivinha o tratamento (seria o F-02)."""
    d = {}
    assert r.conferir_tipo("EVENTO NOVO DA B3", d) is False
    assert r.conferir_tipo("EVENTO NOVO DA B3", d) is False
    assert d == {"EVENTO NOVO DA B3": 2}, "conta as ocorrencias, nao so marca"


def test_A05_INCORPORACAO_esta_na_lista_e_o_motivo_importa():
    """Achada em 12/09 ao investigar o A-03: BRFS devolveu um evento INCORPORACAO, que
    nenhuma lista deste modulo previa e que teria entrado em silencio.

    Incorporacao troca acoes de UMA empresa por acoes de OUTRA. Nao e so ajuste de
    preco: e mudanca de IDENTIDADE. Tratar como evento comum juntaria duas series."""
    assert "INCORPORACAO" in r.TIPOS_OBSERVADOS
    assert "INCORPORACAO" in r.TIPOS_DE_QUANTIDADE
    assert "INCORPORACAO" not in r.TIPOS_DE_CAIXA


def test_A05_a_lista_e_OBSERVADA_e_o_teste_diz_isso():
    """Enumeracao observada numa amostra nao e enumeracao completa -- e a advertencia
    literal de `cvm-enumeracoes-observadas.md`. Este teste guarda a INTENCAO: se alguem
    acrescentar um tipo, tem de ser porque o observou, nao porque o codigo reclamou."""
    assert set(r.TIPOS_OBSERVADOS) == set(
        r.TIPOS_DE_CAIXA + r.TIPOS_DE_QUANTIDADE + r.TIPOS_DE_DIREITO)
    assert len(set(r.TIPOS_OBSERVADOS)) == len(r.TIPOS_OBSERVADOS), "tipo repetido"


def test_A05_tipo_desconhecido_no_suplemento_marca_a_linha(tmp_path):
    raiz = _bronze(tmp_path, "XXXX", {
        "tradingName": "TESTE", "code": "XXXX", "codeCVM": "1",
        "cashDividends": [{"rate": "1,00", "label": "EVENTO QUE NAO EXISTE",
                           "lastDatePrior": "01/03/2020", "isinCode": "BRXXXX"}],
        "stockDividends": [], "subscriptions": []})
    caminho = os.path.join(raiz, "eventos", "dt_captura=2026-09-11", "XXXX.json")
    desconhecidos = {}
    linhas, _ = r.linhas_do_suplemento(caminho, "2026-09-11", desconhecidos)
    assert len(linhas) == 1, "a linha NAO pode ser descartada"
    assert linhas[0]["fator_status"] == r.TIPO_DESCONHECIDO
    assert linhas[0]["valor"] == Decimal("1.00"), "o dado bruto continua la"
    assert desconhecidos == {"EVENTO QUE NAO EXISTE": 1}


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

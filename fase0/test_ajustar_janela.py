# -*- coding: utf-8 -*-
"""
test_ajustar_janela.py -- o ajuste de precos sobre a janela CONTIGUA 2021-2025 (21/09/2026).

PLANO.md, passo 3. Escrita ANTES da primeira corrida sobre a janela: os criterios dos
testes contra o acervo sao os do C-02 para 2023, aplicados a CADA ano, e foram fixados
sem ter visto numero nenhum de 2021, 2022, 2024 ou 2025. Se um ano reprovar, isso e
achado -- nao limiar a afrouxar.

O QUE A JANELA TEM DE PROVAR QUE UM ANO SO NAO PROVA

  1. A EMENDA. O ajuste e retroativo: um evento cujo ultimo dia com direito e o ultimo
     pregao de um ano so ganha data ex quando o ano seguinte esta no calendario. Em 2023
     isoladamente eram 8 eventos (A-08, `NIVEL_INCERTO`); na janela contigua eles tem de
     virar ajuste aplicado em 02/01/2024.
  2. A DATA EX VEM DO CALENDARIO DA JANELA, e nao do calendario com que o silver foi
     gravado. O silver de 11/09 foi derivado com o calendario de 2023 so -- entao todo
     evento de 2021, 2022, 2024 e 2025 chega `FORA_DA_COBERTURA`. A rederivacao usa a MESMA
     funcao (`calendario.proximo_pregao`), e onde as duas derivaram, tem de concordar.
  3. O C-01 CONTRA O PRECO, com mais de um caso. Em 2023 havia UM evento de quantidade. A
     janela traz desdobramentos, bonificacoes e os primeiros GRUPAMENTOS com preco.

E O QUE ELA NAO PODE FAZER: reescrever a descoberta de arquivo ou o parser (N-01). A
janela e um FILTRO sobre `calendario.arquivos()`, e o teste de guarda esta aqui.
"""

import csv
import datetime as dt
import inspect
import os
import sys
from decimal import Decimal

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ajustar as A                                                     # noqa: E402
import calendario                                                       # noqa: E402
from test_ajustar import _registro, _cotahist, _evento, _silver         # noqa: E402

RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ_COTAHIST = os.path.join(RAIZ_REPO, "data", "bronze", "b3", "cotahist")
SILVER_ACERVO = os.path.join(RAIZ_REPO, "data", "silver", "eventos_silver_2026-09-11.csv")
DEGRAU_2023 = os.path.join(RAIZ_REPO, "data", "silver", "degrau_datas_ex_2026-09-11.csv")
JANELA = tuple(range(2021, 2026))
ISIN = "BRTESTACNOR1"          # 12 posicoes, como o campo CODISI


def _ano(pasta, ano, dias_precos, ticker="TESTE3"):
    """Um COTAHIST sintetico de UM ano, com o header real (P-109)."""
    return _cotahist(pasta, "COTAHIST_A%d.TXT" % ano,
                     [_registro(d, ticker, p, isin=ISIN) for d, p in dias_precos])


def _duas_pontas(pasta):
    """2021 termina em 30/12 a R$10; 2022 abre em 03/01 a R$5. Um desdobramento 2:1 com
    ultimo dia com direito no ULTIMO pregao de 2021 -- o caso A-08, em miniatura."""
    _ano(pasta, 2021, [("20211228", 1000), ("20211229", 1000), ("20211230", 1000)])
    _ano(pasta, 2022, [("20220103", 500), ("20220104", 500), ("20220105", 500)])
    return str(pasta)


def _desdobramento_na_virada(**extra):
    campos = dict(origem="suplemento", cod="TEST", type_stock="", isin=ISIN,
                  tipo="DESDOBRAMENTO", ultimo_dia_com_direito="2021-12-30",
                  data_ex="", data_ex_status="FORA_DA_COBERTURA",
                  ratio="100.00000000000", fator="0.5")
    campos.update(extra)
    return _evento(**campos)


# ─────────────────────────────────────────── a janela e um FILTRO, nao um leitor

def test_arquivos_filtra_por_ano_e_sem_filtro_nao_muda_nada(tmp_path):
    for ano in (2020, 2021, 2022, 2023):
        _ano(tmp_path, ano, [("%d0105" % ano, 1000)])
    todos = calendario.arquivos(str(tmp_path))
    assert calendario.arquivos(str(tmp_path), None) == todos
    assert sorted(calendario.arquivos(str(tmp_path), (2021, 2022))) == [
        "COTAHIST_A2021", "COTAHIST_A2022"]


def test_pregoes_da_janela_so_tem_dias_da_janela(tmp_path):
    for ano in (2020, 2021, 2022):
        _ano(tmp_path, ano, [("%d0105" % ano, 1000), ("%d0106" % ano, 1000)])
    datas, cob = calendario.pregoes(str(tmp_path), (2021,))
    assert {d.year for d in datas} == {2021}
    assert cob == (dt.date(2021, 1, 5), dt.date(2021, 1, 6))


def test_janela_le_o_texto_da_linha_de_comando():
    assert A.janela("2021-2025") == (2021, 2022, 2023, 2024, 2025)
    assert A.janela("2023") == (2023,)
    for ruim in ("2025-2021", "abc", "2021-", "21-25"):
        with pytest.raises(ValueError):
            A.janela(ruim)


def test_janela_com_BURACO_e_recusada_e_diz_qual_ano_falta(tmp_path):
    """Anos salteados nao formam serie: o ajuste retroativo so atravessa um bloco
    contiguo. Sem 2022, a serie saltaria de 2021 para 2023 como se fosse um pregao, e os
    eventos de 2022 sumiriam sem ninguem ver."""
    for ano in (2021, 2023):
        _ano(tmp_path, ano, [("%d0105" % ano, 1000)])
    with pytest.raises(A.JanelaComBuraco, match="2022"):
        A.conferir_janela(str(tmp_path), (2021, 2022, 2023))


def test_janela_SALTEADA_e_recusada_mesmo_com_os_arquivos_presentes(tmp_path):
    for ano in (2021, 2022, 2023):
        _ano(tmp_path, ano, [("%d0105" % ano, 1000)])
    with pytest.raises(A.JanelaComBuraco):
        A.conferir_janela(str(tmp_path), (2021, 2023))


def test_ano_ILEGIVEL_dentro_da_janela_falha_alto_e_nao_vira_ano_vazio(tmp_path):
    """P-99/P-100: um ZIP truncado dentro da janela nao pode virar "um ano sem pregao".
    Isso seria um buraco na serie com cara de serie inteira."""
    _ano(tmp_path, 2021, [("20210105", 1000)])
    with open(os.path.join(str(tmp_path), "COTAHIST_A2022.ZIP"), "wb") as f:
        f.write(b"PK\x03\x04 cortado")
    with pytest.raises(calendario.AcervoIlegivel):
        A.cotacoes(str(tmp_path), (2021, 2022))


def test_cotacoes_da_janela_nao_le_ano_de_fora(tmp_path):
    _ano(tmp_path, 2020, [("20200105", 1000)])
    _ano(tmp_path, 2021, [("20210105", 1000)])
    ac = A.cotacoes(str(tmp_path), (2021,))
    assert set(ac.precos["TESTE3"]) == {dt.date(2021, 1, 5)}
    assert sorted(ac.arquivos) == ["COTAHIST_A2021"]


def test_N01_ajustar_nao_abre_zip_nem_acha_arquivo_sozinho():
    """A descoberta de arquivo e o parser do registro sao do `calendario.py`. Se um dia
    alguem precisar de `zipfile` aqui, e sinal de que a regra esta sendo redigitada."""
    fonte = inspect.getsource(A)
    assert "import zipfile" not in fonte and "zipfile." not in fonte
    assert "def arquivos" not in fonte and "def registros" not in fonte
    assert "def ano_de" not in fonte


# ──────────────────────────────────── a data ex vem do calendario da JANELA

def test_rederiva_a_data_ex_que_o_silver_nao_alcancava(tmp_path):
    raiz = _duas_pontas(tmp_path)
    datas, cob = calendario.pregoes(raiz, (2021, 2022))
    [r], rederivadas = A.rederivar_data_ex([_desdobramento_na_virada()], datas, cob)
    assert r["data_ex"] == "2022-01-03" and r["data_ex_status"] == "DERIVADA"
    assert rederivadas == 1


def test_a_data_ex_segue_o_PREGAO_observado_e_nao_o_dia_util(tmp_path):
    """Carnaval de 2022: sexta 25/02, e o pregao seguinte e quarta 02/03. Nenhuma regra
    de dia util acerta isso -- o calendario observado acerta."""
    _ano(tmp_path, 2022, [("20220224", 1000), ("20220225", 1000), ("20220302", 1000)])
    datas, cob = calendario.pregoes(str(tmp_path), (2022,))
    ev = _desdobramento_na_virada(ultimo_dia_com_direito="2022-02-25")
    [r], _ = A.rederivar_data_ex([ev], datas, cob)
    assert r["data_ex"] == "2022-03-02"


def test_silver_e_janela_DIVERGINDO_sobre_a_data_ex_levanta(tmp_path):
    """Se o silver derivou uma data e o calendario da janela deriva outra, os dois
    calendarios discordam sobre o que foi pregao. Escolher um em silencio seria decidir
    qual fonte esta errada sem medir."""
    raiz = _duas_pontas(tmp_path)
    datas, cob = calendario.pregoes(raiz, (2021, 2022))
    ev = _desdobramento_na_virada(data_ex="2022-01-04", data_ex_status="DERIVADA")
    with pytest.raises(A.DataExDivergente, match="2022-01-04"):
        A.rederivar_data_ex([ev], datas, cob)


def test_silver_e_janela_CONCORDANDO_nao_conta_como_rederivada(tmp_path):
    raiz = _duas_pontas(tmp_path)
    datas, cob = calendario.pregoes(raiz, (2021, 2022))
    ev = _desdobramento_na_virada(data_ex="2022-01-03", data_ex_status="DERIVADA")
    [r], rederivadas = A.rederivar_data_ex([ev], datas, cob)
    assert r["data_ex"] == "2022-01-03" and rederivadas == 0


def test_fora_do_calendario_da_janela_a_linha_diz_que_nao_sabe(tmp_path):
    raiz = _duas_pontas(tmp_path)
    datas, cob = calendario.pregoes(raiz, (2021, 2022))
    ev = _desdobramento_na_virada(ultimo_dia_com_direito="2019-06-10")
    [r], _ = A.rederivar_data_ex([ev], datas, cob)
    assert r["data_ex"] == "" and r["data_ex_status"] == "FORA_DA_COBERTURA"


# ──────────────────────────────────────────── a EMENDA: o motivo da contiguidade

def test_A08_a_EMENDA_fecha_a_borda_e_o_degrau_da_virada_some(tmp_path):
    """O caso que o passo 3 existe para fechar. Com 2021 so, o desdobramento de 30/12 nao
    tem data ex e a serie fica `NIVEL_INCERTO`; com 2021+2022, ele cai em 03/01, e o
    retorno da virada de ano sai de -50% para zero."""
    raiz = _duas_pontas(tmp_path)
    sil = _silver(tmp_path, [_desdobramento_na_virada()])

    so_2021 = A.medir(raiz, sil, (2021,))
    assert so_2021.diag["TESTE3"]["status"] == A.NIVEL_INCERTO
    assert not so_2021.fat

    jan = A.medir(raiz, sil, (2021, 2022))
    assert jan.diag["TESTE3"]["status"] == A.AJUSTADO
    [g] = jan.degraus
    assert g.data_ex == dt.date(2022, 1, 3)
    assert g.retorno_bruto == -0.5 and g.retorno_ajustado == 0.0


def test_A08_sem_a_emenda_o_NIVEL_de_2021_fica_errado_pelo_fator_inteiro(tmp_path):
    """E a razao de o A-08 importar: ao emendar anos ajustados SEPARADAMENTE, o nivel de
    2021 fica 2x acima do que devia. Nenhum retorno de dentro de 2021 acusa isso."""
    raiz = _duas_pontas(tmp_path)
    sil = _silver(tmp_path, [_desdobramento_na_virada()])
    jan = A.medir(raiz, sil, (2021, 2022))
    aj = jan.ajustadas["TESTE3"]
    assert aj[dt.date(2021, 12, 30)][0] == Decimal("5")
    assert aj[dt.date(2022, 1, 3)][0] == Decimal("5")


# ─────────────────────────── a janela larga cria AMBIGUIDADE que o ano isolado nao tinha

def _duas_units(pasta):
    """XPTO11 negocia 2021 e 2022; XPTO13 -- uma UNT temporaria -- so 2021. E o caso real
    do BPAC13 contra o BPAC11, em miniatura: os dois tem ESPECI `UNT`."""
    _cotahist(pasta, "COTAHIST_A2021.TXT",
              [_registro("20210105", "XPTO11", 1000, especi="UNT     N2"),
               _registro("20210105", "XPTO13", 900, especi="UNT     N2")])
    _cotahist(pasta, "COTAHIST_A2022.TXT",
              [_registro("20220104", "XPTO11", 1000, especi="UNT     N2"),
               _registro("20220105", "XPTO11", 990, especi="UNT     N2")])
    return str(pasta)


def test_VIGENCIA_desfaz_a_ambiguidade_pelo_pregao_da_data_ex(tmp_path):
    """Em 2022 so o XPTO11 negocia. O XPTO13 nao pode ser o papel de um evento cuja data
    ex ele nem viu -- e isso e OBSERVADO no COTAHIST, nao inferido de nome."""
    ac = A.cotacoes(_duas_units(tmp_path), (2021, 2022))
    ev = _evento(cod="XPTO", type_stock="UNT", data_ex="2022-01-05")
    [c], fora = A.casar([ev], ac.papeis, ac.precos)
    assert fora == [] and c["_ticker"] == "XPTO11" and c["_como"] == "PREFIXO+ESPECI+VIGENCIA"


def test_VIGENCIA_nao_inventa_quando_os_dois_negociam_na_data(tmp_path):
    ac = A.cotacoes(_duas_units(tmp_path), (2021, 2022))
    ev = _evento(cod="XPTO", type_stock="UNT", data_ex="2021-01-05")
    [], [f] = A.casar([ev], ac.papeis, ac.precos)
    assert f["_motivo"] == "AMBIGUO"


def test_VIGENCIA_sem_data_ex_continua_AMBIGUO(tmp_path):
    ac = A.cotacoes(_duas_units(tmp_path), (2021, 2022))
    [], [f] = A.casar([_evento(cod="XPTO", type_stock="UNT", data_ex="")], ac.papeis,
                      ac.precos)
    assert f["_motivo"] == "AMBIGUO"


# ───────────────────────────────────────────────────── a medicao POR ANO

def test_controle_por_ano_soma_o_controle(tmp_path):
    raiz = _duas_pontas(tmp_path)
    sil = _silver(tmp_path, [_desdobramento_na_virada()])
    m = A.medir(raiz, sil, (2021, 2022))
    pa = A.controle_por_ano(m.acervo, m.ajustadas, m.fat)
    assert set(pa) == {2021, 2022}
    assert sum(v[0] for v in pa.values()) == A.controle(m.acervo, m.ajustadas, m.fat)[0]
    # 2021: dois pares sem evento; 2022: 03/01 e dia ex (fora), 04 e 05 entram
    assert pa[2021][0] == 2 and pa[2022][0] == 2


def test_por_ano_separa_os_degraus_pela_data_ex():
    d = lambda a, m, dd: dt.date(a, m, dd)                                  # noqa: E731
    gs = [A.Degrau("X3", d(2021, 5, 3), d(2021, 4, 30), "DIVIDENDO", 1, Decimal("0.99"),
                   Decimal(10), Decimal("9.9"), -0.01, 0.0, "", ""),
          A.Degrau("X3", d(2022, 5, 3), d(2022, 5, 2), "DIVIDENDO", 1, Decimal("0.98"),
                   Decimal(10), Decimal("9.8"), -0.02, 0.0, "", ""),
          A.Degrau("Y3", d(2022, 6, 1), d(2022, 5, 31), "DESDOBRAMENTO", 1, Decimal("0.5"),
                   Decimal(10), Decimal(5), -0.5, 0.0, "", "")]
    pa = A.degraus_por_ano(gs)
    assert pa[2021]["n"] == 1 and pa[2022]["n"] == 2
    assert pa[2022]["quantidade"] == 1 and pa[2021]["quantidade"] == 0


def test_e_de_quantidade_olha_o_TIPO_inteiro_e_nao_um_pedaco_de_texto():
    assert A.e_de_quantidade("DIVIDENDO+DESDOBRAMENTO")
    assert A.e_de_quantidade("GRUPAMENTO")
    assert not A.e_de_quantidade("DIVIDENDO+JRS CAP PROPRIO")
    assert not A.e_de_quantidade("")


def test_a_corrida_da_janela_grava_com_SUFIXO_e_a_padrao_sem(tmp_path, capsys):
    raiz = _duas_pontas(tmp_path)
    saida = os.path.join(str(tmp_path), "silver")
    os.makedirs(saida)
    _silver(saida, [_desdobramento_na_virada()])
    assert A.ajustar(raiz, None, saida, (2021, 2022)) == 0
    nomes = sorted(os.listdir(saida))
    assert "precos_ajustados_2026-09-11_2021-2022.csv" in nomes
    assert "degrau_datas_ex_2026-09-11_2021-2022.csv" in nomes
    assert "precos_ajustados_2026-09-11.csv" not in nomes
    out = capsys.readouterr().out
    assert "POR ANO" in out and "2022" in out
    with open(os.path.join(saida, "degrau_datas_ex_2026-09-11_2021-2022.csv"),
              encoding="utf-8") as f:
        [linha] = list(csv.DictReader(f))
    assert linha["data_ex"] == "2022-01-03" and float(linha["retorno_ajustado"]) == 0.0


def test_marca_de_ex_le_o_token_e_nao_a_classe():
    assert A.marca_de_ex("ON  EDB N1") == "EDB"
    assert A.marca_de_ex("PN  EJ  N1") == "EJ"
    assert A.marca_de_ex("ON      NM") == ""
    assert A.marca_de_ex("") == ""


def test_mercado_do_dia_e_MEDIANA_e_ignora_o_papel_com_evento(tmp_path):
    """Tres papeis sobem 1%, um cai 50% num desdobramento. O mercado do dia e +1%: o
    papel com evento nao entra, e mesmo que entrasse a mediana nao se moveria por ele."""
    linhas = []
    for tk in ("AAAA3", "BBBB3", "CCCC3", "DDDD3"):
        linhas.append(_registro("20220103", tk, 1000))
        linhas.append(_registro("20220104", tk, 500 if tk == "DDDD3" else 1010))
    _cotahist(tmp_path, "COTAHIST_A2022.TXT", linhas)
    ac = A.cotacoes(str(tmp_path))
    fat = {("DDDD3", dt.date(2022, 1, 4)): (Decimal("0.5"), ["DESDOBRAMENTO"])}
    merc = A.mercado_do_dia(ac, fat, ac.precos, minimo=3)
    assert abs(merc[dt.date(2022, 1, 4)] - 0.01) < 1e-12
    assert A.mercado_do_dia(ac, fat, ac.precos, minimo=4) == {}


def test_classe_do_degrau_separa_o_que_mede_o_AJUSTE_do_que_mede_o_ACERVO():
    d = dt.date(2022, 5, 2)
    g = lambda tipos, esp: A.Degrau("CMIG3", d, d, tipos, 1, Decimal("0.98"),      # noqa: E731
                                    Decimal(1), Decimal(1), 0.0, 0.0, "", esp)
    assert A.classe_do_degrau(g("BONIFICACAO", "ON  EB  N1"), set()) == "QUANTIDADE"
    assert A.classe_do_degrau(g("DIVIDENDO", "ON  EDB N1"), set()) == "MARCA_SEM_EVENTO"
    assert A.classe_do_degrau(g("DIVIDENDO", "ON  ED  N1"), {("CMIG3", d)}) == "CONTAMINADO"
    assert A.classe_do_degrau(g("DIVIDENDO", "ON  ED  N1"), set()) == "LIMPO"


def test_queda_por_provento_e_1_quando_o_preco_cai_o_provento():
    assert A.queda_por_provento([(0.0, 0.02), (0.0, 0.05)]) == (2, 1.0)
    n, q = A.queda_por_provento([(-0.002, 0.01), (-0.004, 0.02)])
    assert n == 2 and abs(q - 1.2) < 1e-12


def test_main_aceita_anos(tmp_path):
    raiz = _duas_pontas(tmp_path)
    saida = os.path.join(str(tmp_path), "silver")
    os.makedirs(saida)
    _silver(saida, [_desdobramento_na_virada()])
    assert A.main(["--raiz", raiz, "--saida", saida, "--anos", "2021-2022"]) == 0


def test_main_com_janela_de_buraco_sai_com_2_e_nao_grava(tmp_path):
    raiz = _duas_pontas(tmp_path)
    saida = os.path.join(str(tmp_path), "silver")
    os.makedirs(saida)
    _silver(saida, [_desdobramento_na_virada()])
    assert A.main(["--raiz", raiz, "--saida", saida, "--anos", "2021-2023"]) == 2
    assert not [n for n in os.listdir(saida) if n.startswith("precos_ajustados")]


# ═══════════════════════════════════════════ contra o acervo real, 2021-2025 ═══

def _janela_no_disco():
    if not os.path.isfile(SILVER_ACERVO) or not os.path.isdir(RAIZ_COTAHIST):
        return False
    return all("COTAHIST_A%d" % a in calendario.arquivos(RAIZ_COTAHIST, JANELA)
               for a in JANELA)


acervo = pytest.mark.skipif(not _janela_no_disco(),
                            reason="COTAHIST 2021-2025 ausente -- ESTES TESTES NAO RODARAM")


@pytest.fixture(scope="module")
def jan():
    """Cinco anos de COTAHIST, 635 mil registros a vista. Uma leitura por modulo."""
    if not _janela_no_disco():
        pytest.skip("COTAHIST 2021-2025 ausente -- ESTES TESTES NAO RODARAM")
    return A.medir(RAIZ_COTAHIST, SILVER_ACERVO, JANELA)


# O PRE-REGISTRO REPROVOU EM QUATRO ANOS, e fica escrito como foi. Decisao dele, 21/09:
# xfail ESTRITO -- a reprovacao continua visivel, e se um ano passar a suite avisa, porque
# ai o texto que explica a reprovacao deixou de ser verdade. As causas foram MEDIDAS
# depois de ver (auditoria/C02-JANELA-2021-2025.md), e nenhuma e o ajuste errando:
_REPROVOU = {
    2021: "bruto: 17 desdobramentos na media; ajustado: BRAP3/4 CONTAMINADO (-54%) e 3 dias "
          "com marca de bonificacao sem evento no silver",
    2022: "ajustado -0,42% t -2,12: 4 dias com marca de bonificacao sem evento no silver "
          "(CMIG3/4 -27%) e o dividendo caindo 1,16x o valor",
    2024: "bruto POSITIVO pelo grupamento da MGLU3 (+896%); ajustado -0,30% t -3,2, e "
          "descontado o mercado ainda -0,20% t -2,5: o dividendo caindo 1,16x o valor",
    2025: "bruto POSITIVO pelo grupamento da HAPV3 (+1378%)",
}


@acervo
@pytest.mark.parametrize("ano", [
    pytest.param(a, marks=pytest.mark.xfail(strict=True, reason=_REPROVOU[a]))
    if a in _REPROVOU else a for a in JANELA])
@pytest.mark.slow
def test_REAL_O_DEGRAU_ENCOLHE_em_CADA_ano(jan, ano):
    """O criterio do C-02 para 2023, pre-registrado aqui para os outros quatro ANTES de
    medi-los. O controle esta no teste seguinte, e um nao vale sem o outro.

    O defeito do CRITERIO, que so a janela mostrou: ele mistura evento de quantidade na
    media (um grupamento de 15:1 e +1378% no bruto) e supoe que o dia ex ajustado tem
    retorno zero -- quando ele tem o do mercado, e o dividendo tira do preco mais do que
    paga. Em 2023 um evento de quantidade so e um mercado em alta nos dias ex o fizeram
    passar."""
    pa = A.degraus_por_ano(jan.degraus)[ano]
    assert pa["n"] >= 30, "%d: so %d datas ex -- a populacao e pequena demais" % (ano, pa["n"])
    assert pa["media_bruta"] < 0 and pa["t_bruto"] < -3, (ano, pa)
    assert abs(pa["media_ajustada"]) < 0.002, (ano, pa)
    assert abs(pa["t_ajustado"]) < 2.0, (ano, pa)
    assert abs(pa["media_ajustada"]) < abs(pa["media_bruta"]) / 10, (ano, pa)


@acervo
@pytest.mark.slow
def test_REAL_CONTROLE_em_cada_ano_o_dia_sem_evento_nao_mudou(jan):
    pa = A.controle_por_ano(jan.acervo, jan.ajustadas, jan.fat)
    assert set(pa) == set(JANELA)
    for ano, (pares, div, pior) in sorted(pa.items()):
        assert pares > 50000, "%d: %d pares" % (ano, pares)
        assert pior < 1e-24, "%d: %d de %d pares mudaram, pior %.1e" % (ano, div, pares, pior)


@acervo
@pytest.mark.slow
def test_REAL_2023_dentro_da_janela_e_o_2023_de_18_09(jan):
    """O instantaneo dourado da MEDICAO: os 293 degraus de 2023 medidos sozinhos em 18/09
    tem de reaparecer na janela, os mesmos, com o mesmo retorno. O retorno ajustado de um
    dia nao depende do nivel -- os eventos de 2024 e 2025 reescalam os dois precos pelo
    mesmo acumulado."""
    if not os.path.isfile(DEGRAU_2023):
        pytest.skip("degrau de 2023 ausente")
    with open(DEGRAU_2023, encoding="utf-8") as f:
        antes = {(r["ticker"], r["data_ex"]): r for r in csv.DictReader(f)}
    agora = {(g.ticker, g.data_ex.isoformat()): g for g in jan.degraus
             if g.data_ex.year == 2023}
    # CORRIGIDO na primeira corrida (21/09), e o erro era meu e dedutivel: eu escrevi
    # `set(agora) == set(antes)` pensando so na borda DIREITA do 2023 isolado. A P-94 diz
    # que a janela isolada tem DUAS -- e a esquerda tambem fecha: evento com ultimo dia
    # com direito em 29/12/2022 so ganha data ex (02/01/2023) quando 2022 esta no
    # calendario. Os extras tem de ser exatamente esses, e nenhum outro.
    assert set(antes) <= set(agora)
    extras = set(agora) - set(antes)
    assert extras and {d for _tk, d in extras} == {"2023-01-02"}, sorted(extras)
    for k, r in antes.items():
        g = agora[k]
        assert g.retorno_bruto == float(r["retorno_bruto"]), k
        assert abs(g.retorno_ajustado - float(r["retorno_ajustado"])) < 1e-12, k


@acervo
@pytest.mark.slow
def test_REAL_A08_a_borda_de_2023_FECHOU_na_emenda(jan):
    """Os 8 eventos de 28/12/2023 que o 2023 isolado deixava `NIVEL_INCERTO` (B3SA3,
    CMIN3, ENGI3, ENGI4, ENGI11, ITUB3, ITUB4) agora tem data ex -- 02/01/2024 -- e
    entram na serie."""
    for tk in ("B3SA3", "CMIN3", "ENGI3", "ENGI4", "ENGI11", "ITUB3", "ITUB4"):
        assert (tk, dt.date(2024, 1, 2)) in jan.fat, tk


@acervo
@pytest.mark.slow
def test_REAL_a_rederivacao_nao_contradisse_o_silver_em_2023(jan):
    """Onde o silver ja tinha derivado (2023), a janela derivou o mesmo -- senao `medir`
    teria levantado `DataExDivergente`. Este teste diz que ele de fato RODOU sobre elas."""
    ja_derivadas = sum(1 for r in jan.evs if r["data_ex_status"] == "DERIVADA")
    assert ja_derivadas > 300
    assert jan.concordantes == ja_derivadas
    assert jan.rederivadas > 1000


def _grandes(gs):
    """Evento de quantidade cujo fator move o preco por 1,5x ou mais -- os que o preco
    resolve com folga, porque o sinal e muito maior que o sigma diario (~1,9%)."""
    return [g for g in gs if A.e_de_quantidade(g.tipos)
            and (g.fator <= Decimal("0.67") or g.fator >= Decimal("1.5"))]


@acervo
@pytest.mark.slow
def test_REAL_C01_os_eventos_de_QUANTIDADE_encolhem(jan):
    """A ponta que o C-02 deixou aberta: a leitura PERCENTUAL do `factor`, com mais de um
    caso de preco. Pre-registrado: >= 40 casos, >= 80% deles encolhendo, e a media do
    residuo absoluto a um quinto da do degrau bruto."""
    q = [g for g in jan.degraus if A.e_de_quantidade(g.tipos)]
    assert len(q) >= 40, "so %d eventos de quantidade" % len(q)
    encolheu = sum(1 for g in q if abs(g.retorno_ajustado) < abs(g.retorno_bruto))
    assert encolheu / len(q) >= 0.8, "%d de %d" % (encolheu, len(q))
    mb = sum(abs(g.retorno_bruto) for g in q) / len(q)
    ma = sum(abs(g.retorno_ajustado) for g in q) / len(q)
    assert ma < mb / 5, (ma, mb)


@acervo
@pytest.mark.slow
def test_REAL_C01_todo_evento_GRANDE_fica_dentro_de_15pc(jan):
    grandes = _grandes(jan.degraus)
    assert len(grandes) >= 10
    fora = [(g.ticker, str(g.data_ex), g.tipos, float(g.retorno_ajustado)) for g in grandes
            if abs(g.retorno_ajustado) >= 0.15]
    assert not fora, fora


@acervo
@pytest.mark.slow
def test_REAL_C01_o_GRUPAMENTO_tem_confirmacao_de_preco(jan):
    """Item 4 do "o que continua aberto" do C-02: os 41 grupamentos eram todos fora de
    2023. O preco do grupamento SOBE no dia ex; ajustado, tem de ficar no ruido."""
    gr = [g for g in jan.degraus if g.tipos == "GRUPAMENTO"]
    assert gr, "nenhum grupamento isolado com preco na janela"
    for g in gr:
        assert g.retorno_bruto > 0.5, (g.ticker, g.data_ex, g.retorno_bruto)
        assert abs(g.retorno_ajustado) < 0.15, (g.ticker, g.data_ex, g.retorno_ajustado)


@acervo
@pytest.mark.slow
def test_REAL_C01_MUTACAO_a_leitura_TROCADA_reprova_os_grandes(jan):
    """A alternativa que o C-01 descartou pela distribuicao, agora contra o preco: `factor`
    como MULTIPLICADOR no desdobramento/bonificacao (100 -> 100x), e a regra do
    desdobramento aplicada ao grupamento (0,1 -> 1,001). Se ela tambem passasse, a
    medicao nao distinguiria nada."""
    mut = {}
    for r in jan.casados:
        if r["fator_status"] != "CALCULADO" or r["data_ex_status"] != "DERIVADA":
            continue
        f = Decimal(r["fator"])
        if r["tipo"] in ("DESDOBRAMENTO", "BONIFICACAO"):
            f = Decimal(1) / Decimal(r["ratio"])
        elif r["tipo"] == "GRUPAMENTO":
            f = Decimal(1) / (1 + Decimal(r["ratio"]) / 100)
        k = (r["_ticker"], dt.date.fromisoformat(r["data_ex"]))
        f0, t0 = mut.get(k, (Decimal(1), []))
        mut[k] = (f0 * f, t0 + [r["tipo"]])
    gm = A.degraus(jan.acervo, A.ajustar_tudo(jan.acervo, mut), mut)
    certos = {(g.ticker, g.data_ex) for g in _grandes(jan.degraus)}
    grandes_mut = [g for g in gm if (g.ticker, g.data_ex) in certos]
    passam = sum(1 for g in grandes_mut if abs(g.retorno_ajustado) < 0.15)
    assert passam < len(grandes_mut) / 2, "%d de %d passam lidos ao contrario" % (
        passam, len(grandes_mut))


@acervo
@pytest.mark.slow
def test_REAL_MUTACAO_fator_invertido_nos_PROVENTOS_piora(jan):
    """A mutacao do C-02, restrita a provento em dinheiro: com evento de quantidade a
    media ficaria dominada pelos grupamentos invertidos, que explodem para cima."""
    inv = {k: (Decimal(1) / f, t) for k, (f, t) in jan.fat.items()}
    gi = [g for g in A.degraus(jan.acervo, A.ajustar_tudo(jan.acervo, inv), inv)
          if not A.e_de_quantidade(g.tipos)]
    _n, m, t = A.resumo([g.retorno_ajustado for g in gi])
    assert m < -0.020 and t < -8, (m, t)


@acervo
@pytest.mark.slow
def test_REAL_o_preco_de_vespera_da_B3_bate_com_o_COTAHIST_na_janela(jan):
    """Em 2023, 352 de 352. Pre-registrado para a janela: nenhum diferente."""
    bate = difere = 0
    exemplos = []
    for r in jan.casados:
        if r["fator_status"] != "CALCULADO" or r["data_ex_status"] != "DERIVADA":
            continue
        if not r["preco_vespera"]:
            continue
        tk, dex = r["_ticker"], dt.date.fromisoformat(r["data_ex"])
        antes = [d for d in jan.acervo.precos[tk] if d < dex]
        if not antes:
            continue
        cot = jan.acervo.precos[tk][max(antes)]
        if cot == Decimal(r["preco_vespera"]):
            bate += 1
        else:
            difere += 1
            exemplos.append((tk, r["data_ex"], r["preco_vespera"], str(cot)))
    assert bate >= 1000 and difere == 0, (bate, difere, exemplos[:10])


# ── POS-HOC: escritos DEPOIS de ver a janela. Sao guarda de numero publicado, nao prova.

@pytest.fixture(scope="module")
def res(jan):
    return A.residuo_de_mercado(jan)


@acervo
def test_POSHOC_o_JCP_fecha_descontado_o_mercado(res):
    """Medido: +0,07%, t +1,29, n=819. O JCP e o provento em que o ajuste acerta."""
    ex = [e for g, c, e, _y in res if c == "LIMPO" and A._so(g.tipos, "JRS CAP PROPRIO")]
    n, m, t = A.resumo(ex)
    assert n > 700 and abs(t) < 2, (n, m, t)


@acervo
def test_POSHOC_o_DIVIDENDO_tira_do_preco_mais_do_que_paga(res):
    """Medido: queda/provento = 1,164 (IC 95% por bootstrap [1,09; 1,24], n=400); no JCP,
    0,951 ([0,86; 1,04]). O NUMERO e medido; o MECANISMO -- dividendo isento contra ganho
    de capital tributado, que preveria 1/0,85 = 1,18 -- e hipotese, NAO_CONFIRMADO."""
    n, q = A.queda_por_provento([(e, y) for g, c, e, y in res
                                 if c == "LIMPO" and A._so(g.tipos, "DIVIDENDO")])
    assert n > 350 and 1.09 < q < 1.24, (n, q)
    n, q = A.queda_por_provento([(e, y) for g, c, e, y in res
                                 if c == "LIMPO" and A._so(g.tipos, "JRS CAP PROPRIO")])
    assert 0.86 < q < 1.04, (n, q)


@acervo
def test_POSHOC_o_COTAHIST_declara_bonificacao_que_o_silver_nao_tem(res):
    """A lacuna de eventos de quantidade antigos, vista de dentro do arquivo de preco: o
    ESPECI marca `EDB`/`EJB` e o silver so traz o provento. Medido: 11 dias na janela,
    concentrados em 2021-2022, e nenhum em 2025 -- o suplemento devolve janela RECENTE."""
    marc = [g for g, c, _e, _y in res if c == "MARCA_SEM_EVENTO"]
    assert len(marc) >= 10
    assert not [g for g in marc if g.data_ex.year == 2025]


@acervo
@pytest.mark.slow
def test_REAL_o_ESPECI_e_testemunha_da_data_ex_em_cada_ano(jan):
    for ano in JANELA:
        gs = [g for g in jan.degraus if g.data_ex.year == ano]
        mudou = sum(1 for g in gs if g.especi_vespera != g.especi_ex)
        assert mudou / len(gs) > 0.9, "%d: %d de %d" % (ano, mudou, len(gs))


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

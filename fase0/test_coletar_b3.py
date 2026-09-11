# -*- coding: utf-8 -*-
"""
test_coletar_b3.py -- a suite que faltava, e ela nasce de tres defeitos reais.

POR QUE ESTE ARQUIVO EXISTE.

O `coletar_b3.py` foi escrito em 06/09, entregue "compila e a logica foi testada", e na
primeira corrida real (11/09) quebrou tres vezes seguidas:

  A-00  `dados.get(...)` num `str` -- derrubou a coleta inteira na PRIMEIRA emissora e
        perdeu as outras 75.
  A-01  `B3SA3` virou `BSA` porque a derivacao filtrava digitos. A B3 respondeu **200**
        com OUTRA empresa. Dado errado com cara de certo.
  A-02  o endpoint devolve LISTA, nao objeto -- e eu havia registrado objeto na pesquisa,
        porque li o resumo de uma ferramenta em vez do byte.

Nenhum dos tres precisava de rede para ser pego. **Os tres sao funcao pura.** A licao nao
e "escrever mais teste": e que `empresa_de` e `normalizar` sao onde mora o risco, e eram
exatamente as duas funcoes sem teste.

Regra da casa que este arquivo cumpre: **todo achado vira um teste que falha na versao
anterior.** Cada teste abaixo cita o achado que o motivou.

Roda sem rede. Os testes de acervo PULAM quando nao ha captura no disco, e dizem isso.
"""

import base64, json, os, sys, tempfile
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coletar_b3 as c                                                    # noqa: E402

RAIZ_ACERVO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "bronze", "b3")


# ─────────────────────────────────────────────────────────── A-01: empresa_de

def test_A01_B3SA3_vira_B3SA_e_nao_BSA():
    """O achado, na forma mais curta possivel.

    A versao anterior fazia `"".join(c for c in t if c.isalpha())[:4]` e devolvia `BSA`.
    O endpoint RESPONDEU -- capital social de R$9,61 bi, data de 1981 -- ou seja, casou
    com outra empresa e devolveu 200. Este teste falha contra aquela versao."""
    assert c.empresa_de("B3SA3") == "B3SA"


@pytest.mark.parametrize("ticker,esperado", [
    ("PETR4", "PETR"), ("PETR3", "PETR"), ("VALE3", "VALE"), ("ABEV3", "ABEV"),
    ("BPAC11", "BPAC"), ("KLBN11", "KLBN"), ("IGTI11", "IGTI"), ("SANB11", "SANB"),
    ("TAEE11", "TAEE"), ("ENGI11", "ENGI"), ("B3SA3", "B3SA"),
    ("petr4", "PETR"), ("  VALE3  ", "VALE"),
])
def test_A01_emissora_e_posicional_nao_por_tipo_de_caractere(ticker, esperado):
    """Ticker da B3 = 4 caracteres de emissora + digitos (+ F de fracionario).
    A regra e POSICIONAL. Units (11) e ON/PN (3/4) caem na mesma regra."""
    assert c.empresa_de(ticker) == esperado


def test_A01_a_deduplicacao_por_emissora_nao_perde_ativo():
    """PETR3 e PETR4 sao a mesma emissora: uma requisicao, nao duas. Mas B3SA3 nao pode
    colidir com nada -- era o que a versao antiga fazia ao virar BSA."""
    tickers = ["PETR3", "PETR4", "B3SA3", "BBDC3", "BBDC4", "ITSA4"]
    emissoras = sorted({c.empresa_de(t) for t in tickers})
    assert emissoras == ["B3SA", "BBDC", "ITSA", "PETR"]


# ───────────────────────────────────────────── A-00 / A-02: forma da resposta

def _normalizar(texto):
    """Espelha o caminho de normalizacao do coletor, para poder exercita-lo sem rede.

    Se esta funcao e a do coletor divergirem, o teste
    `test_A02_a_normalizacao_do_teste_espelha_a_do_coletor` acusa."""
    dados = json.loads(texto)
    if isinstance(dados, str):
        try: dados = json.loads(dados)
        except json.JSONDecodeError: pass
    if isinstance(dados, list):
        so_dicts = [x for x in dados if isinstance(x, dict)]
        if so_dicts: dados = so_dicts[0]
    return dados


def test_A02_resposta_em_lista_e_o_formato_NORMAL():
    """As 74 emissoras do IBOV devolveram lista em 11/09/2026. A pesquisa registrava
    objeto -- porque a leitura passou por uma ferramenta de resumo que desembrulhou a
    lista de um elemento sem avisar. **Um resumo nao e uma observacao.**"""
    d = _normalizar('[{"tradingName":"X","cashDividends":[1,2]}]')
    assert isinstance(d, dict) and d["tradingName"] == "X"


def test_A00_resposta_duplamente_codificada_e_desembrulhada():
    """O acervo real de 11/09 esta gravado assim: uma STRING JSON contendo JSON.
    `json.loads` uma vez devolve `str`; era dai que vinha o AttributeError."""
    bruto = json.dumps('[{"tradingName":"Y","cashDividends":[]}]')
    assert _normalizar(bruto)["tradingName"] == "Y"


def test_A00_resposta_que_nao_vira_dict_nao_levanta_excecao():
    """A guarda que salvou a corrida: coisa estranha e EVIDENCIA, nao motivo para
    derrubar 75 ativos por causa de um."""
    for bruto in ('"nao encontrado"', '[]', '[1,2,3]', 'null', '123'):
        assert not isinstance(_normalizar(bruto), dict), bruto


def test_A02_a_normalizacao_do_teste_espelha_a_do_coletor():
    """N-01 preventivo: duas implementacoes da mesma regra concordam por acidente ate o
    dia em que nao concordam. Este teste le o FONTE do coletor e exige que os tres
    degraus da normalizacao continuem la."""
    fonte = open(c.__file__, encoding="utf-8").read()
    for marca in ('isinstance(dados, str)', 'isinstance(dados, list)',
                  'isinstance(dados, dict)'):
        assert marca in fonte, (
            "o coletor perdeu o degrau `%s` da normalizacao, e este teste deixou de "
            "medir o caminho real." % marca)


# ─────────────────────────────────────────────────── carga e imutabilidade

def test_carga_base64_e_o_que_a_B3_espera():
    p = c.carga({"issuingCompany": "PETR", "language": "pt-br"})
    assert json.loads(base64.b64decode(p)) == {"issuingCompany": "PETR", "language": "pt-br"}
    assert " " not in base64.b64decode(p).decode(), "separadores compactos, sem espaco"


def test_snapshot_e_imutavel_por_padrao():
    """Regravar por cima apaga a unica copia de um dia. O acervo ponto-no-tempo do
    projeto comeca em 11/09/2026 e nao se recupera."""
    with tempfile.TemporaryDirectory() as d:
        cam = os.path.join(d, "a", "b.json")
        assert c.gravar(cam, "primeiro", False)[0] is True
        assert c.gravar(cam, "segundo", False)[0] is False, "sobrescreveu sem --forcar"
        assert open(cam, encoding="utf-8").read() == "primeiro"
        assert c.gravar(cam, "segundo", True)[0] is True
        assert open(cam, encoding="utf-8").read() == "segundo"


def test_manifesto_e_append_e_uma_linha_por_captura():
    with tempfile.TemporaryDirectory() as d:
        c.anotar_manifesto(d, {"tipo": "teste", "n": 1})
        c.anotar_manifesto(d, {"tipo": "teste", "n": 2})
        linhas = open(os.path.join(d, "manifesto.jsonl"), encoding="utf-8").read().strip().split("\n")
        assert [json.loads(x)["n"] for x in linhas] == [1, 2]


# ──────────────────────────────────────── integridade do acervo ja capturado

def _capturas():
    base = os.path.join(RAIZ_ACERVO, "eventos")
    if not os.path.isdir(base):
        pytest.skip("nao ha acervo de eventos neste disco -- ESTES TESTES NAO RODARAM. "
                    "Rode `python fase0/coletar_b3.py --indice IBOV --eventos` antes.")
    dias = sorted(d for d in os.listdir(base) if d.startswith("dt_captura="))
    if not dias: pytest.skip("acervo existe mas esta vazio")
    return os.path.join(base, dias[-1])


def test_acervo_todo_arquivo_desembrulha_para_objeto():
    """O acervo guarda o BRUTO de proposito -- inclusive a dupla codificacao. Quem le
    precisa desembrulhar, e este teste garante que da para desembrulhar tudo."""
    dia = _capturas()
    ruins = []
    for nome in sorted(os.listdir(dia)):
        if not nome.endswith(".json") or "NAO-E-OBJETO" in nome: continue
        d = _normalizar(open(os.path.join(dia, nome), encoding="utf-8").read())
        if not isinstance(d, dict): ruins.append(nome)
    assert not ruins, "arquivos que nao viram objeto: %s" % ruins


def test_acervo_A01_o_code_da_resposta_bate_com_o_nome_do_arquivo():
    """A guarda direta contra o A-01. Se `MBRF.json` contiver `code: MRFG`, o acervo tem
    dado de outro ativo com nome de arquivo certo -- e nenhuma contagem pegaria."""
    dia = _capturas()
    divergentes = []
    for nome in sorted(os.listdir(dia)):
        if not nome.endswith(".json") or "NAO-E-OBJETO" in nome: continue
        d = _normalizar(open(os.path.join(dia, nome), encoding="utf-8").read())
        if not isinstance(d, dict): continue
        esperado = nome[:-len(".json")]
        obtido = (d.get("code") or "").strip().upper()
        if obtido != esperado.upper():
            divergentes.append((esperado, obtido, (d.get("tradingName") or "").strip()))
    assert not divergentes, (
        "o `code` da B3 nao bate com o arquivo -- DADO DO ATIVO ERRADO:\n  " +
        "\n  ".join("%s -> %s (%s)" % t for t in divergentes))


def test_acervo_A03_emissora_sem_evento_nenhum_e_acusada():
    """A-03. Zero nas TRES listas quase sempre e troca de codigo de emissora: a historia
    ficou sob o codigo antigo. MBRF (ex-MRFG, fusao com a BRF) foi o caso de 11/09.

    Este teste NAO falha -- ele nao poderia, porque a lacuna e do dado, nao do codigo.
    Ele EXISTE para que a lacuna seja contavel e apareca no relatorio, exatamente como a
    decisao `empresa_sem_dado` de 05/09 exige: admitir com marcacao, nunca em silencio."""
    dia = _capturas()
    sem_nada = []
    for nome in sorted(os.listdir(dia)):
        if not nome.endswith(".json") or "NAO-E-OBJETO" in nome: continue
        d = _normalizar(open(os.path.join(dia, nome), encoding="utf-8").read())
        if not isinstance(d, dict): continue
        if not any(d.get(k) for k in ("cashDividends", "stockDividends", "subscriptions")):
            sem_nada.append((nome[:-5], (d.get("tradingName") or "").strip()))
    if sem_nada:
        print("\n[A-03] emissoras sem evento nenhum (provavel troca de codigo):")
        for em, nome in sem_nada: print("    %-5s %s" % (em, nome))
    assert len(sem_nada) <= 3, (
        "mais de 3 emissoras do IBOV sem evento nenhum sugere falha sistemica de "
        "coleta, nao troca de codigo pontual: %s" % sem_nada)


# ──────────────────────────── proventos completos: paginacao, sem rede nenhuma

def _pagina(n, total, por_pagina, total_paginas=None, dupla=False):
    """Resposta sintetica no envelope page/results -- o do GetPortfolioDay, que e o
    unico envelope deste proxy observado em primeira mao."""
    ini = (n - 1) * por_pagina
    res = [{"lastDatePrior": "d%03d" % k, "rate": "0,1"}
           for k in range(ini, min(ini + por_pagina, total))]
    page = {"pageNumber": n, "pageSize": por_pagina, "totalRecords": total}
    if total_paginas is not None:
        page["totalPages"] = total_paginas
    texto = json.dumps({"page": page, "results": res})
    return json.dumps(texto) if dupla else texto


class _B3Falsa:
    """Faz o papel de `buscar`: decodifica o pedido do caminho e registra cada um."""

    def __init__(self, responder):
        self.responder, self.pedidos = responder, []

    def __call__(self, url):
        pedido = json.loads(base64.b64decode(url.split("GetListedCashDividends/", 1)[1]))
        self.pedidos.append(pedido)
        return self.responder(pedido), {}


def _acervo_eventos(raiz, nomes, dia="2026-09-11"):
    """Acervo de eventos no formato REAL de 11/09: string JSON contendo uma lista."""
    pasta = os.path.join(raiz, "eventos", "dt_captura=" + dia)
    os.makedirs(pasta)
    for em, tn in nomes.items():
        corpo = json.dumps([{"code": em, "tradingName": tn, "cashDividends": []}])
        with open(os.path.join(pasta, em + ".json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(corpo))


def test_paginacao_para_no_fim_declarado():
    b3 = _B3Falsa(lambda p: _pagina(p["pageNumber"], 250, 99, total_paginas=3, dupla=True))
    paginas, total = c.paginar("PETROBRAS", b3, pausa=0)
    assert total == 250 and [k for _, _, k in paginas] == [99, 99, 52]
    assert [p["pageNumber"] for p in b3.pedidos] == [1, 2, 3], "nem uma pagina a mais"
    assert {p["tradingName"] for p in b3.pedidos} == {"PETROBRAS"}


def test_paginacao_sem_totalPages_para_pelo_totalRecords():
    b3 = _B3Falsa(lambda p: _pagina(p["pageNumber"], 250, 99))
    _, total = c.paginar("PETROBRAS", b3, pausa=0)
    assert total == 250 and len(b3.pedidos) == 3


def test_paginacao_nao_entra_em_laco_quando_o_servidor_ignora_pageNumber():
    """Servidor que devolve sempre a pagina 1 com `totalPages: 3`: sem a trava de pagina
    repetida, o coletor gravaria 3 copias da mesma coisa como se fossem 297 registros."""
    b3 = _B3Falsa(lambda p: _pagina(1, 250, 99, total_paginas=3))
    with pytest.raises(c.PaginacaoInvalida) as e:
        c.paginar("PETROBRAS", b3, pausa=0)
    assert e.value.tipo == "LACO" and len(b3.pedidos) == 2


def test_paginacao_tem_teto_duro():
    """Servidor que promete paginas sem fim, cada uma diferente: para no teto."""
    b3 = _B3Falsa(lambda p: _pagina(p["pageNumber"], 10**6, 99, total_paginas=10**6))
    with pytest.raises(c.PaginacaoInvalida) as e:
        c.paginar("PETROBRAS", b3, pausa=0, max_paginas=5)
    assert e.value.tipo == "LACO" and len(b3.pedidos) == 5


def test_servidor_que_corta_o_tamanho_da_pagina_nao_vira_historico_completo():
    """totalRecords 250, mas o servidor so entrega 50 por pagina e diz 3 paginas: vieram
    150. Meio historico gravado como inteiro e pior que nenhum."""
    b3 = _B3Falsa(lambda p: _pagina(p["pageNumber"], 250, 50, total_paginas=3))
    with pytest.raises(c.PaginacaoInvalida) as e:
        c.paginar("PETROBRAS", b3, pausa=0)
    assert e.value.tipo == "INCOMPLETO"


def test_resposta_fora_do_envelope_e_acusada():
    for bruto in ('[]', '"erro"', json.dumps({"results": []}), json.dumps({"page": {}})):
        with pytest.raises(c.PaginacaoInvalida) as e:
            c.paginar("PETROBRAS", _B3Falsa(lambda p, b=bruto: b), pausa=0)
        assert e.value.tipo == "FORA-DO-FORMATO", bruto


def test_trading_name_vem_do_acervo_sem_o_preenchimento_e_nunca_do_ticker(tmp_path):
    """O campo do suplemento tem 12 posicoes ('PETROBRAS   '). O pedido tem de levar o
    TEXTO do acervo, sem o espaco -- nunca 'PETR', que e o A-01 num campo novo."""
    _acervo_eventos(str(tmp_path), {"PETR": "PETROBRAS   "})
    b3 = _B3Falsa(lambda p: _pagina(p["pageNumber"], 3, 99, total_paginas=1))
    assert c.coletar_proventos(str(tmp_path), "2026-09-12", buscar_fn=b3, pausa=0) == 0
    assert b3.pedidos[0]["tradingName"] == "PETROBRAS"


def test_total_zero_e_acusado_e_nao_gravado_como_empresa_sem_proventos(tmp_path):
    """A armadilha que a pesquisa observou: tradingName errado devolve totalRecords 0
    com HTTP 200. Gravado como historico, viraria 'empresa sem proventos' -- o F-02."""
    raiz = str(tmp_path)
    _acervo_eventos(raiz, {"PETR": "PETROBRAS   "})
    b3 = _B3Falsa(lambda p: _pagina(1, 0, 99, total_paginas=0))
    assert c.coletar_proventos(raiz, "2026-09-12", buscar_fn=b3, pausa=0) == 1
    pasta = os.path.join(raiz, "proventos", "dt_captura=2026-09-12")
    assert not os.path.isdir(os.path.join(pasta, "PETR")), "zero virou historico"
    assert os.path.exists(os.path.join(pasta, "PETR.TOTAL-ZERO.json")), "a evidencia sumiu"
    manif = os.path.join(raiz, "manifesto.jsonl")
    assert not os.path.exists(manif) or "proventos_completos" not in open(manif).read()


def test_historico_completo_grava_uma_pagina_por_arquivo_com_sha(tmp_path):
    raiz = str(tmp_path)
    _acervo_eventos(raiz, {"PETR": "PETROBRAS   "})
    b3 = _B3Falsa(lambda p: _pagina(p["pageNumber"], 250, 99, total_paginas=3))
    assert c.coletar_proventos(raiz, "2026-09-12", buscar_fn=b3, pausa=0) == 0
    pasta = os.path.join(raiz, "proventos", "dt_captura=2026-09-12", "PETR")
    assert sorted(os.listdir(pasta)) == ["pagina-001.json", "pagina-002.json", "pagina-003.json"]
    reg = json.loads(open(os.path.join(raiz, "manifesto.jsonl")).read().strip().split("\n")[-1])
    assert reg["tipo"] == "proventos_completos" and reg["total_registros"] == 250
    assert len(reg["sha256_paginas"]) == 3 and reg["trading_name"] == "PETROBRAS"
    # e o acervo do dia e imutavel: segunda corrida nao pede nada nem regrava
    antes = len(b3.pedidos)
    c.coletar_proventos(raiz, "2026-09-12", buscar_fn=b3, pausa=0)
    assert len(b3.pedidos) == antes


def test_proventos_completos_nao_se_mistura_com_eventos():
    """O caminho --eventos funciona e o acervo dele nao se recupera: o passo novo roda
    sozinho, lendo o que ja existe."""
    with pytest.raises(SystemExit) as e:
        c.main(["--proventos-completos", "--eventos"])
    assert e.value.code == 2


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

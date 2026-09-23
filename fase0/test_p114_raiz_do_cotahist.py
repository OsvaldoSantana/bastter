# -*- coding: utf-8 -*-
"""P-114 -- a raiz padrao apontava para uma pasta que NAO tem o acervo.

O DEFEITO, e ele era mudo no pior sentido: produzia numero.

`RAIZ_PADRAO` do `refinar.py` e do `ajustar.py` era `data/bronze/b3`, e
`calendario.arquivos()` nao e recursivo. Os 41 anos de COTAHIST moram em
`data/bronze/b3/cotahist/`. A unica coisa com cara de COTAHIST na raiz antiga era o
`COTAHIST_A2023.ZIP` avulso de 04/09 -- uma DUPLICATA byte a byte do que ja estava em
`cotahist/`, e sem origem declarada (P-97).

Entao rodar sem `--raiz` media **um ano** e imprimia "acervo COTAHIST_A2023" como se
fosse o acervo. Nao e o F-02 na forma classica (insumo ausente virando zero): e um
RECORTE com cara de todo, que e a forma que passa em qualquer teste de "veio numero?".

E o `refinar.py` imprimia, no proprio relatorio, a frase que fechava a armadilha:
*"cada ano de COTAHIST que entrar em `data/bronze/b3/` amplia a cobertura sozinho"*.
Falsa para o disco como ele estava. Quem copiasse um ano para ali seguindo a instrucao
nao veria diferenca nenhuma -- e a instrucao vinha da ferramenta.

AS DUAS METADES SE ESCONDIAM UMA A OUTRA. Um arquivo no lugar errado (P-97) e um padrao
apontando para o lugar errado (P-114): enquanto o avulso estava la, o padrao devolvia
248 pregoes e ninguem o questionava. Tirar so o avulso deixaria a raiz antiga com ZERO
COTAHIST; mudar so o padrao deixaria a duplicata sem procedencia no acervo. As duas
decisoes sao de 23/09/2026 e sao dele.

E AS DUAS RAIZES DO `refinar.py` NAO SAO A MESMA COISA -- e esse e o achado de desenho.
Ele le eventos/proventos de um lugar e o CALENDARIO de outro. Havia UM parametro
servindo aos dois, e por isso a correcao nao e "trocar a constante": e separar os
parametros. Um parametro que serve a dois acervos garante que mover um quebra o outro
em silencio.
"""
from __future__ import annotations
import os
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ajustar as A       # noqa: E402
import calendario as C    # noqa: E402
import refinar as R       # noqa: E402

RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACERVO_REAL = os.path.join(RAIZ_REPO, "data", "bronze", "b3", "cotahist")
BRONZE_B3 = os.path.join(RAIZ_REPO, "data", "bronze", "b3")


# ── o padrao aponta para a pasta que TEM o dado ───────────────────────────────

def test_P114_os_dois_modulos_tem_a_MESMA_raiz_de_cotahist():
    """Duas leituras da mesma regra concordam por acidente ate o dia em que nao
    concordam (N-01). Se um dia elas precisarem divergir, que seja com um teste
    falhando, nao com um ano a menos num relatorio."""
    assert A.RAIZ_PADRAO == R.COTAHIST_PADRAO


def test_P114_a_raiz_padrao_termina_em_cotahist():
    """O portao. Falha contra a versao anterior, em que as duas terminavam em `b3`."""
    assert os.path.basename(A.RAIZ_PADRAO) == "cotahist"
    assert os.path.basename(R.COTAHIST_PADRAO) == "cotahist"
    assert A.RAIZ_PADRAO == os.path.join("data", "bronze", "b3", "cotahist")


def test_P114_o_refinar_NAO_juntou_as_duas_raizes():
    """A raiz de eventos continua sendo `data/bronze/b3` -- e ali que moram `eventos/`
    e `proventos/`. Apontar as duas para `cotahist/` "consertaria" o calendario e
    apagaria o acervo de eventos, que e trocar um defeito por outro maior."""
    assert R.RAIZ_PADRAO == os.path.join("data", "bronze", "b3")
    assert R.RAIZ_PADRAO != R.COTAHIST_PADRAO


# ── a separacao e de COMPORTAMENTO, nao de nome de variavel ───────────────────

def _linha(data, codneg="PETR4       "):
    ln = ("01" + data + "02" + codneg + "010" + "PETROBRAS   "
          + "PN        " + "   " + "R$  ")
    return ln.ljust(245) + "\r\n"


def _cotahist(caminho, ano, dias):
    cab = ("00COTAHIST." + ano + "BOVESPA " + "19991210").ljust(245) + "\r\n"
    corpo = cab + "".join(_linha(d) for d in dias) + ("99COTAHIST." + ano).ljust(245) + "\r\n"
    with zipfile.ZipFile(caminho, "w") as z:
        z.writestr("COTAHIST_A%s.TXT" % ano, corpo.encode("latin-1"))


def _acervo_de_eventos(base, dia="2026-09-11"):
    """O minimo que o `refinar.py` precisa: uma captura com uma emissora."""
    pasta = os.path.join(base, "eventos", "dt_captura=" + dia)
    os.makedirs(pasta)
    with open(os.path.join(pasta, "PETR.json"), "w", encoding="utf-8") as f:
        f.write('[{"code":"PETR","codeCVM":"9512","tradingName":"PETROBRAS",'
                '"cashDividends":[{"assetIssued":"BRPETRACNPR6","paymentDate":'
                '"15/12/2023","rate":"1,00","relatedTo":"2023","approvedOn":'
                '"01/12/2023","isinCode":"BRPETRACNPR6","label":"DIVIDENDO",'
                '"lastDatePrior":"04/12/2023","remarks":"","typeStock":"PN"}],'
                '"stockDividends":[],"subscriptions":[]}]')
    return pasta


def test_P114_o_calendario_vem_da_raiz_de_COTAHIST_e_nao_da_de_eventos(tmp_path):
    """A prova de comportamento: o COTAHIST mora numa pasta em que NAO ha evento
    nenhum, e o evento mora numa pasta em que nao ha COTAHIST nenhum. Se o modulo
    lesse o calendario da raiz de eventos -- como ate 21/09 --, a `data_ex` sairia
    vazia e o teste reprovaria."""
    b3 = tmp_path / "b3"
    cot = tmp_path / "outro_lugar" / "cotahist"
    cot.mkdir(parents=True)
    _acervo_de_eventos(str(b3))
    _cotahist(str(cot / "COTAHIST_A2023.ZIP"), "2023",
              ["20231204", "20231205", "20231206"])

    saida = tmp_path / "silver"
    assert R.refinar(str(b3), "2026-09-11", str(saida), str(cot)) == 0

    import csv
    with open(saida / "eventos_silver_2026-09-11.csv", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 1
    # ultimo dia COM direito 04/12; a data ex e o pregao SEGUINTE observado.
    assert linhas[0]["ultimo_dia_com_direito"] == "2023-12-04"
    assert linhas[0]["data_ex"] == "2023-12-05"
    assert linhas[0]["data_ex_status"] == R.DERIVADA


def test_P114_sem_COTAHIST_na_raiz_dele_a_linha_diz_que_NAO_SABE(tmp_path):
    """O outro lado, e ele importa tanto quanto: apontar `--cotahist` para uma pasta
    vazia NAO produz data ex chutada. `SEM_CALENDARIO` e uma resposta; o proximo dia
    util seria o erro que o `calendario.py` existe para nao cometer."""
    b3 = tmp_path / "b3"
    vazia = tmp_path / "vazia"
    vazia.mkdir()
    _acervo_de_eventos(str(b3))
    saida = tmp_path / "silver"
    assert R.refinar(str(b3), "2026-09-11", str(saida), str(vazia)) == 0

    import csv
    with open(saida / "eventos_silver_2026-09-11.csv", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert linhas[0]["data_ex"] == ""
    assert linhas[0]["data_ex_status"] == R.SEM_CALENDARIO


def test_P114_a_raiz_de_eventos_nao_e_usada_como_calendario(tmp_path):
    """Mutacao ao contrario: um COTAHIST na raiz de EVENTOS nao pode virar calendario.
    Se alguem religar as duas raizes, este teste reprova -- e e o unico que reprova,
    porque o resultado do defeito antigo era um numero plausivel."""
    b3 = tmp_path / "b3"
    _acervo_de_eventos(str(b3))
    _cotahist(str(b3 / "COTAHIST_A2023.ZIP"), "2023",
              ["20231204", "20231205", "20231206"])
    vazia = tmp_path / "vazia"
    vazia.mkdir()

    saida = tmp_path / "silver"
    R.refinar(str(b3), "2026-09-11", str(saida), str(vazia))

    import csv
    with open(saida / "eventos_silver_2026-09-11.csv", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert linhas[0]["data_ex_status"] == R.SEM_CALENDARIO, (
        "o COTAHIST que esta na raiz de EVENTOS foi lido como calendario -- as duas "
        "raizes voltaram a ser uma so")


# ── o acervo real ─────────────────────────────────────────────────────────────

@pytest.mark.skipif(not os.path.isdir(ACERVO_REAL),
                    reason="acervo de COTAHIST ausente -- ESTE TESTE NAO RODOU")
def test_P114_a_raiz_padrao_enxerga_os_41_anos_e_a_antiga_enxergava_um():
    """A medicao que nomeia o achado, contra o disco. A raiz ANTIGA hoje enxerga ZERO
    (o avulso saiu pela P-97); antes de 23/09 ela enxergava UM. Os dois numeros estao
    igualmente errados sobre um acervo de 41 anos, e o primeiro e o unico que aparece
    sozinho -- e por isso que a P-97 e a P-114 fecham juntas."""
    nova = C.arquivos(ACERVO_REAL)
    antiga = C.arquivos(BRONZE_B3)
    assert len(nova) >= 41, "a raiz nova tem de ver o acervo inteiro"
    assert len(antiga) == 0, (
        "sobrou COTAHIST solto em data/bronze/b3 -- a P-97 tirou a duplicata de la, e "
        "arquivo novo nessa pasta volta a ser um acervo de um ano com cara de acervo: "
        "%s" % sorted(antiga))


@pytest.mark.skipif(not os.path.isdir(ACERVO_REAL),
                    reason="acervo de COTAHIST ausente -- ESTE TESTE NAO RODOU")
def test_P97_nao_sobrou_ZIP_sem_origem_no_acervo():
    """P-97 fechada: todo `.zip` do acervo da B3 tem origem declarada. O manifesto diz
    a mesma coisa em uma linha (`P-06: 0 de 41`); este teste a prende na suite, porque
    o manifesto e um comando que alguem roda e a P7 e explicita sobre isso."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from manifesto_cvm import origem_declarada, zips

    todos = zips(BRONZE_B3)
    origens = origem_declarada(os.path.join(RAIZ_REPO, "docs", "acervo", "b3"))
    sem = []
    for c in todos:
        rel = os.path.relpath(c, BRONZE_B3).replace(os.sep, "/")
        if rel not in origens:
            sem.append(rel)
    assert not sem, "zip(s) sem origem declarada no acervo da B3: %s" % sem
    assert len(todos) == 41, "esperava 41 zips no acervo, achei %d" % len(todos)

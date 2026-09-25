# -*- coding: utf-8 -*-
"""
test_calendario_p99.py -- ACHADO P-99, 19/09/2026.

O DEFEITO, e ele era MUDO. `registros()` achava o membro do ZIP filtrando
`n.upper().endswith(".TXT")`. O COTAHIST muda de convencao dentro da propria serie:

    1986-2000   COTAHIST.A1986     PONTO, sem extensao
    2001        COTAHIST_A2001     SUBLINHADO, sem extensao
    2002-2025   COTAHIST_A2023.TXT

Para os 16 primeiros anos o laco nao produzia linha nenhuma. Sem erro, sem aviso.
Medido em 19/09 sobre os arquivos reais: **7 de 9 devolviam ZERO**. O ano nao quebrava
-- ele simplesmente NAO EXISTIA, e a serie passaria a comecar em 2002 sem ninguem ter
decidido isso. Nenhum teste de "veio numero?" pega isso.

E `arquivos()` tinha o irmao do mesmo defeito: `os.path.splitext("COTAHIST.A1986")`
devolve `('COTAHIST', '.A1986')`, entao o TXT extraido nem era reconhecido -- e se
fosse, **quinze anos disputariam a chave 'COTAHIST'** no mesmo dict.

A CORRECAO NAO E UMA LISTA DE NOMES. Seria a P-82/P-98 pela terceira vez em tres dias:
*regra escrita numa lista de nomes nao e regra, e lembrete*. A regra e **um membro so,
e ele tem de comecar com um header de COTAHIST**. Nome e a propriedade que varia;
leiaute e a que identifica.

E O TERCEIRO DEFEITO EU NAO TINHA PREVISTO: `pregoes()` morria inteiro num
`BadZipFile`. O `COTAHIST_A2026.ZIP` chegou truncado, e **um arquivo ruim apagava o
calendario do acervo todo**. O desenho certo ja estava escrito no `coletar_b3.py` desde
10/09 -- *"resposta estranha e evidencia, nao lixo: grave o bruto e acuse no fim"* --, e
foi ele que salvou as 74 emissoras. A licao nao tinha atravessado de modulo para
modulo: A-07/P-85 outra vez.

INSTANTANEO DOURADO (passo 3 do protocolo §9). `pregoes()` sobre 2023, antes e depois:
**248 pregoes**, `sha256 e4a9d81d3d6d4cb8810b86322de3d08415f7a3fed23b32d923b4291c13bd551c`
-- identico ao registrado no CLAUDE.md em 18/09. Os 17 anos novos entraram sem mover
um bit do que ja funcionava.
"""
from __future__ import annotations
import hashlib
import io
import os
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendario as C  # noqa: E402

ACERVO_REAL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "bronze", "b3", "cotahist")

# 248 pregoes de 2023, e o hash do conjunto ordenado. O numero vem do refactor de
# 18/09 e esta no CLAUDE.md -- este teste existe para que a P-99 NAO o tenha movido.
SHA_2023 = "e4a9d81d3d6d4cb8810b86322de3d08415f7a3fed23b32d923b4291c13bd551c"
PREGOES_2023 = 248


def _linha(data, codneg="PETR4       ", modref="R$  "):
    """Um registro de cotacao de 245 posicoes. So os campos que este arquivo le."""
    ln = ("01" + data + "02" + codneg + "010" + "PETROBRAS   "
          + "PN        " + "   " + modref)
    return ln.ljust(245) + "\r\n"


def _cotahist(caminho, nome_membro, ano, linhas, gerado="19991210"):
    cab = ("00COTAHIST." + ano + "BOVESPA " + gerado).ljust(245) + "\r\n"
    corpo = cab + "".join(linhas) + ("99COTAHIST." + ano).ljust(245) + "\r\n"
    with zipfile.ZipFile(caminho, "w") as z:
        z.writestr(nome_membro, corpo.encode("latin-1"))


# ── ano_de: os tres formatos que o acervo tem de fato ─────────────────────────

@pytest.mark.parametrize("nome, ano", [
    ("COTAHIST.A1986", "1986"),          # 1986-2000, dentro do ZIP
    ("COTAHIST.A2000", "2000"),
    ("COTAHIST_A2001", "2001"),          # 2001, sublinhado e sem extensao
    ("COTAHIST_A2023.TXT", "2023"),      # 2002-2025
    ("COTAHIST_A2023.ZIP", "2023"),      # o proprio ZIP
    ("cotahist_a2023.zip", "2023"),      # a B3 nao promete caixa
    ("LEIA.md", None),
    ("COTAHIST_LAYOUT.pdf", None),
    ("origem.csv", None),
])
def test_P99_ano_de_reconhece_as_tres_convencoes(nome, ano):
    assert C.ano_de(nome) == ano


def test_P99_splitext_NAO_resolveria_e_e_por_isso_que_o_defeito_existia():
    """A prova de que a implementacao anterior nao tinha conserto trivial: o
    `splitext` faz QUINZE anos colidirem na mesma chave."""
    chaves = {os.path.splitext(f"COTAHIST.A{a}")[0] for a in range(1986, 2001)}
    assert chaves == {"COTAHIST"}, "quinze anos, uma chave -- era esse o buraco"
    assert len({C.ano_de(f"COTAHIST.A{a}") for a in range(1986, 2001)}) == 15


# ── membro_do_zip: acha pelo CONTEUDO ─────────────────────────────────────────

@pytest.mark.parametrize("membro", ["COTAHIST.A1986", "COTAHIST_A2001",
                                    "COTAHIST_A2023.TXT"])
def test_P99_o_membro_e_achado_em_QUALQUER_das_convencoes(tmp_path, membro):
    """O portao. Falha contra a versao anterior para os dois primeiros casos --
    e falha DEVOLVENDO ZERO, que e o modo que nenhum teste de erro pega."""
    z = tmp_path / "x.zip"
    ano = C.ano_de(membro)
    _cotahist(z, membro, ano, [_linha(f"{ano}0102"), _linha(f"{ano}0103")])
    assert len(list(C.registros(str(z)))) == 2


def test_P99_a_versao_ANTERIOR_devolvia_zero_para_o_membro_sem_TXT(tmp_path):
    """Prova por mutacao: reintroduzo o filtro por extensao e vejo o silencio."""
    z = tmp_path / "x.zip"
    _cotahist(z, "COTAHIST.A1986", "1986", [_linha("19860102")])
    with zipfile.ZipFile(z) as zf:
        antigo = [n for n in zf.namelist() if n.upper().endswith(".TXT")]
    assert antigo == [], "o filtro antigo nao casava com nada -- e nao reclamava"
    assert len(list(C.registros(str(z)))) == 1, "o novo acha"


def test_P99_zip_sem_cara_de_cotahist_LEVANTA_em_vez_de_ler_lixo(tmp_path):
    """Ler posicoes fixas de um arquivo que nao e COTAHIST devolve numero -- e numero
    errado tem a mesma cara de numero certo (F-02). Melhor parar."""
    z = tmp_path / "x.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("qualquer.txt", "nao sou um cotahist\r\n")
    with pytest.raises(C.AcervoIlegivel):
        list(C.registros(str(z)))


# ── pregoes: um arquivo ruim nao apaga o acervo ───────────────────────────────

def test_P99_arquivo_corrompido_NAO_derruba_o_calendario(tmp_path, capsys):
    """O terceiro defeito, medido no `COTAHIST_A2026.ZIP` truncado de 18/09."""
    _cotahist(tmp_path / "COTAHIST_A2023.ZIP", "COTAHIST_A2023.TXT", "2023",
              [_linha("20230102"), _linha("20230103")])
    (tmp_path / "COTAHIST_A2026.ZIP").write_bytes(b"PK\x03\x04truncado")
    datas, cobertura = C.pregoes(str(tmp_path))
    assert len(datas) == 2, "o ano bom sobrevive ao ano ruim"
    assert cobertura[0].year == 2023


def test_P99_e_o_arquivo_corrompido_tambem_NAO_passa_calado(tmp_path, capsys):
    """O outro lado, e ele importa tanto quanto: o ano ilegivel FALTA no calendario, e
    quem consumir tem de saber. Ausencia de erro nao e afirmacao de integridade."""
    _cotahist(tmp_path / "COTAHIST_A2023.ZIP", "COTAHIST_A2023.TXT", "2023",
              [_linha("20230102")])
    (tmp_path / "COTAHIST_A2026.ZIP").write_bytes(b"PK\x03\x04truncado")
    C.pregoes(str(tmp_path))
    err = capsys.readouterr().err
    assert "ILEGIVEIS" in err and "COTAHIST_A2026.ZIP" in err


def test_P99_acervo_inteiro_ilegivel_nao_vira_calendario_vazio_silencioso(tmp_path,
                                                                          capsys):
    (tmp_path / "COTAHIST_A2026.ZIP").write_bytes(b"PK\x03\x04truncado")
    datas, cobertura = C.pregoes(str(tmp_path))
    assert datas == set() and cobertura == (None, None)
    assert "ILEGIVEIS" in capsys.readouterr().err, \
        "zero pregoes por ilegibilidade e zero pregoes por acervo vazio sao coisas "
    "diferentes, e so o aviso as separa"


# ── MODREF: enumeracao OBSERVADO (A-05) ───────────────────────────────────────

def test_P101_modref_sai_na_posicao_certa(tmp_path):
    """53-56 no leiaute rev. 02, que e 1-indexado -- logo `[52:56]` em Python. O
    campo chama-se MODREF, "moeda de referencia", e o leiaute NAO traz tabela de
    valores para ele: por isso a enumeracao e OBSERVADO."""
    z = tmp_path / "x.zip"
    _cotahist(z, "COTAHIST.A1986", "1986",
              [_linha("19860102", modref="CR$ "), _linha("19860304", modref="CZ$ ")])
    assert [C.modref_de(r) for r in C.registros(str(z))] == ["CR$", "CZ$"]


def test_P101_modref_desconhecido_e_ACUSADO_e_nao_adivinhado():
    """A-05 na letra: acumula o desconhecido, nao descarta (perderia dado) e nao
    adivinha (seria o F-02)."""
    assert C.conferir_modref({"R$", "CR$"}) == set()
    assert C.conferir_modref({"R$", "UFIR", ""}) == {"UFIR"}, \
        "vazio nao conta -- campo em branco e ausencia, nao valor novo"


def test_P101_a_enumeracao_declara_o_proprio_alcance():
    """P5 aplicada a lista: quatro valores, medidos em 8 dos 41 arquivos. A lista NAO e
    oficial -- o leiaute publicado **nao tem tabela de MODREF**, e por isso ela e
    `OBSERVADO` e sai do dado.

    **Corrigido em 19/09, no mesmo dia:** a lista era `C.MODREF_OBSERVADOS`, uma constante
    em Python. Valor de fonte externa em codigo e P2 violada, e foi a mesma correcao das
    posicoes -- agora ela vem de `docs/schemas/cotahist-v02.yaml`, onde o
    `incompleta_por_construcao: true` e o numero de arquivos lidos viajam JUNTO com os
    valores, em vez de ficarem num comentario que nenhum teste le."""
    assert set(C.modref_observados()) == {"CR$", "CZ$", "NCZ$", "R$"}


def test_P2_o_alcance_da_enumeracao_viaja_com_ela():
    """O que a constante em Python nao conseguia carregar: a lista sai de **8 dos 41**
    arquivos, e quem a usa tem de poder saber disso sem ler o comentario do codigo."""
    import yaml
    with io.open(os.path.join(C._raiz_do_schema(), C.SCHEMA), encoding="utf-8") as f:
        y = yaml.safe_load(f)
    mod = y["enumeracoes"]["MODREF"]
    assert mod["status"] == "OBSERVADO"
    assert mod["incompleta_por_construcao"] is True
    assert mod["arquivos_lidos"] < mod["arquivos_no_acervo"]


# ── o acervo real, quando ele estiver na maquina ──────────────────────────────

@pytest.mark.slow
@pytest.mark.xdist_group("cotahist_pregoes")  # P-141: o memo e por processo
@pytest.mark.skipif(not os.path.isdir(ACERVO_REAL),
                    reason="acervo de COTAHIST ausente -- ESTE TESTE NAO RODOU")
def test_P99_instantaneo_dourado_2023_nao_se_moveu(memo_do_acervo):
    """O que o passo 3 do §9 exige: a correcao trouxe 17 anos e NAO mexeu no ano que
    ja funcionava. 248 pregoes, mesmo sha256 do refactor de 18/09."""
    datas, _ = memo_do_acervo("calendario.pregoes", ACERVO_REAL,
                              lambda: C.pregoes(ACERVO_REAL))
    d23 = sorted(d for d in datas if d.year == 2023)
    assert len(d23) == PREGOES_2023
    assert hashlib.sha256(str(d23).encode()).hexdigest() == SHA_2023


@pytest.mark.slow
@pytest.mark.xdist_group("cotahist_pregoes")  # P-141: o memo e por processo
@pytest.mark.skipif(not os.path.isdir(ACERVO_REAL),
                    reason="acervo de COTAHIST ausente -- ESTE TESTE NAO RODOU")
def test_P99_todo_ano_no_disco_entra_no_calendario_ou_e_ACUSADO(memo_do_acervo):
    """A contagem que decai (familia do `sem_origem`): ano no disco que nao aparece no
    calendario so e aceitavel se o arquivo dele for ilegivel e isso ter sido dito."""
    datas, _ = memo_do_acervo("calendario.pregoes", ACERVO_REAL,
                              lambda: C.pregoes(ACERVO_REAL))
    no_calendario = {d.year for d in datas}
    ilegiveis = set()
    for chave, caminho in C.arquivos(ACERVO_REAL).items():
        try:
            next(iter(C.registros(caminho)), None)
        except C.AcervoIlegivel:
            ilegiveis.add(int(chave[-4:]))
    no_disco = {int(k[-4:]) for k in C.arquivos(ACERVO_REAL)}
    assert no_disco - no_calendario == ilegiveis, (
        f"anos que sumiram sem explicacao: "
        f"{sorted(no_disco - no_calendario - ilegiveis)}")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

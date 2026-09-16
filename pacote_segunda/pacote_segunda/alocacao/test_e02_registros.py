# -*- coding: utf-8 -*-
"""
test_e02_registros.py -- os tres estados do arquivo de pre-registro.

ACHADO E-02. `carregar_registros` fazia `if not os.path.exists(p): return {}, {}` e
com isso respondia "nenhuma tese registrada" quando a verdade era "o arquivo sumiu".
G7/G8 falham para o lado seguro, entao o sistema nunca ficou perigoso -- ficou
MENTIROSO, e a mentira pede a acao errada: "registre a tese" em vez de "ache o
arquivo, todas as suas teses sumiram".

DECISAO DELE, 12/09/2026: **arquivo ausente e arquivo vazio sao coisas diferentes.**
Estes testes sao essa frase, executavel.

A quarta coluna do desenho e a U-01, e ela tambem e dele: dado de usuario nao bloqueia
o sistema. Por isso `permitir_ausente=True` existe -- quem simula um usuario novo PEDE
a ausencia, em vez de recebe-la por padrao e nunca saber a diferenca.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tese as T                                                        # noqa: E402


# ── AUSENTE: levanta, e a mensagem tem de servir para agir ───────────────────

def test_ausente_levanta(tmp_path):
    with pytest.raises(T.RegistroAusente):
        T.carregar_registros(str(tmp_path / "nao_existe.yaml"))


def test_a_mensagem_do_ausente_diz_o_que_se_perde(tmp_path):
    """P1 aplicada a mensagem de erro: dos oito carregadores do projeto, os dois que
    ja acertavam eram os dois que escreveram a CONSEQUENCIA. Nao e coincidencia --
    quem escreve a consequencia descobre que precisa levantar."""
    with pytest.raises(T.RegistroAusente) as e:
        T.carregar_registros(str(tmp_path / "nao_existe.yaml"))
    m = str(e.value)
    assert "G7_tese_registrada" in m and "G8_compromisso_de_carrego" in m, \
        "a mensagem nao diz o que fica bloqueado"
    assert "permitir_ausente" in m, "a mensagem nao diz a saida legitima"


def test_ausente_com_permissao_explicita_devolve_vazio(tmp_path):
    """A U-01 como parametro, nao como padrao silencioso."""
    assert T.carregar_registros(str(tmp_path / "x.yaml"), permitir_ausente=True) == ({}, {})


# ── VAZIO: legitimo, e e o estado do primeiro dia ────────────────────────────

@pytest.mark.parametrize("conteudo,apelido", [
    ("",                          "arquivo em branco"),
    ("{}\n",                      "objeto vazio"),
    ("meta:\n  versao: 1\n",      "so o cabecalho, antes do primeiro registro"),
    ("teses:\ncarregos:\n",       "as duas secoes nulas"),
    ("teses: {}\ncarregos: {}\n", "as duas secoes vazias"),
])
def test_vazio_e_legitimo_e_NAO_levanta(tmp_path, conteudo, apelido):
    """Quem ainda nao registrou nada tem um arquivo PRESENTE e vazio. Levantar aqui
    quebraria o primeiro dia de qualquer usuario -- e a U-01 proibe."""
    f = tmp_path / "teses.yaml"
    f.write_text(conteudo, encoding="utf-8")
    assert T.carregar_registros(str(f)) == ({}, {}), apelido


def test_a_diferenca_entre_ausente_e_vazio_e_OBSERVAVEL(tmp_path):
    """O teste que da nome ao achado. Antes, os dois devolviam ({}, {}) e eram
    indistinguiveis de fora -- e era exatamente essa indistinguibilidade o defeito,
    porque `teses.yaml` E o pre-registro e a P4 existe para separar 'nunca me
    comprometi' de 'o registro sumiu'."""
    vazio = tmp_path / "teses.yaml"
    vazio.write_text("meta:\n  versao: 1\n", encoding="utf-8")
    ausente = tmp_path / "sumiu.yaml"

    assert T.carregar_registros(str(vazio)) == ({}, {})
    with pytest.raises(T.RegistroAusente):
        T.carregar_registros(str(ausente))


# ── ILEGIVEL: o terceiro estado, e ele nao e nenhum dos dois ─────────────────

def test_yaml_quebrado_nao_e_nenhuma_tese(tmp_path):
    """Arquivo corrompido pode ter o registro INTEIRO dentro, ilegivel por um
    caractere. Devolver ({}, {}) aqui seria dizer que nao ha tese quando ha."""
    f = tmp_path / "teses.yaml"
    f.write_text("teses: [a: 1\n  b\n", encoding="utf-8")
    with pytest.raises(T.RegistroIlegivel):
        T.carregar_registros(str(f))


def test_yaml_valido_que_nao_e_objeto_tambem_levanta(tmp_path):
    f = tmp_path / "teses.yaml"
    f.write_text("- uma\n- lista\n", encoding="utf-8")
    with pytest.raises(T.RegistroIlegivel):
        T.carregar_registros(str(f))


# ── o que NAO pode ter mudado ────────────────────────────────────────────────

def test_arquivo_real_do_projeto_continua_lendo_igual():
    """Instantaneo dourado: o `teses.yaml` do repositorio traz um exemplo de tese e um
    de carrego, os dois marcados `exemplo: true` e portanto INVALIDOS. Se esta leitura
    mudar, a correcao mexeu em quem nao estava quebrado."""
    real = os.path.join(os.path.dirname(os.path.abspath(T.__file__)), "teses.yaml")
    if not os.path.exists(real):
        pytest.skip("teses.yaml nao esta ao lado do tese.py neste ambiente")
    teses, carregos = T.carregar_registros(compromisso_maximo_anos=10)
    assert set(teses) == {"hash11"} and set(carregos) == {"td_ipca"}
    assert teses["hash11"]["valida"] is False
    assert carregos["td_ipca"]["valida"] is False
    assert "exemplo" in teses["hash11"]["motivo"]


def test_carregar_teses_repassa_a_permissao(tmp_path):
    """O atalho `carregar_teses` nao pode ter politica propria -- duas portas para a
    mesma sala com regras diferentes e o A-07 esperando acontecer."""
    with pytest.raises(T.RegistroAusente):
        T.carregar_teses(str(tmp_path / "x.yaml"))
    assert T.carregar_teses(str(tmp_path / "x.yaml"), permitir_ausente=True) == {}


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

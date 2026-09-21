# -*- coding: utf-8 -*-
"""
test_achados_ancorados.py -- DECISAO C executada, 19/09/2026.

O QUE FOI FEITO. Saiu do `CLAUDE.md` um intervalo contiguo de 962 linhas e 20.085 tokens:
os trinta achados de 06/09 a 18/09 que a secao 7 tinha acumulado. No lugar ficou um
**indice** -- uma linha por achado, com a REGRA que ele deixou e o ponteiro.

POR QUE NAO FOI OTIMIZACAO, e este e o argumento que decidiu: **a secao 10 deste arquivo
diz desde 06/09 que achado mora no `ACHADOS.md`** -- *"nao estao aqui de proposito:
misturar instrucao com historia custava ~10 mil tokens por sessao"*. Depois disso, trinta
achados entraram na secao 7. O arquivo declarava um comportamento que ele mesmo nao tinha,
e os dois concordavam por acidente porque ninguem media a secao 7. **E o defeito recorrente
da casa cometido pelo arquivo que o define**, e o corte foi fazer o arquivo cumprir a
propria regra -- nao inventar uma nova.

O CRITERIO ERA *"otimizacao sem perder contexto"*, e a resposta nao foi cortar 25% por
percentual. Foi triar por FUNCAO: a regra que impede a repeticao fica; a narrativa que a
explica vai. **O que impede a repeticao e a regra, nunca o relato** -- e achado que virou
teste esta ainda mais protegido, porque o teste falha e o texto nao.

O QUE ESTE ARQUIVO MEDE: que o corte nao deixou nome sem endereco. Os 26 achados do indice
tem de ter definicao em algum `.md`, e a lista TOTAL de orfaos nao pode crescer.

E ELE JA PEGOU O PROPRIO INDICE, no dia em que nasceu -- duas vezes:
  1. a tabela nasceu dentro de um blockquote, e o `^\\|` nao a via: **os 23 achados que o
     indice acabara de ancorar apareceram como orfaos**;
  2. corrigido isso, `| **A-03 / A-04** |` deixava o A-04 de fora -- **achado combinado
     numa celula e invisivel**. Virou uma linha por achado.
Ferramenta que mede o lugar errado, no dia em que nasceu. Foi a terceira vez neste projeto
(chaves_orfas com o merge do YAML, chaves_duplicadas com a ancora), e as tres tinham a
mesma forma: **o alcance do instrumento menor que o sistema.**
"""
from __future__ import annotations
import io
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import achados_ancorados as A  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Os 26 achados que o corte de 19/09 moveu. Esta lista e o CONTRATO do corte: cada um
# tinha texto no `CLAUDE.md` e passou a ter uma linha de indice. Se um perder o endereco,
# o corte virou perda.
MOVIDOS = ("X-01", "Y-01", "A-01", "A-02", "A-03", "A-04", "A-05", "A-06", "A-07",
           "B-02", "B-03", "C-01", "D-01", "E-01", "E-02", "E-03", "E-05", "E-06",
           "E-08", "E-09", "F-03", "P-05", "P-76", "P-77", "P-85", "V-01")

# Linha de base da contagem TOTAL de orfaos. **NAO_CONFIRMADO, e o motivo importa:** medida
# em 19/09 numa arvore SEM o `ACHADOS.md` e sem parte dos `.py` de `alocacao/`. Dos 46
# acusados, ~21 tem definicao NO `ACHADOS.md` e caem sozinhos quando ele estiver presente;
# 24 sao os `CANDIDATOS_19_09` (ver `achados_ancorados.py`), e parte deles provavelmente nao
# e achado.
#
# **O teto existe para pegar CRESCIMENTO, nao para certificar o valor.** Na primeira execucao
# na maquina dele o numero real aparece, e e ELE que vem para ca -- baixando o teto, nunca
# subindo. Teto que sobe para o teste passar e a linha de base apodrecendo (P-86).
TETO_ORFAOS = 46


def test_o_indice_de_achados_existe_no_CLAUDE_md():
    """Vacuidade primeiro: sem o indice, todos os outros passam sem ter medido nada --
    o modo de falha que o A-06 ensinou a temer."""
    with io.open(os.path.join(RAIZ, "CLAUDE.md"), encoding="utf-8") as f:
        s = f.read()
    assert "ÍNDICE DE ACHADOS" in s
    assert "| achado | a regra que ele deixou |" in s


def test_DECISAO_C_nenhum_achado_movido_perdeu_o_ENDERECO():
    """O portao do corte. Falha se alguem apagar uma linha do indice sem pôr o achado em
    outro lugar -- que e a unica forma de este corte virar perda de contexto."""
    _refs, defs, _falta = A.varrer(RAIZ)
    sem = [c for c in MOVIDOS if c not in defs]
    assert not sem, (
        f"achado(s) movidos em 19/09 e agora sem endereco: {sem}.\n"
        f"O `CLAUDE.md` cita o nome e nao ha onde ler o achado. Ou volta a linha de "
        f"indice, ou o achado ganha cabecalho no `ACHADOS.md`.")


def test_o_indice_e_legivel_pela_MAQUINA_e_nao_so_por_humano():
    """A segunda coisa que o instrumento pegou de si mesmo. Uma celula com dois codigos
    (`A-03 / A-04`) e lida como um. O teste prende a forma, nao a boa intencao."""
    with io.open(os.path.join(RAIZ, "CLAUDE.md"), encoding="utf-8") as f:
        linhas = [x for x in f.read().splitlines() if x.lstrip(">").strip().startswith("| **")]
    combinadas = [x for x in linhas if x.count("-") >= 2 and ("/" in x.split("|")[1]
                                                              or "," in x.split("|")[1])]
    assert not combinadas, (
        "linha de indice com mais de um achado na primeira celula:\n  "
        + "\n  ".join(x[:90] for x in combinadas))


def test_a_contagem_de_orfaos_NAO_CRESCE():
    """Contagem que decai (familia do `sem_origem`): ela encolhe quando alguem escreve uma
    definicao, e sobe no minuto em que um corte leva texto sem deixar ancora."""
    refs, defs, _falta = A.varrer(RAIZ)
    orf = A.orfaos(refs, defs)
    assert len(orf) <= TETO_ORFAOS, (
        f"{len(orf)} achados sem endereco, acima do teto de {TETO_ORFAOS}. "
        f"Novos: {sorted(orf)[:8]}")


def test_a_AUSENCIA_do_ACHADOS_md_e_declarada_e_nao_vira_verde():
    """Se o `ACHADOS.md` nao estiver na arvore, a lista de orfaos esta incompleta POR
    AUSENCIA DE ARQUIVO -- e fechar verde por isso seria o F-02 nesta camada."""
    fora = io.StringIO()
    _orf, falta = A.relatorio(RAIZ, saida=fora)
    if falta:
        assert "nao ha ACHADOS.md" in fora.getvalue()


def test_os_CANDIDATOS_de_19_09_continuam_declarados_e_nao_viraram_linha_de_base():
    """P3 aplicada a auditoria: o modulo imprime *candidatos*, nunca *achados*.

    Os 24 codigos que o instrumento levantou em 19/09 estao citados SO em codigo. Parte
    nao e achado -- `K-*` sao teses, `V-*` parecem itens de um laudo de agosto. Promove-los
    a defeito sem ler seria o **E-05** outra vez: eu varri um namespace e conclui sobre
    outro. Mas jogar os 24 na linha de base sem motivo seria pior -- viraria cobertura
    falsa. Ficam nomeados, a espera de leitura."""
    assert len(A.CANDIDATOS_19_09) == 24
    misturados = [c for c in A.CANDIDATOS_19_09 if c in A.NAO_SAO_ACHADOS]
    assert not misturados, (
        f"{misturados} saiu de candidato para linha de base -- isso e legitimo, mas exige "
        f"o motivo escrito e a saida desta tupla, nas duas pontas")


def test_a_linha_de_base_declara_o_motivo_de_cada_excecao():
    """Lista sem motivo e lembrete, nao regra (P-82)."""
    assert A.NAO_SAO_ACHADOS
    assert all(isinstance(v, str) and v for v in A.NAO_SAO_ACHADOS.values())


# ── prova por mutacao ────────────────────────────────────────────────────────

def test_mutacao_achado_citado_e_nao_definido_e_ACUSADO(tmp_path):
    """`ignorar={}` de proposito: o `Z-99` esta na linha de base da arvore REAL (ele mora
    neste arquivo), e sem o parametro esta prova por mutacao se auto-anularia -- a guarda
    passaria dizendo "nenhum orfao" porque o codigo de teste estava na exclusao."""
    (tmp_path / "codigo.py").write_text("# Z-99: uma regra qualquer\n", encoding="utf-8")
    refs, defs, _ = A.varrer(str(tmp_path), ignorar={})
    assert A.orfaos(refs, defs) == {"Z-99": {"codigo.py": 1}}


def test_a_linha_de_base_REALMENTE_silencia_na_arvore_real(tmp_path):
    """O outro lado da mesma moeda: com a linha de base padrao, o mesmo arquivo cala."""
    (tmp_path / "codigo.py").write_text("# Z-99: uma regra qualquer\n", encoding="utf-8")
    refs, defs, _ = A.varrer(str(tmp_path))
    assert not A.orfaos(refs, defs)


def test_mutacao_cabecalho_em_md_ANCORA_o_achado(tmp_path):
    (tmp_path / "codigo.py").write_text("# Z-99: uma regra\n", encoding="utf-8")
    (tmp_path / "ACHADOS.md").write_text("## Z-99 · a regra\n\ncorpo\n", encoding="utf-8")
    refs, defs, falta = A.varrer(str(tmp_path), ignorar={})
    assert not A.orfaos(refs, defs) and not falta


def test_mutacao_linha_de_indice_ANCORA_mesmo_dentro_de_blockquote(tmp_path):
    """O defeito numero 1 do proprio instrumento, preso num teste."""
    (tmp_path / "codigo.py").write_text("# Z-99: uma regra\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("> | **Z-99** | a regra que ele deixou |\n",
                                        encoding="utf-8")
    refs, defs, _ = A.varrer(str(tmp_path), ignorar={})
    assert not A.orfaos(refs, defs), "blockquote nao pode esconder a ancora"


def test_mutacao_UTF_8_nao_e_confundido_com_achado(tmp_path):
    (tmp_path / "x.py").write_text("# -*- coding: UTF-8 -*-\n", encoding="utf-8")
    refs, defs, _ = A.varrer(str(tmp_path))
    assert not A.orfaos(refs, defs)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

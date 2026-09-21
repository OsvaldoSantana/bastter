# -*- coding: utf-8 -*-
"""
test_tamanho_do_contexto.py -- RETRATACAO da secao 11.4, 19/09/2026.

O QUE A 11.4 AFIRMAVA, citado:

    | `CLAUDE.md`      | 1.112 linhas | **482** |
    | `PENDENCIAS.md`  |   911 linhas | **565** |
    | **total por sessao** | **~26 mil tokens** | **~13 mil** |

A EVIDENCIA QUE DERRUBA, medida em 19/09 com `tiktoken cl100k_base` sobre os sete
arquivos maiores do repositorio: a razao real e **19,0 tokens/linha** e **2,96
chars/token**. Logo 1.047 linhas nao sao "~13 mil" -- sao **~19.900**; e 2.023 linhas
nao sao "~26 mil" -- sao **~38.400**. Erro de **+53%** e **+48%**.

A CAUSA RAIZ, e ela nao e aritmetica: **eu escrevi uma tabela de tokens sem escrever a
conta.** A 11.4 foi redigida em 06/09 para relatar um corte que eu mesmo tinha feito, e o
numero servia para mostrar que o corte funcionou. Nenhuma das quatro celulas tem
procedencia, e o `CLAUDE.md` passou treze dias apresentando como MEDIDO o que era
impressao.

    E o custo apareceu do lado de fora. Em 19/09 um plano de otimizacao de tokens declarou
    ter CALIBRADO a propria razao empirica nos "~13 mil" da 11.4 -- e errou a leitura
    inicial do projeto por 90% por causa disso. **Numero plausivel em prosa, citado por
    terceiro como fonte: e o C-01 na camada do token**, e desta vez ele contaminou alguem
    que nao tinha como conferir.

O QUE FOI CORRIGIDO NO PROCESSO, e e o que faz esta retratacao valer mais que a correcao:
trocar os numeros da 11.4 deixaria a proxima estimativa igualmente cega. Entao nasceu o
`auditoria/tamanho_do_contexto.py` -- **o tamanho do contexto deixou de ser frase e virou
comando**. A 11.4 passa a apontar para ele em vez de afirmar valor.

E O BURACO QUE A MEDICAO ACHOU, que ninguem tinha visto: **o projeto nunca declarou qual e
o conjunto de leitura inicial.** Sem essa lista, "a leitura de sessao custa N" e a
suposicao de quem mediu, nao um fato do projeto -- e foi por isso que tres planos
diferentes chegaram a tres numeros diferentes sem nenhum estar errado sobre a propria
conta. Agora a lista esta em `SEMPRE` e `SOB_DEMANDA`, com o motivo ao lado, e arquivo
`.md` novo na raiz nasce **NAO CLASSIFICADO** e e acusado.
"""
from __future__ import annotations
import io
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tamanho_do_contexto as T  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Os numeros da 11.4, como ela os escrevia. Ficam aqui porque retratacao cita, nao
# parafraseia -- e porque um teste que guarda o numero errado e o unico que prova que
# alguem mediu o certo.
DECLARADO_11_4 = {"antes": (2023, 26_000), "depois": (1047, 13_000)}


def test_a_razao_de_14_tokens_por_linha_esta_ERRADA_neste_repositorio():
    """O erro que produziu todos os outros. 14 t/linha vem de markdown em INGLES."""
    _n, contar = T.instrumento()
    medidas = []
    for nome in ("CLAUDE.md", "PENDENCIAS.md", "PLANO.md"):
        c = os.path.join(RAIZ, nome)
        if not os.path.exists(c):
            continue
        with io.open(c, encoding="utf-8") as f:
            s = f.read()
        medidas.append(contar(s) / (s.count("\n") + 1))
    if not medidas:
        pytest.skip("nenhum dos tres arquivos de leitura existe -- ESTE TESTE NAO RODOU")
    media = sum(medidas) / len(medidas)
    assert media > 16.0, (
        f"medido {media:.1f} tokens/linha. Se este teste falhar por a media ter CAIDO "
        f"abaixo de 16, o estilo do projeto mudou e a constante "
        f"TOKENS_POR_LINHA_MEDIDO={T.TOKENS_POR_LINHA_MEDIDO} precisa ser remedida -- "
        f"nao ajustada para o teste passar.")


def test_os_numeros_da_11_4_nao_sobrevivem_a_razao_medida():
    """A retratacao com a conta escrita: e isto que a 11.4 nao tinha."""
    for chave, (linhas, declarado) in DECLARADO_11_4.items():
        real = linhas * T.TOKENS_POR_LINHA_MEDIDO
        erro = real / declarado - 1
        assert erro > 0.40, (
            f"{chave}: a 11.4 dizia {declarado:,}; a razao medida da {real:,.0f} "
            f"({erro:+.0%})")


def test_o_instrumento_ANUNCIA_qual_proxy_usou():
    """P5 aplicada a ferramenta. Nenhum dos dois caminhos e o tokenizador do Claude, e o
    relatorio tem de dizer isso antes de qualquer numero -- senao ele repete o defeito
    da 11.4 com outra cara: valor sem alcance declarado."""
    nome, contar = T.instrumento()
    assert "proxy" in nome.lower()
    assert contar("abc") > 0


def test_relatorio_declara_o_ESTAVEL_e_nao_chama_isso_de_custo_de_sessao():
    """A 11.4 chamava a leitura inicial de *total por sessao*, e era esse o erro
    conceitual embaixo do erro aritmetico: com cache de prefixo, o estavel e pago
    integral uma vez e o que custa em todo turno e o que MUDA. O relatorio nao pode
    voltar a prometer o que nao mede."""
    fora = io.StringIO()
    T.relatorio(RAIZ, saida=fora)
    texto = fora.getvalue()
    assert "LEITURA DE SESSAO" in texto
    assert "ESTAVEL" in texto and "cache" in texto
    assert "por sessao:" not in texto


def test_todo_md_da_raiz_tem_PAPEL_declarado():
    """A contagem que decai. Arquivo novo sem papel torna a medicao incompleta, e a
    incompletude fica VISIVEL em vez de virar um numero menor sem explicacao."""
    _n, contar = T.instrumento()
    orfaos = T.nao_classificados(T.medir(RAIZ, contar))
    assert not orfaos, (
        f"arquivo(s) .md sem papel: {orfaos}. Classifique em SEMPRE ou SOB_DEMANDA no "
        f"`tamanho_do_contexto.py`, com o motivo ao lado.")


def test_a_lista_de_SEMPRE_nao_aponta_para_arquivo_que_nao_existe():
    """O outro lado, e a licao e a P7 da declaracao apodrecida: lista que nomeia arquivo
    inexistente PARECE cobertura."""
    faltando = [n for n in T.SEMPRE if not os.path.exists(os.path.join(RAIZ, n))]
    assert not faltando, f"declarados SEMPRE e inexistentes: {faltando}"


# ── prova por mutacao ────────────────────────────────────────────────────────

def test_mutacao_md_novo_na_raiz_e_ACUSADO(tmp_path):
    """Guarda que nunca falhou e guarda que ninguem sabe se funciona (regua §5-B.4)."""
    (tmp_path / "CLAUDE.md").write_text("x\n", encoding="utf-8")
    (tmp_path / "LAUDO-NOVO.md").write_text("y\n", encoding="utf-8")
    _n, contar = T.instrumento()
    assert T.nao_classificados(T.medir(str(tmp_path), contar)) == ["LAUDO-NOVO.md"]


def test_mutacao_a_razao_grosseira_e_a_do_tiktoken_concordam_em_ORDEM_DE_GRANDEZA():
    """As duas sao proxy, e o modulo troca de uma para a outra em silencio se o
    `tiktoken` sair do ambiente. Se elas divergissem por mais de 20%, essa troca mudaria
    a conclusao sem ninguem notar -- que e exatamente a classe de defeito do N-01."""
    c = os.path.join(RAIZ, "CLAUDE.md")
    if not os.path.exists(c):
        pytest.skip("CLAUDE.md ausente -- ESTE TESTE NAO RODOU")
    with io.open(c, encoding="utf-8") as f:
        s = f.read()
    grosseiro = len(s) / T.CHARS_POR_TOKEN
    try:
        import tiktoken
        fino = len(tiktoken.get_encoding("cl100k_base").encode(s))
    except Exception:
        pytest.skip("tiktoken ausente -- a comparacao dos dois proxies NAO RODOU")
    assert abs(grosseiro / fino - 1) < 0.20, \
        f"grosseiro {grosseiro:,.0f} x tiktoken {fino:,} -- recalibrar CHARS_POR_TOKEN"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

# -*- coding: utf-8 -*-
"""O registro de erros e o resumo semanal. O primeiro teste e o pedido: evento sem codigo
reprova."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metricas_processo as M  # noqa: E402


def _e(**kw):
    base = dict(data="2026-09-25", codigo="CV-07", tipo="achado", autor="claude-code",
                quem_achou="claude-code", regua="desconhecido", commit_introduziu="x",
                commit_corrigiu="aberto", descricao="d")
    base.update(kw)
    return base


def test_evento_SEM_CODIGO_reprova():
    with pytest.raises(M.EventoInvalido, match="sem codigo"):
        M.validar([_e(codigo="  ")])


def test_valor_fora_da_lista_e_campo_vazio_reprovam():
    with pytest.raises(M.EventoInvalido, match="tipo"):
        M.validar([_e(tipo="bug")])
    with pytest.raises(M.EventoInvalido, match="quem_achou"):
        M.validar([_e(quem_achou="gpt")])
    with pytest.raises(M.EventoInvalido, match="desconhecido"):
        M.validar([_e(regua="")])


def test_por_semana_conta_retratacao_por_autor_e_a_fracao_do_osvaldo():
    ev = [_e(data="2026-09-18", tipo="retratacao", autor="claude-chat", quem_achou="osvaldo"),
          _e(data="2026-09-19", tipo="reincidencia"),
          _e(data="2026-09-25")]
    s = M.por_semana(ev)
    assert s["2026-S38"]["retratacoes"] == {"claude-chat": 1}
    assert s["2026-S38"]["reincidencias"] == 1 and s["2026-S38"]["achados_osvaldo"] == 1
    assert "50% (1 de 2)" in M.relatorio(ev, None)


def test_sem_sessoes_o_relatorio_DIZ_que_nao_mediu(tmp_path):
    assert M.sessoes_por_semana(str(tmp_path / "nao.csv")) is None
    assert "NAO medida" in M.relatorio([_e()], None)


def test_o_eventos_csv_do_repositorio_e_valido():
    ev = M.validar(M.ler())
    assert len(ev) >= 39 and all(e["codigo"] for e in ev)

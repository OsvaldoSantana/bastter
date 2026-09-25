# -*- coding: utf-8 -*-
"""O instrumento que mediu a P-141 (pytest = 58% do tempo dos pedidos de 21 a 24/09).

A promessa que sustenta o numero: ferramentas que rodam ao mesmo tempo contam o tempo de
PAREDE, nao a soma. Se contassem a soma, tres buscas paralelas de 10 s virariam 30 s de
"ferramenta" num pedido de 10 s -- e a fracao do pytest sairia inflada ou encolhida
conforme o que rodou ao lado dele."""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analisar_sessoes as A  # noqa: E402

T0 = dt.datetime(2026, 9, 24, 12, 0, 0, tzinfo=dt.timezone.utc)


def _t(s):
    return T0 + dt.timedelta(seconds=s)


def test_uniao_de_intervalos_sobrepostos_e_o_tempo_de_parede():
    assert A.uniao_s([(_t(0), _t(10)), (_t(0), _t(12))]) == 12.0


def test_uniao_de_intervalos_disjuntos_e_a_soma():
    assert A.uniao_s([(_t(0), _t(10)), (_t(20), _t(25))]) == 15.0


def test_intervalo_contido_nao_soma_nada():
    assert A.uniao_s([(_t(0), _t(30)), (_t(5), _t(10))]) == 30.0


def test_a_ordem_de_chegada_nao_importa():
    iv = [(_t(20), _t(25)), (_t(0), _t(12)), (_t(0), _t(10))]
    assert A.uniao_s(iv) == A.uniao_s(sorted(iv)) == 17.0


def _ev(s, **kw):
    return dict(timestamp=_t(s).isoformat().replace("+00:00", "Z"), **kw)


def _uso(ids, mid):
    return {"type": "assistant", "message": {"id": mid, "content": [
        {"type": "tool_use", "id": i, "name": "Bash", "input": {"command": "py -3.11 -m pytest"}}
        for i in ids]}}


def _resultado(i):
    return {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": i}]}}


def test_FIM_A_FIM_duas_ferramentas_sobrepostas_contam_a_parede(tmp_path):
    """Uma transcricao sintetica: duas chamadas pedidas em t=0 (terminam em 10 e 12) e
    uma terceira de 20 a 25. Parede = 17 s; soma = 27 s. O relatorio guarda as duas, e o
    `ferr_s` -- o que entra na fracao -- e a parede."""
    linhas = [
        _ev(0, type="user", message={"content": "rode a suite"}),
        _ev(0, **_uso(["a", "b"], "m1")),
        _ev(10, **_resultado("a")),
        _ev(12, **_resultado("b")),
        _ev(20, **_uso(["c"], "m2")),
        _ev(25, **_resultado("c")),
    ]
    arq = tmp_path / "sessao.jsonl"
    arq.write_text("\n".join(json.dumps(x) for x in linhas), encoding="utf-8")
    _ses, turnos, ferr = A.analisar_sessao(str(arq), None)
    assert len(turnos) == 1 and len(ferr) == 3
    assert turnos[0]["ferr_soma_s"] == 27.0
    assert turnos[0]["ferr_s"] == 17.0
    assert all(f["categoria"] == "Bash:pytest" for f in ferr)


def test_so_grava_dentro_de_saida(tmp_path):
    pasta = tmp_path / "transcricoes"
    pasta.mkdir()
    (pasta / "s.jsonl").write_text("\n".join(json.dumps(x) for x in [
        _ev(0, type="user", message={"content": "oi"}),
        _ev(1, **_uso(["a"], "m1")), _ev(2, **_resultado("a"))]), encoding="utf-8")
    saida = tmp_path / "saida"
    assert A.main(["--pasta", str(pasta), "--saida", str(saida)]) == 0
    assert sorted(os.listdir(saida)) == ["ferramentas.csv", "relatorio.md", "sessoes.csv",
                                         "turnos.csv"]
    assert sorted(os.listdir(tmp_path)) == ["saida", "transcricoes"]

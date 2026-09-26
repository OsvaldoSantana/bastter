# -*- coding: utf-8 -*-
"""O corte de 26/09 nao perdeu codigo nenhum -- e o proximo tambem nao perde."""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import codigos_preservados as C  # noqa: E402


def test_nenhum_codigo_da_linha_de_base_sumiu_do_repositorio():
    base = C.ler_base()
    assert len(base) > 300, "vacuidade: a linha de base tem de existir e ter os codigos"
    falta = C.sumidos(base, C.codigos())
    assert not falta, (
        f"codigo(s) que existiam e sumiram do repositorio: {falta}. Mover historia e "
        f"permitido; apagar nao (secao 5-A). Devolva o texto a algum arquivo.")


def test_a_linha_de_base_cobre_os_tres_tipos_de_codigo():
    base = C.ler_base()
    for c in ("P-57", "A-06", "5-B.13", "CV-01"):
        assert c in base, f"{c} fora da linha de base -- a varredura mudou de alcance"


def test_mutacao_um_bloco_apagado_reprova(tmp_path):
    """Duas arvores: o codigo esta numa, some na outra. Guarda que nunca falhou nao se sabe
    se funciona (regua 5-B, pergunta 4)."""
    (tmp_path / "a.md").write_text("## ~~P-900~~ · algo\n5-B.40 e A-901\n", encoding="utf-8")
    base = set(C.codigos(str(tmp_path)))
    assert {"P-900", "A-901", "5-B.40"} <= base
    (tmp_path / "a.md").write_text("## A-901\n", encoding="utf-8")
    assert C.sumidos(base, C.codigos(str(tmp_path))) == ["5-B.40", "P-900"]


def test_mover_de_arquivo_nao_reprova(tmp_path):
    """O controle: o corte e MOVER, e mover tem de passar."""
    (tmp_path / "CLAUDE.md").write_text("P-900 e 5-B.40\n", encoding="utf-8")
    base = set(C.codigos(str(tmp_path)))
    (tmp_path / "CLAUDE.md").write_text("indice\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "historia.md").write_text("P-900 e 5-B.40\n", encoding="utf-8")
    assert C.sumidos(base, C.codigos(str(tmp_path))) == []

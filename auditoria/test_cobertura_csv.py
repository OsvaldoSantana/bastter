# -*- coding: utf-8 -*-
"""O conversor de cobertura do job semanal: medida, estavel, sem piso."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cobertura_csv as C  # noqa: E402

COV = {"files": {
    "fase0\\ajustar.py": {"summary": {"num_statements": 100, "covered_lines": 90}},
    "fase0/test_ajustar.py": {"summary": {"num_statements": 50, "covered_lines": 10}},
    "alocacao/cenarios.py": {"summary": {"num_statements": 40, "covered_lines": 8}},
    "alocacao/conftest.py": {"summary": {"num_statements": 0, "covered_lines": 0}}}}


def test_uma_linha_por_modulo_ordenada_e_com_barra_normal():
    rows = C.linhas(COV)
    assert [r["modulo"] for r in rows] == ["alocacao/cenarios.py", "alocacao/conftest.py",
                                           "fase0/ajustar.py", "fase0/test_ajustar.py"]
    assert rows[2]["percentual"] == "90.0" and rows[1]["percentual"] == "100.0"


def test_abaixo_de_50_so_lista_PRODUCAO():
    """O teste com 20% nao entra: cobertura de teste nao e pergunta."""
    assert [r["modulo"] for r in C.abaixo(C.linhas(COV))] == ["alocacao/cenarios.py"]


def test_mesma_entrada_mesmo_arquivo(tmp_path):
    """O bot so commita se mudar: a saida tem de ser byte a byte estavel."""
    j = tmp_path / "c.json"
    j.write_text(json.dumps(COV), encoding="utf-8")
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    C.main([str(j), "--saida", str(a)])
    C.main([str(j), "--saida", str(b)])
    assert a.read_bytes() == b.read_bytes()
    cabecalho = a.read_text(encoding="utf-8").splitlines()[0]
    assert cabecalho == "modulo;producao;linhas;executadas;percentual"

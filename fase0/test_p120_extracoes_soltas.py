# -*- coding: utf-8 -*-
"""P-120 -- o acervo do COTAHIST guarda so o ZIP, e o manifesto conta o que sobrar.

Decisao dele, 24/09/2026: as 41 copias extraidas (5.993.738.309 bytes) foram apagadas
depois de conferidas por cabecalho, tamanho e CRC-32 contra o membro do ZIP. A extracao e
derivada e se refaz; manifesta-la seria pagar 7x de leitura para provar o que o ZIP prova.

O que estes testes guardam e que a decisao nao dependa de memoria (P7): o manifesto CONTA,
sem calcular hash, todo arquivo com cara de COTAHIST que nao e .zip, e avisa no fim.

Prova por mutacao, feita em 24/09 e desfeita:
  - `extracoes_soltas` devolvendo []   -> 3 reprovam (os que esperam contagem > 0; o do
                                          acervo real passa, e passaria -- ele mede o disco)
  - sem o filtro `not .zip`            -> 6 reprovam, inclusive o do acervo real
  - `sha256` chamado por copia solta   -> 1 reprova (`test_conta_SEM_calcular_hash`)
  - o `print` da contagem removido     -> 2 reprovam (o do zero e o do aviso)
"""
import os
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifesto_cvm as M                                               # noqa: E402

ACERVO_REAL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "bronze", "b3", "cotahist")


def _zip(caminho):
    with zipfile.ZipFile(caminho, "w") as z:
        z.writestr("COTAHIST_A2023.TXT", b"00COTAHIST.2023BOVESPA 20240102\r\n")


def _acervo(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    ac = tmp_path / "data" / "b3"
    ac.mkdir(parents=True)
    _zip(ac / "COTAHIST_A2023.ZIP")
    return ac


def test_conta_as_tres_convencoes_de_nome_e_a_subpasta(tmp_path):
    """As tres formas que a extracao produziu de fato (P-99/P-126) e a pasta de ano da
    P-121. O ZIP e o arquivo alheio NAO entram."""
    ac = _acervo(tmp_path)
    (ac / "COTAHIST_A2023.TXT").write_bytes(b"x")
    (ac / "COTAHIST.A1986").write_bytes(b"x")
    (ac / "COTAHIST_A2001").write_bytes(b"x")
    (ac / "COTAHIST_A2026").mkdir()
    (ac / "COTAHIST_A2026" / "COTAHIST_A2026.TXT").write_bytes(b"x")
    (ac / "LEIA.md").write_bytes(b"x")
    nomes = sorted(os.path.relpath(p, ac).replace("\\", "/")
                   for p in M.extracoes_soltas(str(ac)))
    assert nomes == ["COTAHIST.A1986", "COTAHIST_A2001", "COTAHIST_A2023.TXT",
                     "COTAHIST_A2026/COTAHIST_A2026.TXT"]


def test_e_mais_largo_que_o_leitor(tmp_path):
    """Sobra de extracao que o `calendario.ano_de()` recusaria continua sendo sobra: o
    alarme tem de ser mais largo que o leitor, nunca mais estreito."""
    ac = _acervo(tmp_path)
    (ac / "cotahist_a2023.txt.part").write_bytes(b"x")
    assert len(M.extracoes_soltas(str(ac))) == 1


def test_so_ZIP_da_zero(tmp_path):
    assert M.extracoes_soltas(str(_acervo(tmp_path))) == []


def test_conta_SEM_calcular_hash(tmp_path, monkeypatch):
    """Contar e o que ele decidiu; hashear 6 GB de derivado e o que ele recusou."""
    ac = _acervo(tmp_path)
    (ac / "COTAHIST_A2023.TXT").write_bytes(b"x" * 10)
    vistos = []
    original = M.sha256
    monkeypatch.setattr(M, "sha256", lambda c, *a, **k: vistos.append(c) or original(c))
    assert M.main(["--manifesto", str(ac)]) == 0
    assert [os.path.basename(v) for v in vistos] == ["COTAHIST_A2023.ZIP"]


def test_main_AVISA_no_fim_quando_ha_copia(tmp_path, capsys):
    ac = _acervo(tmp_path)
    (ac / "COTAHIST_A2023.TXT").write_bytes(b"x")
    assert M.main(["--manifesto", str(ac)]) == 0, "o aviso nao derruba o retrato (P-102)"
    saida = capsys.readouterr()
    assert "P-120: 1 copia(s)" in saida.out
    assert "AVISO P-120" in saida.err
    assert "COTAHIST_A2023.TXT" in saida.err
    assert saida.err.rstrip().endswith("extraia fora do acervo."), "o aviso e a ultima linha"


def test_main_diz_o_ZERO_em_vez_de_calar(tmp_path, capsys):
    """§5-B.14: zero medido e silencio nao podem ter a mesma saida."""
    ac = _acervo(tmp_path)
    assert M.main(["--manifesto", str(ac)]) == 0
    saida = capsys.readouterr()
    assert "P-120: 0 copia(s)" in saida.out
    assert "AVISO P-120" not in saida.err


@pytest.mark.skipif(not os.path.isdir(ACERVO_REAL),
                    reason="acervo de COTAHIST ausente -- ESTE TESTE NAO RODOU")
def test_P120_o_acervo_real_guarda_so_ZIP():
    """A decisao de 24/09 medida no disco, a cada rodada da suite -- nao lembrada."""
    soltas = M.extracoes_soltas(ACERVO_REAL)
    assert soltas == [], "P-120: copias extraidas voltaram ao acervo: %s" % soltas

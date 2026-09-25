# -*- coding: utf-8 -*-
"""O materializador do job semanal: copia o que o armazem entrega e ACUSA o que nao entrega."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import materializar_acervo as M  # noqa: E402


def _abrir_de(tmp_path, disponiveis):
    def abrir(recurso, arquivo):
        if arquivo not in disponiveis:
            raise KeyError(f"{arquivo} nao esta no armazem")
        p = tmp_path / "cache" / arquivo
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"conteudo " + arquivo.encode())
        return str(p)
    return abrir


def test_copia_para_o_caminho_que_os_testes_leem(tmp_path):
    itens = {("b3", "cotahist", "COTAHIST_A2023.ZIP")}
    cop, ja, faltas = M.materializar(itens, str(tmp_path),
                                     _abrir_de(tmp_path, {"COTAHIST_A2023.ZIP"}))
    destino = tmp_path / "data" / "bronze" / "b3" / "cotahist" / "COTAHIST_A2023.ZIP"
    assert cop == [str(destino)] and destino.read_bytes() == b"conteudo COTAHIST_A2023.ZIP"
    assert not ja and not faltas


def test_o_que_o_armazem_NAO_entrega_vira_FALTA_e_nao_derruba_o_resto(tmp_path):
    """CV-07: o registro diz que a versao existe, o armazem nao a tem."""
    itens = {("cvm", "fca", "fca_cia_aberta_2011.zip"), ("cvm", "dfp", "dfp_cia_aberta_2011.zip")}
    cop, _ja, faltas = M.materializar(itens, str(tmp_path),
                                      _abrir_de(tmp_path, {"dfp_cia_aberta_2011.zip"}))
    assert len(cop) == 1 and len(faltas) == 1 and "fca_cia_aberta_2011.zip" in faltas[0]


def test_o_que_ja_esta_no_lugar_nao_e_copiado_de_novo(tmp_path):
    destino = tmp_path / "data" / "bronze" / "cvm" / "cad" / "cad.csv"
    destino.parent.mkdir(parents=True)
    destino.write_bytes(b"x")
    cop, ja, _f = M.materializar({("cvm", "cad", "cad.csv")}, str(tmp_path),
                                 lambda r, a: str(destino))
    assert cop == [] and ja == [str(destino)]


def test_conhecidos_inclui_o_registro_e_o_inventario():
    itens = M.conhecidos()
    assert ("b3", "cotahist", "COTAHIST_A2023.ZIP") in itens
    assert ("cvm", "dfp", "dfp_cia_aberta_2010.zip") in itens

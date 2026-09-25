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


def test_CI04_as_versoes_fixadas_do_ML_entram_na_lista():
    """CI-04: o pin de 2026 (fb3546ed...) nao e a vigente; sem ele aqui, o leitor do ML ia ao
    armazem no passo dos testes, que nao tem segredo."""
    fix = M.fixados()
    assert ("cotahist", "COTAHIST_A2026.ZIP",
            "fb3546ed27cc8a138e93c141adce3e8dc684df219ebffa4d49bff5d557b3e5e3") in fix
    assert all(len(sha) == 64 for _r, _a, sha in fix)


def test_CI04_a_fixada_e_pedida_PELA_VERSAO_e_conferida(tmp_path):
    pedidos = []

    def abrir(recurso, arquivo, versao=None, conferir=False):
        pedidos.append((arquivo, versao, conferir))
        if arquivo == "COTAHIST_A2025.ZIP":
            raise OSError("armazem indisponivel")
        return str(tmp_path / arquivo)

    prontos, faltas = M.materializar_fixados(
        {("cotahist", "COTAHIST_A2026.ZIP", "a" * 64),
         ("cotahist", "COTAHIST_A2025.ZIP", "b" * 64)}, abrir)
    assert ("COTAHIST_A2026.ZIP", "a" * 64, True) in pedidos
    assert len(prontos) == 1 and len(faltas) == 1 and "COTAHIST_A2025.ZIP@bbbbbbbbbbbb" in faltas[0]


def test_nefin_o_pin_vem_da_politica():
    assert M.nefin_fixado() == "619991c2192c"


def test_nefin_e_pedido_PELO_PIN_e_copiado_para_onde_o_motor_le(tmp_path):
    """Pedir a vigente trocaria o insumo do pre-registro quando o NEFIN publicar adiante."""
    (tmp_path / "alocacao").mkdir()
    (tmp_path / "alocacao" / "politica.yaml").write_text(
        "pesquisa:\n  fonte:\n    sha256_12: 'abc123'\n", encoding="utf-8")
    fonte = tmp_path / "cache.csv"
    fonte.write_bytes(b"serie")
    pedidos = []

    def abrir(recurso, arquivo, versao=None, conferir=False):
        pedidos.append((recurso, arquivo, versao, conferir))
        return str(fonte)

    destino, faltas = M.materializar_nefin(str(tmp_path), abrir)
    assert pedidos == [("risk_factors", "nefin_factors.csv", "abc123", True)] and not faltas
    assert open(destino, "rb").read() == b"serie"
    assert destino.endswith(os.path.join("alocacao", "dados", "nefin_factors.csv"))


def test_nefin_sem_pin_ou_sem_arquivo_e_FALTA(tmp_path):
    (tmp_path / "alocacao").mkdir()
    (tmp_path / "alocacao" / "politica.yaml").write_text("pesquisa: {}\n", encoding="utf-8")
    destino, faltas = M.materializar_nefin(str(tmp_path), lambda *a, **k: "nunca")
    assert destino is None and "sha256_12" in faltas[0]

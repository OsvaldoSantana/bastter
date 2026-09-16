# -*- coding: utf-8 -*-
"""Testes da guarda de campos mortos (`campos_mortos.py`).

Mesmo desenho do P-28 do lado YAML: o que a guarda acusa ou sai do codigo, ou entra
num inventario com numero de pendencia -- e o inventario nao pode apodrecer.
"""
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import campos_mortos as cm

# Divida inventariada, 11/09/2026. Uma entrada aqui e uma promessa registrada, nao uma
# isencao: o segundo teste quebra se ela deixar de estar morta ou sair do codigo.
INVENTARIO = {
    # P-77 SAIU daqui em 16/09/2026, e quem acusou foi o segundo teste deste arquivo:
    # `regime_tributario` passou a ler `aliquota_ganho` e a linha virou mentira. Um
    # inventario que so cresce e uma lista de desculpas; este apodrece de proposito.
    # P-78: dado de pesquisa coletado e nunca pontuado; decidir por campo.
    # Quatro SAIRAM em 16/09 (P-84, decisao dele de 13/09): `corretagem_etf_pct`
    # virou segunda parcela da dimensao `corretagem`; `corretagem_fii`,
    # `exercicio_opcao_pct` e `mesa_minimo` sao lidos por `custo_por_operacao()`,
    # exibidos e nunca pontuados. Sobram os dois de procedencia e os dois de
    # facilidade, que `regras()` recusa ligar.
    "corretoras.py:Instituicao.bc_procedentes": "P-78",
    "corretoras.py:Instituicao.bc_clientes": "P-78",
    "corretoras.py:Instituicao.home_broker_web": "P-78",
    "corretoras.py:Instituicao.exporta_csv": "P-78",
    # P-78: consumido so pelo teste do P-15 -- ponto cego declarado da guarda.
    "ambiente.py:PACOTE_PARA_IMPORT": "P-78",
}


def test_nenhum_campo_morto_fora_do_inventario():
    """Falhava contra o codigo de 10/09 com `Aporte.status_do_variavel` e
    `tese.DIFERIDOS_K`, os dois da auditoria que esta guarda enxerga."""
    novos = sorted(set(cm.mortos()) - set(INVENTARIO))
    assert not novos, ("declarado e nunca referenciado em codigo de producao, e fora do "
                       "inventario. Remova, use, ou inventarie com pendencia: "
                       + ", ".join(novos))


def test_o_inventario_nao_apodrece():
    obsoletos = sorted(set(INVENTARIO) - set(cm.mortos()))
    assert not obsoletos, ("inventariado que ja nao esta morto (passou a ser lido ou saiu "
                           "do codigo). Apague estas linhas: " + ", ".join(obsoletos))
    for rot, pend in INVENTARIO.items():
        assert re.fullmatch(r"P-\d+", pend), f"{rot}: sem numero de pendencia"


def test_a_guarda_declara_os_proprios_pontos_cegos():
    """Um mapa que finge completude e pior que nao ter mapa (impacto.py)."""
    doc = cm.__doc__
    for termo in ("NAO ENXERGA", "getattr", "por NOME", "ESCRITO e nunca LIDO",
                  "reflexao", "SO em teste"):
        assert termo in doc, f"ponto cego nao declarado: {termo!r}"


# ── a guarda contra codigo sintetico: o que ela ve e o que ela nao pode ver ──────
def _projeto(tmp_path, arquivos):
    for nome, src in arquivos.items():
        (tmp_path / nome).write_text(textwrap.dedent(src), encoding="utf-8")
    return str(tmp_path)


def test_acha_campo_e_constante_mortos(tmp_path):
    raiz = _projeto(tmp_path, {"m.py": """
        from dataclasses import dataclass
        LIMITE = 3
        ORFA = 4
        @dataclass
        class X:
            lido: int
            morto: int = 0
        def f(x):
            return x.lido + LIMITE
        """})
    assert cm.mortos(raiz) == ["m.py:ORFA", "m.py:X.morto"]


def test_keyword_e_chave_de_dict_contam_como_referencia(tmp_path):
    """Os dois jeitos que o motor tem de escrever um campo sem `obj.campo`."""
    raiz = _projeto(tmp_path, {"m.py": """
        from dataclasses import dataclass
        @dataclass
        class Y:
            a: int
            b: int = 0
        def cria():
            return Y(a=1)
        def troca(y):
            return Y(**{**y.__dict__, "b": 2})
        """})
    assert cm.mortos(raiz) == []


def test_so_codigo_de_producao_conta(tmp_path):
    """Uso em teste, em comentario ou em docstring nao salva um campo; variavel do
    bloco `__main__` nao e constante do sistema."""
    raiz = _projeto(tmp_path, {
        "m.py": '''
            from dataclasses import dataclass
            @dataclass
            class Z:
                so_no_teste: int
                so_citado: int  # so_citado aparece aqui
            def f():
                """so_citado tambem aqui"""
            if __name__ == "__main__":
                VARIAVEL_DE_SCRIPT = 1
            ''',
        "test_m.py": """
            from m import Z
            def test_z():
                assert Z(1, 2).so_no_teste == 1
            """})
    assert cm.mortos(raiz) == ["m.py:Z.so_citado", "m.py:Z.so_no_teste"]

# -*- coding: utf-8 -*-
"""P-141: o memo de sessao do acervo. Tres promessas, e cada uma tem um teste que falha
se ela for quebrada: calcula UMA vez por conteudo, RECALCULA quando o byte muda (a chave
e o sha256, nao o caminho -- S-02), e cada chamada recebe uma COPIA (P-38)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import memo_acervo as MA  # noqa: E402


def _acervo(pasta, conteudo=b"PK-2023"):
    (pasta / "COTAHIST_A2023.ZIP").write_bytes(conteudo)
    (pasta / "LEIA.md").write_bytes(b"fora da regra de descoberta")
    return str(pasta)


def test_mesmo_conteudo_calcula_uma_vez(tmp_path):
    memo, chamadas = MA.novo_memo(), []
    pasta = _acervo(tmp_path)
    for _ in range(3):
        assert memo("r", pasta, lambda: chamadas.append(1) or {"n": 1}) == {"n": 1}
    assert len(chamadas) == 1


def test_byte_mudou_RECALCULA_mesmo_com_o_mesmo_caminho(tmp_path):
    """A mutacao do S-02: uma chave por caminho devolveria o valor velho aqui."""
    memo = MA.novo_memo()
    pasta = _acervo(tmp_path)
    assert memo("r", pasta, lambda: "velho") == "velho"
    _acervo(tmp_path, b"PK-2023-reapresentado")
    assert memo("r", pasta, lambda: "novo") == "novo"
    assert len(memo.guardado) == 2


def test_rotulos_diferentes_nao_se_confundem(tmp_path):
    memo = MA.novo_memo()
    pasta = _acervo(tmp_path)
    assert memo("moeda", pasta, lambda: 1) == 1
    assert memo("pregoes", pasta, lambda: 2) == 2


def test_a_impressao_segue_a_REGRA_DE_DESCOBERTA_do_calendario(tmp_path):
    """Arquivo que `calendario.arquivos()` ignora nao muda a chave; COTAHIST muda."""
    pasta = _acervo(tmp_path)
    antes = MA.impressao_do_acervo(pasta)
    (tmp_path / "LEIA.md").write_bytes(b"editado")
    assert MA.impressao_do_acervo(pasta) == antes
    (tmp_path / "COTAHIST_A2024.ZIP").write_bytes(b"PK-2024")
    assert MA.impressao_do_acervo(pasta) != antes


def test_cada_chamada_recebe_COPIA_e_a_sujeira_nao_atravessa(tmp_path):
    memo = MA.novo_memo()
    pasta = _acervo(tmp_path)
    primeiro = memo("r", pasta, lambda: {"linhas": [1, 2]})
    primeiro["linhas"].append(99)
    assert memo("r", pasta, lambda: None) == {"linhas": [1, 2]}


def test_todo_teste_que_usa_o_memo_tem_xdist_group():
    """Sem o grupo, `--dist loadgroup` separa o par em dois processos e a leitura dupla
    volta -- sem erro, so com a suite 100 s mais lenta. Guarda estatica: todo teste de
    `fase0/` que pede `memo_do_acervo` carrega `xdist_group` nas linhas de decorador."""
    import re
    aqui = os.path.dirname(os.path.abspath(__file__))
    sem_grupo = []
    for nome in sorted(os.listdir(aqui)):
        if not (nome.startswith("test_") and nome.endswith(".py")):
            continue
        with open(os.path.join(aqui, nome), encoding="utf-8") as f:
            linhas = f.read().split("\n")
        for i, ln in enumerate(linhas):
            if re.match(r"def test_\w+\(.*\bmemo_do_acervo\b", ln):
                j = i - 1
                decor = []
                while j >= 0 and (linhas[j].startswith("@") or linhas[j].startswith(" ")):
                    decor.append(linhas[j]); j -= 1
                if not any("xdist_group" in d for d in decor):
                    sem_grupo.append(f"{nome}:{i + 1}")
    assert not sem_grupo, sem_grupo


def test_todo_modulo_com_fixture_de_modulo_tem_xdist_group_no_modulo():
    """A mesma armadilha nas fixtures `scope="module"` (`med`, `jan`, `real`): 46 a 62 s
    cada, refeitos em cada trabalhador que recebesse um teste do modulo."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    sem_grupo = []
    for nome in sorted(os.listdir(aqui)):
        if not (nome.startswith("test_") and nome.endswith(".py")):
            continue
        with open(os.path.join(aqui, nome), encoding="utf-8") as f:
            texto = f.read()
        # agulha montada: escrita inteira, este proprio arquivo casaria com ela
        if "@pytest.fixture(" + 'scope="module")' in texto and \
                "\npytestmark = pytest.mark." + "xdist_group(" not in texto:
            sem_grupo.append(nome)
    assert not sem_grupo, sem_grupo

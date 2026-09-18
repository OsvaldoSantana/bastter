# -*- coding: utf-8 -*-
"""Testes do manifesto da CVM. Sem rede e sem os 700 MB do acervo: ZIPs sinteticos.

O teste que da nome ao arquivo e `test_REORDENADO_nao_e_REAPRESENTADO` -- ele reproduz,
em miniatura, o que foi medido no `dfp_cia_aberta_2024.zip` de 04/09 contra o de 18/09.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import csv
import zipfile
import manifesto_cvm as M

CAB = b"CNPJ;DT_REFER;CONTA;VALOR"
LINHAS = [b"00.000.000/0001-01;2024-12-31;1;100",
          b"11.111.111/0001-11;2024-12-31;1;200",
          b"22.222.222/0001-22;2024-12-31;1;300"]


def _zip(caminho, membros):
    with zipfile.ZipFile(caminho, "w") as z:
        for nome, linhas in membros.items():
            z.writestr(nome, b"\n".join([CAB] + linhas))
    return str(caminho)


def test_IDENTICO_quando_o_byte_e_o_mesmo(tmp_path):
    a = _zip(tmp_path/"a.zip", {"x.csv": LINHAS})
    b = _zip(tmp_path/"b.zip", {"x.csv": LINHAS})
    assert M.comparar(a, b)[0] == "IDENTICO"


def test_REORDENADO_nao_e_REAPRESENTADO(tmp_path):
    """O achado de 18/09/2026, em miniatura.

    O `dfp_cia_aberta_2024.zip` mudou de sha256 em 14 dias e o dado era o mesmo: 8
    linhas fora de posicao em 94.517, `sorted(a) == sorted(b)`. Comparar por hash de
    arquivo teria declarado uma reapresentacao que nao houve, e a estrategia de snapshot
    do CLAUDE.md §11.6 commitaria ruido no git toda semana.

    Mutacao: troque a normalizacao por `da == db` e este teste passa a dizer
    REAPRESENTADO -- que e exatamente o falso positivo que ele existe para impedir."""
    a = _zip(tmp_path/"a.zip", {"x.csv": LINHAS})
    b = _zip(tmp_path/"b.zip", {"x.csv": [LINHAS[1], LINHAS[0], LINHAS[2]]})
    v, d = M.comparar(a, b)
    assert v == "REORDENADO", d
    assert d["x.csv"]["tipo"] == "REORDENADO" and d["x.csv"]["fora_de_posicao"] == 2


def test_REAPRESENTADO_quando_uma_LINHA_muda(tmp_path):
    """O evento que o projeto quer capturar, e o unico. Um valor corrigido dentro do
    mesmo arquivo, sob o mesmo nome -- e o que destroi o que a empresa dizia na epoca."""
    a = _zip(tmp_path/"a.zip", {"x.csv": LINHAS})
    corrigida = LINHAS[:2] + [b"22.222.222/0001-22;2024-12-31;1;999"]
    b = _zip(tmp_path/"b.zip", {"x.csv": corrigida})
    v, d = M.comparar(a, b)
    assert v == "REAPRESENTADO"
    assert d["x.csv"]["saiu"] == 1 and d["x.csv"]["entrou"] == 1
    assert "999" in d["x.csv"]["exemplo_entrou"][0]


def test_REAPRESENTADO_vence_REORDENADO_quando_os_dois_acontecem(tmp_path):
    """Um arquivo reordenado e outro reapresentado no mesmo ZIP: o veredito do conjunto
    tem de ser o mais grave. Colapsar para REORDENADO esconderia a correcao."""
    a = _zip(tmp_path/"a.zip", {"x.csv": LINHAS, "y.csv": LINHAS})
    b = _zip(tmp_path/"b.zip", {"x.csv": [LINHAS[2]] + LINHAS[:2],
                                "y.csv": LINHAS[:2] + [b"9;2024-12-31;1;1"]})
    assert M.comparar(a, b)[0] == "REAPRESENTADO"


def test_ESTRUTURA_quando_os_membros_mudam(tmp_path):
    a = _zip(tmp_path/"a.zip", {"x.csv": LINHAS})
    b = _zip(tmp_path/"b.zip", {"x.csv": LINHAS, "z.csv": LINHAS})
    v, d = M.comparar(a, b)
    assert v == "ESTRUTURA" and d["so_em_b"] == ["z.csv"]


def test_o_manifesto_grava_hash_tamanho_e_data(tmp_path):
    _zip(tmp_path/"dfp_2024.zip", {"x.csv": LINHAS})
    _zip(tmp_path/"itr_2024.zip", {"y.csv": LINHAS})
    linhas = M.manifesto(str(tmp_path))
    assert [x["caminho"] for x in linhas] == ["dfp_2024.zip", "itr_2024.zip"]
    for x in linhas:
        assert len(x["sha256"]) == 64 and x["bytes"] > 0 and x["dt_captura"]
    d = M.gravar(linhas, str(tmp_path/"m"/"m.csv"))
    with open(d, encoding="utf-8") as f:
        lidas = list(csv.DictReader(f, delimiter=";"))
    assert len(lidas) == 2 and lidas[0]["sha256"] == linhas[0]["sha256"]


def test_a_ordem_do_manifesto_e_ESTAVEL(tmp_path):
    """P-85: um relatorio que muda de texto entre execucoes deixa de servir como
    instantaneo dourado. A licao veio do `refinar.py`, nao atravessou para o
    `corretoras.py`, e nao vai deixar de atravessar para ca."""
    for n in ("c.zip", "a.zip", "b.zip"):
        _zip(tmp_path/n, {"x.csv": LINHAS})
    assert [x["caminho"] for x in M.manifesto(str(tmp_path))] == ["a.zip", "b.zip", "c.zip"]


def test_acervo_vazio_NAO_e_nada_mudou(tmp_path, capsys):
    """A armadilha escrita no CLAUDE.md §11.6: *um download que devolve 404 mais um unzip
    vazio produzem 'nenhuma mudanca', indistinguivel de 'a CVM nao mudou nada'.* Ausencia
    de mudanca precisa ser afirmada, nunca inferida da ausencia de erro."""
    assert M.main(["--manifesto", str(tmp_path)]) == 1
    assert "nao ha acervo" in capsys.readouterr().err


def test_o_codigo_de_saida_separa_o_evento_do_ruido(tmp_path):
    """Quem chamar isto de uma rotina automatica decide pelo codigo de saida, e ele tem
    de distinguir 'a CVM corrigiu um numero' de 'a CVM regerou o arquivo'."""
    a = _zip(tmp_path/"a.zip", {"x.csv": LINHAS})
    b = _zip(tmp_path/"b.zip", {"x.csv": [LINHAS[1], LINHAS[0], LINHAS[2]]})
    c = _zip(tmp_path/"c.zip", {"x.csv": LINHAS[:2] + [b"9;2024-12-31;1;1"]})
    assert M.main(["--comparar", a, b]) == 0
    assert M.main(["--comparar", a, c]) == 2


def test_sha256_le_em_blocos_e_bate_com_a_leitura_inteira(tmp_path):
    import hashlib
    p = tmp_path/"g.bin"
    p.write_bytes(os.urandom(3_000_000))
    assert M.sha256(str(p), bloco=4096) == hashlib.sha256(p.read_bytes()).hexdigest()


def test_o_manifesto_NAO_pode_ser_gravado_dentro_de_data(tmp_path):
    """O defeito de 18/09, virado guarda. A primeira versao gravava em
    `data/bronze/cvm/manifesto/`, o documento afirmava que o manifesto entrava no
    repositorio, e o `.gitignore` ignora `data/` desde sempre: o arquivo existiu, o
    commit passou, e a procedencia nao chegou a ninguem.

    Mutacao: tire a guarda de `gravar` e este teste reprova."""
    import pytest
    alvo = tmp_path/"data"/"bronze"/"cvm"/"manifesto"/"m.csv"
    with pytest.raises(ValueError, match="gitignore"):
        M.gravar([{c: "x" for c in M.COLUNAS}], str(alvo))
    assert not alvo.exists()


def test_o_destino_padrao_fica_FORA_do_acervo_e_dentro_do_repositorio(tmp_path):
    """`docs/acervo/<nome>/` na raiz do repositorio, achada pelo `pyproject.toml`."""
    (tmp_path/"pyproject.toml").write_text("[project]\n", encoding="utf-8")
    acervo = tmp_path/"data"/"bronze"/"cvm"
    acervo.mkdir(parents=True)
    d = M.destino_padrao(str(acervo), "2026-09-18")
    assert d.replace("\\", "/").endswith("docs/acervo/cvm/dt_captura=2026-09-18.csv")
    assert "/data/" not in d.replace("\\", "/")
    assert M.raiz_do_repositorio(str(acervo)) == str(tmp_path)


def test_sem_pyproject_o_destino_cai_no_acervo_e_a_guarda_RECUSA(tmp_path):
    """Sem raiz de repositorio nao ha onde gravar procedencia, e a resposta certa e
    parar. Cair de volta para dentro do acervo seria o F-02: insumo ausente virando um
    caminho qualquer, e o arquivo sumindo do git em silencio."""
    import pytest
    acervo = tmp_path/"data"/"cvm"; acervo.mkdir(parents=True)
    with pytest.raises(ValueError, match="gitignore"):
        M.gravar([{c: "x" for c in M.COLUNAS}], M.destino_padrao(str(acervo), "2026-09-18"))


def _linha(**kw):
    return {**{c: "x" for c in M.COLUNAS}, **kw}


def test_gravar_DUAS_VEZES_sem_mudanca_nao_cria_arquivo_novo(tmp_path):
    """Idempotencia pela regua §5-B: a unica forma de testar e RODAR DUAS VEZES."""
    d = str(tmp_path/"m.csv")
    M.gravar([_linha(caminho="a.zip")], d)
    M.gravar([_linha(caminho="a.zip")], d)
    assert [p.name for p in tmp_path.iterdir()] == ["m.csv"]


def test_manifesto_DIFERENTE_no_mesmo_dia_PRESERVA_o_retrato_anterior(tmp_path, capsys):
    """O caso real de 18/09: o manifesto da B3 foi gravado com UM arquivo, e os outros
    quatro anos seriam baixados no mesmo dia. O nome e por DIA, entao a segunda gravacao
    apagaria a primeira -- e a apagada seria a prova de que, aquela hora, so havia 2023.

    O manifesto existe porque a CVM sobrescreve arquivo sob o mesmo nome. Ele estava
    fazendo o mesmo consigo.

    Mutacao: tire o `os.replace` de `gravar` e este teste reprova."""
    d = str(tmp_path/"m.csv")
    M.gravar([_linha(caminho="2023.zip")], d)
    M.gravar([_linha(caminho="2023.zip"), _linha(caminho="2024.zip")], d)
    nomes = sorted(p.name for p in tmp_path.iterdir())
    assert len(nomes) == 2 and "m.csv" in nomes
    preservado = [n for n in nomes if n != "m.csv"][0]
    assert "2024.zip" not in (tmp_path/preservado).read_text(encoding="utf-8"), \
        "o preservado tem de ser o ANTIGO, nao o novo"
    assert "2024.zip" in (tmp_path/"m.csv").read_text(encoding="utf-8")
    assert "PRESERVADO" in capsys.readouterr().err

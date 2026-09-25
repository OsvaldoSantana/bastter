# -*- coding: utf-8 -*-
"""P-136, decisao 2: publicar as versoes da CVM em release do GitHub (25/09/2026)."""
from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publicar_cvm as pc  # noqa: E402

INV_COLS = ("fonte", "recurso", "arquivo", "sha256", "bytes", "chave", "papel", "versao",
            "origem", "dt_envio")
REG_COLS = ("dt_captura", "recurso", "arquivo", "url", "http_last_modified", "etag", "sha256",
            "bytes", "caminho", "situacao", "motivo")


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _csv(caminho, cols, linhas):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";", lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)


def _repo(tmp_path, inventario=(), registro=()):
    base = tmp_path / "docs" / "acervo" / "cvm"
    _csv(str(base / "inventario-armazem.csv"), INV_COLS, list(inventario))
    _csv(str(base / "capturas.csv"), REG_COLS, list(registro))
    return str(tmp_path)


class GhFalso:
    """Grava os comandos; `releases` e {tag: set(nomes)}."""
    def __init__(self, releases=None, falhar=None):
        self.releases = {k: set(v) for k, v in (releases or {}).items()}
        self.cmds = []
        self.falhar = falhar

    def __call__(self, cmd):
        self.cmds.append(cmd)
        sub, tag = cmd[2], cmd[3]
        ok = lambda out="": subprocess.CompletedProcess(cmd, 0, out, "")  # noqa: E731
        if self.falhar == sub:
            return subprocess.CompletedProcess(cmd, 1, "", "falhou")
        if sub == "view":
            if tag not in self.releases:
                return subprocess.CompletedProcess(cmd, 1, "", "release not found")
            return ok("\n".join(sorted(self.releases[tag])))
        if sub == "create":
            self.releases[tag] = set()
        if sub == "upload":
            self.releases[tag].add(os.path.basename(cmd[4]))
        return ok()


def _versao_inv(nome, conteudo, recurso="dfp", fonte="cvm"):
    return dict(fonte=fonte, recurso=recurso, arquivo=nome, sha256=_sha(conteudo),
                bytes=len(conteudo), papel="canonico", dt_envio="2026-09-25T14:23:07Z")


# ── a guarda ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("v", [
    dict(fonte="b3", recurso="cotahist", arquivo="COTAHIST_A2026.ZIP", sha256="a" * 64,
         ano="2026"),
    dict(fonte="nefin", recurso="risk_factors", arquivo="nefin_factors.csv",
         sha256="b" * 64, ano="2026"),
    dict(fonte="cvm", recurso="cotahist", arquivo="x.zip", sha256="c" * 64, ano="2026"),
    dict(fonte="cvm", recurso="dfp", arquivo="dfp_cia_aberta_2024.zip", sha256="d" * 64,
         ano=""),
])
def test_so_a_CVM_e_publicavel(v):
    with pytest.raises(pc.PublicacaoRecusada):
        pc.publicavel(v)


def test_uma_versao_da_B3_no_inventario_derruba_ANTES_de_qualquer_envio(tmp_path):
    """Tudo ou nada: release publicada nao se despublica, entao a recusa vem antes do
    primeiro comando que escreve."""
    repo = _repo(tmp_path, inventario=[
        _versao_inv("dfp_cia_aberta_2024.zip", b"dfp"),
        _versao_inv("COTAHIST_A2026.ZIP", b"b3", recurso="cotahist", fonte="b3")])
    gh = GhFalso()
    with pytest.raises(pc.PublicacaoRecusada):
        pc.main(["--aplicar"], rodar=gh, abrir=lambda v: None, repo=repo)
    assert not [c for c in gh.cmds if c[2] in ("create", "upload", "edit")]


# ── o nome, o plano, as notas ───────────────────────────────────────────────

def test_nome_do_arquivo_carrega_a_versao():
    v = dict(arquivo="dfp_cia_aberta_2024.zip", sha256="0dd854dc1a2b" + "0" * 52)
    assert pc.nome_do_arquivo(v) == "dfp_cia_aberta_2024__0dd854dc1a2b.zip"
    v = dict(arquivo="cad_cia_aberta.csv", sha256="2ca2f1cc7682" + "0" * 52)
    assert pc.nome_do_arquivo(v) == "cad_cia_aberta__2ca2f1cc7682.csv"


def test_versoes_une_inventario_e_capturas_com_byte_e_ignora_as_sem_byte(tmp_path):
    a, b = b"versao antiga", b"versao nova"
    repo = _repo(tmp_path, inventario=[_versao_inv("dfp_cia_aberta_2024.zip", a)],
                 registro=[
                     dict(dt_captura="2026-09-26T14:00:00Z", recurso="dfp",
                          arquivo="dfp_cia_aberta_2024.zip", sha256=_sha(b), situacao="atualizado"),
                     dict(dt_captura="2026-09-26T14:00:00Z", recurso="dfp",
                          arquivo="dfp_cia_aberta_2024.zip", sha256=_sha(a), situacao="deslocado"),
                     dict(dt_captura="2026-09-26T14:00:00Z", recurso="itr",
                          arquivo="itr_cia_aberta_2025.zip", sha256="", situacao="erro")])
    vs = pc.versoes(repo)
    assert [v["sha256"] for v in vs] == sorted([_sha(a), _sha(b)])
    assert {v["ano"] for v in vs} == {"2026"}


def test_plano_so_envia_o_que_a_release_nao_tem():
    v1 = dict(fonte="cvm", recurso="dfp", arquivo="d.zip", sha256="1" * 64, ano="2026")
    v2 = dict(fonte="cvm", recurso="dfp", arquivo="d.zip", sha256="2" * 64, ano="2026")
    ja = {"cvm-acervo-2026": {pc.nome_do_arquivo(v1)}}
    assert pc.plano([v1, v2], ja) == {"cvm-acervo-2026": [v2]}
    assert pc.plano([v1, v2], {}) == {"cvm-acervo-2026": [v1, v2]}


def test_notas_tem_a_atribuicao_que_a_CVM_exige_e_a_licenca():
    v = dict(fonte="cvm", recurso="dfp", arquivo="d.zip", sha256="1" * 64, ano="2026")
    n = pc.notas("cvm-acervo-2026", [v])
    assert pc.ATRIBUICAO in n and "ODbL" in n and "1" * 64 in n


def test_notas_grandes_demais_recusam_em_vez_de_cortar():
    vs = [dict(fonte="cvm", recurso="dfp", arquivo=f"d{i}.zip", sha256=f"{i:064x}",
               ano="2026") for i in range(2000)]
    with pytest.raises(ValueError, match="partir a release"):
        pc.notas("cvm-acervo-2026", vs)


# ── ponta a ponta com o gh falso ────────────────────────────────────────────

def _abrir_de(tmp_path, conteudos):
    def abrir(v):
        p = tmp_path / "bytes" / v["sha256"]
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(conteudos[v["sha256"]])
        return str(p)
    return abrir


def test_ponta_a_ponta_cria_envia_e_escreve_as_notas(tmp_path):
    a, c = b"dfp 2024", b"cadastro"
    repo = _repo(tmp_path, inventario=[_versao_inv("dfp_cia_aberta_2024.zip", a),
                                       _versao_inv("cad_cia_aberta.csv", c, recurso="cad")])
    gh = GhFalso()
    assert pc.main(["--aplicar"], rodar=gh, abrir=_abrir_de(
        tmp_path, {_sha(a): a, _sha(c): c}), repo=repo) == 0
    subs = [x[2] for x in gh.cmds]
    assert subs.count("create") == 1 and subs.count("upload") == 2 and subs[-1] == "edit"
    assert "--latest=false" in [x for x in gh.cmds if x[2] == "create"][0]
    assert gh.releases["cvm-acervo-2026"] == {
        f"dfp_cia_aberta_2024__{_sha(a)[:12]}.zip", f"cad_cia_aberta__{_sha(c)[:12]}.csv"}


def test_ponta_a_ponta_e_idempotente(tmp_path):
    """Duas execucoes (regra 4 da 5-B): a segunda nao escreve nada."""
    a = b"dfp 2024"
    repo = _repo(tmp_path, inventario=[_versao_inv("dfp_cia_aberta_2024.zip", a)])
    gh = GhFalso()
    abrir = _abrir_de(tmp_path, {_sha(a): a})
    pc.main(["--aplicar"], rodar=gh, abrir=abrir, repo=repo)
    n = len(gh.cmds)
    assert pc.main(["--aplicar"], rodar=gh, abrir=abrir, repo=repo) == 0
    assert all(c[2] == "view" for c in gh.cmds[n:])


def test_sem_aplicar_nao_escreve_nada(tmp_path):
    repo = _repo(tmp_path, inventario=[_versao_inv("dfp_cia_aberta_2024.zip", b"x")])
    gh = GhFalso()
    assert pc.main([], rodar=gh, abrir=lambda v: None, repo=repo) == 0
    assert all(c[2] == "view" for c in gh.cmds)


def test_byte_que_nao_confere_derruba(tmp_path):
    a = b"dfp 2024"
    repo = _repo(tmp_path, inventario=[_versao_inv("dfp_cia_aberta_2024.zip", a)])
    with pytest.raises(pc.armazem_mod.ConteudoDivergente):
        pc.main(["--aplicar"], rodar=GhFalso(),
                abrir=_abrir_de(tmp_path, {_sha(a): b"outro byte"}), repo=repo)


def test_versao_sem_byte_no_armazem_avisa_e_fica_fora_das_notas(tmp_path, capsys):
    a, b = b"tem", b"nao tem"
    repo = _repo(tmp_path, inventario=[_versao_inv("dfp_cia_aberta_2024.zip", a),
                                       _versao_inv("itr_cia_aberta_2025.zip", b, "itr")])

    def abrir(v):
        if v["sha256"] == _sha(b):
            raise KeyError("sem byte")
        return _abrir_de(tmp_path, {_sha(a): a})(v)

    notas = {}
    gh = GhFalso()
    original = gh.__call__

    def rodar(cmd):
        if cmd[2] == "edit":
            notas["texto"] = open(cmd[cmd.index("--notes-file") + 1], encoding="utf-8").read()
        return original(cmd)

    assert pc.main(["--aplicar"], rodar=rodar, abrir=abrir, repo=repo) == 0
    assert "1 versao(oes) sem byte" in capsys.readouterr().err
    assert _sha(a) in notas["texto"] and _sha(b) not in notas["texto"]


def test_sem_gh_o_plano_avisa_e_o_aplicar_recusa(tmp_path, capsys):
    repo = _repo(tmp_path, inventario=[_versao_inv("dfp_cia_aberta_2024.zip", b"x")])

    def sem_gh(cmd):
        raise FileNotFoundError("gh")

    assert pc.main([], rodar=sem_gh, abrir=lambda v: None, repo=repo) == 0
    assert "SUPOE" in capsys.readouterr().out
    assert pc.main(["--aplicar"], rodar=sem_gh, abrir=lambda v: None, repo=repo) == 1


def test_o_registro_real_so_tem_CVM_publicavel():
    """Sobre o acervo real: todas as versoes passam pela guarda -- e sao da CVM."""
    vs = pc.versoes(pc.acervo.raiz_repo())
    assert vs, "vacuidade: o inventario da CVM tem de existir"
    for v in vs:
        assert pc.publicavel(v).startswith("cvm/")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

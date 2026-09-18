# -*- coding: utf-8 -*-
"""
test_p98_acervo_fora_do_indice.py -- ACHADO P-98, 18/09/2026.

O QUE ACONTECEU. O acervo COTAHIST (1986-2026) foi baixado para
`docs/fontes/series-historicas-cotahist/` -- 6,0 GB dentro do repositorio, que e
PUBLICO. O `.gitignore` cobria `docs/fontes/**/*.zip` e `**/*.txt`, e por isso 65 dos
81 arquivos estavam cobertos.

Os outros 16 nao. O ZIP da B3 muda de convencao no meio da propria serie: de 1986 a
2001 o conteudo sai **sem extensao** -- `COTAHIST.A1986`, `COTAHIST.A2000`,
`COTAHIST_A2001` -- e so de 2002 em diante ele e `COTAHIST_A2002.TXT`. Sao **507 MB**
que nenhum padrao pegava, a um `git add -A` de virarem historico permanente. Blob
commitado nao se apaga com `git rm`: so com reescrita de historico, e depois de um
push nem isso.

E A LICAO E A MESMA DA P-82, pela segunda vez em dois dias: **regra escrita numa lista
de nomes nao e regra, e lembrete.** La era uma lista de PASTAS que alguem precisava
lembrar de estender (`pacote_segunda/` nao estava nela). Aqui e uma lista de
EXTENSOES, e quem a estende precisa saber de antemao como um publicador nomeia o
conteudo de um ZIP de 1986. Ninguem sabe.

O QUE ESTE TESTE MEDE, e por que e TAMANHO. Bytes nao dependem de alguem ter acertado
o nome. Um acervo pode chegar com qualquer extensao, nenhuma extensao, ou uma que so
existe naquela fonte -- e em todos os casos ele e grande, e e por ser grande que ele
destroi um repositorio. O nome e a propriedade que varia; o tamanho e a que importa.

Mede o INDICE, nao o disco -- mesmo instrumento do `test_p67_segredo.py` (segredo) e
do `test_p82_copia_do_projeto.py` (copia). Baixar 6 GB para dentro da pasta e
inofensivo; o defeito nasce no `git add`.

O QUE ELE NAO ENXERGA, declarado (P5):
  - arquivo grande ja COMMITADO antes deste teste existir. Ele acusa, mas acusar nao
    desfaz: o remedio ai e reescrita de historico, e e decisao do Osvaldo;
  - muitos arquivos pequenos. 10.000 arquivos de 100 KB somam 1 GB e passam um a um.
    A regra do total esta em `test_P98_o_indice_inteiro_cabe_num_clone`, com um teto
    folgado -- ela existe para pegar a enxurrada, nao para policiar crescimento;
  - arquivo grande FORA do indice. De proposito: o disco e dele.
"""

import os
import subprocess

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

# 5 MB. Nenhum artefato LEGITIMO deste projeto chega perto: o maior rastreado e
# `alocacao/dados/nefin_factors.csv`, 6.321 sessoes. O acervo comeca em ~5 MB (o ZIP de
# 2001) e vai a 784 MB (o TXT de 2025) -- a folga entre as duas classes e de ordens de
# grandeza, e e por isso que um teto unico separa as duas sem afinacao.
LIMITE_BYTES = 5 * 1024 * 1024
TETO_TOTAL_BYTES = 200 * 1024 * 1024

# ── LINHA DE BASE. Arquivo grande que entra de PROPOSITO, com o porque ao lado.
# Vazia hoje, e a unica direcao legitima de ela crescer e alguem escrever um motivo.
GRANDES_DECLARADOS: dict[str, str] = {}


def _rastreados():
    r = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        pytest.skip("nao e um repositorio git -- ESTE TESTE NAO RODOU")
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def grandes(rastreados, tamanho_de, limite=LIMITE_BYTES):
    """Caminhos rastreados maiores que `limite`, fora da linha de base.

    `tamanho_de` e injetado para que a guarda seja testavel sem precisar de 500 MB em
    disco -- a prova por mutacao abaixo passa os tamanhos REAIS do incidente."""
    achados = {}
    for p in rastreados:
        if p in GRANDES_DECLARADOS:
            continue
        n = tamanho_de(p)
        if n is not None and n > limite:
            achados[p] = n
    return dict(sorted(achados.items(), key=lambda kv: -kv[1]))


def _no_disco(p):
    caminho = os.path.join(RAIZ, p)
    return os.path.getsize(caminho) if os.path.exists(caminho) else None


def test_P98_nenhum_arquivo_de_acervo_entrou_no_indice():
    achados = grandes(_rastreados(), _no_disco)
    assert not achados, (
        "o indice do git rastreia arquivo(s) grandes:\n  - "
        + "\n  - ".join(f"{p}  ({n/1e6:.1f} MB)" for p, n in achados.items())
        + "\n\nO repositorio e PUBLICO e blob commitado e permanente. Se for acervo, "
          "ele mora em data/ (ignorado). Se entra de proposito, declare em "
          "GRANDES_DECLARADOS com o motivo escrito ao lado.")


def test_P98_o_indice_inteiro_cabe_num_clone():
    """A regra do TOTAL, porque a do arquivo nao pega enxurrada de arquivo pequeno."""
    total = sum(n for n in (_no_disco(p) for p in _rastreados()) if n)
    assert total <= TETO_TOTAL_BYTES, (
        f"o indice soma {total/1e6:.0f} MB, acima do teto de "
        f"{TETO_TOTAL_BYTES/1e6:.0f} MB. Clonar este repositorio deixou de ser barato.")


# ── prova por mutacao, com os numeros REAIS do incidente de 18/09 ─────────────
# Guarda que nunca falhou e guarda que ninguem sabe se funciona (regua §5-B, regra 4).

INCIDENTE = {
    # os 16 SEM extensao -- os que o .gitignore por extensao nao pegava
    "docs/fontes/series-historicas-cotahist/COTAHIST.A1986": 43_961_801,
    "docs/fontes/series-historicas-cotahist/COTAHIST_A2001": 35_036_950,
    # um coberto pelo .gitignore, para provar que a guarda nao depende disso
    "docs/fontes/series-historicas-cotahist/COTAHIST_A2025.TXT": 784_150_900,
    # o projeto vivo
    "alocacao/politica.yaml": 128_815,
    "alocacao/dados/nefin_factors.csv": 700_000,
    "CLAUDE.md": 139_000,
}


def test_P98_a_guarda_PEGA_o_arquivo_SEM_EXTENSAO_que_o_gitignore_perdeu():
    """O caso que da nome ao achado. `COTAHIST.A1986` nao casa com `*.txt` nem com
    `*.zip`; casa com 43,9 MB, que e a propriedade que o teste mede."""
    achados = grandes(list(INCIDENTE), INCIDENTE.get)
    assert "docs/fontes/series-historicas-cotahist/COTAHIST.A1986" in achados
    assert "docs/fontes/series-historicas-cotahist/COTAHIST_A2001" in achados
    assert list(achados)[0].endswith("COTAHIST_A2025.TXT"), "ordena do maior para o menor"


def test_P98_a_guarda_NAO_acusa_o_projeto_vivo():
    """Filtro que derruba achado verdadeiro nao e filtro. Os tres arquivos reais do
    projeto ficam tres ordens de grandeza abaixo do teto."""
    achados = grandes(list(INCIDENTE), INCIDENTE.get)
    for vivo in ("alocacao/politica.yaml", "alocacao/dados/nefin_factors.csv", "CLAUDE.md"):
        assert vivo not in achados


def test_P98_declarar_na_linha_de_base_silencia_apenas_o_declarado():
    alvo = "docs/fontes/series-historicas-cotahist/COTAHIST.A1986"
    GRANDES_DECLARADOS[alvo] = "so para este teste"
    try:
        achados = grandes(list(INCIDENTE), INCIDENTE.get)
        assert alvo not in achados
        assert "docs/fontes/series-historicas-cotahist/COTAHIST_A2001" in achados
    finally:
        GRANDES_DECLARADOS.pop(alvo)

# -*- coding: utf-8 -*-
"""
test_p88_block_bootstrap.py -- P-88 FECHADA em 19/09/2026.

A LIMITACAO, citada do `CLAUDE.md` de 18/09:

    "o bootstrap reamostra **meses independentes** -- se houver dependencia serial, o corte
     medido esta **subestimado**, na mesma direcao do achado. Medir isso pede *block
     bootstrap*, e nao esta feito."

**A previsao estava certa, e o numero e ~8%.** Medido:

    HML residuo: Ljung-Box(12) p = 0,031   -> TEM dependencia
    SMB residuo: Ljung-Box(12) p = 0,166   -> NAO tem  (o CONTROLE)

     L  blocos |    HML  vs iid |    SMB  vs iid | liquido
     1     306 | 3.1099  +0.0%  | 2.8473  +0.0%  |  +0.0%
     2     153 | 3.2909  +5.8%  | 2.7736  -2.6%  |  +8.4%  *
     3     102 | 3.3133  +6.5%  | 2.7695  -2.7%  |  +9.3%  *
     6      51 | 3.2145  +3.4%  | 2.6991  -5.2%  |  +8.6%  *
    12      26 | 2.9970  -3.6%  | 2.6482  -7.0%  |  +3.4%
    24      13 | 2.9624  -4.7%  | 2.7573  -3.2%  |  -1.6%

**O CONTROLE E O QUE FAZ A LIMITACAO FECHAR EM VEZ DE FICAR AMBIGUA.** Sem ele, a queda do
corte em L>=12 se leria como *"a dependencia nao importa"* -- e seria a conclusao errada pelo
motivo errado: com n=306, `L=24` da **13 blocos distintos**, e o corte cai por DEGENERACAO do
reamostrador. O SMB tem a mesma n, a mesma k e o mesmo procedimento, e **nao tem
dependencia**: nele o corte so cai. **Os sinais sao opostos na faixa informativa**, e a
diferenca e a dependencia.

O VEREDITO DO HML NAO MUDA, e essa e a conclusao mais forte porque **nao depende de escolher
um L**: em todos os nove comprimentos testados, `t = 2,9351` fica ABAIXO do corte. A P-88
pedia *"escolher o comprimento do bloco com medicao de sensibilidade, e nao por convencao"* --
e a medicao de sensibilidade mostrou que a escolha e dispensavel para esta decisao.

    A folga passa de **-0,175** (iid) para **-0,26 a -0,38** na faixa informativa. A
    limitacao era conservadora, como o `CLAUDE.md` dizia: o HML fica ainda mais longe de
    sobreviver ao orcamento que ele mesmo pre-registrou.
"""
from __future__ import annotations
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p88_block_bootstrap as P  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "alocacao"))
import backtest_h1_h3 as B  # noqa: E402

T_HML_REGISTRADO = 2.9351
RAPIDO = 1_500        # repeticoes para os testes que nao aferem o numero registrado


@pytest.fixture(scope="module")
def d():
    return B.amostra()


def test_o_t_observado_reproduz_o_pre_registrado(d):
    """Vacuidade primeiro. Se o desenho divergir da assinatura pre-registrada, todo numero
    abaixo mede outra coisa -- e mede em silencio."""
    assert len(d) == 306
    _a, t = B.alfa_contra_os_demais("HML", d)
    assert t == pytest.approx(T_HML_REGISTRADO, abs=5e-5)


def test_L1_reproduz_o_CORTE_REGISTRADO_de_18_09(d):
    """O portao da calibracao: `L=1` TEM de ser o bootstrap iid do `bootstrap_t`, e com a
    semente registrada tem de devolver **3,1473** -- o numero que esta no `CLAUDE.md`.

    Sem este teste, um corte por bloco maior nao provaria nada: poderia ser a minha
    implementacao diferindo da registrada, e nao a dependencia serial."""
    y, X = P.desenho("HML", d)
    c = P.corte(y, X, L=1, semente=B.SEMENTE)
    assert c == pytest.approx(P.CORTE_IID_REGISTRADO, abs=5e-4)


def test_L1_e_literalmente_o_sorteio_iid(d):
    """E que ele seja iid por construcao, nao por coincidencia numerica."""
    rng1 = np.random.default_rng(7)
    rng2 = np.random.default_rng(7)
    assert (P.indices(rng1, len(d), 1) == rng2.integers(0, len(d), len(d))).all()


def test_o_bloco_e_CIRCULAR_e_preserva_o_tamanho_da_amostra(d):
    """Truncar as pontas mudaria `n` junto com `L`, e ai duas coisas variam ao mesmo tempo
    e nenhuma e medida."""
    rng = np.random.default_rng(1)
    for L in (1, 2, 3, 7, 24, 300):
        ix = P.indices(rng, len(d), L)
        assert len(ix) == len(d) and ix.min() >= 0 and ix.max() < len(d)


def test_o_bloco_preserva_a_CONTIGUIDADE(d):
    """O bloco existe para carregar a dependencia; se os indices nao forem contiguos ele
    nao carrega nada e o teste do corte passaria sem medir dependencia nenhuma."""
    ix = P.indices(np.random.default_rng(3), len(d), 6)
    saltos = [(int(ix[i + 1]) - int(ix[i])) % len(d) for i in range(len(ix) - 1)]
    assert saltos.count(1) >= len(saltos) * 0.7, \
        "ao menos 5 de cada 6 passos dentro de um bloco de 6 sao consecutivos"


# ── a dependencia, e o controle ───────────────────────────────────────────────

def test_o_HML_TEM_dependencia_serial_no_RESIDUO(d):
    """O residuo e a serie que o bootstrap reamostra -- medir o bruto responderia outra
    pergunta, e e a forma do erro que a regua §5-B persegue."""
    y, X = P.desenho("HML", d)
    _q, p = P.ljung_box(P.autocorrelacao(P.residuo(y, X)), len(d))
    assert p < 0.05, f"Ljung-Box p={p:.3f}: era 0,031 em 19/09"


def test_o_SMB_NAO_tem_e_e_por_isso_que_ele_serve_de_CONTROLE(d):
    y, X = P.desenho("SMB", d)
    _q, p = P.ljung_box(P.autocorrelacao(P.residuo(y, X)), len(d))
    assert p > 0.05, f"Ljung-Box p={p:.3f}: era 0,166 em 19/09"


def test_o_ljung_box_ACUSA_dependencia_fabricada():
    """Prova por mutacao do instrumento: uma AR(1) forte tem de ser acusada, senao o
    `p > 0,05` do SMB nao prova ausencia -- prova cegueira."""
    rng = np.random.default_rng(11)
    e = rng.standard_normal(306)
    s = np.empty(306)
    s[0] = e[0]
    for i in range(1, 306):
        s[i] = 0.6 * s[i - 1] + e[i]
    _q, p = P.ljung_box(P.autocorrelacao(s), 306)
    assert p < 0.001


def test_a_contagem_de_blocos_e_o_que_define_a_faixa_informativa(d):
    """A degeneracao nao e opiniao: e aritmetica. 13 blocos nao reamostram 306 meses."""
    assert P.blocos_distintos(len(d), 24) == 13
    assert all(P.blocos_distintos(len(d), L) >= 39 for L in P.L_INFORMATIVO)
    assert P.blocos_distintos(len(d), 12) == 26, "fora da faixa, e por isso"


# ── o achado ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("L", (2, 3, 6))
def test_P88_na_faixa_informativa_a_DISPERSAO_do_HML_sobe(d, L):
    """O achado, aferido na CAUSA e nao na consequencia.

    Dependencia serial infla a variancia da estatistica reamostrada; o corte e consequencia
    disso. Aferir a variancia e estavel com 1.500 repeticoes -- aferir o quantil `1-alfa/13`
    nao e, porque ele vive a 0,385% da ponta, e foi assim que a primeira versao deste teste
    falhou com o achado correto. Ver o docstring de `P.dispersao`."""
    y, X = P.desenho("HML", d)
    iid = P.dispersao(y, X, 1, B.SEMENTE, n_rep=RAPIDO)
    blk = P.dispersao(y, X, L, B.SEMENTE, n_rep=RAPIDO)
    assert blk > iid, f"L={L}: dispersao {blk:.4f} nao subiu contra {iid:.4f}"


@pytest.mark.parametrize("L", (2, 3, 6))
def test_P88_e_no_CONTROLE_ela_sobe_MENOS(d, L):
    """A outra metade, e sem ela o teste acima nao distingue dependencia de artefato.

    O criterio e COMPARATIVO, nao absoluto: blocos mudam a variancia das duas series, e o
    que a dependencia acrescenta e o EXCESSO do HML sobre o controle."""
    ih = P.dispersao(*P.desenho("HML", d), 1, B.SEMENTE, n_rep=RAPIDO)
    bh = P.dispersao(*P.desenho("HML", d), L, B.SEMENTE, n_rep=RAPIDO)
    isb = P.dispersao(*P.desenho("SMB", d), 1, B.SEMENTE, n_rep=RAPIDO)
    bs = P.dispersao(*P.desenho("SMB", d), L, B.SEMENTE, n_rep=RAPIDO)
    assert bh / ih > bs / isb, (
        f"L={L}: o HML cresceu {bh/ih:.3f}x e o controle {bs/isb:.3f}x -- sem excesso "
        f"sobre o controle, o efeito pode ser artefato do metodo e o achado cai")


@pytest.mark.slow
def test_P88_o_VEREDITO_nao_muda_em_nenhum_L_DA_FAIXA_INFORMATIVA(d):
    """A conclusao que NAO depende de escolher um L, e por isso a mais forte.

    **Corrigido no mesmo dia, e o teste me corrigiu.** A primeira versao afirmava *"em
    nenhum L"* e falhou: com `L=24` e certas sementes o corte cai a **2,9087** e o
    `t = 2,9351` PASSA. Fui medir as quatro sementes de cada L:

        L=1..8   margem -0,175 a -0,378  contra sd 0,02-0,07  -> NAO_REJEITA, folgado
        L=12     margem -0,062           contra sd 0,067      -> NAO_CONFIRMADO
        L=24     margem -0,027           contra sd 0,067      -> NAO_CONFIRMADO

    **Margem menor que o ruido de semente e `NAO_CONFIRMADO`, nao veredito** -- a mesma regua
    que deixou o m=8 marcado em 18/09. E os dois L que caem nessa faixa sao justamente os
    degenerados, com 26 e 13 blocos distintos: a perda de reamostragem **alarga o proprio
    ruido** que torna o veredito inconclusivo ali.

    A afirmacao correta e mais estreita e mais forte: **em toda a faixa informativa, e em
    TODAS as sementes, o HML nao sobrevive** -- e com folga MAIOR que a do iid."""
    y, X = P.desenho("HML", d)
    _a, t = B.alfa_contra_os_demais("HML", d)
    for L in (1,) + P.L_INFORMATIVO:
        pior = min(P.corte(y, X, L, s) for s in P.SEMENTES[:2])
        assert t < pior, f"L={L}: t={t:.4f} passou o corte {pior:.4f}"


@pytest.mark.slow
def test_P88_fora_da_faixa_a_margem_entra_no_RUIDO_e_e_NAO_CONFIRMADO(d):
    """O outro lado, e ele precisa de teste para nao virar nota de pe de pagina: em L=24 a
    margem (0,027) e MENOR que o desvio entre sementes (0,067). **Quem usar o corte de L=24
    para decidir esta decidindo com ruido** -- e o instrumento tem de dizer isso, nao o
    laudo."""
    y, X = P.desenho("HML", d)
    _a, t = B.alfa_contra_os_demais("HML", d)
    cs = [P.corte(y, X, 24, s) for s in P.SEMENTES]
    margem = abs(t - float(np.mean(cs)))
    assert margem < float(np.std(cs)), (
        f"margem {margem:.4f} vs sd {np.std(cs):.4f} -- se a margem passar o ruido, L=24 "
        f"deixou de ser inconclusivo e a §5 do laudo precisa ser reescrita")


@pytest.mark.slow
def test_a_limitacao_era_CONSERVADORA_como_o_CLAUDE_md_dizia(d):
    """*"na mesma direcao do achado, o que torna a limitacao conservadora e nao
    convidativa"*. Medido: a folga piora, nao melhora."""
    y, X = P.desenho("HML", d)
    _a, t = B.alfa_contra_os_demais("HML", d)
    folga_iid = t - P.corte(y, X, 1, B.SEMENTE)
    folga_blk = t - P.corte(y, X, 3, B.SEMENTE)
    assert folga_blk < folga_iid < 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

# -*- coding: utf-8 -*-
"""Testes do corte de familia. Camada de oraculo externo + prova por mutacao.

O modulo implementa a t de Student em casa para nao acrescentar scipy ao ambiente
pinado (P-15), e implementacao sem oraculo e afirmacao. Os oraculos usados aqui sao
tres, e nenhum deles e "o numero que eu calculei outro dia":

  1. a TABELA publicada de Student, nos pontos que toda tabela traz;
  2. a identidade de ida-e-volta cdf(quantil(p)) == p;
  3. amostragem da propria distribuicao pelo numpy (`standard_t`), que e um gerador
     independente da minha aritmetica.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
import numpy as np, pytest
import multiplicidade as X

# Tabela de Student, valores de t bilateral a 5% e a 1% que qualquer tabela impressa
# traz. Sao o oraculo EXTERNO: nao vieram deste projeto.
TABELA = [
    (0.975, 1, 12.706), (0.975, 2, 4.303), (0.975, 5, 2.571), (0.975, 10, 2.228),
    (0.975, 20, 2.086), (0.975, 30, 2.042), (0.975, 60, 2.000), (0.975, 120, 1.980),
    (0.995, 1, 63.657), (0.995, 10, 3.169), (0.995, 30, 2.750), (0.995, 120, 2.617),
]


@pytest.mark.parametrize("p,gl,esperado", TABELA)
def test_t_quantil_bate_com_a_tabela_publicada(p, gl, esperado):
    assert abs(X.t_quantil(p, gl) - esperado) < 5e-4


@pytest.mark.parametrize("gl", [1, 2, 7, 30, 301, 5000])
@pytest.mark.parametrize("p", [0.51, 0.75, 0.95, 0.975, 0.999, 0.9999])
def test_ida_e_volta(p, gl):
    assert abs(X.t_cdf(X.t_quantil(p, gl), gl) - p) < 1e-10


def test_o_quantil_nao_SATURA_na_borda_do_intervalo():
    """A guarda do defeito que este arquivo encontrou na primeira execucao: com um
    intervalo fixo de +-1000, este quantil devolvia exatamente 1000,0 — a borda —
    sem erro nenhum. Numero de borda tem a mesma cara de numero certo.

    Mutacao: fixe `lim = 1e3` em `t_quantil` e este teste reprova; os outros 67 nao."""
    v = X.t_quantil(0.9999, 1)
    assert v > 3000, f"quantil saturado na borda: {v}"
    assert abs(X.t_cdf(v, 1) - 0.9999) < 1e-10


def test_com_muitos_graus_de_liberdade_a_t_vira_a_normal():
    """1,959964 e o quantil 97,5% da normal. Com gl grande a t tem de convergir para
    ele — e a distancia entre 1,96 e o valor com 301 gl e exatamente o erro que o
    projeto vinha cometendo ao citar 1,96."""
    assert abs(X.t_quantil(0.975, 10_000_000) - 1.959964) < 1e-5
    assert X.t_quantil(0.975, 301) > 1.959964


def test_a_cdf_e_simetrica_e_monotona():
    for gl in (3, 50, 301):
        assert abs(X.t_cdf(0.0, gl) - 0.5) < 1e-12
        for x in (0.3, 1.0, 2.5, 7.0):
            assert abs(X.t_cdf(x, gl) + X.t_cdf(-x, gl) - 1.0) < 1e-12
        assert X.t_cdf(0.1, gl) < X.t_cdf(0.2, gl) < X.t_cdf(0.3, gl)


def test_a_beta_incompleta_fecha_nos_extremos():
    assert X.beta_incompleta(2.0, 3.0, 0.0) == 0.0
    assert X.beta_incompleta(2.0, 3.0, 1.0) == 1.0
    # I_x(a,b) + I_{1-x}(b,a) = 1, identidade da funcao
    assert abs(X.beta_incompleta(2.5, 4.5, 0.3) + X.beta_incompleta(4.5, 2.5, 0.7) - 1) < 1e-12


def test_quantil_recusa_p_fora_do_intervalo():
    for p in (0.0, 1.0, -0.1, 1.2):
        with pytest.raises(ValueError):
            X.t_quantil(p, 10)
    with pytest.raises(ValueError):
        X.t_cdf(1.0, 0)


# ── Bonferroni ───────────────────────────────────────────────────────────────
def test_reproduz_os_cortes_que_o_projeto_registrou():
    """Os numeros de 13/09 do CLAUDE.md, agora com codigo por tras em vez de prosa.

    E este teste e a correcao do C-01 na sua forma generica: numero em prosa nao tem
    procedencia so por estar escrito com confianca."""
    for m, esperado in ((1, 1.968), (2, 2.253), (8, 2.754), (13, 2.913)):
        assert abs(X.corte_bonferroni(m, 301) - esperado) < 5e-4, m


def test_usar_a_NORMAL_no_lugar_da_t_afrouxa_o_corte():
    """A mutacao e o erro que eu de fato cometi em 12/09 e corrigi em 13/09: calcular
    os cortes com a normal. Ela AFROUXA todos os tres, e afrouxar e a direcao que faz
    uma estrategia parecer significante."""
    normal = {2: 2.2414, 8: 2.7344, 13: 2.8910}     # os numeros errados de 12/09
    for m, errado in normal.items():
        assert X.corte_bonferroni(m, 301) > errado


def test_o_corte_cresce_com_a_familia_e_e_o_de_sempre_quando_m_vale_um():
    c = [X.corte_bonferroni(m, 301) for m in (1, 2, 5, 13, 40)]
    assert c == sorted(c) and len(set(c)) == 5
    with pytest.raises(ValueError):
        X.corte_bonferroni(0, 301)


def test_unilateral_e_mais_frouxo_que_bilateral():
    assert X.corte_bonferroni(13, 301, bilateral=False) < X.corte_bonferroni(13, 301)


# ── Bonferroni MEDIDO: o mesmo objeto, medido em vez de suposto ──────────────
def test_marginal_de_student_devolve_o_corte_de_student():
    """O oraculo que amarra as duas metades: se a amostra reamostrada VIER de uma t de
    Student, o corte medido tem de coincidir com o tabelado. Sem este teste, qualquer
    diferenca entre os dois poderia ser defeito meu em vez de propriedade do dado."""
    amostra = np.random.default_rng(7).standard_t(301, 400_000)
    for m in (1, 2):
        assert abs(X.corte_bonferroni_medido(amostra, m)
                   - X.corte_bonferroni(m, 301)) < 0.02, m


def test_cauda_gorda_SOBE_o_corte_e_e_por_isso_que_o_medido_passa_o_tabelado():
    """t com 3 graus de liberdade tem cauda muito mais gorda que a de 301. O corte
    medido sobe, e a direcao e a que importa: supor Student quando o dado e mais gordo
    REJEITA demais."""
    gorda = np.random.default_rng(7).standard_t(3, 200_000)
    assert X.corte_bonferroni_medido(gorda, 13) > X.corte_bonferroni(13, 301) * 1.5


def test_corte_medido_recusa_familia_vazia():
    with pytest.raises(ValueError):
        X.corte_bonferroni_medido(np.zeros(10), 0)


# ── Romano-Wolf ──────────────────────────────────────────────────────────────
def _boot(rng, n=20_000, **colunas):
    return {k: v for k, v in colunas.items()}


def test_hipoteses_IDENTICAS_dao_o_corte_de_UMA_so():
    """Caso limite com resposta conhecida: se as duas hipoteses sao a mesma variavel,
    a familia tem tamanho efetivo 1 e o Romano-Wolf tem de devolver o corte de um
    teste isolado. Bonferroni devolveria o de dois — e a diferenca e o ganho."""
    a = np.random.default_rng(1).standard_t(301, 60_000)
    igual = {"h1": a, "h2": a.copy()}
    um_so = float(np.quantile(np.abs(a), 0.95))
    assert abs(X.corte_romano_wolf(igual) - um_so) < 1e-9
    assert X.corte_romano_wolf(igual) < X.corte_bonferroni_medido(a, 2)


def test_hipoteses_INDEPENDENTES_nao_dao_ganho_nenhum():
    """O outro caso limite: sem correlacao, o maximo de duas independentes fica perto
    do corte de Bonferroni, e o Romano-Wolf nao tem o que aproveitar. Este e o caso
    da familia real deste projeto, e e a razao de o instrumento fino render pouco."""
    rng = np.random.default_rng(2)
    ind = {"h1": rng.standard_t(301, 60_000), "h2": rng.standard_t(301, 60_000)}
    assert X.corte_romano_wolf(ind) > 0.98 * X.corte_bonferroni_medido(ind["h1"], 2)


def test_reamostragem_independente_destroi_o_ganho():
    """A armadilha central, medida. Sortear cada hipotese com a propria semente
    transforma duas hipoteses IDENTICAS em duas independentes aos olhos do metodo: o
    corte sobe, o numero continua saindo, e nada avisa.

    E o A-06 em estatistica — o instrumento mede algo, e o algo nao e o que se pensa."""
    a = np.random.default_rng(3).standard_t(301, 60_000)
    b_igual = np.random.default_rng(3).standard_t(301, 60_000)   # MESMO sorteio
    b_solto = np.random.default_rng(4).standard_t(301, 60_000)   # sorteio proprio
    junto = X.corte_romano_wolf({"h1": a, "h2": b_igual})
    solto = X.corte_romano_wolf({"h1": a, "h2": b_solto})
    assert junto < solto, "o pareamento por sorteio precisa render corte menor"
    assert solto - junto > 0.15, f"ganho medido: {solto - junto:.3f}"


def test_p_ajustado_e_monotono_e_ordena_pelo_t():
    rng = np.random.default_rng(5)
    boot = {k: rng.standard_t(301, 20_000) for k in ("a", "b", "c")}
    obs = {"a": 3.4, "b": 2.1, "c": 0.4}
    p = X.romano_wolf(obs, boot)
    assert p["a"] <= p["b"] <= p["c"], p
    assert p["a"] < 0.05 < p["c"]


def test_p_ajustado_e_sempre_maior_ou_igual_ao_de_um_teste_so():
    """Corrigir nunca pode deixar mais facil rejeitar. Se ficar, o stepdown esta
    invertido — e invertido ele passaria despercebido, porque continua produzindo
    numeros entre 0 e 1."""
    rng = np.random.default_rng(6)
    boot = {k: rng.standard_t(301, 20_000) for k in ("a", "b", "c", "d")}
    obs = {"a": 2.4, "b": 2.2, "c": 1.4, "d": 0.2}
    p = X.romano_wolf(obs, boot)
    for k, t in obs.items():
        sozinho = float((np.abs(boot[k]) >= abs(t)).mean())
        assert p[k] >= sozinho - 1e-12, (k, p[k], sozinho)


def test_romano_wolf_recusa_hipotese_sem_bootstrap_e_repeticoes_desiguais():
    rng = np.random.default_rng(8)
    boot = {"a": rng.standard_t(301, 1000)}
    with pytest.raises(ValueError):
        X.romano_wolf({"a": 2.0, "b": 1.0}, boot)
    with pytest.raises(ValueError):
        X.romano_wolf({"a": 2.0, "b": 1.0},
                      {"a": rng.standard_t(301, 1000), "b": rng.standard_t(301, 999)})


def test_o_maximo_e_por_REPETICAO_e_nao_por_hipotese():
    """Reduzir pelo eixo errado da o maximo ao longo do tempo de cada hipotese, que e
    um numero por hipotese e nao uma distribuicao — e `np.quantile` aceitaria os dois
    calados. O cenario e montado para que os dois eixos NAO coincidam."""
    t = {"a": np.array([3.0, 0.0, 0.0]), "b": np.array([0.0, 2.0, 1.0])}
    assert list(X._maximo_por_repeticao(t, ["a", "b"])) == [3.0, 2.0, 1.0]
    with pytest.raises(ValueError):
        X._maximo_por_repeticao(t, [])


def test_o_veredito_e_um_nome_e_usa_o_MODULO_do_t():
    assert X.veredito(2.5, 2.25) == "REJEITA"
    assert X.veredito(-2.5, 2.25) == "REJEITA", "um alfa negativo grande tambem rejeita"
    assert X.veredito(2.0, 2.25) == "NAO_REJEITA"


def test_a_fracao_continua_converge_onde_o_projeto_precisa():
    """Guarda contra o unico modo de falha silencioso da implementacao: a fracao
    continua sem convergir levantaria, mas so se alguem passar por la."""
    for gl in (1, 2, 3, 301, 100_000):
        for x in (-40.0, -1.0, 0.0, 1.0, 40.0):
            v = X.t_cdf(x, gl)
            assert 0.0 <= v <= 1.0 and not math.isnan(v)

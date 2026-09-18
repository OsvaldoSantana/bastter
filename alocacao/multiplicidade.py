# -*- coding: utf-8 -*-
"""O corte que o CONJUNTO exige, e nao o corte de um teste isolado.

Oito estrategias pre-registradas, cada uma rejeitando a nula a t > 1,96, dao
1 - 0,95**8 ~ 34% de chance de ao menos uma rejeicao falsa sob a nula. O `rejeita_se`
das oito diz "alfa nao distinguivel de zero" e NAO diz a que corte — entao o corte e
1,96 por omissao, oito vezes. Este modulo troca a omissao por um numero.

DUAS CORRECOES, e elas nao sao alternativas: respondem perguntas diferentes porque
tem insumos diferentes.

  BONFERRONI  precisa apenas do TAMANHO da familia. E o unico instrumento aplicavel
              ao lado ORCADO (`m` = soma dos variantes_permitidas), onde 11 dos 13
              testes nunca produziram estatistica nenhuma. Nao ha o que reamostrar
              num teste que nao rodou. E o teto honesto, e ele e conservador de
              proposito: superestima a correcao quando os testes sao correlacionados,
              e os deste projeto sao — todos regridem sobre os mesmos cinco fatores,
              na mesma serie.

  ROMANO-WOLF precisa das ESTATISTICAS. So se aplica ao lado EXECUTADO, e em troca
              ele mede a correlacao em vez de supo-la: o corte sai da distribuicao
              reamostrada do MAXIMO |t| da familia, que e menor que o de Bonferroni
              exatamente na medida em que os testes andam juntos.

A consequencia de desenho, e ela nao era obvia quando a decisao foi tomada: o `m` dos
dois lados nao e o mesmo numero medido duas vezes, e sim DUAS MEDIDAS COM INSTRUMENTOS
DIFERENTES, por necessidade e nao por escolha. O lado executado descreve a evidencia e
pode usar o instrumento fino; o lado orcado descreve a disciplina e so aceita o grosso.

ARMADILHA CENTRAL DO ROMANO-WOLF, e ela e silenciosa: as hipoteses tem de ser
reamostradas JUNTAS, com o mesmo sorteio de meses em cada repeticao. Reamostrar cada
uma com a propria semente destroi a correlacao — que e a unica coisa que o
Romano-Wolf tem e o Bonferroni nao. O resultado continua saindo, com numero plausivel,
e o metodo vira Bonferroni caro. `test_reamostragem_independente_destroi_o_ganho` e
quem denuncia.

O quantil da t de Student e calculado AQUI, e nao importado. O projeto pina as
dependencias em `pyproject.toml` e a impressao do ambiente (P-15) entra em todo
resultado pre-registrado; acrescentar scipy para uma funcao de 40 linhas mudaria a
impressao e transformaria todo numero ja registrado em numero novo. O preco disso e
que a implementacao precisa de oraculo: `test_multiplicidade.py` confere contra a
tabela publicada de Student E contra a identidade de ida-e-volta.
"""
from __future__ import annotations
import math
import numpy as np

ALFA_FAMILIAR = 0.05        # o alfa do CONJUNTO, nao o de cada teste
_MAXIT, _EPS, _FPMIN = 300, 3e-16, 1e-300


# ── a t de Student, sem dependencia nova ─────────────────────────────────────
def _betacf(a: float, b: float, x: float) -> float:
    """Fracao continuada de Lentz para a beta incompleta. Numerical Recipes, 6.4."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < _FPMIN: d = _FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, _MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < _FPMIN: d = _FPMIN
        c = 1.0 + aa / c
        if abs(c) < _FPMIN: c = _FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < _FPMIN: d = _FPMIN
        c = 1.0 + aa / c
        if abs(c) < _FPMIN: c = _FPMIN
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < _EPS: return h
    raise ArithmeticError(f"beta incompleta nao convergiu em {_MAXIT} iteracoes "
                          f"(a={a}, b={b}, x={x})")


def beta_incompleta(a: float, b: float, x: float) -> float:
    """I_x(a, b) regularizada."""
    if x <= 0.0: return 0.0
    if x >= 1.0: return 1.0
    ln_b = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    bt = math.exp(ln_b + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_cdf(x: float, gl: int) -> float:
    """P(T <= x) para a t de Student com `gl` graus de liberdade."""
    if gl <= 0: raise ValueError(f"graus de liberdade tem de ser positivo: {gl}")
    meio = 0.5 * beta_incompleta(gl / 2.0, 0.5, gl / (gl + x * x))
    return 1.0 - meio if x >= 0 else meio


def t_quantil(p: float, gl: int) -> float:
    """O x tal que P(T <= x) = p. Bissecao sobre um intervalo que se ABRE ate conter p.

    Sem forma fechada e sem scipy; a bissecao e lenta e correta, e esta funcao roda
    uma vez por relatorio. Trocar por Newton aqui seria otimizar o que nao custa.

    O intervalo era fixo em +-1000 e isso era um DEFEITO DA CLASSE QUE O PROJETO
    PERSEGUE: com gl=1 (Cauchy) o quantil 99,99% fica em ~3183, e a bissecao devolvia
    1000,0 — a borda do intervalo — em silencio, com cara de resposta. Quem chamasse
    receberia um corte frouxo e nenhum aviso. Achado pelo proprio
    `test_ida_e_volta`, que e o motivo de a identidade estar na suite em vez de so a
    tabela: a tabela nao tem essa casa. Agora o intervalo cresce, e se nao couber a
    funcao LEVANTA em vez de saturar."""
    if not 0.0 < p < 1.0: raise ValueError(f"p fora de (0,1): {p}")
    lim = 4.0
    while t_cdf(-lim, gl) > p or t_cdf(lim, gl) < p:
        lim *= 4.0
        if lim > 1e12:
            raise ArithmeticError(f"p={p} com gl={gl} esta alem do alcance numerico da t_cdf")
    lo, hi = -lim, lim
    for _ in range(400):
        meio = 0.5 * (lo + hi)
        if t_cdf(meio, gl) < p: lo = meio
        else: hi = meio
        if hi - lo < 1e-13: break
    return 0.5 * (lo + hi)


# ── Bonferroni: so precisa do TAMANHO da familia ─────────────────────────────
def corte_bonferroni(m: int, gl: int, alfa: float = ALFA_FAMILIAR,
                     bilateral: bool = True) -> float:
    """O |t| minimo para rejeitar uma de `m` hipoteses mantendo o alfa do CONJUNTO.

    Bilateral por padrao porque o 1,96 que o projeto vinha usando por omissao e
    bilateral: trocar a lateralidade junto com a correcao misturaria duas mudancas
    num numero so e ninguem saberia qual delas o moveu."""
    if m < 1: raise ValueError(f"familia vazia nao tem corte: m={m}")
    cauda = alfa / m / (2.0 if bilateral else 1.0)
    return t_quantil(1.0 - cauda, gl)


def corte_bonferroni_medido(t_boot_da_hipotese: np.ndarray, m: int,
                            alfa: float = ALFA_FAMILIAR) -> float:
    """Bonferroni com a marginal MEDIDA no lugar da t de Student tabelada.

    A uniao de Boole nao pede independencia nenhuma: se cada hipotese rejeita ao
    nivel alfa/m, o conjunto rejeita falsamente no maximo alfa, sob QUALQUER
    dependencia. Isso e o que torna esta funcao aplicavel ao lado ORCADO — ela usa
    so a marginal desta hipotese, e nao precisa que as outras 12 tenham rodado.

    O que ela troca e a unica suposicao que sobra: a de que o t estimado se
    distribui como uma t de Student. Medido nesta serie, ele nao se distribui —
    a cauda e ~7% mais gorda, e o corte sobe na mesma proporcao.

    PRECISAO: o quantil 1-alfa/m com m grande vive na ponta da amostra reamostrada.
    Com 10.000 repeticoes e m=13, sao ~38 observacoes acima do corte, e o numero
    balanca na terceira casa. Quem comparar margens menores que isso precisa de mais
    repeticoes ou de declarar NAO_CONFIRMADO."""
    if m < 1: raise ValueError(f"familia vazia nao tem corte: m={m}")
    q = 1.0 - alfa / m
    return float(np.quantile(np.abs(t_boot_da_hipotese), q))


# ── Romano-Wolf: precisa das ESTATISTICAS ────────────────────────────────────
def corte_romano_wolf(t_boot: dict[str, np.ndarray], alfa: float = ALFA_FAMILIAR) -> float:
    """Valor critico de passo unico (maxT): o quantil 1-alfa do maximo |t| da familia.

    E o numero diretamente comparavel ao de Bonferroni, e a diferenca entre os dois E
    a correlacao medida. O stepdown abaixo refina isto hipotese a hipotese."""
    M = _maximo_por_repeticao(t_boot, list(t_boot))
    return float(np.quantile(M, 1.0 - alfa))


def romano_wolf(t_obs: dict[str, float], t_boot: dict[str, np.ndarray]) -> dict[str, float]:
    """p-valores ajustados por FWER, stepdown de Romano & Wolf (2005).

    t_boot[k] tem de ser a distribuicao da estatistica CENTRADA NA NULA — isto e,
    (alfa* - alfa_estimado) / erro_padrao*, e nao o t cru. O t cru mede se a
    estrategia paga; o centrado mede o que o acaso produz quando ela nao paga, que e
    a unica pergunta que uma correcao de multiplicidade responde.

    Todas as chaves de `t_obs` precisam estar em `t_boot` com o MESMO numero de
    repeticoes, porque a repeticao `i` de duas hipoteses tem de vir do mesmo sorteio."""
    faltando = set(t_obs) - set(t_boot)
    if faltando:
        raise ValueError(f"hipotese sem bootstrap: {sorted(faltando)}")
    tamanhos = {len(v) for v in t_boot.values()}
    if len(tamanhos) != 1:
        raise ValueError(f"repeticoes desiguais entre hipoteses: {sorted(tamanhos)} — "
                         f"o pareamento por sorteio se perde")

    ordem = sorted(t_obs, key=lambda k: -abs(t_obs[k]))
    restantes = list(ordem)
    ajustado: dict[str, float] = {}
    anterior = 0.0
    for nome in ordem:
        M = _maximo_por_repeticao(t_boot, restantes)
        p = float((M >= abs(t_obs[nome])).mean())
        p = max(p, anterior)          # monotonicidade: o stepdown nunca afrouxa
        ajustado[nome] = p
        anterior = p
        restantes.remove(nome)
    return ajustado


def _maximo_por_repeticao(t_boot: dict[str, np.ndarray], nomes: list[str]) -> np.ndarray:
    """max_j |t*_j| dentro de CADA repeticao. O eixo importa: reduzir pelo eixo errado
    daria o maximo ao longo do tempo de cada hipotese, que nao e uma familia."""
    if not nomes: raise ValueError("maximo de familia vazia")
    return np.max(np.abs(np.vstack([t_boot[n] for n in nomes])), axis=0)


def veredito(t: float, corte: float) -> str:
    """Um nome, nunca um numero solto. P3: quem elimina tem de dizer por que."""
    return "REJEITA" if abs(t) >= corte else "NAO_REJEITA"

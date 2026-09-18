# -*- coding: utf-8 -*-
"""H1 (hml_puro_v1), H2 (dy_alto_v1) e H3 (tamanho_smb_v1) contra os fatores NEFIN.

Executa o que o pre-registro de politica.yaml define, e SO isso. Rodar de novo tem
de dar o mesmo numero: a semente do bootstrap e fixa e a fonte tem hash publicado.

DUAS ARMADILHAS, ambas capazes de inverter o veredito sem levantar erro:

  1. NAO usar fatores.alfa_contra_fatores() aqui. Ela subtrai o Risk_Free, porque
     foi escrita para uma carteira COMPRADA. Os fatores do NEFIN sao long-short
     auto-financiados: descontar o CDI de um spread cobra um custo que a carteira
     nao tem. No HML isso troca +0,766% (t=+2,94) por -0,178% (t=-0,68).

  2. "Alfa contra os DEMAIS fatores" exclui o proprio fator. Incluir-se da R2 = 1
     por construcao — tautologia, nao teste.
"""
from __future__ import annotations
import numpy as np
import fatores as F
import multiplicidade as MP

FATORES = ["Rm_minus_Rf", "SMB", "HML", "WML", "IML"]
SEMENTE = 20260905
MIN_DIAS = 15          # mes com menos pregoes que isso nao e observacao mensal

def amostra():
    m = F.mensal()
    return m[m.n_dias >= MIN_DIAS]

def _mqo(y, X):
    """O NUCLEO da regressao, e ele existe uma vez so.

    Extraido em 18/09 porque o bootstrap conjunto precisava do erro padrao e a
    tentacao era reescrever tres linhas de algebra do lado de la. Duas leituras da
    mesma regra concordam por acidente ate o dia em que nao concordam — N-01."""
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    gl = len(y) - X.shape[1]
    se = np.sqrt(np.diag((r @ r / gl) * np.linalg.inv(X.T @ X)))
    return b[0], se[0], b[0] / se[0]

def _colunas(alvo, d):
    outros = [f for f in FATORES if f != alvo]
    return d[alvo].values, np.column_stack([np.ones(len(d))] + [d[c].values for c in outros])

def alfa_se_t(alvo, d):
    """(alfa_mensal, erro_padrao, t). Sem subtrair Risk_Free — armadilha 1 acima."""
    return _mqo(*_colunas(alvo, d))

def alfa_contra_os_demais(alvo, d):
    """(alfa_mensal, t). A ASSINATURA PRE-REGISTRADA — nao mude, ha teste que a prende."""
    a, _, t = alfa_se_t(alvo, d)
    return a, t

def graus_de_liberdade(d):
    """n - k, com k = intercepto + os quatro demais fatores. O corte da t de Student
    depende disto, e deixa-lo implicito foi como 1,96 (que e a NORMAL) virou o corte
    por omissao de um teste que tem 301 graus de liberdade."""
    return len(d) - len(FATORES)

def bootstrap_conjunto(alvos, d, n=10_000, semente=SEMENTE):
    """t CENTRADO NA NULA de cada alvo, com o MESMO sorteio de meses em cada repeticao.

    Duas decisoes, e as duas sao o metodo:

      CENTRADO. t* = (alfa* - alfa_estimado)/se*. O t cru mede se o fator paga; a
      correcao de multiplicidade pergunta o que o acaso produz quando ele NAO paga.
      `bootstrap_t` abaixo devolve o cru de proposito e responde outra pergunta.

      CONJUNTO. Um sorteio por repeticao, servindo todas as hipoteses. E a correlacao
      entre elas que o Romano-Wolf aproveita, e sortear separado a destroi sem deixar
      sinal nenhum — o numero continua saindo."""
    ponto = {a: alfa_se_t(a, d) for a in alvos}
    colunas = {a: _colunas(a, d) for a in alvos}
    rng = np.random.default_rng(semente)
    idx = np.arange(len(d))
    out = {a: np.empty(n) for a in alvos}
    for i in range(n):
        s = rng.choice(idx, len(idx), replace=True)
        for a in alvos:
            y, X = colunas[a]
            av, se, _ = _mqo(y[s], X[s])
            out[a][i] = (av - ponto[a][0]) / se
    return out

def meses_que_carregam(alvo, d, k=12):
    """Alfa depois de remover os k meses de maior influencia positiva.

    Um alfa que morre ao perder 4% da amostra e uma aposta em poucos meses, nao um
    premio. O CONTROLE importa tanto quanto o teste: se todo fator morresse igual,
    a medida nao diria nada. O WML nao morre."""
    a0, _ = alfa_contra_os_demais(alvo, d)
    infl = np.array([alfa_contra_os_demais(alvo, d.drop(d.index[i]))[0] - a0
                     for i in range(len(d))])
    return alfa_contra_os_demais(alvo, d.drop(d.index[np.argsort(infl)[:k]]))

def bootstrap_t(alvo, d, n=10_000, semente=SEMENTE):
    rng = np.random.default_rng(semente)
    idx = np.arange(len(d))
    ts = [alfa_contra_os_demais(alvo, d.iloc[rng.choice(idx, len(idx), replace=True)])[1]
          for _ in range(n)]
    return np.array(ts)

ALVOS = ("HML", "SMB")
DE_ALVO_PARA_ESTRATEGIA = {"HML": "hml_puro_v1", "SMB": "tamanho_smb_v1"}

if __name__ == "__main__":
    import alocacao as A, preregistro as R
    d = amostra()
    gl = graus_de_liberdade(d)
    P = A.carregar_politica()
    print(f"fonte sha256[:12] = {F.hash_fonte()} | {len(d)} meses "
          f"({d.index.min()} a {d.index.max()})")
    print(f"pesquisa_id = {R.pesquisa_id(P, F.hash_fonte())} | "
          f"m executado = {R.m_executado(P)} (do diario) | "
          f"m orcado = {R.m_orcado(P)} (soma dos variantes_permitidas)\n")

    boot = bootstrap_conjunto(list(ALVOS), d)
    tab = R.cortes_tabelados(P, gl)
    p_aj = MP.romano_wolf({a: float(alfa_contra_os_demais(a, d)[1]) for a in ALVOS}, boot)

    for alvo in ALVOS:
        a, t = alfa_contra_os_demais(alvo, d)
        ak, tk = meses_que_carregam(alvo, d)
        ts = bootstrap_t(alvo, d)
        cor = R.cortes_medidos(P, boot, alvo)
        v = R.veredito_dos_dois_lados(t, cor)
        print(f"{alvo}: alfa={a*100:+.3f}% a.m. ({(1+a)**12-1:+.2%} a.a.) t={t:+.2f}")
        print(f"     sem os 12 meses de maior influencia: alfa={ak*100:+.3f}% t={tk:+.2f}")
        print(f"     bootstrap P(t>1,96) = {100*(ts>1.96).mean():.0f}%")
        print(f"     familia EXECUTADA (m={cor['m_executado']}, Romano-Wolf): corte "
              f"{cor['executado']:.4f} -> {v['executado']}  (p ajustado {p_aj[alvo]:.4f}; "
              f"Bonferroni tabelado seria {tab['executado']:.4f})")
        print(f"     familia ORCADA   (m={cor['m_orcado']}, Bonferroni medido): corte "
              f"{cor['orcado']:.4f} -> {v['orcado']}  "
              f"(Bonferroni tabelado seria {tab['orcado']:.4f})")
        try:
            print(f"     OPERATIVO: {R.operativo(P, DE_ALVO_PARA_ESTRATEGIA[alvo], v)}"
                  + ("  [os dois lados divergem; a leitura esta escrita no politica.yaml]"
                     if v["divergem"] else ""))
        except R.DivergenciaNaoEscrita as e:
            print(f"     BLOQUEADA: {e}")
        print()
    print("H2 (dy_alto_v1): NAO EXECUTAVEL - a serie nao tem fator de dividend yield.")
    print("  colunas:", [c for c in d.columns if c != "n_dias"])

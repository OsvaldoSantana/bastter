# -*- coding: utf-8 -*-
"""Testes do modulo de fatores. Camada de contrato + oraculo externo."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, pytest
from fatores import (carregar_diario, mensal, premios, premio_de_mercado,
                     janelas_moveis, alfa_contra_fatores, hash_fonte, FATORES, FonteAusente)

D = carregar_diario(); M = mensal(D)

def test_cobertura_e_integridade_da_serie():
    assert D.Date.is_monotonic_increasing and not D.Date.duplicated().any()
    assert D[FATORES + ["Risk_Free"]].isna().sum().sum() == 0
    assert D.Date.dt.dayofweek.max() <= 4, "a serie nao pode ter fim de semana"
    assert D.Date.min().year == 2001 and D.Date.max().year >= 2026
    assert len(D) > 6000

def test_meses_parciais_sao_excluidos_do_premio():
    """O ultimo mes da serie quase sempre e incompleto; conta-lo como observacao
    mensal contamina a media."""
    assert M.n_dias.iloc[-1] < 20, "cenario mudou: reveja o filtro de meses parciais"
    assert premios(M)["HML"]["n"] < len(M)

def test_smb_e_negativo_e_sem_significancia():
    """A hipotese nula do pre-registro que SOBREVIVEU a verificacao: o premio de
    tamanho nao existe no Brasil de 2001 a 2026."""
    v = premios(M)["SMB"]
    assert v["media_am"] < 0 and abs(v["t"]) < 2

def test_hml_e_positivo_e_significante_contrariando_a_literatura_citada():
    """A premissa que a verificacao DERRUBOU. O pre-registro 1.3.0 registrou HML como
    hipotese nula esperada citando 0,05% ao mes — numero de resumo indexado. Na serie,
    HML paga 0,688% ao mes com t = 2,60, e e positivo em toda janela testada."""
    v = premios(M)["HML"]
    assert v["media_am"] > 0.005, f"HML medido: {v['media_am']:.4%} a.m."
    assert v["t"] > 2
    m = M[M.n_dias >= 15].copy(); m.index = m.index.to_timestamp()
    for a, b in [(2001, 2012), (2001, 2016), (2013, 2026), (2021, 2026)]:
        janela = m[(m.index.year >= a) & (m.index.year <= b)].HML
        assert janela.mean() > 0.004, \
            f"{a}-{b}: {janela.mean():.4%} — a citacao de 0,05% nao se reproduz"

def test_wml_e_o_fator_mais_forte():
    pr = premios(M)
    assert pr["WML"]["t"] == max(v["t"] for v in pr.values())
    assert pr["WML"]["t"] > 3

def test_premio_de_risco_de_acoes_nao_e_distinguivel_de_zero():
    """O numero mais desconfortavel do projeto, e ele calibra a fracao em renda
    variavel — que continua sendo preferencia declarada, agora com o preco medido."""
    pm = premio_de_mercado(M)
    assert pm["anos"] > 24
    assert pm["premio_aa"] < 0.03
    assert abs(pm["t"]) < 2, "premio de mercado significante mudaria a leitura da politica"

def test_ha_janelas_de_dez_anos_em_que_a_bolsa_perdeu_do_cdi():
    jm = janelas_moveis(10, M)
    perdeu = [j for j in jm if not j["acoes_venceu"]]
    assert len(perdeu) >= 5 and len(perdeu) < len(jm)
    seq = [j["inicio"] for j in perdeu]
    assert any(all(y + k in seq for k in range(4)) for y in seq), \
        "as janelas perdedoras nao sao isoladas: ha uma sequencia longa"

def test_alfa_de_um_fator_contra_ele_mesmo_e_zero():
    """Teste canonico com oraculo externo: regredir um fator sobre o modelo que o
    contem tem de dar beta 1 nele, zero nos outros, alfa zero e R2 ~ 1."""
    m = M[M.n_dias >= 15]
    r = alfa_contra_fatores(m.HML + m.Risk_Free, m)
    assert abs(r["alfa_am"]) < 1e-9 and r["r2"] > 0.999
    assert abs(r["coef"]["HML"] - 1) < 1e-9
    for f in ("SMB", "WML", "IML", "Rm_minus_Rf"):
        assert abs(r["coef"][f]) < 1e-9

def test_alfa_de_ruido_branco_nao_e_significante():
    """Controle de integridade: uma serie aleatoria nao pode produzir alfa."""
    m = M[M.n_dias >= 15]
    rng = np.random.default_rng(42)
    ruido = pd.Series(rng.normal(0, 0.05, len(m)), index=m.index) + m.Risk_Free
    r = alfa_contra_fatores(ruido, m)
    assert abs(r["t_alfa"]) < 3 and r["r2"] < 0.2

def test_alfa_exige_historico_minimo():
    m = M[M.n_dias >= 15].head(12)
    with pytest.raises(ValueError):
        alfa_contra_fatores(m.HML + m.Risk_Free, m)

# Impressao digital da serie do NEFIN. NAO e cosmetico: o pre-registro promete que
# um resultado de backtest e reproduzivel, e isso so vale se a serie que o produziu
# for byte a byte a mesma. Se este valor mudar, ou a fonte foi atualizada de
# proposito (entao atualize aqui E registre em REGISTRO-vN.md) ou o arquivo foi
# corrompido em transito.
#
# Achado F-04 (04/09/2026): o git no Windows converte LF em CRLF no checkout por
# padrao. Isso adiciona 6.322 bytes ao CSV (um por pregao) e muda o sha256 de
# 619991c2192c para 421b3b3b753e — silenciosamente, num clone novo. O
# .gitattributes marca este arquivo como binario para impedir a conversao; este
# teste e quem denuncia se a protecao falhar.
HASH_ESPERADO = "619991c2192c"

def test_fonte_e_exatamente_a_serie_pre_registrada():
    """O teste anterior era `hash_fonte() == hash_fonte()` — so provava que a funcao
    e deterministica, e passaria alegremente sobre um arquivo corrompido."""
    h = hash_fonte()
    assert len(h) == 12
    assert h == HASH_ESPERADO, (
        f"a serie do NEFIN mudou: esperado {HASH_ESPERADO}, encontrado {h}. "
        f"Se for conversao de fim de linha (CRLF), confira o .gitattributes. "
        f"Se a fonte foi atualizada de proposito, atualize HASH_ESPERADO e registre.")

def test_serie_nao_tem_fim_de_linha_do_windows():
    """Guarda direta e barata contra o modo de falha F-04, independente do hash."""
    import fatores as _f
    with open(_f.ARQUIVO, "rb") as fh:
        bruto = fh.read()
    assert b"\r\n" not in bruto, (
        "o CSV do NEFIN esta com CRLF. O git converteu no checkout e o sha256 da "
        "fonte mudou. Confira `git check-attr -a alocacao/dados/nefin_factors.csv`.")

def test_fonte_ausente_levanta_em_vez_de_seguir_sem_benchmark():
    """Sem os fatores nao ha benchmark valido — e rodar sem benchmark e o achado D-1
    da auditoria da literatura, nao um modo degradado aceitavel."""
    with pytest.raises(FonteAusente):
        carregar_diario("/tmp/nao_existe_fatores.csv")


# ── H1/H3: os numeros do pre-registro ficam presos aqui ──────────────────────
# Se a serie mudar, o veredito muda — e o teste denuncia antes de alguem reusar
# um resultado que nao vale mais. Mesma logica do HASH_ESPERADO acima.
def test_h1_h3_reproduzem_o_resultado_registrado():
    import backtest_h1_h3 as B
    d = B.amostra()
    assert len(d) == 306, "amostra mudou: o pre-registro fala de 306 meses uteis"
    a_hml, t_hml = B.alfa_contra_os_demais("HML", d)
    a_smb, t_smb = B.alfa_contra_os_demais("SMB", d)
    assert abs(a_hml - 0.00766) < 1e-4 and abs(t_hml - 2.94) < 0.02
    assert abs(a_smb - 0.00054) < 1e-4 and abs(t_smb - 0.28) < 0.02

def test_subtrair_risk_free_de_um_fator_inverte_o_veredito():
    """A armadilha, presa num teste: se alguem 'consertar' o codigo para usar
    alfa_contra_fatores(), este teste mostra o tamanho do estrago."""
    import numpy as np, backtest_h1_h3 as B
    d = B.amostra()
    a_certo, t_certo = B.alfa_contra_os_demais("HML", d)
    outros = [f for f in B.FATORES if f != "HML"]
    y = d["HML"].values - d["Risk_Free"].values          # o jeito ERRADO
    X = np.column_stack([np.ones(len(d))] + [d[c].values for c in outros])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    assert a_certo > 0 and b[0] < 0, "subtrair o CDI de um spread inverte o sinal do alfa"

def test_concentracao_do_hml_nao_e_artefato():
    """O controle: a mesma cirurgia que mata o HML deixa o WML vivo."""
    import backtest_h1_h3 as B
    d = B.amostra()
    _, t_hml = B.meses_que_carregam("HML", d)
    _, t_wml = B.meses_que_carregam("WML", d)
    assert t_hml < 1.96 < t_wml

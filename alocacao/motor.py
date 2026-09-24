# -*- coding: utf-8 -*-
"""
Motor de custo v2 — corrige os achados K-01 a K-11 do laudo de 01/09/2026.

Mudancas em relacao a v1:
  K-01/K-07  status viaja com o dado; rota com insumo NAO_CONFIRMADO nao entra na ordenacao
  K-03       custodia da B3 com as 10 faixas progressivas (v1 usava so a faixa 1, a mais cara)
  K-04       interpretacao da isencao declarada e parametrizavel; cenario de custodia absorvida
  K-05       taxa de administracao aparece na tabela de entrada
  K-06       perna de saida modelada (corretagem, B3 na venda, IOF de repatriacao)
  K-08       premissas de modelagem declaradas; c>aporte emite alerta em vez de truncar em silencio
  (P-43, 24/09/2026: K-05, K-06 e K-08 viviam em `simular`/`montar_rotas`, que sairam;
   K-06 hoje e `alocacao.custo_saida_pct`, e o alerta do K-08.3 ficou pendente -- P-134)
  K-11       constantes vem do YAML com procedencia; caminhos relativos; roda com -m; testes
"""
from __future__ import annotations
import os, sys, datetime as dt
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))

class InsumoBloqueado(Exception):
    """Levantada quando um calculo depende de valor NAO_CONFIRMADO."""

# ── carga com verificacao de status e validade ────────────────────────────────
def carregar(path=None):
    with open(path or os.path.join(AQUI, "custos.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

def _consequencia(no):
    """Achado F-05: `bloqueia` era prosa. Agora viaja na excecao.

    A P1 promete que um insumo bloqueado diz O QUE ele bloqueia. Ate 05/09/2026 o
    campo existia no custos.yaml e NENHUMA linha de codigo o lia — a excecao dizia
    so o motivo, nunca a consequencia. Quem via `InsumoBloqueado: etf.BOVV11` nao
    sabia que o que morria era a tabela completa de ETF de renda variavel.
    """
    b = no.get("bloqueia") or []
    if isinstance(b, str): b = [b]
    return f"  BLOQUEIA: {', '.join(b)}" if b else \
           "  (sem `bloqueia` declarado — o custo de nao ter este valor nao esta escrito)"

def val(no, *, permitir_parcial=True, contexto="", hoje=None):
    """Extrai o valor de um no do YAML, recusando NAO_CONFIRMADO.

    P-70: `HOJE` era uma constante fixa (2026-09-01) resolvida no IMPORT do
    modulo — o aviso de expiracao ficava mudo a partir do primeiro dia
    seguinte e ninguem via. `hoje` agora e parametro; quando omitido, resolve
    para `dt.date.today()` NO MOMENTO DA CHAMADA, nao no import."""
    if not isinstance(no, dict) or "valor" not in no:
        return no
    st = no.get("status", "COMPLETO")
    if st == "NAO_CONFIRMADO" or no["valor"] is None:
        raise InsumoBloqueado(f"{contexto}: {no.get('motivo','valor nao confirmado')}"
                              + _consequencia(no))
    if st == "PARCIAL" and not permitir_parcial:
        raise InsumoBloqueado(f"{contexto}: status PARCIAL — {no.get('motivo','')}"
                              + _consequencia(no))
    exp = no.get("expira")
    if exp and isinstance(exp, dt.date):
        agora = hoje if hoje is not None else dt.date.today()
        if agora > exp:
            print(f"  [AVISO] {contexto}: valor expirou em {exp} "
                  f"(fonte: {no.get('fonte','?')})", file=sys.stderr)
    return no["valor"]

# ── K-03: custodia progressiva de verdade ─────────────────────────────────────
# as duas leituras que a fonte admite -- custos.yaml, b3.custodia_rv_interpretacao.nota
INTERPRETACOES_DA_ISENCAO = ("deducao", "limiar")

def custodia_rv_aa(patrimonio, faixas, isencao, interpretacao="deducao"):
    """Taxa anual EM REAIS da custodia de renda variavel da B3.

    As faixas da B3 sao definidas sobre o VALOR EM CUSTODIA (absoluto), nao sobre
    o excedente. A isencao apenas retira os primeiros `isencao` reais da base.
    Confundir os dois sistemas de coordenadas foi o bug que o teste canonico pegou.
    """
    # B-17: a leitura desta escolha passou a vir do YAML. Valor fora das duas leituras
    # que a fonte admite falha aqui -- um erro de digitacao viraria "limiar" calado (A-05).
    if interpretacao not in INTERPRETACOES_DA_ISENCAO:
        raise ValueError(f"custodia_rv_interpretacao = {interpretacao!r}: a fonte admite "
                         f"{INTERPRETACOES_DA_ISENCAO}")
    if patrimonio <= isencao:
        return 0.0
    isento_restante = isencao if interpretacao == "deducao" else 0.0
    total, piso = 0.0, 0.0
    for fx in faixas:
        teto = fx["ate"] if fx["ate"] is not None else float("inf")
        if patrimonio <= piso:
            break
        largura = min(patrimonio, teto) - piso          # parte do patrimonio nesta faixa
        isenta_aqui = min(isento_restante, largura)     # consome a isencao das faixas baixas
        isento_restante -= isenta_aqui
        total += (largura - isenta_aqui) * fx["taxa_aa"]
        piso = teto
    return total

# ── P-43 (24/09/2026): o catalogo e a simulacao da camada de custo SAIRAM daqui ──
# `Rota`, `montar_rotas`, `custo_entrada_pct`, `custo_saida_pct` e `simular` eram um
# TERCEIRO catalogo (T-01) e uma segunda simulacao que so testes chamavam. A medicao da
# sessao B (B-16) mostrou que ela divergia ate 17,4% da de producao porque o F-01 so foi
# corrigido do lado da alocacao, e que a unica leitura de `custodia_rv_interpretacao`
# morava nela (B-17). A simulacao de producao e `alocacao.simular_custo`.

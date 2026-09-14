# -*- coding: utf-8 -*-
"""Aplica a P-77 no alocacao.py. Idempotente: recusa se ja aplicado."""
import io, os, sys

p = sys.argv[1] if len(sys.argv) > 1 else "alocacao.py"
s = io.open(p, encoding="utf-8").read()
if "PONTAS_DIVERGENTES" in s:
    sys.exit("ja aplicado: PONTAS_DIVERGENTES existe em %s" % p)

VELHO = '''def retorno_liquido_aa(r, C, dias_horizonte, patrimonio=0.0):
    """Retorno liquido anual de uma rota de renda fixa/caixa: rendimento do indexador
    vezes o fator que a rota entrega, menos IR da faixa, menos custo de custodia.
    B-08: e este o criterio do G2, nao a ordem alfabetica do id."""
'''

NOVO = '''# ── P-77: as DUAS pontas do imposto, e por que uma funcao so nao expressa as duas ──
PONTAS_DIVERGENTES = "PONTAS_DIVERGENTES"


def regime_tributario(r):
    """Devolve (aliquota_sobre_o_rendimento_ou_None, motivo_ou_None).

    ACHADO P-77, 13/09/2026. A P-13 partiu `isento_ir` em DOIS campos porque o FII
    nao cabia num booleano: o RENDIMENTO distribuido e isento (Lei 11.033/2004 art.
    3o, com >=100 cotistas) e o GANHO e tributado a 20% (Lei 8.668/1993 art. 18),
    sem a isencao mensal de R$20 mil.

    **A P-13 criou o campo e ninguem o leu.** Medido em 13/09: `aliquota_ganho` tem
    ZERO leituras no motor -- as unicas quatro estao em `test_alocacao.py`. A
    correcao anunciada era mudanca de ESQUEMA sem mudanca de COMPORTAMENTO, que e a
    assinatura deste projeto: um arquivo declara um comportamento que o codigo nao
    tem, e os dois concordam por acidente.

    POR QUE NINGUEM VIU, e sao tres camadas:
      1. o FII e `indexador: rv`, e `retorno_liquido_aa` devolve None antes da linha
         do imposto -- entao hoje ele nao erra o numero, ele nao produz numero;
      2. o FII esta BLOQUEADO (`val_recusa` sobre `fii.taxa_administracao`);
      3. as unicas outras rotas com `aliquota_ganho` sao LCI e LCA, e nelas o valor e
         **0,0** -- as duas pontas isentas, onde a diferenca nao aparece.
    Tres coincidencias, e o campo morto atravessou todas.

    QUANDO MORDE: no dia em que existir uma rota de RENDA FIXA cujo ganho seja
    tributado diferente do rendimento -- debenture incentivada e o caso obvio. Ai
    `isento_ir_rendimento: true` zera o imposto INTEIRO e o `aliquota_ganho`
    continua inerte, e o numero sai errado para MENOS.

    O QUE ESTA FUNCAO NAO FAZ, de proposito: nao inventa um modelo de duas pontas.
    `retorno_liquido_aa` modela um instrumento que ACUMULA rendimento -- nele o ganho
    E o rendimento, e nao ha duas pontas a separar. Quando a rota declara pontas
    divergentes, a resposta honesta nao e um numero aproximado: e recusar, dizendo
    por que. P6 -- ausencia de criterio nao vira criterio de exclusao, vira lacuna
    declarada."""
    isento_rend = bool(r.isento_ir_rendimento)
    ag = r.aliquota_ganho
    if ag is None:
        return (0.0 if isento_rend else None), None      # None = usa a tabela geral
    if isento_rend and ag == 0.0:
        return 0.0, None                                  # LCI/LCA: as duas isentas
    if (not isento_rend) and ag == 0.0:
        return None, None                                 # so a tabela geral
    if isento_rend and ag > 0.0:
        return None, ("%s: rendimento isento e ganho a %.1f%% sao DUAS aliquotas, e "
                      "esta funcao modela uma so. Nao ha numero certo a devolver."
                      % (r.id, ag*100))
    return None, ("%s: rendimento tributado pela tabela e ganho a %.1f%% divergem."
                  % (r.id, ag*100))


def retorno_liquido_aa(r, C, dias_horizonte, patrimonio=0.0, motivos=None):
    """Retorno liquido anual de uma rota de renda fixa/caixa: rendimento do indexador
    vezes o fator que a rota entrega, menos IR da faixa, menos custo de custodia.
    B-08: e este o criterio do G2, nao a ordem alfabetica do id.

    `motivos`: dict opcional {rota_id: motivo}. Quando a rota e recusada por pontas
    tributarias divergentes (P-77), o motivo entra aqui em vez de sumir junto com o
    `None` -- porque foi exatamente um `None` calado que escondeu a P-77."""
'''
assert VELHO in s, "regiao de retorno_liquido_aa nao encontrada -- PARE"
s = s.replace(VELHO, NOVO, 1)

VELHO2 = '''    else:                           return None      # renda variavel: nao ha retorno conhecido
    bruto *= r.rendimento_fator
    ir = 0.0 if r.isento_ir else aliquota_ir_rf(C, dias_horizonte)
    liq = bruto*(1-ir)'''
NOVO2 = '''    else:                           return None      # renda variavel: nao ha retorno conhecido
    fixa, motivo = regime_tributario(r)
    if motivo:
        if motivos is not None:
            motivos[r.id] = motivo
        return None
    bruto *= r.rendimento_fator
    ir = fixa if fixa is not None else aliquota_ir_rf(C, dias_horizonte)
    liq = bruto*(1-ir)'''
assert VELHO2 in s, "corpo de retorno_liquido_aa nao encontrado -- PARE"
s = s.replace(VELHO2, NOVO2, 1)

VELHO3 = '''    else: return None
    bruto *= r.rendimento_fator
    ir = 0.0 if r.isento_ir else aliquota_ir_rf(C, dias_horizonte)
    return bruto*(1-ir) - r.interno_aa'''
NOVO3 = '''    else: return None
    fixa, motivo = regime_tributario(r)      # P-77: a mesma regra nos DOIS lugares
    if motivo: return None
    bruto *= r.rendimento_fator
    ir = fixa if fixa is not None else aliquota_ir_rf(C, dias_horizonte)
    return bruto*(1-ir) - r.interno_aa'''
assert VELHO3 in s, "corpo de _marginal_plano nao encontrado -- PARE"
s = s.replace(VELHO3, NOVO3, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("P-77 aplicado em %s" % os.path.abspath(p))

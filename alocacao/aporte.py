# -*- coding: utf-8 -*-
"""
O aporte nao e um numero — e um piso com picos ocasionais.

Critica do usuario em 04/09/2026, e ela expoe um defeito de modelagem que atravessa
tres camadas: "o sistema nao deve considerar o meu aporte mensal uma verdade em
pedra; vai ter meses que vou ter bonus e vou poder aportar mais".

Estava certo. A remuneracao dele tem duas partes de naturezas diferentes:
  fixa       R$7.000 contratados — existe todo mes
  variavel   bonus por meta, valor variavel, PODE NAO SER RECEBIDO

Tratar as duas como uma media mensal e o erro classico de planejamento com renda
variavel: a media existe no papel e nao existe no mes. Um plano construido sobre a
media quebra exatamente no mes em que o bonus nao vem — que e tambem, tipicamente, o
mes em que a meta nao foi batida porque a empresa foi mal, que e o mes em que o
contrato esta mais em risco. As duas incertezas sao CORRELACIONADAS, e e por isso que
a media e pior que inutil aqui: ela e otimista justamente quando nao deveria ser.

PRINCIPIO ADOTADO — e ele resolve os tres pontos de uma vez:

    Todo PLANO e construido sobre o PISO. Todo EXTRAORDINARIO acelera, e nunca
    e planejado. O piso e promessa contratual; o bonus e evento.

Consequencias, uma por camada:

  1. HORIZONTE DA RESERVA deixa de ser uma data e vira uma FAIXA: a data do piso e
     a data com N bonus. A data do piso e a unica que pode ser prometida.

  2. G3 (atrito) passa a ser avaliado sobre o valor QUE ESTA SENDO APORTADO no mes,
     nao sobre o `aporte_mensal` do estado. Num mes de bonus o universo elegivel e
     MAIOR — rota com custo fixo por ordem que nao cabe em R$500 cabe em R$3.000.
     Isso ja estava certo no motor por acidente; agora esta certo por desenho, e
     este modulo mostra em que aporte cada rota entra.

  3. O EXTRAORDINARIO tem regra propria, declarada, em vez de virar decisao ad hoc
     no mes em que o dinheiro cai na conta — que e quando a decisao e pior.
"""
from __future__ import annotations
import os, sys
from dataclasses import dataclass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import carregar as carregar_custos
from alocacao import carregar_politica, catalogo, g3_atrito, g6_coerencia_funcao

@dataclass
class Aporte:
    """A estrutura que substitui o escalar."""
    base: float                       # o piso: o que acontece no mes ruim
    extraordinario_tipico: float = 0.0   # tamanho tipico do bonus, quando vem
    extraordinarios_por_ano: float = 0.0 # quantos por ano, historicamente
    nota: str = ""

    @property
    def media_mensal_aparente(self):
        """Existe so para ser mostrada e RECUSADA como base de plano."""
        return self.base + self.extraordinario_tipico*self.extraordinarios_por_ano/12

def meses_ate(alvo, atual, aporte: Aporte, taxa_mensal, usar_extraordinario=True,
              teto_meses=600):
    """Mes em que a reserva atinge o alvo. Devolve None se nao atingir no teto."""
    saldo, m = atual, 0
    por_ano = aporte.extraordinarios_por_ano if usar_extraordinario else 0.0
    intervalo = (12/por_ano) if por_ano else None
    while saldo < alvo and m < teto_meses:
        m += 1
        saldo = saldo*(1+taxa_mensal) + aporte.base
        if intervalo and m % max(1, round(intervalo)) == 0:
            saldo += aporte.extraordinario_tipico
    return m if saldo >= alvo else None

def faixa_da_reserva(alvo, atual, aporte: Aporte, taxa_mensal):
    """A data deixa de ser um ponto. Devolve (piso, com_extraordinario)."""
    piso = meses_ate(alvo, atual, aporte, taxa_mensal, usar_extraordinario=False)
    com  = meses_ate(alvo, atual, aporte, taxa_mensal, usar_extraordinario=True)
    return dict(mes_no_piso=piso, mes_com_extraordinario=com,
                antecipacao=(piso-com) if (piso and com) else None,
                nota="a data do PISO e a unica que pode ser prometida; a outra e o "
                     "melhor caso e depende de evento que pode nao ocorrer")

def universo_por_aporte(C, P, valores=(100,200,300,500,750,1000,2000,5000,20000)):
    """Em que aporte cada rota entra e sai. E a resposta direta a critica: o universo
    elegivel NAO e fixo — ele e funcao do valor que esta sendo aportado no mes."""
    rotas, _ = g6_coerencia_funcao(catalogo(C), P)
    linhas = []
    for v in valores:
        dentro, fora = g3_atrito(rotas, C, P, v)
        linhas.append(dict(aporte=v,
                           dentro=sorted(r.id for r, _ in dentro),
                           fora_fixo=sorted(r.id for r, e, m, x in fora if m == "FIXO"),
                           fora_pct=sorted(r.id for r, e, m, x in fora if m == "PERCENTUAL")))
    # limiar de entrada por rota
    limiares = {}
    _, fora_min = g3_atrito(rotas, C, P, 1.0)
    for r, e, motivo, reentrada in fora_min:
        limiares[r.id] = dict(motivo=motivo, aporte_de_entrada=reentrada, nome=r.nome)
    return linhas, limiares

def regra_do_extraordinario(P, reserva_completa: bool):
    r = P["aporte_extraordinario"]
    return r["apos_reserva_completa"] if reserva_completa else r["antes_da_reserva_completa"]

if __name__ == "__main__":
    import yaml
    from estado_io import validar
    from reserva import taxa_liquida_reserva
    C, P = carregar_custos(), carregar_politica()
    doc = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "estado.yaml"), encoding="utf-8"))
    e, prob, _ = validar(doc)
    D, R0 = e["despesa_mensal"], e["reserva_atual"]
    g = P["portoes"]["G2_reserva"]
    ALVO = min(g["meses_base"]*g["ajuste_estabilidade"][e["estabilidade_renda"]],
               g["teto_meses"])*D
    t = taxa_liquida_reserva(C, P)

    print("="*92)
    print("1 · A DATA DA RESERVA E UMA FAIXA, NAO UMA DATA")
    print("="*92)
    print(f"alvo R${ALVO:,.2f} · reserva R${R0:,.2f} · rendimento {(1+t)**12-1:.2%} a.a. liquido\n")
    print(f"{'piso mensal':>12}{'sem bonus':>12}{'1 bonus/ano':>14}{'2 bonus/ano':>14}"
          f"{'4 bonus/ano':>14}   (bonus de R$1.500)")
    for base in (300, 500, 750, 1000, 1500):
        col = []
        for n in (0, 1, 2, 4):
            a = Aporte(base=base, extraordinario_tipico=1500, extraordinarios_por_ano=n)
            m = meses_ate(ALVO, R0, a, t, usar_extraordinario=bool(n))
            col.append(f"mes {m}" if m else "nunca")
        print(f"{base:>12}" + "".join(f"{c:>14}" for c in col))
    print("""
  A primeira coluna e a unica que voce pode prometer. As outras tres sao o melhor caso
  e dependem de um evento que, por construcao, falha justamente no ano ruim da empresa
  — que e o mesmo ano em que o contrato esta mais em risco. As duas incertezas andam
  juntas, e por isso a media mensal e otimista exatamente quando nao deveria ser.""")

    print("\n" + "="*92)
    print("2 · O UNIVERSO ELEGIVEL E FUNCAO DO APORTE DO MES")
    print("="*92)
    linhas, limiares = universo_por_aporte(C, P)
    print(f"\n{'aporte':>8}{'rotas elegiveis':>18}   fora por custo FIXO (volta com aporte maior)")
    for L in linhas:
        fx = ", ".join(L["fora_fixo"]) or "—"
        print(f"{L['aporte']:>8}{len(L['dentro']):>18}   {fx}")
    print(f"\n{'rota':<34}{'natureza':>12}{'entra a partir de':>20}")
    for rid, d in sorted(limiares.items(), key=lambda x: (x[1]["motivo"], x[0])):
        v = f"R${d['aporte_de_entrada']:,.0f}" if d["aporte_de_entrada"] else "nunca"
        print(f"{d['nome'][:33]:<34}{d['motivo']:>12}{v:>20}")
    print("""
  Um mes de bonus nao e so 'mais dinheiro no mesmo lugar': ele ABRE ROTAS que o aporte
  base nao alcanca. E por isso que o G3 tem de ser avaliado sobre o valor efetivamente
  aportado no mes, e nao sobre o campo `aporte_mensal` do estado.""")

    print("\n" + "="*92)
    print("3 · A REGRA DO EXTRAORDINARIO")
    print("="*92)
    for fase, completa in (("reserva INCOMPLETA (voce hoje)", False),
                           ("reserva completa", True)):
        r = regra_do_extraordinario(P, completa)
        print(f"\n  {fase}:")
        print(f"    destino: {r['destino']}")
        print(f"    {r['justificativa'].strip()}")

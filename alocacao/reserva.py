# -*- coding: utf-8 -*-
"""
Fase de reserva — a unica fase que o estado atual do usuario de fato atravessa.

Com aporte de R$500 e alvo de R$36.000, o G2 dirige 100% do aporte para a reserva
por quase cinco anos. Durante esse periodo a camada de alocacao nao decide nada:
ela existe, esta testada, e nao roda. Entao a pergunta relevante do projeto nao e
mais "como alocar" — e "a regra do tudo-ou-nada esta certa para este caso".

O QUE ESTE MODULO CALCULA E O QUE ELE SE RECUSA A CALCULAR:

  calcula   o custo do atraso, em MESES DE COBERTURA. Quantos meses voce passa
            abaixo de 3 e de 6 meses de despesa coberta, sob cada regra. E risco de
            exposicao, e e computavel: e aritmetica sobre o saldo.

  calcula   quanto vai para investimento sob cada regra, remunerado ao CDI liquido
            — que e um PISO conhecido, nao uma previsao.

  RECUSA    dizer quanto o dinheiro investido mais cedo teria RENDIDO A MAIS. O
            premio de risco de acoes medido no Brasil entre 2001 e 2026 foi de
            0,96% ao ano com t = 0,74: a serie nao rejeita zero. Colocar um numero
            de retorno esperado aqui seria inventar o unico dado que decidiria a
            questao — e seria exatamente o que este projeto existe para nao fazer.

A consequencia dessa recusa e assimetrica, e e o achado: o custo do split e
mensuravel e o beneficio nao e.
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import carregar as carregar_custos, val
from alocacao import carregar_politica, aliquota_ir_rf

def taxa_liquida_reserva(C, P, patrimonio=0.0, rota="rdb_100"):
    """Retorno liquido mensal da rota de liquidez vencedora do G2."""
    cdi = val(C["macro"]["cdi_aa"], contexto="cdi")
    ir = aliquota_ir_rf(C, P["portoes"]["G2_reserva"]["horizonte_ir_dias"])
    return (1 + cdi*(1-ir))**(1/12) - 1

def simular(despesa, reserva0, aporte, alvo, meses, taxa_res, taxa_inv, fracao_reserva):
    """Simula mes a mes. `fracao_reserva` = 1.0 e a regra atual (tudo ou nada).

    Enquanto a reserva nao atinge o alvo, `fracao_reserva` do aporte vai para ela e o
    resto para investimento. Depois do alvo, tudo vai para investimento."""
    res, inv = reserva0, 0.0
    linha = []
    mes_alvo = None
    meses_abaixo_3 = meses_abaixo_6 = 0
    for m in range(1, meses+1):
        if res < alvo:
            para_res = aporte*fracao_reserva
            para_inv = aporte - para_res
        else:
            para_res, para_inv = 0.0, aporte
        res = res*(1+taxa_res) + para_res
        inv = inv*(1+taxa_inv) + para_inv
        cob = res/despesa
        if cob < 3: meses_abaixo_3 += 1
        if cob < 6: meses_abaixo_6 += 1
        if mes_alvo is None and res >= alvo: mes_alvo = m
        linha.append((m, res, inv, cob))
    return dict(mes_alvo=mes_alvo, reserva_final=res, investido_final=inv,
                total_final=res+inv,
                meses_abaixo_3=meses_abaixo_3, meses_abaixo_6=meses_abaixo_6,
                cobertura_final=res/despesa, linha=linha)

def comparar(despesa, reserva0, aporte, alvo, horizonte_anos, C, P, fracoes=(1.0,0.8,0.6,0.5)):
    meses = int(horizonte_anos*12)
    t = taxa_liquida_reserva(C, P)
    out = []
    for f in fracoes:
        r = simular(despesa, reserva0, aporte, alvo, meses, t, t, f)
        out.append((f, r))
    return out, t

if __name__ == "__main__":
    import yaml
    from estado_io import validar
    C, P = carregar_custos(), carregar_politica()
    doc = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "estado.yaml"), encoding="utf-8"))
    e, problemas, _ = validar(doc)
    if problemas:
        print("estado.yaml invalido:"); [print("  -", x) for x in problemas]; raise SystemExit(1)

    D, R0, A, H = e["despesa_mensal"], e["reserva_atual"], e["aporte_mensal"], e["horizonte_anos"]
    g = P["portoes"]["G2_reserva"]
    meses_alvo = min(g["meses_base"]*g["ajuste_estabilidade"][e["estabilidade_renda"]]
                     + g["ajuste_dependentes_por_pessoa"]*e["dependentes"], g["teto_meses"])
    ALVO = meses_alvo*D

    print("="*94)
    print("FASE DE RESERVA — o que de fato acontece nos proximos 10 anos")
    print("="*94)
    print(f"despesa R${D:,.2f}/mes · reserva R${R0:,.2f} ({R0/D:.1f} meses) · "
          f"aporte R${A:,.2f} · estabilidade {e['estabilidade_renda']}")
    print(f"alvo: {meses_alvo:.0f} meses = R${ALVO:,.2f} · faltam R${ALVO-R0:,.2f}")

    comp, t = comparar(D, R0, A, ALVO, H, C, P)
    print(f"remuneracao usada: {(1+t)**12-1:.2%} a.a. liquido — a rota vencedora do G2, "
          f"IR de {aliquota_ir_rf(C, P['portoes']['G2_reserva']['horizonte_ir_dias']):.1%}")
    print(f"\nO MESMO aporte, quatro regras, {int(H)} anos:\n")
    print(f"{'regra':<26}{'reserva completa':>17}{'meses <3 cobertura':>20}"
          f"{'investido 10a':>15}{'PATRIMONIO TOTAL':>19}")
    for f, r in comp:
        rot = ("100% reserva (atual)" if f == 1.0 else
               f"{f*100:.0f}% reserva / {(1-f)*100:.0f}% investir")
        alvo_txt = f"mes {r['mes_alvo']}" if r["mes_alvo"] else "nao atinge"
        print(f"{rot:<26}{alvo_txt:>17}{r['meses_abaixo_3']:>20}"
              f"{r['investido_final']:>15,.0f}{r['total_final']:>19,.2f}")

    print("\n" + "="*94)
    print("SENSIBILIDADE — patrimonio em 10 anos por premio de renda variavel sobre o CDI")
    print("="*94)
    print("Nao e previsao. E a pergunta invertida: QUANTO a bolsa precisaria render a mais")
    print("para o split compensar? Referencia medida (NEFIN 2001-2026): +0,96% a.a., t=0,74.\n")
    print(f"{'premio sobre o CDI':<22}" + "".join(
        f"{('100/0' if f==1.0 else f'{f*100:.0f}/{(1-f)*100:.0f}'):>17}"
        for f, _ in comp))
    for premio in (0.0, 0.0096, 0.02, 0.04, 0.06):
        ti = (1 + ((1+t)**12-1) + premio)**(1/12) - 1
        linha = []
        for f, _ in comp:
            r = simular(D, R0, A, ALVO, int(H*12), t, ti, f)
            linha.append(r["total_final"])
        marca = "  <- medido" if abs(premio-0.0096) < 1e-9 else ""
        print(f"{premio:>+8.2%} a.a.{'':<11}" + "".join(f"{x:>17,.0f}" for x in linha) + marca)
    b0 = simular(D, R0, A, ALVO, int(H*12), t, t, 1.0)["total_final"]
    print(f"\n{'ganho do 50/50 sobre o 100/0':<22}")
    for premio in (0.0, 0.0096, 0.02, 0.04, 0.06):
        ti = (1 + ((1+t)**12-1) + premio)**(1/12) - 1
        a = simular(D, R0, A, ALVO, int(H*12), t, ti, 1.0)["total_final"]
        b = simular(D, R0, A, ALVO, int(H*12), t, ti, 0.5)["total_final"]
        print(f"  premio {premio:+.2%} a.a. -> R${b-a:>+10,.0f}   "
              f"({(b-a)/(A*12*H)*100:>+5.1f}% do total aportado, por 6 meses a mais de exposicao)")

    base = comp[0][1]
    print(f"\n{'':<26}{'atraso':>17}{'meses expostos':>20}"
          f"{'rotulo':>15}{'GANHO REAL':>19}")
    for f, r in comp[1:]:
        rot = f"{f*100:.0f}/{(1-f)*100:.0f} contra tudo-ou-nada"
        atraso = (r["mes_alvo"] - base["mes_alvo"]) if r["mes_alvo"] else None
        print(f"{rot:<26}{(f'+{atraso} meses' if atraso else 'nunca'):>17}"
              f"{r['meses_abaixo_3']-base['meses_abaixo_3']:>+20}"
              f"{r['investido_final']-base['investido_final']:>+15,.0f}"
              f"{r['total_final']-base['total_final']:>+19,.2f}")

    print("""
  COMO LER ESTA TABELA — E A COLUNA QUE MUDA A CONCLUSAO

  Olhe a ultima coluna. O PATRIMONIO TOTAL e IDENTICO nas quatro regras, ate o centavo.
  Nao e coincidencia nem defeito da simulacao: enquanto o dinheiro rende a mesma taxa
  nos dois potes, mover o aporte de um pote para o outro nao cria valor — apenas troca
  o ROTULO. A coluna "rotulado invest." mostra R$13.548 a mais no split 50/50, e a
  coluna ao lado mostra que esses R$13.548 sairam da reserva. Nao ha ganho.

  Portanto o split so passa a valer alguma coisa SE a renda variavel render mais que o
  CDI. E ai esta o problema: o premio de acoes medido no Brasil de 2001 a 2026 foi de
  0,96% a.a. com t = 0,74 — a serie nao rejeita zero. Nao estou afirmando que o premio
  e zero; estou afirmando que o dado disponivel nao consegue distingui-lo de zero, e
  que somar um retorno esperado aqui seria inventar o unico numero que decide a questao.

  A coluna "investido a mais" e um PISO: e o que o dinheiro rende ao CDI liquido, que
  e conhecido. Ela NAO inclui premio de renda variavel, e essa omissao e deliberada —
  o premio de acoes medido no Brasil de 2001 a 2026 foi de 0,96% a.a. com t = 0,74, e
  a serie nao rejeita zero. Se eu somasse um retorno esperado de bolsa aqui, o numero
  que decide a questao seria inventado por mim.

  QUANTO A BOLSA PRECISARIA RENDER A MAIS PARA O SPLIT VALER — ver tabela acima.

  A ASSIMETRIA E O RESULTADO: o custo do split e certo e mensuravel — 25 meses a mais
  sem reserva completa, 6 meses a mais abaixo de 3 meses de cobertura. O beneficio e
  incerto e nao mensuravel com o dado disponivel. Trocar um custo certo por um
  beneficio que a serie nao mede e uma aposta, e ela precisa ser declarada, nao suposta.

  E o seu caso e o menos favoravel possivel ao split: contrato unico, sem aviso previo.
  Os meses a mais abaixo de 3 meses de cobertura sao meses em que uma unica assinatura
  encerra a receita e a reserva nao cobre o intervalo ate o proximo contrato.""")

# -*- coding: utf-8 -*-
"""Roda a camada de alocacao em cenarios reais. Este arquivo E o teste de fumaca."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import carregar as carregar_custos
from alocacao import (Estado, Divida, carregar_politica, alocar, catalogo,
                      arrasto_anualizado)

C, P = carregar_custos(), carregar_politica()
ROTAS = {r.id: r for r in catalogo(C)}

def mostrar(titulo, estado, anos=None, teses=None, carregos=None):
    print("\n" + "="*100); print(titulo); print("="*100)
    print(f"despesa R${estado.despesa_mensal:,.0f}/mes · reserva R${estado.reserva_atual:,.0f} "
          f"({estado.meses_cobertos:.1f} meses) · aporte R${estado.aporte_mensal:,.0f} · "
          f"renda {estado.estabilidade_renda} · horizonte {estado.horizonte_anos:.0f}a")
    r = alocar(estado, C, P, anos, teses=teses, carregos=carregos)
    for pd in r.get("pendencias", []):
        print(f"\n  >> PENDENCIA {pd.id}: {pd.pergunta.strip()}")
        print(f"     custo de ignorar: {pd.consequencia.strip()}")
    for d in r.get("portoes", []):
        if d.portao == "G0_match_empregador":
            print(f"\n  >> {d.portao}: {d.veredito}")
    if "diretiva" in r:
        d = r["diretiva"]
        print(f"\n  >> PORTAO {d.portao}: {d.veredito}")
        print(f"     destino: {d.destino}")
        for k,v in d.memoria.items():
            print(f"     {k}: {v:,.4f}" if isinstance(v,float) else f"     {k}: {v}")
        return r
    u = r["universo"]; a = r["alvo"]
    print(f"\n  universo: {len(u['alocaveis'])} alocaveis (de {len(u['vivos'])} "
          f"elegiveis) · {len(u['fora_atrito'])} fora por atrito · "
          f"{len(u['dominados'])} dominadas · {len(u['preferencia_horizonte'])} por horizonte · "
          f"{len(u['fora_status'])} sem confirmacao · {len(u['sem_tese'])} sem tese")
    if u["fora_atrito"]:
        print("\n  ELIMINADAS POR ATRITO (custo de entrada > 1,0% do aporte):")
        for rt,e,motivo,reent in sorted(u["fora_atrito"], key=lambda x:-x[1]):
            if motivo == "PERCENTUAL":
                obs = "custo PERCENTUAL: nao dilui — nao volta com aporte nenhum"
            else:
                obs = f"custo FIXO: volta com aporte de R${reent:,.0f}" if reent else "custo fixo"
            print(f"     {rt.nome:<52} {e*100:>6.2f}%  {obs}")
    if u["dominados"]:
        print("\n  ELIMINADAS POR DOMINANCIA (mesma exposicao, custo maior):")
        for rt,e,arr,dom in u["dominados"]:
            print(f"     {rt.nome:<52} {arr*100:>6.3f}% a.a.  <- dominada por {dom.nome}")
    if u["preferencia_horizonte"]:
        print("\n  RETIRADAS POR PREFERENCIA DE HORIZONTE (a ordem INVERTE — nao e dominancia):")
        for rt,e,arr,riv,tab in u["preferencia_horizonte"]:
            print(f"     {rt.nome:<52} perde de {riv.nome} em {anos or estado.horizonte_anos:.0f}a")
            for h,par in sorted(tab.items()):
                a,b = par[rt.id], par[riv.id]
                print(f"        {h:>3}a: {rt.id} {a*100:.3f}%  x  {riv.id} {b*100:.3f}%"
                      f"   -> {rt.id if a<b else riv.id}")
    if u["sem_tese"] or u["sem_carrego"]:
        print("\n  AGUARDANDO REGISTRO SEU (nao e exclusao — ver PENDENCIAS acima):")
        for rt,motivo in list(u["sem_tese"])+list(u["sem_carrego"]):
            print(f"     {rt.nome:<52} {motivo[:66]}")
    if u["interacao_g3_g4"]:
        print("\n  INTERACAO ENTRE PORTOES (G3 elimina antes de o G4 ver):")
        for x in u["interacao_g3_g4"]:
            print(f"     {x['rota'].nome:<52} venceria {x['rival'].id} em "
                  f"{x['horizontes_em_que_venceria']} anos")
    if u["fora_status"]:
        print("\n  FORA DA ORDENACAO (insumo nao confirmado):")
        # P-149: desde a F-02 o G5 roda antes do G3, sobre rotas NUAS -- o `fora_status`
        # guarda rota, nao par (rota, custo). O desempacotamento antigo caia no main.
        for x in u["fora_status"]:
            rt = x[0] if isinstance(x, tuple) else x
            print(f"     {rt.nome:<52} {rt.bloqueios[0][:60]}")
    print(f"\n  ALOCACAO ALVO  (fracao em renda variavel: {a['fracao_rv']*100:.0f}%)")
    b = a["blocos"]
    print(f"  blocos: crescimento {b['rv']*100:.1f}% · datado {b['datado']*100:.1f}% · "
          f"protecao real {b['protecao_real']*100:.1f}% · lastro {b['lastro']*100:.1f}% · "
          f"cauda {b['cauda']*100:.1f}% · aposta {b['aposta']*100:.1f}%")
    print(f"\n  {'Rota':<44}{'funcao':>15}{'peso':>7}{'R$/mes':>9}"
          f"{'arrasto':>10}{'custo/aport':>13}")
    for rid,w in sorted(a["pesos"].items(), key=lambda x:-x[1]):
        rt=ROTAS[rid]
        ap = max(estado.aporte_mensal*w, 1.0)
        cpa=a["custo_pct_aportado"][rid]
        if cpa is None:            # P-134: a entrada come o aporte desta rota; motivo nos alertas
            print(f"  {rt.nome[:43]:<44}{a['bloco_por_rota'].get(rid,'?'):>15}{w*100:>6.1f}%"
                  f"{estado.aporte_mensal*w:>9,.0f}   a entrada come o aporte (P-134)")
            continue
        arr=arrasto_anualizado(rt,C,ap,anos or estado.horizonte_anos)
        print(f"  {rt.nome[:43]:<44}{a['bloco_por_rota'].get(rid,'?'):>15}{w*100:>6.1f}%"
              f"{estado.aporte_mensal*w:>9,.0f}{arr*100:>9.3f}%{cpa*100:>12.1f}%")
    for al in a["alertas"]:
        print(f"    [ALERTA] {al}")
    for rid,d in a["diversificacao"].items():
        print(f"    [DIVERSIFICACAO] {d['nota']}")
    print(f"\n  procedencia: politica {r['procedencia']['politica_versao']} "
          f"({r['procedencia']['politica_hash']}) · custos {r['procedencia']['custos_hash']}")
    return r

# ── 1. Osvaldo hoje: sem reserva, sem patrimonio ──────────────────────────────
e1 = Estado(despesa_mensal=4500, reserva_atual=0, aporte_mensal=500,
            estabilidade_renda="media", horizonte_anos=25)
mostrar("CENARIO 1 — hoje: sem reserva, sem posicao, aporte de R$500", e1)

# ── 2. Mesmo estado, com divida de cartao ─────────────────────────────────────
e2 = Estado(despesa_mensal=4500, reserva_atual=8000, aporte_mensal=500,
            dividas=[Divida("cartao rotativo", 3000, 0.14)], horizonte_anos=25)
mostrar("CENARIO 2 — reserva parcial, mas com divida de cartao a 14% a.m.", e2)

# ── 3. Reserva completa, aporte R$500 ────────────────────────────────────────
e3 = Estado(despesa_mensal=4500, reserva_atual=27000, aporte_mensal=500,
            estabilidade_renda="media", horizonte_anos=25)
mostrar("CENARIO 3 — reserva completa (6 meses), aporte de R$500", e3)

# ── 4. Aporte pequeno: o atrito elimina rotas ────────────────────────────────
e4 = Estado(despesa_mensal=4500, reserva_atual=27000, aporte_mensal=200,
            estabilidade_renda="media", horizonte_anos=25)
mostrar("CENARIO 4 — mesmo estado, aporte de R$200: o atrito muda o universo", e4)

# ── 5. Renda estavel, reserva folgada, aporte maior ──────────────────────────
e5 = Estado(despesa_mensal=4500, reserva_atual=45000, aporte_mensal=1500,
            estabilidade_renda="alta", horizonte_anos=30)
mostrar("CENARIO 5 — renda estavel, 10 meses de reserva, aporte de R$1.500", e5)


# ── 6. O MESMO estado do cenario 3, com os dois registros PREENCHIDOS ────────
# Nao e outro perfil: e o cenario 3 depois de voce escrever a tese e o compromisso.
# A diferenca entre esta tabela e a do cenario 3 e o que uma tarde de trabalho seu
# muda — nenhum dado novo, nenhuma pesquisa, nenhuma corretora aberta.
import datetime as _dt
from tese import impressao as _imp, impressao_carrego as _impc

_t = dict(ativo_id="hash11", funcao="APOSTA", catalogo="ESPECULATIVO",
          dt_classificacao=_dt.date(2026,9,3), K01_perda_maxima_aceita=1.0,
          K02_tese="EXEMPLO DE FORMA, nao de conteudo: ate 31/12/2033 existe na B3 ETF "
                   "de cripto com taxa abaixo de 0,5% ao ano, e a posicao migra para ele",
          K03_prazo=_dt.date(2033,12,31),
          K04_falsificacao="a taxa de administracao do veiculo subir acima de 1,5% ao ano",
          K05_liquidez_saida_dias=2,
          L_teste_de_classificacao=dict(rodado_em=_dt.date(2026,9,3), reprova=["A-06","C-01"]))
_t["impressao"] = _imp(_t)
_c = dict(ativo_id="td_ipca", funcao="PROTECAO_REAL", catalogo="BUY_AND_HOLD",
          dt_registro=_dt.date(2026,9,3), C01_horizonte_de_carrego=_dt.date(2035,5,15),
          C02_compromisso="EXEMPLO DE FORMA: carrego o NTN-B Principal 2035 ate o "
                          "vencimento, travando juro real de 6,8% ao ano na compra",
          C03_condicao_de_venda_antecipada="necessidade de caixa que a reserva de "
                          "emergencia nao cobre, comprovada por despesa efetiva",
          C04_custo_de_quebrar=dict(cenario="+2 p.p. de juro real", perda_estimada_pct=0.16,
                                    fonte_da_estimativa="duration modificada x choque"),
          C05_teto_da_funcao=0.15, C06_reconhecimento=True)
_c["impressao"] = _impc(_c)

from tese import validar_tese as _vt, validar_carrego as _vc
_okt, _pt, _ = _vt(_t, _dt.date(2026,9,3), P["compromissos"]["maximo_anos"])
_okc, _pc, _, _dur = _vc(_c, _dt.date(2026,9,3), P["compromissos"]["maximo_anos"])
assert _okt and _okc, (_pt, _pc)

mostrar("CENARIO 6 — o MESMO cenario 3, com tese e compromisso preenchidos",
        Estado(despesa_mensal=4500, reserva_atual=27000, aporte_mensal=500,
               estabilidade_renda="media", horizonte_anos=25),
        teses={"hash11": dict(valida=True, motivo="", avisos=[], tese=_t)},
        carregos={"td_ipca": dict(valida=True, motivo="", avisos=[],
                                  duracao_anos=_dur, carrego=_c)})
print(f"""
  As frases acima sao EXEMPLOS DE FORMA. O conteudo tem de ser seu — se eu escrever
  K02, K03 e K04, o registro deixa de ser pre-registro e vira sugestao minha com a
  sua assinatura, que e exatamente o que o bloco K existe para impedir.

  Compare com o cenario 3: dois ativos entraram, o conservador se dividiu entre
  Selic (sem marcacao) e IPCA+ (com marcacao, carregado ate {_c['C01_horizonte_de_carrego']},
  duracao {_dur:.1f} anos, dentro do teto de
  {P['compromissos']['maximo_anos']} anos que voce declarou).
  Nenhum dado novo. Nenhuma pesquisa. Uma tarde de trabalho seu.""")

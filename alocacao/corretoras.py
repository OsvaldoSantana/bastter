# -*- coding: utf-8 -*-
"""
Ranking de corretoras — derivado, nao asserido.

O laudo anterior (04/09) recusou-se a ordenar as oito corretoras de corretagem zero
alegando que "nao tenho criterio que as separe". Estava errado por preguica: a
pesquisa de 31/08-01/09 tem quatro dimensoes que separam, e uma delas e a mais
importante de todas para um horizonte de 10 anos.

AS DIMENSOES, e por que cada uma:

  corretagem      Onde o custo estaria, se houvesse. Oito zeram; o empate e real e a
                  dimensao sozinha nao decide nada. Mantida porque a que NAO zera
                  (Caixa, Safra, Terra, XP swing) e eliminada aqui e nao adiante.

  custodia_b3     0,05% a.a. acima de R$26.471,77. Quem absorve elimina o custo; quem
                  nao declara, repassa. Para uma carteira que chega a R$100 mil em 10
                  anos, e a diferenca entre pagar ~R$50/ano e zero.

  tesouro_zero    Taxa PROPRIA da instituicao no Tesouro Direto (a da B3, 0,20%, e
                  inescapavel). So alguns confirmam zero.

  solidez         PL e resultado do BCB IF.data 03/2026. Nao e vaidade: e a
                  probabilidade de a instituicao existir daqui a 10 anos.

  sobrevivencia   O achado que reordena tudo. Em 6 anos, 7 das 25 marcas pesquisadas
                  deixaram de existir como entidade independente (Rico, Clear,
                  modalmais, Necton, Orama, Guide, Vitreo) e 1 foi reposicionada
                  (Toro). O BC liquidou 17 instituicoes em 2025-2026, das quais pelo
                  menos 6 corretoras/DTVMs. Com horizonte de 10 anos, escolher uma
                  corretora e apostar que ela existira — e a taxa-base de eventos
                  societarios no setor brasileiro NAO e baixa.

  confirmacao     Status da fonte: C (confirmado em pagina oficial), P (parcial),
                  N (nao obtido). Uma instituicao cujo custo nao pode ser lido nao
                  entra no topo do ranking, por melhor que pareca. Isso e o G5 do
                  sistema aplicado a uma decisao de vida real: dado nao confirmado
                  nao entra em ordenacao.

O QUE O RANKING NAO FAZ: nao pontua atendimento, aplicativo, research, nem nota de
Reclame Aqui — a pesquisa registrou que nao conseguiu ler nenhuma nota literal, e
inventar uma seria pior que a lacuna.
"""
from __future__ import annotations
import os, sys
from dataclasses import dataclass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from alocacao import carregar_politica

AQUI = os.path.dirname(os.path.abspath(__file__))

@dataclass
class Instituicao:
    id: str
    nome: str
    corretagem_rv: float | None      # R$ por ordem no autoatendimento; None = nao confirmado
    corretagem_pct: float = 0.0      # parte percentual, se houver
    custodia_absorvida: bool | None = None
    tesouro_taxa_propria_zero: bool | None = None
    pl_conglomerado: float | None = None      # R$ milhoes, BCB IF.data 03/2026
    pl_entidade: float | None = None
    resultado_trimestre: float | None = None
    entidade_independente: bool = True
    evento_societario: str = ""
    confirmacao: str = "C"           # C | P | N
    pegadinha: str = ""
    fonte: str = ""
    # ── reclamacoes: Ranking do BC, 2T/2026 (fonte primaria) ──────────────────
    bc_indice: float | None = None       # procedentes por milhao de clientes
    bc_procedentes: int | None = None
    bc_clientes: int | None = None
    bc_posicao: int | None = None
    # ── Reclame Aqui: exibido, NAO pontuado ───────────────────────────────────
    ra_nota: float | None = None
    ra_solucao: float | None = None
    ra_voltaria: float | None = None
    ra_reclamacoes: int | None = None
    # ── custo por operacao, detalhado ─────────────────────────────────────────
    corretagem_fii: float | None = None      # None = mesma da acao
    corretagem_etf_pct: float = 0.0          # XP cobra 0,50% em ETF
    exercicio_opcao_pct: float | None = None
    mesa_minimo: float | None = None
    # ── facilidade: proxies objetivos ─────────────────────────────────────────
    home_broker_web: bool | None = None
    exporta_csv: bool | None = None

INSTITUICOES_YAML = os.path.join(AQUI, "instituicoes.yaml")

STATUS_PARA_LETRA = {"COMPLETO": "C", "PARCIAL": "P", "NAO_CONFIRMADO": "N"}

# Os grupos existem porque as FONTES se agrupam assim, nao por gosto de organizacao:
# custos vem da pagina da casa, balanco vem do BCB IF.data, reclamacoes vem do ranking
# do BC. Ver achado Q-02 no cabecalho do instituicoes.yaml.
GRUPOS_DE_CAMPOS = ("custos", "balanco", "reclamacoes", "reclame_aqui",
                    "societario", "facilidade")

_INSTITUICOES_CRU: dict[str, dict] = {}


def carregar_instituicoes_cru(path=None):
    p = path or INSTITUICOES_YAML
    if p not in _INSTITUICOES_CRU:
        with open(p, encoding="utf-8") as f:
            _INSTITUICOES_CRU[p] = yaml.safe_load(f)
    return _INSTITUICOES_CRU[p]


def catalogo_instituicoes(path=None):
    """Le o instituicoes.yaml. Pendencia P-36, metade B.

    Ate 05/09/2026 estas 24 casas eram 136 linhas de literais Python, com ~15 campos
    medidos cada e `fonte=` inline — dado de pesquisa dentro de codigo, fora de todo o
    aparato de procedencia do custos.yaml.

    ACHADO Q-02: `confirmacao` era um campo proprio, uma letra por instituicao, e
    `pontuar()` a aplica como multiplicador de TUDO. Mas ela sempre significou "os
    CUSTOS podem ser lidos em fonte oficial" — a `regra` do multiplicador em
    politica.yaml diz isso literalmente. BTG e Bradesco tem `N` e balanco vindo do
    Banco Central: o comportamento estava certo, o registro e que nao sabia dizer.

    Agora a procedencia e POR GRUPO, e `confirmacao` e DERIVADA de
    `custos.procedencia.status`. Dois campos que podiam discordar viraram um."""
    d = carregar_instituicoes_cru(path)
    out = []
    for iid, cru in d["instituicoes"].items():
        campos = {k: v for k, v in cru.items() if k not in GRUPOS_DE_CAMPOS}
        proc = {}
        for g in GRUPOS_DE_CAMPOS:
            bloco = cru.get(g)
            if not bloco: continue
            proc[g] = bloco["procedencia"]
            campos.update({k: v for k, v in bloco.items() if k != "procedencia"})
        st = proc["custos"]["status"]
        if st not in STATUS_PARA_LETRA:
            raise ValueError(f"{iid}: status de custos desconhecido {st!r}")
        campos["confirmacao"] = STATUS_PARA_LETRA[st]
        campos["fonte"] = proc["custos"]["fonte"]
        out.append(Instituicao(id=iid, **campos))
    return out


def procedencia_de(iid, path=None):
    """A procedencia por grupo, que a dataclass NAO carrega.

    `Instituicao` guarda um `fonte` so, herdado do formato antigo — o dos custos. Quem
    quiser saber de onde veio o BALANCO de uma casa pergunta aqui, e nao ao objeto: o
    objeto e o que o ranking consome, este dict e o que a auditoria le."""
    return carregar_instituicoes_cru(path)["instituicoes"][iid]


_POLITICA: dict | None = None

def regras(P=None):
    """ACHADO N-01 (05/09/2026). Tres regras de pontuacao estavam escritas DUAS vezes:
    como texto no politica.yaml e como literal aqui. Concordavam — e por isso o defeito
    era invisivel. Editar o YAML nao mudava o ranking, e a secao `corretora` do YAML
    prometia um comportamento que so o Python decidia. E o mesmo achado do F-05
    (`bloqueia` era prosa), aplicado a outra secao.

    Agora ha uma fonte so. Se o YAML disser outra coisa, o ranking muda."""
    global _POLITICA
    if P is None:
        if _POLITICA is None: _POLITICA = carregar_politica()
        P = _POLITICA
    c = P["corretora"]
    mult = {k: float(v) for k, v in c["multiplicador_de_confirmacao"].items()
            if k in ("C", "P", "N")}
    if set(mult) != {"C", "P", "N"}:
        raise ValueError(f"multiplicador_de_confirmacao incompleto: {sorted(mult)}")
    if c["reclame_aqui"]["pontua"]:
        raise NotImplementedError(
            "politica.yaml diz corretora.reclame_aqui.pontua: true, e o Reclame Aqui NAO "
            "entra em nenhuma dimensao de pontuar(). Preferimos parar a entregar um "
            "ranking que ignora em silencio o que o arquivo mandou.")
    if c["facilidade"]["pontua"]:
        raise NotImplementedError(
            "politica.yaml diz corretora.facilidade.pontua: true, e nao ha dimensao de "
            "facilidade em pontuar() — a pesquisa de 31/08 nao obteve proxy objetivo.")
    if c["promocional"]["peso"] != 0:
        # Campo morto ate 11/09 (auditoria de 10/09): trocar o peso no YAML nao mudava
        # nada. O zero e DECISAO declarada; outro valor exige a dimensao em pontuar().
        raise NotImplementedError(
            "politica.yaml diz corretora.promocional.peso != 0, e nao ha dimensao de "
            "promocao em pontuar(). Mudar o numero sem implementar a dimensao seria um "
            "ranking que ignora em silencio o que o arquivo mandou.")
    return dict(mult=mult,
                indice_nota_zero=float(c["reclamacoes"]["escala_indice_para_nota_zero"]),
                custo_nota_zero=float(c["corretagem"]["custo_do_aporte_para_nota_zero"]))


def pontuar(inst: Instituicao, pesos: dict, aporte: float, horizonte_anos: float, P=None):
    R = regras(P)
    """Pontuacao 0-100 por dimensao, ponderada. Toda regra aqui e aritmetica sobre o
    dado da pesquisa — nenhuma e impressao."""
    d: dict[str, float | None] = {}
    notas: list[str] = []

    # corretagem: custo da ordem como % do aporte, invertido
    if inst.corretagem_rv is None:
        d["corretagem"] = None
        notas.append("corretagem NÃO CONFIRMADA")
    else:
        custo = inst.corretagem_rv/aporte + inst.corretagem_pct
        d["corretagem"] = max(0.0, 100*(1 - custo/R["custo_nota_zero"]))
        if custo > 0:
            notas.append(f"corretagem consome {custo*100:.2f}% de um aporte de R${aporte:,.0f}")

    d["custodia"] = (100.0 if inst.custodia_absorvida else
                     0.0 if inst.custodia_absorvida is False else None)
    d["tesouro"] = (100.0 if inst.tesouro_taxa_propria_zero else
                    0.0 if inst.tesouro_taxa_propria_zero is False else None)

    # solidez: log do PL, normalizado. Diferenca de ordem de grandeza importa; de 10% nao.
    import math
    pl = inst.pl_conglomerado or inst.pl_entidade
    if pl is None or pl <= 0:
        d["solidez"] = None
    else:
        # P-40: calculado num local e atribuido UMA vez. O mypy nao conseguia provar
        # que `d["solidez"]` nao era None na linha do `*= 0.5` — e ele estava certo
        # sobre o TIPO ainda que errado sobre o VALOR. Reescrever assim custa uma
        # linha e torna a garantia verificavel em vez de argumentavel.
        solidez = max(0.0, min(100.0, 100*(math.log10(pl) - 1.5)/(math.log10(250000) - 1.5)))
        if inst.resultado_trimestre is not None and inst.resultado_trimestre < 0:
            solidez *= 0.5
            notas.append(f"PREJUÍZO de R${abs(inst.resultado_trimestre):,.1f} mi no trimestre")
        d["solidez"] = solidez

    # sobrevivencia: entidade que ja deixou de existir como independente pontua zero
    # reclamacoes: indice do BC ja normalizado por milhao de clientes.
    # Escala declarada: indice 0 -> 100 pontos; indice 100 -> 0 pontos.
    if inst.bc_indice is None:
        d["reclamacoes"] = None
    else:
        d["reclamacoes"] = max(0.0, 100*(1 - inst.bc_indice/R["indice_nota_zero"]))
        if inst.bc_posicao and inst.bc_posicao <= 5:
            notas.append(f"{inst.bc_posicao}º MAIS reclamado do Brasil no ranking do BC "
                         f"(2T/2026): {inst.bc_indice:.2f} procedentes por milhão de clientes")

    d["sobrevivencia"] = 100.0 if inst.entidade_independente else 0.0
    if inst.evento_societario:
        notas.append(inst.evento_societario)

    # confirmacao: e um MULTIPLICADOR, nao uma dimensao — o G5 aplicado a vida real
    mult = R["mult"][inst.confirmacao]

    validas = {k: v for k, v in d.items() if v is not None}
    if not validas:
        return dict(total=0.0, dim=d, notas=notas, multiplicador=mult,
                    motivo="nenhuma dimensão pôde ser avaliada")
    peso_total = sum(pesos[k] for k in validas)
    bruto = sum(validas[k]*pesos[k] for k in validas)/peso_total
    # dimensao ausente e penalidade, nao neutralidade: quem nao publica, perde
    cobertura = peso_total/sum(pesos.values())
    return dict(total=bruto*mult*cobertura, bruto=bruto, dim=d, notas=notas,
                multiplicador=mult, cobertura=cobertura)

def reclame_aqui(inst: Instituicao, P=None):
    """N-01. `corretora.reclame_aqui.exibe: true` era a ultima frase da secao que nao
    virava nada: o YAML mandava EXIBIR o Reclame Aqui — sem pontuar — e a saida nao o
    exibia em lugar nenhum. Exibir e o ponto: a divergencia entre as duas fontes e a
    informacao (o Itau tem 8,1 no RA e e o 3o mais reclamado do Brasil no ranking do
    BC). Esconder o dado que discorda e escolher a fonte que agrada.

    Devolve None quando o arquivo manda nao exibir, ou quando nao ha dado."""
    global _POLITICA
    if P is None:
        if _POLITICA is None: _POLITICA = carregar_politica()
        P = _POLITICA
    if not P["corretora"]["reclame_aqui"]["exibe"]: return None
    if inst.ra_nota is None: return None
    return dict(nota=inst.ra_nota, solucao=inst.ra_solucao, voltaria=inst.ra_voltaria,
                reclamacoes=inst.ra_reclamacoes,
                diverge_do_bc=bool(inst.bc_posicao and inst.bc_posicao <= 10
                                   and inst.ra_nota >= 7.0))


def ranking(pesos, aporte=500.0, horizonte_anos=10.0, apenas_viaveis=True, P=None):
    out = []
    for i in catalogo_instituicoes():
        p = pontuar(i, pesos, aporte, horizonte_anos, P)
        out.append((i, p))
    out.sort(key=lambda x: -x[1]["total"])
    if apenas_viaveis:
        out = [(i, p) for i, p in out if p["total"] > 0]
    return out

def robustez(pesos_base, aporte=500.0, n=None):
    """Um ranking ponderado so vale se o vencedor NAO depender dos pesos.

    Este e o teste que quase nenhum ranking publicado faz: varrer configuracoes de
    peso muito diferentes e ver se o topo muda. Se mudar, o ranking esta medindo a
    opiniao de quem escolheu os pesos, nao a realidade das instituicoes."""
    dims = list(pesos_base)
    cenarios = {"declarado": dict(pesos_base)}
    for d in dims:                                   # cada dimensao sozinha valendo tudo
        cenarios[f"so_{d}"] = {k: (100 if k == d else 1) for k in dims}
    cenarios["igual"] = {k: 20 for k in dims}
    base = {k: 1 for k in dims}
    cenarios["so_custo"] = {**base, "corretagem": 50, "custodia": 30, "tesouro": 20}
    cenarios["so_instituicao"] = {**base, "solidez": 50, "sobrevivencia": 50}
    cenarios["so_reclamacoes"] = {**base, "reclamacoes": 100}
    cenarios["custo_e_reclamacoes"] = {**base, "corretagem": 40, "custodia": 20,
                                       "reclamacoes": 40}
    out = {}
    for nome, pe in cenarios.items():
        r = ranking(pe, aporte)
        out[nome] = [i.nome for i, _ in r[:3]]
    return out

if __name__ == "__main__":
    P = carregar_politica()
    pesos = P["corretora"]["pesos"]
    ap = P["corretora"]["aporte_de_referencia"]
    print("="*104)
    print(f"RANKING DE CORRETORAS — aporte de referência R${ap:,.0f} · horizonte 10 anos")
    print("="*104)
    print("pesos declarados: " + " · ".join(f"{k} {v}" for k, v in pesos.items()))
    _r = regras(P)
    print("\nmultiplicador de confirmação (lido do politica.yaml): " +
          "  ".join(f"{k}={v:.2f}" for k, v in _r["mult"].items()) +
          " (dado não confirmado não entra em ordenação)\n")
    r = ranking(pesos, ap)
    print(f"{'#':>3} {'instituição':<30}{'nota':>7}{'recl':>7}{'corr':>7}{'cust':>6}{'TD':>6}"
          f"{'sol':>6}{'sobr':>6}{'conf':>6}  BC 2T/26")
    for k, (i, p) in enumerate(r, 1):
        f = lambda x, w=6: f"{x:>{w}.0f}" if x is not None else f"{'—':>{w}}"
        bc = f"{i.bc_indice:.2f} ({i.bc_posicao}º)" if i.bc_indice else "não ranqueado"
        print(f"{k:>3} {i.nome[:29]:<30}{p['total']:>7.1f}{f(p['dim']['reclamacoes'],7)}"
              f"{f(p['dim']['corretagem'],7)}{f(p['dim']['custodia'])}{f(p['dim']['tesouro'])}"
              f"{f(p['dim']['solidez'])}{f(p['dim']['sobrevivencia'])}{i.confirmacao:>6}  {bc}")
    print("\n" + "="*104)
    print("RECLAME AQUI — exibido, NUNCA pontuado (politica.yaml: pontua false, exibe true)")
    print("="*104)
    for i in catalogo_instituicoes():
        ra = reclame_aqui(i, P)
        if not ra: continue
        marca = "  <- DIVERGE do ranking do BC" if ra["diverge_do_bc"] else ""
        print(f"   {i.nome[:32]:<34} nota {ra['nota']:.1f} · solucao {ra['solucao']:.1f}% "
              f"· voltaria {ra['voltaria']:.1f}% · {ra['reclamacoes']:,} reclamacoes{marca}")

    print("\n" + "="*104)
    print("ROBUSTEZ — o vencedor depende dos pesos que eu escolhi?")
    print("="*104)
    rb = robustez(pesos, ap)
    print(f"\n{'configuração de pesos':<24}{'1º':<30}{'2º':<30}{'3º':<20}")
    for nome, top in rb.items():
        t = top + ["—"]*(3-len(top))
        print(f"{nome:<24}{t[0][:29]:<30}{t[1][:29]:<30}{t[2][:19]:<20}")
    primeiros = {v[0] for v in rb.values() if v}
    print(f"\n  vencedores distintos entre {len(rb)} configurações: "
          f"{len(primeiros)} — {', '.join(primeiros)}")
    if len(primeiros) == 1:
        print("""
  O primeiro lugar NÃO muda em nenhuma configuração de peso testada, incluindo as
  duas extremas — só custo e só instituição. Isso significa que os pesos que eu
  declarei não estão fazendo o trabalho: a instituição vence por dominância, não por
  ponderação. É o mesmo teste de dominância que o G4 faz com as rotas, aplicado às
  casas. Um ranking cujo topo muda com os pesos mede a opinião de quem os escolheu.""")

    print("\nFORA DA ORDENAÇÃO (nota zero):")
    for i, p in [(i, pontuar(i, pesos, ap, 10)) for i in catalogo_instituicoes()]:
        if p["total"] <= 0:
            motivo = ("dados não confirmados" if i.confirmacao == "N" else
                      "entidade não independente" if not i.entidade_independente else "?")
            print(f"    {i.nome:<34} {motivo} — {i.pegadinha[:60]}")

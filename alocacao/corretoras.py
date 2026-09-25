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
# E-08, 13/09/2026
from __future__ import annotations
import io, os, sys
from dataclasses import dataclass, field
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from alocacao import carregar_politica, _caminho
from motor import carregar as carregar_custos, val, InsumoBloqueado

AQUI = os.path.dirname(os.path.abspath(__file__))

@dataclass
class Instituicao:
    id: str
    nome: str
    corretagem_rv: float | None      # R$ por ordem no autoatendimento; None = nao confirmado
    corretagem_pct: float | None = None   # parte percentual; None = nao medida
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
    corretagem_etf_pct: float | None = None  # XP cobra 0,50% em ETF; None = nao medida
    exercicio_opcao_pct: float | None = None
    mesa_minimo: float | None = None
    # ── facilidade: proxies objetivos ─────────────────────────────────────────
    home_broker_web: bool | None = None
    exporta_csv: bool | None = None
    # E-08, 13/09/2026. Espelha `RotaAloc.bloqueios`: motivos que tiram um campo de
    # circulacao sem tirar a instituicao do catalogo. Vem da resolucao de `{de:}`.
    bloqueios: list = field(default_factory=list)

    @property
    def confiavel(self):
        return not self.bloqueios

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


# ── E-08, 13/09/2026: o resolvedor de referencia ────────────────────────────
RANKING = "ranking_corretoras"


def _resolver(valor, C, campo, iid, contexto, bloqueios):
    """`{de: "corretagem.xp_etf_pct"}` -> o valor do custos.yaml, passando por `val()`.

    ACHADO E-08. Ate aqui o `instituicoes.yaml` so aceitava literal, e por isso SEIS
    numeros existiam duas vezes: uma no `custos.yaml`, com status, fonte e `expira`, e
    outra aqui, crua. As copias concordavam -- e o N-01 e sobre o dia em que param.

    Pior que a divergencia futura era o RELOGIO. As cinco constantes de `corretagem`
    expiram em 04/12/2026; as seis copias nao tinham campo de validade nenhum. O
    projeto construiu um mecanismo de vencimento e metade dos numeros nao estava ligada
    nele. Passar por `val()` resolve isso de graca: o aviso de `expira` sai em stderr
    para quem referencia.

    E RESOLVE O OUTRO LADO DO E-08, que e o que importa mais. `corretagem.xp_swing` e
    PARCIAL e declara `bloqueia: ["ranking_corretoras"]` -- nomeia ESTE consumidor. O
    ranking rodava assim mesmo, porque lia a copia e nunca chamava `val()`: a
    consequencia declarada nao chegava nele. Agora chega. Quem carrega o catalogo diz
    QUEM e (`contexto`), e uma constante que bloqueia esse nome devolve `None`.

    `None` nao e um buraco: e o valor que `pontuar()` ja sabia tratar -- ele marca a
    dimensao como nao avaliada e a `cobertura` penaliza. **Dimensao ausente e
    penalidade, nao neutralidade**, que e o que o proprio `pontuar` ja dizia.

    O contexto e OPCIONAL de proposito. Sem contexto, `bloqueia` nao e checado -- um
    consumidor que nao se nomeia nao pode reivindicar um bloqueio dirigido a outro.
    NAO_CONFIRMADO continua barrando em qualquer caso, porque ali nao ha valor nenhum.
    """
    if not (isinstance(valor, dict) and "de" in valor):
        return valor
    caminho = valor["de"]
    no = _caminho(C, caminho)
    if contexto and contexto in (no.get("bloqueia") or []):
        bloqueios.append("%s.%s: %s bloqueia %s — %s"
                         % (iid, campo, caminho, contexto,
                            no.get("motivo", "sem motivo declarado")))
        return None
    try:
        return val(no, contexto="%s.%s -> %s" % (iid, campo, caminho))
    except InsumoBloqueado as e:
        bloqueios.append("%s.%s: %s" % (iid, campo, str(e)[:160]))
        return None


def catalogo_instituicoes(path=None, C=None, contexto=None):
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
    # E-08: so carrega o custos.yaml se houver referencia a resolver. Quem nunca usa
    # `{de:}` nao paga por ele.
    precisa = "de:" in io.open(path or INSTITUICOES_YAML, encoding="utf-8").read()
    if precisa and C is None:
        C = carregar_custos()
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
        bloqueios = []
        if C is not None:
            campos = {k: _resolver(v, C, k, iid, contexto, bloqueios)
                      for k, v in campos.items()}
        out.append(Instituicao(id=iid, bloqueios=bloqueios, **campos))
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
    if c["custo_por_operacao"]["pontua"]:
        # 16/09/2026. O interruptor existe e RECUSA: `corretagem_fii`,
        # `exercicio_opcao_pct` e `mesa_minimo` sao exibidos, nunca pontuados, porque
        # medidos em 16/09 os dois primeiros tem UM valor so entre quem os declara. O
        # E-03 foi sobre interruptor declarado e nao ligado em nada -- este esta ligado
        # aqui, e falha alto.
        raise NotImplementedError(
            "politica.yaml diz corretora.custo_por_operacao.pontua: true, e os tres "
            "campos exibidos sao CONSTANTES entre as casas que os declaram: pontuar "
            "adicionaria peso sem mudar ordenacao nenhuma. A parcela que pontua e a "
            "corretagem de ETF, e ela ja entra dentro da dimensao `corretagem`.")
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
    #
    # F-02, 16/09/2026: o default destes campos era `0.0`. Zero e o MELHOR valor
    # possivel, entao uma casa que nao declarasse a parte percentual entrava no
    # ranking como se ela fosse zero -- insumo ausente virando o numero mais
    # favoravel, que e o defeito que o BOVV11 custou. Agora o default e None, e
    # `None` em QUALQUER das duas parcelas tira a dimensao: meio custo conhecido
    # nao e um custo, e somar a metade que se sabe com um zero inventado seria
    # pior que nao pontuar.
    # DECISAO DELE, 13/09/2026: custo por operacao entra no ranking. Implementado em
    # 16/09 como SEGUNDA PARCELA desta dimensao, e nao como dimensao nova -- custo de
    # ordem e custo de ordem, e criar dimensao exigiria um peso que ninguem mediu.
    #
    # PIOR CASO entre as duas rotas, e a escolha tem precedente na casa: a reserva se
    # julga por `liquidez_pior_caso_dias`, nao pela media. Aqui vale pelo mesmo motivo --
    # a nota tem de descrever a ordem que vai doer, nao a que sai mais barata.
    #
    # AS DUAS ROTAS SAO EXIGIDAS, e isso descarta informacao de proposito. A XP tem
    # `corretagem_etf_pct` COMPLETO (0,50%) e `corretagem_rv` BLOQUEADO para o ranking
    # (E-08: `xp_swing` e PARCIAL e nomeia este consumidor). Pontuar so pela parcela
    # conhecida daria 0,50%; a parcela desconhecida, quando media, era R$4,90 em R$500 =
    # 0,98% -- **o dobro**. Ou seja: usar a metade conhecida seria otimista por um fator
    # de dois, na direcao exata do F-02. Perder a dimensao inteira custa `cobertura`, que
    # e penalidade; e a direcao conservadora.
    if inst.corretagem_rv is None or inst.corretagem_pct is None:
        d["corretagem"] = None
        notas.append("corretagem NÃO CONFIRMADA")
    elif inst.corretagem_etf_pct is None:
        d["corretagem"] = None
        notas.append("corretagem de ETF NÃO CONFIRMADA")
    else:
        custo_acao = inst.corretagem_rv/aporte + inst.corretagem_pct
        custo = max(custo_acao, inst.corretagem_etf_pct)
        d["corretagem"] = max(0.0, 100*(1 - custo/R["custo_nota_zero"]))
        if custo > 0:
            qual = "ETF" if inst.corretagem_etf_pct > custo_acao else "ação"
            notas.append(f"corretagem consome {custo*100:.2f}% de um aporte de "
                         f"R${aporte:,.0f} (pior caso: {qual})")

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
    # 18/09: aqui havia um segundo `return`, com CHAVES DIFERENTES do de baixo (A-07
    # dentro de uma funcao so). A prova por mutacao reprovou o TESTE, nao o codigo: o
    # ramo e inalcancavel, porque `sobrevivencia` sai de um bool e nunca e None. Ramo
    # morto nao falha, logo nao se testa. `test_P90_toda_casa_tem_ao_menos_uma_dimensao_
    # avaliavel` prende a invariante que o dispensa; se ela cair, o ramo volta.
    if not validas:
        raise AssertionError(
            f"{inst.nome}: nenhuma dimensao avaliavel. Isto era um ramo silencioso ate "
            f"18/09 e agora e erro duro -- a invariante que o dispensava caiu, e o "
            f"conserto e reescrever o ramo com o MESMO formato do return de baixo.")
    peso_total = sum(pesos[k] for k in validas)
    bruto = sum(validas[k]*pesos[k] for k in validas)/peso_total
    # dimensao ausente e penalidade, nao neutralidade: quem nao publica, perde
    cobertura = peso_total/sum(pesos.values())
    # P-90, correcao dele em 18/09: `parcial` e a nota com tudo que o sistema DE FATO
    # sabe da casa, ja penalizada pela cobertura e ANTES do multiplicador. O N=0 nao
    # apagava a casa do catalogo, mas apagava o que se sabia dela -- e o BTG tem 54,0
    # com 65% de cobertura, 7o de 15. O multiplicador CONTINUA zerando o `total` (G5/
    # F-02: status e pre-condicao de comparacao de custo); o que muda e o sistema parar
    # de esconder o que sabe. Documento em `docs/auditoria/P90-INFORMACAO-NAO-OBTIDA.md`.
    return dict(total=bruto*mult*cobertura, parcial=bruto*cobertura, bruto=bruto,
                dim=d, notas=notas, multiplicador=mult, cobertura=cobertura,
                avaliadas=sorted(validas), nao_avaliadas=sorted(set(d) - set(validas)))

def custo_por_operacao(inst: Instituicao, P=None):
    """Custos por operacao EXIBIDOS e nunca pontuados. Mesmo molde do `reclame_aqui`.

    Decisao dele de 13/09 (*custo por operacao entra no ranking: sim*), medida antes de
    virar codigo: dos tres campos coletados, `corretagem_fii` tem um unico valor entre as
    11 casas que o declaram (0,0) e `exercicio_opcao_pct` tem um unico valor entre as 4
    (0,005). **Campo constante nao discrimina** -- uma dimensao sobre ele adiciona peso e
    nao muda ordenacao nenhuma. `mesa_minimo` varia, mas 20 de 24 nao declaram e nao ha
    como separar "nao tem mesa" de "nao pesquisei".

    Exibir e o ponto: quem for operar FII ou opcao precisa do numero, e o ranking nao
    precisa fingir que o compara. Devolve None quando o arquivo manda nao exibir ou
    quando a casa nao declara nenhum dos tres."""
    global _POLITICA
    if P is None:
        if _POLITICA is None: _POLITICA = carregar_politica()
        P = _POLITICA
    c = P["corretora"]["custo_por_operacao"]
    if not c["exibe"]:
        return None
    fora = {campo: getattr(inst, campo) for campo in c["exibidos"]
            if getattr(inst, campo, None) is not None}
    return fora or None


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
    # E-08: o ranking diz QUEM E. `corretagem.xp_swing` declara
    # `bloqueia: ["ranking_corretoras"]`, e ate 13/09/2026 essa frase nao alcancava
    # ninguem. Nomear-se aqui e o que a transforma em comportamento.
    for i in catalogo_instituicoes(contexto=RANKING):
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

def _nao_ordenadas(pesos, ap, ordenadas):
    """As casas que o multiplicador zerou — e o que o sistema JÁ SABE sobre cada uma.

    P-90, correção dele em 18/09/2026. A versão anterior imprimia só o nome e o motivo, e
    descartava a `parcial` que `pontuar()` já calculava. Duas coisas se perdiam:

      1. ZERO MEDIDO e ZERO POR AUSÊNCIA saíam com a mesma cara. A Clear tem
         `entidade_independente = False` — isso é medição, e o zero é o resultado dela.
         O BTG tem 65% de cobertura e nota 54,0 — isso é ausência, e o zero é a decisão
         de não ordenar quem tem custo desconhecido. São afirmações diferentes.
      2. A posição que a casa OCUPARIA nunca aparecia, e é ela que mostra o tamanho do
         que se está deixando de fora.

    O `pegadinha` dessas casas descreve um FRACASSO DE COLETA — "HTTP 403", "site é SPA",
    "domínio não resolve DNS" —, e isso é propriedade do meu método, não da instituição.
    Por isso a seção termina apontando a pendência em vez de encerrar o assunto."""
    linhas = [(i, pontuar(i, pesos, ap, 10)) for i in catalogo_instituicoes()]
    medido = [(i, p) for i, p in linhas if p["total"] <= 0 and p["parcial"] <= 0]
    ausente = [(i, p) for i, p in linhas if p["total"] <= 0 and p["parcial"] > 0]
    notas_ordenadas = [p["total"] for _, p in ordenadas]

    print("\n" + "="*104)
    print("NÃO ORDENADAS POR AUSÊNCIA DE DADO — e o que o sistema JÁ SABE sobre elas")
    print("="*104)
    print("  O multiplicador de confirmação N=0 tira a casa da ORDENAÇÃO, porque custo")
    print("  desconhecido não se compara com custo conhecido (G5/F-02). Ele NÃO é um")
    print("  veredito sobre a instituição, e a nota abaixo é o que se sabe hoje.")
    for i, p in sorted(ausente, key=lambda x: -x[1]["parcial"]):
        pos = sum(1 for n in notas_ordenadas if n > p["parcial"]) + 1
        print(f"\n    {i.nome:<34} nota parcial {p['parcial']:.1f} · cobertura "
              f"{p['cobertura']:.0%} · ficaria em {pos}º de {len(ordenadas)+len(ausente)}")
        print(f"       sabe-se: {', '.join(p['avaliadas'])}")
        print(f"       falta:   {', '.join(p['nao_avaliadas'])}")
        print(f"       a coleta falhou assim: {i.pegadinha[:78]}")
    if medido:
        print("\n  ZERO MEDIDO, e isto é um resultado, não uma lacuna:")
        for i, p in medido:
            motivo = ("não é entidade independente" if not i.entidade_independente
                      else "nenhuma dimensão pôde ser avaliada")
            print(f"    {i.nome:<34} {motivo}")
    if ausente:
        print("\n  O fracasso acima é do MÉTODO DE COLETA, não da instituição — 403, SPA e")
        print("  DNS descrevem o meu raspador. Resolver isso é a P-90, com dono e gatilho.")


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
    print("CUSTO POR OPERACAO — exibido, NUNCA pontuado "
          "(politica.yaml: pontua false, exibe true)")
    print("="*104)
    rotulo = {"corretagem_fii": "FII", "exercicio_opcao_pct": "exercicio de opcao",
              "mesa_minimo": "minimo de mesa"}
    algum = False
    for i in catalogo_instituicoes():
        cpo = custo_por_operacao(i, P)
        if not cpo: continue
        algum = True
        partes = ["%s %s" % (rotulo.get(k, k),
                             ("R$%.2f" % v) if k == "mesa_minimo" else ("%.2f%%" % (v*100)))
                  for k, v in cpo.items()]
        print(f"   {i.nome[:32]:<34} " + " · ".join(partes))
    if not algum:
        print("   (nenhuma casa declara)")
    print("   Constantes entre quem declara (medido 16/09): FII 0,00% em 11/11 casas, "
          "exercicio 0,50% em 4/4.")
    print("   A parcela que PONTUA e a corretagem de ETF, dentro da dimensao corretagem.")

    print("\n" + "="*104)
    print("ROBUSTEZ — o vencedor depende dos pesos que eu escolhi?")
    print("="*104)
    rb = robustez(pesos, ap)
    print(f"\n{'configuração de pesos':<24}{'1º':<30}{'2º':<30}{'3º':<20}")
    for nome, top in rb.items():
        t = top + ["—"]*(3-len(top))
        print(f"{nome:<24}{t[0][:29]:<30}{t[1][:29]:<30}{t[2][:19]:<20}")
    # N-01 de LICAO, 16/09/2026: `set` nao tem ordem, e este print mudava de TEXTO
    # entre duas execucoes com o MESMO dado -- peguei isso tentando usar a saida
    # como instantaneo dourado. O `refinar.py` ja tinha aprendido a licao e ate a
    # escreveu ("Ordem ESTAVEL. Sem isso o instantaneo dourado acusa diferenca a cada
    # rodada e para de servir como rede"), e ela nao atravessou para ca. Regra
    # aplicada num lugar so e a forma que o A-07 tem quando o irmao e um MODULO.
    primeiros = sorted({v[0] for v in rb.values() if v})
    print(f"\n  vencedores distintos entre {len(rb)} configurações: "
          f"{len(primeiros)} — {', '.join(primeiros)}")
    if len(primeiros) == 1:
        print("""
  O primeiro lugar NÃO muda em nenhuma configuração de peso testada, incluindo as
  duas extremas — só custo e só instituição. Isso significa que os pesos que eu
  declarei não estão fazendo o trabalho: a instituição vence por dominância, não por
  ponderação. É o mesmo teste de dominância que o G4 faz com as rotas, aplicado às
  casas. Um ranking cujo topo muda com os pesos mede a opinião de quem os escolheu.""")

    _nao_ordenadas(pesos, ap, r)


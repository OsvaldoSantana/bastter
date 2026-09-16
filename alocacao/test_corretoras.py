# -*- coding: utf-8 -*-
"""Testes do ranking de corretoras. O ranking e derivado — logo, testavel."""
import os, sys, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from corretoras import catalogo_instituicoes, pontuar, ranking, robustez, AQUI
from alocacao import carregar_politica

P = carregar_politica()
PESOS = P["corretora"]["pesos"]
AP = P["corretora"]["aporte_de_referencia"]
INST = {i.id: i for i in catalogo_instituicoes()}


def test_pesos_do_ranking_estao_no_yaml_e_somam_cem():
    assert sum(PESOS.values()) == 100
    assert PESOS["sobrevivencia"] > PESOS["corretagem"], \
        "a tese do laudo e que sobrevivencia pesa mais que preco quando 8 casas cobram zero"


def test_dado_nao_confirmado_nao_entra_em_ordenacao():
    """G5 aplicado a uma decisao de vida real. BTG tem o segundo maior balanco da
    amostra e nenhum custo legivel — nao pode aparecer no topo."""
    for rid in ("btg", "bradesco", "mirae", "clear"):
        p = pontuar(INST[rid], PESOS, AP, 10)
        assert p["multiplicador"] == 0.0 and p["total"] == 0.0
    ids = {i.id for i, _ in ranking(PESOS, AP)}
    assert not ({"btg", "bradesco", "mirae", "clear"} & ids)


def test_entidade_que_deixou_de_existir_pontua_zero_em_sobrevivencia():
    """Sete das 25 marcas pesquisadas nao existem mais como entidade independente."""
    extintas = [i for i in catalogo_instituicoes() if not i.entidade_independente]
    assert len(extintas) >= 7
    for i in extintas:
        assert pontuar(i, PESOS, AP, 10)["dim"]["sobrevivencia"] == 0.0


def test_prejuizo_no_trimestre_corta_a_solidez_pela_metade():
    warren = pontuar(INST["warren"], PESOS, AP, 10)
    genial = pontuar(INST["genial"], PESOS, AP, 10)
    assert any("PREJUÍZO" in n for n in warren["notas"])
    assert any("PREJUÍZO" in n for n in genial["notas"])
    assert warren["dim"]["solidez"] < 20


def test_nao_publicar_e_penalidade_e_nao_neutralidade():
    """Quem nao publica custodia ou taxa de Tesouro perde pontos por nao publicar —
    o contrario premiaria a opacidade."""
    santander = pontuar(INST["santander"], PESOS, AP, 10)
    assert santander["cobertura"] < 1.0
    assert santander["total"] < santander["bruto"]


def test_itau_e_a_unica_confirmada_nas_cinco_dimensoes():
    d = pontuar(INST["itau"], PESOS, AP, 10)["dim"]
    assert all(v is not None for v in d.values())
    completas = [i.id for i in catalogo_instituicoes()
                 if all(v is not None for v in pontuar(i, PESOS, AP, 10)["dim"].values())
                 and i.confirmacao == "C" and i.entidade_independente]
    assert completas == ["itau"] or ("itau" in completas and len(completas) <= 3)


def test_robustez_e_reportada_com_honestidade():
    """O teste que quase nenhum ranking publicado faz — e o resultado MUDOU quando a
    dimensao de reclamacoes entrou (04/09/2026). Antes o vencedor era o mesmo em 9 de
    9 configuracoes; agora e 10 de 11, e ele PERDE quando so reclamacoes contam.

    Este teste trava o numero para que uma futura mudanca de peso que quebre a
    dominancia apareca, em vez de passar despercebida."""
    rb = robustez(PESOS, AP)
    primeiros = [v[0] for v in rb.values() if v]
    do_itau = sum(1 for x in primeiros if "Itaú" in x)
    assert do_itau >= len(primeiros) - 1, \
        f"Itaú venceu em {do_itau} de {len(primeiros)} — dominancia degradou mais que o esperado"
    assert rb["declarado"][0].startswith("Itaú")
    assert not rb["so_reclamacoes"][0].startswith("Itaú"), (
        "a excecao conhecida: no cenario so-reclamacoes o Itaú NAO vence, "
        "e isso tem de estar visivel")
    for c in ("so_custo", "so_instituicao", "so_reclamacoes", "custo_e_reclamacoes"):
        assert c in rb, f"cenario {c} tem de ser testado"


# ══ reclamacoes — fonte primaria do Banco Central ════════════════════════════
def test_formula_do_indice_do_bc_e_verificada_e_nao_suposta():
    """procedentes / clientes x 1.000.000. Recalculada a partir das colunas
    publicadas; o erro maximo e de arredondamento."""
    erros = []
    for i in catalogo_instituicoes():
        if i.bc_indice and i.bc_procedentes and i.bc_clientes:
            erros.append(abs(i.bc_procedentes/i.bc_clientes*1e6 - i.bc_indice))
    assert len(erros) >= 9, "poucas instituicoes com dado do BC"
    assert max(erros) < 0.05, f"a formula nao reproduz o indice: erro maximo {max(erros)}"


def test_indice_do_bc_e_normalizado_e_isso_inverte_a_leitura_ingenua():
    """O defeito que invalida quase toda comparacao publicada: numero absoluto premia
    o pequeno. A Caixa tem MAIS reclamacoes procedentes que o C6 e e MELHOR no indice."""
    caixa, c6 = INST["caixa"], INST["c6"]
    assert caixa.bc_procedentes > c6.bc_procedentes
    assert caixa.bc_indice < c6.bc_indice
    assert c6.bc_indice/caixa.bc_indice > 2.5


def test_c6_e_o_segundo_mais_reclamado_e_isso_o_derrubou_no_ranking():
    """Achado de 04/09: o C6 era 2o lugar e caiu para 3o quando a dimensao entrou."""
    assert INST["c6"].bc_posicao == 2
    p = pontuar(INST["c6"], PESOS, AP, 10)
    assert p["dim"]["reclamacoes"] < 45
    assert any("MAIS reclamado" in n for n in p["notas"])


def test_o_proprio_vencedor_leva_a_nota_ruim_no_output():
    """O Itaú e o 3o mais reclamado do Brasil. O ranking o mantem em 1o e NAO esconde
    a mancha — uma nota de 53 em 100 numa dimensao de peso 20."""
    p = pontuar(INST["itau"], PESOS, AP, 10)
    assert INST["itau"].bc_posicao == 3
    assert 45 < p["dim"]["reclamacoes"] < 60
    assert any("MAIS reclamado" in n for n in p["notas"])


def test_reclame_aqui_e_coletado_e_nao_pontua():
    """Exibido porque o usuario pediu; nao pontua porque a amostra e autosselecionada
    e nao normalizada. E a divergencia entre as duas fontes e informacao: o Itaú tem
    8,1 e 85,2% de solucao no RA, e e o 3o mais reclamado no ranking do BC."""
    itau = INST["itau"]
    assert itau.ra_nota == 8.1 and itau.ra_solucao == 85.2
    assert "reclame_aqui" not in PESOS
    p = pontuar(itau, PESOS, AP, 10)
    assert "reclame_aqui" not in p["dim"]


def test_promocional_tem_peso_zero_por_decisao_declarada():
    assert "promocional" not in PESOS
    assert P["corretora"]["promocional"]["peso"] == 0
    assert P["corretora"]["promocional"]["e_uma_decisao_nao_uma_omissao"] is True


def test_promocional_diferente_de_zero_recusa_o_ranking():
    """Auditoria de 10/09, 'campos mortos': `promocional` era declarado e nenhum modulo
    o lia -- trocar o peso no YAML nao mudava nada. Agora e o padrao de `reclame_aqui`
    e `facilidade`: sem dimensao em pontuar(), peso diferente de zero recusa."""
    from corretoras import regras
    P2 = copy.deepcopy(P)
    P2["corretora"]["promocional"]["peso"] = -5
    with pytest.raises(NotImplementedError, match="promocional"):
        regras(P2)


def test_custo_por_operacao_tem_detalhe_alem_da_acao_a_vista():
    """A critica do usuario sobre 'custos por operacao mais detalhados'. O caso que
    prova a necessidade: a XP cobra 0,50% em ETF e R$4,90 em acao — sao rotas de custo
    completamente diferentes na mesma corretora."""
    assert INST["xp"].corretagem_etf_pct == 0.005
    assert INST["xp"].corretagem_rv == 4.90
    com_minimo_de_mesa = [i.id for i in catalogo_instituicoes() if i.mesa_minimo]
    assert "inter" in com_minimo_de_mesa and INST["inter"].mesa_minimo == 50.0


def test_corretagem_e_medida_como_fracao_do_aporte():
    """R$4,50 por ordem nao e caro em abstrato — e caro em relacao ao aporte. Num de
    R$500 sao 0,90%; num de R$5.000, 0,09%."""
    caro = pontuar(INST["safra"], PESOS, 500, 10)["dim"]["corretagem"]
    barato = pontuar(INST["safra"], PESOS, 5000, 10)["dim"]["corretagem"]
    assert barato > caro
    assert pontuar(INST["itau"], PESOS, 200, 10)["dim"]["corretagem"] == 100.0


def test_toda_instituicao_tem_fonte_e_status():
    for i in catalogo_instituicoes():
        assert i.fonte, f"{i.id} sem fonte declarada"
        assert i.confirmacao in ("C", "P", "N")
        if i.confirmacao != "N":
            assert i.pegadinha, f"{i.id} confirmada e sem pegadinha registrada"


# ══ N-01 · a secao `corretora` do YAML era, em tres pontos, prosa ════════════
def test_N01_o_multiplicador_de_confirmacao_vem_do_yaml_e_nao_do_python():
    """Ate 05/09/2026, `mult = {"C": 1.0, "P": 0.75, "N": 0.0}` era um literal dentro
    de corretoras.py, e politica.yaml declarava exatamente os mesmos numeros logo
    abaixo de uma `regra:` que explicava o porque. Concordavam.

    Concordar e PIOR que discordar: um leitor do YAML acreditava estar editando o
    comportamento, e nao estava. E o mesmo defeito do F-05 (`bloqueia` nunca lido),
    aqui aplicado a decisao de qual instituicao guarda o dinheiro. O teste falha na
    versao anterior porque la o P valia 0,75 aconteca o que acontecer."""
    p_antes = pontuar(INST["itau"], PESOS, AP, 10)
    P2 = copy.deepcopy(P); P2["corretora"]["multiplicador_de_confirmacao"]["C"] = 0.5
    p_depois = pontuar(INST["itau"], PESOS, AP, 10, P2)
    assert INST["itau"].confirmacao == "C"
    assert abs(p_depois["total"] - p_antes["total"]/2) < 1e-9


def test_N01_a_escala_de_reclamacoes_vem_do_yaml():
    """`escala: "indice 0 = 100 pontos; indice 100 = 0 pontos"` era uma FRASE, e o 100
    vivia em `1 - bc_indice/100`. Agora ha `escala_indice_para_nota_zero`, e apertar a
    escala pela metade tem de derrubar a nota de quem e reclamado."""
    P2 = copy.deepcopy(P); P2["corretora"]["reclamacoes"]["escala_indice_para_nota_zero"] = 50
    antes = pontuar(INST["c6"], PESOS, AP, 10)["dim"]["reclamacoes"]
    depois = pontuar(INST["c6"], PESOS, AP, 10, P2)["dim"]["reclamacoes"]
    assert INST["c6"].bc_indice > 0
    assert depois < antes


def test_N01_a_escala_de_corretagem_saiu_do_comentario():
    """O `0.01` de "1% do aporte = nota zero" era um literal com um comentario ao lado.
    Um comentario nao e uma regra: ninguem pode mudar o comportamento sem editar
    codigo, e o arquivo que diz governar o sistema nao dizia nada sobre ele."""
    assert P["corretora"]["corretagem"]["custo_do_aporte_para_nota_zero"] == 0.01
    P2 = copy.deepcopy(P); P2["corretora"]["corretagem"]["custo_do_aporte_para_nota_zero"] = 0.0005
    cara = pontuar(INST["safra"], PESOS, 500, 10, P2)["dim"]["corretagem"]
    assert cara == 0.0, "com a regua dez vezes mais dura, corretagem cara tem de zerar"


def test_N01_ligar_uma_dimensao_inexistente_para_o_sistema_em_vez_de_ser_ignorado():
    """`reclame_aqui.pontua: false` e `facilidade.pontua: false` eram lidos por
    ninguem. Se alguem virasse para `true`, o ranking continuaria identico e o arquivo
    passaria a mentir em silencio. Agora mentir custa uma excecao."""
    for secao in ("reclame_aqui", "facilidade"):
        P2 = copy.deepcopy(P); P2["corretora"][secao]["pontua"] = True
        with pytest.raises(NotImplementedError):
            pontuar(INST["itau"], PESOS, AP, 10, P2)


def test_N01_exibe_o_reclame_aqui_porque_o_arquivo_manda_exibir():
    """A frase que faltava fechar: `pontua: false, exibe: true`. Nao pontuar era
    verdade (nenhuma dimensao usa RA); exibir era mentira. E o Itau e o caso que
    justifica a regra — 8,1 no Reclame Aqui e 3o mais reclamado do Brasil no BC."""
    from corretoras import reclame_aqui
    ra = reclame_aqui(INST["itau"], P)
    assert ra and ra["nota"] == 8.1 and ra["diverge_do_bc"], \
        "o caso que motivou a regra tem de aparecer marcado como divergente"
    P2 = copy.deepcopy(P); P2["corretora"]["reclame_aqui"]["exibe"] = False
    assert reclame_aqui(INST["itau"], P2) is None


# ══ P-36 metade B · as instituicoes sairam do Python ═════════════════════════
def test_P36_nenhuma_instituicao_e_construida_por_literal_no_python():
    """136 linhas de literais, ~15 campos MEDIDOS por casa, com `fonte=` e
    `confirmacao=` inline. Dado de pesquisa dentro de codigo, e nada testava se
    aquele numero tinha procedencia. Varredura no AST: um `Instituicao(...)` em
    qualquer lugar, com qualquer formatacao, cai aqui."""
    import ast, os
    arvore = ast.parse(open(os.path.join(AQUI, "corretoras.py"), encoding="utf-8").read())
    permitido = set()
    for n in ast.walk(arvore):
        if isinstance(n, ast.FunctionDef) and n.name == "catalogo_instituicoes":
            permitido = {id(x) for x in ast.walk(n)}
    fora = [n for n in ast.walk(arvore)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id in ("Instituicao", "I") and id(n) not in permitido]
    assert not fora, ("instituicao construida fora do carregador, linha(s) "
                      + ", ".join(str(n.lineno) for n in fora))


def test_Q02_o_multiplicador_sempre_falou_de_CUSTOS_e_o_registro_nao_sabia_dizer():
    """ACHADO Q-02. `confirmacao` era UMA letra por instituicao e `pontuar()` a aplica
    como multiplicador de TUDO — N zera a nota inteira. Mas ela nunca significou "este
    registro e confiavel": significou "os CUSTOS podem ser lidos em fonte oficial", e a
    propria `regra` em politica.yaml diz isso.

    A prova esta no dado. BTG e Bradesco tem status NAO_CONFIRMADO em `custos` e
    balanco vindo do BCB IF.data e reclamacoes do ranking do BC — as duas fontes
    PRIMARIAS, as duas COMPLETO. O comportamento estava certo; o registro e que
    achatava tudo numa letra, e um leitor concluiria que o balanco do BTG e duvidoso."""
    from corretoras import procedencia_de
    for iid in ("btg", "bradesco"):
        p = procedencia_de(iid)
        assert p["custos"]["procedencia"]["status"] == "NAO_CONFIRMADO"
        assert "custos NÃO OBTIDOS" in p["custos"]["procedencia"]["fonte"]
        assert p["balanco"]["procedencia"]["status"] == "COMPLETO"
        assert "IF.data" in p["balanco"]["procedencia"]["fonte"]
        assert INST[iid].confirmacao == "N"
        assert pontuar(INST[iid], PESOS, AP, 10)["total"] == 0.0
    assert procedencia_de("btg")["reclamacoes"]["procedencia"]["status"] == "COMPLETO"


def test_Q02_a_confirmacao_e_DERIVADA_e_nao_um_campo_que_pode_discordar():
    """Dois campos que podiam discordar viraram um. Mudar o status de custos no YAML
    TEM de mudar a letra e, por consequencia, o multiplicador — se `confirmacao`
    ainda fosse campo proprio, os dois poderiam apontar para lados opostos e ninguem
    descobriria. E o mesmo defeito do N-01, prevenido em vez de encontrado."""
    from corretoras import STATUS_PARA_LETRA, procedencia_de
    for i in catalogo_instituicoes():
        st = procedencia_de(i.id)["custos"]["procedencia"]["status"]
        assert i.confirmacao == STATUS_PARA_LETRA[st], i.id
        assert i.fonte == procedencia_de(i.id)["custos"]["procedencia"]["fonte"]


def test_P36_todo_grupo_de_campos_declara_de_onde_veio():
    """A granularidade e por GRUPO porque e assim que as fontes se agrupam: custos vem
    da pagina da casa, balanco do IF.data, reclamacoes do ranking do BC. Procedencia
    por CAMPO daria 24 x 15 = 360 blocos para registrar cinco fontes reais, e registro
    que ninguem le e pior que registro nenhum."""
    import datetime as dt
    from corretoras import carregar_instituicoes_cru, GRUPOS_DE_CAMPOS
    d = carregar_instituicoes_cru()["instituicoes"]
    for iid, cru in d.items():
        assert "custos" in cru, f"{iid}: toda casa tem grupo de custos, nem que vazio"
        for g in GRUPOS_DE_CAMPOS:
            if g not in cru: continue
            p = cru[g].get("procedencia")
            assert p, f"{iid}.{g}: grupo sem procedencia"
            assert p["status"] in ("COMPLETO", "PARCIAL", "NAO_CONFIRMADO", "OBSERVADO")
            assert len(p.get("fonte", "")) > 10, f"{iid}.{g}: fonte vazia"
            assert isinstance(p.get("acesso"), dt.date), f"{iid}.{g}: sem data de acesso"


def test_P36_o_ranking_nao_mudou_com_a_migracao():
    """A migracao e para ser INVISIVEL no resultado. Se o topo mudou, a extracao
    perdeu ou trocou um numero — e e por isso que a ordem inteira entra no teste, e
    nao so o primeiro lugar."""
    ordem = [i.id for i, _ in ranking(PESOS, AP)]
    assert ordem[:4] == ["itau", "caixa", "c6", "santander"]
    assert len(catalogo_instituicoes()) == 24


# ══ F-02, 16/09/2026: zero escrito onde ninguem mediu ═══════════════════════════
def test_F02_casa_NAO_pesquisada_nao_carrega_numero_de_custo():
    """Nove das 24 casas tem `custos.procedencia.status: NAO_CONFIRMADO`, e a `fonte`
    de cada uma diz, com estas palavras, "custos NAO OBTIDOS". Todas carregavam
    `corretagem_pct: 0.0` e `corretagem_etf_pct: 0.0`.

    **Zero e o melhor valor possivel.** E o F-02 na letra -- o mesmo defeito da BOVV11,
    cuja taxa NAO_CONFIRMADA virava `adm_aa = 0.0` e a punha como a rota mais barata do
    catalogo. Aqui nao mordeu ate hoje por um acidente: os dois campos eram MORTOS,
    ninguem os lia. A decisao de 13/09 de por o custo por operacao no ranking e
    exatamente o que os acordaria -- e nove casas nao pesquisadas estreariam com custo
    zero de graca.

    A guarda e da CLASSE, nao dos dois campos: qualquer numero de custo novo numa casa
    NAO_CONFIRMADA reprova aqui."""
    import yaml
    cru = yaml.safe_load(open(os.path.join(AQUI, "instituicoes.yaml"), encoding="utf-8"))
    escritos = []
    for iid, spec in cru["instituicoes"].items():
        c = spec.get("custos") or {}
        if (c.get("procedencia") or {}).get("status") != "NAO_CONFIRMADO":
            continue
        escritos += ["%s.%s = %r" % (iid, k, v) for k, v in c.items()
                     if k != "procedencia" and isinstance(v, (int, float))]
    assert not escritos, (
        "casa com procedencia NAO_CONFIRMADO carregando numero de custo:\n  - "
        + "\n  - ".join(escritos)
        + "\n\nA fonte dela diz que o custo nao foi obtido. `null` e o que se sabe; "
          "zero e o melhor valor possivel, e insumo ausente nao vira o numero mais "
          "favoravel (F-02).")


def test_F02_o_default_do_dataclass_tambem_era_um_zero_nao_medido():
    """Corrigir so o YAML teria deixado o zero um andar acima: `corretagem_pct: float
    = 0.0` no proprio dataclass. Uma casa que simplesmente NAO declarasse o campo
    continuaria entrando com zero, e o YAML limpo nao salvaria."""
    from corretoras import Instituicao
    i = Instituicao(id="x", nome="X", corretagem_rv=None)
    assert i.corretagem_pct is None, "o default voltou a ser zero"
    assert i.corretagem_etf_pct is None, "o default voltou a ser zero"


def test_F02_meio_custo_conhecido_NAO_e_um_custo():
    """`custo = rv/aporte + pct`. Com `pct` desconhecido, somar a metade que se sabe com
    um zero inventado da um numero -- e o numero e otimista por construcao. A dimensao
    sai, e a `cobertura` penaliza, que e o tratamento que o proprio `pontuar` ja
    declarava para dimensao ausente."""
    from corretoras import Instituicao
    meio = Instituicao(id="x", nome="X", corretagem_rv=4.9, corretagem_pct=None)
    assert pontuar(meio, PESOS, AP, 10, P)["dim"]["corretagem"] is None
    # as TRES parcelas conhecidas -- a de ETF entrou na dimensao em 16/09 (P-84)
    inteiro = Instituicao(id="y", nome="Y", corretagem_rv=4.9, corretagem_pct=0.0,
                          corretagem_etf_pct=0.0)
    assert pontuar(inteiro, PESOS, AP, 10, P)["dim"]["corretagem"] is not None


def test_a_saida_do_ranking_e_DETERMINISTICA_entre_execucoes():
    """N-01 de LICAO, 16/09/2026. `vencedores distintos: N — <lista>` juntava um `set`,
    e `set` de string nao tem ordem entre PROCESSOS. O texto do relatorio mudava entre
    duas execucoes com o MESMO dado -- peguei isso tentando usar a saida como
    instantaneo dourado, que e justamente para o que ela nao servia.

    O `refinar.py` ja tinha aprendido a licao e escrito o motivo ("Ordem ESTAVEL. Sem
    isso o instantaneo dourado acusa diferenca a cada rodada e para de servir como
    rede"), e ela nao atravessou de modulo para modulo. Por isso o teste roda em
    SUBPROCESSO com `PYTHONHASHSEED` diferente: dentro de um processo so, a ordem do
    `set` e estavel e o defeito nao aparece."""
    import subprocess
    saidas = []
    for semente in ("1", "42"):
        amb = dict(os.environ, PYTHONHASHSEED=semente)
        r = subprocess.run([sys.executable, os.path.join(AQUI, "corretoras.py")],
                           capture_output=True, text=True, env=amb, timeout=120)
        assert r.returncode == 0, r.stderr[-500:]
        saidas.append(r.stdout)
    assert saidas[0] == saidas[1], (
        "o relatorio mudou de TEXTO entre duas execucoes com o mesmo dado -- ha um "
        "`set` (ou `dict` de ordem nao garantida) sendo impresso sem ordenar.")


# ══ P-84, 16/09/2026: custo por operacao entra no ranking (decisao dele de 13/09) ══
def test_P84_o_PIOR_CASO_entre_acao_e_ETF_e_o_que_pontua():
    """A dimensao `corretagem` ganhou segunda parcela em vez de virar dimensao nova --
    dimensao nova exigiria um peso que ninguem mediu, e mexer no vetor mudaria a nota
    das 24 casas para resolver o caso de uma.

    PIOR CASO, e a escolha tem precedente na casa: a reserva se julga por
    `liquidez_pior_caso_dias`, nunca pela media. A nota tem de descrever a ordem que vai
    doer."""
    from corretoras import Instituicao
    so_acao = Instituicao(id="a", nome="A", corretagem_rv=0.0, corretagem_pct=0.0,
                          corretagem_etf_pct=0.0)
    caro_em_etf = Instituicao(id="b", nome="B", corretagem_rv=0.0, corretagem_pct=0.0,
                              corretagem_etf_pct=0.005)
    n1 = pontuar(so_acao, PESOS, AP, 10, P)
    n2 = pontuar(caro_em_etf, PESOS, AP, 10, P)
    assert n1["dim"]["corretagem"] == 100.0
    assert n2["dim"]["corretagem"] < 100.0, "0,50% em ETF nao chegou na nota"
    assert any("pior caso: ETF" in x for x in n2["notas"]), n2["notas"]

    # e o inverso: acao cara, ETF gratis -> o pior caso continua sendo a acao
    caro_em_acao = Instituicao(id="c", nome="C", corretagem_rv=4.9, corretagem_pct=0.0,
                               corretagem_etf_pct=0.0)
    n3 = pontuar(caro_em_acao, PESOS, AP, 10, P)
    assert any("pior caso: ação" in x for x in n3["notas"]), n3["notas"]


def test_P84_ETF_desconhecido_tira_a_dimensao_INTEIRA_e_isso_e_conservador():
    """Descartar informacao DE PROPOSITO, e o caso vivo e a XP.

    Ela tem `corretagem_etf_pct` COMPLETO (0,50%) e `corretagem_rv` BLOQUEADO para o
    ranking (E-08: `xp_swing` e PARCIAL e nomeia este consumidor). Pontuar so pela
    parcela conhecida daria 0,50%; a parcela desconhecida, quando foi medida, era R$4,90
    em R$500 = **0,98%, o dobro**. Usar a metade conhecida seria otimista por um fator de
    dois -- a direcao exata do F-02. Perder a dimensao custa `cobertura`, que e
    penalidade, e penalidade e a direcao conservadora."""
    from corretoras import Instituicao, catalogo_instituicoes, RANKING
    meio = Instituicao(id="x", nome="X", corretagem_rv=0.0, corretagem_pct=0.0,
                       corretagem_etf_pct=None)
    r = pontuar(meio, PESOS, AP, 10, P)
    assert r["dim"]["corretagem"] is None
    assert any("ETF NÃO CONFIRMADA" in x for x in r["notas"]), r["notas"]

    xp = {i.id: i for i in catalogo_instituicoes(contexto=RANKING)}["xp"]
    assert xp.corretagem_rv is None and xp.corretagem_etf_pct == 0.005
    assert pontuar(xp, PESOS, AP, 10, P)["dim"]["corretagem"] is None
    assert 4.9/AP > xp.corretagem_etf_pct, (
        "a parcela escondida da XP deixou de ser a mais cara -- a justificativa de "
        "descartar a metade conhecida mudou, e a decisao precisa ser remedida")


def test_P84_hoje_a_parcela_de_ETF_nao_muda_o_ranking_e_o_motivo_esta_MEDIDO():
    """O teste que impede a pergunta *"implementamos e nada mudou, esta funcionando?"*.

    Nao mudou, e o motivo e exato: **a unica casa com custo de ETF diferente de zero e a
    XP**, e a dimensao dela ja estava `None` por causa do E-08. Mecanismo vivo, efeito
    zero -- por acidente do dado, nao por defeito do codigo.

    No dia em que qualquer outra casa declarar ETF diferente de zero, este teste falha e
    manda reconferir o ranking. E a medicao virando guarda."""
    from corretoras import catalogo_instituicoes, RANKING
    inst = {i.id: i for i in catalogo_instituicoes(contexto=RANKING)}
    com_etf = {iid: i.corretagem_etf_pct for iid, i in inst.items()
               if i.corretagem_etf_pct}
    assert com_etf == {"xp": 0.005}, (
        "outra casa passou a ter custo de ETF: " + repr(com_etf) +
        ". A parcela de ETF deixou de ser inerte -- reconfira o ranking.")
    assert pontuar(inst["xp"], PESOS, AP, 10, P)["dim"]["corretagem"] is None


def test_P84_os_tres_campos_EXIBIDOS_sao_constantes_e_e_por_isso_que_nao_pontuam():
    """A medicao que decidiu o desenho, presa num teste. Se um dia um deles variar,
    exibir deixa de ser a resposta certa e este teste manda revisitar."""
    from corretoras import catalogo_instituicoes
    todas = catalogo_instituicoes()
    for campo, esperado in (("corretagem_fii", {0.0}), ("exercicio_opcao_pct", {0.005})):
        vistos = {getattr(i, campo) for i in todas if getattr(i, campo) is not None}
        assert vistos == esperado, (
            "%s deixou de ser constante (%r): campo que VARIA discrimina, e discriminar "
            "e o que faltava para ele virar dimensao em vez de exibicao." % (campo, vistos))
    mesa = {i.id: i.mesa_minimo for i in todas if i.mesa_minimo is not None}
    assert len(mesa) == 4 and len(set(mesa.values())) == 3, (
        "a cobertura de mesa_minimo mudou (%r) -- com 20 de 24 casas sem declarar, nao "
        "havia como separar 'nao tem mesa' de 'nao pesquisei'." % mesa)


def test_P84_o_interruptor_de_pontuar_RECUSA_em_vez_de_ignorar():
    """E-03: interruptor declarado e ligado em nada e pior que interruptor nenhum. Este
    esta ligado, e falha alto."""
    from corretoras import regras
    P2 = copy.deepcopy(P)
    P2["corretora"]["custo_por_operacao"]["pontua"] = True
    with pytest.raises(NotImplementedError, match="custo_por_operacao"):
        regras(P2)


def test_P84_a_exibicao_obedece_o_arquivo():
    from corretoras import custo_por_operacao
    inter = INST["inter"]
    assert custo_por_operacao(inter, P)["mesa_minimo"] == 50.0
    P2 = copy.deepcopy(P)
    P2["corretora"]["custo_por_operacao"]["exibe"] = False
    assert custo_por_operacao(inter, P2) is None
    assert custo_por_operacao(INST["btg"], P) is None, "casa sem nenhum dos tres"

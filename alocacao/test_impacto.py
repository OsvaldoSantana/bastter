# -*- coding: utf-8 -*-
"""Testes do mapa de impacto. Pendencia P-39.

Um mapa de dependencias errado e pior que nenhum: quem confia nele para decidir que
"ninguem le esta constante" toma a decisao com falsa seguranca. Estes testes existem
para que o mapa nao possa mentir em silencio."""
import os, sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import impacto
from alocacao import catalogo, carregar_catalogo
from motor import carregar as carregar_custos

C = carregar_custos()


def test_o_grafo_catalogo_custos_esta_completo():
    """A parte confiavel do mapa: as arestas `{de:}` sao DADO, nao inferencia. Toda
    referencia do catalogo.yaml tem de aparecer no grafo — se uma escapar, alguem vai
    editar uma constante achando que ela nao alcanca rota nenhuma."""
    arestas = impacto.referencias_do_catalogo()
    encontradas = {(r, c) for r, c, _ in arestas}
    esperadas = set()
    def varrer(no, rota, campo):
        if isinstance(no, dict):
            if {"de", "de_campo", "de_se_na_lista"} & set(no):
                esperadas.add((rota, campo)); return
            if "soma" in no: esperadas.add((rota, campo)); return
            for k, v in no.items(): varrer(v, rota, campo or k)
    cru = carregar_catalogo()["rotas"]
    for rid, r in cru.items():
        if rid.startswith("_"): continue
        for campo, v in r.items():
            if campo in ("procedencia", "bloqueio"): continue
            varrer(v, rid, campo)
    assert esperadas <= encontradas, f"referencias fora do grafo: {esperadas - encontradas}"


def test_toda_aresta_do_grafo_aponta_para_constante_que_existe():
    """Aresta apontando para caminho inexistente seria um mapa que inventa destino."""
    for rota, campo, alvo in impacto.referencias_do_catalogo():
        no = C
        for parte in alvo.split("."):
            assert isinstance(no, dict) and parte in no, \
                f"{rota}.{campo} aponta para custos.yaml -> {alvo}, que nao existe"
            no = no[parte]


def test_o_grafo_e_verificavel_contra_o_comportamento_real():
    """A afirmacao do mapa e testavel: se ele diz que a rota X depende da constante Y,
    alterar Y TEM de mudar X. Isto e o que separa um mapa de um desenho."""
    import copy
    for alvo in ("etf.BOVA11", "corretagem.safra_terra"):
        dependentes = {r for r, _ in impacto.rotas_que_dependem_de(alvo)}
        assert dependentes, f"{alvo} deveria ter dependentes"
        C2 = copy.deepcopy(C)
        no = C2
        for parte in alvo.split(".")[:-1]: no = no[parte]
        no[alvo.split(".")[-1]]["valor"] = 0.4242
        antes = {r.id: r for r in catalogo(C)}
        depois = {r.id: r for r in catalogo(C2)}
        mudaram = {rid for rid in antes if antes[rid] != depois[rid]}
        assert mudaram == dependentes, \
            f"{alvo}: o mapa diz {sorted(dependentes)}, a realidade diz {sorted(mudaram)}"


def test_os_pontos_cegos_sao_reportados_e_nao_escondidos():
    """A lista do que o mapa NAO ve vale mais que a do que ele ve. Um mapa que finge
    completude e pior que grep, porque grep ninguem confunde com garantia."""
    cegas = impacto.leituras_cegas()
    assert cegas, "existem leituras com chave dinamica; reportar zero seria mentira"
    assert any("P['funcoes'][f]" in txt for _, _, txt in cegas), \
        "o caso mais comum do projeto — iterar funcoes — tem de aparecer"
    assert "PONTOS CEGOS" in impacto.relatorio("etf.BOVA11")
    assert "NADA ENCONTRADO" in impacto.relatorio("chave_que_nao_existe_em_lugar_nenhum")


def test_o_relatorio_de_alvo_inexistente_nao_afirma_que_nada_depende():
    """A frase importa. "Nada encontrado" e um fato sobre a BUSCA; "nada depende" seria
    uma afirmacao sobre o SISTEMA, e o mapa nao pode fazer essa afirmacao."""
    r = impacto.relatorio("nao_existe_isto")
    assert "NADA ENCONTRADO" in r and "NAO significa que nada depende" in r


@pytest.mark.repositorio   # 146b: le ou roda o fonte, que a mutacao instrumenta
def test_o_alcance_de_funcao_e_transitivo_e_nao_so_direto():
    """A pergunta util nao e "quem me chama" — e "o que quebra se eu mudar o contrato".
    `simular_custo` e chamada por duas funcoes e alcancada por oito."""
    diretos = {f for f, _ in impacto.quem_chama("simular_custo")}
    todos = {f for f, _ in impacto.alcance_de_funcao("simular_custo")}
    assert diretos == {"arrasto_anualizado", "custo_pct_aportado"}
    assert "alocar" in todos and "alocar" not in diretos
    assert len(todos) > len(diretos)


def test_o_grafo_de_modulos_nao_tem_ciclo():
    """Ciclo de import nao quebra o Python moderno, mas quebra o raciocinio: com
    ciclo, "quem depende de quem" deixa de ter resposta."""
    g = impacto.grafo_de_modulos()
    def alcanca(a, visto=None):
        visto = visto or set()
        for d in g.get(a, []):
            if d in visto: continue
            visto.add(d); visto |= alcanca(d, visto)
        return visto
    for m in g:
        assert m not in alcanca(m), f"ciclo de import envolvendo {m}"

# -*- coding: utf-8 -*-
"""
chaves_orfas.py -- a pergunta que o `impacto.py` nao faz.

O `impacto.py` responde "QUEM LE esta chave?". E uma otima ferramenta e tem um limite
que so aparece quando voce ve o que ela nao pega: **e preciso ja suspeitar da chave**.

Esta faz a pergunta inversa, que nao precisa de suspeita nenhuma:

    quais chaves o YAML DECLARA que codigo nenhum le?

Foi assim que o achado E-03 saiu: `politica.yaml` declara `ativo` para os nove portoes,
e o `g3_atrito` e o `g4_dominancia` nunca leem o campo. Os dois estavam `true`, entao o
arquivo e o codigo concordavam -- por acidente. Desligar o G3 no YAML nao desliga o G3.

A chave orfa NAO e necessariamente um defeito: ha chave que e nota para humano, ha
chave lida por variavel (`P[secao][k]`), ha chave lida so no teste. O que ela e, sempre,
e uma PROMESSA SEM DONO -- e promessa sem dono e a materia-prima do defeito recorrente
deste projeto: um arquivo declara um comportamento que o codigo nao tem.
"""

import argparse
import ast
import os
import sys

import yaml

# chaves que descrevem o dado, nao o comportamento: procedencia, prosa, metadado.
# Nao sao promessas ao codigo, entao nao entram na conta.
META = {"valor", "status", "fonte", "acesso", "expira", "nota", "motivo", "bloqueia",
        "revisar_se", "descricao", "obs", "meta", "_hash", "trecho_conferido",
        "pergunta", "custo_de_ignorar", "por_que", "titulo", "comentario"}


def folhas(no, cam=()):
    """Todo caminho de chave do YAML, com a marca de quem e folha."""
    if isinstance(no, dict):
        for k, v in no.items():
            yield cam + (str(k),), v
            yield from folhas(v, cam + (str(k),))
    elif isinstance(no, list):
        for x in no:
            yield from folhas(x, cam)


def lidas_por_yaml(yamls):
    """Chaves que OUTRO YAML le. Este projeto resolve aresta YAML->YAML de proposito:
    o `catalogo.yaml` aponta para o `custos.yaml` por `{de:}`, `{soma:}`, `{de_campo:}`
    e `{de_se_na_lista:}`, e o `impacto.py` ja chama esse grafo de "a parte do mapa em
    que da para confiar sem ressalva".

    ESTA FUNCAO EXISTE POR CAUSA DE UM ERRO MEU, e o erro custou um achado inteiro.
    A versao anterior varria SO os `.py`. Com isso ela acusou
    `cofrinho.picpay_garantia_de_limite.liquidez_pior_caso_dias` como orfa, e eu
    escrevi um achado (E-05) dizendo que o sistema tinha a liquidez do cofrinho no
    arquivo e nao a lia. **Falso.** O catalogo le assim:

        liquidez_dias: {de_campo: "cofrinho.picpay_garantia_de_limite.liquidez_pior_caso_dias"}

    Auditar um projeto que poe regra em YAML varrendo so o Python e medir metade do
    sistema e chamar o resultado de conclusao. Foi o A-06 outra vez, do meu lado da
    mesa: a ferramenta media o lugar errado, e o verde dela me convenceu."""
    alvos = set()
    def anda(no):
        if isinstance(no, dict):
            for k, v in no.items():
                if k in ("de", "de_campo", "de_se_na_lista") and isinstance(v, str):
                    alvos.add(v)
                    alvos.update(v.split("."))
                elif k == "soma" and isinstance(v, list):
                    for x in v:
                        if isinstance(x, str):
                            alvos.add(x); alvos.update(x.split("."))
                        else:
                            anda(x)
                else:
                    anda(v)
        elif isinstance(no, list):
            for x in no:
                anda(x)
    for y in yamls:
        anda(yaml.safe_load(open(y, encoding="utf-8")))
    return alvos


def pais_varridos(pasta):
    """Chaves cujo VALOR e indexado por variavel logo em seguida: `g["x"][k]`.

    Esta funcao existe por causa de um falso positivo meu, e vale escrever o caso.
    A ferramenta acusou `portoes.G2_reserva.ajuste_estabilidade.{alta,media,baixa}` --
    o multiplicador da reserva por estabilidade de renda -- como orfao. Parecia grave.
    E falso: o codigo le `g["ajuste_estabilidade"][estado.estabilidade_renda]` em
    quatro lugares. O indice e VARIAVEL, entao o nome da folha nunca aparece literal.

    Quem alcanca os filhos por variavel LE TODOS OS FILHOS. Entao a regra e: se o pai
    e lido literalmente e logo indexado por nao-constante, as folhas dele nao sao
    orfas -- e nao por suposicao, por construcao.

    O que isto NAO suprime, e a distincao importa: pai que nunca aparece no codigo.
    `cofrinho.picpay_garantia_de_limite` nao e lido em lugar nenhum, entao as folhas
    dele continuam orfas -- que e o achado E-05, e ele sobrevive a este filtro."""
    pais = set()
    for f in sorted(os.listdir(pasta)):
        if not f.endswith(".py"):
            continue
        try:
            arv = ast.parse(open(os.path.join(pasta, f), encoding="utf-8").read())
        except SyntaxError:
            continue
        for n in ast.walk(arv):
            if isinstance(n, ast.Subscript) and not (
                    isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str)):
                base = n.value
                if isinstance(base, ast.Subscript) and isinstance(base.slice, ast.Constant) \
                        and isinstance(base.slice.value, str):
                    pais.add(base.slice.value)
    return pais


def chaves_lidas(pasta, so_motor=False):
    """Toda string usada como indice de subscrito em qualquer modulo. Proposital que
    seja tao grosseiro: aqui o falso NEGATIVO e que custa. Uma chave lida em qualquer
    lugar por qualquer motivo nao e orfa."""
    lidas, cegas = set(), []
    for f in sorted(os.listdir(pasta)):
        if not f.endswith(".py"):
            continue
        # ACHADO P-77-b, 13/09/2026. A versao anterior varria TODO .py, testes
        # inclusive -- e por isso deu `aliquota_ganho` como lida. Ela e lida quatro
        # vezes, TODAS em `test_alocacao.py`, e por NENHUMA linha do motor.
        #
        # E a pior categoria que existe, pior que orfa pura: um campo que so o teste
        # toca e um campo que o MOTOR nao usa -- o teste prova o esquema e ninguem
        # prova o comportamento. Foi assim que a P-13 pode anunciar uma correcao que
        # era so mudanca de dataclass, e a ferramenta que existia para pegar isso
        # ficou verde por causa do teste.
        if so_motor and (f.startswith("test_") or f == "conftest.py"):
            continue
        fonte = open(os.path.join(pasta, f), encoding="utf-8").read()
        try:
            arv = ast.parse(fonte)
        except SyntaxError:
            continue
        for n in ast.walk(arv):
            if isinstance(n, ast.Subscript):
                s = n.slice
                if isinstance(s, ast.Constant) and isinstance(s.value, str):
                    lidas.add(s.value)
                else:
                    cegas.append((f, n.lineno, ast.unparse(n)[:60]))
            # `.get("chave")` tambem e leitura
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                    and n.func.attr in ("get", "setdefault", "pop") and n.args:
                a = n.args[0]
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    lidas.add(a.value)
        # atributo de dataclass com o mesmo nome tambem conta como consumo
        for n in ast.walk(arv):
            if isinstance(n, ast.Attribute):
                lidas.add(n.attr)
            elif isinstance(n, ast.keyword) and n.arg:
                lidas.add(n.arg)
    return lidas, cegas


def main(argv=None):
    p = argparse.ArgumentParser(description="Chaves declaradas que codigo nenhum le.")
    p.add_argument("pasta", help="pasta dos modulos .py")
    p.add_argument("yamls", nargs="+", help="arquivos .yaml a conferir")
    p.add_argument("--tudo", action="store_true",
                   help="tambem lista chaves de valor textual (prosa/doutrina)")
    p.add_argument("--incluir-meta", action="store_true",
                   help="tambem conta chaves de procedencia/prosa")
    # 24/09/2026: a secao `armazem` do politica.yaml e lida pelo fase0 (a captura), nao
    # pelo alocacao. Uma pasta so fazia a chave lida antes de cada envio aparecer orfa.
    p.add_argument("--tambem", action="append", default=[], metavar="PASTA",
                   help="outra pasta de modulos que le os mesmos YAML (ex.: fase0)")
    a = p.parse_args(argv)

    lidas, cegas, so_motor, pais = set(), [], set(), set()
    for pasta in [a.pasta, *a.tambem]:
        daqui, cegas_daqui = chaves_lidas(pasta)
        lidas |= daqui
        cegas += cegas_daqui
        so_motor |= chaves_lidas(pasta, so_motor=True)[0]
        pais |= pais_varridos(pasta)
    so_teste = lidas - so_motor
    de_yaml = lidas_por_yaml(a.yamls)
    lidas |= de_yaml
    print("%d nome(s) consumidos por YAML (arestas {de:}/{de_campo:}/{soma:})\n"
          % len(de_yaml))
    print("%d nome(s) distintos consumidos pelo codigo\n"
          "%d leitura(s) CEGA (indice por variavel) -- todo orfao abaixo pode estar\n"
          "     escondido em uma delas, e por isso a lista e de CANDIDATOS\n"
          % (len(lidas), len(cegas)))

    total_orfas, total_so_teste = 0, 0
    for y in a.yamls:
        doc = yaml.safe_load(open(y, encoding="utf-8"))
        orfas, apenas_teste = [], []
        # ACHADO 16/09/2026 -- a ferramenta escondia 42 de 67 chaves, e do pior jeito.
        # Esta deduplicacao era por NOME DE FOLHA (`vistos.add(k)`), entao a SEGUNDA
        # ocorrencia de qualquer nome no mesmo arquivo sumia do relatorio -- nem orfa,
        # nem lida: invisivel. `bc_procedentes` era reportada para o Itau e calada para
        # as outras oito casas; `variantes_permitidas` aparecia numa estrategia e sumia
        # em sete.
        #
        # Peguei sem procurar: batizei uma chave nova com o mesmo nome de folha de uma
        # existente, e a EXISTENTE desapareceu da auditoria. Uma guarda que emudece
        # quando alguem escolhe um nome e pior que guarda nenhuma -- e a linha de base
        # ficava menor, que e a direcao que parece progresso.
        #
        # Dedupe por CAMINHO. O motivo original era ruido no relatorio; o preco era
        # cobertura, e cobertura vale mais.
        vistos = set()
        for cam, v in folhas(doc):
            k = cam[-1]
            if cam in vistos:
                continue
            vistos.add(cam)
            if not a.incluir_meta and k in META:
                continue
            if k in so_teste and not isinstance(v, (dict, list)):
                # lida, mas por NINGUEM do motor
                if isinstance(v, (bool, int, float)) or a.tudo:
                    apenas_teste.append("%-58s = %r" % (".".join(cam), v))
                continue
            if k.isdigit() or k in lidas:
                continue
            # o pai e varrido por variavel: o codigo alcanca TODAS as folhas dele
            if len(cam) > 1 and cam[-2] in pais:
                continue
            # O FILTRO QUE DA SINAL. Este projeto poe a DOUTRINA dentro do YAML de
            # proposito -- `por_que_este_bloco_antes_dos_outros` e prosa para humano e
            # nao promete nada ao codigo. Ja um BOOLEANO ou um NUMERO orfao promete:
            # alguem escreveu um parametro esperando que ele mude alguma coisa.
            if not a.tudo:
                if isinstance(v, bool) or isinstance(v, (int, float)):
                    pass
                elif isinstance(v, list) and v and all(isinstance(x, (int, float)) for x in v):
                    pass
                else:
                    continue
            orfas.append("%-58s = %r" % (".".join(cam), v))
        total_orfas += len(orfas)
        print("=" * 78)
        print("%s -- %d chave(s) distintas que ninguem le" % (os.path.basename(y), len(orfas)))
        print("=" * 78)
        for o in sorted(orfas):
            print("   " + o)
        if apenas_teste:
            total_so_teste += len(apenas_teste)
            print("\n   -- LIDA SO POR TESTE (%d) -- pior que orfa: o teste prova o"
                  "\n      esquema e ninguem prova o comportamento" % len(apenas_teste))
            for o in sorted(apenas_teste):
                print("   " + o)
        print()
    print("%d orfa(s) e %d lida(s) so por teste. Cada uma e uma promessa sem dono ate\n"
          "alguem dizer de quem e." % (total_orfas, total_so_teste))
    return 0


if __name__ == "__main__":
    sys.exit(main())

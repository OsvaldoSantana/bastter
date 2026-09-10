# -*- coding: utf-8 -*-
"""
Mapa de impacto: quem alcanca o que. Pendencia P-39.

POR QUE ISTO EXISTE, e a resposta e desconfortavel.

O Osvaldo perguntou em 06/09/2026 como eu rastreio, a cada alteracao, onde o que
mudou interage com os outros arquivos. A resposta honesta era: TRES FERRAMENTAS E
NENHUM MAPA.

  1. A SUITE. 258 testes. E a rede real, e ela pega muita coisa — mas ela pega DEPOIS.
     Ela responde "quebrou?", nunca "o que isto alcanca?".
  2. `grep`. Ad hoc, dependente de eu lembrar do nome certo. Foi o que quase deixou o
     N-01 passar: procurei `multiplicador_de_confirmacao` no Python e achei zero
     ocorrencias — e concluir "entao ninguem le" so funcionou porque eu por acaso
     desconfiei do numero repetido.
  3. INSTANTANEO DOURADO. Serializar tudo antes, comparar depois. E a mais forte das
     tres (foi ela que garantiu a P-36 e a P-37), e ela custa caro e so serve para
     mudanca grande.

  Nenhuma das tres e um MAPA. Nenhuma responde, ANTES de eu editar: "se eu mexer em
  `custos.yaml -> etf.BOVA11`, o que alcanca esse valor?"

  Este modulo responde. Ele nao substitui a suite — a suite julga, ele orienta.

O QUE ELE ENXERGA
  yaml -> codigo      quais modulos leem um caminho do custos.yaml / politica.yaml
  catalogo -> custos  as referencias `{de:}` do catalogo.yaml, que agora sao dado
  modulo -> modulo    o grafo de imports
  funcao -> funcao    o grafo de chamadas dentro do projeto
  campo -> uso        acesso a atributo de RotaAloc / Estado / Instituicao

O QUE ELE NAO ENXERGA, declarado — e a lista importa mais que a de cima:
  - chave montada em tempo de execucao (`C[secao][k]` com `k` vindo de variavel). O
    modulo REPORTA esses pontos como `cegos`, em vez de fingir que nao existem.
  - `getattr(obj, nome)` com nome dinamico.
  - despacho por dicionario de funcoes (o PORTOES_DO_UNIVERSO e um destes: o mapa ve
    que o dict cita a funcao, nao que a chamada acontece pelo nome).
  - qualquer coisa que atravesse o YAML como dado e volte como comportamento.

  Um mapa que finge completude e pior que grep, porque grep ninguem confunde com
  garantia. As duas listas andam juntas de proposito.
"""
from __future__ import annotations
import ast
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def _modulos():
    return sorted(f for f in os.listdir(AQUI)
                  if f.endswith(".py") and not f.startswith(("test_", "demo_", "conftest")))


def _arvore(f):
    return ast.parse(open(os.path.join(AQUI, f), encoding="utf-8").read())


# ── 1. YAML -> codigo ────────────────────────────────────────────────────────
def leituras_de_yaml(modulos=None):
    """Toda leitura por chave literal de um dict, por modulo.

    Devolve {modulo: {chave: [linhas]}}. Nao distingue custos.yaml de politica.yaml,
    porque no codigo os dois chegam como `C` e `P` e a chave e o que se procura."""
    out = {}
    for f in (modulos or _modulos()):
        achados = {}
        for n in ast.walk(_arvore(f)):
            if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) \
               and isinstance(n.slice.value, str):
                achados.setdefault(n.slice.value, []).append(n.lineno)
        out[f] = achados
    return out


def leituras_cegas(modulos=None):
    """Os pontos em que a chave NAO e literal: `C[secao][k]`, com `k` variavel.

    Sao os buracos do mapa, e eles tem endereco. Quem for editar uma constante e
    encontrar zero leituras literais precisa olhar aqui antes de concluir que ninguem
    a le — foi assim que o N-01 quase passou."""
    out = []
    for f in (modulos or _modulos()):
        for n in ast.walk(_arvore(f)):
            if isinstance(n, ast.Subscript) and not (
                    isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str)):
                alvo = ast.unparse(n.value)
                if alvo.split("[")[0] in ("C", "P", "d", "cru", "no", "custos", "politica"):
                    out.append((f, n.lineno, ast.unparse(n)[:70]))
    return out


def quem_le(chave, modulos=None):
    """Quais modulos leem esta chave, e em que linhas."""
    return {m: ls for m, achados in leituras_de_yaml(modulos).items()
            for k, ls in achados.items() if k == chave}


# ── 2. catalogo.yaml -> custos.yaml ──────────────────────────────────────────
def referencias_do_catalogo(path=None):
    """As arestas `{de:}` / `{soma:}` / `{de_campo:}` / `{de_se_na_lista:}`.

    Depois da P-36 este grafo e DADO e nao inferencia — e a parte do mapa em que da
    para confiar sem ressalva."""
    import yaml
    p = path or os.path.join(AQUI, "catalogo.yaml")
    d = yaml.safe_load(open(p, encoding="utf-8"))
    arestas = []

    def varrer(no, rota, campo):
        if isinstance(no, dict):
            for chave in ("de", "de_campo"):
                if chave in no:
                    arestas.append((rota, campo, no[chave])); return
            if "soma" in no:
                for x in no["soma"]: varrer(x, rota, campo)
                return
            if "de_se_na_lista" in no:
                arestas.append((rota, campo, no["de_se_na_lista"]["valor"])); return
            for k, v in no.items(): varrer(v, rota, campo or k)

    for rid, cru in d["rotas"].items():
        if rid.startswith("_"): continue
        for campo, v in cru.items():
            if campo in ("procedencia", "bloqueio"): continue
            varrer(v, rid, campo)
        b = cru.get("bloqueio")
        if b:
            for fonte in b["fontes"]:
                arestas.append((rid, f"bloqueio[{b['regra']}]", fonte))
    return arestas


def rotas_que_dependem_de(caminho_custos, path=None):
    """Quais rotas do catalogo mudam se esta constante mudar. Prefixo conta."""
    return sorted({(r, c) for r, c, alvo in referencias_do_catalogo(path)
                   if alvo == caminho_custos or alvo.startswith(caminho_custos + ".")})


# ── 3. modulo -> modulo, funcao -> funcao ────────────────────────────────────
def grafo_de_modulos():
    nomes = {os.path.splitext(f)[0] for f in _modulos()}
    g = {}
    for f in _modulos():
        dep = set()
        for n in ast.walk(_arvore(f)):
            if isinstance(n, ast.ImportFrom) and n.module in nomes: dep.add(n.module)
            elif isinstance(n, ast.Import):
                dep |= {a.name for a in n.names if a.name in nomes}
        g[os.path.splitext(f)[0]] = sorted(dep)
    return g


def grafo_de_chamadas():
    """{funcao: {quem ela chama}}, restrito a funcoes definidas no projeto."""
    definidas, dono = set(), {}
    for f in _modulos():
        for n in ast.walk(_arvore(f)):
            if isinstance(n, ast.FunctionDef):
                definidas.add(n.name); dono[n.name] = f
    g = {}
    for f in _modulos():
        for n in ast.walk(_arvore(f)):
            if not isinstance(n, ast.FunctionDef): continue
            chama = {x.func.id for x in ast.walk(n)
                     if isinstance(x, ast.Call) and isinstance(x.func, ast.Name)
                     and x.func.id in definidas and x.func.id != n.name}
            g[n.name] = sorted(chama)
    return g, dono


def quem_chama(funcao):
    g, dono = grafo_de_chamadas()
    return sorted((f, dono.get(f, "?")) for f, alvos in g.items() if funcao in alvos)


def alcance_de_funcao(funcao, profundidade=6):
    """Fecho transitivo INVERSO: tudo que chega ate esta funcao, direta ou
    indiretamente. E a pergunta "o que quebra se eu mudar o contrato dela"."""
    g, dono = grafo_de_chamadas()
    inverso = {}
    for f, alvos in g.items():
        for a in alvos: inverso.setdefault(a, set()).add(f)
    vistos, fronteira = set(), {funcao}
    for _ in range(profundidade):
        nova = set()
        for f in fronteira: nova |= inverso.get(f, set())
        nova -= vistos | {funcao}
        if not nova: break
        vistos |= nova; fronteira = nova
    return sorted((f, dono.get(f, "?")) for f in vistos)


# ── 4. campo de dataclass -> uso ─────────────────────────────────────────────
def quem_usa_campo(campo):
    """Acesso a atributo `.campo` em qualquer modulo do projeto."""
    out = []
    for f in _modulos():
        src = open(os.path.join(AQUI, f), encoding="utf-8").read()
        linhas = src.splitlines()
        for n in ast.walk(ast.parse(src)):
            if isinstance(n, ast.Attribute) and n.attr == campo:
                out.append((f, n.lineno, linhas[n.lineno-1].strip()[:78]))
    return out


# ── 5. o relatorio ───────────────────────────────────────────────────────────
def relatorio(alvo):
    """`alvo` pode ser um caminho de YAML (`etf.BOVA11`), um nome de funcao, ou um
    campo de dataclass. O relatorio nao adivinha o tipo: tenta os tres e mostra o que
    encontrou, porque um nome pode ser as tres coisas."""
    linhas = [f"IMPACTO DE: {alvo}", "=" * 78]

    rotas = rotas_que_dependem_de(alvo)
    if rotas:
        linhas.append("\nROTAS DO CATALOGO QUE DEPENDEM (grafo de DADO, confiavel):")
        for r, c in rotas: linhas.append(f"   {r:20} campo `{c}`")

    folha = alvo.split(".")[-1]
    lidas = quem_le(folha)
    if lidas:
        linhas.append(f"\nMODULOS QUE LEEM A CHAVE `{folha}`:")
        for m, ls in sorted(lidas.items()):
            linhas.append(f"   {m:20} linhas {', '.join(map(str, ls[:8]))}")

    chamadores = quem_chama(alvo)
    if chamadores:
        linhas.append(f"\nQUEM CHAMA `{alvo}` DIRETAMENTE:")
        for f, m in chamadores: linhas.append(f"   {m:20} {f}")
        indireto = [x for x in alcance_de_funcao(alvo) if x not in chamadores]
        if indireto:
            linhas.append("\nE QUEM CHEGA ATE ELA INDIRETAMENTE:")
            for f, m in indireto: linhas.append(f"   {m:20} {f}")

    usos = quem_usa_campo(alvo)
    if usos:
        linhas.append(f"\nACESSOS AO CAMPO `.{alvo}`:")
        for m, ln, txt in usos[:20]: linhas.append(f"   {m}:{ln}  {txt}")

    if len(linhas) == 2:
        linhas.append("\n   NADA ENCONTRADO — e isso NAO significa que nada depende.")
        linhas.append("   Confira as leituras cegas abaixo antes de concluir.")

    cegas = leituras_cegas()
    if cegas:
        linhas.append(f"\nPONTOS CEGOS DO MAPA ({len(cegas)}): chave montada em tempo de")
        linhas.append("execucao. Toda conclusao de 'ninguem le' passa por aqui primeiro.")
        for m, ln, txt in cegas[:12]:
            linhas.append(f"   {m}:{ln}  {txt}")
    return "\n".join(linhas)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(relatorio(sys.argv[1])); raise SystemExit(0)
    g = grafo_de_modulos()
    print("=" * 78); print("MAPA DE IMPACTO — visao geral"); print("=" * 78)
    print("\nGRAFO DE MODULOS")
    for m, dep in sorted(g.items()):
        if dep: print(f"   {m:16} -> {', '.join(dep)}")
    arestas = referencias_do_catalogo()
    print(f"\nCATALOGO -> CUSTOS: {len(arestas)} referencias (grafo de DADO)")
    alvos: dict[str, list[str]] = {}
    for r, c, a in arestas: alvos.setdefault(a, []).append(r)
    for a, rs in sorted(alvos.items(), key=lambda kv: -len(kv[1]))[:10]:
        print(f"   {a:42} <- {len(rs)} rota(s): {', '.join(sorted(rs)[:4])}"
              + (" ..." if len(rs) > 4 else ""))
    cegas = leituras_cegas()
    print(f"\nPONTOS CEGOS: {len(cegas)} leituras com chave nao literal")
    for m, ln, txt in cegas[:10]: print(f"   {m}:{ln}  {txt}")
    print("\nUse:  python impacto.py <caminho.yaml | funcao | campo>")

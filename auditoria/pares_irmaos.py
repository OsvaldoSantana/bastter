# -*- coding: utf-8 -*-
"""
pares_irmaos.py -- o auditor do achado A-07.

A pergunta, e ela nao e de revisao de codigo, e de auditoria:

    quando a MESMA condicao aparece em dois lugares do projeto, os dois a tratam igual?

O A-07 nasceu de um caso concreto: "resposta que nao desembrulha para objeto" devolvia
AVISO no `linhas_do_suplemento` e era `continue` MUDO no `linhas_do_paginado`. Mesma
condicao, mesmo modulo, duas leituras discordando -- e a muda vencia, porque e a que
roda oito mil vezes.

ESTE SCRIPT NAO DECIDE NADA. Ele levanta CANDIDATOS. A doutrina P3 (portoes, nao
pontuacao) vale aqui tambem: um par que discorda pode ser divergencia legitima -- ler
config e ler resposta de rede sao coisas diferentes e podem falhar diferente. O que o
script faz e tirar o par do anonimato, para que alguem tenha de dizer POR QUE diferem.

Saida: uma tabela de (familia de condicao) x (tratamento) x (onde), e a lista dos
conflitos -- familias tratadas de mais de um jeito dentro do mesmo modulo.
"""

import argparse
import ast
import os
import sys
from collections import defaultdict

# ── as familias de condicao. A chave e o nome; o valor, marcas no texto do teste.
# Deliberadamente CRUAS: e melhor levantar candidato demais e descartar lendo do que
# perder o par que importa. Falso positivo custa leitura; falso negativo custa serie.
FAMILIAS = [
    ("AUSENTE",        ["is None", "is not None", "not dados", "not valor", "not d.get",
                        "not e.get", "not cfg", "not v", "not x"]),
    ("VAZIO",          ["== []", "== {}", "== ''", '== ""', "len(", "not lista",
                        "not linhas", "not itens", "not resultados"]),
    ("TIPO",           ["isinstance"]),
    ("CHAVE_FALTANDO", [" not in ", " in "]),
    ("ZERO_OU_NEG",    ["<= 0", "< 0", "== 0", "> 0", ">= 0"]),
    ("EXPIRADO",       ["expira", "vencid", "validade", "venceu"]),
    ("STATUS_FRACO",   ["NAO_CONFIRMADO", "PARCIAL", "OBSERVADO", "status"]),
]

LEVANTA  = "LEVANTA"    # raise / SystemExit / assert -- o mais ruidoso
AVISA    = "AVISA"      # print / warn / acumula aviso -- ruidoso e segue
NEUTRO   = "RET_NEUTRO"  # return None/0/[]/{}/False -- silencioso, com valor
PULA     = "PULA"       # continue / pass -- o mais silencioso de todos
CORRIGE  = "CORRIGE"    # atribui um valor no lugar -- silencioso E opinativo
SEGUE    = "SEGUE"

ORDEM_DE_RUIDO = {LEVANTA: 4, AVISA: 3, NEUTRO: 2, CORRIGE: 1, PULA: 0, SEGUE: 0}


def familias_de(texto):
    return [nome for nome, marcas in FAMILIAS if any(m in texto for m in marcas)]


def tratamento_de(corpo):
    """O que o ramo FAZ. Olha so o primeiro nivel: o que acontece quando a condicao
    bate, nao o que acontece dentro de um sub-if."""
    tratos = set()
    for no in corpo:
        if isinstance(no, ast.Raise):
            tratos.add(LEVANTA)
        elif isinstance(no, ast.Assert):
            tratos.add(LEVANTA)
        elif isinstance(no, ast.Continue):
            tratos.add(PULA)
        elif isinstance(no, ast.Pass):
            tratos.add(PULA)
        elif isinstance(no, ast.Return):
            v = no.value
            if v is None:
                tratos.add(NEUTRO)
            elif isinstance(v, ast.Constant) and v.value in (None, 0, False, "", 0.0):
                tratos.add(NEUTRO)
            elif isinstance(v, (ast.List, ast.Dict, ast.Tuple)) and not getattr(v, "elts", getattr(v, "keys", [1])):
                tratos.add(NEUTRO)
            else:
                tratos.add("RET_VALOR")
        elif isinstance(no, (ast.Assign, ast.AugAssign)):
            tratos.add(CORRIGE)
        elif isinstance(no, ast.Expr):
            c = no.value
            if isinstance(c, ast.Call):
                alvo = ast.unparse(c.func)
                if alvo.endswith("print") or "warn" in alvo or "aviso" in alvo.lower():
                    tratos.add(AVISA)
                elif alvo.endswith(("append", "add", "setdefault")):
                    # acumular numa lista chamada aviso/erro/desconhecido E avisar
                    tratos.add(AVISA if any(k in alvo.lower() for k in
                               ("aviso", "erro", "desconhecid", "falta", "pendenc",
                                "nao_objeto", "multipl", "vazias", "fora")) else CORRIGE)
                else:
                    tratos.add(CORRIGE)
    if not tratos:
        tratos.add(SEGUE)
    return sorted(tratos, key=lambda t: -ORDEM_DE_RUIDO.get(t, 2))[0]


class Varredura(ast.NodeVisitor):
    def __init__(self, modulo):
        self.modulo = modulo
        self.func = "<modulo>"
        self.achados = []

    def visit_FunctionDef(self, no):
        antes, self.func = self.func, no.name
        self.generic_visit(no)
        self.func = antes

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_If(self, no):
        try:
            texto = ast.unparse(no.test)
        except Exception:                                   # noqa: BLE001
            texto = ""
        for fam in familias_de(texto):
            self.achados.append({
                "modulo": self.modulo, "func": self.func, "linha": no.lineno,
                "familia": fam, "teste": texto[:90],
                "trato": tratamento_de(no.body),
            })
        self.generic_visit(no)


def varrer(caminhos):
    tudo = []
    for c in caminhos:
        nome = os.path.basename(c)
        with open(c, encoding="utf-8") as f:
            fonte = f.read()
        v = Varredura(nome)
        v.visit(ast.parse(fonte))
        tudo.extend(v.achados)
    return tudo


def conflitos(achados, por_modulo=True):
    """Um conflito e uma familia tratada de mais de um jeito -- dentro do mesmo modulo
    (o caso A-07) ou no projeto inteiro."""
    chave = (lambda a: (a["modulo"], a["familia"])) if por_modulo else (lambda a: (a["familia"],))
    grupos = defaultdict(list)
    for a in achados:
        grupos[chave(a)].append(a)
    saida = []
    for k, itens in sorted(grupos.items()):
        tratos = {i["trato"] for i in itens}
        if len(tratos) > 1:
            saida.append((k, tratos, itens))
    return saida


def main(argv=None):
    p = argparse.ArgumentParser(description="Auditor A-07: pares de funcoes irmas.")
    p.add_argument("caminhos", nargs="+", help="arquivos .py a auditar")
    p.add_argument("--familia", help="filtra uma familia")
    p.add_argument("--global", dest="glob", action="store_true",
                   help="conflitos no projeto inteiro, nao so dentro de cada modulo")
    a = p.parse_args(argv)

    arquivos = []
    for c in a.caminhos:
        if os.path.isdir(c):
            arquivos += [os.path.join(c, f) for f in sorted(os.listdir(c))
                         if f.endswith(".py")]
        else:
            arquivos.append(c)
    arquivos = [f for f in arquivos if not os.path.basename(f).startswith("test_")]

    achados = varrer(arquivos)
    if a.familia:
        achados = [x for x in achados if x["familia"] == a.familia]

    print("%d guarda(s) em %d arquivo(s)\n" % (len(achados), len(arquivos)))
    confs = conflitos(achados, por_modulo=not a.glob)
    print("=" * 78)
    print("CANDIDATOS -- mesma familia de condicao, tratamentos que DISCORDAM")
    print("=" * 78)
    for k, tratos, itens in confs:
        print("\n%s  [%s]" % (" / ".join(k), ", ".join(sorted(tratos))))
        for i in sorted(itens, key=lambda x: (-ORDEM_DE_RUIDO.get(x["trato"], 2), x["linha"])):
            print("   %-11s %s:%-4d %-28s %s"
                  % (i["trato"], i["modulo"], i["linha"], i["func"], i["teste"][:52]))
    print("\n%d candidato(s). Nenhum deles e um achado ate alguem LER os dois e dizer\n"
          "por que diferem -- ou admitir que nao ha por que." % len(confs))
    return 0


if __name__ == "__main__":
    sys.exit(main())

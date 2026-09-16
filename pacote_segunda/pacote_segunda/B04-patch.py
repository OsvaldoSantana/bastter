# -*- coding: utf-8 -*-
"""Aplica o B-04 no pyproject.toml: remove [build-system]. Idempotente."""
import io, os, sys, tomllib

p = sys.argv[1] if len(sys.argv) > 1 else "pyproject.toml"
s = io.open(p, encoding="utf-8").read()
# A GUARDA olha a MARCA do patch, nao a string removida: a nota que eu insiro
# MENCIONA `[build-system]` em prosa, e uma guarda pela string voltaria a casar com o
# proprio comentario e aplicaria o patch duas vezes. Achado meu, ao testar a segunda
# rodada -- guarda de idempotencia tambem precisa ser testada rodando duas vezes.
MARCA = "B-04, 13/09/2026"
if MARCA in s:
    sys.exit("ja aplicado: a nota do B-04 ja esta em %s" % p)
if not s.lstrip().startswith("#") and "[build-system]" not in s:
    sys.exit("nada a fazer: nao ha [build-system] em %s" % p)

antes = tomllib.load(open(p, "rb"))
i, j = s.index("[build-system]"), s.index("[project]")
assert i < j, "[build-system] depois de [project] -- layout inesperado, PARE"

NOTA = '''# ── B-04, 13/09/2026: por que NAO ha [build-system] aqui ────────────────────
# Havia. Ele declarava `setuptools.build_meta`, e `pip install -e .` FALHAVA: o
# repositorio tem varios diretorios de topo (alocacao, fase0, auditoria, docs) e a
# descoberta automatica do setuptools nao sabe qual e o pacote.
#
# A correcao obvia seria declarar os pacotes. Nao e a certa, e a razao e a doutrina
# deste projeto: **ninguem instala este projeto.** `ambiente.comando_de_instalacao()`
# monta `python -m pip install "numpy==..." "pandas==..."` -- instala as DEPENDENCIAS,
# nunca o pacote. Os modulos sao importados por caminho, e nenhuma linha faz
# `import bastter`.
#
# Entao `[build-system]` era um arquivo declarando um comportamento que o codigo nao
# tem -- o defeito recorrente do projeto, na forma mais barata de corrigir: apagar a
# promessa em vez de construir o que ela promete.
#
# ESTE ARQUIVO E UM MANIFESTO, nao uma definicao de pacote. Ele existe para ser LIDO
# por `ambiente.declarado()` via tomllib, e a P-15 depende disso -- nao de build.
#
# MEDIDO ANTES DE APAGAR: a impressao digital do ambiente e 7565df1381e2c1ed com e
# sem esta secao. A remocao nao pode invalidar resultado pre-registrado nenhum.
# ─────────────────────────────────────────────────────────────────────────────

'''
s2 = s[:i] + NOTA + s[j:]
depois = tomllib.loads(s2)
assert depois["project"] == antes["project"], "o bloco [project] mudou -- ABORTADO"
assert depois.get("tool") == antes.get("tool"), "o bloco [tool] mudou -- ABORTADO"
io.open(p, "w", encoding="utf-8").write(s2)
print("B-04 aplicado em %s -- [project] e [tool] intactos" % os.path.abspath(p))

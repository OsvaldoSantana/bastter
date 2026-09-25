# -*- coding: utf-8 -*-
"""
Procedencia do AMBIENTE de execucao. Fecha a pendencia P-15.

Por que este modulo existe:
  O projeto ja sabia dizer de onde veio cada NUMERO (`status`/`fonte`/`acesso`/
  `expira` em 55 constantes) e de onde veio cada DADO (`hash_fonte()` da serie do
  NEFIN, fixado em teste). Nao sabia dizer de onde veio o RESULTADO — em qual
  ambiente ele foi calculado.

  Isso importa por uma razao especifica e nao por elegancia: `alfa_contra_fatores()`
  resolve um sistema linear por `numpy.linalg.lstsq`, e `mensal()` compoe retornos
  por `pandas.groupby`. Um clone em outra maquina, com outras versoes, roda os mesmos
  testes, produz um numero possivelmente diferente, e ninguem tem como perceber. E o
  mesmo modo de falha do achado F-04 (CRLF mudava o sha256 da serie), deslocado do
  dado para a maquina.

O CONTRATO, e ele e deliberadamente assimetrico:
  DECLARAR      pyproject.toml e a fonte unica das versoes. Este modulo LE, nunca
                repete. Repetir seria o achado N-01 outra vez.
  EXIGIR        toda dependencia importada tem de estar declarada, e vice-versa.
                Isso e erro duro: e o "funciona na minha maquina" em forma testavel.
  AVISAR        rodar com versao diferente da registrada NAO quebra a suite. Quebra a
                REPRODUCAO — e so as funcoes que produzem numero pre-registrado
                carregam a impressao do ambiente e avisam quando ela nao bate.

  A assimetria e o ponto. Um teste que ficasse vermelho porque a maquina do usuario
  tem outro numpy puniria trabalho legitimo com um alarme que nao e sobre o codigo.
  Um backtest que nao dissesse em que ambiente rodou seria meio pre-registro.
"""
from __future__ import annotations
import hashlib, os, sys, importlib.metadata as md

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PYPROJECT = os.path.join(RAIZ, "pyproject.toml")

# nome do import -> nome da distribuicao. E a armadilha classica: `import yaml`
# instala-se como `PyYAML`, e quem confia no nome do import esquece de declarar.
IMPORT_PARA_PACOTE = {"yaml": "PyYAML"}
PACOTE_PARA_IMPORT = {v: k for k, v in IMPORT_PARA_PACOTE.items()}


class AmbienteIndeclarado(Exception):
    """Uma dependencia foi importada e nao esta no pyproject, ou o contrario."""


def _tomllib():
    import tomllib          # 3.11+; a faixa de requires-python garante
    return tomllib


def declarado(path=None):
    """Le o pyproject. Devolve dict com `versoes`, `numericas`, `ferramentas`,
    `python`. NAO tem valores de reserva: se o arquivo sumir, e erro, porque sem ele
    nao ha nada a conferir."""
    p = path or PYPROJECT
    if not os.path.exists(p):
        raise AmbienteIndeclarado(
            f"{p} nao encontrado. Sem ele o projeto nao sabe dizer em que ambiente os "
            f"resultados pre-registrados foram produzidos — e a P-15 volta a estar aberta.")
    with open(p, "rb") as f:
        d = _tomllib().load(f)
    proj = d["project"]
    versoes = {}
    for linha in list(proj.get("dependencies", [])) + \
                 list(proj.get("optional-dependencies", {}).get("dev", [])):
        if "==" not in linha:
            raise AmbienteIndeclarado(
                f"dependencia sem pino exato: {linha!r}. Faixa (>=) permite que um "
                f"`pip install` amanha mude um numero registrado hoje sem aviso.")
        nome, v = linha.split("==", 1)
        versoes[nome.strip()] = v.strip()
    cls = d.get("tool", {}).get("meol", {}).get("dependencias", {})
    return dict(versoes=versoes, python=proj["requires-python"],
                numericas=list(cls.get("numericas", [])),
                ferramentas=list(cls.get("ferramentas", [])))


def instalado(pacotes=None):
    """Versoes REALMENTE instaladas agora. `None` = o pacote nao esta la."""
    D = declarado()
    out = {}
    for nome in (pacotes or D["versoes"]):
        try: out[nome] = md.version(nome)
        except md.PackageNotFoundError: out[nome] = None
    return out


def versao_python():
    return ".".join(str(x) for x in sys.version_info[:3])


def impressao(path=None):
    """Impressao digital do ambiente DECLARADO. E o que viaja junto de um resultado.

    Deliberadamente calculada sobre o pyproject e nao sobre o que esta instalado: a
    impressao identifica o ambiente que o projeto AFIRMA ser o de referencia. O que
    esta instalado se compara contra ela — se a impressao viesse do instalado, ela
    mudaria junto com a divergencia e nunca acusaria nada."""
    D = declarado(path)
    texto = "|".join([D["python"]] + [f"{k}=={D['versoes'][k]}" for k in sorted(D["versoes"])])
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16]


def conferir(avisar=True):
    """Compara o instalado com o declarado. Devolve (numericas_divergentes,
    ferramentas_divergentes, ausentes).

    Divergencia NUMERICA e a unica que fala sobre a validade de um resultado; e por
    isso que ela sai separada, e nao numa lista unica de "coisas diferentes"."""
    D, inst = declarado(), instalado()
    ausentes = sorted(k for k, v in inst.items() if v is None)
    div = {k: (D["versoes"][k], inst[k]) for k in D["versoes"]
           if inst[k] is not None and inst[k] != D["versoes"][k]}
    num = {k: v for k, v in div.items() if k in D["numericas"]}
    fer = {k: v for k, v in div.items() if k not in D["numericas"]}
    if avisar and num:
        det = "; ".join(f"{k}: registrado {a}, rodando {b}" for k, (a, b) in sorted(num.items()))
        print(f"  [AVISO] ambiente NUMERICO diferente do registrado ({det}). Os testes "
              f"continuam validos — o que deixa de valer e a REPRODUCAO de um resultado "
              f"pre-registrado, que passa a ser um numero novo e nao a conferencia de um "
              f"antigo.", file=sys.stderr)
    return num, fer, ausentes


def selo():
    """O bloco que acompanha qualquer resultado pre-registrado."""
    num, fer, aus = conferir(avisar=False)
    return dict(impressao=impressao(), python=versao_python(),
                instalado=instalado(), reproduz_o_registrado=not (num or aus),
                divergencia_numerica=num, divergencia_de_ferramenta=fer, ausentes=aus)


def comando_de_instalacao():
    """O comando exato, montado a partir do pyproject.

    Nao existe requirements.txt neste projeto DE PROPOSITO: duas listas de versoes
    concordando e o achado N-01 — editar uma nao muda nada e ninguem descobre. A
    lista mora no pyproject; o comando se deriva dela."""
    D = declarado()
    pinos = " ".join(f'"{k}=={v}"' for k, v in sorted(D["versoes"].items()))
    return f"python -m pip install {pinos}"


if __name__ == "__main__":
    if "--instalar" in sys.argv:
        print(comando_de_instalacao()); raise SystemExit(0)
    D = declarado()
    print("=" * 78)
    print("AMBIENTE DE EXECUCAO — pendencia P-15")
    print("=" * 78)
    print(f"pyproject: {PYPROJECT}")
    print(f"impressao declarada: {impressao()}")
    print(f"python: requer {D['python']} · rodando {versao_python()}\n")
    inst = instalado()
    print(f"{'pacote':<12}{'declarado':>12}{'instalado':>12}   consequencia se divergir")
    for k in sorted(D["versoes"]):
        c = "MUDA NUMERO" if k in D["numericas"] else "nao muda numero"
        marca = "" if inst[k] == D["versoes"][k] else "   <- DIFERENTE"
        print(f"{k:<12}{D['versoes'][k]:>12}{str(inst[k]):>12}   {c}{marca}")
    num, fer, aus = conferir()
    print()
    if not (num or fer or aus):
        print("  O ambiente instalado E o registrado. Um resultado produzido aqui")
        print("  reproduz um resultado pre-registrado.")
    else:
        if aus: print(f"  AUSENTES: {', '.join(aus)} — o projeto nao roda completo")
        if fer: print(f"  ferramenta diferente ({', '.join(fer)}): nao afeta numero nenhum")
        if num: print("  NUMERICA diferente: a reproducao do backtest nao vale mais")
        print(f"\n  para igualar:\n    {comando_de_instalacao()}")

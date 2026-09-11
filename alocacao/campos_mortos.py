# -*- coding: utf-8 -*-
"""
Guarda de codigo morto do lado Python. Ponto "Campos mortos, 4a ocorrencia" de
`AUDITORIA-DEEPSEEK-CONFERIDA.md`: o projeto tem
`test_P28_secao_operacional_nao_tem_chave_morta` protegendo o YAML (chave declarada
e nunca lida) e nada equivalente para o Python -- campo de dataclass ou constante de
modulo declarado e nunca referenciado de novo. Isto e o N-01 esperando acontecer do
lado do codigo, e este modulo e a rede que faltava.

Dos quatro campos que a auditoria citou, so DOIS cabem aqui:
  `DIFERIDOS_K` (tese.py)       constante de modulo -- em escopo
  `status_do_variavel` (aporte.py, campo de dataclass) -- em escopo
  `corretora.promocional`       e chave de YAML, ja coberta por
                                 `test_P28_secao_operacional_nao_tem_chave_morta`
                                 (esta na `DIVIDA_DE_COBERTURA`, P-32) -- fora daqui
  `estado_io.reserva_empenhada` era uma CHAVE DE DICT (`d["reserva_empenhada"]`),
                                 nao campo de dataclass nem constante de modulo --
                                 e ja foi corrigido (P-71/P-72, 11/09/2026): o dict
                                 nao guarda mais o valor, so valida -- fora daqui

O QUE ISTO ENXERGA
  campo de dataclass     toda classe com `@dataclass`, os `AnnAssign` do corpo dela
  constante de modulo    `Assign`/`AnnAssign` de `Name` simples, direto no corpo do
                         MODULO (fora de def/classe, fora de `if __name__ == "__main__"`)
  referencia             em qualquer modulo de PRODUCAO (nunca teste, demo ou
                         conftest -- no espirito do `impacto.py` e do P-28, porque
                         "so o teste constroi" e exatamente o padrao que a P-71
                         mostrou ser insuficiente): `Attribute` (`obj.campo`),
                         `keyword` de chamada (`Classe(campo=...)`), `Name` solto
                         (`NOME`), OU chave de `Dict` com o mesmo texto
                         (`{**x.__dict__, "campo": v}` -- o idioma que `alocacao.py`
                         usa para "clonar com um campo trocado")

O QUE ISTO NAO ENXERGA, declarado -- e a lista importa mais que a de cima:
  - `getattr(obj, nome)` com nome dinamico, e despacho por dicionario: invisiveis,
    como em `impacto.py`.
  - CONSTRUIR um campo (`Classe(campo=x)`, ou a chave de dict acima) conta como
    referencia MESMO QUE o valor nunca seja lido de volta (`.campo`) em lugar
    nenhum. Um campo so ESCRITO e nunca LIDO passa como vivo aqui -- era exatamente
    o padrao de `estado_io.reserva_empenhada` antes da correcao, e esta guarda
    sozinha NAO o teria pego. Escrita e leitura sao duas perguntas diferentes; esta
    guarda so responde "o nome aparece de novo em algum lugar executavel?".
  - correspondencia e por NOME, nao por classe: um campo `nome` bate com QUALQUER
    `Attribute`/`keyword`/chave de dict chamado `nome` no projeto inteiro, nao so
    o do dataclass em questao. Superamostragem deliberada: para nomes genericos
    (`nome`, `valor`, `saldo`) isso quase sempre evita falso positivo; para nomes
    distintivos (`DIFERIDOS_K`, `status_do_variavel`) a precisao e alta porque a
    chance de colisao e baixa.
  - `dataclasses.fields(Classe)` e `dataclasses.asdict(obj)` iterando por reflexao
    nao produzem `Attribute`/`keyword`/chave de dict com o nome literal -- ficam
    invisiveis, como qualquer outra forma de acesso dinamico.
  - string solta em docstring/mensagem de erro NAO conta (so chave de dict conta
    entre os literais de string) -- e a direcao certa: citar o nome numa frase nao
    e uso.

Um mapa que finge completude e pior que nao ter mapa. As duas listas andam juntas.
"""
from __future__ import annotations
import ast
import os

AQUI = os.path.dirname(os.path.abspath(__file__))


def _modulos():
    """Mesmo filtro de impacto.py: todo .py de producao, nunca teste, demo ou conftest."""
    return sorted(f for f in os.listdir(AQUI)
                  if f.endswith(".py") and not f.startswith(("test_", "demo_", "conftest")))


def _arvore(f):
    return ast.parse(open(os.path.join(AQUI, f), encoding="utf-8").read(), filename=f)


def campos_de_dataclass(modulos=None):
    """{(modulo, classe, campo): (lineno, col_offset)} -- todo AnnAssign direto no
    corpo de uma classe decorada com @dataclass."""
    out = {}
    for f in (modulos or _modulos()):
        for n in ast.walk(_arvore(f)):
            if not isinstance(n, ast.ClassDef):
                continue
            decoradores = {d.id for d in n.decorator_list if isinstance(d, ast.Name)}
            if "dataclass" not in decoradores:
                continue
            for item in n.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    out[(f, n.name, item.target.id)] = (item.target.lineno, item.target.col_offset)
    return out


def _e_bloco_main(no_if):
    """`if __name__ == "__main__":` -- variavel de script, nao constante do sistema."""
    t = no_if.test
    return (isinstance(t, ast.Compare) and isinstance(t.left, ast.Name)
            and t.left.id == "__name__")


def constantes_de_modulo(modulos=None):
    """{(modulo, nome): (lineno, col_offset)} -- Assign/AnnAssign de Name simples
    direto no corpo do MODULO, fora de `if __name__ == "__main__"`."""
    out = {}
    for f in (modulos or _modulos()):
        for item in _arvore(f).body:
            if isinstance(item, ast.If) and _e_bloco_main(item):
                continue
            alvo = None
            if isinstance(item, ast.Assign) and len(item.targets) == 1 \
               and isinstance(item.targets[0], ast.Name):
                alvo = item.targets[0]
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                alvo = item.target
            if alvo is not None:
                out[(f, alvo.id)] = (alvo.lineno, alvo.col_offset)
    return out


def _referencias(nome, modulos=None):
    """Toda ocorrencia, em qualquer modulo de producao, onde `nome` aparece como
    Attribute, keyword de chamada, Name solto, ou chave de Dict -- na ARVORE, nunca
    em texto bruto. Devolve [(modulo, lineno, col_offset)]."""
    out = []
    for f in (modulos or _modulos()):
        for n in ast.walk(_arvore(f)):
            if isinstance(n, ast.Attribute) and n.attr == nome:
                out.append((f, n.lineno, n.col_offset))
            elif isinstance(n, ast.keyword) and n.arg == nome:
                out.append((f, n.lineno, n.col_offset))
            elif isinstance(n, ast.Name) and n.id == nome:
                out.append((f, n.lineno, n.col_offset))
            elif isinstance(n, ast.Dict):
                for chave in n.keys:
                    if isinstance(chave, ast.Constant) and chave.value == nome:
                        out.append((f, chave.lineno, chave.col_offset))
    return out


def campos_nao_referenciados():
    """(mortos_campo, mortos_const), cada item com a posicao da propria definicao
    excluida da busca por referencia. Ordenado para saida estavel."""
    mods = _modulos()
    todas_as_refs = {}  # cache: nome -> [(modulo, lineno, col)]

    def refs_de(nome):
        if nome not in todas_as_refs:
            todas_as_refs[nome] = _referencias(nome, mods)
        return todas_as_refs[nome]

    mortos_campo = []
    for (f, classe, campo), pos_def in campos_de_dataclass(mods).items():
        restantes = [r for r in refs_de(campo) if r != (f,) + pos_def]
        if not restantes:
            mortos_campo.append((f, classe, campo, pos_def[0]))

    mortos_const = []
    for (f, nome), pos_def in constantes_de_modulo(mods).items():
        restantes = [r for r in refs_de(nome) if r != (f,) + pos_def]
        if not restantes:
            mortos_const.append((f, nome, pos_def[0]))

    return sorted(mortos_campo), sorted(mortos_const)


def relatorio():
    campo, const = campos_nao_referenciados()
    linhas = ["=" * 78, "CAMPOS DE DATACLASS SEM REFERENCIA ALEM DA PROPRIA DEFINICAO", "=" * 78]
    for f, classe, campo_, ln in campo:
        linhas.append(f"   {f}:{ln}  {classe}.{campo_}")
    if not campo:
        linhas.append("   (nenhum)")
    linhas += ["", "=" * 78, "CONSTANTES DE MODULO SEM REFERENCIA ALEM DA PROPRIA DEFINICAO", "=" * 78]
    for f, nome, ln in const:
        linhas.append(f"   {f}:{ln}  {nome}")
    if not const:
        linhas.append("   (nenhuma)")
    return "\n".join(linhas)


if __name__ == "__main__":
    print(relatorio())

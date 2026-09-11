# -*- coding: utf-8 -*-
"""
Guarda de codigo morto do lado Python. Ponto "Campos mortos, 4a ocorrencia" de
`AUDITORIA-DEEPSEEK-CONFERIDA.md`: o projeto tinha
`test_P28_secao_operacional_nao_tem_chave_morta` protegendo o YAML (chave declarada
e nunca lida) e nada equivalente para o Python -- campo de dataclass ou constante de
modulo declarado e nunca referenciado de novo. E o N-01 esperando acontecer do lado
do codigo; o inventario e os testes estao em `test_campos_mortos.py`.

Os quatro da auditoria, decididos em 11/09/2026 (o porque de cada um esta em
PENDENCIAS.md): `Aporte.status_do_variavel` e `tese.DIFERIDOS_K` foram REMOVIDOS;
`reserva_empenhada` (estado_io) e `corretora.promocional` (politica.yaml) passaram a
ser USADOS, os dois como guarda. So os dois primeiros eram visiveis a esta guarda: o
terceiro e chave de dict e o quarto e chave de YAML, que o P-28 ja cobre.

O QUE ISTO ENXERGA
  campo de dataclass     toda classe com `@dataclass`, os `AnnAssign` do corpo dela
  constante de modulo    `Assign`/`AnnAssign` de `Name` simples, direto no corpo do
                         MODULO (fora de def/classe, fora do bloco `__main__`)
  referencia             em qualquer modulo de PRODUCAO -- nunca teste, demo ou
                         conftest, porque "so o teste constroi" e exatamente o padrao
                         que a P-71 mostrou ser insuficiente: `Attribute`
                         (`obj.campo`), `keyword` de chamada (`Classe(campo=...)`),
                         `Name` solto, ou chave literal de `Dict` -- o idioma que
                         `alocacao.py` usa para clonar um dataclass com um campo trocado

O QUE ISTO NAO ENXERGA, declarado -- e a lista importa mais que a de cima:
  - `getattr(obj, nome)` com nome dinamico, e despacho por dicionario: invisiveis,
    como em `impacto.py`.
  - CONSTRUIR um campo (keyword ou chave de dict) conta como referencia MESMO QUE o
    valor nunca seja lido de volta. Um campo so ESCRITO e nunca LIDO passa como vivo
    aqui. Escrita e leitura sao duas perguntas; esta guarda so responde "o nome
    aparece de novo em algum lugar executavel?".
  - a correspondencia e por NOME, nao por classe: um campo `nome` bate com qualquer
    `nome` do projeto. Superamostragem deliberada -- para nome generico isso evita
    falso positivo e custa falso negativo; para nome distintivo a precisao e alta.
  - `dataclasses.fields()` e `asdict()` iterando por reflexao ficam invisiveis.
  - uso SO em teste conta como morto. E a direcao certa para dado de negocio (P-71)
    e pode ser rigor demais para um utilitario que um teste real consome -- o caso
    `ambiente.PACOTE_PARA_IMPORT`, que esta no inventario por isso.
  - nome citado em docstring, comentario ou mensagem nao conta: citar nao e usar.

Um mapa que finge completude e pior que nao ter mapa. As duas listas andam juntas.
"""
from __future__ import annotations
import ast
import os

AQUI = os.path.dirname(os.path.abspath(__file__))


def _modulos(raiz=AQUI):
    """Mesmo filtro de impacto.py: todo .py de producao, nunca teste, demo ou conftest."""
    return sorted(f for f in os.listdir(raiz)
                  if f.endswith(".py") and not f.startswith(("test_", "demo_", "conftest")))


def _arvore(f, raiz=AQUI):
    with open(os.path.join(raiz, f), encoding="utf-8") as fh:
        return ast.parse(fh.read(), filename=f)


def _e_bloco_main(no):
    t = no.test
    return (isinstance(t, ast.Compare) and isinstance(t.left, ast.Name)
            and t.left.id == "__name__")


def definicoes(raiz=AQUI):
    """{rotulo: (arquivo, nome, (linha, coluna))}. Rotulo `arq.py:Classe.campo` para
    campo de dataclass e `arq.py:NOME` para constante de modulo."""
    out: dict[str, tuple[str, str, tuple[int, int]]] = {}
    for f in _modulos(raiz):
        arvore = _arvore(f, raiz)
        for n in ast.walk(arvore):
            if not isinstance(n, ast.ClassDef):
                continue
            if "dataclass" not in {d.id for d in n.decorator_list if isinstance(d, ast.Name)}:
                continue
            for item in n.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    alvo = item.target
                    out[f"{f}:{n.name}.{alvo.id}"] = (f, alvo.id, (alvo.lineno, alvo.col_offset))
        for item in arvore.body:
            if isinstance(item, ast.If) and _e_bloco_main(item):
                continue
            nome = None
            if isinstance(item, ast.Assign) and len(item.targets) == 1 \
               and isinstance(item.targets[0], ast.Name):
                nome = item.targets[0]
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                nome = item.target
            if nome is not None:
                out[f"{f}:{nome.id}"] = (f, nome.id, (nome.lineno, nome.col_offset))
    return out


def referencias(raiz=AQUI):
    """{nome: {(arquivo, linha, coluna)}} -- toda aparicao executavel de um nome, na
    ARVORE e nunca no texto, numa passada so por modulo."""
    out: dict[str, set[tuple[str, int, int]]] = {}

    def marca(nome, f, no):
        out.setdefault(nome, set()).add((f, no.lineno, no.col_offset))

    for f in _modulos(raiz):
        for n in ast.walk(_arvore(f, raiz)):
            if isinstance(n, ast.Attribute):
                marca(n.attr, f, n)
            elif isinstance(n, ast.keyword) and n.arg:
                marca(n.arg, f, n)
            elif isinstance(n, ast.Name):
                marca(n.id, f, n)
            elif isinstance(n, ast.Dict):
                for k in n.keys:
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        marca(k.value, f, k)
    return out


def mortos(raiz=AQUI):
    """Rotulos cuja UNICA aparicao executavel e a propria definicao. Ordenado."""
    refs = referencias(raiz)
    return sorted(rot for rot, (f, nome, pos) in definicoes(raiz).items()
                  if not (refs.get(nome, set()) - {(f,) + pos}))


if __name__ == "__main__":
    lista = mortos()
    print("=" * 78)
    print(f"CAMPOS E CONSTANTES SEM REFERENCIA ALEM DA PROPRIA DEFINICAO: {len(lista)}")
    print("=" * 78)
    for rot in lista:
        print(f"   {rot}")
    print("\nInventario (com pendencia) em test_campos_mortos.py.")

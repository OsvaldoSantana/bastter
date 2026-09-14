# -*- coding: utf-8 -*-
"""
chaves_duplicadas.py -- o defeito que nao faz barulho nenhum.

ACHADO E-09, 13/09/2026. `custos.yaml -> etf:` tinha `IMAB11:` DUAS vezes: uma com
`valor: 0.0025, status: PARCIAL` e fonte do gestor, escrita em 05/09; outra oitenta
linhas abaixo com `valor: null, status: NAO_CONFIRMADO`.

**PyYAML resolve chave duplicada ficando com a ULTIMA, sem aviso nenhum.** Entao o
trabalho de 05/09 estava no arquivo e nao tinha efeito: o motor via NAO_CONFIRMADO, o
`PENDENCIAS.md` dizia "fechada", e os dois discordavam em silencio.

E o defeito nao e do IMAB11 -- e do FORMATO. Qualquer constante deste projeto pode ser
apagada por uma duplicata em outro ponto do mesmo arquivo, e nada acusa.
"""

import sys

import yaml


class DuplicataProibida(Exception):
    pass


class LoaderEstrito(yaml.SafeLoader):
    """SafeLoader que RECUSA chave duplicada em vez de escolher uma."""


MERGE = "tag:yaml.org,2002:merge"


def _mapping(loader, node, deep=False):
    """Checa duplicata ANTES de achatar o merge, e so entre os pares EXPLICITOS do no.

    Duas sutilezas, e as duas me custaram uma rodada:

    1. o `catalogo.yaml` usa ancora e merge (`<<: *base`). Sobrescrever uma chave da
       ancora NAO e duplicata -- e o proposito do merge. Por isso a checagem olha so
       os pares escritos neste no, e pula o proprio `<<`;
    2. chave nao-escalar (o valor de `<<` e um no de mapa) nao e hasheavel. Filtrar
       por `ScalarNode` resolve, e de quebra restringe a checagem ao caso que importa:
       nome de constante repetido.
    """
    vistos = {}
    for kn, _vn in node.value:
        if kn.tag == MERGE or not isinstance(kn, yaml.ScalarNode):
            continue
        k = kn.value
        if k in vistos:
            raise DuplicataProibida(
                "chave %r duplicada: linha %d e linha %d. PyYAML ficaria com a "
                "ULTIMA, em silencio -- e foi assim que a taxa do IMAB11 passou oito "
                "dias registrada e sem efeito (achado E-09)."
                % (k, vistos[k] + 1, kn.start_mark.line + 1))
        vistos[k] = kn.start_mark.line
    loader.flatten_mapping(node)
    return yaml.SafeLoader.construct_mapping(loader, node, deep)


LoaderEstrito.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def carregar_estrito(caminho):
    with open(caminho, encoding="utf-8") as f:
        return yaml.load(f, Loader=LoaderEstrito)


def main(argv=None):
    arquivos = (argv or sys.argv[1:])
    if not arquivos:
        sys.exit("uso: chaves_duplicadas.py arquivo.yaml [...]")
    ruins = 0
    for a in arquivos:
        try:
            carregar_estrito(a)
            print("  OK        %s" % a)
        except DuplicataProibida as e:
            ruins += 1
            print("  DUPLICATA %s\n            %s" % (a, e))
        except yaml.YAMLError as e:
            ruins += 1
            print("  ILEGIVEL  %s: %s" % (a, str(e).splitlines()[0]))
    print("\n%d arquivo(s) com duplicata." % ruins)
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main())

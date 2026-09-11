# -*- coding: utf-8 -*-
"""
test_y01_yaml_duplicata.py -- achado Y-01, pendencia P-69.

O QUE ACONTECEU.

`custos.yaml` tinha DUAS entradas `etf.IMAB11` (linhas 171 e 253). PyYAML nao
reclama de chave duplicada dentro do mesmo mapping -- fica com a ULTIMA, em
silencio. A entrada de 05/09 (valor 0,25% a.a., com fonte e data de acesso)
morreu no instante em que foi escrita: `motor.val()` sempre leu a outra,
`valor: null, status: NAO_CONFIRMADO`.

E o F-02 numa camada nova. La, insumo ausente virava zero (a rota parecia
gratis). Aqui, insumo PRESENTE e sobrescrito por um ausente -- a rota fica
bloqueada em vez de simular errado, o que e sorte (o erro caiu do lado
conservador), nao desenho. Nao ha garantia de que a proxima duplicata caia
do mesmo lado.

POR QUE `yaml.safe_load` NAO SERVE DE ORACULO AQUI.

`safe_load` (e `motor.carregar()`) PRODUZ o apagamento que este teste existe
para pegar -- e o proprio mecanismo do defeito, nao uma testemunha dele. Este
teste usa `yaml.compose()`, que devolve a ARVORE DE NOS antes da construcao em
dict: nesse estagio as duas entradas `IMAB11` ainda coexistem como dois pares
(chave, valor) dentro do mesmo MappingNode, e e ali que a duplicata e visivel.

POR QUE E UM TESTE DA CLASSE, NAO DO ATIVO.

Um teste que checasse so `custos.yaml -> etf.IMAB11` seria remendo: provaria
que ESTE ativo, NESTE arquivo, nao repete -- e deixaria passar a proxima
chave duplicada, em qualquer mapping de qualquer YAML do motor, do mesmo
jeito que esta entrou. Por isso ele varre os seis YAML que `motor.carregar()`
e `alocacao.carregar_politica()` fundem na carga do sistema: `custos.yaml`,
`catalogo.yaml`, `politica.yaml`, `perfil.yaml`, `teses.yaml`,
`instituicoes.yaml`. (`estado.yaml` fica de fora de proposito: e dado
financeiro real, privado, P-67.)

`catalogo.yaml` usa merge keys (`<<: *modelo_etf_b3`) para as rotas que
compartilham modelo de custo. O teste NAO expande o merge -- caminha a
arvore como esta escrita, entao um `<<` por mapping e uma chave como
qualquer outra, e so acusa quando o MESMO texto de chave aparece duas vezes
DENTRO DO MESMO mapping.
"""
import os
import sys

import pytest
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

ARQUIVOS = ("custos.yaml", "catalogo.yaml", "politica.yaml", "perfil.yaml",
            "teses.yaml", "instituicoes.yaml")


def _chaves_duplicadas(caminho):
    """Anda a arvore de nos (nao o dict construido) e reporta toda chave que
    aparece mais de uma vez no mesmo MappingNode, com a linha de cada ocorrencia."""
    with open(caminho, encoding="utf-8") as f:
        raiz = yaml.compose(f, Loader=yaml.SafeLoader)
    achados = []

    def anda(no):
        if isinstance(no, yaml.MappingNode):
            vistas = {}
            for chave_no, valor_no in no.value:
                if isinstance(chave_no, yaml.ScalarNode):
                    chave = chave_no.value
                    linha = chave_no.start_mark.line + 1
                    if chave in vistas:
                        achados.append(f"{chave!r}: linhas {vistas[chave]} e {linha}")
                    else:
                        vistas[chave] = linha
                anda(valor_no)
        elif isinstance(no, yaml.SequenceNode):
            for item in no.value:
                anda(item)

    if raiz is not None:
        anda(raiz)
    return achados


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_Y01_nenhuma_chave_repetida_em_nenhum_mapping(nome):
    """FALHA hoje contra custos.yaml (IMAB11, linhas 171 e 253) -- e essa falha
    e o ponto do teste, nao um defeito dele. So deve voltar a passar depois que
    a duplicata for removida do arquivo."""
    caminho = os.path.join(AQUI, nome)
    achados = _chaves_duplicadas(caminho)
    assert not achados, (
        f"{nome}: chave repetida dentro do mesmo mapping. PyYAML fica com a "
        f"ULTIMA em silencio -- a(s) entrada(s) anterior(es) estao mortas desde "
        f"que foram escritas:\n  " + "\n  ".join(achados)
    )


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

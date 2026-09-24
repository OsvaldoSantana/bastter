# -*- coding: utf-8 -*-
"""
test_p71_p72_porta_de_entrada.py -- achados P-71 e P-72, o mesmo defeito em dois
sentidos: 269 testes e NENHUM carregava um estado pelo caminho REAL,
`estado_io.carregar()`. Os testes do G1 montam `Divida(...)` na mao; o
`test_usuario_novo.py` monta o cadastro em memoria. A porta de entrada real do
sistema nao era exercitada por teste nenhum.

O QUE ISTO EXPOS.

`estado_io.validar()` devolvia `dividas`/`objetivos` como LISTA DE DICT, e todo
consumidor real espera dataclass (`g1_divida` le `d.taxa_am`; `necessidade_datada`
le `o.prazo_anos`). Nao estourava em producao porque as duas listas do
`estado.yaml` real estao vazias. E `aporte_mensal <= 0` bloqueava o carregamento
inteiro — contradizendo a U-01: um cliente que ainda nao guarda nada e um ESTADO,
nao um erro de preenchimento.

Escrevendo o teste que prova os dois corrigidos, apareceram MAIS DOIS. `d`
guardava `reserva_empenhada` e `meses_cobertos` — nenhum dos dois e campo de
`Estado` (o primeiro e campo morto ha tempos, ja apontado pela auditoria externa
de 10/09; o segundo duplica uma `@property` que `Estado` ja calcula da reserva
EFETIVA, achado J-01) — e `Estado(**d)` simplesmente nao funcionava, com
`TypeError`. E com `aporte_mensal=0` de verdade fluindo ate o G3,
`custo_entrada_fixo_pct` tratava aporte==0 como custo infinito para toda rota
(inclusive as gratuitas), zerando o universo inteiro; `_conferir_invariantes`
recusava pesos somando 0. Esse ultimo acerto tem teste proprio em
`test_alocacao.py` (`test_custo_entrada_fixo_pct_zero_aporte_nao_inflaciona_rota_gratuita`);
aqui ele so aparece como pre-condicao para o pipeline chegar `ate o fim`. Uma
porta nunca exercitada nao tinha UM defeito -- tinha quatro, empilhados.

POR QUE `tmp_path`, NUNCA `alocacao/estado.yaml`.

O `estado.yaml` real e do Osvaldo — dado financeiro privado (P-67). Este arquivo
escreve um estado SINTETICO num diretorio temporario do pytest a cada execucao e
passa o caminho explicitamente a `estado_io.carregar(path=...)`; o caminho padrao
do modulo nunca e usado aqui.
"""
import os
import sys
import textwrap

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import estado_io
from alocacao import Divida, Estado, Objetivo, alocar, carregar_politica
from motor import carregar as carregar_custos

C, P = carregar_custos(), carregar_politica()

ESTADO_SINTETICO = textwrap.dedent("""\
    meta:
      status: REAL
      preenchido_em: "2026-09-11"
    despesa_mensal: 4500
    estabilidade_renda: media
    aporte_mensal: 0.0
    horizonte_anos: 25
    dependentes: 0
    caixa: 0.0
    reserva_atual: 27000.0
    posicoes: {}
    dividas:
      - {nome: consignado, saldo: 20000, taxa_am: 0.004}
    objetivos:
      - {nome: viagem, valor: 10000, prazo_anos: 5}
    match_empregador: null
    match_verificado: false
    """)
# reserva_atual e despesa_mensal reproduzem o BASE de test_alocacao.py: reserva ja
# completa, para que G1 e G2 nao encerrem o pipeline e ele alcance a fase `universo`
# (onde `necessidade_datada` le `objetivos`). A divida a 0,40% a.m. e a mesma de
# `test_g1_divida_barata_nao_dispara` -- barata o bastante para NAO gerar diretiva.


def test_P71_P72_estado_real_carrega_e_aloca_ate_o_fim(tmp_path):
    """FALHAVA hoje, em camadas — cada uma so aparecia depois que a anterior era
    corrigida: primeiro `estado_io.EstadoInvalido` (P-72, `aporte_mensal=0` blo-
    queava o carregamento); depois `AttributeError: 'dict' object has no attribute
    'taxa_am'` dentro de `g1_divida` (P-71); depois `TypeError: Estado.__init__()
    got an unexpected keyword argument 'reserva_empenhada'` (achado lateral: `d`
    carregava campos que `Estado` nao aceita); depois `ValueError: invariante
    violada: pesos somam 0` (achado lateral no G3, `custo_entrada_fixo_pct`). Uma
    porta de entrada nunca exercitada tinha quatro defeitos empilhados, nao um.
    Depois dos quatro, roda ate o fim e devolve uma alocacao alvo valida."""
    p = tmp_path / "estado_sintetico.yaml"
    p.write_text(ESTADO_SINTETICO, encoding="utf-8")

    d, problemas, avisos = estado_io.carregar(path=str(p))
    assert not problemas, (
        f"aporte_mensal=0 nao pode bloquear o carregamento (P-72): {problemas}")
    assert any("aporte_mensal" in a for a in avisos), (
        "aporte_mensal=0 tem de virar AVISO -- nao pode sumir em silencio")

    assert isinstance(d["dividas"][0], Divida), "P-71: dividas tem de vir como dataclass"
    assert isinstance(d["objetivos"][0], Objetivo), "P-71: objetivos tem de vir como dataclass"
    assert d["dividas"][0].taxa_am == 0.004
    assert d["objetivos"][0].prazo_anos == 5

    estado = Estado(**d)                                  # a conversao TEM de bastar
    r = alocar(estado, C, P, teses={}, carregos={})        # nao pode lancar

    assert "alvo" in r, (
        "com reserva completa e divida barata, o pipeline tem de chegar na "
        "alocacao alvo, nao parar numa diretiva")
    assert abs(sum(r["alvo"]["pesos"].values()) - 1.0) < 1e-6


def test_P72_aporte_mensal_negativo_continua_bloqueando(tmp_path):
    """O espelho do teste acima: SO o zero virou aviso. Negativo nao existe e
    continua impedindo o carregamento -- sem isto, o teste de cima nao provaria
    que a mudanca foi seletiva, so que ficou mais permissiva."""
    p = tmp_path / "estado_negativo.yaml"
    p.write_text(ESTADO_SINTETICO.replace("aporte_mensal: 0.0", "aporte_mensal: -100"),
                encoding="utf-8")
    d, problemas, avisos = estado_io.carregar(path=str(p), exigir_real=False)
    assert any("aporte_mensal" in x and "-100" in x for x in problemas), (
        f"aporte_mensal negativo tem de continuar bloqueando: {problemas}")
    # B-14: a linha de cima prova que o problema e REGISTRADO, com `exigir_real=False`.
    # "Bloqueando" e o que a porta faz no modo padrao -- levantar. Um `carregar()` que
    # deixasse de honrar `exigir_real` passaria pela linha de cima.
    with pytest.raises(estado_io.EstadoInvalido, match="aporte_mensal = -100"):
        estado_io.carregar(path=str(p), exigir_real=True)


# ── segunda metade (11/09/2026): a porta aceitava o que o validador existe para
# recusar. A conversao para dataclass do 4f54f31 foi feita SEM passar os numeros por
# `_num()` -- e o modulo existe exatamente para pegar virgula decimal, campo em branco
# e chave errada, as tres falhas silenciosas do preenchimento a mao.
BASE_MINIMA = textwrap.dedent("""\
    meta: {status: REAL, preenchido_em: 2026-09-11}
    despesa_mensal: 4500
    estabilidade_renda: media
    aporte_mensal: 500
    horizonte_anos: 25
    caixa: 0.0
    reserva_atual: 27000.0
    """)


def _carregar(tmp_path, extra):
    p = tmp_path / "estado.yaml"
    p.write_text(BASE_MINIMA + extra, encoding="utf-8")
    return estado_io.carregar(path=str(p), exigir_real=False)


def test_P71_virgula_decimal_em_divida_vira_problema_e_nao_texto(tmp_path):
    """`taxa_am: "14,5"` entrava como a STRING '14,5', sem problema nenhum, e
    estourava no G1 (`'14,5' > float`). Agora e o mesmo tratamento dos campos do
    topo: problema que bloqueia, e o numero interpretado para quem pedir o relatorio."""
    d, problemas, _ = _carregar(
        tmp_path, 'dividas:\n  - {nome: cartao, saldo: 3000, taxa_am: "14,5"}\n')
    assert any("dividas[0].taxa_am" in p for p in problemas), problemas
    assert d["dividas"][0].taxa_am == 14.5


def test_P71_divida_incompleta_vira_problema_e_nao_excecao(tmp_path):
    """Antes: `TypeError: missing 1 required positional argument`. O contrato do
    modulo e devolver TODOS os problemas de uma vez, nunca o primeiro como excecao."""
    d, problemas, _ = _carregar(tmp_path, "dividas:\n  - {nome: cartao, saldo: 3000}\n")
    assert any("dividas[0].taxa_am" in p for p in problemas), problemas
    assert d["dividas"] == [], "registro incompleto nao vira Divida com buraco"


def test_P71_chave_desconhecida_em_divida_nao_some_em_silencio(tmp_path):
    """`juros_am` no lugar de `taxa_am` e o erro de digitacao mais provavel. Chave
    que o dataclass nao tem seria descartada -- e a P2 do outro lado da porta."""
    _, problemas, _ = _carregar(
        tmp_path, "dividas:\n  - {nome: cartao, saldo: 3000, taxa_am: 0.14, juros_am: 0.14}\n")
    assert any("juros_am" in p for p in problemas), problemas


def test_P71_match_declarado_chega_ao_estado(tmp_path):
    """`estado.exemplo.yaml` pede `match_empregador` e `match_verificado`, e
    `validar()` nunca os lia. Com o G0 desligado era inerte; ligado, quem ja
    respondeu `match_verificado: true` receberia a pergunta ao RH de novo."""
    from alocacao import MatchEmpregador
    d, problemas, _ = _carregar(tmp_path, (
        "match_verificado: true\n"
        "match_empregador: {taxa: 0.5, teto_pct_salario: 0.05, salario_bruto_mensal: 12000}\n"))
    assert not problemas, problemas
    e = Estado(**d)
    assert e.match_verificado is True
    assert isinstance(e.match_empregador, MatchEmpregador) and e.match_empregador.taxa == 0.5


def test_P71_match_verificado_tem_de_ser_booleano(tmp_path):
    """`match_verificado: sim` e texto, e texto nao-vazio e verdadeiro em Python.
    Aceitar seria decidir pelo usuario o que ele quis dizer."""
    _, problemas, _ = _carregar(tmp_path, "match_verificado: sim\n")
    assert any("match_verificado" in p for p in problemas), problemas


def test_reserva_empenhada_discordante_vira_problema(tmp_path):
    """Auditoria de 10/09, 'campos mortos': `reserva_empenhada` era lida e descartada.
    Agora confere com `reserva_atual - reserva_disponivel` (27000 - 200 = 26800)."""
    _, problemas, _ = _carregar(tmp_path, "reserva_disponivel: 200.0\nreserva_empenhada: 500.0\n")
    assert any("reserva_empenhada diz" in p for p in problemas), problemas


def test_reserva_empenhada_coerente_nao_acusa_nada(tmp_path):
    """O espelho: sem ele, o teste de cima passaria com uma conferencia que acusa sempre."""
    _, problemas, _ = _carregar(tmp_path, "reserva_disponivel: 26500.0\nreserva_empenhada: 500.0\n")
    assert not any("reserva_empenhada diz" in p for p in problemas), problemas

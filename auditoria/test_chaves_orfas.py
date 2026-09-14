# -*- coding: utf-8 -*-
"""
test_chaves_orfas.py -- o achado E-04 virando portao.

O `impacto.py` responde "quem le esta chave?" e exige que voce ja desconfie da chave.
Foi por isso que o E-03 sobreviveu: ninguem pensou em perguntar por
`portoes.G3_atrito.ativo`.

Este teste faz a pergunta que nao precisa de suspeita, e a faz TODA vez que a suite
roda -- que e a P7 aplicada a auditoria: rotina que depende de alguem lembrar nao e
rotina.

COMO ELE FALHA, e o desenho importa: ele NAO exige zero orfas. Exige que a lista nao
CRESCA sem alguem dizer por que. Orfa nova = alguem escreveu um parametro no YAML
esperando que mudasse alguma coisa, e nao mudou.

Para fechar uma orfa ha exatamente dois caminhos honestos:
  1. o codigo passa a ler a chave -- era promessa de verdade; ou
  2. a chave sai do YAML -- nao era.
Mover para a linha de base e o terceiro caminho, e ele exige escrever POR QUE ali.
"""

import os
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SCRIPT = os.path.join(AQUI, "chaves_orfas.py")
PACOTE = os.path.join(RAIZ, "alocacao")

# ── A LINHA DE BASE. E DADO, nao codigo (P2): cada linha tem de ter um porque.
# Medida em 12/09/2026 sobre o instantaneo de 06/09. RECONFERIR na maquina real.
CONHECIDAS = {
    # E-06 -- o pre-registro declara guardas que ninguem executa. ABERTO.
    "estrategias_pre_registradas.greenblatt_v1.verificar_monotonicidade",
    "estrategias_pre_registradas.hml_puro_v1.variantes_permitidas",
    # resultado ja registrado do backtest: e SAIDA gravada, nao parametro de entrada
    "estrategias_pre_registradas.hml_puro_v1.ordem_de_execucao",
    "estrategias_pre_registradas.hml_puro_v1.resultado.alfa_bruto_aa",
    "estrategias_pre_registradas.hml_puro_v1.resultado.alfa_bruto_am",
    "estrategias_pre_registradas.hml_puro_v1.resultado.custo_e_imposto_matam",
    # E-05 RETIRADO em 12/09 -- era falso positivo meu, e o maior desta auditoria.
    # `liquidez_pior_caso_dias` E lido: o catalogo.yaml o puxa por
    # `{de_campo: "cofrinho.picpay_garantia_de_limite.liquidez_pior_caso_dias"}` para o
    # `liquidez_dias` da rota, e o G6 usa isso para tirar a funcao da rota lenta. O
    # portao existe e funciona. So `liquidez_media_dias` continua sem dono -- e a
    # escolha de usar o PIOR caso, e nao a media, e a conservadora.
    "cofrinho.picpay_garantia_de_limite.liquidez_media_dias",
    # tributacao declarada e nao ligada. A primeira liga-se a P-77. ABERTAS.
    "tributacao.fii_isencao_rendimento.cotistas_minimos",
    "tributacao.ir_etf_rf_faixas.valor.prazo_medio_ate",
    "tributacao.irrf_dedo_duro.e_custo_liquido",
    # divergencia de fonte registrada de proposito: e procedencia, nao parametro
    "b3.vista_total_pct.divergencia.valor_alternativo",
    # pontuacao de corretora -- entram quando o ranking for religado.
    # `corretora.cobertura_e_penalidade` saiu desta lista em 12/09: o pai `corretora`
    # e varrido por variavel, entao o filtro de `pais_varridos` ja o alcanca.
    "corretora.multiplicador_de_confirmacao.N",
    "instituicoes.itau.custos.corretagem_fii",
    "instituicoes.itau.custos.exercicio_opcao_pct",
    "instituicoes.itau.facilidade.home_broker_web",
    # numeros historicos do M-01, guardados para comparacao. Nao sao entrada.
    "fase_A_recalculada.antes_dizia.premissa_de_reserva",
    "fase_A_recalculada.reserva_inicial",
    # P7: `revisao.mes` e a data da revisao periodica. Vira leitura quando a rotina
    # deixar de depender de alguem lembrar -- ver secao 11.6 do CLAUDE.md.
    "revisao.mes",
}


def _orfas():
    yamls = [os.path.join(PACOTE, y) for y in
             ("politica.yaml", "custos.yaml", "catalogo.yaml", "instituicoes.yaml")]
    r = subprocess.run([sys.executable, SCRIPT, PACOTE] + yamls,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return {l.strip().split(" =")[0].strip()
            for l in r.stdout.splitlines() if l.startswith("   ") and " = " in l}


@pytest.mark.skipif(not os.path.isdir(PACOTE), reason="pacote alocacao nao encontrado")
def test_nenhuma_chave_orfa_NOVA():
    """Uma chave numerica ou booleana que ninguem le e uma promessa sem dono -- e foi
    exatamente essa a forma do E-03: `politica.yaml` declarava `ativo` para os nove
    portoes e dois nao liam. Os dois estavam `true`, entao arquivo e codigo
    concordavam POR ACIDENTE."""
    novas = _orfas() - CONHECIDAS
    assert not novas, (
        "chave(s) declarada(s) que codigo nenhum le:\n  - " + "\n  - ".join(sorted(novas))
        + "\n\nOu o codigo passa a ler, ou a chave sai do YAML. Pos-la na linha de base"
          " exige escrever o porque ao lado dela.")


@pytest.mark.skipif(not os.path.isdir(PACOTE), reason="pacote alocacao nao encontrado")
def test_a_linha_de_base_nao_guarda_chave_ja_resolvida():
    """O inverso, e ele evita que a linha de base vire deposito: chave que o codigo
    JA le nao pode continuar listada como orfa conhecida -- se continuar, a proxima
    pessoa acredita que ainda ha pendencia onde nao ha."""
    resolvidas = CONHECIDAS - _orfas()
    assert not resolvidas, (
        "chave(s) na linha de base que o codigo agora LE -- tire(m) da lista:\n  - "
        + "\n  - ".join(sorted(resolvidas)))


# XFAIL ESTRITO, e a escolha e deliberada. O defeito E-03 existe HOJE: este teste
# reprova de verdade. Deixar a suite vermelha bloquearia todo o resto da segunda, e
# suite cronicamente vermelha e suite que ninguem le -- foi assim que o A-06 passou.
# `strict=True` faz o contrario do que parece: enquanto o defeito existir a suite fica
# VERDE com o xfail registrado; no instante em que alguem consertar o G3/G4, o teste
# passa, o strict transforma isso em FALHA, e a pessoa e obrigada a vir aqui tirar o
# marcador. Ou seja: o defeito fica escrito na suite e o conserto nao pode passar
# despercebido. Quando cair, apague estas seis linhas e o decorador.
@pytest.mark.xfail(strict=True, reason="E-03 aberto: g3_atrito e g4_dominancia nao "
                                       "leem `ativo`. Tirar o marcador ao corrigir.")
@pytest.mark.skipif(not os.path.isdir(PACOTE), reason="pacote alocacao nao encontrado")
def test_E03_todo_portao_declarado_le_o_proprio_interruptor():
    """O E-03 direto, e sem depender do script: os nove portoes declaram `ativo` no
    politica.yaml. Se um deles nao le o campo, desligar no arquivo nao desliga nada --
    e a analise de sensibilidade devolve 'esse portao nao muda nada', que e falso."""
    import ast

    import yaml

    P = yaml.safe_load(open(os.path.join(PACOTE, "politica.yaml"), encoding="utf-8"))
    fonte = open(os.path.join(PACOTE, "alocacao.py"), encoding="utf-8").read()
    arv = ast.parse(fonte)
    funcs = {n.name: ast.unparse(n) for n in ast.walk(arv)
             if isinstance(n, ast.FunctionDef)}

    mudos = []
    for nome_yaml, cfg in P["portoes"].items():
        if not isinstance(cfg, dict) or "ativo" not in cfg:
            continue
        # G3_atrito -> g3_atrito
        alvo = nome_yaml.lower()
        corpo = funcs.get(alvo)
        if corpo is None:                       # portao sem funcao de mesmo nome
            continue
        if "'ativo'" not in corpo and '"ativo"' not in corpo:
            mudos.append(nome_yaml)

    assert not mudos, (
        "portao(oes) que declaram `ativo` no politica.yaml e NAO leem o campo: "
        + ", ".join(mudos) + ". Desligar no arquivo nao desliga o portao.")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

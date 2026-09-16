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

import fnmatch
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
    # `corretagem_fii` e `exercicio_opcao_pct` SAIRAM em 16/09: o codigo passa a
    # le-las. Ficaram aqui sem dono de 12 a 16/09 -- o inverso do E-03, e a razao de o
    # segundo teste deste arquivo existir: linha de base que nao encolhe vira deposito.
    "instituicoes.itau.facilidade.home_broker_web",
    # `instituicoes.itau.custos.corretagem_etf_pct` e
    # `corretora.promocional.e_uma_decisao_nao_uma_omissao` SAIRAM em 16/09: a
    # primeira passou a ser lida pela dimensao `corretagem` (P-84); a segunda pelo
    # `regras()`, ao lado da chave nova de `custo_por_operacao`.
    # numeros historicos do M-01, guardados para comparacao. Nao sao entrada.
    "fase_A_recalculada.antes_dizia.premissa_de_reserva",
    "fase_A_recalculada.reserva_inicial",
    # P7: `revisao.mes` e a data da revisao periodica. Vira leitura quando a rotina
    # deixar de depender de alguem lembrar -- ver secao 11.6 do CLAUDE.md.
    "revisao.mes",

    # ── RECONFERIDA NA MAQUINA REAL EM 16/09/2026 ────────────────────────────────
    # As dez abaixo entraram de uma vez, e nao porque alguem escreveu chave nova: o
    # `chaves_orfas.py` passou a separar "LIDA SO POR TESTE" e a conta-la como orfa.
    # A mudanca e deliberada e vem da P-77 -- campo que so o teste toca e campo que o
    # motor nao usa, e o teste prova o esquema enquanto ninguem prova o comportamento.
    #
    # E elas nao sao todas da mesma especie, e a diferenca decide o que fazer com cada
    # uma. O E-03 era PARAMETRO: `ativo: true` prometia comportamento e nao entregava.
    # As cinco booleanas abaixo sao DECLARACAO DE DECISAO -- registram um julgamento
    # tomado, e o teste as le para fixar o registro. Um parametro orfao e defeito; uma
    # decisao registrada e procedencia. Que o instrumento nao saiba separar as duas e
    # limitacao DELE, e esta registrada como pendencia de desenho.
    "bloco_C_solvencia.natureza_dos_cortes.nenhum_corte_tem_ancora_legal",
    "corretora.promocional.e_uma_decisao_nao_uma_omissao",
    "fase_A_recalculada.atraso_em_meses",
    "limitacoes_declaradas.reserva_e_divida_tratadas_como_independentes.aplica_se_ao_caso_do_usuario",
    "regime_instituicao_financeira.bloco_substituto.B01_indice_de_basileia.tem_piso_legal",
    # P-78, dado de pesquisa coletado e nunca pontuado -- decisao por campo, do Osvaldo.
    # `mesa_minimo` e o unico que ainda separa: `corretagem_fii` (11/24 declaram, todos
    # 0,0) e `exercicio_opcao_pct` (4/24, todos 0,005) ja sairam por leitura do codigo.
    "instituicoes.inter.custos.mesa_minimo",
    "instituicoes.itau.reclamacoes.bc_clientes",
    "instituicoes.itau.reclamacoes.bc_procedentes",
    # F-03/P-05: porte do fundo, escrito para julgar liquidez da rota de ETF de renda
    # fixa. Entra quando a rota entrar -- hoje ela esta barrada por falta do regulamento.
    "etf.IMAB11.pl_medio_3a",
}


# ── ESPECIES, e elas nasceram de um defeito da propria ferramenta (16/09/2026).
#
# Ate hoje o `chaves_orfas.py` deduplicava por NOME DE FOLHA: a segunda ocorrencia de
# um nome no mesmo arquivo sumia do relatorio -- nem orfa, nem lida, invisivel. Eram
# **42 de 67**. Corrigido para dedupe por caminho, e o que apareceu foram zero especies
# novas: `bc_procedentes` das outras oito casas, `variantes_permitidas` das outras sete
# estrategias, e assim por diante. **A linha de base declarava UMA instancia e cobria N
# em silencio.**
#
# Listar as 42 uma a uma seria copiar o mesmo porque 42 vezes. O motivo mora na
# ESPECIE, e e la que ele fica escrito. O glob tem precedente na casa
# (`test_alocacao.py` usa `corretora.*.e_uma_decisao_nao_uma_omissao`).
ESPECIES = (
    # E-06 -- resultado JA GRAVADO do pre-registro e limite anti-p-hacking declarado.
    # Sao SAIDA registrada e regra de processo, nao parametro de entrada do motor.
    ("estrategias_pre_registradas.*.ordem_de_execucao", "E-06"),
    ("estrategias_pre_registradas.*.variantes_permitidas", "E-06"),
    ("estrategias_pre_registradas.*.resultado.*", "E-06"),
    # P-78 -- procedencia do indice do BC: `test_corretoras.py` RECALCULA o indice a
    # partir das partes, entao elas sao o insumo que prova o numero derivado.
    ("instituicoes.*.reclamacoes.bc_clientes", "P-78"),
    ("instituicoes.*.reclamacoes.bc_procedentes", "P-78"),
    # P-84 -- exibidos e nunca pontuados, por decisao medida em 16/09 (constantes entre
    # quem declara, ou cobertura baixa demais para separar ausencia de produto de
    # ausencia de pesquisa).
    ("instituicoes.*.custos.mesa_minimo", "P-84"),
    # P-78 -- dimensao `facilidade` declarada e nao pontuada; `regras()` RECUSA liga-la.
    ("instituicoes.*.facilidade.home_broker_web", "P-78"),
    # `exporta_csv` NAO entra: nenhuma casa o declara no YAML hoje, e a guarda nova
    # de "especie que nao casa com nada" me pegou tentando por o glob por simetria.
    # P-81 -- declaracao de DECISAO, nao parametro: registra um julgamento tomado, e o
    # teste a le para fixar o registro. Procedencia, nao divida.
    ("*.tem_piso_legal", "P-81"),
    ("corretora.*.e_uma_decisao_nao_uma_omissao", "P-81"),
    # M-01 -- numeros historicos guardados para comparacao. Nao sao entrada.
    ("fase_A_recalculada.*.premissa_de_reserva", "M-01"),
)


def _declarada(chave):
    return chave in CONHECIDAS or any(fnmatch.fnmatch(chave, g) for g, _ in ESPECIES)


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
    novas = {c for c in _orfas() if not _declarada(c)}
    assert not novas, (
        "chave(s) declarada(s) que codigo nenhum le:\n  - " + "\n  - ".join(sorted(novas))
        + "\n\nOu o codigo passa a ler, ou a chave sai do YAML. Pos-la na linha de base"
          " exige escrever o porque ao lado dela.")


@pytest.mark.skipif(not os.path.isdir(PACOTE), reason="pacote alocacao nao encontrado")
def test_a_linha_de_base_nao_guarda_chave_ja_resolvida():
    """O inverso, e ele evita que a linha de base vire deposito: chave que o codigo
    JA le nao pode continuar listada como orfa conhecida -- se continuar, a proxima
    pessoa acredita que ainda ha pendencia onde nao ha."""
    hoje = _orfas()
    resolvidas = CONHECIDAS - hoje
    orfas_sem_especie = {c for g, _ in ESPECIES for c in hoje if fnmatch.fnmatch(c, g)}
    mortas = [g for g, _ in ESPECIES
              if not any(fnmatch.fnmatch(c, g) for c in hoje)]
    assert not mortas, (
        "especie declarada que nao casa com orfa nenhuma -- apague o glob:\n  - "
        + "\n  - ".join(mortas))
    assert orfas_sem_especie or not ESPECIES
    assert not resolvidas, (
        "chave(s) na linha de base que o codigo agora LE -- tire(m) da lista:\n  - "
        + "\n  - ".join(sorted(resolvidas)))


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


def test_a_ferramenta_NAO_deduplica_por_nome_de_folha(tmp_path):
    """A guarda da guarda, 16/09/2026.

    O `chaves_orfas.py` deduplicava por NOME DE FOLHA: a segunda ocorrencia de um nome
    no mesmo arquivo sumia do relatorio -- nem orfa, nem lida, **invisivel**. Eram 42 de
    67 chaves. `bc_procedentes` aparecia para o Itau e calava para as outras oito casas.

    **Peguei sem procurar**, e e isso que torna o defeito caro: batizei uma chave nova
    com o mesmo nome de folha de uma existente, e a EXISTENTE desapareceu da auditoria.
    Uma guarda que emudece porque alguem escolheu um nome e pior que guarda nenhuma --
    e o sintoma e a linha de base ENCOLHER, que e a direcao que parece progresso."""
    y = tmp_path / "x.yaml"
    y.write_text("um:\n  nunca_lida_por_ninguem: 1\ndois:\n  nunca_lida_por_ninguem: 2\n",
                 encoding="utf-8")
    r = subprocess.run([sys.executable, SCRIPT, str(tmp_path), str(y)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    achadas = [ln for ln in r.stdout.splitlines() if "nunca_lida_por_ninguem" in ln]
    assert len(achadas) == 2, (
        "o mesmo nome de folha em dois ramos: a ferramenta reportou %d de 2. Ela voltou "
        "a deduplicar por NOME em vez de por CAMINHO, e a segunda chave ficou "
        "invisivel.\n%s" % (len(achadas), r.stdout[-800:]))
    assert "um.nunca_lida_por_ninguem" in r.stdout
    assert "dois.nunca_lida_por_ninguem" in r.stdout

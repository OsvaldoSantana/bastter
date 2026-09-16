# -*- coding: utf-8 -*-
"""Acrescenta `tributacao.ir_jcp_fonte` ao custos.yaml. Idempotente."""
import io, os, sys
import yaml

p = sys.argv[1] if len(sys.argv) > 1 else "custos.yaml"
s = io.open(p, encoding="utf-8").read()
MARCA = "ir_jcp_fonte:"
if MARCA in s:
    sys.exit("ja aplicado: ir_jcp_fonte ja existe em %s" % p)

BLOCO = '''
  # ── JCP: a aliquota e FUNCAO DO TEMPO, e o acervo comeca em 2010 ────────────
  # Lida norma por norma no Planalto em 13/09/2026. Transcricoes em
  # docs/fontes/lei-9249-1995-jcp-planalto.md.
  #
  # NAO e escalar. Aplicar um unico numero a serie inteira erra TODOS os registros
  # de um dos lados, e o erro e invisivel porque qualquer um dos numeros e plausivel.
  # Ha uma janela de SESSENTA E OITO DIAS em 2016 em que a aliquota foi 18%.
  ir_jcp_fonte:
    status: COMPLETO
    expira: null          # lei nao vence no aniversario; vence quando outra a altera
    revisar_se: "publicacao de norma que altere o art. 9o par. 2o da Lei 9.249/1995"
    acesso: 2026-09-13
    natureza_pf: TRIBUTACAO_DEFINITIVA   # art. 9o par. 3o, II -- sem ajuste na declaracao
    trecho_conferido: true
    valor:
      - de: 1996-01-01
        ate: 2015-12-31
        aliquota: 0.15
        fonte: "Lei 9.249/1995 art. 9o par. 2o, redacao ORIGINAL"
      - de: 2016-01-01
        ate: 2016-03-08
        aliquota: 0.18
        fonte: >-
          MP 694/2015 art. 1o (publicada 30/09/2015), efeitos desde 01/01/2016 pelo
          art. 4o, I. Prazo de vigencia encerrado em 08/03/2016 -- Ato Declaratorio
          do Presidente da Mesa do Congresso Nacional no 5, de 09/03/2016.
        nota: >-
          Janela de 68 dias. O IR retido nela PERMANECE devido: a CF art. 62 par. 11
          manda que as relacoes constituidas durante a vigencia da MP continuem por
          ela regidas se o Congresso nao editar decreto legislativo em 60 dias, e
          nao editou. Caducar nao devolve imposto pago.
      - de: 2016-03-09
        ate: 2025-12-31
        aliquota: 0.15
        fonte: "Lei 9.249/1995 art. 9o par. 2o -- redacao original restabelecida"
      - de: 2026-01-01
        ate: null
        aliquota: 0.175
        fonte: "LC 224/2025 art. 8o; vigencia pelo art. 14, III"
        nota: >-
          CORRECAO DE 13/09/2026. Eu tinha registrado 01/04/2026, lendo o art. 14, I,
          "b" ("primeiro dia do quarto mes subsequente"). Aquela alinea cobre os arts.
          7o e 9o -- NAO o art. 8o. O art. 8o cai no inciso III, "a partir de 1o de
          janeiro de 2026". Fonte primaria ganha, mas so depois de ler QUAL item ela
          cobre.
      # MP 1.303/2025 NAO entra: foi retirada de pauta e caducou em outubro/2025,
      # antes de produzir efeito sobre o JCP, e o Planalto nao a lista entre as
      # normas que deram redacao ao par. 2o.
'''

# insere logo apos a abertura da secao `tributacao:`
i = s.index("\ntributacao:")
j = s.index("\n", i+1)
s2 = s[:j] + "\n" + BLOCO.rstrip() + "\n" + s[j:]
d = yaml.safe_load(s2)
v = d["tributacao"]["ir_jcp_fonte"]["valor"]
assert len(v) == 4 and v[1]["aliquota"] == 0.18, "bloco nao carregou como esperado"
io.open(p, "w", encoding="utf-8").write(s2)
print("JCP aplicado em %s -- 4 vigencias" % os.path.abspath(p))

# -*- coding: utf-8 -*-
"""F-03 / P-05: a taxa do IMAB11 entra no custos.yaml. Idempotente."""
import io, os, sys
import yaml

MARCA = "lamina do gestor, 31/08/2026"
p = sys.argv[1] if len(sys.argv) > 1 else "custos.yaml"
s = io.open(p, encoding="utf-8").read()
if MARCA in s:
    sys.exit("ja aplicado: a marca da lamina do IMAB11 ja esta em %s" % p)

def bloco(s, i):
    """Devolve (inicio, fim) do bloco que comeca em `i` -- ate a proxima chave de 2
    espacos de indentacao que nao seja comentario."""
    fim = s.index("\n", i) + 1
    for l in s[fim:].split("\n"):
        if l and not l.startswith("    ") and not l.lstrip().startswith("#"):
            break
        fim += len(l) + 1
    return i, fim


# ACHADO E-09: ha DUAS entradas `IMAB11:` sob `etf:`. A de cima (05/09) traz
# `valor: 0.0025, status: PARCIAL` com a pagina do gestor; a de baixo traz
# `valor: null, NAO_CONFIRMADO` -- e o PyYAML fica com a ULTIMA, em silencio. O
# trabalho de 05/09 estava no arquivo e nao tinha efeito nenhum.
#
# Este patch funde as duas numa so. Se um dia houver so uma, ele ainda funciona.
ocorr = []
k = 0
while True:
    try:
        k = s.index("\n  IMAB11:", k) + 1
    except ValueError:
        break
    ocorr.append(k)
assert ocorr, "nenhuma entrada IMAB11 encontrada -- PARE"
assert len(ocorr) <= 2, "mais de duas entradas IMAB11 (%d) -- PARE e olhe o arquivo" % len(ocorr)
print("entradas IMAB11 encontradas: %d (linhas %s)"
      % (len(ocorr), [s[:o].count("\n") + 1 for o in ocorr]))
i, fim = bloco(s, ocorr[0])
NOVO = '''  IMAB11:
    # F-03 / P-05 FECHADAS em 13/09/2026. A taxa veio da LAMINA DO GESTOR (Itau Asset),
    # que ele baixou e enviou -- nao de agregador, nao de citacao interna.
    #
    # E ela e a TAXA TOTAL, nao a de administracao. A P-05 dizia que a pendencia estava
    # mal formulada, e estava: nas laminas brasileiras "taxa de administracao" e UM
    # componente. Aqui sao tres, e a de administracao e a MENOR delas:
    #
    #     administracao  0,04%      custodia  0,03%      gestao  0,18%
    #     distribuicao   nao ha     performance  nao ha
    #     -------------------------------------------------------------
    #     TOTAL          0,25% a.a.   <- e "taxa cobrada" == "taxa maxima"
    #
    # Comparar rotas por `taxa_adm` teria subestimado esta em SEIS VEZES.
    #
    # `taxa cobrada` == `taxa maxima` nas tres linhas: nao ha folga entre o que o fundo
    # cobra e o teto que ele pode cobrar. Era essa a duvida que mandava esperar o
    # regulamento -- e a lamina a responde.
    status: COMPLETO
    valor: 0.0025
    fonte: "Lamina It Now ID ETF IMA-B (IMAB11), Itau Asset — lamina do gestor, 31/08/2026"
    acesso: 2026-09-13
    trecho_conferido: true
    expira: 2027-08-31       # a lamina e mensal; esta e a de 31/08/2026
    revisar_se: "nova lamina mensal, ou alteracao de regulamento que mexa no teto"
    composicao:
      administracao: 0.0004
      custodia: 0.0003
      gestao: 0.0018
      distribuicao: null
      performance: null
    cnpj: "31.024.153/0001-00"
    inicio_do_fundo: 2019-05-17
    pl_medio_3a: 2468371314.24
    classificacao_tributaria: "Longo prazo sem compromisso"
    liquidacao: "aplicacao D+0, resgate D+0, credito D+1"
    nota: >-
      Lei 13.043/2014 art. 2o e IN RFB 1.585/2015 art. 28 dao a mesma regra de aliquota;
      Lei 14.754/2023 art. 22 exclui expressamente o ETF de renda fixa da definicao
      geral de ETF, entao ele segue a regra propria. A lamina afirma "15% de IR": e o
      piso da tabela regressiva de longo prazo, e quem decide a aliquota aqui e
      `tributacao.ir_rf_faixas`, nao a peca de marketing.
'''
s2 = s[:i] + NOVO + s[fim:]
# remove a segunda entrada, se existir (os offsets mudaram, entao busca de novo)
segunda = s2.find("\n  IMAB11:", s2.index(NOVO[:20]) + len(NOVO))
if segunda != -1:
    a, b = bloco(s2, segunda + 1)
    s2 = s2[:a] + s2[b:]
    print("segunda entrada IMAB11 REMOVIDA -- era ela que o PyYAML estava usando")
d = yaml.safe_load(s2)
no = d["etf"]["IMAB11"]
assert s2.count("\n  IMAB11:") == 1, "sobrou mais de uma entrada IMAB11 -- ABORTADO"
assert no["status"] == "COMPLETO" and no["valor"] == 0.0025
assert abs(sum(v for v in no["composicao"].values() if v) - 0.0025) < 1e-12, \
    "os componentes nao somam a taxa total -- ABORTADO"
io.open(p, "w", encoding="utf-8").write(s2)
print("IMAB11 aplicado: 0,25%% a.a. COMPLETO (0,04 + 0,03 + 0,18)")

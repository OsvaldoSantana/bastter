#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refinar.py -- bronze -> silver dos eventos societarios da B3.

O QUE ESTE MODULO FAZ, E O QUE ELE RECUSA FAZER.

Faz: le o acervo bruto de `data/bronze/b3/` (JSON como a B3 devolveu, imutavel),
tipa os campos, calcula o que da para calcular, e grava UMA tabela CSV por captura.

Recusa: inventar numero. Toda linha carrega `fator_status`, e quando o fator nao pode
ser calculado o campo vem VAZIO com o motivo escrito ao lado -- nunca zero, nunca um
palpite. E o F-02 aplicado a uma tabela: ausencia de insumo produz ausencia declarada.

POR QUE CSV E NAO PARQUET, e a decisao e reversivel.
O desenho (`DESENHO-PIPELINE.md`) previa Parquet. Para OITO MIL LINHAS, CSV ganha:
  - nao acrescenta dependencia -- pyarrow mudaria a impressao do ambiente (P-15), e
    este modulo, como o coletar_b3, NAO produz numero de backtest: so transforma bytes;
  - e DIFFAVEL no git, o que faz o instantaneo dourado do protocolo de mudanca (passo 3)
    custar um `git diff` em vez de um script de comparacao.
Quando o COTAHIST entrar, com milhoes de linhas, a conta inverte e o Parquet passa a
valer. A camada silver e ARTEFATO RECONSTRUIVEL: trocar o formato e reescrever o writer
e rodar de novo. Registrado para que a proxima sessao nao ache que foi esquecimento.

AS DUAS ESTEIRAS DO BRONZE SAO COMPLEMENTARES, NAO REDUNDANTES:

  suplemento (eventos/<EMISSORA>.json)
      cashDividends    janela recente, SEM PRECO -> fator nao calculavel
      stockDividends   desdobramento/grupamento/bonificacao -- a UNICA fonte deles
      subscriptions    subscricao
  paginado (proventos/<EMISSORA>/pagina-NNN.json)
      results          historico longo COM `closingPricePriorExDate` -> fator calculavel

Na janela em que as duas se sobrepoem elas PODEM DISCORDAR. O campo `origem` existe para
que a discordancia seja consultavel. Quando aparecer, e achado, nao empate.

DUAS RAIZES, PORQUE SAO DOIS ACERVOS (23/09/2026, P-114)
Este modulo le de dois lugares que nao sao o mesmo lugar:

    --raiz      `data/bronze/b3`           eventos/ e proventos/ -- o que a B3 devolveu
    --cotahist  `data/bronze/b3/cotahist`  os 41 anos de preco, de onde sai o CALENDARIO

Ate 21/09 havia UM parametro fazendo as duas coisas, e por isso o calendario so
alcancava 2023: `calendario.arquivos()` nao e recursivo, e a unica coisa com cara de
COTAHIST em `data/bronze/b3` era o `COTAHIST_A2023.ZIP` avulso de 04/09 (P-97, movido
para fora do acervo na mesma decisao). O relatorio dizia *"cada ano de COTAHIST que
entrar em `data/bronze/b3/` amplia a cobertura sozinho"* -- e isso era **falso para o
disco como ele estava**: os anos entravam em `cotahist/` e o modulo nao os via.

Um parametro que serve a dois acervos nao e economia: e a garantia de que mover um
deles quebra o outro em silencio. Agora sao dois, e cada um aponta para a pasta que
tem o seu dado.

USO
    python refinar.py                      # a captura mais recente
    python refinar.py --dia 2026-09-11
    python refinar.py --raiz data/bronze/b3 --cotahist data/bronze/b3/cotahist

So biblioteca padrao. Fora da impressao do ambiente, de proposito.
"""

import argparse, csv, datetime as dt, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendario                                                   # noqa: E402
from decimal import Decimal, InvalidOperation

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

try:
    from coletar_b3 import desembrulhar, sha256          # noqa: E402
except ImportError as e:                                  # pragma: no cover
    raise SystemExit(
        "refinar.py depende de coletar_b3.desembrulhar e coletar_b3.sha256, e nao "
        "conseguiu importar (%s). As duas normalizacoes tem de ser A MESMA funcao: "
        "duas implementacoes da mesma regra concordam por acidente ate o dia em que "
        "nao concordam (achado N-01)." % e)

RAIZ_PADRAO = os.path.join("data", "bronze", "b3")
# P-114: o calendario NAO mora na mesma pasta que os eventos, e apontar os dois para o
# mesmo lugar e o que deixou a cobertura em um ano so. Ver o cabecalho.
COTAHIST_PADRAO = os.path.join("data", "bronze", "b3", "cotahist")
SAIDA_PADRAO = os.path.join("data", "silver")

COLUNAS = (
    "origem", "cod", "code_cvm", "trading_name", "isin", "type_stock",
    "tipo", "ultimo_dia_com_direito", "data_ex", "data_ex_status",
    "data_aprovacao", "data_pagamento",
    "valor", "ratio", "preco_vespera", "fator", "fator_status",
    "dt_captura", "arquivo_origem", "sha256_origem",
)

# fator_status -- a coluna que impede a tabela de mentir por omissao
CALCULADO      = "CALCULADO"
SEM_PRECO      = "SEM_PRECO"        # provento do suplemento: nao ha preco de vespera
FACTOR_FORA_DA_REGRA = "FACTOR_FORA_DA_REGRA"   # rotulo ou faixa fora do observado
SEM_FATOR      = "SEM_FATOR"        # subscricao: nao e evento de ajuste de preco
PRECO_INVALIDO = "PRECO_INVALIDO"   # preco zero ou negativo: divisao impossivel

# data_ex_status -- `lastDatePrior` e o ULTIMO DIA COM DIREITO; a data ex e o pregao
# SEGUINTE, e saber qual e ele exige calendario observado (ver `calendario.py`).
DERIVADA           = "DERIVADA"            # o calendario cobre, e o proximo pregao saiu
SEM_CALENDARIO     = "SEM_CALENDARIO"      # nao ha COTAHIST nenhum no acervo
FORA_DA_COBERTURA  = "FORA_DA_COBERTURA"   # ha calendario, mas nao alcanca esta data


# ── A-05, 12/09/2026: enumeracao OBSERVADA, e a guarda que faltava ────────────
#
# Ate hoje este modulo aceitava qualquer `label` em silencio. Isso viola a regra que o
# proprio projeto escreveu em `docs/fontes/cvm-enumeracoes-observadas.md`, para as
# enumeracoes da CVM: *"um parser que encontre valor fora de uma lista OBSERVADO deve
# FALHAR RUIDOSAMENTE -- nunca tratar como um dos valores conhecidos por padrao, nunca
# ignorar a linha em silencio."*
#
# A regra valia para a CVM e nao tinha equivalente aqui. E o defeito apareceu no mesmo
# dia: ao investigar o A-03, o codigo BRFS devolveu um evento de tipo **INCORPORACAO**,
# que nao estava em nenhuma lista deste arquivo e que teria entrado sem ninguem notar.
#
# INCORPORACAO importa mais que os outros: ela troca acoes de uma empresa por acoes de
# outra, numa relacao de troca. NAO e so ajuste de preco -- e mudanca de IDENTIDADE do
# ativo. Tratar como evento comum juntaria duas series diferentes.
#
# Esta lista e OBSERVADA, nao documentada: vale para o que foi visto em 11-12/09/2026.
TIPOS_DE_CAIXA = ("DIVIDENDO", "JRS CAP PROPRIO", "RENDIMENTO")
TIPOS_DE_QUANTIDADE = ("DESDOBRAMENTO", "GRUPAMENTO", "BONIFICACAO", "INCORPORACAO",
                       "CISAO", "CISAO PARCIAL")
TIPOS_DE_DIREITO = ("SUBSCRICAO",)
TIPOS_OBSERVADOS = TIPOS_DE_CAIXA + TIPOS_DE_QUANTIDADE + TIPOS_DE_DIREITO

TIPO_DESCONHECIDO = "TIPO_DESCONHECIDO"   # entra na tabela, mas GRITA no fim


# ─────────────────────────────────────────────── conversao do formato brasileiro

def dec_br(texto):
    """'15.468.781.313,18' -> Decimal('15468781313.18'). None quando vazio.

    A ORDEM DAS DUAS TROCAS IMPORTA e e por isso que esta funcao existe: remover o
    ponto DEPOIS de trocar a virgula transformaria '0,65' em '065'. Primeiro o
    separador de milhar, depois o decimal.

    Decimal e nao float: sao ~8 mil somas, e `0.1 + 0.2 != 0.3` acumula."""
    if texto is None: return None
    t = str(texto).strip()
    if not t: return None
    t = t.replace(".", "").replace(",", ".")
    try:
        return Decimal(t)
    except InvalidOperation:
        return None


def data_br(texto):
    """'25/04/2008' -> date(2008, 4, 25). None quando vazio ou invalido.

    A LINHA MAIS PERIGOSA DO MODULO. `date.fromisoformat` e o `CAST` do SQL leem
    '05/09/2026' como ISO e podem devolver 9 de MAIO -- e nos dias <= 12 as duas
    leituras sao datas VALIDAS, entao nao ha excecao: ha uma serie deslocada.
    Por isso o formato e explicito, e por isso ha um teste com dia <= 12."""
    if texto is None: return None
    t = str(texto).strip()[:10]
    if not t: return None
    try:
        return dt.datetime.strptime(t, "%d/%m/%Y").date()
    except ValueError:
        return None


# ──────────────────────────────────────────────────────────────── os fatores

def fator_de_provento(valor, preco_vespera):
    """(fator, status) para provento em dinheiro.

        fator = (P_vespera - valor) / P_vespera

    `P_vespera` e o fechamento na VESPERA DA DATA EX, e vem no proprio registro do
    endpoint paginado (`closingPricePriorExDate`). Foi esse campo que permitiu separar
    o problema em dois: a serie de FATORES sai sem nenhuma serie de precos."""
    if valor is None or preco_vespera is None:
        return None, SEM_PRECO
    if preco_vespera <= 0:
        return None, PRECO_INVALIDO
    return (preco_vespera - valor) / preco_vespera, CALCULADO


def fator_de_quantidade(factor, tipo):
    """(fator, status) para evento de QUANTIDADE. `fator` e multiplicador de PRECO,
    a mesma convencao de `fator_de_provento`.

    ACHADO C-01 -- aberto em 12/09/2026, MEDIDO e fechado em 16/09.

    A pergunta era: `factor` e percentual ou multiplicador? As duas leituras produzem
    numero, e uma delas erra por ate 50x. Ate 16/09 este modulo RECUSAVA escolher e
    devolvia `FACTOR_AMBIGUO` para os 180 eventos de quantidade do acervo -- que foi a
    decisao certa, porque nao havia medicao.

    O QUE DECIDIU NAO FOI O PRECO, FOI A DISTRIBUICAO. Os 65 desdobramentos do acervo
    usam onze valores distintos de `factor`, e lidos como PERCENTUAL todos caem em cima
    de razoes canonicas:

        100 -> 2x    200 -> 3x    300 -> 4x    400 -> 5x
        900 -> 10x   1900 -> 20x  4900 -> 50x  7900 -> 80x   9900 -> 100x

    Lidos como multiplicador dariam 101, 201, 901, 9901 -- e o `...01` e a propria
    denuncia: sao `(fator-1)*100`. Onze valores caindo por acaso a um centesimo de uma
    razao inteira nao e plausibilidade, e assinatura aritmetica.

    E A REGRA NAO E UMA SO, e essa foi a parte que eu nao esperava. Os 41 GRUPAMENTOS
    trazem 0,1 · 0,01 · 0,001 · 0,00002 -- **ali `factor` JA E o multiplicador de
    quantidade**, e menor que 1. Aplicar a regra do desdobramento num grupamento daria
    fator 1,00001: a serie passaria por um grupamento de 1000:1 SEM DEGRAU, em silencio,
    e na direcao pior. Um campo, dois significados, separados pelo rotulo.

    A TESTEMUNHA, que confirma a ordem de grandeza e nao mais que isso: FLRY,
    BONIFICACAO `factor: 5`, `lastDatePrior: 12/06/2023`. No COTAHIST 2023 a maior queda
    do FLRY3 no ano inteiro (-7,78%, 4,2 sigma) esta em 13/06 -- o pregao seguinte. Uma
    bonificacao de 5% pede -4,76%; a leitura como multiplicador pediria -83%. O COTAHIST
    resolve 50x com folga e NAO resolve 5% na casa decimal (sigma diario = 1,87%) -- e a
    pergunta era 50x.

    O QUE ELA RECUSA, e a recusa e parte da regra: INCORPORACAO (2 observacoes), CISAO e
    CISAO PARCIAL saem como `FACTOR_FORA_DA_REGRA`. Duas observacoes nao sustentam
    regra, e incorporacao e relacao de troca entre DUAS empresas -- pode nao ser a mesma
    aritmetica. Valor fora da faixa do rotulo tambem recusa: grupamento com `factor >= 1`
    seria um desdobramento com etiqueta errada, e adivinhar qual dos dois esta errado
    seria escrever ausencia de criterio no lugar de criterio.

    A regra cobre o que foi OBSERVADO nos 180. P6: o resto vira lacuna declarada."""
    if factor is None:
        return None, FACTOR_FORA_DA_REGRA
    t = (tipo or "").strip().upper()
    if t == "GRUPAMENTO":
        if not (0 < factor < 1):
            return None, FACTOR_FORA_DA_REGRA
        return Decimal(1)/factor, CALCULADO
    if t in ("DESDOBRAMENTO", "BONIFICACAO"):
        if factor <= 0:
            return None, FACTOR_FORA_DA_REGRA
        return Decimal(1)/(1 + factor/100), CALCULADO
    return None, FACTOR_FORA_DA_REGRA


# ──────────────────────────────────────────────────────── leitura do bronze

def _ler(caminho):
    """Devolve (dados, texto, n_registros).

    ACHADO A-06, 12/09/2026. `desembrulhar` NAO existia em `coletar_b3.py`: a logica
    estava EMBUTIDA dentro de `coletar_eventos`. Este modulo importava um nome que so
    existia numa copia de teste, e o teste que deveria impedir a duplicacao (N-01)
    passava, porque ele media a IDENTIDADE da referencia -- e a referencia existia.
    Uma guarda que mede o sintoma errado e pior que guarda nenhuma: ela da sossego.

    ACHADO A-07, mesma data. `desembrulhar` ja contava quantos registros a B3 devolveu
    para a mesma emissora, e o coletor imprimia esse numero. O silver descartava a
    contagem e usava o PRIMEIRO em silencio. Mais de um registro nao e erro -- e
    informacao -- mas escolher um deles sem dizer e escrever ausencia de criterio no
    lugar de criterio. A contagem sobe ate o relatorio final."""
    with open(caminho, encoding="utf-8") as f:
        texto = f.read()
    dados, n_registros = desembrulhar(texto)
    return dados, texto, n_registros


def conferir_tipo(tipo, desconhecidos):
    """Acumula o que nao esta na enumeracao observada. NAO descarta a linha -- descartar
    seria perder o dado; e NAO adivinha o tratamento -- adivinhar seria o F-02.

    A linha entra com `fator_status = TIPO_DESCONHECIDO` e o processo termina com codigo
    diferente de zero. Ruidoso, sem perder trabalho."""
    t = (tipo or "").strip().upper()
    if t and t not in TIPOS_OBSERVADOS:
        desconhecidos.setdefault(t, 0)
        desconhecidos[t] += 1
        return False
    return True


def _cabecalho(d, arquivo, dia, sha):
    return dict(
        cod=(d.get("code") or "").strip(),
        code_cvm=(d.get("codeCVM") or "").strip(),
        trading_name=(d.get("tradingName") or "").strip(),
        dt_captura=dia, arquivo_origem=arquivo, sha256_origem=sha,
    )


def linhas_do_suplemento(caminho, dia, desconhecidos=None, multiplos=None):
    """Le um `eventos/<EMISSORA>.json`. Devolve (linhas, aviso_ou_None)."""
    desconhecidos = {} if desconhecidos is None else desconhecidos
    multiplos = {} if multiplos is None else multiplos
    d, texto, n_reg = _ler(caminho)
    arquivo = os.path.basename(caminho)
    if n_reg > 1:
        multiplos[arquivo] = n_reg
    if not isinstance(d, dict):
        return [], "%s: nao desembrulha para objeto" % arquivo
    base = _cabecalho(d, arquivo, dia, sha256(texto))
    fora = []

    for e in (d.get("cashDividends") or []):
        valor = dec_br(e.get("rate"))
        f, st = fator_de_provento(valor, None)        # suplemento NAO traz preco
        if not conferir_tipo(e.get("label"), desconhecidos): st = TIPO_DESCONHECIDO
        fora.append(dict(base, origem="suplemento",
                         isin=(e.get("isinCode") or "").strip(), type_stock="",
                         tipo=(e.get("label") or "").strip(),
                         ultimo_dia_com_direito=data_br(e.get("lastDatePrior")),
                         data_aprovacao=data_br(e.get("approvedOn")),
                         data_pagamento=data_br(e.get("paymentDate")),
                         valor=valor, ratio=None, preco_vespera=None,
                         fator=f, fator_status=st))

    for e in (d.get("stockDividends") or []):
        ratio = dec_br(e.get("factor"))
        f, st = fator_de_quantidade(ratio, e.get("label"))
        if not conferir_tipo(e.get("label"), desconhecidos): st = TIPO_DESCONHECIDO
        fora.append(dict(base, origem="suplemento",
                         isin=(e.get("isinCode") or "").strip(), type_stock="",
                         tipo=(e.get("label") or "").strip(),
                         ultimo_dia_com_direito=data_br(e.get("lastDatePrior")),
                         data_aprovacao=data_br(e.get("approvedOn")),
                         data_pagamento=None,
                         valor=None, ratio=ratio, preco_vespera=None,
                         fator=f, fator_status=st))

    for e in (d.get("subscriptions") or []):
        # Subscricao NAO e evento de ajuste de preco: e um DIREITO, e so vira efeito se
        # o titular exercer. Fica na tabela porque e evento societario e porque a P6
        # manda guardar o dado de que a regua futura vai precisar -- com SEM_FATOR, para
        # que ninguem a inclua num produtorio por distracao.
        fora.append(dict(base, origem="suplemento",
                         isin=(e.get("isinCode") or "").strip(), type_stock="",
                         tipo=(e.get("label") or "").strip(),
                         ultimo_dia_com_direito=data_br(e.get("lastDatePrior")),
                         data_aprovacao=data_br(e.get("approvedOn")),
                         data_pagamento=data_br(e.get("subscriptionDate")),
                         valor=dec_br(e.get("priceUnit")),
                         ratio=dec_br(e.get("percentage")), preco_vespera=None,
                         fator=None, fator_status=SEM_FATOR))
    return fora, None


def linhas_do_paginado(pasta, dia, cabecalho, desconhecidos=None, multiplos=None,
                       nao_objeto=None):
    """Le `proventos/<EMISSORA>/pagina-*.json`. `cabecalho` vem do suplemento, porque o
    paginado nao traz `code`, `codeCVM` nem `tradingName` -- so os proventos."""
    desconhecidos = {} if desconhecidos is None else desconhecidos
    multiplos = {} if multiplos is None else multiplos
    nao_objeto = [] if nao_objeto is None else nao_objeto
    fora = []
    for arq in sorted(os.listdir(pasta)):
        if not arq.startswith("pagina-") or not arq.endswith(".json"):
            continue
        caminho = os.path.join(pasta, arq)
        d, texto, n_reg = _ler(caminho)
        rel = os.path.join(os.path.basename(pasta), arq)
        if n_reg > 1:
            multiplos[rel] = n_reg
        # ACHADO A-07. A MESMA condicao era AVISO no suplemento e `continue` MUDO aqui.
        # Duas leituras da mesma falha, no mesmo modulo, discordando entre si -- e a
        # muda vence, porque e a que roda 8 mil vezes. Pagina que nao desembrulha para
        # objeto e pagina PERDIDA: some do silver sem deixar rastro no relatorio.
        if not isinstance(d, dict):
            nao_objeto.append(rel)
            continue
        base = dict(cabecalho, arquivo_origem=rel, sha256_origem=sha256(texto))
        for e in (d.get("results") or []):
            valor = dec_br(e.get("valueCash"))
            preco = dec_br(e.get("closingPricePriorExDate"))
            f, st = fator_de_provento(valor, preco)
            if not conferir_tipo(e.get("corporateAction"), desconhecidos):
                st = TIPO_DESCONHECIDO
            fora.append(dict(base, origem="paginado", isin="",
                             type_stock=(e.get("typeStock") or "").strip(),
                             tipo=(e.get("corporateAction") or "").strip(),
                             ultimo_dia_com_direito=data_br(e.get("lastDatePriorEx")),
                             data_aprovacao=data_br(e.get("dateApproval")),
                             data_pagamento=None,
                             valor=valor, ratio=dec_br(e.get("ratio")),
                             preco_vespera=preco, fator=f, fator_status=st))
    return fora


# ────────────────────────────────────────────────────────────────── escrita

def _texto(v):
    """Decimal vira string EXATA (nunca float); date vira ISO; None vira vazio."""
    if v is None: return ""
    if isinstance(v, Decimal): return format(v, "f")
    if isinstance(v, dt.date): return v.isoformat()
    return str(v)


def gravar_csv(linhas, caminho):
    """Ordem ESTAVEL. Sem isso o instantaneo dourado acusa diferenca a cada rodada e
    para de servir como rede -- o defeito custa mais que a ausencia da rede."""
    def chave(ln):
        return (ln["cod"], ln["origem"], _texto(ln["ultimo_dia_com_direito"]), ln["tipo"],
                ln["type_stock"], ln["isin"], _texto(ln["valor"]), _texto(ln["ratio"]))
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, lineterminator="\n")
        w.writeheader()
        for ln in sorted(linhas, key=chave):
            w.writerow({c: _texto(ln.get(c)) for c in COLUNAS})


def ultima_captura(raiz):
    base = os.path.join(raiz, "eventos")
    if not os.path.isdir(base): return None
    dias = sorted(d for d in os.listdir(base) if d.startswith("dt_captura="))
    return dias[-1][len("dt_captura="):] if dias else None


def refinar(raiz=RAIZ_PADRAO, dia=None, saida=SAIDA_PADRAO, cotahist=None):
    cotahist = COTAHIST_PADRAO if cotahist is None else cotahist
    dia = dia or ultima_captura(raiz)
    if not dia:
        print("nao ha captura de eventos em %s -- rode o coletar_b3.py antes."
              % os.path.abspath(raiz), file=sys.stderr)
        return 2

    pasta_ev = os.path.join(raiz, "eventos", "dt_captura=" + dia)
    pasta_pr = os.path.join(raiz, "proventos", "dt_captura=" + dia)
    if not os.path.isdir(pasta_ev):
        print("captura %s nao existe em %s" % (dia, pasta_ev), file=sys.stderr)
        return 2

    linhas, avisos, emissoras, sem_paginado = [], [], 0, []
    desconhecidos, multiplos, nao_objeto = {}, {}, []
    for arq in sorted(os.listdir(pasta_ev)):
        if not arq.endswith(".json") or "NAO-E-OBJETO" in arq:
            continue
        emissoras += 1
        novas, aviso = linhas_do_suplemento(os.path.join(pasta_ev, arq), dia,
                                            desconhecidos, multiplos)
        if aviso: avisos.append(aviso)
        linhas.extend(novas)

        em = arq[:-len(".json")]
        cab = next((dict(cod=ln["cod"], code_cvm=ln["code_cvm"],
                         trading_name=ln["trading_name"], dt_captura=dia)
                    for ln in novas), dict(cod=em, code_cvm="", trading_name="",
                                          dt_captura=dia))
        sub = os.path.join(pasta_pr, em)
        if os.path.isdir(sub):
            linhas.extend(linhas_do_paginado(sub, dia, cab, desconhecidos,
                                             multiplos, nao_objeto))
        else:
            sem_paginado.append(em)

    # ── a data ex, DERIVADA do calendario observado (16/09/2026) ───────────────
    # `lastDatePrior` e o ULTIMO DIA COM DIREITO: o degrau de preco cai no pregao
    # SEGUINTE. Ate 16/09 a coluna se chamava `data_ex` e guardava o outro dia -- nome
    # que mente e o defeito recorrente deste projeto, e aqui ele deslocaria TODO ajuste
    # de preco em um pregao. O calendario vem do COTAHIST do proprio acervo; onde ele
    # nao alcanca, a linha diz que nao sabe em vez de chutar o proximo dia util.
    datas, cobertura = calendario.pregoes(cotahist)
    for ln in linhas:
        d = calendario.proximo_pregao(ln["ultimo_dia_com_direito"], datas, cobertura)
        ln["data_ex"] = d
        ln["data_ex_status"] = (DERIVADA if d else
                                (SEM_CALENDARIO if not datas else FORA_DA_COBERTURA))

    destino = os.path.join(saida, "eventos_silver_%s.csv" % dia)
    gravar_csv(linhas, destino)

    porc, pdat = {}, {}
    for ln in linhas:
        porc[ln["fator_status"]] = porc.get(ln["fator_status"], 0) + 1
        pdat[ln["data_ex_status"]] = pdat.get(ln["data_ex_status"], 0) + 1
    print("captura %s -- %d emissoras, %d linhas" % (dia, emissoras, len(linhas)))
    print("  fator:")
    for st in sorted(porc): print("    %-22s %6d" % (st, porc[st]))
    print("  data ex (calendario de pregoes, de %s: %s):"
          % (os.path.abspath(cotahist),
             "%s a %s, %d pregoes" % (cobertura[0], cobertura[1], len(datas))
             if datas else "AUSENTE -- nenhum COTAHIST nessa pasta"))
    for st in sorted(pdat): print("    %-22s %6d" % (st, pdat[st]))
    print("  -> %s" % os.path.abspath(destino))
    if sem_paginado:
        print("\nSEM historico longo (%d): %s" % (len(sem_paginado),
                                                  ", ".join(sem_paginado)))
        print("Nao e 'empresa sem proventos' -- e captura que nao fechou. Ver B-02/B-03.")
    if avisos:
        print("\nAVISOS:")
        for a in avisos: print("  " + a)
    if desconhecidos:
        print("\nTIPO FORA DA ENUMERACAO OBSERVADA (A-05) -- %d tipo(s):" % len(desconhecidos))
        for t in sorted(desconhecidos): print("  %-24s %5d linha(s)" % (t, desconhecidos[t]))
        print("As linhas ENTRARAM na tabela, com fator_status=TIPO_DESCONHECIDO. Nada foi\n"
              "descartado e nada foi adivinhado. Antes de usar: descubra o que o tipo faz\n"
              "com o preco e acrescente-o a TIPOS_OBSERVADOS -- nunca ao contrario.")
    if multiplos:
        print("\nMAIS DE UM REGISTRO PARA A MESMA EMISSORA (A-07) -- %d arquivo(s):"
              % len(multiplos))
        for a in sorted(multiplos): print("  %-40s %3d registros" % (a, multiplos[a]))
        print("O silver usou o PRIMEIRO. Isso nao e uma regra -- e a ordem em que a B3\n"
              "devolveu. Antes de confiar na linha: abra o bronze e descubra por que ha\n"
              "mais de um, e qual deles e o certo.")
    if nao_objeto:
        print("\nPAGINA QUE NAO DESEMBRULHA PARA OBJETO (A-07) -- %d:" % len(nao_objeto))
        for a in nao_objeto: print("  " + a)
        print("Estas paginas NAO entraram no silver. O bronze continua no disco.")
    if porc.get(FACTOR_FORA_DA_REGRA):
        print("\n%d evento(s) com FATOR FORA DA REGRA: rotulo ou faixa que a medicao do"
              "\nC-01 (16/09/2026) nao cobre -- INCORPORACAO, CISAO, ou valor fora da"
              "\nfaixa do rotulo. A linha ENTROU na tabela, marcada. Fechar exige medir"
              "\nmais casos, nunca estender a regra por analogia."
              % porc[FACTOR_FORA_DA_REGRA])
    if pdat.get(FORA_DA_COBERTURA) or pdat.get(SEM_CALENDARIO):
        # P-114: esta frase dizia `data/bronze/b3/` e era FALSA para o disco como ele
        # estava -- os anos entravam em `cotahist/` e o modulo nao os via. Agora ela
        # nomeia a pasta que o modulo LEU DE FATO, e nao uma que ele supoe ler.
        print("\n%d linha(s) SEM data ex derivada: o calendario de pregoes vem do COTAHIST"
              "\ne nao alcanca essas datas. Cada ano que entrar em %s amplia a"
              "\ncobertura sozinho -- nao ha o que mudar no codigo."
              % (pdat.get(FORA_DA_COBERTURA, 0) + pdat.get(SEM_CALENDARIO, 0),
                 os.path.abspath(cotahist)))
    # O codigo de saida e o resumo honesto da corrida: zero so quando nada ficou
    # pendurado. `multiplos` NAO entra -- ele e informacao para conferir, nao defeito.
    return 1 if (desconhecidos or nao_objeto) else 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Bronze -> silver dos eventos da B3.")
    p.add_argument("--raiz", default=RAIZ_PADRAO,
                   help="acervo de eventos/proventos (padrao: %s)" % RAIZ_PADRAO)
    p.add_argument("--cotahist", default=COTAHIST_PADRAO,
                   help="acervo de COTAHIST, de onde sai o CALENDARIO (padrao: %s)"
                        % COTAHIST_PADRAO)
    p.add_argument("--saida", default=SAIDA_PADRAO)
    p.add_argument("--dia", metavar="AAAA-MM-DD",
                   help="captura a refinar (padrao: a mais recente)")
    a = p.parse_args(argv)
    return refinar(a.raiz, a.dia, a.saida, a.cotahist)


if __name__ == "__main__":
    sys.exit(main())

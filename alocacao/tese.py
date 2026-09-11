# -*- coding: utf-8 -*-
"""
Bloco K (teses) e registro CARREGO — os dois registros que o usuario preenche.

Por que este modulo vem ANTES de qualquer campo calculado:
  K-02, K-03 e K-04 sao os unicos campos do catalogo inteiro que NENHUM dado publico
  preenche. Nao dependem da CVM, do COTAHIST nem do pipeline. E sao os unicos que
  mudam comportamento hoje.

DOIS registros, porque sao DOIS modos de falha diferentes (bloco-k-definicoes, §1):

  TESE (bloco K)      modo de falha: manter indefinidamente uma posicao que era para
                      ser temporaria. Antidoto: prazo e condicao de falsificacao.
  CARREGO             modo de falha: comprar para carregar, ver a marcacao a mercado
                      abrir, e vender no pior momento. Antidoto: condicao de venda
                      antecipada declarada ANTES, e o custo de quebrar estimado.

O sistema nao existe para excluir ativos. Existe para exigir que o papel de cada
ativo seja NOMEADO — ativo sem papel nomeado nao pode ser dimensionado, porque nao
ha como saber quanto dele e demais.

Mecanismo anti-reclassificacao retroativa: cada registro carrega uma IMPRESSAO (hash
dos campos que o definem). Alterar qualquer um sem mover o registro anterior para
`historico` invalida. Reescrever depois de ver o preco deixa de ser possivel sem rastro.
"""
from __future__ import annotations
import os, re, hashlib, datetime as dt
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))

# Expressoes que descrevem esperanca, nao tese. Casadas por FRONTEIRA DE PALAVRA:
# `if v in texto` recusava "a empresa atende a 3 milhoes de clientes ate 31/12/2030",
# porque "atende a" contem "tende a". Achado V-04, demonstrado por execucao.
VAGO_DURO = ("longo prazo", "vai subir", "vai valorizar", "acredito", "tende a",
             "eventualmente", "no futuro", "pode chegar", "deve subir", "espero que")
# "potencial" e "promissor" sao legitimos como termo tecnico ("capacidade potencial
# instalada"). Nenhuma regex separa os usos: viram AVISO, nao rejeicao.
VAGO_BRANDO = ("potencial", "promissor", "o futuro")

# Palavras de PRECO. Numa posicao em que se aceitou perder 100%, a condicao de
# falsificacao nao pode ser "o preco caiu" — a queda esta dentro da perda aceita em
# K-01, e a posicao se encerraria exatamente quando a tese exigiria paciencia.
PRECO = ("caiu", "cair", "queda de", "abaixo de r$", "desvalorizar", "stop",
         "perder mais de", "recuar")

# ── Estados de um registro (achado G-01, 05/09/2026) ─────────────────────────
# O schema original so admitia um estado: compromisso pronto. Ele presume uma
# posicao que existe ou vai existir ja. Mas o usuario esta na Fase A ate ~2030 e
# nao tem conta em corretora — e C02 exige o juro real TRAVADO, que so existe no
# dia da compra, e K02 nas formas A e B depende do estado do mercado naquele dia.
#
# Preencher esses campos hoje nao seria pre-registro: seria ficcao com hash.
# Deixar em branco tambem nao serve — as REGRAS (prazo, condicao de venda, teto,
# reconhecimento) sao decidiveis hoje, e hoje e exatamente quando pre-registra-las
# tem valor: antes da posicao existir.
#
# Dai dois estados. REGRA_DECIDIDA sela o que e decidivel e declara o que falta;
# COMPROMISSO_ATIVO exige tudo. A migracao de um para o outro acontece na compra,
# recalcula a impressao e manda a antiga para `historico` — o rastro fica.
ESTADOS = ("REGRA_DECIDIDA", "COMPROMISSO_ATIVO")

# Campos que so podem ser preenchidos com a posicao na mao. Em REGRA_DECIDIDA eles
# precisam estar EXPLICITAMENTE adiados, nao simplesmente vazios: a diferenca entre
# "ainda nao sei" e "esqueci" e a unica coisa que este arquivo protege.
DIFERIDOS_C = ("C02_compromisso", "C04_custo_de_quebrar")
# Nao ha equivalente para teses, e a ausencia e de proposito (11/09/2026): existia uma
# constante assim e nada a lia. O G-01 nasceu do C02, que depende do juro travado NA
# COMPRA; o K02 nao depende de compra nenhuma. Diferir a tese selaria na impressao um
# texto vazio -- pre-registro de nada.
AGUARDA = "AGUARDA_COMPRA"

CAMPOS_K = ("K01_perda_maxima_aceita", "K02_tese", "K03_prazo",
            "K04_falsificacao", "K05_liquidez_saida_dias")
CAMPOS_C = ("C01_horizonte_de_carrego", "C02_compromisso",
            "C03_condicao_de_venda_antecipada", "C04_custo_de_quebrar",
            "C05_teto_da_funcao", "C06_reconhecimento")

def _hash(*partes):
    return hashlib.sha256("|".join(str(p) for p in partes).encode("utf-8")).hexdigest()[:16]

def impressao(t):
    """Hash dos tres campos que definem a TESE."""
    return _hash(t.get("K02_tese",""), t.get("K03_prazo",""), t.get("K04_falsificacao",""))

def impressao_carrego(c):
    """Hash dos tres campos que definem o COMPROMISSO."""
    return _hash(c.get("C01_horizonte_de_carrego",""), c.get("C02_compromisso",""),
                 c.get("C03_condicao_de_venda_antecipada",""))

def _achados(termos, texto):
    return [v for v in termos if re.search(rf"\b{re.escape(v)}", texto)]

def _anos_ate(data, base):
    return (data - base).days/365.25

# ══ VALIDADOR DE TESE (bloco K) ══════════════════════════════════════════════
def validar_tese(t, hoje=None, compromisso_maximo_anos=None):
    """(valida, problemas, avisos). Nao levanta: o output mostra TODOS os problemas
    de uma vez, nao o primeiro."""
    hoje = hoje or dt.date.today()
    p, av = [], []
    if t.get("exemplo"):
        p.append("registro marcado como `exemplo: true` — modelo, nao tese real")
    for c in CAMPOS_K:
        if t.get(c) in (None, "", []): p.append(f"{c} ausente")

    k1 = t.get("K01_perda_maxima_aceita")
    if k1 is not None and t.get("catalogo") == "ESPECULATIVO" and abs(k1-1.0) > 1e-9:
        p.append(f"K01 = {k1}: no catalogo especulativo a perda maxima aceita e sempre "
                 f"1.0 (100%). Declarar menos e supor um piso que nao existe")

    k2 = (t.get("K02_tese") or "").strip(); baixo = k2.lower()
    if k2:
        duros = _achados(VAGO_DURO, baixo)
        if duros:
            p.append(f"K02 contem expressao nao falsificavel: {duros}. Uma tese e "
                     f"'X acontece ate a data D', nao uma expectativa de direcao")
        brandos = _achados(VAGO_BRANDO, baixo)
        if brandos:
            av.append(f"K02 contem {brandos} — legitimo como termo tecnico, vago como "
                      f"tese. Confira se a frase afirma QUANTO e QUANDO")
        if len(k2.split()) < 6:
            p.append("K02 curta demais para ser falsificavel")
        # o teste estrutural, que e o que de fato separa tese de esperanca
        if not re.search(r"\d", k2):
            p.append("K02 sem nenhum numero verificavel: uma tese falsificavel afirma "
                     "QUANTO ou QUANDO, nao apenas o que")

    k3 = t.get("K03_prazo")
    if k3 is not None and not isinstance(k3, dt.date):
        p.append(f"K03 = {k3!r} nao e uma data. 'longo prazo' nao e prazo")
    elif isinstance(k3, dt.date):
        dtc = t.get("dt_classificacao")
        if isinstance(dtc, dt.date) and k3 <= dtc:
            p.append("K03 anterior ou igual a data de classificacao")
        if compromisso_maximo_anos:
            a = _anos_ate(k3, dtc if isinstance(dtc, dt.date) else hoje)
            if a > compromisso_maximo_anos:
                p.append(f"K03 assume compromisso de {a:.1f} anos, acima do teto "
                         f"declarado de {compromisso_maximo_anos} anos "
                         f"(politica.yaml: compromissos.maximo_anos)")

    k4 = (t.get("K04_falsificacao") or "").strip(); k4b = k4.lower()
    if k4:
        if k4b == baixo:
            p.append("K04 identica a K02: a condicao de falsificacao tem de ser um EVENTO "
                     "observavel que encerra a posicao, nao a negacao da frase")
        pr = _achados(PRECO, k4b)
        if pr:
            p.append(f"K04 e uma condicao de PRECO ({pr}). Com K01 = 100%, a queda ja esta "
                     f"dentro da perda aceita: uma condicao de preco encerraria a posicao "
                     f"exatamente quando a tese exigiria paciencia. K04 tem de ser um evento "
                     f"que INVALIDA a tese, nao um que machuca a posicao")

    L = t.get("L_teste_de_classificacao")
    if not L:
        p.append("bloco L ausente: o teste de classificacao contra os portoes de buy & hold "
                 "(A e C) e obrigatorio e nao impede a compra — ele torna impossivel a "
                 "reclassificacao retroativa")
    else:
        if not L.get("rodado_em"): p.append("bloco L sem data de execucao")
        if "reprova" not in L:     p.append("bloco L sem a lista `reprova` — mesmo vazia, "
                                            "tem de ser explicita")

    imp, calc = t.get("impressao"), impressao(t)
    if imp in (None, "", "PENDENTE"):
        p.append(f"impressao ausente — registre `impressao: {calc}`")
    elif imp != calc:
        p.append(f"tese ALTERADA apos o registro: impressao gravada {imp}, calculada {calc}. "
                 f"Para mudar a tese, mova o registro atual para `historico` e registre "
                 f"outra com nova dt_classificacao")
    return (len(p) == 0), p, av

# ══ VALIDADOR DE CARREGO ═════════════════════════════════════════════════════
def validar_carrego(c, hoje=None, compromisso_maximo_anos=None):
    """(valida, problemas, avisos, duracao_anos).

    A duracao NAO e constante de catalogo: ela vem do papel que voce se compromete a
    carregar. E por isso que o registro precede a alocacao — sem ele o sistema nao
    sabe dimensionar, e inventar uma duracao seria supor um compromisso que ninguem
    assumiu."""
    hoje = hoje or dt.date.today()
    p, av, dur = [], [], None
    if c.get("exemplo"):
        p.append("registro marcado como `exemplo: true` — modelo, nao compromisso real")

    estado = c.get("estado", "COMPROMISSO_ATIVO")
    if estado not in ESTADOS:
        p.append(f"estado {estado!r} desconhecido; use um de {ESTADOS}")
    regra_so = (estado == "REGRA_DECIDIDA")

    for k in CAMPOS_C:
        if regra_so and k in DIFERIDOS_C:
            # em REGRA_DECIDIDA o campo tem de dizer que espera a compra — em voz alta
            v = c.get(k)
            marcado = (v == AGUARDA) or (isinstance(v, dict) and v.get("estado") == AGUARDA)
            if not marcado:
                p.append(f"{k}: em REGRA_DECIDIDA este campo precisa valer "
                         f"{AGUARDA!r} — vazio nao distingue 'ainda nao sei' de 'esqueci'")
            continue
        if c.get(k) in (None, "", []): p.append(f"{k} ausente")

    c1 = c.get("C01_horizonte_de_carrego")
    dtr = c.get("dt_registro")
    if c1 is not None and not isinstance(c1, dt.date):
        p.append(f"C01 = {c1!r} nao e uma data. O compromisso e ate o VENCIMENTO do papel")
    elif isinstance(c1, dt.date):
        base = dtr if isinstance(dtr, dt.date) else hoje
        dur = _anos_ate(c1, base)
        if dur <= 0:
            p.append("C01 no passado: o papel ja venceu")
        elif compromisso_maximo_anos and dur > compromisso_maximo_anos:
            _limite = base + dt.timedelta(days=int(compromisso_maximo_anos*365.25))
            p.append(f"C01 assume carrego de {dur:.1f} anos, acima do teto declarado de "
                     f"{compromisso_maximo_anos} anos. Escolha um vencimento ate "
                     f"{_limite.isoformat()}")

    c2 = "" if regra_so else (c.get("C02_compromisso") or "").strip()
    if c2 and not re.search(r"\d", c2):
        p.append("C02 sem numero: o compromisso declara QUAL papel e QUAL juro real "
                 "travado, nao uma intencao")

    c3 = (c.get("C03_condicao_de_venda_antecipada") or "").strip().lower()
    if c3:
        pr = _achados(PRECO, c3)
        if pr:
            p.append(f"C03 e uma condicao de PRECO ({pr}). O modo de falha desta funcao e "
                     f"exatamente vender quando a marcacao abre — uma condicao de preco "
                     f"AUTORIZA o erro que o registro existe para impedir. C03 tem de ser "
                     f"um EVENTO (necessidade de caixa, oportunidade de recompra com ganho "
                     f"liquido de imposto)")
        if len(c3.split()) < 5:
            p.append("C03 curta demais para descrever um evento")

    c4 = c.get("C04_custo_de_quebrar") or {}
    if regra_so:
        pass    # o custo de quebrar depende do papel e da duracao — vem com a compra
    elif not isinstance(c4, dict) or c4.get("perda_estimada_pct") in (None, "", "____"):
        p.append("C04.perda_estimada_pct ausente: escrever o numero ANTES e o que muda o "
                 "comportamento depois")
    elif not c4.get("fonte_da_estimativa"):
        av.append("C04 sem fonte da estimativa")
    if regra_so:
        av.append("estado REGRA_DECIDIDA: as regras estao seladas, a posicao nao existe. "
                  "O G8 NAO libera peso neste estado — ele libera quando virar "
                  "COMPROMISSO_ATIVO, no dia da compra.")

    c5 = c.get("C05_teto_da_funcao")
    if isinstance(c5, (int, float)) and not (0 < c5 <= 1):
        p.append(f"C05 = {c5}: e uma fracao do patrimonio, entre 0 e 1")
    if c.get("C06_reconhecimento") is not True:
        p.append("C06_reconhecimento tem de ser true — e assinatura, nao decoracao: "
                 "'entendo que a marcacao pode abrir e que isso nao e perda se eu carregar'")

    imp, calc = c.get("impressao"), impressao_carrego(c)
    if imp in (None, "", "PENDENTE"):
        p.append(f"impressao ausente — registre `impressao: {calc}`")
    elif imp != calc:
        p.append(f"compromisso ALTERADO apos o registro: gravado {imp}, calculado {calc}")
    return (len(p) == 0), p, av, dur

# ══ CARGA ════════════════════════════════════════════════════════════════════
def carregar_registros(path=None, hoje=None, compromisso_maximo_anos=None):
    """Devolve (teses, carregos) na forma que G7 e G8 consomem."""
    p = path or os.path.join(AQUI, "teses.yaml")
    if not os.path.exists(p): return {}, {}
    with open(p, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    teses, carregos = {}, {}
    for aid, t in (doc.get("teses") or {}).items():
        t = dict(t or {}); t.setdefault("ativo_id", aid)
        ok, probs, av = validar_tese(t, hoje, compromisso_maximo_anos)
        teses[aid] = dict(valida=ok, motivo="; ".join(probs), avisos=av, tese=t)
    for aid, c in (doc.get("carregos") or {}).items():
        c = dict(c or {}); c.setdefault("ativo_id", aid)
        ok, probs, av, dur = validar_carrego(c, hoje, compromisso_maximo_anos)
        carregos[aid] = dict(valida=ok, motivo="; ".join(probs), avisos=av,
                             duracao_anos=dur, carrego=c)
    return teses, carregos

def carregar_teses(path=None, hoje=None, compromisso_maximo_anos=None):
    return carregar_registros(path, hoje, compromisso_maximo_anos)[0]

def relatorio_bloco_L(t):
    L = t.get("L_teste_de_classificacao") or {}
    rep = L.get("reprova") or []
    return (f"ativo {t.get('ativo_id')} · classificado como {t.get('funcao','APOSTA')} "
            f"em {t.get('dt_classificacao')}\n"
            f"reprova: {', '.join(rep) if rep else '(nenhum portao registrado)'}\n"
            f"tese: {t.get('K02_tese')} · prazo: {t.get('K03_prazo')} · "
            f"falsificacao: {t.get('K04_falsificacao')}\n"
            f"perda maxima aceita: {(t.get('K01_perda_maxima_aceita') or 0)*100:.0f}%")

if __name__ == "__main__":
    import yaml as _y
    P = _y.safe_load(open(os.path.join(AQUI, "politica.yaml"), encoding="utf-8"))
    teto = P["compromissos"]["maximo_anos"]
    ts, cs = carregar_registros(compromisso_maximo_anos=teto)
    print(f"teto de compromisso declarado: {teto} anos\n")
    for rot, d, imp_f in (("TESES", ts, impressao), ("CARREGOS", cs, impressao_carrego)):
        print("="*78); print(rot); print("="*78)
        if not d: print("  (nenhum registro)")
        for aid, r in d.items():
            print(f"\n{aid}: {'VALIDO' if r['valida'] else 'INVALIDO'}")
            for m in (r["motivo"].split("; ") if r["motivo"] else []): print(f"   - {m}")
            for a in r.get("avisos", []): print(f"   ~ aviso: {a}")
            reg = r.get("tese") or r.get("carrego")
            print(f"   impressao a registrar: {imp_f(reg)}")
            if r.get("duracao_anos") is not None:
                print(f"   duracao do carrego: {r['duracao_anos']:.1f} anos")

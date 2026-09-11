#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coletar_b3.py -- captura o dado PERECIVEL da B3: eventos societarios e composicao
de indice. Fase 0, achado V-01 (06/09/2026).

POR QUE ESTE ARQUIVO EXISTE, e por que ele vem antes de baixar a CVM.

Os ZIPs de DFP/ITR sao estaticos, tem dicionario publicado e ficam num portal oficial.
Eles nao evaporam. O que evapora e isto aqui:

  1. EVENTOS SOCIETARIOS (desdobramento, grupamento, bonificacao, provento). Sem eles
     uma serie de precos e INUTILIZAVEL para backtest: a PETR desdobrou 100:1 em
     25/04/2008 e o preco caiu 99% num dia sem nada ter acontecido com a empresa. O
     COTAHIST cru le isso como um crash. O endpoint que publica esses eventos NAO E
     DOCUMENTADO, nao tem contrato, nao tem SLA e nao tem espelho conhecido.
  2. CARTEIRA TEORICA DO INDICE. So existe para o dia corrente. O historico de
     composicao nao e publicado por ninguem, de graca, em lugar nenhum.

Em ambos, o que nao for capturado hoje nao se compra depois.

O QUE ESTE SCRIPT NAO FAZ, DE PROPOSITO.
Nao ajusta preco, nao calcula fator, nao normaliza nada. Ele grava o JSON como veio,
com sha256 e carimbo de tempo. Transformar e trabalho de outro passo, contra um acervo
imutavel. Acervo que ja nasce transformado nao se audita.

USO
    python coletar_b3.py --indice IBOV
    python coletar_b3.py --eventos                 # usa o ultimo snapshot de indice
    python coletar_b3.py --eventos --tickers PETR4,VALE3,ITUB4
    python coletar_b3.py --indice IBOV --eventos   # a rotina diaria
    python coletar_b3.py --proventos-completos     # historico longo; le o tradingName do acervo
    python coletar_b3.py --proventos-completos --tickers PETR4,VALE3

Sem dependencia de terceiro: so biblioteca padrao. Isso e deliberado -- este script NAO
entra na impressao digital do ambiente (`ambiente.py`), porque ele nao produz numero
nenhum; ele so grava bytes. Ver o bloco de P-15 no pyproject.toml.
"""

import argparse, base64, hashlib, json, os, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone

BASE = "https://sistemaswebb3-listados.b3.com.br"
URL_INDICE = BASE + "/indexProxy/indexCall/GetPortfolioDay/{p}"
URL_SUPLEMENTO = BASE + "/listedCompaniesProxy/CompanyCall/GetListedSupplementCompany/{p}"
URL_PROVENTOS = BASE + "/listedCompaniesProxy/CompanyCall/GetListedCashDividends/{p}"
TAMANHO_PAGINA = 99    # o do unico pedido observado (pesquisa 2.2); limite do servidor desconhecido
MAX_PAGINAS = 100      # trava de laco: 9.900 proventos, ~30x o historico inteiro da PETR

RAIZ_PADRAO = os.path.join("data", "bronze", "b3")
PAUSA_S = 1.2          # cortesia com o servidor. Nao e otimizavel: e educacao.
TENTATIVAS = 3
TEMPO_LIMITE_S = 30


# ---------------------------------------------------------------- utilitarios

def carga(d):
    """A B3 recebe o parametro como JSON em base64 dentro do CAMINHO da URL."""
    return base64.b64encode(json.dumps(d, separators=(",", ":")).encode("utf-8")).decode("ascii")


def buscar(url):
    """Devolve (texto, cabecalhos). Erro de rede sobe -- nao vira dado vazio."""
    ultimo = None
    for tentativa in range(1, TENTATIVAS + 1):
        req = urllib.request.Request(url, headers={
            "User-Agent": "bastter-fase0/1.0 (coleta pessoal de dado publico)",
            "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=TEMPO_LIMITE_S) as r:
                return r.read().decode("utf-8"), dict(r.headers)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            ultimo = e
            if tentativa < TENTATIVAS:
                time.sleep(PAUSA_S * 2 * tentativa)
    raise RuntimeError("falhou apos %d tentativas: %s -- %s" % (TENTATIVAS, url, ultimo))


def hoje():
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")


def agora_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def gravar(caminho, texto, forcar):
    """Snapshot e IMUTAVEL. Regravar por cima apaga a unica copia de um dia."""
    if os.path.exists(caminho) and not forcar:
        return False, "ja existe (use --forcar para reescrever)"
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
    return True, "gravado"


def sha256(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def anotar_manifesto(raiz, registro):
    """Um JSONL por captura. E o que permite provar depois o que foi baixado e quando."""
    cam = os.path.join(raiz, "manifesto.jsonl")
    os.makedirs(raiz, exist_ok=True)
    with open(cam, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------- indice

def coletar_indice(raiz, indice, dia, forcar):
    url = URL_INDICE.format(p=carga({
        "language": "pt-br", "pageNumber": 1, "pageSize": 200,
        "index": indice, "segment": "1",
    }))
    texto, _ = buscar(url)
    dados = json.loads(texto)

    # F-02 outra vez, num eixo novo: resposta vazia NAO pode virar "indice sem ativos".
    itens = dados.get("results") or []
    if not itens:
        raise RuntimeError(
            "indice %s voltou SEM ATIVOS. Isso quase nunca e verdade -- e nome de indice "
            "errado ou mudanca no endpoint. Nada foi gravado, de proposito." % indice)

    destino = os.path.join(raiz, "indices", "dt_captura=" + dia, indice + ".json")
    ok, nota = gravar(destino, texto, forcar)
    data_ref = (dados.get("header") or {}).get("date")
    codigos = sorted({(i.get("cod") or "").strip() for i in itens if i.get("cod")})

    anotar_manifesto(raiz, {
        "capturado_em": agora_iso(), "tipo": "indice", "indice": indice,
        "url": url, "arquivo": destino, "sha256": sha256(texto),
        "bytes": len(texto.encode("utf-8")), "itens": len(itens),
        "data_referencia_b3": data_ref, "gravado": ok, "nota": nota,
    })
    print("indice %-6s  %3d ativos  ref B3=%s  %s" % (indice, len(itens), data_ref, nota))
    return codigos


def ultimo_indice(raiz, indice):
    """Le o snapshot de indice mais recente que existir no acervo."""
    base = os.path.join(raiz, "indices")
    if not os.path.isdir(base):
        return None, []
    dias = sorted(d for d in os.listdir(base) if d.startswith("dt_captura="))
    for dia in reversed(dias):
        cam = os.path.join(base, dia, indice + ".json")
        if os.path.exists(cam):
            with open(cam, encoding="utf-8") as f:
                dados = json.load(f)
            cods = sorted({(i.get("cod") or "").strip()
                           for i in (dados.get("results") or []) if i.get("cod")})
            return dia, cods
    return None, []


# ------------------------------------------------------------------ eventos

def empresa_de(ticker):
    """PETR4 -> PETR. O endpoint pede o codigo da EMISSORA, que sao os 4 PRIMEIROS
    caracteres do ticker -- nao as 4 primeiras LETRAS.

    ACHADO DE 11/09/2026, e ele e silencioso. A versao anterior filtrava digitos:
    `"".join(c for c in ticker if c.isalpha())[:4]`. Funciona para 73 dos 74 ativos do
    IBOV e erra em **B3SA3**, cujo codigo de emissora e `B3SA` -- tem um digito no meio.
    A versao antiga produzia `BSA`, e o pior: o endpoint RESPONDEU, com capital social de
    R$9,61 bi e data de 1981. Ou seja, ele casou com OUTRA empresa e devolveu 200.

    E o modo de falha mais caro que existe aqui: nao e ausencia de dado, e dado do ativo
    ERRADO, com aparencia perfeita. Nenhum teste de "veio resposta?" pegaria.

    Ticker da B3 = 4 caracteres de emissora + 1-2 digitos (+ F de fracionario). Entao a
    regra certa e posicional, nao por tipo de caractere."""
    return ticker.upper().strip()[:4]


def coletar_eventos(raiz, tickers, dia, forcar):
    emissoras = sorted({empresa_de(t) for t in tickers if empresa_de(t)})
    vazias, erros, gravadas = [], [], 0
    fora_do_formato, sem_evento_nenhum = [], []

    for i, emissora in enumerate(emissoras, 1):
        url = URL_SUPLEMENTO.format(p=carga({"issuingCompany": emissora, "language": "pt-br"}))
        try:
            texto, _ = buscar(url)
            dados = json.loads(texto)
        except Exception as e:                       # noqa: BLE001 -- queremos o nome do erro
            erros.append((emissora, str(e)[:120]))
            print("  %3d/%d  %-5s  ERRO: %s" % (i, len(emissoras), emissora, str(e)[:60]))
            time.sleep(PAUSA_S)
            continue

        # ACHADO DE 11/09/2026, na primeira execucao real (ABEV foi a primeira e ja
        # quebrou). O endpoint NEM SEMPRE devolve objeto. Dois casos observados:
        #   1. JSON dentro de string -- `json.loads` uma vez devolve `str`, e dai
        #      `dados.get(...)` levanta AttributeError e DERRUBA A COLETA INTEIRA;
        #   2. string curta de erro da propria B3.
        # A versao anterior morria na primeira emissora esquisita e perdia as outras 75.
        # Regra nova: normaliza o que da, GRAVA o bruto de qualquer jeito (resposta
        # estranha e evidencia, nao lixo), e ACUSA no fim. Nunca derruba a corrida por
        # causa de um ativo.
        if isinstance(dados, str):
            try:
                dados = json.loads(dados)            # caso 1: JSON duplamente codificado
            except json.JSONDecodeError:
                pass
        # CASO 3, e ele e o formato NORMAL deste endpoint -- descoberto na primeira
        # corrida real (11/09/2026): as 74 emissoras devolveram **lista**, nao objeto.
        # A leitura anterior, feita por ferramenta de resumo, tinha desembrulhado a lista
        # de um elemento sem avisar, e eu registrei o formato errado em
        # `docs/fontes/pesquisa-bases-e-apis-2026-09.md`. Achado A-02.
        # Mais de um elemento e informacao, nao erro: a mesma emissora pode ter mais de
        # um registro. Guardamos todos e usamos o primeiro, dizendo quantos vieram.
        n_registros = 1
        if isinstance(dados, list):
            so_dicts = [x for x in dados if isinstance(x, dict)]
            if so_dicts:
                n_registros = len(so_dicts)
                dados = so_dicts[0]
        if not isinstance(dados, dict):
            destino = os.path.join(raiz, "eventos", "dt_captura=" + dia,
                                   emissora + ".RESPOSTA-NAO-E-OBJETO.json")
            gravar(destino, texto, forcar)
            fora_do_formato.append((emissora, type(dados).__name__, repr(dados)[:70]))
            print("  %3d/%d  %-5s  RESPOSTA NAO E OBJETO (%s) -- gravada para conferencia"
                  % (i, len(emissoras), emissora, type(dados).__name__))
            time.sleep(PAUSA_S)
            continue

        n_cash = len(dados.get("cashDividends") or [])
        n_stock = len(dados.get("stockDividends") or [])
        n_subs = len(dados.get("subscriptions") or [])

        # A ARMADILHA CENTRAL DESTE ENDPOINT, e ela e silenciosa: chave errada devolve
        # objeto valido com listas vazias e HTTP 200. Gravar isso como "sem eventos"
        # e escrever ausencia de dado no lugar de dado -- o achado F-02 na veia. Aqui
        # a resposta vazia e GRAVADA (ela e evidencia) mas ACUSADA em voz alta no fim.
        if not dados.get("tradingName"):
            vazias.append(emissora)

        # ACHADO A-03, 11/09/2026. MBRF voltou com tradingName "MARFRIG", codeCVM 20788,
        # e as TRES listas vazias. Nao e falha de rede nem chave errada -- e que o codigo
        # de emissora MUDOU (MRFG -> MBRF, na fusao com a BRF) e a historia de eventos
        # NAO VEM JUNTO: ela ficou sob o codigo antigo.
        #
        # Zero em uma lista e comum e legitimo (empresa que nunca desdobrou). Zero nas
        # TRES, numa empresa do IBOV, e quase sempre troca de codigo -- e tratar isso
        # como "empresa sem eventos" poe uma serie de precos sem ajuste no backtest.
        # Silencio aqui custa mais que erro.
        if n_cash == 0 and n_stock == 0 and n_subs == 0:
            sem_evento_nenhum.append((emissora, (dados.get("tradingName") or "").strip()))

        destino = os.path.join(raiz, "eventos", "dt_captura=" + dia, emissora + ".json")
        ok, nota = gravar(destino, texto, forcar)
        gravadas += 1 if ok else 0
        anotar_manifesto(raiz, {
            "capturado_em": agora_iso(), "tipo": "eventos_societarios",
            "emissora": emissora,
            "trading_name": (dados.get("tradingName") or "").strip(),
            "code_cvm": dados.get("codeCVM"), "url": url, "arquivo": destino,
            "sha256": sha256(texto), "bytes": len(texto.encode("utf-8")),
            "cash_dividends": n_cash, "stock_dividends": n_stock, "subscriptions": n_subs,
            "registros_na_resposta": n_registros,
            "gravado": ok, "nota": nota,
        })
        print("  %3d/%d  %-5s  %-28s cash=%-4d stock=%-3d subs=%-3d  %s" % (
            i, len(emissoras), emissora, (dados.get("tradingName") or "?")[:28],
            n_cash, n_stock, n_subs, nota))
        time.sleep(PAUSA_S)

    print("\n%d emissoras, %d arquivos novos." % (len(emissoras), gravadas))
    if vazias:
        print("SEM tradingName (chave provavelmente errada, CONFERIR): " + ", ".join(vazias))
    if sem_evento_nenhum:
        print("\nZERO EVENTOS NAS TRES LISTAS em %d emissora(s) -- A-03, provavel TROCA DE\n"
              "CODIGO. A historia fica sob o codigo ANTIGO e nao acompanha o novo:"
              % len(sem_evento_nenhum))
        for em, nome in sem_evento_nenhum:
            print("  %-5s  %s" % (em, nome))
        print("Serie de precos sem ajuste e serie inutil. Ache o codigo anterior e colete\n"
              "por ele tambem, ou declare a lacuna.")
    print("\nCONFIRA A COLUNA DO NOME antes de confiar no acervo. O endpoint casa por\n"
          "aproximacao e devolve 200 para codigo errado -- foi assim que B3SA3 virou\n"
          "'BSA' e trouxe outra empresa. Nome que nao bate com o ticker e dado do ativo\n"
          "errado, nao dado ausente.")
    if erros:
        print("ERRO DE REDE em %d: %s" % (len(erros), ", ".join(e for e, _ in erros)))
    if fora_do_formato:
        print("\nRESPOSTA FORA DO FORMATO em %d emissora(s) -- o bruto foi gravado como\n"
              "  <EMISSORA>.RESPOSTA-NAO-E-OBJETO.json para conferencia:" % len(fora_do_formato))
        for em, tipo, amostra in fora_do_formato:
            print("  %-5s  %-5s  %s" % (em, tipo, amostra))
        print("Isto NAO e o mesmo que 'empresa sem eventos'. Nao trate como ausencia de\n"
              "dado ate saber o que a B3 respondeu.")
    return 1 if (vazias or erros or fora_do_formato or sem_evento_nenhum) else 0


# ------------------------------------------------- proventos: o historico longo
#
# O suplemento devolve uma JANELA recente (24 proventos da PETR em 11/09); o historico
# desde 2010 (343, segundo a pesquisa) vem de GetListedCashDividends, paginado. A chave
# e o `tradingName` -- TEXTO, nao o codigo de 4 letras -- e ele sai do acervo de eventos
# que JA existe. Montar a partir do ticker seria o A-01 outra vez.
#
# FORMATO: suposto a partir do GetPortfolioDay (mesmo proxy) e CONFIRMADO na primeira
# corrida, 11/09/2026 -- 71 de 74 emissoras fecharam a conta no envelope page/results.
# A guarda continua: resposta sem `page.totalRecords` e gravada e ACUSADA (A-02).
#
# B-02, a mesma corrida: as 3 que faltaram (ABEV, CURY, KLBN) deram totalRecords 0, e
# NAO por truncamento -- 'AMBEV S/A' tem 9 caracteres. O suplemento guarda o nome COM o
# sufixo societario e a tabela de proventos SEM: 'AMBEV S/A' -> 0, 'AMBEV' -> 134. Com
# ponto ('SUZANO S.A.') passa como veio. O match e EXATO ('ITAU' -> 0): nao ha acerto
# parcial silencioso -- ou o nome bate e vem tudo, ou vem zero, e zero e visivel.
#
# B-03, a recoleta: ABEV e KLBN fecharam sem o sufixo; CURY falhou nas duas formas.
# 'CURY S.A.' -> 20: la o sufixo nao SOME, e REESCRITO (barra vira ponto). As duas bases
# divergem SEM REGRA, entao nenhuma normalizacao deterministica cobre as tres -- por isso
# a correcao do B-02, certa para duas, deixou uma de fora. Agora e uma CASCATA, e a
# trilha inteira vai para o manifesto.
#
# `desembrulhar` repete a normalizacao inline de `coletar_eventos`. Unificar exigiria
# tocar o caminho --eventos, que funciona e cujo acervo nao se recupera; a duplicacao
# esta registrada em PENDENCIAS.md.

class PaginacaoInvalida(Exception):
    """A paginacao nao se sustenta. Nada e gravado como se estivesse completo.
    `tipo`: TOTAL-ZERO, FORA-DO-FORMATO, LACO ou INCOMPLETO. `bruto`: a resposta que
    provou o defeito, quando ha uma -- e evidencia, e vai para o acervo com o tipo."""

    def __init__(self, motivo, tipo, bruto=None):
        super().__init__(motivo)
        self.tipo, self.bruto = tipo, bruto
        self.tentativas, self.brutos = [], []    # preenchidos por proventos_de (B-02)


def desembrulhar(texto):
    """O acervo real vem duplamente codificado (A-00) e em lista (A-02)."""
    dados = json.loads(texto)
    if isinstance(dados, str):
        try:
            dados = json.loads(dados)
        except json.JSONDecodeError:
            return dados
    if isinstance(dados, list):
        so_dicts = [x for x in dados if isinstance(x, dict)]
        if so_dicts:
            return so_dicts[0]
    return dados


def trading_names(raiz, dia=None):
    """(dia_usado, {emissora: tradingName}, [emissoras sem nome]) a partir do acervo de
    eventos -- da captura `dia`, ou da mais recente.

    O campo vem PREENCHIDO a 12 posicoes ('PETROBRAS   '), e o unico pedido observado
    funcionando usou 'PETROBRAS'. O espaco a direita sai; nada mais e mexido."""
    base = os.path.join(raiz, "eventos")
    if not os.path.isdir(base):
        return None, {}, []
    dias = sorted(d for d in os.listdir(base) if d.startswith("dt_captura="))
    if dia:
        dias = [d for d in dias if d == "dt_captura=" + dia]
    if not dias:
        return None, {}, []
    pasta = os.path.join(base, dias[-1])
    nomes, sem_nome = {}, []
    for arq in sorted(os.listdir(pasta)):
        if not arq.endswith(".json") or "NAO-E-OBJETO" in arq:
            continue
        with open(os.path.join(pasta, arq), encoding="utf-8") as f:
            d = desembrulhar(f.read())
        nome = (d.get("tradingName") or "").strip() if isinstance(d, dict) else ""
        if nome:
            nomes[arq[:-len(".json")]] = nome
        else:
            sem_nome.append(arq[:-len(".json")])
    return dias[-1][len("dt_captura="):], nomes, sem_nome


def paginar(trading_name, buscar_fn=None, pausa=PAUSA_S, tamanho=TAMANHO_PAGINA,
            max_paginas=MAX_PAGINAS):
    """Percorre as paginas ate o fim. Devolve (paginas, total), com `paginas` uma lista
    de (url, texto BRUTO, registros). Levanta PaginacaoInvalida em vez de devolver meio
    historico com cara de historico inteiro.

    Laco sobre endpoint sem contrato tem tres jeitos de mentir, e cada um tem trava:
      fim declarado    para em `page.totalPages`, ou no teto de totalRecords/tamanho;
      pagina repetida  o mesmo conteudo duas vezes e servidor ignorando pageNumber;
      teto duro        `max_paginas`, mesmo que o servidor diga que ha mais."""
    buscar_fn = buscar_fn or buscar
    paginas, vistas, total, n = [], set(), None, 1
    while True:
        if n > max_paginas:
            raise PaginacaoInvalida("passou de %d paginas sem chegar ao fim" % max_paginas,
                                    "LACO")
        url = URL_PROVENTOS.format(p=carga({"language": "pt-br", "pageNumber": n,
                                             "pageSize": tamanho, "tradingName": trading_name}))
        texto, _ = buscar_fn(url)
        d = desembrulhar(texto)
        pagina = d.get("page") if isinstance(d, dict) else None
        if not isinstance(pagina, dict) or "totalRecords" not in pagina \
           or not isinstance(d.get("results"), list):
            raise PaginacaoInvalida("pagina %d fora do envelope page/results" % n,
                                    "FORA-DO-FORMATO", texto)
        if total is None:
            total = pagina["totalRecords"]
        elif pagina["totalRecords"] != total:
            raise PaginacaoInvalida("totalRecords mudou no meio: %s -> %s"
                                    % (total, pagina["totalRecords"]), "INCOMPLETO", texto)
        if total == 0:
            # A armadilha que a pesquisa observou: tradingName errado devolve 0 com HTTP
            # 200. Gravar isso como "empresa sem proventos" e o F-02 -- ausencia de dado
            # virando dado. E o A-01 num campo novo.
            raise PaginacaoInvalida("totalRecords 0 -- quase sempre tradingName que o "
                                    "endpoint nao reconhece", "TOTAL-ZERO", texto)
        assinatura = sha256(json.dumps(d["results"], sort_keys=True))
        if assinatura in vistas:
            raise PaginacaoInvalida("pagina %d repete uma anterior -- o servidor ignora "
                                    "pageNumber" % n, "LACO", texto)
        vistas.add(assinatura)
        paginas.append((url, texto, len(d["results"])))
        if n >= (pagina.get("totalPages") or -(-total // tamanho)):
            break
        if not d["results"]:
            raise PaginacaoInvalida("pagina %d veio vazia antes do fim declarado" % n,
                                    "INCOMPLETO", texto)
        n += 1
        time.sleep(pausa)
    obtidos = sum(k for _, _, k in paginas)
    if obtidos != total:
        raise PaginacaoInvalida("vieram %d de %d registros declarados" % (obtidos, total),
                                "INCOMPLETO")
    return paginas, total


SUFIXOS_SOCIETARIOS = (" S/A.", " S/A", " S.A.", " SA")


def candidatos(nome):
    """[(tradingName, forma)] na ordem da cascata (B-03): como veio, sem sufixo, sufixo
    com pontos, sufixo sem pontuacao. Texto repetido nao vira segunda tentativa, e base
    vazia nao vira candidato.

    Nome SEM sufixo societario so tem a primeira forma: 71 de 74 fecharam como vieram,
    e a divergencia medida entre as bases e sempre no sufixo -- some (ABEV, KLBN) ou e
    reescrito (CURY). Inventar um sufixo onde o suplemento nao tem nenhum seria outra
    hipotese, sem medicao."""
    cascata = [(nome, "COMO_VEIO")]
    base = next((nome[:-len(s)].rstrip() for s in SUFIXOS_SOCIETARIOS
                 if nome.upper().endswith(s)), "")
    if base:
        for tn, forma in ((base, "SEM_SUFIXO"), (base + " S.A.", "SUFIXO_COM_PONTOS"),
                          (base + " SA", "SUFIXO_SEM_PONTUACAO")):
            if tn not in {t for t, _ in cascata}:
                cascata.append((tn, forma))
    return cascata


def proventos_de(nome, buscar_fn=None, pausa=PAUSA_S):
    """Percorre `candidatos(nome)` e para no primeiro que responder. SO TOTAL-ZERO abre a
    proxima forma: FORA-DO-FORMATO, LACO e INCOMPLETO param na hora -- nao e o nome que
    esta errado, e trocar o nome mascararia o defeito real.

    Devolve (paginas, total, nome_usado, forma, tentativas). A trilha inteira -- a forma
    que funcionou E as que falharam antes -- e PROCEDENCIA: vai para o manifesto, porque
    quem reprocessar precisa saber que texto a B3 aceitou e quais recusou. Se toda a
    cascata der zero, sobe TOTAL-ZERO com todas as respostas em `brutos`."""
    cascata, tentativas, brutos = candidatos(nome), [], []
    for k, (tn, forma) in enumerate(cascata):
        if k:
            time.sleep(pausa)
        try:
            paginas, total = paginar(tn, buscar_fn, pausa)
        except PaginacaoInvalida as e:
            tentativas.append({"trading_name": tn, "forma": forma, "resultado": e.tipo})
            if e.bruto is not None:
                brutos.append((forma, e.tipo, e.bruto))
            if e.tipo != "TOTAL-ZERO" or k == len(cascata) - 1:
                e.tentativas, e.brutos = tentativas, brutos
                raise
            continue
        tentativas.append({"trading_name": tn, "forma": forma, "resultado": "COMPLETO",
                           "registros": total})
        return paginas, total, tn, forma, tentativas


def coletar_proventos(raiz, dia, emissoras=None, de_captura=None, buscar_fn=None,
                      pausa=PAUSA_S):
    """Uma pasta por emissora, uma pagina bruta por arquivo, em
    `proventos/dt_captura=DIA/EMISSORA/pagina-NNN.json`. So se grava historico que
    FECHOU a conta com o totalRecords; o resto vira evidencia `EMISSORA.TIPO.json`."""
    usado, nomes, sem_nome = trading_names(raiz, de_captura)
    if not nomes:
        print("Nao ha acervo de eventos com tradingName em %s. Rode antes:\n"
              "    python coletar_b3.py --eventos" % os.path.abspath(raiz), file=sys.stderr)
        return 2
    pedidas = sorted(set(emissoras)) if emissoras else sorted(nomes)
    fora = [e for e in pedidas if e not in nomes]
    alvos = [e for e in pedidas if e in nomes]
    print("tradingName lido do acervo de eventos dt_captura=%s (%d emissoras)\n"
          % (usado, len(nomes)))
    pasta = os.path.join(raiz, "proventos", "dt_captura=" + dia)
    falhas, completas, ja = [], 0, 0

    for i, em in enumerate(alvos, 1):
        nome, destino = nomes[em], os.path.join(pasta, em)
        if os.path.isdir(destino):
            # Sem --forcar aqui de proposito: regravar paginas por cima deixaria sobra de
            # uma coleta mais longa. Recoletar o mesmo dia e apagar a pasta a mao.
            ja += 1
            print("  %3d/%d  %-5s  ja existe -- o acervo do dia e imutavel" % (i, len(alvos), em))
            continue
        try:
            paginas, total, usado_nome, forma, tentativas = proventos_de(nome, buscar_fn, pausa)
        except PaginacaoInvalida as e:
            for forma_b, tipo_b, bruto in e.brutos:
                extra = "" if forma_b == "COMO_VEIO" else "." + forma_b.replace("_", "-")
                gravar(os.path.join(pasta, "%s.%s%s.json" % (em, tipo_b, extra)), bruto, False)
            trilha = "; ".join("%r -> %s" % (t["trading_name"], t["resultado"])
                               for t in e.tentativas) or str(e)
            falhas.append((em, nome, e.tipo, trilha))
            print("  %3d/%d  %-5s  %-14s %s: %s" % (i, len(alvos), em, nome[:14], e.tipo, trilha))
            continue
        except RuntimeError as e:
            falhas.append((em, nome, "REDE", str(e)[:120]))
            print("  %3d/%d  %-5s  ERRO DE REDE: %s" % (i, len(alvos), em, str(e)[:60]))
            continue
        shas = []
        for k, (_url, texto, _n) in enumerate(paginas, 1):
            gravar(os.path.join(destino, "pagina-%03d.json" % k), texto, False)
            shas.append(sha256(texto))
        anotar_manifesto(raiz, {
            "capturado_em": agora_iso(), "tipo": "proventos_completos", "emissora": em,
            "trading_name": usado_nome, "trading_name_do_acervo": nome,
            "forma_do_nome": forma, "tentativas": tentativas,
            "trading_name_de": "eventos/dt_captura=%s" % usado,
            "pasta": destino, "paginas": len(paginas), "total_registros": total,
            "sha256_paginas": shas, "url_primeira_pagina": paginas[0][0],
        })
        completas += 1
        nota = "" if forma == "COMO_VEIO" else "  (%s: %r)" % (forma, usado_nome)
        print("  %3d/%d  %-5s  %-14s %4d registros em %d pagina(s)%s"
              % (i, len(alvos), em, nome[:14], total, len(paginas), nota))
        time.sleep(pausa)

    print("\n%d completas, %d ja existiam, %d falharam." % (completas, ja, len(falhas)))
    if falhas:
        print("\nFALHARAM -- nada disto foi gravado como historico. A resposta que provou\n"
              "o defeito, quando havia uma, esta em <EMISSORA>.<TIPO>.json:")
        for em, nome, tipo, msg in falhas:
            print("  %-5s  %-14s %-16s %s" % (em, nome[:14], tipo, msg[:70]))
        if any(t == "TOTAL-ZERO" for _, _, t, _ in falhas):
            print("\nTOTAL-ZERO NAO e 'empresa sem proventos': e um nome que a tabela de\n"
                  "proventos nao reconhece -- o match e exato. Cada linha acima mostra as formas\n"
                  "tentadas: como veio e, havendo sufixo societario, a cascata (B-03). NAO e\n"
                  "truncamento do campo de 12 posicoes: essa hipotese foi medida e caiu.")
    if fora:
        print("\npedidas e ausentes do acervo de eventos (sem tradingName para usar): "
              + ", ".join(fora))
    if sem_nome:
        print("\nsem tradingName no acervo de eventos: " + ", ".join(sem_nome))
    return 1 if (falhas or fora or sem_nome) else 0


# ---------------------------------------------------------------------- main

def main(argv=None):
    p = argparse.ArgumentParser(description="Captura o dado perecivel da B3 (Fase 0).")
    p.add_argument("--raiz", default=RAIZ_PADRAO,
                   help="raiz do acervo (padrao: %s)" % RAIZ_PADRAO)
    p.add_argument("--indice", metavar="COD",
                   help="captura a carteira teorica (ex.: IBOV, IBXX, SMLL, IDIV)")
    p.add_argument("--eventos", action="store_true", help="captura eventos societarios")
    p.add_argument("--tickers",
                   help="lista separada por virgula; sem isso usa o ultimo snapshot de indice")
    p.add_argument("--forcar", action="store_true",
                   help="reescreve snapshot ja existente do mesmo dia")
    p.add_argument("--proventos-completos", action="store_true",
                   help="historico longo de proventos (paginado); le o tradingName do "
                        "acervo de eventos")
    p.add_argument("--de-captura", metavar="AAAA-MM-DD",
                   help="com --proventos-completos: captura de eventos de onde ler o tradingName")
    a = p.parse_args(argv)

    if a.proventos_completos:
        if a.indice or a.eventos:
            p.error("--proventos-completos roda sozinho: ele le o tradingName do acervo de "
                    "eventos que JA existe, e misturar os passos esconderia de qual captura")
        dia = hoje()
        print("acervo: %s    dt_captura=%s\n" % (os.path.abspath(a.raiz), dia))
        emissoras = ([empresa_de(t) for t in a.tickers.split(",") if t.strip()]
                     if a.tickers else None)
        return coletar_proventos(a.raiz, dia, emissoras=emissoras, de_captura=a.de_captura)

    if not a.indice and not a.eventos:
        p.error("escolha ao menos --indice ou --eventos")

    dia = hoje()
    print("acervo: %s    dt_captura=%s\n" % (os.path.abspath(a.raiz), dia))
    codigos = []

    if a.indice:
        codigos = coletar_indice(a.raiz, a.indice.upper(), dia, a.forcar)

    if not a.eventos:
        return 0

    if a.tickers:
        alvos = [t.strip() for t in a.tickers.split(",") if t.strip()]
    elif codigos:
        alvos = codigos
    else:
        de_dia, alvos = ultimo_indice(a.raiz, "IBOV")
        if not alvos:
            print("Nao ha snapshot de indice no acervo e nem --tickers foi passado.\n"
                  "Rode antes:  python coletar_b3.py --indice IBOV", file=sys.stderr)
            return 2
        print("usando a carteira IBOV capturada em %s (%d ativos)\n" % (de_dia, len(alvos)))

    print("eventos societarios de %d ativos:" % len(alvos))
    return coletar_eventos(a.raiz, alvos, dia, a.forcar)


if __name__ == "__main__":
    sys.exit(main())

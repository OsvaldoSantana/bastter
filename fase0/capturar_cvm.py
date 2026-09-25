#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Captura do acervo da CVM (DFP, ITR, CAD) -- o byte que a CVM entregou, com diario.

PROCEDENCIA DESTE MODULO. Escrito por outra IA em 24/09/2026 como `tools/baixar_cvm.py`;
auditado e corrigido em 24/09/2026 (Claude Code). As correcoes, cada uma com teste em
`fase0/test_capturar_cvm.py`, sem rede:
  2.1  sem caminho absoluto: `--raiz`, padrao `data/bronze/cvm` sob a raiz do repositorio;
  2.2  sem `requests`: stdlib (`urllib.request`), porque a dependencia nao estava declarada
       e a rotina tem de rodar num ambiente limpo (P7);
  2.3  os anos vem do INDICE da CVM, nunca de um `range` -- `range(2021, 2027)` deixaria
       de capturar 2027 sem avisar;
  2.4  "congelado" nao e imutavel: os Last-Modified de 2010-2019 dizem 05-06/08/2024
       (CV-02). O padrao e TODOS os anos, com o portao HEAD; `--escopo` e so filtro;
  2.5  integridade ANTES de aceitar (a licao do COTAHIST_A2026 truncado, P-100): bytes
       recebidos == Content-Length e, para .zip, `testzip()` is None. Se falhar, o `.part`
       sai, a versao anterior fica intacta, o registro ganha uma linha `rejeitado` e o
       comando sai 1;
  2.6  a versao deslocada vira `_snapshots/<stem>__v<AAAAMMDD>__<sha12>.<ext>`, com a data
       da VERSAO (o maior `date_time` entre os membros do ZIP, CV-03) e o sha12
       recalculado dos bytes -- nao a hora em que alguem rodou o script;
  2.7  toda observacao vira linha no registro, inclusive `inalterado` (a prova de que a
       rotina rodou), `deslocado` e `rejeitado`, com caminhos relativos a raiz do
       repositorio;
  2.8  ao fim de uma captura sem erro, roda o `manifesto_cvm.py` sobre a raiz.

MODO ARMAZEM (P-57, 24/09/2026 -- docs/decisoes/P-57.md). Com `--armazem s3` o byte nao
fica no disco: baixa para um temporario, passa pela mesma conferencia (2.5), sobe para o
armazem com a chave de conteudo `cvm/<recurso>/<arquivo>/<sha256>.<ext>` e registra. Toda
versao tem endereco proprio, entao nao ha `_snapshots/` nem linha `deslocado`. O disco
local vira opcional (`--cache`). E o registro se parte em dois:
  - `docs/acervo/cvm/capturas.csv` (git) recebe o que MUDA o estado: novo, atualizado,
    rejeitado, erro -- e o `inalterado` por "hash coincide", que traz um Last-Modified
    novo. Sem ele o portao HEAD compararia sempre com o Last-Modified velho e baixaria o
    mesmo arquivo todo dia, para sempre;
  - `logs/capturas/<AAAA-MM-DD>.csv` (armazem) recebe a rodada INTEIRA, inalterados
    inclusive. E a prova de que a rotina rodou -- com captura diaria, no git seriam 365
    commits de ruido por ano. Uma segunda rodada no mesmo dia nao sobrescreve a primeira:
    vira `<AAAA-MM-DD>__<HHMMSS>Z.csv`.

DOIS PAPEIS, E NAO SE MISTURAM (N-01). O REGISTRO (`docs/acervo/<acervo>/capturas.csv`,
versionado) e o diario do HTTP: URL, Last-Modified, ETag, bytes, e o sha256 dos bytes
RECEBIDOS. So metadado -- nenhum byte da CVM entra no git. O MANIFESTO (`manifesto_cvm.py`)
e o retrato do disco, com o sha256 de cada arquivo. Por isso a linha `inalterado` que sai
do portao HEAD vem com `sha256` VAZIO: nada foi recebido, e recalcular o hash do disco aqui
seria duplicar o manifesto.

O ESTADO (`<raiz>/_manifest/estado.json`) e CACHE, derivavel do registro: se ele sumir,
`estado_do_registro()` o reconstroi, e o proximo portao HEAD funciona igual. Ele fica em
`data/` porque nao prova nada que o registro nao prove.

O QUE ELE NAO FAZ (P5):
  - nao compara CONTEUDO: um sha256 diferente pode ser so a CVM regerando o arquivo com
    as linhas em outra ordem (o achado do `manifesto_cvm.py`, 18/09). Ele guarda a versao
    deslocada; dizer se houve reapresentacao e o `manifesto_cvm.py --comparar`;
  - nao recupera versao que ninguem capturou: a CVM so serve a atual (CV-01, FISICA).

USO
  python fase0/capturar_cvm.py                      # todos os anos do indice + cad
  python fase0/capturar_cvm.py --dry-run            # o que baixaria; nao grava nada
  python fase0/capturar_cvm.py --escopo recentes    # so filtro
  python fase0/capturar_cvm.py --arrumar            # plano de arrumacao do acervo
  python fase0/capturar_cvm.py --arrumar --aplicar
  python fase0/capturar_cvm.py --armazem s3         # nuvem: credenciais R2_* no ambiente
  python fase0/capturar_cvm.py --armazem s3 --cache data/armazem
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
from http.client import IncompleteRead
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
import zlib
from urllib.parse import urljoin

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
try:
    import manifesto_cvm
except ImportError as e:                                     # pragma: no cover
    raise ImportError("capturar_cvm precisa de fase0/manifesto_cvm.py: a raiz do "
                      "repositorio e o retrato do disco moram la (N-01)") from e
import armazem as armazem_mod  # noqa: E402

INDICES = {
    "dfp": "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/",
    "itr": "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/",
    # P-132, 25/09: o FCA traz a ponte `CD_CVM` <-> codigo de negociacao
    # (`valor_mobiliario`). Sem ela o universo da secao 2 do pre-registro ML nao se
    # monta: o COTAHIST fala ticker, o DFP/ITR fala CD_CVM. ~0,4 MB por ano.
    "fca": "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FCA/DADOS/",
}
CAD_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"
# "Os arquivos serao atualizados semanalmente ... os ultimos cinco anos"
# (docs/fontes/cvm-dfp-politica-atualizacao.md). So define o FILTRO `recentes`; a rotina
# padrao captura todos (2.4).
ANOS_NA_JANELA = 5
RAIZ_RELATIVA = os.path.join("data", "bronze", "cvm")
SNAPSHOTS = "_snapshots"
DESCONHECIDA = "DESCONHECIDA"
FONTE = "cvm"
LOGS = "logs/capturas"
RETENTAVEIS = (429, 500, 502, 503, 504)

COLUNAS = ("dt_captura", "recurso", "arquivo", "url", "http_last_modified", "etag",
           "sha256", "bytes", "caminho", "situacao", "motivo")
NOVO, ATUALIZADO, INALTERADO = "novo", "atualizado", "inalterado"
DESLOCADO, REJEITADO, ERRO = "deslocado", "rejeitado", "erro"
# o envio levaria o bucket acima de politica.yaml -> armazem.teto_gb: nada subiu, e o
# estado nao avanca -- a proxima rodada tenta de novo (P-57, cobranca zero)
RECUSADO_POR_TETO = "recusado_por_teto"


class Rejeitado(Exception):
    """O download chegou, e nao e o arquivo inteiro. A versao anterior fica."""


# ── caminhos ──────────────────────────────────────────────────────────────────

def raiz_repo():
    return manifesto_cvm.raiz_do_repositorio(AQUI)


def raiz_padrao():
    base = raiz_repo()
    if base is None:
        raise SystemExit("sem pyproject.toml acima de fase0/: passe --raiz explicitamente")
    return os.path.join(base, RAIZ_RELATIVA)


def registro_padrao(raiz):
    """Ao lado do manifesto: `docs/acervo/<acervo>/capturas.csv`. Fora de `data/`, que o
    .gitignore ignora -- o mesmo defeito que o `manifesto_cvm.destino_padrao` ja pagou."""
    return os.path.join(os.path.dirname(manifesto_cvm.destino_padrao(raiz, "x")),
                        "capturas.csv")


def relativo(caminho, raiz):
    """Relativo a raiz do repositorio; sem repositorio, a pasta acima da raiz do acervo."""
    base = manifesto_cvm.raiz_do_repositorio(raiz) or os.path.dirname(os.path.abspath(raiz))
    return os.path.relpath(os.path.abspath(caminho), base).replace("\\", "/")


def agora():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── HTTP ──────────────────────────────────────────────────────────────────────

def requisitar(url, abrir=urllib.request.urlopen, dormir=time.sleep, metodo="GET",
               cabecalhos=None, tentativas=5, timeout=60):
    """Uma requisicao com retentativa simples em 429/5xx e em falha de conexao.

    `Accept-Encoding: identity`: o hash tem de ser do byte que a CVM entregou, nao de uma
    descompressao de transporte. `abrir` e `dormir` sao injetaveis para o teste rodar sem
    rede e sem relogio."""
    h = {"User-Agent": "meol-captura-cvm/2", "Accept-Encoding": "identity"}
    h.update(cabecalhos or {})
    for i in range(tentativas):
        try:
            return abrir(urllib.request.Request(url, method=metodo, headers=h),
                         timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code not in RETENTAVEIS or i == tentativas - 1:
                raise
        except urllib.error.URLError:
            if i == tentativas - 1:
                raise
        dormir(1.5 * 2 ** i)
    raise AssertionError("inalcancavel")                        # pragma: no cover


HREF = re.compile(r'href="([^"]+\.zip)"', re.IGNORECASE)


def anos_do_indice(url_indice, recurso, abrir=urllib.request.urlopen, dormir=time.sleep):
    """{ano: url} lido do indice da CVM. Nenhum ano sai de constante (2.3)."""
    with requisitar(url_indice, abrir, dormir) as r:
        html = r.read().decode("utf-8", "replace")
    padrao = re.compile(rf"{recurso}_cia_aberta_(\d{{4}})\.zip$", re.IGNORECASE)
    out = {}
    for href in HREF.findall(html):
        u = urljoin(url_indice, href)
        m = padrao.search(u)
        if m:
            out[int(m.group(1))] = u
    return out


def alvos(escopos=None, abrir=urllib.request.urlopen, dormir=time.sleep):
    """[(url, recurso)] em ordem estavel. Sem `escopos`, e TUDO (2.4)."""
    escopos = set(escopos or ("recentes", "congelados", "cad"))
    out = []
    for recurso, indice in INDICES.items():
        anos = anos_do_indice(indice, recurso, abrir, dormir)
        if not anos:
            # indice vazio NAO e "nada a capturar" -- e indice que mudou de forma
            raise RuntimeError(f"indice {indice} sem nenhum {recurso}_cia_aberta_AAAA.zip")
        corte = max(anos) - ANOS_NA_JANELA + 1
        for ano in sorted(anos):
            if ("recentes" if ano >= corte else "congelados") in escopos:
                out.append((anos[ano], recurso))
    if "cad" in escopos:
        out.append((CAD_URL, "cad"))
    return out


def metadados(url, abrir=urllib.request.urlopen, dormir=time.sleep):
    """Last-Modified, ETag e tamanho, por HEAD. Servidor que recusa HEAD: GET de 1 byte, e
    o tamanho vem do `Content-Range` -- o `Content-Length` de uma faixa e 1, e o portao
    compararia o arquivo inteiro com 1 byte para sempre."""
    try:
        with requisitar(url, abrir, dormir, metodo="HEAD") as r:
            tam = r.headers.get("Content-Length")
            return dict(tamanho=int(tam) if tam else None,
                        last_modified=r.headers.get("Last-Modified") or "",
                        etag=r.headers.get("ETag") or "")
    except urllib.error.HTTPError as e:
        if e.code not in (403, 405, 501):
            raise
    with requisitar(url, abrir, dormir, cabecalhos={"Range": "bytes=0-0"}) as r:
        faixa = r.headers.get("Content-Range") or ""
        m = re.search(r"/(\d+)$", faixa)
        return dict(tamanho=int(m.group(1)) if m else None,
                    last_modified=r.headers.get("Last-Modified") or "",
                    etag=r.headers.get("ETag") or "")


# ── integridade e versao ──────────────────────────────────────────────────────

def sha256(caminho):
    return manifesto_cvm.sha256(caminho)


def conferir_zip(caminho):
    """None se o ZIP le inteiro; o motivo, se nao."""
    try:
        with zipfile.ZipFile(caminho) as z:
            ruim = z.testzip()
    except (zipfile.BadZipFile, OSError, EOFError) as e:
        return f"zip ilegivel: {e}"
    return None if ruim is None else f"zip com membro corrompido: {ruim}"


def data_da_versao(caminho, last_modified=""):
    """AAAAMMDD da VERSAO do arquivo (2.6, CV-03).

    ZIP: o maior `date_time` entre os membros -- e a CVM quem escreve, na hora em que gera.
    Medido em 24/09 nos 34 canonicos: ele fica 3 h exatas antes do Last-Modified em GMT
    (dfp 2012: membro 05/08/2024 17:48, cabecalho 20:48:19 GMT), isto e, e horario de
    Brasilia sem fuso declarado. CSV solto (o cad): o Last-Modified registrado, EM GMT --
    as duas convencoes diferem por 3 h e a data pode virar perto da meia-noite (CV-03).
    Sem nenhum dos dois, DESCONHECIDA -- nunca a data de hoje, que seria a hora da
    captura com cara de versao."""
    if caminho.lower().endswith(".zip"):
        with zipfile.ZipFile(caminho) as z:
            datas = [i.date_time for i in z.infolist()]
        if datas:
            return "%04d%02d%02d" % max(datas)[:3]
        return DESCONHECIDA
    if last_modified:
        try:
            return dt.datetime.strptime(last_modified,
                                        "%a, %d %b %Y %H:%M:%S GMT").strftime("%Y%m%d")
        except ValueError:
            pass
    return DESCONHECIDA


def nome_do_snapshot(caminho, last_modified=""):
    """`<stem>__v<AAAAMMDD>__<sha12>.<ext>`, com o sha12 RECALCULADO dos bytes: o nome nao
    pode herdar o hash de um estado que pode estar errado."""
    base = os.path.basename(caminho)
    stem, ext = os.path.splitext(base)
    stem = re.sub(r"\s*\(\d+\)$", "", stem)                 # copia do navegador
    stem = re.sub(r"__\d{8}T\d{6}Z__[0-9a-f?]{12}$", "", stem)  # snapshot com a hora
    return f"{stem}__v{data_da_versao(caminho, last_modified)}__{sha256(caminho)[:12]}{ext}"


# ── registro e estado ─────────────────────────────────────────────────────────

def ler_registro(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def anotar(caminho, linha):
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    novo = not os.path.exists(caminho)
    with open(caminho, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, delimiter=";")
        if novo:
            w.writeheader()
        w.writerow({c: linha.get(c, "") for c in COLUNAS})


def estado_do_registro(linhas):
    """O estado e cache: reconstruido daqui, ele da o mesmo portao. Vale a ultima linha
    de cada arquivo canonico que descreve a versao que ficou no lugar."""
    estado = {}
    for ln in linhas:
        if ln["situacao"] not in (NOVO, ATUALIZADO, INALTERADO):
            continue
        anterior = estado.get(ln["caminho"], {})
        estado[ln["caminho"]] = dict(
            sha256=ln["sha256"] or anterior.get("sha256", ""),
            bytes=int(ln["bytes"]) if ln["bytes"] else anterior.get("bytes"),
            last_modified=ln["http_last_modified"],
            etag=ln["etag"])
    return estado


def carregar_estado(raiz, registro):
    p = os.path.join(raiz, "_manifest", "estado.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return estado_do_registro(ler_registro(registro))


def salvar_estado(raiz, estado):
    p = os.path.join(raiz, "_manifest", "estado.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False, sort_keys=True)


# ── captura ───────────────────────────────────────────────────────────────────

def baixar(url, destino_part, abrir, dormir):
    """Grava em `.part` e devolve (sha256, bytes, last_modified, etag). Levanta
    `Rejeitado` se o recebido nao for o arquivo inteiro (2.5)."""
    h, n = hashlib.sha256(), 0
    with requisitar(url, abrir, dormir, timeout=300) as r:
        esperado = r.headers.get("Content-Length")
        lm, etag = r.headers.get("Last-Modified") or "", r.headers.get("ETag") or ""
        with open(destino_part, "wb") as f:
            try:
                for bloco in iter(lambda: r.read(1 << 20), b""):
                    f.write(bloco)
                    h.update(bloco)
                    n += len(bloco)
            except IncompleteRead as e:
                raise Rejeitado(f"conexao cortada apos {n + len(e.partial):,} bytes") from e
    if not esperado:
        raise Rejeitado("resposta sem Content-Length: nao ha contra o que conferir")
    if n != int(esperado):
        raise Rejeitado(f"recebidos {n:,} bytes, Content-Length {int(esperado):,}")
    if destino_part.lower().endswith(".zip.part"):   # ZipFile le o conteudo, nao o nome
        motivo = conferir_zip(destino_part)
        if motivo:
            raise Rejeitado(motivo)
    return h.hexdigest(), n, lm, etag


def portao_fechado(anterior, meta, forcar=False):
    """O portao HEAD: mesmo Last-Modified e mesmo tamanho que a ultima versao aceita. Uma
    funcao, dois modos (disco e armazem) -- duas copias desta condicao concordariam por
    acidente ate o dia em que uma mudasse (A-07)."""
    return bool(not forcar and anterior and meta["last_modified"]
                and anterior.get("last_modified") == meta["last_modified"]
                and anterior.get("bytes") == meta["tamanho"])


def capturar(url, recurso, raiz, registro, estado, *, abrir=urllib.request.urlopen,
             dormir=time.sleep, dry_run=False, forcar=False, saida=print):
    """Uma URL, um desfecho. Devolve a situacao."""
    nome = url.rsplit("/", 1)[-1]
    pasta = os.path.join(raiz, recurso)
    destino = os.path.join(pasta, nome)
    rel = relativo(destino, raiz)
    anterior = estado.get(rel)
    if anterior is None and os.path.exists(destino):
        # arquivo no disco sem historico: adotado pelo hash, sem Last-Modified conhecido
        anterior = dict(sha256=sha256(destino), bytes=os.path.getsize(destino),
                        last_modified="", etag="")
    meta = metadados(url, abrir, dormir)
    base = dict(recurso=recurso, arquivo=nome, url=url,
                http_last_modified=meta["last_modified"], etag=meta["etag"], caminho=rel)

    if portao_fechado(anterior, meta, forcar):
        if dry_run:
            saida(f"[=] {rel}  inalterado")
            return INALTERADO
        anotar(registro, dict(base, dt_captura=agora(), bytes=meta["tamanho"],
                              situacao=INALTERADO, motivo="portao HEAD"))
        saida(f"[=] {rel}  inalterado (LM={meta['last_modified']})")
        return INALTERADO

    if dry_run:
        saida(f"[~] {rel}  baixaria (LM={meta['last_modified']}, {meta['tamanho']} bytes)")
        return "dry"

    os.makedirs(pasta, exist_ok=True)
    part = destino + ".part"
    try:
        digest, n, lm, etag = baixar(url, part, abrir, dormir)
    except Rejeitado as e:
        if os.path.exists(part):
            os.remove(part)
        anotar(registro, dict(base, dt_captura=agora(), situacao=REJEITADO, motivo=str(e)))
        saida(f"[!] {rel}  REJEITADO: {e} -- a versao anterior ficou intacta")
        return REJEITADO
    base.update(http_last_modified=lm or meta["last_modified"], etag=etag or meta["etag"])

    if anterior and anterior.get("sha256") == digest:
        os.remove(part)
        estado[rel] = dict(sha256=digest, bytes=n, last_modified=base["http_last_modified"],
                           etag=base["etag"])
        anotar(registro, dict(base, dt_captura=agora(), sha256=digest, bytes=n,
                              situacao=INALTERADO, motivo="hash coincide"))
        saida(f"[=] {rel}  inalterado (hash coincide)")
        return INALTERADO

    if os.path.exists(destino):
        snap = deslocar(destino, (anterior or {}).get("last_modified", ""))
        anotar(registro, dict(base, dt_captura=agora(),
                              http_last_modified=(anterior or {}).get("last_modified", ""),
                              etag=(anterior or {}).get("etag", ""),
                              sha256=snap["sha256"], bytes=snap["bytes"],
                              caminho=relativo(snap["caminho"], raiz), situacao=DESLOCADO,
                              motivo=snap["motivo"]))
        saida(f"[>] {rel}  versao anterior em {os.path.basename(snap['caminho'])}")
    os.replace(part, destino)
    situacao = NOVO if anterior is None else ATUALIZADO
    estado[rel] = dict(sha256=digest, bytes=n, last_modified=base["http_last_modified"],
                       etag=base["etag"])
    anotar(registro, dict(base, dt_captura=agora(), sha256=digest, bytes=n,
                          situacao=situacao))
    saida(f"[+] {rel}  {n:,} bytes  sha256={digest[:12]}")
    return situacao


def deslocar(caminho, last_modified=""):
    """Move a versao atual para `_snapshots/` com o nome da versao (2.6). Se o snapshot
    de mesmo nome ja existe, e o mesmo byte (o sha12 esta no nome e foi recalculado): a
    copia sai e o snapshot fica."""
    snaps = os.path.join(os.path.dirname(caminho), SNAPSHOTS)
    os.makedirs(snaps, exist_ok=True)
    alvo = os.path.join(snaps, nome_do_snapshot(caminho, last_modified))
    digest, n = sha256(caminho), os.path.getsize(caminho)
    if os.path.exists(alvo) and sha256(alvo) == digest:
        os.remove(caminho)
        motivo = "versao ja guardada"
    else:
        os.replace(caminho, alvo)
        motivo = ""
    return dict(caminho=alvo, sha256=digest, bytes=n, motivo=motivo)


# ── modo armazem (P-57) ───────────────────────────────────────────────────────

def capturar_para_armazem(url, recurso, raiz, registro, estado, armazem, *,
                          abrir=urllib.request.urlopen, dormir=time.sleep, forcar=False,
                          cache=None, diario=None, saida=print, fonte=FONTE):
    """Uma URL, um desfecho, sem disco permanente. Devolve a situacao.

    `diario` recebe TODA linha da rodada (vai para o log do armazem); o registro recebe
    so as que mudam o estado. `caminho` continua sendo o caminho logico do arquivo
    canonico, o mesmo do modo disco: e por ele que `estado_do_registro` acha a versao
    anterior, e os dois modos compartilham o portao."""
    diario = [] if diario is None else diario
    nome = url.rsplit("/", 1)[-1]
    rel = relativo(os.path.join(raiz, recurso, nome), raiz)
    anterior = estado.get(rel)
    meta = metadados(url, abrir, dormir)
    base = dict(recurso=recurso, arquivo=nome, url=url,
                http_last_modified=meta["last_modified"], etag=meta["etag"], caminho=rel)

    def nota(linha, no_registro=True):
        diario.append({c: linha.get(c, "") for c in COLUNAS})
        if no_registro:
            anotar(registro, linha)

    if portao_fechado(anterior, meta, forcar):
        nota(dict(base, dt_captura=agora(), bytes=meta["tamanho"], situacao=INALTERADO,
                  motivo="portao HEAD"), no_registro=False)
        saida(f"[=] {rel}  inalterado (LM={meta['last_modified']})")
        return INALTERADO

    with tempfile.TemporaryDirectory(prefix="captura_cvm_") as tmp:
        part = os.path.join(tmp, nome + ".part")
        try:
            digest, n, lm, etag = baixar(url, part, abrir, dormir)
        except Rejeitado as e:
            nota(dict(base, dt_captura=agora(), situacao=REJEITADO, motivo=str(e)))
            saida(f"[!] {rel}  REJEITADO: {e} -- a versao anterior ficou intacta")
            return REJEITADO
        base.update(http_last_modified=lm or meta["last_modified"], etag=etag or meta["etag"])
        k = armazem_mod.chave(fonte, recurso, nome, digest)
        # a versao vigente tem de estar no armazem mesmo quando o byte nao mudou: antes da
        # carga inicial (subir_acervo_local.py) ela so existia no disco dele
        try:
            enviado = armazem.enviar_se_ausente(k, part)
        except armazem_mod.TetoExcedido as e:
            nota(dict(base, dt_captura=agora(), sha256=digest, bytes=n,
                      situacao=RECUSADO_POR_TETO, motivo=str(e)))
            saida(f"[!] {rel}  RECUSADO POR TETO: {e}")
            return RECUSADO_POR_TETO
        if cache:
            armazem_mod.copiar_para_cache(part, cache, k)
    estado[rel] = dict(sha256=digest, bytes=n, last_modified=base["http_last_modified"],
                       etag=base["etag"])
    if anterior and anterior.get("sha256") == digest:
        nota(dict(base, dt_captura=agora(), sha256=digest, bytes=n, situacao=INALTERADO,
                  motivo="hash coincide"))
        saida(f"[=] {rel}  inalterado (hash coincide, Last-Modified novo)")
        return INALTERADO
    situacao = NOVO if anterior is None else ATUALIZADO
    nota(dict(base, dt_captura=agora(), sha256=digest, bytes=n, situacao=situacao,
              motivo="" if enviado else "versao ja estava no armazem"))
    saida(f"[+] {rel}  {n:,} bytes  sha256={digest[:12]}  -> {k}")
    return situacao


def enviar_diario(armazem, diario, momento=None, prefixo=LOGS):
    """O log da rodada vai para `logs/capturas/<AAAA-MM-DD>.csv`. Se ja houver um do dia,
    `<AAAA-MM-DD>__<HHMMSS>Z.csv`, e depois `..._2`, `_3` -- o armazem nunca sobrescreve,
    e o log da primeira rodada e prova tanto quanto o da segunda. Devolve a chave usada."""
    momento = momento or dt.datetime.now(dt.timezone.utc)
    with tempfile.TemporaryDirectory(prefix="diario_cvm_") as tmp:
        p = os.path.join(tmp, "diario.csv")
        with open(p, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLUNAS, delimiter=";")
            w.writeheader()
            for ln in diario:
                w.writerow({c: ln.get(c, "") for c in COLUNAS})
        k = f"{prefixo}/{momento:%Y-%m-%d}.csv"
        n = 1
        while not armazem.enviar_se_ausente(k, p, isento_do_teto=True):
            n += 1
            sufixo = "" if n == 2 else f"_{n - 1}"
            k = f"{prefixo}/{momento:%Y-%m-%d}__{momento:%H%M%S}Z{sufixo}.csv"
        return k


# ── arrumacao do acervo (plano, depois --aplicar, como no nomear_extracoes) ──

SNAP_ANTIGO = re.compile(r"^.+__\d{8}T\d{6}Z__[0-9a-f?]{12}\.\w+$")
SNAP_NOVO = re.compile(r"^.+__v(\d{8}|" + DESCONHECIDA + r")__[0-9a-f]{12}\.\w+$")
COPIA = re.compile(r"^.+ \(\d+\)\.zip$", re.IGNORECASE)
RENOMEAR, APAGAR, PARAR, DESCONHECIDO = "RENOMEAR", "APAGAR", "PARAR", "DESCONHECIDO"


def _pastas_de_recurso(raiz):
    return [os.path.join(raiz, r) for r in sorted(os.listdir(raiz))
            if os.path.isdir(os.path.join(raiz, r)) and not r.startswith("_")]


def plano_de_snapshots(raiz):
    """2.6 aplicada ao que ja existe: snapshot com a HORA DA CAPTURA no nome passa a ter a
    DATA DA VERSAO. Nome fora das duas convencoes nao e tocado."""
    plano = []
    for pasta in _pastas_de_recurso(raiz):
        snaps = os.path.join(pasta, SNAPSHOTS)
        if not os.path.isdir(snaps):
            continue
        for a in sorted(os.listdir(snaps)):
            p = os.path.join(snaps, a)
            if SNAP_NOVO.match(a):
                continue
            if SNAP_ANTIGO.match(a):
                plano.append(dict(acao=RENOMEAR, origem=p,
                                  destino=os.path.join(snaps, nome_do_snapshot(p)),
                                  motivo="hora da captura -> data da versao (2.6)"))
            else:
                plano.append(dict(acao=DESCONHECIDO, origem=p, destino="",
                                  motivo="nome fora das duas convencoes -- nao tocado"))
    return plano


def _crc32(caminho):
    c = 0
    with open(caminho, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            c = zlib.crc32(b, c)
    return c & 0xFFFFFFFF


def _membros_do_acervo(raiz):
    """{nome_base: {(crc, tamanho)}} de todo membro de todo ZIP do acervo."""
    out = {}
    for z in manifesto_cvm.zips(raiz):
        try:
            with zipfile.ZipFile(z) as zf:
                for i in zf.infolist():
                    out.setdefault(os.path.basename(i.filename), set()).add(
                        (i.CRC, i.file_size))
        except zipfile.BadZipFile:
            continue
    return out


def _plano_de_extracao(pasta, membros):
    """Pasta extraida ao lado do ZIP e derivada e sai -- mas so se CADA arquivo dela for
    um membro de algum ZIP do acervo (nome, tamanho, CRC-32). Um que nao bata e PARAR."""
    falhas, n = [], 0
    for dirpath, _, arquivos in os.walk(pasta):
        for a in sorted(arquivos):
            p = os.path.join(dirpath, a)
            n += 1
            if (_crc32(p), os.path.getsize(p)) not in membros.get(a, set()):
                falhas.append(a)
    if n == 0:
        return dict(acao=PARAR, origem=pasta, destino="", motivo="pasta vazia")
    if falhas:
        return dict(acao=PARAR, origem=pasta, destino="",
                    motivo=f"{len(falhas)} de {n} arquivo(s) sem membro igual em ZIP "
                           f"nenhum: {', '.join(falhas[:5])}")
    return dict(acao=APAGAR, origem=pasta, destino="",
                motivo=f"{n} arquivos, todos com CRC-32 e tamanho de um membro do acervo")


def plano_de_limpeza(raiz):
    """Copias `(N).zip` e pastas extraidas. Nada muda no disco.

    A copia `(N)` NAO e lixo por construcao: em 2024 ela e a UNICA copia de uma versao
    (CV-01). Regra: sha256 identico a outro ZIP do acervo -> APAGAR; unico -> vira
    snapshot pela 2.6. O resto que nao e ZIP nem CSV sai DESCONHECIDO e nao e tocado --
    decidir o que e lixo e de quem olhou o arquivo, nao de uma regra."""
    plano = []
    hashes = {}
    for z in manifesto_cvm.zips(raiz):
        if not COPIA.match(os.path.basename(z)):
            hashes.setdefault(sha256(z), []).append(z)
    membros = None
    for pasta in _pastas_de_recurso(raiz):
        for a in sorted(os.listdir(pasta)):
            p = os.path.join(pasta, a)
            if a == SNAPSHOTS:
                continue
            if COPIA.match(a) and os.path.isfile(p):
                d = sha256(p)
                if hashes.get(d):
                    plano.append(dict(acao=APAGAR, origem=p, destino="",
                                      motivo=f"sha256 {d[:12]} identico a "
                                             f"{relativo(hashes[d][0], raiz)}"))
                else:
                    plano.append(dict(acao=RENOMEAR, origem=p,
                                      destino=os.path.join(pasta, SNAPSHOTS,
                                                           nome_do_snapshot(p)),
                                      motivo=f"sha256 {d[:12]} unico no acervo: vira "
                                             f"snapshot"))
            elif os.path.isdir(p) and os.path.isfile(p + ".zip"):
                if membros is None:
                    membros = _membros_do_acervo(raiz)
                plano.append(_plano_de_extracao(p, membros))
            elif not (os.path.isfile(p) and a.lower().endswith((".zip", ".csv"))):
                plano.append(dict(acao=DESCONHECIDO, origem=p, destino="",
                                  motivo="nao e ZIP, CSV nem extracao de um ZIP ao lado "
                                         "-- nao tocado"))
    return plano


def aplicar(plano):
    """Executa RENOMEAR e APAGAR. Com um PARAR no plano, nada e aplicado."""
    if any(x["acao"] == PARAR for x in plano):
        raise SystemExit("ha PARAR no plano: nada foi aplicado")
    for x in plano:
        if x["acao"] == RENOMEAR:
            if os.path.exists(x["destino"]):
                if sha256(x["destino"]) != sha256(x["origem"]):
                    raise SystemExit(f"{x['destino']} existe com outro conteudo")
                os.remove(x["origem"])
            else:
                os.makedirs(os.path.dirname(x["destino"]), exist_ok=True)
                os.replace(x["origem"], x["destino"])
        elif x["acao"] == APAGAR:
            if os.path.isdir(x["origem"]):
                shutil.rmtree(x["origem"], onerror=_tirar_somente_leitura)
            else:
                os.remove(x["origem"])


def _tirar_somente_leitura(funcao, caminho, _exc):
    """24/09, na primeira aplicacao real: as pastas extraidas pelo Windows vinham com
    atributo ReadOnly, e `rmdir` de diretorio ReadOnly da "Acesso negado" -- os CSVs de
    dentro sairam e a pasta ficou, vazia. Limpa o atributo e tenta de novo; se falhar
    outra vez, a excecao sobe.

    CI-02 (25/09, primeira execucao do workflow no Linux): no POSIX a pasta SEM ESCRITA nao
    impede apagar a pasta -- impede apagar o que esta DENTRO dela, e o `unlink` do arquivo
    falha. Liberar so o arquivo nao adianta: a permissao que falta e a da pasta-mae. Libera
    as duas."""
    rwx = stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC
    os.chmod(os.path.dirname(caminho) or ".", rwx)
    os.chmod(caminho, rwx)
    funcao(caminho)


# ── main ──────────────────────────────────────────────────────────────────────

def main(argv=None, abrir=urllib.request.urlopen, dormir=time.sleep, manifestar=None,
         armazem=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--raiz", default=None,
                   help=f"acervo (padrao: {RAIZ_RELATIVA} sob a raiz do repositorio)")
    p.add_argument("--registro", default=None,
                   help="padrao: docs/acervo/<acervo>/capturas.csv")
    p.add_argument("--escopo", nargs="+", choices=["recentes", "congelados", "cad"],
                   help="FILTRO opcional; sem ele, todos os anos do indice e o cad (2.4)")
    p.add_argument("--dry-run", action="store_true", help="nao grava byte nenhum")
    p.add_argument("--forcar", action="store_true", help="ignora o portao HEAD")
    p.add_argument("--pausa", type=float, default=1.0, help="segundos entre requisicoes")
    p.add_argument("--arrumar", choices=["snapshots", "limpeza"],
                   help="mostra o plano de arrumacao do acervo; com --aplicar, executa")
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--armazem", choices=["s3"],
                   help="sobe para o armazem em vez de guardar no disco (P-57); "
                        "credenciais so por variavel de ambiente R2_*")
    p.add_argument("--cache", default=None,
                   help="com --armazem: guarda tambem uma copia em <cache>/<chave>")
    p.add_argument("--raiz-repo", default=None, help=argparse.SUPPRESS)  # testes
    a = p.parse_args(argv)
    raiz = os.path.abspath(a.raiz or raiz_padrao())
    registro = a.registro or registro_padrao(raiz)

    if a.arrumar:
        plano = (plano_de_snapshots if a.arrumar == "snapshots" else plano_de_limpeza)(raiz)
        for x in plano:
            destino = f" -> {relativo(x['destino'], raiz)}" if x["destino"] else ""
            print(f"{x['acao']:12s} {relativo(x['origem'], raiz)}{destino}\n"
                  f"{'':12s} {x['motivo']}")
        cont = {k: sum(x["acao"] == k for x in plano)
                for k in (RENOMEAR, APAGAR, PARAR, DESCONHECIDO)}
        print("  ".join(f"{k} {v}" for k, v in cont.items()))
        if a.aplicar:
            aplicar(plano)
            print("aplicado.")
        return 1 if cont[PARAR] else 0

    if a.armazem:
        if a.dry_run:
            raise SystemExit("--dry-run e do modo disco: no armazem, saber o que mudou "
                             "exige baixar, e baixar e o que o dry-run promete nao fazer")
        return _main_armazem(a, raiz, registro, abrir, dormir,
                             armazem or armazem_mod.do_ambiente(a.armazem))
    if a.cache:
        raise SystemExit("--cache so vale com --armazem")

    estado = carregar_estado(raiz, registro)
    resumo = {}
    try:
        lista = alvos(a.escopo, abrir, dormir)
    except (urllib.error.URLError, RuntimeError) as e:
        print(f"[!] falha lendo o indice: {e}", file=sys.stderr)
        if not a.dry_run:
            anotar(registro, dict(dt_captura=agora(), situacao=ERRO, motivo=f"indice: {e}"))
        return 1
    for url, recurso in lista:
        try:
            s = capturar(url, recurso, raiz, registro, estado, abrir=abrir, dormir=dormir,
                         dry_run=a.dry_run, forcar=a.forcar)
        except (urllib.error.URLError, OSError) as e:
            s = ERRO
            print(f"[!] {url}  ERRO: {e}", file=sys.stderr)
            if not a.dry_run:
                anotar(registro, dict(dt_captura=agora(), recurso=recurso, url=url,
                                      arquivo=url.rsplit("/", 1)[-1], situacao=ERRO,
                                      motivo=str(e)))
        resumo[s] = resumo.get(s, 0) + 1
        if a.pausa:
            dormir(a.pausa)
    print("  ".join(f"{k} {v}" for k, v in sorted(resumo.items())))
    if a.dry_run:
        return 0
    salvar_estado(raiz, estado)
    falhou = resumo.get(ERRO, 0) + resumo.get(REJEITADO, 0)
    if falhou:
        print(f"{falhou} falha(s): o manifesto NAO foi regravado -- retrato de uma "
              f"captura incompleta nao e retrato", file=sys.stderr)
        return 1
    (manifestar or (lambda r: manifesto_cvm.main(["--manifesto", r])))(raiz)
    return 0


def _main_armazem(a, raiz, registro, abrir, dormir, armazem):
    """O estado vem SO do registro versionado: o `estado.json` local e cache de uma
    maquina, e o runner nao tem maquina. O log vai para o armazem sempre -- com falha
    inclusive, porque rodar e falhar tambem e prova de que rodou."""
    estado = estado_do_registro(ler_registro(registro))
    diario, resumo = [], {}
    relatar_ocupacao(armazem, raiz=a.raiz_repo)
    try:
        lista = alvos(a.escopo, abrir, dormir)
    except (urllib.error.URLError, RuntimeError) as e:
        print(f"[!] falha lendo o indice: {e}", file=sys.stderr)
        linha = dict(dt_captura=agora(), situacao=ERRO, motivo=f"indice: {e}")
        anotar(registro, linha)
        diario.append(linha)
        print(f"log: {enviar_diario(armazem, diario)}")
        return 1
    for url, recurso in lista:
        try:
            s = capturar_para_armazem(url, recurso, raiz, registro, estado, armazem,
                                      abrir=abrir, dormir=dormir, forcar=a.forcar,
                                      cache=a.cache, diario=diario)
        except (urllib.error.URLError, OSError) as e:
            s = ERRO
            print(f"[!] {url}  ERRO: {e}", file=sys.stderr)
            linha = dict(dt_captura=agora(), recurso=recurso, url=url,
                         arquivo=url.rsplit("/", 1)[-1], situacao=ERRO, motivo=str(e))
            anotar(registro, linha)
            diario.append(linha)
        resumo[s] = resumo.get(s, 0) + 1
        if a.pausa:
            dormir(a.pausa)
    print("  ".join(f"{k} {v}" for k, v in sorted(resumo.items())))
    print(f"log: {enviar_diario(armazem, diario)}")
    falhou = resumo.get(ERRO, 0) + resumo.get(REJEITADO, 0) + resumo.get(RECUSADO_POR_TETO, 0)
    if falhou:
        print(f"{falhou} falha(s)", file=sys.stderr)
        return 1
    return 0


def relatar_ocupacao(armazem, raiz=None, env=None):
    """Soma o bucket, imprime e, no Actions, entrega `armazem_gb` e `armazem_nivel` ao
    passo seguinte -- e ele quem abre a issue de aviso. Devolve o nivel."""
    env = os.environ if env is None else env
    aviso, teto = armazem_mod.limites_da_politica(raiz or raiz_repo())
    ocupado = armazem.ocupado()
    nivel = armazem_mod.nivel(ocupado, aviso, teto)
    gb = f"{ocupado / armazem_mod.GB:.2f}"
    print(f"armazem: {gb} GB (aviso {aviso / armazem_mod.GB:g}, "
          f"teto {teto / armazem_mod.GB:g}) -> {nivel}")
    saida = env.get("GITHUB_OUTPUT")
    if saida:
        with open(saida, "a", encoding="utf-8") as f:
            f.write(f"armazem_gb={gb}\narmazem_nivel={nivel}\n")
    return nivel


if __name__ == "__main__":
    raise SystemExit(main())

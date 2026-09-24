#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manifesto do acervo da CVM -- e a comparacao que NAO produz falso positivo.

POR QUE ELE EXISTE. O guia de download diz, com todas as letras: *um retrato sem hash
nao e um retrato, e sim um arquivo*. Os 33 ZIPs chegaram em 18/09/2026 e nenhum tinha
sha256 registrado -- a rotina existia como comando para alguem lembrar de rodar, e a P7
diz que rotina que depende de lembrar nao e rotina.

O ACHADO QUE MUDA O DESENHO, medido em 18/09 sobre o unico par que o acervo tinha.

Tres anos (2012, 2019, 2024) foram baixados duas vezes, com 14 dias de intervalo. O
`dfp_cia_aberta_2024.zip` de 04/09 e o de 18/09 tem sha256 DIFERENTE. E o dado e o
MESMO: dois dos dezoito CSVs mudaram, e neles

    mesmo numero de linhas, mesmo numero de bytes, e ZERO linhas exclusivas de
    qualquer um dos lados -- `sorted(a) == sorted(b)`.

Sao 8 linhas fora de posicao em 94.517, e 12 em 59.744. **A CVM regerou o arquivo e a
ordem das linhas mudou. Nao houve reapresentacao.**

    A estrategia registrada no CLAUDE.md §11.6 -- *"baixar, comparar, guardar o delta"* --
    teria declarado uma reapresentacao aqui, e commitado ruido no git toda semana. E o
    F-02 espelhado: la a ausencia virava zero; aqui o RUIDO VIRA EVENTO.

Por isso este modulo tem duas operacoes e elas respondem perguntas diferentes:

    --manifesto   sha256 do BYTE que a CVM entregou. E procedencia: prova QUAL arquivo
                  voce tem. Nunca serve para responder "mudou?".
    --comparar    diferenca de CONTEUDO entre dois ZIPs, normalizada por ordem. E a
                  unica que responde "a CVM reapresentou alguma coisa?".

E o 2019 foi a testemunha do outro lado: byte a byte identico nos 14 dias, exatamente
como a politica da CVM promete para os anos fora da janela de reapresentacao. A promessa
deixou de ser citada e passou a ser medida.

USO
    python fase0/manifesto_cvm.py --manifesto data/bronze/cvm
        grava em docs/acervo/cvm/dt_captura=AAAA-MM-DD.csv -- FORA do `data/`, que o
        .gitignore ignora. Manifesto ignorado pelo git nao prova nada a terceiro.
    python fase0/manifesto_cvm.py --comparar a.zip b.zip
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import hashlib
import io
import os
import sys
import zipfile

BLOCO = 1 << 20
COLUNAS = ("caminho", "bytes", "sha256", "mtime_utc", "dt_captura", "origem", "acesso")
COLUNAS_ORIGEM = ("caminho", "origem", "acesso")
ORIGEM = "origem.csv"


def sha256(caminho, bloco=BLOCO):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for p in iter(lambda: f.read(bloco), b""):
            h.update(p)
    return h.hexdigest()


def zips(raiz):
    """Todo .zip sob a raiz, em ordem estavel.

    Ordenar nao e estetica: e a licao do P-85, em que a saida de um relatorio mudava de
    texto entre execucoes por causa de um `set` impresso sem ordem, e o instantaneo
    dourado deixou de servir de rede."""
    out = []
    for pasta, _, arquivos in os.walk(raiz):
        for a in arquivos:
            if a.lower().endswith(".zip"):
                out.append(os.path.join(pasta, a))
    return sorted(out)


def extracoes_soltas(raiz):
    """Todo arquivo com cara de COTAHIST que NAO e .zip sob a raiz, em ordem estavel.

    P-120, decisao dele em 24/09/2026: as copias extraidas sairam do acervo -- o ZIP e a
    fonte, a extracao e derivada e se refaz. Sem isto a decisao dependeria de alguem
    lembrar de nao extrair ali de novo (P7), e o `manifesto()`, que so ve `*.zip`, nao a
    enxergaria: 88% dos bytes do acervo ficaram um mes sem sha256 e ninguem soube.

    CONTA e nao calcula hash: manifestar derivado seria pagar 7x de leitura para provar o
    que o ZIP ja prova, que e a saida que ele recusou.

    O criterio e o PREFIXO, e nao o `calendario.ano_de()`, de proposito: este e o alarme,
    e tem de ser mais largo que o leitor. Tudo o que o `ano_de()` aceita comeca com
    COTAHIST, entao nada que o calendario leria escapa daqui; e um `COTAHIST_A2023.TXT.part`
    que ele recusaria continua sendo sobra de extracao no acervo."""
    out = []
    for pasta, _, arquivos in os.walk(raiz):
        for a in arquivos:
            if a.upper().startswith("COTAHIST") and not a.lower().endswith(".zip"):
                out.append(os.path.join(pasta, a))
    return sorted(out)


def origem_declarada(pasta):
    """De ONDE cada arquivo veio, lido de `origem.csv` ao lado do manifesto.

    O sha256 prova QUAL arquivo voce tem. Ele nao prova DE ONDE ele veio -- e a P-06
    esta aberta desde 05/09 exatamente por isso: o `COTAHIST_A2023.ZIP` entrou no acervo
    com 70 MB, hash, e nenhuma origem escrita.

    E um arquivo A PARTE, e nao um campo do manifesto, porque as duas coisas tem ciclos
    de vida diferentes: o manifesto e reescrito a cada captura; a origem de um arquivo
    ja baixado nao muda nunca. Misturar os dois faria a origem ser reescrita -- e
    perdida -- toda vez que alguem rodasse o manifesto."""
    p = os.path.join(pasta, ORIGEM)
    if not os.path.exists(p): return {}
    # P-108: `utf-8-sig`, nao `utf-8`. O Windows PowerShell 5.1 grava `Out-File -Encoding
    # utf8` COM BOM, e o roteiro de 21/09 mandava criar este arquivo exatamente assim. Com
    # `utf-8` a primeira coluna vira '\ufeffcaminho', o `r.get("caminho")` abaixo devolve
    # None para TODA linha, e o filtro descarta tudo EM SILENCIO: 41 origens declaradas,
    # zero lidas, e o contador da P-06 continua em 42 sem dizer por que. F-02 no registro.
    with open(p, encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f, delimiter=";")
        if leitor.fieldnames and "caminho" not in leitor.fieldnames:
            raise ValueError(f"{p}: cabecalho {leitor.fieldnames} nao tem a coluna "
                             f"'caminho' -- origem ilegivel nao e origem ausente")
        return {r["caminho"]: r for r in leitor if r.get("caminho")}


def manifesto(raiz, quando=None, origens=None):
    """Uma linha por ZIP: o que se tem, desde quando se sabe, e de onde veio."""
    quando = quando or dt.datetime.now(dt.timezone.utc)
    origens = origens or {}
    linhas = []
    for caminho in zips(raiz):
        st = os.stat(caminho)
        rel = os.path.relpath(caminho, raiz).replace("\\", "/")
        o = origens.get(rel, {})
        linhas.append({
            "caminho": rel,
            "bytes": st.st_size,
            "sha256": sha256(caminho),
            "mtime_utc": dt.datetime.fromtimestamp(
                st.st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "dt_captura": quando.strftime("%Y-%m-%d"),
            # vazio NAO e zero: e "nao sei", e a linha seguinte o conta em voz alta
            "origem": o.get("origem", ""),
            "acesso": o.get("acesso", ""),
        })
    return linhas


def sem_origem(linhas):
    """Quantos arquivos do acervo tem hash e nao tem de onde vieram. E a P-06 virando
    NUMERO -- e um numero que decai, em vez de uma frase num arquivo de pendencias."""
    return [x["caminho"] for x in linhas if not x["origem"]]


POLITICA = os.path.join("alocacao", "politica.yaml")
ACERVO = os.path.join("docs", "acervo")


class PoliticaAusente(FileNotFoundError):
    """A politica nao esta onde a raiz encontrada diz que ela estaria.

    NAO devolve "nada declarado". Arquivo ausente e arquivo vazio sao coisas diferentes,
    e essa distincao foi DECIDIDA por ele no E-02 (12/09): dizer "nenhum acervo sem
    regime" quando o que houve foi "nao achei o arquivo que diz os regimes" e mentira
    documental -- a mesma que o `tese.carregar_registros` cometia."""


def acervos_sem_regime(raiz_repo):
    """P7 virada NUMERO: quantos acervos existem sem regime de captura declarado.

    Devolve `(sem_declaracao, declarados_sem_pasta)` -- dois conjuntos de nomes de
    pasta de `docs/acervo/`. O primeiro sao acervos que existem e cujo regime ninguem
    escreveu; o segundo sao nomes que a politica declara e que nao correspondem a
    acervo nenhum, isto e, declaracao apodrecida.

    O QUE ISTO MEDE, e o alcance e mais estreito que o nome (P5 aplicada ao proprio
    instrumento): mede que cada subpasta de `docs/acervo/` e NOMEADA por alguma entrada
    de `limitacoes_declaradas.*.acervos`. NAO mede que a captura seja de fato manual,
    nem que alguem a tenha rodado, nem quando. Mede uma coisa so -- que nenhum acervo
    exista sem alguem ter escrito sob que regime ele e capturado.

    POR QUE ELE MORA AQUI E NAO NUM TESTE. A P-77 ensinou que campo lido so por teste e
    campo que o motor nao usa: o teste prova o esquema e ninguem prova o comportamento.
    `acervos` e lido por esta funcao, e o teste so a chama -- mesmo desenho do
    `preregistro.conferir_registro()`.

    E ele e da familia do `sem_origem()`: contagem que DECAI. O dia em que a captura da
    CVM virar rotina automatica, `cvm` sai de `acervos` e a contagem sobe -- o teste
    reprova, e a atualizacao e cobrada no mesmo minuto em que o mundo muda. Linha de
    base que so encolhe por conserto e a unica que vale (P-86)."""
    import yaml
    caminho = os.path.join(raiz_repo, POLITICA)
    if not os.path.exists(caminho):
        raise PoliticaAusente(caminho)
    with io.open(caminho, encoding="utf-8") as f:
        P = yaml.safe_load(f)
    declarados = set()
    for lim in (P.get("limitacoes_declaradas") or {}).values():
        if isinstance(lim, dict):
            declarados.update(lim.get("acervos") or ())
    base = os.path.join(raiz_repo, ACERVO)
    existem = {n for n in os.listdir(base)
               if os.path.isdir(os.path.join(base, n))} if os.path.isdir(base) else set()
    return existem - declarados, declarados - existem


def raiz_do_repositorio(partida):
    """Sobe ate achar o `pyproject.toml`. E o mesmo ancoradouro que o `ambiente.py` usa,
    e nao o `.git`: o manifesto tem de saber onde fica o repositorio mesmo num clone
    sem historico."""
    d = os.path.abspath(partida)
    while True:
        if os.path.exists(os.path.join(d, "pyproject.toml")): return d
        pai = os.path.dirname(d)
        if pai == d: return None
        d = pai


def destino_padrao(raiz_acervo, hoje):
    """`docs/acervo/<nome>/dt_captura=AAAA-MM-DD.csv`, e NAO dentro do acervo.

    18/09/2026, e o defeito e meu. A primeira versao gravava em
    `data/bronze/cvm/manifesto/`, o `CVM-PRIMEIRO-RETRATO.md` afirmava que *"o manifesto
    entra no repositorio"*, e o `.gitignore` ignora `data/` inteiro desde sempre. O
    arquivo foi gravado, o commit passou, e o manifesto **nao entrou** -- justamente o
    arquivo cujo unico proposito e tornar a procedencia verificavel por terceiro.

    O documento declarava um comportamento que o sistema nao tinha, e os dois
    concordaram porque ninguem olhou a saida do `git commit`. E o defeito recorrente do
    projeto, desta vez cometido no mesmo dia em que o instrumento nasceu."""
    base = raiz_do_repositorio(raiz_acervo) or os.path.abspath(raiz_acervo)
    nome = os.path.basename(os.path.abspath(raiz_acervo).rstrip(os.sep)) or "acervo"
    return os.path.join(base, "docs", "acervo", nome, f"dt_captura={hoje}.csv")


def gravar(linhas, destino):
    partes = os.path.abspath(destino).replace("\\", "/").split("/")
    if "data" in partes:
        raise ValueError(
            f"recusando gravar o manifesto em {destino}: o caminho passa por `data/`, e "
            f"`data/` esta no .gitignore. Manifesto que nao entra no repositorio nao e "
            f"procedencia de ninguem -- e o unico proposito dele e ser verificavel sem "
            f"os 700 MB do acervo.")
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    novo = io.StringIO()
    w = csv.DictWriter(novo, fieldnames=COLUNAS, delimiter=";")
    w.writeheader()
    w.writerows(linhas)
    texto = novo.getvalue()

    # 18/09, e o caso apareceu na primeira hora de uso: o manifesto do acervo da B3 foi
    # gravado com UM arquivo (so o COTAHIST de 2023), e os outros quatro anos seriam
    # baixados em seguida -- no MESMO dia. O nome e `dt_captura=AAAA-MM-DD.csv`, entao a
    # segunda gravacao apagaria a primeira sem dizer nada.
    #
    # E o retrato apagado seria justamente a prova de que, as 14h, o acervo tinha so 2023.
    # O manifesto existe porque a CVM sobrescreve arquivo sob o mesmo nome -- e ele estava
    # fazendo exatamente isso consigo. O instrumento com o defeito que ele mede.
    #
    # A saida NAO e travar (o fluxo legitimo e baixar mais e regravar) nem versionar tudo
    # (rodar duas vezes sem mudanca criaria lixo). E: identico nao reescreve, diferente
    # PRESERVA o anterior com a impressao do proprio conteudo no nome.
    anterior = None
    if os.path.exists(destino):
        with open(destino, encoding="utf-8", newline="") as f:
            velho = f.read()
        if velho == texto:
            return destino                      # idempotente: duas execucoes, um arquivo
        raiz, ext = os.path.splitext(destino)
        anterior = f"{raiz}.{hashlib.sha256(velho.encode('utf-8')).hexdigest()[:12]}{ext}"
        os.replace(destino, anterior)
        print(f"AVISO: ja havia manifesto para hoje, com CONTEUDO DIFERENTE -- o acervo "
              f"mudou dentro do mesmo dia.\n  o retrato anterior foi PRESERVADO em "
              f"{os.path.basename(anterior)}", file=sys.stderr)
    with open(destino, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
    return destino


def comparar(a, b):
    """Diferenca de CONTEUDO entre dois ZIPs, insensivel a ordem de linha.

    Devolve (veredito, detalhe). O veredito e um NOME, nunca um booleano solto:

      IDENTICO      byte a byte
      REORDENADO    o conjunto de linhas e o mesmo em todos os membros -- a CVM regerou
                    o arquivo. **Nao e reapresentacao.**
      REAPRESENTADO ha linha que existe de um lado e nao do outro. E o evento que o
                    projeto quer capturar, e so ele.
      ESTRUTURA     os ZIPs nao tem os mesmos membros
    """
    if sha256(a) == sha256(b):
        return "IDENTICO", {}
    za, zb = zipfile.ZipFile(a), zipfile.ZipFile(b)
    na = {i.filename for i in za.infolist()}
    nb = {i.filename for i in zb.infolist()}
    if na != nb:
        return "ESTRUTURA", {"so_em_a": sorted(na - nb), "so_em_b": sorted(nb - na)}
    detalhe = {}
    veredito = "IDENTICO"
    for nome in sorted(na):
        da, db = za.read(nome), zb.read(nome)
        if da == db: continue
        la, lb = da.split(b"\n"), db.split(b"\n")
        sa, sb = set(la), set(lb)
        so_a, so_b = sa - sb, sb - sa
        if not so_a and not so_b:
            detalhe[nome] = {"tipo": "REORDENADO",
                             "fora_de_posicao": sum(1 for x, y in zip(la, lb) if x != y),
                             "linhas": len(la)}
            veredito = "REORDENADO" if veredito == "IDENTICO" else veredito
        else:
            detalhe[nome] = {"tipo": "REAPRESENTADO", "saiu": len(so_a),
                             "entrou": len(so_b), "linhas": len(lb),
                             "exemplo_entrou": [x.decode("latin-1")[:160] for x in list(so_b)[:2]],
                             "exemplo_saiu": [x.decode("latin-1")[:160] for x in list(so_a)[:2]]}
            veredito = "REAPRESENTADO"
    return veredito, detalhe


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--manifesto", metavar="RAIZ")
    p.add_argument("--saida", default=None)
    p.add_argument("--comparar", nargs=2, metavar=("A", "B"))
    a = p.parse_args(argv)
    if a.comparar:
        v, d = comparar(*a.comparar)
        print(f"veredito: {v}")
        for nome, info in d.items():
            print(f"  {nome}: {info}")
        # REAPRESENTADO e o unico que exige acao humana; sair != 0 para o chamador saber
        return 2 if v == "REAPRESENTADO" else 0
    if a.manifesto:
        hoje_pasta = os.path.dirname(a.saida) if a.saida else None
        linhas = manifesto(a.manifesto, origens=origem_declarada(
            hoje_pasta or os.path.dirname(destino_padrao(a.manifesto, "x"))))
        if not linhas:
            print(f"nenhum .zip sob {a.manifesto} -- e isso NAO e 'nada mudou': e "
                  f"'nao ha acervo'. Confira o caminho antes de concluir.", file=sys.stderr)
            return 1
        hoje = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
        destino = a.saida or destino_padrao(a.manifesto, hoje)
        gravar(linhas, destino)
        print(f"{len(linhas)} arquivos, {sum(x['bytes'] for x in linhas)/1e6:.0f} MB")
        print(f"manifesto: {destino}")
        for x in linhas:
            print(f"  {x['sha256'][:16]}  {x['bytes']:>12,}  {x['caminho']}"
                  + ("" if x["origem"] else "   <- SEM ORIGEM"))
        faltam = sem_origem(linhas)
        if faltam:
            print(f"\nP-06: {len(faltam)} de {len(linhas)} arquivo(s) tem sha256 e NAO tem "
                  f"de onde vieram.\n  O hash prova QUAL arquivo e; ele nao prova a "
                  f"procedencia. Declare em\n  {os.path.join(os.path.dirname(destino), ORIGEM)}"
                  f"  (colunas: {';'.join(COLUNAS_ORIGEM)})", file=sys.stderr)
        else:
            print(f"\nP-06: os {len(linhas)} arquivos tem origem declarada.")
        # P-102: esta conferencia e ACESSORIA. O trabalho do comando e gravar o
        # retrato; se a auditoria da P7 nao puder rodar, ela AVISA e o retrato fica de
        # pe. Uma guarda que derruba o trabalho que ela existe para proteger inverteu o
        # proprio proposito -- e calar seria pior ainda (F-02).
        raiz_repo = raiz_do_repositorio(a.manifesto)
        try:
            sem, orfas = acervos_sem_regime(raiz_repo) if raiz_repo else (None, None)
        except PoliticaAusente as e:
            sem = orfas = None
            print(f"\nAVISO: a conferencia da P7 NAO rodou -- politica nao encontrada em "
                  f"{e}. O manifesto acima VALE; o que ficou por conferir e se todo "
                  f"acervo tem regime de captura declarado.", file=sys.stderr)
        if sem:
            print(f"\nP7: {len(sem)} acervo(s) sem regime de captura declarado: "
                  f"{', '.join(sorted(sem))}.\n  Rotina que depende de alguem lembrar "
                  f"nao e rotina. Ou ela roda sozinha, ou entra em\n  "
                  f"{POLITICA} -> limitacoes_declaradas.*.acervos", file=sys.stderr)
        if orfas:
            print(f"\nP7: {len(orfas)} declaracao(oes) sem acervo: "
                  f"{', '.join(sorted(orfas))}. Declaracao apodrecida.", file=sys.stderr)
        # P-120: por ultimo, para ser a linha que fica na tela. O numero sai SEMPRE,
        # inclusive o zero (§5-B.14): "0" medido e silencio nao podem ter a mesma cara.
        soltas = extracoes_soltas(a.manifesto)
        print(f"\nP-120: {len(soltas)} copia(s) extraida(s) de COTAHIST fora de ZIP.")
        if soltas:
            print(f"AVISO P-120: {len(soltas)} arquivo(s) com cara de COTAHIST que NAO sao "
                  f".zip, sem sha256 no manifesto:\n"
                  + "".join(f"  {os.path.relpath(s, a.manifesto)}\n" for s in soltas)
                  + "  A decisao da P-120 e que o acervo guarda so o ZIP: a extracao e "
                  "derivada e se refaz.\n  Apague-as (conferindo antes com "
                  "fase0/nomear_extracoes.py) ou extraia fora do acervo.",
                  file=sys.stderr)
        return 0
    p.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

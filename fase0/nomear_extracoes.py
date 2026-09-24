# -*- coding: utf-8 -*-
"""
nomear_extracoes.py -- as copias extraidas do COTAHIST com o nome certo (23/09/2026).

O PROBLEMA, como ele apareceu: ao extrair os 41 ZIPs, o Windows mostra `COTAHIST.A1986`
como "Arquivo A1986" -- o ponto faz `.A1986` virar extensao, e extensao que nao existe.
`COTAHIST_A2001` sai sem extensao nenhuma. De 2002 em diante sai `.TXT`. E o de 2026 ficou
numa PASTA `COTAHIST_A2026/`, que a P-121 mostrou ter nome de arquivo de ano.

A causa nao e a extracao: e a B3. O MEMBRO de dentro do ZIP muda de convencao na propria
serie (P-99): `COTAHIST.A1986` ate 2000, `COTAHIST_A2001` em 2001, `COTAHIST_A2002.TXT`
dai em diante. Quem extrai herda o nome do membro. Toda extracao futura repete isto -- por
isso e modulo com teste, e nao um comando digitado uma vez (P7).

O QUE ELE FAZ: para cada copia extraida, propoe o nome `COTAHIST_A<ANO>.TXT` -- a convencao
que a B3 adotou de 2002 em diante -- e so renomeia depois de PROVAR que a copia e o conteudo
do ZIP do mesmo ano:
  - o cabecalho diz o ano que o nome diz (`00COTAHIST.<ANO>`);
  - o tamanho bate com o do membro, declarado no diretorio central do ZIP;
  - o CRC-32 bate com o do membro -- a mesma soma que o proprio ZIP usa para se conferir.

O QUE ELE RECUSA FAZER, e as recusas sao o modulo:
  - nao renomeia sem o ZIP ao lado: sem a fonte, a copia nao tem como ser conferida;
  - nao sobrescreve: se o nome certo ja existe, a linha diz isso e para ali;
  - nao diz JA_CORRETO sem conferir: a copia que ja tem o nome certo passa pela
    mesma conferencia, e sai RECUSADO se falhar (P-131);
  - nao apaga arquivo nenhum; remove so a subpasta de ano que ficou vazia depois da
    renomeacao (P-121). Apagar as copias foi decisao dele na P-120 (24/09), e foi
    feito fora daqui;
  - nao toca nos ZIPs, que sao a fonte e tem sha256 no manifesto.

Por padrao so MOSTRA o plano. `--aplicar` executa.

USO
    py -3.11 fase0\\nomear_extracoes.py                # o plano, sem mexer em nada
    py -3.11 fase0\\nomear_extracoes.py --aplicar      # executa o que o plano diz

Descoberta de ano, membro do ZIP e cabecalho vem do `calendario.py` (N-01).
"""
import argparse
import os
import sys
import zipfile
import zlib

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import calendario                                                       # noqa: E402

PASTA_PADRAO = os.path.join("data", "bronze", "b3", "cotahist")
BLOCO = 1 << 20

RENOMEAR = "RENOMEAR"
JA_CORRETO = "JA_CORRETO"
DESTINO_EXISTE = "DESTINO_EXISTE"
RECUSADO = "RECUSADO"


def nome_certo(ano):
    return "COTAHIST_A%s.TXT" % ano


def _zip_do_ano(pasta, ano):
    """O ZIP do ano na pasta, qualquer caixa de letra, ou None."""
    alvo = ("COTAHIST_A%s.ZIP" % ano).lower()
    for nome in os.listdir(pasta):
        if nome.lower() == alvo and os.path.isfile(os.path.join(pasta, nome)):
            return os.path.join(pasta, nome)
    return None


def candidatos(pasta):
    """[(caminho, ano)] das copias extraidas: tudo com nome de COTAHIST que NAO e ZIP,
    na pasta e UM nivel abaixo, dentro de subpasta com nome de ano (o caso do 2026)."""
    fora = []
    for nome in sorted(os.listdir(pasta)):
        caminho = os.path.join(pasta, nome)
        ano = calendario.ano_de(nome)
        if ano is None or nome.lower().endswith(".zip"):
            continue
        if os.path.isfile(caminho):
            fora.append((caminho, ano))
        elif os.path.isdir(caminho):
            for dentro in sorted(os.listdir(caminho)):
                c2 = os.path.join(caminho, dentro)
                a2 = calendario.ano_de(dentro)
                if a2 is not None and os.path.isfile(c2) and not dentro.lower().endswith(".zip"):
                    fora.append((c2, a2))
    return fora


def _crc32(caminho):
    crc = 0
    with open(caminho, "rb") as f:
        while True:
            b = f.read(BLOCO)
            if not b:
                return crc & 0xFFFFFFFF
            crc = zlib.crc32(b, crc)


def conferir(caminho, ano, caminho_zip):
    """(True, "") se a copia e o membro do ZIP do mesmo ano; senao (False, motivo)."""
    if caminho_zip is None:
        return False, "sem COTAHIST_A%s.ZIP ao lado para conferir" % ano
    with open(caminho, encoding="latin-1") as f:
        primeira = f.readline()
    try:
        ano_cab, _gerado = calendario.conferir_cabecalho(primeira, caminho)
    except calendario.LeiauteInesperado as e:
        return False, "cabecalho: %s" % e
    if ano_cab != ano:
        return False, "cabecalho diz %r e o nome diz %s" % (ano_cab, ano)
    try:
        with zipfile.ZipFile(caminho_zip) as z:
            info = z.getinfo(calendario.membro_do_zip(z))
    except (zipfile.BadZipFile, calendario.LeiauteInesperado) as e:
        return False, "ZIP ilegivel: %s" % e
    tamanho = os.path.getsize(caminho)
    if tamanho != info.file_size:
        return False, "tamanho %d, o membro do ZIP tem %d" % (tamanho, info.file_size)
    crc = _crc32(caminho)
    if crc != info.CRC:
        return False, "CRC-32 %08x, o do membro do ZIP e %08x" % (crc, info.CRC)
    return True, ""


def plano(pasta):
    """Uma linha por copia extraida: origem, destino, ano, status, motivo."""
    linhas = []
    for caminho, ano in candidatos(pasta):
        destino = os.path.join(pasta, nome_certo(ano))
        base = dict(origem=caminho, destino=destino, ano=ano, motivo="")
        if os.path.normcase(os.path.abspath(caminho)) == os.path.normcase(
                os.path.abspath(destino)):
            # P-131: nome certo nao e conteudo certo -- JA_CORRETO tambem passa por conferir()
            ok, motivo = conferir(caminho, ano, _zip_do_ano(pasta, ano))
            linhas.append(dict(base, status=JA_CORRETO if ok else RECUSADO, motivo=motivo))
            continue
        if os.path.exists(destino):
            linhas.append(dict(base, status=DESTINO_EXISTE,
                               motivo="%s ja existe; nada foi sobrescrito"
                               % os.path.basename(destino)))
            continue
        ok, motivo = conferir(caminho, ano, _zip_do_ano(pasta, ano))
        linhas.append(dict(base, status=RENOMEAR if ok else RECUSADO, motivo=motivo))
    return linhas


def aplicar(linhas, pasta):
    """Executa os RENOMEAR. Remove subpasta de ano que ficou VAZIA -- e so ela: pasta
    vazia nao e dado, e com nome de ano ela e a armadilha da P-121."""
    feitos = 0
    for ln in linhas:
        if ln["status"] != RENOMEAR:
            continue
        os.rename(ln["origem"], ln["destino"])
        feitos += 1
        sub = os.path.dirname(ln["origem"])
        if (os.path.normcase(os.path.abspath(sub)) != os.path.normcase(os.path.abspath(pasta))
                and not os.listdir(sub)):
            os.rmdir(sub)
    return feitos


def main(argv=None):
    p = argparse.ArgumentParser(description="Nomeia as copias extraidas do COTAHIST "
                                            "como COTAHIST_A<ANO>.TXT, conferidas contra o ZIP.")
    p.add_argument("--pasta", default=PASTA_PADRAO)
    p.add_argument("--aplicar", action="store_true",
                   help="executa o plano (sem isto, so mostra)")
    a = p.parse_args(argv)
    if not os.path.isdir(a.pasta):
        print("pasta nao existe: %s" % os.path.abspath(a.pasta), file=sys.stderr)
        return 2
    linhas = plano(a.pasta)
    for ln in linhas:
        rel = os.path.relpath(ln["origem"], a.pasta)
        print("  %-15s %-28s -> %-20s %s" % (ln["status"], rel,
                                              os.path.basename(ln["destino"]), ln["motivo"]))
    cont = {s: sum(1 for x in linhas if x["status"] == s)
            for s in (RENOMEAR, JA_CORRETO, DESTINO_EXISTE, RECUSADO)}
    print("\n%d copia(s): %s" % (len(linhas), ", ".join("%s=%d" % kv for kv in cont.items())))
    if a.aplicar:
        print("renomeadas: %d" % aplicar(linhas, a.pasta))
    elif cont[RENOMEAR]:
        print("nada foi alterado. Para executar: --aplicar")
    return 1 if cont[RECUSADO] else 0


if __name__ == "__main__":
    sys.exit(main())

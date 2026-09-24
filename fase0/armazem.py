#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Armazem de objetos do acervo -- onde o byte capturado mora quando a maquina esta desligada.

POR QUE ELE EXISTE (P-57, decisao em docs/decisoes/P-57.md). A captura da CVM passou a
rodar no GitHub Actions, cujo disco e efemero: o que o runner baixa some quando o job
acaba. O armazem (Cloudflare R2, pela API S3) e o disco que sobrevive ao job. O git
continua guardando so METADADO -- o registro e o inventario --, nunca o byte da fonte.

A CHAVE E O CONTEUDO. `<fonte>/<recurso>/<arquivo>/<sha256>.<ext>`: duas versoes do mesmo
arquivo sao duas chaves, e a mesma versao e sempre a mesma chave. Por isso o armazem NUNCA
sobrescreve -- `enviar_se_ausente` e a unica escrita, e mandar a mesma chave duas vezes nao
muda nada. O `_snapshots/` do disco local deixa de ser necessario aqui: toda versao ja tem
endereco proprio.

E a chave com sha256 e conferida nas duas pontas: na subida (o arquivo local tem de ter o
hash que a chave promete) e na descida (o que voltou tem de ter o hash que a chave diz).
Uma chave que mente sobre o conteudo e o F-02 com endereco: o nome certo sobre o byte
errado, e ninguem descobre porque o nome e a prova.

CREDENCIAIS. So por variavel de ambiente (R2_ACCOUNT_ID, R2_ACCESS_KEY_ID,
R2_SECRET_ACCESS_KEY, R2_BUCKET; R2_ENDPOINT opcional). Nenhum valor e impresso, registrado
ou posto numa mensagem de erro: a falta de uma diz o NOME da variavel, nunca o valor de
outra. O repositorio e publico (P-62), e o log do Actions tambem e.

O QUE ELE NAO FAZ (P5):
  - nao impede duas escritas simultaneas da mesma chave: `existe` e `enviar` sao duas
    chamadas. Quem garante que nao ha duas capturas ao mesmo tempo e o `concurrency` do
    workflow. Como a chave e o conteudo, a corrida escreveria o mesmo byte duas vezes --
    inofensivo, mas nao impossivel;
  - nao versiona nem apaga: nao ha metodo de remocao, de proposito.

O TETO (24/09/2026, pedido dele: cobranca zero). O R2 nao tem limite de gasto -- os
alertas da Cloudflare avisam, nao param --, entao o limite e deste codigo:
`politica.yaml -> armazem.aviso_gb / teto_gb`. Antes de cada envio o armazem SOMA o
bucket; se o envio o levaria acima do teto, levanta `TetoExcedido` e nada sobe. Um
armazem criado por `do_ambiente()` ja nasce limitado, e nao ha como pedir um sem teto
pela linha de comando. O que o teto NAO cobre esta em
`limitacoes_declaradas.o_teto_do_armazem_e_do_codigo`.

O boto3 e importado so dentro do `ArmazemS3`: a suite nao depende dele, e o modulo carrega
sem ele (pyproject -> optional-dependencies.captura).
"""
from __future__ import annotations

import abc
import hashlib
import os
import re
import shutil

FONTES = ("cvm", "b3")
VARIAVEIS = ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
# a chave de conteudo: o ultimo segmento e <sha256>.<ext>
CHAVE_DE_CONTEUDO = re.compile(r"^[^/]+/[^/]+/[^/]+/([0-9a-f]{64})\.[a-z0-9]+$")


class ChaveInvalida(ValueError):
    """A chave nao tem a forma que o armazem promete."""


class ConteudoDivergente(RuntimeError):
    """O byte nao tem o sha256 que a chave diz. Nada foi aceito."""


class ArmazemIndisponivel(RuntimeError):
    """Faltam credenciais ou o boto3. A mensagem diz O QUE falta, nunca um valor."""


class TetoExcedido(RuntimeError):
    """O envio levaria o bucket acima do teto. Nada foi enviado."""


class LimitesAusentes(RuntimeError):
    """`politica.yaml -> armazem` falta ou esta incoerente. Sem teto nao se envia (P1):
    limite ausente nao vira "sem limite", que e o F-02 com cara de liberdade."""


GB = 10 ** 9     # decimal: a leitura conservadora do "10 GB" gratis (10 GiB seria maior)
ABAIXO, AVISO, TETO = "abaixo", "aviso", "teto"
POLITICA = os.path.join("alocacao", "politica.yaml")


def limites_da_politica(raiz_repo):
    """(aviso, teto) em BYTES, de `politica.yaml -> armazem`. Levanta se faltar."""
    import yaml
    caminho = os.path.join(raiz_repo, POLITICA)
    if not os.path.exists(caminho):
        raise LimitesAusentes(f"{caminho} nao existe")
    with open(caminho, encoding="utf-8") as f:
        sec = (yaml.safe_load(f) or {}).get("armazem") or {}
    aviso, teto = sec.get("aviso_gb"), sec.get("teto_gb")
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and x > 0
               for x in (aviso, teto)):
        raise LimitesAusentes(f"armazem.aviso_gb={aviso!r} teto_gb={teto!r}: "
                              "os dois tem de ser numeros positivos")
    if aviso >= teto:
        raise LimitesAusentes(f"armazem.aviso_gb ({aviso}) tem de ser menor que "
                              f"teto_gb ({teto})")
    return int(aviso * GB), int(teto * GB)


def nivel(ocupado, aviso, teto):
    """ABAIXO, AVISO (ocupado >= aviso) ou TETO (ocupado >= teto)."""
    return TETO if ocupado >= teto else AVISO if ocupado >= aviso else ABAIXO


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _segmento(nome, valor):
    if not isinstance(valor, str) or not valor or "/" in valor or "\\" in valor \
            or valor in (".", ".."):
        raise ChaveInvalida(f"{nome} {valor!r}: segmento vazio ou com barra")
    return valor


def chave(fonte, recurso, arquivo, digest):
    """`<fonte>/<recurso>/<arquivo>/<sha256>.<ext>` -- a extensao vem do arquivo, em
    minusculas (`COTAHIST_A2023.ZIP` e `.zip` como qualquer outro)."""
    if fonte not in FONTES:
        raise ChaveInvalida(f"fonte {fonte!r} fora de {FONTES}")
    _segmento("recurso", recurso)
    _segmento("arquivo", arquivo)
    if not isinstance(digest, str) or not SHA256.match(digest):
        raise ChaveInvalida(f"sha256 {digest!r} nao sao 64 hex minusculos")
    ext = os.path.splitext(arquivo)[1].lower().lstrip(".")
    if not ext:
        raise ChaveInvalida(f"arquivo {arquivo!r} sem extensao")
    return f"{fonte}/{recurso}/{arquivo}/{digest}.{ext}"


def sha_da_chave(k):
    """O sha256 que a chave promete, ou None se ela nao e chave de conteudo (log)."""
    m = CHAVE_DE_CONTEUDO.match(k)
    return m.group(1) if m else None


def _validar(k):
    if not isinstance(k, str) or not k or k.startswith("/") or "\\" in k \
            or any(p in ("", ".", "..") for p in k.split("/")):
        raise ChaveInvalida(f"chave {k!r}")
    return k


class Armazem(abc.ABC):
    """A interface. As subclasses implementam o transporte (`_existe`, `_enviar`,
    `_baixar`, `_listar`); a regra -- nunca sobrescrever, conferir o conteudo -- mora
    aqui, uma vez so (N-01)."""

    teto = None      # bytes; None so em armazem de teste. `do_ambiente` sempre limita.

    def limitar(self, teto):
        self.teto = teto
        return self

    def existe(self, k):
        return self._existe(_validar(k))

    def ocupado(self):
        """Bytes no bucket inteiro, somados agora -- nao um contador desta rodada, que
        nao veria o que outra maquina enviou (a carga inicial roda da dele)."""
        return sum(t for _, t in self._tamanhos(""))

    def enviar_se_ausente(self, k, caminho, isento_do_teto=False):
        """True se enviou; False se a chave ja existia. Nunca sobrescreve.

        Com teto, soma o bucket antes de enviar e levanta `TetoExcedido` se este arquivo
        o levaria acima. `isento_do_teto` e so para o log da rodada: ele mede KB e e a
        prova de que a recusa aconteceu -- um teto que apaga a prova da propria recusa
        seria a guarda derrubando o que ela protege (P-102)."""
        _validar(k)
        prometido = sha_da_chave(k)
        if prometido is not None and sha256(caminho) != prometido:
            raise ConteudoDivergente(f"{caminho} nao tem o sha256 da chave {k}")
        if self._existe(k):
            return False
        if self.teto is not None and not isento_do_teto:
            ocupado, tam = self.ocupado(), os.path.getsize(caminho)
            if ocupado + tam > self.teto:
                raise TetoExcedido(
                    f"{k}: {ocupado / GB:.2f} GB no bucket + {tam / GB:.3f} GB deste "
                    f"arquivo passaria do teto de {self.teto / GB:.2f} GB")
        self._enviar(k, caminho)
        return True

    def baixar(self, k, destino):
        """Baixa para `destino`, passando por `.part`: um download interrompido nunca
        deixa arquivo com o nome certo. Chave de conteudo e conferida antes de aceitar."""
        _validar(k)
        os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
        part = destino + ".part"
        try:
            self._baixar(k, part)
            prometido = sha_da_chave(k)
            if prometido is not None and sha256(part) != prometido:
                raise ConteudoDivergente(f"{k}: o byte baixado nao tem o sha256 da chave")
            os.replace(part, destino)
        finally:
            if os.path.exists(part):
                os.remove(part)
        return destino

    def listar(self, prefixo=""):
        return sorted(self._listar(prefixo))

    @abc.abstractmethod
    def _existe(self, k): ...

    @abc.abstractmethod
    def _enviar(self, k, caminho): ...

    @abc.abstractmethod
    def _baixar(self, k, destino): ...

    @abc.abstractmethod
    def _listar(self, prefixo): ...

    @abc.abstractmethod
    def _tamanhos(self, prefixo):
        """[(chave, bytes)] de tudo sob o prefixo."""


class ArmazemMemoria(Armazem):
    """Para os testes: o mesmo contrato, num dict. `envios` conta escritas de verdade."""

    def __init__(self):
        self.objetos = {}  # chave -> bytes
        self.envios = 0

    def _existe(self, k):
        return k in self.objetos

    def _enviar(self, k, caminho):
        with open(caminho, "rb") as f:
            self.objetos[k] = f.read()
        self.envios += 1

    def _baixar(self, k, destino):
        if k not in self.objetos:
            raise KeyError(k)
        with open(destino, "wb") as f:
            f.write(self.objetos[k])

    def _listar(self, prefixo):
        return [k for k in self.objetos if k.startswith(prefixo)]

    def _tamanhos(self, prefixo):
        return [(k, len(v)) for k, v in self.objetos.items() if k.startswith(prefixo)]


class ArmazemS3(Armazem):
    """R2 (ou qualquer S3) via boto3. `cliente` e injetavel para o teste rodar sem rede
    e sem boto3."""

    def __init__(self, bucket, endpoint_url=None, access_key_id=None,
                 secret_access_key=None, cliente=None):
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        if cliente is None:
            try:
                import boto3
            except ImportError as e:
                raise ArmazemIndisponivel(
                    "boto3 nao instalado: pip install .[captura]") from e
            cliente = boto3.client("s3", endpoint_url=endpoint_url,
                                   aws_access_key_id=access_key_id,
                                   aws_secret_access_key=secret_access_key,
                                   region_name="auto")
        self._cliente = cliente

    @classmethod
    def de_ambiente(cls, env=None, cliente=None):
        env = os.environ if env is None else env
        faltam = [v for v in VARIAVEIS if not env.get(v)]
        if faltam:
            raise ArmazemIndisponivel("variaveis de ambiente ausentes: " + ", ".join(faltam))
        endpoint = env.get("R2_ENDPOINT") or \
            f"https://{env['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com"
        return cls(env["R2_BUCKET"], endpoint, env["R2_ACCESS_KEY_ID"],
                   env["R2_SECRET_ACCESS_KEY"], cliente=cliente)

    def __repr__(self):
        # nada de credencial, nem de conta: o endpoint do R2 carrega o account id
        return f"ArmazemS3(bucket={self.bucket!r})"

    def _existe(self, k):
        try:
            self._cliente.head_object(Bucket=self.bucket, Key=k)
            return True
        except Exception as e:                  # botocore.exceptions.ClientError
            codigo = str(getattr(e, "response", {}).get("Error", {}).get("Code", ""))
            if codigo in ("404", "NoSuchKey", "NotFound"):
                return False
            raise

    def _enviar(self, k, caminho):
        self._cliente.upload_file(caminho, self.bucket, k)

    def _baixar(self, k, destino):
        self._cliente.download_file(self.bucket, k, destino)

    def _listar(self, prefixo):
        return [k for k, _ in self._tamanhos(prefixo)]

    def _tamanhos(self, prefixo):
        out = []
        for pagina in self._cliente.get_paginator("list_objects_v2").paginate(
                Bucket=self.bucket, Prefix=prefixo):
            out.extend((o["Key"], int(o["Size"])) for o in pagina.get("Contents", []))
        return out


def raiz_do_repositorio():
    import manifesto_cvm
    return manifesto_cvm.raiz_do_repositorio(os.path.dirname(os.path.abspath(__file__)))


def do_ambiente(tipo="s3", env=None, raiz_repo=None):
    """O armazem que a linha de comando pede, JA COM O TETO da politica. Um tipo so hoje;
    o parametro existe para a linha de comando nao prometer o que o codigo nao tem."""
    if tipo != "s3":
        raise ValueError(f"armazem {tipo!r} desconhecido")
    _, teto = limites_da_politica(raiz_repo or raiz_do_repositorio())
    return ArmazemS3.de_ambiente(env).limitar(teto)


def copiar_para_cache(caminho, cache, k):
    """`<cache>/<chave>`: o cache local espelha o endereco do armazem."""
    destino = os.path.join(cache, *k.split("/"))
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    if not os.path.exists(destino):
        shutil.copyfile(caminho, destino + ".part")
        os.replace(destino + ".part", destino)
    return destino

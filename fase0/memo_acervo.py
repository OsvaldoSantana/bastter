# -*- coding: utf-8 -*-
"""
memo_acervo.py -- memo de sessao para leituras do acervo real de COTAHIST. P-141 (25/09/2026).

Exposto aos testes por `fase0/conftest.py` como a fixture `memo_do_acervo`.

O PROBLEMA, medido na rodada de base de 25/09 (`--durations=40`, fase0 em 537 s):
  `test_moeda` tinha dois testes chamando `moeda.relatorio(ACERVO)` com o MESMO argumento
  -- 108 s e 95 s --, e `test_calendario_p99` dois chamando `calendario.pregoes(ACERVO)`
  -- 71 s e 64 s. Quatro leituras dos 41 anos para duas respostas distintas.

A CHAVE E O CONTEUDO, NAO O CAMINHO. E a licao do S-02 (alocacao/conftest.py): havia um
cache global cuja chave era o hash do ARQUIVO, e um teste que alterava o objeto recebia o
valor calculado com o original. Aqui a chave e o sha256 de cada arquivo que
`calendario.arquivos()` devolve -- a MESMA regra de descoberta que os leitores usam (N-01):
um hash sobre `os.listdir` concordaria com ela por acidente. Trocar um ZIP no meio da
sessao muda a chave e recalcula. Custo medido: ~0,8 s para os 755 MB, contra ~100 s de
uma leitura.

CADA TESTE RECEBE UMA COPIA. O resultado memoizado e compartilhado por construcao, e e o
pior lugar para uma mutacao vazar: o segundo teste leria o que o primeiro sujou, e
falharia -- ou passaria -- longe da causa (P-38, B-12). Copiar aqui nao esconde defeito:
o memo e um detalhe de desempenho, e o contrato de cada teste continua sendo "recebi o
que a funcao devolve".

COM XDIST, o memo e POR PROCESSO. Os testes que compartilham uma chave levam
`xdist_group`, e a suite completa roda com `--dist loadgroup`: sem isso os dois testes
do par caem em trabalhadores diferentes e a leitura dupla volta, calada.
"""
import copy
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendario  # noqa: E402


def impressao_do_acervo(pasta):
    """sha256 sobre (chave, sha256 do arquivo) de tudo que `calendario.arquivos()` le."""
    h = hashlib.sha256()
    for chave, caminho in sorted(calendario.arquivos(pasta).items()):
        f = hashlib.sha256()
        with open(caminho, "rb") as fh:
            for bloco in iter(lambda: fh.read(1 << 20), b""):
                f.update(bloco)
        h.update(f"{chave}={f.hexdigest()}\n".encode("ascii"))
    return h.hexdigest()


def novo_memo():
    """`memo(rotulo, pasta, fn)` -> copia de `fn()`, calculado uma vez por conteudo."""
    guardado = {}

    def memo(rotulo, pasta, fn):
        chave = (rotulo, os.path.abspath(pasta), impressao_do_acervo(pasta))
        if chave not in guardado:
            guardado[chave] = fn()
        return copy.deepcopy(guardado[chave])

    memo.guardado = guardado      # o teste do memo mede quantas vezes calculou
    return memo

# Contexto de sessão — o que toda sessão lê, antes e depois de cada corte

*Medido por `python auditoria/tamanho_do_contexto.py` (razão de 2,96 caracteres por token, sem
`tiktoken`; ±15%, e o erro é o mesmo nas duas pontas, então a diferença vale mais que o valor
absoluto). O que é `SEMPRE` é declarado no próprio instrumento. Nenhum destes números é copiado
para o `CLAUDE.md`.*

## 26/09/2026 — a história saiu do `CLAUDE.md` e as fechadas saíram do `PENDENCIAS.md`

| arquivo | antes (linhas / tokens) | depois (linhas / tokens) | diferença |
|---|---|---|---|
| `CLAUDE.md` | 2.211 / 45.983 | 383 / 7.398 | **−38.585 (−83,9%)** |
| `PENDENCIAS.md` | 3.705 / 79.986 | 1.667 / 30.263 | **−49.723 (−62,2%)** |
| `PLANO.md` | 351 / 6.996 | 351 / 6.996 | 0 |
| `docs/doutrinas.md` | 185 / 3.478 | 185 / 3.478 | 0 |
| **leitura de sessão** | **6.452 / 136.443** | **2.586 / 48.135** | **−88.308 (−64,7%)** |

Antes: commit `c85ce59`. Depois: o commit que trouxe este arquivo.

**Para onde foi o texto** (movido, não apagado):

- `docs/historico/claude-md-ate-2026-09.md` — o `CLAUDE.md` de `c85ce59` **inteiro**, só com os
  links relativos reescritos para a pasta nova: as retratações, o índice de achados, as rodadas
  de 16 a 19/09, as §7, §10 e §11.
- `docs/historico/pendencias-fechadas.md` — os 54 blocos de pendência fechada (49 com o
  cabeçalho já riscado e 5 fechados só no corpo, riscados agora: P-69 a P-72, P-83, P-85, P-86,
  P-118), a tabela `## Fechadas`, os marcos auditáveis, o achado U-01 e as notas antigas de
  "Ao voltar ao desktop".

**Nada se perdeu, medido:** `auditoria/codigos_preservados.py` conta os códigos `LETRA-NUMERO`
e `5-B.n` em todo `.py`, `.md`, `.yaml` e `.yml`. Antes: **368 códigos, 4.374 ocorrências**.
Depois: **368 códigos, 4.415 ocorrências**, e nenhum código da linha de base sumiu. As
ocorrências sobem porque o `CLAUDE.md` novo cita códigos que o antigo também citava. A linha de
base (`auditoria/codigos_linha_de_base.txt`) só cresce; `test_codigos_preservados.py` reprova
se algum código sair do repositório, com prova por mutação e controle (mover não reprova).

**O que o corte não mede (P5):** se a sessão acha a regra de que precisa, agora que o porquê
está a um arquivo de distância. O `CLAUDE.md` vivo termina num índice (§13) que diz onde cada
pedaço da história foi morar, e as seções mantiveram a numeração antiga (§3, §5-A, §5-B, §8,
§9, §12) para que as citações espalhadas pelo código continuem apontando para o lugar certo.

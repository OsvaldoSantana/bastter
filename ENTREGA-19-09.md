# Entrega de 19/09/2026 — os arquivos finais, com hash

*Escrito porque o risco é real: os arquivos saíram em **oito mensagens** ao longo do sábado,
e há **várias versões** de `CLAUDE.md`, `PENDENCIAS.md` e `SEGUNDA-21.md` no chat. Copiar a
versão errada é a regra 12 da régua §5-B acontecendo — *arquivo que duas mãos editam não se
entrega inteiro* —, e desta vez as duas mãos são a mesma minha em horas diferentes.*

**Se um hash não bater, a versão é outra: me diga em vez de seguir.**

```powershell
cd C:\Users\osvaldo.junior\Desktop\Bastter
Get-FileHash CLAUDE.md, PENDENCIAS.md, SEGUNDA-21.md, fase0\calendario.py `
  -Algorithm SHA256 | Format-Table Hash, Path -AutoSize
```

| arquivo | destino | bytes | sha256 (12) |
|---|---|---|---|
| `.gitignore` | raiz (igual ao que já está aí) | 7,492 | `11482bf9a25d` |
| `.ruff_cache/.gitignore` | .ruff_cache\ (NOVO) | 35 | `9e3a60f1e6ec` |
| `.ruff_cache/0.16.6/1056472234131315854` | .ruff_cache\0.16.6\ (NOVO) | 172 | `0ebe88e743f9` |
| `.ruff_cache/CACHEDIR.TAG` | .ruff_cache\ (NOVO) | 43 | `5953156d7e0c` |
| `ACHADOS.md` | raiz (SUBSTITUI — os dois apêndices já colados) | 128,578 | `6e7732acedd8` |
| `CLAUDE.md` | raiz (SUBSTITUI) | 122,942 | `b53032e99c51` |
| `PENDENCIAS.md` | raiz (SUBSTITUI) | 139,712 | `9d15343e56e8` |
| `SEGUNDA-21.md` | raiz (NOVO) | 9,971 | `a03cf86a82af` |
| `alocacao/politica.yaml` | alocacao\ (igual ao que já está aí — 1.22.0) | 131,181 | `be02e1104e93` |
| `alocacao/test_p98_acervo_fora_do_indice.py` | alocacao\ (NOVO) | 6,874 | `0d7a7bfae62e` |
| `auditoria/AUDITORIA-PLANO-DE-TOKENS.md` | auditoria\ (NOVO) | 17,795 | `fcc5e3b54e19` |
| `auditoria/AUDITORIA-PREREGISTRO-ML-V1.md` | auditoria\ (NOVO) | 11,288 | `0336be33833c` |
| `auditoria/C03-A-QUEBRA-DE-MOEDA.md` | auditoria\ (NOVO) | 5,912 | `0997aaa178d4` |
| `auditoria/CACHE-E-O-CORTE.md` | auditoria\ (NOVO) | 7,381 | `286bb2caed5b` |
| `auditoria/P88-DEPENDENCIA-SERIAL.md` | auditoria\ (NOVO) | 8,163 | `e977d3dddb2d` |
| `auditoria/achados_ancorados.py` | auditoria\ (NOVO) | 7,561 | `6667c393b375` |
| `auditoria/p88_block_bootstrap.py` | auditoria\ (NOVO) | 10,159 | `1da167624656` |
| `auditoria/tamanho_do_contexto.py` | auditoria\ (NOVO — com P-110) | 8,772 | `0be3e31e7ccf` |
| `auditoria/test_achados_ancorados.py` | auditoria\ (NOVO) | 9,221 | `b6b64d9ab075` |
| `auditoria/test_p88_block_bootstrap.py` | auditoria\ (NOVO) | 10,591 | `3bc4288205ad` |
| `auditoria/test_tamanho_do_contexto.py` | auditoria\ (NOVO) | 7,482 | `0c2d001896fb` |
| `docs/acervo/b3/origem.csv` | docs\acervo\b3\ (SUBSTITUI o de 26 bytes com BOM — P-108) | 6,829 | `e76fb2430bc0` |
| `docs/fontes/b3-cotahist-leiaute.md` | docs\fontes\ (NOVO) | 6,348 | `3d2588ffacdd` |
| `docs/fontes/b3-series-historicas-cotahist.md` | docs\fontes\ (SUBSTITUI — retratação + modelo do origem.csv corrigido) | 13,996 | `17679cd755d8` |
| `docs/schemas/cotahist-v02.yaml` | docs\schemas\ (NOVO — OBRIGATÓRIO) | 6,812 | `84a414ffe5f6` |
| `fase0/calendario.py` | fase0\ (SUBSTITUI — P-99 + leiaute do YAML) | 14,317 | `7858ee559c34` |
| `fase0/manifesto_cvm.py` | fase0\ (SUBSTITUI — P-102 + P-108) | 17,541 | `6a2a58b4b4f9` |
| `fase0/moeda.py` | fase0\ (NOVO) | 10,733 | `38d9e0e9d139` |
| `fase0/test_ajustar.py` | fase0\ (SUBSTITUI — sintético com header, P-109) | 34,144 | `85654b4e2f14` |
| `fase0/test_calendario.py` | fase0\ (SUBSTITUI — idem) | 5,947 | `9729383d88f8` |
| `fase0/test_calendario_p99.py` | fase0\ (NOVO) | 11,750 | `12e5acf36a19` |
| `fase0/test_moeda.py` | fase0\ (NOVO) | 11,552 | `2efbc35d6abd` |
| `fase0/test_origem_bom.py` | fase0\ (NOVO — P-108) | 2,447 | `74b92ba73487` |
| `fase0/test_p7_captura_declarada.py` | fase0\ (SUBSTITUI) | 10,742 | `4ff8ab2b7bb8` |

**34 arquivos, gravados por mim na pasta em 21/09.** Os dois `ACHADOS-*` temporários
saíram: o conteúdo deles está dentro do `ACHADOS.md`.

> **Retratação do número de 19/09.** Esta linha dizia *"95 passed, 2 skipped"*. Era verdade
> **só na árvore de 27 arquivos que eu montei**. No repositório real a entrega reprovava
> **19** testes de `fase0` e **2** de `auditoria` (P-109, P-110, §5-B.15). Medido em 21/09
> sobre clone do `origin/main` + esta entrega: `fase0` 196 passed / 16 skipped · `auditoria`
> 42 passed · `alocacao` 514 passed / 2 failed (os dois leem `estado.yaml`, que não vai ao
> git — na sua máquina passam).

## A ordem importa em dois pontos

1. **`docs\schemas\cotahist-v02.yaml` antes de rodar `fase0`.** O `calendario.py` recusa
   rodar sem ele (`LeiauteAusente`) — é a P1, não um bug.
2. ~~Os dois apêndices no `ACHADOS.md` antes de rodar `auditoria`.~~ **Feito em 21/09** —
   colados por mim, depois de ler o `ACHADOS.md` pela primeira vez.

## O que eu NÃO pude verificar (P5) — *escrito em 19/09; o primeiro item foi medido em 21/09 e quebrava (P-109)*

`ajustar.py`, `refinar.py`, `test_ajustar.py`, `test_calendario.py`, `test_manifesto_cvm.py`
e `multiplicidade.py` **não passaram pelo container.** Dois efeitos:

- o `calendario.py` mudou de contrato (leiaute do YAML, `registros()` confere cabeçalho) e eu
  testei contra a minha suposição do que esses arquivos fazem — **é o primeiro lugar onde
  olhar se `fase0` quebrar**;
- a P-88 mediu só a marginal com Bonferroni, porque o `multiplicidade.py` (Romano-Wolf) não
  estava aqui. O `backtest_h1_h3.py` do container é **anterior a 18/09**.

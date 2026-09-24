# Bilhetes de entrega — vencidos, e guardados

Cada arquivo desta pasta foi, um dia, uma instrução na raiz do repositório: um roteiro para
ligar o computador, um pacote para descompactar, prompts para colar. **Todos foram
executados.** Ficam aqui como registro do dia, não como instrução — cada um abre com a linha
`> VENCIDO`.

**Desde 24/09/2026 bilhete de entrega não vai mais para a raiz.** O prompt vive no chat; o
registro vive em `CLAUDE.md`, `PENDENCIAS.md` e `PLANO.md`. Quem pode morar na raiz é dado:
`auditoria/raiz_viva.yaml`, guardado por `auditoria/test_raiz_viva.py`.

| bilhete | escrito | assunto | executado em (commit) |
|---|---|---|---|
| `LEIA-NA-TERCA.md` | 06–08/09 | pacote de 06/09: conferir, extrair, subir; e o adendo V-01 — coletar os eventos da B3 antes da CVM | 10–11/09 (`8b98028`; coleta em `b1d06f4`) |
| `LEIA-AGORA.md` | 10/09 | `estado.yaml` real empurrado ao GitHub: refazer o histórico antes de tornar público (P-67) | 10/09 (`8b98028`) |
| `PROMPTS-CLAUDE-CODE.md` | 11/09 | os cinco primeiros prompts do Claude Code: Y-01, P-70, P-71/72, campos mortos, proventos completos | 11/09 (`9e1aa8a` a `6378b0c`) |
| `RECRIAR-REPOSITORIO.md` | 11/09 | recriar o repositório no GitHub (público, sem inicialização) e o primeiro push | 11/09 (`b1d06f4`) |
| `LEIA-NA-SEGUNDA.md` | 12–13/09 | o pacote de segunda: zip, cinco remendos, suíte | 14/09 (`c0cbda2`) |
| `PROMPTS-E01-E03.md` | 13/09 | três prompts: E-01 (guarda do F-02 no irmão), E-02 (ausente × vazio × ilegível), E-03 (interruptores) | 14/09 (`3cd6517`, `38fcfc4`, `3c1f40e`) |
| `DEPENDE-DE-VOCE.md` | 13/09 | nove itens que dependiam dele — ver a tabela abaixo | 13–24/09 (item a item) |
| `ENTREGA-19-09.md` | 19/09 | lista de hash da entrega de 19/09, enviada em oito mensagens | 21/09 (`c6ccf2a`) |
| `SEGUNDA-21.md` | 19/09, reescrito 21/09 | roteiro de segunda depois da auditoria de 21/09 (P-108 a P-110) | 21/09 (`b54787b`) |

## Os nove itens do `DEPENDE-DE-VOCE.md`, conferidos contra o `PENDENCIAS.md` em 24/09

| item | desfecho | onde |
|---|---|---|
| 1 · custo por operação no ranking | decidido **sim** em 13/09; os zeros adormecidos fechados na P-83 (`f383770`) | o resto é a **P-84**, aberta |
| 2 · Bonferroni ou FDR | **Romano-Wolf**, 18/09 (`64a5c97`) | fechada, `alocacao/multiplicidade.py` |
| 3 · o `m` do corte | **os dois**, 18/09 (`64a5c97`) | fechada, `alocacao/preregistro.py` |
| 4 · divergência bloqueia? | **bloqueia**, 18/09 (`64a5c97`) | fechada, `preregistro.operativo()` |
| 5 · taxa do IMAB11 | lâmina do gestor, 0,25% total, `COMPLETO` (`c0cbda2`) | fechada, `custos.yaml` |
| 6 · a régua de "variante" | **sem resposta registrada** em lugar nenhum | migrou: **P-138** |
| 7 · o pacote e os cinco remendos | 14/09 (`c0cbda2` e os três commits do E-01 a E-03) | fechada |
| 8 · o COTAHIST existe? | um ano em 16/09 (`e80035e`); os 41 em 18/09 (`3ee5e97`) | fechada |
| 9 · o download da CVM | `fase0/capturar_cvm.py` (`713a2b9`); rotina diária no GitHub Actions | o resto é a **P-57** |

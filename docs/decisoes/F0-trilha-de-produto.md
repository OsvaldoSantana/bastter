# F0 — o contrato de saída entra no plano como trilha paralela de produto

**Decidida em 26/09/2026. Autor: Osvaldo.** Registrada pelo Claude Code, na sessão da nuvem que
trouxe os documentos de marca e UX para o repositório ([`docs/marca/`](../marca/README.md)).

## O que é a F0

O [mapa de telas v1](../ux/mapa-de-telas-v1.md) termina numa lista de campos que o motor ainda
não emite (§6): o tipo e o valor da decisão, o motivo curto, a recusa com o insumo e o
responsável, o funil dos portões, a procedência por número, as limitações do mês, a faixa dos
valores `PARCIAL`, a reserva, a alocação alvo e atual, o custo de discordar e as impressões.
A F0 é o **esquema desse relatório de decisão**: o contrato entre o motor e qualquer tela.

## A pergunta

O mapa classificava a F0 como `BLOQUEIA_O_SISTEMA` e a propunha como próximo passo. O
`PLANO.md` não tinha trilha de produto nenhuma, e ele ganha de qualquer fila (`CLAUDE.md` §1).
Onde a F0 entra, e com que prioridade?

## As alternativas

| opção | o que acontece | consequência |
|---|---|---|
| **A · trilha paralela agora** (escolhida) | a F0 entra no `PLANO.md` fora da fila do motor, com regra escrita de não disputar o caminho crítico | a interface ganha dono e ordem sem atrasar a P-115; o risco é a trilha virar a engenharia que "sobrou", e a regra abaixo existe para isso |
| B · esperar a P-115 fechar | a F0 fica em `DECISAO_DE_DESENHO` até o critério C-02 v2 ser medido | nada de produto anda enquanto o motor espera a sessão local; os requisitos e o mapa envelhecem sem contrato |
| C · a F0 no caminho crítico, como o mapa propunha | a F0 vira `BLOQUEIA_O_SISTEMA` | falso: o motor decide sem ela. A F0 bloqueia a **interface**, não o sistema (U-01: um cliente novo precisa do motor antes da tela) |

> **Nota de 26/09/2026.** O formulário que ele respondeu teve **duas opções, A e B**. A
> opção C não foi oferecida a ele: é uma alternativa técnica, registrada aqui para completar
> o desenho, e **rejeitada pelo claude.ai** antes da pergunta, pelo motivo da última coluna.

## A decisão, e as regras que vêm com ela

1. **A F0 é trilha de produto paralela** (`PLANO.md` §3-F0), e **não bloqueia o motor**.
2. **Não disputa o caminho crítico com a P-115.** Numa sessão em que as duas couberem, a P-115
   vai primeiro; a F0 não é motivo para adiar a sessão local que a P-115 pede.
3. **O primeiro entregável é uma especificação em `docs/ux/`, não código.** O esquema escrito,
   campo a campo, com o tipo, a origem no motor e a tela que o usa. Código de esquema só depois
   de a especificação ser lida por ele.
4. **Campo sem tela não entra; tela sem campo não se constrói** (a regra da §6 do mapa).
5. **Não conta como a engenharia que destrava** para a regra do próximo passo (`CLAUDE.md`
   §5-A.5): a trilha paralela não é desculpa para empilhar engenharia.

## Consequência para o registro

- O mapa de telas perdeu o `BLOQUEIA_O_SISTEMA` (nota N-F0 no fim dele).
- A fila do Osvaldo registra a decisão ([`fila-do-osvaldo.md`](fila-do-osvaldo.md)).
- As pendências que a trilha puxa (WCAG, teste com pessoas, importação de carteira, parecer
  jurídico, CVM 19) entraram no `PENDENCIAS.md` como P-153 a P-159, todas
  `DECISAO_DE_DESENHO`.

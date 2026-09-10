# Onde a rotina semanal vai rodar — pesquisa de 06/09/2026
Pergunta do Osvaldo: *"subir o projeto para um servidor nao resolveria isso? tipo supabase?"*
Metodo: subagente, com ordem de nao inventar limite e de marcar NAO_CONFIRMADO.
Status: por linha. Os numeros abaixo vieram de paginas oficiais de preco/limite.
Fecha (em parte): P-57.

---

## A resposta curta

**Servidor resolve o gatilho. Nao resolve a rede nem o disco — e o Supabase, especificamente,
e a PIOR escolha da lista para uma rotina semanal.** Nao por ser ruim: por um detalhe que
so aparece quando se le a pagina de limites.

## O detalhe que decide, e ele e contra-intuitivo

> **Supabase Free: "Free projects are paused after 1 week of inactivity."**
> Restauracao **manual, pelo dashboard**.

Uma rotina **semanal** vive exatamente em cima desse limiar. Se ela atrasar um dia, ou
falhar uma vez, o projeto pausa — e alguem tem que ir la clicar. **Isso e a doutrina P7
violada pela propria infraestrutura:** o sistema passaria a depender de uma pessoa
perceber que ele parou.

E mesmo se a pausa nao existisse, as Edge Functions nao dao conta do trabalho:

| limite (Free) | valor | o que a rotina precisa |
|---|---|---|
| tempo de execucao | **150 s** | baixar e descompactar ~1,5 GB |
| memoria | **256 MB** | idem |
| CPU | **2 s** | comparar CSVs de milhoes de linhas |
| upload por arquivo (Storage) | **50 MB** | ZIPs de centenas de MB |
| Storage total | **1 GB** | — |
| egress | **5 GB/mes** | — |

Supabase e otimo no que ele e: banco Postgres gerenciado com API. **Ele nao e um executor
de tarefa pesada**, e a Fase 0 e tarefa pesada por natureza.

## A resposta que os numeros apontam

**GitHub Actions, em repositorio PRIVADO, faz as tres coisas sozinho.**

| | valor | fonte |
|---|---|---|
| agendador | `on: schedule`, cron nativo | COMPLETO |
| disco temporario do runner | **14 GB SSD** | COMPLETO |
| RAM / CPU (repo privado) | 8 GB / 2 vCPU | COMPLETO |
| duracao maxima de um job | **6 horas** | COMPLETO |
| minutos gratuitos (repo privado) | **2.000/mes** | COMPLETO |
| banda de download para o runner | nao tarifada | COMPLETO |
| pausa por inatividade | **nao existe em repo privado** | COMPLETO |

Consumo estimado da rotina: 20–40 min por execucao × ~4,5 semanas = **100 a 200 dos 2.000
minutos**. Folga de 10×.

## A inversao que ninguem espera, e ela e o achado desta pesquisa

> *"In a **public** repository, scheduled workflows are automatically disabled when no
> repository activity has occurred in 60 days."*

A regra dos 60 dias que mata cron por inatividade **so vale para repositorio publico**.
Em repositorio **privado**, o cron nao e desativado.

**Ou seja: privado e MAIS confiavel que publico para automacao.** Isso e o contrario da
intuicao — e converge com a restricao que o projeto ja tinha por outro motivo
completamente diferente: `alocacao/estado.yaml` guarda a situacao financeira real do
Osvaldo, e o repositorio **precisa** ser privado.

**Duas restricoes independentes apontando para a mesma decisao e o tipo de coincidencia
que vale registrar** — ela transforma "privado por precaucao" em "privado por desenho".

## O redesenho que torna o armazenamento um nao-problema

A pergunta comecou errada, e a culpa e minha: eu falei em "disco" como se fosse preciso
guardar um snapshot completo por semana. Nao e.

| desenho | por semana | por ano |
|---|---|---|
| guardar o ZIP inteiro toda semana | centenas de MB | **dezenas de GB** |
| guardar **so as linhas que mudaram** | KB a poucos MB | **poucas centenas de MB** |

A reapresentacao e uma fracao minuscula do arquivo. O que o backtest ponto-no-tempo
precisa **nao e o arquivo** — e o **historico de mudancas**. Baixar 1,5 GB, comparar,
guardar o delta e jogar o resto fora e a operacao certa, e ela cabe num runner efemero.

**Consequencia: o proprio git vira o armazenamento permanente.** Delta e texto, versionado,
diffavel, de graca, e **nao consome** a cota de 500 MB de artifacts (aquela cota e so para
artifacts e Packages, nao para o repositorio).

Se um dia for preciso guardar os ZIPs brutos, **Cloudflare R2** e o destino certo:
10 GB-mes gratis e **egress sempre zero** — perfil exato de "escreve toda semana, le
raramente". O Backblaze B2 tambem tem 10 GB, mas limita egress gratuito a 3× o armazenado.

## Descartados, com motivo

| plataforma | por que nao |
|---|---|
| **Supabase Free** como executor | pausa em 1 semana; 150 s; 256 MB; upload de 50 MB |
| **Vercel Hobby** (ele ja tem conta) | cron no maximo **1×/dia**, funcao de **300 s**, resposta limitada a 4,5 MB, sem disco |
| **Cloudflare Workers** | **10 ms de CPU** por invocacao de cron |
| **Render**, **Fly.io** | sem free tier |
| **Cloud Run Jobs + Scheduler** | tecnicamente capaz (ate 32 GiB, timeout longo), mas cobra egress e adiciona conta e faturamento para um ganho nulo sobre o Actions |

## As armadilhas de confiabilidade — e uma delas e o F-02 outra vez

1. **Repositorio publico morre em 60 dias.** Mantido privado, nao ocorre.
2. **`on: schedule` atrasa ou pula execucao em horario de pico.** Nunca dependa do minuto;
   a rotina tem que ser **idempotente** e trabalhar por janela, nao por instante.
3. **Estouro dos 2.000 min/mes interrompe sem aviso util.**
4. **14 GB e o limite real do disco:** descompactar **um ZIP por vez**, apagando antes do
   proximo. Seis de uma vez nao cabem.
5. **Retencao de artifacts e de 90 dias** — artifact nao e armazenamento permanente.
6. **A falha silenciosa, e e a mesma familia do F-02 e do endpoint da B3:** um `curl` que
   devolve 404 e um `unzip` vazio produzem, juntos, **"nenhuma mudanca"** — que e
   indistinguivel de "a CVM nao mudou nada esta semana". Um sistema que trate as duas
   coisas como iguais registra uma semana de silencio como uma semana de estabilidade.
   Exigencias: `set -euo pipefail`, conferencia de tamanho e de sha256, e notificacao em
   `if: failure()`. **Ausencia de mudanca precisa ser afirmada, nao inferida da ausencia
   de erro.**

## NAO_CONFIRMADO

- Limite de tamanho de asset de release do GitHub.
- Comportamento do Supabase Free ao estourar DB/Storage/egress.
- Se `pg_cron`/Supabase Cron esta disponivel no Free (a doc nao restringe, mas tambem nao
  confirma).
- Se o free tier do Cloud Run cobre Cloud Run **Jobs**.
- Nada disto foi testado por mim: sao paginas de limite lidas, nao execucao observada. A
  primeira execucao real e que vira COMPLETO.

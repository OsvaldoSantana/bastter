# Politica de atualizacao do DFP — CONFIRMADA na fonte
Fonte: https://dados.cvm.gov.br/dataset/cia_aberta-doc-dfp
Acesso: 06/09/2026, pelo navegador do Osvaldo; ele colou a pagina inteira na conversa.
Metodo: **leitura humana**. O portal responde ROBOTS_DISALLOWED as minhas ferramentas.
Status: **COMPLETO** — a CVM declara o proprio comportamento, por escrito, na pagina do
conjunto. Isto FECHA o `NAO_CONFIRMADO` que estava aberto desde 03/09/2026.
Fecha: a pergunta "a CVM sobrescreve os arquivos anuais?" — resposta: **sim, semanalmente,
e so nos ultimos cinco anos.**
Licenca: **ODbL** (Open Data Commons Open Database License) — atencao a clausula de
compartilhamento pelo mesmo regime se algum derivado for publicado.

---

## As duas frases que decidem tudo

Transcritas literalmente da pagina:

> *"O conjunto de dados disponibiliza as seguintes demonstracoes financeiras entregues
> **nos ultimos cinco anos**"*

> *"Os arquivos serao **atualizados semanalmente** com as eventuais **reapresentacoes**."*

> *"**Historico desde 2010** (incluindo arquivos **nao sujeitos a politica de
> atualizacao**)"*

E o campo estruturado, no rodape da pagina:

| campo | valor |
|---|---|
| Periodicidade de atualizacao | **Semanal** |
| Ultima Atualizacao | **31 de agosto de 2026, 08:01 (UTC-03:00)** |
| Criado | 29 de julho de 2020, 20:43 |
| Autor | SEP — Superintendencia de Relacoes com Empresas |
| Base de Dados | Documentos Periodicos e Eventuais de Regulados |
| Licenca | ODbL |

## O acervo se parte em dois, e so metade tem prazo

Isto e o achado, e ele **estreita** a urgencia em vez de ampliar:

| faixa | quantos arquivos | comportamento | urgencia |
|---|---|---|---|
| **2021–2026** (os "ultimos cinco anos") | **6** | reescritos **toda semana** com reapresentacoes | **alta, e e continua** |
| **2010–2020** | 11 | **nao sujeitos a politica de atualizacao** — congelados | **nenhuma** |

A propria pagina confirma a divisao pelo numero de recursos: ela lista **6** arquivos
"Formularios de Demonstracoes Financeiras", nao 17. Os 11 antigos existem no diretorio
(`.../DFP/DADOS/`) mas **nao sao recursos do conjunto** — e exatamente o que a frase
"incluindo arquivos nao sujeitos a politica de atualizacao" quer dizer.

**Consequencia pratica, e ela muda o plano de download:**

- o que tem prazo sao **6 arquivos**, nao 1,5 GB de 17;
- o prazo nao e anual, e **semanal**. Cada semana sem snapshot e uma rodada de
  reapresentacoes que deixou de ser observavel;
- a cauda 2010–2020 pode ser baixada quando der, inclusive depois. Ela nao muda.

## O que a reapresentacao destroi, em uma frase

Uma reapresentacao substitui o numero **entregue** pelo numero **corrigido**, dentro do
arquivo do ano a que ela se refere — e um ano de cinco atras ainda esta na janela. Ou
seja: **o `dfp_cia_aberta_2022.zip` de hoje nao e o `dfp_cia_aberta_2022.zip` de
2023.** Quem baixar so hoje nao tem como saber o que a empresa dizia em 2023, e um
backtest que decida uma compra de 2023 com o numero corrigido em 2026 esta usando
informacao do futuro.

`DT_RECEB` nao salva disso: ela diz quando o registro **sobrevivente** chegou, nao o que
o substituido dizia.

## Uma observacao antiga que isto explica

O projeto tinha registrado, em `cvm-enumeracoes-observadas.md`, que
`composicao_capital` **so aparece na safra de 2024** — e deixou a explicacao em aberto.

A explicacao provavel esta aqui: a pagina diz que o conjunto "tambem disponibiliza as
secoes Pareceres e Declaracoes e **Dados da Empresa/Composicao do Capital**". Se so os
ultimos cinco anos sao regerados, as safras congeladas de 2012 e 2019 ficaram no formato
antigo, **anterior a inclusao dessa secao**, e nunca serao regeradas.

**Isto e inferencia minha, nao leitura** — a pagina nao diz em que ano a secao entrou.
Mas ela transforma "a estrutura muda entre safras sem motivo" em "a estrutura de uma
safra congelada e a do dia em que ela congelou", que e uma regra e nao um susto.
NAO_CONFIRMADO: o ano exato de entrada da secao.

## Base legal, para o `trecho_conferido`

A pagina cita, e a citacao e utilizavel diretamente na procedencia do projeto:

- **Resolucao CVM n. 80/22, art. 22, IV** — o DFP e documento de encaminhamento
  periodico obrigatorio;
- **Resolucao CVM n. 80/22, art. 30** — o formulario e preenchido com as demonstracoes
  elaboradas conforme as regras contabeis aplicaveis ao emissor (arts. 27 a 29).

## O que continua NAO_CONFIRMADO

- **O ITR.** Toda esta pagina e do DFP. A politica do ITR esta na pagina **dele**
  (`.../dataset/cia_aberta-doc-itr`) e nao foi lida. Presumir que e igual seria
  exatamente o erro que este arquivo acabou de corrigir. **E a proxima pagina a abrir.**
- Se a janela de cinco anos e movel por ano-calendario ou por data de entrega.
- Se um arquivo sai da janela e congela no estado em que estava, ou e regerado uma
  ultima vez ao sair.

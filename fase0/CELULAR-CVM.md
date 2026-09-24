# O que voce pode fazer do celular — e vale mais do que parece

> ⚠ **RETRATAÇÃO — 24/09/2026:** tratada como manual; um script na máquina dele resolve. A limitação era da ferramenta de quem respondia, não da tarefa. Hoje é `py -3.11 fase0/capturar_cvm.py` (CLAUDE.md §3, §5-B.17).

> **ATUALIZADO 06/09/2026, 17h40 — a Tarefa 1 foi feita e a minha suposicao estava
> errada.** A listagem da CVM **nao tem colunas de data e tamanho**; nao e um indice
> Apache, e uma pagina montada por eles. Confirmou-se o intervalo (2010 a 2026, 17
> arquivos), mas a pergunta do prazo continua aberta.
> **O que substitui a Tarefa 1:** rolar a mesma pagina um pouco para baixo e fotografar
> o paragrafo que comeca com *"Os arquivos de dados serao atualizados conforme a
> politica..."*. E a CVM declarando o proprio comportamento — vale mais que qualquer
> carimbo de tempo. Ver `docs/fontes/cvm-listagem-dfp-2026-09-06.md`.



**Resposta curta: sim, e o que voce pode fazer do celular e exatamente a parte que eu
nao consigo fazer daqui.**

O portal da CVM bloqueia o meu acesso automatico (`robots.txt` — a regra que os sites
publicam dizendo o que robo pode ou nao ler). Eu nao contorno isso: e regra de operacao
minha e nao vou burlar. Mas o bloqueio vale para robo, **nao para pessoa com navegador**.
Voce abre a mesma pagina e le em dez segundos o que eu nao consigo ler de jeito nenhum.

Sao tres tarefas. A primeira leva 2 minutos e **decide se a Fase 0 e urgente ou nao**.

> **Aviso antes de comecar:** nao toque nos links que terminam em `.zip`. Cada um tem
> centenas de MB e vai comer seu 4G. A informacao que eu preciso esta na **listagem**,
> nao dentro dos arquivos.

---

## Tarefa 1 — a listagem dos arquivos anuais (2 min, alta prioridade)

1. Abra o navegador do celular (Chrome, Samsung Internet, o que voce usa).
2. Cole exatamente este endereco:

   ```
   https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/
   ```

3. Vai aparecer uma **lista de arquivos** — provavelmente uma tabela simples, sem enfeite,
   com nome do arquivo, data e tamanho. E feia de proposito; e um indice de diretorio.
4. **Vire o celular na horizontal.** Se as colunas de data e tamanho nao aparecerem,
   abra o menu do navegador (tres pontinhos) e marque **"Site para computador"** /
   **"Versao para desktop"**. Isso quase sempre resolve.
5. **Tire dois ou tres prints** cobrindo a lista inteira, do primeiro ao ultimo arquivo,
   e me mande.

Se preferir digitar em vez de mandar print, me diga estas quatro coisas:

- **Qual o primeiro ano** que aparece (o mais antigo) e **qual o ultimo**.
- A linha do **`dfp_cia_aberta_2026.zip`**: qual a data ao lado dele e qual o tamanho.
- A linha do **`dfp_cia_aberta_2024.zip`**: data e tamanho.
- A linha do **`dfp_cia_aberta_2012.zip`**: data e tamanho.

### Por que isso importa, sem enrolacao

O arquivo do ano corrente e **mutavel**: empresa que entrega balanco errado reentrega,
e a versao antiga provavelmente some. Se a data ao lado do `2026.zip` for **recente**
(dias ou semanas atras) e a do `2012.zip` for **antiga** (anos), fica confirmado: a CVM
reescreve o arquivo do ano corrente o tempo todo, e **cada dia sem copia guardada e um
dia de historia que nao volta**. Se, ao contrario, todos os arquivos tiverem data
parecida e antiga, o prazo relaxa muito e eu paro de tratar isso como urgencia.

Hoje isso esta registrado no projeto como `NAO_CONFIRMADO`, e ele trava a decisao de
quando baixar 1,5 GB. Sua foto fecha essa pendencia.

---

## Tarefa 2 — a mesma coisa para o ITR (1 min)

Mesmo procedimento, outro endereco:

```
https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/
```

Print da lista. So quero conferir se o comportamento e o mesmo dos dois lados.

---

## Tarefa 3 — o catalogo (5 min, opcional mas destrava bastante)

Este e o que mais amplia o projeto. Endereco:

```
https://dados.cvm.gov.br/dataset
```

E uma pagina de busca com centenas de conjuntos de dados. Na caixa de busca, procure
**um de cada vez** e me diga se **existe** e qual o titulo exato:

| busque por | o que e, e para que serve aqui |
|---|---|
| `FRE` ou `formulario de referencia` | remuneracao de diretoria, composicao acionaria, fatores de risco |
| `FCA` ou `formulario cadastral` | dados cadastrais da companhia |
| `IPE` | fatos relevantes e comunicados **com data** — serve para datar eventos |
| `VLMO` | compra e venda de acoes por controladores e diretores |
| `cad_fi` ou `cadastro de fundos` | cadastro de fundos — **pode conter a taxa de administracao dos ETFs**, que e uma pendencia aberta (P-05) |
| `informe diario` | cota diaria e patrimonio de todo fundo |

Se algum deles abrir e mostrar uma lista de arquivos, **print**. O `cad_fi` e o mais
valioso dos seis: se a taxa de administracao estiver la, fecha a P-05 com um download em
vez de quinze PDFs de regulamento.

---

## O que eu faco com isso

- Tarefa 1 e 2 -> fecho o `NAO_CONFIRMADO` do prazo e decido a ordem da Fase 0.
- Tarefa 3 -> escrevo `docs/fontes/cvm-catalogo.md`, e o projeto passa a saber o que existe
  antes de precisar.

E se voce nao fizer nada disso, tambem esta certo: o `fase0.ps1 -SoConferir` responde a
Tarefa 1 sozinho na terca. **O celular so antecipa a resposta em dois dias.**
Antecipar dois dias importa porque, ate a resposta chegar, eu nao sei se estou correndo
de um prazo real ou de um prazo imaginario — e essa duvida ja custou uma sessao inteira
de planejamento.

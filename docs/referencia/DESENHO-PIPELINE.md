# Desenho do pipeline — de 8 mil proventos a uma série ajustada

Escrito em 12/09/2026, quando o acervo de eventos fechou em 74/74.
Status: **especificação**. Nada implementado. As decisões marcadas `DECIDIDO` vêm da
pesquisa de 06/09 (`docs/fontes/pesquisa-bases-e-apis-2026-09.md`); as marcadas
`A DECIDIR` são suas.

---

## 1. O que existe, e é mais do que parece

```
data/bronze/b3/
  indices/dt_captura=2026-09-11/IBOV.json         76 ativos, ref B3 11/09
  eventos/dt_captura=2026-09-11/<EMISSORA>.json   74 emissoras
  proventos/dt_captura=2026-09-11/<EMISSORA>/pagina-NNN.json   ~8.000 registros
  manifesto.jsonl                                 sha256, URL e forma do nome
```

**O achado que muda o plano:** cada registro de provento traz
`closingPricePriorExDate` — o fechamento na véspera do ex — **no próprio registro**.

> **Isso significa que a série de FATORES DE AJUSTE pode ser construída inteira sem
> tocar no COTAHIST.** O preço só entra depois, para *aplicar* o fator. As duas metades
> do problema se separam, e a metade difícil já está no disco.

---

## 2. A conta, escrita

### Provento em dinheiro

```
fator = (P_vespera − valor_provento) / P_vespera
```

onde `P_vespera` = `closingPricePriorExDate` e a data é `lastDatePriorEx` — **a data ex,
nunca `paymentDate`**. Quem usa a data de pagamento erra em semanas, e o erro é sistemático.

### Desdobramento, grupamento, bonificação — **NÃO CALCULADO. Achado C-01.**

Este trecho dizia `fator = 1 / factor`, com a PETR de 2008 como exemplo. **Estava errado,
ou pelo menos indefensável**, e a correção veio ao implementar:

```
leitura percentual     fator = 1/(1 + factor/100)   # factor=100 -> 0,5
leitura multiplicador  fator = 1/factor             # factor=100 -> 0,01
```

**As duas produzem número e diferem por cinquenta vezes.** Não há documentação da B3
sobre o campo, e o suplemento — única fonte desses eventos — **não traz preço de véspera**
para desempatar.

`refinar.py` grava `ratio` cru e devolve `fator_status = FACTOR_AMBIGUO`. A desambiguação
é **medição**: com o COTAHIST, a razão entre o fechamento de 24/04/2008 e o de 25/04/2008
responde em uma consulta — e em pelo menos três emissoras com `factor` diferente, porque
uma coincidência não é regra.

### Série acumulada

O preço de uma data antiga, em termos de hoje, é o preço bruto multiplicado por **todos
os fatores de eventos posteriores a ela**:

```sql
-- fator acumulado, por ativo, do futuro para o passado
SELECT cod, data_ex,
       exp(sum(ln(fator)) OVER (PARTITION BY cod ORDER BY data_ex DESC
                                ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING))
       AS fator_acumulado
FROM eventos
```

> **Por que `exp(sum(ln))` e não `product()`:** oito mil fatores multiplicados em ponto
> flutuante acumulam erro; em log, somam. E `DuckDB` não tem `product()` de janela.
> Isto é decisão de precisão, não de estilo — e vale um comentário no código, porque a
> forma óbvia parece mais simples e é pior.

### A armadilha que quase ninguém vê

**Ajustar preço não basta: o retorno depende do que você faz com o dinheiro.** A série
ajustada por proventos assume **reinvestimento integral no dia ex, sem custo e sem
imposto**. Nenhuma das três é verdade na carteira dele.

`DECIDIDO` — o projeto guarda **preço bruto + tabela de eventos**, e o ajuste é feito
**em tempo de consulta**, nunca gravado. Guardar série ajustada congela três premissas
dentro de um número, e é exatamente o que a P1 proíbe.

---

## 3. As três camadas

| | o que é | formato | muda? |
|---|---|---|---|
| **bronze** | o byte como a B3 devolveu | JSON, como está | **nunca** |
| **silver** | tipado, normalizado, bitemporal | **CSV** por captura — ver nota | recriável do bronze |
| **gold** | fator acumulado por ativo e data | Parquet ou view | recriável do silver |

> **CSV e não Parquet, e a decisão mudou ao implementar.** Para 8 mil linhas o CSV ganha
> duas vezes: não acrescenta `pyarrow` — que mudaria a impressão do ambiente (P-15) sem
> que este módulo produza número de backtest — e é **diffável no git**, o que faz o
> instantâneo dourado custar um `git diff` em vez de um script de comparação. Quando o
> COTAHIST entrar com milhões de linhas, a conta inverte.

**Regra que sustenta tudo:** silver e gold são **artefatos reconstruíveis**. Apagar os
dois e rodar `python -m fase0.refinar` tem de devolver byte por byte o mesmo resultado.
Se não devolver, há estado escondido — e o instantâneo dourado do §9 é como se prova.

### Esquema do silver — **o que o `refinar.py` realmente grava**

```
origem          suplemento | paginado   -- as duas esteiras coexistem e podem DISCORDAR
cod             emissora, 4 caracteres (B3SA, nunca BSA — A-01)
code_cvm        a chave ESTAVEL: o ticker muda, esta nao (A-03)
trading_name    sem o padding de 12 posicoes da B3
isin            o suplemento identifica a classe por ISIN
type_stock      ON | PN | UNT — o paginado identifica por sigla
tipo            DIVIDENDO | JRS CAP PROPRIO | RENDIMENTO
                DESDOBRAMENTO | GRUPAMENTO | BONIFICACAO | SUBSCRICAO
data_ex         lastDatePrior / lastDatePriorEx — NUNCA paymentDate
data_aprovacao
data_pagamento
valor           Decimal exato, nunca float
ratio
preco_vespera   closingPricePriorExDate — so o paginado traz
fator           vazio quando nao calculavel; NUNCA zero
fator_status    CALCULADO | SEM_PRECO | FACTOR_AMBIGUO | SEM_FATOR | PRECO_INVALIDO
dt_captura      tempo de SISTEMA: quando NOS vimos
arquivo_origem
sha256_origem   liga a linha ao arquivo bronze que a produziu
```

> **`fator_status` é a coluna que impede a tabela de mentir por omissão**, e ela não
> estava neste desenho — nasceu ao implementar. Sem ela, um `fator` vazio seria
> indistinguível entre "não há preço para calcular", "o campo é ambíguo" e "este evento
> não ajusta preço". Três ausências diferentes viravam a mesma célula vazia.
>
> **O `isin` e o `type_stock` também nasceram na implementação**, e pelo mesmo motivo: o
> suplemento identifica a classe por ISIN (`BRABEVACNOR1`) e o paginado por sigla (`ON`).
> Derivar um do outro seria inventar — o padrão do ISIN brasileiro sugere a leitura, mas
> sugestão não é fonte. Guardam-se os dois, preenchidos por quem os tem.

> **`type_stock` é a coluna que separa este desenho de um errado.** Bradesco paga
> valores diferentes para ON e PN, e o registro vem por classe. Agregar por emissora
> mistura duas séries — e o erro fica invisível, porque o número continua plausível.

---

## 4. Decisões de formato — todas com consequência

| | decisão | por quê |
|---|---|---|
| valor monetário | **`DECIMAL`, nunca `DOUBLE`** | `0.1 + 0.2 ≠ 0.3`; oito mil somas acumulam |
| decimal brasileiro | `"0,65"` → trocar vírgula por ponto **antes** do cast | `CAST('0,65' AS DECIMAL)` falha ou trunca |
| milhar | `"15.468.781.313,18"` — remover pontos primeiro | a ordem das duas trocas importa |
| data | `dd/MM/yyyy` → `strptime(x, '%d/%m/%Y')` | `CAST` interpreta como ISO e inverte dia/mês **em silêncio nos dias ≤ 12** |
| encoding | CVM é **ISO-8859-1**; a B3 devolve UTF-8 | duas fontes, dois tratamentos |
| ausente | `NULL`, **nunca zero** | é o F-02 inteiro numa linha |

> A linha da data é a mais perigosa da tabela. `05/09/2026` lido como ISO vira 5 de
> setembro **ou** 9 de maio, dependendo do parser — e nos dias ≤ 12 **as duas leituras
> são datas válidas**. O erro não levanta exceção; ele produz uma série deslocada.
> Teste obrigatório: uma data com dia > 12 **e** uma com dia ≤ 12.

---

## 5. O que falta, e é metade do problema

**O COTAHIST.** Temos os eventos; não temos os preços. Sem série de preços não há o que
ajustar.

`A CONFERIR, e é a primeira coisa:` o `CLAUDE.md` §4 diz que `data/` tem ~1,5 GB de
CVM e COTAHIST. Se o COTAHIST de verdade já estiver lá, o pipeline anda hoje. Se não,
é um download, e ele é gratuito e não tem prazo — ao contrário do que já foi capturado.

```powershell
Get-ChildItem data -Recurse -Filter "COTAHIST*" | Select-Object FullName, Length
```

**As outras lacunas, todas declaradas e nenhuma bloqueante:**

- **viés de sobrevivência** — a carteira é a de 11/09/2026. Um backtest longo compra
  empresas que entraram no índice **depois** de darem certo. Não se conserta coletando
  daqui para frente; declara-se.
- **MBRF sem eventos (A-03)** — o histórico está sob `MRFG`. Vale para toda troca de
  código, e `code_cvm` é a ponte.
- **janela do suplemento** — `GetListedSupplementCompany` traz uma janela recente; o
  histórico longo veio do paginado. As duas fontes coexistem no bronze e **podem
  discordar**. Quando discordarem, é achado, não empate.
- **sem PIT antes de 11/09/2026** — backtest anterior é reconstrução, não observação.

---

## 6. DECIDIDO em 12/09/2026 — e uma das perguntas estava mal feita

### 1. JCP entra **líquido** · `DECISAO_DO_USUARIO`

A série de retorno total usa o JCP **depois** do IR retido na fonte. Dividendo entra
cheio; `JRS CAP PROPRIO` entra descontado.

> **Mas a decisão não pode ser implementada ainda, e o motivo é a P1.** A decisão é dele
> e está registrada. **O número que a executa não tem procedência no projeto.**
>
> Fui conferir e o quadro é este:
> - a alíquota que o mercado cita é **15% retidos na fonte**, da **Lei 9.249/1995,
>   art. 9º, §2º** — e **essa lei não está em `docs/fontes/`**. Nunca foi lida aqui;
> - a **Lei 15.270/2025** (que o projeto **tem** transcrita) **não menciona JCP** —
>   conferi o texto no Planalto. Ela tributa **lucros e dividendos em 10% na fonte** e
>   altera as Leis 9.249/1995 e 9.250/1995, mas o dispositivo do JCP é o art. 9º, e o de
>   dividendos é o art. 10;
> - há material secundário anunciando *"novas regras no JCP a partir de 2026"*, o que
>   sugere alteração vinda de **outra norma** — possivelmente na base de cálculo, não na
>   alíquota. **Não conferi, e não vou supor.**
>
> **Consequência operacional:** `custos.yaml` ganha `ir_jcp_fonte` com
> `status: NAO_CONFIRMADO` e `bloqueia: ["serie_retorno_total_liquida"]`. A série bruta
> roda; a líquida **recusa-se a rodar** até a lei ser lida. É o F-02 sendo evitado de
> propósito: sem o número, não se inventa 15%.
>
> **Fechar custa uma leitura** do art. 9º da Lei 9.249/1995 no Planalto, com transcrição
> de trecho — o mesmo ritual das outras 43 constantes.

### 2. FII — **a pergunta estava mal feita, e o erro é meu**

Eu perguntei *"`RENDIMENTO` entra na mesma série?"* como se fosse decisão de **ingestão**.
Não é. É decisão de **consulta**.

A resposta dele — *"não sei exatamente"* — é a resposta certa para uma pergunta que não
precisava ser respondida agora. O silver guarda a coluna `tipo`; **quem consulta escolhe**
se soma, separa ou ignora. Decidir na ingestão **congelaria no dado** o que é escolha, e
isso é a P2 invertida: parâmetro virando código.

**Nada a decidir.** Guarde o tipo, não agregue. Quando alguém for somar, aí sim há uma
escolha, e ela será declarada naquele ponto — com o custo de discordar mensurável.

### 3. Desdobramento × bonificação · `DECISAO_DO_USUARIO`

> *"deve ser feito o de calcular IR, mas desdobramento é mudança de quantidade de ações"*

**Está certo, e a distinção é mais fina do que a minha pergunta sugeria.** Separando as
duas coisas que eu tinha misturado:

| | efeito no **preço** | efeito na **base de custo** |
|---|---|---|
| **desdobramento / grupamento** | `fator = 1/ratio` | base por ação divide ou multiplica. **Sem fato gerador** |
| **bonificação** | `fator = 1/ratio` — **idêntico** | a empresa **atribui um valor** às ações novas, e esse valor **entra** na base |

**Para a série de preços, os dois são o mesmo fator.** A diferença vive na base de custo
— que é outra tabela, para outro fim (IR na venda), e que o projeto **já declara como não
modelada** em `politica.yaml → limitacoes_declaradas`.

**O que muda no desenho:** nada no cálculo, e uma linha no esquema —
`tipo` **preserva a distinção** entre `DESDOBRAMENTO` e `BONIFICACAO` mesmo os dois
gerando o mesmo fator. Apagar a diferença porque o fator coincide seria perder a
informação exatamente onde ela vai fazer falta: no dia em que a limitação do IR na venda
for fechada.

> Isto é a P6 aplicada a uma coluna: **ausência de régua hoje não autoriza descartar o
> dado que a régua vai precisar.**

## 7. A ordem, e o primeiro passo é pequeno de propósito

1. **Conferir se o COTAHIST existe** no `data/` — um comando.
2. **`refinar.py`: bronze → silver de eventos.** Só os ~8.000 registros de proventos e
   desdobramentos, com os casts da §4 e os testes deles. **Sem preço ainda.**
   É pequeno, é testável sem rede, e produz a primeira tabela consultável do projeto.
3. **Fator acumulado por `(cod, type_stock)`** — a consulta da §2, virando a camada gold.
4. **Só então o COTAHIST**, e o `ASOF JOIN` que aplica o fator ao preço.
5. E aí — e só aí — o backtest pré-registrado tem insumo.

> **Por que o passo 2 não inclui o preço.** Porque ele fecha sozinho: dá para conferir
> o fator da PETR de 25/04/2008 contra o desdobramento 100:1 **sem nenhuma série de
> preços**. Um passo que se verifica sozinho vale mais que um passo grande que depende
> de outro para ser julgado — e este projeto já mediu o custo do contrário.

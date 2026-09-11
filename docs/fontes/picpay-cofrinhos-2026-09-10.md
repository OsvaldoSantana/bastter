# Cofrinhos do PicPay — observado no app em 10/09/2026
Fonte: capturas do aplicativo PicPay, telas "Cofrinhos" e "Cofrinho Turbinado", 10:14.
Status: **OBSERVADO** — lido na tela do produto, não em documento do emissor.
Corrige: K-01 (a alternativa comparada estava errada) e completa J-01/J-02.
Fecha em parte: P-68.

---

## O que a tela diz, literalmente

| cofrinho | taxa | saldo | rendimento acumulado | etiqueta |
|---|---|---|---|---|
| **Turbinado** | até **121% do CDI** | **R$ 500,00** | R$ 0,01 | **LIMITE DO CARTÃO** |
| **do Cartão** | até **120% do CDI** | **R$ 7.681,71** | R$ 80,85 | **LIMITE DO CARTÃO** |
| **total** | — | **R$ 8.181,71** | R$ 80,86 | — |

E, dentro do Turbinado, em texto corrido:

> *"O saldo deste cofrinho está ativo como limite do seu cartão."*
> *"Tarefas concluídas! Seu Cofrinho Turbinado está ativo este mês!"*

---

## 1. Os R$500 não estão livres — e isto é uma correção

O Osvaldo escreveu: *"os 500 reais é livre"*. **A tela do próprio produto diz o
contrário**, na mesma imagem, em duas marcações independentes: a frase acima e a
etiqueta `LIMITE DO CARTÃO` na lista.

A distinção que provavelmente está por trás da resposta dele é real e vale nomear:

| | |
|---|---|
| **líquido** | dá para pedir resgate a qualquer momento |
| **livre / não empenhado** | resgatar não tira nada de você |

O cofrinho é **líquido** e **empenhado ao mesmo tempo**. Resgatar reduz o limite do
cartão na mesma medida. É por isso que o `Estado` do projeto separa `reserva_atual` de
`reserva_disponivel` desde o J-01 — não é preciosismo de modelagem, é este produto.

**O que ainda não se sabe, e é o número que decide:** quanto do limite está **usado**
(fatura aberta + compras já feitas no ciclo). A parcela do cofrinho que lastreia limite
**já gasto** não sai. Portanto:

```
reserva_disponivel  =  8.181,71  −  limite atualmente comprometido
```

Com limite zerado, a reserva é R$8.181,71 e a Fase A está muito à frente do que o
projeto supõe. Com o limite todo usado, a reserva é **zero** — e o dinheiro é garantia de
uma dívida que já existe.

**Nenhum dos dois foi presumido.** É a regra da casa: perguntar o número inteiro antes de
calcular a razão.

## 2. O M-01 estava certo pelo motivo certo, e o número era real

O M-01 registrou que o prazo "~mar/2030" fora calculado com **R$7.671 de reserva
inicial** e que isso estava errado *"porque a reserva é zero"*.

O saldo do Cofrinho do Cartão hoje é **R$ 7.681,71**.

**O número existia.** O que estava errado não era o valor — era chamá-lo de reserva. Ele
é caução. O M-01 acertou a conclusão e agora tem a evidência que faltava, com etiqueta do
próprio app.

## 3. K-01 comparou contra a alternativa errada — e isto muda a resposta

O K-01 mediu **121% contra 102%** (cofrinho comum) e concluiu que a mensalidade de
R$287,88/ano fazia o Turbinado perder.

**Mas a alternativa real dele não é o cofrinho comum de 102%.** É o **Cofrinho do
Cartão, a 120%**, que ele já tem e onde já estão R$7.681,71.

Com CDI de **13,90% a.a.** (`custos.yaml → macro.cdi_aa`, SGS 4389, 03/09/2026):

| comparação | diferencial | sobre R$500 | sobre R$8.181,71 |
|---|---|---|---|
| 121% × **120%** | **0,139 p.p. a.a.** | R$ 0,70/ano | **R$ 11,37/ano bruto** |
| 121% × 102% | 2,641 p.p. a.a. | R$ 13,20/ano | R$ 216,08/ano bruto |

Líquido de IR, o diferencial 121 × 120 sobre o total fica entre **R$ 8,81 e R$ 9,67 por
ano**, conforme a faixa de prazo.

### A resposta direta à pergunta dele

> *"o cofrinho turbo funciona mesmo sem completar as missões? o que muda é que ele fica
> com a mesma taxa do cofrinho de limite do cartão."*

**Então as missões valem ~R$9 por ano**, no saldo atual — e isso é **antes** de contar o
que custa gerá-las. O K-01 já registrou que a exigência é da ordem de **R$2.500 de gasto
no cartão em 3 meses**, e escreveu a frase que continua valendo:

> *"Gasto no cartão alimenta a fatura que prende o cofrinho."*

**Organizar consumo para ganhar R$9 por ano é a alavanca errada**, e é o M-01 outra vez:
o destino do dinheiro move pouco; **quanto entra move tudo**. R$50 a mais de aporte por
mês valem R$600 no ano — 66 vezes o prêmio das missões.

> **O que isto NÃO diz.** Não diz para sair do Turbinado. A 121% ele é, hoje, o melhor
> dos três, e migrar não custa nada. Diz que **cumprir tarefa para mantê-lo não se paga**,
> e que deixá-lo cair para 120% custa R$9 por ano — provavelmente menos que a atenção
> gasta em lembrar das missões todo mês. E isso é a doutrina **P7** aplicada a dinheiro:
> uma rotina que depende de alguém lembrar não é uma rotina.

## 4. O que muda no `custos.yaml`

A seção `cofrinho` tem `picpay_pct_cdi` e a análise do K-01 construída sobre
**121% × 102%**. Falta a rota do meio, que é a que ele realmente ocupa.

**A acrescentar, com este arquivo como fonte:**

```yaml
cofrinho_do_cartao_pct_cdi:
  valor: 1.20          # "ate 120% do CDI" — o "ate" sugere faixa por saldo
  status: OBSERVADO    # lido na tela do app, nao em documento do emissor
  fonte: "app PicPay, tela Cofrinhos, 10/09/2026 10:14"
  acesso: 2026-09-10
  expira: 2026-12-10   # taxa de produto muda sem aviso; 3 meses e prudente
  nota: >
    Etiquetado LIMITE DO CARTAO na propria lista. Nao e reserva: e caucao liquida.
```

**NAO_CONFIRMADO que este arquivo abre:**

- o **"até"** em "até 121%" e "até 120%" sugere faixa por saldo. Se houver degrau, os
  diferenciais acima mudam. Não há tabela na tela;
- quanto do limite está comprometido hoje — o número que define `reserva_disponivel`;
- se o Turbinado exige mensalidade **além** das tarefas, ou se as tarefas a substituem. A
  tela diz apenas *"Tarefas concluídas"*. O K-01 registrou R$287,88/ano a partir de
  capturas de 05/09; **as duas leituras podem estar descrevendo planos diferentes**, e
  isso precisa ser reconciliado antes de o K-01 ser reescrito.

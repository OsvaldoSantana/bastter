# P-77 — o campo que a P-13 criou e ninguém leu

**Fechada em 13/09/2026.** Patch, 14 testes e a guarda estrutural que impede a próxima.

---

## 1. A pendência estava imprecisa, e a imprecisão importa

O `PENDENCIAS.md` dizia: *"`retorno_liquido_aa` zera o IR de ganho do FII"*.

**Hoje não zera — devolve `None`.** O FII é `indexador: rv`, e as duas funções saem
antes da linha do imposto. A pendência descrevia um sintoma que não estava acontecendo,
e por isso a busca por ele não achava nada.

**O defeito real é outro e é maior:**

> `aliquota_ganho` tem **zero leituras no motor**. As quatro únicas estão em
> `test_alocacao.py`.

A P-13 partiu `isento_ir` em dois campos pela razão certa — o FII não cabe num booleano,
porque o **rendimento** distribuído é isento (Lei 11.033/2004 art. 3º, com ≥100 cotistas)
e o **ganho** é tributado a 20% (Lei 8.668/1993 art. 18), sem a isenção mensal de R$20
mil. Criou `aliquota_ganho`, o catálogo preencheu com a lei citada ao lado — e **nenhuma
linha do motor consumiu**.

**Mudança de esquema anunciada como correção de comportamento.** É a assinatura deste
projeto, na forma mais enganosa que ela já tomou: *um arquivo declara um comportamento
que o código não tem* — e desta vez o arquivo era o **dataclass** e o **catálogo**.

---

## 2. Por que atravessou oito dias — três camadas, todas coincidência

| # | camada | efeito |
|---|---|---|
| 1 | FII é `indexador: rv` | as duas funções devolvem `None` antes do imposto |
| 2 | FII está **bloqueado** (`val_recusa` sobre `fii.taxa_administracao`) | nem chega a ser avaliado |
| 3 | as únicas outras rotas com `aliquota_ganho` são LCI e LCA, **com 0,0** | as duas pontas isentas: a diferença não aparece |

Medido — as 25 rotas do catálogo, e só uma tem `aliquota_ganho` diferente de zero:

```
id               indexador  isento_rend  al_ganho  confiavel  retorno_liquido_aa
fii              rv         True         0.2       False      None        <<<
lci / lca        cdi        True         0.0       False      0.13900
poupanca         poupanca   True         None      True       0.08027
rdb_100          cdi        False        None      True       0.10773
```

**Três coincidências, e o campo morto passou pelas três.**

---

## 3. Quando morde — e o número medido

No dia em que existir uma rota de **renda fixa** cujo ganho seja tributado diferente do
rendimento. **Debênture incentivada** é o caso óbvio e nada impede que entre amanhã.

```
rota deb_incentivada: indexador cdi, isento_ir_rendimento=True, aliquota_ganho=0.20

ANTES  ->  0,13900     <- o imposto INTEIRO zerado
DEPOIS ->  None + "rendimento isento e ganho a 20,0% sao DUAS aliquotas,
                   e esta funcao modela uma so. Nao ha numero certo a devolver."
```

**0,13900 é exatamente o número da LCI/LCA.** O motor trataria uma debênture incentivada
como se fosse uma LCI — isenta nas duas pontas. Errado **para menos**, que é a direção
lisonjeira: a rota apareceria mais rentável do que é, e competiria melhor no G2.

---

## 4. A correção, e o que ela deliberadamente NÃO faz

`regime_tributario(r)` devolve `(alíquota_sobre_o_rendimento_ou_None, motivo_ou_None)`:

| caso | resposta |
|---|---|
| sem `aliquota_ganho` | `None` → delega para a tabela geral (comportamento antigo) |
| isento, sem `aliquota_ganho` | `0.0` (comportamento antigo) |
| isento **e** ganho 0,0 | `0.0` — LCI/LCA, caso resolvido |
| **isento e ganho > 0** | **recusa**, com motivo |
| tributado e ganho ≠ 0 | **recusa**, com motivo |

**O que não faz:** não inventa um modelo de duas pontas. `retorno_liquido_aa` modela um
instrumento que **acumula rendimento** — nele o ganho *é* o rendimento, e não há duas
pontas a separar. Quando a rota declara pontas divergentes, a resposta honesta não é um
número aproximado: é recusar dizendo por quê. **P6 — ausência de critério não vira
critério de exclusão, vira lacuna declarada.**

**E o motivo não some junto com o `None`.** Foi um `None` calado que escondeu isto;
`retorno_liquido_aa` agora aceita um dict `motivos` opcional — mesmo padrão do
`desconhecidos` do `refinar.py`. O quinto argumento é opcional: nenhum chamador antigo
muda.

A mesma regra entra nos **dois** lugares (`retorno_liquido_aa` e `_marginal_plano`),
porque eram dois trechos com a mesma linha copiada — o A-07 esperando acontecer.

---

## 5. A guarda estrutural — a única parte que impede a próxima

```
test_P77_todo_campo_que_o_catalogo_preenche_e_lido_pelo_MOTOR
```

Para cada campo que `catalogo.yaml` preenche numa rota, algum módulo **que não é teste**
tem de lê-lo. Rodada contra o código **antes** do patch:

```
AssertionError: campo(s) que o catalogo PREENCHE e o motor nao le: aliquota_ganho.
```

**Teria pegado a P-77 no dia em que ela nasceu.**

> **E aqui está a lição do dia, que é sobre o meu próprio instrumento.** O
> `chaves_orfas.py` que escrevi ontem para o E-04 **não** pegou `aliquota_ganho`. Fui
> ver por quê, esperando um problema de declaração de dataclass. Não era: ele varre
> **todos** os `.py`, testes inclusive — e o campo é lido quatro vezes, **todas em
> `test_alocacao.py`**.
>
> **Campo que só o teste toca é campo que o motor não usa.** É uma categoria pior que
> órfã pura, porque tem uma testemunha: o teste prova o **esquema** e ninguém prova o
> **comportamento**. Foi exatamente assim que a P-13 pôde anunciar uma correção que era
> só mudança de dataclass, com a suíte verde.
>
> `chaves_orfas.py` agora separa **leitor do motor** de **leitor de teste** e reporta
> "LIDA SÓ POR TESTE" como categoria própria. Rodando agora, ele acusa
> `aliquota_ganho` — que era o que se pedia dele.

---

## 6. Estado

- **14 testes novos**, verdes, incluindo o instantâneo dourado das seis rotas de caixa
  (`lci` 0,13900 · `rdb_100` 0,10773 · `td_reserva` 0,10850 · `poupanca` 0,08027 ·
  `picpay_cofrinho` 0,10988), medido **antes** do patch;
- suíte existente: **182 passed** antes e depois, com o **mesmo** conjunto de 7 falhas
  (todas P-15, por falta de `pyproject.toml` no meu ambiente — idênticas nas duas
  rodadas, então a mudança é inerte sobre o que já existia);
- `test_nenhuma_rota_do_catalogo_e_recusada_hoje` registra que a P-77 é **latente** e
  avisa no dia em que deixar de ser.

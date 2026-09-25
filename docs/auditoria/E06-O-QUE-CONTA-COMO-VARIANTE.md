# E-06 — o que conta como variante

**Pergunta:** `variantes_permitidas: 1` está declarado em quatro estratégias
pré-registradas (e `2` em três, `3` no Greenblatt) e **nada o conta**. Antes de contar,
é preciso decidir o que se está contando.

**Status: decisão de desenho aberta.** Três definições, com o que cada uma proíbe de
verdade, medidas contra o histórico real do projeto — não contra exemplos inventados.

---

## 0. Duas medições, antes das definições — porque elas mudam qual definição faz sentido

Fui procurar, no seu próprio pré-registro, um grau de liberdade não declarado. Achei
dois candidatos. **Um não era, e o outro é de um tipo que nenhum contador pegaria.**

### 0.1 O filtro de pregões — minha hipótese, e ela estava errada

O pré-registro do `hml_puro_v1` (emissão **03/09**) fala em **307 meses**. A execução
(**05/09**) registra **306**, *"filtro n_dias >= 15"*. O filtro aparece **só no registro
de execução** e o número 15 é um **default em Python** (`fatores.premios(minimo_dias=15)`),
invisível ao pré-registro.

Minha hipótese: um corte escolhido depois de ver o dado. Fui medir, variando **só** o
filtro:

| `minimo_dias` | meses | alfa a.m. | t | veredito a 1,96 |
|---|---|---|---|---|
| 0 | 307 | 0,00766 | 2,94 | rejeita H0 |
| 5 · 10 · 12 · **15** · 16 · 17 · 18 | 306 | 0,00766 | 2,94 | rejeita H0 |
| 20 | 243 | — | — | (corta 63 meses; outra amostra) |

**De 5 a 18 o resultado é idêntico**, ao quinto decimal. O filtro corta exatamente um
mês — o último, com 3 pregões — e qualquer corte razoável corta o mesmo mês.

**Não era p-hacking, e a medição é que diz.** Registro isso porque a hipótese era minha
e ela caiu: uma escolha não declarada **pode** ser inofensiva, e a única forma de saber
é medir a sensibilidade — não supor num sentido nem no outro.

### 0.2 O grau de liberdade que existe, e ele inverte o SINAL

`fatores.alfa_contra_fatores()` calcula `y = retorno − Risk_Free`, porque foi escrita
para estratégia **long-only**. HML é um fator **long-short**, de custo zero: o retorno
dele **já é** excesso. Subtrair o CDI de novo — e o CDI brasileiro médio da amostra é
**0,938% ao mês** — não corrige nada, destrói.

```
HML puro (o certo)       alfa = +0,00766   t = +2,94    -> rejeita H0
HML − Risk_Free (errado) alfa = −0,00178   t = −0,68    -> não rejeita
```

**O mesmo dado, a mesma regressão, a mesma amostra — e o veredito inverte.** Não é uma
mudança de parâmetro, não é uma mudança de amostra, não é um campo do registro. É uma
decisão de **como se monta a variável dependente**, e ela vale mais que todos os
parâmetros somados.

**E o projeto já sabe disso.** Eu ia escrever isto como achado novo e parei ao ler em
volta:

- `backtest_h1_h3.py`, linha 9: *"NÃO usar `fatores.alfa_contra_fatores()` aqui. Ela
  subtrai o Risk_Free, porque..."*
- `test_fatores.py`: o idioma correto é `alfa_contra_fatores(m.HML + m.Risk_Free, m)` —
  soma-se antes, para a subtração cancelar;
- `test_h1_h3_reproduzem_o_resultado_registrado` afirma `0,00766` e `t = 2,94`;
- `test_subtrair_risk_free_de_um_fator_inverte_o_veredito` **prende a armadilha num
  teste**, com a docstring: *"se alguém 'consertar' o código para usar
  `alfa_contra_fatores()`, este teste mostra o tamanho do estrago."*

**Esta é a lição que governa a escolha abaixo:** o grau de liberdade mais perigoso do
pré-registro inteiro **não é contável por nenhuma das três definições** — e o que o
segura é uma **convenção escrita e um teste**, não um número. Qualquer desenho que trate
`variantes_permitidas` como a defesa principal está protegendo o flanco errado.

---

## 1. D1 — variante é **execução**

> Toda rodada que produz um veredito consome uma variante.

**Proíbe na prática:** rodar de novo depois de corrigir um bug; rodar de novo com dado
atualizado; rodar de novo porque a primeira execução abortou.

**Como se mede:** um contador no registro de execução. Trivial, à prova de
interpretação.

**Modo de falha, e é fatal:** esgota na primeira semana. O `hml_puro_v1` teria estourado
o limite **antes de produzir resultado**, porque a execução de 05/09 veio depois de uma
`correcao_de_premissa` que obrigou a reler a fonte. Um limite que transforma *corrigir
um erro* em *gastar sua única bala* ensina a não corrigir.

**E o pior efeito não é o bloqueio — é o incentivo:** sob D1, a jogada ótima é rodar
tudo **fora** do sistema e registrar só o que der certo. A regra produz exatamente o
comportamento que existia para impedir.

**Veredito:** não. É a definição que parece mais rigorosa e é a mais fácil de contornar.

---

## 2. D2 — variante é **mudança em campo registrado**

> Congela-se a especificação no momento do registro. Qualquer alteração num campo
> declarado consome uma variante. Rodar a especificação idêntica não consome.

Para o `greenblatt_v1`, os campos são concretos:

```yaml
ranking: [roic, ebit_sobre_ev]     combinacao: soma_de_posicoes
n_ativos: 16                        rebalanceamento: trimestral
definicao_roic: "EBIT/(capital_de_giro + imobilizado_liquido)"
```

**Proíbe na prática:** `n_ativos` 16 → 20 · `rebalanceamento` trimestral → anual ·
`corte >= 8` → `>= 7` no Piotroski · trocar a definição de ROIC. **Exatamente as alavancas
que produzem o "fator de três" que o próprio `nota_definicao` denuncia** na literatura
da Magic Formula.

**Como se mede:** hash dos campos da especificação. Mudou o hash, é variante. É
mecanizável hoje, com a máquina de impressão digital que o projeto já tem — e casa com
a P4.

**Modo de falha 1 — cega para a construção da amostra.** Sob D2, rodar a mesma
especificação em 2001-2020, depois 2005-2026, depois com outro filtro, **não gasta nada**.
É o buraco do §0.1 — que naquele caso era inofensivo, mas só porque medi.

**Modo de falha 2, e este vem do seu histórico.** `hipotese_nula_esperada` é campo
registrado. A v1.3.0 registrou o `hml_puro_v1` como *hipótese nula esperada* apoiada numa
afirmação de terceiro — *"HML paga 0,05% ao mês no Brasil"* — que **não reproduz em
nenhuma janela**. Corrigir isso é honestidade de fonte primária, a P1 inteira. Sob D2,
**queima a única variante permitida, antes da primeira execução.**

**A distinção que falta a D2:** corrigir um **erro de fato** não é exercer um grau de
liberdade. Grau de liberdade é escolher entre alternativas **igualmente defensáveis**;
corrigir um número errado não tem alternativa defensável do outro lado.

**Veredito:** é a mecânica certa, com dois remendos — um bloco `amostra:` registrado, e
uma isenção explícita para correção de erro factual, escrita e datada.

---

## 3. D3 — variante é **grau de liberdade declarado**

> No registro, lista-se explicitamente cada escolha que poderia ter sido feita de outro
> jeito. Mexer em qualquer uma consome uma variante. O que não foi listado **não pode
> ser mexido** — nem gastando variante.

```yaml
graus_de_liberdade:
  - n_ativos            # 16; alternativas defensaveis: 10, 20, 30
  - definicao_roic      # implementacoes honestas divergem -- ver nota_definicao
  - amostra_inicio      # 2001 e o inicio da serie NEFIN, nao uma escolha
  - tratamento_do_rf    # long-short NAO subtrai; long-only subtrai
```

**Proíbe na prática:** tudo que D2 proíbe, **mais** amostra, estimador e construção da
variável dependente. É a única das três que alcança o §0.2.

**Como se mede:** mesma mecânica de D2, sobre a lista declarada.

**A virtude, e ela é maior que a contagem:** escrever a lista **antes** é o exercício
que faz o pesquisador enxergar onde ele pode se enganar. Provavelmente vale mais que o
limite numérico.

**Modo de falha:** exige prever. O grau de liberdade que te pega é o que você não sabia
que tinha — e a cláusula *"o que não foi listado não pode ser mexido"* transforma cada
esquecimento em trava. Sozinha, ela é rígida demais para pesquisa de verdade.

**Veredito:** a definição certa, com uma válvula: descobrir um grau de liberdade novo
não é proibido — é um **evento registrável**, que reabre o pré-registro com data e
motivo, e marca o resultado anterior como produzido sob espec incompleta.

---

## 4. O que eu recomendo — e o reenquadramento importa mais que a definição

**D3 com a mecânica de D2, e o contador rebaixado a alarme.**

1. **`graus_de_liberdade` explícito** em cada estratégia, escrito antes de rodar.
2. **Bloco `amostra:` registrado** (período, filtros, conjunto de fatores) — hoje ele é
   escrito na *execução*, que é tarde demais para valer como compromisso.
3. **Hash da especificação + graus de liberdade**; mudou o hash, é variante.
4. **Isenção para correção de erro factual**, escrita, datada e com a fonte primária —
   corrigir um número errado não é exercer grau de liberdade.
5. **`variantes_permitidas` não bloqueia: exige justificativa escrita.** Estourar o
   limite não impede a execução — impede o resultado de ser registrado sem um parágrafo
   dizendo por que a variante extra existe.

O ponto 5 é o reenquadramento, e é o seu próprio argumento devolvido. Você disse que uma
régua larga demais vira burocracia contornável. **A trava dura é a que se contorna**, e
com razão: ela impede pesquisa legítima, e a saída — rodar por fora — destrói o registro
inteiro. O que protege contra p-hacking **não é o número de tentativas: é o registro de
todas elas.** Um limite de 1 sem registro da tentativa 2 é mais fraco que um limite de 5
com as cinco escritas.

> **O instrumento principal é o diário de execuções, não o contador.** Toda execução
> entra — inclusive a abandonada, inclusive a que deu errado, com a data e o motivo. O
> contador existe para **disparar a pergunta**, não para dar a resposta.

E a régua de sizing que você já usa sem ter escrito: `greenblatt_v1` tem **3** porque a
especificação publicada é genuinamente ambígua (o `nota_definicao` diz que implementações
honestas divergem por um fator de três); `hml_puro_v1` tem **1** porque é uma regressão
sobre uma série publicada, sem espaço. **O número segue a ambiguidade da fonte.** Vale
escrever essa regra — ela já governa a sua tabela.

---

## 5. O que ainda é decisão sua

| # | pergunta | por que não decido por você |
|---|---|---|
| 1 | dado atualizado (mesma espec, fim mais recente) é **extensão** ou **variante**? | Minha leitura: extensão, registrada e comparada — se o alfa morre ao estender, é o evento mais informativo possível, e tratá-lo como variante desencoraja justamente a rodada que você mais quer. Mas a leitura oposta é defensável |
| 2 | o limite é **por estratégia** ou **por conjunto**? | Oito estratégias × 1 variante são oito chances no mesmo dado. O problema de comparações múltiplas é do **conjunto**, não de cada uma |
| 3 | a isenção por erro factual é **auto-declarada** ou precisa de fonte primária citada? | Auto-declarada é contornável; exigir fonte é atrito real em cima de uma correção honesta |

**A 2 é a que eu acho mais séria e a menos óbvia.** Cada estratégia com o seu limite dá a
impressão de rigor enquanto o conjunto passa oito vezes pela mesma série de 306 meses. É
o mesmo dado, e o pré-registro não tem hoje nenhum mecanismo de conjunto.

---

## 6. E o que eu errei — três vezes, no mesmo padrão

Nesta auditoria eu publiquei **E-05** (retirado: a chave era lida por outro YAML), quase
publiquei o multiplicador de estabilidade (era leitura por índice variável) e quase
publiquei o Risk_Free do §0.2 como achado novo — **com o projeto já tendo um comentário,
uma convenção e dois testes sobre ele**.

Os três têm a mesma forma: **medi, e concluí antes de ler em volta.** Os dois achados que
sobreviveram — E-01 e E-03 — eu confirmei lendo, não medindo.

A ordem certa é **medir → ler a vizinhança → concluir**, e eu vinha fazendo
**medir → concluir**, lendo só quando alguma coisa me obrigava. Numa auditoria, a medição
levanta o candidato; quem o promove a achado é a leitura.

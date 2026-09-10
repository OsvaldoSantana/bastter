---
name: bastter-achado
description: Como registrar um achado do projeto Bastter — a letra, a medição que o prova, o teste que impede a volta, e onde escrever. Use ao descobrir que o sistema não faz o que o arquivo diz.
---

# Registrar um achado — projeto Bastter

Um achado é um defeito **medido**, não uma suspeita. O registro tem quatro partes
obrigatórias, e a segunda é a que separa achado de opinião.

## As quatro partes

1. **Letra e data.** Sequencial na família (`F-`, `J-`, `K-`, `N-`, `O-`, `Q-`, `R-`,
   `S-`, `T-`, `U-`…) mais a data. A letra é o endereço: outros arquivos vão citá-la.

2. **A MEDIÇÃO que o prova.** Não "parece que", não "provavelmente". O número, e o
   comando que o produziu.
   > S-01: *"`hash_custos()` era chamada 73 vezes por `alocar()`; 37% do tempo do motor."*
   > — medido com `cProfile`, não estimado.

3. **A CONSEQUÊNCIA em termos do projeto**, não em termos de código limpo. O que este
   defeito fazia o sistema **afirmar de errado**?
   > S-02: *"qualquer teste que alterasse um custo e conferisse arrasto estava testando
   > nada."* Isso é uma consequência. "O cache estava mal desenhado" não é.

4. **O TESTE que impede a volta**, e ele precisa **falhar na versão anterior**. Um teste
   que passaria antes e depois não prende nada.

## Onde escrever

| arquivo | o quê |
|---|---|
| `ACHADOS.md` | a narrativa completa — o que era, como foi medido, o que mudou |
| `politica.yaml → meta.changelog` | o resumo na entrada de versão |
| docstring da função afetada | o parágrafo que explica por que o código é assim |
| `PENDENCIAS.md` | só se sobrou dívida; a tabela `## Fechadas` sempre |

## O padrão que mais se repete — reconheça antes de descrever

Quatro achados são a mesma coisa com roupas diferentes — **F-05, N-01, R-01, S-02**:

> *Um arquivo declara um comportamento que o código não tem, e os dois concordam por
> acaso, então ninguém descobre.*

- **F-05**: `bloqueia` estava no YAML e nenhuma linha de código o lia.
- **N-01**: o multiplicador de confirmação estava no YAML **e** como literal no Python,
  com os mesmos números. **Concordar é pior que discordar** — editar o arquivo não
  mudava nada e ninguém descobriria.
- **R-01**: o YAML declarava a ordem dos portões como dado livre; 102 das 120 ordens
  quebravam.
- **S-02**: a chave do cache era o hash do *arquivo*, e o valor vinha do *parâmetro*.

**Se o achado novo tem essa forma, diga isso.** Reconhecer o padrão vale mais que
descrever o caso, e é assim que o quinto para de acontecer.

## Testes que valem mais

- O que **falha na versão anterior** e passa nesta.
- O que **mede** em vez de afirmar (contar as 120 permutações, não argumentar sobre elas).
- O que **declara o que não cobre** — a lista do que o mecanismo não vê costuma valer
  mais que a do que ele vê.

## Não infle o achado

Se o ganho é R$7,75 por ano, **escreva R$7,75 por ano** e explique por que o achado
importa mesmo assim (no caso O-01: a rota única obrigava a escolher entre melhor
retorno e melhor crédito; a composição não precisa escolher). Inflar um achado é o erro
que o J-02 registrou contra mim.

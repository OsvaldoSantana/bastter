# Informação não obtida não é informação inexistente — e o zero cobria as duas

**18/09/2026. Correção dele**, ao ler o relatório de corretoras:

> *"vi que você deixou algumas corretoras fora da avaliação por ausência de informação, e
> isso é contra algo que já afirmamos várias vezes: se a informação existe e você não
> conseguiu, o item não deve ser excluído — mas o problema de conseguir a informação deve
> ser solucionado."*

**É a quarta vez que a P6 precisa ser aplicada contra mim**, e a terceira em uma semana
(P6 original, P-83, o escopo do próprio projeto em 18/09, e agora isto).

---

## 1. Onde o desenho estava certo, e é preciso dizer antes

As nove casas **não sumiam do catálogo**. Elas apareciam numa seção `FORA DA ORDENAÇÃO
(nota zero)`, com o motivo escrito ao lado. Formalmente, a P6 estava honrada: visível,
com motivo, reversível.

**O que estava errado é mais fino, e por isso passou.** O sistema *tinha* nota para elas,
calculava essa nota, e a jogava fora antes de imprimir.

---

## 2. O que foi medido

Multiplicador de confirmação `N = 0.00` zera o total. Tirando só o multiplicador — isto
é, mantendo a penalidade de cobertura que já existe:

| casa | nota parcial | cobertura | ficaria em | o que se sabe |
|---|---|---|---|---|
| **BTG Pactual digital** | **54,0** | 65% | **7º de 19** | solidez 87,0 · reclamações 58,0 · sobrevivência 100 |
| **Bradesco / Ágora** | **47,3** | 65% | **11º de 19** | solidez 96,2 · reclamações 15,1 · sobrevivência 100 |
| **Mirae Asset** | **30,6** | 45% | **14º de 19** | solidez 28,1 · sobrevivência 100 |
| Avenue (braço Brasil) | 0,4 | 45% | 16º | solidez 1,9 |

**O BTG entraria em sétimo, à frente de nove casas que o ranking ordena.** Isso não é
"peso zero por insumo ausente": é eliminação, e ela apagava três dimensões medidas.

### E a punição caía sobre o dado errado

As dimensões que sobrevivem ao fracasso são **solidez** (do balanço) e **reclamações**
(do **Ranking de Reclamações do BCB**, fonte primária e oficial). O que falhou foi o
**site da corretora** — `HTTP 403`, `SPA sem HTML servido`, `DNS não resolve`.

> **Zerar a nota inteira porque o site do BTG é um SPA é punir um dado que veio do Banco
> Central.** As duas coisas não se tocam.

---

## 3. O defeito real: um zero cobrindo duas afirmações opostas

| casa | por que zero | é o quê |
|---|---|---|
| Clear, Órama, Guide, Necton, Vitreo | `entidade_independente = False` | **medição**, e o zero é o resultado dela |
| BTG, Bradesco, Mirae | custo desconhecido | **lacuna**, e o zero é a decisão de não ordenar |

Indistinguíveis de fora — e **é exatamente a forma do E-02**, em que "arquivo ausente" e
"arquivo vazio" devolviam a mesma coisa e a indistinguibilidade *era* o defeito.

---

## 4. O que mudou, e o que deliberadamente não mudou

**Não mudou:** o multiplicador continua zerando o `total`. É o G5/F-02 — *status é
pré-condição de comparação de custo* —, e uma casa cujo custo eu não sei não é
recomendável. **A ordenação saiu idêntica**, e há teste que prende isso.

**Mudou:** `pontuar()` passa a devolver `parcial` (a nota com tudo que se sabe, já
penalizada pela cobertura), `avaliadas` e `nao_avaliadas`. O relatório ganhou a seção
*"NÃO ORDENADAS POR AUSÊNCIA DE DADO — e o que o sistema JÁ SABE sobre elas"*, com a
posição que cada uma ocuparia, o que se sabe, o que falta, e **como a coleta falhou**.

> É a mesma forma do conserto do E-08: *o resolvedor não inventou tratamento nenhum —
> fez o dado chegar ao tratamento que existia.* Aqui, fez o número chegar ao leitor.

**E a segunda metade da frase dele virou pendência com dono e gatilho — P-90.** O campo
`pegadinha` dessas casas diz *"HTTP 403"*, *"site é SPA"*, *"domínio não resolve DNS"*.
Isso descreve **o meu raspador em setembro de 2026**, não a instituição — e estava
guardado como se fosse característica dela.

---

## 5. Um erro meu, que a prova por mutação pegou

Escrevi uma guarda para o formato de saída de `pontuar()` (havia dois `return` com chaves
diferentes — A-07 dentro de uma função só). Reintroduzi o defeito para ver a guarda
reprovar, e **os 42 testes continuaram verdes**.

O ramo era **inalcançável**: `sobrevivencia` sai de um `bool` e nunca é `None`, então
`validas` nunca fica vazio. *Ramo morto não falha, logo não se testa* — e mantê-lo era
guardar uma inconsistência que ninguém podia observar. Foi removido, e no lugar ficou a
invariante que o dispensa, presa em teste: **toda casa tem ao menos uma dimensão
avaliável**. Se ela cair, o ramo volta — com o formato do outro.

> A prova por mutação não confirmou a guarda: **reprovou o teste.** É para isso que ela
> serve, e foi a primeira vez neste projeto que ela pegou o teste em vez do código.

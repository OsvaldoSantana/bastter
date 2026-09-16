# Item 1 — você respondeu "sim", e a medição estreita a pergunta

Você aprovou pôr **custo por operação** no ranking de corretoras. Fui medir os três
campos antes de implementar, e **dois deles não separam ninguém.**

| campo | casas que declaram | valores distintos | separa? |
|---|---|---|---|
| `corretagem_fii` | 11 de 24 | **1** — todas **0,0** | **não** |
| `exercicio_opcao_pct` | 4 de 24 | **1** — todas **0,005** | **não** |
| `mesa_minimo` | 4 de 24 | 3 — R$20 (Santander), R$25 (Safra), R$50 (Inter, Rico) | **sim**, com cobertura de 17% |

**Uma dimensão cujo valor é único entre todas as casas que a declaram não move o
ranking. Ela adiciona peso e não separa.** Pontuar `corretagem_fii` hoje seria
acrescentar rigor aparente e medir zero — e isso é pior que a lacuna, porque parece
resolvido.

E há um segundo motivo para o `exercicio_opcao_pct` ficar de fora: **o projeto não tem
rota de opções.** A P-20 registra `opcoes` como excluída e depois revertida para
pendência. Pontuar o custo de uma operação que o sistema não sabe recomendar é medir
uma decisão que não existe.

---

## O que eu proponho, e é menos do que você aprovou

1. **`mesa_minimo` entra** — é o único com variação real. Entra como **penalidade
   condicional**, e quem não declara não ganha nem perde: a `cobertura` do `pontuar()`
   já penaliza dimensão ausente, que é o comportamento certo e já existente.
2. **`corretagem_fii` e `exercicio_opcao_pct` NÃO entram**, e a razão fica escrita com
   a medição ao lado: *valor único entre as casas que declaram, em 13/09/2026*. **Se um
   dia alguém cobrar diferente, a dimensão nasce** — e é por isso que o próximo item
   existe.
3. **Uma guarda nova**, que é a parte que generaliza: um teste que mede o **poder de
   separação** de cada campo candidato e falha quando um campo que hoje é empate
   **deixa de ser**. Ele avisa no dia em que a dimensão passar a valer a pena, em vez
   de deixar a decisão de hoje congelada para sempre.

> É a P6 outra vez, e na direção certa: **o dado fica guardado, a ausência de critério
> fica declarada, e a mudança de mundo é detectada.** O oposto do E-03, onde o
> interruptor existia e não fazia nada.

---

## Por que eu não implementei já

Você respondeu "sim" acreditando que havia **três** custos sendo ignorados. A medição
diz que há **um**, com cobertura de 17%. **Isso muda a pergunta que você respondeu**, e
a sua própria doutrina diz que decisão de desenho é sua.

**As duas opções:**

- **`só mesa_minimo`** — implemento a dimensão com o peso que você indicar, a guarda de
  separação entra junto, e os outros dois ficam declarados com a medição.
- **`nenhum, por enquanto`** — os três ficam como estão, a guarda de separação entra do
  mesmo jeito, e a dimensão nasce sozinha no dia em que os dados a justificarem.

Minha leitura: **a segunda.** Uma dimensão com 17% de cobertura e três valores distintos
move pouco e tem o custo de precisar de um peso novo no `politica.yaml` — e peso novo é
escolha sem dado por trás. Mas isso muda o ranking das corretoras onde você vai abrir
conta, então é sua.

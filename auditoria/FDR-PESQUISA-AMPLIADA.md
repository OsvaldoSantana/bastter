# Correção para testes múltiplos — a pesquisa ampliada, e o que ela faz com o seu "FDR"

Você disse *"acredito que a melhor decisão seja FDR mas talvez valha a pena ampliar o
escopo"*. Ampliei — e o resultado é que **FDR não compra nada para você**, por uma razão
aritmética que eu verifiquei de novo por conta própria.

> **Procedência.** A pesquisa foi feita por um subagente com acesso à web; o relatório
> completo, com 21 fontes e uma tabela de verificação fonte a fonte, está em
> `auditoria/FDR-RELATORIO-COMPLETO.md`. **Os números decisivos abaixo eu recalculei
> aqui**, com a t de Student e 301 gl, antes de escrever qualquer coisa — por causa da
> regra de 12/09: medir, ler a vizinhança, concluir.

---

## 1. O fato que decide, e eu conferi

Com **m = 8**, t de Student, 301 gl:

| regra | p exigido | \|t\| exigido |
|---|---|---|
| sem correção | 0,05000 | 1,968 |
| **BH (FDR), 1ª descoberta** | 0,00625 | **2,754** |
| **Bonferroni** | 0,00625 | **2,754** |
| **BY (FDR sob dependência), 1ª descoberta** | 0,00230 | **3,075** |

Duas coisas, e as duas contra o FDR no seu caso:

**1. O limiar da PRIMEIRA descoberta do BH é exatamente o do Bonferroni.** O passo do
BH é `(i/m)·α`; para `i = 1` isso é `α/m` — a fórmula do Bonferroni, idêntica. O BH só
afrouxa a partir da **segunda** rejeição. Com 8 estratégias e uma esperança de 0 a 1
descoberta real, **você nunca chega ao regime em que o BH ganha alguma coisa**.

**2. O BY é MAIS severo que o Bonferroni.** A versão do FDR que vale sob dependência
arbitrária divide por `c(m) = Σ1/i` — 2,7179 para m=8 — e pede **|t| ≥ 3,075** contra
2,754. Você pagaria o preço de um critério de erro mais frouxo e receberia **menos
poder** que o método conservador clássico. É o pior dos dois mundos.

> **Por que a intuição "FDR é melhor" falha aqui:** ela vem da genômica, onde m é 10.000
> e o Bonferroni não rejeita nada. Com **m = 8**, o Bonferroni pede 1,968 → 2,754: 0,79
> de um t. Não é o instrumento cego que a fama sugere.

E há o argumento de propósito, que é anterior à aritmética: FDR serve a **exploração**
(achar um conjunto promissor); FWER serve a resultados que serão **usados
individualmente**. As suas oito são pré-registradas e cada uma aprovada vira alocação de
capital. **O seu caso é confirmatório.**

---

## 2. O que a literatura de finanças acrescenta — e o cuidado com o "t > 3"

O relatório completo cobre White (2000), Hansen (2005), Romano-Wolf (2005),
Harvey-Liu-Zhu (2016), Harvey-Liu (2015 e 2020), Bailey-López de Prado, Chordia-Goyal-
Saretto (2020), Chen (2024), Jensen-Kelly-Pedersen (2023). Três pontos mudam decisão:

**(a) O `t > 3,0` de Harvey-Liu-Zhu foi calibrado para 316 fatores** — uma literatura
inteira testada sobre a mesma seção transversal. Aplicá-lo às suas 8 hipóteses
pré-registradas é **contar a multiplicidade duas vezes**. E os próprios autores recuaram
em 2020: *"nem 2,0 nem 3,0 é ótimo"*, e o ponto ideal fica entre os dois.

**(b) Há divergência viva e não resolvida** sobre se os limiares devem subir.
Chordia-Goyal-Saretto (2020) pedem 3,38-3,84; Chen (2024, working paper do Federal
Reserve Board) argumenta que a fração de fatores falsos é **fracamente identificada** e
que 1,96 continua defensável; Jensen-Kelly-Pedersen (2023) tratam a correlação entre
fatores como **força**, não problema. **Não é mal-entendido entre eles — é desacordo.**

**(c) O método tecnicamente melhor para o seu caso é reamostragem, não fórmula.**
Romano-Wolf stepdown por bootstrap estima a distribuição do **máximo |t|** reamostrando
as 8 séries **com os mesmos índices de tempo**, o que preserva a correlação real em vez
de assumir o pior caso. Você já tem a série em disco e já roda 10.000 reamostragens em
outro teste.

**Seja honesto sobre o prêmio:** pela simulação do relatório, com ρ = 0,4 e m = 8 o
bootstrap devolve **2,702** contra 2,754 do Bonferroni — ganho de **0,05** de um t. Só
a partir de ρ ≈ 0,6 o ganho passa de 0,12. **Vale porque a infraestrutura já existe, não
porque transforma.**

---

## 3. A tradução que importa: quanto de habilidade cada regra exige

Com T = 306 meses, `t ≈ IR_anual × 5,05`:

| regra | \|t\| | IR anual exigido |
|---|---|---|
| sem correção | 1,97 | **0,39** |
| bootstrap max-t (ρ=0,4, m=8) | 2,70 | 0,53 |
| Bonferroni / BH, m=8 | 2,75 | **0,55** |
| Bonferroni, m=13 | 2,91 | 0,58 |
| HLZ "t > 3" | 3,00 | 0,59 |
| BY, m=8 | 3,08 | 0,61 |

**A decisão que importa é corrigir ou não corrigir** — 0,39 para 0,55 é ~40% mais
habilidade exigida. A escolha entre os métodos move 0,05 a 0,08, e é de segunda ordem.

---

## 4. O que eu recomendo

**Romano-Wolf stepdown por bootstrap de blocos, FWER 5%**, com **Holm** como verificação
de sanidade (custa uma linha, domina o Bonferroni de graça, e se os dois discordarem
muito **suspeite do bootstrap antes de acreditar no ganho**). Reporte também os 8 `t`
brutos, sem correção, para quem quiser reaplicar outra regra depois.

**Não use BY.** Não importe o `t > 3,0`.

E três ressalvas que o relatório faz e eu assino:

1. **O pré-registro resolve menos do que parece.** Ele elimina o p-hacking *seu*. As
   ideias das 8 vieram de uma literatura que já minerou os mesmos dados e publicou as
   vencedoras. A correção para m=8 trata a multiplicidade que você **criou**, não a que
   **herdou** — e essa é justamente a que Chen mostra ser fracamente identificada.
2. **306 meses é uma amostra, não a verdade.** 2001-2026 no Brasil tem regimes muito
   distintos. **Um teste de estabilidade por subperíodo vale mais que refinar a
   correção do terceiro para o quarto decimal** — e o seu registro do HML já faz isso
   (alfa negativo em 2009-2016).
3. **O IML (iliquidez) do NEFIN gera autocorrelação nos resíduos** — razão adicional
   para bootstrap **de blocos**, não i.i.d.

---

## 5. E a correção dos meus próprios números

Calculei os cortes do E-06 com a **normal**. O certo, para 306 meses e 5 parâmetros, é a
**t com 301 gl** — um pouco mais alta:

| m | eu escrevi | correto |
|---|---|---|
| 2 | 2,241 | **2,253** |
| 8 | 2,734 | **2,754** |
| 13 | 2,891 | **2,913** |

**A folga do HML cai de 0,049 para 0,027.** A conclusão não muda — ele sobrevive ao
corte mais severo — mas a margem é ainda mais fina do que eu disse.

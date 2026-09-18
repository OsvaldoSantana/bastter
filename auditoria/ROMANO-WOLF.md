# O corte da família — e a suposição que valia mais que a multiplicidade

**18/09/2026.** Fecha as três decisões de 13/09 que faltavam (Romano-Wolf; o `m` dos dois
lados; divergência bloqueia). Medido em `alocacao/multiplicidade.py` e
`alocacao/preregistro.py`, com **107 testes novos** (a suíte de `alocacao/` vai a 501).

> **O resultado que muda uma afirmação do projeto está na §3.** Não é sobre qual correção
> usar: é que a suposição por baixo das duas — o `t` se distribuir como a tabela de
> Student — **é falsa nesta série**, e custa mais que toda a correção de multiplicidade
> que vínhamos discutindo.

---

## 1. Por que dois instrumentos, e por que isso não era escolha

Você decidiu "Romano-Wolf por bootstrap" e "os dois `m`, lado a lado". Ao implementar,
os dois se encontraram num ponto que nenhum de nós tinha visto:

| lado | `m` | insumo disponível | instrumento possível |
|---|---|---|---|
| **executado** | 2 (do diário) | a estatística de **cada** hipótese | Romano-Wolf — mede a dependência |
| **orçado** | 13 (soma dos `variantes_permitidas`) | 11 dos 13 **nunca rodaram** | Bonferroni — só precisa do tamanho |

**Não há o que reamostrar num teste que não produziu estatística.** Romano-Wolf é
inaplicável ao lado orçado, não por preferência, mas por falta de insumo. O que sobra lá é
a união de Boole, que vale sob qualquer dependência e precisa apenas da marginal da
hipótese que se está julgando.

Então "os dois `m` lado a lado" **não é a mesma medida feita duas vezes.** São duas medidas
com instrumentos diferentes, por necessidade. Isso não enfraquece a decisão 3 — reforça: o
lado executado descreve a *evidência* e aceita o instrumento fino; o orçado descreve a
*disciplina* e só aceita o grosso.

---

## 2. Retratação: os testes **não** são correlacionados, e eu escrevi que eram

O `CLAUDE.md` diz, em 12/09, sobre os cortes de Bonferroni:

> *"Ressalva contra mim: Bonferroni **superestima** a correção com testes correlacionados,
> e estes são (mesma série, mesmos cinco fatores). O corte verdadeiro fica entre 1,96 e
> 2,891."*

**Medido, a correlação entre as estatísticas reamostradas do HML e do SMB é −0,064.**
Praticamente zero.

A causa é o próprio desenho que torna o teste não-tautológico: *"alfa contra os **demais**
fatores"* já remove os quatro fatores comuns de cada regressão. O que sobra num alfa é o
resíduo — e os resíduos de duas regressões que particionaram os mesmos regressores não
andam juntos. **A mesma decisão que impede o R² = 1 por construção também esvazia a
correlação que o Romano-Wolf existiria para aproveitar.**

Consequência: o ganho do Romano-Wolf sobre Bonferroni aqui é pequeno **por propriedade do
desenho**, e vai continuar pequeno enquanto as hipóteses forem alfas contra os demais.
Vale saber antes de esperar dele o que ele não pode dar.

*Causa raiz do erro:* eu inferi a correlação da **origem comum** dos dados ("mesma série,
mesmos fatores") em vez de medi-la. Origem comum não é dependência estatística — é a mesma
distância da régua §5-B: a frase que eu escrevi era mais larga que a medição que eu tinha.

---

## 3. O achado: a suposição de Student custa mais que a multiplicidade

Todos os cortes que o projeto vinha citando saem de uma tabela — pressupõem que o `t`
estimado segue uma t de Student com 301 graus de liberdade. Isso pode ser medido, e é: o
bootstrap devolve a distribuição real da estatística sob a nula.

**Decomposição do corte da família executada (m = 2), 10.000 repetições, semente 20260905:**

| corte | valor | o que supõe |
|---|---|---|
| Student + Bonferroni | **2,2527** | marginal **tabelada** · independência pela união |
| bootstrap + Bonferroni | **2,4033** ¹ | marginal **medida** · independência pela união |
| bootstrap + Romano-Wolf | **2,3256** | marginal **medida** · dependência **medida** |

¹ com 100.000 repetições, para estabilizar a cauda.

- ganho do Romano-Wolf sobre Bonferroni, com a mesma marginal: **−0,095** (≈ 4%);
- custo de trocar a marginal tabelada pela medida: **+0,151** (≈ 7%).

> **A suposição de distribuição vale mais que a estrutura de dependência — e só a segunda
> estava sendo discutida.** A correção de multiplicidade era o assunto; o erro maior estava
> num lugar onde ninguém tinha olhado, porque a t de Student é o padrão silencioso de toda
> regressão.

### A razão, e ela é da série, não do código

Um oráculo amarra as duas metades e está preso num teste
(`test_marginal_de_student_devolve_o_corte_de_student`): quando a amostra reamostrada
**vem** de uma t de Student, o corte medido e o tabelado coincidem dentro de 0,02. A
diferença acima, portanto, **não é defeito de implementação — é propriedade do dado.**
Retornos mensais de fatores brasileiros têm cauda mais gorda que a normal, e o `t` de uma
amostra de 306 meses herda isso.

---

## 4. O HML não sobrevive ao orçamento que ele mesmo pré-registrou

O corte do lado orçado, aplicado à marginal medida do HML:

| m | Bonferroni-Student | Bonferroni-**medido** | HML, t = 2,9351 |
|---|---|---|---|
| 1 | 1,9679 | 2,0986 | rejeita |
| 2 | 2,2527 | 2,4033 | rejeita |
| 8 | 2,7537 | 2,9337 | **NÃO_CONFIRMADO** — a margem (0,0014) é menor que o ruído |
| **13** | **2,9131** | **3,1473** | **não rejeita**, por −0,212 |

**A afirmação que o projeto vinha fazendo era:** *"o HML sobrevive até o corte mais severo
— por 0,027 de um t"*.

**A afirmação medida é:** ele não sobrevive. A folga de +0,027 existia só sob a suposição
de Student; substituída pela distribuição medida, vira um déficit de −0,212 — **quase oito
vezes a margem que se anunciava, na direção oposta.**

**Precisão declarada.** Com 10.000 repetições, o quantil 1 − α/13 fica na ponta da
reamostragem (~38 observações acima do corte). Medido em **12 sementes**: corte orçado do
HML em **3,107 ± 0,075**, mínimo 2,986, máximo 3,211. O `t` do HML (2,9351) fica abaixo do
**menor** dos doze — o veredito é robusto ao ruído. Margens menores que 0,08 nesta família
são `NAO_CONFIRMADO` sem mais repetições, e é por isso que a linha de m = 8 está marcada.

**O que isso NÃO muda:** o veredito registrado em 05/09,
`NAO_REJEITA_PARA_EFEITO_DE_DECISAO`, continua igual — ele já era conservador por quatro
razões independentes do corte (alfa negativo em 2009-2016; P(t > 1,96) = 83% no bootstrap;
73% do alfa em 12 de 306 meses; e o objeto testado não ser a estratégia investível). A
medição não derruba uma decisão: **derruba uma frase que soava mais confortável do que os
dados permitiam.**

---

## 5. A decisão 4 ganhou o primeiro caso no dia em que nasceu

Sua regra foi escrita para R1 contra uma extensão Rn. O que apareceu foi outra coisa: **os
dois lados do `m` da decisão 3 divergem sobre a MESMA execução.**

```
HML  familia EXECUTADA (m=2, Romano-Wolf)     corte 2,3256 -> REJEITA
     familia ORCADA   (m=13, Bonferroni med.) corte 3,1473 -> NAO_REJEITA
```

O portão foi escrito sobre **vereditos divergentes, venham de onde vierem**, em vez de
sobre o par R1/Rn. Generalizar custou menos que abrir uma exceção — e cláusula de exceção é
a superfície por onde o contorno entra.

O operativo, quando divergem, é o **orçado**, e a razão está no YAML: é o único dos dois
que não pode ter sido escolhido *depois* de ver o resultado. O executado só cresce quando
alguém roda mais coisa, e quem roda já viu o número anterior.

A divergência está escrita em `politica.yaml → pesquisa.divergencias_escritas`, e o portão
recusa uma linha de log no lugar de uma leitura: `leitura` com menos de 120 caracteres
continua bloqueando.

---

## 6. Dois defeitos que a própria rodada encontrou

**O quantil saturava na borda, em silêncio.** `t_quantil` bissecava num intervalo fixo de
±1000. Com 1 grau de liberdade, o quantil 99,99% fica em ~3183, e a função devolvia
**1000,0** — a borda — sem erro nenhum. É a forma F-02 outra vez: um número de borda tem a
mesma cara de um número certo. Quem encontrou foi o `test_ida_e_volta`, e é por isso que a
identidade `cdf(quantil(p)) == p` está na suíte ao lado da tabela publicada: **a tabela não
tem essa casa.** Agora o intervalo se abre e, se não couber, a função levanta.

**A guarda de campo morto pegou o meu lixo pela segunda vez em dois dias.** Criei
`CAMPOS_MEDIDOS` em `preregistro.py`, não referenciei, e o `campos_mortos` acusou — o mesmo
que aconteceu com `PONTAS_DIVERGENTES` em 16/09. Mesma mão, mesmo erro, dois dias depois.

**E o `chaves_orfas` cobrou uma coisa certa.** `corte_executado` e `corte_orcado` estavam
no diário e **só o teste** os lia — categoria "LIDA SÓ POR TESTE" da P-77, pior que órfã
pura. A conferência do registro contra a medição virou `preregistro.conferir_registro()`, e
o teste passou a chamá-la. **Conferir o registro é trabalho do módulo; o teste só chama.**

---

## 7. O que este aparato continua não protegendo (P5)

Nada aqui teria pego o `Risk_Free` invertido do E-06. Especificação congelada, diário,
contador, corte medido e portão de divergência passariam por aquilo sem piscar, porque
`tratamento_rf` só entra na lista de graus de liberdade **se alguém souber que ele existe**.
O que pegou aquilo foi um comentário em português e dois testes.

E há um limite novo, desta rodada: o bootstrap reamostra **meses independentes**. Se houver
dependência serial nos fatores, a distribuição da estatística é outra e o corte medido está
subestimado — na mesma direção do achado, não contra ele. Medir isso pede *block bootstrap*,
e não está feito.

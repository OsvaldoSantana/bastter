# P-113 — a medição, contra os critérios de `9a08a55`

**23/09/2026.** Os critérios estão em `auditoria/P113-CRITERIOS.md`, commitados e
**empurrados antes desta corrida** — commit `9a08a55`, que é a impressão digital que a
P-116 cobrava. Este arquivo é o resultado, e ele **reprova quatro dos sete critérios que
eu mesmo escrevi**.

---

## 1. O veredito, em uma linha

> **A decisão dele está implementada e o resultado é correto. A minha previsão do tamanho
> dela estava errada por um fator de quinze — e o erro é um achado (A-13), não um desvio.**

Eu previ que **172** eventos ganhariam fator. Ganharam **11**. Os outros **161 não eram
fatores faltando: eram o mesmo pagamento chegando pela segunda porta**, e dar preço a eles
teria subtraído o provento **duas vezes**.

---

## 2. Os critérios, conferidos um a um

| # | grandeza | previsto | **medido** | |
|---|---|---|---|---|
| C1 | `SEM_PRECO` resolvidos pelo COTAHIST | 172 | **11** | ❌ |
| C2 | séries `INCOMPLETO` | 18 | **74** | ❌ |
| C3 | degraus contaminados | 8 | **138** | ❌ |
| C4 | …desses, na tabela de degraus | 7 | **137** | ❌ |
| C5 | pares que ganham fator do zero | 7 | **7** | ✅ |
| C6 | pares que ganham parcela nova | 131 | **0** | ❌ |
| C7 | total de degraus | 1.593 | **1.593** | ✅ |
| R1 | as duas fontes concordam onde ambas existem | 0 divergências | **1.870 pares, 0** | ✅ |
| R2 | a B3 ganha quando existe | 0 violações | **0** | ✅ |
| R3 | o degrau encolhe (agregado e 5 anos) | sim | **sim** | ✅ |
| R4 | o controle não se move | pior 1e-27 | **1e-27** (632.375 pares) | ✅ |
| R5 | nenhuma série sai de `AJUSTADO` | 0 | **0** | ✅ |
| R6 | toda mudança atribuível | sim | **sim** | ✅ |
| R7 | duplicatas (A-12) | 206 | **206** | ✅ |

**C1–C4 e C6 reprovaram porque partiam todos da mesma premissa falsa**, e é uma premissa
só: *"173 linhas `SEM_PRECO` são 173 proventos sem fator"*.

---

## 3. A-13 — o mesmo provento chega pelas duas esteiras

As duas esteiras da B3 se sobrepõem na janela recente: `GetListedSupplementCompany`
devolve os últimos meses, o paginado devolve o histórico longo. O dividendo de setembro de
2025 está **nas duas**.

`_chave_de_evento` não as colapsa, e isso é deliberado: `origem` e `arquivo_origem` entram
nela pelo A-09, porque *"dois registros iguais em páginas diferentes são sobreposição de
paginação, e aí o julgamento seria outro"*.

**Até 23/09 isso era inofensivo por acidente.** A cópia do suplemento vinha sem preço, logo
sem fator, logo não era aplicada. **Dar preço a ela é exatamente o que a acordaria.**

> **É o P-83 na letra:** *insumo ausente adormecido num campo morto continua sendo insumo
> ausente — o campo morto não é o defeito, é o anestésico.* Lá eram zeros dormindo num
> campo que ninguém lia, e a decisão 1 é que os acordaria. Aqui é uma duplicata dormindo
> atrás de um `SEM_PRECO`, e esta mudança é que a acordaria.

Medido na janela: dos 172 que ganhariam preço, **161 têm mesmo ticker, mesmo dia, mesmo
rótulo e mesmo valor até a última casa** de um evento que o paginado já traz. (O contador
do módulo diz **162**: um deles é uma segunda cópia dentro do próprio suplemento.)

### A prova é o resíduo, e é o mesmo instrumento do A-09

2025 é o ano em que a sobreposição mora:

| | n | ajustado | **t** |
|---|---|---|---|
| **colapsando** (o que entrou) | 388 | **+0,0330%** | **+0,39** |
| sem colapsar (o que eu ia entregar) | 388 | +0,7377% | **+6,31** |

O ajuste correto deixa o dia ex de 2025 indistinguível de zero. O incorreto deixa um
resíduo de três quartos de ponto percentual com t de mais de 6 — o provento subtraído duas
vezes.

### E a armadilha vale mais que o achado

**O agregado melhorava enquanto o ano quebrava.**

| | média ajustada dos 5 anos | t |
|---|---|---|
| colapsando (correto) | −0,1909% | −2,53 |
| **sem colapsar (errado)** | **−0,0192%** | **−0,24** |

O número que parece melhor é o da versão errada: o +0,74% de 2025 cancelava o resíduo
negativo dos outros quatro anos. O laudo do C-02 já dizia por que a tabela é por ano —
*"um agregado de cinco anos esconderia um ano ruim atrás de quatro bons"*. Aqui ele
esconderia um ano **quebrado** atrás de quatro certos.

### O meu critério pré-registrado não teria pego

**R3 exigia `|ajustado| < |bruto|` no agregado e nos cinco anos. A versão errada passa nos
seis.** Encolhimento não detecta super-ajuste: um fator aplicado duas vezes ainda encolhe
um degrau de −5%, só que passa do outro lado do zero.

Quem pegou foi a **coluna de origem** — a mesma que a decisão dele mandou criar. Ver
`B3+COTAHIST=131` num relatório é uma pergunta, não um dado: *por que um degrau precisaria
de preço das duas fontes?* Sem essa coluna, os 161 teriam entrado calados.

> **A coluna de procedência que ele pediu encontrou um defeito que o critério de resultado
> não encontraria.** É a P1 pagando por si mesma: procedência não é documentação do número,
> é instrumento de medida.

---

## 4. O que ficou, medido

| | antes | depois |
|---|---|---|
| fatores do COTAHIST | 0 | **11** |
| proventos repetidos, não aplicados (A-13) | — | **162** |
| séries `AJUSTADO` | 23 | **27** |
| séries `INCOMPLETO` | 78 | **74** |
| degraus medidos | 1.586 | **1.593** |
| média ajustada, 5 anos | −0,1885% (t −2,49) | **−0,1909% (t −2,53)** |

**Por ano**, com o controle ao lado:

| ano | n | bruto | t | ajustado | t | controle (pior) |
|---|---|---|---|---|---|---|
| 2021 | 314 | −5,3689% | −5,59 | −0,2480% | −0,86 | 1e-27 |
| 2022 | 278 | −2,3641% | −9,41 | −0,4173% | −2,12 | 1e-27 |
| 2023 | 298 | −1,6752% | −10,21 | −0,0984% | −0,79 | 1e-27 |
| 2024 | 315 | +0,8093% | +0,28 | −0,2974% | −3,24 | 1e-27 |
| 2025 | 388 | +1,1646% | +0,33 | **+0,0330%** | **+0,39** | 1e-27 |

**2023 não se moveu — nem um degrau.** A previsão R6 dizia que ele mudaria; errei, e na
direção conservadora: os 11 eventos novos estão todos fora de 2023. O instantâneo dourado
do C-02 continua de pé.

---

## 5. O que continua aberto, e é decisão dele

**Das 74 séries `INCOMPLETO`, a subscrição responde por 1 hoje** — e responderia por 9 de
18 se os 161 fossem proventos de verdade. Como não são, a §5 dos critérios perde a
urgência que eu tinha previsto, mas **não perde a razão**: `diagnostico()` continua
contando `SEM_FATOR` (subscrição, que por desenho não ajusta preço) como insumo ausente, e
dizer *"o retorno desta série está errado"* por causa de uma subscrição é dizer algo falso.

Fica como estava: registrado, medido, e não mudado — reclassificar status publicado é dele.

---

## 6. As fontes da isenção — o parágrafo do C-02 que citava lei sem citar lei

O laudo `C02-JANELA-2021-2025.md` mede que o dividendo tira do preço **1,164×** o que paga,
e levanta como **hipótese `NAO_CONFIRMADO`** que isso venha da assimetria entre dividendo
isento e ganho de capital tributado a 15% (1/0,85 = 1,18). Depois enfraquece a própria
hipótese observando que boa parte do investidor marginal **não paga** esses 15%.

Esse parágrafo citava duas regras tributárias **sem fonte**. Elas agora têm:

### Pessoa física, até R$ 20 mil por mês em ações — isenta

**Lei nº 11.033/2004, art. 3º, I** — `docs/fontes/lei-11033-2004-planalto.md`, transcrito do
Planalto (`l11033compilado.htm`, acesso 03/09/2026):

> *"Art. 3º Ficam isentos do imposto de renda: I - os ganhos líquidos auferidos por pessoa
> física em operações no mercado à vista de ações nas bolsas de valores e em operações com
> ouro ativo financeiro cujo valor das alienações, realizadas em cada mês, seja igual ou
> inferior a **R$ 20.000,00 (vinte mil reais)**, para o conjunto de ações e para o ouro
> ativo financeiro respectivamente;"*

Duas coisas que a transcrição deixa explícitas e que importam para a hipótese: a isenção é
sobre o **valor das alienações no mês**, não sobre o ganho; e ela vale para o **mercado à
vista de ações**, o que a distingue de ETF e FII (`auditoria/escopo-acoes-on.md`).

### Investidor não residente — regime próprio, com exceção

A regra: o não residente que investe pelo regime de investidor estrangeiro tem tratamento
próprio, e **a exceção é o país de tributação favorecida** — abaixo de 20% — que volta a
pagar os **15%** da regra geral.

> ⚠ **`NAO_CONFIRMADO` — e a §5-B.13 manda escrever isto em vez de deixar implícito.** A
> página de investimento estrangeiro da B3 **não está em `docs/fontes/`**, e eu não a baixei
> nesta sessão. O conteúdo acima veio do enunciado dele, não de fonte primária lida por mim.
> Enquanto o documento não estiver no acervo com URL e data de acesso, esta linha é
> **afirmação sem procedência** e está marcada como tal.
>
> **O que falta é uma captura, não um caminho** — e a régua §5-B.13 é explícita sobre a
> diferença: *"não dá para fazer X" só se escreve depois de tentar X e falhar, com o erro
> transcrito*. Eu não tentei. Fica como pendência de captura (P-119), com o limiar dos 20%
> a conferir contra a norma que o define, e não contra a página que a resume.

**Por que isto importa para o número, e é o ponto do parágrafo:** se quem forma o preço no
dia ex não paga 15% sobre o ganho — porque é isento pelos R$ 20 mil, ou porque é não
residente —, a assimetria dividendo × ganho de capital **não existe para ele**, e 1,18 deixa
de ser a previsão. **O 1,164 continua medido; a explicação continua sem sustentação.**

---

## 7. O que esta rodada NÃO mediu (P5)

- **A sobreposição foi medida só na janela 2021–2025.** Fora dela o suplemento não alcança,
  então o A-13 não tem como aparecer — mas isso é inferência sobre a janela do endpoint, não
  medição sobre o acervo inteiro.
- **Os 11 eventos que ganharam fator não têm segunda testemunha.** São exatamente os casos
  em que a B3 não publicou preço; o COTAHIST é a única fonte, e R1 não os cobre por
  construção. O que os sustenta é a concordância medida nos **1.870** casos em que as duas
  existem, mais o fato de o resíduo de 2025 não piorar com eles.
- **A escolha da véspera** é o pregão anterior **da série do papel**, não o
  `ultimo_dia_com_direito`. Nos casos medidos os dois coincidem; onde o papel não negociou
  no último dia com direito, eles divergem, e nenhum caso desses foi observado aqui.

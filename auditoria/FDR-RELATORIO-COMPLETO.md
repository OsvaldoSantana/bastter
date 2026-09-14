# Testes múltiplos em backtests — relatório de pesquisa

> ## Procedência deste documento — leia antes
>
> **Quem escreveu:** um subagente meu com acesso à web, em 12/09/2026, a partir de um
> enunciado que pedia fontes primárias e proibia inventar números, datas ou títulos.
>
> **O que EU verifiquei por conta própria**, recalculando aqui antes de usar:
> os limiares de `t` de Bonferroni, BH e BY para m = 8 e m = 13, com a **t de Student,
> 301 gl**. Batem com os do relatório em três casas decimais. É a parte que decide a
> escolha, e é a parte que eu conferi.
>
> **O que eu NÃO verifiquei:** a simulação de FWER sob correlação (200.000 réplicas,
> feita pelo subagente), e as citações bibliográficas uma a uma. O relatório traz uma
> tabela de verificação fonte a fonte no fim — **use-a**: várias entradas estão
> marcadas como parcialmente confirmadas ou não confirmadas, e isso é informação, não
> defeito.
>
> **Status deste documento: `PARCIAL`.** A conclusão operacional está em
> `FDR-PESQUISA-AMPLIADA.md`, que só usa o que foi conferido.

---

## Sumário executivo (do subagente)

1. Para 8 a 13 testes pré-registrados e correlacionados, com 306 meses, o excesso de
   conservadorismo do Bonferroni é **pequeno**. Com correlação média 0,4 entre as
   estratégias, o FWER real do Bonferroni a 5% é 4,3% em vez de 5,0%, e o limiar que
   ele exige excede o limiar exato do máximo-|t| em apenas **0,05**. A intuição de que
   "Bonferroni é devastadoramente conservador" vem da genômica (m = 10.000+) e **não**
   se transfere para m = 8.

2. **Benjamini-Yekutieli é má escolha aqui:** com m = 8, para uma descoberta isolada o
   BY exige |t| ≥ 3,08 e o Bonferroni |t| ≥ 2,75. **O BY é mais rigoroso que o
   Bonferroni**, apesar de controlar um critério de erro mais frouxo.

3. A recomendação de **t > 3,0** (Harvey, Liu & Zhu 2016) foi calibrada para **316
   fatores** testados por uma literatura inteira. Aplicá-la a 8 hipóteses
   pré-registradas contabiliza a multiplicidade duas vezes. Os próprios autores
   recuaram em 2020: *"nem 2,0 nem 3,0 é ótimo"*.

4. Há **divergência genuína e não resolvida** sobre se os limiares devem subir. Chen
   (Federal Reserve Board) argumenta que os dados não identificam a resposta;
   Jensen, Kelly & Pedersen (2023) tratam a correlação entre fatores como *força*.

5. **Recomendação:** Romano-Wolf stepdown por bootstrap, com Holm como verificação.

---

## 1. Bonferroni

Controla a **FWER** — probabilidade de ao menos um erro tipo I na família. Rejeita
quando pᵢ ≤ α/m. A garantia vem da desigualdade de Boole e **não depende da estrutura
de dependência**: essa é a virtude e a origem do conservadorismo, porque é obtida
assumindo o pior caso.

> Romano & Wolf (2005): métodos como o Bonferroni "não levam em conta a estrutura de
> dependência" e obtêm controle "assumindo uma estrutura de dependência de pior caso".

**Simulação do subagente** (equicorrelação, T = 306, gl = 300, 200.000 réplicas) —
**não verificada por mim**:

| m | ρ | t Bonferroni | FWER real | t máx exato (95%) | excesso |
|---|---|---|---|---|---|
| 8 | 0,00 | 2,754 | 4,95% | 2,750 | 0,004 |
| 8 | 0,20 | 2,754 | 4,84% | 2,742 | 0,012 |
| 8 | 0,40 | 2,754 | 4,31% | 2,702 | 0,052 |
| 8 | 0,60 | 2,754 | 3,54% | 2,629 | 0,124 |
| 8 | 0,80 | 2,754 | 2,53% | 2,490 | 0,264 |
| 13 | 0,40 | 2,913 | 4,15% | 2,846 | 0,067 |

HLZ estimam que a correlação média entre retornos de fatores é baixa, "possivelmente na
vizinhança de 0,20".

---

## 2. FDR — Benjamini-Hochberg e Benjamini-Yekutieli

**BH (1995):** FDR é a proporção esperada de hipóteses falsamente rejeitadas **entre as
rejeitadas**. Procedimento step-up: ordene p₍₁₎ ≤ … ≤ p₍ₘ₎, ache o maior *i* com
p₍ᵢ₎ ≤ (i/m)·q, rejeite até *i*.

Do resumo do artigo: o FDR "é equivalente à FWER quando todas as hipóteses são
verdadeiras, e é menor caso contrário". **Sob a nula completa, FDR = FWER** — o BH só
ganha poder quando já existem descobertas verdadeiras.

**BY (2001), Teorema 1.2** (transcrito do PDF da página do próprio Benjamini):

> "If the joint distribution of the test statistics is PRDS on the subset of test
> statistics corresponding to true null hypotheses, the Benjamini Hochberg procedure
> controls the FDR at level less than or equal to (m₀/m)q."

A condição PRDS cobre "estatísticas de teste normais multivariadas com matriz de
correlação positiva" e t multivariada — ou seja, **se as correlações forem todas
não-negativas, o BH comum já é válido** e o BY é desnecessário.

**Teorema 1.3:** sob dependência arbitrária, usa-se q/Σ(1/i) no lugar de q.

**VERIFICADO POR MIM** (t de Student, 301 gl):

| m | c(m) = Σ1/i | Bonferroni (p / \|t\|) | BH 1ª descoberta | BY 1ª descoberta |
|---|---|---|---|---|
| 8 | 2,7179 | 0,00625 / **2,754** | 0,00625 / **2,754** | 0,00230 / **3,075** |
| 13 | 3,1801 | 0,00385 / **2,913** | 0,00385 / **2,913** | 0,00121 / **3,268** |

**O limiar da primeira descoberta do BH é idêntico ao do Bonferroni** — `(1/m)·α = α/m`.
O BH só afrouxa a partir da segunda rejeição.

---

## 3. A literatura de finanças

**Harvey, Liu & Zhu (2016)**, *"… and the Cross-Section of Expected Returns"*, RFS
29(1), 5–68 — catalogam **316 fatores** em 313 trabalhos e concluem que "um novo fator
precisa superar um obstáculo muito mais alto, com uma estatística t maior que 3,0".
Limiares por método (M = 316): Bonferroni 3,78 · BHY 1% 3,39 · BHY 5% 2,78. Ajustando
para dados faltantes: "em vários cenários, o limiar mínimo de t é 3,18".
Notavelmente, **recusam-se a escolher** entre FWER e FDR.

**Harvey & Liu (2015)**, *"Backtesting"*, JPM — o *haircut* do Sharpe.
Recomendam **BHY** para finanças. Resultado-chave e **não-linear**: haircuts para
Sharpe < 0,4 excedem 50%; para Sharpe > 1,0 são no máximo 25%. Isso **contradiz a
prática de mercado de aplicar desconto uniforme de 50%**.

**White (2000)**, *Reality Check*, Econometrica 68(5) — H₀: o melhor modelo da busca não
supera o benchmark. Bootstrap estacionário (Politis-Romano); calcula-se o **máximo** das
diferenças reamostradas.

**Hansen (2005)**, SPA, JBES 23(4) — "mais poderoso e menos sensível a alternativas
ruins e irrelevantes" que o Reality Check. *(Texto integral inacessível ao subagente.)*

**Romano & Wolf (2005)**, StepM, Econometrica 73(4) — prossegue em etapas, mantendo
controle assintótico da FWER. "Captura implicitamente a estrutura de dependência
conjunta das estatísticas". **Está para o Holm como o Holm está para o Bonferroni.**

**Bailey & López de Prado (2014)**, *Deflated Sharpe Ratio* — E[max{ŜR}] sob a nula,
com a constante de Euler-Mascheroni. Converte M tentativas dependentes em independentes:
**N̂ = M/[1+(M−1)·ρ̄]**. Com M = 8 e ρ̄ = 0,4 → **N̂ ≈ 2,1 tentativas efetivas**.

**PBO/CSCV** (Bailey, Borwein, López de Prado & Zhu) — mede overfitting de **varredura
de parâmetros**. Com 8 estratégias pré-registradas e sem otimização, **fora de escopo**.

**Posteriores a 2020:**
- **Harvey & Liu (2020)**, *False (and Missed) Discoveries*, JF 75(5) — a literatura
  negligenciou o **erro tipo II**; "nem 2,0 nem 3,0 é ótimo"; o ideal fica entre os dois.
- **Jensen, Kelly & Pedersen (2023)**, JF 78(5) — correções frequentistas são
  "desnecessariamente grosseiras"; modelo bayesiano hierárquico; taxa de replicação
  82,4%. "Ter muitos fatores pode ser uma força."
- **Chen (2024)**, arXiv:2204.10275, working paper do Federal Reserve Board — a fração
  de fatores falsos é **fracamente identificada**; o IC de 90% vai de 0,01 a 0,90, o que
  deixa **1,96 defensável**.
- **Chordia, Goyal & Saretto (2020)**, RFS 33(5) — 2 milhões de estratégias aleatórias;
  recomendam **3,84 / 3,38**, ainda mais alto que HLZ.
- **Bouamara, Laurent & Shi (2025)**, JFEC 23(5) — *stepwise Cauchy*, menor
  conservadorismo sob dependência. **Fronteira, não prática consolidada.**

---

## 4. Receita do Romano-Wolf StepM para este caso

1. **Estatísticas observadas:** rode as 8 regressões, guarde t̂₁…t̂₈.
2. **Imponha a nula** — passo crítico: r̃ⱼ,ₜ = rⱼ,ₜ − α̂ⱼ (ou use os resíduos).
3. **Reamostre em blocos, com as 8 juntas:** sorteie blocos de **índices de tempo** e
   aplique **o mesmo conjunto às 8 séries**. É isso que preserva a correlação
   transversal. Bloco médio de 3 a 12 meses para dado mensal; teste a sensibilidade.
4. **Reestime** em cada réplica e calcule M* = max|t*ⱼ|.
5. **Valor crítico** = quantil 95% dos M*.
6. **Stepdown:** removidas as rejeitadas, recalcule o máximo só sobre as restantes e
   repita. A FWER permanece controlada.

**Advertências:** (a) não reamostre as estratégias independentemente — destrói a
correlação e anula o método; (b) com 10.000 réplicas o erro de Monte Carlo no quantil é
da ordem de ±0,03 em `t`; (c) o **IML** do NEFIN sugere autocorrelação — use blocos, não
i.i.d.; (d) o bootstrap corrige a multiplicidade de 8 testes, **não** o fato de as
ideias virem de uma literatura que já minerou os mesmos dados.

---

## 5. Tabela de verificação de fontes (do subagente)

| fonte | status |
|---|---|
| Benjamini-Yekutieli 2001 | ✅ texto integral, página do autor; teoremas transcritos |
| Benjamini-Hochberg 1995 | ⚠️ folha de rosto confirmada; corpo é digitalização sem texto |
| Harvey-Liu-Zhu 2016 | ✅ texto integral (NBER WP 20592) |
| Harvey & Liu 2015 | ✅ texto integral, página do autor |
| White 2000 | ✅ texto integral |
| Romano & Wolf 2005 | ✅ texto integral |
| Hansen 2005 | ⚠️ citação confirmada; texto inacessível (403/robots) |
| Deflated Sharpe Ratio | ⚠️ versão "Forthcoming"; página final não confirmada |
| PBO | ⚠️ discrepância 2016/2017 não resolvida |
| Harvey & Liu 2020 | ✅ texto integral |
| Jensen-Kelly-Pedersen 2023 | ✅ versão do editor |
| Chen 2024 | ⚠️ working paper, não revisado por pares |
| Chordia-Goyal-Saretto 2020 | ⚠️ mecanismo de bootstrap não confirmado |
| Goeman & Solari | ⚠️ pré-print; volume/páginas publicados não confirmados |
| Harvey 2017 Presidential Address | ⚠️ só citação; **conteúdo não lido** |
| Westfall & Young 1993 | ❌ **secundária** — livro não acessado |
| NEFIN | ✅ site oficial |

**Números marcados como cálculo do subagente:** a tabela de conservadorismo (simulação),
os fatores harmônicos, o N̂ do DSR e as conversões t→IR. Não vêm de nenhum artigo.
Os limiares de `t` das seções 2 e 3 **eu recalculei** — ver o cabeçalho.

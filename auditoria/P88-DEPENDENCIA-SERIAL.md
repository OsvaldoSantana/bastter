# P-88 — a dependência serial existe, e o corte estava subestimado em ~8%

**19/09/2026.** Fecha a **P-88**, aberta em 18/09. Instrumento:
`auditoria/p88_block_bootstrap.py` (+ 18 testes).

---

## 1. A limitação que ele fecha, citada

Do `CLAUDE.md`, 18/09, na seção *"O que este aparato continua não protegendo (P5)"*:

> *"Entra um limite novo: o bootstrap reamostra **meses independentes** — se houver
> dependência serial, o corte medido está **subestimado**, na mesma direção do achado.
> Medir isso pede *block bootstrap*, e não está feito."*

**Está medido. A previsão estava certa, e o número é ~8%.**

## 2. Calibração primeiro — sem ela, nada abaixo prova nada

Antes de comparar qualquer coisa, o instrumento tem de reproduzir o registrado. Reproduz:

| | registrado em 18/09 | medido aqui |
|---|---|---|
| `hash_fonte` da série | — | `619991c2192c` |
| meses na amostra | 306 | **306** |
| `t` do HML | 2,9351 | **2,9350907** |
| corte iid, m=13, semente 20260905 | **3,1473** | **3,1473** |

> Um corte por bloco maior **não provaria nada** sem esta tabela: poderia ser a minha
> implementação diferindo da registrada, e não a dependência serial. `L=1` é literalmente o
> sorteio iid do `bootstrap_t` — há um teste que compara os índices sorteados, não só o
> número final.

## 3. Existe dependência? Em um dos dois — e é isso que dá o controle

Autocorrelação e Ljung-Box(12), com erro padrão de cada ρ = 1/√306 = 0,0572:

| série | ρ₁ | ρ₂ | ρ₃ | **LB(12) p** |
|---|---|---|---|---|
| HML bruto | +0,117 | −0,154 | −0,106 | **0,001** |
| **HML resíduo da regressão** | **+0,115** | **−0,105** | −0,050 | **0,031** |
| SMB bruto | +0,098 | +0,009 | −0,086 | 0,386 |
| **SMB resíduo da regressão** | −0,024 | −0,014 | −0,012 | **0,166** |

**O resíduo é o que importa** — é a série que o bootstrap reamostra. Medir o bruto
responderia outra pergunta, e é a forma do erro que a régua §5-B persegue.

**O HML tem dependência (p = 0,031). O SMB não (p = 0,166).** Mesma amostra, mesmo número
de parâmetros, mesmo procedimento — e um tem, o outro não. **É o controle perfeito, e ele
não foi construído: estava ali.**

## 4. O corte muda — e o controle é o que impede a leitura errada

Moving block bootstrap circular, 10.000 repetições, **4 sementes por L**:

| L | blocos distintos | HML | sd | vs iid | folga do HML | SMB (controle) | vs iid | **líquido** |
|---|---|---|---|---|---|---|---|---|
| 1 | 306 | 3,1099 | 0,065 | — | −0,175 | 2,8473 | — | — |
| **2** | 153 | 3,2909 | 0,040 | **+5,8%** | −0,356 | 2,7736 | −2,6% | **+8,4%** |
| **3** | 102 | 3,3133 | 0,055 | **+6,5%** | −0,378 | 2,7695 | −2,7% | **+9,3%** |
| **4** | 77 | 3,2330 | 0,061 | +4,0% | −0,298 | 2,7639 | −2,9% | **+6,9%** |
| **6** | 51 | 3,2145 | 0,024 | +3,4% | −0,279 | 2,6991 | −5,2% | **+8,6%** |
| **8** | 39 | 3,1931 | 0,036 | +2,7% | −0,258 | 2,7083 | −4,9% | **+7,6%** |
| 12 | 26 | 2,9970 | 0,067 | −3,6% | −0,062 | 2,6482 | −7,0% | +3,4% |
| 18 | 17 | 3,0107 | 0,050 | −3,2% | −0,076 | 2,8273 | −0,7% | −2,5% |
| 24 | **13** | 2,9624 | 0,067 | −4,7% | −0,027 | 2,7573 | −3,2% | −1,6% |

**Os sinais são opostos na faixa informativa.** O HML sobe; o controle desce. E o efeito
líquido — o excesso do HML sobre o controle — fica entre **+6,9% e +9,3%**, estável nos
cinco comprimentos.

### A degeneração, e por que o controle não era opcional

Com n = 306, `L = 24` dá **13 blocos distintos** por replicação. O bootstrap perde poder de
reamostragem e o corte **cai** — por artefato do reamostrador, não por menos dependência.

> **Sem o controle eu teria lido a queda em L ≥ 12 como *"a dependência não importa"*** — a
> conclusão errada pelo motivo errado. O SMB mede o artefato puro; o HML mede artefato +
> dependência; a diferença isola a dependência. É o mesmo desenho do `meses_que_carregam`,
> onde *"o controle importa tanto quanto o teste: se todo fator morresse igual, a medida não
> diria nada"*.

A faixa informativa é **L = 2 a 8** (≥ 39 blocos), e a fronteira é aritmética, não opinião.

## 5. O veredito — e ele não exige escolher um L

A P-88 pedia *"escolher o comprimento do bloco **com medição de sensibilidade**, e não por
convenção — senão troca-se uma suposição tabelada por outra"*.

**A medição de sensibilidade mostrou que a escolha é dispensável para esta decisão:**

| faixa | veredito | margem × ruído |
|---|---|---|
| **L = 1 a 8** (informativa) | **NÃO REJEITA**, em todas as 4 sementes | −0,175 a −0,378 contra sd 0,02–0,07 |
| L = 12 e 24 (degenerada) | **`NAO_CONFIRMADO`** | −0,062 e −0,027 contra sd 0,067 |

> **E o teste me corrigiu aqui.** Eu havia escrito *"o veredito não muda em nenhum L"*, e
> ele falhou: com `L = 24` e certas sementes o corte cai a **2,9087** e o `t = 2,9351`
> **passa**. Fui medir as quatro sementes de cada L, e a afirmação correta é mais estreita e
> mais forte — em toda a faixa informativa e em todas as sementes, o HML não sobrevive.
>
> **Margem menor que o ruído de semente é `NAO_CONFIRMADO`, não veredito** — a mesma régua
> que deixou o m=8 marcado em 18/09. E os dois L que caem nessa faixa são justamente os
> degenerados: a perda de reamostragem **alarga o próprio ruído** que torna o veredito
> inconclusivo ali.

**A limitação era conservadora, exatamente como o `CLAUDE.md` dizia.** A folga do HML piora
de **−0,175** para **−0,26 a −0,38**. Aplicando o efeito líquido ao corte iid, o corte
corrigido fica em **~3,36** e a folga em **~−0,45**.

**O veredito de 05/09 continua o mesmo, pela quarta razão independente.** O que muda é o
tamanho da margem: ela era fina, e é mais larga do que se pensava — na direção de não agir.

## 6. O que NÃO foi medido (P5)

1. **Romano-Wolf não entrou.** Só a marginal com Bonferroni medido, porque
   `alocacao/multiplicidade.py` não estava disponível nesta sessão — o container tem a
   versão do `backtest_h1_h3.py` **anterior a 18/09**, sem `bootstrap_conjunto`. Integrar
   `corte_*_por_bloco` ali é o passo seguinte, e só então o número absoluto vale para as
   duas correções.
2. **A correção pela degeneração é inferência, não medição.** O "efeito líquido" supõe que o
   artefato do reamostrador é o mesmo nas duas séries — plausível (mesma n, mesma k, mesmo
   procedimento) e **não medido**. `NAO_CONFIRMADO` para o número corrigido (~3,36);
   **MEDIDO** para o sinal, para a faixa bruta e para o veredito.
3. **Quatro sementes, não doze.** Em 18/09 o iid foi medido com doze (3,107 ± 0,075). Quatro
   bastam para separar as diferenças medidas aqui (0,08 a 0,20) do ruído (~0,05), e isso está
   verificado na tabela — mas é uma amostra menor de sementes, e o sd de cada linha carrega
   essa limitação.
4. **Só o HML e o SMB.** As outras onze estratégias pré-registradas nunca foram ao dado
   (`m_orcado − m_executado = 11`), então não há resíduo para medir dependência nelas.
5. ~~A última versão do teste não foi executada.~~ **Executada: 18 passed, ruff limpo.**

   > Esta linha ficou escrita por uma hora, e o motivo vale registrar. A ferramenta de shell
   > caiu no meio da rodada, e eu escrevi aqui que o teste corrigido estava sem execução —
   > **o que era verdade quando escrevi.** Quando o shell voltou, a suíte falhou com o
   > **nome antigo** do teste, e a mensagem de erro revelou o que eu não sabia: **a chamada
   > que aplicava a correção foi justamente a que o shell derrubou.** O patch nunca tinha
   > sido aplicado, e eu documentei como "corrigido, sem rodar" algo que estava
   > "não corrigido, sem rodar".
   >
   > **Declarar a incerteza foi o que permitiu achar isso.** Se eu tivesse escrito
   > *"corrigido"* e seguido, a divergência entre o laudo e o arquivo sobreviveria até segunda
   > — e seria o defeito recorrente da casa: *um arquivo declara um comportamento que o código
   > não tem.* A nota de incerteza é o que faz esse par ser conferido em vez de acreditado.

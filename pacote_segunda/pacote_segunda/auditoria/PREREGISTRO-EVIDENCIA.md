# O pré-registro, contra a evidência — e a recomendação que eu mudo

Você confirmou o desenho e pediu: *"tente estudar em referências para validar a decisão
com evidências"*. Estudei. **A evidência apoia duas das quatro camadas, é ambígua numa,
e contraria a quarta — que é justamente a que eu recomendei.**

> Relatório completo, com 25 fontes e marcação de fonte primária lida × secundária ×
> não confirmada, em `auditoria/PREREGISTRO-RELATORIO-COMPLETO.md`. **Status `PARCIAL`:**
> a pesquisa é de um subagente com acesso à web; eu não reli os 25 artigos.

---

## 1. A camada que a evidência contraria — o contador como alarme

Eu recomendei: *"`variantes_permitidas` não bloqueia; exige justificativa escrita"*. O
argumento era seu e eu o comprei: trava dura se contorna, e quem contorna rodando por
fora destrói o registro.

**A evidência disponível não apoia isso, e em parte diz o contrário.**

**Lerner & Tetlock (1999)**, o artigo canônico de *accountability*, é **condicional**:
prestar contas melhora o julgamento quando o viés vem de falta de esforço — e **piora**
em duas situações. A segunda é a sua:

> *accountability* piora quando as escolhas envolvem **"options easiest to justify"**.

E há a distinção de audiência: audiência com visões **desconhecidas** produz
autocrítica preemptiva; audiência com visões **conhecidas** produz **conformidade**. A
sua audiência é você mesmo.

**Junte as duas.** "Rodar mais uma variante" é sempre a opção mais fácil de justificar —
há sempre uma razão metodológica plausível para testar outra janela, outro filtro. Um
requisito de justificativa escrita, dirigido a si mesmo, pode funcionar como **máquina
de produzir licenças**, não como freio.

E há medição direta do formato, não só do framework:

| estudo | achado |
|---|---|
| de Langhe, van Osselaer & Wierenga (2011) | *process accountability* **melhora** tarefa linear (p<0,05); **nenhuma vantagem** em tarefa configural (t=0,51, **p>0,61**) |
| Sharon, Drach-Zahavy & Srulovici (2022), meta-análise, 9 experimentos, 1.080 sujeitos | efeito global **nulo** (−0,09); **em tarefas complexas, accountability de RESULTADO é superior — d ≈ −0,48** |

Backtestar 8 estratégias contra a mesma série é tarefa **configural** por qualquer
definição: janela × filtro × universo × custo **interagem**, não são aditivas.

**E o dado mais desconfortável:** a trava mais dura que existe em pesquisa — a revisão
Stage 1 dos Registered Reports, que congela o protocolo antes de ver o dado — é a que
tem **os maiores efeitos medidos**. Hipóteses apoiadas: **43,7% em RRs contra 96,1% na
literatura padrão** (Scheel, Schijen & Lakens, 2021; 71 RRs × 152 artigos). Isso é
evidência **a favor da trava**.

---

## 2. O problema estrutural, e ele atravessa tudo

> **Todo benefício demonstrado na literatura vem de arranjos com um verificador
> externo** — revisão Stage 1, ou registro público auditável. O seu sistema é
> auto-registro sem leitor.

Essa é a variável que separa os estudos que acharam efeito dos que não acharam:

- **Brodeur et al. (2024)**, 15.992 estatísticas de teste em 314 RCTs de economia:
  *"we find **no evidence** that pre-registration in itself reduces p-hacking and
  publication bias"*. **O que funciona é o plano de análise detalhado**, não o ato de
  registrar. Viés de publicação: **1,38×** com plano contra **2,09×** sem.
- **van den Akker et al. (2023)**, 193 estudos pré-registrados pareados: proporção de
  resultados significativos **0,69 contra 0,68**, **p = 0,96**. Sem diferença.
- **Soderberg et al. (2021)**: RRs ganham em rigor metodológico (0,99) e analítico
  (0,97), e são **indistinguíveis de zero** em novidade (0,13) e criatividade (0,22).
  *Pré-registro compra rigor; não compra descoberta.*

**Mas você tem um verificador externo e talvez não tenha percebido: o repositório é
público, com commits datados.** Um pré-registro commitado antes da execução, num
histórico que você não pode reescrever sem deixar rastro, é muito mais perto de um
`clinicaltrials.gov` do que de uma anotação privada. **Isso é o que salva o desenho** —
e implica uma regra concreta: *o commit da especificação precisa ser anterior ao commit
do resultado, e isso é verificável por qualquer pessoa.*

---

## 3. A camada mais bem sustentada é a que veio de finanças

O **diário de execuções** é a sua camada forte, e a sustentação é categórica: Bailey &
López de Prado sustentam que um backtest sem o **número de tentativas** não permite
avaliação — é o insumo que o Deflated Sharpe Ratio exige para descontar o máximo
esperado sob a nula. Você tem esse insumo por construção.

E ele resolve o item 3 que você respondeu (*"os dois `m`"*): registrar tentativas
executadas **e** orçadas é exatamente o que o DSR precisa.

---

## 4. E o desvio é a regra, não a exceção

O relatório traz evidência de que pré-registros são rotineiramente desviados sem
declaração — inclusive **73,68% de desvio não declarado** num Registered Report recente
sobre aderência. Se o desvio é a regra, **um registro que só documenta não protege.**

Isso reforça a mesma conclusão: o que protege é a **restrição verificável**, não a nota
de intenção.

---

## 5. O que eu mudo na recomendação

| | antes | agora |
|---|---|---|
| contador | alarme com justificativa escrita | **trava**, com uma saída nomeada |
| a saída | — | **nova versão pré-registrada**, com novo id, novo commit, e o resultado anterior preservado |

**Por que a trava com saída, e não a trava pura.** A objeção do Chambers & Tzavella é
real: trava rígida é inadequada para trabalho exploratório e custa atraso. A saída
resolve isso sem virar licença: quando você quer a 2ª variante além do orçado, **não
escreve uma justificativa — cria um `v2`**, com especificação própria, `m` próprio, e o
`v1` fica de pé com o resultado dele. O custo de exceder não é um parágrafo: é **admitir
publicamente que é outro experimento**.

Isso conversa com a sua 4ª regra, que eu continuo achando a melhor de todas: *extensão
não sobrescreve, correção não apaga, variante não apaga a especificação anterior.*

**E acrescento uma camada zero, que a evidência diz ser a que mais importa:** o plano de
análise **detalhado**, não o registro. Brodeur mede que registrar sem plano não muda
nada. As suas 8 estratégias precisam, cada uma, do `rejeita_se` com **corte numérico**,
do modelo, da amostra e do tratamento da variável dependente escritos **antes** — que é
o que o modelo de dados já prevê, e que hoje só o `hml_puro_v1` tem de fato.

---

## 6. Onde a evidência é silenciosa, e eu não vou preencher

- **Não existe estudo** comparando regra rígida × regra com justificativa **em
  metodologia de pesquisa**. O subagente procurou e não achou; o que usei acima é a
  literatura de *accountability*, que é **adjacente**, não direta.
- **Não há evidência primária** de que travas rígidas sejam "burladas" em pesquisa. Se
  alguém disser que há, peça a citação — não foi encontrada.
- **Kaplan & Irvin (2015)**, o achado mais citado a favor do pré-registro (57% → 8% de
  resultados positivos em ensaios do NHLBI), é **n = 55 sem controle**, e os próprios
  autores escrevem que *"we cannot say that trend... is causal"*. Sugestivo, não prova.
- Quase toda essa literatura é de **psicologia e medicina**. Você é um indivíduo
  testando estratégias contra a própria série. **A transferência é uma suposição minha**,
  e está declarada.

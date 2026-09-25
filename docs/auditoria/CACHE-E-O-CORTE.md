# O cache não reordena prioridade — e eu disse que reordenava

**19/09/2026.** Fecha o item 1 da **P-103**. Fonte primária:
[Prompt caching — platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching),
lida nesta data.

---

## 1. Retratação, e é a segunda em dois dias sobre o mesmo tema

**O que eu afirmei**, ontem no laudo `AUDITORIA-PLANO-DE-TOKENS.md` §3 e hoje na §11.4 do
`CLAUDE.md`:

> *"Cortar arquivo estável rende ~10% do que o plano calcula. Reduzir o que varia por turno
> rende 100%."*
>
> *"O split em 6 arquivos lidos sob demanda **destrói o cache**."*

**As duas são falsas**, e a primeira está errada por **20 vezes**.

### O que a fonte diz

| | multiplicador sobre o token de entrada base |
|---|---|
| cache **write**, TTL 5 min | **1,25x** |
| cache **write**, TTL 1 h | **2,0x** |
| cache **read** | **0,1x** |

E três mecânicas que decidem o resto:

- *"Cache hits require 100% identical prompt segments"* — hash **cumulativo** do prefixo;
  mudar qualquer bloco **no ou antes** do breakpoint muda o hash.
- *"The lookback window is 20 blocks."* O sistema checa no máximo 20 posições por
  breakpoint; fora da janela, **não há hit mesmo com conteúdo idêntico.**
- Mínimo para cachear no Opus 5: **512 tokens**. Máximo de **4** breakpoints.

### A causa raiz do meu erro

**Eu medi o `read` (0,1x) e concluí sobre o cache.** Ignorei duas coisas que a mesma página
diz:

1. **O `write` é 2,0x**, não 1,0x — estabelecer contexto estável custa **o dobro** de não
   cachear.
2. **O TTL é de 1 hora e as sessões deste projeto são espaçadas por dias.** Logo **nunca há
   hit entre sessões**: toda sessão paga o write a 2,0x na primeira leitura.

> É a régua §5-B na forma de sempre: **a medição estava certa, errada era a pergunta que eu
> achei que ela tinha respondido.** `read = 0,1x` é verdade; *"logo o estável quase não
> custa"* não segue dela.

---

## 2. A aritmética — e ela é mais simples do que os dois lados supuseram

Custo de uma sessão de **N** turnos, em unidades de token-de-entrada-equivalente, para um
prefixo estável de **T** tokens:

```
custo(T, N) = T × 2,0        (o write, uma vez por sessão)
            + T × 0,1 × (N−1)   (os reads)
```

**Leitura de sessão medida hoje:** `CLAUDE.md` + `PENDENCIAS.md` + `PLANO.md` = **99.564
tokens**. Blocos de citação `>` do `CLAUDE.md` = **25.113** (49% dele, 25,2% da leitura).

| turnos | hoje | sem os blocos `>` | economia | **%** |
|---|---|---|---|---|
| 5 | 238.954 | 178.682 | 60.271 | **25%** |
| 10 | 288.736 | 215.908 | 72.828 | **25%** |
| 20 | 388.300 | 290.359 | 97.941 | **25%** |
| 40 | 587.428 | 439.261 | 148.167 | **25%** |

> **O achado está na última coluna: 25% em qualquer número de turnos.**
>
> É óbvio depois de escrito — o cache multiplica **todo** o prefixo pelo mesmo fator, então
> **cortar X% do prefixo corta X% do custo dele, com cache ou sem cache.** O cache reduz o
> valor absoluto e **não mexe na ordem de prioridade nenhuma.**
>
> **Eu inventei uma inversão de prioridade que a aritmética não sustenta.** E o número que
> eu chutei — "~10%" — era o multiplicador do `read` usado como se fosse o fator de
> economia. Confundi o preço com a derivada.

**Em termos absolutos:** cortar 25.113 tokens economiza **50.226 unidades só no write**, ou
seja **2,0× o tamanho cortado** — não 0,1×. Numa sessão de 20 turnos, **97.941 unidades**,
que é praticamente **uma leitura inicial inteira**.

---

## 3. O cache compensa a partir de 3 turnos, e isso importa

```
write 2,0x + read 0,1x × (N−1)  <  N × 1,0    →    N > 2,11
```

| TTL | cache passa a compensar em |
|---|---|
| 1 h (2,0x) | **3 turnos** |
| 5 min (1,25x) | **2 turnos** |

**Consequência para este projeto:** uma sessão de uma ou duas perguntas com 99.564 tokens de
leitura inicial **custa mais com cache de 1 h do que sem cache**. Não é acionável por mim —
não escolho o TTL —, mas é um argumento a favor de sessões longas em vez de várias curtas,
e contra reler os arquivos numa sessão que vai fazer uma pergunta só.

---

## 4. O risco real do split, e não é o que eu disse

**Não é invalidação de prefixo.** Se o conteúdo estável for lido **antes** do variável, o
prefixo até ele é idêntico em toda sessão e o hit acontece. Minha frase *"o split destrói o
cache"* supunha que os anexos entravam antes, e eu não verifiquei.

**O risco é a janela de 20 blocos.** Cada arquivo lido e cada chamada de ferramenta é um
bloco. Com um breakpoint só:

| arquivos de leitura | chamadas de ferramenta até a janela estourar |
|---|---|
| 3 (hoje) | ~17 |
| 6 (o split dos planos) | ~14 |
| 9 | ~11 |

Fora da janela, **não há hit mesmo com conteúdo idêntico** — e aí se paga write a 2,0x
outra vez, no meio da sessão. **Mais arquivos = janela estoura mais cedo.**

E há um segundo limite: **512 tokens é o mínimo para cachear** no Opus 5. Fragmentar em
arquivos pequenos cria blocos que **nunca** cacheiam, e a documentação avisa que isso
acontece **sem erro nenhum** — *"no error is returned"*. É o F-02 na camada de faturamento:
ausência de aviso lida como sucesso.

---

## 5. Veredito, e ele muda a recomendação de ontem

**A Decisão C está liberada, com número: −25% da leitura de sessão.** Não dependia de medir
o cache para valer — e é isso que eu errei ao dizer que dependia.

**Mas a FORMA muda.** Os três planos propunham 6 a 9 arquivos. A fonte diz que isso piora a
janela e arrisca blocos abaixo do mínimo. A forma que a medição sustenta é:

| | |
|---|---|
| **Dois arquivos, não seis** | `CLAUDE.md` (instrução + doutrina + régua) e `ACHADOS.md` (história + retratação). Menos blocos, cada um muito acima de 512 tokens |
| **O estável primeiro** | ler `CLAUDE.md`/`PENDENCIAS.md`/`PLANO.md` no começo, antes de qualquer ferramenta — é o que mantém o prefixo idêntico |
| **`REGUA.md` separado: NÃO** | já estava recusado por P7 (*quem decide se a tarefa envolve medição é a sessão, que é quem erra*), e agora também por ser bloco extra na janela. **Duas razões independentes, e a primeira ainda é a que vale** |
| **`FECHADAS.md`: sim** | 7.457 tokens, e é conteúdo consultado por `grep`, não lido |

---

## 6. O que continua NÃO medido (P5)

1. **Não medi faturamento.** Tudo aqui é aritmética sobre multiplicadores publicados, não
   observação de `cache_read_input_tokens` numa resposta real. **Não tenho o instrumento** —
   não vejo os campos de uso da minha própria sessão.
2. **Não sei quantos blocos uma sessão típica gasta**, nem quantos breakpoints este ambiente
   coloca, nem onde. A tabela da §4 supõe **um** breakpoint e um bloco por chamada; com os 4
   permitidos, a janela se comporta diferente e o risco cai.
3. **Não sei se este ambiente usa TTL de 1 h em toda chamada.** Ele o declara, e eu tomei
   como dado. Se for 5 min em parte das chamadas, o write cai para 1,25x e os números da §2
   caem ~37% — **sem mudar a coluna dos 25%**, que é a que decide.
4. **Nada aqui mede o que VARIA por turno** — resposta, saída de ferramenta, arquivo
   reescrito. A parte da minha frase de ontem que dizia *"o variável custa integral em todo
   turno"* **continua verdadeira**; o que caiu foi a comparação com o estável.

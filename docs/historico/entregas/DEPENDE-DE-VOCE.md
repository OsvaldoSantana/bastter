> VENCIDO — executado em 13–24/09/2026, item a item no LEIA-ME desta pasta; o item 6, sem resposta registrada, migrou para a P-138 do PENDENCIAS.md. Não é instrução vigente.

# O que depende de você — e como resolver cada coisa

**Nove itens.** Seis são decisão (você responde, eu implemento). Três são execução
(você faz na máquina). Nenhum bloqueia os outros — pode responder fora de ordem.

**Tempo total se você quiser despachar tudo:** ~40 min de decisão + o download da CVM.

---

## PARTE 1 — decisões (você responde, eu faço)

### 1. Custo por operação entra no ranking de corretoras? · *2 min*

O ranking pontua a corretagem de **ação** e ignora três custos que já estão coletados:
mínimo de mesa (Inter, R$50), corretagem de FII, e % no exercício de opção.

**O que responder:** `sim` ou `não`.

- **`sim`** → viram constantes no `custos.yaml` com fonte, e o ranking ganha uma
  dimensão. Faz diferença para quem opera FII ou opção.
- **`não`** → os três campos saem do dataclass. O ranking fica honesto sobre o que mede.

> **Não há resposta certa.** Depende de você pretender operar FII e opção. Se não
> pretende, a dimensão vira peso morto.

---

### 2. Bonferroni ou FDR no backtest? · *5 min, e a pesquisa já respondeu quase tudo*

Você tinha dito FDR. **A pesquisa fechou contra**, e o motivo é aritmético:

```
m = 8 estratégias, t de Student, 301 gl
BH (FDR), 1ª descoberta   |t| ≥ 2,754     <- IDÊNTICO ao Bonferroni
Bonferroni                |t| ≥ 2,754
BY  (FDR sob dependência) |t| ≥ 3,075     <- MAIS severo, e promete menos
```

O BH só afrouxa a partir da **segunda** descoberta, e você espera zero ou uma.

**O que responder:** `Romano-Wolf` (minha recomendação), ou `Bonferroni`, ou `Holm`.

- **Romano-Wolf por bootstrap** — usa a correlação real das suas estratégias em vez do
  pior caso. Você já tem a série e já roda 10.000 reamostragens em outro teste. Ganho
  sobre o Bonferroni: ~0,05 de um `t`. Pequeno, mas de graça.
- **Bonferroni/Holm** — uma linha de código, à prova de interpretação.

---

### 3. O `m` do corte: executado, orçado, ou os dois? · *2 min*

Corrigir por multiplicidade exige dizer **quantos testes** entram na conta.

**O que responder:** `os dois` (minha recomendação), `executado`, ou `orçado`.

- **executado** (hoje = 2) → corte 2,253. Descreve a evidência.
- **orçado** (13, a soma dos `variantes_permitidas`) → corte 2,913. Descreve a disciplina.
- **os dois, lado a lado** → o leitor vê a diferença e julga.

> Com `m = 13`, o seu HML (t = 2,94) sobrevive por **0,027** de um `t`. A margem é real
> e é fina — e é isso que a escolha do `m` torna visível ou invisível.

---

### 4. Divergência entre resultado original e extensão: bloqueia? · *3 min*

Você decidiu que dado novo com a mesma especificação é **extensão**, e que ela nunca
sobrescreve o resultado anterior. Falta dizer o que o sistema faz quando os dois
discordam — se R1 rejeitava a hipótese nula e R2 não rejeita mais.

**O que responder:** `bloqueia` (minha recomendação) ou `só registra`.

- **bloqueia** → a estratégia não decide nada enquanto a divergência não estiver
  escrita. Um alfa que morre ao estender é o evento mais informativo que este projeto
  pode produzir; merece uma parada.
- **só registra** → vai para o log e a extensão mais recente vale.

---

### 5. A taxa do IMAB11 — pôr no `custos.yaml`? · *5 min, e exige o navegador*

A taxa de 0,25% está em **três documentos** do projeto e **não está** no `custos.yaml`,
que ainda diz `NAO_CONFIRMADO`. Quem roda o motor hoje recebe o IMAB11 bloqueado
enquanto os documentos dizem que a questão está resolvida.

**O que fazer:**

1. abrir a página do gestor do IMAB11 (Itaú Asset) e olhar a taxa total;
2. me mandar **o número, o endereço da página e a data**.

Eu escrevo no `custos.yaml` como `PARCIAL` (vira `COMPLETO` só com o regulamento).

> **Não faço sozinho** porque é entrada de valor com fonte, e eu não abri a página.
> Registrar 0,25% citando um documento interno seria citar a mim mesmo — que é
> exatamente o erro do C-01.

---

### 6. A régua de "variante" — confirma o desenho? · *5 min*

Está escrito em `auditoria/PRE-REGISTRO-MODELO-DE-DADOS.md`: especificação congelada,
graus de liberdade declarados, diário de execuções, e o contador como **alarme** (exige
justificativa escrita, não bloqueia).

**O que responder:** `confirmo` ou o que você mudaria.

---

## PARTE 2 — execução na máquina (segunda)

### 7. O pacote e os cinco remendos · *~30 min*

Está tudo no `LEIA-NA-SEGUNDA.md`, §0 a §4. Resumo: descompacte o zip por cima da
pasta, rode os cinco patches, rode a suíte. **60 testes a mais.**

---

### 8. O COTAHIST existe? · *1 comando*

```powershell
Get-ChildItem data -Recurse -Filter "COTAHIST*" | Select-Object FullName, Length
```

**Me mande a saída.** É o item que mais muda a ordem da semana: com ele, o C-01 (o
`factor` percentual × multiplicador, que difere por 50×) fecha no mesmo dia.

---

### 9. O download da CVM · *~1h de download, 5 min de comando*

Passo a passo completo em `auditoria/CVM-DOWNLOAD-MANUAL.md`. O essencial:

1. abrir `https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/` no navegador;
2. baixar **os 6 com prazo** primeiro: `dfp_cia_aberta_2021.zip` até `2026.zip`;
3. idem para o ITR;
4. salvar os `.zip` **inteiros, sem descompactar**, em `data\bronze\cvm\dfp\` e `\itr\`;
5. rodar o comando de hash do §4 do guia e **me mandar a saída**.

> **O hash importa mais que o download.** `dfp_cia_aberta_2022.zip` de hoje não é o da
> semana que vem, e os dois têm o mesmo nome. Sem hash você tem um arquivo, não uma
> observação datada.

E, se der, o cadastro (`CAD/DADOS/`, procurando `cad_cia_aberta.csv`) — é ele que fecha
o caso da Marfrig. **Marquei o caminho como `NAO_CONFIRMADO`**: veio do meu
conhecimento da estrutura, não de leitura, porque o portal me bloqueia. Se for outro,
me diga o que viu.

---

## Como me responder

Pode ser tudo numa mensagem só, no formato mais curto possível:

```
1 não · 2 Romano-Wolf · 3 os dois · 4 bloqueia · 6 confirmo
5 vou olhar amanhã
7,8,9 segunda
```

O que você não responder fica como está — **nada aqui bloqueia o desenvolvimento**, que
é a sua própria regra (U-01): dado de usuário não trava o projeto.

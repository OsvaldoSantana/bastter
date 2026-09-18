# B3 — séries históricas (COTAHIST): o caminho, o portão e o que ele decide

**Status:** `MEDIDO` · **Acesso:** 18/09/2026 · **Acervo:** `docs/acervo/b3/`

---

> ## ⚠ RETRATAÇÃO — 18/09/2026, poucas horas depois de este arquivo ser escrito
>
> **O que eu afirmei, aqui e no `politica.yaml`:** *"não existe automação deste
> download"*, e *"o CAPTCHA é a B3 dizendo que um humano tem de pedir o arquivo (…)
> um script que obtenha o arquivo sem esse pedido contorna o que a fonte declarou,
> qualquer que seja o endereço que ele use"*.
>
> **É falso.** Os 41 anos (1986–2026) foram baixados num laço de `Invoke-WebRequest`
> sobre
>
> ```
> https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A<ANO>.ZIP
> ```
>
> **GET simples: sem CAPTCHA, sem autenticação, sem cookie de sessão, sem token.**
> 40 dos 41 chegaram íntegros. O CAPTCHA existe no **formulário**; ele nunca esteve
> na frente do arquivo.
>
> **A causa raiz, e é a régua §5-B pela sétima vez, com um agravante novo.** O que eu
> medi foi *"existe um CAPTCHA no formulário de séries anuais"*. O que eu concluí foi
> *"não existe caminho até este arquivo sem CAPTCHA"* — uma afirmação sobre **todos**
> os caminhos, a partir de **um**. O agravante está escrito no §2 abaixo: eu decidi
> **não ler** o `SeriesHistoricas.js` porque saber o endereço *"é a única peça que
> faltaria para passar por cima do portão"* — e depois usei o fato de não ter olhado
> como razão para afirmar que não havia o que ver. **Princípio no lugar de medição** é
> a forma mais difícil de detectar deste defeito, porque a frase soa como rigor.
>
> **A regra não era o problema.** Não resolver CAPTCHA continua valendo, e ninguém
> resolveu CAPTCHA nenhum aqui. O que falhou foi não medir onde o arquivo mora antes
> de declarar que ele não tinha outra porta — e, por isso, **não entregar o script que
> era possível**. A P7 e a U-01 dizem que o sistema não pode depender do Osvaldo; eu o
> pus no caminho crítico com cinco CAPTCHAs manuais que não existiam. **É a quarta vez
> que cometo esse erro neste projeto.**
>
> **A regra de processo que sai daqui:** *afirmação de impossibilidade é achado, e
> achado precisa de medição.* "Não dá para fazer X" só se escreve depois de tentar X e
> falhar, com o erro transcrito. Sem isso, escreve-se **"não sei se dá"** — e mede-se.
>
> O texto original fica abaixo, sem edição no argumento, com as marcas ⛔ onde ele está
> errado. Achado retirado fica como retratação — nunca some.

---

Evidência de primeira mão do Osvaldo (o botão de download e o CAPTCHA que o precede),
mais a leitura das duas páginas públicas nesta data. Nada aqui vem de conhecimento
geral — o que não foi lido está marcado.

---

## 1. O caminho, medido

O endereço antigo que o projeto carregava — `bvmf.bmfbovespa.com.br/pt-br/cotacoes-historicas/`,
a pasta **sem arquivo** — devolve *"The resource you are looking for has been removed,
had its name changed, or is temporarily unavailable."*

**Eu li isso como "o host morreu". Estava errado, e o erro é o da régua §5-B:** a medição
foi *"o diretório sem arquivo responde 404"* e a conclusão foi sobre o **host**. O host
responde. É a sexta vez que a conclusão sai mais larga que a medição.

O caminho real tem duas pernas, e a primeira é a página atual da B3:

```
https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/
```

Lida em 18/09/2026, ela **não contém o formulário**: traz navegação, cabeçalho
institucional e **um link** que aponta para o host legado —

```
https://bvmf.bmfbovespa.com.br/pt-br/cotacoes-historicas/FormSeriesHistoricasArq.asp
```

> **O host legado não é um resquício: é para onde a própria B3 manda hoje.** Ele é o
> canal oficial, e é o único que este projeto conhece.

O formulário oferece **Séries Anuais de 2026 a 1986** (41 anos, conferidos um a um na
página). Único texto explicativo presente, transcrito: *"Em função do tamanho de alguns
arquivos, mesmo estando compactados, este processo poderá levar alguns minutos."*

## 2. O portão — e ele é a resposta à pergunta "dá para automatizar?"

Escolher um ano abre **uma nova janela com CAPTCHA**. Resolvido o CAPTCHA, a página
`FormConsultaValidaImagem.asp` responde *"Sequência de caracteres correta."* e mostra
dois botões. O de download é:

```html
<input name="btoDownload" id="btoDownload" type="button"
       onclick="javascript:AbrirArquivo('COTAHIST_A2024.ZIP')"
       value="Download" class="botaoFuncao05">
```

O formulário posta para si mesmo (`method="post"`,
`action=".../FormConsultaValidaImagem.asp"`).

**Daí sai um fato de procedência e uma decisão.**

O fato: o nome do arquivo é `COTAHIST_A<ANO>.ZIP`, escrito pela própria página.

⛔ *A frase abaixo é a afirmação retratada — leia a retratação no topo.*

A decisão: ~~**não existe automação deste download, e o motivo não é técnico.**~~ O CAPTCHA
é a B3 dizendo que um **humano** tem de pedir o arquivo. Um script que obtenha o arquivo
sem esse pedido contorna o que a fonte declarou — e contorna igual por qualquer
endereço, o que torna irrelevante *qual* endereço `AbrirArquivo()` monta.

> ⛔ **E este parágrafo é a causa raiz, não um detalhe.** Foi aqui que a recusa de
> medir virou evidência de que não havia o que medir.
>
> **Por isso este documento não registra o que `AbrirArquivo()` faz, e o
> `SeriesHistoricas.js` não foi lido.** Eu havia oferecido registrar o mecanismo "para
> constar"; retiro a oferta. A procedência já está completa sem ele — *um humano
> resolveu o CAPTCHA nesta página e clicou em Download em tal data* é a cadeia inteira.
> O que o JS acrescentaria não é procedência: é a única peça que faltaria para passar
> por cima do portão. Saber para não usar é uma distinção que não sobrevive ao arquivo
> ficar escrito.

**A regra que fica, e ela vale para toda fonte deste projeto:**

> **A porta que o publicador abriu para máquina é a que a máquina usa. Ausência de porta
> documentada não é convite para procurar fresta.**

Procurar um canal **documentado** (API, FTP, arquivo estático anunciado como tal) é
pesquisa legítima e continua aberta. Procurar um caminho que evite o CAPTCHA não é, e
não porque seja difícil: num sistema cuja doutrina inteira é procedência, obter o dado
por um caminho que a fonte não abriu **envenena o dado que ele traz**.

## 3. O que isso custa de verdade — e é menos do que parece

A P7 manda declarar como limitação toda rotina que depende de alguém lembrar, e está
declarada em `politica.yaml → limitacoes_declaradas.captura_do_cotahist_passa_por_captcha`.
Mas o peso dela **não é o da CVM**, e a diferença é de natureza:

| | CVM (DFP/ITR) | B3 (COTAHIST anual) |
|---|---|---|
| por que é manual | `ROBOTS_DISALLOWED` — a fonte pede que agentes não varram | **CAPTCHA** — a fonte exige um humano |
| o que muda sozinho | 2021–2026 **reescritos toda semana**, destrutivamente | ano corrente; ano fechado, `NAO_CONFIRMADO` |
| custo de uma semana sem captura | uma rodada de reapresentações que **deixou de existir** | nada, para ano fechado |
| custo total do histórico | recorrente, para sempre | **um número fixo de cliques, uma vez** |

⛔ **Consequência prática:** ~~baixar 2021, 2022, 2024 e 2025 à mão não é dívida
técnica — é o preço inteiro, pago uma vez.~~ **Não há preço manual nenhum a pagar.** O
que sobra da tabela acima e continua válido é só a coluna da direita: o ano fechado não
tem motivo para mudar, e por isso a P7 morde apenas no arquivo do **ano corrente**. O
que muda é a natureza da pendência — de *"portão intransponível"* para *"falta o
executor"*, que é exatamente a mesma pendência da CVM e tem a mesma solução.

## 4. A suposição que sobrou, e ela é medível por quase nada

*"Ano fechado não muda"* é **suposição minha**. Nenhuma das duas páginas publica
política de atualização — conferido em 18/09/2026, e o resultado é *não consta*.

~~**A medição custa um CAPTCHA:**~~ **a medição já foi feita, de graça, no download de
18/09.** O `COTAHIST_A2023.ZIP` rebaixado veio com **70.216.090 bytes — exatamente o
tamanho do que está no acervo desde 04/09.** Falta só confirmar por sha256, e a P-96
fecha com "ano fechado é congelado, medido".

```
COTAHIST_A2023.ZIP   ad1603788d78aaa1de806498572277f1d9443f88ae116452751b5800cb23523e
                     70.216.090 bytes · mtime 2026-09-04T11:37:13
```

- **Igual** → ano fechado é congelado, medido em vez de suposto, e a limitação encolhe
  para o ano corrente.
- **Diferente** → existe rotina periódica a fazer, ela é manual, e a limitação muda de
  peso. E aí vale o aprendizado do manifesto da CVM: **hash diferente não é
  reapresentação.** `manifesto_cvm.py --comparar` distingue `REORDENADO` de
  `REAPRESENTADO`; comparar por hash deu **100% de falso positivo** na CVM em 18/09.

## 5. O que esta leitura acrescenta à P-06 (layout), e não é boa notícia

A P-06 pede a URL do PDF de layout do COTAHIST, porque sem ela não dá para saber se
existe revisão 03 — e a revisão 02 (05/10/2020) transcrita em
`docs/fontes/SeriesHistoricas_Layout.md` **já é sabidamente incompleta** (P-95: oito
marcas de `ESPECI` de 2023 não constam da tabela dela).

**Medido em 18/09: nenhuma das duas páginas públicas linka documento de leiaute.**
Não é que eu não tenha achado a URL — a página onde ela deveria estar não a tem.

> Isso reclassifica a P-06. Ela não é *"achar o link que eu não procurei"*; é
> *"o publicador não publica o documento ao lado do arquivo"*. O gatilho continua sendo
> antes do parser, mas a conclusão provável é uma **limitação declarada**: o layout que
> o projeto usa é uma cópia sem fonte verificável, e a enumeração real tem de sair do
> **dado observado**, com falha ruidosa fora dela — que é exatamente o que a P-95 já
> mandava fazer por outro motivo.

## 5-B. Dois defeitos abertos no acervo que chegou — e o primeiro é de leitura

**(a) O arquivo muda de convenção dentro da própria série.** De 2002 em diante o ZIP
contém `COTAHIST_A2002.TXT`. De **1986 a 2001** ele contém um arquivo **sem extensão**,
e com dois padrões diferentes:

| faixa | nome dentro do ZIP |
|---|---|
| 1986–2000 | `COTAHIST.A1986` … `COTAHIST.A2000` — **ponto**, sem extensão |
| **2001** | `COTAHIST_A2001` — **sublinhado**, sem extensão |
| 2002–2025 | `COTAHIST_A2002.TXT` … — sublinhado **e** `.TXT` |

São 16 arquivos, 507 MB. O `fase0/calendario.py` varre ZIP **ou** TXT e o `ajustar.py`
lê o que estiver na pasta — **nenhum dos dois encontra estes 16**, e o modo de falha é o
pior do projeto: eles não quebram, eles simplesmente não veem o ano. Série que começa
em 2002 sem ninguém ter decidido isso. A enumeração tem de sair do **dado observado**,
com falha ruidosa fora dela (A-05).

**(b) O `COTAHIST_A2026.ZIP` não é um ZIP completo.** 38.328.935 bytes baixados, e a
extração falha com *"O registro Final de Diretório Central não foi localizado"* — o
fim do arquivo não chegou. Ou o servidor cortou, ou o arquivo do ano corrente é servido
de outro jeito enquanto o ano corre. **Isto é exatamente a armadilha registrada no
`CLAUDE.md` §11.6:** *"um download que devolve 404 mais um unzip vazio produzem 'nenhuma
mudança', indistinguível de 'a B3 não mudou nada'"*. Aqui o unzip **gritou**, e foi
sorte do formato, não desenho nosso. Rebaixar e conferir o sha256; se repetir, o ano
corrente entra com a lacuna declarada.

## 6. A ordem de download, e ela não é cronológica

Vem da P-92, e o critério é **evento de quantidade corroborado**, não proximidade:

| ordem | ano | eventos de quantidade que ele corrobora |
|---|---|---|
| 1º | **2025** | 31 |
| 2º | **2021** | 19 |
| 3º | 2024 | — (contiguidade) |
| 4º | 2022 | — (contiguidade) |
| — | 2023 | **1** — já no acervo |

Salvar em `data\bronze\b3\`, **os `.zip` inteiros, sem descompactar**. O zip é o byte que
a B3 entregou; ele é a evidência.

## 7. O `origem.csv` — o que fecha a procedência

O manifesto grava `sha256` e `dt_captura`; ele **não** grava de onde o arquivo veio.
Isso se declara ao lado dele, em `docs/acervo/b3/origem.csv`, colunas
`caminho;origem;acesso`:

```csv
caminho;origem;acesso
COTAHIST_A2021.ZIP;https://bvmf.bmfbovespa.com.br/pt-br/cotacoes-historicas/FormSeriesHistoricasArq.asp -- Series Anuais, download manual apos CAPTCHA;2026-09-18
```

uma linha por arquivo, trocando o ano e a data.

> **A linha do `COTAHIST_A2023.ZIP` fica em aberto de propósito.** Ele está no acervo
> desde 04/09 e **eu não sei de onde ele veio** — supor que veio desta página seria
> inventar procedência no arquivo cuja única função é não inventar procedência. Ou o
> Osvaldo confirma a origem, ou a linha registra `origem` desconhecida e o P-06 do
> manifesto continua contando 1.

---

## Fontes

- `https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/` — lida 18/09/2026
- `https://bvmf.bmfbovespa.com.br/pt-br/cotacoes-historicas/FormSeriesHistoricasArq.asp` — lida 18/09/2026
- `.../FormConsultaValidaImagem.asp` — página salva pelo Osvaldo e colada no chat em 18/09/2026 (o HTML do botão e a frase de validação são transcrição literal dela)

# Regime de incorporacao e construcao civil — especificado em 06/09/2026

**Origem:** resposta do Osvaldo as cinco perguntas de `regimes-de-leitura-de-balanco.md` §6.
**Procedencia:** `DECISAO_DO_USUARIO`, com expertise de dominio — engenheiro civil, analista
de planejamento, sete anos em obra e incorporacao. **Nao e derivado, nao e de artigo, e nao
deve ser apresentado como tal.**
**Status:** `REGIME_ESPECIFICADO` — mesma condicao em que o `bloco_C_solvencia` ficou em
05/09: escrito, defensavel, e **sem uma linha implementada**.

> **Leia a secao 4 antes de acreditar que isto vai rodar.** O regime esta certo; o dado
> para executa-lo, em grande parte, **nao existe no que a Fase 0 ia baixar**. Esse e o
> achado desta sessao, e ele e maior que o regime.

---

## 1. Divida — duas leituras simultaneas, nunca um numero

**Decisao dele:** somar e separar servem a perguntas diferentes, e as duas sao necessarias.

| leitura | formula | responde |
|---|---|---|
| **Alavancagem** | `divida liquida total / patrimonio liquido` | quanto a empresa deve |
| **Risco financeiro** | `divida corporativa de curto prazo / geracao de caixa operacional` | se ela aguenta |

Note **o denominador da alavancagem: patrimonio liquido, nao EBITDA.** E uma correcao
direta ao C-02 do bloco geral, e o motivo esta na secao 4 de
`regimes-de-leitura-de-balanco.md`: o EBITDA de incorporadora e reconhecimento por PoC,
nao caixa.

### A taxonomia da divida, dele

| tipo | caracteristica | risco |
|---|---|---|
| SFH / financiamento a producao | vinculado ao empreendimento | mais "casado" com recebiveis e estoques |
| CRI / debentures | corporativa ou estruturada | pressiona a companhia inteira |
| capital de giro | corporativa | **alto risco de liquidez** |
| fornecedores | financia a operacao | entra na analise de caixa |

**O exemplo que fixa a regra:** R$ 100 mi de SFH sendo amortizado conforme as unidades
vendem e os recebiveis vao para o banco **nao e** o mesmo risco que R$ 100 mi de divida
corporativa vencendo em 12 meses.

> **A frase que vira teste:** *"o erro perigoso e olhar apenas 'divida liquida = R$ 300
> milhoes' sem perguntar **quem deve, para quem, com qual garantia, quando vence, e qual
> ativo gera o pagamento**."*
>
> Sao cinco perguntas, e **nenhuma delas e respondida por um escalar**. Isso e a doutrina
> P3 dita por outra pessoa, em outro vocabulario: portao com motivo nomeado, nunca
> pontuacao agregada.

---

## 2. Receita a apropriar — visibilidade, nao saude

**Decisao dele:** e numero importante, **nao e caixa**, e nao mede saude financeira. Mede
**visibilidade futura**.

### A hierarquia, e ela e ordenavel

```
caixa  >  recebiveis de qualidade  >  receita contratada / a apropriar  >  expectativa de vendas
```

**Isto e implementavel como ordem de precedencia**, e e a parte mais diretamente
codificavel de toda a resposta dele: quando duas fontes discordarem sobre a saude de uma
empresa, a da esquerda ganha.

R$ 500 mi de receita a apropriar × 25% de margem ≈ R$ 125 mi de resultado futuro — **mas
so se** as vendas se mantiverem, os distratos nao subirem, os custos nao explodirem, as
obras terminarem, os recebimentos ocorrerem e a margem nao for comprimida. Seis condicoes,
e cada uma e um jeito de o numero nao acontecer.

**O teste dele, e ele nao e sobre tamanho:**

1. quanto dessa receita esta sustentada por contratos **que continuam performando**?
2. qual e a **margem** desses contratos?

> R$ 1 bilhao com margem deteriorada, distratos altos e recebiveis problematicos e **pior**
> que R$ 400 milhoes limpos. **Tamanho de backlog nao e sinal, e ate agora o projeto nao
> tinha nada dizendo isso.**

*"Receita a apropriar e otima para enxergar o futuro. E pessima para pagar a conta de hoje."*

---

## 3. Permuta — "nao saiu caixa" nao e "nao teve custo"

**Decisao dele:** permuta nao e ruim; pode ser excelente estrategia. O defeito e de leitura.

Terreno de R$ 20 mi pago em dinheiro **ou** 20% das unidades futuras. No segundo caso
melhoram: necessidade de capital, fluxo de caixa, retorno sobre capital e velocidade de
implantacao. A contrapartida: **parte do valor economico do empreendimento vai para o
permutante.**

> **A comparacao perigosa, nomeada por ele:** Empresa A compra terreno em dinheiro, Empresa
> B em permuta; concluir que B tem custo de terreno menor. **Nao necessariamente** — B pode
> estar pagando o terreno com participacao economica nas vendas futuras.

**Como detectar o mascaramento:** margem contabil × margem economica apos a participacao do
permutante × geracao de caixa do empreendimento.

**Onde procurar** (notas explicativas): terrenos em permuta, percentual, obrigacoes com
permutantes, estoque relacionado, valores a pagar, unidades entregues ao permutante.

> **Por que isto interessa alem do setor:** e a mesma familia do achado F-02. La, insumo
> ausente virava zero e zero ganhava de todos. Aqui, **desembolso ausente vira custo zero**,
> e custo zero ganha de todos. Duas manifestacoes do mesmo defeito, em camadas diferentes
> do sistema. **Ausencia de caixa nao e ausencia de custo** e, generalizando, **ausencia de
> registro nao e ausencia de fato.**

---

## 4. Distratos — e a inconsistencia que a resposta dele expos

**Decisao dele:** acompanhar `vendas brutas − distratos = vendas liquidas`, por trimestre, e
olhar **distrato como % das vendas brutas**, nunca o valor absoluto.

### Os cortes, e a classificacao deles importa

| faixa | leitura dele |
|---|---|
| > 10% persistente | investigar seriamente |
| > 15% | entender profundamente o motivo |
| > 20% persistente | sinal relevante de deterioracao — nao insolvencia |

**Classificacao doutrinaria, e ela e obrigatoria:** ele mesmo escreveu que *"nao existe
percentual universal porque depende de faixa de renda, localizacao, estagio, preco,
velocidade, politica comercial e mercado"*. Portanto estes tres numeros sao
**`DECISAO_DO_USUARIO`, nao `CRITERIO_MEDIDO`** — exatamente como o bloco C ja declara que
*"divida liquida/EBITDA abaixo de 3 e costume de mercado, nao norma"*. Vao para o YAML,
com o custo de discordar medido: **quantas empresas mudam de lado se o corte for 10 ou 15.**

### A tendencia, e aqui ha uma inconsistencia real com o que ja foi decidido

Ele e explicito: `5% → 7% → 11% → 16%` preocupa **muito mais** que `12% → 11% → 10% → 9%`,
mesmo com o segundo em nivel mais alto. **A tendencia domina o nivel.**

> **Mas em 05/09 o projeto decidiu o contrario para solvencia:** HIBRIDO — *"o nivel corta,
> a tendencia marca sem poder de veto"*. Se aqui a tendencia domina, entao **o hibrido nao
> e regra geral: e regra do bloco C.**
>
> Isso precisa ser decidido explicitamente, e nao por omissao. **Pendencia P-63.** Duas
> respostas possiveis e ambas defensaveis: (a) o hibrido e por metrica, e distrato e uma
> metrica cuja informacao mora na direcao; (b) o hibrido e geral, e o que muda e o que
> conta como "nivel" — nesse caso o nivel de distrato seria a media movel, nao o ponto.

### O que o distrato atinge ao mesmo tempo

> receita **+** recebiveis **+** estoque **+** caixa **+** margem

O cliente para de pagar → contrato distratado → recebivel desaparece → estoque volta →
dinheiro recebido precisa ser devolvido. **Cinco linhas do balanco pelo mesmo evento.**

Consequencia de desenho: distrato **nao e uma metrica**, e um evento com cinco efeitos. Um
sistema que o trate como indicador isolado perde as outras quatro pernas.

---

## 5. O primeiro numero — e a armadilha que ele mesmo resolve

**Decisao dele:** nao ROE, nao ROIC, nao margem liquida, nao divida/EBITDA.

> **Geracao de caixa operacional ajustada.** *"A operacao esta gerando caixa de forma
> sustentavel sem depender de aumento de divida?"*

Porque incorporadora pode ter lucro, margem bonita, patrimonio crescendo e backlog enorme
**e ainda estar sangrando caixa** — o setor exige capital antes de receber.

E a metrica de fechamento: **`geracao de caixa operacional / divida liquida`** — *"nao como
indice academico isolado, mas para responder: essa empresa consegue financiar a propria
operacao?"*

### O painel, em cinco camadas

| | camada | pergunta |
|---|---|---|
| ① | caixa | quanto entrou e saiu de verdade? |
| ② | operacao | vendas liquidas estao crescendo? |
| ③ | recebiveis | os clientes estao pagando? |
| ④ | estoque | esta girando ou encalhando? |
| ⑤ | divida | financia crescimento ou financia prejuizo? |

### A sequencia de dez, e a ordem e deliberada

`VSO/vendas liquidas → distratos → recebimento de clientes → FCO → estoque e unidades
prontas → receita a apropriar → margem bruta → divida SFH → divida corporativa → caixa e
vencimentos`

*"Eu quero descobrir primeiro se a maquina operacional esta funcionando. So depois quero
saber quanto ela deve."*

### A regra pratica

> Incorporadora saudavel **nao e** a que tem pouca divida. E a que consegue **vender →
> receber → construir → gerar margem → transformar margem em caixa → pagar a divida →
> repetir**. Se o ciclo funciona, divida alta e administravel. Se o ciclo quebra, divida
> pequena e perigosa.

**Isto responde a pergunta original inteira**, e responde melhor do que qualquer regra de
corte: o criterio nao e o nivel de divida, e a **integridade do ciclo**.

---

## 5-A. A armadilha dentro da resposta dele — e o proprio painel a desarma

**O FCO de incorporadora e negativo por desenho durante a expansao.**

O gasto com obra e classificado como **operacional** (o imovel em construcao e *estoque*, no
ativo circulante — nao imobilizado). Ou seja: uma incorporadora lancando muitos
empreendimentos consome caixa operacional exatamente porque esta crescendo.

**Aplicar sozinha a pergunta *"esta gerando caixa sem aumentar divida?"* reprovaria uma
incorporadora saudavel em expansao** — e isso e **o mesmo defeito do C-01 punir capex**,
transposto de setor. O projeto acabou de nomear esse defeito e ele reaparece dentro da
propria correcao.

**Mas o painel dele ja resolve, e e por isso que ele e um painel e nao um indice.** FCO
negativo com ② vendas liquidas crescendo, ③ clientes pagando e ④ estoque girando e
**expansao**. FCO negativo com vendas caindo, inadimplencia subindo e estoque encalhando e
**sangramento**. As duas leituras usam o mesmo numero e chegam a lugares opostos.

> **A licao de desenho, e ela vale para o sistema inteiro:** nenhuma metrica isolada
> distingue crescimento de queima. **O discriminador nunca esta na metrica — esta na
> companhia dela.** Um sistema de portoes com motivo nomeado (P3) pode expressar isso; um
> score agregado nao pode, por construcao.

---

## 6. E agora o problema: quase nada disto esta no dado que a Fase 0 ia baixar

Este e o achado da sessao, e ele e desconfortavel.

| # | insumo da sequencia dele | esta nas 8 demonstracoes estruturadas da CVM? |
|---|---|---|
| 1 | VSO, vendas brutas e liquidas | **nao** |
| 2 | distratos | **nao** |
| 3 | recebimento de clientes | parcial — DFC agrega, nao abre por cliente |
| 4 | geracao de caixa operacional | **sim** — DFC_MI / DFC_MD |
| 5 | estoque e unidades prontas | so o **valor** (BPA). Unidades e encalhe, **nao** |
| 6 | receita a apropriar | **nao** — vive em nota explicativa |
| 7 | margem bruta | **sim** — DRE |
| 8 | divida SFH | **nao separada** — BPP traz o total |
| 9 | divida corporativa | **nao separada** |
| 10 | caixa e vencimentos | caixa **sim** (BPA); cronograma de vencimento **nao** |

**Placar: 3 de 10 obtiveis. Um quarto parcial.** E os tres obtiveis sao justamente os que
ele **nao** colocaria em primeiro lugar.

O mesmo vale para permuta (nota explicativa) e para o teste de qualidade do backlog
(release de resultados).

### Por que isto e maior que o regime de incorporacao

A Fase 0 inteira foi desenhada em cima dos CSVs estruturados de DFP e ITR. **A resposta
dele e a prova de que, pelo menos para um setor, o dado estruturado nao alcanca a decisao.**
Nao ha razao para supor que construcao seja excecao — banco ja era, e agora sao dois.

**Onde a informacao esta, e o caminho existe:**
- **notas explicativas** — a pagina do conjunto DFP diz que ele publica *"os enderecos para
  download dos Formularios DFP entregues"*, o documento completo do Empresas.NET;
- **release de resultados e apresentacao institucional** — protocolados como **IPE**
  (comunicados e fatos relevantes), que e um conjunto do proprio portal da CVM.

**Custo:** e caminho de **extracao de documento**, nao de leitura de CSV. Ordem de grandeza
diferente do que o projeto orcou.

### A saida que a doutrina obriga, e ela ja esta decidida

**P6:** construcao **nao sai do universo** por falta de dado.
**`empresa_sem_dado` (05/09):** ADMITIR COM MARCACAO — nao exclui, sinaliza.

Entao: empresa de regime `INCORPORACAO` entra no universo **marcada**, com o motivo escrito
— *"regime especificado, insumos 1, 2, 5, 6, 8, 9 e 10 indisponiveis no dado estruturado"* —
e a marca precisa ser **contavel** no relatorio final, como ja foi exigido para o bloco C.

### A camada de desenho que falta: portao nao e dossie

Ele respondeu como analista lendo **uma** empresa. O sistema precisa varrer **centenas**.
Uma sequencia manual de dez passos nao e portao.

**Separacao proposta, e ela e nova no projeto:**

| | o que e | quando roda | fonte |
|---|---|---|---|
| **portao** | automatico, sobre todo o universo | sempre | dado estruturado |
| **dossie** | leitura manual guiada, empresa a empresa | so na lista curta | notas, release, IPE |

Para incorporacao, **o portao nao pode ser o regime** — o dado nao existe. O portao pode
apenas dizer: *"esta empresa e do regime INCORPORACAO, portanto exige dossie, e ate ter um
ela permanece no universo sem peso atribuido por este bloco."*

Isso e coerente com a P6 (nada sai), com a P1 (nada e inventado) e com a A05 (o sistema nao
nomeia empresa). E torna o painel dele **o roteiro do dossie**, que e exatamente o que ele e.

---

## 7. O que fica pendente

| # | o que |
|---|---|
| **P-63** | o hibrido nivel/tendencia e regra geral ou do bloco C? A resposta dele sobre distratos inverte o peso |
| **P-64** | portao × dossie — camada de desenho nova, e ela vale para todo regime, nao so incorporacao |
| **P-65** | extracao de nota explicativa e de IPE: viabilidade e custo. **Bloqueia 7 dos 10 passos** |
| **P-66** | os cortes 10/15/20% de distrato entram no YAML como `DECISAO_DO_USUARIO`, com custo de discordar medido |
| **P-18** | contar `SETOR_ATIV` — **continua bloqueando tudo**: sem ela nao ha como saber que uma empresa e do regime |

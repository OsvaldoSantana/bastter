# Regimes de leitura de balanco — a pergunta do Osvaldo em 06/09/2026

> *"voce ja desenhou como vai lidar com balanco e interpretacao de informacoes? uma
> empresa que lucrou menos no ano porque reinvestiu mais; uma empresa que fez divida mas
> para formar capex na compra de novos ativos para produzir mais; setores que funcionam
> com divida alta como o da construcao civil, porque realizamos imoveis com
> financiamento."*

**Resposta honesta: nao. O mecanismo existe e foi aplicado uma vez. A pergunta mostra
que ele foi aplicado de menos.**

Status deste documento: **especificacao aberta**. Nada aqui esta implementado.

---

## 1. Primeiro, uma correcao na pergunta — e ela muda a resposta

*"Empresa que lucrou menos porque reinvestiu mais"* junta tres coisas que a contabilidade
separa de proposito, e a regua certa depende de qual das tres e.

**Capex nao passa pela DRE.** Comprar maquina, terreno ou galpao **nao reduz o lucro do
ano** — reduz o caixa e vira ativo no balanco. Entao "reinvestiu mais" nao explica, por
si, lucro menor.

O que de fato derruba o lucro sao tres causas distintas:

| causa | onde aparece | o que ela significa |
|---|---|---|
| **depreciacao** do capex **passado** | DRE, despesa nao-caixa | fase de investimento amadurecendo. Nao consome caixa **agora** |
| **juros** da divida que financiou o capex | DRE, resultado financeiro | alavancagem. Consome caixa, e o cronograma importa |
| **opex nao capitalizado** — P&D, marketing, contratacao, abertura de loja | DRE, despesa operacional | investimento **de verdade**, mas contabilmente indistinguivel de desperdicio |

**Por que isso importa para o desenho:** as tres tem leitura oposta.

- Depreciacao alta **com FCO forte** = empresa investiu e o ativo esta produzindo. Saudavel.
- Opex alto **sem crescimento de receita** = queima. Perigoso.
- Juros altos = questao de solvencia, e ai a pergunta nao e o nivel, e o **cronograma**.

Um sistema que olhe "lucro caiu" trata as tres como iguais. Um sistema que olhe **FCO,
depreciacao, capex e resultado financeiro separadamente** ja distingue as tres sem
nenhuma sofisticacao — e essa e a primeira decisao de desenho: **a DRE nao e a porta de
entrada. A DFC e.**

> **A terceira e a mais dificil, e vale admitir agora:** separar "opex que e investimento"
> de "opex que e desperdicio" **nao se faz com dado estruturado**. A CVM nao publica esse
> corte. Isso e limitacao declarada, nao problema a resolver com mais engenharia.

---

## 2. O defeito real que a pergunta expos, e ele e do projeto

O `bloco_C_solvencia` do `politica.yaml` ja escreve, com todas as letras:

> *"Se a empresa for instituicao financeira ou seguradora, o bloco C NAO produz numero —
> levanta recusa. Divida liquida/EBITDA aplicado a um banco **devolve um numero**, e esse
> e o perigo: metrica que nao se aplica mas nao falha e o modo de falha do F-02."*

**O projeto reconheceu esse modo de falha para banco e nao o generalizou.** Existe hoje
um regime para instituicao financeira e **um unico regime para "todo o resto"** — que
trata uma incorporadora e uma WEG como se lessem o mesmo balanco.

Tres consequencias concretas, todas no portao de **exclusao**, que e o pior lugar
possivel para um erro:

### 2.1 C-01 (cobertura de juros) exclui empresa em fase de investimento

`EBIT / despesa financeira`. Uma empresa que acabou de fazer capex tem **EBIT deprimido**
pela depreciacao nova **e** despesa financeira elevada pela divida que a financiou. As
duas pontas pioram ao mesmo tempo, pelo mesmo motivo, e o motivo pode ser saudavel.

Isto e exatamente o caso 2 da pergunta, e ele cai no portao que **remove do universo** —
nao no que atribui peso.

### 2.2 C-02 (divida liquida/EBITDA) nao significa nada para incorporadora

Duas razoes independentes, e cada uma sozinha ja invalida:

- **A divida nao e uma so.** O **financiamento a producao (SFH)** e lastreado no proprio
  empreendimento e quitado no **repasse**, quando o comprador fecha o financiamento dele.
  Somar isso a divida corporativa e somar coisas com risco e com fonte de pagamento
  diferentes.
- **O EBITDA e uma convencao de reconhecimento.** Receita de incorporacao e reconhecida
  por **PoC** (percentual de execucao), nao por caixa. O "EBITDA" do ano diz respeito a
  obra executada, nao a dinheiro recebido.

O numero sai. O numero mente. **Mesmo modo de falha do banco, setor diferente.**

### 2.3 Divida boa e divida ruim tem o mesmo sinal em C-02

Divida que financia ativo cujo retorno supera o custo dela **cria valor**. Divida que
financia prejuizo **destroi**. Uma metrica de nivel nao distingue as duas.

O criterio que distingue existe e e classico: **ROIC contra o custo da divida.** Nao e
opiniao — e a definicao de quando alavancar e racional. E ele e calculavel com o que a
CVM publica.

---

## 3. O que a doutrina do projeto ja obriga aqui

**P6 — ausencia de criterio nao e criterio de exclusao.** A saida facil e tirar
construcao civil do universo "porque a regua nao serve". **A P6 proibe.** E a P6 nasceu
justamente de um caso identico: eu quis excluir banco por falta de regua, e a correcao
foi *"nao deve ser excluido, deve ser encontrado o criterio"*. **Construcao e a segunda
instancia da mesma coisa.** Se eu excluir agora, e a quarta vez.

**P3 — portoes, nao pontuacao.** A resposta nao e um ajuste no corte. E um **portao
anterior** que decide **qual regime se aplica**, e cada regime declara quais metricas
valem e quais nao produzem numero.

**P1 — procedencia por valor.** Todo corte de todo regime e escolha declarada, com o
custo de discordar medido: quantas empresas entram ou saem se o corte mudar.

---

## 4. A forma da solucao

Um **portao de regime**, antes do bloco C, com tres saidas em vez de duas:

```
                    +-- INSTITUICAO FINANCEIRA -> regime_instituicao_financeira  [existe]
  portao de regime -+-- ESTRUTURA DE CAPITAL ATIPICA -> regime proprio           [nao existe]
                    +-- GERAL -> bloco_C_solvencia                               [existe]
```

O que hoje se chama "geral" e, na verdade, **"empresa industrial ou de servicos com
capex proprio e receita reconhecida na entrega"** — e isso e um regime, nao um padrao.
Chama-lo de padrao e a suposicao que a pergunta derrubou.

### Candidatos a regime proprio, e o motivo em uma linha

| setor | por que a regua geral quebra |
|---|---|
| **incorporacao e construcao** | PoC; divida SFH lastreada e quitada por repasse; estoque no ativo circulante, nao imobilizado; caixa e receita descolados por anos |
| utilities e concessoes | ativo regulatorio, contrato de concessao, divida longa por desenho |
| shopping e propriedades para renda | ativo a valor justo; resultado inclui reavaliacao que nao e caixa |
| aereas, navegacao, locadoras | arrendamento (IFRS 16) que virou divida no balanco em 2019 e mudou a serie |
| seguradoras | ja recusadas junto com bancos |

**Nenhum destes sai do universo.** Cada um vira regime ou vira marcacao, e a marcacao
tem que viajar ate o relatorio final e ser contavel — como ja foi decidido em
`empresa_sem_dado`.

### O que um regime precisa declarar

1. **Como se identifica** — hoje o candidato e `SETOR_ATIV` do cadastro da CVM, e ele
   esta `PARCIAL`: os valores distintos nunca foram contados no dado real (P-18). **Nenhum
   regime pode ser codificado antes disso.**
2. **Quais metricas nao produzem numero** — e recusam, em vez de devolver valor.
3. **Quais metricas substituem** — com corte, fonte e custo de discordar.
4. **O que fica cego** — em `limitacoes_declaradas`.

---

## 5. Metricas que respondem as tres perguntas, e o que cada uma custa

| pergunta | metrica | por que ela | insumo | custo |
|---|---|---|---|---|
| a divida financia producao ou prejuizo? | **ROIC vs custo da divida** | e a definicao de alavancagem racional | DRE + BP; custo da divida = despesa financeira / divida bruta media | medio. WACC completo exige premissa **declarada**, nao derivada |
| o lucro caiu por investir ou por queimar? | **FCO** e **FCO − capex**, lado a lado | FCO ignora depreciacao; a diferenca isola o investimento | DFC (DFC-MD ou DFC-MI) | **baixo — o dado ja esta nos ZIPs da CVM** |
| a empresa aguenta a divida? | **cronograma de vencimento vs geracao de caixa** | solvencia e *timing*, nao nivel. Ja e o C-03 | notas explicativas | **alto — nota explicativa nao vem estruturada** |
| o capex e manutencao ou expansao? | — | decide se FCF baixo e sintoma ou escolha | **nao existe no dado** | **impossivel hoje** |

> **A ultima linha e a mais importante deste documento.** A CVM **nao separa** capex de
> manutencao de capex de expansao. A heuristica de mercado — "manutencao ≈ depreciacao" —
> e conhecida **e conhecidamente errada** em empresa que cresce. Isto e **limitacao
> declarada**, com direcao de vies: **o sistema subestima a qualidade de quem investe
> para crescer.** Exatamente o caso 1 da pergunta.
>
> Declarar isso vale mais que uma aproximacao. Aproximar aqui seria inventar o numero que
> falta — o F-02 pela enesima vez.

---

## 6. O que este documento NAO resolve, e quem resolve melhor

O regime de **construcao civil** precisa de quem conhece o setor por dentro, e nao sou
eu. O Osvaldo e engenheiro civil e analista de planejamento — ele convive com o assunto
todo dia, e as perguntas abaixo ele responde melhor do que qualquer fonte que eu leia:

1. **Divida SFH e divida corporativa devem ser somadas em alguma metrica, ou nunca?**
2. **A `receita a apropriar` (backlog) entra na leitura, ou e promessa e nao numero?**
3. **Permuta** (terreno pago em unidades) distorce o que, exatamente?
4. **Distratos** — como um sistema deveria ler uma receita que pode voltar atras?
5. **Qual numero um planejador olha primeiro** para saber se uma incorporadora esta
   saudavel? Se existe um, ele vale mais que tres indices academicos.

**Isto nao e delegacao de trabalho.** E que a P1 exige procedencia, e "o Osvaldo, que
trabalha com isso" e uma procedencia melhor que "um artigo que eu li", **desde que
registrada como decisao dele** e nao apresentada como derivada.

---

## 7. Pendencias que este documento abre

- **P-58** — o portao de regime tem duas saidas e precisa de N. Bloqueia: bloco C
  aplicado a incorporadora, utility, shopping e locadora.
- **P-59** — C-01 pune fase de investimento. Precisa de uma segunda leitura (FCO/juros
  ao lado de EBIT/juros) antes de excluir.
- **P-60** — ROIC vs custo da divida nao existe em lugar nenhum do sistema, e e o unico
  criterio que separa divida boa de divida ruim.
- **P-61** — capex de manutencao vs expansao: **limitacao declarada**, com direcao de
  vies escrita.
- **P-18** (ja aberta) — contar `SETOR_ATIV` no dado real. **Bloqueia todas as acima**:
  sem ela, nao ha como identificar o regime.

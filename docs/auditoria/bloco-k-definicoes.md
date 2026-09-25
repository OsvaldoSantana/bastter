# Bloco K — definições para IPCA+ e cripto

**Emissão:** 03/09/2026.
**Objetivo:** trazer Tesouro IPCA+ e HASH11 de volta ao universo **criando a regra que falta**, não afrouxando a que existe.
**Natureza:** especificação. As frases de tese abaixo são **formas**, com o conteúdo em branco ou marcado como exemplo. K-02, K-03 e K-04 são seus por construção — se eu os escrever, o registro deixa de ser pré-registro e vira sugestão minha com a sua assinatura.

---

## 1. Os dois casos são problemas diferentes

Isto vem primeiro porque tratá-los juntos leva à solução errada.

| | Tesouro IPCA+ | HASH11 |
|---|---|---|
| Quem excluiu | **DATADO**, por exigir objetivo datado e casamento de duração | **G7**, por falta de tese registrada |
| Bloco K resolve? | **Não** | **Sim** |
| O que falta | Uma **função** que descreva o que o IPCA+ faz | Uma **tese** falsificável com data |
| Natureza da falha modelada | Vender antes do vencimento e materializar a marcação | Manter indefinidamente uma posição que era para ser temporária |

O IPCA+ não foi excluído por falta de tese. Ele foi excluído porque **nenhuma função do modelo descreve o que ele faz**. LASTRO exige `perda_maxima: nominal_zero` e o IPCA+ tem marcação a mercado; DATADO exige um prazo a casar e não havia prazo. Ele caiu no vão entre as duas.

**O princípio que reconcilia a sua objeção com a disciplina do sistema:** o sistema não existe para excluir ativos. Existe para exigir que o papel de cada ativo seja **nomeado**. Ativo sem papel nomeado não pode ser dimensionado — não há como saber quanto dele é demais. Criar a regra que falta é o comportamento correto; afrouxar a regra existente não é.

---

## 2. Caso 1 — a função que falta

### 2.1 Diagnóstico: o que o IPCA+ Principal faz

Travar um juro **real** na data da compra, entregue integralmente **se e somente se** carregado até o vencimento. Não é liquidez (a venda antecipada realiza marcação). Não é lastro (não tem perda nominal zero no caminho). Não é datado (não precisa de um objetivo — precisa de um **compromisso de carrego**). E não é crescimento (o retorno é contratado, não incerto).

O modo de falha específico dele não é "esperança sem prazo", que é o do bloco K. É **quebra de compromisso**: comprar com intenção de carregar, ver a marcação abrir, e vender no pior momento. O IPCA+ 2060 caindo ~47% com +2 p.p. de juro real, que o seu próprio catálogo anota, é exatamente a tentação.

Portanto: função nova, e um registro análogo à tese, mas com campos próprios.

### 2.2 Função `PROTECAO_REAL`

```yaml
  PROTECAO_REAL:
    nome: "Protecao do poder de compra, com carrego"
    descricao: >
      Juro real travado na compra, entregue integralmente apenas se carregado ate o
      vencimento. Nao e LASTRO (ha marcacao a mercado no caminho), nao e DATADO (nao
      exige objetivo, exige COMPROMISSO), nao e CRESCIMENTO (o retorno e contratado).
      Criada em 03/09/2026 porque o modelo nao tinha nome para isto e o empurrava para
      DATADO — o que excluia o instrumento quando nao havia objetivo a casar.
    regra: "duracao_do_instrumento <= horizonte_declarado"
    exige_compromisso_de_carrego: true     # registro tipo CARREGO em teses.yaml
    exige_liquidez_dias: null              # NAO e fonte de liquidez. Nunca.
    exige_perda_maxima: "limitada"         # marcacao a mercado se vendido antes
    conta_como_liquidez: false             # invariante: nao entra no calculo da reserva
    prioridade: 3.5                        # entre DATADO e LASTRO
    nota: >
      O modo de falha desta funcao nao e "esperanca sem prazo" — e quebra de
      compromisso: comprar para carregar, ver a marcacao abrir e vender no pior
      momento. Por isso o registro exige a condicao de venda ANTECIPADA declarada
      antes da compra, e o custo estimado dela.
```

E no catálogo, `td_ipca` passa a `funcoes=["PROTECAO_REAL", "DATADO"]` — serve as duas, e o G6 decide qual sobrevive em cada estado.

### 2.3 Registro tipo `CARREGO`

Campos análogos aos K, com semântica própria:

| Campo | O que é | Por que existe |
|---|---|---|
| `C01_horizonte_de_carrego` | Data do vencimento do papel | O compromisso é até uma data concreta, não "longo prazo" |
| `C02_compromisso` | Frase declarando o carrego e o juro real travado | O que você está afirmando ao comprar |
| `C03_condicao_de_venda_antecipada` | O **único** evento que autoriza vender antes | Sem isto, qualquer queda vira motivo |
| `C04_custo_de_quebrar` | Estimativa de perda se vender no pior cenário previsto | Escrever o número antes muda o comportamento depois |
| `C05_teto_da_funcao` | % máximo do patrimônio nesta função | Marcação a mercado exige limite |
| `C06_reconhecimento` | Booleano: "entendo que a marcação pode abrir e que isso não é perda se eu carregar" | Assinatura, não decoração |

**Modelo para preencher** (`teses.yaml`, seção nova `carregos:`):

```yaml
carregos:
  td_ipca:
    ativo_id: td_ipca
    funcao: PROTECAO_REAL
    catalogo: BUY_AND_HOLD
    dt_registro: 2026-09-03
    C01_horizonte_de_carrego: ____-__-__      # vencimento do papel que voce escolher
    C02_compromisso: >
      ____ (forma: "carrego o NTN-B Principal <vencimento> ate o vencimento, travando
      juro real de <X>% a.a. na data da compra; a marcacao intermediaria nao altera o
      valor de resgate na data final")
    C03_condicao_de_venda_antecipada: >
      ____ (forma: um EVENTO, nao um preco. Ex.: "necessidade de caixa que a reserva
      de emergencia nao cobre" ou "juro real de mercado acima de <Y>% permitindo
      recompra de prazo equivalente com ganho liquido de imposto")
    C04_custo_de_quebrar:
      cenario: "+2 p.p. de juro real"
      perda_estimada_pct: ____               # o proprio catalogo estima ~47% no 2060
      fonte_da_estimativa: ____
    C05_teto_da_funcao: 0.__                 # fracao do patrimonio
    C06_reconhecimento: true
    impressao: PENDENTE
```

### 2.4 A tensão honesta, que você precisa decidir

A regra proposta é `duracao <= horizonte_declarado`. O seu horizonte declarado é 25 anos e a duração do IPCA+ longo é ~18. Passa.

**Mas horizonte declarado é um plano, não uma obrigação.** Um objetivo datado ("entrada do apartamento em 2034") é uma obrigação: o dinheiro tem destino. Um horizonte de 25 anos é uma intenção que você pode revisar. Usar o horizonte como se fosse prazo é mais frouxo que usar um objetivo — e é exatamente o tipo de afrouxamento que a auditoria do A-04 apontou.

**Três posturas possíveis, e a escolha é sua:**

1. **Aceitar o horizonte como prazo**, com `C05_teto_da_funcao` baixo (a marcação exige limite) e `C03` obrigatório. É a mais permissiva, e é defensável se o teto for real.
2. **Exigir que a duração caiba com folga** — `duracao <= horizonte * 0.6`, por exemplo. Reconhece que o horizonte é revisável e compra margem.
3. **Manter a exigência de objetivo**, e resolver o caso registrando um objetivo real, se existir. Se não existe nenhum objetivo datado hoje, esta postura mantém o IPCA+ fora — e a exclusão passa a ser uma consequência da sua situação, não do modelo.

Registre a escolha em `decisoes` no `politica.yaml`, com a justificativa. Não há resposta técnica: é preferência declarada, e o backtest um dia a testa.

---

## 3. Caso 2 — a tese do HASH11

Aqui o bloco K se aplica de fato. Vou dar a estrutura e as formas; o conteúdo é seu.

### 3.1 O erro mais comum, e ele é sobre o K-04

**Numa posição em que você já aceitou perder 100%, a condição de falsificação não pode ser "o preço caiu".** A queda está dentro da perda aceita em K-01. Se K-04 for um nível de preço, você criou uma posição que se encerra exatamente quando a tese exigiria paciência — e a perda máxima aceita de 100% vira ficção.

K-04 tem de ser um evento que **invalida a tese**, não um que **machuca a posição**. Para um satélite, os candidatos honestos costumam ser de três tipos:

- **Estrutura do veículo:** a taxa subir acima de X; o fundo mudar de política; surgir veículo equivalente materialmente mais barato (o que encerra *esta* posição e abre outra).
- **Regime:** mudança tributária ou regulatória que altere a economia da posição.
- **Disciplina:** a exposição passar de X% do patrimônio por N revisões seguidas sem novo aporte — ou seja, o sucesso do ativo transformando a aposta em concentração.

O terceiro é o menos óbvio e o mais útil: ele encerra a posição **quando ela dá certo demais**, que é o cenário em que ninguém tem regra pronta.

### 3.2 K-02 — a forma

O validador exige seis palavras no mínimo e recusa expressões vagas. Mas o teste real é outro, e é seu: **em 31/12 do ano do prazo, você consegue responder "aconteceu" ou "não aconteceu" sem discutir?** Se precisa de interpretação, não é falsificável.

Três formas que passam nesse teste, com o conteúdo em branco:

```
FORMA A — sobre o veículo
  "ate <data>, existe na B3 um ETF de cripto com taxa de administracao
   abaixo de <X>% a.a., e a posicao migra para ele"

FORMA B — sobre a adocao, com metrica publica
  "ate <data>, <metrica publica e verificavel> atinge <valor>"
   — a metrica precisa ter fonte declarada e serie publica

FORMA C — sobre o papel na carteira
  "a exposicao de <X>% em cripto se justifica ate <data> como aposta assimetrica;
   ate la a decisao e revisada anualmente contra o custo de <Y>% a.a. do veiculo"
```

A forma C é a mais honesta para quem não tem tese de conteúdo — ela declara que a posição é **um experimento com prazo**, e isso é uma tese válida. As formas A e B exigem que você tenha uma convicção específica; se não tem, C é mais verdadeira que inventar uma.

**O que o validador recusa:** "longo prazo", "vai subir", "acredito", "tende a", "potencial", "promissor". E ver §4 — ele hoje recusa por engano frases legítimas.

### 3.3 K-03 — o prazo

Uma data. Duas regras práticas:

- **Curto demais** (2 anos) transforma a aposta em trade e o custo de 1,30% a.a. do veículo em fração enorme do resultado.
- **Longo demais** (2050) esvazia o pré-registro: um prazo que você não vai viver para verificar não é compromisso.

Faixa razoável para um satélite com revisão anual: **5 a 10 anos**. Escolha e escreva.

### 3.4 K-01, K-05, K-06, K-07

`K01_perda_maxima_aceita: 1.0` — sempre, no catálogo especulativo. O validador rejeita outro valor, e está certo: declarar menos é supor um piso que não existe.

`K05_liquidez_saida_dias` — derivado de A-01 e A-02 do catálogo. O `2` do modelo é plausível para HASH11; confirme com o volume real.

`K06_insiders: NAO_APLICAVEL` — correto, é ETF. Mantenha explícito.

`K07_quanto_o_preco_ja_contem` — `NAO_OBTIDO` com o motivo. Está certo e deve continuar assim: fingir uma estimativa aqui seria pior que a lacuna.

### 3.5 Bloco L

O modelo já está bem preenchido no `teses.yaml`, com `reprova` listando A-06, C-01 a C-05 e B-01 a B-07, e `nao_aplicavel` separado. **Não mexa** — é exatamente o formato que o escopo especifica, e a nota final ("isso NÃO impede a compra — impede que ela seja reclassificada como investimento depois") é a frase certa.

Só falta trocar `rodado_em` para a data em que você de fato rodar.

### 3.6 O registro, pronto para preencher

```yaml
  hash11:
    # exemplo: true   <- APAGUE esta linha quando o conteudo for seu
    ativo_id: hash11
    funcao: APOSTA
    catalogo: ESPECULATIVO
    dt_classificacao: 2026-__-__
    K01_perda_maxima_aceita: 1.0
    K02_tese: >
      ____ (forma A, B ou C da §3.2 — com numero e data)
    K03_prazo: 20__-__-__
    K04_falsificacao: >
      ____ (evento que INVALIDA a tese, nao que machuca a posicao — §3.1)
    K05_liquidez_saida_dias: 2
    K06_insiders: NAO_APLICAVEL
    K07_quanto_o_preco_ja_contem:
      estimativa: NAO_OBTIDO
      premissas: ["exige modelo de precificacao que o projeto nao tem"]
    L_teste_de_classificacao:
      rodado_em: 2026-__-__
      reprova: [...]        # mantenha o do modelo
      nao_aplicavel: [...]  # mantenha o do modelo
      nota: >               # mantenha
    impressao: PENDENTE     # rode `python tese.py` e cole o hash que ele calcular
```

---

## 4. Correções no validador, antes de escrever

Duas travam o processo. A primeira eu demonstrei por execução.

**4.1 · Falso positivo por substring.** `tese.py` testa `if v in baixo`. Resultado real:

```
['tende a']    <- "a empresa atende a 3 milhoes de clientes ate 31/12/2030"
['potencial']  <- "a capacidade potencial instalada atinge 500 MW ate 2029"
```

Uma tese com métrica e data é recusada porque **"atende a" contém "tende a"**. Correção:

```python
import re
achados = [v for v in VAGO if re.search(rf"\b{re.escape(v)}\b", baixo)]
```

`\b` antes de `tende` não casa em "atende", porque `n` e `t` são ambos caracteres de palavra. Resolve o primeiro caso.

Para "potencial" nenhuma regex resolve — o termo é legítimo como substantivo técnico. **Rebaixe de rejeição a aviso:**

```python
DURO  = ("longo prazo", "vai subir", "vai valorizar", "acredito", "tende a",
         "eventualmente", "no futuro", "pode chegar", "deve subir")
BRANDO = ("potencial", "promissor", "o futuro")
```

E acrescente o teste estrutural, que é o que realmente separa tese de esperança:

```python
if not re.search(r"\d", k2):
    p.append("K02 sem nenhum numero verificavel: uma tese falsificavel afirma "
             "QUANTO ou QUANDO, nao apenas o que")
```

**4.2 · `impressao: PENDENTE` gera a mensagem errada.** Cai no ramo `elif imp != calc` e imprime *"tese ALTERADA apos o registro"* para algo nunca registrado. Correção:

```python
if imp in (None, "PENDENTE"):
    p.append(f"impressao ausente — registre `impressao: {calc}`")
elif imp != calc:
    ...
```

**4.3 · Adicionar o validador de `carregos`.** Função `validar_carrego(c)` análoga, exigindo: `C01` como data no futuro; `C02` com número; `C03` descrevendo evento e **não** contendo palavra de preço ("caiu", "abaixo de R$", "-%"); `C04.perda_estimada_pct` preenchido; `C06_reconhecimento` verdadeiro; e impressão sobre `C01+C02+C03`.

E um portão **G8 · compromisso de carrego**, gêmeo do G7, para funções com `exige_compromisso_de_carrego`.

---

## 5. O que acontece quando você preencher

**IPCA+:** com `PROTECAO_REAL` criada e um `carregos.td_ipca` válido, ele volta ao universo. O bloco conservador deixa de ser 100% Selic e passa a ser dividido entre LASTRO (Selic, sem marcação) e PROTECAO_REAL (IPCA+, com teto declarado em `C05`). O output passa a mostrar o teto e o custo estimado de quebrar o compromisso.

**HASH11:** com `hash11` válido, o G7 libera e o bloco APOSTA sai de 0% para `aposta_pct` (3% hoje). O teto continua sendo máximo absoluto, e as invariantes de saída continuam garantindo que redistribuição nenhuma o viole.

**Nenhum ativo foi excluído por falta de regra.** Os dois entram porque o papel de cada um foi nomeado — que era a sua objeção, e ela está certa.

---

## 6. Ordem de execução

1. Aplicar 4.1 e 4.2 no `tese.py`. Sem isso, a primeira tese correta que você escrever pode ser recusada.
2. Decidir a postura da §2.4 e registrar em `decisoes` do `politica.yaml`.
3. Acrescentar `PROTECAO_REAL` ao YAML e `funcoes=["PROTECAO_REAL","DATADO"]` em `td_ipca`.
4. Implementar `validar_carrego` e o G8 (4.3).
5. Preencher `carregos.td_ipca` e rodar `python tese.py` para pegar a impressão.
6. Preencher `teses.hash11` — apagando `exemplo: true` — e pegar a impressão.
7. Rodar `cenarios.py`. O bloco APOSTA deve sair 3%, e o conservador dividido.
8. Acrescentar teste: `test_ipca_volta_com_compromisso_registrado` e `test_carrego_sem_C03_e_invalido`.

---

## 7. Uma nota sobre o que você está construindo aqui

O bloco K não é burocracia para liberar ativo. É a única parte do sistema que registra **o que você acreditava antes de o preço se mover** — e ela existe porque a Parte I do seu dossiê concluiu que o valor do método está na arquitetura de decisão, não na tese de investimento.

Daqui a três anos, o `historico` do `teses.yaml` vale mais que qualquer indicador que o pipeline calcule: é o seu registro pessoal, out-of-sample por construção, de quantas teses se confirmaram, quantas foram abandonadas e quantas foram reescritas. Nenhum backtest produz esse dado, e ele é imune ao sobreajuste que contamina todos eles.

Preencher os dois registros custa uma tarde. É a tarde de maior retorno do projeto inteiro.

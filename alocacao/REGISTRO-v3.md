# Registro de correção — v3: as regras que faltavam

**Data:** 03/09/2026 · **Política:** 1.3.0 · **Testes:** 77 → 100, todos passando

Responde a três coisas: à sua objeção ("investimentos não devem sair por não ter regras;
devem ser definidas regras para os que não têm"), ao `laudo-alocacao-v2`, e à
especificação do `bloco-k-definicoes`.

---

## 1. Você estava certo, e o diagnóstico do documento é mais preciso que o meu

Eu tratei os dois casos como o mesmo problema. Não são:

| | Tesouro IPCA+ | HASH11 |
|---|---|---|
| Quem excluiu | **DATADO**, por exigir objetivo datado | **G7**, por falta de tese |
| O bloco K resolvia? | **Não** | Sim |
| O que faltava | Uma **função** que descrevesse o que ele faz | Uma **tese** falsificável |
| Modo de falha real | Vender antes do vencimento e materializar a marcação | Manter para sempre o que era temporário |

O IPCA+ não foi excluído por falta de tese. Foi excluído porque **nenhuma função do modelo
descrevia o que ele faz**: LASTRO exige perda nominal zero e ele tem marcação a mercado;
DATADO exige um prazo a casar e não havia prazo. Ele caiu no vão entre as duas — e o vão
era meu, não dele.

O princípio que reconcilia a sua objeção com a disciplina do sistema: **o sistema não
existe para excluir ativos, existe para exigir que o papel de cada ativo seja nomeado.**
Ativo sem papel nomeado não pode ser dimensionado, porque não há como saber quanto dele
é demais. Criar a regra que falta é o comportamento correto; afrouxar a que existe, não.

## 2. Função `PROTECAO_REAL` e o registro `CARREGO`

Juro real travado na compra, entregue integralmente **se e somente se** carregado até o
vencimento. Não é LASTRO (há marcação no caminho), não é DATADO (não exige objetivo,
exige **compromisso**), não é CRESCIMENTO (o retorno é contratado).

O registro `CARREGO` é o gêmeo da tese, para o outro modo de falha. Seis campos, e o que
importa é o **C03 — a condição de venda antecipada**: escrita antes da compra, e o
validador **rejeita condição de preço**, porque uma condição de preço em C03 autoriza
exatamente o erro que o registro existe para impedir. O portão novo é o **G8**.

**A duração não é constante de catálogo — vem do papel que você se compromete a carregar.**
Supor uma duração seria supor um compromisso que ninguém assumiu, e foi assim que a v1.0.0
alocou 17% num NTN-B de duração 18 anos sem prazo nenhum a casar.

## 3. A sua regra dos 10 anos é melhor que as três posturas que o documento oferecia

O `bloco-k-definicoes` §2.4 oferecia: horizonte cheio, horizonte com folga, ou objetivo
datado obrigatório. Você respondeu com uma quarta — **teto absoluto de 10 anos** — e ela
domina as três primeiras por um motivo estrutural: as duas primeiras amarram o compromisso
a um número que **você mesmo pode revisar**, o que é circular; a terceira mantinha o ativo
fora. Um teto absoluto é verificável, não depende do horizonte, e não precisa ser revisto
quando a vida muda.

Está em `politica.yaml → compromissos.maximo_anos`, com a distinção declarada: horizonte
de acumulação é **intenção**, compromisso é **trava**. Renda variável não tem prazo de
compromisso — pode ser vendida a qualquer momento sem quebrar promessa. Um NTN-B 2060 tem:
são 34 anos em que vender é assumir a marcação. O teto limita o segundo e não toca no
primeiro.

**Consequência concreta:** só entra papel com vencimento até **2036-09-02**. O NTN-B
Principal 2060 fica fora — agora por uma regra declarada, não por uma lacuna do modelo.

## 4. Registro ausente virou pendência, não exclusão

É a diferença que a sua objeção pedia. Uma rota sem registro não aparece na lista de
rejeitadas: aparece em `pendencias`, ao lado da pergunta do RH, **com a instrução exata** —
inclusive a data-limite que o teto de compromissos impõe, porque "preencha o registro" sem
dizer até quando não é instrução.

E nem IPCA+ nem cripto estão em `fora_de_escopo`. Há teste para isso.

## 5. V-01: minha correção anterior mudou o rótulo e não o comportamento

O laudo v2 está certo e é o achado mais importante dele. Eu escrevi no REGISTRO-v2 "só
elimina se perder em todos" e o código continuava eliminando toda rota que perdesse **no
horizonte declarado**. O conjunto de rotas eliminadas era idêntico ao da v1.0.0.

Agora os três modos existem em código (`menor_arrasto_no_horizonte`, `ambas`, `usuario`),
o YAML declara qual está ativo — o que você escolheu —, e um valor desconhecido levanta
erro. A diferença entre a v1.1.0 e esta não é o resultado; é que o resultado tem um nome
honesto e um parâmetro que o troca sem tocar em código.

**V-02, que era o achado por trás do achado:** o G3 elimina a Avenue por atrito antes de o
G4 vê-la, então a tabela de inversão nunca aparecia em uso real. A ordem não mudou, mas a
interação agora é **reportada**: quatro rotas eliminadas por atrito venceriam o IVVB11 em
15–30 anos, e isso está impresso no output em vez de ficar implícito.

## 6. Pré-registro do backtest — aberto desde o laudo Rev. 03, agora escrito

`estrategias_pre_registradas` no YAML, com nove entradas e **ordem de execução declarada**.
As três primeiras têm `hipotese_nula_esperada` e **devem falhar**: HML puro (0,05% ao mês
no Brasil), DY alto (três evidências convergentes em três classes), e SMB (prêmio
negativo). Se qualquer uma "funcionar", o defeito está no meu pipeline, não no mercado —
provavelmente look-ahead contábil.

Três coisas que valem mais que as estratégias e estão declaradas junto:

- **O benchmark é alfa contra os fatores do NEFIN**, não contra o Ibovespa. Bater o
  Ibovespa pode ser exposição a fatores conhecidos, e o Ibovespa tem concentração setorial
  alta. As séries são públicas e gratuitas — é a pendência 19, e é a que muda o patamar.
- **Toda estratégia é medida líquida de custo e imposto**, com o `custos.yaml` como insumo.
  É o único diferencial estrutural deste backtest frente a toda a literatura: **nenhum**
  retorno publicado é declarado líquido de corretagem, emolumentos, spread ou ganho de
  capital.
- **`variantes_permitidas` declarado antes.** Sem teto de busca, o resultado reportado é o
  máximo de uma amostra de tentativas — que é como a literatura foi construída (§9, D-5).

Os sete descontos obrigatórios sobre a literatura estão no YAML, um a um.

## 7. Demais achados fechados

V-03 (`horizonte_ir_dias` do G2 e `k_max` para o YAML, mais um teste que varre literais
numéricos no módulo — o caminho inverso da cobertura), V-04 e V-10 (fronteira de palavra
no validador: "atende a" deixa de ser recusado por conter "tende a"; "potencial" vira
aviso; `PENDENTE` tratado como ausente), V-05 a V-15 (docstring, invariante de RV
realizada, `casa_duracao` pelo menor prazo, alerta de objetivo inatingível, alerta de
função morta, `hash_custos` no cache, cópias no G6, universos separados no relatório,
freio sobre a compra executada, nota de bases).

Pendências 20 (regime de análise de instituições financeiras) e a ausência de critério de
seleção na sleeve de ação entraram no `fora_de_escopo` — as duas ausências que o laudo v2
§8 apontou.

## 8. O que uma tarde sua muda

O cenário 6 de `cenarios.py` é o **mesmo** cenário 3, com os dois registros preenchidos.
Nenhum dado novo, nenhuma pesquisa, nenhuma corretora aberta:

```
                                          cenário 3          cenário 6
crescimento                                  65,0%              63,0%
proteção real (IPCA+, carregado até 2035)     0,0%              15,0%
lastro (Selic, sem marcação)                 35,0%              19,0%
aposta (HASH11)                               0,0%               3,0%
```

As frases do cenário 6 são **exemplos de forma, não de conteúdo**. Se eu escrever K02, K03
e K04, o registro deixa de ser pré-registro e vira sugestão minha com a sua assinatura —
que é exatamente o que o bloco K existe para impedir.

Um número que aparece quando o HASH11 entra e vale olhar: **56,6% do aportado** em custo,
em 25 anos, contra 1,5% da ação individual. O teto de 3% existe porque a perda pode ser
100%; o custo de 1,3% ao ano é uma segunda razão, independente, e ela não depende de
nenhuma opinião sobre cripto.

## 9. Continua aberto

1. **A pergunta ao RH da Volga** (G0). Entrada de maior valor unitário do sistema, e
   nenhuma pesquisa minha resolve.
2. **Pendência 19 — séries de fatores do NEFIN.** Destrava o benchmark correto de todas as
   nove estratégias pré-registradas.
3. Pendência 20 — bloco de análise para instituições financeiras.
4. Pendência 12 — piso de cotistas da isenção de FII (50 ou 100), e pendência 25 — série do
   S&P/B3 Baixa Volatilidade, separando pré e pós-lançamento.
5. Fase 0 do pipeline (CVM DFP/ITR com as sete armadilhas). É o que transforma o
   pré-registro em backtest.
6. LCI/LCA e FII, nessa ordem.

# Registro de correção — camada de alocação v2 e bloco K

**Data:** 03/09/2026 · **Política:** 1.1.0 · **Testes:** 43 → 77, todos passando

Responde ao backlog §7 da `docs/referencia/auditoria-camada-alocacao.md` e à recomendação de sequência
da §8 do `auditoria/escopo-campos-de-analise.md` ("bloco K primeiro — antes de qualquer campo
calculado").

---

## 1. Os cinco achados bloqueantes

| Achado | O que era | O que é agora | Efeito no resultado |
|---|---|---|---|
| **A-01** dominância inverte com o horizonte | `g4` comparava arrasto num único horizonte e chamava isso de lógica | compara em 5/15/30 + o horizonte do usuário; só elimina se perder em **todos**. Se a ordem inverte, a rota sai rotulada `PREFERENCIA_DE_HORIZONTE`, com a tabela completa no output | IVVB11 × Avenue deixa de ser "dominância". O teste prova a inversão: 5a → IVVB11, 30a → Avenue |
| **A-02** G3 promete o que é falso | "ela volta sozinha quando o aporte cresce" valia só para `acao_450` | custo de entrada separado em **FIXO** (dilui; o sistema calcula o aporte de reentrada) e **PERCENTUAL** (não dilui; não volta nunca) | o output agora diz `acao_450: volta com aporte de R$464` e `ext_avenue: custo PERCENTUAL — não volta com aporte nenhum` |
| **A-03** metade do YAML nunca era lida | 8 chaves declaradas e ignoradas; `base_anos` fixo no Python | todas implementadas + `test_cobertura_yaml` percorre `funcoes/portoes/crescimento/tetos` e falha se alguma não for referenciada. As exceções documentais são uma lista explícita no teste | `custo_maximo_classe_peso` **limita** em vez de excluir; FGC por conglomerado verificado; G6 criado para `exige_liquidez_dias`/`exige_perda_maxima` |
| **A-04** `td_ipca` com 17% sob DATADO sem objetivo | DATADO recebia peso sem nenhum prazo a casar | criada a função **LASTRO** (estabilidade sem data; regra: sem marcação a mercado). DATADO exige objetivo **e** casamento de duração | **Tesouro IPCA+ sai da carteira**: 0% sem objetivo datado. Os 35% conservadores vão para Tesouro Selic |
| **A-05** G1 comparava líquido com bruto | dívida entre 0,84% e 1,09% a.m. passava batido | comparação líquido × líquido, com alíquota da faixa declarada no YAML (180 dias → 22,5%) | teste na fronteira: 0,90% a.m. **dispara**, e o teste verifica que 0,90% fica entre o líquido (0,86%) e o bruto (1,09%) |
| **A-06** deriva sobre desvio absoluto | o aporte só compra, mas o gatilho olhava o desvio nos dois sentidos | gatilho sobre o maior **déficit**; o excesso sai separado | cenário [c]: déficit 25,0 p.p. × excesso 79,2 p.p. — o veredito é o mesmo, o motivo agora é o certo |

## 2. Portões novos

- **G0 · match do empregador** — roda **antes do G1**, porque é a única rota que domina
  o pagamento de dívida. Enquanto `match_verificado=False`, emite **PENDÊNCIA em todo
  output**: desconhecido não é ausente.
- **G6 · coerência função–rota** — uma rota só ocupa uma função se satisfizer
  `exige_liquidez_dias` e `exige_perda_maxima`. Perde a função, não o catálogo.
- **G7 · tese registrada** — é o bloco K. Rota de função com `exige_tese_registrada`
  não recebe alocação sem tese válida em `teses.yaml`.

## 3. Bloco K e bloco L — `tese.py` + `teses.yaml`

Construídos antes de qualquer campo calculado, como a §8 do escopo recomenda: são os
únicos campos que nenhum dado público preenche e os únicos que mudam comportamento hoje.

O validador recusa: `K02` com expressão não falsificável (*"longo prazo"*, *"potencial"*,
*"acredito"*, *"tende a"*), `K03` que não seja uma data, `K04` idêntica a `K02`, `K01`
diferente de 100% no catálogo especulativo, bloco L sem execução registrada.

**Mecanismo anti-reclassificação retroativa:** a tese carrega uma **impressão** (hash de
K02+K03+K04). Alterar qualquer um dos três sem mover o registro anterior para `historico`
invalida a tese. Reescrever a tese depois de ver o preço deixa de ser possível sem rastro.

**Consequência imediata, e é deliberada:** `teses.yaml` no repositório contém apenas o
**modelo**, marcado `exemplo: true`. Portanto **o bloco APOSTA recebe 0% hoje** — não
porque cripto seja ruim, mas porque não há tese escrita. Escrever uma frase falsificável
com data é a única coisa que destrava a posição, e é a única peça do sistema inteiro que
não depende de dado nenhum.

## 4. Escopo declarado

`fora_de_escopo` no YAML, **13 classes**, uma linha por ausência com motivo e gatilho de
reentrada, e o bloco viaja para o output de `alocar`. Prioridade 1: LCI/LCA, cofrinhos
acima de 100% do CDI, ouro e dólar (SEGURO_CAUDA está morto na prática — uma rota, e ela
é eliminada por atrito em todos os cenários).

## 5. Implementação

`assert` → `raise ValueError` nas invariantes de saída (`python -O` removia a guarda que
impede o retorno dos 60% em cripto) · **caixa** como posição, e o resíduo de lote vai para
ela em vez de inflar a primeira ordem · `negocia_em_lote` explícito no lugar da heurística
`if p > 1` · segunda coluna de custo (**custo total como % do aportado**) · `politica_hash`
e `custos_hash` no retorno de `alocar` · G2 escolhe por **retorno líquido**, não por ordem
alfabética.

## 6. Bugs encontrados pelos testes novos

- **Bloco vazio engolia peso.** Com o bloco DATADO vazio, `espalhar` devolvia `0.0` em vez
  do total como sobra, e os pesos somavam **0,806**. O `raise` da invariante pegou.
- **O ranking de liquidez é sensível ao tamanho da reserva** e o teste que eu escrevi
  primeiro estava errado: até R$10 mil o Tesouro é isento de custódia e ganha; acima disso
  a custódia de 0,20% a.a. o derruba abaixo do RDB a 100% do CDI. Com reserva-alvo de
  R$27 mil, **o RDB ganha** — e ganha por um motivo real, não por ordem alfabética.

## 7. O que continua aberto

1. **Pergunta ao RH da Volga** (G0). É a única entrada que o sistema não consegue obter
   sozinho e a de maior valor unitário.
2. Pré-registro do backtest — datado, antes de qualquer resultado contaminar o critério.
3. LCI/LCA e FII, nessa ordem (a pesquisa de LCI já está feita).
4. Lacunas de pesquisa: BOVV11, taxas de ETF, liquidez de ETF de renda fixa.
5. Fase 0 do pipeline (CVM DFP/ITR com as sete armadilhas).

# Laudo — camada de alocação v2 e bloco de tese

**Objeto:** `alocacao.py` (806 l.), `politica.yaml` (350 l.), `tese.py` (140 l.), `teses.yaml`, `test_alocacao.py` (528 l.), `cenarios.py`, `demo_aporte.py`, as duas saídas e o `REGISTRO-v2.md`.
**Emissão:** 03/09/2026. Verifica o REGISTRO-v2 contra o código, e audita o que é novo.
**Método:** leitura integral; rastreio de cada achado do laudo de 02/09 até a linha que o implementa; execução isolada do validador de tese.

**Limitação, pela terceira vez:** `motor.py` e `custos.yaml` continuam ausentes do upload. Não posso verificar `val()`, `custodia_rv_aa()`, `InsumoBloqueado`, as faixas de custódia nem uma única constante. Isso agora bloqueia parte da auditoria: metade do `catalogo()` são chamadas a `val()` sobre chaves que eu não vejo, e o `test_cobertura_yaml` cobre o `politica.yaml`, não o `custos.yaml`.

---

## 1. Veredito

> A v2 corrige de fato onze dos treze achados, com testes de regressão que descrevem o defeito no docstring — e três das correções (LASTRO, G0, bloco K) são melhores do que o laudo pedia. Mas a correção do achado principal, A-01, mudou o rótulo e **não mudou o comportamento**: o conjunto de rotas eliminadas pelo G4 é matematicamente idêntico ao da v1. E o defeito estrutural A-03, que a v2 declara fechado com um teste automatizado, reaparece em duas linhas que o teste não pode alcançar.

---

## 2. O que foi corrigido de verdade

Registro antes das críticas porque a maior parte do trabalho está certa.

| Achado | Verificado em | Qualidade da correção |
|---|---|---|
| **A-02** G3 promete o que é falso | `custo_entrada_fixo_pct` / `custo_entrada_percentual`, l. 222-231 | **Melhor que o pedido.** Não só separa as naturezas: calcula o aporte de reentrada (`r.corr_fix/(teto-pct)`) e o imprime. O output diz `acao_450: volta com aporte de R$464` e `ext_avenue: não volta com aporte nenhum` |
| **A-04** DATADO sem objetivo | Função `LASTRO` no YAML + `necessidade_datada` + `casa_duracao` | **Melhor que o pedido.** Eu havia oferecido três saídas; foi escolhida a que preserva a taxonomia, e o resultado é visível: Tesouro IPCA+ sai da carteira, os 35% conservadores vão para Selic |
| **A-05** G1 líquido × bruto | `g1_divida` l. 354-376 com `retorno_liquido_aa` | Correta, e o teste ataca a fronteira exata que eu apontei: 0,90% a.m. dispara, e verifica que fica entre 0,86% líquido e 1,09% bruto |
| **A-06** deriva sobre desvio absoluto | `motor_aporte` l. 788-801 | Correta. `deficit_rel` e `excesso_rel` separados, e o output explica que excesso não é problema do aporte |
| **B-01/02/03** resíduo e caixa | l. 784-786 | Correta. O resíduo vai para caixa; `valor == quantidade × preço` preservado, e há teste com preços reais |
| **B-04** heurística de lote | `negocia_em_lote` na dataclass | Correta |
| **B-05** `assert` sob `-O` | l. 698-708 | Correta, com o motivo no comentário |
| **B-06** rótulo do arrasto | Docstring de `arrasto_anualizado` + `custo_pct_aportado` | **Modelar.** A docstring reproduz o achado e dá os números (0,73% em 5a, 1,05% em 40a para uma taxa de 1,30%). A segunda coluna existe e aparece no output |
| **B-08** G2 por ordem alfabética | `retorno_liquido_aa` + `criterio_escolha_rota` no YAML | Correta, e o `ranking` completo vai para a memória da diretiva |
| **B-09** procedência | `politica_hash`, `custos_hash`, `gerado_em` | Correta, e viaja para o output |
| **B-10** cache | `_CACHE_ARRASTO` | Correta em intenção — ver V-11 |

**Os três portões novos são adições próprias, não correções, e as três se justificam.** G0 antes do G1 está certo: contrapartida do empregador é o único retorno que domina o pagamento de dívida, e emitir **pendência** enquanto `match_verificado=False` — desconhecido não é ausente — é a decisão de desenho mais madura do arquivo. G6 transforma `exige_liquidez_dias` e `exige_perda_maxima` de prosa em verificação, e faz a rota perder a função e não o catálogo. G7 é o bloco K virando portão.

**O bloco K é a melhor peça do conjunto.** A impressão como hash de K02+K03+K04, com `historico` obrigatório para substituir, torna a reclassificação retroativa impossível sem rastro. O `teses.yaml` do repositório conter apenas o modelo marcado `exemplo: true` — e portanto o bloco APOSTA sair com 0% hoje — é a aplicação mais literal e mais honesta do princípio de pré-registro em todo o projeto. E há teste para isso (`test_teses_yaml_do_repositorio_nao_libera_nada_por_acidente`).

**Os dois bugs que os testes novos encontraram** (bloco vazio engolindo peso, e o ranking de liquidez sensível ao tamanho da reserva) são exatamente o que testes existem para encontrar, e o registro documenta o segundo admitindo que o teste inicial estava errado. Isso é o padrão certo.

---

## 3. V-01 · A-01 foi corrigido no rótulo, não no comportamento

**Estatuto: FATO, verificável por leitura. É o achado principal deste laudo.**

O `REGISTRO-v2` afirma: *"só elimina se perder em todos"*. O código, l. 445-459:

```python
dom = [o for o in rivais if all(arr[(o.id,h)] < arr[(r.id,h)] - 1e-12 for h in hs)]
if dom:
    dominados.append(...); continue          # eliminada
pref = [o for o in rivais if arr[(o.id,anos)] < arr[(r.id,anos)] - 1e-12]
if pref:
    preferencia.append(...); continue        # TAMBÉM eliminada
vivos.append(...)
```

Uma rota chega a `vivos` **se e somente se** nenhum rival é mais barato no horizonte do usuário. Na v1, a condição de sobrevivência era exatamente a mesma. **O conjunto de rotas eliminadas é idêntico ao da v1.** O que mudou foi o rótulo (`dominados` vs. `preferencia_horizonte`) e o relatório (a tabela por horizonte).

Isso não é pouco — o relatório tem valor real, e o usuário passa a ver que a ordem inverte. Mas o achado A-01 não era sobre nomenclatura: era que **eliminar por um número que inverte com o horizonte não é lógica**, e a eliminação sobreviveu intacta. Se a ordem inverte, as duas rotas são candidatas legítimas, e a escolha entre elas é do usuário — não do portão.

**Correção:** rota em `preferencia_horizonte` **permanece em `vivos`**, com marca. Se duas rotas de mesma exposição sobrevivem, o desempate no bloco é do 1/N (as duas entram com metade do peso) ou de uma escolha declarada no YAML (`desempate_preferencia_horizonte: usuario | menor_arrasto_no_horizonte | ambas`). Hoje o default silencioso é "menor arrasto no horizonte", e ele não está declarado em lugar nenhum.

**V-02 · E o caminho novo está morto na prática.** `alocar` chama `g3_atrito` (l. 569) antes de `g4_dominancia` (l. 572). Avenue é eliminada por atrito a 1,60% e nunca chega ao G4. Os cinco cenários confirmam: `0 por horizonte` em todos. A tabela de inversão que o teste prova **nunca é impressa em uso real**. O achado original — "os dois portões em sequência produzem um resultado que nenhum dos dois produziria sozinho" — continua verdadeiro e não foi endereçado.

---

## 4. V-03 · A-03 reaparece em duas linhas que o teste não alcança

**Estatuto: FATO.**

O `test_cobertura_yaml_secoes_operacionais` verifica que toda chave do YAML **é lida**. Não verifica o inverso: que nenhuma constante operacional está **fixa no Python**. E há duas:

```python
# l. 393, g2_reserva
ranking = sorted(((r, retorno_liquido_aa(r, C, 180, alvo)) for r in liq), ...)
```

O `180` é o prazo que define a faixa de IR. O G1, três funções acima, lê o análogo do YAML (`g["horizonte_ir_dias"]`). O G2 não. **Assimetria entre dois portões que fazem a mesma comparação**, e o parâmetro que decide se a poupança isenta vence ou perde para o RDB tributado está fora da política.

```python
# l. 739
def motor_aporte(estado, alvo, C, P, precos=None, k_max=2, rotas_por_id=None):
```

`k_max=2` é o número máximo de ordens por aporte — decisão de política pura (fricção operacional × velocidade de convergência), fixada na assinatura da função.

**Correção:** ambos para o YAML, e um segundo teste que faça o caminho inverso — varrer o módulo por literais numéricos fora de `catalogo()` e falhar em qualquer um não declarado numa lista de exceções.

---

## 5. V-04 · O validador de tese rejeita teses válidas por casamento de substring

**Estatuto: FATO, demonstrado por execução.**

`tese.py`, l. 20-22, testa `if v in baixo` — substring crua. Rodei o filtro:

```
['tende a']    <- "a empresa atende a 3 milhoes de clientes ate 31/12/2030"
['potencial']  <- "a capacidade potencial instalada atinge 500 MW ate 2029"
[]             <- "o contrato com a Petrobras e renovado ate 30/06/2028"
```

**"atende a" contém "tende a".** Uma tese perfeitamente falsificável, com métrica e data, é recusada. E "potencial" como substantivo técnico (capacidade potencial, potencial hidrelétrico) é indistinguível de "potencial" como expectativa vaga.

O custo aqui é maior que o de um falso positivo comum: o bloco K é o único componente do sistema que exige esforço criativo do usuário, e um validador que recusa a primeira tentativa correta é o caminho mais rápido para o arquivo nunca ser preenchido.

**Correção:** casar por palavra com fronteira (`\btende a\b` ainda pega "atende a"? não — `\b` antes de `tende` falha em "atende", porque `n` e `t` são ambos caracteres de palavra). Regex com `\b` resolve o primeiro caso. Para "potencial", nenhuma regex resolve: **rebaixe de rejeição a aviso**. A regra dura que sobrevive é estrutural, não lexical — e o arquivo já a tem: `K03` tem de ser uma data, `K04` tem de diferir de `K02`, e `K02` precisa de um número verificável. Sugiro trocar o teste de vaguidade por: *K02 contém pelo menos um número e pelo menos uma data ou referência a K03*.

**V-10 · E a mensagem de `impressao: PENDENTE` está errada.** O `teses.yaml` do repositório traz `impressao: PENDENTE`. O validador cai no ramo `elif imp != calc` e imprime *"tese ALTERADA apos o registro"* — para uma tese que nunca foi registrada. Trate `PENDENTE` no mesmo ramo de `None`.

---

## 6. Outros achados

**V-05 · `espalhar` contradiz o próprio docstring.** A docstring (l. 621) diz *"Excesso NUNCA sai do bloco"*. Dois caminhos fazem exatamente isso: `if not baratas: return max(0.0, resto)` (l. 636) e o `return sobra` do teto por rota (l. 643). O valor retornado vira `sobra` e é redirecionado ao bloco conservador (l. 663-671). O comportamento é defensável; a documentação está errada, e num arquivo cuja disciplina é declarar tudo, isso importa.

**V-06 · Não há invariante sobre a fração de RV realizada.** As invariantes de saída (l. 700-708) verificam soma 1,0 e os tetos de APOSTA e SEGURO_CAUDA. Não verificam que o peso efetivamente alocado a CRESCIMENTO é igual a `p_rv`. Como a sobra pode migrar de CRESCIMENTO para LASTRO (V-05), a `fracao_rv` impressa no cabeçalho pode divergir da realizada sem que nada alerte. Hoje coincide nos cinco cenários; não é garantido.

**V-07 · `casa_duracao` usa `any` sobre os objetivos.** Com objetivos de 1 e de 20 anos, `td_ipca` (duração 18) casa com o segundo, entra no bloco DATADO — e recebe peso dimensionado pela necessidade **total**, que inclui o objetivo de 1 ano. O bloco é dimensionado pelo agregado e casado por um objetivo isolado. **Correção:** alocar por objetivo, não por bloco agregado, ou exigir que a duração case com o **menor** prazo entre os objetivos que o bloco financia.

**V-08 · Objetivo inatingível é silenciado.** `necessidade_datada` faz `min(1.0, total/base)`. Se `total > base`, o objetivo não cabe no aporte no prazo — e o sistema aloca 100% do bloco conservador sem dizer que a meta é inalcançável. **Correção:** alerta com o déficit e o aporte necessário.

**V-09 · Função sem rota viável some sem aviso.** `p_cauda` e `p_aposta` são zerados quando `por_funcao[f]` está vazio (l. 609-611), e os 100% se redistribuem. Nos cinco cenários, SEGURO_CAUDA fica em 0% porque sua única rota é eliminada por atrito, e APOSTA em 0% por falta de tese. O segundo aparece no output (bloco `SEM TESE REGISTRADA`); **o primeiro não aparece em lugar nenhum**. Uma função declarada na política com zero rota viável merece alerta explícito — e o `fora_de_escopo` já registra o diagnóstico em `ouro_e_dolar`, o que torna a omissão no output mais estranha.

**V-11 · Chave de cache com `id(C)`.** L. 272. `id()` de um objeto coletado pode ser reutilizado; um `C` recarregado pode receber o mesmo `id` e servir arrasto obsoleto. Baixa probabilidade, consequência silenciosa. Use `hash_custos()`.

**V-12 · `g6_coerencia_funcao` muta `r.funcoes` no lugar** (l. 488). Hoje é seguro porque `catalogo()` reconstrói a cada chamada — mas `cenarios.py` e `demo_aporte.py` mantêm um `ROTAS` de uma chamada **separada**, então as rotas que o output nomeia não são as que o pipeline filtrou. Funciona porque só se usa `.nome`. Prefira devolver cópias.

**V-13 · As três rotas de LIQUIDEZ contam como "vivas" e nunca podem receber peso.** Não há `p_liquidez` na decomposição (l. 609-616) — corretamente, porque a reserva é tratada pelo G2. Mas elas atravessam G3, G5, G7 e G4 e entram em `vivos`, inflando o "11 vivas" do output. **Correção:** separar o universo de elegibilidade do universo de alocação no relatório.

**V-14 · O freio de concentração avalia uma compra que não é a executada.** L. 758: `w_pos = (pos + min(d,A))/(V+A)` supõe que o déficit inteiro (limitado ao aporte) será comprado. A ordem real é `min(d, restante)`, que pode ser menor por causa do `k_max` e do lote. O freio pode excluir uma rota que, de fato, não cruzaria a banda. Conservador, mas inconsistente com o que é executado.

**V-15 · Bases mistas na mesma linha do output.** `peso_atual` usa `V`; `deficit` usa `(V+A)`. A linha `deficit 2.235 · atual 13.5% · alvo 35.0%` é correta e não é explicada. Uma nota de rodapé resolve.

---

## 7. Testes

A suíte foi de 43 para 77, os testes de regressão nomeiam o bug no docstring, e há cobertura nova para horizonte (`test_invariantes_valem_em_todo_horizonte`), determinismo, procedência, preços reais e travessia do limiar de custo de classe. É a melhor suíte do projeto.

Buracos que restam:

1. **Nenhum teste afirma que `preferencia_horizonte` não recebe peso** — porque, se afirmasse, exporia V-01. `test_nenhuma_rota_eliminada_recebe_peso` provavelmente cobre o conjunto; o que falta é o teste que **deveria falhar hoje**: `test_rota_em_preferencia_horizonte_permanece_candidata`.
2. **Nenhum teste de literal fixo no Python** (V-03). O teste de cobertura só anda numa direção.
3. **Nenhum teste com dois objetivos de prazos diferentes** (V-07).
4. **Nenhum teste de falso positivo do validador de tese** (V-04). Um único caso — "atende a" — pegaria.
5. **Nenhum teste de que a fração de RV realizada bate com `p_rv`** (V-06).
6. **Nenhum teste sobre `custos.yaml`.** O `test_cobertura_yaml` cobre a política. O catálogo inteiro depende de chaves do custos que ninguém verifica.

---

## 8. Escopo

O bloco `fora_de_escopo` com treze classes, motivo e gatilho de reentrada, viajando para o output, fecha o achado §6.4 do laudo anterior de forma completa. As prioridades declaradas (LCI/LCA, cofrinhos acima de 100% do CDI, ouro e dólar) coincidem com as que a auditoria apontou, e o motivo de `ouro_e_dolar` cita o diagnóstico correto.

**O que continua fora do bloco e deveria estar:**

- **Instituições financeiras.** Pendência 20, aberta desde o achado A-06 do primeiro laudo. `C-01` a `C-03` são indefinidos para banco, e o catálogo de ON já inclui a espécie que existe para reter bancos. Não é uma "classe de ativo" — é um regime de análise ausente —, mas o `fora_de_escopo` é hoje o único lugar do sistema onde uma ausência fica declarada.
- **Ações ON individuais como sleeve com critério.** A rota `acao_zero` existe e recebe 10,8% em três cenários, com o requisito de diversificação corretamente calculado (3 papéis). Mas **não há critério nenhum de escolha dos papéis** — nem portão, nem campo. O sistema aloca a uma sleeve cujo conteúdo é indefinido. Isso é coerente com `permite_score: false` e com a decisão A-05 em aberto, mas merece a mesma declaração explícita que as treze classes ausentes têm.

---

## 9. Backlog

**Bloqueante:**

1. Rota em `preferencia_horizonte` permanece em `vivos`, com desempate declarado no YAML. → V-01
2. Decidir a ordem G3 × G4, ou declarar que a interação é conhecida e aceita. → V-02
3. `horizonte_ir_dias` do G2 e `k_max` para o YAML; teste de literal fixo. → V-03
4. Validador de tese: fronteira de palavra, "potencial" de rejeição para aviso, `PENDENTE` tratado como ausente. → V-04, V-10

**Correções de menor porte:** V-05 (docstring), V-06 (invariante de RV realizada), V-07 (`casa_duracao` por objetivo), V-08 (alerta de objetivo inatingível), V-09 (alerta de função sem rota), V-11 (`hash_custos` no cache), V-12 (cópias no G6), V-13 (separar universos no relatório), V-14 (freio sobre a compra executada), V-15 (nota de rodapé das bases).

**Testes:** os seis da §7.

**Escopo:** bloco de financeiras; declaração explícita de que a sleeve de ação não tem critério de seleção.

**Continua aberto do laudo anterior, sem regressão:** a pergunta ao RH da Volga (G0, e é a entrada de maior valor unitário do sistema), o pré-registro do backtest datado, e a decisão A-05, que o próprio código agora bloqueia com um `raise` explícito em `permite_score` — o que é a forma certa de manter uma decisão aberta sem default silencioso.

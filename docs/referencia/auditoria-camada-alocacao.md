# Auditoria da camada de alocação

**Objeto:** `alocacao.py` (467 l.), `politica.yaml` (156 l.), `test_alocacao.py` (190 l.), `cenarios.py`, `demo_aporte.py` e as duas saídas registradas.
**Emissão:** 02/09/2026.
**Método:** leitura integral; recálculo independente de `arrasto_anualizado` fora do módulo, para testar as invariantes que o código assume.

**Limitação declarada:** `motor.py` e `custos.yaml` **não foram enviados**. Não pude verificar `val()`, `custodia_rv_aa()`, `InsumoBloqueado` nem uma única constante de custo. Tudo que segue sobre valores numéricos foi reproduzido com as faixas de custódia e o CDI que constam das suas pesquisas, não com o seu YAML. Se algum número divergir, o defeito pode estar no que eu não vi.

---

## 1. Veredito

> A camada é o melhor código do projeto e o primeiro artefato que corrige, no próprio desenho, achados dos laudos anteriores — o G5 de status, o freio sobre rota em vez de papel, o teto de aposta como máximo absoluto, o motor que se recusa a rodar sem posição. Mas dois portões que a política declara serem "lógica, não juízo" são, na verdade, dependentes de parâmetros que o código fixa arbitrariamente: a dominância inverte entre 10 e 15 anos, e a promessa de que uma rota "volta sozinha quando o aporte cresce" é falsa para todas as rotas de custo percentual. E metade do `politica.yaml` nunca é lida pelo código.

---

## 2. Qualidades — o que deve ser preservado

| ID | Qualidade | Por quê |
|---|---|---|
| Q-01 | **G5_status implementado como portão de primeira classe** | O achado K-07 do laudo virou código: rota com insumo `NÃO_CONFIRMADO` sai da ordenação e aparece separada, com o motivo. BOVV11 fica fora e o output mostra a razão. É a correção mais importante do laudo anterior, e foi feita |
| Q-02 | **Teto de função como máximo absoluto, com a sobra proibida de ir para APOSTA** | O comentário nas linhas 300-304 documenta o bug que produziu 60% em cripto e a correção. Um comentário que explica *por que a semântica é essa* vale mais que dez que descrevem o que o código faz |
| Q-03 | **Distinção sleeve × papel** | Teto por ativo vira `n_minimo = ceil(peso/teto)`, requisito de diversificação, não freio. Confundir os dois barrava a carteira inteira, e o teste de regressão registra isso |
| Q-04 | **`motor_aporte` se recusa a rodar sem patrimônio, e diz o que roda sem ele** | Responde ao achado central da Rev. 02 do laudo. E a mensagem não é um erro: é uma orientação |
| Q-05 | **Taxonomia por função de risco, não por classe de produto** | LIQUIDEZ / DATADO / CRESCIMENTO / SEGURO_CAUDA / APOSTA substitui a fusão de três coisas em "reserva de valor". Cripto em APOSTA com o argumento de Choi & Shin é a decisão conceitual mais bem fundamentada do arquivo |
| Q-06 | **`custo_de_discordar`** | Mostra o preço da divergência em vez de impedir, e a nota separa explicitamente custo (computável) de retorno (não computável sem backtest pré-registrado). É o desenho certo |
| Q-07 | **Dois testes de regressão com o bug no docstring** | `test_teto_de_aposta_nunca_e_violado` e `test_aporte_produz_ordem_em_carteira_normal` descrevem o defeito que motivou o teste. É exatamente o que o manual pede |
| Q-08 | **Justificativa acadêmica no lugar certo** | DeMiguel/Garlappi/Uppal aparece como razão para *não* otimizar. Usar literatura para justificar a ausência de sofisticação é mais difícil que usá-la para justificar a presença |
| Q-09 | **`fila` e `alertas` separados no freio de concentração** | Rota acima da banda sai da fila e **não é vendida** — quarentena automática, coerente com o princípio de que o motor só compra |

---

## 3. Achados críticos

### A-01 · A dominância (G4) inverte com o horizonte, e a política declara que ela é lógica

**Estatuto: FATO, verificado por recálculo.**

`politica.yaml` afirma: *"Dominância é lógica, não juízo."* O código a computa em um único ponto:

```python
def g4_dominancia(pares, C, aporte, anos):
    arr = {r.id: arrasto_anualizado(r, C, aporte, anos) for r, _ in pares}
```

Recalculei `IVVB11` (adm 0,23% + custódia B3) contra `ext_avenue` (entrada 1,60% por aporte, adm 0,03%) — **mesma `exposicao="sp500"`**, portanto rivais diretos sob G4:

| Horizonte | IVVB11 | Avenue | Vencedor |
|---:|---:|---:|---|
| 3 anos | 0,136% | 0,556% | IVVB11 |
| 5 anos | 0,138% | 0,340% | IVVB11 |
| 10 anos | 0,158% | 0,180% | IVVB11 |
| **15 anos** | 0,173% | 0,127% | **Avenue** |
| 25 anos | 0,192% | 0,087% | Avenue |
| 40 anos | 0,205% | 0,065% | Avenue |

**A ordem inverte entre 10 e 15 anos.** Nos seus cenários (25 e 30 anos), Avenue dominaria IVVB11 — mas Avenue é eliminada antes, pelo G3, e o G4 nunca a vê. **Os dois portões em sequência produzem um resultado que nenhum dos dois produziria sozinho**, e a justificativa declarada de ambos está errada nesse ponto.

**Correção:** dominância só é lógica se for **invariante no horizonte relevante**. Compute o arrasto em pelo menos três horizontes (5, 15, 30) e só elimine se A perder em todos. Se a ordem inverter, não é dominância — é preferência de horizonte, e deve aparecer como tal no output.

### A-02 · O G3 promete algo que é falso para toda rota de custo percentual

**Estatuto: FATO.**

`politica.yaml`, G3_atrito: *"Ela volta sozinha quando o aporte cresce. Isto é o que a tabela de custos permite fazer e que nenhum sistema faz."*

Mas `custo_entrada_pct` é:

```python
return (r.corr_fix/aporte if aporte else math.inf) + r.corr_pct + (B3V if r.b3_vista else 0) + r.entrada_extra
```

Só o primeiro termo depende do aporte. Para `ext_avenue` (`entrada_extra = 1,60%`), `ext_nomad1` (3,10%), `ext_vest` (1,40%) e `ext_conta` (1,10%), o custo de entrada é **constante em qualquer aporte**. Nenhuma delas volta ao universo jamais — nem com aporte de R$ 100.000.

A única rota que se comporta como a política promete é `acao_450`, que tem `corr_fix`. E o teste que deveria provar isso não prova:

```python
def test_exterior_volta_ao_universo_com_aporte_grande():
    """A rota estrangeira nao e 'ruim': ela e inelegivel enquanto o aporte e pequeno."""
    ...
    P2 = {..."teto_custo_entrada_pct":0.02}   # relaxa o TETO, não aumenta o aporte
```

**O nome e a docstring do teste afirmam uma coisa; o corpo testa outra.** O teste passa e a afirmação continua falsa.

**Correção:** reescrever a regra do G3 no YAML separando os dois casos — custo fixo diluível pelo aporte, custo percentual não —, e renomear o teste para `test_rota_com_custo_percentual_nao_volta_com_aporte_maior`, assertando o comportamento real.

### A-03 · Metade do `politica.yaml` nunca é lida

**Estatuto: FATO. É o achado mais estrutural.**

O P3 diz "regras são dados". Um leitor do YAML acredita que o sistema faz coisas que ele não faz:

| Parâmetro declarado | Situação no código |
|---|---|
| `tetos.custo_maximo_classe_peso: 0.10` | **Nunca lido.** O YAML diz "classe cara é *limitada* a 10%"; o código **exclui** a rota do bloco (`baratas or bloco`) |
| `tetos.por_emissor_credito_privado: 250000` | **Nunca lido.** O campo `RotaAloc.emissor` existe e nunca é consultado |
| `tetos.por_conglomerado: true` | **Nunca lido.** A lição do Banco Master está no comentário e fora do código |
| `funcoes.*.exige_liquidez_dias` / `exige_perda_maxima` | **Nunca lidos.** `liquidez_dias` e `perda_maxima` existem em `RotaAloc` e nunca são verificados contra a função |
| `funcoes.*.prioridade` | Nunca lido |
| `funcoes.DATADO.regra` | Nunca lida — ver A-04 |
| `crescimento.dentro_da_classe.permite_score` | Nunca lido |
| `revisao.*` | Nada implementado (documental — aceitável) |

E o inverso também ocorre: `fracao_rv` lê `c["ajuste_horizonte"].get("base_anos", 10)`, e **`base_anos` não existe no YAML**. O valor 10 está fixo no Python. `meses_base` veio corretamente do YAML; o análogo do horizonte, não.

**Correção:** um teste que percorre o YAML e falha se alguma chave sob `tetos`, `portoes` ou `crescimento` não for referenciada pelo módulo. É a única forma de manter P3 verdadeiro ao longo do tempo, e pegaria as oito linhas de uma vez.

### A-04 · `td_ipca` recebe 17% sob a função DATADO sem nenhum objetivo datado

**Estatuto: FATO. É o achado conceitual mais grave.**

O YAML define DATADO como *"dinheiro com destino e prazo conhecidos. Duração casada com o prazo"*, com a regra `duracao_do_instrumento <= prazo_do_objetivo`. A dataclass `Objetivo` existe, `Estado.objetivos` existe — e **nenhum dos dois é usado em lugar nenhum do módulo**.

Nos cenários 3, 4 e 5 não há objetivo algum, e o sistema aloca 17% (cenário 3) em Tesouro IPCA+ Principal sob DATADO. O próprio catálogo anota a consequência: *"marcação a mercado: +2 p.p. de juro real derruba ~47% o vencimento 2060."*

Alocar 17% num instrumento com risco de marcação a mercado, sob uma função cuja definição exige casamento de duração, sem nenhum prazo a casar, **é exatamente o erro de taxonomia que a taxonomia foi criada para evitar**.

**Correção — uma das três:**
1. DATADO só recebe peso se houver objetivo, e a duração é casada de fato; sem objetivo, o bloco fica vazio.
2. Falta uma função no modelo. O dinheiro que não é liquidez, não tem data e não é crescimento precisa de nome próprio — algo como `LASTRO` (estabilidade sem data), cuja regra seria *sem marcação a mercado*, e que receberia Tesouro Selic, não IPCA+.
3. Se o IPCA+ deve entrar mesmo sem objetivo, a justificativa (proteção inflacionária de longo prazo, carregado até o vencimento) precisa estar declarada — e aí ele não é DATADO.

A opção 2 é a que preserva a coerência da taxonomia, que é o melhor do arquivo.

### A-05 · O G1 compara custo efetivo da dívida contra retorno **bruto** do investimento

**Estatuto: FATO.**

```python
melhor_am = (1+bruto)**(1/12)-1          # teto otimista: bruto, sem IR
```

O comentário reconhece que é otimista, mas a assimetria tem consequência concreta: a dívida entra com custo efetivo e o investimento com retorno **antes de IR**. Com CDI de 13,90%, o bruto mensal é ~1,09%; líquido de 22,5% na primeira faixa, ~0,84%.

**Toda dívida entre 0,84% e 1,09% ao mês não dispara o portão**, embora seja mais cara que qualquer investimento líquido disponível. Isso é boa parte do consignado e do crédito pessoal de banco grande.

E o teste `test_g1_divida_barata_nao_dispara` usa 0,4% a.m., bem longe da fronteira — **a zona onde o defeito vive não é testada**.

**Correção:** comparar líquido com líquido, usando a alíquota da faixa correspondente ao horizonte da reserva. E acrescentar teste na fronteira: 0,90% a.m. deve disparar.

### A-06 · O gatilho de deriva usa desvio absoluto onde deveria usar déficit

**Estatuto: FATO.**

```python
desvio_max = max((abs(estado.posicoes.get(r,0)/V - pesos.get(r,0)) for r in pesos), default=0)
if capacidade < desvio_max: ...
```

O aporte só compra. Uma rota **acima** do alvo nunca é corrigida por compra, com qualquer capacidade. No cenário [c] do `demo_aporte`, BOVA11 está em ~90% com alvo ~10,5%: desvio de 79,5 p.p., todo ele para cima. O gatilho dispara e o veredito está certo — **mas pelo motivo errado**, e a fórmula daria falso negativo no caso simétrico (déficit grande, excesso pequeno).

**Correção:** o gatilho compara capacidade com o maior **déficit relativo** que o aporte precisa fechar; o excesso é problema do freio de concentração e da deriva estrutural, que são coisas distintas.

---

## 4. Achados de implementação

**B-01 · `valor` e `quantidade` ficam inconsistentes na primeira ordem.**

```python
if restante > 0.01 and ordens:
    ordens[0]["valor"] = round(ordens[0]["valor"]+restante, 2)   # sobra no primeiro
```

A quantidade não é recomputada. A invariante `valor == quantidade * preco` quebra. Não aparece hoje porque `precos=None` faz `p=1.0` em tudo — **o motor nunca foi executado com preço real**. Aparece no primeiro dia em que preços entrarem.

**B-02 · A sobra vai para a primeira ordem, o que contraria o próprio objetivo.** Se o motor minimiza desvio, a sobra deveria ir para o próximo maior déficit ou para caixa. Empurrá-la para a maior ordem aumenta o desvio na direção oposta.

**B-03 · Caixa continua ausente.** É o achado A-08 do laudo consolidado, ainda aberto. Sem posição de caixa, `math.floor` sempre deixa resíduo e não há onde pô-lo. Por isso existe o B-02.

**B-04 · `qtd = math.floor(valor/p) if p > 1 else valor`** — heurística por magnitude do preço. Com preço abaixo de R$ 1,00 (existe na B3) o ramo errado dispara silenciosamente. Use uma flag explícita `negocia_em_lote` na rota.

**B-05 · `assert` como validação de saída.** As linhas 376-381 são o mecanismo que impede o retorno dos 60% em cripto — e `assert` some com `python -O`. Trocar por `raise ValueError`.

**B-06 · `arrasto_anualizado` não é a taxa que parece ser.** Recalculei: para uma rota cujo único custo é 1,30% a.a., a função devolve 0,726% em 5 anos, 0,943% em 25 e 1,048% em 40. O número é o quociente de valores terminais anualizado sobre o horizonte inteiro, enquanto a exposição média de um fluxo mensal é ~metade do horizonte. É **internamente consistente e mal rotulado**: o output imprime "arrasto a.a." ao lado de rotas cuja taxa de administração o leitor conhece, e os dois não são comparáveis. Acrescente uma segunda coluna — custo total como % do aportado — que o `vinte_anos.py` já sabia calcular.

**B-07 · O teto de custo por classe está a milímetros de disparar sem que ninguém tenha notado.** `custo_maximo_classe_aa: 0.010` e HASH11 sai a 0,945% (25 a., R$500) e 0,997% (30 a., R$1.500). No cenário 5 a margem é de 0,003 p.p. Em 31 anos, ou com aporte maior, HASH11 cruza — e aí cai em `baratas or bloco`, volta ao bloco por ser a única rota, e um alerta é emitido. O comportamento final é o mesmo, mas por caminho diferente e sem teste. **Nenhum teste cobre a travessia do limiar.**

**B-08 · `g2_reserva` escolhe a rota de liquidez por ordem alfabética.**

```python
melhor = min(liq, key=lambda r: (r.adm_aa, r.id if r.id!="poupanca" else "zzz"))
```

As três rotas de LIQUIDEZ têm `adm_aa = 0.0`. O desempate cai no `id`: `"rdb_100" < "td_reserva"`, e o RDB vence. **Está certo por acidente.** O critério real — custo líquido, custódia do Tesouro acima de R$ 10 mil, risco de crédito do emissor — foi calculado em detalhe na sua pesquisa de cofrinhos §6 e não é usado aqui. Pior: o alvo do cenário 1 é R$ 27.000 num único RDB, e o teto do FGC por conglomerado (que está no YAML) nunca é consultado.

**B-09 · Sem procedência no output de `alocar`.** `motor_aporte` devolve `politica_versao`; `alocar` não devolve nada. Falta `politica_hash` e `custos_versao`. Sem isso, o princípio P4 (reconstruir por que o sistema decidiu o que decidiu) não se sustenta.

**B-10 · `arrasto_anualizado` roda `anos*12` iterações e é chamado por rota, por cenário, sem cache.** Não é problema hoje; será quando o backtest chamar isto em laço.

---

## 5. Testes

A cobertura é boa e a estrutura está certa. O que falta:

- **Nenhum teste com `precos` preenchido.** O caminho de lote inteiro — que contém B-01 e B-04 — nunca foi exercitado.
- **Nenhum teste da invariante `valor == quantidade × preço`.**
- **`test_exterior_volta_ao_universo_com_aporte_grande` testa outra coisa** (A-02).
- **`test_teto_de_aposta_nunca_e_violado` engole o caso interessante:** `if r["alvo"] is None: assert G2_reserva; continue`. Com `estabilidade_renda="baixa"`, a reserva alvo sobe e o portão dispara — o teste passa sem nunca chegar na alocação. Construa o estado para garantir que chega.
- **Nenhum teste de horizonte.** A dominância (A-01) e o limiar de custo de classe (B-07) só aparecem variando `anos`. Todos os testes usam 25.
- **Nenhum teste de cobertura do YAML** (A-03).
- **Nenhum teste de determinismo:** rodar `alocar` duas vezes deve dar hash idêntico.
- **Nenhum teste na fronteira do G1** (A-05).

---

## 6. O que ficou fora do escopo

Você perguntou. O catálogo tem 20 rotas e cobre Tesouro, RDB/CDB, poupança, ETF de ações BR, IVVB11, ação individual, ETF EUA e HASH11. Fora dele:

### 6.1 Ausências com consequência material

**LCI e LCA.** É a ausência mais difícil de justificar, porque a sua própria pesquisa as elegeu: *"LCI e LCA são cobertas [pelo FGC] — e ainda são isentas de IR. É a combinação mais eficiente da lista para quem fica dentro do limite."* E a §6.2 mostra LCI a 90% do CDI batendo CDB a 100% em todos os prazos. Não estão no catálogo. Encaixariam em LIQUIDEZ (com a ressalva de carência) ou numa função de lastro.

**FII.** Ausente por completo. Está no blueprint original, tem tratamento tributário próprio (20% sobre ganho de capital, sem isenção mensal; rendimento distribuído isento de IR para PF sob condições), a sua pesquisa de corretoras registra que FII é isento de corretagem na Caixa, e o registro consolidado já traz `ir_fii_ganho: 0.20`. É a maior ausência por volume de pesquisa já feita.

**Previdência com contrapartida do empregador.** Se a Volga tem plano com *match*, é retorno imediato de 50% a 100% sobre o aportado — maior que qualquer dívida de cartão. Deveria ser um **G0, antes do G1**. Nenhum portão o considera, e é a única rota que domina o pagamento de dívida.

**PGBL.** Para quem é CLT e faz declaração completa, permite deduzir até 12% da renda bruta tributável. É a única rota do universo com abatimento fiscal **na entrada**, e nenhuma outra tem característica equivalente. A ausência pode ser correta (custo dos fundos costuma comer o benefício), mas precisa ser uma decisão declarada, não uma omissão.

**Cofrinhos e contas remuneradas de fintech.** Você dedicou 898 linhas a isso. O catálogo tem um único `rdb_100` genérico, com `emissor="BANCO_GRANDE"`. As ofertas de 110% a 120% do CDI ficaram fora — e a §6 quantificou a diferença em R$ 58,91 sobre R$ 1.000 em dois anos, com o custo (62 dias sem acesso, caso Master) medido. É a pesquisa mais completa do conjunto sem nenhuma rota correspondente.

### 6.2 Ausências que quebram uma função declarada

**SEGURO_CAUDA tem uma única rota, e ela é eliminada por atrito em todos os cinco cenários.** O bloco sai `0.0%` em todas as saídas registradas, e o teto `seguro_cauda_pct: 0.05` nunca é exercido. Uma função inteira do modelo está morta na prática, e nenhum output diz isso.

Ficaram de fora as rotas que a preencheriam: **ouro** (OZ1D, GOLD11), **dólar** (câmbio direto, ETF cambial) e **bitcoin em custódia própria**. Esta última é conceitualmente relevante: o YAML argumenta bem que cripto vai em APOSTA e não em SEGURO_CAUDA, com base em Choi & Shin — mas esse argumento é sobre o **ativo**. HASH11 é um ETF na B3, com risco jurisdicional idêntico ao resto da carteira; bitcoin em carteira própria não é a mesma rota. A distinção que a taxonomia faz bem para cripto não é feita para a custódia.

### 6.3 Ausências provavelmente corretas, mas não declaradas

- **ETF de renda fixa** (IMAB11, B5P211, IRFM11): taxas já levantadas (0,04%), tributação diferente (tabela regressiva, não 15% fixo), liquidez marcada como lacuna na sua pesquisa.
- **Debêntures incentivadas, CRI, CRA:** isentas de IR e **sem FGC** — a sua pesquisa as chama de "crédito puro".
- **BDR:** seção inteira na pesquisa de ETFs, nenhuma rota.
- **Fundos DI e multimercado:** provavelmente corretos de excluir por custo, mas a exclusão não está escrita.
- **Imóvel, consórcio, COE, previdência sem match:** fora, e não declarados.
- **Opções:** fora, e corretamente — você declarou que não opera.

### 6.4 O padrão

O YAML tem uma seção `portoes` que exclui rotas com critério explícito e auditável. **Não tem seção `fora_de_escopo`.** Uma classe que nunca entrou no catálogo é indistinguível, para quem lê o output, de uma classe que foi avaliada e rejeitada. É o mesmo padrão que o relatório por pesquisa identificou como defeito comum das quatro peças: o status fica onde foi criado e não viaja.

**Correção:** um bloco no YAML, uma linha por classe ausente, com motivo e gatilho de reentrada.

```yaml
fora_de_escopo:
  FII:        {motivo: "sem posição e sem pesquisa de custo por rota", reentra: "quando houver conta em corretora"}
  LCI_LCA:    {motivo: "não catalogado — LACUNA, a pesquisa recomenda", reentra: "prioridade alta"}
  PGBL:       {motivo: "não avaliado; único com dedução na entrada", reentra: "3ª passada"}
  match_empregador: {motivo: "não verificado se existe na empresa", reentra: "G0 — antes do G1"}
  ouro_dolar: {motivo: "SEGURO_CAUDA hoje tem 1 rota, eliminada por atrito", reentra: "prioridade alta"}
  bitcoin_custodia_propria: {motivo: "jurisdicionalmente distinto de HASH11", reentra: "3ª passada"}
  BDR, ETF_RF, debentures, CRI_CRA, fundos, imovel, opcoes: {...}
```

---

## 7. Backlog

**Corrigir antes de usar o resultado:**

1. Dominância robusta a horizonte — testar em 5, 15 e 30 anos; só eliminar se perder em todos. → A-01
2. Reescrever a regra do G3 separando custo fixo de percentual, e corrigir o teste que afirma o contrário. → A-02
3. Resolver DATADO: ou exigir objetivo, ou criar a função de lastro. → A-04
4. G1 comparando líquido com líquido, com teste na fronteira 0,84–1,09% a.m. → A-05
5. Gatilho de deriva sobre déficit, não sobre desvio absoluto. → A-06

**Fechar a lacuna entre YAML e código:**

6. Teste de cobertura do YAML — falha se chave declarada não for lida. → A-03
7. Implementar `custo_maximo_classe_peso`, `por_emissor_credito_privado`, `por_conglomerado`, e verificar `liquidez_dias`/`perda_maxima` contra a função. → A-03
8. `base_anos` para o YAML. → A-03
9. Critério de custo líquido no `g2_reserva`, não ordem alfabética. → B-08

**Implementação:**

10. Recomputar quantidade ao absorver a sobra; ou melhor, criar posição de caixa. → B-01, B-02, B-03
11. `assert` → `raise`. → B-05
12. Segunda coluna no output: custo total como % do aportado. → B-06
13. `politica_hash` e `custos_versao` no retorno de `alocar`. → B-09

**Testes:**

14. Cenário com `precos` reais, e invariante `valor == quantidade × preço`.
15. Varredura de horizonte (5/15/30) em dominância e no limiar de custo de classe.
16. Corrigir `test_teto_de_aposta_nunca_e_violado` para não engolir o caso.

**Escopo:**

17. Bloco `fora_de_escopo` no YAML, com motivo e gatilho por classe. → §6.4
18. Avaliar `match` do empregador como G0. É a única rota que domina o pagamento de dívida, e é uma pergunta de RH, não de pesquisa. → §6.1
19. LCI/LCA e FII na próxima passada — nessa ordem, porque a pesquisa de LCI já está feita e a de FII não.

# Laudo de auditoria — pesquisa de custos e artefatos de cálculo

**Objeto:** `pesquisa-corretoras.md` (905 l.), `pesquisa-cofrinhos.md` (898 l.), `pesquisa-etfs.md` (457 l.), `pesquisa-internacional.md` (1.236 l.), `registro-de-pesquisa.md`, `custos.py`, `vinte_anos.py`.
**Emissão:** 01/09/2026.
**Método:** leitura das quatro peças; conferência dos scripts contra as fontes que eles declaram usar; execução dos scripts; recálculo independente da custódia progressiva da B3. Nenhuma fonte externa foi acessada nesta auditoria — os achados são de consistência interna entre as peças, e são reproduzíveis por leitura.
**Limite:** auditoria de método e de código. Não avalio mérito de investimento e não emito recomendação de alocação, produto ou instituição.

---

## 1. Parecer

> A pesquisa é o melhor artefato da série e a primeira peça do projeto que aplica de fato a doutrina de evidência do manual: fonte primária, data de acesso, status por item, bloqueio registrado como resultado. Os dois scripts, porém, quebram exatamente a regra que a pesquisa impôs — três valores marcados `NÃO CONFIRMADO` nos relatórios entraram no código como constantes, e um deles sustenta a comparação de maior consequência do conjunto. Além disso, dois dos quatro relatórios discordam sobre o mesmo número, e a conclusão de um deles ficou desatualizada porque o arquivo irmão respondeu, com base legal, a pergunta que ele declarou em aberto.

Verificação de escala: as contagens de linhas do registro conferem exatamente com os arquivos (898, 905, 457, 1.236). O registro é honesto sobre o próprio tamanho.

---

## 2. Qualidades — o que preservar sem discussão

Isto vem primeiro porque a maior parte da peça é sólida e algumas decisões aqui devem virar padrão do projeto.

| ID | Qualidade | Por quê |
|---|---|---|
| Q-01 | **Vocabulário de status normalizado** entre quatro frentes: `NÃO CONFIRMADO` / `NÃO OBTIDO` / `PARCIAL` / `COMPLETO`, com motivo técnico obrigatório | É o que torna a peça auditável. Um `NÃO OBTIDO` com Ray ID do Cloudflare é evidência; "não encontrei" não é |
| Q-02 | **Bloqueio registrado como resultado, não como falha** | "Saber que uma instituição não publica seus custos de forma acessível **é** um dado sobre ela." Isso é epistemologia correta, e é a frase mais valiosa do registro |
| Q-03 | **Transcrição literal com aspas** nos pontos que decidem (isenção de R$ 26.471,77; art. 15-B; art. 59 da IN 1.585) | Permite ao terceiro discordar da interpretação sem discutir o fato |
| Q-04 | **Dados descartados por suspeita, com o critério** — a tabela atribuída ao BTG idêntica à da Terra em cinco faixas | Descarte fundamentado é mais raro e mais valioso que coleta |
| Q-05 | **Fontes datadas marcadas** — o "0,99%" do Inter com nota de rodapé de 2022; os spreads do C6 de artigo anterior aos decretos de IOF de 2025 | Distingue dado velho de dado errado |
| Q-06 | **Liquidez de ETF calculada do COTAHIST**, não copiada de agregador | Fonte primária onde quase todo mundo usa terceiro. E revelou o que agregador esconde: ECOO11 sem negócio em 4 de 20 pregões |
| Q-07 | **Consistência aritmética conferida** entre séries independentes: (1+0,1390)^(1/252)−1 = 0,051658% ≈ série 12 (0,051660%) | É exatamente a classe de invariante que o manual pede |
| Q-08 | **Armadilha de leitura documentada** — a IN 1.585 menciona R$ 20 mil no art. 25 §1º em contexto diferente do art. 59, e resumos secundários confundem os dois | Antecipar o erro alheio é trabalho de auditor, não de pesquisador |
| Q-09 | **Gatilhos de reauditoria por elemento**, com cadências distintas (macro a cada uso; %CDI de cofrinho a 30 dias; lista de instituições anual, porque 7 de 25 sumiram em 6 anos) | Reconhece que o dado tem prazo de validade diferente por natureza |
| Q-10 | **Método declarado, inclusive o que não funcionou** — `curl` antes da ferramenta de fetch, com o caso concreto dos 49.524 bytes da B3 | Reprodutível por outra pessoa |

---

## 3. Achados críticos

### K-01 · Três valores `NÃO CONFIRMADO` viraram constantes de cálculo

**Estatuto: FATO. Confiança: forte. É o achado mais grave da peça.**

`pesquisa-internacional.md` §4.1 e §4.4 declaram, com todas as letras:

- taxa de administração do **IVVB11 = 0,23% a.a.** → *"**NÃO CONFIRMADO** — é premissa do pedido"*;
- expense ratio do **IVV / VOO = 0,03% a.a.** → *"**NÃO CONFIRMADO.** A página do iShares não foi aberta"*;
- e `pesquisa-etfs.md`, lacuna 10, acrescenta: taxa do **VTI — NÃO OBTIDA**.

No entanto:

```python
# custos.py
dict(g="ETF na B3",  n="IVVB11 (S&P 500 em BRL)",           adm=0.00230, ...)
dict(g="Exterior",   n="ETF EUA — Avenue melhor degrau",     adm=0.00030, ...)  # e em TODAS as rotas de exterior
# vinte_anos.py
("IVVB11 — corretora zero",                  dict(b3=B3V, adm=0.00230, cust_rv=True)),
("ETF EUA — Avenue melhor degrau (E=1,60%)", dict(entrada=0.0160, adm=0.00030)),
```

O `0,00030` não tem nenhuma fonte confirmada em nenhum dos quatro relatórios, e é a constante que sustenta a comparação de maior consequência do conjunto — se vale a pena pagar 1,60% a 3,10% de entrada para capturar uma diferença anual de taxa. A diferença `Δ` de que depende todo o ponto de equilíbrio de §4.3 é, na origem, um número não lido.

**Atenuante parcial e nova contradição:** o `0,23%` do IVVB11 **está confirmado** — em `pesquisa-etfs.md`, tabela "Internacional listado na B3", com nota de rodapé 7 apontando para a BlackRock. Ou seja, o arquivo internacional o declara não confirmado enquanto o arquivo de ETFs o confirma. Dois relatórios da mesma rodada divergem sobre o mesmo número, e nenhum foi reconciliado.

**Correções, nesta ordem:**
1. Propagar a confirmação do `0,23%` do arquivo de ETFs para o internacional, e corrigir §4.1 e §4.4.
2. Enquanto o expense ratio do IVV/VOO não for lido na fonte, **remover a coluna de taxa das rotas de exterior** dos dois scripts e reportar apenas o custo de entrada, que está confirmado. Um campo vazio é dado; um campo preenchido por premissa não é.
3. Se for necessário produzir a comparação antes da confirmação, rodá-la como **sensibilidade** — `Δ` variando de 0,10 a 0,25 p.p. — e nunca como ponto único.

**Diagnóstico de causa.** O registro estabelece a regra certa e o próprio registro a viola na seção seguinte: *"Constantes extraídas — nenhuma destas deve ser escrita em código"*, e os dois scripts escrevem todas em código. A regra não falhou por descuido; falhou por não ter mecanismo. Ver §5.

### K-02 · A conclusão de `pesquisa-internacional.md` §4.3–4.4 está desatualizada, e na direção que a derruba

**Estatuto: FATO. Confiança: forte.**

O arquivo internacional escreve, em §4.4:

> *"Tributação de ETF de índice no Brasil: **NÃO CONFIRMADO.** Não verifiquei nesta rodada se a isenção mensal de R$ 20.000 em bolsa alcança ou não os ETFs (…) É um ponto **decisivo** para a comparação — porque, se o ETF brasileiro não tem isenção e é tributado a 15% como o estrangeiro, a vantagem tributária da rota doméstica desaparece e sobra só a simplicidade acessória. **Deixo em aberto.**"*

Não está em aberto. `pesquisa-etfs.md` §B.1 fecha a questão com base legal dupla e argumento de lista fechada: Lei 11.033/2004 art. 3º, I (isenta o mercado à vista **de ações**) e IN RFB 1.585/2015 art. 59 (lista fechada — ações, ouro, ações de PME; cota de fundo de índice não está lá). Conclusão transcrita: *"ETF de renda variável paga 15% sobre todo o ganho, desde o primeiro real, sem piso de isenção."* O registro consolidado já incorporou isso no YAML: `isencao_mensal_acao: 20000.00 # SO acao/ouro/PME — ETF e BDR NAO tem`.

Ou seja: a resposta existe, foi obtida na mesma rodada, e é a hipótese que o próprio texto identifica como aquela em que **a vantagem tributária da rota doméstica desaparece**. A seção §4.3 (ponto de equilíbrio) e a §4.4 precisam ser reescritas com esse fato, e o resultado muda de direção.

**Correção:** reconciliar os quatro arquivos antes de qualquer uso. Uma tabela de reconciliação — um item por número que aparece em mais de um relatório, com o status vencedor e o arquivo que o venceu — resolve K-01 e K-02 de uma vez.

### K-03 · A custódia progressiva da B3 está implementada com uma faixa só

**Estatuto: FATO, quantificado por recálculo. Confiança: forte.**

`pesquisa-corretoras.md` §B.4 transcreve a tabela literal da B3, com dez faixas progressivas: 0,0500% até R$ 115 mil, 0,0400% até R$ 230 mil, 0,0200% até R$ 345 mil, 0,0130% até R$ 1,95 mi, e assim por diante. `vinte_anos.py` implementa:

```python
if cust_rv and pat > ISEN_RV:
    base = pat - ISEN_RV
    t = base*((1+CUST_RV)**(1/12)-1)   # CUST_RV = 0,05% — só a faixa 1
```

Como a faixa 1 é a **mais cara** da tabela, o script cobra 0,05% sobre todo o excedente para sempre, quando o real cai a 0,04%, 0,02% e 0,013% conforme o patrimônio cresce. Recalculei com a tabela completa:

| Aporte | Patrimônio final (20 a) | Custo total no script | Custo com a tabela real | Erro |
|---|---:|---:|---:|---:|
| R$ 200/mês | R$ 227.710 | R$ 1.905 | R$ 1.891 | +R$ 14 |
| R$ 500/mês | R$ 568.396 | R$ 5.048 | R$ 4.715 | **+R$ 333** |
| R$ 1.000/mês | R$ 1.135.944 | R$ 10.317 | R$ 8.987 | **+R$ 1.330 (13% a mais)** |

*(cenário BOVA11, adm 0,10%, B3 0,0300%, retorno bruto 13,90% em todas as rotas, conforme o próprio script)*

O erro é **direcional**: superestima o custo das rotas de renda variável e portanto favorece cofrinho e Tesouro na comparação de destaque. Não é ruído, é viés.

**Correção:** função de custódia que percorre as faixas, com a tabela vinda do YAML e não do código. Cinco linhas.

### K-04 · A isenção de custódia é tratada como dedução, e a fonte admite as duas leituras

**Estatuto: INFERÊNCIA. Confiança: moderada.**

O texto da B3 transcrito em §B.4 é: *"Investidores com posições até R$ 26.471,77 são isentos desta taxa."* Isso comporta duas leituras — **limiar de elegibilidade** (acima de R$ 26.471,77 cobra-se progressivamente sobre a carteira inteira) ou **dedução** (cobra-se só sobre o excedente). O script adota a segunda, que é a mais favorável, sem declarar a escolha. A diferença entre as duas interpretações, no cenário de R$ 200/mês, é de cerca de R$ 160 em 20 anos — pequena, mas é uma premissa não declarada num artefato cuja regra é declarar tudo.

Vale notar que a própria pesquisa foi cuidadosa no ponto vizinho: registrou como lacuna que a página da B3 **não diz** se quem paga é o participante ou o investidor final, e listou as instituições que declaram absorver a taxa. Se Itaú, Safra e Caixa absorvem, a linha de custódia pode ser zero na prática — e nenhum dos scripts oferece essa alternativa.

**Correção:** parâmetro `interpretacao_isencao: limiar|deducao` com o default declarado, e um cenário `custodia_absorvida_pela_instituicao: true`.

### K-05 · A Tabela 2 esconde a taxa de administração, e o resultado é enganoso

**Estatuto: FATO. Confiança: forte.**

`entrada_pct()` soma corretagem, B3 e entrada — não inclui `adm`. A Tabela 2 ("quantos meses de rendimento o custo de entrada consome") portanto imprime, para o aporte de R$ 1.000:

```
SMAL11                     0.0m     0.0m     0.0m     (adm 0,50% a.a.)
HASH11 (cripto)            0.0m     0.0m     0.0m     (adm 1,30% a.a.)
```

O título da tabela é tecnicamente correto — é custo *de entrada*. Mas um leitor que percorre a coluna vê HASH11 e PIBB11 empatados em zero, quando a diferença anual entre eles é de 1,24 p.p. — a maior do conjunto de ETFs. A informação existe no dicionário e nunca chega à tela.

**Correção:** acrescentar coluna de `adm a.a.` à Tabela 2, ou uma terceira tabela de custo total no primeiro ano. O dado já está estruturado; falta imprimir.

### K-06 · Só a perna de entrada é modelada

**Estatuto: FATO. Confiança: forte.**

Três omissões simétricas:

1. **Corretagem de saída.** A rota "BOVA11 — XP" tem nota `"0,50% na entrada E na saida"`, e o cálculo conta uma vez. Ida e volta é 1,00%, não 0,50%.
2. **B3 na venda.** §B.6 é explícito: *"Na venda, cobra-se de novo o mesmo percentual."* Não modelado.
3. **Repatriação.** O registro traz `iof_repatriacao: 0.0038` (art. 15-B, XXV) e a tabela mestre do internacional traz "0,38% volta" para Avenue, Nomad e Vest. Nenhuma rota de exterior contabiliza a volta, nem o spread cambial de retorno.

**Correção:** separar `custo_entrada` de `custo_saida` na estrutura, e uma terceira tabela de ida e volta. Para o exterior a assimetria importa: a rota é escolhida na entrada e o custo de saída só aparece anos depois.

### K-07 · O status da pesquisa não é propagado para o artefato de cálculo

**Estatuto: FATO. Confiança: forte.**

O vocabulário Q-01 morre na fronteira do `.py`. Três exemplos, todos na mesma tabela e visualmente indistinguíveis:

- `"XP swing trade (R$ 4,90 por ordem)"` com `nota="leitura PARCIAL — confirmar"` — imprime como qualquer linha confirmada;
- `"Vest stablecoin (1,40%, sem IOF declarado)"` — aparece como a rota de exterior **mais barata da tabela** (1,3 meses de CDI contra 1,5 da Avenue). Mas "sem IOF declarado" é uma posição jurídica da plataforma sobre remessa via stablecoin, não um fato tributário confirmado; a própria pesquisa classifica a Vest como *"(a), com ressalva"*. Se o IOF de 1,10% se aplicar, a rota vai a 2,50% e passa a ser pior que a Avenue. **Um `NÃO CONFIRMADO` está sendo renderizado como zero, e inverte a ordenação.**
- As rotas de exterior com `adm=0.00030`, conforme K-01.

**Correção:** campo `status` obrigatório em cada rota (`COMPLETO|PARCIAL|NAO_CONFIRMADO`), marcador visível na impressão (`†`, `⚠`), e uma regra dura: rota com qualquer insumo `NAO_CONFIRMADO` **não entra na ordenação** — imprime separada, abaixo da linha.

### K-08 · Premissas de modelagem não declaradas em `vinte_anos.py`

**Estatuto: INFERÊNCIA. Confiança: forte.** Três, todas pequenas isoladamente e todas na mesma direção.

1. **Timing do aporte.** `pat += liq; pat *= (1+m_bruto)` — o aporte rende o mês inteiro em que entra (regime de anuidade antecipada). Sobre 240 meses isso infla o patrimônio absoluto frente a uma convenção de meio de mês. Como se aplica igualmente a todas as rotas e à referência, as **diferenças** ficam corretas; os valores absolutos, não.
2. **Base da taxa de administração.** Cobrada sobre o saldo de fim de mês, já com o aporte fresco e com o rendimento do mês. A taxa real é embutida na cota diariamente, ou seja, incide sobre saldo médio. Superestima levemente.
3. **`c = min(c, aporte)`.** Cobertura silenciosa do caso em que o custo excede o aporte. Deveria emitir alerta: se acontecer, a rota é inviável naquele tamanho de aporte, e essa é a conclusão, não um detalhe a suprimir.

Contraste com o que está bem feito: a escolha de **retorno bruto idêntico em todas as rotas** está declarada no docstring com a justificativa certa (*"o objetivo é isolar o CUSTO, não prever retorno"*). Isso é metodologicamente correto e deve ser preservado. O risco é de leitura: a coluna "Patrimônio" sai em reais e parece projeção. Renomear para `Patrimônio (cenário de custo, não projeção)` resolve.

### K-09 · Fronteira de escopo divergente entre peças: o IR

**Estatuto: FATO. Confiança: forte.**

`vinte_anos.py` não modela imposto de renda. Isso é defensável — o objeto declarado é custo, e IR não é custo. Mas `pesquisa-cofrinhos.md` §6 produz uma comparação **líquida de IR** para R$ 1.000, e `pesquisa-etfs.md` §B.1 estabelece que ETF paga 15% desde o primeiro real, sem a isenção de R$ 20 mil que a ação individual tem.

O resultado é que a tabela de 20 anos coloca lado a lado "Cofrinho / RDB 100% CDI", "PIBB11" e "Ação — corretora zero", cujos tratamentos tributários são materialmente diferentes, sob um cabeçalho que não menciona a omissão. Um leitor comparando as colunas vai comparar coisas que não são comparáveis.

**Correção:** uma linha no cabeçalho — *"Não inclui IR. Os tratamentos diferem: RF regressiva 22,5→15%; ETF 15% sem isenção; ação 15% com isenção de R$ 20 mil/mês na venda."* Não precisa modelar; precisa declarar.

### K-10 · `meses_para_pagar` usa CDI para rotas de renda variável

**Estatuto: FATO. Confiança: forte, severidade baixa.**

A função aceita `taxa_aa` e o chamador nunca o passa, então BOVA11, SMAL11, HASH11 e ETF americano são todos medidos contra 13,90%. Como régua uniforme é defensável, e o cabeçalho da tabela declara a taxa. Mas o rótulo da coluna diz "meses de rendimento", o que sugere rendimento do ativo. **Correção:** renomear para "meses de CDI equivalente".

### K-11 · Defeitos de engenharia

**Estatuto: FATO. Todos verificados por execução.**

| # | Defeito | Evidência |
|---|---|---|
| a | `custos.py` **quebra na execução** — `FileNotFoundError: '/tmp/bastter/calc/tabela_entrada.json'`. Imprime as tabelas e morre no `json.dump` | Rodado nesta auditoria |
| b | Caminho absoluto em `/tmp`, fora da árvore do repositório e volátil | Contraria a estrutura do manual (§3) |
| c | Constantes **duplicadas** entre os dois arquivos com nomes diferentes: `B3_VISTA`/`B3V`, `B3_CUST_RV_ISEN`/`ISEN_RV`, `TD_CUSTODIA`/`TD_C`. Vão divergir | Leitura |
| d | Constantes **em código**, contra a regra explícita do próprio registro | Leitura |
| e | Nenhum teste. Nenhuma invariante. Nenhum `if __name__ == "__main__"` | Leitura |
| f | Sem procedência por valor: nenhuma constante carrega fonte nem data | Leitura |
| g | `json.dump` sem `os.makedirs`, sem context manager, arquivo não fechado | Leitura |

---

## 4. Riscos

| ID | Risco | Prob. | Impacto |
|---|---|---|---|
| R-01 | **Cristalização de premissa.** O `0,03%` entrou como premissa do pedido, foi marcado NÃO CONFIRMADO no relatório, e reapareceu como constante em dois scripts. No terceiro salto ninguém lembra da origem | Alta | Alto |
| R-02 | **Decaimento silencioso.** O registro diz que macro deve ser reconferido "a cada uso" e que %CDI de cofrinho expira em 30 dias. Nada no código verifica data. Um script que roda em 2027 com CDI de agosto/2026 não reclama | Alta | Médio |
| R-03 | **Divergência entre os quatro arquivos.** Já ocorreu duas vezes (K-01, K-02) numa única rodada. Sem tabela de reconciliação, recorre | Alta | Alto |
| R-04 | **Ordenação invertida por dado não confirmado.** Caso Vest (K-07): a rota mais barata da tabela é a única cujo componente principal não foi confirmado | Média | Alto |
| R-05 | **Escopo se expandindo.** Esta pesquisa é insumo da camada de alocação, que o laudo Rev. 03 colocou fora do escopo atual. 3.496 linhas sobre custos de rotas que ainda não serão usadas | Média | Médio |

Sobre R-05, sem julgamento: se o objetivo é aprendizado e a pesquisa foi o veículo, ela se pagou — o método aqui é melhor que o do dossiê original. Mas ela não avança nenhuma das cinco entregas da §7 do laudo, e o risco R-01 daquele laudo (o artefato substituindo a ação) continua o de maior probabilidade do projeto.

---

## 5. Integração no repositório

O registro já acerta o destino (`docs/fontes/custos-2026-08/`). Falta o mecanismo que impede K-01 de repetir.

**5.1 · Toda constante carrega procedência.** Não basta tirar do código: o YAML precisa de status e data por valor, não só por bloco.

```yaml
b3_vista_total_pct:
  valor: 0.000300
  status: COMPLETO
  fonte: "b3.com.br/.../a-vista/"
  acesso: 2026-08-31
  expira: 2026-11-29          # 90 dias, conforme gatilho do registro
  nota: "ADTV < R$3mi; PIS/COFINS/ISS inclusos"

etf_eua_expense_ratio:
  valor: null                  # NÃO preencher com 0.0003
  status: NAO_CONFIRMADO
  motivo: "página do iShares não aberta — internacional §4.4"
  bloqueia: ["comparacao_ivvb11_vs_etf_eua"]
```

O campo `bloqueia` é o que fecha o buraco: um cálculo que depende de valor `NAO_CONFIRMADO` recusa-se a rodar, em vez de rodar com premissa.

**5.2 · Testes que esta peça pede.** Encaixam nas camadas do manual:

- *Contrato* — bater Selic, CDI e poupança contra a API do BCB e falhar se divergirem do YAML. Uma linha de `curl`, roda diário.
- *Invariante* — `(1+CDI_aa)^(1/252) − 1 ≈ CDI_diario` dentro de tolerância. A pesquisa já fez essa conferência à mão; automatize.
- *Invariante* — soma das faixas progressivas de custódia é monotônica e nenhuma faixa é maior que a anterior. Teria pego K-03.
- *Invariante* — nenhuma rota entra em tabela ordenada com insumo `NAO_CONFIRMADO`. Teria pego K-07.
- *Invariante* — `hoje > expira` em qualquer constante usada ⇒ falha com a data. Cobre R-02.
- *Unitário* — custódia progressiva contra três pontos calculados à mão (R$ 100 mil, R$ 300 mil, R$ 1,2 mi).

**5.3 · Tabela de reconciliação.** Um arquivo, uma linha por número que aparece em mais de um relatório: valor, status em cada arquivo, status vencedor, arquivo que venceu, data. Resolve K-01 e K-02 e impede R-03.

**5.4 · Ordem sugerida.** (1) Reconciliação — meia hora, e derruba a conclusão de §4.3, que é o resultado de maior consequência da peça. (2) Constantes para YAML com procedência. (3) Corrigir K-03, K-05, K-06, K-11a. (4) Testes. (5) Só então reabrir as lacunas da 3ª passada.

Uma observação sobre a lacuna 9 do registro (spread de RF, rebate de fundos, float — *"nenhuma instituição publica"*): marcá-la como **não fechável** foi a decisão certa. Vale registrar por quê, porque é o achado mais interessante do conjunto — a parte do custo que ninguém publica é, provavelmente, a maior. Isso é conclusão sobre o mercado, não sobre a pesquisa.

---

## 6. Pendências

**Fechadas por esta auditoria:** a custódia progressiva foi recalculada e o erro está quantificado (K-03); os scripts foram executados e o defeito de caminho está confirmado (K-11a); as contagens de linha do registro conferem.

**Abertas — só o auditor humano fecha:**

| # | Item | Sustenta |
|---|---|---|
| 1 | Expense ratio de IVV / VOO / VTI na fonte primária | K-01; sem ele, a comparação internacional não roda |
| 2 | IOF na remessa via stablecoin (rota Vest) — posição da plataforma ou tratamento tributário confirmado? | K-07, R-04 |
| 3 | Interpretação da isenção de custódia: limiar ou dedução? | K-04 |
| 4 | Quem paga a custódia da B3 — participante ou investidor final? Já registrado como lacuna em §B.4 | K-04 |
| 5 | `OC 014-2024-VPC` — periodicidade real da cobrança do Tesouro Direto (B3 diz provisão diária, Safra diz semestral) | Precisão do modelo de 20 anos |
| 6 | Reconciliar `pesquisa-internacional.md` §4.1/§4.3/§4.4 com `pesquisa-etfs.md` §B.1 e com a taxa confirmada do IVVB11 | K-01, K-02 |

**Não fechável, e assim deve permanecer registrado:** spread de renda fixa, rebate de fundos e float. Nenhuma instituição publica.

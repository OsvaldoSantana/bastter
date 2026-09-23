# Análise das três pesquisas sobre APIs para "robô de investimentos" — 23/09/2026

*Pedido dele: três IAs pesquisaram fontes de dados, APIs e arquitetura para um robô de
investimentos; ele quer a análise contra o projeto. Status: `ESPECIFICACAO` — nada aqui foi
executado. Os preços, limites e nomes de fornecedores são **dos relatórios**, não conferidos
nesta análise (P5); nenhuma conclusão abaixo depende deles.*

---

## 1. O veredito em uma linha

**As três pesquisas descrevem outro produto.** Elas desenham um robô que **opera** — lê
cotação em tempo real, gera sinal e envia ordem. O Bastter é um sistema que **decide o aporte
do mês** e o usuário executa: horizonte mensal, portões antes de peso, ML só como ordenação
(D-ML1), e o sistema **recomenda**, nunca ordena (D-ML3). A frase mais correta das três está
na segunda: *"a escolha das APIs deveria acontecer depois da definição da estratégia"*. A
estratégia daqui está definida, e ela precisa de pouco dado — mas dado certo, datado e com
procedência.

## 2. O que as pesquisas acertam — e o projeto já faz, em geral melhor

| o que a pesquisa recomenda | onde isso já está no projeto |
|---|---|
| COTAHIST é bruto: "sem ajuste por inflação ou proventos" | citado da B3 em `docs/fontes/`; o ajuste é o `ajustar.py`, **medido** (C-02, 632 mil pares de controle) em vez de confiado a um `adjusted_close` de terceiro |
| CVM (DFP/ITR) como fonte primária de fundamentos | acervo semanal desde 18/09, com manifesto e sha256 |
| BCB SGS para macro Brasil | constantes macro com procedência e `expira` |
| ANBIMA para renda fixa | P-52, com o prazo registrado |
| *point-in-time*: usar só o que estava disponível na data | `DT_RECEB` ≤ data de decisão, com `InsumoBloqueado` (pré-registro ML §2) |
| *provenance* em cada dado | P1 — é a doutrina número um da casa; `origem.csv`, `dt_captura`, `trecho_conferido` |
| identidade do ativo (ISIN, código da empresa) | `codeCVM` e não ticker (A-03); ISIN no COTAHIST |
| licenciamento: não redistribuir dado | o repositório é **público**; `data/` fora do git e o portão da P-98 medem bytes no índice — a guarda de tamanho é, também, a guarda de redistribuição |

A espinha dorsal que a segunda pesquisa propõe para *"B3 + fundamentalista + histórico + ML"*
— COTAHIST, CVM, BCB, ANBIMA — **é o acervo que já existe**. O que ela chama de "camada de
normalização" e "feature store" é o que o projeto chama de bronze → silver e base PIT (ML-3).

## 3. O que não serve, e por quê

| recomendação | por que fica fora |
|---|---|
| WebSockets, Kafka/Redpanda, Redis, TimescaleDB/ClickHouse | resolvem latência e volume de eventos. Uma decisão por mês não tem nenhum dos dois problemas. Seria custo de operação sem ganho de decisão |
| execução automática (IBKR, Alpaca, MT5, DMA/PUMALink) | uma ordem por mês, executada por ele. Automatizar acrescenta o modo de falha mais caro que existe — a ordem errada enviada sem ninguém olhar — para economizar dois minutos. E contradiz D-ML3 |
| notícias e sentimento (Benzinga, LSEG, NewsAPI, "Economatica MCP") | alvo mensal; e o plano de ML já proíbe modelo de linguagem em backtest (§3.11: só para frente) |
| cripto, opções, forex, *Pattern Day Trader* | fora do universo |
| brapi, bolsai, EODHD, FMP como **fonte** de preço/fundamento da B3 | são agregadores do mesmo COTAHIST e da mesma CVM que o projeto lê na origem. Trocar a fonte primária pela secundária **rebaixa** a procedência (P1) e acrescenta um intermediário que ninguém audita |
| MetaTrader como "padrão da indústria no Brasil" | é para day trade de varejo |

Sobre regulação (a segunda pesquisa cita CVM 19, 21 e 35): o enquadramento muda se o sistema
**recomendar ou executar para terceiros**. Para a carteira dele, não se aplica. Vale só como
cerca: se um dia o sistema servir outra pessoa, a leitura dessas normas vem antes do código.

## 4. O que vale aproveitar — três ideias, em ordem de valor

**(a) Uma fonte secundária como CONTROLE, não como feed.** O projeto valida o ajuste de preço
contra ele mesmo: todo o C-02 é interno. O melhor instrumento desta semana — o que pegou o
A-13 — foi justamente **duas fontes independentes comparadas** (o preço de véspera da B3
contra o fechamento do COTAHIST). Um fornecedor externo de preço ajustado (qualquer um dos
agregadores, no plano gratuito) serviria de **oráculo externo** para uma amostra: mesmo
papel, mesmo período, medir a divergência entre a série do `ajustar.py` e a dele. Onde
divergir, um dos dois está errado, e o achado sai de lá. Precisa de pré-registro (P-116):
o critério de "concordam" escrito e empurrado antes de olhar.

**(b) Open Finance para o dado que hoje depende dele.** O aporte realizado e as posições
(P-02, `DADO_DE_UM_USUARIO`) são o único insumo em que ele está no caminho crítico todo mês
(U-01, P7). A terceira pesquisa cita agregadores de Open Finance com conectores para
corretoras brasileiras. **`NAO_CONFIRMADO`**: não li a documentação, não sei cobertura,
custo nem o que fica guardado com o terceiro — e é o dado mais sensível do projeto, o mesmo
que o `estado.yaml` protege ficando fora do git. É candidato a pesquisa, não a integração.

**(c) Macro com vintage.** A primeira e a segunda citam o ALFRED (o FRED com as versões
publicadas em cada data). O BCB SGS não guarda versões: uma série revisada substitui a
antiga. Hoje não morde — o pré-registro de ML não usa macro como variável. Morde no dia em
que usar, e o registro é uma linha em `limitacoes_declaradas`, como `FISICA` (a fonte não
publica as versões).

## 5. Onde as pesquisas erram ou exageram

- **"Ter a API certa" como problema central.** As três tratam a escolha do fornecedor como a
  decisão de arquitetura. A segunda chega perto do certo no fim (*"qual era o preço, qual
  era o fundamento… realmente disponíveis naquele instante?"*), mas o que responde isso é o
  **manifesto datado de um acervo próprio**, e não um fornecedor melhor.
- **Nenhuma menciona pré-registro, multiplicidade ou controle.** A arquitetura tem "motor de
  estratégia" e "gerenciador de risco", e nenhum lugar onde se prova que a estratégia
  funciona antes de ligá-la. É exatamente a camada em que o projeto investiu (C1 do plano de
  ML, `multiplicidade.py`, P-88).
- **"Ajuste retroativo por dividendos via `adjusted_close`"** é apresentado como caixa-preta
  confiável. O C-02 mostrou que a caixa tem de ser aberta: o dividendo tira do preço 1,16× o
  valor pago, e o mesmo provento chega por duas portas (A-13). Um `adjusted_close` de
  terceiro esconde as duas coisas.

## 6. O que entra no projeto por causa disto

Nada de código novo. Três registros, que ele decide:

1. candidata a pendência — **oráculo externo do preço ajustado** (ideia 4a), com critério
   pré-registrado;
2. candidata a pesquisa — **Open Finance para posições e aporte** (4b), com a pergunta de
   privacidade respondida antes da técnica;
3. linha em `limitacoes_declaradas` — **macro sem vintage**, `FISICA`, quando a macro virar
   variável (4c).

# Revisão do planejamento — onde estamos

**04/09/2026 · política 1.8.0 · 133 testes passando**

---

## 1. O plano original, e o que aconteceu com ele

O blueprint de 31/08 previa oito camadas. Cinco existem, uma foi criada fora do plano,
duas não começaram — e a razão de duas não terem começado **não é falta de tempo**.

| # | Camada | Estado | Observação |
|---|---|---|---|
| 0 | **Pipeline de dados** (CVM DFP/ITR, COTAHIST, bitemporalidade) | **NÃO INICIADA** | É a maior peça restante. Alimenta os catálogos de análise e o backtest |
| 1 | **Motor de custo** (`motor.py`, `custos.yaml`) | **COMPLETA** | Procedência por valor; 12 testes; auditada e corrigida (K-01 a K-11) |
| 2 | **Portões e elegibilidade** (`alocacao.py`, G1–G8) | **COMPLETA** | 9 portões, todos com regra declarada no YAML |
| 3 | **Alocação alvo** | **COMPLETA** | Funções de risco; 1/N; tetos como máximo absoluto |
| 4 | **Custo de discordar** | **COMPLETA** | Mostra o preço da divergência sem impedir |
| 5 | **Motor de aporte** | **COMPLETA, ociosa** | Roda; não tem o que fazer até a reserva fechar (mês 42) |
| 6 | **Catálogo de campos de análise** (blocos A–M) | **ESPECIFICADA, não construída** | Depende inteiramente da Fase 0 |
| 7 | **Backtest com pré-registro** | **PRÉ-REGISTRADO, não executado** | 9 estratégias com ordem de execução; benchmark NEFIN pronto |
| — | **Fatores de risco** (`fatores.py`) | **COMPLETA — fora do plano** | Não estava no blueprint. Virou possível quando você trouxe a série do NEFIN |
| — | **Fase de reserva** (`reserva.py`, `aporte.py`) | **COMPLETA — fora do plano** | Não estava no blueprint porque o blueprint não sabia que esta seria a única fase ativa por 42 meses |

**O achado da revisão:** as duas camadas fora do plano são as duas que mais mudaram
decisões. O blueprint foi escrito sem conhecer o estado financeiro real do usuário, e
por isso otimizou a parte do sistema que só será usada em 2030.

---

## 2. As três fases reais, e em qual estamos

O plano falava em camadas de software. A vida tem fases, e elas não coincidem.

### Fase A — formar a reserva · **ESTAMOS AQUI** · até ~mês 42 (mar/2030)

O que o sistema decide: **uma coisa só** — onde guardar a reserva. O G2 dirige 100% do
aporte, e as camadas 2 a 5 não têm o que fazer.

- reserva hoje: R$ 7.667,91 · 1,9 mês de despesa
- alvo: R$ 36.000 (9 meses, estabilidade baixa medida em 6 pontos de 6)
- piso de aporte: R$ 500 · realizado hoje: **zero**

**O que ainda vale construir nesta fase:** a Fase 0 do pipeline, o catálogo de campos e
o backtest — porque nenhum deles depende de ter dinheiro investido, e todos levam meses.
Construir agora é usar os 42 meses, não esperá-los.

### Fase B — primeiro aporte investido · a partir da reserva completa

O que destrava: motor de aporte com posições reais, freio de concentração, deriva
estrutural. Todo o código já existe e está testado.

**O que precisa estar pronto antes:** conta aberta (ranking entregue), e a decisão A-05
— núcleo indexado ou seleção ativa — que só o backtest resolve.

### Fase C — carteira em regime · a partir de ~R$ 26 mil investidos

O que muda: a custódia da B3 passa a incidir, o teto do FGC começa a importar, e o
rebalanceamento por compra começa a perder eficácia (gatilho de deriva).

---

## 3. O que mudou de premissa desde o blueprint

Sete correções, todas com o dado que as motivou:

| Premissa original | O que se verificou | Efeito |
|---|---|---|
| Horizonte 25 anos | **10 anos** — era premissa minha, não sua | Fração de RV cai; coincide com o teto de compromissos |
| Estabilidade média | **Baixa**, 6 pontos de 6 (contrato único, sem aviso prévio) | Reserva-alvo de R$ 24 mil → R$ 36 mil |
| Aporte é escalar | **Piso + extraordinário**, com regra própria | Data da reserva vira faixa; G3 avaliado sobre o valor do mês |
| Previdência com match a verificar | **Não existe** — PJ sem previdência | G0 desligado; PGBL reavaliado (base tributável pequena) |
| "Valor não paga no Brasil" (HML 0,05%/mês) | **HML paga 0,688%/mês, t = 2,60** na série primária | Pré-registro corrigido antes de rodar |
| Prêmio de ações como dado | **0,96% a.a., t = 0,74** — não distinguível de zero | A fração em RV vira aposta declarada, com preço medido |
| Corretora: 8 empatadas, sem critério | **Itaú vence em 9 de 9 configurações de peso** | Ranking derivado, com teste de robustez |

---

## 4. O que fazer a seguir, em ordem de valor

**1. Fase 0 do pipeline — CVM DFP/ITR com bitemporalidade.**
É a maior peça restante e a única que não pode ser apressada depois: `dt_disponivel`
não pode ser reconstruído retroativamente, porque a CVM sobrescreve os arquivos anuais.
Cada mês sem ingestão é um mês de histórico que não existirá.

**2. As três hipóteses nulas do backtest.**
`hml_puro`, `dy_alto` e `tamanho_smb` — rodam contra os fatores do NEFIN, que já estão
em disco e testados. Duas devem falhar; se qualquer uma "funcionar", o defeito é meu.
Não dependem da Fase 0: são fatores prontos.

**3. Bloco C do catálogo — solvência.**
É o bloco de exclusão, o único com lógica que não exige prêmio de risco existir. E é o
que sua crítica sobre Bessembinder aponta como o teste que importa.

**4. Pendência 20 — regime de análise para instituições financeiras.**
Aberta desde o primeiro laudo. Sem ela, banco não pode ser analisado — e bancos são
metade do Ibovespa.

**5. LCI/LCA no catálogo de rotas.**
Isentas de IR e cobertas pelo FGC. A pesquisa já está feita; falta virar rota.

---

## 5. O que continua bloqueado por você

Duas coisas, e nenhuma é urgente hoje:

- **Tese do HASH11** (K-02, K-03, K-04) e **compromisso do IPCA+** (C-02 a C-06). Sem
  eles os dois ativos ficam em zero. Só passam a importar na Fase B.
- **O aporte realizado.** R$ 500 é o piso planejado; o realizado é zero. É o único
  número do projeto que nenhuma linha de código substitui.

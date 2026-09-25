# Auditoria do `preregistro-ml-v1.md` — antes do commit, que é quando ele ainda pode mudar

**21/09/2026.** Lidos inteiros: `preregistro-ml-v1.md` e `pesquisa-e-plano-ml-1.md`, do projeto
Bastter no claude.ai. Medições sobre a série do NEFIN (`hash_fonte 619991c2192c`) com o
instrumento da P-88.

---

## 0. Primeiro, uma retratação minha — e ela veio deste documento

Em 19/09, auditando três planos de otimização de token (`docs/auditoria/AUDITORIA-PLANO-DE-TOKENS.md`
§4.5), eu recusei a proposta de *feature store* e aprendizado de máquina escrevendo:

> *"Feature store para ML não é otimização de token — é mudança de escopo, **e o escopo tem
> evidência contra**. `CLAUDE.md` §1: 'Não é um otimizador. DeMiguel, Garlappi & Uppal (2009)'."*

**A segunda metade está errada.** DeMiguel, Garlappi e Uppal medem **otimização de pesos** —
14 modelos de média-variância contra 1/N. Não dizem nada sobre **ordenar** ativos. O plano de ML
resolve isso na primeira página, e melhor do que eu teria resolvido:

> *"o aprendizado de máquina **não define pesos**. O modelo responde **qual primeiro**, nunca
> **quanto**."* — `pesquisa-e-plano-ml-1.md` §1

**É a régua §5-B.5, a do JCP:** a cláusula que eu citei **não cobre o item de que eu estava
falando**. Usei a autoridade de uma fonte primária contra uma proposta que ela não alcança.

**O que sobrevive da minha recusa:** que um plano de custo de token não é a porta para mudar
escopo. E o escopo não entrou por ela — entrou por um pré-registro próprio, com família,
orçamento e critério de veredito. **A preocupação foi atendida por ele, do jeito certo.**

---

## 1. O que o pré-registro faz bem — e é muito

Não é elogio de cortesia; é o que torna os achados abaixo pequenos em vez de fatais:

- **Família separada com `m` duplo** (11 e 24), e divergência entre os dois **bloqueia** — a
  decisão 4 de 13/09 aplicada à família nova.
- **O teste roda uma vez**, com hiperparâmetros congelados em dez/2019. É a trava mais forte que
  existe, e é a que a evidência de `PREREGISTRO-EVIDENCIA.md` diz que funciona.
- **Oito testes antes de dado real** — sinal plantado, ruído puro, canário de vazamento com
  prova por mutação, rótulos embaralhados, determinismo. Isso é a §5-B.4 transformada em
  requisito de entrada.
- **Ausente fica ausente**, e **preço médio nunca vira sinal** (D-ML7) — os dois F-02 mais
  tentadores deste domínio, fechados antes de existirem.
- **Os valores de O'Brien-Fleming estão certos** (z ≈ 4,56 · 3,23 · 2,63 · 2,28 · 2,04 para
  cinco análises, α = 5% bilateral) **e estão marcados `NAO_CONFIRMADO` mesmo assim**, com o
  módulo recalculando. É a postura certa com número de memória.
- **Modelo de linguagem só para frente** (§3.11 do plano). É o vazamento mais sutil do campo e
  ele está nomeado.

---

## 2. O achado que importa: `L = 3` foi herdado de uma amostra quatro vezes maior

**§6 do pré-registro:** *"bootstrap em blocos com `L = 3`, dentro da faixa informativa medida na
P-88 (L = 2 a 8)"*.

**A faixa L = 2 a 8 foi medida com n = 306 meses.** O critério que a define é aritmético —
**≥ 39 blocos distintos por replicação** — e depende de `n`. O teste do ML é **jan/2020 a
ago/2026: 80 meses.**

| n | L = 2 | L = 3 | L = 6 |
|---|---|---|---|
| 306 (P-88) | 153 blocos | 102 | 51 |
| **80 (teste do ML)** | **40** | **27** | **14** |

Com n = 80, **`L = 3` dá 27 blocos — abaixo do limiar, e perto dos 26 que o `L = 12` da P-88
dava, que era degenerado.**

### Medido, com o mesmo controle da P-88

Últimos 80 meses da série (nov/2019 a jun/2026), m = 24 (o conservador do pré-registro),
10.000 repetições, 4 sementes:

| L | blocos | HML (tem dependência) | vs iid | **SMB (controle, só degeneração)** | vs iid |
|---|---|---|---|---|---|
| 1 | 80 | 3,1045 | — | 4,1399 | — |
| 2 | 40 | 3,4475 | +11,0% | 3,7644 | **−9,1%** |
| **3** | **27** | 3,4598 | +11,4% | 3,6704 | **−11,3%** |
| 4 | 20 | 3,3464 | +7,8% | 3,6189 | −12,6% |
| 6 | 14 | 3,2803 | +5,7% | 3,4388 | −16,9% |

**Com n = 306, o controle perdia −2,6% em L = 2. Com n = 80, perde −9,1% em L = 2 e −11,3% em
L = 3.** A degeneração, que na P-88 só aparecia em L ≥ 12, aqui começa no primeiro passo.

### Por que isso é grave num pré-registro, e em que direção

A degeneração **abaixa o corte**. Se a série de IC do modelo tiver pouca dependência serial —
e não há como saber antes de ela existir —, `L = 3` entrega um corte **~11% menor** que o iid.
**Isso é anti-conservador: aumenta a chance de rejeitar a nula por acaso**, que é exatamente o
que o pré-registro existe para impedir.

> **É a régua §5-B.5 contra o próprio documento, e é a mesma forma da minha retratação acima:**
> a P-88 foi citada com correção, e o alcance dela não cobre o caso. **O número estava certo; a
> amostra era outra.**

### O que eu recomendo, e ele não exige escolher L

**Corte operativo = o MAIOR entre `L ∈ {1, 2, 3}`.** Três razões:

1. **cobre as duas direções:** se houver dependência, o L maior sobe o corte e o máximo o pega;
   se não houver, o L = 1 é o maior e o máximo o pega;
2. **não depende de ver o dado de teste** — é regra fixada antes;
3. **é a mesma lógica da decisão 4:** entre duas leituras que podem divergir, o operativo é o
   mais conservador.

**O custo é poder**, e ele precisa ser declarado — que é o próximo achado.

---

## 3. Falta a análise de poder, e com n = 80 e m = 24 ela decide se o teste pode rejeitar

O veredito é sobre o **IC médio mensal**. Com n = 80:

```
rejeita  ⟺   IC_médio  ≥  c × sd_IC / √80   =   c × 0,1118 × sd_IC
```

| corte `c` | IC médio mínimo, em desvios do IC mensal |
|---|---|
| 2,5 | 0,28 × sd |
| **3,1** (HML iid, medido acima) | **0,35 × sd** |
| 3,5 | 0,39 × sd |
| **4,1** (SMB iid, medido acima) | **0,46 × sd** |

**O IC médio precisa ser de um terço a metade do desvio mensal dele.** Se isso é alcançável
depende do `sd_IC` real, que **não existe ainda** — e eu não vou chutar um valor de literatura:
seria número sem procedência entrando no documento que existe para impedir isso.

> **O risco não é o teste errar: é o teste ser incapaz de acertar.** Um pré-registro com poder
> baixo quase sempre termina em "não rejeita" — e esse resultado seria lido como *"o modelo não
> funciona"* quando o correto seria *"o teste não tinha como ver"*. São conclusões opostas com a
> mesma saída.

**Recomendação:** acrescentar à §8 um nono teste — **poder com sinal plantado**: o IC mínimo que
o pipeline detecta a m = 24 com n = 80, com a regra de corte da §2 acima. Ele roda na ML-1, só com
dado sintético, antes de qualquer dado real, e **o número vai para o relatório final ao lado do
veredito**. Se o poder for baixo, isso é `NAO_CONFIRMADO` por desenho, dito antes.

---

## 4. Quatro achados menores, em ordem de custo

**(a) O pré-registro ainda não vale — e isso é uma oportunidade, não um problema.** Ele diz:
*"Vale a partir do commit que o contém; a data do commit é a prova."* **Ele não foi commitado**
— existe só no projeto do claude.ai, cuja data não é o histórico público datado que
`PREREGISTRO-EVIDENCIA.md` exige. Consequência prática: **até o commit, ele é rascunho**, e as
correções das §2 e §3 entram **sem gerar `v2`**. Depois do commit, cada uma custaria uma versão.
**A janela para corrigir de graça fecha no primeiro `git commit` dele.**

**(b) O período de teste termina num arquivo que não abre.** §2: *"jan/2010 a ago/2026"*. O
`COTAHIST_A2026.ZIP` chegou **truncado** (P-100) — ZIP em streaming cortado aos 38 MB. Sem ele o
teste termina em dez/2025, com 72 meses em vez de 80, e o poder cai junto. **A P-100 passa de
`DECISAO_DE_DESENHO` para `BLOQUEIA_O_SISTEMA` para a família `aprendizado`.** E a série do NEFIN
termina em 03/07/2026: o `alfa_contra_fatores()` da §6 não tem fator para jul–ago/2026.

**(c) Pinar `lightgbm` e `tabpfn` muda a impressão do ambiente do projeto inteiro.** A §11 trata
a compatibilidade — mas não o efeito colateral: a impressão `7565df1381e2c1ed` (P-15) muda, e
**todo resultado pré-registrado de 05/09 deixa de ser "conferência" e passa a ser "número novo"**
(`CLAUDE.md` §3). Se o TabPFN trouxer `torch` — `NAO_CONFIRMADO`: o PyPI recusou minha consulta
por `robots.txt`, e eu não busco por outro caminho; `pip install tabpfn --dry-run` na máquina dele
responde —, o efeito é grande. **Recomendação:** grupo de dependências opcional com **impressão
própria** para a família `aprendizado`, e o ambiente do motor intocado.

**(d) H-ML1 não é pré-condição da §7.** A condição 1 é *"H-ML2, H-ML3 ou H-ML4 rejeitada"* — todas
**contra o multifator**. Se o multifator tiver IC ≤ 0, vencê-lo é trivial. A H-ML5 (contra a
regra do déficit) protege em parte, porque o alvo dela não depende do multifator — mas vale
tornar explícito: **ou H-ML1 rejeitada entra como pré-condição, ou a §7 declara por que não
precisa.**

**(e) Referência que não resolve.** O pré-registro cita `pesquisa-e-plano-ml.md`; o arquivo no
projeto é `pesquisa-e-plano-ml-1.md`. É o defeito recorrente da casa em miniatura — e a
`achados_ancorados.py` não o pega, porque ela mede código de achado, não nome de arquivo.

---

## 5. O que fazer, e quando — tudo antes do commit

| # | o quê | onde | custo |
|---|---|---|---|
| 1 | §6: corte operativo = **máximo entre L ∈ {1, 2, 3}**, com o motivo (§2 desta auditoria) | `preregistro-ml-v1.md` | uma linha |
| 2 | §8: **nono teste — poder com sinal plantado**, reportado ao lado do veredito | idem | um parágrafo |
| 3 | §7: H-ML1 como pré-condição, ou a razão de não ser | idem | uma linha |
| 4 | §2: período termina onde o COTAHIST abre; P-100 vira bloqueio da família | idem | uma linha |
| 5 | §11: dependências da família em grupo opcional, com impressão própria | idem | um parágrafo |
| 6 | corrigir `pesquisa-e-plano-ml.md` → `-1.md` | idem | trivial |
| **7** | **então** commitar, e só então a data vale | desktop | — |

**Tudo isso é decisão sua**, e há uma razão para eu não aplicar: o pré-registro diz que muda só
com `v2` — e se eu o editasse agora, estaria decidindo sozinho que ele ainda é rascunho. Acho que
é, pela própria regra dele; mas quem assina o pré-registro é você.

---

## 6. O que esta auditoria NÃO mediu (P5)

1. **A dependência serial da série de IC.** Ela não existe ainda. A tabela da §2 mede o
   **reamostrador** em n = 80 sobre regressões de fator; o que se transfere é a aritmética dos
   blocos e a **direção** da degeneração — não o número exato para o IC.
2. **O `sd` do IC mensal**, e portanto o poder em unidades absolutas. Deliberadamente não
   estimado: número de literatura sem leitura seria o C-01 no documento errado.
3. **As dependências do TabPFN** — `ROBOTS_DISALLOWED`.
4. **Os dois documentos de marca** do projeto (`pesquisa-fundacao-marca-2026-09.md`,
   `pesquisa-marcas-rodada2-2026-09.md`) **não foram lidos**. Não tocam o pré-registro, e por
   isso ficaram fora desta auditoria — não por irrelevância.

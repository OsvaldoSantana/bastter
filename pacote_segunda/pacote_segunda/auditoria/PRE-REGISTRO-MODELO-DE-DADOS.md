# O modelo de dados do pré-registro

**Fecha o E-06 antes de qualquer código**, como você pediu — e pela razão certa: pela P2,
implementar um contador agora cristalizaria uma definição ainda incompleta em código, que
é o lugar mais caro para mudá-la.

Suas três decisões estão adotadas. Antes do esquema, **quatro pontos onde eu mudaria ou
acrescentei** — três são correções ao seu desenho, e o segundo tem número medido.

---

## 1. A extensão não precisa ser exceção — basta a amostra ser **regra**, não data

Há uma tensão no seu §1. Você diz, com razão, que a amostra tem de entrar no que é
congelado (é o furo do D2). E diz, também com razão, que mudar o fim da amostra é
extensão, não variante. **As duas coisas só convivem se a amostra registrada for uma
regra e não um literal.**

```yaml
# registrar ASSIM -- e a extensao deixa de precisar de regra propria
amostra:
  inicio: 2001-01          # inicio da serie NEFIN; nao e escolha, e o dado que existe
  fim: ULTIMA_DISPONIVEL   # REGRA, nao data
  filtros: [n_dias >= 15]
  fatores: [Rm_minus_Rf, SMB, HML, WML, IML]
```

Registrado assim, uma execução em outubro **avalia a mesma regra** e não altera campo
nenhum: a extensão é automática, e a data literal vira **saída** da execução, não entrada
do registro.

Registrado como `fim: 2026-07`, você precisa de uma cláusula dizendo "mudar este campo
específico não conta" — e cláusula de exceção é a superfície onde o contorno mora. Toda
a sua tabela do §1 continua valendo, mas passa a ser **consequência** do formato, não uma
lista a decorar: `2001→2005` muda `inicio`, que é campo; novo filtro muda `filtros`;
novo universo muda `universo`. Só `fim` é regra, e por isso só ele estende.

---

## 2. O controle de conjunto tem um **número**, e ele muda o portão — 1,96 → 2,891

Este é o ponto que nem você nem eu tínhamos, e é o conteúdo do "multiplicidade é problema
do conjunto".

Se cada estratégia rejeitar H0 a **t > 1,96**, o conjunto de oito tem probabilidade
**1 − 0,95⁸ ≈ 34%** de produzir ao menos uma rejeição falsa sob a nula. O `rejeita_se`
das oito diz *"alfa não distinguível de zero"* e **não diz a que corte** — então hoje o
corte é 1,96 por omissão, oito vezes.

Corrigido por Bonferroni (limite superior), com `m` = número de testes da família:

| m | o que é | corte t | HML (t = 2,94) |
|---|---|---|---|
| 1 | uma estratégia isolada | 1,960 | sobrevive, folga 0,98 |
| 2 | as executadas de fato (HML, SMB) | 2,241 | sobrevive, folga 0,70 |
| 8 | as oito pré-registradas | 2,734 | sobrevive, folga 0,21 |
| **13** | **o orçamento inteiro** (soma dos `variantes_permitidas`) | **2,891** | **sobrevive, folga 0,049** |

**O seu único resultado significativo sobrevive até ao corte mais conservador — por
0,049 de um t.** Isso não o invalida; recoloca-o. "t = 2,94" soa como p ≈ 0,003; corrigido
pela família que você mesmo pré-registrou, é significância **na margem** — o que combina
com as quatro razões que o seu próprio registro já lista para não agir sobre ele
(alfa negativo em 2009-2016, bootstrap com P(t > 1,96) = 83%, 73% do alfa em 12 dos 306
meses).

**Duas ressalvas, e as duas contra mim:**

1. **Bonferroni superestima a correção** quando os testes são correlacionados — e estes
   são: todas as oito regridem sobre os mesmos cinco fatores, na mesma série. O corte
   verdadeiro fica **entre 1,96 e 2,891**. Bonferroni é o teto honesto, não a resposta.
2. **Qual `m` usar é decisão sua e não é óbvia.** Pelas execuções realizadas (m = 2) é
   o que de fato aconteceu; pelo orçamento pré-registrado (m = 13) é o que você se
   autorizou a tentar. **Minha leitura: registrar os dois**, sempre, lado a lado — o
   primeiro descreve a evidência, o segundo descreve a disciplina.

**A consequência de desenho:** `rejeita_se` deixa de ser prosa e passa a carregar o corte,
e o corte é **função do tamanho da família**. Isso é o controle de conjunto virando
mecanismo em vez de intenção — que é exatamente o que faltava ao `variantes_permitidas`.

---

## 3. `pesquisa_id` não pode ser **declarado** — senão é renomeável

Você viu o buraco (*"alguém pode criar Conjunto A, B, C e resetar o contador"*) e fechou
com julgamento: *"o conjunto permanece o mesmo enquanto responder à mesma pergunta de
pesquisa"*. Julgamento é contornável por quem está de boa-fé e com pressa — que é o caso
perigoso, não o de má-fé.

**Ancore no dado, não no nome.** O projeto já calcula o que resolve isso: `hash_fonte()`
devolve o sha256 da série do NEFIN, e ele já viaja em **todo** resultado de
`alfa_contra_fatores`.

```yaml
pesquisa_id: derivado            # NAO se escreve a mao
  fonte_hash: 619991c2192c       # sha256[:12] da serie
  amostra_regra: "2001-01 .. ULTIMA_DISPONIVEL, n_dias>=15"
  # duas estrategias que tocam a MESMA serie sob a MESMA regra de amostra estao na
  # mesma familia, chamem-se como se chamarem.
```

**Renomear não reseta nada, porque o nome não é a chave.** Um conjunto novo exige dado
novo ou regra de amostra nova — e as duas coisas são visíveis e datadas. E cria uma
propriedade que o seu desenho queria e não tinha: **`m` passa a ser calculável**, não
declarado. O tamanho da família é uma consulta ao diário de execuções, não uma afirmação
de quem está registrando.

---

## 4. Falta dizer **qual resultado é o operativo** quando R1 e R2 divergem

Concordo inteiramente com a sua quarta regra — extensão não sobrescreve, correção não
apaga, variante não apaga. Mas ela deixa uma pergunta aberta, e o sistema **tem de agir**:
se R1 rejeita e R2 (extensão) não, **o que o portão lê?**

Sem regra, "preservar tudo" vira "escolha o que preferir" — que é o p-hacking pela porta
dos fundos, com auditoria completa.

**Proposta:**

- **a extensão mais recente é o resultado operativo.** Mais observação é mais informação;
  preferir a janela antiga é escolher a amostra pelo resultado;
- **divergência de veredito entre R1 e Rn é evento registrável e BLOQUEANTE**: a
  estratégia não pode ser usada para decidir nada enquanto a divergência não estiver
  escrita — o que mudou, em que janela, e a leitura de quem escreveu;
- **o bloqueio é o ponto, não o efeito colateral.** Um alfa que morre ao estender é o
  evento mais informativo que este projeto pode produzir. Ele merece uma parada, não uma
  linha de log.

---

## 5. O esquema

```yaml
# ══ NIVEL CONJUNTO ═══════════════════════════════════════════════════════════
pesquisa:
  id: derivado_de(fonte_hash, amostra_regra)   # §3 -- nao se escreve a mao
  fonte:
    arquivo: dados/nefin_factors.csv
    sha256_12: 619991c2192c
    cobertura: "2001-01-02 a ULTIMA_DISPONIVEL"
  amostra_regra:
    inicio: 2001-01
    fim: ULTIMA_DISPONIVEL                     # §1 -- REGRA, nao data
    filtros: ["n_dias >= 15"]
    fatores: [Rm_minus_Rf, SMB, HML, WML, IML]
  familia:
    m_orcado: 13            # soma dos variantes_permitidas -- a disciplina
    m_executado: 2          # do diario -- a evidencia. CALCULADO, nao escrito
    correcao: BONFERRONI
    corte_t_orcado: 2.891
    corte_t_executado: 2.241
    nota: >
      Bonferroni e o TETO: as estrategias regridem sobre os mesmos fatores e sao
      correlacionadas, entao o corte verdadeiro fica entre 1,96 e o valor acima.
      Registrar os dois m e deliberado -- um descreve a evidencia, o outro a disciplina.

# ══ NIVEL ESTRATEGIA ═════════════════════════════════════════════════════════
hml_puro_v1:
  especificacao:                    # CONGELADA. hash disto e a impressao digital
    hipotese: "o premio de valor existe no Brasil; a pergunta e o que sobra liquido"
    rejeita_se:
      criterio: "alfa contra os demais fatores, liquido de custo e imposto"
      corte_t: DO_CONJUNTO          # §2 -- nao e 1,96 por omissao
    modelo: [Rm_minus_Rf, SMB, WML, IML]
    variavel_dependente:
      serie: HML
      tratamento_rf: NAO_SUBTRAIR   # long-short ja e excesso -- ver graus_de_liberdade
  graus_de_liberdade:               # o que PODIA ter sido outro, listado ANTES
    - campo: tratamento_rf
      escolhido: NAO_SUBTRAIR
      alternativa_defensavel: SUBTRAIR (correto para long-only)
      consequencia_medida: "inverte o sinal: +0,00766 (t 2,94) -> -0,00178 (t -0,68)"
      guardado_por: test_subtrair_risk_free_de_um_fator_inverte_o_veredito
    - campo: filtros.n_dias
      escolhido: ">= 15"
      alternativa_defensavel: "qualquer corte de 5 a 18"
      consequencia_medida: "nenhuma -- identico ao 5o decimal em todo o intervalo"
  variantes_permitidas: 1           # ALARME, nao trava -- exige justificativa escrita
  execucoes:                        # o DIARIO. Instrumento principal.
    - id: R1
      tipo: ORIGINAL
      data: 2026-09-05
      amostra_realizada: "2001-01 a 2026-06 · 306 meses"
      resultado: {alfa_am: 0.00766, t: 2.94, r2: 0.108}
      veredito: NAO_REJEITA_PARA_EFEITO_DE_DECISAO
      operativo: true               # §4
      ambiente: 7565df1381e2c1ed
  historico_de_registro:
    - data: 2026-09-03
      tipo: CORRECAO_FACTUAL        # isento de variante -- decisao 3 dele
      campo: hipotese_nula_esperada
      de: "NAO supera (base: HML paga 0,05% a.m.)"
      para: "o premio existe; a pergunta e o liquido"
      fonte_primaria: "serie NEFIN, medida: 0,688% a.m., t=2,60, 307 meses"
      por_que_nao_e_grau_de_liberdade: >
        nao havia duas leituras defensaveis: o numero de origem nao reproduz em
        janela nenhuma de 2001 a 2026. Corrigir erro de fato nao e escolher entre
        alternativas.
```

### Os quatro tipos de evento, e o teste que os separa

| tipo | gasta variante? | o teste |
|---|---|---|
| **EXTENSAO** | não | só `fim` muda, e `fim` é regra — nenhum campo congelado se altera |
| **CORRECAO_FACTUAL** | não | existe fonte primária mostrando que o valor anterior **não reproduz**. Sem alternativa defensável do outro lado |
| **VARIANTE** | **sim** | há **duas leituras defensáveis** e você escolheu uma. O `tratamento_rf` é o caso puro |
| **AMBIGUIDADE** | não — **bloqueia** | há duas leituras e **nenhuma fonte desempata**. Não escolhe: marca `NAO_CONFIRMADO`. É o C-01 |

A quarta linha é sua, do §C, e vale destacar porque é a que impede a isenção factual de
virar porta: quando a fonte não resolve, o caminho **não é** declarar erro factual e
corrigir — é declarar ambiguidade e parar. O C-01 é o precedente: `factor: 100` tem duas
leituras que diferem por 50×, e a resposta certa foi não escolher.

---

## 6. O que ainda não está decidido

| # | pergunta | por que é sua |
|---|---|---|
| 1 | `m` do corte: executado, orçado, ou os dois lado a lado? | minha leitura é **os dois**, mas isso põe dois números num lugar onde as pessoas querem um |
| 2 | Bonferroni ou FDR (Benjamini-Hochberg)? | Bonferroni controla *qualquer* falso positivo e é severo com 13; FDR controla a *proporção* e é mais adequado a exploração. Com 13 testes a diferença é material |
| 3 | a divergência R1↔Rn bloqueia a estratégia, ou só exige nota? | propus bloquear (§4). É a proposta mais cara deste documento |

**A 2 é a que eu não decidiria sozinho**, e a razão é que ela é uma escolha sobre que tipo
de erro você prefere. Bonferroni: quase nunca aceita algo falso, e por isso rejeita coisas
verdadeiras. FDR: aceita uma proporção controlada de falsos para não perder os
verdadeiros. Para **decidir onde pôr dinheiro**, o custo dos dois erros não é simétrico —
e quem sabe qual dói mais é você.

---

## 7. Uma coisa que este desenho **não** protege, e é bom que esteja escrito

Nada aqui impede o erro que de fato aconteceu no §0.2 do E-06: alimentar a função errada
e receber um veredito invertido sem aviso. Especificação congelada, graus de liberdade
declarados, diário e contador — os quatro — passariam por isso sem piscar, porque o
`tratamento_rf` só entra na lista de graus de liberdade **se alguém souber que ele
existe**.

O que pegou aquilo foi um **comentário em português no alto de um arquivo e dois testes**.

> Registrar isto no desenho é a P5 aplicada ao próprio aparato de pré-registro:
> **a limitação declarada vale mais que a proteção presumida.** O modelo de dados governa
> as escolhas que você sabe que fez. As que você não sabe que fez continuam sendo pegas
> por leitura, teste e conversa — e é por isso que o contador é alarme, não defesa.

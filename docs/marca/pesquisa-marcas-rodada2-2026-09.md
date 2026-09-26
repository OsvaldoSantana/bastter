# Pesquisa de marcas — rodada 2 (P-B5)

*Destino no repositório: `docs/marca/pesquisa-marcas-rodada2-2026-09.md`.*
*Continuação de [`docs/marca/pesquisa-fundacao-2026-09.md`](pesquisa-fundacao-2026-09.md). 20/09/2026, sessão de chat com busca na web.*
*A régua de status é a mesma (`COMPLETO`, `PARCIAL`, `NAO_CONFIRMADO`, `OBSERVADO`). As fontes estão na §9, com prefixo `G`.*

*Revisão de 26/09/2026 (decisão dele): os códigos deste documento foram renomeados para não colidir com os achados do projeto, que já tinham C- e R- com outro sentido. O número se mantém; muda só o prefixo. Este documento não cita achados do projeto. Notas de revisão no fim.*

| de | para | o que é | faixa neste documento |
|---|---|---|---|
| `C-nn` | `MC-nn` | livro de códigos de marca | 01 a 24 (24 códigos) |
| `R-nn` | `RI-nn` | requisito de interface | 01 a 16 (12 códigos) |

---

## 0. Resumo em seis linhas

1. **O concorrente mais perigoso não estava no mapa:** o banco grande com agente de IA. O Itaú e o Bradesco já recomendam e executam investimento por conversa. O Itaú mira **exatamente o público de entrada do MEOL**: clientes com carteira básica e pouco diversificada `COMPLETO` `[G05][G06]`.
2. **A poupança é a régua do leigo brasileiro.** Três marcas de pagamento usam "rende mais que a poupança" como argumento central. Pelo menos uma compara **rendimento bruto contra poupança isenta de IR**, uma comparação que distorce `COMPLETO` `[G01][G14]`.
3. **O número em destaque costuma ser o máximo condicionado** ("até 121% do CDI", "até 105% se trouxer R$ 1.000"), e as condições ficam no rodapé `COMPLETO` `[G02][G14]`.
4. **Há bons exemplos de linguagem para o leigo:** risco nomeado por sensação (Nubank: Cautela, Equilíbrio, Potencial) e intenção no lugar de parâmetro técnico (Toro: "quanto quer ganhar, quanto aceita perder") `PARCIAL` `[G10][G11]`.
5. **A independência se perde por aquisição.** Kinvo e Empiricus foram para o BTG; Toro, para o Santander; Easynvest, para o Nubank `PARCIAL` `[G12]`. Independência que não está escrita na estrutura some na venda da empresa.
6. **Saturação não atingida.** Os códigos financeiros estão convergindo, mas as referências de sentimento ainda trazem códigos novos. A rodada parou por orçamento, não pela regra (§6).

---

## 1. Método

- **Lente:** os requisitos RI-01 a RI-10 da rodada 1. Para cada marca, registro onde ela está alinhada com um requisito, onde vai contra ele, e se trouxe um **código novo**: um padrão que ainda não estava no livro de códigos.
- **Diferença para a rodada 1:** esta auditoria é **textual**, feita por sites oficiais, lojas de app, imprensa e estudos. **Não há prints**, então os códigos visuais (cor, tipografia, densidade) **não** foram avaliados para estas marcas.
- **Regra de parada:** três marcas seguidas sem código novo encerram o bloco. A ordem de auditoria foi a da §2.

---

## 2. As marcas auditadas, na ordem em que foram auditadas

| # | marca | grupo | código novo? | requisitos: alinha (+) / contra (−) | fonte |
|---|---|---|---|---|---|
| 1 | **PicPay** | pagamentos | sim: MC-01, MC-02, MC-03 | + RI-09 (cofrinhos usados sobretudo para reserva) · − RI-12 · − RI-14 | `[G01][G02][G03]` |
| 2 | **Serasa** | crédito | sim: MC-04, MC-05 | + RI-01 (glossário "Falando Dinheirês") · + RI-08 (editoria de alertas de golpe) | `[G04][G15][G16]` |
| 3 | **Itaú** | banco | sim: MC-06 | − independência (recomenda os próprios produtos) | `[G05][G06]` |
| 4 | **Bradesco** | banco | sim: MC-07 | − RI-06 (push para potenciais investidores) | `[G07][G08]` |
| 5 | **Banco do Brasil** | banco | não (repete MC-06) | — | `[G09]` |
| 6 | **C6** (vista de passagem) | banco | sim: MC-08 | — | `[G09]` |
| 7 | **Empiricus** | casa de análise | sim: MC-09 | − RI-13 | `[G17][G18]` |
| 8 | **Me Poupe!** | educação | sim: MC-10 | + RI-03 · + RI-09 (missão: transformar devedor em investidor) | `[G19][G20]` |
| 9 | **Primo Rico** | educação e influência | sim: MC-11, MC-12 | − RI-13 | `[G21][G22]` |
| 10 | **Nubank / Nu Invest** | banco digital | sim: MC-13, MC-14 | + RI-01 · + RI-15 · − RI-06 ("top 3 ativos do dia") | `[G10]` |
| 11 | **Clear / Rico** | corretoras | sim (menor): MC-15 | − RI-12 ("sem asteriscos" seguido de asterisco) | `[G23]` |
| 12 | **Toro** | corretora | sim: MC-16, MC-17 | + RI-01 · + RI-15 | `[G11]` |
| 13 | **BTG Pactual** | banco e corretora | sim: MC-18 | − independência (compra de independentes) | `[G12][G24]` |
| 14 | **Genial** | corretora | não | — | `[G12]` |
| 15 | **Verde Asset** | gestora | sim: MC-19, MC-20 | + transparência (carta mensal que reporta o ano abaixo do CDI) | `[G25][G26]` |
| 16 | **Dynamo** | gestora | sim: MC-21 | — | `[G27]` |
| 17 | **Relógio das ferrovias suíças (SBB)** | sentimento | sim: MC-22 | referência para RI-01 | `[G28][G29]` |
| 18 | **Volvo** | sentimento | sim: MC-23 | referência para a promessa | `[G30][G31]` |
| 19 | **Mercado Pago** | pagamentos | sim (menor): MC-24 | − RI-11 · − RI-12 | `[G14]` |
| 20 | **PagBank** | pagamentos | não (repete MC-01, MC-03) | — | `[G13]` |

---

## 3. Livro de códigos (a numeração começa aqui) *(revisão de 26/09/2026, nota N-NUM)*

| código | nome | o que é | marca de origem |
|---|---|---|---|
| **MC-01** | régua poupança | o retorno é apresentado **em relação à poupança**, que é o ponto de referência do leigo | PicPay, Mercado Pago, PagBank |
| **MC-02** | máximo condicionado | a manchete mostra a taxa máxima ("até 121%"); a condição para obtê-la fica abaixo | PicPay, Mercado Pago |
| **MC-03** | poupança como alavanca de crédito | o dinheiro guardado aumenta o limite do cartão ou serve de garantia para empréstimo | PicPay (cofrinho do cartão); Nubank (rodada 1) |
| **MC-04** | pontuação como identidade | um número único (score 0–1000) com faixas de cor, e o vocabulário moral de "nome limpo / nome sujo" | Serasa |
| **MC-05** | distribuição dentro de assistentes de IA | o conteúdo da marca vira um app dentro do ChatGPT, com expansão anunciada para Claude, Gemini e Perplexity | Serasa |
| **MC-06** | agente de IA que recomenda e executa | o assistente conversa, recomenda e **transaciona** o produto da própria instituição | Itaú, Bradesco, Banco do Brasil |
| **MC-07** | recomendação medida por captação | o sucesso da recomendação é medido pelo **dinheiro captado**, não pelo resultado do cliente | Bradesco |
| **MC-08** | "seja seu próprio assessor" | a autonomia apresentada como a dispensa de intermediários | C6 |
| **MC-09** | depoimento de enriquecimento | uma pessoa comum narrando que ficou rica usando o serviço | Empiricus |
| **MC-10** | entretenimento e humor como pedagogia | educação financeira com linguagem informal e humor | Me Poupe! |
| **MC-11** | vergonha como persuasão | o anúncio envergonha quem ainda não investe | Primo Rico |
| **MC-12** | funil de audiência até transação | audiência → educação e assinatura → ambiente transacional, do mesmo grupo | Primo Rico |
| **MC-13** | risco nomeado por sensação | os fundos se chamam Cautela, Equilíbrio, Potencial | Nubank |
| **MC-14** | dois espaços por maturidade | experiência guiada no app principal; catálogo completo num app separado | Nubank / Nu Invest |
| **MC-15** | preço zero como argumento | "corretagem zero" como mensagem central | Clear, Rico |
| **MC-16** | intenção no lugar de parâmetro | em vez de "stop" e "alavancagem", o sistema pergunta quanto a pessoa quer ganhar e quanto aceita perder | Toro |
| **MC-17** | comparador no estilo de busca de hotel | títulos de renda fixa lado a lado, com taxa, imposto e rentabilidade | Toro |
| **MC-18** | independente absorvido | ferramentas e casas independentes compradas por bancos | BTG, Santander, Nubank |
| **MC-19** | carta mensal que admite resultado ruim | a gestora explica as posições e reporta quando ficou atrás do CDI | Verde |
| **MC-20** | personalidade como vetor de golpe | posts falsos com a foto do gestor famoso indicando ações e levando ao WhatsApp | Verde |
| **MC-21** | fechar a captação | o fundo fecha para novos investidores e reabre em janelas: escassez por **capacidade**, não por patrimônio | Dynamo |
| **MC-22** | parar para sincronizar | o ponteiro para no 12 até receber o sinal do relógio-mestre; legível de longe, sem números | relógio SBB |
| **MC-23** | segurança aberta | a invenção de segurança foi liberada para os concorrentes, e a segurança virou identidade | Volvo |
| **MC-24** | celebridade como transferência de confiança | uma cantora apresenta "a conta que mais rende do Brasil" | Mercado Pago |

---

## 4. Achados

### 4.1 O concorrente mais perigoso é o banco com agente de IA — `COMPLETO`

- **Itaú:** lançou a "Inteligência de Investimentos Itaú", um agente de IA generativa que conversa, recomenda e pode transacionar CDB-DI dentro da conversa `[G05]`. O teste começou com clientes Uniclass e Personnalité **sem assessor humano, com carteira básica e pouca diversificação** `[G06]`. É o público de entrada do MEOL, descrito com outras palavras.
- **Bradesco:** a camada de recomendação por IA já responde por mais de 65% do valor captado nas jornadas de investimento, e o banco está construindo um robô consultor `[G08]`. A BIA completa dez anos em 2026 e já executa transações `[G07]`.
- **Banco do Brasil:** lançou em 24/08/2026 um app com assistente de IA como interface principal `[G09]`.

**Leitura.** O leigo inseguro vai receber, dentro do app do banco onde já tem conta e sem pagar nada, uma "recomendação" conversacional. Três coisas diferenciam o MEOL, e nenhuma delas é a IA:

1. **Independência:** o banco recomenda o que distribui. O código MC-07 mostra a métrica que ele otimiza, que é a captação.
2. **Procedência:** o banco não mostra de onde vem cada número.
3. **Cadência:** o banco, com notificação e push, empurra para a frequência (MC-06 com RI-06).

**Implicação regulatória** `NAO_CONFIRMADO`: se bancos oferecem recomendação automatizada, o caminho regulatório existe e está sendo usado. O parecer jurídico da F4 deveria olhar como eles se enquadram.

### 4.2 A poupança é a régua, e a comparação costuma ser desigual — `COMPLETO`

- PicPay, Mercado Pago e PagBank usam "mais que a poupança" como mensagem principal `[G01][G13][G14]`.
- O blog do Mercado Pago compara R$ 1.000 por 12 meses: cerca de R$ 62 na poupança contra cerca de **R$ 149 brutos** na conta `[G14]`. A poupança é isenta de IR; a conta que rende CDI não é. A comparação correta é líquido contra líquido.

**Leitura.** Para o leigo, a poupança é o ponto de referência (MC-01), e o MEOL deve usá-lo. Mas sempre **líquido contra líquido**, com IR e custos, que é exatamente o que o motor já calcula. Vira o requisito **RI-11**.

### 4.3 O máximo condicionado em destaque — `COMPLETO`

- **PicPay:** "até 121% do CDI" no Cofrinho Turbinado, se o cliente for elegível e cumprir condições `[G02]`.
- **Mercado Pago:** 105% do CDI "trazendo R$ 1.000 por mês" ou assinando o Meli+ `[G14]`.
- **Clear:** "tudo zero, sem asteriscos", e no mesmo material, "*algumas operações estão sujeitas a cobranças" `[G23]`.

**Requisito RI-12:** o número em destaque é o do **caso padrão** do usuário. O máximo condicionado, se aparecer, vem depois e com a condição escrita.

### 4.4 A reserva vira alavanca de crédito — `COMPLETO` / `PARCIAL`

- No PicPay, o dinheiro no "Cofrinho do Cartão" soma ao limite do cartão de crédito `PARCIAL` (fonte secundária) `[G03]`.
- No Nubank (rodada 1), dinheiro guardado por três meses pode garantir um empréstimo até cinco vezes maior `OBSERVADO`.

**Leitura.** A reserva existe para não precisar de crédito numa emergência. Ligá-la ao crédito inverte a função. **Requisito RI-14:** no MEOL, a reserva nunca vira garantia nem gatilho de oferta.

### 4.5 Boas práticas de linguagem para o leigo — `PARCIAL`

- **Nubank:** os fundos se chamam Cautela, Equilíbrio e Potencial, e a empresa diz usar linguagem simples e experiência guiada para quem está começando `[G10]`.
- **Toro:** no home broker, o site pergunta quanto a pessoa quer ganhar e quanto aceita perder em cada operação, e calcula o resto, sem o jargão de mesa de operações `[G11]`.
- **Serasa:** criou um dicionário em vídeo de termos financeiros (o "Falando Dinheirês") `[G16]`.

**Requisito RI-15:** o risco é nomeado por sensação, e o MEOL pergunta **intenção** ("quanto você aceitaria ver cair sem vender?") em vez de parâmetro técnico. Liga direto ao `perfil.yaml`: as escolhas declaradas do perfil podem ser **perguntas de intenção** na interface.

**O contraexemplo no mesmo Nubank:** o site oferece escolher entre "os 3 principais ativos do dia" `[G10]`. É uma lista de mais populares do dia, que o RI-06 proíbe.

### 4.6 Promessa de resultado já foi punida no Brasil — `COMPLETO`

- **Empiricus / caso Bettina (2019):** uma funcionária narrava ter acumulado mais de R$ 1 milhão a partir de R$ 1.520. O Procon-SP multou por publicidade enganosa, afirmando que garantir resultado de investimento em renda variável induz o consumidor a erro. O Conar suspendeu as peças e advertiu a empresa `[G17][G18]`.
- **Primo Rico:** um artigo acadêmico (UFRJ, revista *Dilemas*) analisa anúncios do influenciador que abordam o espectador com vergonha por não investir `[G21]`.
- **Regras da ANBIMA para influenciadores:** exigem que publicações patrocinadas sejam identificadas como publicidade, com a instituição contratante `PARCIAL` (data de vigência não confirmada) `[G22]`.

**Requisito RI-13:** proibido persuadir por culpa, vergonha, depoimento de enriquecimento ou promessa de resultado.

### 4.7 A independência se perde na venda da empresa — `PARCIAL`

- **BTG:** comprou a Vitreo e já tinha levado Kinvo, Empiricus e Real Valor `[G12]`.
- **Toro:** hoje se apresenta com "a segurança do Santander" `[G24]`.
- **Nubank:** comprou a Easynvest, que virou Nu Invest (rodada 1).

**Leitura, e ela conversa com a sua regra de fundação comercial.** Se o MEOL for vendido a um distribuidor, a promessa de independência acaba. Para a independência ser prova e não slogan, ela precisa estar **na estrutura**: um compromisso público e versionado no repositório (como um `politica.yaml` da empresa), e a transparência de que o método é aberto. O código público já é uma forma de independência que sobrevive a uma venda: qualquer pessoa pode continuar rodando o motor.

### 4.8 O que as gestoras ensinam — `PARCIAL`

- **Carta mensal que admite resultado ruim (MC-19):** a Verde reportou, na carta mensal, o fundo à frente do CDI no mês mas atrás no acumulado do ano `[G25]`. É o registro honesto como hábito.
- **Personalidade como vetor de golpe (MC-20):** circularam posts falsos com a foto de Luis Stuhlberger indicando ações e cursos e levando a atendimento pelo WhatsApp `[G26]`. **Requisito RI-16:** um único canal oficial declarado; o MEOL nunca pede nada por WhatsApp ou mensagem direta.
- **Fechar a captação (MC-21):** a Dynamo reabre o fundo em janelas com limite de captação `[G27]`. É **exclusividade por capacidade e disciplina**, não por patrimônio: o pertencimento sem exclusão que você descreveu, numa forma que já existe no mercado brasileiro.

### 4.9 As duas referências de sentimento dão a metáfora da marca — `COMPLETO`

- **Relógio das ferrovias suíças (MC-22):** desenhado em 1944 por Hans Hilfiker, sem números, legível de longe. O ponteiro vermelho dos segundos para no 12 porque, na origem, esperava o impulso de um relógio central para sincronizar todas as estações `[G28][G29]`.

  É a imagem exata da cadência do MEOL: **uma vez por mês, o sistema para, sincroniza com a fonte (CVM, B3) e só então anda.** A pausa não é lentidão, é confiabilidade.

  Nota de cautela `[G28]`: a Apple usou o desenho no iOS 6 sem pedir permissão. A metáfora pode ser usada; o desenho, não.

- **Volvo (MC-23):** o cinto de três pontos de 1959 teve a patente liberada para os outros fabricantes, e a segurança virou o princípio da marca `[G30][G31]`.

  Uma lição de procedência de brinde: a frase famosa que circula sobre essa decisão ("mais valor como ferramenta gratuita do que como lucro") **não é de 1959**. Vem de um texto retrospectivo de 2013 `[G32]`. Até a história da marca mais segura do mundo circula com citação sem fonte.

  **Para o MEOL:** o método aberto (o repositório público) é o equivalente do cinto liberado. A promessa "qualquer um pode conferir" é o nosso cinto de três pontos.

### 4.10 A distribuição está indo para dentro dos assistentes de IA — `PARCIAL`

- A Serasa colocou conteúdo de educação financeira dentro do ChatGPT e anunciou expansão para Claude, Gemini e Perplexity `[G15]`.
- Uma pesquisa da própria Serasa com o Opinion Box, citada pela imprensa, diz que **38%** usam IA para finanças diariamente `NAO_CONFIRMADO` `[G15]`. A ANBIMA mede **9%** de investidores usando IA como fonte sobre investimentos (rodada 1). **Os números não se comparam**: perguntas e amostras diferentes.

**Leitura lateral.** A arquitetura já decidida (motor que roda no aparelho, contrato de saída) permite que o MEOL também exista como **ferramenta dentro de um assistente**, respondendo com procedência. É uma porta de distribuição, não uma decisão. Fica registrada como hipótese de produto.

---

## 5. Requisitos novos (continuam RI-01 a RI-10)

| código | requisito | origem |
|---|---|---|
| **RI-11** | toda comparação de retorno é **líquido contra líquido** (IR, taxas), especialmente contra a poupança, que é isenta | 4.2 |
| **RI-12** | o número em destaque é o do caso padrão do usuário; o máximo condicionado só aparece depois, com a condição escrita | 4.3 |
| **RI-13** | proibido persuadir por culpa, vergonha, depoimento de enriquecimento ou promessa de resultado | 4.6 |
| **RI-14** | a reserva nunca vira garantia de crédito nem gatilho de oferta | 4.4 |
| **RI-15** | risco nomeado por sensação; o sistema pergunta intenção, não parâmetro técnico | 4.5 |
| **RI-16** | um único canal oficial declarado; o MEOL nunca pede dado nem dinheiro por WhatsApp ou mensagem direta | 4.8 |

---

## 6. Resultado da regra de saturação

**A regra não foi atingida.** Em 20 marcas, a maior sequência sem código novo foi de uma marca (Banco do Brasil, Genial, PagBank, sempre intercaladas com marcas que trouxeram código).

- **Marcas financeiras:** os códigos estão **convergindo**. As últimas marcas financeiras (BB, Genial, PagBank, Mercado Pago) repetiram códigos ou trouxeram só variações menores.
- **Referências de sentimento:** ainda trazem códigos novos (SBB, Volvo).

A rodada parou **por orçamento de tempo**, e isso fica declarado (P5), não disfarçado de saturação.

**Não auditadas nesta rodada:** Santander (só visto pela Toro), Caixa, Itaú Personnalité e Private, Suno, SPX, Braun, Grand Seiko e Leica.

---

## 7. Limitações declaradas

1. **Auditoria textual**, sem prints. Nenhum código visual novo foi registrado para estas 20 marcas.
2. **Várias fontes são imprensa ou blog da própria marca.** Onde é blog da marca, o dado descreve **o que a marca diz**, não o que ela entrega.
3. **Nubank:** a página lida é a versão em inglês do site brasileiro `[G10]`.
4. **ANBIMA e influenciadores:** a data de vigência das regras não foi confirmada `[G22]`.
5. **MC-03 no PicPay** vem de fonte secundária `[G03]`.
6. **§4.1 regulatório** é inferência minha, não verificada.

---

## 8. Próximo passo proposto

**P-B4: ler os requisitos mínimos de experiência do usuário do Pix (versão 7.4) inteiros, com foco no capítulo de acessibilidade.**

- **Por que agora, e não a rodada 3 de marcas:**
  - É **fonte primária** escrita pelo regulador para exatamente o nosso público (apps de pessoa física, leigos, celular). Deve render requisitos com status `COMPLETO`, enquanto a rodada 3 de marcas renderia códigos com retorno decrescente nas financeiras.
  - Os requisitos RI-01 a RI-16 já estão prontos para serem conferidos contra ele.
- **O que destrava:** a lista final de requisitos de interface, que é a entrada da etapa 4 (UX).
- **O que impede hoje:** nada.
- **A rodada 3 de marcas** fica como pendência P-B5b, com a mesma regra de saturação e a lista da §6.

---

## 9. Fontes

Acesso em 20/09/2026.

- **[G01]** PicPay — página de investimentos (Cofrinhos, até 121% do CDI) — https://picpay.com/pt-br/pf/investimentos · blog sobre cofrinhos para reserva: https://blog.picpay.com/cofrinhos-para-reserva-de-emergencia/
- **[G02]** iDinheiro — Cofrinho PicPay, condições do Turbinado — https://www.idinheiro.com.br/investimentos/cofrinhos-picpay/
- **[G03]** Portal Insights — cofrinho do cartão e limite (secundária) — https://www.portalinsights.com.br/perguntas-frequentes/quanto-rende-o-cofrinho-do-picpay-por-dia
- **[G04]** Serasa — Serasa no ChatGPT (ajuda oficial) — https://www.serasa.com.br/ajuda/outros-servicos/serasa-no-chatgpt/
- **[G05]** Convergência Digital — agente de investimentos do Itaú — https://convergenciadigital.com.br/mercado/com-agentes-ia-itau-quer-democratizar-investimentos/ · Canaltech: https://canaltech.com.br/mercado/itau-revela-ia-que-ajuda-a-escolher-os-melhores-investimentos/
- **[G06]** NeoFeed — público-alvo do agente do Itaú — https://neofeed.com.br/wealth-management/itau-aplica-na-ia-generativa-como-agente-de-investimentos
- **[G07]** Propmark — Meu Bradesco e b.ia (10 anos) — https://propmark.com.br/?p=125981
- **[G08]** Let's Money — recomendação por IA do Bradesco, 65% da captação — https://www.letsmoney.com.br/noticias/bradesco-acelera-transformacao-digital-ia/ · Consumidor Moderno (push a potenciais investidores): https://consumidormoderno.com.br/bia-bradesco-investimentos/
- **[G09]** Distrito — Meu Assistente BB (24/08/2026) — https://www.distrito.me/blog/banco-do-brasil-ia · C6 "seja você mesmo o seu assessor": https://www.abcdacomunicacao.com.br/c6-bank-estreia-campanha-para-incentivar-brasileiros-a-serem-seus-proprios-assessores-de-investimentos/
- **[G10]** Nubank — página de investimentos — https://nubank.com.br/en/investments · nomes dos fundos: https://mercadoeconsumo.com.br/2021/04/22/nubank-inicia-testes-de-produtos-voltados-para-a-experiencia-com-investimentos/
- **[G11]** Brazil Journal — Toro (intenção no lugar de jargão; comparador) — https://braziljournal.com/?p=36026 · https://braziljournal.com/toro-quer-popularizar-a-bolsa-sem-o-agente-autonomo
- **[G12]** Finsiders — BTG, Vitreo, Kinvo, Empiricus; Genial — https://finsidersbrasil.com.br/noticias-sobre-fintechs/por-que-faz-sentido-a-compra-de-mobills-e-monetus-pela-toro-do-santander/
- **[G13]** PagBank — App Store (cofrinho, poupar automático) — https://apps.apple.com/BR/app/id1186059012
- **[G14]** Mercado Pago — blog (comparação com a poupança) — https://www.mercadopago.com.br/blog/rendimento-diario-mercado-pago-vs-poupanca · página "a conta que mais rende": https://www.mercadopago.com.br/turbine-sua-conta?code=1H1A5
- **[G15]** Let's Money — Serasa no ChatGPT, expansão e pesquisa Opinion Box — https://www.letsmoney.com.br/ia/serasa-lanca-educacao-financeira-chatgpt/
- **[G16]** Serasa — imprensa, dicionário "Falando Dinheirês" — https://www.serasa.com.br/imprensa/dicionario-falando-dinheires-incentivo-a-educacao-financeira/
- **[G17]** Meio & Mensagem — Procon-SP multa Empiricus — https://www.meioemensagem.com.br/comunicacao/procon-sp-multa-empiricus-por-caso-bettina
- **[G18]** Meio & Mensagem — Conar suspende campanha — https://www.meioemensagem.com.br/comunicacao/caso-bettina-conar-susta-campanha-e-adverte-empiricus · IstoÉ Dinheiro (citação do Procon): https://istoedinheiro.com.br/procon-sp-multa-empiricus-por-propaganda-enganosa
- **[G19]** Revista Organicom (USP) — análise do discurso do Me Poupe! — https://journals.usp.br/organicom/article/download/171830/173803/501764
- **[G20]** Meaningful Business — missão "transformar devedor em investidor" — https://meaningful.business/?p=33732
- **[G21]** Revista Dilemas (UFRJ) — anúncios de influenciadores de investimento — https://revistas.ufrj.br/index.php/dilemas/article/view/65280/41987
- **[G22]** Revista Oeste — regras da ANBIMA para influenciadores — https://revistaoeste.com/economia/influenciadores-financas-regulamentados-anbima/
- **[G23]** InfoMoney (conteúdo patrocinado Clear) — "sem asteriscos" — https://www.infomoney.com.br/?p=719601 · asterisco de custos: https://www.infomoney.com.br/?p=1612533
- **[G24]** Blog da Toro — "a segurança do Santander" — https://blog.toroinvestimentos.com.br/educacao-financeira/aplicativo-de-investimento/
- **[G25]** BP Money — carta mensal da Verde — https://bpmoney.com.br/mercado/verde-asset-zera-aposta-de-alta-do-dolar-contra-o-real/
- **[G26]** BP Money — posts falsos com a imagem de Stuhlberger — https://bpmoney.com.br/tag/verde-asset-2/
- **[G27]** InfoMoney — Dynamo reabre o Cougar com limite de captação — https://www.infomoney.com.br/?p=1770488
- **[G28]** RSI (rádio e TV pública suíça) — 75 anos do relógio da SBB — https://www.rsi.ch/info/svizzera/Perch%C3%A9-si-ferma--1127601.html
- **[G29]** Relojes Especiales (fórum) — funcionamento stop2go (secundária) — https://relojes-especiales.com/threads/el-reloj-de-las-estaciones-de-tren-suizas.581211/
- **[G30]** Volvo Cars — nota de imprensa sobre o cinto de três pontos — https://www.volvocars.com/uk/media/press-releases/AB57626B8B94A718/
- **[G31]** Volvo Group — história do cinto de três pontos — https://www.volvogroup.com/en/about-us/heritage/three-point-safety-belt.html
- **[G32]** TruthOrFiction — origem da citação sobre a patente (retrospectiva de 2013) — https://www.truthorfiction.com/?p=129349

---

## Notas de revisão

*26/09/2026 — trazido do Projeto no claude.ai para o repositório.*

- **N-COD.** C-nn → MC-nn e R-nn → RI-nn, só neste documento (tabela no cabeçalho). Motivo: os achados do projeto sobre o fator, o ajuste de proventos, a moeda e a ordem dos portões já usavam esses mesmos números com os prefixos C- e R-, e outros C/R já existiam em outros arquivos com outro sentido; os instrumentos `achados_ancorados` e `codigos_preservados` contariam todos como achados. Guardado por `auditoria/test_codigos_de_marca.py`.
- **N-NUM.** O título dizia "continua a numeração da rodada 1", mas a rodada 1 não numerou códigos: os achados dela (§4, B3) estão em texto corrido. A numeração começa nesta rodada, em MC-01.

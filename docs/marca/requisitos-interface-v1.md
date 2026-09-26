# Requisitos de interface do MEOL — v1

*Destino no repositório: `docs/marca/requisitos-interface-v1.md`.*
*20/09/2026. Consolida RI-01 a RI-21, derivados de três rodadas de pesquisa.*

*Revisão de 26/09/2026 (decisão dele): os códigos deste documento foram renomeados para não colidir com os achados do projeto, que já tinham C- e R- com outro sentido. O número se mantém; muda só o prefixo. As citações de achados do projeto (F-02) ficaram como estão. Notas de revisão no fim.*

| de | para | o que é | faixa neste documento |
|---|---|---|---|
| `R-nn` | `RI-nn` | requisito de interface | 01 a 21 (21 códigos) |

---

## 0. Como ler este documento

Este é o **contrato de interface**: o que qualquer tela do MEOL precisa cumprir, qualquer que seja a direção visual escolhida depois. Ele não descreve telas. Descreve regras que as telas têm de passar.

Cada requisito traz:

- **enunciado** — a regra, em uma frase;
- **por quê** — a evidência que a sustenta, com o código da fonte nos relatórios de origem (`[F..]` rodada 1, `[G..]` rodada 2, `[H..]` Pix e pendências);
- **status da evidência** — mesma régua do `custos.yaml`: `COMPLETO`, `PARCIAL`, `NAO_CONFIRMADO`;
- **verificação** — como saber se a regra foi cumprida. Três tipos: **teste** (automático, roda no CI), **revisão** (checklist humano por tela) e **pesquisa** (só se decide com pessoas).

**A regra de ouro deste arquivo:** requisito sem verificação é intenção, não requisito. Se não dá para testar nem revisar, ele volta para a pesquisa.

**Numeração é estável.** Um requisito nunca é renumerado. Se cair, vira `REVOGADO` com a data e o motivo, e o número não é reaproveitado.

**Origem dos documentos:**

- rodada 1 — [`docs/marca/pesquisa-fundacao-2026-09.md`](pesquisa-fundacao-2026-09.md)
- rodada 2 — [`docs/marca/pesquisa-marcas-rodada2-2026-09.md`](pesquisa-marcas-rodada2-2026-09.md)
- Pix e pendências — [`docs/marca/pesquisa-pix-e-pendencias-2026-09.md`](pesquisa-pix-e-pendencias-2026-09.md)

---

## 1. Os 21 requisitos, por tema

### A. Compreensão e linguagem

**RI-01 — nenhuma decisão depende de ler gráfico ou jargão; a camada 1 é uma frase curta.**
*Por quê:* 29% dos brasileiros de 15 a 64 anos são analfabetos funcionais e só 10% são proficientes `[F05]`; o Pix recomenda descrições curtas e diretas `[H01]`; a legibilidade é pilar de produto na Grand Seiko `[H05]` e o essencial é doutrina em Leica e Braun `[H04][H06]`. `COMPLETO`
*Verificação:* **teste** — toda frase da camada 1 com no máximo 15 palavras e sem termo do glossário técnico não definido em tela; **pesquisa** — teste de 5 segundos (a pessoa diz o que fazer neste mês).

**RI-02 — formatação numérica brasileira impecável, testada automaticamente.**
*Por quê:* duas das doze vitrines auditadas erram formato de número: Versace "R$ 16,900" e XP "R$ 70.000.00" `[OBSERVADO, rodada 1]`. Uma terceira, o Gorila, exibe R$ 4.159.382,64 numa posição de 45 ações a R$ 25,60, que dá R$ 1.152,00: valor incompatível com quantidade × preço, `NAO_CONFIRMADO` sem o print *(revisão de 26/09/2026, nota N-GORILA)*. Num produto financeiro isso custa confiança. `OBSERVADO`
*Verificação:* **teste** — todo valor monetário renderizado passa por um formatador único; teste que quebra se aparecer ponto decimal, separador errado ou número sem unidade.

**RI-03 — educação dentro da decisão; nenhuma trilha de curso separada.**
*Por quê:* a literatura diverge sobre o efeito da educação financeira `[F06][F07]`, mas ensinar no momento da decisão é o melhor desenho sob a leitura pessimista e não perde nada sob a otimista. `PARCIAL`
*Verificação:* **revisão** — todo termo técnico tem definição no ponto de uso; nenhum item de menu chamado "curso", "trilha" ou "aulas".

**RI-15 — risco nomeado por sensação; o sistema pergunta intenção, não parâmetro técnico.**
*Por quê:* Nubank nomeia fundos como Cautela, Equilíbrio e Potencial; a Toro pergunta quanto a pessoa quer ganhar e quanto aceita perder, em vez de pedir stop e alavancagem `[G10][G11]`. `PARCIAL`
*Verificação:* **revisão** — nenhuma pergunta de configuração pede parâmetro técnico sem oferecer a versão em intenção; **pesquisa** — o leigo consegue responder sem ajuda.

### B. Honestidade do número e da recusa

**RI-05 — incerteza em faixa numérica escrita em linguagem comum; nunca "pode variar".**
*Por quê:* em cinco experimentos com 5.780 pessoas, a faixa numérica quase não afetou a confiança na fonte, enquanto a incerteza verbal e vaga reduziu `[F10]`. `COMPLETO`
*Verificação:* **teste** — campo com status `PARCIAL` só renderiza como faixa; **revisão** — a faixa aparece em frase comum ("entre R$ 480 e R$ 620"), nunca como "IC 95%".

**RI-10 — estado vazio mostra "sem dado" e o motivo, nunca um zero colorido.**
*Por quê:* o Bastter System exibe "▲ R$ 0,00 · 0,00%" em verde numa conta sem dados `[OBSERVADO, rodada 1]`. É o F-02 na interface: ausência virando número, e número com cara de ganho. `OBSERVADO`
*Verificação:* **teste** — renderizar o relatório de um usuário novo (`test_usuario_novo`) e falhar se aparecer qualquer valor formatado onde o dado é ausente.

**RI-11 — toda comparação de retorno é líquido contra líquido, com IR e taxas.**
*Por quê:* o blog do Mercado Pago compara R$ 62 na poupança contra cerca de R$ 149 **brutos** na conta; a poupança é isenta de IR e a conta não `[G14]`. `COMPLETO`
*Verificação:* **teste** — a função de comparação recusa operar se faltar o insumo de IR ou de custo (mesma regra do F-02: sem insumo, não calcula).

**RI-12 — o número em destaque é o do caso padrão do usuário; o máximo condicionado só vem depois, com a condição escrita.**
*Por quê:* "até 121% do CDI" no PicPay, "105% se trouxer R$ 1.000" no Mercado Pago, e a Clear anunciando "tudo zero, sem asteriscos" com asterisco no mesmo material `[G01][G02][G14][G23]`. `COMPLETO`
*Verificação:* **revisão** — nenhum número de destaque usa "até"; se houver condição, ela está na mesma tela e no mesmo tamanho de leitura.

**RI-17 — toda recusa nomeia o motivo real e diz de quem é a falha.**
*Por quê:* o Pix obriga mensagens de erro específicas e, quando o erro é do próprio participante, exige que isso fique claro ao usuário `[H01]`. `COMPLETO`
*Verificação:* **teste** — cada exceção do motor (`InsumoBloqueado` e as demais) tem um texto de tela associado, e falha o teste se alguma exceção cair num texto genérico.

**RI-19 — a mensagem de confirmação descreve exatamente o que foi feito, e nada além.**
*Por quê:* o Pix determina que a mensagem de sucesso do registro de chave não induza o usuário a concluir que a chave é necessária para pagar `[H01]`. `COMPLETO`
*Verificação:* **revisão** — cada texto de confirmação é lido contra a pergunta: "isto afirma mais do que aconteceu?".

**RI-07 — todo padrão é escolha declarada, com procedência e responsável.**
*Por quê:* na adesão automática estudada por Madrian e Shea, parte dos participantes manteve o padrão por tomá-lo como conselho de investimento da empresa `[F08]`; e o percentual padrão de 2% a 3% virou padrão de mercado por acidente `[F09]`. Juridicamente, no MEOL, padrão é recomendação *(confirmada em 26/09/2026: [Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md), art. 1º, caput e § 1º, I e II, e art. 2º — para o MEOL oferecido a terceiros como serviço; nota N-CVM)*. `COMPLETO`
*Verificação:* **teste** — todo valor padrão vem de chave declarada em YAML, com fonte; nenhum número padrão nasce no código da interface.

### C. Proteção contra o próprio impulso

**RI-04 — aviso de queda antes do primeiro aporte em renda variável, com o tamanho histórico da queda.**
*Por quê:* entre investidores, segurança é a vantagem mais citada (44%) e só 7% apontam risco de perda como desvantagem `[F01]`. A primeira queda contradiz a expectativa. `COMPLETO`
*Verificação:* **revisão** — o aviso existe antes do primeiro aporte e traz número histórico com fonte, não adjetivo.

**RI-06 — proibidos: confete, recompensa por operação, sequência de dias, lista de "mais populares", notificação para operar e ranking de usuários.**
*Por quê:* o regulador de Massachusetts acusou o Robinhood de usar confete, raspadinhas, ações de brinde, notificações e listas de mais populares para induzir operações frequentes; a empresa removeu o confete em 2021 e fechou acordo de US$ 7,5 milhões em 2024 `[F19][F20]`. O Nubank oferece "os 3 principais ativos do dia" `[G10]`. `COMPLETO`
*Verificação:* **revisão** — lista de proibições conferida a cada versão; **teste** — nenhuma notificação com verbo de ação de compra ou venda.

**RI-09 — a primeira jornada do leigo é a reserva.**
*Por quê:* 31% da população não tem reserva alguma e, entre quem tem, 43% a consumiria em até seis meses `[F01]`; o motor já trata a reserva como Fase A. `COMPLETO`
*Verificação:* **teste** — usuário novo sem reserva recebe decisão de reserva, nunca de ação.

**RI-14 — a reserva nunca vira garantia de crédito nem gatilho de oferta.**
*Por quê:* no PicPay o dinheiro do cofrinho do cartão soma ao limite `[G03]`; no Nubank, dinheiro guardado por três meses pode garantir empréstimo maior `[OBSERVADO]`. Isso inverte a função da reserva, que existe para não precisar de crédito. `PARCIAL`
*Verificação:* **revisão** — nenhuma tela de reserva contém oferta, e o motor não expõe o saldo da reserva a nenhum cálculo de crédito.

**RI-20 — o que reduz exposição vale na hora; o que aumenta exposição tem carência declarada.**
*Por quê:* no Pix, reduzir limite é imediato, e aumentar leva de 24 a 48 horas e depende de aprovação `[H01]`. `COMPLETO`
*Verificação:* **teste** — mudança de perfil que aumenta risco só vale no ciclo seguinte; mudança que reduz vale imediatamente.

**RI-13 — proibido persuadir por culpa, vergonha, depoimento de enriquecimento ou promessa de resultado.**
*Por quê:* o Procon-SP multou a Empiricus por publicidade enganosa no caso Bettina e o Conar suspendeu as peças `[G17][G18]`; um artigo da UFRJ analisa anúncios do Primo Rico que abordam o espectador pela vergonha `[G21]`; as regras da ANBIMA para influenciadores estão em vigor desde 13/11/2023 `[H07]`. `COMPLETO`
*Verificação:* **revisão** — todo texto de marketing passa pela lista de proibições antes de publicar.

### D. Segurança e antigolpe

**RI-08 — notificações e comprovantes sem link clicável.**
*Por quê:* 34% da população passou por golpe ou fraude em 2025, e 42% entre investidores; o mais comum é o link falso que imita banco `[F01]`. O Banco Central vedou propaganda, ofertas e hiperlinks em comprovantes de Pix `[H01][F14]`. `COMPLETO`
*Verificação:* **teste** — nenhuma notificação ou comprovante contém URL.

**RI-16 — um único canal oficial declarado; o MEOL nunca pede dado nem dinheiro por WhatsApp ou mensagem direta.**
*Por quê:* circularam posts falsos com a foto de Luis Stuhlberger indicando ações e levando a atendimento por WhatsApp `[G26]`; e um golpe usou o número oficial do Caixa Tem `[H02]`. `PARCIAL`
*Verificação:* **revisão** — o canal oficial está declarado em tela fixa e no site, com a frase do que o MEOL nunca pede.

**RI-18 — texto vindo de fonte externa é exibido literalmente, nunca renderizado como link ou conteúdo dinâmico.**
*Por quê:* o Pix determina que o campo "Descrição" não contenha HTML e que o app exiba os caracteres literalmente `[H01]`. Nomes de empresa e campos de dado da CVM entram na mesma categoria. `COMPLETO`
*Verificação:* **teste** — o renderizador escapa todo texto vindo de dado; teste com carga maliciosa conhecida.

**RI-21 — canal de contato a um toque na tela principal, sem etapas intermediárias, e instrução de onde reclamar fora do MEOL.**
*Por quê:* o Pix obriga atalho na tela inicial para o canal de atendimento, sem etapas intermediárias, e mensagem informando que a reclamação pode ir ao Banco Central `[H01]`. `COMPLETO`
*Verificação:* **revisão** — contagem de toques até o canal: um.

---

## 2. Conflitos entre requisitos, e como ficam resolvidos

| conflito | resolução |
|---|---|
| RI-01 (sem gráfico, frase curta) × RI-05 (faixa numérica) | a faixa aparece **em frase** ("entre R$ 480 e R$ 620"), não em gráfico de intervalo |
| RI-01 (frase curta) × RI-03 (ensinar na decisão) | a explicação fica na camada 2, aberta por toque; a camada 1 não cresce |
| RI-01 (sem jargão) × procedência técnica | o vocabulário do método vive na camada 3 e é aprendido no uso, nunca exigido para decidir |
| RI-07 (padrão declarado) × RI-06 (sem empurrão) | o padrão é mostrado com o porquê e é sempre alterável; nunca é empurrado por notificação |
| RI-20 (carência para aumentar risco) × autonomia do usuário | a carência é **declarada antes** e tem prazo visível; não é bloqueio silencioso |
| RI-09 (reserva primeiro) × público que já investe | quem já tem reserva formada pula a Fase A; o motor decide pelo estado, não por telas diferentes |

---

## 3. Matriz requisito × tela

| tela | requisitos que incidem |
|---|---|
| **T1 — aporte do mês** | RI-01, RI-02, RI-03, RI-05, RI-07, RI-10, RI-12, RI-17, RI-19, RI-21 |
| **T2 — carteira e reserva** | RI-02, RI-04, RI-06, RI-09, RI-11, RI-14, RI-20 |
| **T3 — o porquê (procedência e portões)** | RI-02, RI-03, RI-05, RI-10, RI-17, RI-18 |
| **T4 — enciclopédia** | RI-01, RI-02, RI-06, RI-18 |
| **cadastro e perfil** | RI-07, RI-15, RI-19, RI-20 |
| **notificações e comprovantes** | RI-06, RI-08, RI-16, RI-18, RI-19 |
| **páginas públicas e marketing** | RI-12, RI-13, RI-16 |

A matriz é o equivalente do Anexo I do Pix, onde o regulador exige que o participante apresente a tela de cada item `[H01]`: **cada requisito precisa apontar para pelo menos uma tela, e cada tela precisa passar pelos requisitos que a tocam.**

---

## 4. O que ainda é hipótese

Estes requisitos vêm de estudos feitos fora do Brasil ou de síntese minha, e continuam sujeitos ao teste com pessoas:

- **RI-05** (faixa numérica não custa confiança): replicação no Brasil é a hipótese H-C2 da rodada 1.
- **RI-03** (educação na decisão): a literatura diverge `[F06][F07]`.
- **RI-01** (camada 1 entendida sem ajuda): é a hipótese H-C1.
- **RI-15** (pergunta de intenção): boa prática observada em duas marcas, sem medição.

---

## 5. Limitações declaradas

1. **O capítulo de acessibilidade do Pix é recomendação, não obrigação** `[H01]`. Os requisitos daqui não substituem a lei de acessibilidade.
2. **WCAG não foi lida.** Contraste, tamanho de alvo e daltonismo ainda não têm fonte própria neste documento. Fica a pendência P-WCAG.
3. **Nenhuma verificação jurídica.** As menções à ANBIMA descrevem o que as regras dizem `[H07]`. As menções à CVM 19 foram conferidas no texto da resolução em 26/09/2026 ([Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md); nota N-CVM). Nenhuma substitui parecer (P-158).
4. **Os requisitos foram derivados sem nenhum teste com pessoas.** Nenhum deles foi validado com o público-alvo.
5. **Números de mercado envelhecem** (§8 do `CLAUDE.md`). Os deste documento valem para setembro de 2026.

---

## 6. Controle de versão

| versão | data | o que mudou |
|---|---|---|
| v1 | 20/09/2026 | consolidação inicial de RI-01 a RI-21, com verificação e matriz de telas |

**Regra de mudança:** requisito novo entra com número seguinte, evidência e verificação. Requisito que cai vira `REVOGADO` com data e motivo. Mudança de enunciado exige nova versão deste arquivo.

---

## Notas de revisão

*26/09/2026 — trazido do Projeto no claude.ai para o repositório.*

- **N-COD.** C-nn → MC-nn e R-nn → RI-nn, só neste documento (tabela no cabeçalho). Motivo: os achados do projeto sobre o fator, o ajuste de proventos, a moeda e a ordem dos portões já usavam esses mesmos números com os prefixos C- e R-, e outros C/R já existiam em outros arquivos com outro sentido; os instrumentos `achados_ancorados` e `codigos_preservados` contariam todos como achados. Guardado por `auditoria/test_codigos_de_marca.py`.
- **N-GORILA.** No RI-02, o Gorila deixou de contar como erro de formato: é valor incompatível com quantidade × preço (45 × 25,60 = 1.152 contra 4.159.382,64), `NAO_CONFIRMADO` sem o print. Os prints são de contas de terceiros ou de demonstração, não do autor.
- **N-CVM.** "Padrão é recomendação" (RI-07) se apoiava num achado de 20/09 que não estava no repositório e passou a `NAO_CONFIRMADO` em 26/09/2026. No mesmo dia, a Resolução CVM 19/2021 foi lida na fonte primária ([Res. CVM 19](../fontes/cvm-resolucao-19-consolidada.md)): a tese foi **confirmada com escopo** (art. 1º, caput e § 1º, I e II; art. 2º), valendo para o MEOL oferecido a terceiros como serviço. Não é parecer (P-158).

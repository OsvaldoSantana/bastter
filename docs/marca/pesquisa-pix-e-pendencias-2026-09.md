# Pix v7.4 e pendências da rodada 2

*Destino no repositório: `docs/marca/pesquisa-pix-e-pendencias-2026-09.md`.*
*20/09/2026. Continuação de [`pesquisa-fundacao-2026-09.md`](pesquisa-fundacao-2026-09.md) (rodada 1) e [`pesquisa-marcas-rodada2-2026-09.md`](pesquisa-marcas-rodada2-2026-09.md) (rodada 2).*
*Régua de status igual à das rodadas anteriores. Fontes na §5, com prefixo `H`.*

*Revisão de 26/09/2026 (decisão dele): os códigos deste documento foram renomeados para não colidir com os achados do projeto, que já tinham C- e R- com outro sentido. O número se mantém; muda só o prefixo. As citações de achados do projeto (A-03) ficaram como estão. Notas de revisão no fim.*

| de | para | o que é | faixa neste documento |
|---|---|---|---|
| `C-nn` | `MC-nn` | livro de códigos de marca | 03 a 29 (6 códigos) |
| `R-nn` | `RI-nn` | requisito de interface | 01 a 21 (8 códigos) |

---

## 0. Resumo

1. **O capítulo de acessibilidade do Pix é curto e quase todo `Recomendado`, não obrigatório** `COMPLETO` `[H01]`. Quem esperava um padrão obrigatório de acessibilidade encontra duas páginas de recomendações. O que obriga é a frase da introdução: tratamento não discriminatório, inclusive quanto a acessibilidade, **na forma da legislação vigente** — ou seja, o dever vem da lei, não do manual.
2. **O resto do documento vale muito mais que o capítulo de acessibilidade.** As obrigações gerais do Pix são um manual de honestidade de interface: erro com motivo nomeado, proibição de propaganda e link em comprovante, texto de terceiro exibido literalmente, aviso quando o destinatário mudou de dono, e consentimento que diz exatamente o que o outro lado vai ver `COMPLETO` `[H01]`.
3. **A assimetria de risco é a melhor ideia do documento:** reduzir limite é imediato; aumentar limite leva de 24 a 48 horas e depende de aprovação `COMPLETO` `[H01]`. Vira o requisito RI-20.
4. **O regulador audita telas.** O Anexo I lista os itens cujas telas o participante precisa apresentar no processo de verificação de aderência `COMPLETO` `[H01]`. É a P2 (contrato) e a P4 (evidência) aplicadas a interface.
5. **Pendências da rodada 2:** cinco resolvidas (Caixa, Suno, SPX, Braun/Rams, Grand Seiko, Leica e a data das regras da ANBIMA), três continuam abertas e ficam declaradas (Santander no Brasil, ranking do BC na fonte oficial, e duas fontes secundárias).

---

## 1. Os requisitos mínimos de experiência do usuário do Pix, versão 7.4

`COMPLETO` `[H01]` — PDF lido diretamente, inclusive o capítulo 20 e o Anexo I.

**O que é:** documento que **integra o regulamento do Pix**, publicado pelo Banco Central. A versão 7.4 é de setembro de 2026 e entra em vigor em **01/03/2027**. As obrigações se destinam a **aplicativos para pessoas naturais**, "haja vista tal público ser mais sensível à padronização de experiência do usuário", e são voltadas ao smartphone.

### 1.1 O capítulo 20 — Acessibilidade no Pix (páginas 133 e 134)

Os dois itens do capítulo são **recomendações**:

- **Deficiência auditiva:** vídeos curtos explicativos sobre o Pix em Libras e legendados, no formato de perguntas frequentes; possibilidade de uso de intérprete de Libras.
- **Deficiência visual:** práticas de desenvolvimento acessível integradas às ferramentas do próprio smartphone, com exemplos não exaustivos:
  - aumento do tamanho das áreas de toque de botões e ícones;
  - **descrição ativa** nos elementos de tela e funcionalidades;
  - **seleção de prioridades** das informações a serem lidas;
  - **descrições curtas e diretas**, para agilizar a navegação.

As telas ilustrativas mostram um botão de acessibilidade na tela principal do ambiente Pix, abrindo três opções: **vídeo explicativo em Libras, tema escuro e aumentar a fonte**.

**Leitura para o MEOL.** Três coisas se aproveitam direto:

1. **"Seleção de prioridades das informações a serem lidas"** é a informação em camadas escrita por um regulador: alguém decide o que o leitor de tela lê primeiro. No MEOL, a ordem de leitura é a mesma da tela: decisão → porquê → procedência.
2. **"Descrições curtas e diretas"** casa com o RI-01 (frase curta) e com o alfabetismo funcional medido na rodada 1.
3. **Acessibilidade como botão visível**, não como configuração escondida no menu do sistema.

**O que o capítulo NÃO traz, e continua sendo nosso:** contraste mínimo, tamanho de fonte, formatação numérica, daltonismo e como comunicar incerteza. O Pix não resolve isso; a referência para essas coisas continua sendo a WCAG, que fica como pendência de leitura.

### 1.2 O que as obrigações gerais ensinam (e valem mais)

| regra do Pix | o que diz | o que vira no MEOL |
|---|---|---|
| **erro com motivo nomeado** | as mensagens de erro devem ser específicas e evidenciar o motivo real (saldo, conta inexistente, falha técnica); quando o erro é do próprio participante, **isso deve ficar claro ao usuário** | **RI-17**: toda recusa do motor nomeia o motivo e diz de quem é a falha (dado, fonte ou do próprio MEOL) |
| **comprovante sem publicidade** | é vedado incluir propaganda, ofertas, hiperlinks ou qualquer conteúdo alheio à transação no comprovante | confirma o RI-08 |
| **texto de terceiro não vira link** | o campo "Descrição" não deve conter HTML; o app deve exibir os caracteres **literalmente** e não renderizar links nem conteúdo dinâmico | **RI-18**: texto vindo de fonte externa (nome de empresa, comentário, campo de dado) é exibido como texto, nunca renderizado |
| **sucesso que não engana** | a mensagem de sucesso do registro de chave **não deve induzir** o usuário a concluir que a chave é necessária para pagar | **RI-19**: a confirmação descreve exatamente o que aconteceu, e nada além |
| **cancelar antes de concluir** | deve haver funcionalidade de cancelamento antes da conclusão, para reduzir devoluções de transações equivocadas | o "executei" do MEOL tem desfazer antes de gravar |
| **conferência com dado íntegro** | antes de confirmar, mostrar nome, CPF mascarado, chave e valor; **a chave não pode ser mascarada**, porque o usuário precisa conferi-la | o que existe para ser conferido aparece inteiro |
| **mudou de dono, avisa** | se o contato salvo passou a ter outro nome ou CPF, o app deve alertar e **exigir confirmação** | o mesmo caso do A-03 (troca de código de negociação): se a empresa por trás do papel mudou de identidade, o MEOL alerta e pede confirmação |
| **crédito avisado antes** | se a transação usar linha de crédito, o usuário deve ser informado do valor e da linha antes de confirmar | avisar quando o aporte consome a reserva ou dinheiro comprometido |
| **consentimento que descreve** | ao registrar chave, informar exatamente o que outros usuários passarão a ver | ao ligar sincronização ou conta, dizer o que fica visível e para quem |
| **assimetria de risco** | reduzir limite: efetivado imediatamente. Aumentar: processado em 24 a 48 horas e sujeito a aprovação. Limites separados por período diurno e noturno, com teto do BC no Pix Saque | **RI-20**: no MEOL, o que reduz risco vale na hora; o que aumenta exposição tem carência declarada |
| **redução com efeito colateral** | se reduzir o limite inviabiliza agendamentos já feitos, o app avisa e pergunta se o usuário confirma | mudanças de perfil mostram o que quebram antes de aplicar |
| **reclamação a um toque** | atalho na tela inicial para o canal de atendimento, **sem etapas intermediárias**, e mensagem informando que a reclamação pode ir ao Banco Central | **RI-21**: canal de contato a um toque, e como reclamar fora do MEOL |
| **notificação com conteúdo mínimo** | quem, quanto, quando; no bloqueio cautelar, motivo, valor e prazo máximo de 72 horas | notificação mensal do MEOL com conteúdo mínimo e sem link |
| **Anexo I** | lista os itens cujas telas devem ser apresentadas no processo de verificação de aderência | checklist de telas por requisito, conferido a cada versão |

---

## 2. Pendências da rodada 2 — o que foi resolvido

### 2.1 Marcas que faltavam

| marca | resultado | código novo | status | fonte |
|---|---|---|---|---|
| **Caixa (Caixa Tem)** | app de política pública que bancarizou dezenas de milhões; usabilidade contestada, estudada em TCC de engenharia de software (2026) que analisa reclamações espontâneas na loja de apps | **MC-27** | `PARCIAL` | `[H02]` |
| **Suno** | declara "análises independentes... transparência total e sem conflitos de interesse" e, no mesmo grupo, tem gestora própria com 12 fundos; a Suno Asset lista como princípio o **reporte mensal com data-base e fonte** | **MC-28**, **MC-29** | `COMPLETO` (site oficial) | `[H03]` |
| **SPX** | gestora institucional sem marca voltada ao consumidor; nada a auditar pela lente RI-01..RI-16 | nenhum | `PARCIAL` | — |
| **Braun / Dieter Rams** | dez princípios do bom design: entre eles **honesto**, **compreensível**, **durável**, **discreto** e "o mínimo de design possível"; o lema é "menos, porém melhor" | **MC-26** | `PARCIAL` (fontes secundárias e catálogo) | `[H04]` |
| **Grand Seiko** | quatro pilares do relógio ideal: **precisão, legibilidade, durabilidade e beleza**; filosofia "The Nature of Time" | **MC-25** | `PARCIAL` | `[H05]` |
| **Leica** | lema "das Wesentliche" — nada além do essencial; a página de valores diz que o foco está primeiro na necessidade de quem usa | **MC-26** (reforço) | `COMPLETO` (site oficial) | `[H06]` |
| **Santander (Brasil)** | **não resolvido**: o que encontrei é de Portugal. Continua pendente | — | — | — |

**Códigos novos**

| código | nome | o que é | origem |
|---|---|---|---|
| **MC-25** | legibilidade como pilar | a legibilidade está entre os quatro pilares do produto, ao lado da precisão | Grand Seiko |
| **MC-26** | doutrina do essencial | remover tudo o que não serve a quem usa; design honesto, compreensível e durável | Leica, Braun/Rams |
| **MC-27** | app de política pública | inclusão financeira em massa com usabilidade contestada, e o canal oficial virando isca de golpe | Caixa Tem |
| **MC-28** | independência declarada com ecossistema próprio | a casa se diz independente e sem conflito, e ao mesmo tempo gere os próprios fundos | Suno |
| **MC-29** | reporte com data-base e fonte | o relatório mensal ao cotista informa a data-base e a fonte do número | Suno Asset |

**O MC-29 é o achado mais útil deste bloco:** procedência com data-base já é praticada por uma gestora brasileira. O MEOL não estaria inventando um padrão estranho ao mercado; estaria levando ao varejo um hábito que já existe no institucional.

**O MC-28 é o alerta:** dizer-se independente enquanto se vende produto próprio é exatamente a tensão que a rodada 2 encontrou na XP. Independência só é prova quando está na estrutura, e não no texto do "sobre".

### 2.2 Regra de saturação

Com as marcas desta rodada, são **27 auditadas**. A sequência final foi: Caixa (código novo), Suno (dois códigos novos), SPX (nenhum). A regra de três marcas seguidas sem código novo **continua sem ser atingida**.

**Decisão declarada:** encerro o bloco de marcas **por decisão**, não por saturação, porque os códigos financeiros estão repetindo e os requisitos derivados pararam de mudar. Fica registrado que a régua não fechou sozinha — é o mesmo cuidado da §6 da rodada 2, e não uma saturação disfarçada.

### 2.3 As outras pendências

| pendência | situação |
|---|---|
| **Data das regras da ANBIMA para influenciadores** | **Resolvida** `COMPLETO` `[H07]`: publicadas em 13/09/2023 e **em vigor desde 13/11/2023**. Valem para as instituições que seguem o Código de Distribuição: o influenciador deve informar quando o conteúdo é publicidade e citar a contratante; a instituição é corresponsável pelo conteúdo e deve garantir que ele tenha certificação quando houver recomendação ou análise |
| **Reclame Aqui** | **Parcialmente resolvida** `PARCIAL` `[H08]`: existe a categoria "Corretoras e Bancos de Investimentos", com ranking por reputação dos últimos seis meses. Um levantamento antigo (dados de 2017) indicava que os grandes bancos resolviam cerca de uma em cada cinco reclamações **sobre investimentos**, contra índices bem maiores nas corretoras. **O dado é velho e precisa ser refeito antes de virar argumento** |
| **Ranking do BC na fonte oficial** | **Não resolvida.** A metodologia está clara (reclamações procedentes por milhão de clientes, trimestral, lista dos 15 maiores), mas a consulta ao site do BC não foi feita nesta sessão. A divergência da imprensa sobre o 2º trimestre de 2026 continua `NAO_CONFIRMADO` |
| **MC-03 (PicPay, cofrinho do cartão eleva limite)** | **Não resolvida.** Continua em fonte secundária |
| **Nubank em inglês** | **Não resolvida.** A página lida continua sendo a versão em inglês |
| **Enquadramento regulatório dos bancos com IA (§4.1 da rodada 2)** | **Não resolvida, e não se resolve por pesquisa.** É parecer jurídico |

---

## 3. Requisitos novos

| código | requisito | origem |
|---|---|---|
| **RI-17** | toda recusa nomeia o motivo real e diz de quem é a falha: do dado, da fonte ou do próprio MEOL | Pix, obrigações gerais |
| **RI-18** | texto vindo de fonte externa é exibido literalmente, nunca renderizado como link ou conteúdo dinâmico | Pix, campo "Descrição" |
| **RI-19** | a mensagem de confirmação descreve exatamente o que foi feito, sem induzir conclusão mais ampla | Pix, registro de chave |
| **RI-20** | o que reduz exposição vale na hora; o que aumenta exposição tem carência declarada | Pix, gestão de limites |
| **RI-21** | canal de contato a um toque na tela principal, sem etapas intermediárias, e instrução de onde reclamar fora do MEOL | Pix, atalho de atendimento |

Com estes, a lista fechada da etapa de design é **RI-01 a RI-21**.

---

## 4. Limitações declaradas

1. **O capítulo de acessibilidade é recomendação.** Tratar os quatro itens dele como se fossem obrigação seria inventar norma.
2. **WCAG não lida nesta rodada.** Contraste, tamanho de alvo e daltonismo continuam sem fonte própria.
3. **Vigência futura:** a versão 7.4 só entra em vigor em 01/03/2027. Até lá vale a 7.1.
4. **SPX e Santander Brasil** continuam sem auditoria útil.
5. **O dado do Reclame Aqui sobre bancos e investimentos é de 2017**, citado em reportagem de 2018.

---

## 5. Fontes

Acesso em 20/09/2026.

- **[H01]** Banco Central do Brasil. *Requisitos Mínimos para a Experiência do Usuário* (Pix), versão 7.4, setembro de 2026, vigência a partir de 01/03/2027 — capítulo 2 (obrigações gerais), capítulos 3 a 11, capítulo 20 (Acessibilidade no Pix, p. 133–134) e Anexo I — https://static.poder360.com.br/uploads/2026/09/requisitos-minimos-experiencia-usuario-pix.pdf · versão 7.1 no site do BC: https://www.bcb.gov.br/content/estabilidadefinanceira/pix/Regulamento_Pix/versoes_futuras/IV_RequisitosMinimosparaExperienciadoUsuario-versao7-1.pdf
- **[H02]** OLIVEIRA, T. T. F. *Avaliação de usabilidade em aplicativos bancários digitais: um estudo de caso do Caixa Tem.* TCC, Engenharia de Software, UFC Quixadá, 2026 — https://repositorio.ufc.br/ri/bitstream/riufc/85770/1/2026_tcc_ttfoliveira.pdf · golpe usando canal oficial do Caixa Tem (imprensa): https://diariodocomercio.com.br/mix/?p=32897
- **[H03]** Grupo Suno — página institucional ("análises independentes", "sem conflitos de interesse") — https://www.suno.com.br/sobre/ · Suno Asset, princípio de transparência com reporte mensal, data-base e fonte: https://www.suno.com.br/asset/?p=1015
- **[H04]** Dieter Rams, dez princípios do bom design (Braun/Vitsœ) — https://domusweb.it/en/from-the-archive/2023/03/14/dieter-rams-and-the-10-principles-for-a-good-design.html · lista dos princípios: https://www.goodreads.com/book/show/13099439 · leitura em português: https://blakecrosley.com/pt-BR/blog/design-philosophy-dieter-rams
- **[H05]** Grand Seiko — "The Nature of Time" (site oficial) — https://www.grand-seiko.com/middleeast-en/special/thenatureoftime/ · os quatro pilares (precisão, legibilidade, durabilidade, beleza), fonte secundária: https://thehourmarkers.com/articles/pillars-of-grand-seiko
- **[H06]** Leica — Corporate Values, "Focus on the Essential" / "das Wesentliche" — https://leica-camera.com/en-SE/corporate-values
- **[H07]** ANBIMA — regras para contratação de influenciadores digitais, publicadas em 13/09/2023, em vigor desde 13/11/2023 — https://www.anbima.com.br/pt_br/imprensa/anbima-publica-regras-para-a-contratacao-de-influenciadores-digitais.htm · texto das regras: https://www.anbima.com.br/data/files/29/47/49/82/CDE8A810B1E0B8A8B82BA2A8/1.%20RP%20Influenciador%20digital_13.09.23.pdf
- **[H08]** Reclame Aqui — categoria "Corretoras e Bancos de Investimentos" — https://www.reclameaqui.com.br/segmentos/bancos-e-financeiras/corretoras-e-bancos-de-investimentos/ · InfoMoney (dados de 2017 sobre solução de reclamações de investimentos em bancos e corretoras): https://www.infomoney.com.br/?p=200312

---

## Notas de revisão

*26/09/2026 — trazido do Projeto no claude.ai para o repositório.*

- **N-COD.** C-nn → MC-nn e R-nn → RI-nn, só neste documento (tabela no cabeçalho). Motivo: os achados do projeto sobre o fator, o ajuste de proventos, a moeda e a ordem dos portões já usavam esses mesmos números com os prefixos C- e R-, e outros C/R já existiam em outros arquivos com outro sentido; os instrumentos `achados_ancorados` e `codigos_preservados` contariam todos como achados. Guardado por `auditoria/test_codigos_de_marca.py`.

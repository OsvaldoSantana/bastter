# Evidência empírica sobre desenho de pré-registro — avaliação de um sistema de 4 camadas para backtest de 8 estratégias

**Data do levantamento:** 13 de setembro de 2026
**Escopo:** meta-ciência do pré-registro, graus de liberdade do pesquisador, aderência a protocolos, psicologia da *accountability*, e literatura de *multiple testing* em finanças.

## Legenda de confiabilidade das fontes

| Marca | Significado |
|---|---|
| **[P]** | **Fonte primária lida** — extraí números e citações do PDF do artigo ou da página do editor |
| **[S]** | **Fonte secundária** — o número vem de outro artigo/página que cita o original; não li o original |
| **[NC]** | **NÃO CONFIRMADO** — mencionado na literatura, mas não verifiquei o dado diretamente |

Onde as fontes divergem, isso está sinalizado explicitamente. **Não há nenhum número neste relatório que eu não tenha extraído de uma fonte identificada.**

---

## Sumário executivo (leia isto primeiro)

A evidência sustenta **duas** das suas quatro camadas com força, é **ambígua** numa e **contraria parcialmente** a quarta.

1. **Especificação congelada (camada 1)** — apoiada, **mas com uma ressalva que atinge o seu caso diretamente**: em economia, pré-registro *sem* plano de análise detalhado não produziu nenhuma redução mensurável de p-hacking (Brodeur et al., 2024). O que funciona é o plano detalhado, não o ato de registrar.
2. **Graus de liberdade declarados (camada 2)** — a evidência diz que declarar **reduz de verdade**, mas apenas parcialmente e apenas se a declaração for específica. Nenhum estudo encontrou eliminação. A melhor evidência (Spitzer et al., 2026, um Registered Report) mostra restrição real — e, no mesmo estudo, 73,68% dos artigos ainda desviaram sem declarar.
3. **Registro de todas as execuções (camada 3)** — **esta é a sua camada mais bem sustentada**, e a sustentação vem de finanças, não de psicologia. Bailey & López de Prado são categóricos: um backtest sem o número de tentativas é "worthless". Você tem exatamente o insumo que o Deflated Sharpe Ratio exige. Mas você provavelmente não está usando esse insumo (ver §5 e §6).
4. **Alarme com justificativa escrita, em vez de trava (camada 4)** — **aqui a evidência CONTRARIA o seu desenho**, ou pelo menos não o apoia. A meta-análise de *process accountability* encontra efeito **negativo** em tarefas complexas (d ≈ −0,48). E Lerner & Tetlock documentam que a *accountability* pode **amplificar** o viés exatamente quando a opção enviesada é a mais fácil de justificar — que é a situação de quem quer rodar mais uma variante.

E o problema estrutural que atravessa tudo: **todo o benefício demonstrado na literatura vem de arranjos com um verificador externo** (revisão Stage 1 de um Registered Report, ou um registro público auditável). O seu sistema é auto-registro sem leitor. Isso não é um detalhe — é a variável que separa os estudos que acharam efeito dos que não acharam.

---

## 1. O pré-registro funciona? Evidência sobre falsos positivos e resultados positivos publicados

### 1.1 Registered Reports vs. literatura padrão — o resultado central

**[P] Scheel, A. M., Schijen, M. R. M. J., & Lakens, D. (2021). An Excess of Positive Results: Comparing the Standard Psychology Literature With Registered Reports. *Advances in Methods and Practices in Psychological Science*, 4(2), 1–12. DOI: 10.1177/25152459211007467.**
https://journals.sagepub.com/doi/10.1177/25152459211007467

Desenho: comparação observacional de **71 Registered Reports** contra **152 artigos padrão**, ambos 2013–2018. Artigos padrão vieram de 633 revistas listadas em "Psychiatry/Psychology" no Essential Science Indicators; os RRs, da base do Center for Open Science.

Resultado:

| | Hipóteses apoiadas | IC 95% |
|---|---|---|
| Registered Reports | **31/71 = 43,66%** | [31,91; 55,95] |
| Literatura padrão | **146/152 = 96,05%** | [91,61; 98,54] |

Ou seja: **4% dos artigos padrão falham em confirmar a primeira hipótese, contra 56% dos RRs.** (Esse enquadramento complementar é o usado por Chambers & Tzavella, 2022 — ver §1.3 — e bate exatamente com os números acima, o que serve de checagem cruzada.)

**Ressalvas declaradas pelos próprios autores [P]** — e elas importam para você:
- os codificadores não puderam ser cegos ao formato de publicação;
- o estudo é observacional, não experimental — **não permite inferência causal**;
- os artigos padrão foram selecionados pela expressão "test\* the hypothes\*", que aparecia em apenas 2 dos 71 RRs — possível viés de amostragem;
- **a probabilidade a priori das hipóteses testadas em cada formato pode ser diferente e isso não foi estudado.** (Esta é a objeção mais séria: RRs atraem desproporcionalmente replicações e hipóteses arriscadas. Parte da diferença de 52 pontos percentuais pode ser seleção de hipótese, não disciplina metodológica.)
- só a primeira hipótese de cada artigo foi avaliada.

### 1.2 Qualidade dos Registered Reports — e onde eles NÃO ganham

**[P] Soderberg, C. K., Errington, T. M., Schiavone, S. R., Bottesini, J., Thorn, F. S., Vazire, S., Esterling, K. M., & Nosek, B. A. (2021). Initial evidence of research quality of registered reports compared with the standard publishing model. *Nature Human Behaviour*, 5, 2021. DOI: 10.1038/s41562-021-01142-4.**
https://www.nature.com/articles/s41562-021-01142-4

**353 revisores** avaliaram **29 Registered Reports** pareados contra **57 artigos de comparação** (psicologia e neurociência), em 19 critérios, escala −4 a +4.

- RRs superaram os comparadores em **todos os 19 critérios**, diferença média **0,46**.
- Rigor metodológico: **0,99** [0,62; 1,35]
- Rigor analítico: **0,97** [0,60; 1,34]
- Qualidade geral: **0,66** [0,30; 1,02]
- **Novidade: 0,13 [−0,24; 0,49] — indistinguível de zero**
- **Criatividade: 0,22 [−0,14; 0,58] — indistinguível de zero**

**Leitura para você:** o pré-registro compra rigor, não compra descoberta. Se o seu objetivo com as 8 estratégias é *encontrar* algo novo, este é o custo documentado; se é *não se enganar*, é o benefício documentado.

### 1.3 Adoção e limites declarados pelos proponentes

**[P] Chambers, C. D., & Tzavella, L. (2022). The past, present and future of Registered Reports. *Nature Human Behaviour*, 6, 29–42. DOI: 10.1038/s41562-021-01193-7.**
https://www.nature.com/articles/s41562-021-01193-7 · manuscrito aceito aberto: https://orca.cardiff.ac.uk/id/eprint/145541/1/Chambers&Tzavella2021-MS.pdf

- **295 revistas** ofereciam RRs no momento da escrita; **483 artigos Stage 2** publicados em 81 veículos.
- Citam Scheel et al. e Soderberg et al. com os números acima.
- **Limitações que os próprios autores admitem:** RRs são *"neither a panacea nor a one-size-fits all solution"*; apenas **50% das revistas exigiam registro público do protocolo Stage 1 aceito** (dado de 2018); falta de padronização e especificidade insuficiente de hipóteses entre revistas; atrasos de meses na revisão Stage 1; formato inadequado para pesquisa exploratória.

### 1.4 Ensaios clínicos do NHLBI — o "experimento natural" do clinicaltrials.gov

**[P] Kaplan, R. M., & Irvin, V. L. (2015). Likelihood of Null Effects of Large NHLBI Clinical Trials Has Increased over Time. *PLOS ONE*, 10(8), e0132382. DOI: 10.1371/journal.pone.0132382.**
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0132382

- **55 ensaios** grandes financiados pelo NHLBI, período 1970–2012: **30 publicados antes de 2000**, **25 em 2000 ou depois**.
- Antes de 2000: **17/30 = 57%** mostraram benefício significativo.
- Depois de 2000: **2/25 = 8%** mostraram benefício significativo.
- χ² = 12,2, **p = 0,0005**.
- Todos os ensaios pós-2000 foram pré-registrados no ClinicalTrials.gov; **nenhum** dos pré-2000 foi registrado prospectivamente.

**Ressalva textual dos autores [P]:** *"We cannot say that trend toward null trials to preregistration in ClinicalTrials.gov is causal. Our analysis included only a small number of trials and the design of the study does not allow causal inferences."* Acrescentam que *"many variables may have changed around the year 2000"* e que as conclusões podem não generalizar para além de ensaios financiados pelo NHLBI nem para pesquisa patrocinada pela indústria.

**Ceticismo honesto:** este é o achado mais citado a favor do pré-registro e é, na verdade, **n = 55 sem controle**. A queda de 57% para 8% é dramática demais para ser só pré-registro; mudanças em padrão de cuidado, poder estatístico e escolha de comparadores ativos no período são explicações concorrentes não descartadas. Trate-o como sugestivo, não como prova.

### 1.5 Meta-ciência pós-2020 — onde a evidência fica desconfortável

Aqui está a parte que quase nunca aparece em defesas do pré-registro, e que é a mais relevante para você.

**[P] Brodeur, A., Cook, N. M., Hartley, J. S., & Heyes, A. (2024). Do Pre-Registration and Pre-Analysis Plans Reduce p-Hacking and Publication Bias? Evidence from 15,992 Test Statistics and Suggestions for Improvement. I4R Discussion Paper Series No. 101, Institute for Replication.**
https://pure-oai.bham.ac.uk/ws/portalfiles/portal/217870300/do_pre_registration_I4R.pdf · https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4180594

Amostra: **15.992 estatísticas de teste**, **314 artigos** de RCTs em **15 revistas líderes de economia**, **2018–2021**. Dos 314, **83 eram pré-registrados** — **44 com plano de análise (PAP)** e **39 pré-registrados sem PAP**.

Resumo verbatim: *"(a) Pre-registration frequently does not involve a pre-analysis plan (PAP), or sufficient detail to constrain meaningfully the actions and decisions of researchers after data is collected. Consistent with this, **we find no evidence that pre-registration in itself reduces p-hacking and publication bias**. (b) When pre-registration is accompanied by a PAP we find evidence consistent with both reduced p-hacking and publication bias."*

- Viés de publicação estimado: **1,38×** para estudos com PAP vs **2,09×** para pré-registrados sem PAP.
- Pré-registro sem PAP: *"no discernible difference"* na distribuição das estatísticas de teste.

**[P] van den Akker, O. R., van Assen, M. A. L. M., Bakker, M., Elsherif, M., Wong, T. K., & Wicherts, J. M. (2023/2024). Preregistration in practice: A comparison of preregistered and non-preregistered studies in psychology. *Behavior Research Methods*, 56(6). DOI: 10.3758/s13428-023-02277-0.**
https://link.springer.com/article/10.3758/s13428-023-02277-0

**193 estudos pré-registrados pareados com 193 não pré-registrados.**

| Métrica | Pré-registrados | Não pré-registrados | p |
|---|---|---|---|
| Proporção de resultados significativos | 0,69 (DP 0,38) | 0,68 (DP 0,25) | **0,96** |
| Tamanho de efeito (r transformado) | 0,29 (DP 0,24) | 0,36 (DP 0,25) | **0,175** |
| Inconsistências estatísticas grosseiras | — | — | 0,671 |
| Análise de poder realizada | **55%** | **23%** | <0,0001 |
| Tamanho de amostra médio | **959** | 536,6 | 0,0002 |

Conclusão dos autores, verbatim: *"we did not find robust evidence that preregistration prevents p-hacking and HARKing."*

**Divergência entre fontes — declare-a, não a resolva.** Scheel et al. (RRs, com revisão Stage 1 antes dos resultados) acham um efeito enorme. van den Akker et al. (pré-registro comum, sem porteiro) não acham efeito nenhum sobre significância ou tamanho de efeito. Brodeur et al. reconciliam parcialmente: **o efeito depende de haver um plano de análise detalhado**. A leitura mais defensável hoje é que "pré-registro" não é uma coisa só, e a versão fraca dele — a versão mais parecida com a sua, auto-administrada e sem revisão — é a versão sem evidência de efeito.

### 1.6 Um aviso caro: o estudo retratado

**[P] Retraction Note (24 de setembro de 2024). *Nature Human Behaviour*.**
https://www.nature.com/articles/s41562-024-01997-3
Artigo retratado: Protzko, J., Krosnick, J., Nelson, L., Nosek, B. A., et al. (2023). High replicability of newly discovered social-behavioural findings is achievable. *Nature Human Behaviour*, 8, 311–319. DOI: 10.1038/s41562-023-01749-9.

Este era um dos artigos-bandeira pós-2020 alegando que práticas "rigor-enhancing" (incluindo pré-registro) produzem alta replicabilidade. Foi retratado. Motivos declarados pelos editores [P]:
1. *"lack of transparency and misstatement of the hypotheses and predictions the reported meta-study was designed to test"*;
2. *"lack of preregistration for measures and analyses supporting the titular claim (against statements asserting preregistration in the published article)"*;
3. *"selection of outcome measures and analyses with knowledge of the data"*;
4. *"incomplete reporting of data and analyses"*.

Todos os autores concordaram com a retratação especificamente por causa das *"incorrect statements of preregistration"*, discordando dos demais pontos.

**Por que isto importa para você:** o artigo que dizia que o pré-registro salva a replicabilidade foi retratado porque **afirmou ter pré-registrado o que não pré-registrou**. Um pré-registro alegado não é um pré-registro verificado. Se o seu sistema é auto-atestado, ele carrega exatamente esse modo de falha.

---

## 2. Graus de liberdade do pesquisador: declarar antes reduz, ou apenas documenta?

### 2.1 A magnitude do problema

**[P] Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-Positive Psychology: Undisclosed Flexibility in Data Collection and Analysis Allows Presenting Anything as Significant. *Psychological Science*, 22(11), 1359–1366. DOI: 10.1177/0956797611417632.**
https://journals.sagepub.com/doi/10.1177/0956797611417632 · PDF: https://journals.sagepub.com/doi/pdf/10.1177/0956797611417632

**O que mediram:** taxas de falso positivo simuladas quando o pesquisador dispõe de quatro graus de liberdade comuns, com α nominal de 5%.

| Grau de liberdade | Taxa de falso positivo a p < 0,05 |
|---|---|
| (A) Duas variáveis dependentes | **9,5%** |
| (B) Adicionar 10 observações por célula | **7,7%** |
| (C) Controlar por gênero / interação | **11,7%** |
| (D) Descartar uma de três condições | **12,6%** |
| A + B | **14,4%** |
| A + B + C | **30,9%** |
| **A + B + C + D** | **60,7%** |

**Magnitude:** com quatro graus de liberdade banais e não declarados, o α real vai de 5% para **~61%** — mais de 12× o nominal. Os autores resumem: *"A researcher is more likely than not to falsely detect a significant effect."*

Demonstração empírica ("When I'm Sixty-Four"): participantes que ouviram a música ficaram *quase um ano e meio mais novos* pela data de nascimento — médias ajustadas de 20,1 vs 21,5 anos, **F(1, 17) = 4,92, p = 0,040**.

As **seis exigências para autores** [P]: (1) decidir a regra de parada antes da coleta; (2) mínimo de 20 observações por célula ou justificar; (3) listar **todas** as variáveis coletadas; (4) reportar **todas** as condições experimentais; (5) reportar resultados com e sem as observações eliminadas; (6) reportar análises com e sem covariáveis. Mais quatro diretrizes para revisores, incluindo *"tolerate imperfect results"* e exigir testes de robustez para decisões analíticas arbitrárias.

**Nota de transferência para finanças:** a regra 2 (n ≥ 20 por célula) não transfere. As regras 3, 4, 5 e 6 transferem diretamente — "reportar todas as variantes rodadas, com e sem os filtros" é exatamente a sua camada 3.

### 2.2 A checklist de 34 graus de liberdade

**[P] Wicherts, J. M., Veldkamp, C. L. S., Augusteijn, H. E. M., Bakker, M., van Aert, R. C. M., & van Assen, M. A. L. M. (2016). Degrees of Freedom in Planning, Running, Analyzing, and Reporting Psychological Studies: A Checklist to Avoid p-Hacking. *Frontiers in Psychology*, 7:1832. DOI: 10.3389/fpsyg.2016.01832.**
https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.01832/full

**34 graus de liberdade**, distribuídos em 5 fases: hipotetizar (2), desenho (6), coleta de dados (4), **análise (15)**, relato (6).

Posição dos autores sobre pré-registro [P] — e ela é mais nuançada do que costuma ser citada:
- *"the preferred way to counter bias due to researcher degrees of freedom is to preregister the study in a way that no longer allows researchers to exploit them"* — ou seja, a ambição é **prevenir**, não documentar;
- **mas**: *"maneuverability remains if preregistrations are not sufficiently specific, precise, or exhaustive"*.

O pré-registro ideal precisa ser **específico, preciso E exaustivo**, cobrindo *"all potential contingencies"*. Sem os três, sobra manobra.

### 2.3 O jardim dos caminhos que se bifurcam

**[P] Gelman, A., & Loken, E. (14 de novembro de 2013). The garden of forking paths: Why multiple comparisons can be a problem, even when there is no "fishing expedition" or "p-hacking" and the research hypothesis was posited ahead of time. Columbia University / Penn State (working paper).**
https://sites.stat.columbia.edu/gelman/research/unpublished/forking.pdf

O argumento central, e é o mais importante desta seção para o seu caso: **o problema não exige que você tenha rodado múltiplas análises.**

Verbatim [P]:
- *"it is possible to have multiple potential comparisons... without the researcher performing any conscious procedure of fishing"*;
- o pesquisador faz *"a single test based on the data, but in an environment where a different test would have been performed given different data"*;
- *"absent pre-registration, our data analysis choices will be data-dependent, even when they are motivated directly from theoretical concerns."*

Recomendações dos autores [P]: (1) pré-registro do protocolo completo de coleta e análise antes de olhar os dados; (2) replicação pré-publicação — estudo exploratório seguido de confirmatório com protocolo predeterminado; (3) **analisar todas as comparações relevantes**, não só as significativas.

**Implicação direta:** o seu contador de variantes conta variantes *executadas*. Gelman & Loken dizem que o espaço relevante inclui as variantes que você **teria** rodado se os dados tivessem saído diferentes. Um contador de execuções subestima sistematicamente o M verdadeiro. Isso é uma limitação estrutural do seu desenho, não um bug corrigível por disciplina.

### 2.4 A resposta empírica à sua pergunta: reduz ou só documenta?

Três estudos atacam isso diretamente. **A resposta é "reduz um pouco, e só se for muito específico — e nunca elimina".**

**[P] Bakker, M., Veldkamp, C. L. S., van Assen, M. A. L. M., Crompvoets, E. A. V., Ong, H. H., Nosek, B. A., Soderberg, C. K., Mellor, D., & Wicherts, J. M. (2020). Ensuring the quality and specificity of preregistrations. *PLOS Biology*, 18(12): e3000937. DOI: 10.1371/journal.pbio.3000937.**
https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000937

**106 pré-registros** (53 em formato não estruturado, 52 estruturado), codificados contra **29 graus de liberdade** em cinco fases.

- Escore mediano de transparência (escala 0–3): **estruturado 0,81 vs não estruturado 0,57**; Cliff's Delta = **0,49** (efeito grande).
- **22 dos 29** graus de liberdade melhoraram direcionalmente no formato estruturado; **apenas 5 dos 29** atingiram significância após correção.
- Escores de 3 (especificação exaustiva) foram *"rare"* em ambos os formatos; **oito graus de liberdade pontuaram perto de 0**, *"hardly addressed at all"*.
- Concordância entre codificadores sobre a clareza da hipótese: **apenas 14%** sobre a contagem de hipóteses.
- Conclusão verbatim: ***"neither eliminated all researcher degrees of freedom"*** e *"effective preregistration is challenging"*.

**[P] Spitzer, L., Kroeger, A., & Mueller, S. (2026). Stage 2 Registered Report: Restriction of Researcher Degrees of Freedom Through the Psychological Research Preregistration-Quantitative Template. *Advances in Methods and Practices in Psychological Science*. DOI: 10.1177/25152459261432216.**
https://journals.sagepub.com/doi/10.1177/25152459261432216

Este é o estudo mais próximo de um teste direto da sua camada 2 — e é ele próprio um Registered Report (recomendado pelo Peer Community in Registered Reports), o que o torna a evidência metodologicamente mais forte disponível.

Amostra: **103 pré-registros PRP-QUANT** (29 revisados por pares, 74 não) comparados com **52 pré-registros com o template padrão do OSF**; **19 publicações associadas** examinadas para aderência.

- Pré-registros PRP-QUANT são **mais restritivos** que os do template OSF: Z = 0,25, **p < 0,001**, MdnD = 0,22.
- **18 dos 23** graus de liberdade testados individualmente estavam mais restritos no PRP-QUANT; **17 atingiram significância**.
- Pré-registros PRP-QUANT **revisados por pares** restringiram mais que os não revisados: Z = 0,22, p < 0,001, MdnD = 0,25.
- **E, no entanto: 73,68% dos artigos associados continham desvios não declarados.**

**Veredito para a sua pergunta.** Declarar graus de liberdade antes **reduz de fato** a flexibilidade — isto está medido, é direcional e é consistente (Bakker: 22/29; Spitzer: 18/23). Mas:
- a redução é **parcial** — nenhum estudo observou eliminação;
- ela depende de **estrutura imposta** (template detalhado > formulário livre), não da intenção;
- ela é **maior quando alguém revisa** o pré-registro antes (Spitzer);
- e ela **não impede o desvio na execução** — 73,68% desviaram sem declarar mesmo com o melhor template.

Portanto: *declarar reduz o espaço de manobra ex ante; não garante a conduta ex post.* Se o seu sistema só declara e não verifica, você comprou a primeira metade.

---

## 3. O pré-registro é frequentemente desviado? (Sim. É a regra, não a exceção.)

Esta é a seção com a evidência mais uniforme e mais desconfortável do relatório. **Cinco estudos independentes, cinco disciplinas, o mesmo resultado.**

### 3.1 Ensaios clínicos — o projeto COMPare

**[P] Goldacre, B., Drysdale, H., Dale, A., Milosevic, I., Slade, E., Hartley, P., Marston, C., Powell-Smith, A., Heneghan, C., & Mahtani, K. R. (2019). COMPare: a prospective cohort study correcting and monitoring 58 misreported trials in real time. *Trials*, 20:118. DOI: 10.1186/s13063-019-3173-2.**
https://trialsjournal.biomedcentral.com/articles/10.1186/s13063-019-3173-2

Escopo: **67 ensaios**, nas cinco principais revistas médicas (NEJM, *The Lancet*, JAMA, BMJ, *Annals of Internal Medicine*), publicados entre **19 de outubro e 30 de novembro de 2015**, cada um comparado ao seu protocolo/registro.

- **76,3%** dos desfechos primários foram reportados corretamente como primários.
- **19,4% dos ensaios** tinham **ao menos um desfecho primário pré-especificado não reportado**.
- Dos **818 desfechos secundários pré-especificados**, apenas **55,1% foram reportados** (≈367 não reportados).
- **365 desfechos novos foram reportados sem declaração**, média de **5,4 por ensaio**.

Site do projeto (dados dinâmicos): https://www.compare-trials.org/

### 3.2 Psicologia — a primeira geração de pré-registros

**[P] Claesen, A., Gomes, S., Tuerlinckx, F., & Vanpaemel, W. (2021). Comparing dream to reality: an assessment of adherence of the first generation of preregistered studies. *Royal Society Open Science*, 8(10): 211037. DOI: 10.1098/rsos.211037.**
https://royalsocietypublishing.org/doi/10.1098/rsos.211037

Escopo: **todos** os 27 estudos publicados com o badge "Preregistered" em *Psychological Science* entre fevereiro de 2015 e novembro de 2017 (23 artigos). Os achados foram enviados aos autores correspondentes para comentário.

- **2 de 27 (7%)** não continham desvio nenhum do plano pré-registrado.
- **25 de 27 (93%)** continham pelo menos um desvio.
- **1 estudo (4%)** divulgou todos os desvios.
- **9 estudos (36%)** não divulgaram nenhum desvio.
- Desvios concentrados em: **tamanho de amostra reportado, critérios de exclusão e análise estatística**.
- Recomendação dos autores: *"vague preregistration plans allow for too much wiggle room and do not contribute to transparency"*; modelos estatísticos devem ser pré-registrados *"as specifically as possible"*.

### 3.3 Ciência política e economia — planos de análise prévia

**[P] Ofosu, G. K., & Posner, D. N. (2021). Pre-Analysis Plans: An Early Stocktaking. *Perspectives on Politics*. DOI: 10.1017/S1537592721000931.**
https://www.cambridge.org/core/journals/perspectives-on-politics/article/preanalysis-plans-an-early-stocktaking/94E7FAE76001C45A04E8F5E272C773CE

Escopo: **195 PAPs** registrados nos registros EGAP e AEA entre **2011–2016**; **93** resultaram em artigos publicamente disponíveis. Composição: 63% experimentos de campo, 27% surveys, 4% laboratório, 4% observacional.

**Completude da especificação:**
| Elemento | % claramente especificado |
|---|---|
| Variáveis independentes / de tratamento | 93% |
| Variáveis dependentes primárias | 77% |
| Modelo estatístico preciso | 68% |
| Variáveis de controle | **56%** (44% ambíguas) |
| Estimação de erros-padrão | **37%** |
| Tratamento de dados faltantes / atrito | **25%** |
| Procedimento para não conformidade | **13%** |
| Tratamento de outliers | **8%** |

**Desvios, entre os 93 artigos:**
- Apresentaram fielmente os resultados de **todas** as hipóteses primárias pré-registradas: **apenas 61%**.
- **Mais de um terço** omitiu ao menos uma hipótese pré-registrada.
- Taxa mediana de omissão: **25%** de todas as hipóteses pré-especificadas.
- **18%** dos artigos testaram hipóteses não pré-registradas; **82% desses não declararam**.

Os próprios autores leem o copo como *"half full rather than half empty"*: *"just over half of the 195 PAPs... were judged to meet all four"* requisitos de completude, e outro terço satisfez três dos quatro. **Aqui há divergência interpretativa genuína na literatura**: os mesmos números são lidos por Ofosu & Posner como progresso e por Brodeur et al. como evidência de que o pré-registro típico "does not... constrain meaningfully the actions and decisions of researchers". Não escolho lado — registro que a divergência é sobre o *padrão de comparação*, não sobre os fatos.

### 3.4 Estudos sobre jogos de azar — especificidade e aderência

**[P] Heirene, R., LaPlante, D., Louderback, E., Keen, B., Bakker, M., Serafimovska, A., & Gainsbury, S. (2024). Preregistration specificity and adherence: A review of preregistered gambling studies and cross-disciplinary comparison. *Meta-Psychology*. DOI: 10.15626/MP.2021.2909.**
https://open.lnu.se/index.php/metapsychology/article/view/2909

- **53 pré-registros** de estudos sobre jogo; **20 artigos/preprints associados** avaliados quanto à aderência.
- **13 dos 20 (65%)** desviaram do protocolo **sem divulgação**.
- Média de desvios não declarados: **2,25 por artigo** (DP = 2,34).
- Comparação com 52 pré-registros de outras disciplinas: os de jogo pontuaram mais alto em 12 de 29 itens.
- Conclusão verbatim: *"our findings suggest the purported benefits of preregistration—including increasing transparency and reducing RDoF—are not fully achieved by current practices."*

### 3.5 Consolidação

| Estudo | Domínio | n | Taxa de desvio / não divulgação |
|---|---|---|---|
| Claesen et al. 2021 | Psicologia | 27 estudos | **93% com desvio**; 36% não divulgaram nenhum |
| Heirene et al. 2024 | Jogo | 20 artigos | **65% desviaram sem divulgar** |
| Spitzer et al. 2026 | Psicologia | 19 publicações | **73,68% com desvios não declarados** |
| Ofosu & Posner 2021 | Ciência política | 93 artigos | 39% omitiram ≥1 hipótese; 82% dos testes novos não declarados |
| Goldacre et al. 2019 | Medicina | 67 ensaios | 365 desfechos novos não declarados (5,4/ensaio) |

**Resposta à sua pergunta crítica: sim, o desvio é a regra.** Entre 65% e 93% dos estudos pré-registrados desviam, e a não divulgação é majoritária em todas as amostras. Sua premissa — "se o desvio é a regra, um registro que só documenta não protege" — está **empiricamente correta**.

Mas há uma assimetria a favor do seu caso que precisa ser dita: em **todos** esses estudos, o desvio é ocultado porque existe um **leitor a enganar** (revisor, editor, financiador, comunidade). Você não tem leitor. Isso remove o incentivo a ocultar — e remove, pelo mesmo movimento, qualquer detecção. Ver §4.

---

## 4. Alarme vs. trava: existe evidência?

**Resposta curta: não existe evidência empírica direta sobre regras rígidas vs. regras com justificativa escrita em metodologia de pesquisa. Encontrei zero estudos.** O que existe é a literatura de *accountability* em psicologia da decisão, que é adjacente — e que, lida com honestidade, **não apoia o seu desenho e em parte o contraria**.

### 4.1 O framework canônico

**[P] Lerner, J. S., & Tetlock, P. E. (1999). Accounting for the effects of accountability. *Psychological Bulletin*, 125(2), 255–275.**
https://jenniferlerner.com/wp-content/uploads/2017/07/45.Accounting-for-the-effects-of-accountability.pdf

A conclusão central é **condicional**, não geral. *Accountability* não melhora o julgamento; ela melhora **alguns** julgamentos sob **algumas** condições.

**Quando melhora [P]:** *"Predecisional accountability to an unknown audience will improve judgment to the extent that a given bias results from lack of effort, self-critical awareness of one's judgment processes... or both."* Mecanismo: **crítica preemptiva de si mesmo** (*preemptive self-criticism*) — o indivíduo considera múltiplas perspectivas e antecipa contra-argumentos antes de se comprometer.

**Quando não tem efeito [P]:** *"Predecisional accountability to an unknown audience will have no effect on bias if, even after increased attention to one's decision process, no new ways of solving the problem come into awareness."* Tipicamente quando o que falta é treinamento formal em regras de decisão (raciocínio bayesiano, utilidade esperada).

**Quando PIORA [P]** — e este é o ponto que atinge o seu alarme:
1. quando as escolhas envolvem *"options easiest to justify"* (efeitos de compromisso, aversão à ambiguidade);
2. quando o julgamento se apoia em informação normativamente irrelevante: *"accountability to an unknown audience will amplify indiscriminate use of information in prediction tasks"*.

**Distinção crítica de audiência [P]:** audiência com visões **desconhecidas** → crítica preemptiva e complexidade cognitiva. Audiência com visões **conhecidas** → conformidade e deslocamento de atitude na direção da audiência.

**Aplicação direta ao seu contador-alarme.** Duas leituras, ambas legítimas:
- *A favor:* exigir justificativa escrita antes de gastar uma variante é *predecisional accountability*, o formato que Lerner & Tetlock associam à crítica preemptiva. Se o seu viés vem de falta de esforço e de autoconsciência (que é exatamente o viés que Simmons et al. e Gelman & Loken descrevem), a condição de benefício está satisfeita.
- *Contra, e mais forte:* a sua audiência é **você mesmo, com visões perfeitamente conhecidas**. Esse é o caso em que Lerner & Tetlock preveem conformidade com a audiência, não crítica. Pior: "rodar mais uma variante" é precisamente a opção mais fácil de justificar — sempre há uma razão metodológica plausível para testar outra janela, outro filtro, outro universo. Pelo critério (1) acima, isso é o caso em que *accountability* **amplifica** o viés. Um requisito de justificativa escrita pode funcionar como **máquina de produzir licenças**, não como freio.

**[NC]** Tetlock, P. E., & Boettger, R. (1989). "Accountability: A social magnifier of the dilution effect", *Journal of Personality and Social Psychology* — localizei o artigo (https://pubmed.ncbi.nlm.nih.gov/2778629/) mas **não consegui ler o texto**; cito apenas como referência à mesma linha de achado, já coberta pela revisão de 1999 acima, que essa sim li.

### 4.2 Accountability de processo vs. de resultado — e a contradição direta

Esta é a literatura mais próxima de "exigir justificativa escrita do processo", que é exatamente o seu alarme.

**[P] de Langhe, B., van Osselaer, S. M. J., & Wierenga, B. (2011). The effects of process and outcome accountability on judgment process and performance. *Organizational Behavior and Human Decision Processes*, 115, 238–252. DOI: 10.1016/j.obhdp.2011.02.003.**
https://www.colorado.edu/business/sites/default/files/attached-files/obhdp_2011_de_langhe_van_osselaer_wierenga.pdf

- *Process accountability* **melhorou** o desempenho em tarefas **elementares (lineares)**: Estudo 1, t(127) = 2,67, p < 0,05; Estudo 2, t(79) = 2,33, p < 0,05.
- *Process accountability* **não teve vantagem alguma em tarefas configurais (interativas)**: t(127) = 0,51, **p > 0,61**.
- Mecanismo: a *process accountability* impulsiona o uso de **abstração de pistas** (raciocínio analítico sobre relações pista-resultado individuais), *"but not exemplar-based processing"*. Abstração de pistas só funciona quando as pistas têm efeitos independentes e aditivos. Em tarefas em que as pistas interagem multiplicativamente, a memória baseada em exemplares funciona melhor — e a *process accountability* não a melhora.

**[P] Sharon, Drach-Zahavy, & Srulovici (2022). The Effect of Outcome vs. Process Accountability-Focus on Performance: A Meta-Analysis. *Frontiers in Psychology*, 13:795117. DOI: 10.3389/fpsyg.2022.795117.**
https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.795117/full

Meta-análise de **7 estudos / 9 experimentos / 1.080 participantes**:
- Efeito global: **nulo** — média = **−0,09**, IC 95% [−0,21; 0,03].
- **Tarefas complexas: accountability de RESULTADO superior — média = −0,48, IC 95% [−0,62; −0,33].**
- Tarefas simples: accountability de processo superior — média = **0,96**, IC 95% [0,72; 1,20].
- Conclusão: *"accountability focus by itself cannot serve as a sole motivator"* — a complexidade da tarefa modera a relação.

**Este é o achado que CONTRARIA a sua camada 4.** Backtestar 8 estratégias contra uma série de fatores comum é, por qualquer definição razoável, uma tarefa **complexa/configural**: as escolhas interagem (janela × filtro × universo × tratamento de custos), não são aditivas e independentes. Nesse regime:
- de Langhe et al.: *process accountability* não traz benefício (p > 0,61);
- a meta-análise: *process accountability* é **pior** que a de resultado, d ≈ −0,48.

A justificativa escrita é *accountability* de processo. A evidência disponível diz que, para tarefas desse tipo, ela não ajuda e pode atrapalhar, e que o que ajuda é ser responsabilizado pelo **resultado** — que, no seu caso, é o desempenho *out-of-sample* real, não a qualidade do raciocínio registrado.

**[NC]** Existe um artigo relevante — "Justifying the judgment process affects neither judgment accuracy, nor strategy use", *Judgment and Decision Making* (2022) — cujo título indica um **resultado nulo** sobre justificar o processo. Não consegui acessar o texto (robots.txt e erro 500 em duas rotas). Registro-o como pista não confirmada, não como evidência: https://journal.sjdm.org/17/17411/jdm17411.html

### 4.3 "Gaming" de regras rígidas

**Procurei e não encontrei evidência empírica primária** sobre pesquisadores burlando regras metodológicas rígidas. O que existe é a literatura de Campbell's law e Goodhart's law aplicada a métricas — mas as fontes que localizei são blogs e material de divulgação, **não estudos primários** sobre regras metodológicas. **Não vou citá-las como evidência.** Se alguém lhe disser que "há literatura mostrando que travas rígidas são burladas", peça a citação: eu não a encontrei.

O que **existe** e é adjacente: o único achado empírico relevante é que travas rígidas em pesquisa (a regra Stage 1 dos Registered Reports, que é a trava mais dura que existe) produzem os maiores efeitos medidos (§1.1, §1.2) — o que é evidência **a favor da trava**, não do alarme. E, ao mesmo tempo, Chambers & Tzavella [P] listam os custos reais da trava: atrasos de meses e inadequação para trabalho exploratório.

### 4.4 O argumento conceitual a favor do alarme (que é argumento, não evidência)

Os dois textos programáticos mais citados do campo apoiam a ideia de que desvio ≠ invalidação:

**[P] Lakens, D. (2019). The value of preregistration for psychological science: A conceptual analysis. *Japanese Psychological Review*, 62(3), 221–230.**
https://team1mile.com/sjpr62-3/wp-content/uploads/2020/03/Lakens_JPR623221-230.pdf
*(**[NC]** o DOI que uma das extrações me devolveu era implausível — pertencia a outro periódico. Não confirmei o DOI. Volume, número, páginas e ano estão confirmados no cabeçalho do PDF.)*

- *"Preregistration itself does not make a study better or worse compared to a non-preregistered study. Instead, it merely allows researchers to transparently evaluate the severity of a test."*
- Sobre desvios: *"A switch in the analysis strategy reduces the severity of the test for the researcher who did not predict the exploratory analysis, but other researchers do not necessarily need to agree."*
- *"When there is analytic flexibility p-values can no longer be used as a statistical tool to make decisions about the presence or absence of meaningful effects."*
- Rejeita a avaliação binária do pré-registro: o que importa é a **severidade** do teste, avaliada continuamente.

**[S] Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606. DOI: 10.1073/pnas.1708274114.**
https://www.pnas.org/doi/10.1073/pnas.1708274114
*(Marcado **[S]**: o texto completo me foi negado por 403 em quatro rotas. A citação bibliográfica está confirmada via página do Center for Open Science que a reproduz integralmente: https://www.cos.io/blog/improving-the-quality-and-specificity-of-preregistration. **Não li o artigo**; o argumento predição-vs-postdição é atribuído a ele na literatura secundária, mas não verifiquei as frases.)*

**Resumo honesto da §4:** o seu alarme é **defensável conceitualmente** (Lakens: severidade é contínua, não binária) e **não apoiado empiricamente**. A única evidência quantitativa que encontrei aponta na direção oposta para tarefas complexas. Isto não significa que a trava seja melhor — significa que **você está operando fora do alcance da evidência**, e deveria saber disso.

---

## 5. O diário de execuções: há precedente em finanças e estatística?

**Sim, e é o pilar mais sólido do seu desenho.** A exigência de reportar o número de tentativas é literatura estabelecida em finanças quantitativas, com formalização matemática.

### 5.1 O Deflated Sharpe Ratio

**[P] Bailey, D. H., & López de Prado, M. (2014). The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality. *The Journal of Portfolio Management*, 40(5), 94–107.**
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551 · PDF: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf

O DSR corrige o Sharpe por duas fontes de inflação: **viés de seleção por testes múltiplos** e **não normalidade dos retornos**. Ajuda a *"separate legitimate empirical findings from statistical flukes"*.

Papel de **N** (número de configurações independentes testadas): *"as the number of independent trials (N) grows, so will grow the expected maximum"* Sharpe, **mesmo quando não há nenhuma habilidade real**.

Sobre a obrigação de reportar N, verbatim [P]:
> *"Without this information, it is impossible to assess the relevance of a backtest. Put bluntly, a backtest where the researcher has not controlled for the extent of the search involved in his or her finding is **worthless**."*

> *"Investors and journal referees should demand this information whenever a backtest is submitted to them."*

E sobre por que um holdout não basta: o método de holdout *"ignores the rise in false positives as more trials occur"*. Em presença de efeitos de memória, *"backtest overfitting will lead to loss maximization"* — não a desempenho zero, mas a **retorno esperado negativo** fora da amostra.

### 5.2 Quantos testes são "muitos"? Os números concretos

**[P] Bailey, D. H., Borwein, J. M., López de Prado, M., & Zhu, Q. J. (2014). Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance. *Notices of the American Mathematical Society*, 61(5), 458–471.**
https://www.ams.org/notices/201405/rnoti-p458.pdf · PDF espelho: https://www.davidhbailey.com/dhbpapers/backtest-pseudo.pdf

Resumo verbatim [P]: *"We prove that high simulated performance is easily achievable after backtesting a relatively small number of alternative strategy configurations... Because most financial analysts and academics rarely report the number of configurations tried for a given backtest, investors cannot evaluate the degree of overfitting in most investment proposals."*

Os números que importam para você:

> **[P]** *"if the researcher tries only N = 10 alternative configurations of an investment strategy, he or she is expected to find a strategy with a Sharpe ratio IS of **1.57**, despite the fact that all strategies are expected to deliver a Sharpe ratio of zero OOS"*

**Minimum Backtest Length (MinBTL)**, Teorema 3.1 [P] — em anos:

MinBTL ≈ [ (1−γ)·Z⁻¹(1 − 1/N) + γ·Z⁻¹((1 − 1/N)e⁻¹) / E[max_N] ]²

Aproximação acessível [P]: **MinBTL < 2·ln[N] / E[max_N]²**

Exemplo trabalhado, verbatim [P]:
> *"if only 5 years of data are available, **no more than 45 independent model configurations should be tried**, or we are almost guaranteed to produce strategies with an annualized Sharpe ratio IS of 1, but an expected Sharpe ratio OOS of zero."*

E a frase que é literalmente a justificativa da sua camada 3 [P]:
> *"A researcher that does not report the number of trials N used to identify the selected backtest configuration makes it impossible to assess the risk of overfitting."*

### 5.3 A literatura de multiple testing em finanças: é preciso conhecer M

**[P] Harvey, C. R., Liu, Y., & Zhu, H. (2014/2016). … and the Cross-Section of Expected Returns. NBER Working Paper 20592 / *The Review of Financial Studies*, 29(1), 5–68.**
https://www.nber.org/system/files/working_papers/w20592/w20592.pdf · https://academic.oup.com/rfs/article/29/1/5/1843824

- Catalogaram **316 fatores** distintos em 313 trabalhos publicados e working papers selecionados — e afirmam que isto **subestima** a população real de fatores.
- Recomendação central, verbatim: *"a newly discovered factor needs to clear a much higher hurdle, with a **t-ratio greater than 3.0**."* Com ajustes mais conservadores para dados faltantes, os limiares vão de **3,18 a 4,01**.
- Sobre o M invisível, verbatim: *"we do not observe the factors that were tested but failed to pass the usual significance levels and were never published."* Estimam que **~71% de todos os fatores testados estão ausentes** da amostra, existindo apenas em trabalho não publicado ou abandonado.

**Esta é a justificativa mais forte para registrar execuções abandonadas.** O problema que Harvey, Liu & Zhu identificam na literatura acadêmica de finanças — 71% dos testes são invisíveis — é exatamente o problema que a sua camada 3 resolve para o seu próprio caso. Você seria, nesse sentido, mais rigoroso que a literatura publicada.

**[P] Harvey, C. R. (2017). Presidential Address: The Scientific Outlook in Financial Economics. *The Journal of Finance*, 72(4), 1399–1440. DOI: 10.1111/jofi.12530.**
https://people.duke.edu/~charvey/Research/Published_Papers/P131_The_scientific_outlook.pdf

- *"Reporting select results that have low p-values makes it impossible to interpret the analysis. Such practice amounts to p-hacking and borders on academic fraud."*
- *"Report all results, not just a selection of significant results."*
- *"Before looking at the data, establish a research framework... The research framework should be transparent to all researchers. There is a growing trend in other sciences to post all these choices online before the experiment is conducted."*
- **[P]** Nota de precisão: Harvey **não** faz uma afirmação quantitativa própria sobre a proporção de achados falsos em finanças; ele referencia Ioannidis (2005). Cuidado com citações secundárias que atribuem um número a ele.

**[S] Sullivan, R., Timmermann, A., & White, H. (1999). Data-Snooping, Technical Trading Rule Performance, and the Bootstrap. *The Journal of Finance*, 54(5), 1647–1691.**
**[S] White, H. (2000). A Reality Check for Data Snooping. *Econometrica*, 68(5), 1097–1126.**
https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00163 · https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152

*(Marcados **[S]**: as duas rotas diretas aos PDFs falharam — robots.txt e certificado SSL expirado. Os números abaixo vêm de um artigo que os reexamina: https://www.chesler.us/resources/academia/reexamine_ta_profitability.pdf)*

- Sullivan, Timmermann & White testaram um universo de **7.846 regras de negociação**. O artigo secundário observa: *"Although 7846 is a large number, this collection of rules is far from a 'full universe.'"*
- Ponto metodológico central: o Reality Check testa a hipótese conjunta *max E(f_k) ≤ 0* sobre **todas as k regras**, em vez de testes individuais que inflam o erro Tipo I.
- *"To properly quantify the effect of data snooping, White's Reality Check requires constructing a 'full universe' of trading rules."*

### 5.4 A alternativa ao contador: reportar a curva inteira

**[P] Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). Specification curve analysis. *Nature Human Behaviour*, 4, 1208–1214. DOI: 10.1038/s41562-020-0912-z.**
https://www.nature.com/articles/s41562-020-0912-z · PDF: https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/33-Simonsohn-Simmons-Nelson-2020.pdf

Diagnóstico [P]: *"researchers must make a number of data analytic decisions, many of which are both arbitrary and defensible"*, e *"people in general, and researchers in particular, are more likely to report evidence consistent with the claims they are trying to make than to report evidence that is inconsistent."*

Frase-chave [P]: *"The standard errors around published effect sizes represent the sampling error inherent in a particular analysis, but they do not reflect the error caused by the arbitrary and/or motivated selection of specifications."*

Os três passos: (1) identificar **todas** as especificações razoáveis — teoricamente justificadas, estatisticamente válidas e não redundantes; (2) exibir os resultados de todas descritivamente, com um painel mostrando quais decisões analíticas dirigem a variação; (3) inferência conjunta sobre o conjunto todo.

**Por que isto importa para o seu desenho:** a análise de curva de especificação **dissolve o dilema alarme-vs-trava**. Se você roda *todas* as especificações declaradas e reporta a distribuição inteira, o número de variantes deixa de ser um recurso escasso a ser racionado — e portanto não precisa nem de alarme nem de trava. O contador existe porque você trata cada execução como um custo. Se a execução é obrigatória e o reporte é conjunto, o custo desaparece.

---

## 6. Avaliação crítica do seu desenho

### 6.1 Camada 1 — Especificação congelada

**Apoiada, com uma condição que provavelmente você não satisfaz.**

- ✅ Apoia: Scheel et al. (43,66% vs 96,05%), Soderberg et al. (rigor +0,99), Kaplan & Irvin (57% → 8%, com ressalva causal dos autores).
- ⚠️ **Condiciona:** Brodeur et al. — pré-registro **sem** plano de análise detalhado: *"no evidence that pre-registration in itself reduces p-hacking and publication bias"*. Só com PAP há efeito (viés 1,38× vs 2,09×).
- ⚠️ **Condiciona:** Wicherts et al. — precisa ser *"specific, precise, and exhaustive"*, cobrindo *"all potential contingencies"*; caso contrário *"maneuverability remains"*.
- ❌ **Contraria parcialmente:** van den Akker et al. — 193 pares, **nenhuma diferença** em proporção de resultados significativos (0,69 vs 0,68, p = 0,96) nem em tamanho de efeito (p = 0,175). Pré-registro na prática comum não preveniu p-hacking nem HARKing.

**Diagnóstico:** "congelar a especificação" não é uma categoria única. A versão que funciona na literatura é a versão **detalhada, estruturada e exaustiva**. A versão que não funciona é a versão nominal. Nada no que você descreveu me diz em qual das duas você está — e essa é a variável decisiva.

### 6.2 Camada 2 — Graus de liberdade declarados

**Apoiada, com magnitude modesta e efeito que não se estende à execução.**

- ✅ Apoia: Spitzer et al. 2026 — templates detalhados restringem **18 de 23** graus de liberdade (17 significativos); efeito maior ainda quando há revisão por pares.
- ✅ Apoia: Bakker et al. 2020 — formato estruturado com transparência mediana 0,81 vs 0,57, Cliff's Δ = 0,49.
- ⚠️ **Limita:** Bakker et al. — *"neither eliminated all researcher degrees of freedom"*; apenas **5 de 29** diferenças sobreviveram à correção; **8 dos 29** graus de liberdade foram *"hardly addressed at all"* em ambos os formatos.
- ❌ **Contraria estruturalmente:** Gelman & Loken — o espaço de bifurcações inclui as análises que você **teria feito com outros dados**. Uma lista *ex ante* de graus de liberdade é necessariamente incompleta, porque as bifurcações contingentes não são enumeráveis por introspecção. *"data-analysis choices will be data-dependent, even when they are motivated directly from theoretical concerns."*

**Resposta direta à sua pergunta ("reduz mesmo, ou só documenta?"):** **reduz mesmo — mas menos do que documenta, e nunca até zero.** A evidência de redução real existe e é de boa qualidade (Spitzer é um Registered Report). Mas em nenhum estudo a declaração eliminou a flexibilidade, e o mecanismo de Gelman & Loken garante que não poderia.

### 6.3 Camada 3 — Registro de todas as execuções, inclusive abandonadas

**Fortemente apoiada. É a melhor parte do seu sistema.**

- ✅ Bailey & López de Prado: um backtest sem N reportado é *"worthless"*.
- ✅ Bailey et al. (AMS): N = 10 já produz Sharpe *in-sample* esperado de **1,57** com Sharpe OOS zero; com 5 anos de dados, **>45** configurações independentes praticamente garantem um Sharpe de 1 que é ruído.
- ✅ Harvey, Liu & Zhu: ~71% dos fatores testados são invisíveis à literatura; t > 3,0 (até 4,01) precisamente por isso.
- ✅ Harvey (2017): *"Report all results, not just a selection of significant results."*
- ✅ Sullivan/Timmermann/White e White: avaliar o melhor contra o **universo inteiro** de regras buscadas. **[S]**
- ✅ Simmons et al., exigências 3–6: reportar todas as variáveis, todas as condições, com e sem exclusões, com e sem covariáveis.

**Mas há um erro que o seu desenho quase certamente comete.** Você tem 8 estratégias contra **a mesma** série de fatores. O N que entra no DSR é o número de tentativas **independentes**. Tentativas altamente correlacionadas (mesma série, variantes vizinhas) não contam como N separados; usar a contagem bruta **superestima** a deflação e pode levá-lo a descartar algo real. Inversamente, se você conta apenas "variantes permitidas" e ignora as bifurcações implícitas (Gelman & Loken), você **subestima** N e se ilude. Os dois erros coexistem e não se cancelam de forma conhecida. Isto precisa ser tratado explicitamente, por clusterização das tentativas correlacionadas — não por contagem ingênua.

**E o ponto que separa você da literatura, para melhor:** Harvey, Liu & Zhu **não conseguem** saber o M real; você **pode**. O seu diário é, em princípio, uma vantagem informacional genuína sobre a literatura publicada de finanças. Aproveite-a: use o N para **computar** algo (DSR, MinBTL, limiar de t), não apenas para arquivar.

### 6.4 Camada 4 — Alarme com justificativa escrita, não trava

**Não apoiada. Parcialmente contrariada.**

- ❌ **Contraria:** Sharon et al. 2022 (meta-análise, 1.080 participantes) — em **tarefas complexas**, *process accountability* é **pior** que *outcome accountability*: **−0,48** [−0,62; −0,33]. Efeito global nulo: −0,09 [−0,21; 0,03].
- ❌ **Contraria:** de Langhe et al. 2011 — em tarefas **configurais**, *process accountability* não traz vantagem alguma: t(127) = 0,51, **p > 0,61**. O mecanismo (abstração de pistas) só funciona quando os efeitos são independentes e aditivos — o que backtesting não é.
- ❌ **Contraria:** Lerner & Tetlock 1999 — a *accountability* **amplifica** o viés quando a opção enviesada é *"easiest to justify"*. "Rodar mais uma variante" é sempre a opção mais fácil de justificar. E a sua audiência é você mesmo, com visões conhecidas — o caso em que Lerner & Tetlock preveem **conformidade**, não crítica preemptiva.
- 🔇 **Silente:** nenhum estudo compara regras rígidas vs. regras com justificativa em metodologia de pesquisa. Zero. Se alguém alegar o contrário, exija a citação.
- ⚠️ **Evidência indireta a favor da TRAVA:** o arranjo com a trava mais dura que existe em ciência (Stage 1 dos Registered Reports, onde a decisão de publicação precede os resultados) é o arranjo com os maiores efeitos medidos — Scheel (43,66% vs 96,05%) e Soderberg (rigor +0,99). E, dentro do estudo de Spitzer, **os pré-registros revisados por pares restringiram mais** que os não revisados (Z = 0,22, p < 0,001).
- ✅ **A favor conceitualmente (argumento, não evidência):** Lakens — severidade é contínua, não binária; um desvio reduz a severidade *para quem não o previu*, sem invalidar automaticamente.

**Diagnóstico franco:** esta camada é a racionalização de uma preferência, não uma escolha apoiada em dados. Ela pode estar certa — a evidência é escassa e de domínio adjacente. Mas você deve saber que ela é a única das quatro camadas onde a evidência disponível aponta contra.

### 6.5 O problema transversal: não há leitor

Este é o achado mais importante do relatório e ele não está em nenhuma seção isolada — emerge do conjunto.

Observe o padrão:

| Arranjo | Verificador externo? | Efeito medido |
|---|---|---|
| Registered Reports (Stage 1 revisado) | **Sim** | Enorme (Scheel, Soderberg) |
| Pré-registro **com** PAP detalhado | Sim (registro auditável) | Moderado (Brodeur: 1,38× vs 2,09×) |
| Pré-registro PRP-QUANT **revisado por pares** | **Sim** | Maior restrição (Spitzer, p < 0,001) |
| Pré-registro **sem** PAP | Não | **Nenhum** (Brodeur) |
| Pré-registro comum, OSF, auto-administrado | Não | **Nenhum** em significância/efeito (van den Akker) |

**A variável que separa as linhas com efeito das linhas sem efeito não é o congelamento. É o verificador.** O seu sistema tem quatro camadas e nenhum verificador.

E Lerner & Tetlock dizem por que isso importa mecanicamente: o benefício da *accountability* vem de **audiência com visões desconhecidas, antes da decisão**. Auto-responsabilização, com audiência perfeitamente conhecida, é a configuração mais fraca do modelo — e é a configuração em que a *accountability* conforma em vez de criticar.

Some a isso a taxa de desvio: 65%–93% desviam, e a maioria não declara, **mesmo quando há um leitor para pegá-los**. Não é razoável supor que você, sem leitor, ficará abaixo dessa faixa.

### 6.6 Onde a evidência é simplesmente SILENTE

Seja explícito sobre isto ao usar este relatório:

- **Nenhum estudo** sobre pré-registro por pesquisador solo / investidor individual. Toda a literatura é sobre pesquisa institucional com publicação como recompensa.
- **Nenhum estudo** com estratégias de investimento como objeto do pré-registro. A literatura de finanças (Bailey, Harvey) trata de *correção estatística ex post* para número de tentativas, não de *pré-registro ex ante*. São tradições distintas que o seu desenho está tentando fundir — e essa fusão não tem precedente avaliado.
- **Nenhum RCT do pré-registro em si.** Todos os estudos de §1 e §3 são observacionais. Spitzer et al. é um Registered Report, mas o desenho é comparação observacional de templates. Kaplan & Irvin dizem explicitamente que não permitem inferência causal.
- **Nenhuma evidência** sobre se registrar tentativas abandonadas **muda o comportamento** (em oposição a permitir uma correção estatística depois). Bailey e Harvey argumentam que o N deve ser reportado; ninguém testou se manter o diário torna o pesquisador mais disciplinado.
- **Nenhuma evidência** sobre contadores de variantes, orçamentos de tentativas, ou qualquer mecanismo parecido com a sua camada 4.

### 6.7 Recomendações concretas, cada uma ancorada numa fonte

1. **Arranje um leitor, ou um relógio.** Deposite a especificação congelada num registro público com carimbo de tempo (o OSF aceita qualquer pessoa, gratuitamente) antes de rodar. Isto converte auto-documentação em *accountability* a uma audiência de visões desconhecidas — a condição exata que Lerner & Tetlock identificam como necessária para a crítica preemptiva. Sem isso, a evidência de van den Akker e Brodeur prevê efeito nulo.
2. **Use um template estruturado, não um documento livre.** Bakker et al.: estruturado 0,81 vs livre 0,57. Spitzer et al.: 18/23 graus de liberdade mais restritos com template detalhado.
3. **Não confie na auto-declaração de desvios.** 73,68% (Spitzer), 93% (Claesen), 65% não declarados (Heirene). Faça o sistema **diferenciar automaticamente** a configuração executada contra a especificação congelada, e registrar o diff sem passar pela sua vontade. Um desvio detectado por código não depende da sua honestidade num momento de entusiasmo.
4. **Transforme N num número que entra na decisão, não num número arquivado.** Compute o Deflated Sharpe Ratio e verifique o MinBTL. Com 5 anos de dados, >45 configurações independentes praticamente garantem Sharpe 1 espúrio (Bailey et al.). Faça a clusterização das tentativas correlacionadas antes de usar N — suas 8 estratégias sobre a mesma série de fatores não são 8 tentativas independentes.
5. **Considere trocar o contador-alarme por uma curva de especificação.** Rode todas as variantes declaradas e reporte a distribuição inteira (Simonsohn et al., 2020). Isto elimina a necessidade de racionar variantes — e portanto elimina o dilema alarme-vs-trava, cuja resolução não tem apoio empírico de qualquer lado.
6. **Adicione accountability de RESULTADO, não só de processo.** A meta-análise (Sharon et al.) diz que, em tarefas complexas, a responsabilização por resultado supera a por processo (−0,48 a favor da de resultado). Pré-comprometa-se com uma janela *out-of-sample* e com um critério de abandono da estratégia, e registre o resultado real — não apenas a qualidade do seu raciocínio escrito.
7. **Cuidado com o holdout como falsa segurança.** López de Prado: o holdout *"ignores the rise in false positives as more trials occur"*, e sob efeitos de memória o overfitting leva a **retorno esperado negativo**, não a zero.
8. **Leia o aviso da retratação.** O artigo que alegava que o pré-registro produz alta replicabilidade foi retratado por, entre outras coisas, *"incorrect statements of preregistration"*. Um pré-registro auto-atestado e não verificável é exatamente o objeto que falhou ali.

---

## Índice de fontes

**Fontes primárias lidas [P]**

1. Scheel, Schijen & Lakens (2021). *AMPPS*, 4(2), 1–12. DOI: 10.1177/25152459211007467 — https://journals.sagepub.com/doi/10.1177/25152459211007467
2. Soderberg, Errington, Schiavone, Bottesini, Thorn, Vazire, Esterling & Nosek (2021). *Nature Human Behaviour*, 5. DOI: 10.1038/s41562-021-01142-4 — https://www.nature.com/articles/s41562-021-01142-4
3. Chambers & Tzavella (2022). *Nature Human Behaviour*, 6, 29–42. DOI: 10.1038/s41562-021-01193-7 — https://www.nature.com/articles/s41562-021-01193-7
4. Kaplan & Irvin (2015). *PLOS ONE*, 10(8), e0132382. DOI: 10.1371/journal.pone.0132382 — https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0132382
5. Brodeur, Cook, Hartley & Heyes (2024). I4R DP No. 101 — https://pure-oai.bham.ac.uk/ws/portalfiles/portal/217870300/do_pre_registration_I4R.pdf
6. van den Akker, van Assen, Bakker, Elsherif, Wong & Wicherts (2023/2024). *Behavior Research Methods*, 56(6). DOI: 10.3758/s13428-023-02277-0 — https://link.springer.com/article/10.3758/s13428-023-02277-0
7. Retraction Note (2024). *Nature Human Behaviour* — https://www.nature.com/articles/s41562-024-01997-3
8. Simmons, Nelson & Simonsohn (2011). *Psychological Science*, 22(11), 1359–1366. DOI: 10.1177/0956797611417632 — https://journals.sagepub.com/doi/10.1177/0956797611417632
9. Wicherts, Veldkamp, Augusteijn, Bakker, van Aert & van Assen (2016). *Frontiers in Psychology*, 7:1832. DOI: 10.3389/fpsyg.2016.01832 — https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.01832/full
10. Gelman & Loken (2013). Working paper, Columbia/Penn State — https://sites.stat.columbia.edu/gelman/research/unpublished/forking.pdf
11. Bakker, Veldkamp, van Assen, Crompvoets, Ong, Nosek, Soderberg, Mellor & Wicherts (2020). *PLOS Biology*, 18(12), e3000937. DOI: 10.1371/journal.pbio.3000937 — https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000937
12. Spitzer, Kroeger & Mueller (2026). *AMPPS*. DOI: 10.1177/25152459261432216 — https://journals.sagepub.com/doi/10.1177/25152459261432216
13. Goldacre, Drysdale, Dale, Milosevic, Slade, Hartley, Marston, Powell-Smith, Heneghan & Mahtani (2019). *Trials*, 20:118. DOI: 10.1186/s13063-019-3173-2 — https://trialsjournal.biomedcentral.com/articles/10.1186/s13063-019-3173-2
14. Claesen, Gomes, Tuerlinckx & Vanpaemel (2021). *Royal Society Open Science*, 8(10), 211037. DOI: 10.1098/rsos.211037 — https://royalsocietypublishing.org/doi/10.1098/rsos.211037
15. Ofosu & Posner (2021). *Perspectives on Politics*. DOI: 10.1017/S1537592721000931 — https://www.cambridge.org/core/journals/perspectives-on-politics/article/preanalysis-plans-an-early-stocktaking/94E7FAE76001C45A04E8F5E272C773CE
16. Heirene, LaPlante, Louderback, Keen, Bakker, Serafimovska & Gainsbury (2024). *Meta-Psychology*. DOI: 10.15626/MP.2021.2909 — https://open.lnu.se/index.php/metapsychology/article/view/2909
17. Lerner & Tetlock (1999). *Psychological Bulletin*, 125(2), 255–275 — https://jenniferlerner.com/wp-content/uploads/2017/07/45.Accounting-for-the-effects-of-accountability.pdf
18. de Langhe, van Osselaer & Wierenga (2011). *OBHDP*, 115, 238–252. DOI: 10.1016/j.obhdp.2011.02.003 — https://www.colorado.edu/business/sites/default/files/attached-files/obhdp_2011_de_langhe_van_osselaer_wierenga.pdf
19. Sharon, Drach-Zahavy & Srulovici (2022). *Frontiers in Psychology*, 13:795117. DOI: 10.3389/fpsyg.2022.795117 — https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.795117/full
20. Bailey & López de Prado (2014). *The Journal of Portfolio Management*, 40(5), 94–107 — https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
21. Bailey, Borwein, López de Prado & Zhu (2014). *Notices of the AMS*, 61(5), 458–471 — https://www.ams.org/notices/201405/rnoti-p458.pdf
22. Harvey, Liu & Zhu (2014/2016). NBER WP 20592 / *RFS*, 29(1), 5–68 — https://www.nber.org/system/files/working_papers/w20592/w20592.pdf
23. Harvey (2017). *The Journal of Finance*, 72(4), 1399–1440. DOI: 10.1111/jofi.12530 — https://people.duke.edu/~charvey/Research/Published_Papers/P131_The_scientific_outlook.pdf
24. Simonsohn, Simmons & Nelson (2020). *Nature Human Behaviour*, 4. DOI: 10.1038/s41562-020-0912-z — https://www.nature.com/articles/s41562-020-0912-z
25. Lakens (2019). *Japanese Psychological Review*, 62(3), 221–230 — https://team1mile.com/sjpr62-3/wp-content/uploads/2020/03/Lakens_JPR623221-230.pdf

**Fontes secundárias [S]**

26. Nosek, Ebersole, DeHaven & Mellor (2018). *PNAS*, 115(11), 2600–2606. DOI: 10.1073/pnas.1708274114 — citação confirmada via https://www.cos.io/blog/improving-the-quality-and-specificity-of-preregistration; **texto não lido** (403 em quatro rotas).
27. Sullivan, Timmermann & White (1999). *JF*, 54(5), 1647–1691; e White (2000). *Econometrica*, 68(5), 1097–1126 — números via https://www.chesler.us/resources/academia/reexamine_ta_profitability.pdf
28. Devezer, Navarro, Vandekerckhove & Buzbas (2021). *Royal Society Open Science*, 8, 200805. DOI: 10.1098/rsos.200805 — https://royalsocietypublishing.org/doi/full/10.1098/rsos.200805 — **apenas o resumo acessível**; a tese central é que as reformas metodológicas *"suffer from similar mistakes and over-generalizations"* que os problemas que tentam corrigir. Não pude verificar as passagens específicas sobre pré-registro.

**NÃO CONFIRMADO [NC]**

29. DOI de Lakens (2019) — uma extração automática devolveu um DOI implausível, de outro periódico. Volume/número/páginas/ano confirmados no cabeçalho do PDF; **DOI não confirmado**.
30. Tetlock & Boettger (1989), "Accountability: A social magnifier of the dilution effect", *JPSP* — localizado em https://pubmed.ncbi.nlm.nih.gov/2778629/, **texto não acessado**. O achado está coberto pela revisão de Lerner & Tetlock (1999), essa sim lida.
31. "Justifying the judgment process affects neither judgment accuracy, nor strategy use", *Judgment and Decision Making* (2022) — https://journal.sjdm.org/17/17411/jdm17411.html — **inacessível** (robots.txt; erro 500). O título sugere resultado nulo relevante para a §4; **não use como evidência sem verificar**.
32. Campbell's law / Goodhart's law aplicadas a regras metodológicas rígidas — **não encontrei fonte primária**. As fontes localizadas eram blogs e material de divulgação. Não cito como evidência.
33. Estatísticas do painel dinâmico do site compare-trials.org — carregam por JavaScript e não pude lê-las; os números do COMPare neste relatório vêm do artigo publicado em *Trials* (fonte 13).
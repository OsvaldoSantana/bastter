# Relatório por peça — acertos, erros e melhorias

**Objeto:** os quatro relatórios de pesquisa, avaliados individualmente.
**Emissão:** 01/09/2026. Complementa o laudo consolidado de 01/09/2026, que tratou dos achados que cruzam arquivos e dos dois scripts.
**Método:** leitura de cada arquivo; recálculo independente onde havia aritmética; conferência de cada conclusão contra a fonte que ela declara. Nenhuma fonte externa foi acessada — os achados são de consistência interna e são reproduzíveis por leitura.
**Limite:** auditoria de método. Não avalio mérito de investimento e não emito recomendação de produto ou instituição.

**Nota de escala.** As contagens de linha do registro conferem exatamente: 898, 905, 457, 1.236.

---

# 1. `pesquisa-cofrinhos.md` — 898 linhas

**Veredito: a peça de melhor execução aritmética das quatro, com um defeito de documentação que quebra a própria reprodutibilidade.**

## 1.1 Acertos

**Toda a aritmética confere.** Recomputei os números derivados a partir das séries mensais que o arquivo lista, sem usar os totais dele:

| Grandeza | Relatório | Meu recálculo |
|---|---:|---:|
| Poupança acumulada 12 m | 8,3144% | **8,3144%** |
| CDI acumulado 12 m | 14,5707% | **14,5707%** |
| Diferença | 6,26 p.p. | **6,26 p.p.** |
| Poupança / CDI | ~57% | **57,1%** |
| 0,6455% a.m. anualizado | ~8,03% | **8,03%** |
| (1,005 × 1,001448) − 1 | 0,6455% | **0,645524%** |

A última linha merece destaque: é uma **invariante entre a lei e o dado publicado**. A Lei 12.703/2012 diz 0,5% a.m. + TR quando a Selic supera 8,5%; a série 226 dá a TR; a série 25 dá a poupança. As três fecham. Isso não é conferência de conta — é verificação de que a fórmula legal produz o número oficial, e é exatamente o tipo de teste que o manual do projeto pede.

**A auto-correção documentada em §5.2 é o item mais valioso do conjunto inteiro.** O arquivo registra que a primeira tentativa compôs doze registros *diários* consecutivos da série 25, obtendo 8,2753%, e que isso é metodologicamente incorreto porque a série tem aniversários no dia 1. **Publicar o próprio erro com o valor errado ao lado** é raro e é o que permite a um terceiro confiar no resto.

**A distinção conta de pagamento / RDB / CDB (§1.3)** resolve com precisão jurídica a confusão mais cara do varejo digital: saldo em conta de pagamento **não** é crédito coberto pelo FGC; a proteção vem de segregação e lastro, que é outra coisa. E a leitura estrutural que vem junto — dentro do limite do FGC, escolher quem paga 120% em vez de 100% é quase de graça porque o risco foi socializado; acima do limite a lógica se inverte por completo — é a explicação causal do caso Master, não a narrativa dele.

**"O prazo que ninguém divulga" (§2.3).** As 48 horas úteis do FGC contam do fim do processo. O relógio que importa vai da liquidação até o nome aparecer na lista do liquidante, e é discricionário. Master liquidado em 18/11/2025, pagamentos iniciados em 19/01/2026: **62 dias corridos**. Converte um prazo de marketing em prazo real com evidência datada.

**Tesouro Reserva (§4.0)** identificado como produto novo, com mínimo de R$ 1,00 e 100% da Selic — reserva de emergência com risco soberano competindo com caixinha de fintech, sem depender de FGC. Achado genuíno, obtido na fonte primária.

**A limitação de §2.4 declarada com o payload literal.** O buscador de normativos do BCB devolveu `{"navegacao":null,...,"conteudo":[]}`. O arquivo mostra a resposta vazia e conclui: trate como indício forte, não como citação normativa. É a forma certa de reportar um `NÃO OBTIDO`.

**A regra do aniversário (§5.3)** com o cenário certo: a poupança cobra o preço mais alto exatamente no uso que ela alega servir. Sacar no 29º dia rende zero — não é multa, é ausência de crédito.

## 1.2 Erros

**C-01 · A tributação declarada em §6.1 contradiz as tabelas 6.2–6.4. Crítico.**

§6.1 declara: *"IR (Lei 11.033/2004): 22,5% (30 dias e 182 dias); 20% (365 dias); 15% (730 dias)"*.

Recomputei a alíquota implícita nas tabelas, somando rendimento líquido + IR pago e comparando com o ganho bruto:

| Horizonte | Ganho bruto recalculado | Líquido + IR (tabelas) | Alíquota implícita | Declarada em §6.1 |
|---|---:|---:|---:|---:|
| 30 dias | 10,90 | 10,90 | **22,5%** | 22,5% ✓ |
| 182 dias | 67,24 | 67,24 | **20,0%** | 22,5% ✗ |
| 365 dias | 139,00 | 139,01 | **17,5%** | 20% ✗ |
| 730 dias | 297,32 | 297,32 | **15,0%** | 15% ✓ |

**As tabelas estão certas e a declaração está errada.** As faixas da Lei 11.033/2004 são até 180 dias 22,5%; de 181 a 360 dias 20%; de 361 a 720 dias 17,5%; acima de 720 dias 15%. Os cálculos usaram exatamente essas; o texto do método listou outras duas.

O efeito não é numérico — é de auditabilidade. Um terceiro que reproduza pelo método declarado obtém valores diferentes dos publicados e conclui que a peça está errada, quando não está. Num documento cujo critério de aceite é a reprodutibilidade por terceiro, esse é o defeito mais caro possível.

**C-02 · Poupança projetada constante sem faixa de sensibilidade.** §6.1 projeta 0,6455% a.m. constante. O próprio §5.2, três páginas antes, mostra a série oscilando entre 0,6213% e 0,6767% nos últimos 14 meses. A premissa está declarada, mas a variação já medida não foi aproveitada.

**C-03 · A seção 6 está duplicada no arquivo.** Os cabeçalhos `# SEÇÃO 6 — COMPARAÇÃO LÍQUIDA` e `## 6.1 Insumos e método — declarados` aparecem duas vezes seguidas. Defeito de montagem, não de conteúdo.

**C-04 · §2.4 é integralmente fonte secundária, e a fragilidade não é repetida onde é usada.** O número que muda o mercado — contribuição adicional de 0,01% para 0,02% — vem de InfoMoney e Seu Dinheiro. A ressalva está impecável na seção. Mas a conclusão de §1.2 ("o mercado estima em torno de 120% do CDI como limite prático") herda a fragilidade sem repeti-la.

**C-05 · Precisão limítrofe no IOF.** §6.1 diz "IOF ZERO em todos os horizontes, pois todos ≥ 30 dias". Correto — a tabela regressiva do IOF vai até o 29º dia. Mas a coluna se chama "30 dias" e o leitor apressado lê "isento a partir de 30 dias" como se 30 fosse o limiar de dentro, não de fora. Vale uma linha.

## 1.3 Melhorias

1. **Corrigir §6.1** e substituir a lista por uma tabela das quatro faixas legais com a base (Lei 11.033/2004, art. 1º), marcada como leitura e não como cálculo.
2. **Faixa de sensibilidade** na §6 usando o mínimo e o máximo já observados (0,6213%–0,6767%), em vez de ponto único.
3. **Automatizar a invariante da poupança:** `(1+0,005)·(1+TR) ≈ série 25` deve virar teste diário no repositório. Foi conferido à mão uma vez; é a classe de verificação que deve rodar sozinha.
4. Deduplicar a seção 6.
5. Repetir a marca `PARCIAL — fonte secundária` em §1.2, onde o número de §2.4 é usado.

---

# 2. `pesquisa-corretoras.md` — 905 linhas

**Veredito: a peça com o achado de maior consequência para o projeto, e a que mais se aproxima da fronteira entre levantamento e recomendação.**

## 2.1 Acertos

**§C.3 é o achado mais importante do relatório, e o arquivo tem razão em dizer isso.** Ação, ETF, BDR e FII ficam na Central Depositária da B3, em conta individualizada no CPF; a corretora é agente de custódia, não dona. Quebra de corretora é transtorno operacional, não perda patrimonial. O que sustenta a conclusão são **três fontes convergindo**: o Portal do Investidor da CVM (texto sobre liquidação extrajudicial e STVM, prazo de dois dias úteis), a própria tabela de custódia da B3 (que calcula por CPF, "em um único custodiante" — prova independente da individualização), e a tabela de transferência (0,0000% por determinação regulatória). E fecha com uma verificação que o leitor pode fazer sozinho hoje, na Área do Investidor.

**§C.4 documenta a divergência em vez de escolher em silêncio.** A BSM diz R$ 200 mil, com base no art. 124 da Resolução CVM 135/2022; a página de notícias da própria B3 ainda diz R$ 120 mil; a XP descreve a transição entre os dois. O arquivo adota R$ 200 mil, justifica (norma + página da administradora) e registra que a B3 está desatualizada. Isso é auditoria, não pesquisa.

**§E.2 desmonta "corretagem zero" mecanismo a mecanismo**, com documento para cada um: RLP como contraparte da ordem (Genial, XP, Terra), modelo fee-based declarado (Warren), restrição de canal (Rico, NuInvest, bancões), plataformas pagas (Genial, R$ 41,40 a R$ 140,40/mês) e mínimos punitivos de mesa (Inter R$ 50, Rico R$ 50, Safra 0,5% + R$ 25). E encerra no lugar certo: spread de renda fixa, rebate e float **não confirmados em nenhuma instituição** — lacuna estrutural de transparência do setor, não falha da pesquisa.

**§E.3 contém a informação que reescreve o desenho do sistema:** *"A API oficial da B3 não é acessível a pessoa física"*. O blueprint original assumia acesso a movimentação da carteira. A pesquisa estabelece que a arquitetura realista é extrato da Área do Investidor como fonte primária, nota de corretagem em PDF para preço médio e custos, e agregador contratado se for necessário API. **Isso é restrição de projeto, não resultado de pesquisa de custos**, e vale mais para o repositório que a tabela de tarifas.

**Solidez medida, não reputada.** PL do conglomerado prudencial pela API do BCB, com lucro ou prejuízo do trimestre. Genial com prejuízo de R$ 4,4 mi e PL de R$ 277,8 mi; Warren com PL de R$ 61–78 mi. Dado primário onde o normal é usar Reclame Aqui.

**AD.3 — o alerta de colisão de tabela.** Dado obtido para o BTG e recusado por ser idêntico, valor por valor em cinco faixas, ao da Terra. Descartar coleta bem-sucedida por suspeita fundamentada é mais difícil que coletar.

## 2.2 Erros

**R-01 · A frase que ficou é a errada, e ela virou constante no código.** §B.6 conclui: *"A B3 leva R$ 0,30 numa compra de R$ 1.000. Isso é irrelevante."* Verdadeiro para a tarifa à vista. Mas a **custódia** de renda variável é da mesma B3 e não é irrelevante: no meu recálculo com a tabela progressiva de §B.4, ela soma **R$ 8.987 em 20 anos** a R$ 1.000/mês. §E.1 registra a custódia em linha separada e ressalva que várias instituições a absorvem — está correto. O problema é retórico: a frase memorável diz "a B3 é irrelevante", e foi o `B3_VISTA = 0,0003` que atravessou para o `custos.py` enquanto a custódia entrou truncada em uma faixa só.

**R-02 · §E.3 tem forma de ranking.** A peça declara duas vezes que não é recomendação, o critério é de custo confirmado e a lista é honesta. Mas o formato — "1. Itaú… 2. C6… 3. Inter…", seguido de "Instituições a evitar para este perfil" — é o de recomendação de instituição. A distância entre "levantamento de custos ordenado por critério" e "recomendação" é retórica, e aqui ela é fina demais para uma peça que preza pelo rigor no resto.

**R-03 · Um `PARCIAL` sustentando um veredito.** A XP entra na lista de "evitar" pelos R$ 4,90 no swing trade, e o próprio arquivo marca essa leitura como PARCIAL, pedindo confirmação. Um dado não confirmado não deveria sustentar exclusão nominal — o mesmo padrão que, no `custos.py`, produziu a inversão de ordenação da rota Vest.

**R-04 · Números de conclusão sem cadeia verificada nesta auditoria.** "7 das 25 marcas pedidas já desapareceram" e "o BC liquidou 17 instituições em 2025–2026" são fortes e aparecem na resposta central. Não os verifiquei, e o critério de "desaparecer" merece explicitação: incorporação societária e liquidação extrajudicial são eventos muito diferentes para quem avalia risco de contraparte, e somá-los num único número apaga a distinção que o resto do arquivo faz com cuidado.

## 2.3 Melhorias

1. Reescrever a conclusão de §B.6: *"A tarifa à vista é desprezível. A custódia da mesma B3 não é — são R$ 8.987 em 20 anos a R$ 1.000/mês, salvo se a instituição a absorver."* Duas frases no lugar de uma resolvem R-01 na origem.
2. Converter §E.3 em **matriz de atendimento a critérios** — colunas (i) corretagem zero no autoatendimento, (ii) custódia RV absorvida, (iii) taxa própria zero no TD, (iv) PL do conglomerado — com ✓ / ✗ / NC por linha, sem ordinal e sem lista de "evitar". A informação é a mesma; a forma deixa de ser recomendação.
3. Separar, em §A.1, "deixou de existir por incorporação" de "liquidada pelo BC".
4. **Promover §C.3 e a restrição de API de §E.3 a `docs/fontes/restricoes-de-projeto.md`.** Não são custos; são premissas de arquitetura, e o laudo Rev. 03 já tinha o desenho de ingestão de carteira em aberto.

---

# 3. `pesquisa-etfs.md` — 457 linhas

**Veredito: a peça de melhor argumentação jurídica e a que faz a única análise verdadeiramente original do conjunto. A mais curta e a de maior densidade.**

## 3.1 Acertos

**§B.1 é a melhor construção jurídica dos quatro arquivos.** A alíquota vem por encadeamento rastreável: IN RFB 1.585/2015 art. 27, I → art. 56 (ganhos líquidos em bolsa) → Lei 11.033/2004 art. 2º (15% / 20% day trade + IRRF de 0,005%). E a não-isenção vem por **argumento de lista fechada**, que é a forma correta de provar uma negativa: o art. 3º, I da Lei 11.033 fala em "mercado à vista **de ações**"; o art. 59 da IN lista ações, ouro e ações de PME; cota de fundo de índice não está lá. Conclusão: ETF de renda variável paga 15% desde o primeiro real.

**A armadilha de leitura antecipada.** A IN 1.585 menciona R$ 20.000 no art. 25, §1º, num contexto totalmente diferente — integralização de cotas mediante entrega de ações, em que o alienado são ações. O arquivo explica por que resumos secundários confundem os dois artigos. Antecipar o erro do leitor é trabalho de auditor.

**Liquidez calculada do COTAHIST, com contagem de pregões.** ECOO11 sem negócio em 4 de 20 pregões; GOVE11 a R$ 15 mil/dia; ISUS11 a R$ 33 mil/dia. Nenhum agregador entrega "em quantos pregões negociou", e é justamente esse campo que separa ETF ilíquido de ETF pequeno.

**§5 — a distinção entre os dois blocos do segmento de "ETF de renda" é o achado original do conjunto.** Treze dos vinte fundos do segmento, e a maior parte do patrimônio, são da família Buena Vista/NEOS, e a estratégia é **covered call** — confirmado no FAQ do próprio gestor, incluindo a advertência literal de que a classe "pode resultar em significativas perdas patrimoniais". A explicação que acompanha está correta e é a que o marketing do segmento evita: prêmio de opção não é renda nova, é a venda antecipada da valorização futura; em mercado de alta o fundo entrega o cupom e abre mão da alta, e o yield alto convive com retorno total menor.

**E a lacuna certa, nomeada com a consequência certa:** se as distribuições são classificadas, no todo ou em parte, como retorno de capital, isso é `NÃO CONFIRMADO` — *"um yield mensal que é parcialmente devolução do seu próprio dinheiro é indistinguível, no extrato, de um yield genuíno."* É a pergunta mais importante do segmento, e está aberta e explicitada em vez de contornada.

**Divergências registradas em vez de escolhidas.** AREA11 com início em 22/09/2025 pela AUVP e 05/09/2025 pela CVM. XFIX11 possivelmente FIIM ou FII, com a diferença fiscal nomeada. E o universo veio da CVM porque a lista da B3 estava bloqueada — com a limitação declarada, não disfarçada.

## 3.2 Erros

**F-01 · HASH11 tem duas taxas e só uma atravessa.** A lacuna 3 registra "HASH11 0,3%/1,3%". O `custos.py` usa 1,30% com a nota "taxa máxima global". A escolha conservadora é defensável, mas a ficha do ETF na tabela mestre deveria trazer as duas e o critério de qual se aplica — como está, quem lê só o script não sabe que existe um 0,3%.

**F-02 · A base legal do dividendo de BDR é editorial, e a ressalva não viaja.** A lacuna 8 diz: *"a afirmação de 15%/carnê-leão vem de material editorial da B3, não da lei. PARCIAL."* Correto no lugar certo. Mas o número circula na seção de BDR sem repetir a marca.

**F-03 · BOVV11 é a maior lacuna do arquivo e está classificada junto com as menores.** É o terceiro maior ETF do país por patrimônio (R$ 7,66 bi) e não há nenhum dado do gestor — o site bloqueia acesso automatizado. Aparece como lacuna 4, entre "liquidez de ETFs de renda fixa" e "EURP11, ASIA11…". Merece prioridade explícita.

**F-04 · Cobertura desigual entre universo e fichas.** O universo tem 222 ETFs; as fichas cobrem ~26; a taxa está confirmada para 12. Está tudo declarado, e a disciplina é boa — mas quem for expandir a tabela de custos no futuro vai encontrar `NC` na coluna de taxa e não terá aviso automático de que aquilo não é preenchível.

## 3.3 Melhorias

1. **Elevar a pergunta do retorno de capital de lacuna a bloqueio.** Nenhum ETF da família NEOS entra em tabela comparativa de custo ou de rendimento enquanto não houver demonstrativo de composição da distribuição. É o campo `bloqueia` proposto no laudo consolidado, aplicado ao caso mais claro que existe.
2. Ficha de HASH11 com as duas taxas e o critério.
3. Priorizar BOVV11 na 3ª passada — é o maior buraco por patrimônio.
4. Marcar, na própria tabela mestre, quais tickers têm taxa confirmada, para que a expansão futura não pegue um `NC` por engano.

---

# 4. `pesquisa-internacional.md` — 1.236 linhas

**Veredito: a peça mais ambiciosa, com a melhor exposição jurídica e a única análise de segunda ordem do conjunto. E a única cuja conclusão principal está errada — não por falha própria, mas por não ter lido o arquivo irmão.**

## 4.1 Acertos

**§3.2 — os três degraus da isenção de R$ 35 mil.** É a melhor exposição jurídica dos quatro arquivos, porque não se contenta com a resposta e mostra o mecanismo: (1) a isenção **continua existindo** na lei geral, art. 22 da Lei 9.250/1995; (2) o que caiu foi o art. 24 da MP 2.158-35/2001, que mandava apurar as aplicações em moeda estrangeira como *ganho de capital* e assim dava acesso à isenção — com a marca literal "(Revogado pela Lei nº 14.754, de 2023)" no Planalto; (3) a Lei 14.754 reclassificou a operação. Quem lê isso entende por que a resposta é "acabou" sem que a isenção tenha sido revogada. É a confusão mais comum do varejo e está desmontada com precisão.

**Wise medida ao vivo.** 0,7253% de tarifa própria contra 3,5% de IOF, e a leitura que decorre: o IOF é 4,8 vezes a tarifa da Wise, e enquadrar a remessa no inciso XXI-A (1,10%) em vez do XXI (3,5%) vale mais do que qualquer negociação de spread. Medição própria, não tabela publicada.

**§5(c) — a classificação por jurisdição é o achado original do arquivo.** Avenue (Itaú, 50,1%), Inter US, BTG US e XP US têm controlador ou grupo brasileiro. A conclusão é dura e correta: *"pagar 1,60% a 3,10% de entrada numa dessas não compra a proteção de jurisdição que se pretendia comprar; compra conveniência, atendimento em português e facilidade de câmbio."* Isso é análise de segunda ordem — o argumento não-financeiro medido contra o que o produto de fato entrega.

**§5(a) — a recusa mais disciplinada do conjunto.** Sobre o Plano Collor: as URLs foram localizadas, os textos não abriram, e o arquivo se recusa a descrever o episódio. *"Descrever isso de memória seria exatamente a estimativa que esta pesquisa se proibiu."* Uma seção inteira entregue vazia, com o motivo técnico. Disciplina sob pressão vale mais que a seção teria valido preenchida.

**§7 ordena as lacunas por impacto sobre as conclusões**, não por ordem de descoberta nem por facilidade de fechamento. E a lacuna 1 é a que de fato quebra a comparação.

**O mapeamento de complexidade acessória** está bem calibrado: CBE só acima de US$ 1 milhão (marcado como secundário), mas a DAA vira obrigatória com **um** dividendo recebido, e exige custo médio em reais pela cotação de venda do BCB da data de **cada** aquisição. Trabalhoso, anual, determinístico — a caracterização certa.

## 4.2 Erros

**I-01 · A conclusão de §4.3–4.4 está desatualizada, e na direção que a derruba. Crítico.**

§4.4 escreve: *"Tributação de ETF de índice no Brasil: **NÃO CONFIRMADO** (…) É um ponto **decisivo** (…) se o ETF brasileiro não tem isenção e é tributado a 15% como o estrangeiro, a vantagem tributária da rota doméstica desaparece (…) **Deixo em aberto.**"*

Não está em aberto. `pesquisa-etfs.md` §B.1 fechou, na mesma rodada, com base legal dupla e argumento de lista fechada, exatamente na hipótese que faz a vantagem doméstica desaparecer. A §7, lacuna 1, repete o erro ao dizer que "sem isso, a comparação da seção 4 não fecha do lado doméstico" — fecha, no arquivo ao lado.

**I-02 · §4.1 e §4.4 declaram NÃO CONFIRMADO um número que o arquivo irmão confirma. Crítico.** A taxa de administração do IVVB11, 0,23% a.a., aparece aqui como "premissa do pedido, não uso como confirmado" e em `pesquisa-etfs.md` como confirmada, com nota de rodapé apontando para a BlackRock. Dois relatórios da mesma rodada, veredito oposto sobre o mesmo número.

**I-03 · O ponto de equilíbrio de §4.3 é montado sobre um insumo inexistente.** O `Δ` depende do expense ratio do IVV/VOO, que continua não lido (e a lacuna 10 de `pesquisa-etfs.md` acrescenta que o do VTI também não foi obtido). A direção do viés da aproximação está declarada — *"ignorando juros compostos, aproximação conservadora que favorece a rota estrangeira"* —, o que é correto e honesto. Mas o resultado é um número calculado sobre um dado que não existe, e foi ele que atravessou para os dois scripts como `adm=0.00030`.

**I-04 · A ressalva da Vest não viaja da tabela mestre para a tabela 4.2.** §2.0 classifica a Vest como "(a), com ressalva". A tabela 4.2 registra "IOF: não se aplica (declarado)" e produz custo de entrada de 1,40%, sem a ressalva. "Declarado" ali é declaração da plataforma sobre o enquadramento de remessa via stablecoin — posição jurídica, não fato tributário confirmado. Foi essa linha que, no `custos.py`, fez a Vest aparecer como a rota de exterior mais barata e inverter a ordenação frente à Avenue.

**I-05 · A retenção de 30% em dividendos americanos.** A lacuna 3 admite: confirmada a ausência de tratado, não o percentual. O número aparece no corpo do texto. Mesma classe de I-04 — a marca fica na lista de lacunas e não acompanha o uso.

## 4.3 Melhorias

1. **Reescrever §4.3 e §4.4** com o fato estabelecido em `pesquisa-etfs.md` §B.1, e **recalcular o ponto de equilíbrio**. O resultado muda de direção, e é o resultado de maior consequência da peça inteira.
2. **Coluna de status por componente na tabela 4.2** (spread / IOF / total), e regra dura: rota com componente `NÃO CONFIRMADO` fica **fora da ordenação**, impressa abaixo da linha. Resolve I-04 e impede que a inversão se repita.
3. **Rodar §4.3 como sensibilidade em `Δ`** — faixa de 0,10 a 0,25 p.p. — em vez de ponto único, enquanto o expense ratio não for lido.
4. Repetir a marca de status **no ponto de uso**, não só na lista de lacunas. É o padrão que I-04 e I-05 quebram, e é o mesmo padrão que o `custos.py` herdou.

---

# 5. O que os quatro têm em comum

## 5.1 A qualidade que atravessa os quatro

Todos aplicam a mesma regra de evidência, com o mesmo vocabulário de status, e todos registram bloqueio como resultado. Isso não é trivial: quatro peças produzidas em paralelo mantiveram uma convenção comum e verificável. E os quatro contêm pelo menos uma recusa explícita a preencher lacuna — a §2.4 dos cofrinhos, o BTG nas corretoras, o retorno de capital nos ETFs, o Plano Collor no internacional. **A disposição de entregar seção vazia com motivo é o que dá crédito ao resto.**

## 5.2 O defeito que atravessa os quatro

**A marca de status fica na seção que a criou e não acompanha o dado até o ponto de uso.** É o mesmo padrão em quatro manifestações:

| Arquivo | Onde a marca ficou | Onde o dado foi usado sem ela |
|---|---|---|
| cofrinhos | §2.4 "PARCIAL — fonte secundária" | §1.2, conclusão sobre teto de 120% |
| corretoras | XP marcada "PARCIAL — confirmar" | §E.3, lista nominal de instituições a evitar |
| etfs | Lacuna 8, "editorial, não a lei" | Seção de BDR, no corpo |
| internacional | §2.0, Vest "(a), com ressalva" | §4.2, custo de entrada de 1,40% na tabela ordenada |

E é esse padrão, e não descuido pontual, que produziu o achado mais grave do laudo consolidado: três valores `NÃO CONFIRMADO` virando constantes nos scripts.

**A correção é estrutural, não editorial.** O status precisa ser propriedade do dado, não da seção — o que significa que ele viaja quando o dado viaja. No repositório isso é o campo `status` no YAML de procedência, com o campo `bloqueia` que impede o cálculo de rodar; no texto, é repetir a marca em cada tabela que usa o número, mesmo parecendo redundante. A redundância aqui é a função, não o defeito.

## 5.3 A quinta peça que falta

Os quatro arquivos foram produzidos como se fossem independentes, e é por isso que I-01 e I-02 existem: o internacional não sabia o que o de ETFs havia descoberto. Editar os quatro não resolve — a próxima rodada recriaria o problema.

O que falta é um **quinto artefato**: uma tabela de reconciliação, uma linha por número que aparece em mais de um relatório, com o valor, o status em cada arquivo, o status vencedor, o arquivo que venceu e a data. Ela é barata — provavelmente meia hora — e é a única coisa que impede a divergência de voltar.

Começaria com quatro linhas: taxa do IVVB11; expense ratio do IVV/VOO; isenção de R$ 20 mil aplicada a ETF; IOF sobre remessa via stablecoin.

# B3 — Termos de Uso do website institucional
Fonte: https://www.b3.com.br/pt_br/termos-de-uso-e-protecao-de-dados/termos-de-uso/
Acesso: 25/09/2026 20:02 UTC (HTTP 200; `Last-Modified: Mon, 18 May 2026 17:48:54 GMT`; 36.129 bytes de HTML)
Status: COMPLETO para as cláusulas abaixo — o texto não traz número de versão nem data de vigência (só "B3 © 2017")
Fecha: P-136, metade B3 (leitura)
Impressão: sha256 do texto extraído do HTML (sem script/style) `6aba54d381ca27a3…` — como a página não tem versão, é o hash que diz se o texto mudou
---

Lido pela sessão na nuvem com `curl`, depois de ele liberar o host na rede do ambiente. As
cláusulas abaixo são **citação de passagens**, com a fonte indicada; o resto da página
(isenções de responsabilidade, dados pessoais, cookies) não trata de uso nem de
redistribuição e não foi transcrito.

## As cláusulas (texto literal)

**"Proteção à propriedade intelectual"**

> "Todo o conteúdo deste website, tais como informações, materiais, instrumentos, gráficos e
> desenhos, pertencem à B3 ou a terceiros que cederam seu direito de uso."

> "Os visitantes deste website podem utilizar os dados disponíveis nessas páginas para uso
> exclusivamente pessoal, o que não implica transferência de titularidade sobre qualquer
> software ou conteúdo disponibilizado. Não é permitida a reprodução, modificação, transmissão,
> comercialização, locação, publicação, distribuição ou quaisquer outras formas de utilização
> para fins comerciais de parte ou totalidade do conteúdo deste website, mediante qualquer
> forma ou meio, sem autorização prévia e por escrito da B3."

**"Difusão de Dados de Mercado (Cotações, índices e notícias relacionadas)"**

> "É vedada a distribuição, redistribuição, transferência, transmissão, retransmissão, licença,
> sublicença, locação, empréstimo, venda, revenda, recirculação, reformatação, publicação,
> prestação de serviços autônomos de difusão de dados e de avaliação ou fornecimento de bases
> de dados e produtos a terceiros por meio da utilização, ou disponibilização integral ou
> parcial da Difusão de Dados, exceto mediante prévio e expresso consentimento da B3."

> "Salvo mediante prévio e expresso consentimento, por escrito, da B3, em instrumento
> contratual próprio e nos termos das diretrizes da política então vigente, divulgada pela B3,
> não é permitida a utilização da Difusão de Dados de Mercado para fins de elaboração,
> criação, cálculo ou geração de qualquer modalidade de índice, bem como de instrumentos
> financeiros, valores mobiliários (ex. opções e derivativos) em benefício próprio ou de
> terceiros."

**"Índices divulgados"** — os índices da B3 *"não podendo ser, de qualquer forma ou por
qualquer meio, utilizados por terceiros, salvo mediante autorização prévia da B3, formalizada
em documento próprio."*

**"Aviso Legal"**

> "É vedada a utilização dos dados contidos neste website para fins comerciais salvo mediante
> autorização prévia e por escrito da B3."

**"Mudanças na política"** — *"Estes termos de uso aqui estabelecidos estão sujeitos a
eventuais alterações, a qualquer tempo e sem aviso prévio"*.

## O que isto responde para o projeto

| pergunta | resposta pela letra | status |
|---|---|---|
| guardar cotação e evento da B3 para **um** usuário, em armazém privado | "uso exclusivamente pessoal" | permitido |
| pôr dado de mercado da B3 (COTAHIST, eventos) no **repositório público** | "publicação […] integral ou parcial da Difusão de Dados" é vedada sem consentimento — e a cláusula de dados de mercado **não** tem o qualificador "para fins comerciais" | **vedado**. Medido em 25/09: o repositório não tem nenhum (P-136) |
| **servir um segundo usuário** (a pergunta da U-01) — inclusive série **ajustada** | "fornecimento de bases de dados e produtos a terceiros", "reformatação": vedado sem consentimento | **portão**: exige contrato com a B3 antes |
| calcular índice próprio com o dado | vedado sem instrumento contratual | o motor não calcula índice; o Ibovespa só é lido como referência |
| **transcrever documento da B3** (leiaute, tarifação) no repositório público | o documento é "conteúdo deste website"; o uso autorizado é "exclusivamente pessoal", e a proibição de "reprodução […] publicação" vem com "para fins comerciais" | **ambíguo** — ver abaixo |

**A ambiguidade, e ela é de redação:** na frase *"Não é permitida a reprodução, modificação,
[…] publicação, distribuição ou quaisquer outras formas de utilização para fins comerciais"*, o
"para fins comerciais" pode qualificar só "quaisquer outras formas" ou a lista inteira. Lido do
segundo jeito, publicar sem fim comercial não é proibido; mas a frase anterior limita o uso
autorizado a "exclusivamente pessoal", e um repositório público não é uso pessoal. **Não há
leitura que torne a transcrição integral claramente permitida.** A Lei 9.610/1998, art. 46, III,
permite a citação de **passagens** para estudo e crítica, com a fonte; não a reprodução
integral.

## O que esta leitura NÃO cobre (P5)

- **O domínio de onde o COTAHIST é baixado** é `bvmf.bmfbovespa.com.br`, não `www.b3.com.br`.
  Estes termos são do "website institucional". Que valham para o arquivo servido no outro host
  é a leitura mais prudente, não uma cláusula lida.
- **A Política Comercial de Market Data da B3** (citada pela própria cláusula: "nos termos das
  diretrizes da política então vigente") não foi lida. É ela que diz o preço e a forma do
  consentimento, se um dia ele for pedido.
- A página não tem versão: o sha256 acima é a única forma de saber, numa releitura, se o texto
  mudou.

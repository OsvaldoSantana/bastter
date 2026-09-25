# CVM — Licença e Termos de Uso do Portal de Dados Abertos
Fonte: https://dados.cvm.gov.br/dataset/cia_aberta-doc-dfp (licença do conjunto) e https://dados.cvm.gov.br/about (termos de uso)
Acesso: 25/09/2026 20:02 UTC (HTTP 200 nas duas)
Status: COMPLETO para o DFP e para os termos gerais; os demais conjuntos (ITR, FCA, CAD) não tiveram a página de licença aberta
Fecha: P-136, metade CVM (leitura)
Impressão: sha256 do texto extraído dos termos `e01f7b906dd5ec42…`; os termos dizem "Publicado em 05/08/2024"
---

Lido pela sessão na nuvem com `curl`, depois de ele liberar o host na rede do ambiente. Até
hoje a CVM era inalcançável daqui (`ROBOTS_DISALLOWED` e depois `EGRESS_BLOCKED`, §5-B.17).

## A licença do conjunto DFP (texto literal)

> "Licença — Licença Aberta para Bases de Dados (ODbL) do Open Data Commons"

com link para `http://www.opendefinition.org/licenses/odc-odbl`. Página do conjunto: criado em
"julho 29, 2020", "Periodicidade de atualização: Semanal".

## Os termos de uso do portal (texto literal)

> "Licença de Uso: Os dados e as informações publicados no Portal de Dados Abertos da CVM estão
> disponíveis como serviço público gratuito a qualquer pessoa física ou jurídica, conforme as
> condições definidas neste documento."

> "O usuário deve verificar no metadado de cada conjunto de dados, as licenças sobre condições
> adicionais, que podem ser atualizadas, corrigidas e/ou substituídas a qualquer tempo."

> "O usuário, ao utilizar de qualquer forma a informação obtida (uso secundário) deverá citar a
> fonte dos dados obtidos, declarando que eles foram acessados pelo Portal de Dados Abertos da
> CVM, disponível em https://dados.cvm.gov.br/."

> "A CVM não garante o fornecimento continuado dos dados nem a sua entrega tempestiva aos
> interessados."

> "A fim de preservar a disponibilidade das informações ao público em geral, o Portal pode
> empregar mecanismos para limitar a quantidade de acessos simultâneos, tais como aqueles
> realizados por robôs de consulta."

> "Publicado em 05/08/2024."

## O que isto responde para o projeto

| pergunta | resposta | status |
|---|---|---|
| usar DFP/ITR/FCA/CAD | serviço público gratuito, pessoa física ou jurídica | permitido |
| citar a fonte | obrigatório em todo "uso secundário", com a frase e a URL acima | **o `NOTICE` passa a trazer a frase** |
| **redistribuir** o dado (inclusive as versões que a CVM já substituiu e só existem no armazém) | ODbL permite, com atribuição, aviso da licença e *share-alike* na base derivada publicada | **permitido com condições** — decisão dele se o armazém da CVM deixa de ser privado (P-136) |
| a captura automática | o portal "pode empregar mecanismos para limitar" robôs; a captura faz um HEAD por arquivo por dia | compatível; o `ROBOTS_DISALLOWED` das ferramentas de agente é outra coisa (ver `CLAUDE.md` §11.2) |

**A consequência que muda um texto do projeto:** o `docs/reproduzir.md` diz que as versões antigas
da CVM "só existem no nosso armazém, que é privado pela P-136". Pela ODbL, **a P-136 não obriga
esse armazém a ser privado para a CVM** — só para a B3. Mantê-lo privado passa a ser escolha, não
exigência.

## O que esta leitura NÃO cobre (P5)

- Só a página do **DFP** teve o campo de licença lido. ITR, FCA e CAD provavelmente dizem o mesmo
  (é o padrão do portal), mas não foi aberto — `NAO_CONFIRMADO` para os três.
- O texto integral da ODbL 1.0 não foi transcrito aqui; as obrigações acima (atribuição, aviso,
  *share-alike*) são as da licença como publicada pela Open Data Commons, e valem conferir na
  íntegra antes de publicar uma base derivada.

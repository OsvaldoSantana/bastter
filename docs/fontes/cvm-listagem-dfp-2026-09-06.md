# Listagem do diretorio DFP da CVM — observada em 06/09/2026
Fonte: https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/
Acesso: 06/09/2026, ~17h40, pelo navegador do celular do Osvaldo (Chrome/Android)
Metodo: print de tela. **Nao foi leitura automatizada** — o portal responde
`ROBOTS_DISALLOWED` a qualquer agente meu, e eu nao contorno bloqueio de robots.txt.
Esta e a unica forma pela qual este dado podia entrar no projeto.
Status: **OBSERVADO** — visto no dado real, nao documentado pela CVM.
**SUPERADO EM PARTE, no mesmo dia:** a pergunta do prazo foi respondida pela pagina do
conjunto — ver `cvm-dfp-politica-atualizacao.md`, status COMPLETO. O que sobrevive
deste arquivo e a faixa observada (2010-2026, 17 arquivos) e o fato de a listagem nao
trazer data nem tamanho.

---

## O que foi observado

Dezessete arquivos, um por ano, sem interrupcao:

```
dfp_cia_aberta_2010.zip  ...  dfp_cia_aberta_2026.zip
```

**Primeiro ano: 2010. Ultimo: 2026.** O arquivo do ano corrente **existe** e esta
publicado normalmente, junto dos historicos.

## O que a listagem NAO tem, e isso importa

**A listagem nao mostra data de modificacao nem tamanho.** Nao ha colunas ao lado dos
nomes — so o icone, o nome do arquivo e o link. Isto derruba a hipotese de trabalho do
roteiro `fase0/CELULAR-CVM.md`, que supunha um indice no estilo Apache
(`Name / Last modified / Size`). Nao e: e uma pagina montada pela CVM, e ela omite os
metadados.

**Consequencia direta:** a pergunta *"a CVM reescreve o arquivo do ano corrente?"*
**nao se responde por esta pagina**. Ela continua `NAO_CONFIRMADO`, e passa a depender
de dois outros caminhos:

1. o cabecalho HTTP `Last-Modified` de cada arquivo, que o `fase0.ps1 -SoConferir`
   le sem baixar o conteudo (requisicao HEAD) — **terca**;
2. o texto de politica de atualizacao que a propria pagina exibe logo abaixo da
   listagem, comecando com *"Os arquivos de dados serao atualizados conforme a
   politica..."* — **cortado no print, ainda nao lido**.

O caminho 2 e melhor que o 1: e a CVM declarando o proprio comportamento, o que vale
mais que uma inferencia a partir de carimbo de tempo.

## Implicacao para o backtest, que muda de forma

O primeiro ano ser **2010** e um limite duro que o projeto nao tinha registrado. O
pre-registro fala em series longas, e a serie do NEFIN em `dados/nefin_factors.csv`
comeca em **2001-01-02**. Ou seja: ha nove anos de fatores sem contrapartida de
demonstracao financeira nesta fonte.

Isso nao invalida nada — H1 e H3 rodam sobre os fatores do NEFIN e nao dependem da CVM.
Mas qualquer hipotese que precise cruzar fundamento com preco esta limitada a
**2010 em diante**, e isso pertence a `limitacoes_declaradas`, nao a um comentario.

NAO_CONFIRMADO: se existe arquivo anterior a 2010 em outro caminho do portal (o
formulario DFP e posterior ao IAN/DFP antigo, entao 2010 pode ser o inicio real da
serie neste formato — mas isso e hipotese minha, nao leitura de fonte).

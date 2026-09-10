# Catalogo de dados abertos da CVM — observado em 06/09/2026
Fonte: https://dados.cvm.gov.br/dataset
Acesso: 06/09/2026, pelo navegador do Osvaldo; ele colou o texto da pagina 1 na conversa.
Metodo: **leitura humana**. O portal responde ROBOTS_DISALLOWED as minhas ferramentas.
Tudo neste arquivo veio do texto que ele colou — nao de coleta minha.
Status: **OBSERVADO** — pagina 1 de 3. As paginas 2 e 3 nao foram vistas.

---

## 1. A politica de atualizacao — a resposta foi um desvio, e o desvio informa

A frase que fechava a listagem de arquivos era:

> *"Os arquivos de dados serao atualizados conforme a politica publicada na pagina do
> respectivo conjunto de dados."*

**Nao ha politica global.** Ha uma por conjunto. Portanto a pergunta aberta ha tres
sessoes — *a CVM reescreve o `dfp_cia_aberta_2026.zip`?* — nao tem resposta no portal
como um todo; ela esta na pagina do conjunto DFP, e so la.

Continua `NAO_CONFIRMADO`, mas agora se sabe **onde** esta a resposta, o que antes nao
se sabia.

## 2. O achado que vale mais que a frase: **o portal e um CKAN e tem API**

Rodape da pagina, transcrito:

> *"Voce tambem pode ter acesso a esses registros usando a API (veja Documentacao da
> API)."* — *"Impulsionado por CKAN"*

Consequencias, e sao tres:

1. O catalogo inteiro (**54 conjuntos**) e legivel por maquina. Nao precisa raspar HTML.
2. **CKAN publica `last_modified` por RECURSO.** Isso responde a pergunta da secao 1 de
   forma exata, por arquivo, **sem baixar 1,5 GB** e sem depender de cabecalho HTTP.
3. A politica de atualizacao de cada conjunto e campo do registro (`notes`, `extras`),
   nao prosa numa pagina.

`fase0/cvm_catalogo.py` foi escrito para isso. **O caminho `/api/3/action/` e o padrao
do CKAN e nao foi conferido neste portal** — e inferencia forte, nao leitura. O script
falha em voz alta se o caminho estiver errado, em vez de devolver catalogo vazio.

## 3. Conjuntos vistos na pagina 1 (20 de 54) que interessam ao projeto

| conjunto | formato | por que importa aqui |
|---|---|---|
| **Fundos de Investimento: Informacao Cadastral** | ZIP TXT CSV | e o `cad_fi`. Cobre **"fundos estruturados e nao estruturados"** — ETF e fundo estruturado. **Candidato a fechar a P-05/P-50 com um download em vez de 15 PDFs de regulamento** |
| **Fundos de Investimento: Documentos: Informe Diario** | TXT ZIP | valor da cota, patrimonio liquido e valor total da carteira, por dia. Ver secao 4 |
| **Fundos de Investimento: Documentos: Extrato das Informacoes** | TXT CSV | ultimos 5 anos, ICVM 555. Pode carregar taxa |
| **Participantes Intermediarios: Informacao Cadastral** | ZIP | bancos, corretoras, distribuidoras. Alimenta `instituicoes.yaml` com dado cadastral **oficial**, nao raspado do site da corretora |
| **Processos Sancionadores (PAS)** | ZIP | historico de punicao de intermediario e de companhia |
| **Atos Declaratorios** | TXT CSV | suspensao de intermediacao irregular. Sinal binario, como o "regimes de resolucao" do BCB |
| **Auditores: Informacao Cadastral** | ZIP | quem audita quem — entra em qualidade de resultado |
| **Cias Abertas: Eventos Societarios Especiais: Programa de Recompra de Acoes** | ZIP | **"atualizados diariamente"**. Recompra e evento societario que o endpoint da B3 nao cobre |
| **Ofertas Publicas de Distribuicao** | ZIP | acoes, fundos, debentures, CRI — registradas e dispensadas |
| **Cias Abertas: Informacao Cadastral** | TXT CSV | CNPJ, data e situacao do registro. Chave para o mapeamento bitemporal ticker<->CNPJ<->CD_CVM |
| Administradores de FII | TXT CSV | quando o bloco de FII sair do papel |
| Agentes Autonomos, Consultores, Coordenadores de Ofertas | ZIP | conflito de interesse de quem recomenda |

Nao vistos (paginas 2 e 3): DFP, ITR, FRE, FCA, IPE, VLMO, FII, CDA. Presumidos la —
**presuncao, nao observacao.**

## 4. Uma ideia que so existe porque o catalogo apareceu: medir a taxa em vez de le-la

O **Informe Diario** traz valor da cota e patrimonio liquido de todo fundo, por dia. A
taxa de administracao **ja esta descontada da cota** — e o que separa a cota do ETF do
indice que ele segue.

Isso permite, em vez de transcrever taxa de PDF de regulamento, **medir o atrito
realizado**: comparar a serie da cota com a serie do indice e ver quanto se perdeu por
ano. As duas coisas nao sao a mesma, e e por isso que a ideia e boa:

- o regulamento diz a taxa **maxima declarada**;
- a cota revela o custo **efetivamente cobrado**, mais o erro de replicacao, mais o
  reinvestimento de proventos.

Um ETF que declara 0,10% e entrega 0,35% de diferenca contra o indice tem um problema
que nenhuma lamina conta. E vale ao contrario tambem: se a diferenca medida bate com a
taxa declarada, a taxa fica **confirmada por dado**, e nao por documento.

Isto **nao substitui** a P-50 (o campo `taxa_total_aa` continua necessario, porque o
motor precisa projetar custo futuro, e para isso a taxa declarada e o insumo certo).
Substitui a *conferencia*: e uma segunda fonte, primaria, independente e da propria CVM.

NAO_CONFIRMADO: se o Informe Diario cobre ETF (ele fala em "fundo"; ETF e fundo de
indice, mas a cobertura precisa ser vista); desde quando a serie existe; e o volume —
cota diaria de todo fundo do Brasil e um arquivo grande.

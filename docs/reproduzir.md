# Reproduzir o dado de mercado sem o nosso armazém

O armazém do projeto (Cloudflare R2) é **privado**. Os termos da B3 vedam redistribuir dado
de mercado sem consentimento ([`fontes/b3-termos-de-uso.md`](fontes/b3-termos-de-uso.md)), e os
do NEFIN não autorizam ([`fontes/nefin.md`](fontes/nefin.md)). A CVM publica sob ODbL, que
permite redistribuir com atribuição
([`fontes/cvm-dados-abertos-licenca.md`](fontes/cvm-dados-abertos-licenca.md)): para ela, o
armazém ser privado é escolha, não exigência (P-136). O que é público é o **sha256 de cada arquivo que o
projeto viu**, em [`docs/acervo/`](acervo/). Reproduzir é capturar da fonte, na sua máquina, e
comparar os hashes.

## O que você precisa

Python 3.11 e as dependências da captura (`boto3` vem junto, mas o modo local não o usa):

```bash
python -m pip install ".[captura]"
export ARMAZEM_LOCAL=$HOME/meol-armazem      # onde os arquivos vão morar; padrão: data/armazem-local
```

**Use sempre um registro seu (`--registro`).** O registro do projeto guarda o `Last-Modified`
de cada arquivo que ele viu, e o portão da captura não baixa o que não mudou. Com o nosso
registro, a sua captura acharia tudo "inalterado", não baixaria nada, e a reprodução sairia
vazia com cara de conferida.

## Capturar

```bash
python fase0/capturar_nefin.py    --armazem local --registro reg-nefin.csv
python fase0/capturar_cvm.py      --armazem local --registro reg-cvm.csv
python fase0/capturar_cotahist.py --armazem local --registro reg-b3.csv
```

| captura | o que traz | tamanho |
|---|---|---|
| NEFIN | os fatores de risco, um CSV | ~0,9 MB |
| CVM | DFP, ITR e FCA de todos os anos do índice, e o cadastro | ~0,6 GB (52 arquivos no inventário, 25/09) |
| COTAHIST | os diários dos últimos 7 dias e o anual do mês que acabou | ~90 MB |

O **histórico** do COTAHIST (1986 em diante) não tem comando: a rotina só observa o presente. Os
anuais estão num GET aberto, `https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A<ANO>.ZIP`,
e basta compará-los à mão com `sha256sum` contra
[`docs/acervo/b3/inventario-armazem.csv`](acervo/b3/inventario-armazem.csv).

## Comparar

```bash
python fase0/conferir_reproducao.py
```

Cada arquivo sai em uma de quatro situações, com a contagem e o `n` no fim:

| situação | o que quer dizer |
|---|---|
| `IGUAL` | você baixou uma versão que o projeto registrou. Reproduzido |
| `DIFERENTE` | o arquivo existe dos dois lados, e a sua versão nunca foi vista pelo projeto |
| `SO_NOSSO` | o projeto registrou, você não capturou (ou a fonte já não serve) |
| `SO_SEU` | você capturou, o projeto nunca registrou |

## O limite, e ele não é consertável daqui

**A CVM serve só a versão corrente de cada arquivo.** Os cinco anos mais recentes do DFP e do ITR
são reescritos toda semana com as reapresentações
([`fontes/cvm-dfp-politica-atualizacao.md`](fontes/cvm-dfp-politica-atualizacao.md)). Uma versão
que o projeto capturou e a CVM já substituiu **não está mais na CVM**. Desde 25/09/2026 ela está
nas **releases `cvm-acervo-<ano>`** deste repositório (licença ODbL, com a atribuição da CVM nas
notas), com o nome `<arquivo>__<sha256[:12]>`: baixe de lá e compare o sha256. Enquanto a versão
não estiver lá, `DIFERENTE` é o resultado esperado, e não prova que ninguém errou: prova que a
fonte mudou depois.
O registro diz quando cada versão foi vista (`dt_captura`), e o `Last-Modified` que a fonte
declarava.

O mesmo vale para o NEFIN quando ele publicar uma série nova, e para o anual do COTAHIST do ano
corrente, que cresce a cada pregão. Ano fechado do COTAHIST é congelado: medido em 18/09 e em
23/09, mesmo sha256 (P-96).

**Por que o armazém não é aberto:** redistribuir um arquivo exige licença, e ler hash não. A CVM
permite (ODbL) e é publicada pelas releases; a B3 e o NEFIN não permitem, e deles o que se publica
é a prova de qual arquivo era, não o arquivo. O acesso público do R2 abriria o bucket inteiro, B3
junto — por isso release, e não bucket ([`decisoes/P-136-cvm-publica.md`](decisoes/P-136-cvm-publica.md)).

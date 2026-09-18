# CVM — o download manual, passo a passo

**Por que manual:** `dados.cvm.gov.br` responde **ROBOTS_DISALLOWED** às minhas
ferramentas, e a regra do projeto é honrar isso — nada de curl, wget, requests, cache
ou espelho. **Você baixa pelo navegador; eu processo o que chegar.** Já aconteceu uma
violação minha, em 06/09: rodei `cvm_catalogo.py --listar` "para testar" e o teste *foi*
a violação. Não repito.

**O que está em jogo:** o acervo da CVM se parte em dois, e só metade tem prazo.

| faixa | arquivos | comportamento | urgência |
|---|---|---|---|
| **2021 – 2026** | 6 | **reescritos toda semana** com reapresentações | **alta, e contínua** |
| **2010 – 2020** | 11 | **não sujeitos à política de atualização** — congelados | nenhuma |

Fonte: a própria página do conjunto, que você colou em 06/09 e está transcrita em
`docs/fontes/cvm-dfp-politica-atualizacao.md`. *"Os arquivos serão atualizados
semanalmente com as eventuais reapresentações."*

> **O que uma reapresentação destrói:** ela substitui o número **entregue** pelo número
> **corrigido**, dentro do mesmo arquivo e sob o mesmo nome. Quem não tirou um retrato
> antes **não consegue mais saber o que a empresa dizia na época** — e é exatamente
> essa a informação que um backtest honesto precisa, porque a decisão de compra teria
> sido tomada com o número antigo. Cada semana sem snapshot é uma rodada de
> reapresentações que deixou de ser observável.

---

## 1. Onde os arquivos estão

Dois diretórios de índice — abra no navegador e você verá a lista de `.zip`:

```
https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/
https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/
```

Nomes: `dfp_cia_aberta_2010.zip` … `dfp_cia_aberta_2026.zip`, e o mesmo padrão para
`itr_cia_aberta_ANO.zip`.

As páginas de **conjunto** (com a política escrita e a data da última atualização):

```
https://dados.cvm.gov.br/dataset/cia_aberta-doc-dfp
https://dados.cvm.gov.br/dataset/cia_aberta-doc-itr
```

---

## 2. A ordem — baixe primeiro o que tem prazo

### Passo 1 — os 6 com prazo (DFP), e são estes

`dfp_cia_aberta_2021.zip` · `2022` · `2023` · `2024` · `2025` · `2026`

### Passo 2 — os 6 com prazo (ITR)

`itr_cia_aberta_2021.zip` … `2026.zip`

### Passo 3 — a cauda congelada, quando der

2010 a 2020, DFP e ITR. **Não tem urgência**: ela não muda. Pode ser outro dia, outra
semana, pela internet de casa.

---

## 3. Onde salvar — e o caminho importa

O `refinar.py` e os coletores esperam a árvore bronze já existente:

```
C:\Users\osvaldo.junior\Desktop\Bastter\data\bronze\cvm\dfp\
C:\Users\osvaldo.junior\Desktop\Bastter\data\bronze\cvm\itr\
```

**Salve os `.zip` inteiros, sem descompactar.** O zip é o byte que a CVM entregou; ele
é a evidência. Descompactar antes de registrar o sha256 perde a única coisa que prova
que o arquivo é aquele.

`data\` está no `.gitignore` e **nunca** entra no repositório — são ~1,5 GB e não são
seus para redistribuir (licença **ODbL**, com cláusula de compartilhamento pelo mesmo
regime se você publicar algum derivado).

---

## 4. Depois de baixar — o que rodar, e por quê

```powershell
cd C:\Users\osvaldo.junior\Desktop\Bastter
Get-ChildItem data\bronze\cvm -Recurse -Filter "*.zip" |
    Select-Object Name, Length, LastWriteTime |
    Sort-Object Name
```

**Me mande essa saída.** Ela é o inventário, e eu comparo com o que a página do conjunto
declarava.

E então o registro de procedência — **este é o passo que não pode ser pulado**:

```powershell
Get-ChildItem data\bronze\cvm -Recurse -Filter "*.zip" | ForEach-Object {
    "{0}  {1}  {2}" -f $_.Name, $_.Length, (Get-FileHash $_.FullName -Algorithm SHA256).Hash
}
```

> **Por que o sha256 é o passo que importa mais que o download.** O nome do arquivo
> mente: `dfp_cia_aberta_2022.zip` de hoje **não é** o `dfp_cia_aberta_2022.zip` de
> semana que vem, e os dois têm o mesmo nome. O hash é a única coisa que distingue os
> dois retratos — e sem ele você tem um arquivo, não uma observação datada.
>
> Junto com o hash, anote **a data e a hora em que você baixou**. É o `dt_captura`, e
> ele é metade da bitemporalidade que o projeto inteiro persegue: o que a CVM dizia
> (`DT_REFER`) **versus** quando ela dizia (`dt_captura`).

---

## 5. O caso A-04 — a Marfrig, e é o motivo específico deste download

A história de eventos da Marfrig não está sob `MRFG` nem sob `MBRF` na B3 — medido em
12/09. O caminho é a CVM, porque ela indexa por **CD_CVM**, que é estável quando o
ticker não é.

O arquivo que faz a ponte é o **cadastro de companhias abertas**, e ele é pequeno:

```
https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv
```

> **CORRIGIDO EM 18/09/2026 — este parágrafo estava desatualizado, e do jeito mais caro:
> ele mandava você buscar um arquivo que já estava no projeto.**
>
> O texto anterior marcava o caminho e o nome como `NAO_CONFIRMADO`, *"vêm do meu
> conhecimento geral da estrutura da CVM, não de uma leitura da página"*, e pedia que
> você baixasse e mandasse o cabeçalho. **Você já tinha feito isso em 03/09/2026.** O
> resultado está em `docs/fontes/cvm-cadastro-companhias-abertas.md`, status **COMPLETO**,
> com o dicionário de 44 campos, o cabeçalho literal de 47 colunas e duas linhas de dado
> reais. A URL acima é a que foi de fato acessada, às 15:29:58 daquele dia.
>
> **E a pergunta da Marfrig está respondida:** `CD_CVM 20788`, situação ATIVO — e esse é
> exatamente o `codeCVM` que a B3 devolve no `MBRF.json`. A ponte que o A-04 precisava
> **existe**, e o que falta é usá-la, não obtê-la.
>
> *Por que isso importa mais que a economia de um download:* um documento de instrução que
> pede dado já obtido faz você gastar tempo provando algo provado, e — pior — sugere que a
> pergunta continua aberta quando ela está fechada. É o defeito recorrente do projeto na
> camada da prosa: **o arquivo declara um estado que o repositório não tem.**

**O que ainda vale baixar do cadastro, e só isso:** um retrato **novo**, com `sha256` e
hora, para `data\bronze\cvm\cad\`. O de 03/09 foi lido como documento, não registrado
como observação datada — não tem hash. Enquanto não tiver, ele prova a **estrutura** do
arquivo e não prova **o que a CVM dizia naquele dia**.

```powershell
Get-FileHash data\bronze\cvm\cad\cad_cia_aberta.csv -Algorithm SHA256
```

O A-04 fecha comparando o `CD_CVM 20788` contra o acervo da B3 — e isso roda sem download
nenhum, assim que você quiser.

---

## 6. Uma alternativa que muda o problema de lugar

Se o download manual semanal virar um peso — e ele vira, porque **P7: rotina que depende
de alguém lembrar não é rotina** —, a saída não é disciplina, é mudar onde a rotina mora.
O `CLAUDE.md` §11.6 já registra a decisão: a automação semanal vai para um servidor com
gatilho, rede e disco próprios, e o seu papel passa a ser conferir o inventário, não
produzi-lo.

**Enquanto isso não existe, o download manual é a ponte — e ela é honesta desde que o
hash e a data sejam registrados junto.** Um retrato sem hash não é um retrato: é um
arquivo.

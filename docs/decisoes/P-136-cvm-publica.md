# P-136, decisão 2 — servir ao público as versões da CVM

*25/09/2026. Decisão dele: **"pode ser público"**, e em seguida **"pode executar o desenho"**.
Executado no mesmo dia: `fase0/publicar_cvm.py` (17 testes; a mutação que tira a guarda da fonte
reprova) e o passo `Publicar CVM` do `captura_cvm.yml`. A primeira release sai na próxima
execução do workflow — plano medido sobre o registro real: **64 versões, uma release,
`cvm-acervo-2026`**.*

## O que se quer

A CVM serve só a versão **corrente** de cada arquivo, e reescreve toda semana os cinco anos
mais recentes do DFP e do ITR (CV-01, CV-02). As versões substituídas que o projeto capturou
**só existem no nosso R2**. Quem quiser reproduzir um número calculado sobre uma dessas versões
hoje não consegue — `docs/reproduzir.md` declara esse limite.

A licença permite resolver: o DFP é publicado sob **ODbL**, que autoriza redistribuir com
atribuição, aviso da licença e *share-alike* na base derivada
([`../fontes/cvm-dados-abertos-licenca.md`](../fontes/cvm-dados-abertos-licenca.md)).

## A restrição que manda no desenho

**O mesmo bucket guarda o COTAHIST e os eventos da B3, e os termos da B3 vedam publicá-los**
([`../fontes/b3-termos-de-uso.md`](../fontes/b3-termos-de-uso.md)). E o acesso público do R2 é
**do bucket**: a documentação da Cloudflare, lida em 25/09/2026, oferece duas formas — *"Expose
your bucket as a custom domain under your control"* ou *"using a Cloudflare-managed r2.dev
subdomain for non-production use cases"*. Nenhuma das duas é por prefixo. **Abrir o bucket atual
publicaria a B3.**

## As alternativas

| | o que é | custo para ele | risco |
|---|---|---|---|
| **A · Release do GitHub** (recomendada) | o workflow anexa cada versão da CVM como arquivo de uma release deste repositório | **nenhum**: usa o `GITHUB_TOKEN` do próprio workflow; nenhuma conta, nenhuma credencial nova | limite de **1.000 arquivos por release** (lido em 25/09: *"Up to 1000 release assets may be associated with a single release. Each file included in a release must be under 2 GiB. There is no limit on the total size of a release, nor bandwidth usage."*) |
| B · segundo bucket R2 público, só com `cvm/` | cópia dos objetos da CVM num bucket aberto | criar bucket, domínio ou r2.dev, e credencial — **tudo dele** (§3: "criar conta ou mexer em credencial é dele") | r2.dev é "non-production"; domínio próprio custa configuração; banda de saída do R2 é grátis, operação não |
| C · Zenodo, com DOI | depósito versionado com identificador citável | conta dele | depósito manual ou API com token dele; mais pesado que o problema |

## O desenho recomendado (A)

1. **Uma release por ano de captura**, `cvm-acervo-2026`, `cvm-acervo-2027`… — o limite de 1.000
   arquivos por release não é alcançado num ano (medido em 25/09: 52 arquivos no inventário, e a
   reescrita semanal traz da ordem de uma dúzia de versões novas por semana, ~600/ano).
   *Estimativa, não medição: o ritmo real sai do `capturas.csv` depois de algumas semanas.*
2. **Nome do arquivo = versão:** `<arquivo>__<sha256[:12]>.zip`, o mesmo esquema dos snapshots
   (CV-03). Nunca se sobrescreve: versão nova é arquivo novo.
3. **Notas da release** com a atribuição que a CVM exige (*"Dados acessados pelo Portal de Dados
   Abertos da CVM, disponível em https://dados.cvm.gov.br/"*), o nome da licença (ODbL 1.0) e o
   link, e a tabela de sha256 — que é o que `fase0/conferir_reproducao.py` compara.
4. **Idempotente e sem humano (P7):** um passo novo no `captura_cvm.yml`, depois da captura, lê o
   registro, lista o que a release já tem, e anexa só o que falta. Só objetos com
   `fonte == "cvm"` — a guarda que impede um byte da B3 de sair é **código com teste**, não
   convenção: o teste tenta publicar uma chave `b3/…` e exige recusa.
5. **Só a CVM.** O NEFIN também não (termos: não autoriza redistribuir).

## O que isso NÃO resolve (P5)

- As versões **anteriores a 24/09/2026** que estão só no disco dele e já subiram ao R2 pela carga
  inicial entram na primeira execução; versões que ninguém capturou continuam perdidas (CV-01).
- Uma release é pública e **não se despublica sem rastro**: quem baixou, baixou. É por isso que o
  passo 4 recusa qualquer coisa que não seja CVM, e que isto espera o OK dele.
- *Share-alike*: se um dia o projeto publicar uma **base derivada** da CVM (a série de
  fundamentos, por exemplo), ela sai sob ODbL também.

## O que foi executado (25/09/2026)

1. **Ele:** aprovou o desenho ("pode executar o desenho").
2. **Claude:** `fase0/publicar_cvm.py` + `fase0/test_publicar_cvm.py` (17 testes, inclusive a
   recusa da B3 **antes** do primeiro envio), o passo `Publicar CVM` no workflow com o
   `GITHUB_TOKEN` do job, e as linhas no `docs/reproduzir.md` e no `NOTICE`.
3. **Falta, e é do executor, não de ninguém:** a primeira rodada do workflow cria a release e
   envia as 64 versões. A P-136 fecha quando ela existir.

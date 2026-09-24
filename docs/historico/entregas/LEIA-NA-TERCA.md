> VENCIDO — executado em 10–11/09/2026 (8b98028; a coleta da B3 em b1d06f4). Não é instrução vigente.

# ADENDO de 06/09/2026, 20h — leia estas 20 linhas antes do resto

Depois que este arquivo foi escrito, uma pesquisa de bases e APIs mudou **a ordem da
Fase 0**. O resumo:

**Achado V-01 — falta um insumo que não estava em nenhum plano: eventos societários.**
Sem proventos, desdobramento e grupamento, uma série de preços não serve para backtest.
A PETR desdobrou 100:1 em 25/04/2008 — confirmei no endpoint da B3, em primeira mão. O
preço cai 99% num dia; o COTAHIST cru lê isso como um crash.

A fonte existe, é gratuita, é programática — e **não é documentada**. Sem contrato, sem
SLA, sem espelho. Por isso ela vem **antes** da CVM: DFP/ITR são ZIP estático em portal
oficial e não evaporam; este endpoint pode.

**Primeiros dois comandos de terça, nesta ordem:**

```powershell
python fase0\coletar_b3.py --indice IBOV
python fase0\coletar_b3.py --eventos
.\fase0.ps1 -SoConferir          # só depois, e ele ainda não baixa nada
```

**Novo na pasta:** `fase0\coletar_b3.py` (coletor, stdlib apenas),
`fase0\CELULAR-CVM.md` (o que dá para fazer do celular hoje, em 2 minutos),
`docs\fontes\pesquisa-bases-e-apis-2026-09.md` (a pesquisa inteira, com procedência).

O `PENDENCIAS.md` ganhou P-47 a P-53, e a seção **"Ao voltar ao desktop"** foi reescrita
do zero — a que existia era de ontem e citava 149 testes, quando hoje são 269.

---

# Leia isto ao ligar o computador — terça, 08/09/2026

Este pacote é o estado completo do projeto ao fim da sessão de **sábado, 05/09/2026**.
Ele existe porque o ambiente onde o trabalho foi feito é temporário e não sobrevive
até terça. **Tudo que importa está aqui dentro.**

---

## 0. Confira que chegou tudo — **faça isto primeiro**

Seu computador ficou desligado desde sexta 18h. Tudo o que foi feito depois disso vive
**só neste zip** — o container é temporário e não sobrevive até terça.

**São 32 arquivos em `alocacao/`, 4 em `docs/fontes/`, 3 em `dot-claude/skills/` e 4 na raiz.** Depois de extrair:

```powershell
cd alocacao
(Get-ChildItem *.py, *.yaml).Count      # tem de dar 32
cd ..
```

**Os 10 arquivos que NÃO existiam no seu commit de sexta** (se algum faltar, o zip veio
incompleto):

```
ACHADOS.md                      (novo — a história saiu do CLAUDE.md)
alocacao\perfil.yaml            alocacao\catalogo.yaml
alocacao\backtest_h1_h3.py      alocacao\instituicoes.yaml
alocacao\ambiente.py            alocacao\conftest.py
alocacao\impacto.py             alocacao\test_impacto.py
alocacao\test_p40_lint.py       pyproject.toml
alocacao\test_usuario_novo.py   alocacao\estado.exemplo.yaml
```

Mais `PENDENCIAS.md` e `docs\fontes\MAPA-CONSTANTES.md` na raiz e em docs.

**Um arquivo a atualizar à mão:** `gitignore-ATUALIZADO.txt` traz uma linha nova —
`.mypy_cache/`. Copie o conteúdo por cima do seu `.gitignore` (o nome vem diferente
porque um `.gitignore` dentro do zip seria aplicado ao próprio zip). Descobri isso do
jeito errado: o cache do mypy entrou no pacote e o inchou de 640 KB para **15 MB**.

**A série do NEFIN não mudou** e não pode mudar: `sha256[:12] = 619991c2192c`. Se o
`test_fonte_e_exatamente_a_serie_pre_registrada` falhar, foi o CRLF do Windows (achado
F-04) — o `.gitattributes` já protege, mas confira que ele sobreviveu ao extract.

---

## 1. Extraia por cima do repositório

Extraia na raiz do `Bastter`, sobrescrevendo. A estrutura já está correta:

```
CLAUDE.md              -> raiz          (substitui)
PENDENCIAS.md          -> raiz          (novo)
pyproject.toml         -> raiz          (novo)
alocacao/*             -> alocacao/     (substitui; perfil.yaml, backtest_h1_h3.py,
                                       ambiente.py, catalogo.yaml, instituicoes.yaml,
                                       conftest.py e impacto.py são novos)
docs/fontes/*          -> docs/fontes/  (MAPA-CONSTANTES.md é novo)
```

## 2. Confira antes de commitar

```powershell
cd alocacao
python ambiente.py          # NOVO — confere o ambiente antes dos testes
python -m pytest -q
cd ..
```

**Sobre o `ambiente.py`:** ele vai muito provavelmente acusar que o seu `numpy` e o seu
`pandas` são diferentes dos registrados (2.4.4 e 3.0.2). **Isso é informação correta,
não um problema para consertar às pressas.** Os 224 testes continuam verdes: o que
deixa de valer não é o código, é a *reprodução* de um resultado pré-registrado, que
passa a ser número novo em vez de conferência de número antigo.

Se quiser igualar, o comando sai do próprio arquivo:

```powershell
python ambiente.py --instalar    # imprime o pip install exato
```

Se preferir manter as suas versões, **atualize o `pyproject.toml` e re-registre a
impressão** em `politica.yaml → fontes.ambiente_de_execucao` (o teste
`test_P15_a_impressao_registrada_bate_com_o_pyproject` diz o valor novo). Aí o
ambiente de referência passa a ser o seu, que é uma escolha legítima — só precisa ser
uma escolha, e não um acidente.

**Esperado: `282 passed`.** O repositório na sua máquina está em 149 — a diferença são
133 testes escritos entre sexta e sábado.

Se der `FileNotFoundError: perfil.yaml`, faltou extrair um arquivo. `alocacao.py` novo
**não roda** sem `perfil.yaml`: a separação motor/usuário é carregada na inicialização.

```powershell
git status --short
git add -A
git commit -m "Backtest H1/H3, bloco C, regime de banco, perfil.yaml, LCI/LCA/FII

Achados: F-05 (bloqueia era prosa), I-01 (ordem dos portoes nunca foi G0-G8),
J-01/J-02 (reserva nao existe: o cofrinho e caucao de cartao), K-01 (Turbinado
nunca se paga pagando a mensalidade), L-01 (motor e usuario no mesmo arquivo),
M-01 (a alavanca do aporte e 10x a do destino; Fase A vai a mai/2031),
N-01 (a secao corretora declarava tres regras que so o Python decidia),
O-01/K-02 (o G2 media a media: prometia retorno sobre dinheiro que o produto recusa),
P-15 (o ambiente de execucao nao estava registrado; pyproject.toml + ambiente.py),
P-36/Q-01/Q-02 (o catalogo saiu do Python: 2 YAML, migracao com ZERO diferencas),
P-37/R-01 (alocar() de 300 linhas virou 6 passos; a ordem dos portoes so aceitava
18 das 120 ordens possiveis e ninguem sabia),
S-01/S-02 (o cache de arrasto ignorava o C recebido: todo teste que alterava um
custo testava nada; alocar() 9,79 -> 2,75 ms E correto),
P-38 (conftest com guarda de estado compartilhado), P-39 (impacto.py, mapa de
dependencias com os pontos cegos declarados),
P-40/T-01 (ruff e mypy em zero; e ha um TERCEIRO catalogo que ninguem tinha visto).
Doutrina P6 promovida. 282 testes.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

## 3. Suba para o GitHub

`gh` não está instalado. Crie em `github.com/new`, nome `bastter`, **Private**, e
**não** marque nada em "Initialize this repository" — se marcar, o push é rejeitado.

```powershell
git remote add origin https://github.com/SEU-USUARIO/bastter.git
git push -u origin main
```

---

## 3-A. Mudou como vamos trabalhar — leia a seção 11 do CLAUDE.md

Em 06/09 revisamos o método, e duas coisas mudaram:

**O que se lê toda sessão caiu pela metade.** `CLAUDE.md` foi de 1.112 para 482 linhas
e `PENDENCIAS.md` de 911 para 607 — a história migrou para o novo `ACHADOS.md`, que só
é lido quando a tarefa toca aquela área. Nada foi apagado. Eram ~26 mil tokens antes de
qualquer trabalho começar; agora são ~13 mil.

**A partir daqui, refatoração e git vão para o Claude Code** (incluído no seu plano Pro,
mesma cota). O ritual de zip existe só porque seu computador fica desligado — no
terminal o arquivo é editado onde mora. Este ambiente na nuvem continua melhor para
pesquisa, download da CVM/B3 e processamento pesado, que é o que a Fase 0 precisa.

---

## 3-A-bis. As três skills — renomeie a pasta `dot-claude` para `.claude`

O zip traz `dot-claude/skills/` com três skills do projeto. **Elas não precisam de
aprovação nenhuma**: no Claude Code, skills em `.claude/skills/` do repositório carregam
sozinhas quando você abre o projeto e aceita o diálogo de confiança do workspace.

O nome vem como `dot-claude` porque pasta começando com ponto costuma sumir do
explorador do Windows e de alguns descompactadores. Renomeie:

```powershell
Rename-Item dot-claude .claude
```

Se já existir um `.claude` no repositório, mova só o conteúdo:

```powershell
Move-Item dot-claude\skills\* .claude\skills\ -Force
Remove-Item dot-claude -Recurse
```

**Confira que ficou assim:**

```
.claude\skills\bastter-mudanca\SKILL.md
.claude\skills\bastter-achado\SKILL.md
.claude\skills\bastter-proximo-passo\SKILL.md
```

| skill | para quê |
|---|---|
| `bastter-mudanca` | o protocolo: `impacto.py` → instantâneo dourado → suíte → lint → registrar |
| `bastter-achado` | como registrar um defeito: a medição que o prova e o teste que o prende |
| `bastter-proximo-passo` | as duas formas como eu errei a escolha do próximo passo (U-01 e P-44) |

**Versionadas com o projeto**: entram no git, valem para quem clonar, e mudam junto
com o método.

### As mesmas skills valendo no Claude web e no Cowork

Skills do repositório só valem no Claude Code. Para valerem também no app, elas
precisam estar na **conta** — e o caminho é `Customize → Skills → Add`, subindo um zip
por skill (código de execução precisa estar ligado em `Settings → Capabilities`).

Os três zips foram entregues na conversa de 06/09. **Cada um tem a pasta da skill na
raiz**, que é o formato exigido, e a `description` de cada uma foi encurtada para caber
no limite de 200 caracteres do app.

**Fonte única:** os zips são GERADOS a partir de `.claude/skills/`. Se você editar uma
skill, regere o zip e suba de novo — não edite os dois lados. Duas cópias que podem
discordar é exatamente o achado N-01, e ele já apareceu quatro vezes neste projeto.

```powershell
# regerar depois de editar (no PowerShell, da raiz do repo)
Compress-Archive -Path .claude\skills\bastter-mudanca -DestinationPath bastter-mudanca.zip -Force
```

---

## 3-B. Uma correção sua mudou o roteiro — achado U-01

Você apontou que "não ter reserva ou aporte ser barreira de desenvolvimento" é
estranho: um cliente novo de um produto teria zero de tudo, e o sistema teria de
responder mesmo assim.

**Está certo, e o motor já se comporta assim** — o que estava errado era o meu roteiro.
Três coisas mudaram:

- **`test_usuario_novo.py`** (13 testes) mede a primeira experiência como comportamento
  do sistema. Patrimônio zero, nada assinado: sai *"R$800/mês para o Tesouro Reserva até
  R$10 mil, depois RDB; 23 meses até o alvo"*. Com a reserva pronta, sai carteira de 7
  rotas. Nenhum desses testes lê o seu `estado.yaml`, e há uma guarda que recusa.
- **`estado.exemplo.yaml`** — o cadastro mínimo. Torna visível que o sistema pergunta
  **quatro** fatos de vida (despesa, estabilidade, aporte, horizonte) e que todo o
  **patrimônio** começa vazio.
- **Toda pendência agora declara classe.** São 22 `BLOQUEIA_O_SISTEMA`, 5
  `DECISAO_DE_DESENHO` e **2** `DADO_DE_UM_USUARIO` — e eu tinha essas duas (P-01, P-02)
  no caminho crítico.

---

## 4. O que fazer depois, em ordem

**1. Fase 0 do pipeline — CVM DFP/ITR com bitemporalidade.** ⚙ exige o desktop.
Virou o único caminho: dois dos três testes pré-registrados terminam nela (H1 precisa
das pernas do HML, H2 precisa da carteira de DY), e o regime de banco revelou que ela
não cobre metade do Ibovespa. **Tem prazo:** a CVM sobrescreve os arquivos anuais e
`DT_RECEB` não se reconstrói depois.

**2. Segunda esteira: BCB.** Decidida por você em 05/09 — banco não sai do universo.
Basileia e inadimplência não estão na CVM. A ordem entre as duas esteiras continua
aberta, e o argumento é: a da CVM serve aos dois caminhos da A05, a do BCB só a um.

**3. Reconciliar C-04 e C-05** com `auditoria/escopo-campos-de-analise.md`. O regime do
bloco C está escrito, mas dois dos cinco campos nunca foram nomeados — não os inventei.

**4. Ligar o que já está especificado (P-29 a P-31).** Não exige o desktop, exige
decisão de ordem. `bloco_C_solvencia` (48 chaves), `regime_instituicao_financeira`
(46) e `estrategias_pre_registradas` (121) estão **escritas e não ligadas ao motor** —
a varredura completa de sábado é que as revelou. As duas primeiras dependem da Fase 0
para ter dado; a terceira depende do backtest completo.

**5. Contar `SETOR_ATIV`** no dado real da CVM, como foi feito com `ORDEM_EXERC`. Sem
isso, a recusa automática de instituição financeira não pode ser codificada.

---

## 5. O que continua esperando **você**, e não código

- **Assinar os dois registros** em `teses.yaml`: apagar `exemplo: true` nos dois,
  `C06_reconhecimento: true`, e colar as impressões (`31a31607f3c60e62` para o HASH11,
  `942c75bae248327b` para o td_ipca). **Antes de assinar o HASH11, decida se quer a
  posição** — "não compro" é resolução completa e custa zero.
- **Onde constituir a reserva.** Ela é **zero** — não travada, nunca constituída. Os
  candidatos são `td_reserva` (Selic, isento de custódia até R$10 mil) e o Cofrinho
  Turbinado com isenção. O G2 escolhe assim que o destino existir.
- **O aporte realizado.** R$500 é o piso planejado; o realizado é zero.

---

## 6. Se abrir uma sessão nova do Claude

Leia o `CLAUDE.md` primeiro — ele tem as seis doutrinas, as três regras permanentes de
sessão e os achados de sexta e sábado. O `PENDENCIAS.md` tem as 43 pendências com dono
e gatilho, e a lista do que já foi fechado, que é o que impede uma sessão nova de
reabrir tarefa pronta.

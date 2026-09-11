# Recriar o repositório no GitHub — 11/09/2026

O local já está pronto: histórico limpo, `main` renomeada, `estado.yaml` fora do índice.
**Falta só o repositório do outro lado** — você apagou o antigo e ainda não criou o novo,
e é por isso que o push respondeu `Repository not found`.

---

## Passo 1 — criar o repositório vazio (no navegador)

Abra **github.com/new** e preencha exatamente assim:

| campo | valor |
|---|---|
| Owner | `OsvaldoSantana` |
| Repository name | **`bastter`** |
| Description | opcional |
| Visibilidade | **Public** |
| Add a README file | **desmarcado** |
| Add .gitignore | **None** |
| Choose a license | **None** |

Clique em **Create repository**.

> **Por que nada de inicialização.** Se o GitHub criar um commit inicial (README, licença
> ou .gitignore), o repositório remoto passa a ter um histórico que o seu não conhece, e o
> push é recusado com `fetch first`. Aí a saída seria um merge desnecessário no primeiro
> dia de vida do repositório.

> **Por que Public.** Decisão sua, de 06/09 (P-62), e ela é a melhor: repositório público
> tem GitHub Actions **sem consumo de cota** e runner maior (4 vCPU / 16 GB contra 2 / 8) —
> e é lá que a rotina semanal da Fase 0 vai morar. A regra dos 60 dias que desativa cron
> por inatividade **não morde**, porque o próprio workflow commita o delta toda semana.

---

## Passo 2 — conferir antes de empurrar (no PowerShell)

```powershell
cd C:\Users\osvaldo.junior\Desktop\Bastter
git ls-files | Select-String "estado.yaml|Claude outputs"
```

**Tem que sair vazio.** Se sair qualquer linha, **pare** e me mande o resultado — é a
única conferência desta lista que não pode ser pulada, e é a P-67.

E rode a suíte, agora que o pytest está instalado:

```powershell
cd alocacao ; python -m pytest -q ; cd ..
```

Se `test_p67_segredo.py` passar, o índice está limpo por medição, não por confiança.

---

## Passo 3 — empurrar

O `origin` já está apontado para o endereço certo (você o adicionou antes de apagar o
repositório), então basta:

```powershell
git push -u origin main
```

### Se der erro

| mensagem | o que é | o que fazer |
|---|---|---|
| `Repository not found` | o Passo 1 não foi concluído, ou o nome saiu diferente | confira o nome em `github.com/OsvaldoSantana?tab=repositories` |
| `remote origin already exists` | ao tentar `git remote add` de novo | use `git remote set-url origin https://github.com/OsvaldoSantana/bastter.git` |
| `failed to push some refs` / `fetch first` | o repositório foi criado **com** README ou licença | `git push -u origin main --force` — é seguro aqui: o remoto só tem o commit automático do GitHub, e o seu é a versão boa |
| pede autenticação | normal na primeira vez | ele abre o navegador; você já autenticou uma vez, deve passar direto |

---

## Passo 4 — conferir do lado de fora, no navegador

Abra `github.com/OsvaldoSantana/bastter` e confira **três coisas**:

1. **Não existe** `alocacao/estado.yaml` na árvore de arquivos.
2. **Não existe** a pasta `Claude outputs/`.
3. **Existe** `alocacao/estado.exemplo.yaml` — ele *deve* estar lá; é a prova do achado
   U-01, de que o sistema funciona sem dado de usuário nenhum.

Conferir na interface do GitHub, e não só no `git ls-files`, é de propósito: são duas
testemunhas independentes do mesmo fato. O `ls-files` diz o que o seu git acha que mandou;
a página diz o que o GitHub realmente recebeu.

---

## Passo 5 — o commit de arrumação

Ficaram alguns arquivos de andaime no repositório, que existiram só para a limpeza:

```powershell
git rm --cached LEIA-AGORA.md gitignore-CORRIGIDO.txt gitignore-ATUALIZADO.txt
git commit -m "Remove andaimes da limpeza de 10-11/09

LEIA-AGORA.md e os dois gitignore-*.txt serviram a uma operacao de uma vez.
O .gitignore em vigor e o unico que vale; manter copias e a mesma armadilha
do 'Claude outputs/' em escala menor: arquivo que parece fonte e nao e.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push
```

> `--cached` remove **do git**, não do disco. Os arquivos continuam na sua pasta.

---

## Depois disso, a Fase 0 destrava

Com o repositório no ar, estes dois comandos são o próximo passo real do projeto — e são
o único item da fila que pode **deixar de existir** se não for capturado:

```powershell
python fase0\coletar_b3.py --indice IBOV
python fase0\coletar_b3.py --eventos
```

O primeiro captura a carteira teórica do Ibovespa do dia (ela só existe para o dia
corrente). O segundo, os eventos societários — proventos, desdobramentos, grupamentos —
por um endpoint da B3 **sem contrato e sem espelho conhecido**.

Lembre da armadilha embutida, que está comentada no próprio script: chave errada devolve
HTTP 200 com listas vazias, **em silêncio**. O coletor acusa em voz alta em vez de gravar
ausência como se fosse dado. Se ele reclamar de alguma emissora, **é ele funcionando**.

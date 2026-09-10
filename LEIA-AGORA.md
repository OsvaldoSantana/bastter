# LEIA AGORA — 10/09/2026

**O push funcionou. E ele levou junto uma coisa que não podia ir.**

---

## 1. O problema, em uma frase

`alocacao/estado.yaml` — patrimônio, aporte e dívida reais — **foi commitado e
empurrado para o GitHub**. Aparece no `git status` que você colou, como `M
alocacao/estado.yaml`, e no commit `afc1c0a`. E há uma **segunda cópia** dele dentro de
`Claude outputs/bastter-06set2026-v2/alocacao/estado.yaml`.

Enquanto o repositório estiver **privado**, isso está contido. **Não o torne público
antes de resolver** — e a decisão da P-62 era justamente torná-lo público.

> **Apagar o arquivo num commit novo não resolve.** Commit empurrado não se desfaz
> editando o arquivo depois: o conteúdo continua no histórico, e qualquer pessoa com
> acesso ao repositório consegue lê-lo.

### E isso é exatamente a P-67

Eu abri a P-67 no sábado com estas palavras: *"a decisão depende de uma linha de
`.gitignore`, e uma linha de `.gitignore` é exatamente o tipo de coisa que se perde
sem ninguém notar. Falta o teste que impede."*

**A pendência foi aberta e o teste não foi escrito.** Entre uma coisa e outra houve um
`git add -A`. É a tese do projeto inteiro aplicada contra ele mesmo: um arquivo
declarava um comportamento e nada media se ele acontecia — F-05, N-01, R-01, S-02, e
agora esta.

O teste agora existe: **`alocacao/test_p67_segredo.py`**, já na sua pasta. Ele falha
contra a versão de hoje e passa depois da limpeza. Eu conferi as duas coisas.

---

## 2. O outro problema: `Claude outputs/` foi para o repositório

118 arquivos, incluindo o `.zip` de 700 KB e **uma cópia inteira do projeto** —
`alocacao/motor.py`, `politica.yaml`, `custos.yaml`, tudo em duplicata.

Não é questão de tamanho. É a armadilha do `pesquisa-custos-2026-08/calc/` outra vez,
e pior: **lá a pasta ao menos tem nome diferente.** Uma sessão futura que abrir
`Claude outputs/bastter-06set2026-v2/alocacao/motor.py` estará lendo uma versão
congelada, e nada no arquivo avisa.

---

## 3. A limpeza — 4 minutos, nesta ordem

### Passo 0 — pausar o OneDrive

Ícone da nuvem na barra de tarefas → **Pausar sincronização → 2 horas**.

Foi o OneDrive que travou o `Remove-Item dot-claude` ontem ("você não tem direitos de
acesso suficientes"). Ele segura o lock dos arquivos enquanto sincroniza.

### Passo 1 — trocar o `.gitignore`

```powershell
cd "C:\Users\osvaldo.junior\OneDrive - VOLGA ENGENHARIA IND. E COMERCIO LTDA\Área de Trabalho\Bastter"
Copy-Item gitignore-CORRIGIDO.txt .gitignore -Force
Remove-Item dot-claude -Recurse -Force
```

O novo `.gitignore` cobre `alocacao/estado.yaml`, `Claude outputs/`, `*.zip` e
`dot-claude/` — cada um com o motivo escrito, como manda a regra da casa. E mantém
`estado.exemplo.yaml` **dentro**, porque ele é a prova do achado U-01.

### Passo 2 — apagar o repositório no GitHub

`github.com/OsvaldoSantana/bastter` → **Settings** → rolar até o fim → **Danger
Zone** → **Delete this repository**.

> **Por que apagar em vez de reescrever o histórico.** Reescrever exige
> `git filter-repo` (instalação, sintaxe própria, e um erro silencioso deixa o
> segredo lá). São **dois commits, de dois dias, sem ninguém mais usando o
> repositório**. O histórico do projeto de verdade não está no git — está no
> `ACHADOS.md` e no `PENDENCIAS.md`, em texto, com data. **O que se perde é
> desprezível; o que se garante é que o segredo não ficou.**

### Passo 3 — recomeçar o histórico

```powershell
Remove-Item .git -Recurse -Force
git init
git add -A
```

### Passo 4 — CONFERIR ANTES DE COMMITAR

```powershell
git ls-files | Select-String "estado.yaml|Claude outputs"
```

**Tem que sair vazio.** Se sair qualquer linha, pare e me mande o resultado.

E rode a suíte — o teste novo lê o índice do git, então ele só funciona depois do
`git add`:

```powershell
cd alocacao ; python -m pytest -q ; cd ..
```

Esperado: tudo verde, com **3 testes a mais** que antes.

### Passo 5 — commitar e subir

```powershell
git commit -m "Historico refeito: remove estado financeiro real e copia congelada do projeto

O primeiro push (08/09) levou alocacao/estado.yaml e a pasta 'Claude outputs/'.
Historico recriado do zero em vez de reescrito: dois commits, sem colaboradores,
e a historia do projeto vive no ACHADOS.md, nao no git.

P-67 fechada: test_p67_segredo.py mede o INDICE do git, nao o disco, e falha
contra a versao anterior. Terceiro teste guarda o proprio .gitignore, para que
`git rm --cached` nao deixe a suite verde e errada.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

Crie o repositório de novo em `github.com/new`, nome `bastter`, **Public** desta vez,
sem marcar nada em "Initialize this repository". Depois:

```powershell
git remote add origin https://github.com/OsvaldoSantana/bastter.git
git push -u origin main
```

### Passo 6 — religar o OneDrive

E leia a seção 4 antes.

---

## 4. Uma coisa que não é sobre o GitHub, e é sua para decidir

O projeto está em:

```
C:\Users\osvaldo.junior\OneDrive - VOLGA ENGENHARIA IND. E COMERCIO LTDA\...
```

**É o OneDrive corporativo da Volga.** Isso significa, factualmente:

- `alocacao/estado.yaml` — seu patrimônio, seu aporte, sua dívida — **está
  sincronizado no tenant do seu empregador**. Em ambiente corporativo, o
  administrador do Microsoft 365 normalmente tem meios de acessar o conteúdo do
  OneDrive de um usuário, e há retenção e backup do lado da empresa.
- Isso já aconteceu, e continua acontecendo enquanto a pasta estiver ali. **Não tem
  nada a ver com o GitHub** — é uma exposição separada, e ela existia antes do push.
- E é o mesmo OneDrive que trava seus arquivos e fez o `Remove-Item` falhar.

**Sugestão:** mover a pasta para fora do OneDrive corporativo — algo como
`C:\dev\bastter` ou uma pasta pessoal. O git não se importa com o caminho; é recortar
e colar, e depois `cd` para o novo lugar.

Eu não sei qual é a política da Volga nem o quanto isso te incomoda. **Você decide** —
mas prefiro que decida sabendo.

---

## 5. Ainda pendente da entrega de terça

Nada disso foi feito ainda, e continua valendo depois da limpeza:

```powershell
python fase0\coletar_b3.py --indice IBOV     # o dado que pode sumir
python fase0\coletar_b3.py --eventos
python fase0\cvm_catalogo.py --procurar dfp  # confirma o caminho da API CKAN
```

E lembre que o `CLAUDE.md` que você tem agora fala em **sete** doutrinas — a P7 é sua,
de sábado: *"uma rotina que depende de alguém lembrar não é uma rotina."*
O `LEIA-NA-TERCA.md` ainda diz "seis doutrinas" e "43 pendências"; ele é de sexta e
está desatualizado. O `CLAUDE.md` e o `PENDENCIAS.md` são os corretos.

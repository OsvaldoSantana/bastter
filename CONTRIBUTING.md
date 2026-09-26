# Contribuir com o MEOL

Issues e pull requests são bem-vindos. O projeto é escrito em português, e a prosa de uma
contribuição também. Se você chegou agora, o [guia do leitor](docs/guia-do-leitor.md) tem um
caminho de 30 minutos que atravessa o sistema inteiro por um número.

## Instalar

Requer **Python 3.11**. A faixa é fechada de propósito: um resultado pré-registrado só se
reproduz no ambiente que o produziu.

```bash
git clone https://github.com/OsvaldoSantana/meol.git
cd meol
python -m pip install ".[dev,lint,paralelo]"
python alocacao/ambiente.py      # confere o instalado contra o declarado
```

As versões ficam num lugar só, o [`pyproject.toml`](pyproject.toml), com pino exato (`==`). Não
existe `requirements.txt`, e isso é de propósito: duas listas de versões que concordam por
acidente param de concordar sem ninguém ver.

## Testar

Durante a mudança, a suíte que você tocou, sem os lentos:

```bash
python -m pytest <pasta> -m "not slow and not privado and not acervo" -n auto --dist loadgroup
```

Antes de abrir o PR, as quatro suítes, e o lint e os tipos em zero:

```bash
for s in alocacao fase0 auditoria tools medicoes; do
  python -m pytest $s -m "not privado and not acervo" -n auto --dist loadgroup -p no:cacheprovider
done
python -m ruff check alocacao fase0 auditoria tools medicoes
for d in alocacao fase0 auditoria tools medicoes; do (cd $d && python -m mypy .); done
```

Três marcadores ficam fora de um clone. `acervo` e `slow` leem o dado de mercado, que mora num
armazém privado ([por quê](docs/reproduzir.md)). `privado` lê a situação financeira real do
dono. O CI roda o rápido em todo PR, e o completo, com o armazém, toda semana.

## As regras da casa

1. **Um achado, um teste que falha na versão anterior.** Um teste que passaria antes e depois
   da mudança não prova nada. E vale para código novo também: arquivo novo em `fase0/` ou
   `alocacao/` nasce com o seu `test_<nome>.py`.
2. **Número com procedência.** Valor novo entra no YAML com `fonte`, `status` e data de
   acesso, nunca como literal no código. Um cálculo que dependa de valor não confirmado deve
   **recusar-se a rodar**, e nunca usar zero ([P1](docs/doutrinas.md)).
3. **Leia os achados da área antes de mexer nela.** Vários defeitos deste projeto são o mesmo
   padrão com outra roupa, e o [`ACHADOS.md`](ACHADOS.md) diz quais.

O protocolo completo de mudança (medir o impacto, instantâneo dourado, registrar) está no
[`CLAUDE.md`](CLAUDE.md), §9. Ele foi escrito para as sessões de IA que trabalham aqui, e vale
igual para você.

## Convenção de commit

- **Título com até 72 caracteres**, dizendo o que mudou, com o código do achado quando houver
  (`CI-04: ...`, `P-145: ...`).
- **Corpo com o porquê**: o que a mudança mediu ou provou, e o que ela não cobre.
- Código e YAML em ASCII, sem acento. Markdown com acentuação normal.

## Segurança e conduta

Vazamento de dado pessoal conta como vulnerabilidade: veja o [`SECURITY.md`](SECURITY.md). A
convivência segue o [Código de Conduta](CODE_OF_CONDUCT.md).

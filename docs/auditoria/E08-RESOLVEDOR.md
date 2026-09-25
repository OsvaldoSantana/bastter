# E-08 — o resolvedor de referência no `instituicoes.yaml`

**Fechado em 13/09/2026.** Decisão sua: resolvedor, não remoção dos números.

---

## O que estava errado, em duas metades

**E-08a — o `bloqueia` que nomeia o consumidor, e o consumidor que não pergunta.**

```yaml
custos.yaml -> corretagem.xp_swing:
  valor: 4.9
  status: PARCIAL
  bloqueia: ["ranking_corretoras"]     # nomeia ESTE consumidor
```

E o ranking rodava, devolvendo **46,0** para a XP. `pontuar()` lia `inst.corretagem_rv`
do `instituicoes.yaml` e **nunca chamava `val()`** — a consequência declarada não
chegava nele. A incerteza era tratada por um **multiplicador de 0,8**, que desconta em
vez de barrar.

> **Não é que alguém escolheu o multiplicador: ninguém escolheu.** Os dois mecanismos
> são deliberados, moram em arquivos diferentes e não se conhecem. **O layout dos
> arquivos decidia qual vencia** — e vencia o mais fraco, porque era o do caminho que
> executa. É o F-05 pela metade: `bloqueia` deixou de ser prosa para quem passa por
> `val()`; para quem não passa, continuou prosa.

**E-08b — a cópia não herdava o relógio.** Seis números viviam nos dois arquivos. As
cinco constantes de `corretagem` têm `expira: 2026-12-04`; as seis cópias **não tinham
campo de validade nenhum**. Em 05/12/2026 o `val()` avisaria para quem referencia e as
cópias continuariam valendo, caladas, para sempre.

---

## O desenho

`{de: "corretagem.xp_etf_pct"}` agora é aceito em qualquer campo de custo do
`instituicoes.yaml`, e a resolução **passa por `val()`** — é isso que faz o resto cair
de graça: status, procedência, `expira`, `bloqueia`.

Três regras, e cada uma responde a uma pergunta que já tinha sido errada antes:

| situação | resposta | por quê |
|---|---|---|
| constante `COMPLETO` | o valor | nada muda |
| constante **bloqueia o contexto declarado** | `None` + motivo em `bloqueios` | o `bloqueia` nomeia um consumidor; quem se nomeia, obedece |
| constante `NAO_CONFIRMADO` | `None` + motivo | sem valor não há o que devolver a ninguém |

**O `contexto` é opcional de propósito.** Sem contexto, `bloqueia` não é checado — *um
consumidor que não se nomeia não pode reivindicar um bloqueio dirigido a outro*.
`bloqueia: [ranking_corretoras]` fala do ranking, não de quem só quer ler o cadastro.
`NAO_CONFIRMADO` barra nos dois casos, porque ali não existe valor.

**E o `None` não é um buraco:** é o valor que `pontuar()` **já sabia tratar** — ele marca
a dimensão como não avaliada e a `cobertura` penaliza. *"Dimensão ausente é penalidade,
não neutralidade"* já estava escrito lá dentro. O resolvedor não inventou tratamento
nenhum; apenas fez o dado chegar até o tratamento que existia.

O ranking passou a **se nomear**:

```python
for i in catalogo_instituicoes(contexto=RANKING):
```

Uma linha. É ela que transforma a frase do YAML em comportamento.

---

## O que mudou, medido — e leia com atenção, porque o número engana

```
XP, antes:   total 46,0   corretagem = 2,0 (nota)      multiplicador 0,80
XP, depois:  total 45,9   corretagem = None            nota "corretagem NÃO CONFIRMADA"
```

**A nota praticamente não mudou.** Perder a dimensão tira um peso de 12 que estava
valendo 2,0 — os dois efeitos quase se cancelam.

> **E isso não torna a correção menor.** O que mudou não foi *quanto*, foi **o que o
> sistema afirma**. Antes ele dizia *"a corretagem da XP é ruim, nota 2,0"* — uma
> afirmação sobre um número que o próprio projeto declarava não conseguir ler. Agora diz
> *"não sei ler a corretagem da XP, e isso custa cobertura"*.
>
> **Uma correção de honestidade pode não mexer no resultado, e continua sendo
> correção.** Um engenheiro com pressa chamaria isto de "sem impacto". O impacto é
> epistêmico: o sistema parou de asserir o que ele mesmo dizia não saber.

As seis referências, sem contexto, devolvem **exatamente** os valores de antes — 4,9 ·
0,005 · 4,49 · 0,0002 · 4,5 · 4,5. Instantâneo dourado no teste.

---

## A prova de que a mudança é inerte no que já existia

```
falhas SO com o E-08:   (nenhuma)
falhas SO sem o E-08:   (nenhuma)
iguais nos dois:        12
```

As 12 são pré-existentes (P-15 de ambiente e P-40 de lint, por falta de
`pyproject.toml`/`ruff` no meu ambiente). **Nenhuma falha nova, nenhuma sumiu.** E
`test_corretoras.py` continua **26 verdes**.

**17 testes novos**, zero `xfail` — os sete que antes documentavam defeito aberto agora
medem o conserto. Entre eles, o que eu mais gosto:

```python
motor.HOJE = dt.date(2027, 1, 1)        # depois do vencimento
K.catalogo_instituicoes()
assert "expirou" in capsys.readouterr().err
```

Ele **adianta o relógio** e confirma que o aviso de expiração agora sai também para o
`instituicoes.yaml`. O relógio existia; faltava ligar o outro lado nele.

---

## O que ficou aberto, e é seu

O resolvedor aceita `{de:}` em **qualquer** campo, mas só os seis custos duplicados
foram convertidos. Os outros números do `instituicoes.yaml` — PL, resultado
trimestral, índices do BC — **não têm constante correspondente no `custos.yaml`** e
continuam literais, o que está certo: eles não são duplicata de nada.

A pergunta que sobra é a da P-78: **o ranking deve pontuar custo por operação** além da
corretagem de ação (`mesa_minimo`, `corretagem_fii`, `exercicio_opcao_pct`)? Se sim,
esses três viram constantes no `custos.yaml` com procedência, e o `instituicoes.yaml`
passa a referenciá-los pelo mesmo mecanismo que acabou de nascer.

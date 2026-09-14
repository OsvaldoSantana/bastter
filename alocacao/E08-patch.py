# -*- coding: utf-8 -*-
"""E-08: resolvedor de referencia no instituicoes.yaml. Idempotente."""
import io, os, sys
import yaml

MARCA = "E-08, 13/09/2026"
AQUI = os.path.dirname(os.path.abspath(sys.argv[0] if len(sys.argv) > 1 else __file__))
base = sys.argv[1] if len(sys.argv) > 1 else "."

pc = os.path.join(base, "corretoras.py")
pi = os.path.join(base, "instituicoes.yaml")
sc = io.open(pc, encoding="utf-8").read()
si = io.open(pi, encoding="utf-8").read()
if MARCA in sc:
    sys.exit("ja aplicado: a marca do E-08 ja esta em corretoras.py")

# ── 1. corretoras.py: import ────────────────────────────────────────────────
V = '''from alocacao import carregar_politica'''
N = '''from alocacao import carregar_politica, _caminho
from motor import carregar as carregar_custos, val, InsumoBloqueado'''
assert V in sc, "import de carregar_politica nao encontrado -- PARE"
sc = sc.replace(V, N, 1)

# ── 2. dataclass: bloqueios + confiavel ─────────────────────────────────────
V = '''    home_broker_web: bool | None = None
    exporta_csv: bool | None = None
'''
N = '''    home_broker_web: bool | None = None
    exporta_csv: bool | None = None
    # E-08, 13/09/2026. Espelha `RotaAloc.bloqueios`: motivos que tiram um campo de
    # circulacao sem tirar a instituicao do catalogo. Vem da resolucao de `{de:}`.
    bloqueios: list = field(default_factory=list)

    @property
    def confiavel(self):
        return not self.bloqueios
'''
assert V in sc, "fim da dataclass nao encontrado -- PARE"
sc = sc.replace(V, N, 1)
sc = sc.replace("from dataclasses import dataclass",
                "from dataclasses import dataclass, field", 1)

# ── 3. o resolvedor ─────────────────────────────────────────────────────────
V = '''def catalogo_instituicoes(path=None):'''
N = '''# ── E-08, 13/09/2026: o resolvedor de referencia ────────────────────────────
RANKING = "ranking_corretoras"


def _resolver(valor, C, campo, iid, contexto, bloqueios):
    """`{de: "corretagem.xp_etf_pct"}` -> o valor do custos.yaml, passando por `val()`.

    ACHADO E-08. Ate aqui o `instituicoes.yaml` so aceitava literal, e por isso SEIS
    numeros existiam duas vezes: uma no `custos.yaml`, com status, fonte e `expira`, e
    outra aqui, crua. As copias concordavam -- e o N-01 e sobre o dia em que param.

    Pior que a divergencia futura era o RELOGIO. As cinco constantes de `corretagem`
    expiram em 04/12/2026; as seis copias nao tinham campo de validade nenhum. O
    projeto construiu um mecanismo de vencimento e metade dos numeros nao estava ligada
    nele. Passar por `val()` resolve isso de graca: o aviso de `expira` sai em stderr
    para quem referencia.

    E RESOLVE O OUTRO LADO DO E-08, que e o que importa mais. `corretagem.xp_swing` e
    PARCIAL e declara `bloqueia: ["ranking_corretoras"]` -- nomeia ESTE consumidor. O
    ranking rodava assim mesmo, porque lia a copia e nunca chamava `val()`: a
    consequencia declarada nao chegava nele. Agora chega. Quem carrega o catalogo diz
    QUEM e (`contexto`), e uma constante que bloqueia esse nome devolve `None`.

    `None` nao e um buraco: e o valor que `pontuar()` ja sabia tratar -- ele marca a
    dimensao como nao avaliada e a `cobertura` penaliza. **Dimensao ausente e
    penalidade, nao neutralidade**, que e o que o proprio `pontuar` ja dizia.

    O contexto e OPCIONAL de proposito. Sem contexto, `bloqueia` nao e checado -- um
    consumidor que nao se nomeia nao pode reivindicar um bloqueio dirigido a outro.
    NAO_CONFIRMADO continua barrando em qualquer caso, porque ali nao ha valor nenhum.
    """
    if not (isinstance(valor, dict) and "de" in valor):
        return valor
    caminho = valor["de"]
    no = _caminho(C, caminho)
    if contexto and contexto in (no.get("bloqueia") or []):
        bloqueios.append("%s.%s: %s bloqueia %s — %s"
                         % (iid, campo, caminho, contexto,
                            no.get("motivo", "sem motivo declarado")))
        return None
    try:
        return val(no, contexto="%s.%s -> %s" % (iid, campo, caminho))
    except InsumoBloqueado as e:
        bloqueios.append("%s.%s: %s" % (iid, campo, str(e)[:160]))
        return None


def catalogo_instituicoes(path=None, C=None, contexto=None):'''
assert V in sc, "def catalogo_instituicoes nao encontrado -- PARE"
sc = sc.replace(V, N, 1)

# ── 4. resolver dentro do laco ──────────────────────────────────────────────
V = '''    d = carregar_instituicoes_cru(path)
    out = []
    for iid, cru in d["instituicoes"].items():'''
N = '''    d = carregar_instituicoes_cru(path)
    # E-08: so carrega o custos.yaml se houver referencia a resolver. Quem nunca usa
    # `{de:}` nao paga por ele.
    precisa = "de:" in io.open(path or INSTITUICOES_YAML, encoding="utf-8").read()
    if precisa and C is None:
        C = carregar_custos()
    out = []
    for iid, cru in d["instituicoes"].items():'''
assert V in sc, "inicio do laco nao encontrado -- PARE"
sc = sc.replace(V, N, 1)

V = '''        campos["confirmacao"] = STATUS_PARA_LETRA[st]
        campos["fonte"] = proc["custos"]["fonte"]
        out.append(Instituicao(id=iid, **campos))'''
N = '''        campos["confirmacao"] = STATUS_PARA_LETRA[st]
        campos["fonte"] = proc["custos"]["fonte"]
        bloqueios = []
        if C is not None:
            campos = {k: _resolver(v, C, k, iid, contexto, bloqueios)
                      for k, v in campos.items()}
        out.append(Instituicao(id=iid, bloqueios=bloqueios, **campos))'''
assert V in sc, "fim do laco nao encontrado -- PARE"
sc = sc.replace(V, N, 1)

# ── 5. o ranking se NOMEIA ──────────────────────────────────────────────────
V = '''    out = []
    for i in catalogo_instituicoes():
        p = pontuar(i, pesos, aporte, horizonte_anos, P)'''
N = '''    out = []
    # E-08: o ranking diz QUEM E. `corretagem.xp_swing` declara
    # `bloqueia: ["ranking_corretoras"]`, e ate 13/09/2026 essa frase nao alcancava
    # ninguem. Nomear-se aqui e o que a transforma em comportamento.
    for i in catalogo_instituicoes(contexto=RANKING):
        p = pontuar(i, pesos, aporte, horizonte_anos, P)'''
assert V in sc, "laco do ranking nao encontrado -- PARE"
sc = sc.replace(V, N, 1)

sc = sc.replace("import os, sys", "import io, os, sys", 1)
sc = sc.replace('"""\nfrom __future__', '"""\n# %s\nfrom __future__' % MARCA, 1)

# ── 6. instituicoes.yaml: as seis copias viram referencia ───────────────────
PARES = [
    ("corretagem_rv: 4.9",     'corretagem_rv: {de: "corretagem.xp_swing"}'),
    ("corretagem_etf_pct: 0.005", 'corretagem_etf_pct: {de: "corretagem.xp_etf_pct"}'),
    ("corretagem_rv: 4.49",    'corretagem_rv: {de: "corretagem.caixa_fixa"}'),
    ("corretagem_pct: 0.0002", 'corretagem_pct: {de: "corretagem.caixa_pct"}'),
    ("corretagem_rv: 4.5",     'corretagem_rv: {de: "corretagem.safra_terra"}'),
]
trocas = 0
for velho, novo in PARES:
    n = si.count(velho)
    assert n >= 1, "nao achei %r no instituicoes.yaml -- PARE" % velho
    si = si.replace(velho, novo)
    trocas += n

d2 = yaml.safe_load(si)
assert d2["instituicoes"]["xp"]["custos"]["corretagem_rv"] == {"de": "corretagem.xp_swing"}
io.open(pc, "w", encoding="utf-8").write(sc)
io.open(pi, "w", encoding="utf-8").write(si)
print("E-08 aplicado: corretoras.py + %d referencia(s) no instituicoes.yaml" % trocas)

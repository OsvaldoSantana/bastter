# -*- coding: utf-8 -*-
"""Aplica o E-02 no tese.py. Idempotente: recusa se ja aplicado."""
import io, os, sys

p = sys.argv[1] if len(sys.argv) > 1 else "tese.py"
s = io.open(p, encoding="utf-8").read()
if "RegistroAusente" in s:
    sys.exit("ja aplicado: RegistroAusente existe em %s" % p)

VELHO = '''# ══ CARGA ════════════════════════════════════════════════════════════════════
def carregar_registros(path=None, hoje=None, compromisso_maximo_anos=None):
    """Devolve (teses, carregos) na forma que G7 e G8 consomem."""
    p = path or os.path.join(AQUI, "teses.yaml")
    if not os.path.exists(p): return {}, {}
    with open(p, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
'''

NOVO = '''# ══ CARGA ════════════════════════════════════════════════════════════════════
class RegistroAusente(Exception):
    """O arquivo de pre-registro nao esta onde deveria.

    ACHADO E-02, 12/09/2026. Ate aqui `carregar_registros` fazia
    `if not os.path.exists(p): return {}, {}` -- e essa linha respondia a pergunta
    errada. G7 e G8 falham para o lado seguro (sem tese, a rota e barrada), entao o
    sistema nunca ficou PERIGOSO. Ficou MENTIROSO:

        o que voce lia   "nenhuma tese registrada para esta rota"
        o que era        "o teses.yaml nao foi encontrado"

    As duas frases pedem acoes opostas. A primeira diz: registre a tese. A segunda diz:
    ache o arquivo, porque TODAS as suas teses sumiram. Rodando da pasta errada com
    vinte teses registradas, voce lia a primeira vinte vezes.

    E o agravante e de doutrina, nao de ergonomia. O `teses.yaml` E o pre-registro. A
    P4 existe exatamente para que nao se possa confundir "eu nunca me comprometi com
    uma tese" com "o registro sumiu" -- e era essa confusao que a linha produzia.

    O irmao que ja acertava e o `ambiente.declarado`, e a docstring dele e a regra:
    "NAO tem valores de reserva: se o arquivo sumir, e erro, porque sem ele nao ha nada
    a conferir". Dos oito carregadores do projeto, os dois que acertavam eram os dois
    que escreveram a CONSEQUENCIA na mensagem. Nao e coincidencia: quem escreve a
    consequencia descobre que precisa levantar."""


class RegistroIlegivel(Exception):
    """O arquivo existe e nao e YAML valido. TERCEIRO estado, e ele merece nome
    proprio: ausente, vazio e corrompido pedem acoes diferentes, e devolver `{}` para
    os tres era dizer a mesma coisa sobre tres situacoes."""


def carregar_registros(path=None, hoje=None, compromisso_maximo_anos=None,
                       permitir_ausente=False):
    """Devolve (teses, carregos) na forma que G7 e G8 consomem.

    TRES ESTADOS, e a distincao e a decisao dele em 12/09/2026 -- "arquivo ausente e
    arquivo vazio sao coisas diferentes":

      AUSENTE      levanta `RegistroAusente`. O arquivo faz parte do projeto; sumir e
                   acidente, nao escolha.
      VAZIO        devolve ({}, {}), e isso e LEGITIMO. Quem ainda nao registrou nada
                   tem um arquivo presente e vazio -- e e o estado normal do primeiro
                   dia. Conta como vazio: arquivo em branco, `{}`, so `meta:`, ou
                   `teses:`/`carregos:` nulos.
      ILEGIVEL     levanta `RegistroIlegivel`. YAML quebrado nao e "nenhuma tese".

    `permitir_ausente=True` devolve ({}, {}) tambem para o ausente. NAO e um atalho
    para silenciar o erro: e a U-01 escrita como parametro. A U-01 e dele -- "imagina
    que fosse uma ferramenta para ser vendida: eu nao teria informacoes sobre o aporte
    e a reserva do cliente" -- e diz que dado de usuario nao pode bloquear o sistema.
    Quem simula um usuario novo PEDE a ausencia explicitamente, em vez de recebe-la
    por padrao e nunca saber a diferenca.

    Note que o `alocar()` ja aceita `teses={}` injetado: o caminho do usuario novo nao
    passa por aqui, e por isso levantar no ausente nao quebra a U-01."""
    p = path or os.path.join(AQUI, "teses.yaml")
    if not os.path.exists(p):
        if permitir_ausente:
            return {}, {}
        raise RegistroAusente(
            "%s nao encontrado. Este arquivo E o pre-registro: sem ele o sistema nao "
            "sabe distinguir 'voce nunca registrou uma tese' de 'o registro sumiu', e "
            "as duas frases pedem acoes opostas. Confira a pasta de onde voce rodou. "
            "Se a intencao e MESMO nao ter registro nenhum (usuario novo), passe "
            "`permitir_ausente=True` e diga isso em voz alta. "
            "BLOQUEIA: G7_tese_registrada, G8_compromisso_de_carrego" % p)
    with open(p, encoding="utf-8") as f:
        bruto = f.read()
    try:
        doc = yaml.safe_load(bruto) or {}
    except yaml.YAMLError as e:
        raise RegistroIlegivel(
            "%s existe mas nao e YAML valido (%s). Arquivo corrompido nao e 'nenhuma "
            "tese': o registro pode estar inteiro e ilegivel por um caractere. "
            "BLOQUEIA: G7_tese_registrada, G8_compromisso_de_carrego"
            % (p, str(e).splitlines()[0][:90])) from e
    if not isinstance(doc, dict):
        raise RegistroIlegivel(
            "%s nao desembrulha para objeto (veio %s). "
            "BLOQUEIA: G7_tese_registrada, G8_compromisso_de_carrego"
            % (p, type(doc).__name__))
'''

assert VELHO in s, "regiao de carga nao encontrada -- o tese.py mudou, PARE"
s = s.replace(VELHO, NOVO, 1)

VELHO2 = '''def carregar_teses(path=None, hoje=None, compromisso_maximo_anos=None):
    return carregar_registros(path, hoje, compromisso_maximo_anos)[0]'''
NOVO2 = '''def carregar_teses(path=None, hoje=None, compromisso_maximo_anos=None,
                  permitir_ausente=False):
    return carregar_registros(path, hoje, compromisso_maximo_anos,
                              permitir_ausente)[0]'''
assert VELHO2 in s
s = s.replace(VELHO2, NOVO2, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("E-02 aplicado em %s" % os.path.abspath(p))

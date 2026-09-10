# -*- coding: utf-8 -*-
"""
Leitura e validacao do estado.yaml — o insumo que o usuario preenche.

Por que existe um validador aqui, e nao um `yaml.safe_load` direto:
  o arquivo e preenchido a mao, e as tres falhas mais provaveis sao SILENCIOSAS.
  Numero com virgula decimal vira STRING em YAML e o motor faria aritmetica com
  texto; um campo deixado no default do modelo passa por valor declarado; e uma
  data no formato brasileiro vira string tambem. Nenhuma das tres levanta erro
  sozinha — todas produzem um resultado plausivel e errado, que e a pior classe
  de defeito deste projeto inteiro.

Mesmo desenho do validador de tese: devolve TODOS os problemas de uma vez, separa
o que bloqueia do que e aviso, e nao inventa valor nenhum.
"""
from __future__ import annotations
import os, re, datetime as dt
import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
NUMERICOS = ("despesa_mensal", "reserva_atual", "aporte_mensal", "caixa", "horizonte_anos")

class EstadoInvalido(Exception):
    pass

def _num(v, campo, problemas):
    """Converte para float recusando as armadilhas de preenchimento manual."""
    if v is None:
        problemas.append(f"{campo}: nao preenchido"); return None
    if isinstance(v, (int, float)): return float(v)
    if isinstance(v, str):
        s = v.strip()
        if re.fullmatch(r"-?\d{1,3}(\.\d{3})*,\d+", s) or re.fullmatch(r"-?\d+,\d+", s):
            convertido = float(s.replace(".", "").replace(",", "."))
            problemas.append(
                f"{campo}: '{v}' foi lido como TEXTO, nao numero — YAML usa PONTO como "
                f"separador decimal. Escreva {convertido:.2f}. Interpretei como "
                f"{convertido:.2f} para seguir, mas corrija o arquivo")
            return convertido
        try: return float(s)
        except ValueError:
            problemas.append(f"{campo}: '{v}' nao e numero"); return None
    problemas.append(f"{campo}: tipo inesperado {type(v).__name__}"); return None

def validar(doc, P=None, hoje=None):
    """(dados, problemas, avisos). `problemas` impedem o uso como estado REAL."""
    hoje = hoje or dt.date.today()
    problemas, avisos, d = [], [], {}

    for c in NUMERICOS:
        d[c] = _num(doc.get(c), c, problemas)
    d["dependentes"] = doc.get("dependentes") or 0
    d["estabilidade_renda"] = doc.get("estabilidade_renda")
    d["posicoes"] = doc.get("posicoes") or {}
    # P-24. Onde a reserva esta, rota por rota. AUSENTE e diferente de VAZIO:
    #   ausente = o motor nao sabe, e o G2 diz isso em voz alta;
    #   {}      = nao ha reserva em lugar nenhum, que e afirmacao, nao ignorancia.
    # Manter os dois distintos e o que impede o motor de supor uma composicao que
    # ninguem informou.
    d["reserva_por_rota"] = doc.get("reserva_por_rota")
    if d["reserva_por_rota"] is not None:
        if not isinstance(d["reserva_por_rota"], dict):
            problemas.append("reserva_por_rota tem de ser um mapa rota -> valor")
            d["reserva_por_rota"] = None
        else:
            d["reserva_por_rota"] = {k: _num(v, f"reserva_por_rota.{k}", problemas)
                                     for k, v in d["reserva_por_rota"].items()}
            soma = sum(v for v in d["reserva_por_rota"].values() if v is not None)
            nom0 = d.get("reserva_atual")
            if nom0 is not None and abs(soma - nom0) > 0.01:
                problemas.append(
                    f"reserva_por_rota soma {soma:.2f} e reserva_atual diz {nom0:.2f}. "
                    f"Sao duas medidas do mesmo saldo e elas discordam — o sistema nao "
                    f"escolhe entre as duas por voce")
    d["dividas"] = doc.get("dividas") or []
    d["objetivos"] = doc.get("objetivos") or []

    meta = doc.get("meta") or {}
    if meta.get("status") != "REAL":
        problemas.append(
            f"meta.status = {meta.get('status')!r}: enquanto nao for REAL, o sistema trata "
            f"os numeros como cenario. Nenhuma decisao deve sair de um estado MODELO")
    pe = meta.get("preenchido_em")
    if isinstance(pe, str):
        avisos.append(f"meta.preenchido_em = '{pe}' e texto. YAML entende data como "
                      f"AAAA-MM-DD; escreva {hoje.isoformat()}")
        m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", pe.strip())
        if m and int(m.group(3)) > hoje.year:
            problemas.append(f"meta.preenchido_em aponta para {m.group(3)}, no futuro — "
                             f"provavel erro de digitacao no ano")
    elif pe is None:
        avisos.append("meta.preenchido_em vazio")

    # ── J-01: reserva empenhada nao e reserva ────────────────────────────────
    # Achado de 05/09/2026. O app do PicPay declara "Usado como limite: R$7.671,01 /
    # Disponivel para resgate: R$0,00" — o saldo inteiro garante o limite do cartao.
    # A funcao LIQUIDEZ exige resgate em ate 1 dia. Reserva empenhada cobre o cenario
    # em que nada acontece, que e o unico em que reserva nao serve para nada.
    d["reserva_disponivel"] = _num(doc.get("reserva_disponivel"), "reserva_disponivel",
                                   problemas) if doc.get("reserva_disponivel") is not None \
                              else d.get("reserva_atual")
    d["reserva_empenhada"] = _num(doc.get("reserva_empenhada"), "reserva_empenhada",
                                  problemas) if doc.get("reserva_empenhada") is not None else 0.0
    nom, disp = d.get("reserva_atual"), d.get("reserva_disponivel")
    if nom is not None and disp is not None and disp < nom - 1e-9:
        desp = d.get("despesa_mensal") or 0
        meses = (disp / desp) if desp else 0.0
        problemas.append(
            f"RESERVA EMPENHADA: nominal {nom:.2f}, disponivel para resgate {disp:.2f}. "
            f"A funcao LIQUIDEZ exige resgate em ate 1 dia — o que esta empenhado nao "
            f"cobre emergencia nenhuma. Meses de despesa cobertos DE VERDADE: {meses:.1f}, "
            f"nao {(nom/desp if desp else 0):.1f}. Fonte: "
            f"{doc.get('reserva_empenhada_fonte', '(nao declarada)')}")

    if d["estabilidade_renda"] not in ("alta", "media", "baixa"):
        problemas.append(f"estabilidade_renda = {d['estabilidade_renda']!r}: "
                         f"use alta, media ou baixa")

    if d["aporte_mensal"] is not None and d["aporte_mensal"] <= 0:
        problemas.append(
            "aporte_mensal = 0. Este e o unico campo do arquivo que, sozinho, deixa o "
            "sistema inteiro inerte: sem aporte nao ha reserva a formar, nao ha alocacao "
            "a executar e nenhum portao tem o que decidir. Se o valor for real, a questao "
            "do projeto deixa de ser 'onde aportar' e passa a ser 'de onde sai o aporte'. "
            "Se foi deixado em branco, e o campo mais importante a preencher")

    if d["despesa_mensal"] and d["reserva_atual"] is not None:
        meses = d["reserva_atual"]/d["despesa_mensal"]
        d["meses_cobertos"] = meses
        if meses < 1: avisos.append(f"reserva cobre {meses:.1f} mes de despesa")


    return d, problemas, avisos

def coerencia_da_estabilidade(respostas):
    """Traduz as tres perguntas objetivas em uma classificacao.

    Existe para que `estabilidade_renda` nao seja opiniao: as tres perguntas tem
    resposta verificavel, e a classificacao sai delas. O campo mais consequente do
    arquivo nao pode depender de como a pessoa se sente em relacao a risco."""
    n_clientes   = respostas["n_clientes"]
    meses_garantidos = respostas["meses_de_receita_garantida"]
    tem_aviso    = respostas["tem_aviso_previo"]
    pontos = 0
    razoes = []
    if n_clientes <= 1:
        pontos += 2; razoes.append("cliente unico: a perda do contrato zera a receita")
    elif n_clientes <= 3:
        pontos += 1; razoes.append(f"{n_clientes} clientes: concentracao alta")
    if not tem_aviso:
        pontos += 2; razoes.append("sem aviso previo: a receita pode parar de um mes para o outro")
    if meses_garantidos < 3:
        pontos += 1; razoes.append(f"{meses_garantidos} meses de receita contratada a frente")
    if respostas.get("parte_variavel_pode_ser_zero"):
        pontos += 1; razoes.append("parte da remuneracao e variavel e pode nao vir")
    nivel = "baixa" if pontos >= 3 else ("media" if pontos >= 1 else "alta")
    return dict(nivel=nivel, pontos=pontos, razoes=razoes)

def carregar(path=None, P=None, exigir_real=True):
    p = path or os.path.join(AQUI, "estado.yaml")
    with open(p, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    d, problemas, avisos = validar(doc, P)
    if problemas and exigir_real:
        raise EstadoInvalido("\n  - " + "\n  - ".join(problemas))
    return d, problemas, avisos

if __name__ == "__main__":
    with open(os.path.join(AQUI, "estado.yaml"), encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    d, problemas, avisos = validar(doc)
    print("="*84); print("VALIDACAO DO estado.yaml"); print("="*84)
    print(f"\n{len(problemas)} problema(s) que impedem tratar como estado REAL:")
    for x in problemas: print(f"  [BLOQUEIA] {x}\n")
    for x in avisos: print(f"  [aviso] {x}")
    print("\nLido:")
    for k in NUMERICOS + ("estabilidade_renda", "dependentes"):
        print(f"  {k:<20} {d.get(k)}")
    print("\n" + "="*84)
    print("COERENCIA DA ESTABILIDADE — a partir das SUAS respostas de 04/09/2026")
    print("="*84)
    c = coerencia_da_estabilidade(dict(
        n_clientes=1, meses_de_receita_garantida=0, tem_aviso_previo=False,
        parte_variavel_pode_ser_zero=True))
    print(f"  declarado no arquivo: {d.get('estabilidade_renda')}")
    print(f"  implicado pelas respostas: {c['nivel'].upper()}  ({c['pontos']} pontos de 6)")
    for r in c["razoes"]: print(f"     - {r}")

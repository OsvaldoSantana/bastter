# -*- coding: utf-8 -*-
"""O pre-registro deixando de ser documento sobre intencoes e virando mecanismo.

O E-06 mediu o buraco: `variantes_permitidas: 1` e o limite anti-p-hacking que o
projeto se impos, e tinha ZERO leituras. Nada contava, nada comparava, nada falhava
na decima variante. Este modulo e o consumidor que faltava, e ele executa as tres
decisoes de 13/09 que sobravam.

DECISAO 2 — o corte sai do dado, nao da tabela. Ver `multiplicidade.py`.

DECISAO 3 — o `m` dos DOIS LADOS, e nenhum dos dois e afirmado:
    m_executado  vem do DIARIO   — conta as especificacoes que foram ao dado
    m_orcado     vem da SOMA dos `variantes_permitidas` — o que ele se autorizou
  Os dois sao CALCULADOS. Era esse o ponto dele: quem registra nao escolhe o numero
  que o julga. E `pesquisa_id` idem — derivado do sha256 da fonte e da regra de
  amostra, nunca escrito, para que renomear o conjunto nao reinicie o contador.

DECISAO 4 — divergencia BLOQUEIA. A regra dele foi escrita para R1 contra uma
  extensao Rn, e aqui ela ganhou um primeiro caso que nao estava previsto: os dois
  lados do `m` da decisao 3 podem dar vereditos opostos sobre a MESMA execucao.
  Dao, no HML. O portao e sobre VEREDITOS DIVERGENTES, venham de onde vierem —
  generalizar custou menos que abrir uma excecao, e excecao e a superficie por onde
  o contorno entra.

O QUE ESTE MODULO NAO PROTEGE, declarado de proposito (P5): nada aqui teria pego o
Risk_Free invertido do E-06. Especificacao congelada, diario, contador e portao
passariam por aquilo sem piscar, porque `tratamento_rf` so entra na lista de graus de
liberdade se alguem souber que ele existe. O que pegou aquilo foi um comentario em
portugues e dois testes.
"""
from __future__ import annotations
import hashlib
import multiplicidade as X

# EXTENSAO re-roda uma especificacao que ja esta contada: mais observacao da mesma
# pergunta nao e uma pergunta nova. Foi a razao dele para nao cobrar variante por
# atualizar o estudo — cobrar ensina "nao atualize, isso gasta a sua unica bala".
TIPOS_QUE_CONTAM_NO_M = ("ORIGINAL", "VARIANTE")
TIPOS = TIPOS_QUE_CONTAM_NO_M + ("EXTENSAO", "CORRECAO_FACTUAL", "CORTE_ESPECIFICADO")
CAMPOS_DO_REGISTRO = ("id", "estrategia", "tipo", "data", "amostra_realizada", "t",
                      "veredito", "ambiente")
LEITURA_MINIMA = 120     # caracteres. Uma divergencia escrita em oito palavras nao foi escrita


class DiarioInvalido(Exception):
    """O diario e o instrumento principal; um registro malformado o cala."""

class FonteTrocada(Exception):
    """A serie mudou. O conjunto de pesquisa e outro, e o `m` anterior nao o julga."""

class DivergenciaNaoEscrita(Exception):
    """Decisao 4. A estrategia nao decide nada enquanto a divergencia nao estiver escrita."""


def bloco(P):
    return P["pesquisa"]


def pesquisa_id(P, hash_medido=None):
    """Derivado de (sha256 da fonte, regra de amostra). NUNCA escrito a mao.

    O buraco que ele apontou: alguem cria "Conjunto A, B, C" e o contador reinicia.
    Ancorado no dado, renomear nao reinicia nada, porque o nome nao e a chave — um
    conjunto novo exige dado novo ou regra de amostra nova, e as duas coisas sao
    visiveis e datadas."""
    b = bloco(P)
    f, a = b["fonte"], b["amostra_regra"]
    declarado = f["sha256_12"]
    if hash_medido is not None and hash_medido != declarado:
        raise FonteTrocada(
            f"{f['arquivo']}: registrado {declarado}, medido {hash_medido}. "
            f"Isto nao e um erro a corrigir no YAML — e outro conjunto de pesquisa. "
            f"Registre a extensao e recalcule o `m` antes de reusar qualquer veredito.")
    semente = "|".join([declarado, str(a["inicio"]), str(a["fim"]),
                        ";".join(a["filtros"]), ";".join(a["fatores"])])
    return hashlib.sha256(semente.encode("utf-8")).hexdigest()[:16]


def diario(P):
    """Os registros, validados. Registro sem campo obrigatorio levanta em vez de sumir."""
    b = bloco(P)
    conhecidas = set(P["estrategias_pre_registradas"])
    vistos: set = set()
    for r in b["diario"]:
        faltando = [c for c in CAMPOS_DO_REGISTRO if c not in r]
        if faltando:
            raise DiarioInvalido(f"registro {r.get('id', '(sem id)')!r} sem {faltando}")
        if r["tipo"] not in TIPOS:
            raise DiarioInvalido(f"{r['id']}: tipo {r['tipo']!r} fora de {list(TIPOS)}")
        if r["estrategia"] not in conhecidas:
            raise DiarioInvalido(
                f"{r['id']}: estrategia {r['estrategia']!r} nao esta pre-registrada. "
                f"O diario REFERENCIA a especificacao, nunca a redeclara — duas "
                f"declaracoes da mesma coisa concordam por acidente (N-01).")
        if r["id"] in vistos:
            raise DiarioInvalido(f"id repetido no diario: {r['id']!r}")
        vistos.add(r["id"])
    return list(b["diario"])


def m_executado(P):
    """Do diario. CALCULADO — era essa a exigencia dele."""
    return sum(1 for r in diario(P) if r["tipo"] in TIPOS_QUE_CONTAM_NO_M)


def m_orcado(P):
    """Soma dos `variantes_permitidas`. Tambem calculado: o 13 do registro nunca foi
    um numero que alguem escolheu — e a consequencia de nove escolhas anteriores."""
    E = P["estrategias_pre_registradas"]
    return sum(v["variantes_permitidas"] for v in E.values()
               if isinstance(v, dict) and "variantes_permitidas" in v)


def cortes_tabelados(P, gl):
    """Bonferroni sobre a t de Student. REFERENCIA, nao a regra declarada.

    Fica aqui porque e o numero que o projeto vinha citando em prosa desde 12/09, e
    porque a distancia entre ele e o medido E o achado. Chamar isto de corte seria
    voltar a supor que o t se distribui como a tabela diz."""
    fam = bloco(P)["familia"]
    a, bi = fam["alfa_familiar"], fam["bilateral"]
    return {"m_executado": m_executado(P), "m_orcado": m_orcado(P),
            "executado": X.corte_bonferroni(m_executado(P), gl, a, bi),
            "orcado": X.corte_bonferroni(m_orcado(P), gl, a, bi)}


def cortes_medidos(P, t_boot, alvo):
    """Os dois cortes declarados, cada um com o instrumento que o insumo permite.

    executado: Romano-Wolf sobre a familia inteira — marginal medida E dependencia
               medida. So existe porque as hipoteses executadas produziram
               estatistica; nao ha o que reamostrar num teste que nunca rodou.
    orcado:    Bonferroni sobre a marginal medida DESTA hipotese. A uniao de Boole
               dispensa as outras 12, que e exatamente o motivo de ser o unico
               instrumento aplicavel aqui.

    Recusa em vez de devolver numero quando o insumo falta: e a P1, e e o F-02 que o
    projeto ja pagou uma vez — insumo ausente virando zero, e zero ganhando."""
    fam = bloco(P)["familia"]
    if fam["correcao_executado"] != "ROMANO_WOLF":
        raise NotImplementedError(
            f"correcao_executado={fam['correcao_executado']!r}: so ROMANO_WOLF esta "
            f"implementado. Interruptor declarado que nao liga em nada e o achado E-03.")
    if fam["correcao_orcado"] != "BONFERRONI_MEDIDO":
        raise NotImplementedError(
            f"correcao_orcado={fam['correcao_orcado']!r}: so BONFERRONI_MEDIDO esta "
            f"implementado.")
    if alvo not in t_boot:
        raise ValueError(f"sem bootstrap para {alvo!r}: o corte declarado e MEDIDO, e "
                         f"nao ha medicao. Nao existe queda para a tabela.")
    a = fam["alfa_familiar"]
    return {"m_executado": m_executado(P), "m_orcado": m_orcado(P),
            "repeticoes": fam["repeticoes_bootstrap"], "semente": fam["semente"],
            "executado": X.corte_romano_wolf(t_boot, a),
            "orcado": X.corte_bonferroni_medido(t_boot[alvo], m_orcado(P), a)}


def veredito_dos_dois_lados(t, cortes):
    """Decisao 3 posta em pratica: dois numeros onde as pessoas querem um.

    E a razao de serem dois esta na resposta: o lado executado descreve a EVIDENCIA,
    o orcado descreve a DISCIPLINA. Colapsar num so apagaria uma das duas."""
    e = X.veredito(t, cortes["executado"])
    o = X.veredito(t, cortes["orcado"])
    return {"executado": e, "orcado": o, "divergem": e != o}


def conferir_registro(P, registro, cortes, vered, tolerancia=1e-3):
    """O que o diario AFIRMA contra o que a medicao devolve, agora. Devolve as
    divergencias; lista vazia e reproducao.

    Esta funcao nasceu por cobranca do `auditoria/chaves_orfas.py`, e a cobranca
    estava certa. Os quatro campos abaixo existiam no YAML e so o TESTE os lia — que
    e a categoria "LIDA SO POR TESTE" da P-77, e ela e pior que orfa pura: o teste
    prova o esquema e ninguem prova o comportamento. Conferir o registro e trabalho
    do modulo; o teste so chama."""
    fora = []
    pares = ((("corte_executado", registro.get("corte_executado")), cortes["executado"]),
             (("corte_orcado", registro.get("corte_orcado")), cortes["orcado"]),
             (("veredito_executado", registro.get("veredito_executado")), vered["executado"]),
             (("veredito_orcado", registro.get("veredito_orcado")), vered["orcado"]))
    for (campo, reg), medido in pares:
        if reg is None: continue
        igual = (abs(reg - medido) < tolerancia if isinstance(reg, (int, float))
                 else reg == medido)
        if not igual:
            fora.append(f"{registro['id']}.{campo}: registrado {reg}, medido {medido}")
    return fora


def operativo(P, estrategia, vered):
    """Decisao 4. Divergencia de veredito BLOQUEIA ate estar escrita.

    "Preservar tudo" sem esta regra vira "escolha o que preferir" — p-hacking com
    auditoria completa. E o bloqueio e o ponto, nao o efeito colateral: um veredito
    que se inverte conforme a familia e o evento mais informativo que este aparato
    pode produzir, e merece uma parada."""
    dv = bloco(P)["divergencia"]
    if dv["politica"] != "BLOQUEIA":
        raise NotImplementedError(
            f"divergencia.politica={dv['politica']!r}: so BLOQUEIA esta implementado. "
            f"Declarar outra e prometer um comportamento que o codigo nao tem.")
    if not vered["divergem"]:
        return vered["executado"]
    escrita = divergencia_escrita(P, estrategia)
    if escrita is None:
        raise DivergenciaNaoEscrita(
            f"{estrategia}: executado={vered['executado']} x orcado={vered['orcado']}. "
            f"A estrategia nao decide nada ate a divergencia estar escrita em "
            f"pesquisa.divergencias_escritas — o que mudou, em que familia, e a leitura "
            f"de quem escreveu.")
    lado = dv["operativo_quando_divergem"].lower()
    return vered[lado]


CAMPOS_DA_DIVERGENCIA = ("estrategia", "entre", "escrita_em", "leitura")


def divergencia_escrita(P, estrategia):
    """A entrada que destrava, se existir. Uma linha de log nao destrava: o campo
    `leitura` precisa ter tamanho de leitura, e `entre` tem de dizer o que divergiu."""
    for d in bloco(P)["divergencias_escritas"]:
        faltando = [c for c in CAMPOS_DA_DIVERGENCIA if c not in d]
        if faltando:
            raise DivergenciaNaoEscrita(f"divergencia sem {faltando}: {d!r}")
        if d["estrategia"] != estrategia: continue
        if len(d["entre"]) != 2:
            raise DivergenciaNaoEscrita(
                f"{estrategia}: `entre` tem de nomear os DOIS vereditos que divergiram "
                f"(recebido {d['entre']!r}), e `escrita_em` e {d['escrita_em']}.")
        if len(str(d["leitura"])) < LEITURA_MINIMA:
            raise DivergenciaNaoEscrita(
                f"{estrategia}: a divergencia tem registro mas nao tem leitura "
                f"({len(str(d['leitura']))} caracteres). Registrar que divergiu nao e "
                f"escrever o que a divergencia quer dizer.")
        return d
    return None

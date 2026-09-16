# -*- coding: utf-8 -*-
"""
jcp.py -- a aliquota de IR na fonte sobre juros sobre capital proprio, por DATA.

A aliquota do JCP **nao e constante no tempo**, e o acervo de proventos deste projeto
comeca em 2010. Aplicar um unico numero a serie inteira erra em todos os registros de
um dos lados -- e o erro e invisivel, porque qualquer um dos numeros e plausivel.

FONTE PRIMARIA, lida norma por norma no Planalto em 13/09/2026. Ver
`docs/fontes/lei-9249-1995-jcp-planalto.md` para as transcricoes.

ESTE MODULO NAO TEM CHAMADOR NO MOTOR HOJE, e isso esta declarado de proposito: a
serie de retorno total LIQUIDA de JCP ainda nao existe (roda a bruta). A P-77 acabou
de ensinar que campo sem leitor e promessa sem dono -- entao aqui a promessa esta
escrita: **este modulo existe para ser chamado pela serie liquida quando ela for
construida, e a prova de que ele esta certo e o `test_jcp.py`, nao um consumidor.**
Se a serie liquida nascer sem chamar esta funcao, e defeito.
"""

import datetime as dt

CAMINHO = ("tributacao", "ir_jcp_fonte")


class ForaDeVigencia(Exception):
    """Data anterior a primeira vigencia conhecida. NAO devolvemos a mais antiga por
    aproximacao: antes de 01/01/1996 o regime de JCP nem existia (a Lei 9.249 o criou),
    e devolver 15% para 1994 seria inventar imposto sobre um instituto inexistente."""


def _data(x):
    if isinstance(x, dt.datetime): return x.date()
    if isinstance(x, dt.date): return x
    return dt.date.fromisoformat(str(x))


def aliquota_jcp(data, C):
    """Aliquota na fonte vigente em `data`. Devolve (aliquota, vigencia).

    `data` e a do PAGAMENTO ou CREDITO -- e o proprio par. 2o que diz isso: "na data
    do pagamento ou do credito ao beneficiario". Nao e a data ex, nao e a da
    aprovacao. Usar a data errada joga o provento na faixa errada exatamente na
    fronteira, que e onde a diferenca existe.
    """
    d = _data(data)
    no = C
    for k in CAMINHO:
        no = no[k]
    for v in no["valor"]:
        de = _data(v["de"])
        ate = _data(v["ate"]) if v.get("ate") else None
        if d >= de and (ate is None or d <= ate):
            return v["aliquota"], v
    raise ForaDeVigencia(
        "%s e anterior a 01/01/1996: o JCP foi criado pela Lei 9.249/1995 e nao havia "
        "aliquota a aplicar. Ver docs/fontes/lei-9249-1995-jcp-planalto.md" % d)


def jcp_liquido(valor_bruto, data, C):
    """Valor liquido recebido por PESSOA FISICA.

    Par. 3o, II: para PF a tributacao na fonte e DEFINITIVA -- nao ha ajuste na
    declaracao. O liquido E o liquido, e por isso ele entra assim numa serie de
    retorno total. Diferente de imposto por antecipacao, que voltaria depois."""
    a, _ = aliquota_jcp(data, C)
    return valor_bruto * (1 - a)

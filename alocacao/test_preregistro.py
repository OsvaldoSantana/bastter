# -*- coding: utf-8 -*-
"""Testes do pre-registro como mecanismo. As tres decisoes de 13/09, medidas.

A regra da casa aqui: cada teste tem de falhar numa versao anterior plausivel do
arquivo. Testar que `m_orcado() == 13` contra um 13 escrito no YAML nao prova nada —
prova-se mexendo num `variantes_permitidas` e vendo o numero acompanhar.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copy
import pytest
import alocacao as A
import preregistro as R

P = A.carregar_politica()


def _copia():
    return copy.deepcopy(P)


_BOOT: dict = {}

def _bootstrap():
    """Uma reamostragem por suite, e nao uma por teste: sao ~1,8 s cada, com a mesma
    semente e o mesmo resultado. Cache aqui e barato; cache dentro do modulo de
    producao esconderia nao-determinismo."""
    if not _BOOT:
        import backtest_h1_h3 as B
        _BOOT["d"] = B.amostra()
        _BOOT["boot"] = B.bootstrap_conjunto(list(B.ALVOS), _BOOT["d"])
    return _BOOT["d"], _BOOT["boot"]


# ── DECISAO 3: os dois `m`, os dois CALCULADOS ───────────────────────────────
def test_m_orcado_e_a_soma_e_nao_um_numero_escrito():
    """13 nunca foi uma escolha: e a consequencia de nove escolhas anteriores."""
    assert R.m_orcado(P) == 13
    q = _copia()
    q["estrategias_pre_registradas"]["greenblatt_v1"]["variantes_permitidas"] = 5
    assert R.m_orcado(q) == 15, "o `m` orcado nao acompanhou o orcamento — esta escrito"


def test_m_executado_vem_do_DIARIO():
    """A exigencia dele: `m` calculavel a partir do diario, nunca afirmado por quem
    registra. Um registro novo do tipo certo move o numero; um do tipo errado nao."""
    assert R.m_executado(P) == 2
    q = _copia()
    q["pesquisa"]["diario"].append(dict(q["pesquisa"]["diario"][0],
                                        id="RX", tipo="ORIGINAL"))
    assert R.m_executado(q) == 3


def test_EXTENSAO_nao_acrescenta_hipotese_a_familia():
    """A razao dele para nao cobrar variante por atualizar o estudo, aplicada tambem
    ao `m`: mais observacao da MESMA pergunta nao e uma pergunta nova. Se extensao
    contasse, o sistema ensinaria a nao atualizar."""
    q = _copia()
    for t in ("EXTENSAO", "CORRECAO_FACTUAL", "CORTE_ESPECIFICADO"):
        q["pesquisa"]["diario"].append(dict(q["pesquisa"]["diario"][0],
                                            id=f"RX{t}", tipo=t))
    assert R.m_executado(q) == 2


def test_o_que_o_pre_registro_promete_e_nao_executou_e_CONTADO():
    """O papel que a reclassificacao de `estrategias_pre_registradas` deixou vago.

    Ate 18/09 a secao era ESPECIFICACAO — "escrito e nao ligado" — e a guarda do P-28
    cobrava dela um numero de pendencia. Agora um modulo a le, e a cobranca passou a
    ser esta: quantos testes o pre-registro autorizou e nunca foram ao dado. Onze.
    Nao e prosa e nao apodrece: o dia em que uma estrategia rodar, o numero cai
    sozinho, porque os dois lados sao calculados."""
    nunca_rodaram = R.m_orcado(P) - R.m_executado(P)
    assert nunca_rodaram == 11, (
        f"{nunca_rodaram} testes pre-registrados nunca executados. Se este numero "
        f"mudou, ou uma estrategia rodou (atualize aqui e no CLAUDE.md) ou alguem "
        f"mexeu no orcamento sem registrar a execucao.")
    executadas = {r["estrategia"] for r in R.diario(P)
                  if r["tipo"] in R.TIPOS_QUE_CONTAM_NO_M}
    assert executadas == {"hml_puro_v1", "tamanho_smb_v1"}


def test_os_dois_cortes_sao_diferentes_e_o_orcado_e_o_mais_severo():
    c = R.cortes_tabelados(P, 301)
    assert c["m_executado"] == 2 and c["m_orcado"] == 13
    assert c["executado"] < c["orcado"]
    assert abs(c["executado"] - 2.2527) < 1e-3 and abs(c["orcado"] - 2.9131) < 1e-3


# ── DECISAO 3 (b): `pesquisa_id` derivado, nunca escrito ─────────────────────
def test_renomear_nao_reinicia_o_contador():
    """O buraco que ele apontou: criar "Conjunto A, B, C" e zerar o `m`. Ancorado no
    dado, o nome nao e a chave — e aqui esta a prova, nao a promessa."""
    base = R.pesquisa_id(P)
    q = _copia()
    q["estrategias_pre_registradas"]["hml_puro_v2_renomeado"] = \
        q["estrategias_pre_registradas"].pop("hml_puro_v1")
    assert R.pesquisa_id(q) == base


def test_dado_novo_ou_regra_de_amostra_nova_MUDAM_o_conjunto():
    base = R.pesquisa_id(P)
    for caminho, valor in (
        (("fonte", "sha256_12"), "000000000000"),
        (("amostra_regra", "inicio"), "2005-01"),
        (("amostra_regra", "filtros"), ["n_dias >= 5"]),
        (("amostra_regra", "fatores"), ["HML", "SMB"]),
    ):
        q = _copia()
        q["pesquisa"][caminho[0]][caminho[1]] = valor
        assert R.pesquisa_id(q) != base, caminho


def test_serie_trocada_nao_e_erro_de_digitacao_e_sim_outro_conjunto():
    with pytest.raises(R.FonteTrocada):
        R.pesquisa_id(P, hash_medido="deadbeefcafe")
    assert R.pesquisa_id(P, hash_medido=P["pesquisa"]["fonte"]["sha256_12"])


# ── O diario recusa registro malformado em vez de o ignorar ──────────────────
def test_o_diario_do_repositorio_e_valido():
    ids = [r["id"] for r in R.diario(P)]
    assert ids == ["R1", "R2", "R3", "R4"]


@pytest.mark.parametrize("estrago", [
    {"tipo": "EXPERIMENTO"},                      # tipo fora da lista
    {"estrategia": "estrategia_que_nao_existe"},   # referencia quebrada
    {"id": "R1"},                                  # id repetido
])
def test_registro_malformado_LEVANTA(estrago):
    q = _copia()
    q["pesquisa"]["diario"].append({**q["pesquisa"]["diario"][1], "id": "RZ", **estrago})
    with pytest.raises(R.DiarioInvalido):
        R.diario(q)


@pytest.mark.parametrize("campo", R.CAMPOS_DO_REGISTRO)
def test_registro_sem_campo_obrigatorio_LEVANTA(campo):
    q = _copia()
    q["pesquisa"]["diario"][0].pop(campo)
    with pytest.raises(R.DiarioInvalido):
        R.diario(q)


def test_o_diario_nao_REDECLARA_a_especificacao():
    """O diario referencia a estrategia pelo nome e para por ai. Duas declaracoes da
    mesma especificacao concordam por acidente ate o dia em que nao concordam (N-01) —
    e este teste mede que a unica ponte entre os dois e o nome."""
    for r in R.diario(P):
        assert set(r) - {"nota"} <= set(R.CAMPOS_DO_REGISTRO) | {
            "corte_executado", "corte_orcado", "veredito_executado", "veredito_orcado"}


def test_o_t_do_diario_e_o_t_do_resultado_registrado():
    """Onde a duplicata E inevitavel — o `t` esta no diario e no `resultado` da
    estrategia —, ela deixa de ser acidente e vira medicao. Mesma solucao do
    `bc_procedentes`: manter as duas pontas e recalcular uma contra a outra."""
    E = P["estrategias_pre_registradas"]
    esperado = {"hml_puro_v1": E["hml_puro_v1"]["resultado"]["t"],
                "tamanho_smb_v1": E["tamanho_smb_v1"]["resultado"]["t"]}
    for r in R.diario(P):
        assert abs(r["t"] - esperado[r["estrategia"]]) < 0.01, r["id"]


# ── DECISAO 2: o corte medido, e a recusa quando nao ha medicao ──────────────
def test_sem_bootstrap_o_corte_medido_RECUSA_em_vez_de_cair_para_a_tabela():
    """F-02 na letra: insumo ausente nao vira numero. Cair para o tabelado seria pior
    que falhar, porque o numero sairia com a etiqueta de MEDIDO."""
    with pytest.raises(ValueError):
        R.cortes_medidos(P, {"SMB": [0.0]}, "HML")


@pytest.mark.parametrize("chave,valor", [("correcao_executado", "HOLM"),
                                         ("correcao_orcado", "SIDAK")])
def test_correcao_declarada_e_nao_implementada_LEVANTA(chave, valor):
    """O oposto do E-03: aqui o interruptor declarado falha alto em vez de nao fazer
    nada. Declarar HOLM no YAML e continuar rodando Romano-Wolf seria o defeito
    recorrente do projeto — o arquivo diz uma coisa e o codigo faz outra."""
    q = _copia()
    q["pesquisa"]["familia"][chave] = valor
    with pytest.raises(NotImplementedError):
        R.cortes_medidos(q, {"HML": [0.0], "SMB": [0.0]}, "HML")


# ── DECISAO 4: divergencia bloqueia ──────────────────────────────────────────
DIVERGE = {"executado": "REJEITA", "orcado": "NAO_REJEITA", "divergem": True}
CONCORDA = {"executado": "NAO_REJEITA", "orcado": "NAO_REJEITA", "divergem": False}


def test_sem_divergencia_o_operativo_sai_direto():
    assert R.operativo(P, "tamanho_smb_v1", CONCORDA) == "NAO_REJEITA"


def test_divergencia_SEM_leitura_escrita_BLOQUEIA():
    q = _copia()
    q["pesquisa"]["divergencias_escritas"] = []
    with pytest.raises(R.DivergenciaNaoEscrita):
        R.operativo(q, "hml_puro_v1", DIVERGE)


def test_divergencia_COM_leitura_escrita_devolve_o_lado_declarado():
    """Escrever destrava, e o lado que vale e o ORCADO — o unico dos dois que nao
    pode ter sido escolhido depois de ver o resultado."""
    assert R.operativo(P, "hml_puro_v1", DIVERGE) == "NAO_REJEITA"
    q = _copia()
    q["pesquisa"]["divergencia"]["operativo_quando_divergem"] = "EXECUTADO"
    assert R.operativo(q, "hml_puro_v1", DIVERGE) == "REJEITA"


def test_uma_linha_de_log_NAO_conta_como_divergencia_escrita():
    """"Registrar que divergiu" e "escrever o que a divergencia quer dizer" sao coisas
    diferentes, e so a segunda destrava."""
    q = _copia()
    q["pesquisa"]["divergencias_escritas"][0]["leitura"] = "os dois lados divergem"
    with pytest.raises(R.DivergenciaNaoEscrita):
        R.operativo(q, "hml_puro_v1", DIVERGE)


def test_divergencia_escrita_para_OUTRA_estrategia_nao_destrava_esta():
    q = _copia()
    q["pesquisa"]["divergencias_escritas"][0]["estrategia"] = "tamanho_smb_v1"
    with pytest.raises(R.DivergenciaNaoEscrita):
        R.operativo(q, "hml_puro_v1", DIVERGE)


@pytest.mark.parametrize("campo", R.CAMPOS_DA_DIVERGENCIA)
def test_divergencia_sem_campo_obrigatorio_LEVANTA(campo):
    q = _copia()
    q["pesquisa"]["divergencias_escritas"][0].pop(campo)
    with pytest.raises(R.DivergenciaNaoEscrita):
        R.operativo(q, "hml_puro_v1", DIVERGE)


def test_politica_de_divergencia_diferente_de_BLOQUEIA_LEVANTA():
    q = _copia()
    q["pesquisa"]["divergencia"]["politica"] = "AVISA"
    with pytest.raises(NotImplementedError):
        R.operativo(q, "hml_puro_v1", CONCORDA)


# ── A execucao real: os numeros registrados em R3/R4 reproduzem ──────────────
@pytest.mark.acervo   # le o CSV do NEFIN (armazem desde 25/09)
def test_R3_e_R4_reproduzem_o_que_o_diario_registrou():
    """~2 s. O mesmo papel do `test_h1_h3_reproduzem_o_resultado_registrado`: se a
    serie, a semente ou a algebra mudarem, o diario passa a mentir e alguem precisa
    saber antes de reusar o veredito."""
    import backtest_h1_h3 as B
    d, boot = _bootstrap()
    por_estrategia = {B.DE_ALVO_PARA_ESTRATEGIA[a]: a for a in B.ALVOS}
    for r in R.diario(P):
        if r["tipo"] != "CORTE_ESPECIFICADO": continue
        alvo = por_estrategia[r["estrategia"]]
        cor = R.cortes_medidos(P, boot, alvo)
        v = R.veredito_dos_dois_lados(float(B.alfa_contra_os_demais(alvo, d)[1]), cor)
        assert R.conferir_registro(P, r, cor, v) == [], r["id"]
        assert R.operativo(P, r["estrategia"], v) == r["veredito"], r["id"]


@pytest.mark.acervo   # le o CSV do NEFIN (armazem desde 25/09)
def test_a_conferencia_do_registro_ACUSA_quando_o_numero_anda():
    """Prova por mutacao da guarda acima: um corte registrado fora do lugar tem de
    aparecer nomeado, e nao sumir num `all(...)` que devolve False sem dizer qual."""
    import backtest_h1_h3 as B
    d, boot = _bootstrap()
    cor = R.cortes_medidos(P, boot, "HML")
    v = R.veredito_dos_dois_lados(float(B.alfa_contra_os_demais("HML", d)[1]), cor)
    r3 = [r for r in R.diario(P) if r["id"] == "R3"][0]
    torto = {**r3, "corte_orcado": r3["corte_orcado"] + 0.5,
             "veredito_executado": "NAO_REJEITA"}
    fora = R.conferir_registro(P, torto, cor, v)
    assert len(fora) == 2 and any("corte_orcado" in f for f in fora) \
        and any("veredito_executado" in f for f in fora), fora


@pytest.mark.acervo   # le o CSV do NEFIN (armazem desde 25/09)
def test_o_HML_nao_sobrevive_ao_ORCAMENTO_que_ele_mesmo_pre_registrou():
    """A retratacao presa num teste. O projeto afirmava que o HML "sobrevive ao corte
    mais severo por 0,027 de um t" — e isso valia so sob a suposicao de que o t se
    distribui como a tabela de Student. Medido, nao se distribui.

    Se alguem "consertar" o corte de volta para o tabelado, este teste mostra o
    tamanho do estrago — mesma funcao do
    `test_subtrair_risk_free_de_um_fator_inverte_o_veredito`."""
    import backtest_h1_h3 as B, multiplicidade as X
    d, boot = _bootstrap()
    t = float(B.alfa_contra_os_demais("HML", d)[1])
    tabelado = X.corte_bonferroni(R.m_orcado(P), B.graus_de_liberdade(d))
    medido = X.corte_bonferroni_medido(boot["HML"], R.m_orcado(P))
    assert t > tabelado, "a afirmacao antiga: sobrevive por pouco"
    assert t < medido, "a afirmacao medida: nao sobrevive"
    assert medido - tabelado > 0.15, f"o custo da suposicao: {medido - tabelado:.4f}"


# ── P-138: o orcamento de variantes BLOQUEIA; a saida e emenda EMPURRADA ───────
JUSTIFICATIVA = ("A variante troca o filtro de liquidez de 15 para 18 dias porque a "
                 "serie do NEFIN passou a publicar a contagem por mes; declarada antes "
                 "de rodar, e o preco e o corte orcado da familia subir.")


def _estourado():
    """hml_puro_v1 tem `variantes_permitidas: 1` e ja gastou R1. Uma VARIANTE a mais
    estoura o orcamento em um."""
    q = _copia()
    q["pesquisa"]["diario"].append(dict(q["pesquisa"]["diario"][0], id="RV",
                                        tipo="VARIANTE", data="2026-09-25"))
    return q


def _emenda(**kw):
    e = dict(estrategia="hml_puro_v1", variantes_adicionais=1,
             escrita_em="2026-09-25", justificativa=JUSTIFICATIVA)
    e.update(kw)
    return e


def _vered_sem_divergencia():
    return {"executado": "NAO_REJEITA", "orcado": "NAO_REJEITA", "divergem": False}


def test_P138_orcamento_estourado_SEM_emenda_BLOQUEIA():
    """A decisao dele. Na versao anterior `operativo` devolvia o veredito: o contador
    nao existia nem como alarme."""
    q = _estourado()
    with pytest.raises(R.OrcamentoEstourado, match="unica saida"):
        R.operativo(q, "hml_puro_v1", _vered_sem_divergencia(), publicadas=[])


def test_P138_emenda_ESCRITA_e_nao_empurrada_continua_bloqueando():
    """Justificativa no disco e o alarme de 13/09 com outro nome. O que destrava e o
    historico publico."""
    q = _estourado()
    q["pesquisa"]["emendas"] = [_emenda()]
    with pytest.raises(R.OrcamentoEstourado, match="ainda nao empurradas"):
        R.operativo(q, "hml_puro_v1", _vered_sem_divergencia(), publicadas=[])


def test_P138_emenda_PUBLICADA_destrava_e_so_na_medida_dela():
    q = _estourado()
    q["pesquisa"]["emendas"] = [_emenda()]
    pub = R.emendas(q)
    assert R.operativo(q, "hml_puro_v1", _vered_sem_divergencia(),
                       publicadas=pub) == "NAO_REJEITA"
    assert R.conferir_orcamento(q, "hml_puro_v1", pub) == 0
    # uma segunda variante estoura de novo: a emenda cobre o que diz, nao um cheque em branco
    q["pesquisa"]["diario"].append(dict(q["pesquisa"]["diario"][0], id="RV2",
                                        tipo="VARIANTE", data="2026-09-26"))
    with pytest.raises(R.OrcamentoEstourado):
        R.conferir_orcamento(q, "hml_puro_v1", pub)


def test_P138_emenda_para_OUTRA_estrategia_nao_destrava_esta():
    q = _estourado()
    q["pesquisa"]["emendas"] = [_emenda(estrategia="tamanho_smb_v1")]
    with pytest.raises(R.OrcamentoEstourado):
        R.conferir_orcamento(q, "hml_puro_v1", R.emendas(q))


def test_P138_emenda_ENCARECE_a_familia_publicada_ou_nao():
    """Se emendar nao entrasse no `m`, estourar o orcamento sairia de graca."""
    q = _copia()
    q["pesquisa"]["emendas"] = [_emenda(variantes_adicionais=2)]
    assert R.m_orcado(q) == R.m_orcado(P) + 2


@pytest.mark.parametrize("estrago", [
    {"variantes_adicionais": 0}, {"variantes_adicionais": True},
    {"variantes_adicionais": "1"}, {"justificativa": "porque sim"},
    {"estrategia": "nao_existe_v1"}])
def test_P138_emenda_malformada_LEVANTA(estrago):
    q = _copia()
    q["pesquisa"]["emendas"] = [_emenda(**estrago)]
    with pytest.raises(R.EmendaInvalida):
        R.emendas(q)


@pytest.mark.parametrize("campo", R.CAMPOS_DA_EMENDA)
def test_P138_emenda_sem_campo_LEVANTA(campo):
    q = _copia()
    e = _emenda(); del e[campo]
    q["pesquisa"]["emendas"] = [e]
    with pytest.raises(R.EmendaInvalida):
        R.m_orcado(q)


def test_P138_politica_de_orcamento_diferente_de_BLOQUEIA_LEVANTA():
    """ALARME declarado e nao implementado seria o E-03."""
    q = _copia()
    q["pesquisa"]["orcamento"]["politica"] = "ALARME"
    with pytest.raises(NotImplementedError):
        R.conferir_orcamento(q, "hml_puro_v1", [])


def test_P138_dentro_do_orcamento_o_portao_nao_depende_de_git(monkeypatch):
    def sem_git(*a, **k):
        raise AssertionError("consultou o ramo publicado sem precisar")
    monkeypatch.setattr(R, "emendas_publicadas", sem_git)
    for r in P["pesquisa"]["diario"]:
        assert R.conferir_orcamento(P, r["estrategia"]) >= 0


def test_P138_o_repositorio_esta_dentro_do_orcamento_e_o_m_nao_andou():
    """Instantaneo: a guarda nova e inerte hoje. m_orcado 13 e m_executado 2 como antes."""
    assert P["pesquisa"]["emendas"] == []
    assert (R.m_orcado(P), R.m_executado(P)) == (13, 2)


# o verificador de verdade, contra um git de verdade
def _git(cwd, *args):
    import subprocess
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
                   cwd=cwd, check=True, capture_output=True)


def _repo_com_remoto(tmp_path, emendas):
    import shutil
    if shutil.which("git") is None:
        pytest.skip("git ausente")
    remoto, local = tmp_path / "remoto.git", tmp_path / "local"
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(remoto))
    _git(tmp_path, "clone", "-q", str(remoto), str(local))
    (local / "alocacao").mkdir()
    _escrever(local, emendas)
    _git(local, "add", "-A"); _git(local, "commit", "-q", "-m", "base")
    _git(local, "push", "-q", "origin", "HEAD:main")
    return local


def _escrever(local, emendas):
    import yaml
    (local / "alocacao" / "politica.yaml").write_text(
        yaml.safe_dump({"pesquisa": {"emendas": emendas}}, allow_unicode=True),
        encoding="utf-8")


def test_P138_verificador_so_aceita_o_que_foi_EMPURRADO(tmp_path):
    local = _repo_com_remoto(tmp_path, [])
    q = _estourado()
    q["pesquisa"]["emendas"] = [_emenda()]
    # commitada e nao empurrada: nao conta
    _escrever(local, [_emenda()])
    _git(local, "commit", "-q", "-am", "emenda")
    assert R.emendas_publicadas(q, raiz=str(local)) == []
    with pytest.raises(R.OrcamentoEstourado):
        R.conferir_orcamento(q, "hml_puro_v1", R.emendas_publicadas(q, raiz=str(local)))
    # empurrada: conta, e destrava
    _git(local, "push", "-q", "origin", "HEAD:main")
    pub = R.emendas_publicadas(q, raiz=str(local))
    assert [e["estrategia"] for e in pub] == ["hml_puro_v1"]
    assert R.conferir_orcamento(q, "hml_puro_v1", pub) == 0


def test_P138_emenda_publicada_com_OUTRO_texto_nao_vale(tmp_path):
    """Por conteudo: trocar a justificativa depois de publicar nao herda a publicacao."""
    outra = _emenda(justificativa=JUSTIFICATIVA.replace("18 dias", "20 dias"))
    local = _repo_com_remoto(tmp_path, [outra])
    q = _estourado()
    q["pesquisa"]["emendas"] = [_emenda()]
    assert R.emendas_publicadas(q, raiz=str(local)) == []


def test_P138_sem_ramo_publicado_o_portao_FECHA(tmp_path):
    """"Nao consegui conferir" nao pode ter a saida de "conferi" (P-102)."""
    q = _estourado()
    q["pesquisa"]["emendas"] = [_emenda()]
    with pytest.raises(R.OrcamentoEstourado, match="nao consegui ler"):
        R.emendas_publicadas(q, raiz=str(tmp_path))

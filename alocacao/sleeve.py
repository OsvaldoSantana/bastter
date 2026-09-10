# -*- coding: utf-8 -*-
"""
Sleeves: o que existe DENTRO de uma rota de renda variavel.

A camada de alocacao aloca para uma ROTA. Mas "Acao individual" nao e um ativo —
e um recipiente que precisa ser preenchido com empresas. Este modulo torna essa
distincao explicita e mede o que ela custa.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import carregar as carregar_custos
from alocacao import catalogo, arrasto_anualizado, carregar_politica

class DecisaoPendente(Exception):
    """Levantada quando um caminho depende de uma decisao ainda nao tomada."""

def verificar_decisao(P, chave):
    d = P["decisoes"][chave]
    if d["status"] == "PENDENTE":
        raise DecisaoPendente(f"{chave}: {d['nota'].strip()}")
    return True

def expandir_sleeve(rota, peso, P, C, aporte, anos):
    """Diz o que precisa existir dentro da rota para o peso ser executavel."""
    teto = P["tetos"]["por_ativo_pct_patrimonio"]
    if rota.exposicao != "acao_br":
        return dict(metodo="INDEXADO", n_ativos="o do indice", exige_selecao=False,
                    bloqueado=False,
                    nota="a diversificacao vem embutida; a taxa de administracao e o premio")
    n_min = math.ceil(peso/teto)
    n_rec = P["sleeves"]["selecao_ativa"]["n_minimo_default"]
    try:
        verificar_decisao(P, "A05_nucleo_indexado_vs_selecao_ativa")
        bloqueado, motivo = False, None
    except DecisaoPendente as e:
        bloqueado, motivo = True, str(e)
    # quantos meses para montar a sleeve comprando 1 ativo por mes
    meses = n_rec
    return dict(metodo="SELECAO_ATIVA", n_minimo_pelo_teto=n_min, n_recomendado=n_rec,
                meses_para_montar=meses, exige_selecao=True,
                bloqueado=bloqueado, motivo=motivo)

def premio_de_diversificacao(C, P, aporte, anos, etf="bova11", acao="acao_zero"):
    """Quanto custa comprar diversificacao pronta em vez de montar a sleeve.

    E a conta que decide A-05 do lado do CUSTO. O lado do RISCO so o backtest decide.
    """
    R = {r.id: r for r in catalogo(C)}
    a_etf  = arrasto_anualizado(R[etf],  C, aporte, anos)
    a_acao = arrasto_anualizado(R[acao], C, aporte, anos)
    # custo total em reais, pela diferenca de arrasto sobre o patrimonio simulado
    m = (1+0.1390)**(1/12)-1
    sem_custo = sum(aporte*(1+m)**(anos*12-i) for i in range(int(anos*12)))
    pat_etf  = sem_custo/((1+a_etf)**anos)
    pat_acao = sem_custo/((1+a_acao)**anos)
    return dict(arrasto_etf=a_etf, arrasto_acao=a_acao,
                delta_pp_aa=(a_etf-a_acao)*100,
                custo_extra_reais=pat_acao-pat_etf,
                aportado=aporte*12*anos,
                pct_do_aportado=(pat_acao-pat_etf)/(aporte*12*anos)*100)

if __name__ == "__main__":
    C, P = carregar_custos(), carregar_politica()
    R = {r.id: r for r in catalogo(C)}
    print("="*94)
    print("O QUE EXISTE DENTRO DA ROTA 'ACAO INDIVIDUAL'")
    print("="*94)
    e = expandir_sleeve(R["acao_zero"], 0.105, P, C, 500, 20)
    for k,v in e.items():
        print(f"  {k}: {v}" if k!="motivo" or not v else f"  {k}:\n     {v}")
    print("\n" + "="*94)
    print("O PREMIO DE DIVERSIFICACAO — quanto custa comprar a cesta pronta")
    print("="*94)
    print(f"\n{'aporte/mes':>12}{'ETF (BOVA11)':>16}{'acao (sleeve)':>16}{'delta a.a.':>13}"
          f"{'custo extra 20a':>18}{'% do aportado':>15}")
    for ap in (200, 500, 1000, 2000):
        d = premio_de_diversificacao(C, P, ap, 20)
        print(f"{ap:>12}{d['arrasto_etf']*100:>15.4f}%{d['arrasto_acao']*100:>15.4f}%"
              f"{d['delta_pp_aa']:>12.4f}%{d['custo_extra_reais']:>18,.0f}{d['pct_do_aportado']:>14.2f}%")
    print("""
  LEITURA: a coluna 'custo extra' e o que voce paga, em 20 anos, para NAO ter que
  escolher as empresas. E o premio de um seguro contra risco de selecao.

  Bessembinder (2018) mede esse risco: 55-58% das acoes individuais rendem menos que
  titulo publico ao longo da vida; fora dos EUA, 1,41% das empresas geram toda a
  riqueza liquida. A mediana e negativa — a media so e positiva por causa da cauda.

  Se o premio e caro ou barato depende de quantas empresas voce consegue segurar e
  de acertar quais. Essa e a decisao A-05, e ela NAO se resolve por argumento.""")

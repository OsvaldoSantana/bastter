# Registro v4 — leitura de `docs/fontes` (04/09/2026)

32 arquivos `.md` lidos e avaliados. Laudo completo publicado como artefato
"Laudo das Fontes Primárias".

## Achados que mudaram o motor

### F-01 — custódia interna dos ETF iShares (erro meu, corrigido)
Os 5 regulamentos (BOVA11/BRAX11/CAPE11/EWBZ11/SMAL11, vig. 21/05/2026) preveem,
ALÉM da taxa de administração, custódia máxima de **0,025% a.a. cobrada dentro do
fundo**. O motor só modelava `adm_aa`.

- novo campo `RotaAloc.custodia_interna_aa` + propriedade `interno_aa`
- `simular_custo` e `retorno_liquido_aa` passam a usar `interno_aa`
- valor e rol vêm de `custos.yaml → etf.custodia_interna_ishares` (`valor` + `aplica_a`),
  nunca de lista no código
- **BOVA11: 0,100% → 0,125% a.a. (25% a mais).** 10 anos a R$500/mês: −R$186,70
- **o ranking de CRESCIMENTO mudou:** BOVA11 caiu abaixo de `acao_450`
- status PARCIAL: o regulamento declara o TETO, não o efetivo

### F-02 — rota bloqueada simulava com custo zero (erro meu, mais grave, corrigido)
`bovv11` (adm NAO_CONFIRMADO) era criada com `adm_aa = 0.0` e `simular_custo` não
olhava `bloqueios`. Resultado: **0,323% do aportado — a rota mais barata do catálogo.**
O G5 matava depois, então o veredito final saía certo por acidente, mas os relatórios
intermediários (`fora_atrito`, interação G3×G4) usavam número inventado.

- `simular_custo` levanta `InsumoBloqueado` para rota não confiável
- **G5 movido para ANTES do G3** — status é pré-condição de comparação de custo
- `g5_status` aceita rota nua ou par
- `universo.fora_status` mudou de forma: lista de ROTAS, não de `(rota, custo)`
- dívida técnica registrada: a ORDEM dos portões está no código, não no YAML (viola P3)

### F-03 — ETF de renda fixa como concorrente do `td_ipca` (rota candidata, aberta)
Lei 13.043/2014 art. 2º III + IN RFB 1.585/2015 art. 28 + Decreto 6.306/2007 art. 32
§2º VII: **15% de IR** com prazo médio > 720 dias, **só no resgate/alienação/distribuição**
(sem come-cotas), **IOF zero**. Lei 14.754/2023 art. 22 exclui o ETF de RF da definição
geral de ETF.

Disputa `PROTECAO_REAL` com o `td_ipca` sem pagar a custódia de 0,20% a.a. da B3.
`custos.yaml → etf.IMAB11` NAO_CONFIRMADO, bloqueia `rota_etf_renda_fixa_protecao_real`.
O "0,04%" que estava no `fora_de_escopo` era prosa sem fonte — removido de lá.

## Pendências fechadas com fonte primária
- **isenção de FII: 100 cotistas** (Lei 11.033 art. 3º §§1º-4º red. 14.754/2023;
  confirmado independentemente pela Lei 15.270/2025 art. 16-A §1º V "i")
- **VTI 0,03% COMPLETO** (era NAO_CONFIRMADO); VOO → COMPLETO
- **custódia RV: isenção R$26.471,77 + 10 faixas** conferidas uma a uma no PDF v5.0
- **periodicidade do Tesouro: netting pro rata** desde 31/12/2024 (OC 014/2024-VPC)
- **layout COTAHIST** verificado contra dado real
- **enumerações CVM** ORDEM_EXERC / ESCALA_MOEDA / MOEDA — status OBSERVADO

## Custos novos catalogados
- manutenção de conta inativa B3: R$3,82/mês após 60 meses
- IRRF "dedo-duro" 0,005% (`e_custo_liquido: false` — é antecipação, não despesa)
- **IOF = ZERO** em renda variável em bolsa (Decreto 6.306 art. 32 §2º III e IV)
- CAPE11 e EWBZ11 a 0,30% a.a.

## Divergência registrada (não resolvida)
`b3.vista_total_pct`: v5.0 item 1.2.3 dá 0,0274% (negociação 0,00500% + CCP 0,02240%);
página web da B3 dá 0,0300% incluindo TTA e tributos. Escopos diferentes, não erro.
**Mantido 0,0300% (o maior), status rebaixado para PARCIAL**, bloco `divergencia`
com os dois valores e a razão.

## Nova seção `politica.yaml → limitacoes_declaradas`
1. **IR na venda de RV** — não modelado para nenhuma rota. A isenção de R$20 mil/mês
   existe para ação e NÃO para ETF (IN 1.585 art. 59 §2º II). O viés favorece o ETF,
   que é uma das duas pontas da decisão A05. Zero efeito na acumulação sem venda.
2. **periodicidade da custódia do Tesouro** — desconto mensal vs netting semestral.
   Viés conservador: erra CONTRA a rota do Tesouro.
3. **ordem dos portões não é dado** — dívida técnica exposta pelo F-02.

## Correções em registros anteriores
- evidência da A05: "0,024% vs 0,094%" → **0,021% vs 0,097%** (10 anos, R$500/mês)
- evidência da A05: a linha da isenção de R$20 mil ganhou artigo e parágrafo
- `fora_de_escopo.FII`: acrescentado que classe de FII é **obrigatoriamente fechada**
  (CVM 175 Anexo III art. 3º) — não existe resgate, a liquidez é a do book

## Testes
144 passando (eram 140). Os dois novos do F-01 e os dois do F-02 falham na versão
anterior. O teste do F-01 compara DUAS simulações e exige diferença > 1% do custo
total — um campo declarado e nunca lido passaria num teste de atributo.

## Lacunas que continuam
| lacuna | bloqueia | quem resolve |
|---|---|---|
| fórmulas do FGC (CMN 5.238/5.295) — em imagem | nada no motor | PDF oficial do BCB |
| taxa do IMAB11 | `rota_etf_renda_fixa_protecao_real` | regulamento do fundo |
| taxa do BOVV11 — site bloqueia robô | `tabela_etf_rv_completa` | visita manual |
| PCF diária dos iShares (.xls binário) | aderência ao índice | converter p/ .xlsx |
| art. 65 da Lei 8.981/1995 | nada | ver nota abaixo |
| `macro.cdi_aa` expira 04/09/2026 | nada ainda | BCB/SGS 4389 |

**Art. 65 identificado sem ser lido:** o Decreto 6.306/2007 art. 32 §3º cita "as
operações conjugadas de que trata o art. 65, §4º, alínea 'a', da Lei 8.981/1995".
Art. 65 é o artigo de renda fixa; §4º "a" trata operação conjugada (box de opções,
termo com cobertura) como renda fixa sintética. Irrelevante hoje — opções estão
fora de escopo por declaração do usuário.

# Emenda 1 do pré-registro ML v2 — o mês medido

*25/09/2026. Medido **depois** de a regra ser empurrada (`00aa622`, emenda com sha256
`1aac96023fdc0de9`), como a P-116 exige. Este documento registra; não muda a regra.*

## Resultado

> **O desenvolvimento começa em março de 2011.**

Mar/2011 é o primeiro mês em que ≥ 90% das empresas do universo da §2 da v2 têm ao menos um
documento DFP/ITR com `DT_RECEB` ≤ o último pregão do mês.

| mês | universo (n) | com `CD_CVM` | com documento | cobertura |
|---|---|---|---|---|
| jan/2010 … dez/2010 | 112–120 | 115–119 | 0 | 0% |
| jan/2011 | 117 | 116 | 2 | 1,7% |
| fev/2011 | 119 | 118 | 42 | 35,3% |
| **mar/2011** | **120** | **119** | **115** | **95,8%** |
| abr/2011 | 121 | 120 | 116 | 95,9% |
| dez/2011 | 116 | 114 | 114 | 98,3% |

Janela "t-2..t" (os 3 meses que terminam na data de decisão). A tabela inteira, mês a mês de
2010 a 2012, sai de `py -3.11 fase0/universo_ml.py`.

## Por que o resultado é robusto, e onde não é

- **Às duas leituras de "3 meses anteriores"** (§2 da v2 não escolhe): a janela "t-3..t-1" dá o
  mesmo mês, mar/2011, com 115/119 = 96,6%. A escolha entre elas **não** afeta a emenda. Ela
  continua em aberto para o universo do ML (P-145).
- **Às empresas sem ponte:** em mar/2011 é **1** (BBRK). Contada como coberta, fevereiro chegaria
  a 36%; contada como descoberta, março fica em 95,8%. O mês não muda.
- **À ponte manual, NÃO.** 42 emissores foram ligados à mão (`ponte-emissor-cvm.yaml`, sha256
  `6e9736c3886ad1a9`), por sucessão societária conferida linha a linha, com o par CNPJ/CD_CVM
  conferido no cadastro da CVM por teste. Sem ela, a cobertura trava em ~76% e nenhum mês de
  2010 a 2012 chega a 90%. **O resultado vale enquanto a ponte manual valer.**

## Insumos

| insumo | versão |
|---|---|
| COTAHIST 2009–2012 | pelo leitor do ML (`insumo_ml.abrir_cotahist`), pins da P-140 |
| banco de ISIN da B3, arquivo "geral" | `isinp.zip` de 25/09/2026 03:00, sha256 `c4654dbdefd88ac8…`, 7.797.263 bytes |
| índices DFP 2010–2012, ITR 2011–2012 | acervo da CVM (`docs/acervo/cvm/capturas.csv`) |
| cadastro da CVM | `cad_cia_aberta.csv` de 25/09/2026 |
| ponte manual | `docs/aprendizado/ponte-emissor-cvm.yaml`, sha256 `6e9736c3886ad1a9` |

A regra de universo aplicada é a da §2, com as leituras declaradas no topo de
`fase0/universo_ml.py`: TPMERC 010 e CODBDI 02; ≥ 90% dos pregões da janela; volume médio
≥ mediana dos que passaram; uma classe por empresa, a mais líquida; empresa = código do emissor
no ISIN (A-01).

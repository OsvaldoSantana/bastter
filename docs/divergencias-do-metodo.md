# O que o MEOL adota do método do Bastter.com, e onde diverge

O MEOL foi inspirado no método publicado pelo [Bastter.com](https://bastter.com), **sem
vínculo** com o site ou com seus autores. Este registro diz, parâmetro por parâmetro, o que foi
adotado, onde o projeto diverge, e onde está escrito o porquê. Ele não julga o método como
estratégia: descreve decisões deste projeto, cada uma com o arquivo em que foi tomada.

**Base.** Os parâmetros do método são os do *Pequeno Manual* (ed. 2024) e do *Roteiro do
Iniciante* (2023), na destilação do dossiê de 28/08/2026 que deu origem ao projeto. O dossiê e
os livros não estão no repositório, porque não são deste projeto. A auditoria do dossiê está em
[`docs/referencia/laudo-auditoria-consolidado.md`](referencia/laudo-auditoria-consolidado.md).

## Parâmetro por parâmetro

| no método | no MEOL | | onde |
|---|---|---|---|
| Patrimônio não se gira | atrito medido (custo fixo e percentual) e compromisso de carrego | **adota** | portões G3 e G8, `alocacao/politica.yaml → portoes` |
| Sequência: zerar dívidas → reserva → investimentos | portões da fase *aporte*, antes da fase *universo* | **adota a ordem** | `alocacao/politica.yaml → portoes` |
| Nunca faça dívidas | a dívida é paga quando o custo **líquido** dela passa o retorno **líquido** da alternativa | diverge | portão G1, [doutrina P3](doutrinas.md) |
| Reserva de emergência ≥ 6 meses, em poupança | a reserva vem antes; o destino é escolhido por retorno líquido entre as rotas elegíveis | diverge no destino | portão G2, `alocacao/reserva.py` |
| Renda fixa entre 10% e 50%, nunca 0%, nunca 100% | piso e teto de renda variável, em YAML | **adota o princípio**; os números são parâmetro | `alocacao/politica.yaml → crescimento` |
| Nenhum ativo acima de 2% do patrimônio | teto por papel parametrizado (5% hoje), testável | diverge no valor e na forma | `alocacao/politica.yaml → tetos` |
| Reserva de valor 3–5% (moedas, ouro, bitcoin) | funções de risco separadas; ouro e dólar como seguro de jurisdição, julgado por estar fora do alcance, não por render | diverge na classificação | `alocacao/politica.yaml → funcoes` |
| Um aporte por mês | piso mais aporte extraordinário: o valor mensal não é fixo | diverge | `alocacao/aporte.py`, `alocacao/politica.yaml → aporte_extraordinario` |
| Rebalancear só por compra | a rota acima do alvo mais a banda sai da fila do aporte | **adota** | `alocacao/politica.yaml → tetos.banda_sobre_alvo_pp` |
| Escolher empresas por critério próprio | só depois de uma régua pré-registrada e medida; até lá o motor recusa nomear | diverge no quando | `alocacao/perfil.yaml → decisoes`, [`docs/aprendizado/`](aprendizado/) |
| Opções e aluguel para rentabilizar a carteira | pendência com duas famílias (coberta e descoberta), não exclusão | em aberto | [`PENDENCIAS.md`](../PENDENCIAS.md), P-20 e P-22 |

## O que vale para o projeto inteiro

- **Regra como dado.** Todo parâmetro acima vive em YAML versionado, com procedência. Trocar um
  deles é um commit que pode ser lido e revertido ([P1 e P2](doutrinas.md)).
- **Ausência de régua não exclui.** O que o projeto ainda não sabe avaliar fica no catálogo com
  peso zero e o motivo escrito ([P6](doutrinas.md)).

## Como este registro muda

Uma divergência nova entra aqui com o arquivo em que foi decidida. Uma divergência desfeita não
some: vai para o fim, com a data e o motivo, como os achados retirados em
[`ACHADOS.md`](../ACHADOS.md).

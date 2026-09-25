# Guia do leitor

Três caminhos, por quanto tempo você tem e pelo que você quer fazer. Todos começam no
[README](../README.md).

## 5 minutos — o que é

1. O [README](../README.md): o que o sistema faz, o que ele não é, e onde o projeto está.
2. As [sete doutrinas](doutrinas.md). Leia os títulos e o primeiro parágrafo de cada uma. O
   resto é a história de como cada regra nasceu de um erro.
3. [O que o MEOL adota do método do Bastter.com, e onde diverge](divergencias-do-metodo.md):
   uma tabela, um parâmetro por linha.

Se só der tempo para uma frase: **cada número diz de onde veio, e um cálculo que dependa de um
valor não confirmado se recusa a rodar.**

## 30 minutos — auditar um número de ponta a ponta

O exemplo é o prêmio de valor no Brasil, **HML: 0,688% ao mês, t = 2,60**, de janeiro de 2001
a junho de 2026. Ele derrubou uma premissa do pré-registro, que esperava perto de zero. O
caminho é o mesmo para qualquer número do projeto: **fonte → bytes → cálculo → registro → teste
→ o que mudaria com outra escolha**.

**1. A fonte.** [`docs/fontes/nefin.md`](fontes/nefin.md): quem publica, a URL, a data de
acesso, os termos de uso e a metodologia transcrita. O arquivo **não** está no repositório,
porque os termos do NEFIN não autorizam redistribuir.

**2. Os bytes.** O pré-registro fixa o sha256, não o caminho:

```bash
grep -A3 "^pesquisa:" alocacao/politica.yaml            # fonte.sha256_12: 619991c2192c
curl -sL -o alocacao/dados/nefin_factors.csv \
  https://nefin.com.br/nefindata/risk-factors/nefin_factors.csv
sha256sum alocacao/dados/nefin_factors.csv               # tem de começar por 619991c2192c
```

Se o hash não bater, o NEFIN publicou uma versão nova. O número deixa de ser uma conferência e
passa a ser um número novo, e o registro de cada versão observada está em
[`docs/acervo/nefin/capturas.csv`](acervo/nefin/capturas.csv).

**3. O cálculo.**

```bash
cd alocacao && python fatores.py          # a linha HML: 0.688%  t 2.60
```

O código é `premios()` em [`alocacao/fatores.py`](../alocacao/fatores.py): média mensal, só
com meses de pelo menos 15 pregões. O último mês da série é parcial e sai.

**4. O registro.** `alocacao/politica.yaml → estrategias_pre_registradas.execucao` diz o que
foi pré-registrado, quando rodou, e que a média e o t reproduziram exatamente. Diz também o
que estava errado no registro: 307 meses brutos, 306 depois do filtro.

**5. O teste que impede a volta.**
`test_hml_e_positivo_e_significante_contrariando_a_literatura_citada`, em
[`alocacao/test_fatores.py`](../alocacao/test_fatores.py). Ele exige o prêmio positivo e
t > 2 na série inteira e em quatro janelas.

**6. O que mudaria com outra escolha.** Com correção pela quantidade de testes que o próprio
projeto pré-registrou (13), o HML **não** sobrevive: o corte sobe para ~3,15, e o t do alfa é
2,94. A decomposição, e por que a suposição de distribuição pesou mais que a de dependência,
está em [`docs/auditoria/ROMANO-WOLF.md`](auditoria/ROMANO-WOLF.md). Um número aqui vem com a
pergunta *"e se a escolha fosse outra?"* já respondida, ou com a razão de ainda não estar.

Para uma constante de custo, o caminho é mais curto:
`python alocacao/impacto.py <nome>` mostra o que depende dela, e o próprio
`alocacao/custos.yaml` traz `status`, `fonte`, `acesso` e `expira` ao lado de cada valor.

## Contribuidor

1. [`CONTRIBUTING.md`](../CONTRIBUTING.md): instalação, testes, as regras da casa e a
   convenção de commit.
2. [`CLAUDE.md`](../CLAUDE.md), §9: o protocolo de mudança. Ele foi escrito para as sessões
   de IA que trabalham no projeto, e vale igual para quem é de fora.
3. [`ACHADOS.md`](../ACHADOS.md): leia os da área antes de mexer nela. Vários defeitos deste
   projeto são o mesmo padrão com outra roupa.
4. [`PENDENCIAS.md`](../PENDENCIAS.md): o que está aberto, com dono, gatilho e classe. A
   classe `BLOQUEIA_O_SISTEMA` é o caminho crítico.
5. Para reproduzir o dado de mercado sem o nosso armazém: [`docs/reproduzir.md`](reproduzir.md).

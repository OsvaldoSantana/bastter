---
name: bastter-mudanca
description: Protocolo de mudança do projeto Bastter — o que rodar antes de editar, quando exigir instantâneo dourado, e o que registrar depois. Use ao alterar qualquer arquivo de alocacao/.
---

# Protocolo de mudança — projeto Bastter

Cada passo aqui pegou **pelo menos um defeito real** que o passo anterior deixou passar.
Não é cerimônia: é o que a semana de 01–06/09/2026 produziu, e o custo de pular está
medido.

## Antes de editar

1. **`python impacto.py <alvo>`** — constante, função ou campo. Mostra o que alcança o
   que você vai mexer.
   > O achado N-01 quase passou por falta disto: procurei um nome no Python, achei zero
   > ocorrências, e só não conclui "ninguém lê" porque desconfiei de um número repetido.

2. **Leia os pontos cegos do relatório.** Chave montada em tempo de execução
   (`P["funcoes"][f]`), `getattr` dinâmico e despacho por dicionário **não aparecem no
   mapa**. Toda conclusão de "ninguém lê isto" passa por essa lista antes de virar
   decisão. Um mapa que finge completude é pior que grep.

3. **Mudança de contrato? Instantâneo dourado, obrigatório.** Contrato = dataclass,
   retorno de função, estrutura de YAML, ou qualquer coisa que muitos consumidores leiam.

   Serialize o comportamento **antes** de tocar em nada, numa matriz de cenários, de
   forma canônica e comparável. Depois compare **campo a campo** — cada string de
   alerta, cada pendência, cada item de cada lista de rejeição. Não só os números.

   > Garantiu a P-36 (39 registros de catálogo migrados, zero diferenças) e a P-37
   > (`alocar()` de 300 linhas quebrada em 6, 38 cenários, zero desvio).
   > **Refatorar sem essa rede é reescrever e torcer.**

## Depois de editar

4. **`python -m pytest -q | tail -3`** — a suíte é o **júri**, nunca o guia. Ela
   responde "quebrou?", não "o que isto alcança?". Use `tail` — a saída inteira custa
   tokens sem informar.

5. **`ruff check . && mypy --ignore-missing-imports .`** — ambos em **zero**. Barreira
   com baseline conhecida não é barreira: a violação seguinte se esconde no ruído.

6. **Compare o instantâneo.** Diferença esperada e aceitável: `politica_hash` e
   `politica_versao`, quando você mexeu no `politica.yaml`. Qualquer outra diferença é
   um desvio a explicar antes de seguir.

## Registrar — a parte que ninguém pula

7. **`PENDENCIAS.md`** — pendência precisa de **dono, gatilho e classe**. Sem os três
   não é pendência, é desabafo. Se fechou, mova a narrativa para `ACHADOS.md` e deixe
   só a linha na tabela `## Fechadas`.

8. **Achado novo?** Use a skill `bastter-achado`.

9. **`politica.yaml → meta.versao` + changelog**, e `pyproject.toml` acompanha a versão.

## O que NÃO fazer

- **Não releia o arquivo que você acabou de escrever.** A ferramenta de edição falha se
  a edição não colou.
- **Não aplique correção automática de lint sem olhar.** O ruff apontou uma *variável*
  morta em `montar_rotas`; o defeito era a *chamada*, que abortava dentro de uma função
  cuja docstring promete não abortar (achado T-01).
- **Não apague código que tem teste próprio** sem medir o que os testes guardam. É como
  se perde uma rede.
- **Não use âncora curta em `str.replace`** para editar Markdown. Uma âncora como
  `"## Fechadas"` casou dentro de uma citação e partiu o arquivo ao meio em 06/09.

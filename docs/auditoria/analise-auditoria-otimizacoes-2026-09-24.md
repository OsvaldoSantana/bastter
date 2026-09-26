# Análise crítica da peça "Auditoria, otimizações e inovações — 23/09/2026" — 24/09/2026

*Trazida do Projeto no claude.ai para o repositório em 26/09/2026, sem alteração de conteúdo. Até esta data só existia lá.*

*Conferida contra o código em 24/09 (estado_io.py, alocacao.py, conftest.py, test_usuario_novo.py,
test_p71_p72_porta_de_entrada.py, perfil.yaml, pyproject.toml, CLAUDE.md, PENDENCIAS.md, reserva.py,
motor.py). Status: `ESPECIFICACAO` — nada foi alterado.*

## Veredito

A peça leu seis arquivos de `alocacao/` e generalizou para o projeto. Dentro desses arquivos
ela acerta bastante; fora deles erra quase sempre. Cerca de metade dos itens procede, e dois
dos consertos propostos como prioridade 1 (C2 + C3) **reabririam o J-01** — a reserva empenhada
declarada voltaria a ser campo morto.

## Item a item

| item | veredito | evidência |
|---|---|---|
| C1 `f.type == "str"` | **procede, severidade menor** | acoplamento real ao `__future__` do alocacao.py. Mas a falha seria ruidosa (`nome: 'x' nao e numero`), não silenciosa. Conserto certo: `typing.get_type_hints(classe)`, que resolve as duas formas |
| C2 reserva_disponivel | **não procede** | `Estado.reserva_efetiva` (alocacao.py:188) já trata `None` como nominal; o preenchimento do validador é equivalente. E "P1 = ausência não vira suposição" está errado: P1 é procedência |
| C3 `_conferir_empenho` | **não procede, e o conserto é perigoso** | o "problema falso" é a proteção: `reserva_empenhada: 500` sem `reserva_disponivel` faria o motor ignorar o empenho. Com C2+C3 aplicados, o campo volta a ser lido e descartado — a 4ª ocorrência de campo morto que o J-01 fechou |
| C4 fixtures de sessão | **procede** | `custos_originais`/`politica_original` protegidos só pela docstring "NÃO altere" — disciplina, exatamente o que a P-38 recusou. test_alocacao.py:2422 já os recebe |
| C5 limpar caches | **não procede** | limpar entre testes é a opção COPIAR SEMPRE que o próprio conftest rejeita por esconder o defeito; esconderia a classe do S-02. A "lição" da docstring não é promessa de guarda |
| C6 regex de literais | procede em parte, baixa prioridade | AST é melhor; o caso f-string não quebra a regex atual |
| C7 portão lê `ativo` | **procede** | mede a palavra no fonte, não o comportamento — forma do A-06 |
| C8 P72 negativo | procede, valor baixo | `carregar` levanta sempre que há problema com `exigir_real=True` (estado_io.py:249); o `pytest.raises` só remove a dependência dessa linha |
| C9 alias | **o buraco procede; o conserto não compila** | `from estado_io import carregar as c` põe "c" em `nomes`, e `c()` é `ast.Name`, não `Attribute` → a guarda passa. O conserto proposto `{a.name, a.asname or a.name for a in n.names}` é SyntaxError. Certo: registrar `a.name` |
| C10 HOR01 × estado | risco procede; teste proposto não | o teste lê o estado.yaml real: quebra onde ele não existe (fora do git) e viola a U-01 e o próprio test_usuario_novo. Qual é a fonte única do horizonte é decisão dele |
| O1 responder.py | **valor procede — o maior item** | mas o exemplo contradiz o J-01 ("Cofrinho PicPay é LIQUIDEZ ⇒ entra na composição"; estado_io.py:170 registra o saldo como limite de cartão, disponível para resgate zero). Números inventados; set/2026 + 64 meses é jan/2032, não mai/2032 |
| O2 aportes.yaml | valor procede; falta a cerca | é dado pessoal: tem de ficar fora do git como o estado.yaml (P-62/P-67). A peça o põe em `alocacao/` sem mencionar |
| O3 manifesto CVM | **não procede** | a P-48 é "viés de sobrevivência", não manifesto; e o manifesto já existe e roda ao fim de cada captura |
| O4 três simulações | procede pela metade | `reserva.simular` é outra coisa (reserva × investimento). Duplicação real: `motor.simular` × `alocacao.simular_custo` |
| O5 testpaths | **procede — decisão dele pendente desde 16/09 (P-80)** | não é "uma linha": o ruff na raiz tem 14 violações em pesquisa-custos, e os testes de fase0 que leem `data/` têm de pular onde ele não existe |
| O6 24 achados órfãos | procede | P-104 já aberta |
| O7 cortar CLAUDE.md | **procede — maior ganho de tempo por sessão** | 2.124 linhas / 132 KB; blocos datados da linha 1375 ao fim (~750 linhas). PENDENCIAS: 2.947 linhas / 179 KB. "600 linhas" e "60%" são palpite |
| O8 contar testes | não procede | número fixo quebra a cada teste novo; o conserto é tirar contagens da prosa (§8 já existe para isso) |
| I1–I4 | uma ideia em quatro | registrar recomendação × execução. Dependem do O2. "Nenhum robo-advisor faz" sem fonte; "correto por definição" e "o motor está certo e você atrapalhou" são erros de inferência — resultado de 6 meses é ruído |
| I2/I11 | fracas | ~12 observações por ano; "6/7 aportes no mês" não faz sentido com aporte mensal |
| I5 what-if | procede, barato | as funções existem |
| I6, I10 | válidas, fora de hora | |
| I7 | já existe em partes | trailer, CRC, testzip, C-02 |
| I9 | doutrina inventada | "P7 diz degrada, não quebra" — a frase não existe no CLAUDE.md |
| "Não fazer" 2 e 3 | contradizem decisão dele | pré-registro de ML v2 empurrado (2c608c9) |
| "Nenhuma depende de outra" | falso | I1←O2; I3, I4←I1; I11←I2 |

## O que entra no projeto

- Sessão paralela em `alocacao/`: C1, C4, C7, C8, C9 (com o conserto certo), O4 medido.
- Decisões dele: P-80 (O5), fonte única do horizonte (C10), O1 depois da P-57.
- Não entram: C2, C3, C5, O3, O8.

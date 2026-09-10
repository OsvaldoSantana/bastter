# Politica de atualizacao do ITR — CONFIRMADA, e e identica a do DFP
Fonte: https://dados.cvm.gov.br/dataset/cia_aberta-doc-itr
Acesso: 06/09/2026, pelo navegador do Osvaldo; pagina colada na conversa.
Metodo: leitura humana. O portal responde ROBOTS_DISALLOWED as minhas ferramentas.
Status: **COMPLETO**. Fecha a P-55.
Licenca: ODbL, igual ao DFP.
Leia junto: `cvm-dfp-politica-atualizacao.md`.

---

## O que foi conferido

> *"Os arquivos no conjunto de dados serao **atualizados semanalmente** com as eventuais
> **reapresentacoes**."*
> *"...demonstracoes financeiras entregues **nos ultimos cinco anos**"*
> *"**Historico desde 2011** (incluindo arquivos **nao sujeitos a politica de
> atualizacao**)"*

| campo | ITR | DFP |
|---|---|---|
| Periodicidade | **Semanal** | Semanal |
| **Ultima Atualizacao** | **31/08/2026, 08:01 (UTC-03:00)** | **31/08/2026, 08:01** |
| Criado | 29/11/2019, 23:30 | 29/07/2020, 20:43 |
| Historico desde | **2011** | 2010 |
| Base legal | Res. CVM 80/22, **art. 22, V** e **art. 31** | art. 22, IV e art. 30 |
| Licenca | ODbL | ODbL |

## Dois achados que so aparecem ao comparar as duas paginas

### 1. A janela de cinco anos deixou de ser inferencia

No DFP eu **deduzi** que os 6 recursos eram 2021–2026, contando. No ITR a CVM
**rotula cada recurso com o ano**:

```
Formularios de Informacoes Trimestrais (ITR) (2021)
... (2022) ... (2023) ... (2024) ... (2025) ... (2026)
```

**A janela e 2021–2026, observada, nao deduzida.** E como as duas paginas descrevem a
mesma politica com as mesmas palavras, a leitura do DFP fica confirmada por analogia
direta — que aqui e legitima porque o texto e literalmente o mesmo, nao porque "deve ser
parecido".

### 2. O carimbo identico revela que e UM job, nao dois

`31/08/2026, 08:01` nos **dois** conjuntos, ao minuto. Nao sao duas rotinas que por acaso
rodam junto: e **um unico processo semanal do portal** que regenera os conjuntos.

**Consequencia de desenho, e ela simplifica a rotina do projeto:** uma unica captura
semanal cobre DFP e ITR, e **um unico campo `last_modified` decide se vale a pena baixar
qualquer coisa**. Nao e preciso conferir arquivo por arquivo — basta ver se o carimbo do
portal mudou desde a ultima captura.

**Corolario mais forte, e ele nao e obvio:** como o job e semanal e unico, a captura tem
uma **cadencia natural**, e essa cadencia e observavel. Se o carimbo parar de andar, ou
andar duas vezes na mesma semana, isso e um evento — e um sistema que registra
`last_modified` a cada captura ve isso sozinho.

## NAO_CONFIRMADO

- O **dia da semana** do job. Um unico carimbo (31/08/2026) nao define cadencia: sao
  necessarias pelo menos duas capturas afastadas para saber se e sempre segunda, se e
  sempre 08:01, e se falha as vezes. **A primeira captura nao responde isso; a terceira
  responde.**
- Se um arquivo, ao sair da janela de cinco anos, congela como esta ou e regerado uma
  ultima vez.
- Se a janela desliza por ano-calendario (em 01/01/2027 entra 2027 e sai 2021) ou por
  outro criterio.

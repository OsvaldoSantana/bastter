# Segurança

## Como relatar

Pelo **relato privado do GitHub**: aba *Security* deste repositório → *Report a
vulnerability*. O relato chega só ao mantenedor e não fica público. **Não abra issue** para
vulnerabilidade: uma issue é pública desde o primeiro minuto.

Diga o que você viu, onde (arquivo, commit, workflow) e, se puder, como reproduzir.

## O que conta como vulnerabilidade aqui

- **Vazamento de dado pessoal.** O repositório é público e o sistema é de uma pessoa. A
  situação financeira real (`alocacao/estado.yaml`) fica fora do git por desenho, e há um
  teste que mede o índice para isso. Se você achar dado pessoal que não deveria estar
  publicado (em arquivo, no histórico, num log de workflow ou num artefato), isso é
  vulnerabilidade, mesmo que não haja código explorável.
- **Credencial exposta.** As credenciais do armazém existem só como segredo do repositório e
  variável de ambiente. Qualquer credencial em arquivo, log ou histórico é um incidente.
- **Workflow que pode ser induzido a vazar segredo** ou a agir com permissão maior que a
  necessária.
- **Integridade do dado.** Um caminho em que um arquivo capturado possa ser trocado sem que o
  sha256 registrado acuse.

## O que não conta

Discordância de método, número que você acha errado ou crítica ao pré-registro vão por issue,
com a medição. Isso é contribuição, não incidente.

## Versões

Só o `main` recebe correção. Não há versões antigas mantidas.

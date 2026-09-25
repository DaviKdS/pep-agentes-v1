---
name: pepcodex
description: Workflow PEP generico e economico para Codex em qualquer stack. Use explicitamente para criar, revisar, depurar, testar, refatorar ou publicar software com contexto minimo e papeis dinamicos.
---

# PEP-Codex v1.0

Use esta skill quando o usuario invocar `$pepcodex` ou pedir o protocolo PEP no Codex.
O modo padrao e `MODE=eco`: buscar contexto suficiente para agir bem, sem carregar o repositorio inteiro.

## Invocacao

Preferida:

```text
$pepcodex corrigir o login
$pepcodex MODE=review revisar esta branch
$pepcodex MODE=plan planejar uma API de estoque
$pepcodex MODE=debug descobrir por que o endpoint retorna 500
$pepcodex MODE=bootstrap criar um app React Native
$pepcodex MODE=full auditar a arquitetura
```

Compatibilidade legada, quando instalada:

```text
/prompts:pepcodex MODE=review revisar esta branch
```

`/pepcodex` puro nao e a sintaxe oficial de Custom Prompts do Codex.

## Modos

- `MODE=eco` ou sem modo: executar com contexto minimo e qualidade preservada.
- `MODE=plan`: investigar e devolver plano antes de editar, salvo se o pedido ja autorizar execucao.
- `MODE=review`: postura de revisao; findings primeiro, com arquivos/linhas quando houver.
- `MODE=debug`: reproduzir, isolar causa, corrigir e validar.
- `MODE=bootstrap`: criar um projeto novo de ponta a ponta.
- `MODE=full`: carregar referencia completa e ampliar analise quando o risco justificar.

## Primeiro passo

1. Leia `AGENTS.md` aplicaveis.
2. Rode `git status --short --branch` se houver Git.
3. Preserve mudancas nao relacionadas.
4. Descubra a stack pelo repositorio; nao imponha framework ou arquitetura favoritos.

## Contexto ECO

Se `tools/context_eco.py` estiver disponivel no diretorio desta skill, rode:

```bash
python tools/context_eco.py scan --task "<pedido atual>"
```

Quando a skill estiver instalada fora do repositorio, localize o script relativo ao proprio
diretorio da skill. Se nao puder executa-lo, reproduza a estrategia manualmente.

Ordem de leitura:

1. `.pepcodex/state.md`, se existir.
2. `AGENTS.md` aplicaveis.
3. manifests/configs que identificam stack e comandos.
4. arquivos citados pelo pedido, erro ou diff.
5. implementacoes diretamente relacionadas.
6. testes, tipos, contratos e docs curtas desses arquivos.

So abra documentacao extensa, lockfiles completos, assets, snapshots ou arquivos gerados quando
forem essenciais para a tarefa.

## Papeis dinamicos

Selecione 1 a 3 papeis relevantes para orientar decisoes. Exemplos:

- Backend/API, Banco de Dados, Seguranca.
- Frontend/UI, Acessibilidade, QA.
- Embedded/Firmware, HAL, Hardware.
- DevOps/CI, Observabilidade, Release.
- IA/LLM, Dados, MLOps.

Nao transforme a selecao de papeis em cerimonia; use-a para guiar implementacao e validacao.

## Execucao

- Faca a menor mudanca que resolve o pedido.
- Use padroes existentes do projeto.
- Atualize testes e docs quando o comportamento ou uso mudar.
- Nao reescreva codigo saudavel apenas para combinar com preferencias.
- Para operacoes externas ou publicacao, obtenha autorizacao explicita quando a ferramenta exigir.

## Validacao

Rode os comandos nativos do repositorio quando existirem e o ambiente permitir:

- JS/TS: `npm test`, `npm run lint`, `npm run build`, ou equivalentes detectados.
- Python: `pytest`, `ruff`, `mypy`, ou scripts do projeto.
- Rust: `cargo test`, `cargo clippy`.
- Go: `go test ./...`.
- Java/Kotlin: `./gradlew test` ou Maven.
- .NET: `dotnet test`.
- PlatformIO/embarcados: `pio run` e ambientes detectados.

Diferencie:

- executado e passou;
- executado e falhou;
- nao executado por bloqueio;
- depende de hardware, servico externo ou credencial.

## Checkpoint ECO

Ao terminar uma unidade util, atualize `.pepcodex/state.md` com no maximo cerca de 30 linhas:

```markdown
# PEP-Codex State
Objetivo: ...
Stack: ...
Status: ...
Ultima mudanca: ...
Arquivos-chave: ...
Validacao: ...
Bloqueios: ...
Proximo: ...
Decisoes: ...
```

Nao coloque segredos, logs longos, dumps, tokens, dados pessoais ou conteudo ja gravado nos arquivos.

## Protocolo completo

Abra `references/PROTOCOLO.md` apenas para:

- projeto novo complexo;
- decisao arquitetural ampla;
- definicao de papeis;
- requisitos de seguranca/entrega que nao estejam claros aqui;
- `MODE=full`.

No modo ECO, nao carregue essa referencia automaticamente.

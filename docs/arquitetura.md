# Arquitetura do PEP-Agentes

O projeto separa CLI, serviços, providers e recursos para que Codex e Claude Code compartilhem infraestrutura sem acoplamento entre suas regras específicas.

## Visão geral

```text
CLI / GUI
   ↓
pep.services.manager
   ↓
provider selecionado
   ↓
pep.core
   ↓
filesystem do projeto / escopo global
```

## Pacote `pep`

### `pep/cli.py`

Entrypoint da distribuição Python:

```toml
[project.scripts]
pep = "pep.cli:main"
```

Responsável por parsing de argumentos e despacho das operações.

### `pep/services/manager.py`

Camada de orquestração compartilhada pela CLI e pela GUI. Resolve escopos, seleciona providers e agrega resultados.

### `pep/providers/`

Implementações específicas:

- `claude.py`: gerencia `CLAUDE.md` e `/pep`;
- `codex.py`: gerencia `AGENTS.md`, skill `$pepcodex` e prompt legado opcional.

Cada provider implementa operações equivalentes: instalação, remoção, status e reparo.

### `pep/core/`

Contém componentes reutilizáveis:

- resolução de paths;
- modelos de status/operação;
- manipulação de markers;
- detecção usada pelo `doctor`;
- versão da aplicação.

### `pep/resources/`

Recursos usados em runtime:

```text
pep/resources/
├── claude/
├── codex/
└── prompts/
```

A partir da versão 1.2.1 esses arquivos são distribuídos como `package-data`. Isso elimina a dependência do antigo layout `sys.prefix/share/pep-agentes`, que podia gerar caminhos inválidos em instalações Windows com Python localizado em unidades como `D:`.

## Resolução de recursos

O helper de paths prioriza:

1. diretório temporário do PyInstaller quando a aplicação está congelada;
2. árvore de desenvolvimento quando executada do checkout;
3. `pep/resources` quando instalada como pacote Python.

O objetivo é manter a mesma API interna independentemente da origem da execução.

## Blocos gerenciados

O PEP não substitui arquivos completos quando não é necessário. `CLAUDE.md` e `AGENTS.md` usam markers para delimitar o conteúdo controlado pelo gerenciador.

Isso permite:

- atualizar apenas o bloco PEP;
- preservar instruções manuais fora dos markers;
- detectar estado atual, desatualizado, parcial ou corrompido.

## Build Windows

`scripts/build_windows.py` usa o GenPyEXE como backend preferencial. Os recursos necessários ao executável são incluídos no bundle e o runtime do PEP não depende do GenPyEXE instalado na máquina final.

## Empacotamento Python

O pacote usa `setuptools` com `pyproject.toml`.

Pontos principais:

- pacote: `pep-agentes`;
- módulo importável: `pep`;
- entrypoint: `pep`;
- recursos: `tool.setuptools.package-data`;
- versão mínima: Python 3.10.

## Princípios de manutenção

- providers devem permanecer independentes;
- lógica compartilhada deve ir para `core` ou `services`;
- recursos de runtime devem ficar dentro de `pep/resources`;
- novos providers devem reutilizar `Scope`, `Status` e `OperationResult`;
- mudanças de empacotamento devem ser validadas instalando a wheel construída, não apenas com `twine check`.

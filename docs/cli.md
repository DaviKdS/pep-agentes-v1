# Referência da CLI

A CLI `pep` centraliza operações dos providers Codex e Claude Code.

## Sintaxe

```text
pep <comando> [provider] [escopo] [opções]
```

Providers aceitos:

```text
claude
codex
all
```

## Comandos

### `install`

Instala os recursos gerenciados.

```bash
pep install all --here
pep install codex --global
pep install claude --path "C:/Projetos/App"
```

Use `--force` para sobrescrever recursos gerenciados que já existem.

### `update`

Atualiza os recursos instalados.

```bash
pep update all --here
pep update codex --global --force
```

### `status`

Mostra se cada provider está atual, ausente, parcial, desatualizado ou corrompido.

```bash
pep status all --here
pep status codex --global
```

### `doctor`

Diagnostica ferramentas e instalação.

```bash
pep doctor all --global
```

### `repair`

Reaplica recursos gerenciados quando a instalação está parcial ou desatualizada.

```bash
pep repair codex --global
```

O reparo evita sobrescrever automaticamente blocos com markers corrompidos quando isso puder destruir conteúdo manual.

### `uninstall`

Remove os recursos PEP gerenciados.

```bash
pep uninstall all --here
```

### `version`

```bash
pep version
```

## Escopos

### Diretório atual

```bash
--here
```

### Caminho específico

```bash
--path "C:/Projetos/App"
```

A opção pode ser repetida para operar sobre mais de um projeto.

### Global

```bash
--global
```

Para Claude Code, o destino global é `~/.claude`. Para Codex, o destino principal é `~/.codex`, com a skill em `~/.agents/skills/pepcodex`.

## Compatibilidade legada do Codex

```bash
pep install codex --global --legacy-prompt
```

Essa opção mantém `/prompts:pepcodex` para instalações que ainda dependem do formato legado. O uso recomendado é a skill `$pepcodex`.

## Códigos de saída

- `0`: operação concluída;
- `2`: nenhum escopo válido foi informado ou erro de uso equivalente;
- outros códigos podem ser propagados por falhas inesperadas do runtime.

## Exemplos

Instalar tudo no projeto atual:

```bash
pep install all --here
```

Atualizar Codex em dois projetos:

```bash
pep update codex --path "C:/Projetos/A" --path "C:/Projetos/B" --force
```

Validar instalação global:

```bash
pep doctor all --global
pep status all --global
```

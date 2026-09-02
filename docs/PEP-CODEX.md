# PEP-Codex v1.2.0

Port do PEP-Agentes para Codex, genérico para qualquer stack e com economia de contexto por padrão.

## Instalação recomendada

```bash
python scripts/pep.py install codex --global
```

Instala:

```text
~/.codex/AGENTS.md
~/.agents/skills/pepcodex/
```

Por projeto:

```bash
python scripts/pep.py install codex --here
```

Instala:

```text
AGENTS.md
.agents/skills/pepcodex/
```

## Uso

```text
$pepcodex corrigir o login
$pepcodex MODE=review revisar esta branch
$pepcodex MODE=plan planejar uma API
```

## Compatibilidade slash

```bash
python scripts/pep.py install codex --global --legacy-prompt
```

Use:

```text
/prompts:pepcodex MODE=review revisar esta branch
```

`/pepcodex` puro não é a sintaxe oficial de Custom Prompts do Codex.

## Status, Doctor e Repair

```bash
python scripts/pep.py status codex --global
python scripts/pep.py doctor codex --global
python scripts/pep.py repair codex --global
```

O reparo recria componentes ausentes ou desatualizados e preserva conteúdo manual fora dos markers.
Markers corrompidos não são reparados automaticamente.

## ECO

O modo padrão é `MODE=eco`: ler o mínimo necessário para agir bem, preservando qualidade, testes e
segurança.

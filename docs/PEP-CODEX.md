# PEP-Codex v1.0

Port do PEP-Agentes para Codex, generico para qualquer stack e com economia de contexto por padrao.

## Por que Skill em vez de `/pepcodex` puro

O Codex atual usa Skills como mecanismo recomendado para workflows reutilizaveis e compartilhaveis.
Custom Prompts ainda existem como compatibilidade, mas aparecem com o prefixo `/prompts:` e estao
depreciados.

Por isso o uso principal e:

```text
$pepcodex
```

Compatibilidade opcional:

```text
/prompts:pepcodex
```

Nao existe garantia oficial para um Custom Prompt chamado `/pepcodex` sem o prefixo.

## Instalacao global

```bash
python scripts/install_codex.py --global
```

Depois reinicie/abra uma sessao Codex e use:

```text
$pepcodex corrigir o login
```

## Instalacao por projeto

Dentro do projeto alvo:

```bash
python /caminho/pep-agentes-v1/scripts/install_codex.py --here
```

Isso instala:

```text
AGENTS.md
.agents/skills/pepcodex/
```

## Compatibilidade slash

```bash
python scripts/install_codex.py --global --legacy-prompt
```

Use:

```text
/prompts:pepcodex MODE=review revisar esta branch
```

## ECO

O modo padrao e `MODE=eco`.

Ele nao corta testes para poupar tokens. Ele reduz contexto desnecessario:

- checkpoint curto;
- deteccao de stack por manifests;
- busca por nomes/conteudo antes de abrir arquivos;
- limite de arquivos candidatos;
- exclusao de vendor, builds, caches, lockfiles completos e docs extensas sem necessidade;
- resposta final compacta;
- referencia completa carregada apenas quando necessaria.

Utilitario:

```bash
python codex/skills/pepcodex/tools/context_eco.py scan --task "corrigir login"
```

Checkpoint:

```bash
python codex/skills/pepcodex/tools/context_eco.py checkpoint \
  --goal "corrigir login" \
  --status "implementado" \
  --files "src/auth.ts tests/auth.test.ts" \
  --validation "npm test -- auth: passou" \
  --next "revisar integracao"
```

## Modos

```text
$pepcodex MODE=eco ...
$pepcodex MODE=plan ...
$pepcodex MODE=debug ...
$pepcodex MODE=review ...
$pepcodex MODE=full ...
$pepcodex MODE=bootstrap ...
```

## Estrutura no repositorio

```text
pep-agentes-v1/
├─ claude/                       # suporte Claude existente
├─ codex/
│  ├─ AGENTS.md
│  ├─ prompts/pepcodex.md
│  └─ skills/pepcodex/
│     ├─ SKILL.md
│     ├─ agents/openai.yaml
│     ├─ references/PROTOCOLO.md
│     └─ tools/context_eco.py
├─ scripts/
│  ├─ install_claude.py
│  └─ install_codex.py
└─ docs/PEP-CODEX.md
```

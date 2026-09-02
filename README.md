# PEP-Agentes v1.2.0

Gerenciador portátil e instalável do protocolo PEP para múltiplos agentes de desenvolvimento.

O projeto mantém Claude Code e Codex como providers independentes, mas agora compartilha um core comum
para instalação, status, diagnóstico e reparo.

## Conteúdo

```text
pep-agentes-v1/
├── pep/                         # core, providers e serviços do Manager
├── scripts/
│   ├── pep.py                   # CLI central
│   ├── pep_gui.py               # PEP-Agentes Manager
│   ├── install_claude.py        # wrapper compatível
│   ├── install_codex.py         # wrapper compatível
│   ├── build_windows.py         # build preferencial com GenPyEXE
│   └── build_app.py             # wrapper compatível do build
├── claude/
├── codex/
├── prompts/
├── docs/
├── installer/
└── tests/
```

## CLI central

Instalação via pip, depois que o pacote estiver publicado no PyPI:

```bash
python -m pip install pep-agentes
pep version
pep install all --here
```

Uso direto pelo checkout continua disponível:

```bash
python scripts/pep.py install all --here
python scripts/pep.py install codex --global
python scripts/pep.py update claude --path "C:/Projetos/App" --force
python scripts/pep.py status all --global
python scripts/pep.py doctor all --global
python scripts/pep.py repair codex --global
python scripts/pep.py uninstall claude --here
python scripts/pep.py version
```

Providers: `claude`, `codex`, `all`.

Escopos: `--here`, `--path CAMINHO`, `--global`. O Codex também aceita `--legacy-prompt` para instalar
ou remover a compatibilidade `/prompts:pepcodex`.

## Compatibilidade

Os comandos antigos continuam disponíveis:

```bash
python scripts/install_claude.py --here
python scripts/install_claude.py --global
python scripts/install_codex.py --here
python scripts/install_codex.py --global --legacy-prompt
```

Eles chamam o mesmo core usado pela CLI central e pela GUI.

## GUI

```bash
python -m pip install -r requirements-app.txt
python scripts/pep_gui.py
```

O PEP-Agentes Manager permite escolher plataforma, ação, escopo, executar Doctor/Status e copiar os
prompts de Claude ou Codex. Os logs são locais e não devem conter tokens, senhas ou chaves.

## Build Windows

O backend preferencial é o GenPyEXE.

```bash
python -m pip install -r requirements-app.txt
python -m pip install -r requirements-build.txt
python scripts/build_windows.py
```

O script usa `genpyexeks.build` apenas no processo de build e inclui `claude/`, `codex/`, `prompts/`
e `docs/` como recursos do executável. O runtime do PEP Manager não depende de GenPyEXE.

Artefatos esperados em `dist/`:

```text
PEP-Agentes-1.2.0-Portable-x64.exe
PEP-Agentes-1.2.0-Setup-x64.exe
PEP-Agentes-1.2.0-SHA256SUMS.txt
```

## Releases e pacote Python

Tags `v*` disparam:

- build Windows com GitHub Release e assets anexados;
- build do pacote Python (`sdist` e `wheel`);
- publicação no PyPI via Trusted Publishing, quando o projeto `pep-agentes` estiver configurado no PyPI.

Build local do pacote:

```bash
python -m pip install build twine
python -m build --outdir python-dist
python -m twine check python-dist/*
```

## Codex

Uso recomendado após instalar:

```text
$pepcodex corrigir o login
$pepcodex MODE=review revisar esta branch
```

Compatibilidade opcional:

```text
/prompts:pepcodex MODE=review revisar esta branch
```

## Validação

```bash
python -m compileall -q scripts pep claude codex
python scripts/validate_package.py
pytest
```

## Segurança

Os scripts são locais: não coletam dados pessoais, não enviam projetos a servidores externos e não
leem credenciais desnecessárias. Alterações em `CLAUDE.md` e `AGENTS.md` usam marcadores gerenciados
para preservar conteúdo manual fora do bloco PEP.

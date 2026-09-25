# PEP-Agentes

[![PyPI](https://img.shields.io/pypi/v/pep-agentes)](https://pypi.org/project/pep-agentes/)
[![Python](https://img.shields.io/pypi/pyversions/pep-agentes)](https://pypi.org/project/pep-agentes/)
[![License](https://img.shields.io/github/license/DaviKdS/pep-agentes-v1)](LICENSE)
[![CI](https://github.com/DaviKdS/pep-agentes-v1/actions/workflows/ci.yml/badge.svg)](https://github.com/DaviKdS/pep-agentes-v1/actions/workflows/ci.yml)

**Gerencie o protocolo PEP para Codex e Claude Code por CLI, interface gráfica ou executável Windows.**

O PEP-Agentes centraliza instalação, atualização, diagnóstico, reparo e remoção das instruções PEP em projetos locais ou no escopo global do usuário. O mesmo core atende múltiplos providers e mantém recursos empacotados dentro do próprio pacote Python para funcionar de forma consistente em Windows, Linux, `venv`, PyPI e instalação direta pelo GitHub.

```bash
python -m pip install pep-agentes
pep version
pep install all --here
```

---

## Índice

- [Por que existe](#por-que-existe)
- [Instalação](#instalação)
- [Uso rápido](#uso-rápido)
- [Providers](#providers)
- [Escopos](#escopos)
- [Referência da CLI](#referência-da-cli)
- [Interface gráfica](#interface-gráfica)
- [Arquitetura](#arquitetura)
- [Build para Windows](#build-para-windows)
- [Release e PyPI](#release-e-pypi)
- [Documentação](#documentação)
- [Solução de problemas](#solução-de-problemas)
- [Segurança e privacidade](#segurança-e-privacidade)
- [Licença e autoria](#licença-e-autoria)

---

## Por que existe

Manter instruções de agentes em vários projetos tende a gerar cópias divergentes, arquivos manuais fora de sincronia e configurações diferentes entre Codex e Claude Code.

O PEP-Agentes resolve isso com um gerenciador único que:

- instala e atualiza blocos gerenciados sem sobrescrever conteúdo manual fora dos marcadores;
- mantém providers independentes para Codex e Claude Code;
- oferece `status`, `doctor`, `repair` e `uninstall` pelo mesmo core;
- suporta instalação local por projeto ou global;
- disponibiliza CLI, GUI e artefatos Windows;
- empacota os recursos necessários dentro da wheel, evitando dependência de caminhos externos como `share/pep-agentes`.

---

## Instalação

### PyPI

```bash
python -m pip install pep-agentes
```

Confirme a instalação:

```bash
pep version
```

### GitHub

Versão atual da branch principal:

```bash
python -m pip install "git+https://github.com/DaviKdS/pep-agentes-v1.git"
```

Versão específica:

```bash
python -m pip install "git+https://github.com/DaviKdS/pep-agentes-v1.git@v1.2.1"
```

### Checkout local

```bash
git clone https://github.com/DaviKdS/pep-agentes-v1.git
cd pep-agentes-v1
python -m pip install -e .
```

Mais detalhes: [docs/instalacao.md](docs/instalacao.md).

---

## Uso rápido

Instalar Codex e Claude Code no projeto atual:

```bash
pep install all --here
```

Verificar o estado:

```bash
pep status all --here
```

Diagnosticar instalação global:

```bash
pep doctor all --global
```

Atualizar e sobrescrever apenas os arquivos gerenciados:

```bash
pep update all --here --force
```

Reparar um provider:

```bash
pep repair codex --global
```

Remover:

```bash
pep uninstall all --here
```

---

## Providers

| Provider | Arquivos principais | Uso recomendado |
|---|---|---|
| `codex` | `AGENTS.md`, skill `$pepcodex`, prompt legado opcional | Codex em projetos locais ou configuração global |
| `claude` | `CLAUDE.md`, comando `/pep` | Claude Code em projeto ou escopo global |
| `all` | aplica ambos | ambientes que usam os dois providers |

### Codex

Após a instalação:

```text
$pepcodex corrigir o login
$pepcodex MODE=review revisar esta branch
$pepcodex MODE=debug investigar o erro 500
```

Compatibilidade opcional com prompt legado:

```bash
pep install codex --global --legacy-prompt
```

### Claude Code

```bash
pep install claude --here
```

O PEP mantém o bloco gerenciado em `CLAUDE.md` e instala o comando `/pep` no escopo correspondente.

---

## Escopos

| Escopo | Exemplo | Efeito |
|---|---|---|
| projeto atual | `--here` | usa o diretório atual |
| projeto específico | `--path "C:/Projetos/App"` | aplica em um caminho informado |
| global | `--global` | usa os diretórios globais do provider |

Exemplo:

```bash
pep install codex --path "C:/Projetos/MeuApp"
```

---

## Referência da CLI

```text
pep install [claude|codex|all]    instala recursos PEP
pep update [claude|codex|all]     atualiza recursos gerenciados
pep uninstall [provider]           remove recursos gerenciados
pep repair [provider]              repara instalação parcial/desatualizada
pep status [provider]              mostra o estado atual
pep doctor [provider]              diagnostica ferramentas e instalação
pep version                        mostra a versão instalada
```

Opções de escopo:

```text
--here
--path CAMINHO
--global
--legacy-prompt
--force
```

Referência detalhada: [docs/cli.md](docs/cli.md).

---

## Interface gráfica

Instale as dependências opcionais:

```bash
python -m pip install "pep-agentes[app]"
```

No checkout do repositório:

```bash
python scripts/pep_gui.py
```

O PEP-Agentes Manager permite selecionar provider, ação e escopo, além de executar diagnóstico e consultar o estado da instalação sem editar arquivos manualmente.

---

## Arquitetura

```text
pep-agentes-v1/
├── pep/
│   ├── cli.py
│   ├── core/
│   ├── providers/
│   ├── services/
│   └── resources/
│       ├── claude/
│       ├── codex/
│       └── prompts/
├── scripts/
├── docs/
├── installer/
├── tests/
├── pyproject.toml
└── genpyexe.toml
```

### Fluxo interno

```text
CLI / GUI
   ↓
services.manager
   ↓
provider selecionado
   ↓
core de paths / markers / models
   ↓
arquivos do projeto ou escopo global
```

Os recursos de runtime ficam em `pep/resources/` e são distribuídos como `package-data`. Essa abordagem evita caminhos dependentes de `sys.prefix/share` e torna a wheel mais previsível entre plataformas.

Detalhes: [docs/arquitetura.md](docs/arquitetura.md).

---

## Build para Windows

O backend preferencial é o [GenPyEXE](https://github.com/DaviKdS/GenPyEXE).

```bash
python -m pip install -r requirements-app.txt
python -m pip install -r requirements-build.txt
python scripts/build_windows.py
```

Artefatos esperados:

```text
PEP-Agentes-1.2.1-Portable-x64.exe
pep-agentes-1.2.1-setup-x64.exe
PEP-Agentes-1.2.1-SHA256SUMS.txt
```

O GenPyEXE é dependência de build, não de runtime.

---

## Release e PyPI

Tags `v*` acionam o workflow de release.

Fluxo protegido:

```text
tag v1.2.1
   ↓
build Windows
   ↓
build da wheel
   ↓
instalação real da wheel no Windows
   ↓
GitHub Release + artefatos
   ↓
publish-pypi aguarda build-windows
   ↓
build + instalação real da wheel no Linux
   ↓
publicação no PyPI
```

A publicação no PyPI depende explicitamente da validação do job Windows. Se a instalação da wheel falhar no Windows, o job de publicação não é executado.

Build local do pacote:

```bash
python -m pip install build twine
python -m build --outdir python-dist
python -m twine check python-dist/*
```

---

## Documentação

| Documento | Conteúdo |
|---|---|
| [docs/instalacao.md](docs/instalacao.md) | instalação por PyPI, GitHub, checkout e validação |
| [docs/cli.md](docs/cli.md) | comandos, providers, escopos e exemplos |
| [docs/arquitetura.md](docs/arquitetura.md) | core, providers, recursos e fluxo interno |
| [docs/release.md](docs/release.md) | build, CI, GitHub Release e publicação no PyPI |
| [docs/solucao-de-problemas.md](docs/solucao-de-problemas.md) | erros comuns e diagnóstico |
| [docs/PEP-CODEX.md](docs/PEP-CODEX.md) | uso específico do provider Codex |
| [docs/COMO_FOI_GERADO.md](docs/COMO_FOI_GERADO.md) | histórico técnico do projeto |

---

## Solução de problemas

### `pep` não é reconhecido

Descubra a pasta de scripts do Python:

```bash
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
```

Verifique se o launcher foi criado nessa pasta e se ela está no `PATH`.

### Wheel tentando instalar em `D:share\...`

Esse problema existia na versão 1.2.0 por causa do uso de `data-files`. A partir da 1.2.1 os recursos ficam dentro do pacote `pep/resources` e são distribuídos via `package-data`.

### Diagnóstico completo

```bash
pep doctor all --global
pep status all --global
```

Mais casos: [docs/solucao-de-problemas.md](docs/solucao-de-problemas.md).

---

## Segurança e privacidade

- não armazena tokens, senhas ou chaves;
- não envia o conteúdo dos projetos para um backend próprio;
- preserva conteúdo manual fora dos blocos PEP gerenciados;
- usa arquivos locais e caminhos explícitos;
- GitHub Actions usa Trusted Publishing para publicação no PyPI;
- a release só publica o pacote após validações reais de instalação.

Consulte também [SECURITY.md](SECURITY.md).

---

## Licença e autoria

Licenciado sob **Apache License 2.0**. Consulte [LICENSE](LICENSE).

Autor e mantenedor: **Davi Kasmirski dos Santos / DaviKdS**.

# Release, CI e publicação

Este documento descreve o fluxo oficial de entrega do PEP-Agentes.

## Objetivo

Uma versão só deve ser publicada quando o pacote Python for realmente instalável nos ambientes validados. `twine check` verifica metadados, mas não substitui um teste de instalação da wheel.

## Fluxo de release

```text
criar tag vX.Y.Z
   ↓
job build-windows
   ├─ build dos artefatos Windows
   ├─ build da wheel/sdist
   ├─ twine check
   ├─ instalação da wheel em venv Windows
   ├─ execução de pep version
   └─ GitHub Release
   ↓
job publish-pypi (needs: build-windows)
   ├─ build da wheel/sdist no Linux
   ├─ twine check
   ├─ instalação da wheel em venv Linux
   ├─ execução de pep version
   └─ Trusted Publishing no PyPI
```

## Gate de publicação

O job `publish-pypi` possui dependência explícita:

```yaml
publish-pypi:
  needs: build-windows
```

Assim, uma falha no build ou no teste de instalação Windows bloqueia a publicação no PyPI.

Esse gate é importante porque versões publicadas no PyPI são imutáveis: corrigir uma release exige publicar uma nova versão.

## Criando uma release

Antes de criar a tag:

1. atualize a versão em `pyproject.toml`;
2. atualize `pep/core/version.py`;
3. atualize metadados de build aplicáveis, como `genpyexe.toml`;
4. ajuste testes que validam a versão;
5. documente as mudanças em `CHANGELOG.md`;
6. abra PR e aguarde o CI passar.

Depois do merge:

```bash
git checkout main
git pull
git tag v1.2.1
git push origin v1.2.1
```

A tag inicia `.github/workflows/release.yml`.

## Validação local do pacote

```bash
python -m pip install --upgrade build twine
python -m build --outdir python-dist
python -m twine check python-dist/*
```

Teste em uma venv limpa:

### Windows

```cmd
python -m venv .venv-wheel-test
.venv-wheel-test\Scripts\python.exe -m pip install python-dist\pep_agentes-*.whl
.venv-wheel-test\Scripts\pep.exe version
```

### Linux/macOS

```bash
python -m venv .venv-wheel-test
.venv-wheel-test/bin/python -m pip install python-dist/pep_agentes-*.whl
.venv-wheel-test/bin/pep version
```

## GitHub Release

A release anexa:

- executável portátil Windows;
- instalador Windows;
- checksums quando gerados;
- wheel Python;
- sdist Python.

## PyPI

A publicação usa Trusted Publishing via GitHub Actions. Não é necessário armazenar um token PyPI no repositório quando o ambiente do PyPI estiver configurado corretamente.

## Falhas comuns

### Windows passou, Linux falhou

O job de publicação para antes do upload no PyPI. Corrija a branch, gere uma nova tag somente quando a versão ainda não tiver sido publicada.

### Windows falhou

`publish-pypi` é bloqueado por `needs: build-windows`.

### Versão já existe no PyPI

Não tente substituir a distribuição existente. Incrementar a versão é o caminho correto.

# Instalação do PEP-Agentes

Este guia cobre instalação por PyPI, GitHub, checkout local e validação do ambiente.

## Requisitos

- Python 3.10 ou superior;
- `pip` atualizado;
- Git apenas para instalação diretamente do repositório;
- Windows, Linux ou macOS para a CLI Python;
- Windows 64 bits para os artefatos executáveis publicados em Releases.

## Instalação pelo PyPI

```bash
python -m pip install pep-agentes
```

Valide:

```bash
pep version
```

## Instalação pelo GitHub

Branch principal:

```bash
python -m pip install "git+https://github.com/DaviKdS/pep-agentes-v1.git"
```

Tag específica:

```bash
python -m pip install "git+https://github.com/DaviKdS/pep-agentes-v1.git@v1.2.1"
```

## Instalação para desenvolvimento

```bash
git clone https://github.com/DaviKdS/pep-agentes-v1.git
cd pep-agentes-v1
python -m pip install -e .
```

Dependências opcionais da GUI:

```bash
python -m pip install "pep-agentes[app]"
```

Dependências de build:

```bash
python -m pip install "pep-agentes[build]"
```

## Verificação do launcher

No Windows:

```cmd
where pep
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
```

No Linux/macOS:

```bash
which pep
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
```

Se o módulo estiver instalado mas o launcher não estiver acessível, confirme se o diretório retornado por `sysconfig.get_path('scripts')` está no `PATH`.

## Validação funcional

```bash
pep version
pep doctor all --global
```

Teste em um projeto temporário:

```bash
mkdir pep-test
cd pep-test
pep install all --here
pep status all --here
pep uninstall all --here
```

## Atualização

```bash
python -m pip install --upgrade pep-agentes
```

## Remoção

```bash
python -m pip uninstall pep-agentes
```

A remoção do pacote Python não remove automaticamente configurações PEP já instaladas em projetos. Para isso, execute `pep uninstall` antes de desinstalar o pacote.

# Solução de problemas

Guia de diagnóstico para instalação, CLI, providers e empacotamento.

## `pep` não é reconhecido

Confirme se o pacote está instalado:

```bash
python -m pip show pep-agentes
```

Veja onde os scripts são instalados:

```bash
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
```

No Windows:

```cmd
where pep
```

No Linux/macOS:

```bash
which pep
```

Se o launcher existir mas não for encontrado, adicione a pasta de scripts ao `PATH`.

## O módulo funciona, mas `pep.exe` não existe

Teste o entrypoint diretamente:

```bash
python -c "from pep.cli import main; main(['version'])"
```

Confira o metadata:

```bash
python -c "import importlib.metadata as m; print(list(m.distribution('pep-agentes').entry_points))"
```

Deve existir um `console_scripts` chamado `pep` apontando para `pep.cli:main`.

## Erro `D:share\pep-agentes\...`

Sintoma observado na versão 1.2.0:

```text
The wheel ... has a file 'D:share\pep-agentes\...' trying to install outside the target directory 'D:'
```

Causa: recursos distribuídos por `data-files` eram resolvidos incorretamente em alguns layouts de Python no Windows.

Correção aplicada na 1.2.1:

- recursos movidos para `pep/resources`;
- `data-files` removido;
- uso de `package-data`;
- resolução de recursos adaptada para pacote instalado, source e PyInstaller;
- teste real de instalação da wheel no Windows antes de publicar no PyPI.

Atualize:

```bash
python -m pip install --upgrade pep-agentes
```

## `Host key verification failed` ao instalar via SSH

Isso é uma configuração SSH do GitHub, não um erro do PEP-Agentes.

Use HTTPS se não precisar de SSH:

```bash
python -m pip install "git+https://github.com/DaviKdS/pep-agentes-v1.git"
```

## URL GitHub copiada em formato Markdown

Errado:

```text
git+[https://github.com/...](https://github.com/...)
```

Correto:

```text
git+https://github.com/DaviKdS/pep-agentes-v1.git
```

## `Nenhum alvo selecionado`

A CLI precisa de um escopo para operações que atuam em arquivos.

Use um destes:

```bash
--here
--path "C:/Projetos/App"
--global
```

Exemplo:

```bash
pep status all --global
```

## Instalação parcial ou desatualizada

```bash
pep status all --here
pep repair all --here
```

Se quiser sobrescrever recursos gerenciados:

```bash
pep update all --here --force
```

## Markers corrompidos

Quando os delimitadores gerenciados foram editados de forma incompatível, o reparo automático pode ser cancelado para preservar conteúdo manual.

Faça backup do arquivo, corrija os markers ou remova conscientemente o bloco inválido antes de reinstalar.

## Diagnóstico recomendado

```bash
pep version
pep doctor all --global
pep status all --global
```

Para problemas de `pip`:

```bash
python --version
python -m pip --version
python -m pip show pep-agentes
python -c "import sys; print(sys.executable)"
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
```

## Reportando um bug

Ao abrir uma issue, informe:

- sistema operacional;
- versão do Python;
- versão do `pip`;
- versão do PEP-Agentes;
- comando executado;
- saída completa do erro sem credenciais ou dados sensíveis;
- se a instalação veio do PyPI, GitHub ou checkout local.

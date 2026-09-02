# Como usar o PEP-Agentes v1.2.0

## Instalar pela CLI central

Via pip, depois da publicação no PyPI:

```bash
python -m pip install pep-agentes
pep install all --here
```

Direto pelo repositório:

```bash
python scripts/pep.py install all --here
python scripts/pep.py install all --global
python scripts/pep.py doctor all --global
```

Para um provider específico:

```bash
python scripts/pep.py install claude --path "C:/Projetos/App"
python scripts/pep.py install codex --global --legacy-prompt
```

## Instalar pela GUI

```bash
python -m pip install -r requirements-app.txt
python scripts/pep_gui.py
```

Escolha plataforma, ação e escopo, depois clique em `Executar`.

## Usar no Claude Code

Depois da instalação, o `CLAUDE.md` gerenciado fica ativo no escopo escolhido. O comando `/pep`
também é instalado.

## Usar no Codex

Depois da instalação:

```text
$pepcodex sua tarefa aqui
```

Compatibilidade opcional:

```text
/prompts:pepcodex sua tarefa aqui
```

## Scripts antigos

Continuam válidos:

```bash
python scripts/install_claude.py --here
python scripts/install_codex.py --global
```

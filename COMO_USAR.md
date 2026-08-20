# Como usar o PEP-Agentes v1.0

## Ativação completa

Cole o conteúdo de `prompts/pep-agentes-completo.txt` no começo de qualquer novo chat.

## Ativação curta

Cole o conteúdo de `prompts/pep-agentes-curto.txt` quando quiser uma ativação mais rápida.

## Definir desenvolvedor

Você pode complementar o prompt com:

```text
[DESENVOLVEDOR]
Nome: Davi
Nível: Pleno
Stack: Python, TypeScript, React, FastAPI
Frameworks: React, FastAPI, Tailwind
Banco de Dados: PostgreSQL
Estilo: Clean Code, SOLID, pragmático
Arquitetura: Modular monolith primeiro, microserviços só se fizer sentido
Idioma: pt-BR
Foco: inovação viável
```

## Exemplo de pedido

```text
Usando o PEP-Agentes v1.0, crie um site para barbeiro com landing page, catálogo de serviços, botão de WhatsApp, agendamento e área administrativa simples.
```

## O que esperar

O assistente deve organizar a resposta com agentes dinâmicos, arquitetura, estrutura de arquivos, código, comandos, segurança, melhorias futuras e prompt para Codex.

## Codex

Para usar o PEP no Codex, instale a skill:

```bash
python scripts/install_codex.py --global
```

Depois use:

```text
$pepcodex sua tarefa aqui
```

O modo econômico já é padrão. Para compatibilidade com Custom Prompts:

```bash
python scripts/install_codex.py --global --legacy-prompt
```

Então use `/prompts:pepcodex`. O comando `/pepcodex` puro não é a sintaxe oficial atual do Codex.

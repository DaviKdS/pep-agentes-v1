---
description: Ativa PEP-Codex em modo economico para qualquer projeto
argument-hint: [MODE=eco|plan|review|debug|full|bootstrap] [pedido]
---

Aplique o workflow da Skill `$pepcodex` ao pedido abaixo.

- Se MODE nao estiver explicito, use `MODE=eco`.
- Detecte a stack pelo repositorio antes de decidir arquitetura ou comandos.
- Preserve mudancas nao relacionadas.
- Use o menor contexto suficiente e valide com os comandos nativos do projeto.
- Diferencie teste local de validacao que depende de hardware, servico externo ou credencial.
- Nao exponha segredos, nao invente resultados e preserve licencas/creditos.

Pedido: $ARGUMENTS

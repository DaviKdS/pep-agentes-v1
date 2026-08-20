# PEP-Codex v1.0 - protocolo completo

Adaptacao do PEP-Agentes v1.0 para Codex. Use este documento como referencia de apoio, nao como
texto obrigatorio para toda tarefa. O `SKILL.md` e a fonte operacional curta.

## Objetivo

Atuar sobre sistemas, sites, APIs, automacoes, apps, firmware, dados, IA, infraestrutura e
documentacao com qualidade profissional, seguranca e economia de contexto.

## Principios

1. Segurança, legalidade e privacidade vencem conveniencia.
2. O repositorio existente ensina a stack, os comandos e o estilo.
3. Contexto deve ser carregado sob demanda.
4. Alteracoes pequenas e validadas sao melhores que refatoracoes amplas sem necessidade.
5. Toda entrega deve separar fato executado de inferencia ou pendencia.

## Fluxo padrao

```text
pedido
  -> detectar stack e estado git
  -> ler checkpoint ECO
  -> localizar arquivos relevantes
  -> selecionar papeis necessarios
  -> planejar proporcionalmente
  -> implementar
  -> validar
  -> revisar diff
  -> atualizar checkpoint ECO
  -> responder curto
```

## Papeis dinamicos

Escolha os papeis de acordo com o pedido:

- Arquiteto: fronteiras, contratos, dependencias e trade-offs.
- Backend/API: rotas, servicos, filas, autenticacao e autorizacao.
- Frontend/UI: componentes, estado, acessibilidade, responsividade e browser QA.
- Mobile: navegacao, storage, permissao, offline e distribuicao.
- Embedded/Firmware: HAL, drivers, RTOS, memoria, pinagem e build para placa.
- Banco de Dados: schema, migracoes, indices, transacoes e consultas.
- Seguranca: segredos, validacao, autorizacao, supply chain e logs.
- QA/Testes: cobertura proporcional, regressao, fixtures e verificacao manual.
- DevOps: CI, build, release, variaveis e ambientes.
- IA/LLM: prompts, ferramentas, avaliacao, guardrails, custos e privacidade.
- Documentacao: uso, manutencao, runbooks e notas de mudanca.

Use apenas os papeis que melhoram a tarefa atual.

## Modos

### eco

Padrao. Otimiza contexto com checkpoint curto, manifests, busca direcionada e leitura minima.
Nao reduz testes nem pula validacao para economizar tokens.

### plan

Use quando a tarefa for ampla, ambigua ou de alto risco. Entregue plano curto com arquivos
provaveis, validacoes e riscos. Se o usuario ja pediu execucao e o escopo estiver claro, execute.

### review

Priorize bugs, regressao, riscos e testes ausentes. Findings primeiro, ordenados por severidade,
com referencias a arquivo/linha quando possivel.

### debug

Reproduza ou caracterize o erro, isole a causa, aplique a menor correcao e valide. Se nao puder
reproduzir, documente o bloqueio e a melhor evidencia local.

### bootstrap

Para projeto novo, entregue estrutura executavel com README, `.env.example`, testes minimos,
comandos claros e CI quando fizer sentido. Evite landing page quando o pedido for app/ferramenta.

### full

Use para auditoria, arquitetura, migracoes e decisoes transversais. Pode carregar mais docs,
mapear dependencias e propor etapas.

## Deteccao de stack

Sinais comuns:

- JavaScript/TypeScript: `package.json`, `tsconfig.json`, `vite.config.*`, `next.config.*`.
- Python: `pyproject.toml`, `requirements.txt`, `setup.py`, `Pipfile`.
- Rust: `Cargo.toml`.
- Go: `go.mod`.
- Java/Kotlin: `pom.xml`, `build.gradle`, `settings.gradle`.
- .NET: `*.csproj`, `*.sln`.
- PHP: `composer.json`.
- Ruby: `Gemfile`.
- Flutter/Dart: `pubspec.yaml`.
- Swift/iOS: `Package.swift`, `.xcodeproj`, `.xcworkspace`.
- C/C++: `CMakeLists.txt`, `Makefile`, `meson.build`.
- Embedded: `platformio.ini`, `sdkconfig`, ESP-IDF/CMake, Arduino.
- Infra: `Dockerfile`, `compose.yml`, `docker-compose.yml`, Terraform, Kubernetes, GitHub Actions.
- Monorepo: `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, Yarn/NPM workspaces.

## Seguranca

- Nunca grave credenciais reais.
- Trate logs e dumps como potencialmente sensiveis.
- Use variaveis de ambiente documentadas em `.env.example`.
- Nao amplie permissoes ou escopo sem necessidade.
- Em autenticacao/autorizacao, prefira falha fechada e testes de regressao.
- Para scripts de instalacao, deixe claro o que e lido, escrito e removido.

## Quando expandir contexto

Expanda contexto se:

- a interface publica estiver incerta;
- o erro atravessar modulos;
- testes indicarem comportamento inesperado;
- houver migracao, seguranca, concorrencia ou dados;
- a decisao tiver impacto arquitetural;
- a validacao local divergir do objetivo do usuario.

## Checkpoint ECO

O checkpoint deve ajudar a proxima tarefa sem virar diario. Maximo recomendado:

```markdown
# PEP-Codex State
Objetivo:
Stack:
Status:
Ultima mudanca:
Arquivos-chave:
Validacao:
Bloqueios:
Proximo:
Decisoes:
```

Atualize apenas quando houver uma unidade de trabalho concluida ou uma decisao importante.

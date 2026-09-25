# Instrucoes do projeto (Codex)

Bloco PEP-Codex gerenciado por scripts/install_codex.py.

<!-- PEP-CODEX:START (gerenciado por scripts/install_codex.py) -->
## PEP-Codex v1.0

Em pedidos tecnicos sobre sistemas, sites, APIs, automacoes, agentes, firmware, apps,
infraestrutura, revisoes ou depuracao, siga este protocolo de forma proporcional ao risco.

### Regras gerais

1. Nunca gerar conteudo ilegal, malicioso, fraudulento ou invasivo.
2. Nunca expor, inventar ou armazenar credenciais, tokens, senhas, chaves ou dados pessoais.
3. Use `.env.example` para variaveis sensiveis; nunca coloque segredos reais no codigo.
4. Nao afirme que comandos foram executados se nao foram.
5. Nao invente bibliotecas, APIs, resultados de teste ou limitacoes.
6. Preserve licencas, creditos e autoria legitimos.
7. Explique estrategia, arquitetura e decisoes com evidencias objetivas, sem raciocinio interno.

### Modo ECO

Economize contexto antes de economizar qualidade:

1. Leia o pedido atual e o checkpoint curto em `.pepcodex/state.md`, se existir.
2. Leia `AGENTS.md` aplicaveis e manifests/configs suficientes para identificar a stack.
3. Busque arquivos por nome, conteudo, erro ou diff antes de abrir muitos arquivos.
4. Ignore vendor, caches, builds, lockfiles completos, assets grandes e docs extensas sem motivo.
5. Abra apenas os arquivos diretamente ligados ao pedido, mais testes, tipos e contratos.
6. Expanda para modo completo quando houver risco arquitetural, seguranca, concorrencia, migracao,
   bug transversal ou incerteza sobre interfaces publicas.

### Papeis dinamicos

Escolha somente os papeis necessarios ao trabalho atual: Arquiteto, Backend, Frontend, Mobile,
Embedded/Firmware, Banco de Dados, Seguranca, QA, DevOps, Documentacao, IA/LLM, MLOps ou outro
papel especifico. Nao anuncie um grupo grande de agentes quando dois papeis resolvem.

### Execucao

1. Inspecione o estado local antes de editar.
2. Preserve mudancas nao relacionadas.
3. Prefira alteracoes pequenas, testaveis e reversiveis.
4. Use a stack e os comandos nativos do repositorio.
5. Rode testes/builds aplicaveis quando o ambiente permitir.
6. Diferencie claramente validacao local de validacao que depende de hardware, servico externo ou credencial.

### Entrega

Para mudancas em codigo existente, responda de forma compacta:

- o que mudou;
- validacoes executadas;
- riscos ou bloqueios;
- proximo passo somente se util.

Para projeto novo, produza arquitetura, estrutura, arquivos, comandos, testes, seguranca,
publicacao e prompt de continuacao conforme o pedido.
<!-- PEP-CODEX:END -->

# Como este pacote foi gerado

Este pacote foi montado como um artefato portátil contendo:

- um prompt completo de ativação do PEP-Agentes v1.0;
- uma versão curta do prompt;
- documentação de uso;
- scripts locais e auditáveis para regenerar PDF, validar estrutura e criar ZIP;
- instruções de publicação no GitHub;
- orientações de segurança e privacidade.

## Processo técnico

1. A estrutura de pastas foi definida para separar prompts, documentação e scripts.
2. O prompt completo foi salvo em `prompts/pep-agentes-completo.txt`.
3. O prompt curto foi salvo em `prompts/pep-agentes-curto.txt`.
4. A documentação textual foi salva em Markdown.
5. O PDF foi gerado a partir de conteúdo textual objetivo.
6. O manifesto foi criado com a lista de arquivos e metadados básicos.
7. O pacote ZIP foi gerado localmente com `scripts/build_zip.py`.

## Limites

Este documento não inclui raciocínio interno oculto, credenciais, dados pessoais, tokens, chaves privadas ou informações sensíveis do ambiente.

## Como modificar

Edite os arquivos em `prompts/` e depois rode:

```bash
python scripts/generate_documentation_pdf.py
python scripts/validate_package.py
python scripts/build_zip.py
```

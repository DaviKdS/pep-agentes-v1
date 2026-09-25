# Changelog

## 1.2.1

- Corrige a instalação da wheel no Windows removendo `data-files` externos que podiam gerar caminhos inválidos como `D:share\pep-agentes\...`.
- Move os recursos de runtime para `pep/resources` e passa a empacotá-los como `package-data`.
- Ajusta a resolução de recursos para funcionar em instalação via wheel/PyPI e manter compatibilidade com PyInstaller e árvore de desenvolvimento.
- Adiciona teste de instalação real da wheel no workflow de release antes da publicação no PyPI.
- Torna o nome e os comandos da GitHub Release baseados na tag atual.

## 1.2.0

- Adiciona core compartilhado `pep/` para markers, providers, status, doctor e operações.
- Adiciona CLI central `scripts/pep.py`.
- Adiciona pacote Python `pep-agentes` com entrypoint `pep`.
- Transforma a GUI em PEP-Agentes Manager multi-provider.
- Mantém wrappers compatíveis `install_claude.py` e `install_codex.py`.
- Adiciona build preferencial com GenPyEXE em `scripts/build_windows.py`.
- Adiciona GitHub Release, pacote Python, testes automatizados e workflows de CI/release.

## 1.1

- Adiciona suporte inicial a PEP-Codex e skill `$pepcodex`.

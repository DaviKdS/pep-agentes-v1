#!/usr/bin/env bash
set -euo pipefail

# Publica o projeto no GitHub usando Git nativo.
# Uso:
#   ./scripts/publish_github.sh https://github.com/seu-usuario/seu-repositorio.git
#
# Este script não cria repositório remoto. Crie antes no GitHub ou use GitHub CLI.

REPO_URL="${1:-}"

if [[ -z "$REPO_URL" ]]; then
  echo "Informe a URL do repositório remoto."
  echo "Exemplo: ./scripts/publish_github.sh https://github.com/seu-usuario/seu-repositorio.git"
  exit 2
fi

git init
git add .
git commit -m "Initial commit"
git branch -M main

git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
git push -u origin main

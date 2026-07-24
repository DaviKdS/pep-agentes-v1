param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl
)

# Publica o projeto no GitHub usando Git nativo.
# Uso:
#   powershell -ExecutionPolicy Bypass -File scripts/publish_github.ps1 -RepoUrl "https://github.com/seu-usuario/seu-repositorio.git"

if ([string]::IsNullOrWhiteSpace($RepoUrl)) {
    Write-Error "Informe a URL do repositório remoto."
    exit 2
}

git init
git add .
git commit -m "Initial commit"
git branch -M main

git remote remove origin 2>$null
git remote add origin $RepoUrl
git push -u origin main

# Remove o PEP-Agentes (GUI) instalado por install_app.ps1.
#
# Uso:
#   powershell -ExecutionPolicy Bypass -File installer/uninstall_app.ps1

$ErrorActionPreference = "SilentlyContinue"

$AppName = "PEP-Agentes"
$InstallDir = Join-Path $env:LOCALAPPDATA "Programs\$AppName"

# Atalhos
$desktop = [Environment]::GetFolderPath("Desktop")
Remove-Item (Join-Path $desktop "$AppName.lnk") -Force
$startMenu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\$AppName"
Remove-Item $startMenu -Recurse -Force

# Arquivos
Remove-Item $InstallDir -Recurse -Force

# Registro
Remove-Item "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppName" -Recurse -Force

Write-Host "PEP-Agentes removido."

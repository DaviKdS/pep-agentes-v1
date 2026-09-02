# Instala o PEP-Agentes (GUI) no PC do usuario atual, sem privilegios de admin.
# Copia dist/PEP-Agentes.exe para %LOCALAPPDATA%\Programs\PEP-Agentes e cria atalhos
# na Area de Trabalho e no Menu Iniciar.
#
# Uso:
#   powershell -ExecutionPolicy Bypass -File installer/install_app.ps1
#
# Local-only: nao envia dados nem le credenciais.

$ErrorActionPreference = "Stop"

$AppName = "PEP-Agentes"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ExeSource = Join-Path $ProjectRoot "dist\$AppName.exe"

if (-not (Test-Path $ExeSource)) {
    Write-Error "Executavel nao encontrado: $ExeSource`nRode antes: D:\python.exe scripts\build_app.py"
}

$InstallDir = Join-Path $env:LOCALAPPDATA "Programs\$AppName"
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
$ExeTarget = Join-Path $InstallDir "$AppName.exe"
Copy-Item -Path $ExeSource -Destination $ExeTarget -Force
Write-Host "Copiado para: $ExeTarget"

function New-Shortcut([string]$LinkPath, [string]$TargetPath, [string]$WorkDir) {
    $shell = New-Object -ComObject WScript.Shell
    $sc = $shell.CreateShortcut($LinkPath)
    $sc.TargetPath = $TargetPath
    $sc.WorkingDirectory = $WorkDir
    $sc.Description = "PEP-Agentes v1.2.0 - Manager Claude Code e Codex"
    $sc.Save()
}

# Atalho na Area de Trabalho
$desktop = [Environment]::GetFolderPath("Desktop")
New-Shortcut (Join-Path $desktop "$AppName.lnk") $ExeTarget $InstallDir
Write-Host "Atalho criado na Area de Trabalho."

# Atalho no Menu Iniciar
$startMenu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\$AppName"
New-Item -ItemType Directory -Force -Path $startMenu | Out-Null
New-Shortcut (Join-Path $startMenu "$AppName.lnk") $ExeTarget $InstallDir
Write-Host "Atalho criado no Menu Iniciar."

# Registro de desinstalacao (Adicionar/Remover Programas)
$uninstallScript = Join-Path $ProjectRoot "installer\uninstall_app.ps1"
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppName"
New-Item -Path $regPath -Force | Out-Null
Set-ItemProperty -Path $regPath -Name "DisplayName" -Value "PEP-Agentes v1.2.0"
Set-ItemProperty -Path $regPath -Name "DisplayVersion" -Value "1.2.0"
Set-ItemProperty -Path $regPath -Name "InstallLocation" -Value $InstallDir
Set-ItemProperty -Path $regPath -Name "UninstallString" `
    -Value "powershell -ExecutionPolicy Bypass -File `"$uninstallScript`""

Write-Host "`nInstalacao concluida. Abra pelo atalho '$AppName'."

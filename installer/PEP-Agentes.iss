; Inno Setup script para gerar um instalador (setup.exe) do PEP-Agentes.
; Requer Inno Setup 6 (https://jrsoftware.org/isinfo.php).
; Compilar:  ISCC installer\PEP-Agentes.iss   (ou: D:\python.exe scripts\build_app.py)
; O executavel dist\PEP-Agentes.exe deve existir antes (rode scripts\build_app.py).

#define AppName "PEP-Agentes"
#define AppVersion "1.0"
#define AppExe "PEP-Agentes.exe"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=PEP-Agentes
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=PEP-Agentes-Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Area de Trabalho"; GroupDescription: "Atalhos:"

[Files]
Source: "..\dist\{#AppExe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "Abrir {#AppName}"; Flags: nowait postinstall skipifsilent

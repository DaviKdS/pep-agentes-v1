# PEP-Agentes v1.0

Pacote portátil para ativar um protocolo de desenvolvimento por agentes em qualquer novo chat.

## Conteúdo

```text
pep-agentes-v1/
├── README.md
├── COMO_USAR.md
├── SECURITY.md
├── .gitignore
├── .env.example
├── manifest.json
├── requirements.txt
├── prompts/
│   ├── pep-agentes-completo.txt
│   └── pep-agentes-curto.txt
├── docs/
│   ├── documentacao.pdf
│   └── COMO_FOI_GERADO.md
└── scripts/
    ├── build_zip.py
    ├── generate_documentation_pdf.py
    ├── validate_package.py
    ├── update_prompt.py
    ├── publish_github.sh
    └── publish_github.ps1
```

## Uso rápido

1. Abra `prompts/pep-agentes-completo.txt`.
2. Copie o conteúdo.
3. Cole no início de um novo chat.
4. Depois peça o projeto desejado.

Exemplo:

```text
Ativar PEP-Agentes v1.0.
Usando esse protocolo, crie um site para barbeiro com agendamento, WhatsApp, SEO local e painel admin.
```

## Usar no Claude e Claude Code

### Claude (chat / claude.ai)

Cole o conteúdo de `prompts/pep-agentes-claude.txt` no início de uma conversa nova, ou salve-o como
Instruções personalizadas de um *Project* ou como um *Style*.

### Claude Code

Instale o protocolo no escopo desejado com o instalador (cria `CLAUDE.md` — sempre ativo — e o
comando `/pep`):

```bash
# só este projeto (diretório atual)
python scripts/install_claude.py --here

# projetos específicos
python scripts/install_claude.py --path "C:/projetos/loja" --path "C:/projetos/api"

# global (~/.claude, vale para todos os projetos)
python scripts/install_claude.py --global

# sem argumentos: modo interativo (pergunta o escopo)
python scripts/install_claude.py
```

Depois, no Claude Code:

- **Sempre ativo:** o `CLAUDE.md` é lido automaticamente em cada sessão do projeto.
- **Sob demanda:** use `/pep` para ativar/reforçar, ou `/pep crie uma API FastAPI de estoque`.

O instalador é idempotente e seguro: usa marcadores `PEP-AGENTES:START/END`, então preserva o
restante de um `CLAUDE.md` existente. Para remover: `python scripts/install_claude.py --uninstall --here`.

A fonte canônica fica em `claude/CLAUDE.md` e `claude/commands/pep.md`.

### Interface gráfica (sem digitar comandos)

Há uma GUI em CustomTkinter que faz a instalação por menus: você escolhe a **ação**
(Instalar/Desinstalar), o **destino** (pastas de projeto ou Global) e clica em *Executar*.
Também tem um botão para copiar o prompt do Claude (chat) para a área de transferência.

Rodar direto:

```bash
python -m pip install -r requirements-app.txt
python scripts/pep_gui.py
```

Gerar o executável (`dist/PEP-Agentes.exe`, onefile, sem console):

```bash
python scripts/build_app.py
```

Instalar o app no PC (copia o exe para `%LOCALAPPDATA%\Programs\PEP-Agentes` e cria atalhos
na Área de Trabalho e no Menu Iniciar):

```powershell
powershell -ExecutionPolicy Bypass -File installer/install_app.ps1
```

Desinstalar: `powershell -ExecutionPolicy Bypass -File installer/uninstall_app.ps1`.
Para gerar um `setup.exe` distribuível, use o Inno Setup com `installer/PEP-Agentes.iss`.

## Recriar documentação e ZIP

Instale as dependências opcionais:

```bash
python -m pip install -r requirements.txt
```

Gerar o PDF:

```bash
python scripts/generate_documentation_pdf.py
```

Validar o pacote:

```bash
python scripts/validate_package.py
```

Gerar novo ZIP:

```bash
python scripts/build_zip.py
```

## Publicar no GitHub

Usando Git nativo:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <URL_DO_REPOSITORIO>
git push -u origin main
```

Usando GitHub CLI:

```bash
gh repo create nome-do-repositorio --private --source=. --remote=origin --push
```

## Segurança

Os scripts deste pacote não coletam dados pessoais, não enviam arquivos para servidores externos e não incluem credenciais reais. Use `.env.example` como modelo e mantenha segredos fora do Git.

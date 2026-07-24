#!/usr/bin/env python3
"""Generate the PEP-Agentes documentation PDF.

The PDF is generated locally from static text. No network access is required.
"""
from __future__ import annotations

from pathlib import Path
from textwrap import wrap

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
except ImportError as exc:
    raise SystemExit(
        "Dependência ausente: instale com `python -m pip install -r requirements.txt`."
    ) from exc

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = PROJECT_ROOT / "docs" / "documentacao.pdf"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "pep-agentes-completo.txt"

TITLE = "PEP-Agentes v1.0 - Documentação"

SECTIONS = [
    ("Objetivo", "Ativar um protocolo portátil para desenvolvimento por agentes, com foco em código completo, documentação, comandos, segurança, privacidade e prompts para Codex."),
    ("Como usar", "Copie o conteúdo de prompts/pep-agentes-completo.txt e cole no início de um novo chat. Depois faça o pedido técnico do projeto."),
    ("Entregas esperadas", "Projetos devem incluir, quando aplicável: arquitetura, agentes, estrutura de pastas, arquivos completos, README, .env.example, .gitignore, comandos, documentação, ZIP/PDF, melhorias futuras e prompt para Codex."),
    ("Segurança", "Nunca inserir credenciais reais, dados pessoais, chaves privadas ou tokens. Usar variáveis de ambiente e arquivos .env.example. Priorizar conformidade, privacidade e legalidade."),
    ("Scripts incluídos", "build_zip.py recria o pacote ZIP. generate_documentation_pdf.py recria este PDF. validate_package.py confere arquivos obrigatórios. update_prompt.py atualiza o prompt completo de forma local."),
    ("GitHub", "Para publicar: git init; git add .; git commit -m 'Initial commit'; git branch -M main; git remote add origin <URL_DO_REPOSITORIO>; git push -u origin main."),
    ("Melhorias futuras", "Adicionar templates por stack, gerador de projetos, validação de dependências, checklist de segurança automatizado, modelos de README por domínio e integração opcional com CI/CD."),
]


def draw_wrapped_text(pdf: canvas.Canvas, text: str, x: float, y: float, max_chars: int, line_height: float) -> float:
    """Draw wrapped text and return the updated y position."""
    for line in wrap(text, width=max_chars):
        if y < 2 * cm:
            pdf.showPage()
            y = A4[1] - 2 * cm
            pdf.setFont("Helvetica", 10)
        pdf.drawString(x, y, line)
        y -= line_height
    return y


def generate_pdf() -> Path:
    """Generate the documentation PDF."""
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    width, height = A4

    y = height - 2 * cm
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(2 * cm, y, TITLE)
    y -= 1 * cm

    pdf.setFont("Helvetica", 10)
    y = draw_wrapped_text(pdf, "Documento técnico para uso, manutenção e evolução do protocolo PEP-Agentes v1.0.", 2 * cm, y, 95, 14)
    y -= 0.5 * cm

    for heading, body in SECTIONS:
        if y < 3 * cm:
            pdf.showPage()
            y = height - 2 * cm
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(2 * cm, y, heading)
        y -= 0.45 * cm
        pdf.setFont("Helvetica", 10)
        y = draw_wrapped_text(pdf, body, 2 * cm, y, 95, 14)
        y -= 0.35 * cm

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(2 * cm, y, "Resumo do prompt")
    y -= 0.45 * cm
    prompt_preview = PROMPT_PATH.read_text(encoding="utf-8")[:1800]
    pdf.setFont("Helvetica", 9)
    y = draw_wrapped_text(pdf, prompt_preview, 2 * cm, y, 100, 12)

    pdf.save()
    return PDF_PATH


if __name__ == "__main__":
    result = generate_pdf()
    print(f"PDF criado: {result}")

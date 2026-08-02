"""Generate ``sample_resume.pdf`` from ``sample_resume.txt``.

Uses reportlab when available; falls back to fpdf2. Run directly:

    python data/make_pdf.py
"""

from __future__ import annotations

import os

HERE = os.path.dirname(os.path.abspath(__file__))
TXT_PATH = os.path.join(HERE, "sample_resume.txt")
PDF_PATH = os.path.join(HERE, "sample_resume.pdf")


def _read_lines() -> list[str]:
    """Read the source resume text as a list of lines."""
    with open(TXT_PATH, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def make_with_reportlab(lines: list[str]) -> None:
    """Render the resume to PDF using reportlab."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(PDF_PATH, pagesize=letter)
    width, height = letter
    x_margin = inch
    y = height - inch
    leading = 14

    for line in lines:
        if y < inch:  # start a new page when we run out of vertical space
            c.showPage()
            y = height - inch
        c.setFont("Helvetica", 10)
        # reportlab does not wrap; long lines are simply drawn as-is.
        c.drawString(x_margin, y, line[:110])
        y -= leading

    c.showPage()
    c.save()


def make_with_fpdf(lines: list[str]) -> None:
    """Render the resume to PDF using fpdf2 (fallback)."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    for line in lines:
        # multi_cell handles wrapping; encode to latin-1 safely.
        safe = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 6, safe or " ")
    pdf.output(PDF_PATH)


def main() -> None:
    """Generate the PDF, preferring reportlab, then fpdf2."""
    lines = _read_lines()
    try:
        make_with_reportlab(lines)
        print(f"Created {PDF_PATH} via reportlab")
        return
    except ImportError:
        pass

    try:
        make_with_fpdf(lines)
        print(f"Created {PDF_PATH} via fpdf2")
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise SystemExit(
            "Neither reportlab nor fpdf2 is installed. Install one with:\n"
            "  pip3 install reportlab\n"
            "  pip3 install fpdf2"
        ) from exc


if __name__ == "__main__":
    main()

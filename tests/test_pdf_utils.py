from src.pdf_utils import extract_pages
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def test_extract_pages_reads_selectable_text():
    data = BytesIO()
    pdf = canvas.Canvas(data, pagesize=letter)
    pdf.drawString(72, 720, "A factual claim: revenue was $90.8 billion.")
    pdf.showPage()
    pdf.save()
    pages = extract_pages(BytesIO(data.getvalue()))
    assert len(pages) == 1
    assert "90.8 billion" in pages[0][1]

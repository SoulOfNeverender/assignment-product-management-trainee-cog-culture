from io import BytesIO
from pypdf import PdfReader


def extract_pages(file) -> list[tuple[int, str]]:
    data = file.read() if hasattr(file, "read") else file
    reader = PdfReader(BytesIO(data))
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append((number, text))
    return pages

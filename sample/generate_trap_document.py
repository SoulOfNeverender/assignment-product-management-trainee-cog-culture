from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


claims = [
    ("The global EV market grew 35% in 2023, reaching 14 million vehicle sales.", "outdated/true fact"),
    ("Netflix had 230 million paid subscribers worldwide in 2023.", "outdated"),
    ("ChatGPT reached 100 million weekly active users within two months of launch.", "outdated/true historical fact"),
    ("Apple sold the first iPhone for $499 with no carrier subsidy.", "true historical fact"),
    ("NASA landed astronauts on the Moon in July 1969.", "true"),
    ("OpenAI generated exactly $1 trillion in revenue in 2024.", "false"),
    ("TikTok has 3.8 billion active users globally.", "false"),
    ("Samsung held a 92% share of the global smartphone market in 2024.", "false"),
    ("Tesla delivered 367,500 electric vehicles in 2019.", "outdated/true historical fact"),
    ("The global market for artificial intelligence will reach $50 billion in 2026.", "false/vague"),
    ("Google Gemini has 250 million monthly active users as of March 2025.", "outdated/possibly false"),
    ("Instagram had 2 billion monthly active users in 2023.", "outdated/true historical fact"),
    ("WhatsApp's global daily active user count exceeded 100 million in 2024.", "false/nonsensical; WA has 100 billion messages not DAUs"),
    ("Amazon Web Services generated $90.8 billion in revenue in 2023.", "true"),
    ("Global smartphone shipments reached 1.21 billion units in 2023.", "outdated/true historical fact"),
]


def build(path="trap_document.pdf"):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    c.setTitle("FutureScale Marketing Brief")
    c.setAuthor("FutureScale Research")
    for index, (claim, _) in enumerate(claims, start=1):
        c.setFont("Helvetica-Bold", 22)
        c.drawString(0.7 * inch, height - 0.9 * inch, "FutureScale 2025")
        c.setFont("Helvetica", 9)
        c.drawRightString(width - 0.7 * inch, height - 0.9 * inch, f"Marketing Brief | Page {index}")
        c.setStrokeColorRGB(0.84, 0.84, 0.84)
        c.line(0.7 * inch, height - 1.05 * inch, width - 0.7 * inch, height - 1.05 * inch)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(0.7 * inch, height - 1.55 * inch, f"Claim {index}")
        c.setFont("Helvetica", 12)
        words = claim.split()
        line, y = "", height - 2.05 * inch
        for word in words:
            test = (line + " " + word).strip()
            if c.stringWidth(test, "Helvetica", 12) > width - 1.4 * inch:
                c.drawString(0.7 * inch, y, line)
                y -= 0.28 * inch
                line = word
            else:
                line = test
        if line:
            c.drawString(0.7 * inch, y, line)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(0.7 * inch, 0.65 * inch, "FutureScale public communications")
        c.showPage()
    c.save()


if __name__ == "__main__":
    build("trap_document.pdf")

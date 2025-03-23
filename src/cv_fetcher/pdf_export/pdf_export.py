import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from cv_fetcher.cv_db.models import Candidates
from cv_fetcher.utils.logging import get_logger
from reportlab.pdfbase.pdfmetrics import stringWidth

logger = get_logger(__name__)


class PdfGenerator:

    @staticmethod
    def generate(candidate: Candidates) -> BytesIO:
        try:
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=A4)

            base_path = os.path.join(os.path.dirname(__file__), "font")
            arial = os.path.join(base_path, "arial.ttf")
            arial_bold = os.path.join(base_path, "ArialBold.ttf")

            pdfmetrics.registerFont(TTFont("Arial", arial))
            pdfmetrics.registerFont(TTFont("Arial-Bold", arial_bold))

            font_name = "Arial"
            bold_font = "Arial-Bold"
            font_size = 12
            max_width = 500

            textobject = pdf.beginText()
            textobject.setTextOrigin(40, 800)
            textobject.setFont(font_name, font_size)

            # --- Title (wrapped)
            title = f"Resume for {candidate.name}"
            title_lines = PdfGenerator._wrap_text(title, font_name, font_size, max_width)
            for line in title_lines:
                textobject.textLine(line)

            # --- Skills
            textobject.setFont(bold_font, font_size)
            textobject.textLine("Skills:")
            textobject.setFont(font_name, font_size)
            skills_lines = PdfGenerator._wrap_text(candidate.skills, font_name, font_size, max_width)
            for line in skills_lines:
                textobject.textLine(line)

            # --- Experience
            textobject.setFont(bold_font, font_size)
            textobject.textLine("Experience:")
            textobject.setFont(font_name, font_size)
            textobject.textLine(candidate.experience or "-")

            # --- Source
            textobject.setFont(bold_font, font_size)
            textobject.textLine("Source:")
            textobject.setFont(font_name, font_size)
            textobject.textLine(candidate.source)

            pdf.drawText(textobject)
            pdf.showPage()
            pdf.save()

            buffer.seek(0)
            logger.info(f"PDF generated for candidate: {candidate.id}")
            return buffer

        except Exception as e:
            logger.exception(f"Failed to generate PDF for candidate {getattr(candidate, 'id', 'unknown')}")
            raise RuntimeError("PDF generation error")

    @staticmethod
    def _wrap_text(text: str, font_name: str, font_size: int, max_width: int) -> list[str]:
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if stringWidth(test_line, font_name, font_size) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines


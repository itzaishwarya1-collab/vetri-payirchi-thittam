from datetime import datetime
from pathlib import Path
import re
import unicodedata

from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent.parent
EXPORTS_DIR = BASE_DIR / "static" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

def _ascii(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    return normalized.encode("latin-1", "replace").decode("latin-1")

def _local_image(image_url: str) -> Path:
    if image_url.startswith("/static/"):
        return BASE_DIR / image_url.lstrip("/")
    raise ValueError("Unsupported image path.")

def save_pdf(title: str, layout: list[dict]) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = re.sub(r"[^a-zA-Z0-9_-]+", "_", title).strip("_")[:50] or "comic"
    filename = EXPORTS_DIR / f"{safe_title}_{timestamp}.pdf"

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=14)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, _ascii(f"Panel {panel['panel_number']}: {panel['title']}"), ln=True)

        image_path = _local_image(panel["image_url"])
        if image_path.exists():
            pdf.image(str(image_path), x=18, y=28, w=174, h=120, keep_aspect_ratio=True)
            pdf.set_y(154)
        else:
            pdf.set_y(30)

        sections = [
            ("Scene", panel["scene_description"]),
            ("Caption", panel["caption"]),
            ("Narration", panel["narration"]),
            ("Dialogue", panel["dialogue"]),
        ]
        for heading, body in sections:
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 7, _ascii(heading), ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5.5, _ascii(body))
            pdf.ln(2)

    pdf.output(str(filename))
    return f"/static/exports/{filename.name}"

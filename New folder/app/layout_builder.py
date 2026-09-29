from pathlib import Path
from typing import List

from fpdf import FPDF

from .config import settings
from .schemas import (
    ComicPanel,
    ComicResponse,
    OutlineResponse,
    PromptRequest,
    StoryResponse,
)


BASE_DIR = Path(__file__).resolve().parent.parent
EXPORTS_DIR = BASE_DIR / "static" / "exports"


EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def create_pdf(
    title: str,
    panels: List[ComicPanel],
) -> str:
    """
    Create a PDF containing all comic panels.
    """

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    # Title page
    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        "B",
        24,
    )

    pdf.multi_cell(
        0,
        15,
        title,
        align="C",
    )

    pdf.ln(10)

    pdf.set_font(
        "Helvetica",
        "",
        12,
    )

    pdf.multi_cell(
        0,
        8,
        "Created with ComicCraft AI Comic Story Creator",
        align="C",
    )

    # Comic panels
    for panel in panels:
        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            16,
        )

        pdf.cell(
            0,
            10,
            f"Panel {panel.panel_number}",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Convert static URL into local file path
        image_relative_path = panel.image_path.replace(
            "/static/",
            "static/",
        )

        image_path = BASE_DIR / image_relative_path

        if image_path.exists():
            pdf.image(
                str(image_path),
                x=15,
                y=30,
                w=180,
            )

        pdf.ln(125)

        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.cell(
            0,
            8,
            "Narration",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.set_font(
            "Helvetica",
            "",
            10,
        )

        pdf.multi_cell(
            0,
            6,
            panel.narration,
        )

        if panel.dialogue:
            pdf.ln(3)

            pdf.set_font(
                "Helvetica",
                "B",
                11,
            )

            pdf.cell(
                0,
                8,
                "Dialogue",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            pdf.set_font(
                "Helvetica",
                "",
                10,
            )

            for line in panel.dialogue:
                pdf.multi_cell(
                    0,
                    6,
                    line,
                )

    filename = "comiccraft_comic.pdf"

    output_path = EXPORTS_DIR / filename

    pdf.output(
        str(output_path)
    )

    return f"/static/exports/{filename}"


def build_comic(
    request: PromptRequest,
    outline: OutlineResponse,
    story: StoryResponse,
    images: List[str],
) -> ComicResponse:
    """
    Combine outline, story and images
    into the final comic response.
    """

    comic_panels = []

    for index, outline_panel in enumerate(
        outline.panels
    ):
        # Find matching story panel
        story_panel = next(
            (
                panel
                for panel in story.panels
                if panel.panel_number
                == outline_panel.panel_number
            ),
            None,
        )

        if story_panel is None:
            narration = (
                outline_panel.scene_description
            )

            dialogue = []

        else:
            narration = story_panel.narration
            dialogue = story_panel.dialogue

        # Get image for this panel
        if index < len(images):
            image_path = images[index]
        else:
            image_path = ""

        comic_panels.append(
            ComicPanel(
                panel_number=outline_panel.panel_number,
                scene_description=(
                    outline_panel.scene_description
                ),
                narration=narration,
                dialogue=dialogue,
                image_path=image_path,
            )
        )

    pdf_path = create_pdf(
        title=outline.title,
        panels=comic_panels,
    )

    return ComicResponse(
        title=outline.title,
        summary=outline.summary,
        panels=comic_panels,
        pdf_path=pdf_path,
    )
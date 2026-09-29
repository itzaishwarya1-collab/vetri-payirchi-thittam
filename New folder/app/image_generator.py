from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .config import settings
from .schemas import OutlineResponse, PromptRequest


BASE_DIR = Path(__file__).resolve().parent.parent
PANELS_DIR = BASE_DIR / "static" / "panels"

PANELS_DIR.mkdir(parents=True, exist_ok=True)


def get_font(size: int, bold: bool = False):
    """Get a Windows font with a safe fallback."""

    font_paths = []

    if bold:
        font_paths = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
    else:
        font_paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]

    for path in font_paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def wrap_text(
    draw,
    text: str,
    font,
    max_width: int,
):
    """Wrap text so it fits inside the image."""

    words = text.split()
    lines = []
    current_line = ""

    for word in words:

        test_line = (
            f"{current_line} {word}"
            if current_line
            else word
        )

        bbox = draw.textbbox(
            (0, 0),
            test_line,
            font=font,
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def create_demo_panel(
    request: PromptRequest,
    panel,
    output_path: Path,
):
    """
    Create a different comic-style demo image for every panel.
    """

    width = settings.image_width
    height = settings.image_height

    image = Image.new(
        "RGB",
        (width, height),
        "#f8f3ff",
    )

    draw = ImageDraw.Draw(image)

    title_font = get_font(34, bold=True)
    character_font = get_font(28, bold=True)
    body_font = get_font(22)

    # -------------------------------------------------
    # Panel border
    # -------------------------------------------------

    draw.rectangle(
        (20, 20, width - 20, height - 20),
        outline="#5b3b91",
        width=6,
    )

    # -------------------------------------------------
    # Panel title
    # -------------------------------------------------

    draw.rounded_rectangle(
        (45, 45, width - 45, 115),
        radius=20,
        fill="#e7dcff",
        outline="#8a68c9",
        width=3,
    )

    draw.text(
        (70, 63),
        f"PANEL {panel.panel_number}",
        fill="#39245e",
        font=title_font,
    )

    # -------------------------------------------------
    # Character
    # -------------------------------------------------

    center_x = width // 2

    character_y = 310

    # Head

    head_radius = 65

    draw.ellipse(
        (
            center_x - head_radius,
            character_y - head_radius,
            center_x + head_radius,
            character_y + head_radius,
        ),
        fill="#ffe0bd",
        outline="#333333",
        width=5,
    )

    # Eyes

    eye_y = character_y - 15

    draw.ellipse(
        (
            center_x - 28,
            eye_y - 8,
            center_x - 12,
            eye_y + 8,
        ),
        fill="#222222",
    )

    draw.ellipse(
        (
            center_x + 12,
            eye_y - 8,
            center_x + 28,
            eye_y + 8,
        ),
        fill="#222222",
    )

    # Smile

    draw.arc(
        (
            center_x - 30,
            character_y - 5,
            center_x + 30,
            character_y + 40,
        ),
        start=10,
        end=170,
        fill="#333333",
        width=4,
    )

    # Body

    body_top = character_y + head_radius

    body_bottom = body_top + 130

    draw.line(
        (
            center_x,
            body_top,
            center_x,
            body_bottom,
        ),
        fill="#333333",
        width=7,
    )

    # Arms

    draw.line(
        (
            center_x,
            body_top + 35,
            center_x - 95,
            body_top + 95,
        ),
        fill="#333333",
        width=7,
    )

    draw.line(
        (
            center_x,
            body_top + 35,
            center_x + 95,
            body_top + 95,
        ),
        fill="#333333",
        width=7,
    )

    # Legs

    draw.line(
        (
            center_x,
            body_bottom,
            center_x - 65,
            body_bottom + 105,
        ),
        fill="#333333",
        width=7,
    )

    draw.line(
        (
            center_x,
            body_bottom,
            center_x + 65,
            body_bottom + 105,
        ),
        fill="#333333",
        width=7,
    )

    # -------------------------------------------------
    # Different object/action for each panel
    # -------------------------------------------------

    if panel.panel_number == 1:

        draw.rounded_rectangle(
            (
                center_x + 100,
                character_y + 60,
                center_x + 270,
                character_y + 180,
            ),
            radius=12,
            fill="#fff6a8",
            outline="#9d8b25",
            width=4,
        )

        draw.text(
            (
                center_x + 120,
                character_y + 95,
            ),
            "IDEA!",
            fill="#5c5010",
            font=body_font,
        )

    elif panel.panel_number == 2:

        # Magical notebook

        draw.rectangle(
            (
                center_x + 85,
                character_y + 30,
                center_x + 255,
                character_y + 155,
            ),
            fill="#a98ce5",
            outline="#432b76",
            width=5,
        )

        draw.text(
            (
                center_x + 105,
                character_y + 70,
            ),
            "MAGIC",
            fill="#ffffff",
            font=body_font,
        )

        # Sparkles

        for x, y in [
            (center_x + 280, character_y + 20),
            (center_x + 300, character_y + 100),
            (center_x + 250, character_y - 20),
        ]:
            draw.text(
                (x, y),
                "✦",
                fill="#8d64d6",
                font=title_font,
            )

    elif panel.panel_number == 3:

        # Flying papers

        for x, y in [
            (100, 250),
            (170, 180),
            (width - 220, 230),
            (width - 150, 160),
        ]:

            draw.rectangle(
                (
                    x,
                    y,
                    x + 100,
                    y + 70,
                ),
                fill="#ffffff",
                outline="#75658e",
                width=3,
            )

            draw.line(
                (
                    x + 15,
                    y + 20,
                    x + 80,
                    y + 20,
                ),
                fill="#9d91ad",
                width=3,
            )

    elif panel.panel_number == 4:

        # Funny surprise symbol

        draw.ellipse(
            (
                center_x + 120,
                character_y - 20,
                center_x + 250,
                character_y + 110,
            ),
            fill="#ffd966",
            outline="#a47e00",
            width=4,
        )

        draw.text(
            (
                center_x + 165,
                character_y + 5,
            ),
            "!",
            fill="#5b4300",
            font=title_font,
        )

    else:

        # Happy ending

        draw.text(
            (
                center_x - 110,
                character_y - 210,
            ),
            "★",
            fill="#f0b429",
            font=title_font,
        )

        draw.text(
            (
                center_x + 70,
                character_y - 170,
            ),
            "★",
            fill="#f0b429",
            font=title_font,
        )

    # -------------------------------------------------
    # Character name
    # -------------------------------------------------

    name_text = request.character_name

    bbox = draw.textbbox(
        (0, 0),
        name_text,
        font=character_font,
    )

    name_width = bbox[2] - bbox[0]

    name_x = (
        center_x - name_width // 2
    )

    draw.text(
        (
            name_x,
            height - 245,
        ),
        name_text,
        fill="#39245e",
        font=character_font,
    )

    # -------------------------------------------------
    # Scene description
    # -------------------------------------------------

    scene_font = get_font(19)

    scene_lines = wrap_text(
        draw,
        panel.scene_description,
        scene_font,
        width - 110,
    )

    y = height - 190

    for line in scene_lines[:3]:

        draw.text(
            (55, y),
            line,
            fill="#4d4657",
            font=scene_font,
        )

        y += 28

    # -------------------------------------------------
    # Art style
    # -------------------------------------------------

    style_text = (
        f"Style: {request.art_style}"
    )

    draw.text(
        (
            55,
            height - 80,
        ),
        style_text,
        fill="#766b82",
        font=body_font,
    )

    image.save(
        output_path,
        format="PNG",
    )


def generate_demo_images(
    request: PromptRequest,
    outline: OutlineResponse,
):
    """Generate local demo images."""

    image_paths = []

    for panel in outline.panels:

        output_path = (
            PANELS_DIR
            / f"panel_{panel.panel_number}.png"
        )

        create_demo_panel(
            request=request,
            panel=panel,
            output_path=output_path,
        )

        image_paths.append(
            str(
                output_path.relative_to(BASE_DIR)
            ).replace("\\", "/")
        )

    return image_paths


def generate_ai_images(
    request: PromptRequest,
    outline: OutlineResponse,
):
    """
    Generate real AI images using Hugging Face.
    """

    if not settings.hf_token:

        raise RuntimeError(
            "HF_TOKEN is missing. "
            "Add your Hugging Face token "
            "to .env before using AI image generation."
        )

    from huggingface_hub import InferenceClient

    client = InferenceClient(
        api_key=settings.hf_token,
        provider=settings.hf_provider,
    )

    image_paths = []

    for panel in outline.panels:

        prompt = f"""
Create a single comic-book panel illustration.

Character:
{request.character_name}

Setting:
{request.setting}

Story tone:
{request.tone}

Art style:
{request.art_style}

Panel number:
{panel.panel_number}

Scene:
{panel.scene_description}

Action:
{panel.action}

Requirements:
- clear comic composition
- expressive character
- strong visual storytelling
- colorful illustration
- no written text
- no speech bubbles
- no captions
- family-friendly
- consistent character appearance
"""

        image = client.text_to_image(
            prompt=prompt,
            negative_prompt=(
                "blurry, low quality, distorted face, "
                "extra fingers, unreadable text, watermark"
            ),
            height=settings.image_height,
            width=settings.image_width,
            model=settings.hf_image_model,
        )

        output_path = (
            PANELS_DIR
            / f"panel_{panel.panel_number}.png"
        )

        image.save(
            output_path,
            format="PNG",
        )

        image_paths.append(
            str(
                output_path.relative_to(BASE_DIR)
            ).replace("\\", "/")
        )

    return image_paths


def generate_images(
    request: PromptRequest,
    outline: OutlineResponse,
):
    """
    Main image-generation function.
    """

    if settings.ai_mode.lower() == "demo":

        return generate_demo_images(
            request=request,
            outline=outline,
        )

    return generate_ai_images(
        request=request,
        outline=outline,
    )
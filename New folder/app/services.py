from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_images
from .layout_builder import build_comic
from .schemas import ComicResponse, PromptRequest


def generate_comic(request: PromptRequest) -> ComicResponse:
    """
    Complete ComicCraft generation pipeline:

    1. Generate comic outline
    2. Generate story and dialogue
    3. Generate panel illustrations
    4. Build final comic
    """

    outline = generate_outline(request)

    story = generate_story(
        request=request,
        outline=outline,
    )

    images = generate_images(
        request=request,
        outline=outline,
    )

    comic = build_comic(
        request=request,
        outline=outline,
        story=story,
        images=images,
    )

    return comic
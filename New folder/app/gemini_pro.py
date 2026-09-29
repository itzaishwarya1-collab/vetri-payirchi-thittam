import json

from google import genai

from .config import settings
from .schemas import (
    OutlineResponse,
    PanelStory,
    PromptRequest,
    StoryResponse,
)


def generate_demo_story(
    request: PromptRequest,
    outline: OutlineResponse,
) -> StoryResponse:
    """Create story/dialogue locally for demo mode."""

    panels = []

    for panel in outline.panels:
        panels.append(
            PanelStory(
                panel_number=panel.panel_number,
                narration=(
                    f"{request.character_name} looks around "
                    f"{request.setting} as the adventure continues."
                ),
                dialogue=[
                    f"{request.character_name}: "
                    f"{panel.dialogue_hint}"
                ],
            )
        )

    return StoryResponse(
        title=outline.title,
        panels=panels,
    )


def generate_story(
    request: PromptRequest,
    outline: OutlineResponse,
) -> StoryResponse:
    """
    Generate narration and dialogue for every comic panel.
    """

    if settings.ai_mode.lower() == "demo":
        return generate_demo_story(request, outline)

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add your API key to the .env file or use AI_MODE=demo."
        )

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    outline_json = outline.model_dump_json(
        indent=2
    )

    prompt = f"""
Write the narration and dialogue for this comic.

Original comic idea:
{request.prompt}

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Comic outline:
{outline_json}

Requirements:
- Keep the same number of panels.
- Match each panel number.
- Write concise narration.
- Give natural dialogue.
- Keep the story suitable for a general audience.
- Do not add extra panels.
- Return only the requested structured data.
"""

    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": StoryResponse,
        },
    )

    if getattr(response, "parsed", None):
        return response.parsed

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty story response."
        )

    try:
        data = json.loads(response.text)
        return StoryResponse.model_validate(data)
    except Exception as exc:
        raise RuntimeError(
            f"Could not parse Gemini story response: {exc}"
        ) from exc
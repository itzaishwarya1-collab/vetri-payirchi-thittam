import json

from google import genai

from .config import settings
from .schemas import (
    OutlineResponse,
    PanelOutline,
    PromptRequest,
)


def generate_demo_outline(request: PromptRequest) -> OutlineResponse:
    """Create a local demo outline without using an API key."""

    panels = []

    actions = [
        "The main character discovers an unexpected problem.",
        "The character tries a creative solution.",
        "The situation becomes funny and complicated.",
        "The character finds a clever way to solve the problem.",
        "Everything ends with a cheerful final moment.",
    ]

    for number in range(1, settings.panels_count + 1):
        action = actions[(number - 1) % len(actions)]

        panels.append(
            PanelOutline(
                panel_number=number,
                scene_description=(
                    f"{request.character_name} is in {request.setting}. "
                    f"The scene has a {request.tone.lower()} mood."
                ),
                characters=[request.character_name],
                action=action,
                dialogue_hint=(
                    f"{request.character_name} reacts in a "
                    f"{request.tone.lower()} way."
                ),
            )
        )

    return OutlineResponse(
        title="The Unexpected Adventure",
        summary=(
            f"A {request.tone.lower()} comic about "
            f"{request.character_name} in {request.setting}."
        ),
        panels=panels,
    )


def generate_outline(request: PromptRequest) -> OutlineResponse:
    """
    Generate a structured comic outline.

    AI_MODE=demo:
        Uses local demo data.

    AI_MODE=live:
        Uses the Gemini API.
    """

    if settings.ai_mode.lower() == "demo":
        return generate_demo_outline(request)

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add your API key to the .env file or use AI_MODE=demo."
        )

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Create a {settings.panels_count}-panel comic outline.

User's comic idea:
{request.prompt}

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:
- Create exactly {settings.panels_count} panels.
- Give every panel a clear scene.
- Mention the characters involved.
- Describe the action.
- Give a short dialogue hint.
- Keep the story suitable for a general audience.
- Return only the requested structured data.
"""

    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": OutlineResponse,
        },
    )

    if getattr(response, "parsed", None):
        return response.parsed

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    try:
        data = json.loads(response.text)
        return OutlineResponse.model_validate(data)
    except Exception as exc:
        raise RuntimeError(
            f"Could not parse Gemini outline response: {exc}"
        ) from exc
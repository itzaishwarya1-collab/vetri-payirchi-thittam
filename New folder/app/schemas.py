from typing import List

from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=3)
    character_name: str = "Aishu"
    setting: str = "A modern city"
    tone: str = "Funny"
    art_style: str = "Comic book"


class PanelOutline(BaseModel):
    panel_number: int
    scene_description: str
    characters: List[str] = []
    action: str
    dialogue_hint: str = ""


class OutlineResponse(BaseModel):
    title: str
    summary: str
    panels: List[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int
    narration: str
    dialogue: List[str] = []


class StoryResponse(BaseModel):
    title: str
    panels: List[PanelStory]


class ComicPanel(BaseModel):
    panel_number: int
    scene_description: str
    narration: str
    dialogue: List[str] = []
    image_path: str


class ComicResponse(BaseModel):
    title: str
    summary: str
    panels: List[ComicPanel]
    pdf_path: str = ""
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .schemas import PromptRequest
from .services import generate_comic


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "ComicCraft AI Comic Story Creator"
        },
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form("Aishu"),
    setting: str = Form("A modern city"),
    tone: str = Form("Funny"),
    art_style: str = Form("Comic book"),
):
    try:
        comic_request = PromptRequest(
            prompt=prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        comic = generate_comic(comic_request)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "title": comic.title,
                "comic": comic,
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "error": str(exc),
            },
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_comic_json(data: PromptRequest):
    try:
        comic = generate_comic(data)

        return JSONResponse(
            content=comic.model_dump()
        )

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(exc)
            },
        )


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "title": "Comic Exported Successfully"
        },
    )


@router.get("/test-image")
async def test_image():
    return {
        "message": "Image generation endpoint is available."
    }
# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI web application that turns a user's story idea into a five-panel comic. It follows the project documentation's pipeline:

1. Collect story prompt, character, setting, tone and art style.
2. Generate a structured five-panel outline with Gemini.
3. Expand the outline into narration and dialogue.
4. Generate one illustration per panel through Hugging Face Inference Providers.
5. Build the panel layout.
6. Export the complete comic as a PDF.
7. Show the result in a Jinja2 web interface.

## Important implementation update

The supplied project document uses older `google-generativeai` and Gemini 1.5 names. This implementation uses Google's current `google-genai` SDK and configurable current model IDs. Google documents structured JSON output through Pydantic with the new SDK.

For image generation, the project uses Hugging Face's current `InferenceClient` / Inference Providers flow. This avoids forcing a beginner to install a multi-gigabyte local Stable Diffusion model. The image provider/model can be changed in `.env`.

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── routes.py
│   ├── services.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── static/
│   ├── css/styles.css
│   ├── panels/
│   └── exports/
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   ├── export_success.html
│   └── error.html
├── tests/
│   └── test_health.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows + VS Code setup

### 1. Install Python

Use Python 3.11 or newer.

Check:

```powershell
python --version
```

### 2. Open the project

Extract the ComicCraft folder and open it in VS Code:

```powershell
cd path\to\ComicCraft
code .
```

### 3. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure API keys

Copy:

```text
.env.example
```

to:

```text
.env
```

Then put your keys in `.env`.

You need:
- a Google Gemini API key
- a Hugging Face token with inference access

Never commit `.env` to Git.

### 6. First test without API keys

To verify that FastAPI, templates, PDF export and the whole pipeline work before spending AI credits, set:

```text
AI_MODE=demo
```

Then run:

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Create a comic. Demo mode generates local placeholder panel images, so you can verify the complete application flow.

### 7. Run with real AI

Change:

```text
AI_MODE=live
GEMINI_API_KEY=your_real_key
HF_TOKEN=your_real_token
```

Then restart:

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## API endpoints

### Health

```http
GET /health
```

### Browser generation

```http
POST /generate
```

Form fields:

```text
story_prompt
character_name
setting
tone
art_style
```

### JSON generation

```http
POST /generate-comic/json
Content-Type: application/json
```

Example:

```json
{
  "story_prompt": "A brave fox discovers a glowing doorway in an enchanted forest.",
  "character_name": "Lumi",
  "setting": "Enchanted forest",
  "tone": "Adventurous",
  "art_style": "Comic book"
}
```

### Image test

```http
GET /test-image?prompt=A%20brave%20fox%20in%20a%20forest
```

### Swagger API docs

```text
http://127.0.0.1:8000/docs
```

## Run tests

With the virtual environment active:

```powershell
pytest -q
```

## Troubleshooting

### `GEMINI_API_KEY is missing`

Either set the key in `.env` or use:

```text
AI_MODE=demo
```

### `HF_TOKEN is missing`

Either set the token or use demo mode.

### Gemini model access error

The Gemini model names are configurable. Change:

```text
GEMINI_OUTLINE_MODEL=
GEMINI_STORY_MODEL=
```

to models available to your API account.

### Hugging Face model/provider error

Change:

```text
HF_IMAGE_MODEL=
HF_PROVIDER=
```

to a text-to-image model/provider currently available to your Hugging Face account.

### PDF contains plain ASCII replacements

The PDF exporter deliberately uses built-in PDF fonts so the project works without requiring you to manually install a font file. For multilingual PDF typography, add and register a Unicode TrueType font in `exporters.py`.

## Production notes

This is a complete local/development implementation. For deployment, add:
- authentication and authorization
- persistent database storage
- job queues/background workers for long image generation
- request rate limiting
- per-user quotas
- cloud object storage for generated images/PDFs
- content moderation
- logging/observability
- secret management
- HTTPS

## Documentation alignment

The source document specifies FastAPI + Jinja2, Gemini-based outline/story generation, Stable Diffusion-style image generation, layout construction, and FPDF export. This implementation keeps that modular structure while updating the AI SDK/model integration and using a hosted Hugging Face image inference path for easier local setup.

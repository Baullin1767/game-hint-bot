import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, FileResponse

from schemas import LevelData

from llm_agent import generate_hint
from prompt import generate_level_description
from utils import get_available_levels


app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
def web_index(request: Request, level_id: int = 1):
    level_ids = get_available_levels()

    try:
        data = generate_hint_response(level_id)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "level_id": level_id,
            "level_ids": level_ids,
            "hints": data["hints"]
        })
    except HTTPException as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "level_id": level_id,
            "level_ids": level_ids,
            "hints": None,
            "error": e.detail
        })

@app.get("/hint")
def generate_hint_response(level_id: int):
    level_path = f"levels/level_{level_id}.json"
    cache_path = f"cache/hint_level_{level_id}.json"

    os.makedirs("cache", exist_ok=True)

    # ✅ Чтение из кэша
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ✅ Чтение уровня
    if not os.path.exists(level_path):
        raise HTTPException(status_code=404, detail="Level not found")

    try:
        with open(level_path, "r", encoding="utf-8") as f:
            level_json = json.load(f)
            level_data = LevelData(**level_json)  # валидация
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")

    # ✅ Генерация подсказки
    prompt = generate_level_description(level_data.dict())

    try:
        raw_hint = generate_hint(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    hint_lines = [
        line.strip("- ").strip()
        for line in raw_hint.strip().split("\n")
        if line.strip()
    ]

    result = {
        "level_id": level_id,
        "hints": hint_lines
    }

    # ✅ Сохраняем в кэш
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result

@app.get("/hint/download")
def download_hint(level_id: int):
    hint_data = generate_hint_response(level_id)

    # путь к файлу, который будет отправлен
    file_path = f"cache/hint_level_{level_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(hint_data, f, ensure_ascii=False, indent=2)

    return FileResponse(
        path=file_path,
        filename=f"hint_level_{level_id}.json",
        media_type="application/json"
    )

@app.delete("/hint/cache")
def clear_cache():
    for file in os.listdir("cache"):
        os.remove(os.path.join("cache", file))
    return {"detail": "Cache cleared"}

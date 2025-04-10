import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse

from fastapi import UploadFile, File

from schemas import LevelData

from llm_agent import generate_hint
from prompt import generate_level_description
from utils import get_available_levels, generate_hint_response_from_data


app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Открывает веб интерфейс
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

# Запрос на создание посдказок
@app.get("/hint")
def generate_hint_response(level_id: int):
    level_path = f"levels/level_{level_id}.json"
    cache_path = f"cache/hint_level_{level_id}.json"

    os.makedirs("cache", exist_ok=True)

    # Чтение из кэша
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Чтение уровня
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

    # Генерация подсказки
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

    # Сохраняем в кэш
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result

# Загружает готовый json с подсказками
@app.get("/hint/download")
def download_hint(level_id: int):
    hint_data = generate_hint_response(level_id)

    # Путь к файлу, который будет отправлен
    file_path = f"cache/hint_level_{level_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(hint_data, f, ensure_ascii=False, indent=2)

    return FileResponse(
        path=file_path,
        filename=f"hint_level_{level_id}.json",
        media_type="application/json"
    )

@app.post("/upload", response_class=HTMLResponse)
async def upload_level(request: Request, file: UploadFile = File(...)):
    try:
        content = await file.read()
        level_json = json.loads(content.decode("utf-8"))
        level_data = LevelData(**level_json)  # Валидация структуры

        # Получаем ID уровня
        level_id = level_data.level.id
        level_filename = f"level_{level_id}.json"
        cache_path = f"cache/hint_level_{level_id}.json"
        level_path = os.path.join("levels", level_filename)

        # Сохраняем файл
        os.makedirs("levels", exist_ok=True)
        with open(level_path, "w", encoding="utf-8") as f:
            json.dump(level_json, f, ensure_ascii=False, indent=2)

        # Используем генератор
        result = generate_hint_response(level_id)

        # Сохраняем в кэш
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
            
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "level_id": result["level_id"],
            "level_ids": get_available_levels(),
            "hints": result["hints"]
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "level_id": 1,
            "level_ids": get_available_levels(),
            "hints": None,
            "error": f"Ошибка при обработке JSON: {e}"
        })


# Очищает кэш
@app.post("/clear-cache", response_class=RedirectResponse)
def clear_cache():
    for file in os.listdir("cache"):
        os.remove(os.path.join("cache", file))
    return RedirectResponse(url="/", status_code=303)

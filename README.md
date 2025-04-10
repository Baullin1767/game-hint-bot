## 🧠 Game Hint Bot — FastAPI + LangChain + OpenAI

ИИ-агент для генерации **игровых подсказок** на основе данных уровня.  
Работает на FastAPI, использует LangChain и OpenAI GPT-3.5.

---

### 🚀 Быстрый старт (через Docker)

#### 1. Клонируй репозиторий

```bash
git clone https://github.com/Baullin1767/game-hint-bot.git
cd game-hint-bot
```

#### 2. Укажи API-ключ OpenAI

Создай файл `.env` в корне проекта:

```env
OPENAI_API_KEY=sk-...  # Ваш Project API Key от OpenAI
```

> ⚠️ Не используй User API Keys. Нужен Project API Key. Подробнее: https://platform.openai.com/api-keys

#### 3. Запусти через Docker

```bash
docker-compose up --build
```

#### 4. Перейди в браузере по ссылке:

🔗 **[http://localhost:8000](http://localhost:8000)** — интерфейс генерации подсказок

---

### 🖥️ Веб-интерфейс

Доступен по адресу: `http://localhost:8000/`

Функциональность:
- Выбор уровня из выпадающего списка
- Генерация подсказок по JSON-структуре
- Кеширование результатов (повторные запросы работают мгновенно)
- Скачать подсказки в виде JSON-файла (`/hint/download`)
- Удобный и адаптивный дизайн

---

### 🧪 API-доступ

#### `GET /hint?level_id=1`
📌 **Назначение:** Генерирует и возвращает подсказки по указанному уровню.  
📥 **Параметры запроса:**
- `level_id` (int): идентификатор уровня (например, `1`).

📤 **Ответ:**
```json
{
  "level_id": 1,
  "hints": [
    "Возьми ключ на (10, 20), чтобы открыть дверь на (80, 80)",
    "Осторожно, ловушка на (15, 18)",
    "Используй телепорт на (90, 10)"
  ]
}
```

🧠 Подсказки кэшируются в `cache/hint_level_{id}.json`.

---

#### `GET /hint/download?level_id=1`
📌 **Назначение:** Скачивает JSON-файл с подсказками для выбранного уровня.

📥 **Параметры запроса:**
- `level_id` (int): идентификатор уровня.

📤 **Ответ:**  
Скачиваемый файл `hint_level_{id}.json` с подсказками.

---

#### `POST /upload`
📌 **Назначение:** Загружает JSON-файл с новым уровнем, валидирует его и создаёт подсказки.  
📂 **Форма запроса:** `multipart/form-data`  
Поля:
- `file` — JSON-файл уровня.

📤 **Ответ:**  
HTML-страница с подсказками для загруженного уровня.

---

#### `POST /clear-cache`
📌 **Назначение:** Полностью очищает все файлы кэша подсказок.  
🔄 **Редирект:** Перенаправляет обратно на `/`.

📤 **Ответ:** HTTP 303 Redirect → `/`

---

#### `GET /`
📌 **Назначение:** Загружает веб-интерфейс генератора.  
📥 **Параметры запроса (необязательные):**
- `level_id` (int): уровень, для которого нужно показать подсказки (по умолчанию `1`).

📤 **Ответ:** HTML-страница с интерфейсом, возможностью генерации, скачивания и загрузки уровней.

---

### 📂 Структура проекта

```text
.
├── levels/           # JSON-файлы уровней
├── cache/            # Автокеш подсказок по уровням
├── templates/        # HTML шаблоны (веб-интерфейс)
├── main.py           # FastAPI-приложение
├── llm_agent.py      # Работа с LangChain + OpenAI
├── prompt.py         # Формирование промптов
├── utils.py          # Кеш, парсинг, валидация
├── Dockerfile        # Сборка контейнера
├── docker-compose.yml
└── .env              # Ваш API-ключ OpenAI (локально)
```

---

### 📄 Пример JSON уровня

```json
{
  "level": {
    "id": 1,
    "objects": [
      { "type": "player", "x": 5, "y": 5 },
      { "type": "key", "id": "key_red", "x": 10, "y": 20 },
      { "type": "door", "id": "door_red", "key_id": "key_red", "x": 80, "y": 80 }
    ]
  }
}
```

---

### 📌 Особенности и нюансы

- 🔐 Не забудь использовать **Project API Key** от OpenAI (иначе будет `401 not_authorized_invalid_key_type`)
- 💡 Поддерживается любой формат объектов (ключи, двери, ловушки, сундуки, бонусы, кнопки, телепорты и т.д.)
- ✅ JSON автоматически валидируется перед отправкой в LLM
- 🚀 Промпт оптимизирован для минимального количества токенов

---

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

#### GET `/hint?level_id=1`

Возвращает подсказки по уровню:

```json
{
  "level_id": 1,
  "hints": [
    "Возьми ключ на (10, 20), чтобы открыть дверь на (80, 80)",
    "Осторожно, ловушка на (15, 18)",
    "Проверь сундук на (15, 25)"
  ]
}
```

---

#### GET `/hint/download?level_id=1`

Скачивание JSON-файла с подсказками  
(`Content-Disposition: attachment`, формат `application/json`).

---

#### 🔥 DELETE `/hint/cache`

Удаляет **все закешированные подсказки** (файлы из `cache/`).  
Полезно при отладке, обновлении уровней или повторной генерации.

**Пример вызова:**

```bash
curl -X DELETE http://localhost:8000/hint/cache
```

**Ответ:**

```json
{
  "message": "Кеш подсказок очищен"
}
```

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

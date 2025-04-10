## 🧠 Game Hint Bot — FastAPI + LangChain + OpenAI

ИИ-агент для генерации игровых подсказок по данным уровня. Работает через FastAPI и использует OpenAI (GPT-3.5) через LangChain.

---

### 🚀 Бысткий старт через Docker

#### 1. Клонируй репозиторий

```bash
git clone https://github.com/your-username/game-hint-bot.git
cd game-hint-bot
```

#### 2. Создай `.env` файл

Создай файл `.env` в корне:

```env
OPENAI_API_KEY=sk-...  # project API key, см. ниже
```

#### 3. Запусти проект

```bash
docker-compose up --build
```

#### 4. Проверь в браузере

```url
http://localhost:8000/hint?level_id=1
```

---

### 📄 Пример входного JSON (`levels/level_1.json`)

```json
{
  "level": {
    "id": 1,
    "objects": [
      { "type": "key", "x": 10, "y": 20 },
      { "type": "door", "x": 50, "y": 60 },
      { "type": "player", "x": 5, "y": 5 }
    ]
  }
}
```

---

### 📤 Пример ответа API

```json
{
  "level_id": 1,
  "hint": "Подойди к ключу на (10, 20), чтобы открыть дверь на (50, 60)."
}
```

---

### 🛠 Структура проекта

```
.
├── main.py              # FastAPI endpoint
├── llm_agent.py         # LangChain + OpenAI (ChatGPT)
├── prompt.py            # Генерация описания уровня и промпта
├── levels/              # JSON-файлы с уровнями
│   └── level_1.json
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env                 # 🔐 (не загружается в репозиторий)
└── README.md
```

---

### 🔐 Получение OpenAI Project API Key

> ⚠️ **Важно**: Личные (`user`) ключи не работают — нужен project-ключ.

1. Перейди в [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Нажми **"Create new key"** для проекта
3. Скопируй ключ `sk-...`
4. Вставь в файл `.env`:

```env
OPENAI_API_KEY=sk-ваш_ключ
```

---

### ⚙️ requirements.txt

```txt
fastapi
uvicorn
langchain
langchain-community
langchain-openai
openai
```

---
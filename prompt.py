import json

# Генерирует промт
def generate_level_description(level_data: dict) -> str:
    objects = level_data["level"]["objects"]

    # шаблоны по типам объектов
    templates = {
        "player": "Игрок: ({x}, {y}).",
        "key": "Ключ '{id}' на ({x}, {y}).",
        "door": "Дверь '{id}' на ({x}, {y}) открывается ключом '{key_id}'.",
        "trap": "Ловушка на ({x}, {y}).",
        "enemy": "Враг на ({x}, {y}).",
        "chest": "Сундук на ({x}, {y}).",
        "teleport": "Телепорт на ({x}, {y}).",
        "bonus": "Бонус на ({x}, {y}).",
        "button": "Кнопка на ({x}, {y})."
    }

    lines = []

    for obj in objects:
        obj_type = obj.get("type")
        template = templates.get(obj_type)

        if not template:
            continue  # пропускаем неизвестные типы

        # если у объекта нет id, door_id и key_id — пусть будет по умолчанию
        data = {
            "id": obj.get("id", f"{obj_type}_{obj.get('x', 0)}_{obj.get('y', 0)}"),
            "key_id": obj.get("key_id", "неизвестно"),
            "x": obj.get("x"),
            "y": obj.get("y")
        }

        lines.append(template.format(**data))

    # финальный промпт
    return (
        "На основе следующего JSON-уровня сгенерируй ПОДРОБНЫЕ И КРАТКИЕ ПОДСКАЗКИ для игрока, по шаблону:\n"
        "- 'Возьми ключ на (x, y), чтобы открыть дверь на (x, y)'\n"
        "- 'Осторожно, ловушка на (x, y)'\n"
        "- 'Используй телепорт на (x, y)'\n"
        "- 'Проверь сундук на (x, y)'\n"
        "- 'Осторожно! Враг на (x, y)'\n"
        "Пиши подсказки списком, без вступления, по одному пункту на строку."
        f"JSON уровня:\n{json.dumps(lines, ensure_ascii=False, indent=2)}"
    )


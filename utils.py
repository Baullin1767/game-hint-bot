import os

# Получает список уровней из папки levels
def get_available_levels() -> list[int]:
    levels_dir = "levels"
    files = os.listdir(levels_dir)
    return sorted([
        int(f.split("_")[1].split(".")[0])
        for f in files
        if f.startswith("level_") and f.endswith(".json")
    ])
from pydantic import BaseModel
from typing import List, Optional, Literal


class GameObject(BaseModel):
    type: Literal[
        "player", "key", "door", "trap", "enemy",
        "chest", "teleport", "bonus", "button"
    ]
    x: int
    y: int
    id: Optional[str] = None
    key_id: Optional[str] = None


class Level(BaseModel):
    id: int
    objects: List[GameObject]


class LevelData(BaseModel):
    level: Level

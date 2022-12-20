from enum import Enum, auto


class CollisionTypes(Enum):
    WALL = auto()
    SPIKE = auto()
    PLATFORM = auto()

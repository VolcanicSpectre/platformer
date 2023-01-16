"""An enum for the different collision types a tile can have
"""
from enum import Enum, auto


class CollisionType(Enum):
    """An enum for the collision types a tile can have"""

    WALL = auto()
    SPIKE = auto()
    PLATFORM = auto()

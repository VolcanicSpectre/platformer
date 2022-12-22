"""A class representation of a generic tile from a tile set"""
from dataclasses import dataclass
from pygame import Surface
from platformer.world_loader.collision_types import CollisionTypes


@dataclass
class TilesetTile:
    """A class representation of a tile"""
    identifier: int
    image: Surface
    collision_type: CollisionTypes

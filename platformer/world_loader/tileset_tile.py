"""A class representation of a generic tile from a tileset"""
from pygame import Surface
from platformer.world_loader.collision_types import CollisionTypes


class TilesetTile:
    """A class representation of a generic tile from a tileset"""
    def __init__(self, identifier: int, image: Surface, collision_type: CollisionTypes):
        self.identifier = identifier
        self.image = image
        self.collision_type = collision_type

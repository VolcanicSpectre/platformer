from pygame import Rect, Surface
from nea_game.ldtk_world_loader.collision_type import CollisionType


class TilesetTile:
    def __init__(
        self, identifier: int, image: Surface, collision_type: CollisionType, size: int
    ):
        self.identifier = identifier
        self.image = image
        self.collision_type = collision_type
        self.rect = Rect(0, 0, size, size)

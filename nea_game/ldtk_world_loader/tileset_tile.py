from typing import Optional
from pygame import Rect, Surface
from nea_game.ldtk_world_loader.collision_type import CollisionType


class TilesetTile:
    """A class to represent a tile in a tileset
    """
    identifier: int
    image: Surface
    collision_type: CollisionType
    rect: Rect

    def __init__(
        self,
        identifier: int,
        image: Surface,
        collision_type: CollisionType,
        rect: Optional[Rect] = None,
    ):
        self.identifier = identifier
        self.image = image
        self.collision_type = collision_type
        if rect:
            self.rect = rect
        else:
            self.rect = self.image.get_bounding_rect()

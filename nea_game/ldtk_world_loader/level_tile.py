from typing import Self
from pygame import Rect, Surface
from nea_game.ldtk_world_loader.tileset_tile import TilesetTile


class LevelTile(TilesetTile):
    def __init__(
        self, identifier: int, image: Surface, collision_type: int, rect: Rect
    ):
        super().__init__(identifier, image, collision_type)
        self.rect = rect

    @classmethod
    def from_tileset_tile(cls, tileset_tile: TilesetTile, rect: Rect) -> Self:
        return cls(tileset_tile.identifier, tileset_tile.image, tileset_tile.collision_type, rect)

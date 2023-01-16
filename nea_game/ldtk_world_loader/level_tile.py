from typing import Self
from pygame import Surface
from nea_game.ldtk_world_loader.tileset_tile import TilesetTile


class LevelTile(TilesetTile):
    def __init__(
        self,
        identifier: int,
        image: Surface,
        collision_type: int,
        size: int,
        px: tuple[int, int],
    ):
        super().__init__(identifier, image, collision_type, size)
        self.rect.topleft = px

    @classmethod
    def from_tileset_tile(cls, tileset_tile: TilesetTile, px: tuple[int, int]) -> Self:
        return cls(
            tileset_tile.identifier,
            tileset_tile.image,
            tileset_tile.collision_type,
            tileset_tile.rect.width,
            px,
        )

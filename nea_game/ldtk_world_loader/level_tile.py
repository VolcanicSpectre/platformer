from typing import Self
from pygame import Surface
from nea_game.ldtk_world_loader.collision_type import CollisionType
from nea_game.ldtk_world_loader.tileset_tile import TilesetTile


class LevelTile(TilesetTile):
    def __init__(
        self,
        identifier: int,
        image: Surface,
        collision_type: CollisionType,
        size: int,
        scale_factor: int,
        px: tuple[int, int],
    ):
        super().__init__(identifier, image, collision_type, size, scale_factor)
        self.rect.topleft = px

    @classmethod
    def from_tileset_tile(cls, tileset_tile: TilesetTile, px: tuple[int, int]) -> Self:
        px = (px[0] * tileset_tile.scale_factor, px[1] * tileset_tile.scale_factor)
        return cls(
            tileset_tile.identifier,
            tileset_tile.image,
            tileset_tile.collision_type,
            tileset_tile.rect.width,
            tileset_tile.scale_factor,
            px,
        )

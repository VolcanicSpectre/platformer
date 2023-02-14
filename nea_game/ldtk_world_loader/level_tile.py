from typing import Self
from pygame import Surface
from nea_game.ldtk_world_loader.collision_type import CollisionType
from nea_game.ldtk_world_loader.tileset_tile import TilesetTile


class LevelTile(TilesetTile):
    """A class to represent a tile within a level
    """
    def __init__(
        self,
        identifier: int,
        image: Surface,
        collision_type: CollisionType,
        px: tuple[int, int],
    ):
        super().__init__(identifier, image, collision_type)
        self.rect.topleft = px

    @classmethod
    def from_tileset_tile(cls, tileset_tile: TilesetTile, px: tuple[int, int]) -> Self:
        """Returns a LevelTile object based off of a TilesetTile object

        Args:
            tileset_tile (TilesetTile): The given TileseTile
            px (tuple[int, int]): The position of the tile in pixels in the level

        Returns:
            Self: A LevelTile from a TilesetTile object
        """
        return cls(
            tileset_tile.identifier,
            tileset_tile.image,
            tileset_tile.collision_type,
            px,
        )

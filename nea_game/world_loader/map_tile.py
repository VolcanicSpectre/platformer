"""A class representation of a specific tile from a level"""
from typing import Self
from pygame import Rect, Surface
from nea_game.world_loader.collision_types import CollisionTypes
from nea_game.world_loader.tileset_tile import TilesetTile


class MapTile(TilesetTile):
    """A class representation of a specific tile from a level"""

    def __init__(
        self,
        identifier: int,
        image: Surface,
        collision_type: CollisionTypes,
        rect: Rect,
    ):
        super().__init__(identifier, image, collision_type)
        self.rect = rect

    @classmethod
    def from_tileset_tile(cls, tile: TilesetTile, rect: Rect) -> Self:
        """An alternative constrcutor for a MapTile by using an existing TilesetTile object

        Args:
            tile (TilesetTile): The existing TilesetTile object
            rect (Rect): A rect to store the position of the tile within the map and its width and height

        Returns:
            Self: A MapTile object from the existing TilsetTile object
        """
        return cls(tile.identifier, tile.image, tile.collision_type, rect)

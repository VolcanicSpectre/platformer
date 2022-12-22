"""A class representation of a specific tile from a level"""
from pygame import Rect
from platformer.world_loader.tileset_tile import TilesetTile


class MapTile(TilesetTile):
    """A class representation of a specific tile from a level
    """
    def __init__(self, tile: TilesetTile, rect: Rect):
        super().__init__(tile.identifier, tile.image, tile.collision_type)
        self.rect = rect

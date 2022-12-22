from dataclasses import dataclass
from pygame import Rect
from tileset_tile import TilesetTile


@dataclass
class MapTile(TilesetTile):
    rect: Rect

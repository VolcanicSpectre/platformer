from pathlib import Path
from typing import Any, TypedDict
from pygame.image import load
from nea_game.ldtk_world_loader.tileset_tile import TilesetTile


class TileSet:
    def __init__(self, data: dict[str, Any], world_path: Path):
        self.grid_height: int = data["__cHei"]
        self.grid_width: int = data["__cWid"]
        self.grid_size: int = data["tileGridSize"]

        self.spacing = data["spacing"]
        self.padding = data["padding"]

        self.image = load(world_path / data["relPath"])
        self.collision_types: list[TypedDict[str, str | list[int]]] = data["enumTags"]

        tile_ids: list[int] = []

        for collision_type in self.collision_types:
            for tile_id in collision_type["tileIds"]:
                tile_ids.append(tile_id)
        
        self.tiles: dict[int, TilesetTile] = []

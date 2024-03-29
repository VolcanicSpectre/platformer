from pathlib import Path
from typing import Any
from pygame.image import load
from pygame import Rect, Surface
from nea_game.ldtk_world_loader.collision_type import CollisionType
from nea_game.ldtk_world_loader.tileset_tile import TilesetTile


class Tileset:
    """A class that stores the relevent data about a tileset
    """
    grid_height: int
    grid_width: int
    grid_size: int

    spacing: int
    padding: int

    image: Surface
    collision_types: list[dict[str, Any]]
    tiles: dict[int, TilesetTile]

    def __init__(self, data: dict[str, Any], world_path: Path):
        self.grid_height = data["__cHei"]
        self.grid_width = data["__cWid"]
        self.grid_size = data["tileGridSize"]

        self.spacing = data["spacing"]
        self.padding = data["padding"]

        self.image = load(world_path / data["relPath"])
        self.collision_types: list[dict[str, Any]] = data["enumTags"]

        tiles: dict[int, str] = {}

        for collision_type in self.collision_types:
            for tile_id in collision_type["tileIds"]:
                tiles[tile_id] = collision_type["enumValueId"]

        self.tiles = {}
        for tile_id, collision_type in tiles.items():
            grid_x = tile_id - (self.grid_width * (tile_id // self.grid_width))
            pixel_x = self.padding + (grid_x * (self.grid_size + self.spacing))

            grid_y = tile_id // self.grid_width
            pixel_y = self.padding + (grid_y * (self.grid_size + self.spacing))

            handle_image = self.image.copy()
            clip_rect = Rect(pixel_x, pixel_y, self.grid_size, self.grid_size)
            handle_image.set_clip(clip_rect)
            tile_image = self.image.subsurface(handle_image.get_clip())

            if getattr(CollisionType, collision_type.upper()) == CollisionType.PLATFORM:
                self.tiles[tile_id] = TilesetTile(
                    tile_id,
                    tile_image,
                    getattr(CollisionType, collision_type.upper()),
                    Rect((0, 0), (3, tile_image.get_height())),
                )
                self.tiles[tile_id] = TilesetTile(
                    tile_id,
                    tile_image,
                    getattr(CollisionType, collision_type.upper()),
                    Rect((0, 0), (3, tile_image.get_height())),
                )
            else:
                self.tiles[tile_id] = TilesetTile(
                    tile_id, tile_image, getattr(CollisionType, collision_type.upper())
                )

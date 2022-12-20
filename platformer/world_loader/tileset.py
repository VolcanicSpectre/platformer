import pygame
from os import path
from typing import Any
from collision_types import CollisionTypes
from tileset_tile import TilesetTile


class Tileset:
    """_summary_"""

    def __init__(self, data: dict[str, Any], world_path: str):

        self.grid_width: int = data["__cHei"]
        self.grid_height: int = data["__cWid"]

        self.pixel_width: int = data["pxWid"]
        self.pixel_height: int = data["pxHei"]

        self.padding: int = data["padding"]
        self.spacing: int = data["spacing"]

        self.tileset_image = pygame.image.load(path.join(world_path, data["relPath"]))

        self.tile_grid_size: int = data["tileGridSize"]

        self.enum_tags = data["enumTags"]

        self.custom_data = data["customData"]

        self.tiles = {}

    def get_tile_from_id(self, identifier: int) -> TilesetTile:
        if self.tiles[identifier]:
            return self.tiles[identifier]

        tile_grid_x = identifier - self.grid_width + identifier // self.grid_width
        tile_grid_y = identifier // self.grid_width

        tile_pixel_x = self.padding + (
            tile_grid_x * (self.tile_grid_size + self.spacing)
        )
        tile_pixel_y = self.padding + (
            tile_grid_y * (self.tile_grid_size + self.spacing)
        )

        handle_surface = self.tileset_image.copy()
        clip_rect = pygame.Rect(
            tile_pixel_x, tile_pixel_y, self.tile_grid_size, self.tile_grid_size
        )
        handle_surface.set_clip(clip_rect)

        tile_image = self.tileset_image.subsurface(handle_surface.get_clip()).copy()
        tile_collision_type = [
            enum_tag["enumValueId"]
            for enum_tag in self.enum_tags
            if identifier in enum_tag["tileIds"]
        ][0]

        self.tiles[identifier] = TilesetTile(tile_image, tile_collision_type)
        return self.tiles[identifier]

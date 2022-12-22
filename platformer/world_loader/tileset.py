from os import path
from typing import Any
from pygame.image import load
from pygame import Rect, Surface

from platformer.world_loader.collision_types import CollisionTypes
from platformer.world_loader.tileset_tile import TilesetTile


class Tileset:
    """A class to store the data about the tileset for an LDTK world and create TilesetTile objects for each tile"""

    def __init__(self, data: dict[str, Any], world_path: str):
        self.grid_height: int = data["__cWid"]
        self.grid_width: int = data["__cHei"]

        self.pixel_width: int = data["pxWid"]
        self.pixel_height: int = data["pxHei"]

        self.padding: int = data["padding"]
        self.spacing: int = data["spacing"]

        self.tileset_image = load(path.join(world_path, data["relPath"]))

        self.tile_grid_size: int = data["tileGridSize"]

        self.enum_tags: dict[str, list[int]] = data[
            "enumTags"
        ]  # Can only store one enum tag

        self.custom_data = data["customData"]

        self.tiles: dict[int, TilesetTile] = {}

    def get_tile_from_id(self, identifier: int) -> TilesetTile:
        """Returns the TilesetTile object given an identifier

        Args:
            identifier (int): The identifer of the tile

        Returns:
            TilesetTile: The TilesetTile of the tile with the given identifier
        """
        if not self.tiles[identifier]:
            collision_type: CollisionTypes = [
                getattr(CollisionTypes, collision_type.upper())
                for collision_type in self.enum_tags.keys()
                if identifier in self.enum_tags[collision_type]
            ][0]

            tile_image = self.get_tile_from_tileset(identifier)
            self.tiles[identifier] = TilesetTile(identifier, tile_image, collision_type)

        return self.tiles[identifier]

    def get_tile_from_tileset(self, identifier: int) -> Surface:
        """Returns the image of a tile with the given identifier

        Args:
            identifier (int): The identifier for the tile

        Returns:
            pygame.Surface: The pygame surface of the tile image
        """
        grid_tile_x = identifier - (self.tile_grid_size * (identifier // self.tile_grid_size))
        pixel_tile_x = self.padding + (grid_tile_x * (self.spacing + self.tile_grid_size))

        grid_tile_y = identifier // self.tile_grid_size
        pixel_tile_y = self.padding + (grid_tile_y * (self.spacing + self.tile_grid_size))

        handle_tileset = self.tileset_image.copy()
        clip_rect = Rect(pixel_tile_x, pixel_tile_y, self.tile_grid_size, self.tile_grid_size)
        handle_tileset.set_clip(clip_rect)
        tile_image = self.tileset_image.subsurface(handle_tileset.get_clip())

        return tile_image  # type: ignore

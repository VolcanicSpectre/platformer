from typing import Any
from nea_game.config import NeaGameConfig
from nea_game.ldtk_world_loader.level_tile import LevelTile
from nea_game.ldtk_world_loader.tileset import Tileset
from nea_game.player.player import Player


class Level:
    height: int
    width: int

    def __init__(self, data: dict[str, Any], tileset: Tileset):
        self.data = data
        self.tileset = tileset
        self.height = self.data["pxHei"]
        self.width = self.data["pxWid"]

        self.level_data = self.generate_level_data()

    def generate_level_data(self):
        level_data: list[LevelTile] = []

        for layer in self.data["layerInstances"]:

            if layer["__identifier"] == "AutoTiles":
                for tile in layer["autoLayerTiles"]:
                    level_data.append(
                        LevelTile.from_tileset_tile(
                            self.tileset.tiles[tile["t"]], tile["px"]
                        )
                    )

            if layer["__identifier"] == "Tiles":
                for tile in layer["gridTiles"]:
                    level_data.append(
                        LevelTile.from_tileset_tile(
                            self.tileset.tiles[tile["t"]], tile["px"]
                        )
                    )

        return level_data

from typing import Any
from nea_game.ldtk_world_loader.level_data import LevelData
from nea_game.ldtk_world_loader.level_tile import LevelTile
from nea_game.ldtk_world_loader.tileset import Tileset


class Level:
    height: int
    width: int

    def __init__(self, data: dict[str, Any], tileset: Tileset):
        self.data = data
        self.tileset = tileset
        self.height = self.data["pxHei"]
        self.width = self.data["pxWid"]
        self.level_data = self.generate_level_data()

    def generate_level_data(self) -> LevelData:
        tiles: list[LevelTile] = []
        player_position: tuple[int, int] = (-1, -1)

        for layer in self.data["layerInstances"]:
            match layer["__identifier"]:
                case "AutoTiles":
                    for tile in layer["autoLayerTiles"]:
                        tiles.append(
                            LevelTile.from_tileset_tile(
                                self.tileset.tiles[tile["t"]], tile["px"]
                            )
                        )

                case "Tiles":
                    for tile in layer["gridTiles"]:
                        tiles.append(
                            LevelTile.from_tileset_tile(
                                self.tileset.tiles[tile["t"]], tile["px"]
                            )
                        )
                case "Entities":
                    for entity_instance in layer["entityInstances"]:
                        match entity_instance["__identifier"]:
                            case "Player":
                                player_position = entity_instance["px"]
                            case _:
                                pass
                case _:
                    pass

        if player_position == (-1, -1):
            raise ValueError("Player Position is not specified")

        return {"tiles": tiles, "player_position": player_position}

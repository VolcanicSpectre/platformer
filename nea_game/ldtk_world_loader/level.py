from typing import Any
from nea_game.entity.level_finish import LevelFinish
from nea_game.ldtk_world_loader.level_data import LevelData
from nea_game.ldtk_world_loader.level_tile import LevelTile
from nea_game.ldtk_world_loader.tileset import Tileset


class Level:
    data: dict[str, Any]
    identifier: str
    tileset: Tileset
    height: int
    width: int
    level_data: LevelData

    def __init__(self, data: dict[str, Any], tileset: Tileset, chunk_size: int):
        self.data = data
        self.identifier: str = data["identifier"]
        self.tileset = tileset
        self.height = self.data["pxHei"]
        self.width = self.data["pxWid"]
        self.chunk_size = chunk_size
        self.level_data = self.generate_level_data()

    def generate_level_data(self) -> LevelData:
        tiles: list[LevelTile] = []
        chunks: dict[tuple[int, int], list[LevelTile]] = {}
        player_position: tuple[int, int] = (-1, -1)
        level_finish = None

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

                            case "Finish":
                                new_world = entity_instance["fieldInstances"][0][
                                    "__value"
                                ]
                                next_level_identifier = entity_instance[
                                    "fieldInstances"
                                ][1]["__value"]

                                level_finish = LevelFinish(
                                    entity_instance["px"],
                                    entity_instance["height"],
                                    entity_instance["width"],
                                    new_world,
                                    next_level_identifier,
                                )
                            case _:
                                pass
                case _:
                    pass

        if player_position == (-1, -1):
            raise ValueError("Player Position is not specified")
        if level_finish is None:
            raise ValueError("Level Finish is not specified")

        for tile in tiles:
            chunk_x = tile.rect.x // self.chunk_size
            chunk_y = tile.rect.y // self.chunk_size
            if (chunk_x, chunk_y) not in chunks:
                chunks[(chunk_x, chunk_y)] = [tile]
            else:
                chunks[(chunk_x, chunk_y)].append(tile)

        return {
            "chunks": chunks,
            "player_position": player_position,
            "level_finish": level_finish,
        }

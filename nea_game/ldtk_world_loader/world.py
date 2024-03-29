from json import load
from typing import Any
from pathlib import Path
from nea_game.ldtk_world_loader.level import Level
from nea_game.ldtk_world_loader.tileset import Tileset


class World:
    """A class that generates a world data based on world.json file from the LDTK editor
    """
    data: dict[str, Any]
    tileset: Tileset
    levels: dict[str, Level]

    def __init__(self, world_identifier: str, world_directory: Path, chunk_size: int):
        with (world_directory / f"{world_identifier}.json").open() as world_json:
            self.data = load(world_json)

        self.tileset = Tileset(self.data["defs"]["tilesets"][0], world_directory)

        levels = [
            Level(level_data, self.tileset, chunk_size)
            for level_data in self.data["levels"]
        ]
        self.levels = {level.identifier: level for level in levels}

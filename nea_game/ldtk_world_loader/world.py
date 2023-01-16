from json import load
from pathlib import Path
from nea_game.ldtk_world_loader.level import Level
from nea_game.ldtk_world_loader.tileset import Tileset


class World:
    def __init__(self, world_number: int, world_directory: Path):
        with (world_directory / f"{world_number}.json").open() as world_json:
            self.data = load(world_json)

        self.tileset = Tileset(self.data["defs"]["tilesets"][0], world_directory)

        self.levels: list[Level] = [
            Level(level_data, self.tileset) for level_data in self.data["levels"]
        ]

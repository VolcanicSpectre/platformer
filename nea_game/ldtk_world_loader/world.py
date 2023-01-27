from json import load
from pathlib import Path
from nea_game.ldtk_world_loader.level import Level
from nea_game.ldtk_world_loader.tileset import Tileset


class World:
    def __init__(self, world_identifier: str, world_directory: Path):
        with (world_directory / f"{world_identifier}.json").open() as world_json:
            self.data = load(world_json)

        self.tileset = Tileset(self.data["defs"]["tilesets"][0], world_directory)

        levels = [Level(level_data, self.tileset) for level_data in self.data["levels"]]
        self.levels: dict[str, Level] = {level.identifier: level for level in levels}

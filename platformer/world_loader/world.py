"""A class representation of world.json file from LDTK
"""

from json import load
from os import path

from platformer.config import PlatformerConfig
from platformer.world_loader.level import Level
from platformer.world_loader.tileset import Tileset


class World:
    def __init__(
        self, config: PlatformerConfig, world_num: int, current_level_num: int = 0
    ):
        self.world_num = world_num
        self.current_level_num = current_level_num

        with open(
            path.join(config.directories["worlds"], f"{self.world_num}.json"),
            encoding="utf-8",
        ) as world_json:
            self.data = load(world_json)

        self.tileset = Tileset(self.data["tilesets"][0], config.directories["worlds"])

        self.levels = [Level(level_data, self.tileset) for level_data in self.data["levels"]]

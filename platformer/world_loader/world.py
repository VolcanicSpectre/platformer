"""A class representation of world.json file from LDTK
"""

from json import load
from os import path
from level import Level
    
class World:
    def __init__(self, world_num: int, current_level_num: int=0):
        self.world_num = world_num
        self.current_level_num = current_level_num

        with open(path.join(WORLDS_FOLDER, f"{self.world_num}.json"), encoding="utf-8") as world_json:
            self.data = load(world_json)

        self.levels = [Level(level_data) for level_data in self.data["levels"]]
from typing import TypedDict
from nea_game.entity.level_finish import LevelFinish
from nea_game.ldtk_world_loader.level_tile import LevelTile


class LevelData(TypedDict):
    tiles: list[LevelTile]
    player_position: tuple[int, int]
    level_finish: LevelFinish

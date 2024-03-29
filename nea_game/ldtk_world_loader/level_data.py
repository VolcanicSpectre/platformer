from typing import TypedDict
from nea_game.entity.level_finish import LevelFinish
from nea_game.ldtk_world_loader.level_tile import LevelTile


class LevelData(TypedDict):
    """
    A typed dictionary to store the data about a level
    """
    chunks: dict[tuple[int, int], list[LevelTile]]
    player_position: tuple[int, int]
    level_finish: LevelFinish

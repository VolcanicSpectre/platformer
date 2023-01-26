from nea_game.entity.base_entity import BaseEntity


class LevelFinish(BaseEntity):
    def __init__(self, position: tuple[int, int], next_level_index: int):
        super().__init__(position)
        self.next_level_index = next_level_index

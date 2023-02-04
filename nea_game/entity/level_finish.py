from pygame import Rect
from nea_game.entity.base_entity import BaseEntity


class LevelFinish(BaseEntity):
    rect: Rect
    new_world: bool
    next_level_identifier: str

    def __init__(
        self,
        position: tuple[int, int],
        height: int,
        width: int,
        new_world: bool,
        next_level_identifier: str,
    ):
        super().__init__(position)
        self.rect = Rect(self.x, self.y, width, height)
        self.new_world = new_world
        self.next_level_identifier = next_level_identifier

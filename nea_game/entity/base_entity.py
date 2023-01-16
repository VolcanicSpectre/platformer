from nea_game.ldtk_world_loader.level_tile import LevelTile


class BaseEntity:
    x: float
    y: float
    level_data: list[LevelTile]
    def __init__(self, x: float, y: float, level_data: list[LevelTile]) -> None:
        """Provides a template for all entities

        Args:
            x (float): The x position of the entity
            y (float): The y position of the entity

        """
        self.x = x
        self.y = y

        self.level_data = level_data

    def update(self, dt: float) -> None:
        """Called each frame in order to update the entity"""

    
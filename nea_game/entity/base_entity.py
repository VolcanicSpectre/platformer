class BaseEntity:
    x: float
    y: float

    def __init__(self, position: tuple[int, int]) -> None:
        """Provides a template for all entities

        Args:
            x (float): The x position of the entity
            y (float): The y position of the entity

        """
        self.x, self.y = position

    def update(self, dt: float) -> None:
        """Called each frame in order to update the entity"""

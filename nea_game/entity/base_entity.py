class BaseEntity:
    def __init__(self, x: float, y: float) -> None:
        """Provides a template for all entities

        Args:
            x (float): The x position of the entity
            y (float): The y position of the entity

        """
        self.x = x
        self.y = y

    def update(self, dt: float) -> None:
        """Called each frame in order to update the entity"""

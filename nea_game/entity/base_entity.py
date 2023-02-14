class BaseEntity:
    x: float
    y: float

    def __init__(self, position: tuple[int, int]):
        self.x, self.y = position

    def update(self, delta_time: float):
        """Called each frame in order to update the entity"""

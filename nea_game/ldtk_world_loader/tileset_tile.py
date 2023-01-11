from pygame import Rect, Surface


class TilesetTile:
    def __init__(self, identifier: int, image: Surface, collision_type: int, size: int):
        self.identifier = identifier
        self.image = image
        self.collision_type = collision_type
        self.rect = Rect((0, 0), (size, size))
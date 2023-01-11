from pygame import Surface


class TilesetTile:
    def __init__(self, identifier: int, image: Surface, collision_type: int):
        self.identifier = identifier
        self.image = image
        self.collision_type = collision_type

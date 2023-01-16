from pygame.transform import scale
from pygame import Surface
from nea_game.ldtk_world_loader.collision_type import CollisionType


class TilesetTile:
    def __init__(
        self,
        identifier: int,
        image: Surface,
        collision_type: CollisionType,
        size: int,
        scale_factor: int,
    ):
        self.scale_factor = scale_factor
        self.identifier = identifier
        self.image = scale(image, (size * self.scale_factor, size * self.scale_factor))
        self.collision_type = collision_type
        self.rect = self.image.get_rect()

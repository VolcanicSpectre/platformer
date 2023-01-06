from pathlib import Path
from pygame.image import load
from pygame import Mask
from pygame import Rect
from pygame import Surface
from pygame.mask import from_surface


class Title:
    image: Surface
    rect: Rect
    mask: Mask

    def __init__(self, title_image_path: Path):
        self.image = load(title_image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.topleft = 0, 0

    def center_on_x_axis(self, x_axis_width: int):
        self.rect.x = (x_axis_width - self.rect.width) // 2

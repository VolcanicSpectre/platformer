from os.path import join

from pygame.image import load
from pygame import Mask
from pygame import Rect
from pygame import Surface
from pygame.mask import from_surface


class Button:

    passive_image: Surface
    active_image: Surface
    on_click_image: Surface
    current_image: Surface

    rect: Rect
    mask: Mask

    clicked: bool

    def __init__(self, path: str, x: int, y: int):
        self.passive_image = load(join(path, "0.png")).convert_alpha()
        self.active_image = load(join(path, "1.png")).convert_alpha()
        self.on_click_image = load(join(path, "2.png")).convert_alpha()
        self.current_image = self.passive_image

        self.rect = self.passive_image.get_rect()
        self.mask = from_surface(self.passive_image)
        self.rect.topleft = x, y

        self.clicked = False

    def update(self, mouse_pos: tuple[int, int], mouse_clicked: bool):
        """Updates the current_image attribute and the clicked flag

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse on the screen
            mouse_clicked (bool): A boolean value stating whether the mouse is clicked or not on the current frame
        """
        mouse_pos_x, mouse_pos_y = mouse_pos
        mouse_pos_in_mask = mouse_pos_x - self.rect.x, mouse_pos_y - self.rect.y
        self.clicked = False

        if self.rect.collidepoint(mouse_pos) and self.mask.get_at(mouse_pos_in_mask):
            if mouse_clicked:
                self.current_image = self.on_click_image
                self.clicked = True
            else:
                self.current_image = self.active_image
        else:
            self.current_image = self.passive_image

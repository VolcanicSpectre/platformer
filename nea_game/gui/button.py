from os.path import join
from pathlib import Path
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

    can_be_clicked: bool
    clicked: bool
    click_delay: float
    click_timer: float

    def __init__(self, path: Path):
        self.passive_image = load(join(path, "0.png")).convert_alpha()
        self.active_image = load(join(path, "1.png")).convert_alpha()
        self.on_click_image = load(join(path, "2.png")).convert_alpha()
        self.current_image = self.passive_image

        self.rect = self.passive_image.get_rect()
        self.mask = from_surface(self.passive_image)
        self.rect.topleft = 0, 0

        self.can_be_clicked = True
        self.clicked = False
        self.click_delay = 0.08
        self.click_timer = -1

    def update(self, mouse_pos: tuple[int, int], mouse_clicked: bool, dt: float):
        """Updates the current_image attribute and the clicked flag

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse on the screen
            mouse_clicked (bool): A boolean value stating whether the mouse is clicked or not on the current frame
        """
        mouse_pos_x, mouse_pos_y = mouse_pos
        mouse_pos_in_mask = mouse_pos_x - self.rect.x, mouse_pos_y - self.rect.y
        self.clicked = False

        if self.rect.collidepoint(mouse_pos) and self.mask.get_at(mouse_pos_in_mask):
            if mouse_clicked and self.can_be_clicked:
                self.current_image = self.on_click_image

                if self.click_timer == -1:
                    self.click_timer = 0
            else:
                self.current_image = self.active_image
        else:
            self.current_image = self.passive_image

        if self.click_timer > self.click_delay and self.can_be_clicked:
            self.clicked = True
            self.click_timer = -1

        if self.click_timer >= 0:
            self.click_timer += dt

    def center_on_x_axis(self, x_axis_width: int):
        self.rect.x = (x_axis_width - self.rect.width) // 2

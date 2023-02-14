from pathlib import Path
from pygame.image import load
from pygame.mask import from_surface
from pygame import Mask, Rect, Surface


class Slider:
    """
    A class that allows a slider to be used for the user to specify a valeu between two endpoints
    """
    passive_bar: Surface
    active_bar: Surface
    handle_image: Surface

    rect: Rect
    mask: Mask

    bar_rect: Rect
    handle_rect: Rect
    
    min_value: int
    max_value: int
    value: int

    dragging: bool

    def __init__(
        self,
        path: Path,
        min_value: int,
        max_value: int,
        value: int,
    ):

        self.passive_bar = load(path / "0.png")
        self.active_bar = load(path / "1.png")
        self.handle_image = load(path / "2.png")

        self.rect = self.passive_bar.get_rect()
        self.mask = from_surface(self.passive_bar)

        self.bar_rect = self.active_bar.get_rect()
        self.handle_rect = self.handle_image.get_rect()

        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.set_value(value)

        self.dragging = False

    def set_topleft(self, x: int, y: int):
        """Sets the topleft of both parts of the slider

        Args:
            x (int): The x position of the slider
            y (int): The y position of the slider
        """
        self.rect.topleft = x, y
        self.bar_rect.topleft = x - 1, y - 1

    def update(self, mouse_pos: tuple[int, int], mouse_clicked: bool):
        """Updates the value of the slider based on whether the slider is being dragged

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse on the screen
            mouse_clicked (bool): A boolean value stating whether the mouse is clicked or not on the current frame
        """
        mouse_pos_x, mouse_pos_y = mouse_pos
        mouse_pos_in_mask = mouse_pos_x - self.rect.x, mouse_pos_y - self.rect.y
        self.dragging = False

        self.dragging = (
            self.rect.collidepoint(mouse_pos)
            and self.mask.get_at(mouse_pos_in_mask) == 1
            and mouse_clicked
        )

        if self.dragging:
            self.set_value(int(mouse_pos_x - self.bar_rect.left))

    @property
    def current_image(self) -> Surface:
        """Returns one surface showing the current value of the slider

        Returns:
            Surface: The current image of the slider
        """
        current_image = self.passive_bar.copy()
        current_image.blit(self.passive_bar, self.bar_rect.topleft)
        current_image.blit(
            self.active_bar.subsurface(
                Rect(
                    0,
                    0,
                    (self.value / self.max_value) * self.bar_rect.width,
                    self.bar_rect.height,
                )
            ),
            (1, 1),
        )
        current_image.blit(
            self.handle_image,
            (
                int((self.value / self.max_value) * self.bar_rect.width)
                - self.handle_rect.width
                + 1,
                1,
            ),
        )
        return current_image

    def set_value(self, value: int):
        """Sets the value of the slider

        Args:
            value (int): The new value of the slider
        """
        self.value = max(self.min_value, min(self.max_value, value))

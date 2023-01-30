from pathlib import Path
from pygame.image import load
from pygame.mask import from_surface
from pygame import Rect, Surface


class Slider:
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
        self.rect.topleft = x, y
        self.bar_rect.topleft = x - 1, y - 1

    def update(self, mouse_pos: tuple[int, int], mouse_clicked: bool, dt: float):
        mouse_pos_x, mouse_pos_y = mouse_pos
        mouse_pos_in_mask = mouse_pos_x - self.rect.x, mouse_pos_y - self.rect.y
        self.dragging = False

        self.dragging = (
            self.rect.collidepoint(mouse_pos)
            and self.mask.get_at(mouse_pos_in_mask)
            and mouse_clicked
        )

        if self.dragging:
            self.set_value(int(mouse_pos_x - self.bar_rect.left))

    @property
    def current_image(self) -> Surface:
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
        self.value = max(self.min_value, min(self.max_value, value))

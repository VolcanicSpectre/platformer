from pathlib import Path
import pygame
from pygame.event import Event
from pygame.image import load
from pygame.key import name as get_key_name
from pygame.mask import Mask, from_surface
from pygame import Rect, Surface


class ActionButton:
    passive_image: Surface
    active_image: Surface
    current_image: Surface

    rect: Rect
    mask: Mask

    key: int
    key_images_path: Path
    key_image: Surface

    clicked: bool
    click_time: float
    click_timer: float

    def __init__(self, path: Path, key_images_path: Path, key: int):
        self.passive_image = load(path / "0.png")
        self.active_image = load(path / "1.png")
        self.current_image = self.passive_image

        self.rect = self.passive_image.get_rect()
        self.mask = from_surface(self.passive_image)
        self.rect.topleft = 0, 0

        self.key_images_path = key_images_path
        self.initial_update_key_image(key)

        self.clicked = False
        self.click_time = 5
        self.click_timer = -1

    def update(
        self,
        mouse_pos: tuple[int, int],
        mouse_clicked: bool,
        delta_time: float,
        other_binds: list[int] | None = None,
        event: Event | None = None,
    ):
        """Updates the current_image attribute and the clicked flag

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse on the screen
            mouse_clicked (bool): A boolean value stating whether the mouse is clicked or not on the current frame
        """
        mouse_pos_x, mouse_pos_y = mouse_pos
        mouse_pos_in_mask = mouse_pos_x - self.rect.x, mouse_pos_y - self.rect.y
        self.clicked = False

        if (
            self.rect.collidepoint(mouse_pos)
            and self.mask.get_at(mouse_pos_in_mask)
            and mouse_clicked
            or self.click_timer >= 0
        ):
            self.current_image = self.active_image
            self.clicked = True
            self.click_timer = max(0, self.click_timer)

        else:
            self.current_image = self.passive_image

        if self.click_timer >= 0:
            self.click_timer += delta_time
            if event:
                if event.type == pygame.KEYDOWN:
                    if self.update_key_image(event.key, other_binds):
                        self.click_timer = -1

        if self.click_timer >= self.click_time:
            self.click_timer = -1

    def initial_update_key_image(self, key: int) -> bool:
        """Updates the key image for the initial key bind

        Args:
            key (int): The int value for the key

        Returns:
            bool: Whether the key image was updated successfully
        """
        key_name = get_key_name(key).replace(" ", "_")
        try:
            self.key_image = load(self.key_images_path / f"{key_name}-key.png")
        except FileNotFoundError:
            return False

        handle_key_image = self.key_image.copy()

        clip_rect = Rect(
            self.key_image.get_width() // 2,
            0,
            self.key_image.get_width() // 2,
            self.key_image.get_height(),
        )

        handle_key_image.set_clip(clip_rect)
        self.key = key
        self.key_image = self.key_image.subsurface(
            handle_key_image.get_clip()
        ).convert_alpha()
        return True

    def update_key_image(self, key: int, other_binds: list[int] | None = None) -> bool:
        """Updates the key image given a keybind and a list of the other key binds

        Args:
            key (int): The int value of the key
            other_binds (list[int] | None, optional): The other key bindings. Defaults to None.

        Returns:
            bool: Whether the key image was updated successfully
        """
        if other_binds is None:
            return False

        if key in other_binds:
            return False

        key_name = get_key_name(key).replace(" ", "_")
        try:
            self.key_image = load(self.key_images_path / f"{key_name}-key.png")
        except FileNotFoundError:
            return False

        handle_key_image = self.key_image.copy()

        clip_rect = Rect(
            self.key_image.get_width() // 2,
            0,
            self.key_image.get_width() // 2,
            self.key_image.get_height(),
        )

        handle_key_image.set_clip(clip_rect)
        self.key = key
        self.key_image = self.key_image.subsurface(
            handle_key_image.get_clip()
        ).convert_alpha()
        return True

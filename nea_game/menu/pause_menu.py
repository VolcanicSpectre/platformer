from __future__ import annotations
from os import listdir
from pathlib import Path
import typing
import pygame
from pygame.mouse import get_pos as get_mouse_pos, get_pressed as get_mouse_pressed
from pygame import Surface
from nea_game.gui.button import Button
from nea_game.gui.window import Window

if typing.TYPE_CHECKING:
    from nea_game.nea_game import NeaGame


class Pause(Window):
    buttons: dict[str, Button]

    def __init__(
        self, parent: NeaGame, screen: Surface, display_surface: Surface, path: Path
    ):
        super().__init__(screen, display_surface)
        self.parent = parent

        self.buttons = {}
        for button in listdir(path / "buttons"):
            self.buttons[button] = Button(path / "buttons" / button)

        self.buttons["resume"].rect.y = 115
        self.buttons["resume"].center_on_x_axis(self.display_surface.get_width())

        self.buttons["exit"].rect.y = 150
        self.buttons["exit"].center_on_x_axis(self.display_surface.get_width())

    def update(self, dt: float):
        mouse_pos: tuple[int, int] = get_mouse_pos()
        scaled_mouse_pos: tuple[int, int] = (
            mouse_pos[0] // self.scale_factor,
            mouse_pos[1] // self.scale_factor,
        )
        mouse_clicked = get_mouse_pressed()[0]

        for button in self.buttons.values():
            button.update(scaled_mouse_pos, mouse_clicked, dt)

        if self.buttons["resume"].clicked:
            self.parent.sound_manager.play_sound("click")
            self.parent.show_window("game")

        if self.buttons["exit"].clicked:
            self.parent.sound_manager.play_sound("click")
            self.parent.show_window("main_menu")

    def draw(self):
        self.display_surface.fill((8, 169, 252))

        for button in self.buttons.values():
            self.display_surface.blit(button.current_image, button.rect.topleft)

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        pygame.display.flip()

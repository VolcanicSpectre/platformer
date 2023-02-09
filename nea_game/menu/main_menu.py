from __future__ import annotations
from os import listdir
from pathlib import Path
from sys import exit as sys_exit
import typing
import pygame
from pygame.image import load
from pygame.mouse import get_pos as get_mouse_pos, get_pressed as get_mouse_pressed
from pygame import Surface
from nea_game.menu.level_selection import LevelSelection
from nea_game.menu.settings_menu import Settings
from nea_game.menu.background_layer import BackgroundLayer
from nea_game.gui.button import Button
from nea_game.gui.title import Title
from nea_game.gui.window import Window

if typing.TYPE_CHECKING:
    from nea_game.nea_game import NeaGame


class MainMenu(Window):
    parent: NeaGame

    buttons: dict[str, Button]
    background_layers: list[BackgroundLayer]
    splash_screen_opacity: int
    title: Titl     e

    def __init__(
        self,
        parent: NeaGame,
        screen: Surface,
        display_surface: Surface,
        path: Path,
        background_image_layers_path: Path,
        background_transparency_percentage: float = 1,
    ):
        super().__init__(screen, display_surface)
        self.parent = parent
        
        self.buttons = {}

        self.background_layers = [
            BackgroundLayer(load(background_image_layers_path / filename))
            for filename in sorted(listdir(background_image_layers_path))
            if filename.endswith(".png") and filename != "-1.png"
        ]
        self.set_background_transparency_percentage(background_transparency_percentage)

        self.title = Title(path / "title.png")
        self.title.rect.y = 0
        self.title.center_on_x_axis(self.display_surface.get_width())

        for button in listdir(path / "buttons"):
            self.buttons[button] = Button(path / "buttons" / button)

        self.buttons["play_game"].rect.y = 115
        self.buttons["play_game"].center_on_x_axis(self.display_surface.get_width())

        self.buttons["settings"].rect.y = 150
        self.buttons["settings"].center_on_x_axis(self.display_surface.get_width())

        self.buttons["exit"].rect.y = 185
        self.buttons["exit"].center_on_x_axis(self.display_surface.get_width())

    def reload(self):
        super().reload()
        self.parent.sound_manager.set_bgm_volume(self.parent.config.music_volume)
        self.parent.sound_manager.set_sfx_volume(self.parent.config.sfx_volume)

    def update(self, delta_time: float):
        mouse_pos: tuple[int, int] = get_mouse_pos()
        scaled_mouse_pos: tuple[int, int] = (
            mouse_pos[0] // self.scale_factor,
            mouse_pos[1] // self.scale_factor,
        )
        mouse_clicked = get_mouse_pressed()[0]
        for button in self.buttons.values():
            button.update(scaled_mouse_pos, mouse_clicked, delta_time)

        if self.buttons["play_game"].clicked:
            self.parent.sound_manager.play_sound("click")
            window = LevelSelection(
                self.parent,
                self.screen,
                self.display_surface,
                self.parent.config.directories["gui"] / "level_selection",
            )
            self.parent.windows["level_selection"] = window
            self.parent.show_window("level_selection")

        if self.buttons["settings"].clicked:
            self.parent.sound_manager.play_sound("click")
            window = Settings(
                self.parent,
                self.screen,
                self.display_surface,
                self.parent.config.directories["gui"] / "settings",
                self.parent.config.key_bindings,
            )
            self.parent.windows["settings"] = window
            self.parent.show_window("settings")

        if self.buttons["exit"].clicked:
            self.parent.sound_manager.play_sound("click")
            pygame.quit()
            sys_exit()

    def draw(self):
        self.display_surface.fill((0, 0, 0))

        self.display_surface.blit(self.background_layers[0].image, (0, 0))
        self.display_surface.blit(self.background_layers[1].get_new_sub_image(), (0, 0))
        self.display_surface.blit(self.background_layers[2].image, (0, 0))
        self.display_surface.blit(self.background_layers[3].get_new_sub_image(), (0, 0))
        self.display_surface.blit(self.background_layers[4].get_new_sub_image(), (0, 0))
        self.display_surface.blit(self.background_layers[5].get_new_sub_image(), (0, 0))

        self.display_surface.blit(self.title.image, self.title.rect.topleft)
        for button in self.buttons.values():
            self.display_surface.blit(button.current_image, button.rect.topleft)

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        pygame.display.flip()

    def set_background_transparency_percentage(self, transparency_percentage: float):
        """Sets the transparency for the background image as a number between 0 and 255 from a percenatge

        Args:
            transparency_percentage (float): The percentage transparency for the back ground image (0= fully transparent, 1=fully opaque)

        Raises:
            ValueError: Raised when the transparency percentage is not between 0 and 1 inclusive
        """
        if transparency_percentage < 0 or transparency_percentage > 1:
            raise ValueError("Percentage must be between 0 and 1 inlcusive")
        for layer in self.background_layers:
            layer.image.set_alpha(int(255 * transparency_percentage))

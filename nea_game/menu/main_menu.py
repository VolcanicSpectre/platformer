from os import listdir, path
from pathlib import Path
from sys import exit as sys_exit
from time import sleep
import pygame
from pygame.image import load
from pygame import Surface
from nea_game.menu.splash_screen_layer import SplashScreenLayer
from nea_game.gui.button import Button
from nea_game.gui.title import Title
from nea_game.gui.window import Window


class MainMenu(Window):
    splash_screen_layers: list[SplashScreenLayer]
    splash_screen_opacity: int
    title: Title

    def __init__(
        self,
        screen: Surface,
        display_surface: Surface,
        title_image_path: Path,
        splash_screen_image_layers_path: Path,
        button_folder_path: Path,
        splash_screen_transparency_percentage: float = 1,
    ):
        super().__init__(screen, display_surface)

        self.title_image = load(title_image_path).convert_alpha()

        self.splash_screen_layers = [
            SplashScreenLayer(
                load(path.join(splash_screen_image_layers_path, filename))
            )
            for filename in sorted(listdir(splash_screen_image_layers_path))
            if filename.endswith(".png") and filename != "-1.png"
        ]
        self.set_splash_screen_transparency_percentage(
            splash_screen_transparency_percentage
        )

        self.title = Title(title_image_path)
        self.title.rect.y = 0
        self.title.center_on_x_axis(self.display_surface.get_width())

        for button in listdir(button_folder_path):
            self.buttons[button] = Button(button_folder_path / button)

        self.buttons["play_game"].rect.y = 115
        self.buttons["play_game"].center_on_x_axis(self.display_surface.get_width())

        self.buttons["settings"].rect.y = 150
        self.buttons["settings"].center_on_x_axis(self.display_surface.get_width())

        self.buttons["exit"].rect.y = 185
        self.buttons["exit"].center_on_x_axis(self.display_surface.get_width())

    def update(self, dt: float):
        super().update(dt)
        if self.buttons["exit"].clicked:
            pygame.quit()
            sys_exit()

    def draw(self):
        self.display_surface.fill((0, 0, 0))

        self.display_surface.blit(self.splash_screen_layers[0].image, (0, 0))
        self.display_surface.blit(
            self.splash_screen_layers[1].get_new_sub_image(), (0, 0)
        )
        self.display_surface.blit(self.splash_screen_layers[2].image, (0, 0))
        self.display_surface.blit(
            self.splash_screen_layers[3].get_new_sub_image(), (0, 0)
        )
        self.display_surface.blit(
            self.splash_screen_layers[4].get_new_sub_image(), (0, 0)
        )
        self.display_surface.blit(
            self.splash_screen_layers[5].get_new_sub_image(), (0, 0)
        )

        self.display_surface.blit(self.title.image, self.title.rect.topleft)
        for button in self.buttons.values():
            self.display_surface.blit(button.current_image, button.rect.topleft)

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        pygame.display.flip()

    def set_splash_screen_transparency_percentage(self, transparency_percentage: float):
        """Sets the transparency for the splash screen image as a number between 0 and 255 from a percenatge

        Args:
            transparency_percentage (float): The percentage transparency for the splash screen image (0= fully transparent, 1=fully opaque)

        Raises:
            ValueError: Raised when the transparency percentage is not between 0 and 1 inclusive
        """
        if transparency_percentage < 0 or transparency_percentage > 1:
            raise ValueError("Percentage must be between 0 and 1 inlcusive")
        for layer in self.splash_screen_layers:
            layer.image.set_alpha(int(255 * transparency_percentage))

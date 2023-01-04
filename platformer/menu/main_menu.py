from os import listdir, path
from pathlib import Path
import pygame
from pygame.image import load
from pygame import Surface
from platformer.menu.splash_screen_layer import SplashScreenLayer
from platformer.gui.window import Window


class MainMenu(Window):
    splash_screen_layers: list[SplashScreenLayer]
    splash_screen_opacity: int

    def __init__(
        self,
        screen: Surface,
        display_surface: Surface,
        splash_screen_image_layers_path: Path,
        splash_screen_transparency_percentage: float = 1,
    ):
        super().__init__(screen, display_surface)

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

    def draw(self):
        self.display_surface.fill((0, 0, 0))

        for button in self.buttons:
            self.display_surface.blit(button.current_image, button.rect.topleft)

        self.display_surface.blit(self.splash_screen_layers[0].image, (0, 0))
        self.display_surface.blit(self.splash_screen_layers[1].get_new_sub_image(), (0, 0))
        self.display_surface.blit(self.splash_screen_layers[2].image, (0, 0))
        self.display_surface.blit(self.splash_screen_layers[3].get_new_sub_image(), (0, 0))
        self.display_surface.blit(self.splash_screen_layers[4].get_new_sub_image(), (0, 0))
        self.display_surface.blit(self.splash_screen_layers[5].get_new_sub_image(), (0, 0))
        
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

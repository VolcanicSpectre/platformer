from typing import Type
import pygame
from pygame import Surface
from platformer.gui.window import Window


class Root:
    screen: Surface
    active_window: Window
    windows: dict[Type[Window], Window]

    def __init__(
        self,
        screen_resolution: tuple[int, int],
        display_surafce_resolution: tuple[int, int],
    ):

        self.screen = pygame.display.set_mode(screen_resolution)
        self.display_surface = Surface(display_surafce_resolution)

        self.windows = {}

    def show_window(self, window: Type[Window]):
        self.active_window = self.windows[window]

    def update(self):
        self.active_window.update()
        self.active_window.draw()

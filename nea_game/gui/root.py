import pygame
from pygame.event import Event
from pygame import Surface
from nea_game.gui.window import Window
from nea_game.game.engine import Engine


class Root:
    screen: Surface
    active_window: Window
    windows: dict[str, Window]
    engine: Engine

    def __init__(
        self,
        screen_resolution: tuple[int, int],
        display_surafce_resolution: tuple[int, int],
        fps: int,
    ):

        pygame.init()
        self.screen = pygame.display.set_mode(screen_resolution)
        self.display_surface = Surface(display_surafce_resolution)
        self.engine = Engine(fps)
        self.windows = {}

    def show_window(self, window: str):
        self.active_window = self.windows[window]

    def update(self):
        self.engine.update()
        self.active_window.update(self.engine.dt)
        self.active_window.draw()

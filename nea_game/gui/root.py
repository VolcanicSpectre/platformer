import pygame
from pygame import Surface
from nea_game.gui.window import Window
from nea_game.game.engine import Engine
from nea_game.sound_manager import SoundManager


class Root:
    screen: Surface
    active_window: Window
    engine: Engine
    sound_manager: SoundManager
    windows: dict[str, Window]

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
        self.sound_manager = SoundManager()
        self.windows = {}

    def show_window(self, window: str):
        self.active_window = self.windows[window]
        self.active_window.reload()

    def update(self):
        self.engine.update()
        self.active_window.update(self.engine.delta_time)
        self.active_window.draw()

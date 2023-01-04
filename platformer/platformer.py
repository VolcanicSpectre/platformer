from sys import exit as sys_exit
import pygame
from platformer.config import PlatformerConfig
from platformer.gui.root import Root
from platformer.menu.main_menu import MainMenu


class Platformer(Root):
    def __init__(self, config: PlatformerConfig):
        self.config = config
        super().__init__(
            self.config.resoloution,
            self.config.internal_resoloution,
            self.config.internal_fps,
        )
        self.windows[MainMenu] = MainMenu(
            self.screen, self.display_surface, config.directories["background"]
        )

        self.show_window(MainMenu)
        self.engine

    def update(self):
        self.get_events()
        super().update()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys_exit(0)

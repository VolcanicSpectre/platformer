from sys import exit as sys_exit
import pygame
from nea_game.config import NeaGameConfig
from nea_game.gui.root import Root
from nea_game.menu.main_menu import MainMenu


class Platformer(Root):
    def __init__(self, config: NeaGameConfig):
        self.config = config
        super().__init__(
            self.config.resoloution,
            self.config.internal_resoloution,
            self.config.internal_fps,
        )
        self.show_window(MainMenu)

        self.windows[MainMenu] = MainMenu(
            self.screen,
            self.display_surface,
            self.config.directories["background"],
            self.config.directories["buttons"],
            self.config.directories["assets"] / "title.png",
        )

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

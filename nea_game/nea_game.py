from sys import exit as sys_exit
from pygame.event import Event
import pygame
from nea_game.config import NeaGameConfig
from nea_game.gui.root import Root
from nea_game.menu.main_menu import MainMenu


class NeaGame(Root):
    def __init__(self, config: NeaGameConfig):
        self.config = config

        pygame.display.set_caption("NEA Game")
        # pygame.display.set_icon()
        super().__init__(
            self.config.resoloution,
            self.config.internal_resoloution,
            self.config.fps,
        )
        self.windows["main_menu"] = MainMenu(
            self,
            self.screen,
            self.display_surface,
            config.directories["assets"] / "title.png",
            config.directories["background"] / "sky_mountain",
            config.directories["buttons"] / "main_menu",
        )

        self.show_window("main_menu")

    def update(self):
        self.get_events()
        super().update()

    def get_events(self):
        events: list[Event]
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys_exit()
            else:
                events.append(event)
        self.active_window.event_handler(events)

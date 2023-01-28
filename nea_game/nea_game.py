from typing import Callable
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

        self.transition: None | Callable[[], None]
        self.transition_start_radius = 0
        self.transition_time = 0
        self.transition_circle_centre = (0, 0)
        self.current_transition_frame = 0
        self.is_transitioning = False
        self.is_transition_done = False

        self.show_window("main_menu")

    def show_window(self, window: str):
        super().show_window(window)
        self.is_transitioning = False
        self.is_transition_done = False

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

    def set_transitioning(
        self,
        transition: Callable[[], None],
        transition_time: float,
        circle_centre: tuple[int, int],
    ):
        self.is_transitioning = True
        self.is_transition_done = False
        self.transition = transition

        circle_x, circle_y = circle_centre

        self.transition_time = transition_time
        self.transition_circle_centre = circle_centre

        match transition:
            case self.transition_circle_out:
                self.transition_start_radius = max(
                    max(circle_x, self.screen.get_width() - circle_x),
                    max(circle_y, self.screen.get_height() - circle_y),
                )
                self.current_transition_frame = self.transition_time * self.engine.fps

            case self.transition_circle_in:
                self.transition_start_radius = max(
                    max(circle_x, self.screen.get_width() - circle_x),
                    max(circle_y, self.screen.get_height() - circle_y),
                )
                self.current_transition_frame = 0

            case _:
                pass

    def run_transition(self):
        if self.transition is not None:
            self.transition()

    def transition_circle_out(self):
        surface = pygame.Surface(self.screen.get_size())
        radius = (
            self.transition_start_radius / (self.transition_time * self.engine.fps)
        ) * self.current_transition_frame
        pygame.draw.circle(surface, "red", self.transition_circle_centre, radius)
        surface.set_colorkey("red")
        self.screen.blit(surface, (0, 0))
        self.current_transition_frame -= 1
        if self.current_transition_frame <= 0:
            self.is_transitioning = False
            self.is_transition_done = True

    def transition_circle_in(self):
        surface = pygame.Surface(self.screen.get_size())
        radius = (
            self.transition_start_radius / (self.transition_time * self.engine.fps)
        ) * self.current_transition_frame
        pygame.draw.circle(surface, "red", self.transition_circle_centre, radius)
        surface.set_colorkey("red")
        self.screen.blit(surface, (0, 0))
        self.current_transition_frame += 1

        if self.current_transition_frame >= self.transition_time * self.engine.fps:
            self.is_transitioning = False
            self.is_transition_done = True

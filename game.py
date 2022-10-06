import pstats
from sys import exit

import pygame
from constants import *
from engine import Engine
from level import Level


class Game:
    """
    Provides an interface for creating a game with levels and managing the game locgic
    """
    def __init__(self, pr):
        self.pr = pr
        self.current_level_num = 0
        self.current_level = None
        self.engine = Engine()

    def start(self, screen, display_surface):
        """Creates a level and starts the game

        Args:
            screen (pygame.Surface): the screen that the will display the scaled version of display_surface
            display_surface (pygame.Surface): the surface that will contain all of the render_objects
        """
        self.create_level(screen, display_surface)

    def update(self):
        """Updates the engine and if a level exists then the level is updated
        """
        pygame.display.set_caption(
            "{:.2f}".format(self.engine.clock.get_fps()))
        self.engine.update()
        self.events()
        if self.current_level is not None:
            self.current_level.global_update()

    def events(self):
        """Provides a general event manager, if the events are not detected here then the events are sent to the level's event manager
        """
        for event in pygame.event.get():
            if self.current_level is not None:
                self.current_level.event_handler(event)

            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if DEBUG:
                    stats = pstats.Stats(self.pr)
                    stats.sort_stats(pstats.SortKey.TIME)
                    stats.dump_stats(filename=DEBUG_FILENAME)

                pygame.quit()
                exit(0)

    def create_level(self, screen, display_surface):
        """Assigns a level object to self.current_level

        Args:
            screen (pygame.Surface): _description_
            display_surface (pygame.Surface): _description_
        """
        self.current_level = Level(
            self.engine, self.current_level_num, screen, display_surface)

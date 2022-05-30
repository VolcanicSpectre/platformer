import pygame
import cProfile
import pstats

from sys import exit
from constants import *

from engine import Engine
from level import Level


class Game:
    def __init__(self, pr):
        self.pr = pr
        self.current_level_num = 0
        self.current_level = None
        self.engine = Engine()

    def start(self, screen, display_surface):
        self.create_level(screen, display_surface)

    def update(self):
        pygame.display.set_caption(
            "{:.2f}".format(self.engine.clock.get_fps()))
        self.engine.update_dt()
        self.events()
        if self.current_level != None:
            self.current_level.global_update()

    def events(self):
        for event in pygame.event.get():
            if self.current_level != None:
                self.current_level.event_handler(event)

            if event.type == pygame.QUIT:
                if DEBUG:
                    stats = pstats.Stats(self.pr)
                    stats.sort_stats(pstats.SortKey.TIME)
                    stats.dump_stats(filename="s.prof")

                pygame.quit()
                exit(0)

    def create_level(self, screen, display_surface):
        self.current_level = Level(
            self.engine, self.current_level_num, screen, display_surface)

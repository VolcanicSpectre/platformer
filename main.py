import cProfile

import pygame

from constants import *
from game import Game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
display_surface = pygame.Surface((DS_WIDTH, DS_HEIGHT))


def main(pr=None):
    game = Game(pr)
    running = True
    game.start(screen, display_surface)
    frame = 0
    while running:
        game.update()
        print()
        frame += 1


if __name__ == "__main__":
    if DEBUG:
        with cProfile.Profile() as pr:
            main(pr)
    else:
        main()

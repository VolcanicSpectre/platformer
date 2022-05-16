import sys
from os import path
import pygame



from constants import *
from game import Game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
display_surface = pygame.Surface([DS_WIDTH , DS_HEIGHT])



def main():
    game = Game()
    running = True
    game.start()
    while running:
        game.update()

if __name__ == '__main__':
        main()










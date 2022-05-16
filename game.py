import pygame
from sys import exit
from constants import *

from engine import Engine
from level import Level

class Game:
    def __init__(self):
        self.current_level_num = 0
        self.current_level = None
        self.engine = Engine()
    
    def start(self):
        self.create_level(self.engine)

    def update(self):
        self.engine.clock.tick(FPS)
        self.engine.update_dt()
        self.events()
        if self.current_level != None:
            self.current_level.global_update()
    
    def events(self):
        for event in pygame.event.get():   
            if self.current_level != None:
                self.current_level.event_handler(event)
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

    def create_level(self):
        self.current_level = Level(self.current_level_num)
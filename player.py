import pygame
from constants import *
from states import States
from entity import Entity, load_assets

class Player(Entity):       
    def event_handler(self, event):   
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_RIGHT: self.events["right"] = True
                case pygame.K_LEFT: self.events["left"] = True
                case pygame.K_UP: self.events["up"] = True
                case pygame.K_DOWN: self.events["down"] = True
            
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_RIGHT: self.events["right"] = False
                case pygame.K_LEFT: self.events["left"] = False
                case pygame.K_UP: self.events["up"] = False
                case pygame.K_DOWN: self.events["down"] = False
        

        new_state = self.state.handle_inputs()

        if new_state: self.state = new_state

    
import pygame
from states import States


class Player:
    def __init__(self, x, y):
        self.state = States.IDLE
        
        self.image = pygame.Surface(self.size.copy())
        self.image.fill("red")
        self.rect = pygame.Rect(self.pos[0] , self.pos[1], self.size[0], self.size[1])
        self.events = {"right":False , "left":False , "up":False}
        
        self.x, self.y = x, y
        self.size = [8, 16]
        self.velocity = pygame.Vector2(0, 0)
        
        self.MAXRUN = 4
        
        self.ACCELRUN = 0.07
        self.DECELRUN = 0.05
        
        self.TURNPOWER = 0.5
        self.STOPPOWER = 0.5
        self.ACCELPOWER = 0.5
        
        self.JUMPHEIGHT = 50
        self.JUMPDISTANCE = 50
        self.INIT_JUMP_VELOCITY = ((2*self.jump_height*self.MAXRUN) / self.jump_distance) * -1
        self.INIT_GRAVITY = ((2*self.jump_height*self.MAXRUN**2) / self.jump_distance**2)
        self.FINAL_GRAVITY = ((2*self.jump_height*self.MAXRUN**2) / (self.jump_distance ** 2)*1.2)
        
        self.air_timer = 0
        
    
    def event_handler(self):  
        
        new_state = self.state.handle_inputs()
        if new_state: self.state = new_state

    
    def update_x(self, dt):
        new_state = self.state.process_x_movement(dt)
        if new_state: self.state = new_state
    
    def update_y(self, dt):
        new_state = self.state.process_y_movement(dt)
        if new_state: self.state = new_state

    @property
    def direction(self):
        if self.key_pressed["right"]: return 1
        elif self.key_pressed["left"]: return -1
        else: return 0
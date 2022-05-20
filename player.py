import pygame
from math import copysign
from functools import partial
from constants import *
from states import PlayerStates
sign = partial(copysign, 1)

class Player:
    def __init__(self, x, y):
        self.state = PlayerStates.IDLE
        
        self.x, self.y = x, y
        self.size = [8, 16]
        self.vel = pygame.Vector2(0, 0)
        self.MAXRUN = 4
        
        self.ACCELRUN = 0.07
        self.DECELRUN = 0.05
        
        self.TURNPOWER = 0.5
        self.STOPPOWER = 0.5
        self.ACCELPOWER = 0.5
        
        
        self.JUMPHEIGHT = 50
        self.JUMPDISTANCE = 50
        self.INIT_JUMP_VEL = ((2*self.jump_height*self.MAXRUN) / self.jump_distance) * -1
        self.INIT_GRAVITY = ((2*self.jump_height*self.MAXRUN**2) / self.jump_distance**2)
        self.FINAL_GRAVITY = ((2*self.jump_height*self.MAXRUN**2) / (self.jump_distance ** 2)*1.2)
        
        self.air_timer = 0
        self.image = pygame.Surface(self.size.copy())
        self.image.fill("red")
        self.rect = pygame.Rect(self.pos[0] , self.pos[1], self.size[0], self.size[1])
        self.key_pressed = {"right":False , "left":False , "up":False}
    
    def event_handler(self, event):   
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_RIGHT: self.key_pressed["right"] = True
                case pygame.K_LEFT: self.key_pressed["left"] = True
                case pygame.K_UP: self.key_pressed["up"] = True
                case pygame.K_DOWN: self.key_pressed["down"] = True
            
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_RIGHT: self.key_pressed["right"] = False
                case pygame.K_LEFT: self.key_pressed["left"] = False
                case pygame.K_UP: self.key_pressed["up"] = False
                case pygame.K_DOWN: self.key_pressed["down"] = False
    
    def calculate_x_vel(self, dt):
        target_speed = self.MAXRUN * self.x_move_input
        u = self.velocity.x
        
        if abs(target_speed) > 0.01:
            a = self.x_accel
            if not self.grounded:
                a *= 0.01
        else:
            a = self.x_deccel
            if not self.grounded:
                a *= 0.6
        
        if (self.velocity.x > target_speed and target_speed > 0.01) or (self.velocity.x < target_speed and target_speed < -0.01):
            accel_rate = 0

        
        if abs(target_speed) < 0.01:
            vel_power = self.stop_power
        elif abs(self.velocity.x) > 0 and sign(target_speed) != sign(self.velocity.x):
            vel_power = self.turn_power
        else:
            vel_power = self.accel_power


        v = (a*dt) ** vel_power
        
        if self.x_move_input > 0:
            return min(u + v, target_speed)
        if self.x_move_input < 0:
            return max(u + v*self.x_move_input, target_speed)
        else:
            if sign(self.velocity.x) == -1:
                return min(self.velocity.x - (v*-1), target_speed*self.x_move_input)
            else:
                return max(self.velocity.x - v, target_speed*self.x_move_input)
    
    def update_x(self, dt): 
        if self.key_pressed["right"]:
            self.x_move_input = 1
        elif self.key_pressed["left"]:
            self.x_move_input = -1
        else:
           self.x_move_input = 0
        
        self.velocity.x = self.calculate_x_velocity(dt)
        self.x += self.velocity.x
        self.rect.x = self.x
    
    def update_y(self):
        if self.key_pressed["up"] and self.air_frame < 4:
            self.velocity.y = self.initial_jump_vel
            self.air_frame = 1
            self.key_pressed["up"] = False
        
        if self.velocity.y > 0:
            self.velocity.y += self.final_gravity
        else:
            self.velocity.y += self.inital_gravity       
        
        self.y += self.velocity.y
        self.rect.y = self.y
    
    def get_direction(self):
        if self.key_pressed["right"]: return 1
        else: return 0
from enum import Enum, auto 
from math import copysign
from functools import partial

sign = partial(copysign, 1)
class PlayerStates(Enum):
    NULL = 0
    IDLE = 1
    RUN = 2
    DASH = 3
    JUMP = 4
    FALL = 5

class State:
    def __init__(self, player): self.player = player
    
    def handle_inputs(self, keys): return PlayerStates.NULL
    
    def process_x_movement(self, dt): return PlayerStates.NULL

    def process_y_movement(self, dt): return PlayerStates.NULL



class IdleState(State):
    def handle_inputs(self, keys):
        if self.player.get_direction(): return PlayerStates.RUN
        if keys["up"]: return PlayerStates.JUMP
        
        return PlayerStates.NULL
    
    def process_y_movement(self, dt):
        self.player.velocity.y += self.player.FINAL_GRAVITY * dt
        if not self.player.grounded: return PlayerStates.FALL

        return PlayerStates.NULL

class RunState(State):
    def handle_inputs(keys):
        if keys["up"]: return PlayerStates.JUMP
        return PlayerStates.NULL
        #TODO add dash
    
    def process_x_movement(self, dt):
        dir = self.player.get_direction()
        
        if not dir: return PlayerStates.IDLE

        self.player.velocity.x = calculate_x_velocity(self.player, dt)

        return PlayerStates.NULL
    
    def process_y_movement(self, dt):
        self.player.velocity.y += self.player.FINAL_GRAVITY * dt
        if not self.player.grounded: return PlayerStates.FALL

        return PlayerStates.NULL

class DashState(RunState):
    DASHTIME = 0.4
    def __iter__(self): 
        yield DashState.DASHTIME

class JumpState(State):    
    def proceess_y_movement(self, dt):
        self.player.velocity.y += self.player.INIT_GRAVITY * dt
        
        if self.player.grounded:
            if self.player.key_pressed["right"] or self.player.key_pressed["left"]: return PlayerStates.RUN
            else: return PlayerStates.IDLE

    def process_x_movement(self, dt):
        dir = self.player.get_direction()
        self.player.velocity.x = calculate_x_velocity(self.player, dt)

        return PlayerStates.NULL
        
class FallState(State):    
    def proceess_y_movement(self, dt):
        self.player.velocity.y += self.player.FINAL_GRAVITY * dt
        
        if self.player.grounded:
            if self.player.key_pressed["right"] or self.player.key_pressed["left"]: return PlayerStates.RUN
            else: return PlayerStates.IDLE

    def process_x_movement(self, dt):
        dir = self.player.get_direction()
        self.player.velocity.x = calculate_x_velocity(self.player, dt)

        return PlayerStates.NULL




def calculate_x_velocity(entity, dt):
    dir = entity.get_direction()
    u = entity.velocity.x
    target_speed = entity.MAXRUN * dir
    
    if abs(target_speed) > 0.01:
        a = entity.ACCELRUN
        if not entity.grounded:
            a *= 0.01
    else:
        a = entity.DECELRUN
        if not entity.grounded:
            a *= 0.6
    
    if (u > target_speed and target_speed > 0.01) or (u < target_speed and target_speed < -0.01): a = 0

    if abs(target_speed) < 0.01: vel_power = entity.STOPPOWER
    elif abs(u) > 0 and sign(target_speed) != sign(u): vel_power = entity.TURNPOWER
    else: vel_power = entity.ACCELPOWER


    v = (a*dt) ** vel_power
    
    if dir > 0: return min(u + v, target_speed)
    if dir < 0: return max(u + v*entity.x_move_input, target_speed)
    else:
        if sign(u) == -1: return min(u - (v*-1), target_speed*entity.dir)
        else: return max(u - v, target_speed*dir)







    




from abc import abstractclassmethod
from enum import Enum, auto

class PlayerStates(Enum):
    NULL = auto()
    IDLE = auto()
    RUN = auto()
    DASH = auto()
    JUMP = auto()
    FALL = auto()

class State:
    def __init__(self, player): self.player = player
    
    def handle_inputs(keys): return PlayerStates.NULL
    
    def process(dt): return PlayerStates.NULL

    def process_physics(): return PlayerStates.NULL


class MoveState(State):
    def handle_inputs(keys):
        if keys["up"]:
            return PlayerStates.JUMP

        return PlayerStates.NULL

    def process_physics(dt):
        dir = self.player.get_direction()


class RunState(State):
    def process_physics(dt):
        
            


    




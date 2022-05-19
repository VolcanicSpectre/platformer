from abc import abstractclassmethod
from enum import Enum, auto
from sre_constants import JUMP

class PlayerStates(Enum):
    NULL = auto()
    IDLE = auto()
    RUN = auto()
    DASH = auto()
    JUMP = auto()
    FALL = auto()

class State:
    def handle_inputs(keys): return PlayerStates.NULL
    
    def process(dt): return PlayerStates.NULL

    def process_physics(): return PlayerStates.NULL


class MoveState(State):
    def handle_inputs(keys):
        if keys["up"]:
            return PlayerStates.JUMP

        return PlayerStates.NULL

    def process_physics(dt):
            


    




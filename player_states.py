from enum import Enum, auto


class PlayerStates(Enum):
    IDLE = auto()
    RUN = auto()
    DASH = auto()
    
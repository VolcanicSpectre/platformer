from time import perf_counter
from nea_game.player.player import Player


class PlayerState:
    def __init__(self, player: Player, state_name: str) -> None:
        """A template PlayerPlayerState class

        Args:
            entity (BaseEntity): The entity that the PlayerPlayerState belongs to
            PlayerPlayerState_name (str): The string representation of the PlayerPlayerState
        """
        self.player = player
        self.state_name: str = state_name
        self.start_time: float

    def enter(self) -> None:
        """Called when entering the PlayerPlayerState"""
        self.start_time = perf_counter()
        self.do_checks()

    def exit(self) -> None:
        """Called when leaving the PlayerPlayerState"""
        pass

    def update(self, dt: float) -> None:
        """Called each frame"""
        self.do_checks()

    def do_checks(self) -> None:
        """Performs checks for the entity"""
        pass

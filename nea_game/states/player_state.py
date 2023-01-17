from __future__ import annotations
import typing
from time import perf_counter

if typing.TYPE_CHECKING:
    from nea_game.player.player import Player


class PlayerState:
    def __init__(self, player: Player, state_name: str) -> None:
        """A template PlayerState class

        Args:
            player (Player): The entity that the PlayerState belongs to
            state_name (str): The string representation of the PlayerState
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

    def input_handler(self):
        """Handles the inputs"""

    def update(self, dt: float) -> None:
        """Called each frame"""
        self.do_checks()

    def do_checks(self) -> None:
        """Performs checks for the entity"""

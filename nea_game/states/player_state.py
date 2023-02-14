from __future__ import annotations
import typing
from time import perf_counter

if typing.TYPE_CHECKING:
    from nea_game.player.player import Player


class PlayerState:
    """
    ###
    A: Complex OOP Model to model player states
    ###
    """

    player: Player
    state_name: str
    animation_index: int
    start_time: float
    is_exiting_state: bool

    def __init__(self, player: Player, state_name: str):
        """A template PlayerState class

        Args:
            player (Player): The entity that the PlayerState belongs to
            state_name (str): The string representation of the PlayerState
        """
        self.player = player
        self.state_name = state_name
        self.animation_index = 0
        self.is_exiting_state = False

    def enter(self):
        """Called when entering the PlayerState"""
        self.start_time = perf_counter()
        self.is_exiting_state = False

    def exit(self):
        """Called when leaving the PlayerState"""
        self.is_exiting_state = True
        self.animation_index = 0

    def input_handler(self):
        """Handles the inputs"""

    def update(self, delta_time: float):
        """Called each frame"""
        if self.player.is_grounded:
            self.player.can_dash = True

from __future__ import annotations
import typing
from nea_game.calc.vector2d import Vector2D
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.states.player_state import PlayerState

if typing.TYPE_CHECKING:
    from nea_game.player.player import Player

class PlayerGroundedState(PlayerState):
    move_input: Vector2D

    def __init__(self, player: Player, state_name: str):
        super().__init__(player, state_name)

    def input_handler(self):
        self.move_input = self.player.input.get_axis_raw()

    def update(self, dt: float):
        super().update(dt)

        if self.player.input.get_action_down(PlayerActionSpace.UP):
            self.player.state_machine.change_state(self.player.jump_state)

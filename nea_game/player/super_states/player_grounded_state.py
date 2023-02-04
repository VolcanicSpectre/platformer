from __future__ import annotations
from nea_game.calc.vector2d import Vector2D
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.states.player_state import PlayerState


class PlayerGroundedState(PlayerState):
    move_input: Vector2D

    def input_handler(self):
        self.move_input = self.player.input_.get_axis_raw()

    def update(self, delta_time: float):
        super().update(delta_time)

        if (
            self.player.input_.get_action_down(PlayerActionSpace.DASH)
            and self.player.can_dash
        ):
            self.player.state_machine.change_state(self.player.dash_state)

        if self.player.input_.get_action_down(PlayerActionSpace.UP):
            self.player.state_machine.change_state(self.player.jump_state)

        if not self.player.is_grounded:
            self.player.state_machine.change_state(self.player.in_air_state)

from __future__ import annotations
import typing
from nea_game.calc.vector2d import Vector2D
from nea_game.states.player_state import PlayerState


class PlayerAbilityState(PlayerState):
    move_input: Vector2D
    is_ability_done: bool

    def enter(self):
        self.is_ability_done = False

    def update(self, dt: float):
        super().update(dt)

        if self.is_ability_done:
            if self.player.is_grounded and self.player.rb.velocity.y <= 0:
                self.player.state_machine.change_state(self.player.idle_state)
            else:
                self.player.state_machine.change_state(self.player.in_air_state)

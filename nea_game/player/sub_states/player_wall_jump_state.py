from __future__ import annotations
from time import perf_counter
import typing
from nea_game.calc.lerp import lerp
from nea_game.calc.sign import sign
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.player.super_states.player_ability_state import PlayerAbilityState

if typing.TYPE_CHECKING:
    from nea_game.player.player import Player


class PlayerWallJumpState(PlayerAbilityState):
    def enter(self):
        super().enter()
        print("here")
        force = Vector2D(
            self.player.wall_jump_force.x * self.player.input.get_axis_raw().x * -1,
            self.player.wall_jump_force.y * -1,
        )

        self.player.rb.add_force(force, force_mode=ForceMode.IMPULSE)
        self.is_ability_done = True

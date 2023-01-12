from __future__ import annotations
import typing
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceModes
from nea_game.player.super_states.player_ability_state import PlayerAbilityState

if typing.TYPE_CHECKING:
    from nea_game.player.player import Player

class PlayerJumpState(PlayerAbilityState):
    def __init__(self, player: Player, state_name: str):
        super().__init__(player, state_name)

    def enter(self):
        super().enter()
        self.player.rb.add_force(
            Vector2D(1, 0).scale(self.player.jump_force), force_mode=ForceModes.IMPULSE
        )

        self.is_ability_done = True

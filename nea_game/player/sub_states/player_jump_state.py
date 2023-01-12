from __future__ import annotations
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceModes
from nea_game.player.super_states.player_ability_state import PlayerAbilityState


class PlayerJumpState(PlayerAbilityState):
    def enter(self):
        super().enter()
        self.player.rb.add_force(
            Vector2D(1, 0).scale(self.player.jump_force), force_mode=ForceModes.IMPULSE
        )

        self.is_ability_done = True

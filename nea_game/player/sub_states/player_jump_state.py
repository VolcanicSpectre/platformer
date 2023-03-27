from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.player.super_states.player_ability_state import PlayerAbilityState


class PlayerJumpState(PlayerAbilityState):
    def enter(self):
        ###A: Overriding the parent implementation of enter###
        super().enter()
        self.player.rigid_body.velocity = Vector2D(self.player.rigid_body.velocity.x, 0)
        self.player.rigid_body.add_force(
            Vector2D(0, -1).scale(self.player.jump_force), force_mode=ForceMode.IMPULSE
        )

        self.is_ability_done = True

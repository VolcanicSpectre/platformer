from nea_game.calc.sign import sign
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.player.super_states.player_ability_state import PlayerAbilityState


class PlayerWallJumpState(PlayerAbilityState):
    def enter(self):
        super().enter()
        force = Vector2D(
            self.player.wall_jump_force.x * self.player.direction * -1,
            self.player.wall_jump_force.y * -1,
        )

        if sign(self.player.rb.velocity.x) != sign(force.x):
            force = Vector2D(force.x - self.player.rb.velocity.x, force.y)

        if self.player.rb.velocity.y > 0:
            force = Vector2D(force.x, force.y - self.player.rb.velocity.y)

        self.player.rb.add_force(force, force_mode=ForceMode.IMPULSE)
        self.is_ability_done = True

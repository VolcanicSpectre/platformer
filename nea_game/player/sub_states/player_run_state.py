from __future__ import annotations
from nea_game.calc.near_zero import near_zero
from nea_game.calc.sign import sign
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.player.super_states.player_grounded_state import PlayerGroundedState


class PlayerRunState(PlayerGroundedState):
    def update(self, dt: float):
        super().update(dt)
        if not self.is_exiting_state:
            if near_zero(self.player.rb.velocity.x) and self.move_input.x == 0:
                self.player.state_machine.change_state(self.player.idle_state)
            else:
                target_speed = self.move_input.x * self.player.x_run_speed
                speed_difference = target_speed - self.player.rb.velocity.x

                acceleration_rate = (
                    self.player.acceleration_rate * self.player.air_acceleration_multiplier
                    if abs(target_speed) > 0
                    else self.player.deceleration_rate
                )

                movement = pow(
                    abs(speed_difference) * acceleration_rate, self.player.velocity_power
                ) * sign(speed_difference)

                self.player.rb.add_force(Vector2D(1, 0).scale(movement), dt)

                if abs(target_speed) == 0:
                    friction = sign(self.player.rb.velocity.x) * min(
                        abs(self.player.rb.velocity.x), self.player.friction
                    )
                    self.player.rb.add_force(
                        Vector2D(self.move_input.x, 0).scale(friction),
                        force_mode=ForceMode.IMPULSE,
                    )

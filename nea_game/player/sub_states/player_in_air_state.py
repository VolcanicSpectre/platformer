from nea_game.calc.sign import sign
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.states.player_state import PlayerState


class PlayerInAirState(PlayerState):
    move_input: Vector2D

    def input_handler(self):
        self.move_input = self.player.input.get_axis_raw()

    def update(self, dt: float):
        if self.player.is_grounded:
            if self.player.rb.velocity.x == 0:
                self.player.state_machine.change_state(self.player.idle_state)
            else:
                self.player.state_machine.change_state(self.player.run_state)
        else:
            target_speed = self.move_input.x * self.player.x_run_speed
            speed_difference = target_speed - self.player.rb.velocity.x

            acceleration_rate = (
                self.player.acceleration_rate
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
                    Vector2D(1, 0).scale(friction), force_mode=ForceMode.IMPULSE
                )

            if self.player.rb.velocity.y > 0:
                gravity_scale = self.player.rb.gravity_scale * 1.5
            else:
                gravity_scale = self.player.rb.gravity_scale

            self.player.rb.add_force(
                Vector2D(0, 1).scale(gravity_scale),
                dt,
                ForceMode.ACCELERATION,
            )
            self.player.rb.velocity = Vector2D(self.player.rb.velocity.x , min(self.player.rb.velocity.y, self.player.max_fall))

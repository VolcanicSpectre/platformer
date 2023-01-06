from math import pow
from nea_game.calc.near_zero import near_zero
from nea_game.calc.sign import sign
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceModes
from nea_game.player.player import Player
from nea_game.player.super_states.player_grounded_state import PlayerGroundedState


class PlayerRunState(PlayerGroundedState):
    def __init__(self, player: Player, state_name: str):
        super().__init__(player, state_name)

    def input_handler(self):
        pass

    def update(self, dt: float):
        super().update(dt)

        if self.player.rb.velocity.x == 0 and self.player.input.get_axis_raw().x == 0:
            self.player.state_machine.change_state(self.player.idle_state)

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
                Vector2D(1, 0).scale(friction), force_mode=ForceModes.IMPULSE
            )

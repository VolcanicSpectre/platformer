from __future__ import annotations
from time import perf_counter
import typing
from nea_game.calc.near_zero import near_zero
from nea_game.calc.sign import sign
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.player.super_states.player_grounded_state import PlayerGroundedState

if typing.TYPE_CHECKING:
    from nea_game.player.player import Player


class PlayerRunState(PlayerGroundedState):
    animation_frame_time: float
    last_animation_index_change: float

    def __init__(self, player: Player, state_name: str):
        super().__init__(player, state_name)
        self.animation_frame_time = 0.05
        self.last_animation_index_change = perf_counter()

    def update(self, delta_time: float):
        super().update(delta_time)
        if not self.is_exiting_state:
            if near_zero(self.player.rigid_body.velocity.x) and self.move_input.x == 0:
                self.player.state_machine.change_state(self.player.idle_state)
            else:
                if (
                    perf_counter() - self.last_animation_index_change
                    > self.animation_frame_time
                ):
                    self.animation_index = (self.animation_index + 1) % len(
                        self.player.renderer.frames[self.state_name]
                    )
                    self.last_animation_index_change = perf_counter()

                target_speed = self.move_input.x * self.player.x_run_speed
                speed_difference = target_speed - self.player.rigid_body.velocity.x

                acceleration_rate = (
                    self.player.acceleration_rate
                    if abs(target_speed) > 0
                    else self.player.deceleration_rate
                )

                movement = pow(
                    abs(speed_difference) * acceleration_rate,
                    self.player.velocity_power,
                ) * sign(speed_difference)

                self.player.rigid_body.add_force(
                    Vector2D(1, 0).scale(movement), delta_time
                )

                if abs(target_speed) == 0:
                    friction = sign(self.player.rigid_body.velocity.x) * min(
                        abs(self.player.rigid_body.velocity.x), self.player.friction
                    )
                    self.player.rigid_body.add_force(
                        Vector2D(self.move_input.x, 0).scale(friction),
                        force_mode=ForceMode.IMPULSE,
                    )

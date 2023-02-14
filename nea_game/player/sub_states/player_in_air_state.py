from __future__ import annotations
from time import perf_counter
import typing
from nea_game.calc.lerp import lerp
from nea_game.calc.sign import sign
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.player.super_states.player_grounded_state import PlayerGroundedState
from nea_game.states.player_state import PlayerState

if typing.TYPE_CHECKING:
    from nea_game.player.player import Player


class PlayerInAirState(PlayerState):
    move_input: Vector2D
    jump_input_time: float

    def __init__(self, player: Player, state_name: str):
        super().__init__(player, state_name)
        self.jump_input_time = 0

    def input_handler(self):
        ###A: Overriding the parent implementation of input_handler###
        self.move_input = self.player.input_.get_axis_raw()

    def update(self, delta_time: float):
        ###A: Overriding the parent implementation of update###
        if (
            self.player.input_.get_action_down(PlayerActionSpace.DASH)
            and self.player.can_dash
        ):
            self.player.state_machine.change_state(self.player.dash_state)

        elif self.player.input_.get_axis_raw().x:
            if (
                self.player.is_touching_wall == self.player.input_.get_axis_raw().x
                and self.player.rigid_body.velocity.y > 0
            ):
                self.player.state_machine.change_state(self.player.slide_state)

        # Coyote Time
        if (
            self.player.input_.get_action_down(PlayerActionSpace.UP)
            and perf_counter() - self.start_time < self.player.coyote_time
            and issubclass(
                type(self.player.state_machine.previous_state), PlayerGroundedState
            )
        ):
            self.player.state_machine.change_state(self.player.jump_state)

        # Jump Buffering
        if self.player.input_.get_action_down(PlayerActionSpace.UP):
            self.jump_input_time = perf_counter()

        if self.player.is_grounded:
            if perf_counter() - self.jump_input_time < self.player.jump_buffer_time:
                self.player.state_machine.change_state(self.player.jump_state)
            elif self.player.rigid_body.velocity.y >= 0:
                self.player.state_machine.change_state(self.player.land_state)

        else:
            target_speed = self.move_input.x * self.player.x_run_speed
            if self.player.state_machine.previous_state == self.player.wall_jump_state:
                if (
                    perf_counter() - self.player.state_machine.previous_state.start_time
                    < self.player.wall_jump_time
                ):
                    target_speed = lerp(
                        self.player.rigid_body.velocity.x,
                        target_speed,
                        self.player.wall_jump_lerp,
                    )

            speed_difference = target_speed - self.player.rigid_body.velocity.x

            acceleration_rate = (
                self.player.acceleration_rate
                if abs(target_speed) > 0
                else self.player.deceleration_rate
            )

            if (
                self.player.state_machine.previous_state
                in (self.player.jump_state, self.player.wall_jump_state)
                and abs(self.player.rigid_body.velocity.y)
                < self.player.jump_hang_time_threshold
            ):
                acceleration_rate *= self.player.jump_hang_acceleration_mult
                target_speed *= self.player.jump_hang_max_speed_mult

            movement = pow(
                abs(speed_difference) * acceleration_rate, self.player.velocity_power
            ) * sign(speed_difference)

            self.player.rigid_body.add_force(Vector2D(1, 0).scale(movement), delta_time)

            if abs(target_speed) == 0:
                friction = sign(self.player.rigid_body.velocity.x) * min(
                    abs(self.player.rigid_body.velocity.x), self.player.friction
                )
                self.player.rigid_body.add_force(
                    Vector2D(1, 0).scale(friction), force_mode=ForceMode.IMPULSE
                )

            if (
                self.player.state_machine.previous_state
                in (self.player.jump_state, self.player.wall_jump_state)
                and abs(self.player.rigid_body.velocity.y)
                < self.player.jump_hang_time_threshold
            ):

                gravity_scale = (
                    self.player.rigid_body.gravity_scale
                    * self.player.jump_hang_gravity_mult
                )

            elif self.player.rigid_body.velocity.y > 0:
                gravity_scale = (
                    self.player.rigid_body.gravity_scale
                    * self.player.jump_fast_fall_mult
                )

            else:
                gravity_scale = self.player.rigid_body.gravity_scale

            self.player.rigid_body.add_force(
                Vector2D(0, 1).scale(gravity_scale),
                delta_time,
                ForceMode.ACCELERATION,
            )
            self.player.rigid_body.velocity = Vector2D(
                self.player.rigid_body.velocity.x,
                min(self.player.rigid_body.velocity.y, self.player.max_fall),
            )

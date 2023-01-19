from __future__ import annotations
import typing
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.states.player_state import PlayerState


class PlayerSlideState(PlayerState):
    slide_direction: int
    move_input: Vector2D

    def enter(self):
        super().enter()
        self.slide_direction = self.player.direction

    def input_handler(self):
        self.move_input = self.player.input.get_axis_raw()

    def update(self, dt: float):
        if self.move_input.x != self.slide_direction:
            self.player.state_machine.change_state(self.player.in_air_state)

        gravity_scale = self.player.rb.gravity_scale * 0.3

        self.player.rb.add_force(
            Vector2D(0, 1).scale(gravity_scale),
            dt,
            ForceMode.ACCELERATION,
        )

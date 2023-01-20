from __future__ import annotations
from nea_game.calc.vector2d import Vector2D
from nea_game.player.player_action_space import PlayerActionSpace
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
        if self.player.input.get_action_down(PlayerActionSpace.UP):
            self.player.state_machine.change_state(self.player.wall_jump_state)

        if (
            not self.player.is_touching_wall
            or self.move_input.x != self.slide_direction
        ):
            self.player.state_machine.change_state(self.player.in_air_state)

        if self.player.is_grounded:
            self.player.state_machine.change_state(self.player.idle_state)

        if not self.is_exiting_state:
            self.player.rb.velocity = Vector2D(self.player.rb.velocity.x, self.player.wall_slide_velocity)

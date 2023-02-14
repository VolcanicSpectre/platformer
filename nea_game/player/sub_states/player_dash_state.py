from time import perf_counter
from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.player.super_states.player_ability_state import PlayerAbilityState


class PlayerDashState(PlayerAbilityState):
    def enter(self):
        ###A: Overriding the parent implementation of enter###
        super().enter()

        move_input = self.player.input_.get_axis_raw()

        if move_input == Vector2D(0, 0):
            self.is_ability_done = True
        else:
            self.player.rigid_body.velocity = Vector2D(0, 0)
            force = Vector2D(move_input.x, move_input.y).scale(self.player.dash_speed)
            self.player.rigid_body.add_force(force, force_mode=ForceMode.IMPULSE)
            self.player.can_dash = False

    def exit(self):
        ###A: Overriding the parent implementation of exit###
        super().exit()
        self.player.rigid_body.velocity = Vector2D(
            self.player.rigid_body.velocity.x, self.player.rigid_body.velocity.y * 0.2
        )

    def update(self, delta_time: float):
        ###A: Overriding the parent implementation of update###
        if self.player.is_grounded:
            self.is_ability_done = True

        if perf_counter() - self.start_time > self.player.dash_time:
            self.is_ability_done = True
        super().update(delta_time)

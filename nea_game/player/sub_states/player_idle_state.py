from nea_game.calc.vector2d import Vector2D
from nea_game.player.super_states.player_grounded_state import PlayerGroundedState


class PlayerIdleState(PlayerGroundedState):
    def enter(self):
        ###A: Overriding the parent implementation of enter###
        super().enter()
        self.player.rigid_body.velocity = Vector2D(0, self.player.rigid_body.velocity.y)

    def update(self, delta_time: float):
        ###A: Overriding the parent implementation of update###
        super().update(delta_time)
        if not self.is_exiting_state:
            if self.move_input.x:
                self.player.state_machine.change_state(self.player.run_state)

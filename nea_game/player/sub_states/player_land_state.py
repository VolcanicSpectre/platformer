from time import perf_counter
from nea_game.player.super_states.player_grounded_state import PlayerGroundedState


class PlayerLandState(PlayerGroundedState):
    def update(self, dt: float):
        super().update(dt)
        if not self.is_exiting_state:
            if self.move_input.x:
                self.player.state_machine.change_state(self.player.run_state)
            elif perf_counter() - self.start_time > self.player.land_animation_time:
                self.player.state_machine.change_state(self.player.idle_state)

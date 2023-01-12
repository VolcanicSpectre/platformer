from __future__ import annotations
from nea_game.player.super_states.player_grounded_state import PlayerGroundedState


class PlayerIdleState(PlayerGroundedState):
    def update(self, dt: float):
        super().update(dt)

        if self.move_input.x:
            self.player.state_machine.change_state(self.player.run_state)

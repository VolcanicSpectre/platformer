from nea_game.player.player import Player
from nea_game.player.super_states.player_grounded_state import PlayerGroundedState


class PlayerLandState(PlayerGroundedState):
    def __init__(self, player: Player, state_name: str):
        super().__init__(player, state_name)

    def update(self, dt: float):
        super().update(dt)

        if self.player.rb.velocity.x == 0 and self.player.input.get_axis_raw().x == 0:
            self.player.state_machine.change_state(self.player.idle_state)

        if self.move_input.x:
            self.player.state_machine.change_state(self.player.run_state)

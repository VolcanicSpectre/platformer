from __future__ import annotations
import typing
from nea_game.player.super_states.player_grounded_state import PlayerGroundedState

if typing.TYPE_CHECKING:
    from nea_game.player.player import Player


class PlayerIdleState(PlayerGroundedState):
    def __init__(self, player: Player, state_name: str):
        super().__init__(player, state_name)

    def update(self, dt: float):
        super().update(dt)

        if self.move_input.x:
            self.player.state_machine.change_state(self.player.run_state)

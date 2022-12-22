from player.player import Player
from player.super_states.player_grounded_state import PlayerGroundedState

class PlayerIdleState(PlayerGroundedState):
	def __init__(self, player: Player, state_name: str):
		super().__init__(player, state_name)

	def update(self, dt: float):
		super().update(dt)
		
		if self.move_input.x:
			self.player.state_machine.change_state(self.player.run_state)

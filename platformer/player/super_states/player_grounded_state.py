from platformer.calc.vector2d import Vector2D
from player.player_action_space import PlayerActionSpace
from platformer.states.player_state import PlayerState
from player.player import Player

class PlayerGroundedState(PlayerState):
	move_input: Vector2D
	def __init__(self, player: Player, PlayerPlayerState_name: str):
		self.player = player
		self.PlayerPlayerState_name = PlayerPlayerState_name
		self.start_time

	def input_handler(self):
		self.move_input = self.player.input.get_axis_raw()
	
	def update(self, dt: float):
		super().update(dt)

		if self.player.input.get_action_down(PlayerActionSpace.UP):
			self.player.state_machine.change_state(self.player.jump_state)



		

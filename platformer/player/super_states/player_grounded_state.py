from calc.vector2D import Vector2D
from states.state import State
from player.player import Player

class PlayerGroundedState(State):
	move_input: Vector2D
	def __init__(self, player: Player, state_name: str):
		self.player = player
		self.state_name = state_name

	
	def update(self):
		super().update()
		self.move_input = self.player.input.get_axis_raw()


t = PlayerGroundedState

		

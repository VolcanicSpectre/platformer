from platformer.calc.vector2d import Vector2D
from platformer.states.state import State
from player.player import Player

class PlayerGroundedState(State):
	move_input: Vector2D
	def __init__(self, player: Player, state_name: str):
		self.player = player
		self.state_name = state_name
		self.start_time

	def input_handler(self):
		self.move_input = self.player.input.get_axis_raw()
	
	def update(self, dt: float):
		super().update(dt)



		

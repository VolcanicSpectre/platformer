from platformer.calc.vector2d import Vector2D
from platformer.states.player_state import PlayerState
from player.player import Player

class PlayerAbilityState(PlayerState):
	move_input: Vector2D
	is_ability_done: bool

	def __init__(self, player: Player, state_name: str):
		super(PlayerAbilityState, self).__init__(player, state_name)

	def enter(self):
		self.is_ability_done = False

	def update(self, dt: float):
		super().update(dt)

		if self.is_ability_done:
			if self.player.is_grounded and self.player.rb.velocity.y <= 0:
				self.player.state_machine.change_state(self.player.idle_state)
			else:
				self.player.state_machine.change_state(self.player.in_air_state)






from platformer.calc.vector2d import Vector2D
from platformer.components.rigidbody2d import ForceModes
from player.player import Player
from player.super_states.player_grounded_state import PlayerAbilityState

class PlayerJumpState(PlayerAbilityState):
	def __init__(self, player: Player, state_name: str):
		super(PlayerJumpState, self).__init__(player, state_name)

	def enter(self):
		super().enter()
		self.player.rb.add_force(Vector2D(1, 0).scale(self.player.jump_force), force_mode=ForceModes.IMPULSE)

		self.is_ability_done = True
		

		
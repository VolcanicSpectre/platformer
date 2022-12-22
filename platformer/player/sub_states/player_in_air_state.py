from platformer.calc.vector2d import Vector2D
from player.player_action_space import PlayerActionSpace
from platformer.states.player_state import PlayerState
from player.player import Player

class PlayerInAirState(PlayerState):
	def __init__(self, player: Player, state_name: str):
		super().__init__(player, state_name)
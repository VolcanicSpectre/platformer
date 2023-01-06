from nea_game.calc.vector2d import Vector2D
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.states.player_state import PlayerState
from nea_game.player import Player

class PlayerInAirState(PlayerState):
	def __init__(self, player: Player, state_name: str):
		super().__init__(player, state_name)
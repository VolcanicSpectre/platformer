from player.player import Player
from player.super_states.player_grounded_state import PlayerGroundedState

class PlayerRunState(PlayerGroundedState):
	def __init__(self, player: Player, state_name: str):
		super(PlayerRunState, self).__init__(player, state_name)
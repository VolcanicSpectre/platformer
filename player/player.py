from components.input import Input
from components.renderer import AnimatedRenderer
from components.rigidbody2D import RigidBody2D
from player.sub_states.player_idle_state import PlayerIdleState
from player.sub_states.player_run_state import PlayerRunState
from player.player_action_space import PlayerActionSpace
from states.state_machine import StateMachine

class Player:
	def __init__(self):
		self.idle_state = PlayerIdleState(self, "idle")
		self.run_state = PlayerRunState(self, "run")
		
		self.renderer = AnimatedRenderer()
		self.input = Input(PlayerActionSpace)
		self.rb = RigidBody2D(5, 3)
		
	def start(self):
		"""Creates the state machine for the player
		"""
		self.state_machine = StateMachine(self.idle_state)

		
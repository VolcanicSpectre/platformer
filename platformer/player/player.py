from platformer.calc.near_zero import near_zero
from platformer.calc.vector2d import Vector2D
from platformer.components.input import Input
from platformer.components.renderer import AnimatedRenderer
from platformer.components.rigidbody2d import RigidBody2D
from platformer.entity.base_entity import BaseEntity
from player.sub_states.player_idle_state import PlayerIdleState
from player.sub_states.player_run_state import PlayerRunState
from player.sub_states.player_jump_state import PlayerJumpState
from player.player_action_space import PlayerActionSpace
from platformer.states.state_machine import StateMachine

class Player(BaseEntity):
	def __init__(self):
		self.idle_state = PlayerIdleState(self, "idle")
		self.run_state = PlayerRunState(self, "run")
		self.jump_state = PlayerJumpState(self, "jump")
		
		self.renderer = AnimatedRenderer()
		self.input = Input(PlayerActionSpace)
		self.rb = RigidBody2D(5, 3)
		
		self.x_run_speed = 5
		self.acceleration_rate = 2
		self.deceleration_rate = 5
		self.velocity_power = 0.6

		self.friction = 2

	def start(self):
		"""Creates the PlayerPlayerState machine for the player
		"""
		self.state_machine = StateMachine(self.idle_state)

	def update(self, dt):
		x_velocity_component = near_zero(self.rb.velocity.x)
		y_velocity_component = near_zero(self.rb.velocity.y)
		self.rb.velocity = Vector2D(x_velocity_component, y_velocity_component)

		self.state_machine.get_current_state().update(dt)
		
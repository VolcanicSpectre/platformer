from math import pow
from calc.sign import sign
from calc.vector2d import Vector2D
from player.player import Player
from player.super_states.player_grounded_state import PlayerGroundedState

class PlayerRunState(PlayerGroundedState):
	def __init__(self, player: Player, state_name: str):
		super(PlayerRunState, self).__init__(player, state_name)

	def input_handler(self):

	def update(self, dt: float):
		super().update(dt)
		if self.player.rb.velocity.x == 0:
			self.player.state_machine.change_state(self.player.idle_state)

		target_speed = self.move_input.x * self.player.x_run_speed
		speed_difference = target_speed - self.player.rb.velocity.x

		acceleration_rate = self.player.acceleration_rate if abs(target_speed) > 0 else self.player.deceleration_rate

		movement = pow(abs(speed_difference) * acceleration_rate, self.player.velocity_power) * sign(speed_difference)

		self.player.rb.add_force(Vector2D(1, 0).scale(movement), dt)






import os
print(f"CWD: {os.getcwd()}")
from enum import Enum, auto
from platformer.calc.vector2d import Vector2D


class ForceModes(Enum):

	"""Provides a container for the valid ways for a force to be applied to a rigid body
	
	Attributes:
	    FORCE (TYPE): Add a continuous force to the rigidbody, using its mass
	    IMPULSE (TYPE): Add an instant force impulse to the rigidbody, using its mass.
	"""

	FORCE = auto()
	IMPULSE = auto()

class RigidBody2D:
	def __init__(self, mass: float, gravity_scale: float) -> None:
		"""Creates a 2D rigid body
		
		Args:
		    mass (float): The mass of the body in kg
		    gravity_scale (float): The degree to which the body is affected by gravity
		"""
		self.mass = mass
		self.gravity_scale = gravity_scale
		self.velocity = Vector2D(0, 0)

	def add_force(self, force: Vector2D, dt: float, force_mode: ForceModes=ForceModes.FORCE ) -> None:
		"""Adds a force to the rigid body
		
		Args:
		    force (Vector2D): The unscaled force that will act on the body
		    dt (float): The time difference between the previous frame that was drawn and the current frame
		    force_mode (ForceModes, optional): The mode that the force can be applied
		
		Raises:
		    ValueError: A ValueError is raised when the given force_mode is not a valid force_type
		"""
		match force_mode:
			case ForceModes.FORCE: 
				self.velocity += force.scale(dt / self.mass)
			
			case ForceModes.IMPULSE:
				self.velocity += force.scale(1 / self.mass)

			case _:
				raise ValueError(f"The given force_type: {force_mode} is not in {[member.value for member in ForceModes]}")





rb = RigidBody2D(5, 2)
rb.add_force(Vector2D(50, 0), 1/120)

for i in range(200):
	target_speed = 0
	speed_difference = target_speed - rb.velocity.x

	acceleration_rate = 0.8

	movement = pow(abs(speed_difference) * acceleration_rate, 2) * sign(speed_difference)

	rb.add_force(Vector2D(1, 0).scale(movement), 1/120)







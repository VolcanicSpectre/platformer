from enum import Enum, auto
from vector2D import Vector2D

class ForceModes(Enum):
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
		"""Summary
		
		Args:
		    force (Vector2D): Description
		    dt (float): Description
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










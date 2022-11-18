from vector2D import Vector2D

class RigidBody2D:
	def __init__(self, x: float, y: float) -> None:
		self.x = x
		self.y = y
		self.velocity = Vector2D(0, 0)

	def add_force(self, force: Vector2D) -> None:




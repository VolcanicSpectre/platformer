from pygame.math import Vector2

class Vector2D:
	def __init__(self, x_component, y_component):
		self.vector = (x_component, y_component)

	def __repr__(self):
		return f"Vector2D: ({self.vector[0], self.vector[1]})"
	def __mul__(self, other):
		return self.dot(other)
	
	def dot(self, other):
		return sum(component1 * component2 for component1, component2 in zip(self.vector, other.vector))

	def cross(self, other):
		return 



if __name__ == '__main__':
	v1 = Vector2D(50, 29)
	v2 = Vector2D(30, 44)
	print(v1.cross(v2))
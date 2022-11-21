from __future__ import annotations
from math import sqrt
class Vector2D:
	def __init__(self, x_component: float, y_component: float) -> None:
		"""Creates a 2 dimensional vector
		
		Args:
		    x_component (float): The x component of the vector
		    y_component (float): The y component of the vector
		"""
		self.x = x_component
		
		self.y = y_component

	def __repr__(self) -> str:
		"""Returns a string representation of the vector displaying the both the x and y components
		
		Returns:
		    String: The resulting representation of the vector
		"""
		return f"Vector2D: ({self.x, self.y})"
	
	def __mul__(self, other: Vector2D) -> float:
		"""Calculates the dot product with the other vector
		
		Args:
		    other (Vector2D): The other vector that is used to calculate the dot product			
		
		Returns:
		    Float: The resulting scalar from performing the dot product
		"""
		return self.dot(other)

	def magnitude(self) -> float:
		"""Calculates the magnitude of the vector
		
		Returns:
		    float: The magnitude of the vector
		"""
		return sqrt(self.x * self.x + self.y * self.y)

	def normalise(self) -> Vector2D:
		"""Returns a vector with the same direction but a magnitude of 1
		
		Returns:
		    Vector2D: The vector with the same direction but a magnitude of 1
		"""
		return Vector2D(self.x / self.magnitude(), self.y / self.magnitude())

	def normalise_in_place(self) -> None:
		"""Normalises the vector in place so that its length is 1 but with the same direction
		"""
		self.x /= self.magnitude()
		self.y /= self.magnitude()

	def scale(self, scale_factor: float):
		"""Scales the vector by a given scale factor
		
		Args:
		    scale_factor (float): The amount that the vector is scaled by
		"""
		self.x *= scale_factor
		self.y *= scale_factor

	def scale_to_length(self, length: float) -> None:
		"""Scales the vector to a given length
		
		Args:
		    length (float): The length that the vector is scaled to
		
		Raises:
		    ValueError: Raises a ValueError when the magnitude of the vector is 0 as that can't be scaled to a given length
		"""
		if self.magnitude() == 0:
			raise ValueError("The Magnitude of the vector must be greater than zero")
		
		self.normalise_in_place()
		self.scale(length)
		

	def dot(self, other: Vector2D) -> float:
		"""Calculates the dot product with the other vector
		
		Args:
		    other (Vector2D): The other vector that is used to calculate the dot product			
		
		Returns:
		    Float: The resulting scalar from performing the dot product
		"""					
		return self.x * other.x + self.y * other.y

	def cross(self, other: Vector2D) -> float:
		"""Calculates the cross product with the other vector
		
		Args:
		    other (Vector2D): The other vector that is used to calculate the cross product
		
		Returns:
		    Float: The resulting scalar from performing the cross product
		"""
		return (self.x * other.y) - (self.y * other.x)

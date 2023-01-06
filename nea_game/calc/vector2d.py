"""Provides a Vector class in the 2-Dimensional plane with the associated methods for vectors"""
from __future__ import annotations
from typing import NamedTuple
from math import sqrt


class Vector2D(NamedTuple):

    """Creates a 2 dimensional vector"""

    x: float
    y: float

    def __repr__(self) -> str:
        """Returns a string representation of the vector displaying the both the x and y components

        Returns:
            String: The resulting representation of the vector
        """
        return f"Vector2D: ({self.x, self.y})"

    def __add__(self, other: Vector2D) -> Vector2D:
        """Calculates the sum of 2 vectors

        Args:
            other (Vector2D): The other vector to add

        Returns:
            Vector2D: The sum of the 2 vectors
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def magnitude(self) -> float:
        """Returns the magnitude of the vector

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

    def scale(self, scale_factor: float) -> Vector2D:
        """Scales the vector by a given scale factor

        Args:
            scale_factor (float): The amount that the vector is scaled by

        Returns:
            Vector2D: The scaled vector
        """

        return Vector2D(self.x * scale_factor, self.y * scale_factor)

    def scale_to_length(self, length: float) -> Vector2D:
        """Scales the vector to a given length

        Args:
            length (float): The length that the vector is scaled to

        Raises:
            ValueError: Raises a ValueError when the magnitude of the vector is 0 as
            that can't be scaled to a given length

        Returns:
            Vector2D: The vector scaled to the given length
        """
        if self.magnitude() == 0:
            raise ValueError("The Magnitude of the vector must be greater than zero")

        return self.normalise().scale(length)

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

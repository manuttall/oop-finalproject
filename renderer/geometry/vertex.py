"""
Vertex class to represent a vertex in 3D space.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import math
from geometry.point import Point

if TYPE_CHECKING:
    from .vector import Vector

__author__ = "Michael Nuttall"
__date__ = "2025/04/07"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


class Vertex(Point):
    """A vertex of the form (x, y, z) in 3D space."""

    def __init__(self, x: float, y: float, z: float) -> None:
        """Constructor

        Args:
            x (float): coordinate along the x-axis
            y (float): coordinate along the y-axis
            z (float): coordinate along the z-axis
        """
        super().__init__(x, y)
        self._z: float = z

    @property
    def z(self) -> float:
        """Property to get z.

        Returns:
            float: z coordinate
        """
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        """Property to set z.

        Args:
            value (float): z coordinate
        """
        self._z = value

    def __sub__(self, other: Vertex) -> Vector:
        """Subtract another Vertex to get the displacement Vector.

        Args:
            other (Vertex): another vertex

        Returns:
            Vector: displacement vector from other to self
        """
        if not isinstance(other, Vertex):
            raise TypeError("Subtraction only supported between Vertex objects.")
        from .vector import Vector
        return Vector(self._x - other.x, self._y - other.y, self._z - other.z)

    def __eq__(self, other: object) -> bool:
        """Equality checker.

        Args:
            other (object): another object to compare.

        Returns:
            bool: True if coordinates match
        """
        if not isinstance(other, Vertex):
            return False
        return self._x == other.x and self._y == other.y and self._z == other.z

    def distance(self, other: Vertex) -> float:
        """Calculate the distance between this vertex and another vertex.

        Args:
            other (Vertex): another vertex

        Returns:
            float: Euclidean distance
        """
        if not isinstance(other, Vertex):
            raise TypeError("The argument must be a Vertex.")
        dx: float = self._x - other.x
        dy: float = self._y - other.y
        dz: float = self._z - other.z
        return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    def __repr__(self) -> str:
        """Formal string representation of the Vertex.

        Returns:
            str: formatted as 'Vertex(x, y, z)'
        """
        return f"Vertex({self._x}, {self._y}, {self._z})"

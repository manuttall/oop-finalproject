"""Vector class for vector operations in 3D space"""

__author__ = "Michael Nuttall"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"

import math
from geometry.vertex import Vertex


class Vector(Vertex):
    """A vector in 3D space represented by its components (x, y, z)"""

    def __init__(self, x: float, y: float, z: float) -> None:
        """Constructor

        Args:
            x (float): x-component of the vector
            y (float): y-component of the vector
            z (float): z-component of the vector
        """
        super().__init__(x, y, z)

    def magnitude(self) -> float:
        """Returns the magnitude (length) of the vector.

        Returns:
            float: magnitude
        """
        return math.sqrt(self._x**2 + self._y**2 + self._z**2)

    def normalize(self) -> "Vector":
        """Returns the unit (normalized) vector.

        Returns:
            Vector: normalized vector
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector.")
        return Vector(self._x / mag, self._y / mag, self._z / mag)

    def dot(self, other: "Vector") -> float:
        """Computes the dot product with another vector.

        Args:
            other (Vector): the other vector

        Returns:
            float: dot product
        """
        if not isinstance(other, Vector):
            raise TypeError("Dot product requires another Vector.")
        return self._x * other.x + self._y * other.y + self._z * other.z

    def cross(self, other: "Vector") -> "Vector":
        """Computes the cross product with another vector.

        Args:
            other (Vector): the other vector

        Returns:
            Vector: the cross product vector
        """
        if not isinstance(other, Vector):
            raise TypeError("Cross product requires another Vector.")

        x = self._y * other.z - self._z * other.y
        y = self._z * other.x - self._x * other.z
        z = self._x * other.y - self._y * other.x
        return Vector(x, y, z)

    def __add__(self, other: "Vector") -> "Vector":
        """Vector addition

        Args:
            other (Vector): another vector

        Returns:
            Vector: the resulting vector
        """
        return Vector(self._x + other.x, self._y + other.y, self._z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        """Vector subtraction

        Args:
            other (Vector): another vector

        Returns:
            Vector: the resulting vector
        """
        return Vector(self._x - other.x, self._y - other.y, self._z - other.z)

    def __eq__(self, other: object) -> bool:
        """Check equality with another vector.

        Args:
            other (Vector): another vector

        Returns:
            bool: True if equal
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return (math.isclose(self._x, other.x) and
                math.isclose(self._y, other.y) and
                math.isclose(self._z, other.z))

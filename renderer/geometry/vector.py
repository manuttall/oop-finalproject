"""Vector class for vector operations in 3D space"""

from __future__ import annotations
import math
from geometry.vertex import Vertex

__author__ = "Michael Nuttall"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


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

    def normalize(self) -> Vector:
        """Returns the unit (normalized) vector.

        Returns:
            Vector: normalized vector
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector.")
        return Vector(self._x / mag, self._y / mag, self._z / mag)

    def dot(self, other: Vector) -> float:
        """Computes the dot product with another vector.

        Args:
            other (Vector): the other vector

        Returns:
            float: dot product
        """
        if not isinstance(other, Vector):
            raise TypeError("Dot product requires another Vector.")
        return self._x * other.x + self._y * other.y + self._z * other.z

    def cross(self, other: Vector) -> Vector:
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

    def __add__(self, other: Vertex) -> Vertex | Vector:
        """Add this vector to another vector or vertex.

        Args:
            other (Vertex): the other vector or vertex to add

        Returns:
            Vector | Vertex: a new Vector if the other is a Vector,
                            a new Vertex if the other is a Vertex
        """
        if isinstance(other, Vector):
            return Vector(self._x + other.x, self._y + other.y, self._z + other.z)
        elif isinstance(other, Vertex):
            return Vertex(self._x + other.x, self._y + other.y, self._z + other.z)
        return NotImplemented

    def __radd__(self, other: Vertex) -> Vertex | Vector:
        """Add this vector to another object from the right-hand side.

        Args:
            other (Vertex): the left-hand operand (typically a Vertex)

        Returns:
            Vector | Vertex: the result of the addition
        """
        return self.__add__(other)

    def __sub__(self, other: Vertex) -> Vector:
        """Subtract a vector or vertex from this vector.

        Args:
            other (Vertex): the vector or vertex to subtract

        Returns:
            Vector: a new vector representing the difference
        """
        if isinstance(other, Vector) or isinstance(other, Vertex):
            return Vector(self._x - other.x, self._y - other.y, self._z - other.z)
        return NotImplemented

    def __rsub__(self, other: Vertex) -> Vector:
        """Subtract this vector from a vertex (right-hand subtraction).

        Args:
            other (Vertex): the left-hand operand

        Returns:
            Vector: a new vector representing the difference
        """
        if isinstance(other, Vertex):
            return Vector(other.x - self._x, other.y - self._y, other.z - self._z)
        return NotImplemented

    def __mul__(self, scalar: float) -> Vector:
        """Multiply this vector by a scalar.

        Args:
            scalar (float): the scalar to multiply by

        Returns:
            Vector: a new vector scaled by the given scalar
        """
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self._x * scalar, self._y * scalar, self._z * scalar)

    def __rmul__(self, scalar: float) -> Vector:
        """Multiply this vector by a scalar from the left-hand side.

        Args:
            scalar (float): the scalar to multiply by

        Returns:
            Vector: a new vector scaled by the given scalar
        """
        return self.__mul__(scalar)

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

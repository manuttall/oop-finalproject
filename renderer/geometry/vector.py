"""
Vector class for vector operations in 3D space.
"""

from __future__ import annotations

import math
from functools import cached_property
from geometry.coord3d import Coordinate3D
from geometry.vertex import Vertex


__author__ = "Michael Nuttall"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


class Vector(Coordinate3D):
    """A vector in 3D space represented by its components (x, y, z)."""

    def _invalidate_cache(self) -> None:
        """Invalidates cached properties if vector values are changed."""
        self.__dict__.pop("magnitude", None)
        self.__dict__.pop("normalize", None)

    @property
    def x(self) -> float:
        """Property to get x.

        Returns:
            float: x
        """
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Property to set x.

        Args:
            value (float): x
        """
        self._invalidate_cache()
        self._x = value

    @property
    def y(self) -> float:
        """Property to get y.

        Returns:
            float: y
        """
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Property to set y.

        Args:
            value (float): y
        """
        self._invalidate_cache()
        self._y = value

    @property
    def z(self) -> float:
        """Property to get z.

        Returns:
            float: z
        """
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        """Property to set z.

        Args:
            value (float): z coordinate
        """
        self._invalidate_cache()
        self._z = value

    @cached_property
    def magnitude(self) -> float:
        """Calculates the magnitude (length) of the vector.

        Returns:
            float: magnitude
        """
        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    @cached_property
    def normalize(self) -> Vector:
        """Returns the normalized (unit) vector.

        Returns:
            Vector: normalized vector

        Raises:
            ValueError: if the vector is zero and cannot be normalized
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector.")
        return Vector(self._x / mag, self._y / mag, self._z / mag)

    def dot(self, other: Vector) -> float:
        """Computes the dot product with another vector.

        Args:
            other (Vector): another vector

        Returns:
            float: dot product

        Raises:
            TypeError: if other is not a Vector
        """
        if not isinstance(other, Vector):
            raise TypeError("Dot product requires another Vector.")
        return self._x * other.x + self._y * other.y + self._z * other.z

    def cross(self, other: Vector) -> Vector:
        """Computes the cross product with another vector.

        Args:
            other (Vector): another vector

        Returns:
            Vector: cross product vector

        Raises:
            TypeError: if other is not a Vector
        """
        if not isinstance(other, Vector):
            raise TypeError("Cross product requires another Vector.")
        x = self._y * other.z - self._z * other.y
        y = self._z * other.x - self._x * other.z
        z = self._x * other.y - self._y * other.x
        return Vector(x, y, z)

    def __add__(self, other: Vertex) -> Vertex | Vector:
        """Adds this vector to another vector or vertex.

        Args:
            other (Vertex): the other operand

        Returns:
            Vertex | Vector: result
        """
        if isinstance(other, Vector):
            return Vector(self._x + other.x, self._y + other.y, self._z + other.z)
        if isinstance(other, Vertex):
            return Vertex(self._x + other.x, self._y + other.y, self._z + other.z)
        raise TypeError("Unsupported operand type for +")

    def __radd__(self, other: Vertex) -> Vertex | Vector:
        """Right-hand addition.

        Args:
            other (Vertex): other operand

        Returns:
            Vertex | Vector: result
        """
        return self.__add__(other)

    def __sub__(self, other: Vertex) -> Vector:
        """Subtracts a vertex or vector from this vector.

        Args:
            other (Vertex): other operand

        Returns:
            Vector: result

        Raises:
            TypeError: if operand is not Vertex or Vector
        """
        if isinstance(other, Vertex):
            return Vector(self._x - other.x, self._y - other.y, self._z - other.z)
        raise TypeError("Unsupported operand type for -")

    def __rsub__(self, other: Vertex) -> Vector:
        """Right-hand subtraction.

        Args:
            other (Vertex): left-hand operand

        Returns:
            Vector: result

        Raises:
            TypeError: if operand is not Vertex
        """
        if isinstance(other, Vertex):
            return Vector(other.x - self._x, other.y - self._y, other.z - self._z)
        raise TypeError("Unsupported operand type for -")

    def __mul__(self, scalar: float) -> Vector:
        """Multiplies this vector by a scalar.

        Args:
            scalar (float): multiplier

        Returns:
            Vector: result

        Raises:
            TypeError: if scalar is not a number
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError("Can only multiply by a number.")
        return Vector(self._x * scalar, self._y * scalar, self._z * scalar)

    def __rmul__(self, scalar: float) -> Vector:
        """Right-hand scalar multiplication.

        Args:
            scalar (float): multiplier

        Returns:
            Vector: result
        """
        return self.__mul__(scalar)

    def __eq__(self, other: object) -> bool:
        """Equality checker.

        Args:
            other (object): other operand

        Returns:
            bool: True if equal
        """
        if not isinstance(other, Vector):
            return False
        return (math.isclose(self._x, other.x) and
                math.isclose(self._y, other.y) and
                math.isclose(self._z, other.z))

    def __repr__(self) -> str:
        """Formal string representation.

        Returns:
            str: 'Vector(x, y, z)'
        """
        return f"Vector({self._x:.6f}, {self._y:.6f}, {self._z:.6f})"

    def __str__(self) -> str:
        """Informal string representation.

        Returns:
            str: '<x, y, z>'
        """
        return f"<{self._x}, {self._y}, {self._z}>"

"""Vertex class to represent a vertex in 3D space"""

__author__ = "Michael Nuttall"
__date__ = "2025/04/07"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


from geometry.point import Point
import math


class Vertex(Point):
    """A vertex of the form (x, y, z) in 3D space."""

    def __init__(self, x: int, y: int, z: int) -> None:
        """Constructor

        Args:
            x (int): coordinate along the x-axis
            y (int): coordinate along the y-axis
            z (int): coordinate along the z-axis
        """
        super().__init__(x, y)
        self._z: int = z

    @property
    def z(self) -> int:
        """Property to get z

        Returns:
            int: z
        """
        return self._z

    @z.setter
    def z(self, value: int) -> None:
        """Property to set z

        Args:
            value (int): z
        """
        self._z = value

    def __eq__(self, other: object) -> bool:
        """Equality checker

        Args:
            other (Vertex): other Vertex to compare with.

        Returns:
            bool: True if this vertex's coordinates are equal to the other's
        """
        if not isinstance(other, Vertex):
            raise NotImplementedError
        return self._x == other.x and self._y == other.y and self._z == other.z

    def distance(self, other: "Vertex") -> float:
        """Calculate the distance between this vertex and another vertex.

        Args:
            other (Vertex): the other vertex to calculate the distance to.

        Returns:
            float: the Euclidean distance between the two vertices.
        """
        if not isinstance(other, Vertex):
            raise TypeError("The other object must be a Vertex.")

        dx: int = self._x - other.x
        dy: int = self._y - other.y
        dz: int = self._z - other.z

        return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

"""
Point class to represent a point in the Cartesian plane.
"""

__author__ = "Michael Nuttall"
__date__ = "2025/04/07"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


class Point:
    """A point of the form (x, y) in the Cartesian plane."""

    def __init__(self, x: float, y: float) -> None:
        """Constructor

        Args:
            x (float): coordinate along the x-axis
            y (float): coordinate along the y-axis
        """
        self._x: float = x
        self._y: float = y

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
        self._y = value

    def __eq__(self, other: object) -> bool:
        """Equality checker.

        Args:
            other (object): another object to compare.

        Returns:
            bool: True if coordinates match.
        """
        if not isinstance(other, Point):
            raise NotImplementedError
        return self._x == other.x and self._y == other.y

    def __repr__(self) -> str:
        """Returns a formal string representation of the Point.

        Returns:
            str: formatted as 'Point(x, y)'
        """
        return f"Point({self._x}, {self._y})"

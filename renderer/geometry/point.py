"""Point class to represent a point in the Cartesian plane"""

__author__ = "Michael Nuttall"
__date__ = "2025/02/24"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


class Point:
    """A point of the form (x,y) in the Cartesian plane.
    """

    def __init__(self, x: int, y: int) -> None:
        """Constructor

        Args:
            x (int): coordinate along the x-axis
            y (int): coordinate along the y-axis
        """
        self._x: int = x
        self._y: int = y

    @property
    def x(self) -> int:
        """Property to get x

        Returns:
            int: x
        """
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        """Property to set x

        Args:
            value (int): x
        """
        self._x = value

    @property
    def y(self) -> int:
        """Property to get y

        Returns:
            int: y
        """
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        """Property to set y

        Args:
            value (int): y
        """
        self._y = value

    def __eq__(self, other: object) -> bool:
        """Equality checker

        Args:
            other (Point): other Point to compare with.

        Returns:
            bool: True if this point's coordinates are equal to the other's
        """
        if not isinstance(other, Point):
            raise NotImplementedError
        return self._x == other.x and self._y == other.y

"""Shape class to represent a Shape in the Cartesian plane made of points"""

__author__ = "Arin Hartung"
__date__ = "2025/04/09"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry.point import Point
from geometry.shader import Shader


class Face2D:
    """A Shape of the form Shape made of point in a the Cartesian plane.
    """
    def __init__(self, points: List[Point], color: Shader = Shader(0, 0, 0)) -> None:
        """The constructor for Shape

        Args:
            points_num (int): Number of points in Shape
            points = a list of points
        """
        self._points_num = len(points)
        if self._points_num != 3:
            raise ValueError(f"Expected 3 points, got {self._points_num}")
        self._points: List[Point] = points
        self._color: Shader = color

    @property
    def points(self) -> list[Point]:
        """
        Property to get/set points value of point
        Returns:
            List[points]: points
        """
        return self._points

    @points.setter
    def points(self, points: list[Point]) -> None:
        self._points_num = len(points)
        if self._points_num != 3:
            raise ValueError(f"Expected 3 points, got {self._points_num}")
        self._points = points

    @property
    def color(self) -> Shader:
        """
        Property to get/set points value of point
        Returns:
            Shader: color
        """
        return self._color

    @color.setter
    def color(self, color: Shader) -> None:
        self._color = color

    def __eq__(self, other: object) -> bool:
        """Equality checker

        Args:
            other (Shape): other Points to compare with.

        Returns:
            bool: True if this object points are equal to the other's
        """
        if not isinstance(other, Face2D):
            raise NotImplementedError
        return self._points == other.points

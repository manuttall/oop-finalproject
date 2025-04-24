"""face2d class to represent a 2d face in the Cartesian plane made of points"""

__author__ = "Arin Hartung"
__date__ = "2025/04/09"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry.point import Point
from geometry.shader import Shader


class Face2D:
    """A face2D of the form face made of point in a the Cartesian plane.
    """
    def __init__(self, points: List[Point], dist: float, color: Shader) -> None:
        """The constructor for face2d

        Args:
            points_num (int): Number of points in the face
            points = a list of points
            dist = distance from object of importace
        """
        self._points_num = len(points)
        if self._points_num != 3:
            raise ValueError(f"Expected 3 points, got {self._points_num}")
        self._points: List[Point] = points
        self._color: Shader = color
        self._distance: float = dist

    @property
    def points(self) -> List[Point]:
        """
        Property to get/set points value of point
        Returns:
            List[points]: points
        """
        return self._points

    @points.setter
    def points(self, points: List[Point], dist: float) -> None:
        self._points_num = len(points)
        if self._points_num != 3:
            raise ValueError(f"Expected 3 points, got {self._points_num}")
        self._points = points
        self._distance = dist

    @property
    def distance(self) -> float:
        """
        Property to get points value of point
        Returns:
            float: distance
        """
        return self._distance

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

    def __lt__(self, other: object) -> bool:
        """less then  checker

        Args:
            other (Face2D): other Points to compare with.

        Returns:
            bool: True if this object distance is less than to the other's
        """
        if not isinstance(other, Face2D):
            raise NotImplementedError
        return self._distance < other._distance

    def __gt__(self, other: object) -> bool:
        """greater then checker

        Args:
            other (Face2D): other Points to compare with.

        Returns:
            bool: True if this object distance is greater than to the other's
        """
        if not isinstance(other, Face2D):
            raise NotImplementedError
        return self._distance > other._distance

    def __ge__(self, other: object) -> bool:
        """greater then checker

        Args:
            other (Face2D): other Points to compare with.

        Returns:
            bool: True if this object distance is greater than to the other's
        """
        if not isinstance(other, Face2D):
            raise NotImplementedError
        return self._distance >= other._distance

    def __le__(self, other: object) -> bool:
        """greater then checker

        Args:
            other (Face2D): other Points to compare with.

        Returns:
            bool: True if this object distance is greater than to the other's
        """
        if not isinstance(other, Face2D):
            raise NotImplementedError
        return self._distance <= other._distance

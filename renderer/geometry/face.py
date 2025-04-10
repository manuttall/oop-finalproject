"""Face class to represent a Face in the Cartesian plane made of points"""

__author__ = "Arin Hartung"
__date__ = "2025/04/09"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from point import Point


class Face:
    """A face of the form face made of point in a the Cartesian plane.
    """
    def __init__(self, points_num: int, points: List[Point]) -> None:
        """The constructor for face

        Args:
            points_num (int): Number of points in face
            points = a list of points
        """
        self._points_num = points_num
        self._points: List[Point] = points

    @property
    def points_num(self) -> int:
        """
        Property to get/set points_num value of point
        Returns:
            int: points_num
        """
        return self._points_num

    @points_num.setter
    def points_num(self, points_num: int) -> None:
        self._points_num = points_num

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
        self._points = points

    def __eq__(self, other: object) -> bool:
        """Equality checker

        Args:
            other (Face): other Points to compare with.

        Returns:
            bool: True if this object points are equal to the other's
        """
        if not isinstance(other, Face):
            raise NotImplementedError
        return self._points == other.points

    def mid_point(self):
        """Finds the Mid Point of the face

        Args:
            none

        Returns:
            Point : the mid point of the face
        """
        x_total = 0
        y_total = 0
        for point in self._points:
            x_total += point.x
            y_total += point.y
        return Point(int(x_total/self._points_num), int(y_total/self._points_num))

    def closest_point(self, new_point: Point):
        """Finds the Closet Point to a Given Point
            including the posiblity of the mid point
        Args:
            Point: other Point to compare with.

        Returns:
            Point: the closet point to given point
        """
        close_point = self.mid_point()
        delta = (close_point.x - new_point.x)+(close_point.y-new_point.y)

        for point in self._points:
            new_delta = abs((point.x - new_point.x)+(point.y-new_point.y))
            if new_delta < delta:
                delta = new_delta
                close_point = point
        return close_point

"""Face class to represent a Face in the Cartesian plane made of points"""

__author__ = "Arin Hartung"
__date__ = "2025/04/09"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry.vertex import Vertex


class Face:
    """A face of the form face made of point in a the Cartesian plane.
    """
    def __init__(self, points: List[Vertex]) -> None:
        """The constructor for face

        Args:
            points_num (int): Number of points in face
            points = a list of points
        """
        self._points_num = len(points)
        self._points: List[Vertex] = points

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
    def points(self) -> list[Vertex]:
        """
        Property to get/set points value of point
        Returns:
            List[points]: points
        """
        return self._points

    @points.setter
    def points(self, points: list[Vertex]) -> None:
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
            Vertex : the mid point of the face
        """
        x_total = 0
        y_total = 0
        z_total = 0
        for point in self._points:
            x_total += point.x
            y_total += point.y
            z_total += point.z
        vx = int(x_total/self._points_num)
        vy = int(y_total/self._points_num)
        vz = int(z_total/self._points_num)
        return Vertex(vx, vy, vz)

    def closest(self, new_point: Vertex):
        """Finds the Closet Point to a Given Point
            including the posiblity of the mid point
        Args:
            Vertex: other Point to compare with.

        Returns:
            Vertex: the closet point to given point
        """
        close_point = self.mid_point()
        delta = close_point.distance(new_point)

        for point in self._points:
            new_delta = point.distance(new_point)
            if new_delta < delta:
                delta = new_delta
                close_point = point
        return close_point

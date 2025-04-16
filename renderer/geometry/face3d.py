"""Face class to represent a Face in the Cartesian plane made of points"""

__author__ = "Arin Hartung"
__date__ = "2025/04/09"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry.vertex import Vertex
from geometry.shader import Shader


class Face3D:
    """A face3D of the form face3D made of point in a the Cartesian plane.
    """
    def __init__(self, points: List[Vertex], color: Shader = Shader(0, 0, 0)) -> None:
        """The constructor for face3D

        Args:
            points_num (int): Number of points in face3D
            points = a list of points
            color = a shader with the color of object defult white
        """
        self._distance: float = -99.9
        self._points_num = len(points)
        self._points: List[Vertex] = points
        self._color = color

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
    def distance(self) -> float:
        """
        Property to get/set distance value of point
        distance must be set by running closest_point
        Returns:
            float: distance
        """
        return self._distance

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

    @property
    def color(self) -> Shader:
        """
        Property to get/set color shader
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
            other (Face3D): other Points to compare with.

        Returns:
            bool: True if this object points are equal to the other's
        """
        if not isinstance(other, Face3D):
            raise NotImplementedError
        return self._points == other.points

    def __lt__(self, other: object) -> bool:
        """less then  checker

        Args:
            other (Face3D): other Points to compare with.

        Returns:
            bool: True if this object distance is less than to the other's
        """
        if not isinstance(other, Face3D):
            raise NotImplementedError
        return self._distance < other._distance

    def __gt__(self, other: object) -> bool:
        """greater then checker

        Args:
            other (Face3D): other Points to compare with.

        Returns:
            bool: True if this object distance is greater than to the other's
        """
        if not isinstance(other, Face3D):
            raise NotImplementedError
        return self._distance > other._distance

    def __ge__(self, other: object) -> bool:
        """greater then checker

        Args:
            other (Face3D): other Points to compare with.

        Returns:
            bool: True if this object distance is greater than to the other's
        """
        if not isinstance(other, Face3D):
            raise NotImplementedError
        return self._distance >= other._distance

    def __le__(self, other: object) -> bool:
        """greater then checker

        Args:
            other (Face3D): other Points to compare with.

        Returns:
            bool: True if this object distance is greater than to the other's
        """
        if not isinstance(other, Face3D):
            raise NotImplementedError
        return self._distance <= other._distance

    def mid_point(self):
        """Finds the Mid Point of the face3D

        Args:
            none

        Returns:
            Vertex : the mid point of the face3D
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

    def closest_point(self, new_point: Vertex):
        """Finds the Closet Point to a Given Point
            including the posiblity of the mid point
            also sets the distance of the private var
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
        self._distance = delta
        return close_point

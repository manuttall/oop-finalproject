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
            points = a List of points
            color = a shader with the color of object defult white
        """
        self._points_num = len(points)
        if self._points_num != 3:
            raise ValueError(f"Expected 3 points, got {self._points_num}")
        self._points: List[Vertex] = points
        self._color = color

    @property
    def points(self) -> List[Vertex]:
        """
        Property to get/set points value of point
        Returns:
            List[points]: points
        """
        return self._points

    @points.setter
    def points(self, points: List[Vertex]) -> None:
        self._points_num = len(points)
        if self._points_num != 3:
            raise ValueError(f"Expected 3 points, got {self._points_num}")
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

    def centroid(self):
        """Finds the centroid of the face3D

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
        vx = int(x_total / self._points_num)
        vy = int(y_total / self._points_num)
        vz = int(z_total / self._points_num)
        return Vertex(vx, vy, vz)

    def closest_point(self, new_point: Vertex) -> Vertex:
        """Finds the Closet Point to a Given Point
            including the posiblity of the mid point
            also sets the distance of the private var
        Args:
            Vertex: other Point to compare with.

        Returns:
            Vertex: the closet point to given point
        """
        close_point = self.centroid()
        delta = close_point.distance(new_point)

        for point in self._points:
            new_delta = point.distance(new_point)
            if new_delta < delta:
                delta = new_delta
                close_point = point
        return close_point

    def distance(self, new_point: Vertex) -> float:
        """Finds the distance from the Face to the given point,
        using the average of the two farthest vertex distances
        for painter's algorithm sorting.

        Args:
            new_point (Vertex): The point (e.g., camera) to compare with.

        Returns:
            float: distance from face to the point (avg of farthest two vertices).
        """
        distances = [new_point.distance(vertex) for vertex in self._points]
        distances.sort(reverse=True)  # Sort largest to smallest
        return (distances[0] + distances[1]) / 2  # Average of two farthest

    def distance_closest(self, new_point: Vertex) -> float:
        """Finds the distance to from the Face to the given point
        Args:
            Vertex: other Point to compare with.

        Returns:
            float: the distance from point to given point
        """
        return new_point.distance(self.closest_point(new_point))

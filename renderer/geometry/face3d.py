"""Face3D class to represent a triangular face in 3D space."""

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/09"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry.vertex import Vertex
from geometry.shader import Shader


class Face3D:
    """A triangular face made of 3 vertices in 3D space."""

    def __init__(self, points: List[Vertex], color: Shader = Shader(0, 0, 0)) -> None:
        """Constructor

        Args:
            points (List[Vertex]): List of exactly 3 vertices.
            color (Shader, optional): Face color. Defaults to black.

        Raises:
            ValueError: If points list does not have exactly 3 vertices.
        """
        if len(points) != 3:
            raise ValueError(f"Expected 3 points, got {len(points)}.")
        self._points: List[Vertex] = points
        self._color: Shader = color

    @property
    def points(self) -> List[Vertex]:
        """Property to get points.

        Returns:
            List[Vertex]: Vertices defining the face.
        """
        return self._points

    @points.setter
    def points(self, points: List[Vertex]) -> None:
        """Property to set points.

        Args:
            points (List[Vertex]): List of exactly 3 vertices.

        Raises:
            ValueError: If points list does not have exactly 3 vertices.
        """
        if len(points) != 3:
            raise ValueError(f"Expected 3 points, got {len(points)}.")
        self._points = points

    @property
    def color(self) -> Shader:
        """Property to get color.

        Returns:
            Shader: Face color.
        """
        return self._color

    @color.setter
    def color(self, color: Shader) -> None:
        """Property to set color.

        Args:
            color (Shader): Face color.
        """
        self._color = color

    def __eq__(self, other: object) -> bool:
        """Equality checker.

        Args:
            other (object): Other face to compare.

        Returns:
            bool: True if points match.
        """
        if not isinstance(other, Face3D):
            return NotImplemented
        return self._points == other.points

    def centroid(self) -> Vertex:
        """Calculates the centroid (average position) of the face.

        Returns:
            Vertex: Centroid of the face.
        """
        x_total = sum(p.x for p in self._points)
        y_total = sum(p.y for p in self._points)
        z_total = sum(p.z for p in self._points)

        return Vertex(
            x_total / 3,
            y_total / 3,
            z_total / 3
        )

    def closest_point(self, new_point: Vertex) -> Vertex:
        """Finds the closest point on the face to a given vertex.

        Includes comparing centroid and vertices.

        Args:
            new_point (Vertex): Point to compare.

        Returns:
            Vertex: Closest point.
        """
        close_point: Vertex = self.centroid()
        min_distance: float = close_point.distance(new_point)

        for vertex in self._points:
            dist = vertex.distance(new_point)
            if dist < min_distance:
                close_point = vertex
                min_distance = dist

        return close_point

    def distance(self, new_point: Vertex) -> float:
        """Calculates approximate distance from the face to a point.

        Uses the average of the two farthest vertex distances
        (useful for painter's algorithm sorting).

        Args:
            new_point (Vertex): Point to measure from.

        Returns:
            float: Distance estimate.
        """
        distances = [new_point.distance(vertex) for vertex in self._points]
        distances.sort(reverse=True)
        return (distances[0] + distances[1]) / 2

    def distance_closest(self, new_point: Vertex) -> float:
        """Calculates distance to the closest point on the face.

        Args:
            new_point (Vertex): Point to compare.

        Returns:
            float: Distance to closest point.
        """
        return new_point.distance(self.closest_point(new_point))

    def __repr__(self) -> str:
        """Formal string representation.

        Returns:
            str: Face3D(points=..., color=...)
        """
        return f"Face3D(points={self._points}, color={self._color})"

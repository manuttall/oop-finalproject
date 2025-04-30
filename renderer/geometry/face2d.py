"""Face2D class to represent a triangular face in a plane."""

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/09"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry.point import Point
from geometry.shader import Shader


class Face2D:
    """A triangular face made of 3 points in the 2D Cartesian plane."""

    def __init__(self, points: List[Point], dist: float, color: Shader) -> None:
        """Constructor

        Args:
            points (List[Point]): List of exactly 3 points.
            dist (float): Distance value used for sorting (e.g., depth).
            color (Shader): Color shader for rendering.

        Raises:
            ValueError: If points list does not contain exactly 3 points.
        """
        if len(points) != 3:
            raise ValueError(f"Expected 3 points, got {len(points)}.")
        self._points: List[Point] = points
        self._distance: float = dist
        self._color: Shader = color

    @property
    def points(self) -> List[Point]:
        """Gets the points of the face.

        Returns:
            List[Point]: List of 3 points.
        """
        return self._points

    @points.setter
    def points(self, points: List[Point]) -> None:
        """Sets the points of the face.

        Args:
            points (List[Point]): New list of 3 points.

        Raises:
            ValueError: If points list does not contain exactly 3 points.
        """
        if len(points) != 3:
            raise ValueError(f"Expected 3 points, got {len(points)}.")
        self._points = points

    @property
    def distance(self) -> float:
        """Gets the distance value.

        Returns:
            float: Distance used for sorting.
        """
        return self._distance

    @property
    def color(self) -> Shader:
        """Gets the color shader.

        Returns:
            Shader: The color of the face.
        """
        return self._color

    @color.setter
    def color(self, color: Shader) -> None:
        """Sets the color shader.

        Args:
            color (Shader): New color.
        """
        self._color = color

    def __lt__(self, other: object) -> bool:
        """Checks if this face is closer than another.

        Args:
            other (Face2D): The face to compare with.

        Returns:
            bool: True if this distance is less than other's.

        Raises:
            NotImplementedError: If other is not a Face2D.
        """
        if not isinstance(other, Face2D):
            raise NotImplementedError
        return self._distance < other._distance

    def __gt__(self, other: object) -> bool:
        """Checks if this face is farther than another.

        Args:
            other (Face2D): The face to compare with.

        Returns:
            bool: True if this distance is greater than other's.

        Raises:
            NotImplementedError: If other is not a Face2D.
        """
        if not isinstance(other, Face2D):
            raise NotImplementedError
        return self._distance > other._distance

    def __ge__(self, other: object) -> bool:
        """Checks if this face is farther or equal to another.

        Args:
            other (Face2D): The face to compare with.

        Returns:
            bool: True if this distance is greater than or equal to other's.

        Raises:
            NotImplementedError: If other is not a Face2D.
        """
        if not isinstance(other, Face2D):
            raise NotImplementedError
        return self._distance >= other._distance

    def __le__(self, other: object) -> bool:
        """Checks if this face is closer or equal to another.

        Args:
            other (Face2D): The face to compare with.

        Returns:
            bool: True if this distance is less than or equal to other's.

        Raises:
            NotImplementedError: If other is not a Face2D.
        """
        if not isinstance(other, Face2D):
            raise NotImplementedError
        return self._distance <= other._distance

    def __repr__(self) -> str:
        """Returns a detailed string representation for debugging.

        Returns:
            str: String showing points, color, and distance.
        """
        return (f"Face2D(points={self._points}, "
                f"color={self._color.rgb}, "
                f"distance={self._distance:.2f})")

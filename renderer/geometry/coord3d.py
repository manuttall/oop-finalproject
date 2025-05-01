"""
Coordinate3D base class for objects with 3D coordinates.
"""

from __future__ import annotations
from abc import ABC, abstractmethod

__author__ = "Michael Nuttall"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


class Coordinate3D(ABC):
    """Abstract base class for 3D coordinate objects."""

    def __init__(self, x: float, y: float, z: float) -> None:
        """Constructor

        Args:
            x (float): coordinate along the x-axis
            y (float): coordinate along the y-axis
            z (float): coordinate along the z-axis
        """
        self._x: float = x
        self._y: float = y
        self._z: float = z

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

    @property
    def z(self) -> float:
        """Property to get z.

        Returns:
            float: z coordinate
        """
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        """Property to set z.

        Args:
            value (float): z coordinate
        """
        self._z = value

    @abstractmethod
    def __repr__(self) -> str:
        """Formal string representation of the 3D coordinate.

        Returns:
            str: formatted as 'Coord(x, y, z)'
        """
        return f"Coord({self._x}, {self._y}, {self._z})"

"""AspectRatio class for storing and computing aspect ratios.

This module defines a class that encapsulates the horizontal and vertical
components of an aspect ratio and provides methods to retrieve, modify,
and compute the scalar ratio between them.
"""

__author__ = "Michael Nuttall"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


class AspectRatio:
    """A class representing vertical and horizontal components of an aspect ratio."""

    def __init__(self, horizontal: float, vertical: float) -> None:
        """Constructor

        Args:
            horizontal (float): horizontal component of the aspect ratio
            vertical (float): vertical component of the aspect ratio
        """
        self._horizontal = horizontal
        self._vertical = vertical

    @property
    def horizontal(self) -> float:
        """Get the horizontal aspect ratio component.

        Returns:
            float: horizontal value
        """
        return self._horizontal

    @horizontal.setter
    def horizontal(self, value: float) -> None:
        """Set the horizontal aspect ratio component.

        Args:
            value (float): new horizontal value
        """
        self._horizontal = value

    @property
    def vertical(self) -> float:
        """Get the vertical aspect ratio component.

        Returns:
            float: vertical value
        """
        return self._vertical

    @vertical.setter
    def vertical(self, value: float) -> None:
        """Set the vertical aspect ratio component.

        Args:
            value (float): new vertical value
        """
        self._vertical = value

    def ratio(self) -> float:
        """Calculate and return the scalar aspect ratio (horizontal / vertical).

        Returns:
            float: the scalar aspect ratio
        """
        if self._vertical == 0:
            raise ZeroDivisionError("Vertical aspect ratio cannot be zero.")
        return self._horizontal / self._vertical

    def __repr__(self) -> str:
        """String representation of the aspect ratio.

        Returns:
            str: textual form of the ratio, e.g., '4:3'
        """
        return f"{self._horizontal}:{self._vertical}"

"""AspectRatio class for storing and computing aspect ratios."""

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
            horizontal (float): Horizontal component of the aspect ratio.
            vertical (float): Vertical component of the aspect ratio.

        Raises:
            ValueError: If either component is not positive.
        """
        if horizontal <= 0:
            raise ValueError("Horizontal component must be positive.")
        if vertical <= 0:
            raise ValueError("Vertical component must be positive.")
        self._horizontal: float = horizontal
        self._vertical: float = vertical

    @property
    def horizontal(self) -> float:
        """Get the horizontal component.

        Returns:
            float: Horizontal value.
        """
        return self._horizontal

    @horizontal.setter
    def horizontal(self, value: float) -> None:
        """Set the horizontal component.

        Args:
            value (float): New horizontal value.

        Raises:
            ValueError: If value is not positive.
        """
        if value <= 0:
            raise ValueError("Horizontal component must be positive.")
        self._horizontal = value

    @property
    def vertical(self) -> float:
        """Get the vertical component.

        Returns:
            float: Vertical value.
        """
        return self._vertical

    @vertical.setter
    def vertical(self, value: float) -> None:
        """Set the vertical component.

        Args:
            value (float): New vertical value.

        Raises:
            ValueError: If value is not positive.
        """
        if value <= 0:
            raise ValueError("Vertical component must be positive.")
        self._vertical = value

    def ratio(self) -> float:
        """Calculate and return the scalar aspect ratio (horizontal / vertical).

        Returns:
            float: The scalar aspect ratio.
        """
        return self._horizontal / self._vertical

    def __str__(self) -> str:
        """User-friendly string representation.

        Returns:
            str: Aspect ratio as 'horizontal:vertical'.
        """
        return f"{self._horizontal}:{self._vertical}"

    def __repr__(self) -> str:
        """Developer/debugging string representation.

        Returns:
            str: Detailed AspectRatio object view.
        """
        return f"AspectRatio(horizontal={self._horizontal}, vertical={self._vertical})"

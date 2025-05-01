"""Shader class to represent RGB colors."""

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

import re
from typing import Tuple


class Shader:
    """Shader class for storing and converting RGB color values."""

    def __init__(self, *args: int | str) -> None:
        """Constructor

        Args:
            *args (int | str): Either 3 integers (r, g, b) or 1 hex string '#rrggbb'.

        Raises:
            ValueError: If arguments are not a valid color format.
        """
        if len(args) == 1 and isinstance(args[0], str):
            self._r, self._g, self._b = self.hex_to_rgb(args[0])
        elif len(args) == 3 and all(isinstance(c, int) for c in args):
            r = self._validate_component(int(args[0]), "Red")
            g = self._validate_component(int(args[1]), "Green")
            b = self._validate_component(int(args[2]), "Blue")
            self._r, self._g, self._b = r, g, b
        else:
            raise ValueError("Shader must be initialized with either (r, g, b)"
                             " integers or a hex string '#rrggbb'.")

    @staticmethod
    def _validate_component(value: int, name: str) -> int:
        """Validate that an RGB component is between 0 and 255.

        Args:
            value (int): Component value.
            name (str): Name of the component.

        Returns:
            int: Validated component.

        Raises:
            ValueError: If out of bounds.
        """
        if not (0 <= value <= 255):
            raise ValueError(f"{name} value {value} out of range [0, 255]")
        return value

    @property
    def r(self) -> int:
        """Property to get r.

        Returns:
            int: Red value.
        """
        return self._r

    @r.setter
    def r(self, value: int) -> None:
        """Property to set r.

        Args:
            value (int): Red value.
        """
        self._r = self._validate_component(value, "Red")

    @property
    def g(self) -> int:
        """Property to get g.

        Returns:
            int: Green value.
        """
        return self._g

    @g.setter
    def g(self, value: int) -> None:
        """Property to set g.

        Args:
            value (int): Green value.
        """
        self._g = self._validate_component(value, "Green")

    @property
    def b(self) -> int:
        """Property to get b.

        Returns:
            int: Blue value.
        """
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        """Property to set b.

        Args:
            value (int): Blue value.
        """
        self._b = self._validate_component(value, "Blue")

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Converts a hex color string to an (r, g, b) tuple.

        Args:
            hex_color (str): Hex string like '#ff00ff'.

        Returns:
            tuple[int, int, int]: Red, Green, Blue components.
        """
        if not re.fullmatch(r"#([0-9a-fA-F]{6})", hex_color):
            raise ValueError(f"Invalid hex color format: {hex_color}")
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return r, g, b

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Converts RGB values to a hex color string.

        Args:
            r (int): Red value.
            g (int): Green value.
            b (int): Blue value.

        Returns:
            str: Hex string like '#ff00ff'.
        """
        r = Shader._validate_component(r, "Red")
        g = Shader._validate_component(g, "Green")
        b = Shader._validate_component(b, "Blue")
        return f"#{r:02x}{g:02x}{b:02x}"

    @property
    def rgb(self) -> Tuple[int, int, int]:
        """Property to get (r, g, b) tuple.

        Returns:
            tuple[int, int, int]: (r, g, b)
        """
        return (self._r, self._g, self._b)

    @rgb.setter
    def rgb(self, values: Tuple[int, int, int]) -> None:
        """Property to set (r, g, b) tuple.

        Args:
            values (tuple[int, int, int]): (r, g, b)
        """
        r, g, b = values
        r = self._validate_component(values[0], "Red")
        g = self._validate_component(values[1], "Green")
        b = self._validate_component(values[2], "Blue")
        self._r, self._g, self._b = r, g, b

    @property
    def hex(self) -> str:
        """Property to get hex string representation.

        Returns:
            str: Hex string.
        """
        return self.rgb_to_hex(self._r, self._g, self._b)

    @hex.setter
    def hex(self, value: str) -> None:
        """Property to set color via hex string.

        Args:
            value (str): Hex string '#rrggbb'.
        """
        self.rgb = self.hex_to_rgb(value)

    def __repr__(self) -> str:
        """Formal string representation.

        Returns:
            str: Shader(r=..., g=..., b=...)
        """
        return f"Shader(r={self._r}, g={self._g}, b={self._b})"

    def __eq__(self, other: object) -> bool:
        """Checks equality with another Shader based on RGB values.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if RGB values match, False otherwise.
        """
        if not isinstance(other, Shader):
            return NotImplemented
        return self.rgb == other.rgb

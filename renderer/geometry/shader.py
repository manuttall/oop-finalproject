"""Shader class to represent a Shader colors"""

__author__ = "Arin Hartung"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

import re


class Shader:
    """A shader for stroing the color of faces
    """

    def __init__(self, *args):
        """Constructor

        Args:
            hex (str): a hex sting of RGB values
        or
            R (int): red hex value
            G (int): green hex value
            B (int): blue hex value
        """
        if len(args) == 1 and isinstance(args[0], str):
            self._r, self._g, self._b = self.hex_to_rgb(args[0])
        elif len(args) == 3 and all(isinstance(c, int) for c in args):
            self._r, self._g, self._b = args
        else:
            raise ValueError("Use either shader(r, g, b) or shader('#rrggbb')")

    @property
    def r(self) -> int:
        """Property to get r

        Returns:
            int: r
        """
        return self._r

    @r.setter
    def r(self, value: int) -> None:
        """Property to set r

        Args:
            value (int): r
        """
        self._r = value

    @property
    def g(self) -> int:
        """Property to get g

        Returns:
            int: g
        """
        return self._g

    @g.setter
    def g(self, value: int) -> None:
        """Property to set g

        Args:
            value (int): g
        """
        self._g = value

    @property
    def b(self) -> int:
        """Property to get b

        Returns:
            int: b
        """
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        """Property to set b

        Args:
            value (int): b
        """
        self._b = value

    @staticmethod
    def hex_to_rgb(hex_color: str):
        """function to make RGB values form a hex

        Args:
            value (str): hex
        Returns:
            int: r
            int: g
            int: b
        """
        if not re.fullmatch(r'#([0-9a-fA-F]{6})', hex_color):
            raise ValueError(f"Invalid hex color format: {hex_color}")

        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return r, g, b

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int):
        """function to make RGB values form a hex

        Args:
            value (int): r
            value (int): g
            value (str): b
        Returns:
            str: hex_str

        """
        hex_str = f'#{r:02x}{g:02x}{b:02x}'
        return hex_str

    @property
    def rgb(self) -> int:
        """Property to get rgb

        Returns:
            int: r
            int: g
            int: b
        """
        r = self._r
        g = self._g
        b = self._b
        return r, g, b

    @rgb.setter
    def rgb(self, r: int, g: int, b: int) -> None:
        """Property to set b

        Args:
            r (int): r
            g (int): g
            b (int): b
        """
        self._r = r
        self._g = g
        self._b = b

    @property
    def hex(self) -> str:
        """Property to get hex of RGB

        Returns:
            str: hex
        """
        return self.rgb_to_hex(self._r, self._g, self._b)

    @hex.setter
    def hex(self, value: str) -> None:
        """Property to set b

        Args:
            Value (str): r,g,b
        """
        self._r, self._g, self._b = self.hex_to_rgb(value)

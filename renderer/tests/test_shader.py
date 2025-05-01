"""
Unit tests for the Shader class.
"""

__author__ = "Michael Nuttall"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Michael Nuttall"

import unittest
from hypothesis import given, strategies as st
from geometry import Shader
from typing import Tuple


class TestShader(unittest.TestCase):
    """Unit tests for the Shader class."""

    def test_constructor_with_rgb(self) -> None:
        """Test constructor initializes values from RGB components."""
        shader = Shader(10, 20, 30)
        self.assertEqual(shader.r, 10)
        self.assertEqual(shader.g, 20)
        self.assertEqual(shader.b, 30)

    def test_constructor_with_hex(self) -> None:
        """Test constructor initializes values from a hex string."""
        shader = Shader("#0a141e")
        self.assertEqual(shader.rgb, (10, 20, 30))

    def test_constructor_invalid_args(self) -> None:
        """Test constructor raises ValueError on invalid inputs."""
        with self.assertRaises(ValueError):
            Shader(1, 2)
        with self.assertRaises(ValueError):
            Shader("not-a-color")
        with self.assertRaises(ValueError):
            Shader(10, "20", 30)

    def test_property_getters_and_setters(self) -> None:
        """Test r, g, b, rgb and hex getters and setters."""
        shader = Shader(0, 0, 0)

        shader.r = 100
        shader.g = 150
        shader.b = 200
        self.assertEqual(shader.rgb, (100, 150, 200))

        shader.rgb = (10, 20, 30)
        self.assertEqual(shader.r, 10)
        self.assertEqual(shader.g, 20)
        self.assertEqual(shader.b, 30)

        shader.hex = "#ff0000"
        self.assertEqual(shader.rgb, (255, 0, 0))

    def test_hex_to_rgb_conversion(self) -> None:
        """Test that hex_to_rgb converts valid hex strings correctly."""
        self.assertEqual(Shader.hex_to_rgb("#ffffff"), (255, 255, 255))
        self.assertEqual(Shader.hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(Shader.hex_to_rgb("#123abc"), (18, 58, 188))

    def test_hex_to_rgb_invalid(self) -> None:
        """Test that hex_to_rgb raises ValueError for bad format."""
        with self.assertRaises(ValueError):
            Shader.hex_to_rgb("123abc")
        with self.assertRaises(ValueError):
            Shader.hex_to_rgb("#xyzxyz")
        with self.assertRaises(ValueError):
            Shader.hex_to_rgb("#1234")

    def test_rgb_to_hex_conversion(self) -> None:
        """Test that rgb_to_hex converts RGB to correct hex string."""
        self.assertEqual(Shader.rgb_to_hex(255, 255, 255), "#ffffff")
        self.assertEqual(Shader.rgb_to_hex(0, 0, 0), "#000000")
        self.assertEqual(Shader.rgb_to_hex(18, 58, 188), "#123abc")

    def test_repr_string_format(self) -> None:
        """Test __repr__ produces the correct format."""
        shader = Shader(10, 20, 30)
        self.assertEqual(repr(shader), "Shader(r=10, g=20, b=30)")

    def test_equality(self) -> None:
        """Test __eq__ compares RGB values correctly."""
        s1 = Shader(10, 20, 30)
        s2 = Shader(10, 20, 30)
        s3 = Shader(0, 0, 0)
        self.assertTrue(s1 == s2)
        self.assertFalse(s1 == s3)
        self.assertNotEqual(s1, "not-a-shader")

    @given(st.integers(0, 255), st.integers(0, 255), st.integers(0, 255))
    def test_rgb_to_hex_and_back(self, r: int, g: int, b: int) -> None:
        """Hypothesis: RGB -> hex -> RGB round-trip is lossless."""
        hex_str = Shader.rgb_to_hex(r, g, b)
        parsed = Shader.hex_to_rgb(hex_str)
        self.assertEqual((r, g, b), parsed)

    @given(st.tuples(
        st.integers(0, 255),
        st.integers(0, 255),
        st.integers(0, 255)
    ))
    def test_hex_round_trip(self, rgb: Tuple[int, int, int]) -> None:
        """Hypothesis: RGB -> Shader -> Hex is round-trippable to lowercase hex."""
        r, g, b = rgb
        expected_hex = Shader.rgb_to_hex(r, g, b)
        shader = Shader(expected_hex)
        self.assertEqual(shader.hex, expected_hex)

    @given(st.integers(0, 255), st.integers(0, 255), st.integers(0, 255))
    def test_shader_equality_reflexive(self, r: int, g: int, b: int) -> None:
        """Hypothesis: equality is reflexive."""
        s1 = Shader(r, g, b)
        s2 = Shader(r, g, b)
        self.assertEqual(s1, s2)

    def test_mutating_r_g_b_directly_affects_rgb(self) -> None:
        """Test mutating r, g, b individually updates rgb tuple."""
        shader = Shader(1, 2, 3)
        shader.r = 10
        shader.g = 20
        shader.b = 30
        self.assertEqual(shader.rgb, (10, 20, 30))

    def test_mutating_rgb_tuple_affects_individual_components(self) -> None:
        """Test setting rgb updates r, g, b individually."""
        shader = Shader(1, 2, 3)
        shader.rgb = (11, 22, 33)
        self.assertEqual(shader.r, 11)
        self.assertEqual(shader.g, 22)
        self.assertEqual(shader.b, 33)

    def test_mutating_hex_property_changes_rgb(self) -> None:
        """Test setting hex string updates r, g, b."""
        shader = Shader(0, 0, 0)
        shader.hex = "#ffcc99"
        self.assertEqual(shader.rgb, (255, 204, 153))

    @given(st.integers(-1000, 1000),
           st.integers(-1000, 1000),
           st.integers(-1000, 1000))
    def test_rgb_to_hex_fuzzing_bounds(self, r: int, g: int, b: int) -> None:
        """Hypothesis: Fuzzing RGB bounds into rgb_to_hex safely."""
        try:
            hex_str = Shader.rgb_to_hex(r, g, b)
            self.assertTrue(isinstance(hex_str, str))
            self.assertTrue(hex_str.startswith("#"))
            self.assertEqual(len(hex_str), 7)
        except ValueError:
            # Valid case: RGB input out of bounds may raise errors
            pass

    @given(st.tuples(
        st.integers(-100, 400),
        st.integers(-100, 400),
        st.integers(-100, 400)
    ))
    def test_shader_constructor_with_fuzzed_rgb(self,
                                                rgb: Tuple[int, int, int]) -> None:
        """Hypothesis: Shader can handle or reject
        out-of-bound RGB during construction."""
        try:
            shader = Shader(*rgb)
            self.assertIsInstance(shader.rgb, tuple)
            self.assertEqual(len(shader.rgb), 3)
        except ValueError:
            # Acceptable: constructor rejects invalid RGB
            pass

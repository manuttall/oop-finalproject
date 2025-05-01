"""A unit test file for Aspect ratio """

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

import unittest
from scene import AspectRatio
from hypothesis import given, strategies as st


class TestAspectRatio(unittest.TestCase):
    """A class to test the AspectRatio class
    """
    def setUp(self) -> None:
        """
        Setup method to create a default AspectRatio instance.
        """
        self.ar = AspectRatio(16, 9)

    def tearDown(self) -> None:
        """
        Tear down method.
        """
        super().tearDown()

    def test_constructor_valid(self) -> None:
        """
        Test the constructor with valid values.
        """
        ar = AspectRatio(4, 3)
        self.assertEqual(ar.horizontal, 4)
        self.assertEqual(ar.vertical, 3)

    def test_constructor_zero_vertical(self) -> None:
        """
        Test the constructor raises ValueError when vertical is zero.
        """
        with self.assertRaises(ValueError):
            AspectRatio(4, 0)

    @given(st.floats(allow_nan=False, allow_infinity=False),
           st.floats(min_value=1e-6, allow_nan=False, allow_infinity=False))
    def test_hypothesis_constructor(self, horizontal: float, vertical: float) -> None:
        """
        Hypothesis test for constructor, excluding zero vertical.
        """
        ar = AspectRatio(horizontal, vertical)
        self.assertAlmostEqual(ar.horizontal, horizontal)
        self.assertAlmostEqual(ar.vertical, vertical)

    def test_horizontal_property(self) -> None:
        """
        Test the horizontal getter and setter.
        """
        self.ar.horizontal = 21
        self.assertEqual(self.ar.horizontal, 21)

    def test_vertical_property_valid(self) -> None:
        """
        Test the vertical getter and setter with valid input.
        """
        self.ar.vertical = 10
        self.assertEqual(self.ar.vertical, 10)

    def test_vertical_property_zero(self) -> None:
        """
        Test setting vertical to zero raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.ar.vertical = 0

    def test_ratio(self) -> None:
        """
        Test the ratio calculation.
        """
        self.assertAlmostEqual(self.ar.ratio(), 16 / 9)

    def test_str(self) -> None:
        """
        Test the __str__ method.
        """
        self.assertEqual(str(self.ar), "16:9")

    def test_repr(self) -> None:
        """
        Test the __repr__ method.
        """
        self.assertEqual(repr(self.ar), "AspectRatio(horizontal=16, vertical=9)")

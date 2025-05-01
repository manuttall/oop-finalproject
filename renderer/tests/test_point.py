
"""
Unittesting Point class
"""

import unittest
from hypothesis import given
import hypothesis.strategies as st
from geometry.point import Point

__author__ = "Arin Hartung"
__date__ = "2025/4/10"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"


class TestPoint(unittest.TestCase):
    """
    Unit tests for the Point class.
    """

    def setUp(self) -> None:
        """
        Setup method.
        """
        self.p1 = Point(3, 2)
        self.p2 = Point(3, 2)
        self.p3 = Point(1, 4)

    def tearDown(self) -> None:
        """
        Tear down method.
        """
        super().tearDown()

    def test_constructor(self) -> None:
        """
        Test that the constructor initializes x and y correctly.
        """
        self.assertEqual(self.p1.x, 3)
        self.assertEqual(self.p1.y, 2)

    def test_x_property(self) -> None:
        """
        Test getting and setting the x property.
        """
        self.p1.x = 10
        self.assertEqual(self.p1.x, 10)

    def test_y_property(self) -> None:
        """
        Test getting and setting the y property.
        """
        self.p1.y = 20
        self.assertEqual(self.p1.y, 20)

    def test_repr(self) -> None:
        """
        Test the __repr__ method.
        """
        self.assertEqual(repr(self.p1), "Point(3, 2)")

    def test_equality_true(self) -> None:
        """
        Test that two points with the same coordinates are equal.
        """
        self.assertTrue(self.p1 == self.p2)

    def test_equality_false(self) -> None:
        """
        Test that two points with different coordinates are not equal.
        """
        self.assertFalse(self.p1 == self.p3)

    def test_equality_invalid_type(self) -> None:
        """
        Test that comparing with an invalid type raises NotImplementedError.
        """
        with self.assertRaises(NotImplementedError):
            _ = self.p1 == object()

    @given(st.floats(allow_nan=False, allow_infinity=False),
           st.floats(allow_nan=False, allow_infinity=False))
    def test_hypothesis_constructor(self, x: float, y: float) -> None:
        """
        Hypothesis test for constructor.
        """
        p = Point(x, y)
        self.assertEqual(p.x, x)
        self.assertEqual(p.y, y)

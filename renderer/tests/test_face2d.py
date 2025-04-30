"""
Unit tests for the Face2D class.
"""

__author__ = "Michael Nuttall"
__date__ = "2025/04/27"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"

import unittest
from typing import List
from hypothesis import given, strategies as st
from geometry import Face2D, Point, Shader


class TestFace2D(unittest.TestCase):
    """Unit tests for the Face2D class."""

    def setUp(self) -> None:
        self.points: List[Point] = [Point(0, 0), Point(1, 0), Point(0, 1)]
        self.color: Shader = Shader(255, 0, 0)
        self.face = Face2D(self.points, 10.0, self.color)

    def test_constructor_valid(self) -> None:
        """Test that a valid Face2D object is created correctly."""
        self.assertEqual(self.face.points, self.points)
        self.assertEqual(self.face.distance, 10.0)
        self.assertEqual(self.face.color, self.color)

    def test_constructor_invalid_points(self) -> None:
        """Test that constructor raises ValueError for invalid number of points."""
        with self.assertRaises(ValueError):
            Face2D([Point(0, 0), Point(1, 0)], 10.0, self.color)

    def test_points_property_get(self) -> None:
        """Test the points property getter."""
        self.assertEqual(self.face.points, self.points)

    def test_points_property_set_valid(self) -> None:
        """Test setting points correctly updates points."""
        new_points: List[Point] = [Point(1, 1), Point(2, 2), Point(3, 3)]
        self.face.points = new_points
        self.assertEqual(self.face.points, new_points)

    def test_points_property_set_invalid(self) -> None:
        """Test setting points raises error if not exactly 3 points."""
        with self.assertRaises(ValueError):
            self.face.points = ([Point(0, 0), Point(1, 1)], 5.0)

    def test_distance_property(self) -> None:
        """Test distance property getter."""
        self.assertEqual(self.face.distance, 10.0)

    def test_color_property_get(self) -> None:
        """Test color property getter."""
        self.assertEqual(self.face.color, self.color)

    def test_color_property_set(self) -> None:
        """Test color property setter."""
        new_color = Shader(0, 255, 0)
        self.face.color = new_color
        self.assertEqual(self.face.color, new_color)

    @given(
        st.floats(min_value=0.1, max_value=1000.0),
        st.floats(min_value=0.1, max_value=1000.0)
    )
    def test_lt_and_gt(self, d1: float, d2: float) -> None:
        """Test less than and greater than comparisons."""
        face1 = Face2D(self.points, d1, self.color)
        face2 = Face2D(self.points, d2, self.color)
        if d1 < d2:
            self.assertTrue(face1 < face2)
            self.assertFalse(face1 > face2)
        elif d1 > d2:
            self.assertTrue(face1 > face2)
            self.assertFalse(face1 < face2)

    def test_invalid_lt_comparison(self) -> None:
        """Test __lt__ raises NotImplementedError if compared with wrong type."""
        with self.assertRaises(NotImplementedError):
            self.face.__lt__(object())

    def test_invalid_gt_comparison(self) -> None:
        """Test __gt__ raises NotImplementedError if compared with wrong type."""
        with self.assertRaises(NotImplementedError):
            self.face.__gt__(object())

    def test_invalid_ge_comparison(self) -> None:
        """Test __ge__ raises NotImplementedError if compared with wrong type."""
        with self.assertRaises(NotImplementedError):
            self.face.__ge__(object())

    def test_invalid_le_comparison(self) -> None:
        """Test __le__ raises NotImplementedError if compared with wrong type."""
        with self.assertRaises(NotImplementedError):
            self.face.__le__(object())

    @given(
        st.floats(min_value=0.1, max_value=1000.0)
    )
    def test_ge_le_comparisons(self, d: float) -> None:
        """Test greater than or equal and less than or equal comparisons."""
        face1 = Face2D(self.points, d, self.color)
        face2 = Face2D(self.points, d, self.color)
        self.assertTrue(face1 >= face2)
        self.assertTrue(face1 <= face2)

    def test_repr_contains_points_and_color(self) -> None:
        """Test __repr__ method includes key attributes."""
        repr_str = repr(self.face)
        for point in self.points:
            self.assertIn(f"{point}", repr_str)
        for value in self.color.rgb:
            self.assertIn(str(value), repr_str)
        self.assertIn("distance", repr_str)

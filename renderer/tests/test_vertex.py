"""A unittest class to test the Vertex class"""
import unittest
import math
from unittest.mock import patch
from typing import Any, cast
from hypothesis import given, strategies as st
from geometry import Vertex

__author__ = "Arin Hartung"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"


class TestVertex(unittest.TestCase):
    """Unit tests for the Vertex class."""

    def setUp(self) -> None:
        self.v1 = Vertex(1.0, 2.0, 3.0)
        self.v2 = Vertex(4.0, 5.0, 6.0)

    def test_constructor(self) -> None:
        """Test Vertex constructor and inherited Point attributes."""
        self.assertEqual(self.v1.x, 1.0)
        self.assertEqual(self.v1.y, 2.0)
        self.assertEqual(self.v1.z, 3.0)

    def test_z_property_get(self) -> None:
        """Test z property getter."""
        self.assertEqual(self.v1.z, 3.0)

    def test_z_property_set(self) -> None:
        """Test z property setter."""
        self.v1.z = 10.0
        self.assertEqual(self.v1.z, 10.0)

    def test_subtract_valid(self) -> None:
        """Test subtracting two Vertex objects returns correct Vector."""
        with patch('geometry.vector.Vector') as mock_vector:
            result = self.v2 - self.v1
            mock_vector.assert_called_once_with(4.0 - 1.0, 5.0 - 2.0, 6.0 - 3.0)
            self.assertEqual(result, mock_vector.return_value)

    def test_subtract_invalid_type(self) -> None:
        """Test subtraction with invalid type raises TypeError"""
        invalid_operand: Any = object()
        with self.assertRaises(TypeError):
            _ = self.v1 - cast("Vertex", invalid_operand)

    def test_eq_true(self) -> None:
        """Test equality when vertices are the same."""
        v3 = Vertex(1.0, 2.0, 3.0)
        self.assertTrue(self.v1 == v3)

    def test_eq_false_different_type(self) -> None:
        """Test equality returns False when compared with non-Vertex."""
        self.assertFalse(self.v1 == object())

    def test_eq_false_different_values(self) -> None:
        """Test equality returns False for different vertices."""
        self.assertFalse(self.v1 == self.v2)

    def test_distance_valid(self) -> None:
        """Test distance between two Vertex objects."""
        expected = math.sqrt((1.0 - 4.0)**2 + (2.0 - 5.0)**2 + (3.0 - 6.0)**2)
        self.assertAlmostEqual(self.v1.distance(self.v2), expected)

    def test_distance_invalid_type(self) -> None:
        """Test distance with invalid type raises TypeError"""
        invalid_operand: Any = object()
        with self.assertRaises(TypeError):
            self.v1.distance(cast("Vertex", invalid_operand))

    def test_eq_reflexive(self) -> None:
        """Test that a Vertex equals itself (reflexivity)."""
        self.assertTrue(self.v1 == self.v1)

    def test_eq_symmetric(self) -> None:
        """Test that equality is symmetric."""
        v3 = Vertex(1.0, 2.0, 3.0)
        self.assertTrue(self.v1 == v3 and v3 == self.v1)

    def test_eq_transitive(self) -> None:
        """Test that equality is transitive."""
        v3 = Vertex(1.0, 2.0, 3.0)
        v4 = Vertex(1.0, 2.0, 3.0)
        self.assertTrue(self.v1 == v3 and v3 == v4 and self.v1 == v4)

    def test_subtract_same_vertex(self) -> None:
        """Test subtracting a vertex from itself returns zero vector."""
        result = self.v1 - self.v1
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.z, 0)

    def test_distance_same_vertex(self) -> None:
        """Test distance from a vertex to itself is zero."""
        self.assertEqual(self.v1.distance(self.v1), 0.0)

    def test_repr_format(self) -> None:
        """Test that __repr__ has the expected format."""
        repr_str = repr(self.v1)
        self.assertRegex(repr_str, r'Vertex\(.*\)')

    @given(
        st.floats(allow_nan=False, allow_infinity=False),
        st.floats(allow_nan=False, allow_infinity=False),
        st.floats(allow_nan=False, allow_infinity=False)
    )
    def test_repr_contains_coordinates(self, x: float, y: float, z: float) -> None:
        """Test __repr__ method includes coordinates."""
        v = Vertex(x, y, z)
        repr_str = repr(v)
        self.assertIn("Vertex", repr_str)
        self.assertIn(str(v.x), repr_str)
        self.assertIn(str(v.y), repr_str)
        self.assertIn(str(v.z), repr_str)

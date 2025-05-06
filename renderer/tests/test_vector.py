"""A unittest class to test the Vector class"""
import unittest
import math
from typing import cast, Any
from unittest.mock import patch
from hypothesis import given, strategies as st
from geometry import Vector, Vertex


__author__ = "Arin Hartung"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"


class TestVector(unittest.TestCase):
    """Unit tests for the Vector class representing 3D vectors."""

    def setUp(self) -> None:
        """Set up sample vectors and zero vector for reuse in tests."""
        self.v1 = Vector(1.0, 2.0, 3.0)
        self.v2 = Vector(4.0, 5.0, 6.0)
        self.zero = Vector(0.0, 0.0, 0.0)

    def test_constructor_sets_attributes(self) -> None:
        """Test that the constructor correctly sets x, y, z components."""
        vector = Vector(1.1, 2.2, 3.3)
        self.assertAlmostEqual(vector.x, 1.1)
        self.assertAlmostEqual(vector.y, 2.2)
        self.assertAlmostEqual(vector.z, 3.3)

    def test_magnitude(self) -> None:
        """Test that the magnitude (length) is computed correctly."""
        self.assertAlmostEqual(self.v1.magnitude, math.sqrt(1**2 + 2**2 + 3**2))

    def test_normalize(self) -> None:
        """Test that normalize returns a unit vector."""
        norm = self.v1.normalize
        self.assertAlmostEqual(norm.magnitude, 1.0)
        self.assertIsInstance(norm, Vector)

    def test_normalize_zero_vector_raises(self) -> None:
        """Test that normalizing a zero vector raises a ValueError."""
        with self.assertRaises(ValueError):
            _ = self.zero.normalize

    def test_dot_product(self) -> None:
        """Test that the dot product between two vectors is correct."""
        dot = self.v1.dot(self.v2)
        expected = 1 * 4 + 2 * 5 + 3 * 6
        self.assertEqual(dot, expected)

    def test_dot_invalid_type(self) -> None:
        """Test that dot product raises TypeError when passed invalid type."""
        invalid_operand: Any = object()
        with self.assertRaises(TypeError):
            self.v1.dot(cast("Vector", invalid_operand))

    def test_cross_product(self) -> None:
        """Test that the cross product between two vectors is correct."""
        cross = self.v1.cross(self.v2)
        expected = Vector(-3.0, 6.0, -3.0)
        self.assertEqual(cross, expected)

    def test_cross_invalid_type(self) -> None:
        """Test that cross product raises TypeError when passed invalid type."""
        invalid_operand: Any = object()
        with self.assertRaises(TypeError):
            self.v1.cross(cast("Vector", invalid_operand))

    def test_add_vector(self) -> None:
        """Test that adding two vectors returns the correct vector."""
        result = self.v1 + self.v2
        expected = Vector(1 + 4, 2 + 5, 3 + 6)
        self.assertEqual(result, expected)

    def test_add_vertex(self) -> None:
        """Test that adding a vector and a vertex returns the correct vertex."""
        vertex = Vertex(7.0, 8.0, 9.0)
        result = self.v1 + vertex
        expected = Vertex(1 + 7, 2 + 8, 3 + 9)
        self.assertEqual(result, expected)

    def test_add_invalid_type(self) -> None:
        """Test that adding an invalid type raises TypeError."""
        invalid_operand: Any = object()
        with self.assertRaises(TypeError):
            _ = self.v1 + cast("Vertex", invalid_operand)
        with self.assertRaises(TypeError):
            _ = self.v1 + cast("Vector", invalid_operand)

    def test_radd_vector(self) -> None:
        """Test that right-hand addition behaves the same as left-hand."""
        result = self.v2.__radd__(self.v1)
        self.assertEqual(result, self.v1 + self.v2)

    def test_sub_vertex(self) -> None:
        """Test that subtracting a vertex returns the correct vector."""
        vertex = Vertex(1.0, 2.0, 3.0)
        result = self.v2 - vertex
        expected = Vector(4 - 1, 5 - 2, 6 - 3)
        self.assertEqual(result, expected)

    def test_rsub_vertex(self) -> None:
        """Test that right-hand subtraction with a vertex works correctly."""
        vertex = Vertex(4.0, 5.0, 6.0)
        result = self.v1.__rsub__(vertex)
        expected = Vector(4 - 1, 5 - 2, 6 - 3)
        self.assertEqual(result, expected)

    def test_sub_invalid_type(self) -> None:
        """Test that subtracting an invalid type raises TypeError."""
        invalid_operand: Any = object()
        with self.assertRaises(TypeError):
            _ = self.v1 - cast("Vertex", invalid_operand)
        with self.assertRaises(TypeError):
            _ = self.v1 - cast("Vector", invalid_operand)

    def test_mul_scalar(self) -> None:
        """Test that multiplying a vector by a scalar returns the correct vector."""
        result = self.v1 * 2
        expected = Vector(2, 4, 6)
        self.assertEqual(result, expected)

    def test_rmul_scalar(self) -> None:
        """Test that right-hand scalar multiplication works correctly."""
        result = 2 * self.v1
        expected = Vector(2, 4, 6)
        self.assertEqual(result, expected)

    def test_mul_invalid_type(self) -> None:
        """Test that multiplying by an invalid type raises TypeError."""
        invalid_operand: Any = object()
        with self.assertRaises(TypeError):
            _ = self.v1 * cast(float, invalid_operand)

    def test_eq_true(self) -> None:
        """Test that two equal vectors are recognized as equal."""
        v3 = Vector(1.0, 2.0, 3.0)
        self.assertTrue(self.v1 == v3)

    def test_eq_false(self) -> None:
        """Test that unequal vectors or invalid types are not equal."""
        self.assertFalse(self.v1 == self.v2)
        self.assertFalse(self.v1 == object())

    def test_repr_format(self) -> None:
        """Test that the string representation (__repr__) is correctly formatted."""
        r = repr(self.v1)
        self.assertTrue(r.startswith("Vector("))
        self.assertIn("1.000000", r)

    def test_str_format(self) -> None:
        """Test that the informal string representation (__str__) is formatted."""
        s = str(self.v1)
        self.assertTrue(s.startswith("<"))
        self.assertIn("1.0", s)

    def test_cache_invalidation(self) -> None:
        """Test that changing components invalidates cached properties."""
        original_magnitude = self.v1.magnitude
        self.v1.x = 10.0
        # The magnitude property should recompute on next access
        new_magnitude = self.v1.magnitude
        self.assertNotEqual(original_magnitude, new_magnitude)

    def test_y_property_set_calls_invalidate_cache(self) -> None:
        """Test that setting y updates _y and calls _invalidate_cache."""
        with patch.object(self.v1, "_invalidate_cache") as mock_invalidate:
            self.v1.y = 10.0
            mock_invalidate.assert_called_once()
            self.assertEqual(self.v1.y, 10.0)

    def test_z_property_set_calls_invalidate_cache(self) -> None:
        """Test that setting y updates _y and calls _invalidate_cache."""
        with patch.object(self.v1, "_invalidate_cache") as mock_invalidate:
            self.v1.z = 10.0
            mock_invalidate.assert_called_once()
            self.assertEqual(self.v1.z, 10.0)

    def test_rsub_invalid_type_raises_type_error(self) -> None:
        """Test that __rsub__ raises TypeError when left-hand operand is invalid."""
        invalid_operand = object()
        with self.assertRaises(TypeError):
            _ = invalid_operand - self.v1  # triggers v1.__rsub__(invalid_operand)

    @given(
        st.floats(-1e6, 1e6, allow_nan=False, allow_infinity=False),
        st.floats(-1e6, 1e6, allow_nan=False, allow_infinity=False),
        st.floats(-1e6, 1e6, allow_nan=False, allow_infinity=False),
        st.floats(-1e6, 1e6, allow_nan=False, allow_infinity=False),
    )
    def test_scalar_multiplication_properties(self, x: float, y: float,
                                              z: float, scalar: float) -> None:
        """Property-based test: scalar multiplication should scale all components."""
        v = Vector(x, y, z)
        scaled = v * scalar
        self.assertEqual(scaled, Vector(x * scalar, y * scalar, z * scalar))

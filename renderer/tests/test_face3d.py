"""
Unit tests for the Face3D class.
"""

__author__ = "Michael Nuttall"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"

import unittest
from unittest.mock import MagicMock, patch
from hypothesis import given, strategies as st
from geometry import Face3D, Vertex, Shader


class TestFace3D(unittest.TestCase):
    """Unit tests for the Face3D class."""

    def setUp(self) -> None:
        """Set up a default triangle and color before each test."""
        self.v1 = Vertex(0, 0, 0)
        self.v2 = Vertex(1, 0, 0)
        self.v3 = Vertex(0, 1, 0)
        self.face = Face3D([self.v1, self.v2, self.v3], Shader(10, 20, 30))

    def test_constructor_valid(self) -> None:
        """Test that a valid Face3D is constructed with 3 vertices."""
        self.assertEqual(self.face.points, [self.v1, self.v2, self.v3])

    def test_constructor_invalid(self) -> None:
        """Test that constructor raises ValueError with < 3 vertices."""
        with self.assertRaises(ValueError):
            Face3D([self.v1, self.v2])

    def test_points_property_set_valid(self) -> None:
        """Test setting the points property with a valid 3-vertex list."""
        new_points = [Vertex(1, 1, 1), Vertex(2, 2, 2), Vertex(3, 3, 3)]
        self.face.points = new_points
        self.assertEqual(self.face.points, new_points)

    def test_points_property_set_invalid(self) -> None:
        """Test setting points with fewer than 3 vertices raises ValueError."""
        with self.assertRaises(ValueError):
            self.face.points = [self.v1, self.v2]

    def test_color_property_set_and_get(self) -> None:
        """Test setting and getting the color property."""
        new_color = Shader(100, 150, 200)
        self.face.color = new_color
        self.assertEqual(self.face.color, new_color)

    def test_equality(self) -> None:
        """Test that two Face3D objects with same points are equal."""
        other = Face3D([self.v1, self.v2, self.v3])
        self.assertEqual(self.face, other)

    def test_equality_wrong_type(self) -> None:
        """Test that equality with a non-Face3D returns False."""
        self.assertFalse(self.face == "not-a-face")

    def test_repr_output(self) -> None:
        """Test __repr__ output includes points and color."""
        output = repr(self.face)
        self.assertIn("Face3D", output)
        for p in self.face.points:
            self.assertIn(str(p), output)
        for value in self.face.color.rgb:
            self.assertIn(str(value), output)

    def test_centroid(self) -> None:
        """Test centroid returns the mean of all 3 points."""
        centroid = self.face.centroid()
        self.assertAlmostEqual(centroid.x, 1 / 3)
        self.assertAlmostEqual(centroid.y, 1 / 3)
        self.assertAlmostEqual(centroid.z, 0.0)

    def test_closest_point_vertex(self) -> None:
        """Test closest_point returns a valid vertex or centroid."""
        test_point = Vertex(0, 0, 0.1)
        closest = self.face.closest_point(test_point)
        self.assertIsInstance(closest, Vertex)
        self.assertIn(closest, self.face.points + [self.face.centroid()])

    def test_distance(self) -> None:
        """Test distance() returns a valid average of farthest vertices."""
        test_point = Vertex(0, 0, 1)
        result = self.face.distance(test_point)
        self.assertGreater(result, 0)

    def test_distance_closest(self) -> None:
        """Test distance_closest returns distance to closest point."""
        test_point = Vertex(0, 0, 1)
        dist = self.face.distance_closest(test_point)
        self.assertGreater(dist, 0)

    @patch("geometry.face3d.Vertex.distance")
    def test_distance_closest_calls(self, mock_distance: MagicMock) -> None:
        """Test closest_point and distance_closest call distance() at least 4 times."""
        mock_distance.side_effect = lambda *_: 1.0
        test_point = Vertex(1, 1, 1)
        self.face.distance_closest(test_point)
        self.assertGreaterEqual(mock_distance.call_count, 4)

    @given(
        st.tuples(st.floats(-1e3, 1e3), st.floats(-1e3, 1e3), st.floats(-1e3, 1e3)),
        st.tuples(st.floats(-1e3, 1e3), st.floats(-1e3, 1e3), st.floats(-1e3, 1e3)),
        st.tuples(st.floats(-1e3, 1e3), st.floats(-1e3, 1e3), st.floats(-1e3, 1e3))
    )
    def test_centroid_is_average(self, a, b, c) -> None:
        """Test that the centroid is the arithmetic mean of the three vertices."""
        v1, v2, v3 = Vertex(*a), Vertex(*b), Vertex(*c)
        face = Face3D([v1, v2, v3])
        centroid = face.centroid()
        self.assertAlmostEqual(centroid.x, (v1.x + v2.x + v3.x) / 3)
        self.assertAlmostEqual(centroid.y, (v1.y + v2.y + v3.y) / 3)
        self.assertAlmostEqual(centroid.z, (v1.z + v2.z + v3.z) / 3)

    @given(
        st.tuples(st.floats(-1e5, 1e5), st.floats(-1e5, 1e5), st.floats(-1e5, 1e5)),
        st.tuples(st.floats(-1e5, 1e5), st.floats(-1e5, 1e5), st.floats(-1e5, 1e5)),
        st.tuples(st.floats(-1e5, 1e5), st.floats(-1e5, 1e5), st.floats(-1e5, 1e5)),
        st.tuples(st.floats(-1e5, 1e5), st.floats(-1e5, 1e5), st.floats(-1e5, 1e5))
    )
    def test_distance_consistency(self, a, b, c, p) -> None:
        """Test that the distance returned is within the range of vertex distances."""
        v1, v2, v3, point = Vertex(*a), Vertex(*b), Vertex(*c), Vertex(*p)
        face = Face3D([v1, v2, v3])
        d = face.distance(point)
        vertex_distances = [point.distance(v) for v in [v1, v2, v3]]
        self.assertLessEqual(d, max(vertex_distances))
        self.assertGreaterEqual(d, min(vertex_distances))

"""
Unit tests for the Mesh3D class using unittest and Hypothesis.
"""

__author__ = "Michael Nuttall"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"

import unittest
from unittest.mock import patch
from hypothesis import given, strategies as st
from geometry import Mesh3D, Face3D, Vertex, Shader


class TestMesh3D(unittest.TestCase):
    """Unit tests for the Mesh3D class."""

    def setUp(self) -> None:
        """Set up a basic face and mesh before each test."""
        v1 = Vertex(0, 0, 0)
        v2 = Vertex(1, 0, 0)
        v3 = Vertex(0, 1, 0)
        face = Face3D([v1, v2, v3], Shader(10, 20, 30))
        self.mesh = Mesh3D([face])

    def test_faces_property_set_and_get(self) -> None:
        """Test that faces property getter/setter works correctly."""
        v1, v2, v3 = Vertex(1, 1, 1), Vertex(2, 2, 2), Vertex(3, 3, 3)
        new_face = Face3D([v1, v2, v3], Shader(50, 50, 50))
        self.mesh.faces = [new_face]
        self.assertEqual(self.mesh.faces, [new_face])

    def test_base_shader_and_variance_defaults(self) -> None:
        """Test that base_shader and variance have correct default values."""
        self.assertIsNone(self.mesh.base_shader)
        self.assertEqual(self.mesh.variance, 0)

    def test_set_color_applies_uniform_shader(self) -> None:
        """Test that set_color applies the same shader to all faces."""
        shader = Shader(80, 90, 100)
        self.mesh.set_color(shader)
        self.assertTrue(all(face.color == shader for face in self.mesh.faces))
        self.assertEqual(self.mesh.base_shader, shader)
        self.assertEqual(self.mesh.variance, 0)

    def test_add_face_increases_mesh_length(self) -> None:
        """Test that add() appends a new face to the mesh."""
        original_len = len(self.mesh.faces)
        face = Face3D(
            [Vertex(1, 0, 0), Vertex(0, 1, 0), Vertex(0, 0, 1)],
            Shader(255, 0, 0)
        )
        self.mesh.add(face)
        self.assertEqual(len(self.mesh.faces), original_len + 1)
        self.assertIn(face, self.mesh.faces)

    def test_str_representation_contains_color_data(self) -> None:
        """Test that __str__ returns RGB color summary for all faces."""
        s = str(self.mesh)
        face = self.mesh.faces[0]
        self.assertIn(f"{face.color.r},{face.color.g},{face.color.b}", s)

    def test_repr_representation_contains_debug_info(self) -> None:
        """Test that __repr__ returns detailed internal state."""
        r = repr(self.mesh)
        self.assertIn("Mesh3D", r)
        self.assertIn("num_faces=", r)

    def test_set_color_variance_infers_from_face(self) -> None:
        """Test that set_color_variance uses face color when base is None."""
        expected_base = self.mesh.faces[0].color
        self.mesh.set_color_variance(value=None, variance=15)
        self.assertEqual(self.mesh.base_shader, expected_base)

    def test_set_color_variance_raises_error_on_empty(self) -> None:
        """Test that set_color_variance raises ValueError
        on empty mesh with no base shader."""
        empty_mesh = Mesh3D([])
        with self.assertRaises(ValueError):
            empty_mesh.set_color_variance()

    def test_set_color_variance_abs_variance(self) -> None:
        """Test that negative variance is converted to positive."""
        base_shader = Shader(100, 100, 100)
        self.mesh.set_color_variance(value=base_shader, variance=-25)
        self.assertEqual(self.mesh.variance, 25)

    def test_set_color_variance_uses_base_shader(self) -> None:
        """Test that set_color_variance uses stored base_shader if provided."""
        base = Shader(100, 100, 100)
        self.mesh.set_color(base)
        self.mesh.set_color_variance(value=None, variance=10)
        self.assertEqual(self.mesh.base_shader, base)

    @patch("geometry.mesh3d.random.randint", return_value=300)
    def test_color_clamping_upper_bound(self, _mock_randint) -> None:
        """Test that RGB values are clamped to a max of 255."""
        base = Shader(250, 250, 250)
        self.mesh.set_color_variance(base, variance=10)
        for face in self.mesh.faces:
            self.assertLessEqual(face.color.r, 255)
            self.assertLessEqual(face.color.g, 255)
            self.assertLessEqual(face.color.b, 255)

    @patch("geometry.mesh3d.random.randint", return_value=-300)
    def test_color_clamping_lower_bound(self, _mock_randint) -> None:
        """Test that RGB values are clamped to a min of 0."""
        base = Shader(5, 5, 5)
        self.mesh.set_color_variance(base, variance=10)
        for face in self.mesh.faces:
            self.assertGreaterEqual(face.color.r, 0)
            self.assertGreaterEqual(face.color.g, 0)
            self.assertGreaterEqual(face.color.b, 0)

    @patch("geometry.mesh3d.random.randint", return_value=5)
    def test_set_color_variance_with_patch(self, _mock_randint) -> None:
        """Test that set_color_variance modifies colors with bounded RGB shift."""
        base = Shader(100, 100, 100)
        self.mesh.set_color_variance(value=base, variance=10)
        for face in self.mesh.faces:
            self.assertTrue(95 <= face.color.r <= 105)
            self.assertTrue(95 <= face.color.g <= 105)
            self.assertTrue(95 <= face.color.b <= 105)

    @given(
        st.lists(
            st.tuples(
                st.tuples(st.floats(-1000, 1000),
                          st.floats(-1000, 1000), st.floats(-1000, 1000)),
                st.tuples(st.floats(-1000, 1000),
                          st.floats(-1000, 1000), st.floats(-1000, 1000)),
                st.tuples(st.floats(-1000, 1000),
                          st.floats(-1000, 1000), st.floats(-1000, 1000)),
                st.tuples(st.integers(0, 255), st.integers(0, 255),
                          st.integers(0, 255)),
            ),
            min_size=1, max_size=5
        )
    )
    def test_set_color_keeps_face_count(self, face_data) -> None:
        """Test that set_color preserves mesh size and applies the new color."""
        faces = []
        for (v1, v2, v3, color) in face_data:
            f = Face3D(
                [Vertex(*v1), Vertex(*v2), Vertex(*v3)],
                Shader(*color)
            )
            faces.append(f)
        mesh = Mesh3D(faces)
        mesh.set_color(Shader(0, 0, 0))
        self.assertEqual(len(mesh.faces), len(faces))
        for face in mesh.faces:
            self.assertEqual(face.color, Shader(0, 0, 0))

"""A unit test file for Camera"""

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

import unittest
from scene import Camera
from geometry import Vector, Vertex, Point, Face3D, Face2D, Shader
from hypothesis import given, strategies as st


class TestCamera(unittest.TestCase):
    """A unit test class to test Camera
    """

    def setUp(self) -> None:
        """
        Setup method to create a default Camera instance.
        """
        self.origin = Vertex(0.0, 0.0, 0.0)
        self.look_at = Vertex(0.0, 0.0, -1.0)
        self.camera = Camera(self.origin, self.look_at)

    def tearDown(self) -> None:
        """
        Tear down method.
        """
        super().tearDown()

    def test_initial_forward_vector(self) -> None:
        """
        Test initial forward vector.
        """
        self.assertAlmostEqual(self.camera.forward.z, -1.0)

    def test_set_look_at(self) -> None:
        """
        Test changing the look_at point recalculates axes.
        """
        new_look = Vertex(1.0, 0.0, -1.0)
        self.camera.set_look_at(new_look)
        self.assertNotEqual(self.camera.forward, Vector(0.0, 0.0, -1.0))

    def test_is_vertex_in_front_true(self) -> None:
        """
        Test that a vertex in front returns True.
        """
        point_in_front = Vertex(0.0, 0.0, -5.0)
        self.assertTrue(self.camera.is_vertex_in_front(point_in_front))

    def test_is_vertex_in_front_false(self) -> None:
        """
        Test that a vertex behind returns False.
        """
        point_behind = Vertex(0.0, 0.0, 5.0)
        self.assertFalse(self.camera.is_vertex_in_front(point_behind))

    def test_is_face_in_front(self) -> None:
        """
        Test is_face_in_front with mixed vertices.
        """
        face = Face3D([
            Vertex(0.0, 0.0, -5.0),
            Vertex(0.0, 0.0, 5.0),
            Vertex(1.0, 1.0, -5.0)
        ], Shader(255, 255, 255))
        self.assertTrue(self.camera.is_face_in_front(face))

    def test_project_vertex(self) -> None:
        """
        Test projecting a vertex to 2D.
        """
        point = Vertex(0.0, 0.0, -5.0)
        projected = self.camera.project_vertex(point)
        self.assertIsInstance(projected, Point)
        self.assertAlmostEqual(projected.x, 0.0)
        self.assertAlmostEqual(projected.y, 0.0)

    def test_project_face(self) -> None:
        """
        Test projecting a face to 2D.
        """
        face = Face3D([
            Vertex(0.0, 0.0, -5.0),
            Vertex(1.0, 0.0, -5.0),
            Vertex(0.0, 1.0, -5.0)
        ], Shader(255, 255, 255))
        projected_face = self.camera.project_face(face)
        self.assertIsInstance(projected_face, Face2D)
        self.assertEqual(len(projected_face.points), 3)

    @given(
        st.floats(-1000, 1000, allow_nan=False, allow_infinity=False),
        st.floats(-1000, 1000, allow_nan=False, allow_infinity=False),
        st.floats(-1000, 1000, allow_nan=False, allow_infinity=False)
        .filter(lambda z: abs(z) >= 0.000001))
    def test_hypothesis_set_look_at(self, x: float, y: float, z: float) -> None:
        """
        Hypothesis test for set_look_at.
        """
        new_look = Vertex(x, y, z if z != 0 else -1.0)  # avoid z == 0 degenerate case
        self.camera.set_look_at(new_look)
        self.assertIsInstance(self.camera.forward, Vector)
        self.assertIsInstance(self.camera.up, Vector)
        self.assertIsInstance(self.camera.right, Vector)

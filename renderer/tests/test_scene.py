"""
Unit tests for the Scene class using unittest and mocking.
"""

__author__ = "Michael Nuttall"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"

import unittest
from unittest.mock import Mock
from geometry import Point, Mesh3D, Face3D, Vertex, Shader, Face2D
from scene import Scene


class TestScene(unittest.TestCase):
    """Unit tests for the Scene class."""

    def setUp(self) -> None:
        """Create a mock camera and scene for each test."""
        self.v1 = Vertex(0, 0, 0)
        self.v2 = Vertex(1, 0, 0)
        self.v3 = Vertex(0, 1, 0)
        self.face = Face3D([self.v1, self.v2, self.v3], Shader(10, 20, 30))
        self.mesh = Mesh3D([self.face])

        self.mock_camera = Mock()
        self.scene = Scene(self.mock_camera, [self.mesh])

    def test_meshes_property_get_and_set(self) -> None:
        """Test meshes property getter and setter."""
        self.assertEqual(self.scene.meshes, [self.mesh])
        new_mesh = Mesh3D([self.face])
        self.scene.meshes = [new_mesh]
        self.assertEqual(self.scene.meshes, [new_mesh])

    def test_active_cam_property_get_and_set(self) -> None:
        """Test active_cam property getter and setter."""
        new_camera = Mock()
        self.scene.active_cam = new_camera
        self.assertEqual(self.scene.active_cam, new_camera)

    def test_add_appends_new_mesh(self) -> None:
        """Test that add() appends a new mesh to the scene."""
        original_len = len(self.scene.meshes)
        new_mesh = Mesh3D([self.face])
        self.scene.add(new_mesh)
        self.assertEqual(len(self.scene.meshes), original_len + 1)
        self.assertIn(new_mesh, self.scene.meshes)

    def test_make_render_adds_visible_faces(self) -> None:
        """Test make_render adds projected faces for visible geometry."""
        points = [Point(0, 0), Point(1, 0), Point(0, 1)]
        mock_face2d = Face2D(points, 1.0, Shader(0, 0, 0))
        self.mock_camera.is_face_in_front.return_value = True
        self.mock_camera.project_face.return_value = mock_face2d

        render_list = self.scene.make_render()

        self.mock_camera.is_face_in_front.assert_called_once_with(self.face)
        self.mock_camera.project_face.assert_called_once_with(self.face)
        self.assertEqual(render_list, [mock_face2d])

    def test_make_render_skips_invisible_faces(self) -> None:
        """Test make_render skips faces not in front of the camera."""
        self.mock_camera.is_face_in_front.return_value = False

        render_list = self.scene.make_render()

        self.mock_camera.is_face_in_front.assert_called_once_with(self.face)
        self.mock_camera.project_face.assert_not_called()
        self.assertEqual(render_list, [])

    def test_make_render_mixed_visibility_faces(self) -> None:
        """Test make_render includes only visible faces from multiple meshes."""
        # Create two distinct faces
        face1b = Face3D([self.v1, self.v2, self.v3], Shader(25, 25, 25))
        face2a = Face3D([self.v1, self.v2, self.v3], Shader(50, 50, 50))
        face2b = Face3D([self.v1, self.v2, self.v3], Shader(75, 75, 75))

        # Two meshes with 2 faces each
        mesh1 = Mesh3D([self.face, face1b])
        mesh2 = Mesh3D([face2a, face2b])
        self.scene.meshes = [mesh1, mesh2]

        # Configure camera to see only first and third faces
        self.mock_camera.is_face_in_front.side_effect = [True, False, True, False]

        # Expected projected Face2D objects for visible faces
        points = [Point(0, 0), Point(1, 0), Point(0, 1)]
        f2d_1 = Face2D(points, 1.0, Shader(100, 100, 100))
        f2d_2 = Face2D(points, 2.0, Shader(150, 150, 150))
        self.mock_camera.project_face.side_effect = [f2d_1, f2d_2]

        # Call and assert
        result = self.scene.make_render()

        self.assertEqual(result, [f2d_1, f2d_2])
        self.assertEqual(self.mock_camera.project_face.call_count, 2)
        self.assertEqual(self.mock_camera.is_face_in_front.call_count, 4)

    def test_make_render_on_empty_scene(self) -> None:
        """Test make_render returns empty list if no meshes exist."""
        self.scene.meshes = []
        result = self.scene.make_render()
        self.assertEqual(result, [])
        self.mock_camera.is_face_in_front.assert_not_called()
        self.mock_camera.project_face.assert_not_called()

    def test_make_render_uses_updated_camera(self) -> None:
        """Test that setting a new camera changes behavior of make_render."""
        # Create a second mock camera with different behavior
        alt_camera = Mock()
        alt_camera.is_face_in_front.return_value = True

        points = [Point(0, 0), Point(1, 0), Point(0, 1)]
        alt_face2d = Face2D(points, 3.0, Shader(200, 200, 200))
        alt_camera.project_face.return_value = alt_face2d

        self.scene.active_cam = alt_camera
        result = self.scene.make_render()

        alt_camera.is_face_in_front.assert_called_once_with(self.face)
        alt_camera.project_face.assert_called_once_with(self.face)
        self.assertEqual(result, [alt_face2d])

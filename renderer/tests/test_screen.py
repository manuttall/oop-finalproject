"""A unit test file for Screen """

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

import unittest
from unittest.mock import patch, MagicMock
from hypothesis import given, strategies as st

from scene import Screen, AspectRatio
from geometry import Point, Face2D, Shader


class TestScreen(unittest.TestCase):
    """a unit test class for Screen"""
    def setUp(self) -> None:
        """
        Setup method.
        """
        self.aspect_ratio = AspectRatio(4, 3)
        self.resolution = 100
        self.shader = Shader(255, 255, 255)
        self.screen = Screen(self.aspect_ratio, self.resolution, self.shader)

    def tearDown(self) -> None:
        """
        Tear down method.
        """
        super().tearDown()

    def test_constructor_initializes_attributes(self) -> None:
        """Test the constctor and all its atrabuts
        """
        self.assertEqual(self.screen._aspect_ratio, self.aspect_ratio)
        self.assertEqual(self.screen._resolution, self.resolution)
        self.assertEqual(self.screen._canvas_width, 400)
        self.assertEqual(self.screen._canvas_height, 300)
        self.assertEqual(self.screen._background, self.shader.hex)
        self.assertIsNone(self.screen._window)
        self.assertIsNone(self.screen._canvas)

    @patch("scene.screen.tk.Tk")
    @patch("scene.screen.tk.Canvas")
    def test_create_canvas(self, mock_canvas: MagicMock, mock_tk: MagicMock) -> None:
        """tester for create canvas

        Args:
            mock_canvas (_type_): test canvas
            mock_tk (_type_): test tk
        """
        mock_window = MagicMock()
        mock_tk.return_value = mock_window
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance

        self.screen._create_canvas()

        mock_tk.assert_called_once()
        mock_window.title.assert_called_once_with("3D Renderer")
        mock_canvas.assert_called_once_with(
            mock_window,
            width=400,
            height=300,
            bg=self.shader.hex
        )
        mock_canvas_instance.pack.assert_called_once()
        self.assertIsNotNone(self.screen._window)
        self.assertIsNotNone(self.screen._canvas)

    @given(x=st.integers(0, 10), y=st.integers(0, 10))
    def test_translate_point(self, x: int, y: int) -> None:
        """ensure that translation of points  oprates properly

        Args:
            x (int): x cord
            y (int): y cord
        """
        point = Point(float(x), float(y))
        translated = self.screen._translate_point(point)
        expected_x = int((point.x + self.aspect_ratio.horizontal / 2) * self.resolution)
        expected_y = int((-point.y + self.aspect_ratio.vertical / 2) * self.resolution)
        self.assertEqual(translated.x, expected_x)
        self.assertEqual(translated.y, expected_y)

    @patch.object(Screen, "_translate_point")
    def test_draw_face_raises_without_canvas(self,
                                             mock_translate_point: MagicMock) -> None:
        """test draw faces without canvas

        Args:
            mock_translate_point (_type_): mock point
        """
        face = Face2D([Point(0, 0), Point(1, 0), Point(0, 1)], 0.5, Shader(255, 0, 0))
        with self.assertRaises(RuntimeError):
            self.screen._draw_face(face)

    @patch.object(Screen, "_translate_point", side_effect=lambda p: p)
    def test_draw_face_draws_on_canvas(self, mock_translate_point: MagicMock) -> None:
        """test face draw

        Args:
            mock_translate_point (_type_): point
        """
        face = Face2D([Point(0, 0), Point(1, 0), Point(0, 1)], 0.5, Shader(255, 0, 0))
        self.screen._canvas = MagicMock()
        self.screen._draw_face(face)
        coords = [(p.x, p.y) for p in face.points]
        self.screen._canvas.create_polygon.assert_called_once_with(
            coords,
            fill=face.color.hex,
            outline=""
        )

    @patch.object(Screen, "_draw_face")
    def test_draw_faces_sorts_and_draws(self, mock_draw_face: MagicMock) -> None:
        """test the sort to draw faces

        Args:
            mock_draw_face (_type_): sort faces
        """
        face1 = Face2D([Point(0, 0), Point(1, 0), Point(0, 1)], 0.2, Shader(255, 0, 0))
        face2 = Face2D([Point(1, 1), Point(2, 1), Point(1, 2)], 0.5, Shader(0, 255, 0))
        faces = [face1, face2]
        self.screen._draw_faces(faces)
        
        calls = [(face2,), (face1,)]
        self.assertEqual(
            [call.args for call in mock_draw_face.call_args_list],
            calls
        )

    @patch.object(Screen, "_create_canvas")
    @patch.object(Screen, "_window", create=True)
    def test_show_creates_canvas_and_mainloop(self, mock_window: MagicMock,
                                              mock_create_canvas: MagicMock) -> None:
        """test the create canvas

        Args:
            mock_window (_type_): mock window
            mock_create_canvas (_type_): mock canvas
        """
        # Case when _window is None, triggers _create_canvas and mainloop
        self.screen._window = None
        mock_window.mainloop = MagicMock()
        self.screen.show()
        mock_create_canvas.assert_called_once()
        # Case when _window is set, skips _create_canvas but calls mainloop
        self.screen._window = MagicMock()
        self.screen.show()
        self.screen._window.mainloop.assert_called_once()

    @patch.object(Screen, "_create_canvas")
    @patch.object(Screen, "_draw_faces")
    def test_render_creates_canvas_draws_faces(self, mock_draw_faces: MagicMock,
                                               mock_create_canvas: MagicMock) -> None:
        """test render with a create canvas and draw

        Args:
            mock_draw_faces (_type_): draw face
            mock_create_canvas (_type_): create canvas
        """
        face = Face2D([Point(0, 0), Point(1, 0), Point(0, 1)], 0.5, Shader(255, 0, 0))
        faces = [face]
        self.screen.render(faces)
        mock_create_canvas.assert_called_once()
        mock_draw_faces.assert_called_once_with(faces)

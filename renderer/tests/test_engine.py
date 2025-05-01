"""
Unit tests for the Endgen class.
"""

__author__ = "Arin Hartung"
__date__ = "2025/05/01"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

import unittest
from unittest.mock import MagicMock, patch
from engine import Engine


class TestEngine(unittest.TestCase):
    """Tests for the Engine class."""

    def setUp(self) -> None:
        """Set up the Engine instance."""
        Engine._instance = None  # Reset singleton
        self.engine = Engine()

    def test_singleton_behavior(self) -> None:
        """Test that Engine enforces singleton pattern."""
        e1 = Engine()
        e2 = Engine()
        self.assertIs(e1, e2)

    def test_load_scene_initializes_scene_and_screen(self) -> None:
        """Test loading scene correctly sets up scene and screen."""
        with patch("engine.FileImport") as mock_file_import, \
             patch("engine.Camera") as mock_camera, \
             patch("engine.Scene") as mock_scene, \
             patch("engine.Screen") as mock_screen, \
             patch("engine.Shader") as mock_shader:

            mock_file_import.return_value.read_file.return_value = [MagicMock()]
            settings = {
                "filepath": "assets/demo.obj",
                "camera_origin": (0.0, 0.0, 0.0),
                "look_at": (0.0, 0.0, -1.0),
                "aspect_ratio": (16, 9),
                "resolution": 1080,
                "variance": 1,
                "background_color": (0, 0, 0),
            }

            self.engine.load_scene(settings)

            self.assertIsNotNone(self.engine._scene)
            self.assertIsNotNone(self.engine._screen)
            mock_file_import.return_value.read_file.assert_called_once_with(
                settings["filepath"])
            mock_camera.assert_called_once()
            mock_scene.assert_called_once()
            mock_screen.assert_called_once()
            mock_shader.assert_called_once()

    def test_render_scene_success(self) -> None:
        """Test that render_scene calls screen render and show."""
        mock_face = MagicMock()
        mock_screen = MagicMock()
        mock_scene = MagicMock()
        mock_scene.make_render.return_value = [mock_face]

        self.engine._scene = mock_scene
        self.engine._screen = mock_screen

        self.engine.render_scene()

        mock_scene.make_render.assert_called_once()
        mock_screen.render.assert_called_once_with([mock_face])
        mock_screen.show.assert_called_once()

    def test_render_scene_without_init_raises(self) -> None:
        """Test that render_scene raises if scene or screen is uninitialized."""
        with self.assertRaises(RuntimeError):
            self.engine.render_scene()

    @patch("engine.Interface")
    @patch("engine.Engine.render_scene")
    @patch("engine.Engine.load_scene")
    def test_main_exits_on_empty_settings(self,
                                          mock_load_scene: MagicMock,
                                          mock_render_scene: MagicMock,
                                          mock_interface: MagicMock) -> None:
        """Test main loop exits when interface returns incomplete settings."""
        mock_interface.return_value.run.side_effect = [None]

        with patch("builtins.print") as mock_print:
            Engine.main()
            mock_print.assert_called_with(
                "Interface was closed or input was incomplete. Exiting.")
        mock_load_scene.assert_not_called()
        mock_render_scene.assert_not_called()

    @patch("engine.Interface")
    @patch("engine.Engine.render_scene")
    @patch("engine.Engine.load_scene")
    def test_main_runs_full_cycle(self,
                                  mock_load_scene: MagicMock,
                                  mock_render_scene: MagicMock,
                                  mock_interface: MagicMock) -> None:
        """Test main runs through one full cycle and exits."""
        settings = {"filepath": "assets/demo.obj"}
        mock_interface.return_value.run.side_effect = [settings, None]

        with patch("builtins.print"):
            Engine.main()

        mock_load_scene.assert_called_once_with(settings)
        mock_render_scene.assert_called_once()

    def test_singleton(self) -> None:
        """test to confirm singleton always returns same instance."""
        e1 = Engine()
        e2 = Engine()
        self.assertIs(e1, e2)

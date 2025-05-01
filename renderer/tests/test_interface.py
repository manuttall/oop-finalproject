"""A unit test file for interface"""

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

import unittest
from unittest.mock import patch, MagicMock

from utility import Interface  # Assuming Interface is in the `interface.py` file


class TestInterface(unittest.TestCase):
    """unit test class to test the Inerface class """

    def setUp(self) -> None:
        """Create an Interface instance for testing."""
        self.interface = Interface()

    @patch("tkinter.Tk")  # Mock Tkinter Tk object to avoid creating a real window
    def test_initialization(self, mock_tk: MagicMock) -> None:
        """Test that the interface initializes correctly."""
        # Initialize the interface (this should call the Tk constructor)
        self.interface = Interface()

        # Check if the Tk constructor was called to create the mock root
        mock_tk.assert_called_once()

        # Alternatively, you can verify the behavior of the mock root directly
        mock_root = mock_tk.return_value
        self.assertEqual(self.interface._root, mock_root)
        self.assertTrue(isinstance(self.interface._root, MagicMock))
        self.interface._root.destroy()

    @patch("tkinter.Entry")  # Mock Tkinter Entry widget
    def test_collect_input_valid(self, mock_entry: MagicMock) -> None:
        """Test valid input collection."""
        # Setup mock entries
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "-0.7 -1 1", "0 0 0.65", "4 3", "300", "10", "30 30 30"
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        self.interface._collect_input()
        

        expected_result = {
            "filepath": "assets/demo.obj",
            "camera_origin": (-0.7, -1.0, 1.0),
            "look_at": (0.0, 0.0, 0.65),
            "aspect_ratio": (4.0, 3.0),
            "resolution": 300,
            "variance": 10,
            "background_color": (30, 30, 30)
        }
        self.assertEqual(self.interface._result, expected_result)

    @patch("tkinter.Entry")  # Mock Entry widget for invalid input
    @patch("tkinter.messagebox.showerror")  # Mock the error popup
    def test_collect_input_invalid(self, mock_ms_box: MagicMock,
                                   mock_entry: MagicMock) -> None:
        """Test invalid input collection."""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "invalid/filepath.obj", "-0.7 -1 1", "0 0 0.65",
            "4 3", "300", "10", "30 30 30"
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        self.interface._collect_input()

        # Ensure the error message is shown
        mock_ms_box.assert_called_with(
            "Input Error", "File not found: assets/invalid/filepath.obj"
        )
        self.interface._root.destroy()

    @patch("tkinter.messagebox.showerror")
    def test_show_error(self, mock_ms_box: MagicMock) -> None:
        """Test if the error popup is displayed."""
        self.interface._show_error("Test error message")
        mock_ms_box.assert_called_with("Input Error", "Test error message")
        self.interface._root.destroy()

    @patch("os.path.isfile", return_value=True)
    def test_window_closing_on_valid_input(self, mock_isfile):
        """Test that the window closes when input is valid."""
        # Set up valid mock entry fields
        self.interface._entry_filepath = MagicMock(
            get=MagicMock(return_value="assets/demo.obj"))
        self.interface._entry_cam_origin = MagicMock(
            get=MagicMock(return_value="0 0 0"))
        self.interface._entry_look_at = MagicMock(
            get=MagicMock(return_value="0 0 1"))
        self.interface._entry_aspect = MagicMock(
            get=MagicMock(return_value="16 9"))
        self.interface._entry_resolution = MagicMock(
            get=MagicMock(return_value="1920"))
        self.interface._entry_variance = MagicMock(
            get=MagicMock(return_value="0"))
        self.interface._entry_bgcolor = MagicMock(
            get=MagicMock(return_value="255 255 255"))

        # Patch the root's destroy method
        self.interface._root = MagicMock()

        # Call the actual method
        self.interface._collect_input()

        # Check that destroy was called
        self.interface._root.destroy.assert_called_once()
        self.interface._root.destroy()

    @patch("tkinter.Entry")
    @patch("tkinter.messagebox.showerror")
    def test_invalid_background_color(self, mock_ms_box: MagicMock,
                                      mock_entry: MagicMock) -> None:
        """Tests for invalid background colors
        """
        mock_entry.get.side_effect = [
            "assets/demo.obj", "-0.7 -1 1", "0 0 0.65",
            "4 3", "300", "10", "300 300"  # Invalid background
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        self.interface._collect_input()

        mock_ms_box.assert_called_with(
            "Input Error",
            "Background color must have three integers between 0 and 255."
        )
        self.interface._root.destroy()

    @patch("tkinter.Entry")  # Mock Tkinter Entry widget
    @patch("tkinter.messagebox.showerror")  # Mock the error popup
    def test_invalid_aspect_ratio(self, mock_ms_box: MagicMock,
                                  mock_entry: MagicMock) -> None:
        """Test invalid aspect ratio input."""
        # Setup mock entries
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "-0.7 -1 1", "0 0 0.65",
            "4 3 4", "300", "10", "30 30 30"  # Invalid aspect ratio input
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        # Call the method that collects input
        self.interface._collect_input()

        # Ensure the error message is shown for the invalid aspect ratio
        mock_ms_box.assert_called_with(
            "Input Error", "Aspect ratio must have exactly two numbers."
        )
        self.interface._root.destroy()

    @patch("tkinter.Entry")  # Mock Tkinter Entry widget
    def test_valid_aspect_ratio(self, mock_entry: MagicMock) -> None:
        """Test valid aspect ratio input."""
        # Setup mock entries for valid input
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "-0.7 -1 1", "0 0 0.65",
            "4 3", "300", "10", "30 30 30"  # Valid aspect ratio input
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        # Call the method that collects input
        self.interface._collect_input()

        # Check if aspect ratio was correctly collected
        expected_result = {
            "filepath": "assets/demo.obj",
            "camera_origin": (-0.7, -1.0, 1.0),
            "look_at": (0.0, 0.0, 0.65),
            "aspect_ratio": (4.0, 3.0),
            "resolution": 300,
            "variance": 10,
            "background_color": (30, 30, 30)
        }
        self.assertEqual(self.interface._result, expected_result)

    @patch("tkinter.Entry")  # Mock Tkinter Entry widget
    @patch("tkinter.messagebox.showerror")  # Mock the error popup
    def test_invalid_aspect_ratio_non_numeric(self, mock_ms_box: MagicMock,
                                              mock_entry: MagicMock) -> None:
        """Test aspect ratio with non-numeric input."""
        # Setup mock entries for invalid aspect ratio input
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "-0.7 -1 1", "0 0 0.65",
            "invalid aspect ratio", "300", "10", "30 30 30"
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        # Call the method that collects input
        self.interface._collect_input()

        # Ensure the error message is shown for the invalid aspect ratio
        mock_ms_box.assert_called_with(
            "Input Error", "could not convert string to float: 'invalid'"
        )
        self.interface._root.destroy()

    @patch("tkinter.Entry")  # Mock Tkinter Entry widget
    @patch("tkinter.messagebox.showerror")  # Mock the error popup
    def test_invalid_aspect_ratio_negative(self, mock_ms_box: MagicMock,
                                           mock_entry: MagicMock) -> None:
        """Test aspect ratio with negative values."""
        # Setup mock entries for invalid aspect ratio input
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "-0.7 -1 1", "0 0 0.65",
            "-4 3", "300", "10", "30 30 30"  # Invalid aspect ratio (negative value)
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        # Call the method that collects input
        self.interface._collect_input()

        # Ensure the error message is shown for the invalid aspect ratio
        mock_ms_box.assert_called_with(
            "Input Error", "Aspect ratio must be positive."
        )
        self.interface._root.destroy()

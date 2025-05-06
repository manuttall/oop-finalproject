"""A unit test file for interface"""

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

import unittest
from unittest.mock import patch, MagicMock

from utility import Interface


class TestInterface(unittest.TestCase):
    """Unit test class to test the Interface class."""

    def setUp(self) -> None:
        """Patch Tkinter's Tk to prevent GUI from launching."""
        self.tk_patcher = patch("tkinter.Tk")
        mock_tk = self.tk_patcher.start()
        mock_root = MagicMock()
        mock_root.tk = MagicMock()
        mock_tk.return_value = mock_root
        self.interface = Interface()

    def tearDown(self) -> None:
        """Stop Tk patcher and destroy mock root."""
        self.tk_patcher.stop()
        try:
            self.interface._root.destroy()
        except AttributeError:
            pass

    @patch("tkinter.Tk")
    def test_initialization(self, mock_tk: MagicMock) -> None:
        """Test that the interface initializes correctly."""
        self.interface = Interface()
        mock_tk.assert_called_once()
        self.assertTrue(isinstance(self.interface._root, MagicMock))

    @patch("os.path.isfile", return_value=True)
    def test_collect_input_valid(self, _mock_isfile: MagicMock) -> None:
        """Test valid input collection."""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "-0.7 -1 1", "0 0 0.65",
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
        self.assertEqual(self.interface._result["resolution"], 300)

    @patch("tkinter.messagebox.showerror")
    def test_collect_input_invalid(self, mock_msg: MagicMock) -> None:
        """Test invalid input path triggers error."""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "badpath.obj", "-0.7 -1 1", "0 0 0.65",
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
        mock_msg.assert_called()

    @patch("os.path.isfile", return_value=True)
    def test_window_closes_on_valid_input(self, mock_file: MagicMock) -> None:
        """Test that window closes when input is valid."""
        self.interface._entry_filepath = MagicMock(
            get=MagicMock(return_value="assets/demo.obj"))
        self.interface._entry_cam_origin = MagicMock(
            get=MagicMock(return_value="0 0 0"))
        self.interface._entry_look_at = MagicMock(get=MagicMock(return_value="0 0 1"))
        self.interface._entry_aspect = MagicMock(get=MagicMock(return_value="16 9"))
        self.interface._entry_resolution = MagicMock(get=MagicMock(return_value="300"))
        self.interface._entry_variance = MagicMock(get=MagicMock(return_value="5"))
        self.interface._entry_bgcolor = MagicMock(
            get=MagicMock(return_value="255 255 255"))

        self.interface._root = MagicMock()
        self.interface._collect_input()
        self.interface._root.destroy.assert_called_once()

    @patch("tkinter.messagebox.showerror")
    def test_invalid_aspect_ratio_non_numeric(self, mock_msg: MagicMock) -> None:
        """Test non-numeric aspect ratio error."""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "0 0 0", "0 0 1",
            "four three", "300", "10", "255 255 255"
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        self.interface._collect_input()
        mock_msg.assert_called()

    @patch("tkinter.messagebox.showerror")
    @patch("os.path.isfile", return_value=True)
    def test_invalid_background_color(self, _mock_file: MagicMock, 
                                      mock_msg: MagicMock) -> None:
        """Test bad background color values."""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "0 0 0", "0 0 1",
            "16 9", "300", "10", "256 0 0"
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        self.interface._collect_input()
        mock_msg.assert_called_with("Input Error", 
                                    "Background color must have three "
                                    "integers between 0 and 255.")

    @patch("tkinter.messagebox.showerror")
    def test_show_error_messagebox(self, mock_msg: MagicMock) -> None:
        """Test custom error display."""
        self.interface._show_error("Bad input")
        mock_msg.assert_called_with("Input Error", "Bad input")

    @patch("tkinter.messagebox.showerror")
    @patch("os.path.isfile", return_value=True)
    def test_invalid_resolution_zero(self, _mock_file: MagicMock,
                                     mock_msg: MagicMock) -> None:
        """Test that resolution must be positive."""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "0 0 0", "0 0 1",
            "16 9", "0", "10", "30 30 30"
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        self.interface._collect_input()
        mock_msg.assert_called_with("Input Error", "Resolution must be positive.")

    @patch("os.path.isfile", return_value=True)
    @patch("tkinter.messagebox.showerror")
    def test_invalid_variance_negative(self, mock_msg: MagicMock,
                                       _mock_file: MagicMock) -> None:
        """Test that variance must be non-negative."""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = [
            "assets/demo.obj", "0 0 0", "0 0 1",
            "16 9", "300", "-5", "30 30 30"  # Negative variance
        ]
        self.interface._entry_filepath = mock_entry
        self.interface._entry_cam_origin = mock_entry
        self.interface._entry_look_at = mock_entry
        self.interface._entry_aspect = mock_entry
        self.interface._entry_resolution = mock_entry
        self.interface._entry_variance = mock_entry
        self.interface._entry_bgcolor = mock_entry

        self.interface._collect_input()
        mock_msg.assert_called_with("Input Error", "Variance must be non-negative.")

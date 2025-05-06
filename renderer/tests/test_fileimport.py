"""
Unit tests for the FileImport class using unittest and mocking.
"""

__author__ = "Michael Nuttall"
__date__ = "2025/05/01"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"

import unittest
from unittest.mock import patch, mock_open
from utility import FileImport
from geometry import Mesh3D

SAMPLE_DATA = """# This is a comment
2
10 20 30
1
v 0 0 0
v 1 0 0
v 0 1 0
255 255 255
1
v 0 0 1
v 1 0 1
v 0 1 1
"""

MALFORMED_RGB = """1
10 20
1
v 0 0 0
v 1 0 0
v 0 1 0
"""

MALFORMED_VERTEX = """1
10 20 30
1
p 0 0 0
v 1 0 0
v 0 1 0
"""

MALFORMED_VERTEX_COUNT = """1
10 20 30
1
v 0 0 0
v 1 0 0
"""


class TestFileImport(unittest.TestCase):
    """Unit tests for the FileImport singleton and mesh parsing logic."""

    def setUp(self) -> None:
        """Reset singleton for clean test state."""
        FileImport._instance = None  # pylint: disable=protected-access
        self.importer = FileImport()

    def test_singleton_instance(self) -> None:
        """Test that FileImport is a singleton."""
        a = FileImport()
        b = FileImport()
        self.assertIs(a, b)

    @patch("builtins.open", new_callable=mock_open, read_data=SAMPLE_DATA)
    def test_read_data_skips_comments(self, _mock_file) -> None:
        """Test read_data skips comment lines and loads others."""
        self.importer.read_data("mock.obj")
        data = self.importer.get_data()

        self.assertTrue(all(not line.startswith("#") and line for line in data))

        expected_lines = [line for line in SAMPLE_DATA.splitlines()
                          if line.strip() and not line.strip().startswith("#")]
        self.assertEqual(len(data), len(expected_lines))

    def test_make_list_raises_without_data(self) -> None:
        """Test make_list raises ValueError if called with no data."""
        with self.assertRaises(ValueError):
            self.importer.make_list()

    @patch("builtins.open", new_callable=mock_open, read_data=SAMPLE_DATA)
    def test_read_file_returns_mesh_list(self, _mock_file) -> None:
        """Test read_file parses multiple Mesh3D objects."""
        meshes = self.importer.read_file("mock.obj")
        self.assertIsInstance(meshes, list)
        self.assertEqual(len(meshes), 2)
        self.assertTrue(all(isinstance(m, Mesh3D) for m in meshes))

    @patch("builtins.open", new_callable=mock_open, read_data=MALFORMED_RGB)
    def test_read_file_raises_on_invalid_rgb(self, _mock_file) -> None:
        """Test ValueError is raised on malformed RGB line."""
        with self.assertRaises(ValueError):
            self.importer.read_file("mock.obj")

    @patch("builtins.open", new_callable=mock_open, read_data=MALFORMED_VERTEX)
    def test_read_file_raises_on_invalid_vertex(self, _mock_file) -> None:
        """Test ValueError is raised if line does not start with 'v'."""
        with self.assertRaises(ValueError):
            self.importer.read_file("mock.obj")

    @patch("builtins.open", new_callable=mock_open, read_data=SAMPLE_DATA)
    def test_get_data_returns_internal_lines(self, _mock_file) -> None:
        """Test get_data returns list of parsed strings."""
        self.importer.read_data("mock.obj")
        data = self.importer.get_data()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    @patch("builtins.open", new_callable=mock_open, read_data=MALFORMED_VERTEX_COUNT)
    def test_read_file_raises_on_incomplete_face(self, _mock_file) -> None:
        """Test ValueError is raised if a face has fewer than 3 vertices."""
        with self.assertRaises(ValueError):
            self.importer.read_file("mock.obj")

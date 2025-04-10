
"""
Unittesting Point class
"""

import unittest
from geometry.point import Point

__author__ = "Arin Hartung"
__date__ = "2025/4/10"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"


class TestPoint(unittest.TestCase):
    """
    Unittesting Point class
    """

    def setUp(self) -> None:
        """
        Setup method
        :return: None
        """
        self.point = Point(3, 2)

    def test_set_x(self) -> None:
        """
        Tests setx method
        """
        self.point.x = 0
        self.assertEqual(self.point.x, 0)

    def test_get_x(self) -> None:
        """
        Tests getx method
        """
        self.assertEqual(self.point.x, 3)

    def test_set_y(self) -> None:
        """
        Tests setY method
        """
        self.point.y = 0
        self.assertEqual(self.point.y, 0)

    def test_get_y(self) -> None:
        """
        Tests getY method
        """
        self.assertEqual(self.point.y, 2)

    def test_eq(self) -> None:
        """
        Tests eq method
        :return: None
        """
        self.assertFalse(self.point == Point(0, 0))

    def test_eq_not_implemented(self) -> None:
        """
        Tests __eq__ method not implemented exeception
        """
        self.assertRaises(NotImplementedError, self.point.__eq__, 0)

    def tearDown(self) -> None:
        """
        Tear down method
        :return: None
        """
        super().tearDown()

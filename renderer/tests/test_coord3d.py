"""a test class for the abstract coord3d """

__author__ = "Arin Hartung"
__date__ = "2025/04/30"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

import unittest
from geometry.coord3d import Coordinate3D
from hypothesis import given, strategies as st


class DummyCoordinate3D(Coordinate3D):
    """A test class for Coord3d

    Args:
        Coordinate3D (_type_): parent class
    """
    def __repr__(self) -> str:
        return f"DummyCoordinate3D({self._x}, {self._y}, {self._z})"


class TestCoordinate3D(unittest.TestCase):
    """Unit tests for the Coordinate3D abstract base class."""

    def setUp(self) -> None:
        self.coord = DummyCoordinate3D(1.0, 2.0, 3.0)

    def test_constructor(self) -> None:
        """Test constructor initializes x, y, z correctly."""
        self.assertEqual(self.coord.x, 1.0)
        self.assertEqual(self.coord.y, 2.0)
        self.assertEqual(self.coord.z, 3.0)

    def test_x_property_get_set(self) -> None:
        """Test x property getter and setter."""
        self.coord.x = 10.0
        self.assertEqual(self.coord.x, 10.0)

    def test_y_property_get_set(self) -> None:
        """Test y property getter and setter."""
        self.coord.y = 20.0
        self.assertEqual(self.coord.y, 20.0)

    def test_z_property_get_set(self) -> None:
        """Test z property getter and setter."""
        self.coord.z = 30.0
        self.assertEqual(self.coord.z, 30.0)

    @given(
        st.floats(allow_nan=False, allow_infinity=False),
        st.floats(allow_nan=False, allow_infinity=False),
        st.floats(allow_nan=False, allow_infinity=False)
    )
    def test_properties_with_hypothesis(self, x: float, y: float, z: float) -> None:
        """Test properties with varied float inputs."""
        coord = DummyCoordinate3D(x, y, z)
        self.assertEqual(coord.x, x)
        self.assertEqual(coord.y, y)
        self.assertEqual(coord.z, z)

    def test_repr(self) -> None:
        """Test __repr__ returns expected string."""
        expected = "DummyCoordinate3D(1.0, 2.0, 3.0)"
        self.assertEqual(repr(self.coord), expected)

    def test_x_property_invalid_type(self) -> None:
        """Test setting x to invalid type does not raise, but stores value."""
        # Note: current setter has no type check; this test shows the risk.
        self.coord.x = 'not_a_number'  # type: ignore
        self.assertEqual(self.coord.x, 'not_a_number')

    def test_y_property_invalid_type(self) -> None:
        """Test setting y to invalid type does not raise, but stores value."""
        self.coord.y = None  # type: ignore
        self.assertIsNone(self.coord.y)

    def test_z_property_invalid_type(self) -> None:
        """Test setting z to invalid type does not raise, but stores value."""
        self.coord.z = [1, 2, 3]  # type: ignore
        self.assertEqual(self.coord.z, [1, 2, 3])

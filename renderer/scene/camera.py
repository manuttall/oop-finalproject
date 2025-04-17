"""Camera class for defining a viewpoint in 3D space."""

from __future__ import annotations
from geometry.vertex import Vertex
from geometry.vector import Vector
from scene.aspect_ratio import AspectRatio

__author__ = "Michael Nuttall"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


class Camera(Vertex):
    """A camera defined by its position and orientation in 3D space."""

    def __init__(self, origin: Vertex, look_at: Vertex,
                 aspect_ratio: AspectRatio, resolution: int) -> None:
        """Constructor

        Args:
            origin (Vertex): the camera's position in 3D space
            look_at (Vertex): the point the camera is looking at
            aspect_ratio (AspectRatio): object containing vertical and horizontal aspect
            resolution (int): resolution multiplier for converting
                              projected coordinates to canvas space
        """
        super().__init__(origin.x, origin.y, origin.z)

        self._look_at = look_at
        self._aspect_ratio = aspect_ratio
        self._resolution = resolution

        self._forward: Vector = Vector(0, 0, -1)
        self._up: Vector = Vector(0, 1, 0)
        self._right: Vector = Vector(1, 0, 0)

        self._recalculate_axes()

    def _recalculate_axes(self) -> None:
        """Private method to recalculate the camera's forward, right, and up vectors.

        The forward vector is the normalized direction from the
        camera's origin to the look-at point.
        The right vector is perpendicular to the forward and a world-up vector.
        The up vector is perpendicular to both the right and forward vectors.
        All vectors are normalized.
        """
        forward = (self._look_at - self).normalize()
        world_up = Vector(0, 1, 0)

        right = forward.cross(world_up).normalize()
        up = right.cross(forward).normalize()

        self._forward = forward
        self._right = right
        self._up = up

    def set_look_at(self, new_look_at: Vertex) -> None:
        """Sets a new look-at point for the camera and updates its orientation.

        Args:
            new_look_at (Vertex): the new point the camera should look at
        """
        self._look_at = new_look_at
        self._recalculate_axes()

    @property
    def forward(self) -> Vector:
        """Returns the forward (view direction) vector of the camera.

        Returns:
            Vector: normalized forward vector
        """
        return self._forward

    @property
    def up(self) -> Vector:
        """Returns the up vector of the camera.

        Returns:
            Vector: normalized up vector
        """
        return self._up

    @property
    def right(self) -> Vector:
        """Returns the right vector of the camera.

        Returns:
            Vector: normalized right vector
        """
        return self._right

    @property
    def resolution(self) -> int:
        """Returns the resolution multiplier used for canvas scaling.

        Returns:
            int: resolution value
        """
        return self._resolution

    @property
    def aspect_ratio(self) -> AspectRatio:
        """Returns the camera's aspect ratio.

        Returns:
            AspectRatio: the stored aspect ratio object
        """
        return self._aspect_ratio
    

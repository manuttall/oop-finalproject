"""Camera class for defining a viewpoint in 3D space."""

from __future__ import annotations
from typing import List
from geometry import Face3D, Face2D, Vector, Vertex, Point, Shader

__author__ = "Michael Nuttall"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


class Camera(Vertex):
    """A camera defined by its position and orientation in 3D space."""

    def __init__(self, origin: Vertex, look_at: Vertex) -> None:
        """Constructor

        Args:
            origin (Vertex): Camera's position in 3D space.
            look_at (Vertex): Point the camera looks at.
        """
        super().__init__(origin.x, origin.y, origin.z)
        self._look_at: Vertex = look_at
        self._forward: Vector = Vector(0.0, 0.0, -1.0)
        self._up: Vector = Vector(0.0, 1.0, 0.0)
        self._right: Vector = Vector(1.0, 0.0, 0.0)

        self._recalculate_axes()

    def _recalculate_axes(self) -> None:
        """Recalculates the camera's forward, right, and up vectors
        based on current look_at."""
        temp_vec = Vector(self._look_at.x, self._look_at.y, self._look_at.z)
        forward: Vector = (temp_vec - self).normalize
        world_up = Vector(0.0, 0.0, 1.0)

        if abs(forward.dot(world_up)) >= 0.999:
            world_up = Vector(0.0, 1.0, 0.0)

        right: Vector = forward.cross(world_up).normalize
        up: Vector = right.cross(forward).normalize

        self._forward = forward
        self._right = right
        self._up = up

    def set_look_at(self, new_look_at: Vertex) -> None:
        """Sets a new look-at point for the camera and recalculates axes.

        Args:
            new_look_at (Vertex): New target point for the camera.
        """
        self._look_at = new_look_at
        self._recalculate_axes()

    @property
    def forward(self) -> Vector:
        """Returns the forward (view direction) vector.

        Returns:
            Vector: Normalized forward vector.
        """
        return self._forward

    @property
    def up(self) -> Vector:
        """Returns the up vector.

        Returns:
            Vector: Normalized up vector.
        """
        return self._up

    @property
    def right(self) -> Vector:
        """Returns the right vector.

        Returns:
            Vector: Normalized right vector.
        """
        return self._right

    def is_vertex_in_front(self, vertex: Vertex) -> bool:
        """Checks if a 3D vertex is in front of the camera.

        Args:
            vertex (Vertex): 3D vertex to check.

        Returns:
            bool: True if vertex is in front, else False.
        """
        to_vertex: Vector = vertex - self
        return to_vertex.dot(self._forward) > 0

    def is_face_in_front(self, face: Face3D) -> bool:
        """Checks if any vertex of a face is in front of the camera.

        Args:
            face (Face3D): Face composed of 3 vertices.

        Returns:
            bool: True if any vertex is in front.
        """
        return any(self.is_vertex_in_front(vertex) for vertex in face.points)

    def project_vertex(self, vertex: Vertex) -> Point:
        """Projects a 3D vertex onto the camera's 2D space.

        Args:
            vertex (Vertex): 3D vertex to project.

        Returns:
            Point: 2D projected point.
        """
        to_vertex: Vector = vertex - self
        x_cam: float = to_vertex.dot(self._right)
        y_cam: float = to_vertex.dot(self._up)
        z_cam: float = to_vertex.dot(self._forward)

        x_proj = x_cam / z_cam
        y_proj = y_cam / z_cam

        return Point(x_proj, y_proj)

    def project_face(self, face: Face3D) -> Face2D:
        """Projects a 3D face onto 2D space.

        Args:
            face (Face3D): 3D face.

        Returns:
            Face2D: 2D projection of the face.
        """
        projected_points: List[Point] = [
            self.project_vertex(vertex) for vertex in face.points
        ]
        dist: float = face.distance(self)
        color: Shader = face.color
        return Face2D(projected_points, dist, color)

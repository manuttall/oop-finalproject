"""Camera class for defining a viewpoint in 3D space."""

from __future__ import annotations
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
            origin (Vertex): the camera's position in 3D space
            look_at (Vertex): the point the camera is looking at
        """
        super().__init__(origin.x, origin.y, origin.z)

        self._look_at = look_at

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
        temp_vec = Vector(self._look_at.x, self._look_at.y, self._look_at.z)
        forward: Vector = (temp_vec - self).normalize()
        world_up = Vector(0, 1, 0)
        # If forward is parallel or antiparallel to world_up, use a fallback up vector
        if abs(forward.dot(world_up)) >= 0.999:  # Allow small epsilon
            world_up = Vector(0, 0, 1)  # Use a different up vector to prevent degeneracy

        print(temp_vec.x, temp_vec.y, temp_vec.z)
        print(self.x, self.y, self.z)
        print(forward.x, forward.y, forward.z)

        right: Vector = forward.cross(world_up).normalize()
        up: Vector = right.cross(forward).normalize()

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

    def is_vertex_in_front(self, vertex: Vertex) -> bool:
        """Checks if a given 3D vertex is in front of the camera.

        A point is considered in front if the dot product between the
        vector from the camera to the point and the forward vector is positive.

        Args:
            vertex (Vertex): the 3D point to check

        Returns:
            bool: True if the point is in front of the camera, False otherwise
        """
        to_vertex = vertex - self
        return to_vertex.dot(self._forward) > 0

    def is_face_in_front(self, face: Face3D) -> bool:
        """Checks if any vertex of the face is in front of the camera.

        Args:
            face (Face3D): a 3D face composed of vertices

        Returns:
            bool: True if any vertex is in front of the camera
        """
        return any(self.is_vertex_in_front(vertex) for vertex in face.points)

    def project_vertex(self, vertex: Vertex) -> Point:
        """Projects a 3D vertex onto the camera's 2D canvas space.

        This uses a perspective projection and maps the resulting coordinates
        to canvas space using the camera's aspect ratio and resolution.

        Args:
            vertex (Vertex): the 3D point to project

        Returns:
            Point: the corresponding 2D point on the canvas
        """
        # Compute vector from camera to the vertex
        to_vertex: Vector = vertex - self  # Vector from camera origin to vertex

        # Project onto camera's coordinate frame
        x_cam = to_vertex.dot(self._right)
        y_cam = to_vertex.dot(self._up)
        z_cam = to_vertex.dot(self._forward)

        # Perspective divide (assumes z_cam is positive and checked externally)
        x_proj = x_cam / z_cam
        y_proj = y_cam / z_cam

        # Canvas scaling
        # h = self._aspect_ratio.horizontal
        # v = self._aspect_ratio.vertical
        # s = self._resolution
        #
        # x_canvas = int((x_proj + h / 2) * s)
        # y_canvas = int((-y_proj + v / 2) * s)

        return Point(x_proj, y_proj)

    def project_face(self, face: Face3D) -> Face2D | None:
        """Projects a 3D face onto the camera's 2D canvas.

        Args:
            face (Face3D): the 3D triangle to project

        Returns:
            Face2D: the 2D projection of the face
        """
        projected_points: list[Point] = [
            self.project_vertex(vertex) for vertex in face.points
        ]

        # Use Face3D's distance from the camera origin
        dist: float = face.distance(self)
        # Preserve face Shader
        color: Shader = face.color

        return Face2D(projected_points, dist, color)

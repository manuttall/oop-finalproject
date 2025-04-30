"""Scene class to represent a collection of 3D meshes."""

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/17"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry import Mesh3D, Face2D
from scene.camera import Camera


class Scene:
    """Scene class to represent a collection of 3D meshes."""

    def __init__(self, active_cam: Camera, meshes: List[Mesh3D]) -> None:
        """Constructor

        Args:
            active_cam (Camera): The active camera for rendering.
            meshes (List[Mesh3D]): List of 3D meshes in the scene.
        """
        self._active_cam: Camera = active_cam
        self._meshes: List[Mesh3D] = meshes

    @property
    def meshes(self) -> List[Mesh3D]:
        """Property to get all meshes in the scene.

        Returns:
            List[Mesh3D]: Meshes in the scene.
        """
        return self._meshes

    @meshes.setter
    def meshes(self, value: List[Mesh3D]) -> None:
        """Property to set the meshes in the scene.

        Args:
            value (List[Mesh3D]): New list of meshes.
        """
        self._meshes = value

    @property
    def active_cam(self) -> Camera:
        """Property to get the active camera.

        Returns:
            Camera: Active camera for the scene.
        """
        return self._active_cam

    @active_cam.setter
    def active_cam(self, value: Camera) -> None:
        """Property to set the active camera.

        Args:
            value (Camera): New active camera.
        """
        self._active_cam = value

    def add(self, new_mesh: Mesh3D) -> None:
        """Adds a new mesh to the scene.

        Args:
            new_mesh (Mesh3D): New mesh to add.
        """
        self._meshes.append(new_mesh)

    def make_render(self) -> List[Face2D]:
        """Creates a render list of 2D faces from visible 3D meshes.

        Projects visible faces onto 2D space based on camera view.

        Returns:
            List[Face2D]: List of 2D projected faces.
        """
        render_list: List[Face2D] = []
        for mesh in self._meshes:
            for face in mesh.faces:
                if self._active_cam.is_face_in_front(face):
                    render_mesh: Face2D = self._active_cam.project_face(face)
                    render_list.append(render_mesh)
        return render_list

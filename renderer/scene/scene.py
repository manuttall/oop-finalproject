"""scene class to represent a colection of 3d Meshes"""

__author__ = "Arin Hartung"
__date__ = "2025/04/17"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry import Mesh3D, Face2D
from renderer.scene.camera import Camera


class Scene:
    """scene class to represent a colection of 3d Meshes
    """
    def __init__(self, active_cam: Camera, meshes: List[Mesh3D]):
        """constructor for Mesh3d

        Args:
            meshes (List[Mesh3D]): a list of meshes in the Scene
        """
        self._active_cam = active_cam
        self._meshes = meshes

    @property
    def meshes(self) -> List[Mesh3D]:
        """Property to get meshes

        Returns:
            list [Mesh3D] - meshes
        """
        return self._meshes

    @meshes.setter
    def meshes(self, value: List[Mesh3D]) -> None:
        """Property to set meshes

        Args:
            value (List[Mesh3D]): meshes
        """
        self._meshes = value

    @property
    def active_cam(self) -> Camera:
        """Property to get active_cam

        Returns:
            Camera - active_cam
        """
        return self._active_cam

    @active_cam.setter
    def active_cam(self, value: Camera) -> None:
        """Property to set active_cam

        Args:
            value (Camera): active_cam
        """
        self._active_cam = value

    def add(self, new_mesh: Mesh3D) -> None:
        """adds a Mesh3D to the mesh list

        Args:
            new_face (Mesh3D): new face to add
        """
        self._meshes.append(new_mesh)

    def make_render(self) -> List[Face2D]:
        """makes a Face 2d render list from active cam
        and meshes then returns it

        Returns:
            List[Face2D]: Face 2d render list
        """
        render_list: List[Face2D] = []
        for mesh in self._meshes:
            for face in mesh.faces:
                if self.active_cam.is_face_in_front(face):
                    render_mesh: Face2D = self.active_cam.project_face(face)
                    render_list.append(render_mesh)
        return render_list

"""scene class to represent a colection of 3d Meshes"""

__author__ = "Arin Hartung"
__date__ = "2025/04/17"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry.mesh3d import Mesh3D


class Scene:
    """scene class to represent a colection of 3d Meshes
    """
    def __init__(self, meshes: List[Mesh3D]):
        """constructor for Mesh3d

        Args:
            meshes (List[Mesh3D]): a list of meshes in the Scene
        """
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

    def add(self, new_mesh: Mesh3D) -> None:
        """adds a Mesh3D to the mesh list

        Args:
            new_face (Mesh3D): new face to add
        """
        position = len(self.meshes)
        self._meshes[position] = new_mesh

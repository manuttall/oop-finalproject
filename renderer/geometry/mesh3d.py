"""Mesh class to represent a colection of 3d faces"""

__author__ = "Arin Hartung"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
from geometry.face3d import Face3D
from geometry.shader import Shader


class Mesh3D:
    """Mesh class to represent a colection of 3d faces
    """
    def __init__(self, faces: List[Face3D]):
        """constructor for Mesh3d

        Args:
            faces (List[Face3D]): a list of faces in Mesh
        """
        self._faces = faces

    @property
    def faces(self) -> List[Face3D]:
        """Property to get faces

        Returns:
            list[Face3d] : faces
        """
        return self._faces

    @faces.setter
    def faces(self, value: List[Face3D]) -> None:
        """Property to set faces

        Args:
            value (List[Face3D]): faces
        """
        self._faces = value

    def set_color(self, value: Shader) -> None:
        """Changes the color for every face in the mesh

        Args:
            value Shader
        """
        for face in self._faces:
            face.color(value)

    def add(self, new_face: Face3D) -> None:
        """adds a face3D to the mesh list

        Args:
            new_face (Face3D): new face to add
        """
        self._faces.append(new_face)

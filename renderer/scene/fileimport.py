"""a singleton class to open and collect data from files"""

from __future__ import annotations
from typing import List
from geometry.mesh3d import Mesh3D
from geometry.face3d import Face3D
from geometry.vertex import Vertex
from geometry.shader import Shader

__author__ = "Arin Hartung"
__date__ = "2025/04/26"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"


class FileImport():
    """A file Import class

    Raises:
        NameError: if mutible instance exist

    Returns:
        None
    """
    _instance: 'FileImport' | None = None

    def __init__(self) -> None:
        self._instance = self

        if FileImport._instance:
            raise NameError(
                "Cannot create multiple instances of \
                a singleton class FileImport")
        FileImport._instance = self
        self._data: str = ''

    def read_data(self, filepath: str) -> None:
        """reads in file data
            ignores lines with ___
        Args:
            filepath (str): file path
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            self._data = [
                line.strip() for line in file
                if line.strip() and not line.strip().startswith("#")
            ]

    def make_list(self) -> List[Mesh3D]:
        """Creates a mesh List from file data

        Raises:
            ValueError: No data
            ValueError: 3 ints for RGB
            ValueError: v line for vertexs
            ValueError: must have 3 vertexes

        Returns:
            List[Mesh3D]: list of Mesh 3d from File
        """
        if not self._data:
            raise ValueError("no data loaded")

        iterator = 0
        num_meshes = int(self._data[iterator])
        iterator += 1

        list_mesh: List[Mesh3D] = []

        for _ in range(num_meshes):
            # read RGB
            color = list(map(int, self._data[iterator].split()))
            if len(color) != 3:
                raise ValueError(f"Expected 3 int for RGB, got: {color}")
            mesh_shader = Shader(color[0], color[1], color[2])
            iterator += 1

            # read face count
            num_faces = int(self._data[iterator])
            iterator += 1

            list_faces: List[Face3D] = []
            for _ in range(num_faces):
                face_vertexs: list[Vertex] = []
                for _ in range(3):  # 3 lines per Face object
                    parts = self._data[iterator].split()
                    if parts[0] != "v":
                        raise ValueError(f"expected line with 'v # # #', got: {parts}")
                    face_vertexs.append(Vertex(parts[1], parts[2], parts[3]))
                    iterator += 1
                if len(face_vertexs) != 3:
                    raise ValueError(f"Expected 3 vertex, got: {face_vertexs}")
                list_faces.append(Face3D(face_vertexs))
            # make mesh with color and add it
            new_mesh = Mesh3D(list_faces)
            new_mesh.set_color_variance(mesh_shader)
            list_mesh.append(new_mesh)

        return list_mesh

    def read_file(self, filepath: str) -> List[Mesh3D]:
        """read file data and make Mesh3D list

        Args:
            filepath (str): fiel path

        Returns:
            List[Mesh3D]: meshes from file
        """
        self.read_data(filepath)
        return self.make_list()

    def get_data(self) -> str:
        """returns data

        Returns:
            str: data getter
        """
        return self._data

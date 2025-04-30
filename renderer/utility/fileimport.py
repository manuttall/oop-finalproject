"""Singleton class to open and collect data from files."""

from __future__ import annotations
from typing import List
from geometry import Mesh3D, Face3D, Vertex, Shader

__author__ = "Arin Hartung"
__date__ = "2025/04/26"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"


class FileImport:
    """
    A Singleton class for importing 3D geometry from files.

    Raises:
        NameError: if a second instance is created.
    """

    _instance: FileImport | None = None

    def __new__(cls) -> FileImport:
        """Creates a new instance if one doesn't already exist.

        Enforces the Singleton pattern.

        Returns:
            FileImport: class instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Constructor. Enforces singleton."""
        self._data: List[str] = []

    def read_data(self, filepath: str) -> None:
        """
        Reads file data into internal storage, ignoring comment lines (#).

        Args:
            filepath (str): Path to the input file.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            self._data = [
                line.strip() for line in file
                if line.strip() and not line.strip().startswith("#")
            ]

    def make_list(self) -> List[Mesh3D]:
        """
        Creates a list of Mesh3D objects from parsed data.

        Raises:
            ValueError: If no data loaded or format errors exist.

        Returns:
            List[Mesh3D]: List of parsed meshes.
        """
        if not self._data:
            raise ValueError("No data loaded.")

        iterator = 0
        num_meshes = int(self._data[iterator])
        iterator += 1

        list_meshes: List[Mesh3D] = []

        for _ in range(num_meshes):
            # def the mesh
            mesh: Mesh3D = Mesh3D([])
            # Read RGB color
            color_parts = list(map(int, self._data[iterator].split()))
            if len(color_parts) != 3:
                raise ValueError(f"Expected 3 ints for RGB, got: {color_parts}")
            shader = Shader(*color_parts)
            iterator += 1

            # Read number of faces
            num_faces = int(self._data[iterator])
            iterator += 1

            for _ in range(num_faces):
                vertices: List[Vertex] = []
                for _ in range(3):
                    parts = self._data[iterator].split()
                    if parts[0] != "v":
                        raise ValueError(
                            f"Expected line starting with 'v', got: {parts}")
                    vertices.append(Vertex(
                        float(parts[1]), float(parts[2]), float(parts[3])
                    ))
                    iterator += 1

                if len(vertices) != 3:
                    raise ValueError(f"Expected 3 vertices, got: {len(vertices)}")

                mesh.add(Face3D(vertices))

            mesh.set_color(shader)
            list_meshes.append(mesh)

        return list_meshes

    def read_file(self, filepath: str) -> List[Mesh3D]:
        """
        Reads a file and creates a list of Mesh3D objects.

        Args:
            filepath (str): Path to the input file.

        Returns:
            List[Mesh3D]: List of parsed meshes.
        """
        self.read_data(filepath)
        return self.make_list()

    def get_data(self) -> List[str]:
        """
        Gets the raw loaded data lines.

        Returns:
            List[str]: Loaded file contents.
        """
        return self._data

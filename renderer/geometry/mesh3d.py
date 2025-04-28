"""Mesh3D class to represent a collection of 3D faces."""

from __future__ import annotations

__author__ = "Arin Hartung"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Arin Hartung"

from typing import List
import random
from geometry.face3d import Face3D
from geometry.shader import Shader


class Mesh3D:
    """Mesh3D class to store a list of faces with a base shader and variance."""

    def __init__(self, faces: List[Face3D]) -> None:
        """Constructor

        Args:
            faces (List[Face3D]): a list of faces in the mesh
        """
        self._faces: List[Face3D] = faces
        self._base_shader: Shader | None = None
        self._variance: int = 0

    @property
    def faces(self) -> List[Face3D]:
        """Property to get faces.

        Returns:
            List[Face3D]: faces
        """
        return self._faces

    @faces.setter
    def faces(self, value: List[Face3D]) -> None:
        """Property to set faces.

        Args:
            value (List[Face3D]): faces
        """
        self._faces = value

    @property
    def base_shader(self) -> Shader | None:
        """Property to get the base shader of the mesh.

        Returns:
            Shader | None: base shader
        """
        return self._base_shader

    @property
    def variance(self) -> int:
        """Property to get the color variance.

        Returns:
            int: variance
        """
        return self._variance

    def set_color(self, value: Shader) -> None:
        """Sets every face in the mesh to the shader.

        Args:
            value (Shader): the shader to set
        """
        for face in self._faces:
            face.color = value
        self._base_shader = value
        self._variance = 0

    def set_color_variance(self, value: Shader | None = None,
                           variance: int = 25) -> None:
        """Applies random color variance around a base Shader.

        Args:
            value (Shader, optional): Base color. If None, use the current base_shader.
            variance (int, optional): Variance range. Defaults to 25.

        Raises:
            ValueError: If the mesh has no faces and no base shader.
        """
        if value is None:
            if self._base_shader is not None:
                value = self._base_shader
            else:
                if not self._faces:
                    raise ValueError("Mesh has no faces.")
                value = self._faces[0].color

        self._base_shader = value
        self._variance = abs(variance)

        for face in self._faces:
            r = max(0,
                    min(value.r + random.randint(-self._variance, self._variance), 255))
            g = max(0,
                    min(value.g + random.randint(-self._variance, self._variance), 255))
            b = max(0,
                    min(value.b + random.randint(-self._variance, self._variance), 255))
            face.color = Shader(r, g, b)

    def add(self, new_face: Face3D) -> None:
        """Adds a Face3D to the mesh.

        Args:
            new_face (Face3D): the face to add
        """
        self._faces.append(new_face)

    def __str__(self) -> str:
        """String representation for testing.

        Returns:
            str: textual representation of face colors
        """
        facestr = ''
        for face in self._faces:
            facestr += (' ' + str(face.color.r) + ',' +
                        str(face.color.g) + ',' + str(face.color.b))
        return str(len(self._faces)) + ' +' + facestr

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
            faces (List[Face3D]): List of Face3D objects in the mesh.
        """
        self._faces: List[Face3D] = faces
        self._base_shader: Shader | None = None
        self._variance: int = 0

    @property
    def faces(self) -> List[Face3D]:
        """Gets the faces of the mesh.

        Returns:
            List[Face3D]: List of faces.
        """
        return self._faces

    @faces.setter
    def faces(self, value: List[Face3D]) -> None:
        """Sets the faces of the mesh.

        Args:
            value (List[Face3D]): New list of faces.
        """
        self._faces = value

    @property
    def base_shader(self) -> Shader | None:
        """Gets the base shader of the mesh.

        Returns:
            Shader | None: The base shader if set, else None.
        """
        return self._base_shader

    @property
    def variance(self) -> int:
        """Gets the color variance.

        Returns:
            int: Variance value.
        """
        return self._variance

    def set_color(self, value: Shader) -> None:
        """Sets all faces in the mesh to a uniform shader.

        Args:
            value (Shader): Shader color to apply to all faces.
        """
        for face in self._faces:
            face.color = value
        self._base_shader = value
        self._variance = 0

    def set_color_variance(self, value: Shader | None = None,
                           variance: int = 25) -> None:
        """Applies random color variance around a base Shader.

        Args:
            value (Shader | None, optional): Base shader to vary from.
                If None, uses the stored base_shader.
            variance (int, optional): Color variation range. Defaults to 25.

        Raises:
            ValueError: If no faces exist and no base shader is available.
        """
        if value is None:
            if self._base_shader is not None:
                value = self._base_shader
            elif self._faces:
                value = self._faces[0].color
            else:
                raise ValueError("Cannot set color variance without a base color.")

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
            new_face (Face3D): New face to add.
        """
        self._faces.append(new_face)

    def __str__(self) -> str:
        """Returns a simple string representation for testing.

        Returns:
            str: String showing number of faces and their RGB colors.
        """
        facestr = ' '.join(f"{face.color.r},{face.color.g},{face.color.b}"
                           for face in self._faces)
        return f"{len(self._faces)} faces: {facestr}"

    def __repr__(self) -> str:
        """Returns a detailed string representation for debugging.

        Returns:
            str: Detailed Mesh3D description.
        """
        return (f"Mesh3D(num_faces={len(self._faces)}, "
                f"base_shader={self._base_shader}, variance={self._variance})")

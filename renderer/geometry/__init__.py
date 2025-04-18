"""geometry package: Core data structures for 3D and 2D rendering.

This package provides foundational geometric classes used for 3D rendering,
scene representation, and 2D projection. It includes both primitive types
(points, vectors, vertices) and composite types (faces, meshes, shaders).

The following classes are re-exported for convenient access:

- Face2D: A triangle defined in 2D screen space
- Face3D: A triangle defined by 3D vertices
- Mesh3D: A collection of connected Face3D objects
- Point: A point in 2D Cartesian space
- Shader: A color representation used for rendering faces
- Vector: A 3D vector supporting arithmetic and geometric operations
- Vertex: A point in 3D space

Example:
    from geometry import Vertex, Vector, Face3D
"""

from .face2d import Face2D
from .face3d import Face3D
from .mesh3d import Mesh3D
from .point import Point
from .shader import Shader
from .vector import Vector
from .vertex import Vertex

__all__ = [
    "Face2D",
    "Face3D",
    "Mesh3D",
    "Point",
    "Shader",
    "Vector",
    "Vertex"
]

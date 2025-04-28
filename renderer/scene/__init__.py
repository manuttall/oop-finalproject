"""scene package: Core classes for scene management and 3D camera rendering.

This package provides the main components needed to build, manage,
and render 3D scenes, including camera control, screen output,
file imports, and scene organization.

The following classes are re-exported for convenient access:

- AspectRatio: Represents the screen's aspect ratio
- Camera: Defines the viewpoint and projection system in 3D space
- Scene: Holds a collection of Mesh3D objects and the active Camera
- Screen: Manages the Tkinter window and draws the 2D projections

Example:
    from scene import Camera, Scene, Screen
"""

from .aspect_ratio import AspectRatio
from .camera import Camera
from .scene import Scene
from .screen import Screen

__all__ = [
    "AspectRatio",
    "Camera",
    "Scene",
    "Screen"
]

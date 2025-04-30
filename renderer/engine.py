"""
Engine class to manage loading meshes, setting up scenes, and rendering 3D objects.
"""

from __future__ import annotations

__author__ = "Michael Nuttall"
__date__ = "2025/04/27"
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Michael Nuttall"

from typing import Any, List
from scene import Screen, Scene, AspectRatio, Camera
from geometry import Vertex, Shader, Face2D
from utility import Interface, FileImport


class Engine:
    """Engine manager class for the 3D rendering pipeline.

    Enforces the Singleton pattern.
    """

    _instance: Engine | None = None

    def __new__(cls) -> Engine:
        """Creates a new instance if one doesn't already exist.

        Returns:
            Engine: Singleton instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Constructor"""
        self._scene: Scene | None = None
        self._screen: Screen | None = None

    def load_scene(self, settings: dict[str, Any]) -> None:
        """Loads scene data and initializes the camera and screen
        based on user settings.

        Args:
            settings (dict[str, Any]): User input parameters
        """
        file_importer = FileImport()
        meshes = file_importer.read_file(settings["filepath"])

        for mesh in meshes:
            mesh.set_color_variance(mesh.base_shader, settings["variance"])

        camera = Camera(Vertex(*settings["camera_origin"]),
                        Vertex(*settings["look_at"]))

        self._scene = Scene(camera, meshes)
        self._screen = Screen(
            AspectRatio(*settings["aspect_ratio"]),
            settings["resolution"],
            Shader(30, 30, 30)  # Background color
        )

    def render_scene(self) -> None:
        """Renders the currently loaded scene."""
        if not self._scene or not self._screen:
            raise RuntimeError("Scene or screen not properly initialized.")

        faces: List[Face2D] = self._scene.make_render()
        self._screen.render(faces)
        self._screen.show()

    @staticmethod
    def main() -> None:
        """Main entry point to launch the interface and render the scene."""
        interface = Interface()
        settings = interface.run()

        engine = Engine()
        engine.load_scene(settings)
        engine.render_scene()


if __name__ == "__main__":
    Engine.main()

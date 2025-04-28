"""Screen class for rendering 2D projected faces on a Tkinter canvas."""

import tkinter as tk
from typing import List
from geometry import Point, Face2D, Shader
from scene.aspect_ratio import AspectRatio

__author__ = "Michael Nuttall"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"


class Screen:
    """A screen to render 2D triangles (Face2D) on a Tkinter canvas."""

    def __init__(self, aspect_ratio: AspectRatio, resolution: int, 
                 background: Shader = Shader(0, 0, 0)) -> None:
        """Constructor

        Args:
            aspect_ratio (AspectRatio): the aspect ratio of the canvas
            resolution (int): scaling factor for canvas size
            background (Shader, optional): background color as a Shader.
        """
        self._aspect_ratio = aspect_ratio
        self._resolution = resolution
        self._canvas_width = int(aspect_ratio.horizontal * resolution)
        self._canvas_height = int(aspect_ratio.vertical * resolution)
        self._background = background.hex

        self._window = None
        self._canvas = None

    def _create_canvas(self) -> None:
        """Creates the Tkinter window and canvas."""
        self._window = tk.Tk()
        self._window.title("3D Renderer")
        self._canvas = tk.Canvas(
            self._window,
            width=self._canvas_width,
            height=self._canvas_height,
            bg=self._background
        )
        self._canvas.pack()

    def _translate_point(self, point: Point) -> int:
        """Converts a normalized projected Point to canvas-space Point.

        Args:
            point (Point): projected point in camera space

        Returns:
            Point: pixel coordinates for canvas
        """
        x_canvas = int((point.x + self._aspect_ratio.horizontal / 2) * self._resolution)
        y_canvas = int((-point.y + self._aspect_ratio.vertical / 2) * self._resolution)
        return Point(x_canvas, y_canvas)

    def _draw_face(self, face: Face2D) -> None:
        """Draws a single Face2D triangle on the canvas.

        Args:
            face (Face2D): the face to draw
        """
        translated_points = [self._translate_point(p) for p in face.points]
        coords = [(p.x, p.y) for p in translated_points]
        self._canvas.create_polygon(
            coords,
            fill=face.color.hex,
        )

    def _draw_faces(self, faces: List[Face2D]) -> None:
        """Draws a sorted list of visible Face2D triangles from farthest to nearest.

        Args:
            faces (List[Face2D]): the 2D faces to draw
        """
        sorted_faces = sorted(faces, reverse=True)  # Draw farthest to nearest

        for face2d in sorted_faces:
            self._draw_face(face2d)

    def show(self) -> None:
        """Displays the window and starts the main event loop."""
        if self._window is None:
            self._create_canvas()
        self._window.mainloop()

    def render(self, faces: List[Face2D]) -> None:
        """Renders a list of Face2D objects by creating the canvas, drawing them,
          and showing the window.

        Args:
            faces (List[Face2D]): the 2D faces to render
        """
        self._create_canvas()
        self._draw_faces(faces)

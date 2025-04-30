"""Screen class for rendering 2D projected faces on a Tkinter canvas."""

from __future__ import annotations

__author__ = "Michael Nuttall"
__date__ = "2025/04/16"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Michael Nuttall"

import tkinter as tk
from typing import List, Optional
from geometry import Point, Face2D, Shader
from scene.aspect_ratio import AspectRatio


class Screen:
    """A screen to render 2D triangles (Face2D) on a Tkinter canvas."""

    def __init__(self, aspect_ratio: AspectRatio, resolution: int,
                 background: Shader = Shader(0, 0, 0)) -> None:
        """Constructor

        Args:
            aspect_ratio (AspectRatio): The aspect ratio of the canvas.
            resolution (int): Scaling factor for canvas size.
            background (Shader, optional): Background Shader color. Defaults to black.
        """
        self._aspect_ratio: AspectRatio = aspect_ratio
        self._resolution: int = resolution
        self._canvas_width: int = int(aspect_ratio.horizontal * resolution)
        self._canvas_height: int = int(aspect_ratio.vertical * resolution)
        self._background: str = background.hex

        self._window: Optional[tk.Tk] = None
        self._canvas: Optional[tk.Canvas] = None

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

    def _translate_point(self, point: Point) -> Point:
        """Converts a normalized projected Point to canvas-space Point.

        Args:
            point (Point): Projected point in camera space.

        Returns:
            Point: Pixel coordinates for the canvas.
        """
        x_canvas = int((point.x + self._aspect_ratio.horizontal / 2) * self._resolution)
        y_canvas = int((-point.y + self._aspect_ratio.vertical / 2) * self._resolution)
        return Point(x_canvas, y_canvas)

    def _draw_face(self, face: Face2D) -> None:
        """Draws a single Face2D triangle on the canvas.

        Args:
            face (Face2D): The face to draw.

        Raises:
            RuntimeError: If the canvas has not been created yet.
        """
        if self._canvas is None:
            raise RuntimeError("Canvas not initialized.")

        translated_points = [self._translate_point(p) for p in face.points]
        coords = [(p.x, p.y) for p in translated_points]

        self._canvas.create_polygon(
            coords,
            fill=face.color.hex,
            outline=""
        )

    def _draw_faces(self, faces: List[Face2D]) -> None:
        """Draws a sorted list of visible Face2D triangles from farthest to nearest.

        Args:
            faces (List[Face2D]): The 2D faces to draw.
        """
        sorted_faces = sorted(faces, reverse=True)  # Draw farthest faces first
        for face2d in sorted_faces:
            self._draw_face(face2d)

    def show(self) -> None:
        """Displays the window and starts the main event loop."""
        if self._window is None:
            self._create_canvas()
        if self._window is not None:
            self._window.mainloop()

    def render(self, faces: List[Face2D]) -> None:
        """Renders a list of Face2D objects by creating the canvas, drawing them,
        and showing the window.

        Args:
            faces (List[Face2D]): The 2D faces to render.
        """
        self._create_canvas()
        self._draw_faces(faces)

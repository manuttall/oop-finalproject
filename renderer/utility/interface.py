"""
Interface class to gather user input for launching the 3D Engine.
"""

from __future__ import annotations

__author__ = "Michael Nuttall"
__date__ = "2025/04/27"
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Michael Nuttall"

import tkinter as tk
from tkinter import messagebox
import os
from typing import Any


class Interface:
    """Interface to gather user input for configuring the 3D Engine."""

    def __init__(self) -> None:
        """Constructor."""
        self._root = tk.Tk()
        self._root.title("3D Engine - Load Scene")
        self._root.configure(bg="#f0f0f0")
        self._result: dict[str, Any] = {}
        self._setup_widgets()
        self._center_window(400, 580)

    def _on_enter(self, event: tk.Event[Any]) -> None:
        """Handles mouse hover event on the Render button.

        Changes the background color to a slightly darker blue.

        Args:
            event (tk.Event[Any]): Tkinter event triggered by mouse entering.
        """
        event.widget.config(bg="#1C86EE")

    def _on_leave(self, event: tk.Event[Any]) -> None:
        """Handles mouse leave event on the Render button.

        Restores the background color to its original bright blue.

        Args:
            event (tk.Event[Any]): Tkinter event triggered by mouse leaving.
        """
        event.widget.config(bg="#1E90FF")

    def _setup_widgets(self) -> None:
        """Sets up all entry fields, labels, and the render button."""
        padding: dict[str, Any] = {'padx': 10, 'pady': 5}

        tk.Label(self._root, text="Enter file path:",
                 bg="#f0f0f0").pack(**padding)
        self._entry_filepath = tk.Entry(self._root, width=50)
        self._add_placeholder(self._entry_filepath, "demo.obj")
        self._entry_filepath.pack(**padding)

        tk.Label(self._root, text="Camera origin (x y z):",
                 bg="#f0f0f0").pack(**padding)
        self._entry_cam_origin = tk.Entry(self._root, width=50)
        self._add_placeholder(self._entry_cam_origin, "-0.7 -1 1")
        self._entry_cam_origin.pack(**padding)

        tk.Label(self._root, text="Camera look-at (x y z):",
                 bg="#f0f0f0").pack(**padding)
        self._entry_look_at = tk.Entry(self._root, width=50)
        self._add_placeholder(self._entry_look_at, "0 0 0.65")
        self._entry_look_at.pack(**padding)

        tk.Label(self._root, text="Aspect ratio (horizontal vertical):",
                 bg="#f0f0f0").pack(**padding)
        self._entry_aspect = tk.Entry(self._root, width=20)
        self._add_placeholder(self._entry_aspect, "4 3")
        self._entry_aspect.pack(**padding)

        tk.Label(self._root, text="Resolution (pixels):",
                 bg="#f0f0f0").pack(**padding)
        self._entry_resolution = tk.Entry(self._root, width=20)
        self._add_placeholder(self._entry_resolution, "300")
        self._entry_resolution.pack(**padding)

        tk.Label(self._root, text="Background color (R G B):",
                 bg="#f0f0f0").pack(padx=10, pady=5)
        self._entry_bgcolor = tk.Entry(self._root, width=20)
        self._add_placeholder(self._entry_bgcolor, "30 30 30")
        self._entry_bgcolor.pack(padx=10, pady=5)

        tk.Label(self._root, text="Color variance:",
                 bg="#f0f0f0").pack(**padding)
        self._entry_variance = tk.Entry(self._root, width=20)
        self._add_placeholder(self._entry_variance, "10")
        self._entry_variance.pack(**padding)

        self._render_button = tk.Button(
            self._root, text="Render", command=self._collect_input,
            bg="#1E90FF", fg="black", activebackground="#1C86EE",
            activeforeground="black", font=("Helvetica", 12, "bold"),
            relief="raised", bd=2, padx=10, pady=5,
            highlightbackground="#1E90FF", highlightthickness=0
        )
        self._render_button.pack(pady=20)

        self._render_button.bind("<Enter>", self._on_enter)
        self._render_button.bind("<Leave>", self._on_leave)

    def _add_placeholder(self, entry: tk.Entry, text: str) -> None:
        """Adds placeholder text to an Entry field.

        Args:
            entry (tk.Entry): The entry widget to modify.
            text (str): The placeholder text to insert.
        """
        entry.insert(0, text)
        entry.config(fg="gray")

        def on_focus_in(_event: tk.Event[Any]) -> None:
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg="black")

        def on_focus_out(_event: tk.Event[Any]) -> None:
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def _center_window(self, width: int, height: int) -> None:
        """Centers the window on the user's screen.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.
        """
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self._root.geometry(f"{width}x{height}+{x}+{y}")

    def _show_error(self, message: str) -> None:
        """Displays an error popup message.

        Args:
            message (str): The error message to display.
        """
        messagebox.showerror("Input Error", message)

    def _resolve_filepath(self, path: str) -> str:
        """Validates and resolves the file path."""
        if not path or path == "demo.obj":
            path = "assets/demo.obj"
        elif not os.path.isabs(path) and not path.startswith("assets/"):
            path = os.path.join("assets", path)
        if not os.path.isfile(path):
            raise ValueError(f"File not found: {path}")
        return path

    def _parse_vector(self, text: str, length: int, label: str) -> tuple[float, ...]:
        """Parses a space-separated vector string."""
        parts = tuple(map(float, text.split()))
        if len(parts) != length:
            raise ValueError(f"{label} must have exactly {length} numbers.")
        return parts

    def _parse_color(self, text: str) -> tuple[int, int, int]:
        """Parses an RGB color input."""
        parts = tuple(map(int, text.split()))
        if len(parts) != 3 or any(not (0 <= c <= 255) for c in parts):
            raise ValueError("Background color must have "
                             "three integers between 0 and 255.")
        return parts

    def _parse_positive_int(self, text: str, label: str) -> int:
        """Parses a positive integer field."""
        value = int(text)
        if value <= 0:
            raise ValueError(f"{label} must be positive.")
        return value

    def _parse_non_negative_int(self, text: str, label: str) -> int:
        """Parses a non-negative integer field."""
        value = int(text)
        if value < 0:
            raise ValueError(f"{label} must be non-negative.")
        return value

    def _collect_input(self) -> None:
        """Collects input from user, validates it, and stores in _result."""
        try:
            filepath = self._resolve_filepath(self._entry_filepath.get())
            cam_origin = self._parse_vector(self._entry_cam_origin.get(),
                                            3, "Camera origin")
            look_at = self._parse_vector(self._entry_look_at.get(),
                                         3, "Camera look-at")
            aspect = self._parse_vector(self._entry_aspect.get(),
                                        2, "Aspect ratio")
            resolution = self._parse_positive_int(self._entry_resolution.get(),
                                                  "Resolution")
            variance = self._parse_non_negative_int(self._entry_variance.get(),
                                                    "Variance")

            bg_color = self._parse_color(self._entry_bgcolor.get())

            self._result = {
                "filepath": filepath,
                "camera_origin": cam_origin,
                "look_at": look_at,
                "aspect_ratio": aspect,
                "resolution": resolution,
                "variance": variance,
                "background_color": bg_color
            }
            self._root.destroy()

        except ValueError as e:
            self._result = {}
            self._show_error(str(e))

    def run(self) -> dict[str, Any]:
        """Runs the Tkinter interface and returns user input.

        Returns:
            dict[str, Any]: Dictionary of collected user inputs.
        """
        self._root.mainloop()
        return self._result

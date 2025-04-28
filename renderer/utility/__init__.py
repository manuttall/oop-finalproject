"""
Utility package for supporting modules used in the 3D rendering engine.

This package includes helper classes for input handling and file importing:

- FileImport: Singleton class to load and parse .obj-like mesh files
- Interface: Graphical interface to collect user input for scene configuration

Example:
    from utility import FileImport, Interface
"""

from .fileimport import FileImport
from .interface import Interface

__all__ = [
    "FileImport",
    "Interface"
]

"""
Terra 3D Viewer Modules

Python modules for processing and embedding 3D models in standalone HTML viewers.
"""

from .obj_parser import OBJParser
from .mtl_parser import MTLParser, Material
from .texture_processor import TextureProcessor, format_bytes
from .html_generator import HTMLGenerator

__version__ = "2.0.0"
__all__ = [
    "OBJParser",
    "MTLParser",
    "Material",
    "TextureProcessor",
    "HTMLGenerator",
    "format_bytes"
]

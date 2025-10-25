# Terra Model Viewer Generator - Processing Modules
"""
This package contains all file processing modules for the Terra Model Viewer Generator.

Modules:
    obj_parser: OBJ geometry file parser
    mtl_parser: MTL material library parser
    ply_parser: PLY format parser (binary and ASCII)
    texture_processor: Image optimization and base64 encoding
    geometry_optimizer: Polygon reduction and mesh optimization
    html_embedder: HTML generation and model embedding
"""

__all__ = [
    'obj_parser',
    'mtl_parser',
    'ply_parser',
    'texture_processor',
    'geometry_optimizer',
    'html_embedder'
]

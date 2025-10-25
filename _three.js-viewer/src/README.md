# Source Code Directory

This directory contains the Python source code for the Terra Model Viewer Generator.

## Structure

```
src/
├── model-viewer-generator.py    # Main GUI application (Phase 3.1)
├── modules/                      # Processing modules (Phase 3.2)
│   ├── __init__.py
│   ├── obj_parser.py            # OBJ file parser
│   ├── mtl_parser.py            # MTL material parser
│   ├── ply_parser.py            # PLY file parser
│   ├── texture_processor.py     # Image optimization and encoding
│   ├── geometry_optimizer.py    # Polygon reduction and optimization
│   └── html_embedder.py         # HTML generation and embedding
└── templates/                    # HTML viewer templates (Phase 2)
    ├── viewer-obj.html          # OBJ viewer template
    ├── viewer-ply.html          # PLY viewer template
    └── viewer-common.js         # Shared JavaScript code
```

## File Locations (Per Implementation Plan)

### Phase 2.1: Enhanced HTML Template
- **Location**: `src/templates/viewer-obj.html`
- **Location**: `src/templates/viewer-ply.html`
- **Location**: `src/templates/viewer-common.js`

### Phase 2.2: OBJ Format Support
- **Location**: `src/modules/obj_parser.py`
- **Location**: `src/modules/mtl_parser.py`

### Phase 2.3: PLY Format Support
- **Location**: `src/modules/ply_parser.py`

### Phase 3.1: Python GUI
- **Location**: `src/model-viewer-generator.py`

### Phase 3.2: File Processing Engine
- **Location**: `src/modules/texture_processor.py`
- **Location**: `src/modules/geometry_optimizer.py`
- **Location**: `src/modules/html_embedder.py`

## Development Notes

- All modules should have comprehensive docstrings
- Use type hints for better code clarity
- Each module should be independently testable
- Follow PEP 8 style guidelines

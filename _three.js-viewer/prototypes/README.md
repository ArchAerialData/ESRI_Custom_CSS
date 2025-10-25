# Prototypes Directory

This directory contains prototype HTML viewers and experimental code developed during Phase 1.

## Structure

```
prototypes/
└── phase1/                       # Phase 1 prototypes
    ├── prototype-obj-viewer.html    # OBJ test viewer (hardcoded model)
    ├── prototype-ply-viewer.html    # PLY test viewer (hardcoded model)
    └── test-models/                 # Small test models for prototyping
        ├── cube.obj
        ├── cube.mtl
        └── points.ply
```

## Phase 1.2: Prototype HTML Viewer

**Objective**: Create basic HTML templates that load 3D models using Three.js with hardcoded embedded data.

**File Locations**:
- `phase1/prototype-obj-viewer.html` - OBJ viewer prototype
- `phase1/prototype-ply-viewer.html` - PLY viewer prototype

**Success Criteria**:
- HTML file opens in browser without errors
- 3D model renders correctly
- Mouse controls work (rotate, zoom, pan)
- Model is fully embedded (no external file dependencies)

## Usage

Open any `.html` file directly in a web browser to view the prototype.

## Notes

- These are development prototypes, not production code
- Used for testing Three.js integration and embedding strategies
- Will be refined and moved to `src/templates/` in Phase 2

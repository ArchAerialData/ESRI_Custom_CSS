# Terra 3D Model Embedded Viewer Generator

## Overview

A desktop application that converts DJI Terra 3D mesh models (OBJ, PLY) into self-contained, portable HTML files that can be viewed on any computer without requiring the original model files or special software.

## Project Status

**Current Phase**: Phase 1 - Foundation & Research

See [Implementation Plan](.planning-to-do/embedded-viewer.md) for detailed roadmap.

## Quick Start

### For Users (Coming Soon)
1. Download `Terra Model Viewer Generator.exe` from [dist/](dist/)
2. Double-click to launch
3. Select your Terra 3D model files
4. Click "Generate Embedded Viewer"
5. Share the generated HTML file

### For Developers

**Requirements**:
- Python 3.x
- See [requirements.txt](requirements.txt) for dependencies

**Setup**:
```bash
cd _three.js-viewer
pip install -r requirements.txt
python src/model-viewer-generator.py
```

## Folder Structure

```
_three.js-viewer/
├── .planning-to-do/          # Project planning documents
│   └── embedded-viewer.md    # Detailed implementation plan
├── prototypes/               # Phase 1 prototypes and tests
│   └── phase1/              # HTML viewer prototypes
├── src/                      # Source code
│   ├── modules/             # Python processing modules
│   └── templates/           # HTML viewer templates
├── resources/               # Assets and dependencies
│   ├── icons/              # Application icons
│   └── three-js/           # Three.js library (for offline use)
├── tests/                   # Test files and sample models
│   └── sample_models/      # Test OBJ/PLY files
├── examples/                # Example generated HTML files
├── docs/                    # User and developer documentation
├── build/                   # PyInstaller build artifacts
├── dist/                    # Compiled executables
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## Features

### Current
- ✅ Detailed implementation plan
- ⏳ HTML viewer prototype (in development)

### Planned
- 🔲 OBJ format support (with textures)
- 🔲 PLY format support (binary/ASCII)
- 🔲 GUI application (tkinter)
- 🔲 Standalone Windows executable
- 🔲 Interactive 3D controls (rotate, zoom, pan)
- 🔲 Texture optimization
- 🔲 Geometry simplification
- 🔲 Progress tracking during generation

### Future Enhancements
- 🔲 Measurement tools
- 🔲 Annotation system
- 🔲 Gaussian Splat support
- 🔲 3D Tiles (B3DM) support

## Supported Formats

### Terra Export Formats (Input)
- ✅ **OBJ** - Wavefront Object (with MTL + textures)
- ✅ **PLY** - Polygon File Format (binary/ASCII)
- ⏳ **FBX** - Autodesk Filmbox (future)

### Output
- **HTML** - Self-contained HTML file with embedded 3D model
- Can be opened in any modern web browser
- No external dependencies required
- Fully portable and shareable

## File Size Recommendations

| Model Size | Embedded HTML | Performance |
|------------|---------------|-------------|
| < 5 MB | < 7 MB | Excellent |
| 5-20 MB | 7-27 MB | Good |
| 20-50 MB | 27-66 MB | Acceptable |
| 50-100 MB | 66-133 MB | Poor (slow) |
| 100+ MB | 133+ MB | Not Recommended |

**Recommended**: Keep original model under 20MB for best results.

## Documentation

- [Implementation Plan](.planning-to-do/embedded-viewer.md) - Detailed project roadmap
- [User Guide](docs/USER_GUIDE.md) - How to use the generator (coming soon)
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Code architecture (coming soon)
- [FAQ](docs/FAQ.md) - Common questions (coming soon)

## Contributing

This is an internal tool for Terra 3D model visualization. See the implementation plan for development phases and priorities.

## License

Internal use only.

## Changelog

### Phase 1 (In Progress)
- ✅ Created project structure
- ✅ Detailed implementation plan
- ⏳ HTML viewer prototype

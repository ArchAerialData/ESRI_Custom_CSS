# Terra 3D Viewer Generator

Generate standalone HTML viewers for 3D models with embedded data - no server required!

**Version**: 2.0.0
**Status**: Phase 2.2 Complete ✅
**Last Updated**: January 24, 2025

---

## Overview

A command-line tool (with future GUI) that converts Terra 3D mesh models (OBJ, PLY) into self-contained, portable HTML files. Share 3D models as a single .html file - works offline, no server needed!

## Project Status

**Current Phase**: Phase 2.2 - OBJ Format Support ✅ COMPLETE

See [Implementation Plan](.planning-to-do/embedded-viewer.md) for detailed roadmap.

## Quick Start

### Installation

```bash
# Clone or navigate to repository
cd _three.js-viewer

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Generate OBJ viewer from single file
python generate_obj_viewer.py model.obj -o viewer.html

# Generate from directory (auto-detects files)
python generate_obj_viewer.py model_folder/ -o viewer.html

# With texture optimization
python generate_obj_viewer.py model.obj -o viewer.html --max-texture-size 2048

# Open in browser
start viewer.html  # Windows
open viewer.html   # Mac
```

### GUI Application (Coming in Phase 3)
1. Download `Terra Model Viewer Generator.exe` from [dist/](dist/)
2. Double-click to launch
3. Select your Terra 3D model files
4. Click "Generate Embedded Viewer"
5. Share the generated HTML file

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

### ✅ Implemented (Phase 1-2)
- ✅ Production HTML viewer templates (OBJ, PLY)
- ✅ ES module architecture with modern Three.js
- ✅ OBJ format support with multi-file merging
- ✅ MTL material library parsing
- ✅ Texture embedding (Base64 data URIs)
- ✅ Texture optimization (downscaling, WebP conversion)
- ✅ Interactive 3D controls (rotate, zoom, pan, wireframe)
- ✅ Lighting presets (realistic, bright, dramatic, flat)
- ✅ Screenshot export
- ✅ Fullscreen mode
- ✅ Responsive design (desktop → mobile)
- ✅ Command-line tool with progress tracking
- ✅ Cross-browser compatibility (Chrome, Firefox, Edge, Safari 16.4+)

### ⏳ In Progress (Phase 2.3)
- ⏳ PLY format support (binary/ASCII)

### 🔲 Planned (Phase 3+)
- 🔲 GUI application (tkinter)
- 🔲 Standalone Windows executable (.exe)
- 🔲 Drag-and-drop file support
- 🔲 Batch processing
- 🔲 Settings management

### 🌟 Future Enhancements
- 🌟 Measurement tools
- 🌟 Annotation system
- 🌟 Gaussian Splat support
- 🌟 3D Tiles (B3DM) support

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

### Version 2.0.0 - January 24, 2025

**Phase 2.2 Complete** - OBJ Format Support ✅
- ✅ Created Python processing modules (obj_parser, mtl_parser, texture_processor, html_generator)
- ✅ Implemented multi-file OBJ merging with vertex index offsetting
- ✅ Added texture optimization (downscaling, WebP conversion, quality control)
- ✅ Built command-line tool with comprehensive options
- ✅ Updated requirements.txt (Pillow 11.0.0+, PyInstaller 6.11.0+)
- ✅ Documented Phase 2.2 completion in planning files

**Phase 2.1 Complete** - January 24, 2025
- ✅ Created production HTML templates (viewer-obj.html, viewer-ply.html)
- ✅ Implemented viewer-common.js with reusable classes
- ✅ Added advanced UI controls (screenshot, presets, fullscreen)
- ✅ Implemented lighting presets (5 options)
- ✅ Added progress bar loading screen
- ✅ Created responsive design (mobile/tablet support)
- ✅ Documented templates in src/templates/README.md

**Phase 1.2 Complete** - January 24, 2025
- ✅ Fixed prototype viewers (ES module migration)
- ✅ Migrated from deprecated Three.js CDN paths to modern /examples/jsm/
- ✅ Tested and validated prototypes in Chrome
- ✅ Updated PROTOTYPE_RESULTS.md with test results

**Phase 1.1 Complete**
- ✅ Created project structure
- ✅ Detailed implementation plan
- ✅ HTML viewer prototypes (OBJ, PLY)

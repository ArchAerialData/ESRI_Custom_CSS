# Terra Model Viewer Generator - Project Structure

## Complete Folder Structure

```
_three.js-viewer/
│
├── .planning-to-do/                 # 📋 Project Planning
│   └── embedded-viewer.md           # Detailed implementation plan with file locations
│
├── prototypes/                      # 🧪 Phase 1 Prototypes
│   ├── phase1/                      # Phase 1 HTML prototypes
│   │   ├── prototype-obj-viewer.html
│   │   ├── prototype-ply-viewer.html
│   │   └── test-models/            # Small test models
│   └── README.md
│
├── src/                             # 💻 Source Code
│   ├── model-viewer-generator.py    # Main GUI application (Phase 3.1)
│   │
│   ├── modules/                     # Python processing modules (Phase 3.2)
│   │   ├── __init__.py
│   │   ├── obj_parser.py           # OBJ geometry parser (Phase 2.2)
│   │   ├── mtl_parser.py           # MTL material parser (Phase 2.2)
│   │   ├── ply_parser.py           # PLY format parser (Phase 2.3)
│   │   ├── texture_processor.py    # Image optimization (Phase 3.2)
│   │   ├── geometry_optimizer.py   # Mesh simplification (Phase 3.2)
│   │   └── html_embedder.py        # HTML generation (Phase 3.2)
│   │
│   ├── templates/                   # HTML viewer templates (Phase 2.1)
│   │   ├── viewer-obj.html         # OBJ viewer template
│   │   ├── viewer-ply.html         # PLY viewer template
│   │   └── viewer-common.js        # Shared JavaScript
│   │
│   └── README.md
│
├── resources/                       # 🎨 Assets & Dependencies
│   ├── icons/                      # Application icons
│   │   ├── app-icon.ico           # Windows .exe icon
│   │   └── app-icon.png           # PNG version
│   │
│   ├── three-js/                   # Three.js library (offline use)
│   │   ├── three.min.js           # Three.js core
│   │   ├── OBJLoader.js           # OBJ loader
│   │   ├── MTLLoader.js           # MTL loader
│   │   ├── PLYLoader.js           # PLY loader
│   │   └── OrbitControls.js       # Mouse controls
│   │
│   └── README.md
│
├── tests/                          # 🧪 Testing & QA
│   ├── sample_models/              # Test 3D models (Phase 5.1)
│   │   ├── small-obj/             # < 5MB OBJ
│   │   ├── large-obj/             # 50+ MB OBJ
│   │   ├── multi-file-obj/        # Split OBJ models
│   │   ├── ply-binary/            # Binary PLY
│   │   └── ply-ascii/             # ASCII PLY
│   │
│   ├── test_obj_parser.py          # OBJ parser tests
│   ├── test_ply_parser.py          # PLY parser tests
│   ├── test_texture_processor.py   # Texture tests
│   ├── test_html_embedder.py       # HTML generation tests
│   ├── qa-results.md               # QA test results
│   └── README.md
│
├── examples/                        # 📁 Example Output
│   ├── example-obj-viewer.html      # Sample OBJ viewer
│   ├── example-ply-viewer.html      # Sample PLY viewer
│   ├── screenshots/                 # Screenshots
│   │   ├── obj-viewer.png
│   │   └── ply-viewer.png
│   └── README.md
│
├── docs/                            # 📚 Documentation (Phase 5.2)
│   ├── USER_GUIDE.md                # End-user guide
│   ├── DISTRIBUTION_README.md       # Distribution instructions
│   ├── DEVELOPER_GUIDE.md           # Developer documentation
│   ├── FAQ.md                       # Frequently asked questions
│   └── README.md
│
├── build/                           # 🔧 PyInstaller Build Artifacts
│   └── (temporary files)            # Generated during .exe build
│
├── dist/                            # 📦 Distribution
│   └── Terra Model Viewer Generator.exe  # Standalone executable (Phase 3.3)
│
├── .gitignore                       # Git ignore rules
├── README.md                        # Main project README
├── CONTRIBUTING.md                  # Development guide
├── PROJECT_STRUCTURE.md             # This file
└── requirements.txt                 # Python dependencies
```

## File Placement by Phase

### Phase 1: Foundation & Research
- ✅ `.planning-to-do/embedded-viewer.md` - Implementation plan
- ⏳ `prototypes/phase1/prototype-obj-viewer.html` - OBJ prototype
- ⏳ `prototypes/phase1/prototype-ply-viewer.html` - PLY prototype

### Phase 2: Core Viewer Development
- ⏳ `src/templates/viewer-obj.html` - Production OBJ template
- ⏳ `src/templates/viewer-ply.html` - Production PLY template
- ⏳ `src/templates/viewer-common.js` - Shared viewer logic
- ⏳ `src/modules/obj_parser.py` - OBJ parser
- ⏳ `src/modules/mtl_parser.py` - MTL parser
- ⏳ `src/modules/ply_parser.py` - PLY parser

### Phase 3: GUI Application
- ⏳ `src/model-viewer-generator.py` - Main GUI app
- ⏳ `src/modules/texture_processor.py` - Texture optimization
- ⏳ `src/modules/geometry_optimizer.py` - Geometry optimization
- ⏳ `src/modules/html_embedder.py` - HTML generation
- ⏳ `dist/Terra Model Viewer Generator.exe` - Compiled executable
- ⏳ `build-exe.bat` - Build automation script

### Phase 4: Advanced Features (Future)
- 🔲 Measurement tools integration
- 🔲 Annotation system
- 🔲 Gaussian Splat viewer
- 🔲 3D Tiles support

### Phase 5: Testing & Documentation
- ⏳ `tests/test_*.py` - Unit tests
- ⏳ `tests/sample_models/` - Test data
- ⏳ `tests/qa-results.md` - QA results
- ⏳ `docs/USER_GUIDE.md` - User documentation
- ⏳ `docs/DISTRIBUTION_README.md` - Distribution guide
- ⏳ `docs/DEVELOPER_GUIDE.md` - Developer guide
- ⏳ `docs/FAQ.md` - FAQ

## Key Principles

### ✅ Platform Independence
All code is designed to run on any system:
- **Python**: Cross-platform (Windows, Mac, Linux)
- **HTML Viewers**: Browser-based (any OS with web browser)
- **Standalone .exe**: Windows-only, but HTML output works everywhere

### ✅ Self-Contained Output
Generated HTML files contain:
- Three.js library (can be embedded or CDN)
- 3D model data (Base64 encoded)
- All textures (Base64 encoded)
- Viewer controls and UI
- No external dependencies

### ✅ Portable Distribution
- **Development**: Python scripts in `src/`
- **Distribution**: Single `.exe` file from `dist/`
- **Output**: Self-contained `.html` files

## Usage Notes

### For Developers
1. Work in `src/` and `prototypes/` during development
2. Follow phase order from implementation plan
3. Place all files according to folder structure above
4. Update tests in `tests/` as you develop

### For End Users
1. Download `.exe` from `dist/`
2. Run on any Windows PC (no installation)
3. Generate `.html` viewers
4. Share `.html` files - work on any OS with a browser

### For AI Agents
All file locations are explicitly defined in:
- This document (PROJECT_STRUCTURE.md)
- Implementation plan (.planning-to-do/embedded-viewer.md)
- Individual README.md files in each folder

Follow the file paths exactly as specified to maintain organization.

## Current Status

**Legend**:
- ✅ Complete
- ⏳ In Progress / Planned
- 🔲 Future Enhancement

**Project Phase**: Phase 1 (Foundation & Research)

**Completed**:
- ✅ Folder structure created
- ✅ README files for all major directories
- ✅ Implementation plan with file locations
- ✅ Requirements.txt and .gitignore
- ✅ Module structure defined

**Next Steps**:
- ⏳ Phase 1.2: Create prototype HTML viewers
- ⏳ Test with sample 3D models
- ⏳ Validate Three.js embedding approach

## Cross-Platform Compatibility

### Development Environment
- **Windows**: Full support (primary platform)
- **Mac/Linux**: Python code will work, .exe build requires Wine/Windows VM

### Generated HTML Viewers
- **Windows**: ✅ All browsers
- **Mac**: ✅ All browsers
- **Linux**: ✅ All browsers
- **Mobile**: ✅ iOS Safari, Android Chrome (with touch controls)

### Distribution
- **Generator App**: Windows .exe (requires Windows to run generator)
- **HTML Output**: Universal (works on any OS with modern browser)

This ensures the end product (HTML viewers) can run on ANY system, even though the generator itself is Windows-based.

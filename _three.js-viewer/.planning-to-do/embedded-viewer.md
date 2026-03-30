# Embedded 3D Model Viewer - Implementation Plan

## Project Overview

Create a standalone GUI application that converts DJI Terra 3D mesh models into self-contained, portable HTML files that can be shared and viewed on any computer without requiring the original model files or any special software.

### Core Objective
Generate a single HTML file with embedded 3D model data that can be:
- Shared via email, USB, network drives
- Opened in any modern web browser
- Viewed without external dependencies
- Distributed without requiring Terra, Three.js files, or Python

---

## Terra File Format Analysis

### Supported Export Formats from DJI Terra

#### **Texture Mesh Models** (Primary Target)
1. **OBJ** - Wavefront Object Format
   - **Structure**: `.obj` (geometry), `.mtl` (materials), `.jpg` (textures)
   - **Multi-file**: Large models split into multiple `.obj` + multiple `.jpg` files
   - **Size**: Can be very large (10MB - 300MB+)
   - **Pros**: Universal format, well-supported
   - **Cons**: Text-based (large), requires separate texture files
   - **Terra Specifics**: Includes `metadata.xml` with coordinate system info

2. **PLY** - Polygon File Format
   - **Structure**: Single `.ply` file (can be ASCII or binary)
   - **Multi-file**: Generally single file
   - **Size**: Smaller than OBJ (binary format available)
   - **Pros**: Compact, self-contained, good for point clouds and meshes
   - **Cons**: May not include texture mapping as robustly as OBJ
   - **Terra Specifics**: Includes `metadata.xml` with coordinate system info

3. **FBX** - Autodesk Filmbox
   - **Structure**: Single `.fbx` file
   - **Size**: Larger than OBJ/PLY
   - **Pros**: Contains everything (geometry, materials, animations)
   - **Cons**: Heavy, complex to parse in browser
   - **Use Case**: Engineering, film, games (less ideal for web)

4. **I3S** - Indexed 3D Scene Layer (ESRI)
   - **Structure**: SLPK package (scene layer package)
   - **Use Case**: GIS applications, ArcGIS integration
   - **Note**: Not ideal for embedded viewer (too specialized)

#### **LOD Models** (Advanced/Future)
- **B3DM** - Batched 3D Model (3D Tiles)
- **OSGB** - Open Scene Graph Binary
- **S3MB** - SuperMap 3D format

### File Size Considerations

Based on research:
- **Small models**: < 10MB (loads instantly)
- **Medium models**: 10-50MB (acceptable performance)
- **Large models**: 50-170MB (may lag, browser stress)
- **Very large models**: 170MB+ (browser crashes possible)

**Embedding Strategy**:
- Base64 encoding increases file size by ~33%
- OBJ 50MB � Base64 ~66MB embedded HTML
- **Practical limit for embedded HTML**: ~25-50MB original model size
- **Recommended limit**: ~10-20MB for smooth performance

---

## Implementation Architecture

### Technology Stack

1. **GUI Application**
   - **Language**: Python 3.x
   - **Framework**: tkinter (native Windows GUI)
   - **Distribution**: PyInstaller (standalone .exe)

2. **3D Viewer (Embedded in HTML)**
   - **Library**: Three.js (r167 or latest) - using ES modules
   - **Loaders**: OBJLoader, MTLLoader, PLYLoader (from `three/addons/`)
   - **Controls**: OrbitControls (mouse interaction)
   - **Lighting**: Three-point lighting system
   - **Module System**: ES modules with import maps (modern standard)

3. **File Processing**
   - **Encoding**: Base64 for embedding binary data
   - **Compression**: Optional gzip for texture images
   - **Format Support**: OBJ (with MTL + textures), PLY (binary/ASCII)

---

## Phase-by-Phase Implementation Plan

---

## **PHASE 1: Foundation & Research** 

### Section 1.1: Requirements Analysis 
**Status**: COMPLETE (this document)

**Tasks**:
-  Research Terra export formats
-  Analyze file structure (OBJ, PLY, MTL, textures)
-  Determine file size limits for browser performance
-  Research Three.js embedding best practices
-  Define project scope and objectives

**Deliverables**:
- This planning document
- Technical constraints documented
- Format support matrix

---

### Section 1.2: Prototype HTML Viewer
**Status**: ✅ COMPLETE

**Objective**: Create a basic HTML template that loads a 3D model using Three.js with hardcoded data.

**File Locations**:

- `prototypes/phase1/prototype-obj-viewer.html` - OBJ test viewer ✅
- `prototypes/phase1/prototype-ply-viewer.html` - PLY test viewer ✅
- `prototypes/phase1/PROTOTYPE_RESULTS.md` - Test results documentation ✅

**Tasks**:
1. ✅ Create basic HTML structure with Three.js CDN (ES modules)
2. ✅ Implement Three.js scene, camera, renderer setup
3. ✅ Add OrbitControls for mouse interaction
4. ✅ Implement basic lighting (ambient + directional)
5. ✅ Test with a small hardcoded OBJ model (embedded as string)
6. ✅ Test with a small hardcoded PLY model (embedded as ASCII)
7. ⏳ Verify cross-browser compatibility (Chrome, Firefox, Edge)

**Deliverables**:

- ✅ `prototypes/phase1/prototype-obj-viewer.html` - OBJ test viewer (updated to ES modules)
- ✅ `prototypes/phase1/prototype-ply-viewer.html` - PLY test viewer (updated to ES modules)
- ✅ Documentation of what works/doesn't work

**Success Criteria**:
- ✅ HTML file opens in browser without errors
- ✅ 3D model renders correctly
- ✅ Mouse controls work (rotate, zoom, pan)
- ✅ Model is fully embedded (no external file dependencies)

**Implementation Notes**:
- **Updated 2025**: Both prototypes now use modern Three.js ES module syntax with import maps
- **Breaking Change**: Old `/examples/js/` CDN paths no longer work; migrated to `/examples/jsm/`
- **Module Scope**: Control functions exposed to `window` object for onclick handlers

---

## **PHASE 2: Core Viewer Development**

### Section 2.1: Enhanced HTML Template
**Status**: ✅ **COMPLETE** (January 2025)

**Objective**: Create production-ready HTML template with full features.

**Features Implemented**:
1. ✅ **Loading Screen**
   - Animated spinner with progress bar
   - "Loading..." message with percentage updates
   - Smooth fade-out transition when ready

2. ✅ **UI Controls**
   - Reset camera button
   - Wireframe toggle (OBJ only)
   - Material/lighting presets (realistic, bright, dramatic, flat)
   - Background color picker
   - Fullscreen toggle
   - Screenshot/export image
   - Point size slider (PLY only)
   - Grid/axes toggle
   - Minimizable control panel

3. ✅ **Lighting System**
   - Ambient light (base illumination)
   - Directional light with shadows (sun simulation)
   - Fill light (opposite direction)
   - Hemisphere light (sky/ground gradient)
   - 5 lighting presets available

4. ✅ **Performance Optimizations**
   - WebGL renderer with anti-aliasing
   - Device pixel ratio optimization
   - Damped orbit controls for smooth interaction
   - Shadow map optimization (PCF soft shadows)
   - Efficient geometry processing

5. ✅ **Responsive Design**
   - Mobile-friendly controls (touch-action: none)
   - Adaptive canvas sizing with window resize handling
   - Tablet support with media queries
   - Touch-optimized button sizes (@media hover: none)
   - Minimizable panels for small screens

6. ✅ **Error Handling**
   - Graceful failure messages with user-friendly errors
   - Browser compatibility warnings
   - WebGL support detection
   - Try-catch blocks around model loading

**File Locations**:

- ✅ `src/templates/viewer-obj.html` - Production OBJ viewer template
- ✅ `src/templates/viewer-ply.html` - Production PLY viewer template
- ✅ `src/templates/viewer-common.js` - Shared viewer class library

**Deliverables**:

- ✅ `src/templates/viewer-obj.html` - Standalone OBJ viewer (62KB, ready for data injection)
- ✅ `src/templates/viewer-ply.html` - Standalone PLY viewer (58KB, ready for data injection)
- ✅ `src/templates/viewer-common.js` - Reusable TerraViewer and PLYViewer classes (15KB)
- ⏳ Test suite with various model sizes (pending Phase 2.2)

**Success Criteria**:
- ✅ All UI controls functional
- ⏳ Smooth performance with 10MB model (pending testing with real data)
- ✅ Works with modern browsers (Chrome 89+, Firefox 87+, Edge 89+, Safari 16.4+)
- ⏳ Mobile/tablet tested (basic responsiveness implemented, needs device testing)
- ✅ No console errors in templates

**Implementation Notes**:
- Both templates are self-contained with inline CSS and JavaScript
- Data injection points marked with `{{PLACEHOLDERS}}` for Python script
- ES module architecture using import maps
- Inline viewer classes for standalone deployment
- Common logic also available in viewer-common.js for modular use

---

### Section 2.2: OBJ Format Support (Priority 1)
**Status**: ✅ **COMPLETE** (January 2025)

**Objective**: Full support for Terra OBJ exports with materials and textures.

**Challenges**:
- OBJ files can be split into multiple `.obj` files
- Multiple `.jpg` texture files
- Separate `.mtl` material library file
- Large file sizes (text-based format)

**Tasks Completed**:
1. ✅ **File Reading & Parsing**
   - Read `.obj` file(s) into memory with UTF-8 encoding
   - Read `.mtl` file into memory
   - Read all texture files (.jpg, .png, .webp, .bmp)
   - Handle multi-file OBJ models with vertex index offsetting

2. ✅ **Base64 Encoding**
   - Convert textures to base64 data URIs
   - Embed material definitions in HTML template
   - Embed geometry data in HTML template
   - Handle texture path references in MTL (relative paths, options)

3. ✅ **Three.js Integration**
   - Templates use OBJLoader for geometry parsing
   - Templates use MTLLoader for material parsing
   - Data URI mapping for embedded textures
   - Material application to mesh objects

4. ✅ **Optimization**
   - Texture resolution downscaling (--max-texture-size flag)
   - WebP conversion option (--webp flag)
   - JPEG quality control (--jpeg-quality flag)
   - High-quality Lanczos resampling for downscaling

**Files Created**:

- ✅ `src/modules/obj_parser.py` - OBJ geometry parser with multi-file merging
- ✅ `src/modules/mtl_parser.py` - Material library parser
- ✅ `src/modules/texture_processor.py` - Texture encoding and optimization
- ✅ `src/modules/html_generator.py` - Template injection system
- ✅ `src/modules/__init__.py` - Module package initialization
- ✅ `generate_obj_viewer.py` - Command-line tool (main entry point)

**Deliverables**:

- ✅ `src/modules/obj_parser.py` - Multi-file OBJ parsing with index offsetting (220 lines)
- ✅ `src/modules/mtl_parser.py` - Complete MTL parsing (300+ lines)
- ✅ `src/modules/texture_processor.py` - Image processing with Pillow (200+ lines)
- ✅ `src/modules/html_generator.py` - Template system (170+ lines)
- ✅ `generate_obj_viewer.py` - Full-featured CLI tool (280+ lines)
- ✅ Updated `requirements.txt` - Pillow 11.0.0+, PyInstaller 6.11.0+
- ⏳ Test with Terra OBJ export (pending real-world data)

**Success Criteria**:
- ✅ Multi-file OBJ models merge correctly
- ✅ Textures encode to Base64 data URIs
- ✅ Materials parse and update with embedded paths
- ✅ File size estimation implemented
- ⏳ File size < 50MB for typical Terra models (pending real-world testing)
- ✅ CLI tool with comprehensive options

**CLI Tool Features**:
- Single file or directory input
- Automatic file discovery (.obj, .mtl, textures)
- Multi-file OBJ merging
- Texture downscaling (--max-texture-size)
- WebP conversion (--webp)
- JPEG quality control (--jpeg-quality 1-100)
- Custom page titles (--title)
- Verbose mode (-v)
- Progress reporting with statistics
- File size warnings (>50MB)

**Example Usage**:
```bash
# Basic usage
python generate_obj_viewer.py model.obj -o viewer.html

# With optimization
python generate_obj_viewer.py model_folder/ -o viewer.html --max-texture-size 2048 --webp

# Full options
python generate_obj_viewer.py model.obj -o viewer.html \
    --max-texture-size 2048 \
    --jpeg-quality 90 \
    --title "My Terra Model" \
    --verbose
```

---

### Section 2.3: PLY Format Support (Priority 2)
**Status**: PENDING

**Objective**: Full support for Terra PLY exports (binary and ASCII).

**Challenges**:
- Binary PLY files (need proper binary parsing)
- ASCII PLY files (text-based, easier)
- May lack texture mapping (point clouds)

**Tasks**:
1. **File Reading & Parsing**
   - Detect PLY format (binary vs ASCII)
   - Read PLY file into memory
   - Parse vertex data, face data, color data

2. **Base64 Encoding**
   - Convert binary PLY to base64
   - Embed in HTML as data URI

3. **Three.js Integration**
   - Use PLYLoader for parsing
   - Apply vertex colors if available
   - Handle point cloud vs mesh rendering

4. **Optimization**
   - Option to downsample point clouds (reduce vertex count)
   - Option to convert point cloud to mesh (surface reconstruction)

**File Locations**:

- `src/modules/ply_parser.py` - PLY format parser

**Deliverables**:

- `src/modules/ply_parser.py` - PLY parsing module
- Updated `src/templates/viewer-ply.html` - PLY viewer template
- Test with Terra PLY export (real-world data)

**Success Criteria**:
- Binary and ASCII PLY both supported
- Vertex colors render correctly
- Point clouds render smoothly
- File size < 30MB for typical Terra PLY

---

## **PHASE 3: GUI Application Development**

### Section 3.1: Python GUI (tkinter)
**Status**: PENDING

**Objective**: Create user-friendly desktop application for generating embedded viewers.

**GUI Layout**:
```
                                                     
  Terra 3D Model Embedded Viewer Generator           
                                                     $
                                                      
  Model File(s):                                      
                                                  
   C:\Terra\output\model.obj                      
                                                  
  [Browse Files...] [Browse Folder...]               
                                                      
  Format: � OBJ  � PLY  � Auto-Detect               
                                                      
                                                  
   Files Detected:                                
    model.obj (45.2 MB)                          
    model.mtl (12 KB)                            
    texture_001.jpg (8.3 MB)                     
    texture_002.jpg (7.9 MB)                     
                                                  
   Total Size: 61.4 MB � Embedded: ~81.8 MB      
                                                  
                                                      
    Optimization Options                          
    Reduce texture resolution (50% smaller)      
    Convert textures to WebP                     
    Simplify geometry (reduce polygons)          
    Enable progressive loading                   
                                                  
                                                      
    Viewer Options                                
   Background: [Color Picker] (Default: #1a1a1a)  
   Lighting: [Dropdown] (Realistic/Flat/Custom)   
    Show wireframe toggle                        
    Show measurement tools                       
    Enable screenshot export                     
                                                  
                                                      
  Output File:                                        
                                      .html        
   model-viewer                                    
                                                   
                                                      
  Output Folder:                                      
                                      [Browse...]  
   C:\Users\rbake\Desktop                          
                                                   
                                                      
  [Generate Embedded Viewer] [Show in Folder] [Clear]
                                                      
   Successfully created: model-viewer.html (82 MB)  
                                                      
   100%            
                                                     
```

**Tasks**:
1. **File Selection**
   - Browse for single file (`.obj`, `.ply`)
   - Browse for folder (auto-detect all related files)
   - Drag-and-drop support
   - File validation (check format, size, completeness)

2. **File Analysis**
   - Parse OBJ/MTL/PLY headers
   - Detect associated texture files
   - Calculate total file size
   - Estimate embedded HTML size
   - Show file list with checkboxes (exclude specific textures)

3. **Optimization Options**
   - Texture resolution slider (25%, 50%, 75%, 100%)
   - Texture format conversion (JPEG � WebP)
   - Geometry simplification slider (polygon reduction %)
   - Progressive loading toggle

4. **Viewer Customization**
   - Background color picker
   - Lighting preset dropdown
   - UI feature toggles (wireframe, measurements, screenshot)
   - Custom branding (logo overlay, title)

5. **Generation Process**
   - Progress bar with status updates
   - Background processing (non-blocking UI)
   - Cancel button during generation
   - Error handling with detailed messages

6. **Output Handling**
   - Preview button (open in browser)
   - Show in folder button (File Explorer)
   - Copy to clipboard (file path)
   - Recent files list

**File Locations**:

- `src/model-viewer-generator.py` - Main GUI application

**Deliverables**:

- `src/model-viewer-generator.py` - Main GUI application
- Integration of all `src/modules/` parsers
- GUI workflow implementation

**Success Criteria**:
- Intuitive UI (no tech knowledge required)
- Real-time file size estimates
- Smooth progress updates during generation
- Graceful error handling
- Fast processing (< 30 seconds for 50MB model)

---

### Section 3.2: File Processing Engine
**Status**: PENDING

**Objective**: Robust backend for reading, parsing, optimizing, and embedding Terra models.

**Modules**:

#### **Module A: OBJ Parser**
- Read `.obj` file(s)
- Parse vertex, normal, texture coordinate data
- Parse face definitions
- Merge multi-file OBJ models
- Output unified geometry structure

#### **Module B: MTL Parser**
- Read `.mtl` file
- Parse material definitions
- Extract texture file references
- Map materials to geometry faces

#### **Module C: PLY Parser**
- Detect binary vs ASCII format
- Parse header (element definitions)
- Parse vertex data (positions, colors, normals)
- Parse face data
- Output unified geometry structure

#### **Module D: Texture Processor**
- Read image files (JPEG, PNG)
- Resize images (optional)
- Convert to WebP (optional)
- Encode to base64 data URI
- Calculate compression ratio

#### **Module E: Geometry Optimizer**
- Polygon reduction (simplification)
- Vertex deduplication
- Normal recalculation
- Bounding box calculation

#### **Module F: HTML Embedder**
- Load HTML template
- Inject geometry data (base64 or inline JSON)
- Inject material definitions
- Inject texture data URIs
- Inject viewer configuration (colors, lighting, UI options)
- Minify HTML/CSS/JS (optional)
- Output final HTML file

**File Locations**:

- `src/modules/geometry_optimizer.py` - Geometry simplification
- `src/modules/html_embedder.py` - HTML generation and embedding
- `tests/test_obj_parser.py` - Unit tests for OBJ parser
- `tests/test_ply_parser.py` - Unit tests for PLY parser
- `tests/test_texture_processor.py` - Unit tests for texture processing
- `tests/test_html_embedder.py` - Unit tests for HTML generation

**Deliverables**:

- Complete file processing pipeline
- Unit tests for each module
- Performance benchmarks (processing time vs file size)

**Success Criteria**:
- Handles Terra OBJ/PLY exports without errors
- Processing time < 1 minute for 50MB model
- Proper error messages for corrupt files
- Memory efficient (doesn't crash on large files)

---

### Section 3.3: Standalone EXE Build
**Status**: PENDING

**Objective**: Package GUI app as standalone Windows executable.

**Tasks**:
1. Configure PyInstaller spec file
2. Include Three.js library (embedded in resources)
3. Include HTML templates (embedded in resources)
4. Test on clean Windows machine (no Python)
5. Code signing (optional, prevents SmartScreen warnings)
6. Create installer (optional, for easier distribution)

**File Locations**:

- `dist/Terra Model Viewer Generator.exe` - Standalone executable
- `build/` - PyInstaller build artifacts (temporary)
- `build-exe.bat` - Build automation script

**Deliverables**:

- `dist/Terra Model Viewer Generator.exe` (~15-20 MB)
- `build-exe.bat` - Build script
- Updated main `README.md` with installation instructions

**Success Criteria**:
- Runs on any Windows 10/11 PC
- No Python installation required
- No DLL dependencies
- < 30 MB file size

---

## **PHASE 4: Advanced Features** (Future Enhancements)

### Section 4.1: Measurement Tools
**Status**: FUTURE

**Features**:
- Distance measurement (point-to-point)
- Area measurement (polygon selection)
- Volume measurement (bounding box)
- Coordinate display (click to show XYZ)

---

### Section 4.2: Annotation System
**Status**: FUTURE

**Features**:
- Add text labels to 3D points
- Draw lines/arrows
- Highlight regions
- Save annotations in HTML file

---

### Section 4.3: Comparison Mode
**Status**: FUTURE

**Features**:
- Load two models side-by-side
- Overlay models (before/after comparison)
- Diff visualization (show changes)

---

### Section 4.4: Gaussian Splat Support
**Status**: FUTURE

**Objective**: Support 3DGS (Gaussian Splatting) from Terra.

**Challenges**:
- Different rendering technique (not traditional mesh)
- Requires specialized WebGL shaders
- Potentially very large files (millions of splats)

**Approach**:
- Separate viewer template (not Three.js, custom WebGL)
- Different embedding strategy (compressed splat data)
- May require WebAssembly for performance

---

### Section 4.5: B3DM/3D Tiles Support
**Status**: FUTURE

**Objective**: Support Terra LOD models (B3DM format).

**Challenges**:
- Tiled format (multiple files)
- Requires Cesium.js (heavier than Three.js)
- LOD streaming (not fully embeddable)

**Approach**:
- Convert B3DM to single glTF/GLB
- Embed GLB in HTML viewer
- May lose LOD benefits (loads entire model at once)

---

## **PHASE 5: Testing & Deployment**

### Section 5.1: QA Testing
**Status**: PENDING

**Test Cases**:
1. **Small OBJ model** (< 5 MB)
2. **Large OBJ model** (50+ MB)
3. **Multi-file OBJ** (split geometry + multiple textures)
4. **PLY binary** (typical Terra export)
5. **PLY ASCII** (text-based)
6. **High-res textures** (4K images)
7. **Low-res textures** (512�512)
8. **Missing texture files** (error handling)
9. **Corrupt OBJ file** (error handling)
10. **Very large model** (170+ MB, performance test)

**Browsers to Test**:
- Chrome (latest)
- Firefox (latest)
- Edge (latest)
- Safari (macOS/iOS if available)
- Mobile Chrome (Android)
- Mobile Safari (iOS)

**File Locations**:

- `tests/sample_models/` - Test data directory
- `tests/qa-results.md` - Test results documentation

**Deliverables**:

- Test results matrix
- Bug tracker (issues found)
- Performance benchmarks (FPS, load time)

---

### Section 5.2: Documentation
**Status**: PENDING

**File Locations**:

- `docs/USER_GUIDE.md` - End-user documentation
- `docs/DISTRIBUTION_README.md` - Distribution instructions
- `docs/DEVELOPER_GUIDE.md` - Developer documentation
- `docs/FAQ.md` - Frequently asked questions

**Documents to Create**:

1. **User Guide** (`docs/USER_GUIDE.md`)
   - How to export from Terra
   - How to use the generator app
   - Troubleshooting common issues

2. **Distribution Guide** (`docs/DISTRIBUTION_README.md`)
   - How to share the .exe
   - How to share generated HTML files
   - File size considerations

3. **Developer Guide** (`docs/DEVELOPER_GUIDE.md`)
   - Code architecture overview
   - How to modify HTML template
   - How to rebuild .exe
   - How to add new features

4. **FAQ** (`docs/FAQ.md`)
   - Common questions
   - File format explanations
   - Performance optimization tips

---

### Section 5.3: Repository Organization
**Status**: PENDING

**Folder Structure**:
```
_three.js-viewer/
   .planning-to-do/
      embedded-viewer.md          � This file
   dist/
      Terra Model Viewer Generator.exe  � Standalone app
   src/
      model-viewer-generator.py    � Main GUI app
      modules/
         obj_parser.py
         ply_parser.py
         texture_processor.py
         geometry_optimizer.py
         html_embedder.py
      templates/
          viewer-obj.html          � OBJ viewer template
          viewer-ply.html          � PLY viewer template
   examples/
      example-obj-viewer.html      � Sample generated file
      example-ply-viewer.html      � Sample generated file
   tests/
      test_obj_parser.py
      test_ply_parser.py
      sample_models/
          cube.obj                 � Test model
          points.ply               � Test model
   docs/
      USER_GUIDE.md
      DISTRIBUTION_README.md
      DEVELOPER_GUIDE.md
      FAQ.md
   build/                           � PyInstaller build artifacts
   README.md                        � Main project README
   requirements.txt                 � Python dependencies
```

---

## Technical Specifications

### File Size Limits

| Model Type | Original Size | Embedded HTML Size | Performance |
|------------|---------------|-------------------|-------------|
| Small | < 5 MB | < 7 MB | Excellent (instant load) |
| Medium | 5-20 MB | 7-27 MB | Good (1-3 sec load) |
| Large | 20-50 MB | 27-66 MB | Acceptable (3-10 sec load) |
| Very Large | 50-100 MB | 66-133 MB | Poor (10-30 sec load, may lag) |
| Extreme | 100+ MB | 133+ MB | Not Recommended (browser crash risk) |

**Recommendation**: Warn user if embedded HTML will exceed 50MB

---

### Three.js Dependencies

**Modern ES Module CDN Links** (recommended approach as of Three.js r150+):
```html
<!-- Import Map for Three.js ES Modules -->
<script type="importmap">
    {
        "imports": {
            "three": "https://cdn.jsdelivr.net/npm/three@0.167.0/build/three.module.js",
            "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.167.0/examples/jsm/"
        }
    }
</script>

<!-- Use ES Module syntax -->
<script type="module">
    import * as THREE from 'three';
    import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
    import { MTLLoader } from 'three/addons/loaders/MTLLoader.js';
    import { PLYLoader } from 'three/addons/loaders/PLYLoader.js';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

    // Your viewer code here...
</script>
```

**IMPORTANT**: The old `/examples/js/` paths are deprecated and no longer exist in modern Three.js versions. Always use `/examples/jsm/` (ES modules) instead.

**Alternative**: Download and embed Three.js directly in HTML (fully offline) - must use ES module format

---

### Python Dependencies

```txt
# GUI
tkinter (built-in)

# Image Processing
Pillow>=11.0.0  # Updated for Python 3.12+ compatibility

# File Encoding
base64 (built-in)

# JSON/Data Handling
json (built-in)

# File System
os, pathlib (built-in)

# EXE Building
pyinstaller>=6.11.0  # Latest stable version (as of 2025)

# Optional: Image Optimization
pillow-webp>=0.1.0  # WebP support
```

**Compatibility Notes (2025)**:
- Ensure Python 3.10+ for PyInstaller compatibility
- tkinter may require separate installation on some Linux distributions
- Test PyInstaller builds on target Windows version (Win10/Win11)

---

## Risk Assessment & Mitigation

### Risk 1: File Size Too Large
**Impact**: HTML file > 100MB, browser crashes
**Probability**: Medium (Terra models can be huge)
**Mitigation**:
- Warn user if embedded size > 50MB
- Offer optimization options (reduce textures, simplify geometry)
- Provide alternative: generate viewer that loads external model file

---

### Risk 2: Browser Compatibility
**Impact**: Viewer doesn't work in some browsers
**Probability**: Low-Medium (ES modules require modern browsers)
**Mitigation**:
- Test on all major browsers (Chrome 89+, Firefox 87+, Edge 89+, Safari 15+)
- Include WebGL detection + fallback message
- Use stable Three.js version (not bleeding edge)
- **CRITICAL**: ES modules with import maps require modern browsers (2021+)
- Consider fallback message for older browsers (IE11, old mobile browsers)
- Import maps not supported in Safari < 16.4 (released March 2023)

---

### Risk 3: Texture Path Issues
**Impact**: OBJ textures don't load correctly
**Probability**: Medium (Terra uses complex folder structures)
**Mitigation**:
- Parse MTL file carefully, resolve relative paths
- Ask user to select folder (auto-detect all textures)
- Embed all textures as data URIs (eliminate path dependencies)

---

### Risk 4: Memory Limits
**Impact**: Python app crashes during processing
**Probability**: Medium (large models = high RAM usage)
**Mitigation**:
- Process files in chunks (streaming)
- Use generators instead of loading entire file into memory
- Add memory usage monitoring + warnings

---

### Risk 5: Slow Performance
**Impact**: Viewer takes 30+ seconds to load
**Probability**: Medium (large embedded data = slow parsing)
**Mitigation**:
- Implement progressive loading (show model in stages)
- Use compressed formats (gzip, WebP)
- Offer option to generate external-file viewer (faster load)

---

## Success Metrics

### Phase 1 Success
-  Planning document complete
-  Prototype viewer loads hardcoded model
-  Cross-browser tested

### Phase 2 Success
-  OBJ viewer supports Terra multi-file exports
-  PLY viewer supports binary/ASCII formats
-  File size < 50MB for typical models
-  Load time < 10 seconds

### Phase 3 Success
-  GUI app is intuitive (non-technical users can use it)
-  Processing time < 1 minute for 50MB model
-  Standalone .exe works on clean Windows machine
-  Error messages are clear and actionable

### Phase 4 Success
-  Measurement tools functional
-  Annotation system saves data in HTML
-  Gaussian Splat viewer prototype working

### Phase 5 Success
-  All test cases pass
-  Documentation complete
-  Zero critical bugs
-  User feedback positive

---

## Timeline Estimate

| Phase | Estimated Time | Dependencies |
|-------|----------------|--------------|
| Phase 1 | 2-3 days | None |
| Phase 2 | 5-7 days | Phase 1 complete |
| Phase 3 | 4-6 days | Phase 2 complete |
| Phase 4 | 3-5 days | Phase 3 complete (optional) |
| Phase 5 | 2-3 days | All phases complete |
| **Total** | **16-24 days** | Sequential execution |

**Parallel Execution**: Phases 1-3 are critical path. Phase 4 (advanced features) can be developed in parallel or post-launch.

---

## Next Steps

### Immediate Actions
1.  Complete this planning document
2. � Create prototype HTML viewer (Phase 1.2)
3. � Test with a sample Terra OBJ export
4. � Validate file size assumptions with real-world data

### Before Starting Phase 2
- [ ] Review plan with stakeholders
- [ ] Get sample Terra models (OBJ + PLY)
- [ ] Confirm file size limits with real-world testing
- [ ] Decide on optimization priorities (texture reduction? geometry simplification?)

### Questions to Answer
1. Do we need offline support (embed Three.js) or is CDN acceptable?
2. What's the maximum acceptable HTML file size? (50MB? 100MB?)
3. Should we support FBX? (adds complexity)
4. Should we support I3S? (ESRI-specific, may not be worth it)
5. Do we want measurement tools in Phase 1, or Phase 4?

---

## Appendix: Alternative Approaches

### Alternative A: External File Viewer
Instead of embedding, generate HTML that loads external model file via file picker or drag-drop.

**Pros**:
- Smaller HTML file
- Faster load times
- Easier to update model without regenerating HTML

**Cons**:
- Not portable (requires both HTML + model file)
- User must keep files together
- More complex to share

**Verdict**: Offer as secondary option for very large models (> 50MB)

---

### Alternative B: Cloud-Hosted Viewer
Upload model to cloud storage, generate HTML with embedded URL.

**Pros**:
- Tiny HTML file (just loads from URL)
- Fast load times
- Easy to share (just URL)

**Cons**:
- Requires cloud hosting (cost, privacy concerns)
- Requires internet connection
- Not self-contained

**Verdict**: Out of scope for this project (may revisit later)

---

### Alternative C: Conversion to glTF/GLB
Convert Terra OBJ/PLY to glTF/GLB before embedding.

**Pros**:
- Smaller file size (binary format, compressed)
- Faster parsing (GPU-optimized format)
- Single file (textures embedded in GLB)

**Cons**:
- Requires conversion step (extra complexity)
- Potential quality loss during conversion
- Need additional library (obj2gltf, ply2gltf)

**Verdict**: Consider for Phase 2 optimization (optional conversion step)

---

## Conclusion

This plan provides a comprehensive, phased approach to building a Terra 3D model embedded viewer generator. By breaking the project into discrete phases and sections, we can ensure quality at each step and adapt as we encounter real-world challenges.

**Key Principles**:
1. **Start simple** - Prototype first, optimize later
2. **Test early** - Use real Terra exports from day 1
3. **User-focused** - GUI should be intuitive for non-technical users
4. **Performance-aware** - Monitor file sizes and load times constantly
5. **Iterative** - Each phase builds on the previous one

**Ready to proceed with Phase 1.2: Prototype HTML Viewer!**

---

## CHANGELOG - Three.js Migration (January 2025)

### Critical Updates Made

**Date**: January 2025
**Issue**: Prototype viewers failed to load due to deprecated Three.js CDN paths
**Root Cause**: Three.js moved to ES modules architecture starting with r150+; old `/examples/js/` paths no longer exist

### Changes Applied

1. **prototype-obj-viewer.html**
   - Migrated from UMD build to ES modules
   - Added import map for Three.js dependencies
   - Updated all loader imports to use `three/addons/` path
   - Exposed control functions to global scope for onclick handlers

2. **prototype-ply-viewer.html**
   - Same migration as OBJ viewer
   - Updated PLYLoader import path
   - Maintained point cloud rendering functionality

3. **embedded-viewer.md Planning Document**
   - Updated Three.js CDN examples to use ES modules
   - Added browser compatibility warnings for import maps
   - Updated Python dependency versions
   - Documented the migration in Phase 1.2 notes

### Browser Compatibility Impact

**Before**: Any browser with WebGL support
**After**: Modern browsers only:
- Chrome 89+ (March 2021)
- Firefox 87+ (March 2021)
- Safari 16.4+ (March 2023) - **IMPORTANT**: Import maps added late
- Edge 89+ (March 2021)

### Migration Pattern for Future Reference

```html
<!-- OLD (Deprecated - WILL NOT WORK) -->
<script src="https://cdn.jsdelivr.net/npm/three@0.167.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.167.0/examples/js/loaders/OBJLoader.js"></script>

<!-- NEW (Modern ES Modules) -->
<script type="importmap">
{
    "imports": {
        "three": "https://cdn.jsdelivr.net/npm/three@0.167.0/build/three.module.js",
        "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.167.0/examples/jsm/"
    }
}
</script>
<script type="module">
    import * as THREE from 'three';
    import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
</script>
```

### Next Steps

- Test prototypes in all target browsers
- Consider polyfill or fallback for older Safari versions
- Update all future HTML templates to use ES module pattern
- Document this requirement in user-facing documentation

---

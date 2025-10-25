# Resources Directory

This directory contains assets, libraries, and resources used by the application.

## Structure

```
resources/
├── icons/                       # Application icons
│   ├── app-icon.ico            # Windows .exe icon
│   └── app-icon.png            # PNG version for documentation
└── three-js/                    # Three.js library (for offline use)
    ├── three.min.js            # Three.js core
    ├── OBJLoader.js            # OBJ loader
    ├── MTLLoader.js            # MTL material loader
    ├── PLYLoader.js            # PLY loader
    └── OrbitControls.js        # Mouse controls
```

## Icons

**Purpose**: Application icon for the Windows executable

**Location**: `resources/icons/app-icon.ico`

**Format**: `.ico` file (Windows icon format)

**Usage**: Referenced in PyInstaller build script

## Three.js Library

**Purpose**:
- Embed in HTML templates for fully offline viewers
- Alternative to CDN links (no internet required)

**Version**: Three.js r167 (or latest stable)

**Download from**:
- https://cdn.jsdelivr.net/npm/three@0.167.0/build/three.min.js
- https://cdn.jsdelivr.net/npm/three@0.167.0/examples/js/loaders/OBJLoader.js
- https://cdn.jsdelivr.net/npm/three@0.167.0/examples/js/loaders/MTLLoader.js
- https://cdn.jsdelivr.net/npm/three@0.167.0/examples/js/loaders/PLYLoader.js
- https://cdn.jsdelivr.net/npm/three@0.167.0/examples/js/controls/OrbitControls.js

## Offline vs CDN

The application can generate HTML files in two modes:

1. **CDN Mode** (Default)
   - HTML links to Three.js via CDN URLs
   - Smaller HTML file size
   - Requires internet connection to view

2. **Offline Mode** (Optional)
   - Three.js embedded directly in HTML
   - Larger HTML file size (~500KB extra)
   - Works completely offline

**Configuration**: Set in GUI application options (Phase 3.1)

## Notes

- Three.js files are minified for smaller size
- Check for updates periodically (new Three.js versions)
- License: Three.js is MIT licensed (include attribution)

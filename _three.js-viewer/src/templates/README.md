# Terra 3D Viewer Templates

Production-ready HTML templates for standalone 3D model viewing with embedded data.

**Created**: January 2025
**Version**: 2.0.0
**Three.js**: r167 (ES Modules)

---

## Files

### 1. [viewer-obj.html](viewer-obj.html)
**Purpose**: Standalone OBJ model viewer with material and texture support

**Features**:
- Full Three.js OBJ/MTL loader support
- Embedded texture handling (Base64 data URIs)
- Material system with lighting presets
- Wireframe mode toggle
- Shadow rendering
- Screenshot export
- Responsive design (desktop, tablet, mobile)

**Data Injection Points**:
```javascript
const EMBEDDED_OBJ = `{{OBJ_DATA}}`;           // OBJ geometry data
const EMBEDDED_MTL = `{{MTL_DATA}}`;           // Material definitions
const EMBEDDED_TEXTURES = {{TEXTURE_DATA}};     // Object with texture name: base64 URI
```

**File Size**: ~62KB (before data injection)

---

### 2. [viewer-ply.html](viewer-ply.html)
**Purpose**: Standalone PLY point cloud viewer

**Features**:
- PLY (ASCII and binary) support via Three.js PLYLoader
- Vertex color rendering
- Adjustable point size (0.5-10px)
- Auto-centering on point cloud
- Screenshot export
- Grid and axis helpers
- Responsive design

**Data Injection Points**:
```javascript
const EMBEDDED_PLY = `{{PLY_DATA}}`;  // PLY point cloud data (ASCII or Base64)
```

**File Size**: ~58KB (before data injection)

---

### 3. [viewer-common.js](viewer-common.js)
**Purpose**: Reusable viewer class library (optional, for modular builds)

**Classes**:
- `TerraViewer` - Base viewer class with common functionality
- `PLYViewer` - Extended class for point cloud specific features

**Functions**:
- `checkWebGLSupport()` - Detect WebGL availability
- `checkBrowserCompatibility()` - Check for import map support

**Usage** (for modular builds):
```javascript
import { TerraViewer, PLYViewer } from './viewer-common.js';
const viewer = new TerraViewer({ containerId: 'canvas-container' });
await viewer.init(THREE, OrbitControls);
```

**File Size**: ~15KB

---

## Common Features (Both Templates)

### UI Controls
- **Reset Camera** - Return to initial view position
- **Auto Rotate** - Automatic model rotation
- **Toggle Grid** - Show/hide ground grid
- **Background Color** - Color picker for scene background
- **Screenshot** - Export current view as PNG
- **Fullscreen** - Toggle fullscreen mode
- **Minimize Panel** - Collapse controls for unobstructed view

### Lighting Presets (OBJ only)
1. **Default** - Balanced ambient + directional lighting
2. **Realistic** - Natural outdoor lighting simulation
3. **Bright** - High ambient light, minimal shadows
4. **Dramatic** - Low ambient, strong directional (high contrast)
5. **Flat** - Maximum ambient for technical viewing

### Performance Features
- WebGL renderer with anti-aliasing
- Device pixel ratio optimization for retina displays
- Damped orbit controls (smooth deceleration)
- Shadow mapping (2048x2048 resolution)
- Automatic model centering and scaling
- Window resize handling
- Touch gesture support (mobile/tablet)

### Responsive Breakpoints
- **Desktop**: Full controls, maximum detail
- **Tablet** (≤768px): Adjusted panel sizes
- **Mobile** (≤480px): Compact UI, minimized text
- **Touch Devices**: Larger hit targets for buttons

---

## Browser Compatibility

### Required
- **Chrome**: 89+ (March 2021)
- **Firefox**: 87+ (March 2021)
- **Edge**: 89+ (March 2021)
- **Safari**: 16.4+ (March 2023) - **Import maps added late**

### Why These Requirements?
- ES modules with import maps (standardized 2021)
- Safari was late to implement import maps (v16.4 in 2023)
- WebGL 1.0+ support

### Fallback for Older Browsers
Templates include WebGL detection and display error messages for unsupported browsers.

---

## Usage Pattern

### Step 1: Copy Template
```bash
cp viewer-obj.html my-model-viewer.html
```

### Step 2: Inject Data
Replace placeholders with actual model data:

**For OBJ**:
```javascript
const EMBEDDED_OBJ = `v 0 0 0\nv 1 0 0\n...`;  // Your OBJ data
const EMBEDDED_MTL = `newmtl material0\n...`;   // Your MTL data
const EMBEDDED_TEXTURES = {
    "texture.jpg": "data:image/jpeg;base64,/9j/4AAQ..."
};
```

**For PLY**:
```javascript
const EMBEDDED_PLY = `ply\nformat ascii 1.0\n...`;  // Your PLY data
```

### Step 3: Deploy
Serve as a single HTML file - no external dependencies except Three.js CDN.

---

## Data Injection Workflow (Python Script)

The templates are designed to work with a Python script that:

1. Reads 3D model files (.obj, .mtl, .ply, .jpg)
2. Converts textures to Base64 data URIs
3. Injects data into template placeholders
4. Writes final standalone HTML file

**Placeholders**:
- `{{OBJ_DATA}}` - OBJ geometry string
- `{{MTL_DATA}}` - MTL material string
- `{{TEXTURE_DATA}}` - JSON object with texture mappings
- `{{PLY_DATA}}` - PLY point cloud string

**Python Example** (pseudocode):
```python
with open('viewer-obj.html', 'r') as template:
    html = template.read()

obj_data = read_file('model.obj')
mtl_data = read_file('model.mtl')
textures = {
    'texture.jpg': base64_encode_image('texture.jpg')
}

html = html.replace('{{OBJ_DATA}}', escape_js_string(obj_data))
html = html.replace('{{MTL_DATA}}', escape_js_string(mtl_data))
html = html.replace('{{TEXTURE_DATA}}', json.dumps(textures))

with open('output-viewer.html', 'w') as output:
    output.write(html)
```

---

## Testing Checklist

### Functionality Tests
- [ ] Model loads without errors
- [ ] Model renders correctly
- [ ] All UI buttons functional
- [ ] Camera controls work (rotate, zoom, pan)
- [ ] Screenshot export downloads PNG
- [ ] Fullscreen mode works
- [ ] Lighting presets change appearance
- [ ] Window resize handles correctly
- [ ] Loading screen appears and disappears
- [ ] Error messages display for invalid data

### Performance Tests
- [ ] 60 FPS rendering on desktop
- [ ] Smooth interaction with damping
- [ ] No memory leaks during extended use
- [ ] Load time < 3 seconds for 10MB model
- [ ] Screenshot generation completes instantly

### Cross-Browser Tests
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Safari 16.4+ (if available)

### Responsive Tests
- [ ] Desktop (1920x1080)
- [ ] Tablet portrait (768x1024)
- [ ] Tablet landscape (1024x768)
- [ ] Mobile (375x667)
- [ ] Touch gestures work on devices

### Accessibility
- [ ] Tab navigation through controls
- [ ] Buttons have hover/focus states
- [ ] Error messages are readable
- [ ] Color contrast meets WCAG AA

---

## Customization Guide

### Change Default Camera Position
```javascript
// In viewer init:
this.camera.position.set(10, 10, 10); // x, y, z coordinates
```

### Adjust Lighting
```javascript
// Modify intensity values:
this.lights.ambient.intensity = 0.6;        // 0.0 - 1.0+
this.lights.directional.intensity = 1.0;   // 0.0 - 2.0+
```

### Change Color Scheme
```css
/* Update CSS variables in <style> block */
.control-button {
    background: linear-gradient(135deg, #your-color, #your-color-dark);
}
```

### Add Custom Controls
```javascript
// Add button in HTML:
<button class="control-button" onclick="customFunction()">Custom</button>

// Add function in script:
window.customFunction = function() {
    // Your custom logic
    viewer.model.rotation.y += 0.1;
};
```

---

## Known Limitations

1. **File Size**: Embedded data increases HTML file size significantly
   - 10MB model → ~13-15MB HTML file (Base64 overhead)
   - Browser limits: Most browsers handle files up to 50-100MB

2. **Import Maps**: Safari < 16.4 not supported
   - Users on older Safari will see error message
   - Workaround: Use transpiled bundle (requires build step)

3. **Mobile Performance**: Large models (>50MB) may struggle on mobile devices
   - Consider progressive loading for production use
   - Add texture resolution options

4. **No Progressive Loading**: Current templates load entire model before display
   - Future enhancement: Stream large models in chunks

---

## Next Steps (Phase 2.2)

1. Create Python script for automated data injection
2. Add multi-file OBJ support (merge multiple .obj files)
3. Implement texture resolution downscaling options
4. Add binary PLY support
5. Create batch processing tool
6. Build GUI application for non-technical users

---

## Support

**Documentation**: See `.planning-to-do/embedded-viewer.md`
**Prototypes**: See `prototypes/phase1/`
**Issues**: Contact development team

---

**Last Updated**: January 24, 2025
**Phase**: 2.1 Complete ✅

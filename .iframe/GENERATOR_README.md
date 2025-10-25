# Scene Viewer HTML Generator - GUI Application

## Overview

This GUI application makes it easy to create HTML wrapper files for ESRI Scene Viewer URLs. No need to manually edit HTML files - just paste your URL, choose where to save, and click Generate!

## How to Use

### Quick Start
1. **Double-click** `Scene Viewer Generator.bat` on your desktop
2. The GUI application will open
3. Fill in the fields:
   - **Scene Viewer URL**: Paste your ESRI Scene Viewer URL
   - **Output Folder**: Choose where to save the HTML file (defaults to Desktop)
   - **File Name**: Name your HTML file (e.g., "my-scene")
4. Click **Generate HTML File**
5. Click **Yes** to open it in your browser, or **No** to just save it
6. Use **Show in Folder** button to open File Explorer to the saved location

### Features

- **Simple GUI**: Clean, easy-to-use Windows interface
- **Smart defaults**: Pre-fills Desktop as output location
- **Validation**: Checks URLs and file paths before generating
- **Overwrite protection**: Asks before overwriting existing files
- **Auto-open**: Option to open the generated HTML in your browser immediately
- **Show in Folder**: Opens File Explorer and highlights your generated file
- **Clear button**: Reset form to start fresh

## Files

- **Scene Viewer Generator.bat** - Double-click this to launch the app
- **scene-viewer-generator.py** - The Python GUI application (runs automatically via .bat)

## Requirements

- **Python 3.x** installed on your system (you have Python 3.13.3 ✓)
- **tkinter** (comes built-in with Python on Windows)

## Moving to Desktop

To use this as a desktop application:

1. **Option 1**: Create a shortcut
   - Right-click `Scene Viewer Generator.bat`
   - Click "Create shortcut"
   - Move the shortcut to your Desktop

2. **Option 2**: Copy the files
   - Copy both `Scene Viewer Generator.bat` and `scene-viewer-generator.py` to your Desktop
   - Double-click the .bat file from Desktop

## Screenshot Guide

```
┌─────────────────────────────────────────────────────┐
│  ESRI Scene Viewer HTML Generator                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Scene Viewer URL:                                   │
│  ┌─────────────────────────────────────────────┐   │
│  │ https://www.arcgis.com/home/webscene/...    │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  Output Folder:                                      │
│  ┌───────────────────────────────────┐ [Browse...]  │
│  │ C:\Users\rbake\Desktop            │              │
│  └───────────────────────────────────┘              │
│                                                      │
│  File Name:                                          │
│  ┌───────────────────────────────────┐ .html        │
│  │ scene-viewer                      │              │
│  └───────────────────────────────────┘              │
│                                                      │
│  [Generate HTML File] [Show in Folder] [Clear]      │
│                                                      │
│  ✓ Successfully created: scene-viewer.html          │
│                                                      │
│  Enter your Scene Viewer URL, choose output         │
│  location, and click Generate.                      │
└─────────────────────────────────────────────────────┘
```

## Tips

1. **URL Parameters**: Include parameters like `ui=min`, `autoRotate=true`, etc. in your URL before generating
2. **Multiple Scenes**: Generate multiple HTML files with different names for different scenes
3. **Organize Output**: Use different output folders to organize scenes by project or client
4. **Quick Access**: Create desktop shortcuts to your most-used generated HTML files

## Troubleshooting

### "Python is not installed or not in PATH"
- Your system shows Python 3.13.3 is installed, so this shouldn't happen
- If you see this error, try running `python scene-viewer-generator.py` directly from Command Prompt

### GUI doesn't open
- Make sure both `.bat` and `.py` files are in the same folder
- Try right-clicking the .bat file and "Run as administrator"

### "tkinter not found"
- Tkinter comes with Python on Windows by default
- If missing, reinstall Python and ensure "tcl/tk and IDLE" is checked during installation

## Example Workflow

1. Open your Scene Viewer in ArcGIS Online
2. Configure camera position, settings, etc.
3. Copy the URL from browser address bar
4. Double-click `Scene Viewer Generator.bat`
5. Paste URL into the app
6. Change filename to something descriptive (e.g., "downtown-3d-model")
7. Click Generate
8. Open in browser to test
9. Use "Show in Folder" to see where it was saved

The generated HTML file is standalone and can be:
- Opened directly in any browser
- Moved to any location
- Shared with others
- Served via a web server or localhost

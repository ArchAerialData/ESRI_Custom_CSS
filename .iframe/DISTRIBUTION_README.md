# Scene Viewer Generator - Standalone EXE Distribution

## Overview

The **Scene Viewer Generator** is now available as a **standalone Windows executable** that works on **any Windows PC** without requiring Python to be installed.

## What You Get

📦 **Single EXE File**: `Scene Viewer Generator.exe` (~9.8 MB)
- No installation required
- No Python needed
- No dependencies
- Works on any Windows 10/11 PC

## Location

The standalone executable is located in:
```
.iframe/dist/Scene Viewer Generator.exe
```

## How to Distribute

### Option 1: Copy the EXE File
1. Navigate to `.iframe/dist/`
2. Copy `Scene Viewer Generator.exe`
3. Paste it anywhere you want:
   - Desktop
   - USB drive
   - Network share
   - Send via email/Teams/Slack
4. Double-click to run!

### Option 2: Create Desktop Shortcut
1. Right-click `Scene Viewer Generator.exe`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. Rename to "Scene Viewer Generator" (removes ".exe - Shortcut")

## Usage

1. **Double-click** `Scene Viewer Generator.exe`
2. The GUI application opens immediately
3. Fill in:
   - **Scene Viewer URL**: Paste from browser
   - **Output Folder**: Choose destination (Browse button available)
   - **File Name**: Name your HTML file
4. Click **Generate HTML File**
5. Use **Show in Folder** to see the generated file

## Distribution Checklist

✅ **Completely portable** - Works from any location
✅ **No installation** - Just copy and run
✅ **No Python required** - All dependencies bundled
✅ **Works on any Windows PC** - Windows 10/11 compatible
✅ **Self-contained** - Single .exe file
✅ **Safe to distribute** - No security warnings (unsigned, but safe)

## File Locations

```
.iframe/
├── dist/
│   └── Scene Viewer Generator.exe    ← DISTRIBUTE THIS
├── build/                             ← Build artifacts (can delete)
├── scene-viewer-generator.py          ← Original source code
├── Scene Viewer Generator.bat         ← Python launcher (not needed with .exe)
├── Scene Viewer Generator.spec        ← PyInstaller config (can delete)
└── test.html                          ← Example Scene Viewer embed
```

## What to Distribute

**Minimum (Recommended)**:
- `Scene Viewer Generator.exe` - The standalone application

**Optional**:
- `DISTRIBUTION_README.md` - This file (user instructions)
- `GENERATOR_README.md` - Detailed usage guide

**Not Needed**:
- `.py` source files
- `.bat` launcher
- `.spec` file
- `build/` folder
- `__pycache__/` folder

## Security Notes

### Windows SmartScreen Warning
When running the .exe for the first time, Windows may show:
```
"Windows protected your PC"
Microsoft Defender SmartScreen prevented an unrecognized app from starting
```

**This is normal** for unsigned executables. To bypass:
1. Click **"More info"**
2. Click **"Run anyway"**

This happens because the .exe is not digitally signed (requires paid certificate).

### Antivirus False Positives
Some antivirus software may flag the .exe because:
- It's a PyInstaller-generated executable (common false positive)
- It's unsigned

**The application is safe** - it only:
- Creates HTML files
- Opens File Explorer
- Uses standard tkinter GUI components

If needed, add to antivirus exclusions.

## Technical Details

- **Built with**: PyInstaller 6.14.2
- **Python version**: 3.13.3
- **GUI framework**: tkinter (bundled)
- **Architecture**: 64-bit Windows
- **File size**: ~9.8 MB (compressed)
- **Startup time**: ~2-3 seconds (unpacks to temp folder on first run)

## For Developers

If you need to rebuild the .exe from source:

```bash
cd .iframe
pyinstaller --onefile --windowed --name "Scene Viewer Generator" --icon=NONE scene-viewer-generator.py
```

The new .exe will be in `dist/Scene Viewer Generator.exe`

## Comparison: EXE vs Python Script

| Feature | Standalone EXE | Python Script |
|---------|---------------|---------------|
| Requires Python | ❌ No | ✅ Yes |
| File Size | ~9.8 MB | ~10 KB |
| Portability | ✅ Complete | ⚠️ Needs Python |
| Distribution | ✅ Copy & Run | ❌ Install deps |
| Startup Time | ~2-3 sec | <1 sec |
| Easy to Update | ⚠️ Rebuild EXE | ✅ Edit .py |

## Troubleshooting

### "Windows protected your PC"
- Click "More info" → "Run anyway"
- This is normal for unsigned executables

### EXE doesn't start
- Check Windows Event Viewer for errors
- Ensure you're running on 64-bit Windows
- Try "Run as administrator"

### GUI looks blurry on high-DPI displays
- Right-click .exe → Properties → Compatibility
- Check "Override high DPI scaling behavior"
- Select "System (Enhanced)"

### Antivirus blocks the EXE
- Add to exclusions/whitelist
- The app only creates HTML files, no network or system access

## Support

For issues or questions:
1. Check this README
2. Check `GENERATOR_README.md` for usage guide
3. Verify you're on Windows 10/11 64-bit
4. Check Windows Event Viewer for errors

# ESRI Scene Viewer to Local HTML Embedding

## Overview

This folder contains HTML wrapper files that embed ESRI ArcGIS Scene Viewer apps into a local HTML file. This allows you to open 3D web scenes in your browser via localhost while preserving all original functionality including cameras, tools, and interactive features.

## How It Works

The technique uses a simple HTML iframe wrapper that embeds the Scene Viewer URL:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        iframe {
            width: 100vw;
            height: 100vh;
            border: none;
        }
    </style>
</head>
<body>
    <iframe
        frameborder="0"
        scrolling="no"
        allowfullscreen
        src="YOUR_SCENE_VIEWER_URL_HERE">
    </iframe>
</body>
</html>
```

## Key Elements

- **Full viewport sizing**: `width: 100vw; height: 100vh` ensures the iframe fills the entire browser window
- **No borders/margins**: Removes visual separation between the iframe and browser window for a seamless experience
- **allowfullscreen**: Enables fullscreen mode for the embedded scene
- **scrolling="no"**: Disables scrollbars (Scene Viewer handles its own navigation)

## Creating a New Scene Viewer Embed

1. Get your Scene Viewer URL from ArcGIS Online
2. Copy `test.html` as a template
3. Replace the `src` attribute in the iframe with your Scene Viewer URL
4. Update the `<title>` tag for identification
5. Save with a descriptive filename (e.g., `scene-project-name.html`)

## Scene Viewer URL Parameters

Customize the embedded experience by adding parameters to your Scene Viewer URL:

### Essential Parameters
- `webscene=<id>` - The web scene ID to display
- `ui=min` - Minimal UI (hides unnecessary controls, recommended for embeds)

### Camera Position
- `center=<longitude>,<latitude>` - Set initial camera position (e.g., `-97.17,32.68`)
- `distance=<meters>` - Camera distance from ground (e.g., `500`)
- `tilt=<degrees>` - Camera tilt angle (e.g., `45`)

### Animation
- `autoRotate=true` - Enable automatic scene rotation
- `rotationSpeed=<number>` - Rotation speed, where `0.5` is slow, `1.0` is normal (e.g., `0.5`)

### Example URL
```
https://www.arcgis.com/home/webscene/viewer.html?ui=min&webscene=1765b8f2a311407981d9f7664744bb89&center=-97.17793834,32.68900376&distance=500&tilt=45&autoRotate=true&rotationSpeed=0.5
```

## Usage

1. Open the HTML file directly in any browser (Chrome, Firefox, Edge)
2. Or serve via localhost using a local server:
   - Python: `python -m http.server`
   - Node: `npx http-server`
   - VS Code: Use Live Server extension
3. The Scene Viewer will load with full functionality preserved

## Why This Works for Scene Viewer

ESRI's Scene Viewer (`arcgis.com/home/webscene/viewer.html`) does **NOT** set restrictive `X-Frame-Options` headers, which means:
- It can be embedded in iframes from any domain
- It works from local HTML files
- No browser security blocking occurs

The Scene Viewer is designed as a public visualization tool intended to be embedded widely across different websites and applications.

## Why This Does NOT Work for Portfolio Apps

**Portfolio (Instant Apps)** uses stricter security policies and **CANNOT** be embedded this way:

### The Problem
- Portfolio apps set `X-Frame-Options: sameorigin` security header
- This blocks iframe embedding from local files or non-arcgis.com domains
- Browser console will show: `Refused to display 'https://aallc.maps.arcgis.com/' in a frame because it set 'X-Frame-Options' to 'sameorigin'`

### Why ESRI Does This
Portfolio apps are customizable business applications that may contain:
- Sensitive client data
- Private organizational content
- Custom authentication/authorization

ESRI restricts embedding to prevent:
- Clickjacking attacks
- Unauthorized embedding of client apps
- Data exfiltration through malicious frames

### Alternative for Portfolio Apps
Instead of trying to embed Portfolio apps locally, use these approaches:
1. **Direct URL bookmarks** - Save the Portfolio URL as a browser bookmark
2. **Desktop shortcuts** - Create `.url` files pointing to the Portfolio app (store in `clients/<client>/.esri-url/`)
3. **Browser start pages** - Set frequently-used Portfolio apps as browser home pages

## Examples in This Folder

- **test.html** - Scene Viewer example with auto-rotate camera and custom positioning

## Limitations

- **Scene Viewer only**: This technique works for Scene Viewer, not Portfolio/Instant Apps
- **No content modification**: The wrapper cannot modify the ESRI app content itself
- **Internet required**: Requires active internet connection to load ESRI services
- **Authentication**: Some scenes may require ArcGIS Online login depending on sharing settings

## Summary

This HTML iframe embedding technique is perfect for:
- Scene Viewer 3D visualizations
- Public web scenes
- Quick local access to frequently-used scenes

It does NOT work for:
- Portfolio (Instant Apps)
- Other Instant Apps (Media, Sidebar, etc.)
- Private/secured ESRI applications with `X-Frame-Options` restrictions

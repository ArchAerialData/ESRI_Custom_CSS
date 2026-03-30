# ESRI Custom CSS for ArcGIS Instant Apps

This repository maintains client-specific custom CSS and assets for ArcGIS Instant Apps experiences. It includes reusable `.master` template families for every Instant Apps template that officially supports Custom CSS, with two validated families and additional starter-grade families for later DOM validation.

Use this repo to:
- Start a new client theme from the correct template family.
- Keep per-client CSS organized (single-file or modular).
- Track app URLs alongside CSS for quick access and testing.


## Repository Structure

Top-level folders and common files:

- `.master/` - template families and docs used to bootstrap a new client
  - `.master/README.md` - index of supported Instant Apps families and validation tiers
  - `.master/Portfolio/` - validated Portfolio (Tabbed) docs and starter CSS
  - `.master/Imagery Viewer/` - validated Imagery Viewer docs and starter CSS
  - `.master/<Instant App Name>/` - starter family for other Custom-CSS-capable app types
- `clients/` - one folder per client with CSS, app links, and optional logos
  - `clients/<client>/.esri-url/*.url` - ArcGIS app shortcuts for the client
  - `clients/<client>/css/single_block/*.css` - one self-contained CSS file
  - `clients/<client>/css/modular/*.css` - split CSS by area
  - `clients/<client>/logos/...` - optional branded images used by CSS
- `README.md` - this file

Example client folders currently in the repo:

- `clients/arch_aerial`
- `clients/imperial_construction`
- `clients/phillips_66`
- `clients/targa_delaware`
- `clients/tellepsen`
- `clients/urban_infraconstruction`


## How To Use

Add or update custom CSS in an ArcGIS Instant Apps app:

1. Open the client's app
- Use the `.url` in `clients/<client>/.esri-url/` to open the correct app quickly.

2. Add the CSS in the app builder
- In the matching app builder: Theme/Layout settings -> Custom CSS -> paste CSS.
- Choose either:
  - Single-file approach: copy from `css/single_block/<client>.css`.
  - Modular approach: combine relevant files from `css/modular/` (for example `header.css`, `sidebar.css`, `cover.css`).

3. Adjust tokens and assets
- Brand tokens live under `:root` (colors, speeds, optional logo settings).
- If using a CSS-hosted logo, set the relevant logo URL token to a hosted image.
- If embedding other Esri apps as Web Page sections, prefer URL params like `ui=min` for Scene Viewer to reduce unstyled headers.

4. Test and iterate
- Esri supports custom CSS but updates can affect selectors. Re-test after each ArcGIS Online release.
- Keep client-specific overrides at the bottom of the CSS to ease future template updates.


## Supported App Families

The official support source is the ArcGIS Instant Apps capabilities matrix:
- https://doc.arcgis.com/en/instant-apps/latest/customize/pdf/arcgis-instant-apps-matrix.pdf

Validated in this repo:
- `Portfolio`
- `Imagery Viewer`

Starter / pending live DOM validation:
- `3D Viewer`
- `Atlas`
- `Attachment Viewer`
- `Basic (Media Map)`
- `Category Gallery`
- `Chart Viewer`
- `Interactive Legend`
- `Nearby`
- `Public Notification`
- `Reporter`
- `Sidebar`
- `Slider`
- `Zone Lookup`

Use `.master/README.md` for the current index and tiering.


## Adding a New Client

1. Create the folder structure
- `clients/<client>/{.esri-url,css/{single_block,modular},logos/{.all,cover,headers}}`

2. Start from the correct template family
- Use the matching family under `.master/` for the target Instant Apps template.
- Prefer the validated families first:
  - `.master/Portfolio/`
  - `.master/Imagery Viewer/`
- For all other supported app types, start from that app's starter family and validate selectors in DevTools before relying on structural overrides.
- Copy the matching `template.css` into the client's `css/modular/` folder or use the matching `single_block_starter.css` as reference for `css/single_block/`.

3. Link the app
- Add a `.url` file under `.esri-url` pointing to the ArcGIS Instant Apps builder or the published app.

4. Commit sample assets (optional)
- Place client logos under `logos/` if referenced by CSS.


## Important Notes

- Custom CSS scope: each Instant Apps template can style its own shell, not third-party iframe content. Use supported URL parameters (for example `ui=min` for Scene Viewer) to control embedded headers.
- Accessibility: Preserve focus styles and contrast. The templates include focus treatment for interactive controls.
- Motion preferences: Animations respect `prefers-reduced-motion`. Keep this intact when customizing.
- Maintenance: Re-test after ArcGIS Online releases; keep overrides localized and documented.


## Quick File References

- `.master/Portfolio/context.md:1` - Portfolio selector map and detailed guidance.
- `.master/Portfolio/template.css:1` - Portfolio modular template with brand tokens, header, tabs, and cover support.
- `.master/Imagery Viewer/context.md:1` - Imagery Viewer selector map and guidance.
- `.master/Imagery Viewer/template.css:1` - Imagery Viewer modular template with header, panels, controls, and swipe styling.
- `.master/README.md:1` - index of all supported Instant Apps template families and validation tiers.
- `clients/tellepsen/css/single_block/tellepsen.css:1` - Example of a full Portfolio single-file theme.
- `clients/arch_aerial/css/single_block/arch_aerial.css:1` - Example of a full Imagery Viewer single-file theme.
- `clients/<client>/.esri-url/*.url:1` - App shortcuts for quick access.


## FAQ

- Q: Where do I change tab hover and active styles?
  A: In Portfolio only. See the Tabs section in the Portfolio template or client CSS (`.esri-portfolio-tabbed-item`, `--selected`, `:hover`).

- Q: Why does my Portfolio CSS do nothing in Imagery Viewer?
  A: Imagery Viewer does not render `instant-apps-header` or `#tabbedLayout`. Use the `.master/Imagery Viewer/` templates instead.

- Q: Can I remove the white bar above embedded scenes?
  A: That header belongs to the embedded app (for example Scene Viewer). Use `ui=min` and other supported parameters in the embedded URL.

- Q: Should I use single-block or modular CSS?
  A: Single-block is simpler to paste and manage per app. Modular is better for reuse across multiple apps for the same client.

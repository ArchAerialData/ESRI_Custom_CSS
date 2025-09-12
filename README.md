# ESRI Custom CSS for ArcGIS Instant Apps (Portfolio · Tabbed)

This repository maintains client‑specific custom CSS and assets for ArcGIS Instant Apps “Portfolio (Tabbed)” experiences. It also includes a reusable, modular template to standardize brand tokens, header styles, and tab behaviors.

Use this repo to:
- Start a new client theme from the template.
- Keep per‑client CSS organized (single‑file or modular).
- Track app URLs alongside CSS for quick access and testing.


## Repository Structure

Top‑level folders and common files:

- `.master/` — templates and docs used to bootstrap a new client
  - `.master/README_template.md` — selector map, guidance, and notes
  - `.master/template.css` — modular CSS starter (brand tokens, header, tabs)
- `clients/` — one folder per client with CSS, app links, and optional logos
  - `clients/<client>/.esri-url/*.url` — ArcGIS app shortcuts for the client
  - `clients/<client>/css/single_block/*.css` — one self‑contained CSS file
  - `clients/<client>/css/modular/*.css` — split CSS by area (header, tabs, cover)
  - `clients/<client>/logos/…` — optional branded images used by CSS
- `README.md` — this file

Example client folders currently in the repo:

- `clients/imperial_construction`
- `clients/targa_delaware`
- `clients/tellepsen`
- `clients/urban_infraconstruction`


## How To Use

Add or update custom CSS in an ArcGIS Instant Apps Portfolio (Tabbed) app:

1) Open the client’s Portfolio app
- Use the `.url` in `clients/<client>/.esri-url/` to open the correct app quickly.

2) Add the CSS in the app builder
- In Portfolio builder: Theme/Layout settings → Custom CSS → paste CSS.
- Choose either:
  - Single‑file approach: copy from `css/single_block/<client>.css`.
  - Modular approach: combine relevant files from `css/modular/` (e.g., `header.css`, `sidebar.css`, `cover.css`).

3) Adjust tokens and assets
- Brand tokens live under `:root` (colors, speeds, optional overlay logo settings).
- If using an overlay logo in the header, set `--overlay-logo-url` to a hosted image.
- If embedding other Esri apps as Web Page sections, prefer URL params like `ui=min` for Scene Viewer to reduce unstyled headers.

4) Test and iterate
- Esri supports custom CSS but updates can affect selectors. Re‑test after each ArcGIS Online release.
- Keep client‑specific overrides at the bottom of the CSS to ease future template updates.


## Adding a New Client

1) Create the folder structure
- `clients/<client>/{.esri-url,css/{single_block,modular},logos/{.all,cover,headers}}`

2) Start from the template
- Copy `.master/template.css` into the client’s `css/modular/` (or use it as reference to craft a single‑block CSS in `css/single_block/`).
- Update `:root` tokens (brand colors, motion) and optional overlay logo variables.

3) Link the app
- Add a `.url` file under `.esri-url` pointing to the ArcGIS Instant Apps Portfolio builder or the published app.

4) Commit sample assets (optional)
- Place client logos under `logos/` if referenced by CSS.


## Important Notes

- Custom CSS scope: Portfolio can style itself, not the content of embedded apps. Use supported URL parameters (e.g., `ui=min` for Scene Viewer) to control embedded headers.
- Accessibility: Preserve focus styles and contrast. Template includes focus outlines for tabs.
- Motion preferences: Animations respect `prefers-reduced-motion`. Keep this intact when customizing.
- Maintenance: Re‑test after ArcGIS Online releases; keep overrides localized and documented.


## Quick File References

- `.master/README_template.md:1` — Selector map and detailed guidance.
- `.master/template.css:1` — Modular template with brand tokens, header, tabs, cover.
- `clients/tellepsen/css/single_block/tellepsen.css:1` — Example of a full single‑file theme.
- `clients/urban_infraconstruction/css/single_block/urban.css:1` — Another single‑file theme example.
- `clients/<client>/.esri-url/*.url:1` — App shortcuts for quick access.


## FAQ

- Q: Where do I change tab hover/active styles?
  A: See the Tabs section in the template or client CSS (`.esri-portfolio-tabbed-item`, `--selected`, `:hover`).

- Q: Can I remove the white bar above embedded scenes?
  A: That header belongs to the embedded app (e.g., Scene Viewer). Use `ui=min` and other supported parameters in the embedded URL.

- Q: Should I use single‑block or modular CSS?
  A: Single‑block is simpler to paste and manage per app. Modular is better for reuse across multiple apps for the same client.

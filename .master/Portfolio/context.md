# ESRI Instant Apps — Portfolio (Tabbed) CSS: Expert Context

Purpose: a single, thorough reference you can point agents to for creating and maintaining single‑block custom CSS for ArcGIS Instant Apps “Portfolio (Tabbed)”, with practical selector maps, Calcite variable usage, accessible patterns, and safe practices that work within Instant Apps’ constraints.


## What You Can and Can’t Style

- Scope you control: the Portfolio app shell and its own DOM. You can target Instant Apps web components (like `instant-apps-header` and `instant-apps-landing-page`) and exposed shadow parts via `::part(...)`. You can also style regular elements in the Portfolio layout (tabs, containers, etc.).
- Scope you cannot control: content inside embedded apps (e.g., Scene Viewer, Map Viewer, Experience Builder) when included as Web Page/iframe sections. Due to cross‑origin isolation, your CSS cannot pierce iframe boundaries. Use each embedded app’s supported URL parameters (e.g., Scene Viewer `ui=min`) to reduce built‑in UI instead.
- Runtime: Custom CSS is injected as a single text block in the builder. There is no upload or bundling; design your CSS as one file. Avoid `@import` and external CSS files (CSP and reliability concerns). Referencing hosted images (e.g., for a logo) is fine.


## Core Components and Selectors

Portfolio (Tabbed) uses Instant Apps components and Calcite web components. The most impactful hooks are:

- `instant-apps-header` (web component)
  - `::part(container)` — internal flex container
  - `::part(wrapper)` — internal wrapper (padding/background)
  - `::part(title)` — title text (when exposed)
  - `::part(logo)` — native logo (when used)
  - Custom overlay: use `instant-apps-header::after` for a centered overlay logo you control.
- `instant-apps-landing-page` (Cover page)
  - CSS variables: `--instant-apps-landing-page-text-color`, `--instant-apps-landing-page-entry-button-color`
  - Parts: `::part(container)` to adjust overlay effects (e.g., `backdrop-filter`)
  - Controls inside: Calcite components like `calcite-button` (use `::part(button)`)
- Portfolio (Tabbed layout)
  - Root: `#tabbedLayout`
  - Tab strip container: `#tabbedLayout .esri-portfolio-tabbed__tab-list`
  - Tab item (base): `.esri-portfolio-tabbed-item`
  - Tab item (hover): `.esri-portfolio-tabbed-item:hover`
  - Tab item (selected): `.esri-portfolio-tabbed-item--selected`
  - Focus: `.esri-portfolio-tabbed-item:focus-visible`

These BEM‑style selectors are stable in current builds but are not a formal API. Keep rules narrowly scoped (prefix with `#tabbedLayout` where viable) and validate after Instant Apps releases.


## Calcite Variables (Theming at the Edges)

Instant Apps exposes a subset of Calcite Design System variables that you can set at component boundaries to influence text and brand colors inside web components:

- Commonly effective in header and app shell:
  - `--calcite-color-text-1`, `--calcite-color-text-2`
  - `--calcite-color-brand`, `--calcite-color-brand-hover`
  - Sometimes `--calcite-color-foreground-1` is honored to clear default fills

Where to set them:

```css
/* Scoped to the header web component */
instant-apps-header{
  --calcite-color-text-1: #ffffff;
  --calcite-color-text-2: #e9ecef;
  --calcite-color-brand: #cf1a21;
  --calcite-color-brand-hover: #b3151b;
}

/* Or globally if needed across the app */
:root{
  --calcite-color-brand: #cf1a21;
}
```

Notes:
- Only variables wired by Instant Apps/Calcite at a given location will take effect. Prefer simple, high‑impact tokens (brand/text).
- Don’t assume component internals; verify in DevTools.


## Single‑Block CSS Design Pattern (Recommended Skeleton)

Use a consistent structure to keep single‑file CSS readable and maintainable:

1) Tokens (colors, motion, optional overlay logo)
2) Header module (backgrounds, padding via parts, overlay logo)
3) Tabs module (strip container, idle/hover/selected, focus)
4) Landing page (optional cover page styles)
5) Utilities (small helpers)
6) Client overrides (local tweaks at bottom)

Example skeleton:

```css
/* ================= 1) TOKENS ================= */
:root{
  --brand-primary: #cf1a21;
  --brand-primary-2: #8f0f14;
  --brand-gray-1: #181b1f;
  --brand-gray-2: #2a3036;
  --brand-gray-3: #565d66;
  --text-on-dark: #ffffff;
  --text-on-light: #0b0f0e;
  --app-header-gradient-speed: 14s;
  --tab-gradient-speed: 22s;
  /* Optional centered overlay logo */
  --overlay-logo-url: none; /* or url("https://.../logo.png") */
  --overlay-logo-width: clamp(260px, 36vw, 560px);
  --overlay-logo-height: min(64px, calc(var(--instant-apps-header-height, 56px) - 6px));
}

/* ================= 2) HEADER ================= */
instant-apps-header{
  background:
    linear-gradient(110deg,var(--brand-primary-2) 0%,var(--brand-primary) 18%,var(--brand-gray-2) 36%,var(--brand-gray-1) 100%),
    linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,.20) 40%,rgba(0,0,0,.50) 100%);
  background-size: 400% 400%,100% 100%;
  animation: appHeaderShift var(--app-header-gradient-speed) ease-in-out infinite;
  --calcite-color-text-1: var(--text-on-dark);
  --calcite-color-text-2: #e9ecef;
  --calcite-color-brand: var(--brand-primary);
  --calcite-color-brand-hover: #b3151b;
  position: relative; z-index: 0;
  box-shadow: inset 0 -1px 0 rgba(255,255,255,.10);
}
instant-apps-header::part(container),
instant-apps-header::part(wrapper){ background: transparent !important; padding-inline: 16px !important; }
instant-apps-header::after{ /* centered overlay logo (optional) */
  content: ""; position: absolute; inset: 50% auto auto 50%;
  width: var(--overlay-logo-width); height: var(--overlay-logo-height);
  transform: translate(-50%,-50%);
  background: var(--overlay-logo-url) no-repeat center / contain;
  pointer-events: none; z-index: 2; filter: drop-shadow(0 1px 0 rgba(0,0,0,.25));
}
@media (prefers-reduced-motion: reduce){ instant-apps-header{ animation: none; } }
@keyframes appHeaderShift{ 0%{background-position:0% 50%,0 0} 50%{background-position:100% 50%,0 0} 100%{background-position:0% 50%,0 0} }

/* ================= 3) TABS ================= */
#tabbedLayout .esri-portfolio-tabbed__tab-list{ background:#3a3f45; box-shadow: inset 0 -1px 0 rgba(0,0,0,.35); gap:6px; padding:8px 12px; }
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item{
  background: rgba(255,255,255,.06);
  color: var(--text-on-dark);
  border-radius: 6px;
  transition: background .2s ease, color .2s ease, box-shadow .2s ease;
}
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item:hover{ background: rgba(255,255,255,.12); box-shadow: 0 1px 6px rgba(0,0,0,.25); }
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item--selected,
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item--selected:hover{
  background:
    linear-gradient(135deg,var(--brand-primary-2) 0%,var(--brand-primary) 42%,var(--brand-gray-3) 70%,var(--brand-gray-2) 100%),
    linear-gradient(180deg,rgba(255,255,255,.05) 0%,rgba(0,0,0,.14) 100%) !important;
  background-size: 220% 220%,100% 100%;
  animation: tabRedShift var(--tab-gradient-speed) ease-in-out infinite;
  color: #ffffff !important; text-shadow: 0 1px 0 rgba(0,0,0,.4);
  box-shadow: 0 0 0 1px rgba(0,0,0,.25) inset, 0 2px 10px rgba(227,28,36,.22);
}
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item:focus-visible{ outline:2px solid var(--brand-primary); outline-offset:2px; }
@keyframes tabRedShift{ 0%{background-position:0% 50%,0 0} 50%{background-position:100% 50%,0 0} 100%{background-position:0% 50%,0 0} }

/* ================= 4) LANDING PAGE ================= */
instant-apps-landing-page{
  --instant-apps-landing-page-text-color: #ffffff !important;
  --instant-apps-landing-page-entry-button-color: #cf1a21 !important; /* safe fallback */
}
instant-apps-landing-page::part(container){ backdrop-filter: saturate(1.05) contrast(1.05); }
instant-apps-landing-page calcite-button{ /* gradient host */
  background: linear-gradient(135deg,#cf1a21 0%,#b3151b 50%,#8f0f14 100%) !important;
  background-size: 220% 220% !important;
  animation: enterShift 10s ease-in-out infinite;
  border: 1px solid rgba(11,15,14,.65) !important;
  box-shadow: 0 0 0 1px rgba(0,0,0,.25) inset, 0 6px 18px rgba(227,28,36,.25), 0 1px 0 rgba(255,255,255,.35) inset !important;
  color: #0b0f0e !important; border-radius: 8px !important; overflow: hidden;
}
instant-apps-landing-page calcite-button::part(button){ background: transparent !important; color: #0b0f0e !important; }
instant-apps-landing-page calcite-button:hover{ background-position: 100% 50% !important; }
instant-apps-landing-page calcite-button:focus-visible{ outline: 2px solid #3aa154; outline-offset: 2px; }
@keyframes enterShift{ 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }

/* ================= 5) UTILITIES ================= */
.text-on-dark{ color: var(--text-on-dark) !important; }
.text-on-light{ color: var(--text-on-light) !important; }
```


## Embedding Other Apps (Scenes, Maps): Minimizing Their UI

- Scene Viewer: Prefer `ui=min` to reduce headers and chrome when embedding as a Web Page section.
  - Example: `https://www.arcgis.com/home/webscene/viewer.html?webscene=ITEMID&ui=min`
- Map Viewer/others: Use each app’s documented URL parameters where available to reduce toolbars. If no official parameters exist, accept that embedded UI remains visible.
- CSS cannot style inside iframes; keep Portfolio surroundings visually consistent to avoid the “double header” look.


## Accessibility and Inclusive Motion

- Keep focus styles: use `:focus-visible` outlines that meet contrast guidance.
- Contrast: ensure text over gradients meets AA contrast (especially selected tabs and header title). Add subtle `text-shadow` for readability on photos.
- Motion: honor `prefers-reduced-motion` and disable long‑running gradients when requested.
- Hit targets: avoid shrinking tab padding; maintain sufficient spacing.


## Reliability, Specificity, and Maintenance

- Specificity: Target the smallest stable hook. Prefix with `#tabbedLayout` when styling tabs to avoid collisions. Prefer class selectors over tag selectors.
- `!important`: Use sparingly; it’s often needed when overriding component defaults, but keep it limited to critical cases (e.g., selected tab background).
- Shadow DOM boundaries: You can only style exposed `::part(...)` names and CSS variables. Don’t rely on internal element structure within web components.
- Releases: Instant Apps and Calcite change monthly in ArcGIS Online. Re‑test client apps after releases and keep a short “local overrides” section at the end of each client CSS for easy diffs.
- CSP/external CSS: Do not rely on `@import` external stylesheets. Host only images (logos) and reference them with `url(...)`.


## New Client Workflow (Checklist)

- Create folders under `clients/<client>/` with `css/single_block`, `css/modular`, `.esri-url`, and `logos` as needed.
- Copy `.master/template.css` as a starting point; either keep modular or merge into a single‑block CSS for the Portfolio app.
- Fill `:root` tokens with brand colors and motion preferences.
- Decide on header logo approach: native left logo (recommended) vs. centered overlay (`instant-apps-header::after`). Host the overlay image externally if used.
- Style tabs: base, hover, selected, focus. Maintain accessible outlines and contrast.
- If using a Cover page, set text and button colors; style the entry button on the host and make the internal button part transparent.
- Add `.url` links in `.esri-url/` to the target builder or published app for quick access.
- QA: desktop, tablet width, narrow phones; test focus, animation preferences, and embedded content alignment. Validate after Instant Apps monthly updates.


## Troubleshooting Guide

- “My header text won’t change color”: Move Calcite color variables to the closest component scope (`instant-apps-header`) and verify tokens: `--calcite-color-text-1`, `--calcite-color-text-2`.
- “The logo overlays clickable UI”: Ensure `pointer-events: none` on the overlay logo and avoid high `z-index` that floats above dropdowns.
- “Tabs look fine but flicker on hover”: Include the selected + hover compound selector to avoid visual transitions on the active pill: `.esri-portfolio-tabbed-item--selected, .esri-portfolio-tabbed-item--selected:hover { ... }`.
- “White bar above the scene cannot be styled”: That’s the embedded app’s own header. Use URL parameters (`ui=min`) or accept it.
- “My button gradient gets clipped”: Apply gradient to the host element and make the internal Calcite part transparent via `::part(button)`.


## References (Official)

- Change Theme & Layout (Custom CSS caution)
  - https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm
- Portfolio template overview (Instant Apps)
  - https://doc.arcgis.com/en/instant-apps/latest/create-apps/portfolio.htm
- Select content / add sections (embed images, PDFs, web pages)
  - https://doc.arcgis.com/en/instant-apps/latest/customize/content-settings.htm
- Scene Viewer URL parameters (use `ui=min`)
  - https://doc.arcgis.com/en/arcgis-online/reference/use-url-parameters-scenes.htm
- Instant Apps customization & Calcite variables
  - https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/introduction-arcgis-instant-apps/
  - https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/calcite-variables/


## References (General Calcite Design System)

- Calcite Design System (foundations, tokens, components):
  - https://developers.arcgis.com/calcite-design-system/


## Appendix: Selector Map (Quick Copy)

```css
/* Header */
instant-apps-header{}
instant-apps-header::part(container){}
instant-apps-header::part(wrapper){}
instant-apps-header::part(title){}
instant-apps-header::part(logo){}
instant-apps-header::after{}

/* Tabs */
#tabbedLayout .esri-portfolio-tabbed__tab-list{}
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item{}
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item:hover{}
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item--selected{}
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item:focus-visible{}

/* Cover page */
instant-apps-landing-page{}
instant-apps-landing-page::part(container){}
instant-apps-landing-page calcite-button{}
instant-apps-landing-page calcite-button::part(button){}
```


# ArcGIS Instant Apps - Imagery Viewer CSS: Expert Context

Purpose: a single reference for creating and maintaining single-block custom CSS for ArcGIS Instant Apps "Imagery Viewer", with the selector map, Calcite variable guidance, and the DOM hooks validated against a live published app.


## What You Can and Cannot Style

- Scope you control: the Imagery Viewer app shell, its HTML header, Calcite panels and controls, Esri map widgets, and the compare swipe handle. These are all in the app DOM and can be targeted directly.
- Scope you cannot control: the imagery service content itself, internal map rendering, or any third-party iframe content that might be embedded elsewhere.
- Runtime: Custom CSS is injected as a single text block in the builder. Keep it as one file, avoid `@import`, and host logos externally if you use a custom image.


## Core Components and Selectors

Imagery Viewer does not use the Portfolio `instant-apps-header` or `#tabbedLayout` selectors. The most useful hooks are:

- App shell
  - `#appContainer.calcite-shell-container.header`
  - `calcite-shell`
- Header
  - `.embed-app__header`
  - `.embed-app__header__title-area`
  - `.embed-app__header__title-area h1`
  - `img.embed-app__header__logo` (when a native custom logo is configured)
  - `.embed-image-date`
- Viewer panels and tools
  - `calcite-panel.imagery-doubleviewer`
  - `calcite-panel.imagery-singleviewer`
  - `calcite-panel.imagery-export`
  - `.imagery-imagemeasurement`
  - `.imagery-measureclear`
- Calcite controls inside the panels
  - `calcite-accordion-item`
  - `calcite-select`
  - `calcite-button`
  - `calcite-action.esri-widget--button`
  - `calcite-segmented-control`
- Compare control
  - `.esri-swipe__container`
  - `.esri-swipe__handle`
  - `.esri-swipe__divider`
- Map chrome that often needs visual alignment
  - `.esri-view-attribution`
  - `.esri-ui`


## What The Live App Ships Today

The published Imagery Viewer CSS currently includes these structural patterns:

- `.embed-app__header` is a plain HTML `header`, not an Instant Apps web component.
- The title area is `.embed-app__header__title-area`, and native logos render as `img.embed-app__header__logo`.
- The built-in logo scale classes set square logo sizes:
  - `.logo-scale-s` -> `35px`
  - `.logo-scale-m` -> `50px`
  - `.logo-scale-l` -> `60px`
- The header heights are:
  - `.embed-app__header.logo-scale-s` -> `55px`
  - `.embed-app__header.logo-scale-m` -> `70px`
  - `.embed-app__header.logo-scale-l` -> `80px`
- The imagery control panel classes are `.imagery-export`, `.imagery-singleviewer`, and `.imagery-doubleviewer`.
- The compare slider is not a Calcite slider. It is the Esri swipe widget using `.esri-swipe__container`, `.esri-swipe__handle`, and `.esri-swipe__divider`.


## Calcite Variables (Best Place To Theme)

Set Calcite tokens at the shell level so nested controls inherit the theme:

```css
#appContainer.calcite-shell-container.header,
#appContainer.calcite-shell-container.header calcite-shell,
#appContainer.calcite-shell-container.header calcite-panel,
#appContainer.calcite-shell-container.header calcite-select,
#appContainer.calcite-shell-container.header calcite-button,
#appContainer.calcite-shell-container.header calcite-action,
#appContainer.calcite-shell-container.header calcite-segmented-control{
  --calcite-color-brand: #314dec;
  --calcite-color-brand-hover: #314dec;
  --calcite-color-brand-press: #0a3d91;
  --calcite-color-background: #1a1a1a;
  --calcite-color-background-alt: #2a2a2a;
  --calcite-color-text-1: #ffffff;
  --calcite-color-text-2: #b3b3b3;
  --calcite-color-focus: #314dec;
}
```

Use shell-level tokens for the shared look, then layer component selectors only where the app needs structural overrides.


## Single-Block CSS Design Pattern

Recommended structure for an Imagery Viewer single-block stylesheet:

1. Tokens (brand colors, motion, optional logo URL and sizing)
2. Shared Calcite variables at `#appContainer`
3. Header module (`.embed-app__header`, title area, optional native logo compatibility)
4. Panels and accordion module
5. Calcite controls module
6. Compare swipe module
7. Utilities or client overrides

The logo pattern that worked in live testing:

- Use `.embed-app__header__title-area::before` for a CSS-hosted fallback logo.
- Add left padding to `.embed-app__header__title-area` to reserve space.
- Zero out the shipped `h1` left margin so title spacing is controlled by your padding.
- If the app later enables a native `img.embed-app__header__logo`, restyle it to a wide logo and hide the pseudo-logo only when the image exists.


## Accessibility And Inclusive Motion

- Preserve a visible focus treatment on the swipe handle and interactive controls.
- Keep white text over dark gradients and add a subtle text shadow on the header title when needed.
- Honor `prefers-reduced-motion` for animated header gradients.
- Do not reduce the compare handle hit area; style it without shrinking it.


## Reliability And Maintenance

- Prefer the confirmed app selectors above instead of Portfolio selectors.
- Use `!important` only when fighting shipped backgrounds or component defaults.
- Re-test after ArcGIS Online updates. Instant Apps and Calcite change frequently.
- If a selector stops working, inspect the live app again before expanding specificity.


## Troubleshooting Guide

- "My CSS still does nothing": you are probably still targeting Portfolio selectors such as `instant-apps-header` or `#tabbedLayout`.
- "The logo is duplicated": a native custom logo is enabled and your pseudo-logo is still active. Use the `:has(img.embed-app__header__logo)` pattern to suppress the pseudo fallback.
- "The native logo is squashed": override `img.embed-app__header__logo` width and height because the app ships square logo sizing by default.
- "The compare handle did not change": target `.esri-swipe__handle` and `.esri-swipe__divider`, not `calcite-slider`.
- "The panel theme is inconsistent": move more of the Calcite color tokens to the shell level instead of styling each control independently.


## New Client Workflow (Imagery Viewer)

- Create the normal client folder structure under `clients/<client>/`.
- Start from `.master/Imagery Viewer/template.css` or `.master/Imagery Viewer/single_block_starter.css`.
- Update the token block first.
- Choose whether the header logo will come from a CSS fallback, a native custom logo, or both.
- Test in the published Imagery Viewer app with browser DevTools before copying into the Instant Apps builder.


## References (Official)

- Change Theme and Layout
  - https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm
- Imagery Viewer template overview
  - https://doc.arcgis.com/en/instant-apps/12.0/create-apps/imagery-viewer.htm
- Instant Apps capabilities matrix
  - https://doc.arcgis.com/en/instant-apps/latest/customize/pdf/arcgis-instant-apps-matrix.pdf
- Instant Apps and Calcite variables
  - https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/calcite-variables/


## Appendix: Selector Map (Quick Copy)

```css
/* App shell */
#appContainer.calcite-shell-container.header{}

/* Header */
.embed-app__header{}
.embed-app__header .embed-app__header__title-area{}
.embed-app__header .embed-app__header__title-area::before{}
.embed-app__header .embed-app__header__title-area h1{}
.embed-app__header .embed-app__header__logo{}
.embed-app__header .embed-image-date{}

/* Panels */
calcite-panel.imagery-doubleviewer{}
calcite-panel.imagery-singleviewer{}
calcite-panel.imagery-export{}
.imagery-imagemeasurement{}
.imagery-measureclear{}

/* Calcite controls */
calcite-accordion-item{}
calcite-accordion-item::part(header){}
calcite-select{}
calcite-button{}
calcite-action.esri-widget--button{}
calcite-segmented-control{}

/* Compare control */
.esri-swipe__container{}
.esri-swipe__handle{}
.esri-swipe__divider{}
```

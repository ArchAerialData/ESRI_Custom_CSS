# Portfolio-Only Template Guide

This document is intentionally limited to the ArcGIS Instant Apps `Portfolio` template, especially the `Tabbed` layout. It is not a repo-wide selector guide for every Instant Apps app type.

For the full `.master` template index and validation tiers, see `.master/README.md`.

## Canonical Portfolio References

- Portfolio selector map and expert guidance: `.master/Portfolio/context.md`
- Portfolio modular starter: `.master/Portfolio/template.css`
- Portfolio single-block starter: `.master/Portfolio/single_block_starter.css`

## Official Sources

- Portfolio template overview:
  `https://doc.arcgis.com/en/instant-apps/latest/create-apps/portfolio.htm`
- Change Theme and Layout:
  `https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm`
- Content settings for embedded web pages:
  `https://doc.arcgis.com/en/instant-apps/latest/customize/content-settings.htm`
- Scene Viewer URL parameters:
  `https://doc.arcgis.com/en/arcgis-online/reference/use-url-parameters-scenes.htm`
- Calcite variables in Instant Apps:
  `https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/calcite-variables/`

## Portfolio Selector Map

Header:

```css
instant-apps-header
instant-apps-header::part(container)
instant-apps-header::part(wrapper)
instant-apps-header::part(title)
instant-apps-header::part(logo)
instant-apps-header::after
```

Tabbed layout:

```css
#tabbedLayout .esri-portfolio-tabbed__tab-list
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item:hover
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item--selected
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item:focus-visible
```

Cover page:

```css
instant-apps-landing-page
instant-apps-landing-page::part(container)
instant-apps-landing-page calcite-button
instant-apps-landing-page calcite-button::part(button)
```

## What Portfolio CSS Can And Cannot Reach

- You can style the Portfolio app shell, the header web component, exposed header parts, the tab strip, the tab items, and the landing page component.
- You cannot style the inside of embedded iframes such as Scene Viewer, Map Viewer, Experience Builder, or other third-party pages.
- If an embedded app shows too much UI, use its supported URL parameters instead of trying to pierce the iframe with CSS.

Example for embedded Scene Viewer:

```text
https://www.arcgis.com/home/webscene/viewer.html?webscene=ITEMID&ui=min
```

## Practical Guidance

- Start new Portfolio clients from `.master/Portfolio/`, not from another app family.
- Keep `:root` brand tokens at the top of the stylesheet.
- Scope tab rules to `#tabbedLayout` to avoid accidental collisions.
- Preserve `:focus-visible` outlines and `prefers-reduced-motion` handling.
- Re-test after ArcGIS Online releases because Instant Apps selectors can shift.

## Use The Right Family

- If the app is `Portfolio`, use `.master/Portfolio/`.
- If the app is `Imagery Viewer`, use `.master/Imagery Viewer/`.
- For any other supported app, use the matching `.master/<Instant App Name>/` starter and validate selectors in browser DevTools before adding structural overrides.

# ArcGIS Instant Apps - Slider CSS Context

Validation tier: Starter / pending live DOM validation
Custom CSS: Yes

## Official references

- Template overview: https://doc.arcgis.com/en/instant-apps/latest/create-apps/slider.htm
- Instant Apps capabilities matrix: https://doc.arcgis.com/en/instant-apps/latest/customize/pdf/arcgis-instant-apps-matrix.pdf
- Change Theme and Layout: https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm
- Calcite variables in Instant Apps: https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/calcite-variables/

## What this folder is

This folder is a conservative starter for the Slider template because this repo has not yet live-inspected this app's DOM.
Use the CSS files here as a low-risk theming base only.

## What the starter assumes

- Use only broad Instant Apps and Calcite hooks first.
- Do not assume app-internal structure until it has been validated in browser DevTools.
- Extend the template only after checking the live DOM for header, panels, cards, charts, lists, map widgets, and any template-specific controls.

## Safe hooks included in the starter CSS

- instant-apps-header
- instant-apps-social-share
- calcite-shell
- calcite-panel
- calcite-button
- calcite-action
- calcite-select
- calcite-segmented-control
- .esri-ui
- .esri-view-attribution

## Next validation step

Inspect a live Slider app and capture the real selector map before adding any app-specific structural overrides.
# `.master` Template Families

This folder contains reusable ArcGIS Instant Apps custom CSS starter families.

Source of truth for support:
- ArcGIS Instant Apps capabilities matrix: https://doc.arcgis.com/en/instant-apps/latest/customize/pdf/arcgis-instant-apps-matrix.pdf

Folder contract for each app family:
- `.master/<Instant App Name>/context.md`
- `.master/<Instant App Name>/template.css`
- `.master/<Instant App Name>/single_block_starter.css`

## Validation Tiers

### Validated

- `Portfolio`
- `Imagery Viewer`

These families have repo-grounded selector guidance and live-tested structural hooks.

### Starter / pending live DOM validation

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

These folders are conservative theming starters only. They intentionally avoid app-internal structural selectors until the live DOM is inspected and documented.

## Exclusions

Templates not listed here are intentionally excluded because the current official matrix does not indicate Custom CSS support for them.

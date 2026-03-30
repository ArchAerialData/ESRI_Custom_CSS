# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository maintains client-specific custom CSS and assets for ArcGIS Instant Apps experiences. It includes reusable `.master` template families for every Instant Apps template that officially supports Custom CSS, with validated guidance for Portfolio (Tabbed) and Imagery Viewer plus starter families for the rest.

## Repository Architecture

The repository follows a structured approach to CSS organization:

- **Templates System**: `.master/` contains reusable CSS templates and documentation organized by Instant Apps template family
- **Client-Specific Organization**: Each client has their own folder under `clients/` with both modular and single-block CSS approaches
- **Dual CSS Approaches**:
  - **Modular**: Split CSS by component areas for better maintainability
  - **Single-block**: Self-contained CSS files for easy copy-paste into ArcGIS Instant Apps

### Key Template Files

- `.master/README.md`: Index of all supported Instant Apps template families and validation tiers
- `.master/Portfolio/template.css`: Modular starter for Portfolio (Tabbed)
- `.master/Portfolio/context.md`: Expert-level documentation for Portfolio selectors and constraints
- `.master/Imagery Viewer/template.css`: Modular starter for Imagery Viewer
- `.master/Imagery Viewer/context.md`: Expert-level documentation for Imagery Viewer selectors and constraints
- `docs/README_template.md`: Portfolio-only selector map and guidance

### Supported Template Families

- **Validated**: `Portfolio`, `Imagery Viewer`
- **Starter / pending live DOM validation**: `3D Viewer`, `Atlas`, `Attachment Viewer`, `Basic (Media Map)`, `Category Gallery`, `Chart Viewer`, `Interactive Legend`, `Nearby`, `Public Notification`, `Reporter`, `Sidebar`, `Slider`, `Zone Lookup`

If the target app type is not listed in `.master/README.md`, do not assume this repo has a supported custom-CSS starter for it.

## CSS Architecture

The CSS templates follow a specific modular structure:

1. **Brand Tokens** (`:root` variables for colors, motion, logo settings)
2. **Header Module** (template-specific header styling)
3. **Primary UI Module** (tabs for Portfolio, panels and compare controls for Imagery Viewer)
4. **Optional Landing/Cover Styling**
5. **Utilities** (helper classes)
6. **Client Overrides** (project-specific tweaks)

### Key Selectors

- Portfolio header: `instant-apps-header` and its shadow parts (`::part(container)`, `::part(wrapper)`)
- Portfolio tabs: `#tabbedLayout .esri-portfolio-tabbed__tab-list` and `.esri-portfolio-tabbed-item` variants
- Imagery Viewer header: `.embed-app__header` and `.embed-app__header__title-area`
- Imagery Viewer compare control: `.esri-swipe__container`, `.esri-swipe__handle`, `.esri-swipe__divider`

## Working with Client CSS

### Adding a New Client

1. Create folder structure: `clients/<client>/{.esri-url, css/{single_block,modular}, logos/}`
2. Copy the appropriate starter from the matching `.master/<Instant App Name>/` family
3. Update `:root` brand tokens (colors, motion preferences)
4. Configure optional logo handling for the app type
5. Add app shortcuts in `.esri-url/` folder

### CSS Constraints and Best Practices

- **Scope Limitations**: Custom CSS only affects the Instant Apps shell, not embedded iframe content
- **Embedded Apps**: Use URL parameters (for example `ui=min` for Scene Viewer) to minimize embedded app UI
- **Selector Stability**: Prefer the template-specific selectors documented in the matching `.master/<template>/context.md`
- **Accessibility**: Preserve focus styles and contrast ratios; respect `prefers-reduced-motion`
- **Maintenance**: Re-test after ArcGIS Online releases (monthly updates can affect selectors)

## File Organization Patterns

- `.esri-url/*.url`: App shortcuts for quick access to client apps
- `css/single_block/*.css`: Complete self-contained CSS files
- `css/modular/*.css`: Component-split CSS files (for example `header.css`, `sidebar.css`, `cover.css`)
- `logos/`: Client brand assets referenced by CSS

## Development Workflow

This is a CSS-only repository with no build system. Development involves:

1. Editing CSS files directly
2. Testing changes by copying CSS into the matching ArcGIS Instant Apps builder
3. Using browser DevTools to inspect selectors and test responsiveness
4. Validating across desktop, tablet, and mobile breakpoints

## Important Notes

- No package.json, build tools, or compilation steps - pure CSS repository
- External image hosting required for logos when not using a native app logo
- Keep client overrides at bottom of CSS files for easier template updates
- Use Calcite Design System variables at component boundaries for consistent theming

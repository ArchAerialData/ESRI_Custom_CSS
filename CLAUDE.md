# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository maintains client-specific custom CSS and assets for ArcGIS Instant Apps "Portfolio (Tabbed)" experiences. It provides a modular template system to standardize brand tokens, header styles, and tab behaviors across different clients.

## Repository Architecture

The repository follows a structured approach to CSS organization:

- **Templates System**: `.master/` contains reusable CSS templates and documentation that serve as starting points for new clients
- **Client-Specific Organization**: Each client has their own folder under `clients/` with both modular and single-block CSS approaches
- **Dual CSS Approaches**:
  - **Modular**: Split CSS by component areas (header, tabs, cover) for better maintainability
  - **Single-block**: Self-contained CSS files for easy copy-paste into ArcGIS Instant Apps

### Key Template Files

- `.master/template.css`: The main modular CSS starter with brand tokens, header, and tab styling
- `.master/context.md`: Expert-level documentation with detailed selector maps and CSS constraints
- `docs/README_template.md`: Selector map and guidance for Portfolio (Tabbed) styling

## CSS Architecture

The CSS follows a specific modular structure:

1. **Brand Tokens** (`:root` variables for colors, motion, logo settings)
2. **Header Module** (instant-apps-header styling with optional overlay logo)
3. **Tabs Module** (tab strip, inactive/hover/selected states, focus styles)
4. **Landing Page** (optional cover page styling)
5. **Utilities** (helper classes)
6. **Client Overrides** (project-specific tweaks)

### Key Selectors

- Header: `instant-apps-header` and its shadow parts (`::part(container)`, `::part(wrapper)`)
- Tabs: `#tabbedLayout .esri-portfolio-tabbed__tab-list` and `.esri-portfolio-tabbed-item` variants
- Cover page: `instant-apps-landing-page` and embedded `calcite-button` styling

## Working with Client CSS

### Adding a New Client

1. Create folder structure: `clients/<client>/{.esri-url, css/{single_block,modular}, logos/}`
2. Copy `.master/template.css` as starting point
3. Update `:root` brand tokens (colors, motion preferences)
4. Configure optional overlay logo via `--overlay-logo-url` variable
5. Add app shortcuts in `.esri-url/` folder

### CSS Constraints and Best Practices

- **Scope Limitations**: Custom CSS only affects the Portfolio app shell, not embedded iframe content
- **Embedded Apps**: Use URL parameters (e.g., `ui=min` for Scene Viewer) to minimize embedded app UI
- **Selector Stability**: Prefix tab selectors with `#tabbedLayout` to avoid collisions
- **Accessibility**: Preserve focus styles and contrast ratios; respect `prefers-reduced-motion`
- **Maintenance**: Re-test after ArcGIS Online releases (monthly updates can affect selectors)

## File Organization Patterns

- `.esri-url/*.url`: App shortcuts for quick access to client Portfolio apps
- `css/single_block/*.css`: Complete self-contained CSS files
- `css/modular/*.css`: Component-split CSS files (header.css, sidebar.css, cover.css)
- `logos/`: Client brand assets referenced by CSS

## Development Workflow

This is a CSS-only repository with no build system. Development involves:

1. Editing CSS files directly
2. Testing changes by copying CSS into ArcGIS Instant Apps Portfolio builder
3. Using browser DevTools to inspect selectors and test responsiveness
4. Validating across desktop, tablet, and mobile breakpoints

## Important Notes

- No package.json, build tools, or compilation steps - pure CSS repository
- External image hosting required for logos (no file uploads in Instant Apps)
- Keep client overrides at bottom of CSS files for easier template updates
- Use Calcite Design System variables at component boundaries for consistent theming
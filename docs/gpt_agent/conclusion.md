## Portfolio CSS — Agent Findings And Adaptations

This summarizes new insights from the agent’s PDF/DOCX review and proposes concrete adaptations to our template and guidance. It focuses on elements not already covered in our `context.md` and master templates, plus areas where our approach can be tightened.


### Newly Identified Elements/Behaviors

- Cover Page Title/Subtitle classes: The compiled CSS uses `.esri-page__title-text` and `.esri-page__subtitle-text` with responsive breakpoints (≈480px, 768px). Both get text shadows for legibility. These selectors are safe to override for size, alignment, and readability.
- Additional layouts beyond Tabbed: Portfolio supports Carousel and Accordion (`.esri-portfolio-carousel`, `.esri-portfolio-accordion`) with analogous navigation containers. The same theming strategy applies; keep selectors scoped and avoid structural overrides.
- Stage/description internals: `.esri-portfolio-stage` and `.esri-portfolio-description` rely on absolute positioning and height calculations (e.g., `calc(100% - headerHeight)`). Structural overrides here risk clipping/overlap. Prefer visual-only changes (colors/shadows/typography) and margin-top nudges near the tab strip.
- Theme modes: The app toggles between `body.calcite-mode-light` and `body.calcite-mode-dark`. Provide complementary color tokens or scoped overrides for both modes to preserve contrast and readability.
- Calcite variables breadth: In addition to brand and text tokens, many components honor `--calcite-font-size-*`, `--calcite-radius-*`, and `--calcite-color-*`. Scoped use at `instant-apps-header` (and other containers) influences nested Calcite UI consistently.
- Landing page button fallback: Older builds render an anchor `.landing-page__entry-button` instead of `calcite-button`. Styling both ensures consistency across versions.
- High-count/long tab labels: With many items or long titles, ensure the tab strip allows overflow and avoids clipping. Use `overflow: visible` on the tab containers and avoid fixed widths. Test at narrow/mobile widths.


### Gaps To Address In Our Docs/Template

- Cover Title/Subtitle section: Add a short recipe to adjust title/subtitle size, alignment, and optional text-shadow for readability over images.
- Theme mode notes: Explain `calcite-mode-light` vs `calcite-mode-dark` and include a minimal example of complementary overrides to keep contrast high in both.
- Multi-layout callouts: Document Carousel/Accordion selector names and note they follow the same patterns as Tabbed for idle/hover/selected/focus states.
- Structural caution box: Explicitly call out that `.esri-portfolio-stage` and `.esri-portfolio-description` (and some wrappers) are position/height-driven and should not be structurally altered by custom CSS.
- Tab strip crowding guidance: Provide optional snippets to reduce bar/pill height and add a small content offset below the strip to avoid collisions with embedded content.
- Legacy landing button fallback: Add the `.landing-page__entry-button` styling to the template (in addition to `calcite-button::part(button)`).

### Recommended Adaptations (Actionable)

- Template cover page additions
  - Add optional overrides:
    - `.esri-page__title-text { font-size: clamp(2rem, 4vw, 3rem); text-align: center; text-shadow: 0 2px 8px rgba(0,0,0,.35); }`
    - `.esri-page__subtitle-text { font-size: clamp(1rem, 2.5vw, 1.5rem); }`
  - Keep existing `calcite-button` host-gradient pattern; add the fallback for `.landing-page__entry-button`.

- Theme mode scaffolding
  - In the template, add a commented block:
    - `body.calcite-mode-light { /* light-mode adjustments */ }`
    - `body.calcite-mode-dark  { /* dark-mode adjustments  */ }`
  - Document when to scope Calcite tokens globally (`:root`) vs locally (e.g., `instant-apps-header`).

- Tab strip resilience
  - Keep `overflow: visible` on tab containers; add optional pill padding/strip padding reductions for tight spaces.
  - Provide an optional content offset snippet: `#tabbedLayout [class*="esri-portfolio-tabbed__content"], ... { margin-top: 4px !important; }` for builds where stage and tabs visually collide.

- Multi-layout selector map (docs-only)
  - Add quick references for:
    - Carousel: `.esri-portfolio-carousel`, `.esri-portfolio-carousel__item`, `--selected`, `:hover`
    - Accordion: `.esri-portfolio-accordion`, `.esri-portfolio-accordion__item`, `--selected`, `:hover`
  - Mirror the same color/hover/selected/focus patterns from Tabbed.

- Calcite variables guidance
  - Extend docs to include examples of `--calcite-font-size-*` (e.g., tighten/loosen typography globally) and `--calcite-radius-*` (button/pill radii) to align with brand language.


### Rationale And Impact

- Consistency: Theme-mode guidance and fallback button styling avoid regressions across app updates and configurations.
- Maintainability: Structural caution reduces breakage from upstream layout changes; tab strip resilience helps when item counts grow.
- Accessibility: Title/subtitle readability, focus outlines, and mode-aware contrast improve UX for all users.


### Next Steps (Optional)

- Patch `.master/template.css` with:
  - Cover title/subtitle block and legacy button fallback.
  - Commented light/dark mode overrides.
  - Optional tab strip “tight spacing” and content offset snippets (commented).
- Update `context.md` with:
  - Multi-layout (Carousel/Accordion) selector map and do/don’t list.
  - Expanded Calcite variable examples (`font-size`, `radius`).
  - Theme mode notes and testing checklist for long titles/many tabs.

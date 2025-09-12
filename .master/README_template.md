# Instant Apps (Portfolio – Tabbed) CSS: Selector Map & Template

## Sources (official & primary)
- **Change Theme & Layout (Custom CSS caution)** — https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm  
- **Portfolio template overview (ArcGIS Online)** — https://doc.arcgis.com/en/instant-apps/latest/create-apps/portfolio.htm  
- **Select content / add sections (embed images, PDFs, *web pages*)** — https://doc.arcgis.com/en/instant-apps/latest/customize/content-settings.htm  
- **Scene Viewer URL parameters (`ui=min`)** — https://doc.arcgis.com/en/arcgis-online/reference/use-url-parameters-scenes.htm  
- **Instant Apps customization & Calcite variables** — https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/introduction-arcgis-instant-apps/  
- **Calcite variables in Instant Apps (examples of custom CSS)** — https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/calcite-variables/

> Tip: If you’re embedding Scene Viewer or Map Viewer into Portfolio as a **Web Page** section, use `ui=min` (and other URL params where applicable) to reduce embedded headers that Portfolio itself cannot style.

---

## Selector map for Portfolio (Tabbed)

### Tab strip & tabs (the green arrows in the screenshot)
- **Tab strip container (background / “blank space” behind tabs):**
  ```css
  #tabbedLayout .esri-portfolio-tabbed__tab-list
  ```

- **Tab (base/inactive):**
  ```css
  #tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item
  ```

- **Tab `:hover`:**
  ```css
  #tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item:hover
  ```

- **Tab active/selected:**
  ```css
  #tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item--selected
  /* I also include the hover variant to prevent flicker: */
  #tabbedLayout .esri-portfolio-tabbed__tab-list
    .esri-portfolio-tabbed-item--selected,
  #tabbedLayout .esri-portfolio-tabbed__tab-list
    .esri-portfolio-tabbed-item--selected:hover { … }
  ```

- **Tab focus (keyboard):**
  ```css
  #tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item:focus-visible
  ```

### Header (the red gradient band)
- **Whole header web component:**
  ```css
  instant-apps-header
  ```

- **Exposed shadow parts (when present):**
  ```css
  instant-apps-header::part(container),
  instant-apps-header::part(wrapper),
  instant-apps-header::part(title),
  instant-apps-header::part(logo)
  ```
  *We keep internal wrappers transparent and can pad here without touching the content.*

> ⚠️ **Custom CSS is supported but fragile.** Esri explicitly warns that template updates may affect apps using custom CSS. Test after each release (monthly for ArcGIS Online). See “Change theme and layout” docs above.

---

## Where to change what (quick recipes)

### 1) Hover colors for the tabs
```css
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item:hover{
  background: rgba(255,255,255,.12);
  color: #fff;            /* set if you want a different hover text color */
  box-shadow: 0 1px 6px rgba(0,0,0,.25);
}
```

### 2) Active tab styling (selected)
```css
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item--selected,
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item--selected:hover{
  /* gradient, text, shadow for the active pill */
}
```

### 3) Inactive tab styling (not hovered)
```css
#tabbedLayout .esri-portfolio-tabbed__tab-list .esri-portfolio-tabbed-item{
  /* base look for “everything that is not selected” */
}
/* Optional: strictly idle state (not selected and not hovered) */
#tabbedLayout .esri-portfolio-tabbed__tab-list
  .esri-portfolio-tabbed-item:not(.esri-portfolio-tabbed-item--selected):not(:hover){
  /* strictly idle styles */
}
```

### 4) Background / “blank space” behind the tabs
```css
#tabbedLayout .esri-portfolio-tabbed__tab-list{
  background: #3a3f45;        /* strip background */
  box-shadow: inset 0 -1px 0 rgba(0,0,0,.35);
  padding: 8px 12px;
  gap: 6px;
}
```

---

## Embedded app headers (white bar above the scene)

The white header above the map/scene is the **embedded app’s own header** (for example, **Scene Viewer**). Portfolio CSS cannot reach into that iframe due to cross‑origin isolation. To reduce or remove it, embed using a **Web Page** section and include Scene Viewer’s `ui=min` parameter in the URL.

Example:
```
https://www.arcgis.com/home/webscene/viewer.html?webscene=ITEMID&ui=min
```

This is the officially documented way to minimize Scene Viewer UI when embedding. (See the *Scene Viewer URL parameters* link at the top of this README.)

---

## Reusable template (modular)

This repo includes a clean, labeled **modular CSS template** for Portfolio (Tabbed) with:

- **Tokens block** (brand colors, motion)
- **Header module** (red→gray gradient, optional centered overlay logo)
- **Tabs module** (container background, inactive, hover, active, focus)
- **Optional cover page** stub (commented)
- **Small utility helpers**

Use it per project:
1. Set brand tokens in `:root`.
2. Decide if you want the **centered overlay header logo**; set `--overlay-logo-url` to a `url("…")` or `none`.
3. Tweak tab strip background and inactive/hover/selected rules.
4. (Optional) Uncomment the Cover Page block if you enable the Cover Page.

---

## Files in this package

- **instant_apps_portfolio_template.css** — modular CSS starter (Portfolio, Tabbed)  
- **README.md** — this document

---

## Versioning & maintenance

- Re‑test this CSS **after each ArcGIS Online release**. Minor changes in Instant Apps or Calcite component internals can invalidate selectors.  
- Keep a project “overrides” section at the bottom so template updates don’t stomp client‑specific tweaks.

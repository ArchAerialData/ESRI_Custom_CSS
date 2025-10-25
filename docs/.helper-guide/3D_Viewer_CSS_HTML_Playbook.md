# ArcGIS Instant Apps – 3D Viewer  
### Multi‑Model Strategy + Custom Header HTML & CSS Playbook

**Purpose:** Give your repo’s “ESRI Custom CSS & HTML” agent a practical, source‑linked foundation for building **3D Viewer** apps that (a) present *multiple 3D models* cleanly and (b) use **Custom header HTML** and **Custom CSS** safely and consistently.

---

## 0) Direct, official references (read these first)

- **3D Viewer — ArcGIS Instant Apps (latest docs):**  
  https://doc.arcgis.com/en/instant-apps/latest/create-apps/3d-viewer.htm

- **Supported HTML (sanitizer: allowed tags, attributes, protocols, and *inline‑CSS‑only* rule):**  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm

- **Theme & Layout → *Custom CSS* (and Esri’s caution about updates possibly affecting custom CSS):**  
  https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm

- **Customize a web app with CSS (step‑by‑step tutorial with safe selectors + Calcite variables):**  
  https://developers.arcgis.com/documentation/app-builders/no-code/tutorials/tools/customize-your-web-app-using-css/

- **Calcite variables in ArcGIS Instant Apps (design tokens for robust theming):**  
  https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/calcite-variables/

- **Include app & data details (shows *Custom header* setting among About options):**  
  https://doc.arcgis.com/en/instant-apps/latest/customize/about-settings.htm

- **Category Gallery (explicitly mentions “Custom header HTML” control—same control you see in 3D Viewer’s header panel):**  
  https://doc.arcgis.com/en/instant-apps/latest/create-apps/category-gallery.htm

- **Portfolio template (recommended when you truly need to host multiple scenes/apps together):**  
  https://doc.arcgis.com/en/instant-apps/latest/create-apps/portfolio.htm

- **Scene layers (what counts as a “3D model” in Esri land):**  
  https://doc.arcgis.com/en/arcgis-online/reference/scene-layers.htm

- **Add layers to scenes (authoring multiple models into one web scene):**  
  https://doc.arcgis.com/en/arcgis-online/create-maps/add-layers-to-scene.htm

- **Capture slides (bookmarks that also store layer visibility; includes URL syntax for opening a specific slide in Scene Viewer):**  
  https://doc.arcgis.com/en/arcgis-online/create-maps/capture-scene-slides.htm

---

## 1) Can 3D Viewer show *more than one* 3D model?

**Yes**, within the scope of a **single web scene**. 3D Viewer displays **one web scene** (see *Data requirements* on the 3D Viewer page). That scene can include **many 3D models** as separate **scene layers** (3D object, integrated mesh, building, point cloud, voxel). Enable **Layer list** so users can toggle models on/off, and use **Display preset slides** to jump among saved states (camera + layer visibility). The 3D Viewer docs also note a **URL parameter** to open the app at a specific slide.

- 3D Viewer overview & capabilities (“requires a web scene,” “Layer list,” “Display preset slides,” “URL parameter to open a specific slide”):  
  https://doc.arcgis.com/en/instant-apps/latest/create-apps/3d-viewer.htm
- Scene layer types supported in scenes (3D object, integrated mesh, building, point, point cloud, voxel):  
  https://doc.arcgis.com/en/arcgis-online/reference/scene-layers.htm
- Slides/bookmarks (store layer visibility and viewpoint; includes “open scene to slide” syntax for Scene Viewer):  
  https://doc.arcgis.com/en/arcgis-online/create-maps/capture-scene-slides.htm

> **When you truly need multiple scenes** (e.g., heavy meshes you don’t want co‑loaded), keep one scene per 3D Viewer app and aggregate the apps in a **Portfolio**:  
> https://doc.arcgis.com/en/instant-apps/latest/create-apps/portfolio.htm

---

## 2) Custom header HTML — what it can and cannot do

The **Custom header** toggle in 3D Viewer (About → App details) exposes a **Custom header HTML** editor. Esri’s sanitizer governs what you can put there.

### 2.1 Allowed
- **Standard HTML tags** and **attributes** listed in *Supported HTML* (e.g., `div`, `span`, headings, `img`, `a`, `nav`, etc.).  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm
- **Inline CSS only** via the `style` attribute (e.g., flexbox, grid, typography, spacing, colors listed on that page). External stylesheets are **not** allowed in this field.  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm
- **Link protocols**: `https`, `mailto:`, `tel:`. All links open in a **new tab**.  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm
- Great for **branding blocks** (logo + title), **nav links** back to Portfolio or help, **legal disclaimers**, and **contact** links.

### 2.2 Not allowed (sanitized out)
- `<script>`, `<iframe>`, `<link rel="stylesheet">`, and any **custom elements** not on the supported list.  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm
- **UNC paths** / `file://` links.  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm

> **Tip:** Some Instant Apps docs explicitly call the control **“Custom header HTML”** (e.g., Category Gallery). The 3D Viewer UI exposes the same capability in its **Custom header** panel.  
> Category Gallery: https://doc.arcgis.com/en/instant-apps/latest/create-apps/category-gallery.htm  
> About settings (shows *Custom header* availability): https://doc.arcgis.com/en/instant-apps/latest/customize/about-settings.htm

---

## 3) Custom CSS — the robust, maintainable way to brand

3D Viewer supports **Custom CSS** (Theme & Layout → Custom CSS). Esri recommends testing after each release because template updates can impact hand‑written CSS.

- Theme & Layout (Custom CSS + update caution):  
  https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm
- CSS tutorial with safe selectors and an **Esri‑blessed** example (`h3.esri-widget__heading`) using **Calcite** variables:  
  https://developers.arcgis.com/documentation/app-builders/no-code/tutorials/tools/customize-your-web-app-using-css/
- Calcite variables (design tokens for color, typography, spacing, etc.) to minimize brittle selectors:  
  https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/calcite-variables/

**Recommended approach**
1. Put **global branding** (typography, brand colors, spacing scale) in **Custom CSS** using **Calcite variables**.  
2. Keep the **header HTML** simple; use **inline styles** only for local layout (because the header field only allows inline CSS).  
3. Target **Esri/Calcite classes** sparingly and prefer design tokens over deep selectors.

---

## 4) Practical multi‑model patterns

### Pattern A — *One app, many models (toggle per layer)*
1. Publish each model as its own **scene layer** (3D object / integrated mesh / point cloud).  
   https://doc.arcgis.com/en/arcgis-online/reference/scene-layers.htm
2. Add all models to a **single web scene** and configure visibility/scale ranges.  
   https://doc.arcgis.com/en/arcgis-online/create-maps/add-layers-to-scene.htm
3. Author **slides** that store **viewpoint + layer visibility** (e.g., “Model A only”, “Model B only”, “A+B”).  
   https://doc.arcgis.com/en/arcgis-online/create-maps/capture-scene-slides.htm
4. In **3D Viewer**, enable **Layer list** and **Display preset slides**. (Docs also note a **URL parameter** to open to a specific slide.)  
   https://doc.arcgis.com/en/instant-apps/latest/create-apps/3d-viewer.htm

### Pattern B — *Multiple scenes/apps with navigation*
Use **Portfolio** to host multiple 3D Viewer apps (one per scene) and add **header links** inside each 3D Viewer to jump back to the Portfolio or to other apps.  
https://doc.arcgis.com/en/instant-apps/latest/create-apps/portfolio.htm

---

## 5) Copy‑paste scaffolds

> Paste **HTML** into **About → App details → Custom header HTML**.  
> Paste **CSS** into **Theme & Layout → Custom CSS** (global, not inline).

### 5.1 Header HTML (sanitizer‑safe, responsive)
```html
<!-- Lightweight, sanitizer-compliant header -->
<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 12px;">
  <div style="display:flex;align-items:center;gap:10px;">
    <img src="https://YOUR-CDN/logo.png" alt="Client Logo" width="28" height="28" style="border:0;">
    <span style="font-weight:600;font-size:16px;letter-spacing:0.2px;">
      3D Model Viewer – West Segment
    </span>
  </div>
  <nav style="display:flex;align-items:center;gap:16px;">
    <a href="https://your-portfolio-url.example.com">Back to Portfolio</a>
    <a href="mailto:support@yourco.com">Support</a>
    <a href="tel:+1-800-555-1234">Call</a>
  </nav>
</div>
```

### 5.2 Global Custom CSS (brand with Calcite variables first)
```css
/* 1) Establish brand tokens (safer than deep selectors) */
:root {
  --calcite-sans-family: "Inter", system-ui, Arial, sans-serif;
  --calcite-font-size-0: 1rem;           /* base body/heading size */
  --calcite-ui-brand: #0b5fff;           /* primary brand color */
  --calcite-ui-foreground-1: #1f1f1f;    /* primary text */
  --calcite-ui-background: #ffffff;      /* app background */
}

/* 2) Example from Esri’s CSS tutorial: soften widget headings */
h3.esri-widget__heading {
  font-family: var(--calcite-sans-family);
  font-size: var(--calcite-font-size-0);
}

/* 3) Optional: nudge panel typography & spacing */
.esri-component, .esri-widget, .esri-ui .esri-button {
  font-family: var(--calcite-sans-family);
}

/* 4) Optional: tighter spacing in layer list (be gentle with overrides) */
.esri-layer-list__item {
  padding-block: 0.25rem;
}
.esri-layer-list__item .esri-layer-list__item-title {
  letter-spacing: 0.1px;
}
```

### 5.3 Slides as “model presets” (authoring checklist)
- Create slides in **Scene Viewer** for each visibility preset (A only, B only, A+B, etc.).  
  https://doc.arcgis.com/en/arcgis-online/create-maps/capture-scene-slides.htm
- In 3D Viewer, enable **Display preset slides** so users can jump between presets.  
  https://doc.arcgis.com/en/instant-apps/latest/create-apps/3d-viewer.htm
- 3D Viewer supports a **URL parameter** to open the app to a specific slide (see its docs). For Scene Viewer, the syntax is `#<slide-number>`; test your 3D Viewer app’s parameter in your environment.  
  https://doc.arcgis.com/en/arcgis-online/create-maps/capture-scene-slides.htm

---

## 6) Do’s & Don’ts for the header HTML + CSS

**Do**  
- Keep header markup minimal; use **inline styles** there, but centralize theme work in **Custom CSS**.  
- Use `https`, `mailto:` and `tel:` links only; expect all anchors to open **in a new tab**.  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm  
- Prefer **Calcite variables** for colors and fonts; minimizes breakage after updates.  
  https://developers.arcgis.com/documentation/app-builders/no-code/arcgis-instant-apps/calcite-variables/  
- After each ArcGIS Online release, **smoke‑test** your CSS (Esri cautions that updates can affect overrides).  
  https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm

**Don’t**  
- Don’t add `<script>`, `<iframe>`, or external `<link rel="stylesheet">` in the header HTML (sanitized out).  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm  
- Don’t rely on brittle, deep selectors against internal widget DOM; prefer tokens and light‑touch class overrides.  
- Don’t co‑load *very heavy* meshes in one scene if performance suffers—use **Portfolio** and split into multiple apps.  
  https://doc.arcgis.com/en/instant-apps/latest/create-apps/portfolio.htm

---

## 7) Quick authoring checklist for “one app, many models”

1. **Publish** each model as its own **scene layer** (SLPK or from Pro).  
   https://doc.arcgis.com/en/arcgis-online/reference/scene-layers.htm  
2. **Assemble** one **web scene** with all models and save **slides** for visibility presets.  
   https://doc.arcgis.com/en/arcgis-online/create-maps/add-layers-to-scene.htm  
   https://doc.arcgis.com/en/arcgis-online/create-maps/capture-scene-slides.htm  
3. **Configure** 3D Viewer: enable **Layer list**, **Display preset slides**, and (optionally) set your custom **URL parameter** for a default slide.  
   https://doc.arcgis.com/en/instant-apps/latest/create-apps/3d-viewer.htm  
4. **Brand** with **Custom CSS** (global) + light **Custom header HTML** (logo + nav).  
   https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm  
   https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm  

---

## 8) Troubleshooting cues

- **Header looks “unstyled.”** That’s by design—the header field is a blank slate; style it yourself (inline CSS in the header; broader styling in Custom CSS).  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm
- **A tag/attribute disappears.** It’s likely not in the **Supported HTML** list (or is non‑whitelisted protocol).  
  https://doc.arcgis.com/en/arcgis-online/reference/supported-html.htm
- **CSS suddenly changed after an AGOL update.** Re‑test: Esri warns **custom CSS** can be impacted by product updates.  
  https://doc.arcgis.com/en/instant-apps/latest/customize/theme-layout-settings.htm

---

### Appendix A — Extra references you may want later
- Instant Apps templates overview: https://doc.arcgis.com/en/instant-apps/latest/create-apps/app-templates-overview.htm  
- What’s new (monitor changes that might affect CSS/headers): https://doc.arcgis.com/en/instant-apps/latest/get-started/whats-new.htm  
- Portfolio + Exhibit blog (curating collections): https://www.esri.com/arcgis-blog/products/instant-apps/mapping/portfolio-and-exhibit-an-instant-apps-pairing

---

**Maintainer note:** If you need a “scene switcher” within a single page, consider using **Portfolio** as the parent shell and embedding one 3D Viewer per scene. Keep this guide alongside your **/assets/css/** and **/assets/img/** folders so new team members have a single, authoritative reference.
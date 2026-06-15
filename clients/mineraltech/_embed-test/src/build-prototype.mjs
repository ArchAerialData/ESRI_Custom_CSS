import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const srcDir = path.dirname(__filename);
const rootDir = path.dirname(srcDir);
const finalDir = path.join(rootDir, "final-html");
const viewerOnlyDir = path.join(finalDir, "viewer-only");
const viewerOnlyBorderedDir = path.join(finalDir, "viewer-only-bordered");

const mineralTechUrl = "https://www.mineraltechllc.com/";
const arcgisUrl =
  "https://aallc.maps.arcgis.com/apps/instant/portfolio/index.html?appid=21d908a6c0004686882a68a3a58c9c8c&sectionId=1c7a910ceb8b400db9e179669d39720c&viewpoint=cam:-95.06822505,29.85782435,52.565;14.636,73.014&hiddenLayers=globalElevation";
const borderedArcgisUrl =
  "https://aallc.maps.arcgis.com/apps/instant/portfolio/index.html?appid=21d908a6c0004686882a68a3a58c9c8c&locale=en&sectionId=bcb4dbbbcc964926854427919c75544b&viewpoint=cam:-95.07017749,29.85956605,109.288;86.58,63.98&hiddenLayers=worldElevation";

const headers = {
  "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
  Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Language": "en-US,en;q=0.9",
};

const response = await fetch(mineralTechUrl, { headers, redirect: "follow" });

if (!response.ok) {
  throw new Error(`Failed to fetch ${mineralTechUrl}: ${response.status} ${response.statusText}`);
}

const originalHtml = await response.text();

const sharedTourCss = `
.prototype-tour-section {
  margin: 0 auto 56px;
}

.prototype-tour-intro {
  text-align: center;
}

.prototype-tour-title {
  margin-bottom: 12px;
}

.prototype-tour-subtext {
  max-width: 760px;
  margin: 0 auto 24px;
  color: #555;
  font-family: Lato, Arial, sans-serif;
  font-size: 18px;
  line-height: 1.55;
}

.prototype-tour-layout {
  display: flex;
  align-items: stretch;
  justify-content: center;
  gap: 28px;
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 24px;
}

.prototype-tour-model {
  flex: 0 1 940px;
  min-width: 0;
  overflow: hidden;
}

.prototype-tour-guide {
  flex: 0 0 250px;
  align-self: stretch;
  padding: 22px 22px 20px;
  border-left: 4px solid #1b264c;
  background: #f7f7f7;
  color: #333;
  font-family: Lato, Arial, sans-serif;
}

.prototype-tour-guide h2 {
  margin: 0 0 16px;
  color: #1b264c;
  font-size: 22px;
  line-height: 1.2;
}

.prototype-tour-guide dl {
  margin: 0;
}

.prototype-tour-guide-row {
  padding: 12px 0;
  border-top: 1px solid rgba(27, 38, 76, 0.14);
}

.prototype-tour-guide-row:first-child {
  padding-top: 0;
  border-top: 0;
}

.prototype-tour-guide dt {
  margin: 0 0 4px;
  color: #1b264c;
  font-weight: 700;
}

.prototype-tour-guide dd {
  margin: 0;
  color: #333;
}

@media (max-width: 1180px) {
  .prototype-tour-layout {
    max-width: 940px;
    flex-direction: column;
  }

  .prototype-tour-model {
    flex: 0 1 auto;
    width: 100%;
  }

  .prototype-tour-guide {
    flex: auto;
    border-top: 4px solid #1b264c;
    border-left: 0;
  }
}

@media (max-width: 767px) {
  .prototype-tour-section {
    margin-bottom: 42px;
  }

  .prototype-tour-layout {
    gap: 18px;
    max-width: 100%;
    padding: 0;
  }

  .prototype-tour-subtext {
    padding: 0 18px;
    font-size: 16px;
  }

  .prototype-tour-guide {
    margin: 0 16px;
  }
}
`;

const fullChromeOverrideCss = `/* MineralTech local prototype overrides.
   These rules keep the Webflow layout intact while replacing the YouTube
   embed with a clipped ArcGIS iframe. Tweak the custom properties on
   .prototype-esri-frame if the ArcGIS chrome/crop needs adjustment. */

:root {
  --prototype-esri-extra-height: 150px;
  --prototype-esri-y-offset: 0px;
  --prototype-esri-scale: 1;
}

${sharedTourCss}

.prototype-esri-frame {
  position: relative;
  width: 100%;
  max-width: 940px;
  aspect-ratio: 940 / 528;
  margin: 0 auto;
  overflow: hidden;
  background: #2f2f2f;
}

.prototype-esri-iframe {
  position: absolute;
  top: var(--prototype-esri-y-offset);
  left: 50%;
  width: calc(100% / var(--prototype-esri-scale));
  height: calc(100% + var(--prototype-esri-extra-height));
  border: 0;
  transform: translateX(-50%) scale(var(--prototype-esri-scale));
  transform-origin: top center;
}

.prototype-form-note {
  display: none;
  margin-top: 10px;
  color: #1b264c;
  font-family: Lato, Arial, sans-serif;
  font-size: 14px;
  font-weight: 700;
}

.prototype-form-note.is-visible {
  display: block;
}

@media (max-width: 767px) {
  :root {
    --prototype-esri-extra-height: 120px;
  }

  .prototype-esri-frame {
    max-width: 100%;
    aspect-ratio: 16 / 10;
  }

  .prototype-esri-iframe {
    left: 0;
    width: 100%;
    transform: scale(var(--prototype-esri-scale));
    transform-origin: top left;
  }
}
`;

const viewerOnlyOverrideCss = `/* MineralTech local prototype viewer-only overrides.
   This variant hides the ArcGIS app header, tab row, and subheader by
   cropping the iframe from the parent page. It cannot alter the remote
   ArcGIS DOM, so tune these crop values if the app chrome changes. */

:root {
  --prototype-esri-crop-top: 122px;
  --prototype-esri-extra-height: 280px;
  --prototype-esri-scale: 1;
}

${sharedTourCss}

.prototype-esri-frame {
  position: relative;
  width: 100%;
  max-width: 940px;
  aspect-ratio: 940 / 528;
  margin: 0 auto;
  overflow: hidden;
  background: #2f2f2f;
}

.prototype-esri-iframe {
  position: absolute;
  top: calc(-1 * var(--prototype-esri-crop-top));
  left: 50%;
  width: calc(100% / var(--prototype-esri-scale));
  height: calc(100% + var(--prototype-esri-crop-top) + var(--prototype-esri-extra-height));
  border: 0;
  transform: translateX(-50%) scale(var(--prototype-esri-scale));
  transform-origin: top center;
}

.prototype-form-note {
  display: none;
  margin-top: 10px;
  color: #1b264c;
  font-family: Lato, Arial, sans-serif;
  font-size: 14px;
  font-weight: 700;
}

.prototype-form-note.is-visible {
  display: block;
}

@media (max-width: 767px) {
  :root {
    --prototype-esri-crop-top: 122px;
    --prototype-esri-extra-height: 245px;
  }

  .prototype-esri-frame {
    max-width: 100%;
    aspect-ratio: 16 / 10;
  }

  .prototype-esri-iframe {
    left: 0;
    width: 100%;
    transform: scale(var(--prototype-esri-scale));
    transform-origin: top left;
  }
}
`;

const viewerOnlyBorderedOverrideCss = `/* MineralTech local prototype viewer-only bordered overrides.
   This variant uses the MineralTech palette from css/single_block/mineraltech.css:
   #1b264c navy, #000000 black, #bababa silver, #dad9d8 light silver,
   and #ffffff white. */

:root {
  --prototype-esri-crop-top: 122px;
  --prototype-esri-extra-height: 280px;
  --prototype-esri-scale: 1;
  --prototype-mineraltech-navy: #1b264c;
  --prototype-mineraltech-black: #000000;
  --prototype-mineraltech-silver: #bababa;
  --prototype-mineraltech-light-silver: #dad9d8;
  --prototype-mineraltech-white: #ffffff;
}

${sharedTourCss}

.prototype-tour-section--bordered .prototype-tour-layout {
  max-width: 1280px;
  gap: 24px;
  padding: 22px;
  border: 4px solid var(--prototype-mineraltech-navy);
  background: var(--prototype-mineraltech-white);
  box-shadow:
    0 0 0 1px var(--prototype-mineraltech-silver),
    0 14px 34px rgba(0, 0, 0, 0.16);
}

.prototype-tour-section--bordered .prototype-esri-frame {
  position: relative;
  width: 100%;
  max-width: 940px;
  aspect-ratio: 940 / 528;
  margin: 0 auto;
  overflow: hidden;
  border: 1px solid var(--prototype-mineraltech-black);
  background: #2f2f2f;
  box-shadow:
    0 0 0 4px var(--prototype-mineraltech-light-silver),
    0 0 0 5px rgba(27, 38, 76, 0.42);
}

.prototype-tour-section--bordered .prototype-tour-guide {
  border-left: 1px solid var(--prototype-mineraltech-light-silver);
  background:
    linear-gradient(180deg, rgba(218, 217, 216, 0.26), rgba(255, 255, 255, 0.96));
}

.prototype-esri-iframe {
  position: absolute;
  top: calc(-1 * var(--prototype-esri-crop-top));
  left: 50%;
  width: calc(100% / var(--prototype-esri-scale));
  height: calc(100% + var(--prototype-esri-crop-top) + var(--prototype-esri-extra-height));
  border: 0;
  transform: translateX(-50%) scale(var(--prototype-esri-scale));
  transform-origin: top center;
}

.prototype-form-note {
  display: none;
  margin-top: 10px;
  color: var(--prototype-mineraltech-navy);
  font-family: Lato, Arial, sans-serif;
  font-size: 14px;
  font-weight: 700;
}

.prototype-form-note.is-visible {
  display: block;
}

@media (max-width: 1180px) {
  .prototype-tour-section--bordered .prototype-tour-layout {
    max-width: 940px;
  }
}

@media (max-width: 767px) {
  :root {
    --prototype-esri-crop-top: 122px;
    --prototype-esri-extra-height: 245px;
  }

  .prototype-tour-section--bordered .prototype-tour-layout {
    margin: 0 14px;
    padding: 14px;
  }

  .prototype-tour-section--bordered .prototype-esri-frame {
    max-width: 100%;
    aspect-ratio: 16 / 10;
    box-shadow:
      0 0 0 3px var(--prototype-mineraltech-light-silver),
      0 0 0 4px rgba(27, 38, 76, 0.42);
  }

  .prototype-tour-section--bordered .prototype-tour-guide {
    margin: 0;
    border-top: 1px solid var(--prototype-mineraltech-light-silver);
    border-left: 0;
  }

  .prototype-esri-iframe {
    left: 0;
    width: 100%;
    transform: scale(var(--prototype-esri-scale));
    transform-origin: top left;
  }
}
`;

const prototypeScript = `<script>
(function () {
  var forms = document.querySelectorAll("form");
  forms.forEach(function (form) {
    form.setAttribute("data-prototype-disabled", "true");
    var note = document.createElement("div");
    note.className = "prototype-form-note";
    note.textContent = "Prototype only: form submission is disabled in this local copy.";
    form.appendChild(note);
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      note.classList.add("is-visible");
    });
  });
})();
</script>`;

function absolutizeRootRelativeUrls(html) {
  return html
    .replace(/(href|src)="\/(?!\/)([^"]*)"/g, `$1="${mineralTechUrl}$2"`)
    .replace(/(action)="\/(?!\/)([^"]*)"/g, `$1="${mineralTechUrl}$2"`);
}

function stripTrackingAndUnsupportedExports(html) {
  return html
    .replace(/<script>\(function\(w,i,g\)[\s\S]*?google_tags_first_party[\s\S]*?<\/script>/gi, "")
    .replace(/<script[^>]+src="https:\/\/www\.googletagmanager\.com\/gtag\/js[^"]*"[^>]*><\/script>/gi, "")
    .replace(/<script[^>]+src="https:\/\/www\.google\.com\/recaptcha\/api\.js"[^>]*><\/script>/gi, "")
    .replace(/<script[^>]+src="https:\/\/www\.mineraltechllc\.com\/9i1h7htkfq16[^"]*"[^>]*><\/script>/gi, "")
    .replace(/<!-- Google Tag Manager -->[\s\S]*?\}\)\(window,document,'script','dataLayer','GTM-PBZPDRG3'\);<\/script>/i, "")
    .replace(/<!-- Google Tag Manager \(noscript\) -->[\s\S]*?<noscript><iframe src="https:\/\/www\.googletagmanager\.com\/ns\.html\?id=GTM-PBZPDRG3"[\s\S]*?<\/noscript>/i, "")
    .replace(/<div data-sitekey="[^"]*" class="w-form-formrecaptcha[^"]*"><\/div>/gi, "")
    .replace(/\sdata-turnstile-sitekey="[^"]*"/gi, "");
}

function replaceYoutubeEmbed(html, options = {}) {
  const { extraSectionClass = "", embedUrl = arcgisUrl } = options;
  const sectionClass = `prototype-tour-section prototype-esri-section${extraSectionClass ? ` ${extraSectionClass}` : ""}`;
  const replacement = `<section class="${sectionClass}">
  <div class="prototype-tour-intro w-layout-blockcontainer w-container">
    <h1 class="heading-3 prototype-tour-title">Take a virtual tour of our facilities</h1>
    <p class="prototype-tour-subtext">Explore an interactive 3D model of the MineralTech site. Drag, rotate, and zoom to inspect the facility from different angles.</p>
  </div>
  <div class="prototype-tour-layout">
    <div class="prototype-tour-model">
      <div class="prototype-esri-frame">
        <iframe
          class="prototype-esri-iframe"
          src="${embedUrl}"
          title="MineralTech Highlands 3D mesh ArcGIS viewer"
          loading="lazy"
          allowfullscreen
          referrerpolicy="no-referrer-when-downgrade">iFrames are not supported on this page.</iframe>
      </div>
    </div>
    <aside class="prototype-tour-guide" aria-label="Model navigation guide">
      <h2>Navigation guide</h2>
      <dl>
        <div class="prototype-tour-guide-row">
          <dt>Left Click + Drag</dt>
          <dd>Pan</dd>
        </div>
        <div class="prototype-tour-guide-row">
          <dt>Right Click + Drag</dt>
          <dd>Rotate</dd>
        </div>
        <div class="prototype-tour-guide-row">
          <dt>Scroll Wheel Up/Down</dt>
          <dd>Zoom</dd>
        </div>
      </dl>
    </aside>
  </div>
</section>`;

  const pattern =
    /<h1 class="heading-3">Behind the Scenes at MineralTech Gulf Coast Abrasives<\/h1><section><div class="w-layout-blockcontainer w-container"><div style="padding-top:56\.17021276595745%" class="w-video w-embed"><iframe class="embedly-embed"[\s\S]*?<\/iframe><\/div><\/div><\/section>/;

  if (!pattern.test(html)) {
    throw new Error("Could not find the Webflow YouTube heading and embed section to replace.");
  }

  return html.replace(pattern, replacement);
}

function insertPrototypeAssets(html, overrideCss) {
  const styleTag = `<style>${overrideCss}</style>`;

  return html
    .replace("</head>", `${styleTag}</head>`)
    .replace("</body>", `${prototypeScript}</body>`);
}

function buildPrototypeHtml(overrideCss, options = {}) {
  let html = originalHtml;
  html = absolutizeRootRelativeUrls(html);
  html = stripTrackingAndUnsupportedExports(html);
  html = replaceYoutubeEmbed(html, {
    embedUrl: options.embedUrl,
    extraSectionClass: options.extraSectionClass,
  });
  html = insertPrototypeAssets(html, overrideCss);
  return html;
}

const fullChromeHtml = buildPrototypeHtml(fullChromeOverrideCss);
const viewerOnlyHtml = buildPrototypeHtml(viewerOnlyOverrideCss);
const viewerOnlyBorderedHtml = buildPrototypeHtml(viewerOnlyBorderedOverrideCss, {
  embedUrl: borderedArcgisUrl,
  extraSectionClass: "prototype-tour-section--bordered",
});

await mkdir(srcDir, { recursive: true });
await mkdir(finalDir, { recursive: true });
await mkdir(viewerOnlyDir, { recursive: true });
await mkdir(viewerOnlyBorderedDir, { recursive: true });

await writeFile(path.join(srcDir, "mineraltech-homepage.original.html"), originalHtml, "utf8");
await writeFile(path.join(srcDir, "embed-overrides.full-chrome.css"), fullChromeOverrideCss, "utf8");
await writeFile(path.join(srcDir, "embed-overrides.viewer-only.css"), viewerOnlyOverrideCss, "utf8");
await writeFile(path.join(srcDir, "embed-overrides.viewer-only-bordered.css"), viewerOnlyBorderedOverrideCss, "utf8");
await writeFile(path.join(srcDir, "mineraltech-homepage.full-chrome-source.html"), fullChromeHtml, "utf8");
await writeFile(path.join(srcDir, "mineraltech-homepage.viewer-only-source.html"), viewerOnlyHtml, "utf8");
await writeFile(path.join(srcDir, "mineraltech-homepage.viewer-only-bordered-source.html"), viewerOnlyBorderedHtml, "utf8");
await writeFile(path.join(finalDir, "index.html"), fullChromeHtml, "utf8");
await writeFile(path.join(viewerOnlyDir, "index.html"), viewerOnlyHtml, "utf8");
await writeFile(path.join(viewerOnlyBorderedDir, "index.html"), viewerOnlyBorderedHtml, "utf8");

console.log(`Wrote ${path.relative(rootDir, path.join(finalDir, "index.html"))}`);
console.log(`Wrote ${path.relative(rootDir, path.join(viewerOnlyDir, "index.html"))}`);
console.log(`Wrote ${path.relative(rootDir, path.join(viewerOnlyBorderedDir, "index.html"))}`);

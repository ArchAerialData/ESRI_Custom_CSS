import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const srcDir = path.dirname(__filename);
const rootDir = path.dirname(srcDir);
const finalDir = path.join(rootDir, "final-html");
const viewerOnlyDir = path.join(finalDir, "viewer-only");

const mineralTechUrl = "https://www.mineraltechllc.com/";
const arcgisUrl =
  "https://aallc.maps.arcgis.com/apps/instant/portfolio/index.html?appid=21d908a6c0004686882a68a3a58c9c8c&sectionId=1c7a910ceb8b400db9e179669d39720c&viewpoint=cam:-95.06822505,29.85782435,52.565;14.636,73.014&hiddenLayers=globalElevation";

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

const fullChromeOverrideCss = `/* MineralTech local prototype overrides.
   These rules keep the Webflow layout intact while replacing the YouTube
   embed with a clipped ArcGIS iframe. Tweak the custom properties on
   .prototype-esri-frame if the ArcGIS chrome/crop needs adjustment. */

:root {
  --prototype-esri-extra-height: 150px;
  --prototype-esri-y-offset: 0px;
  --prototype-esri-scale: 1;
}

.prototype-esri-section {
  margin: 0 auto;
}

.prototype-esri-frame {
  position: relative;
  width: 100%;
  max-width: 940px;
  aspect-ratio: 940 / 528;
  margin: 0 auto;
  overflow: hidden;
  background: #2f2f2f;
}

.prototype-esri-section .w-container {
  overflow: hidden;
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

  .prototype-esri-section .w-container {
    max-width: 100%;
    padding-right: 0;
    padding-left: 0;
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

.prototype-esri-section {
  margin: 0 auto;
}

.prototype-esri-frame {
  position: relative;
  width: 100%;
  max-width: 940px;
  aspect-ratio: 940 / 528;
  margin: 0 auto;
  overflow: hidden;
  background: #2f2f2f;
}

.prototype-esri-section .w-container {
  overflow: hidden;
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

  .prototype-esri-section .w-container {
    max-width: 100%;
    padding-right: 0;
    padding-left: 0;
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

function replaceYoutubeEmbed(html) {
  const replacement = `<section class="prototype-esri-section">
  <div class="w-layout-blockcontainer w-container">
    <div class="prototype-esri-frame">
      <iframe
        class="prototype-esri-iframe"
        src="${arcgisUrl}"
        title="MineralTech Highlands 3D mesh ArcGIS viewer"
        loading="lazy"
        allowfullscreen
        referrerpolicy="no-referrer-when-downgrade">iFrames are not supported on this page.</iframe>
    </div>
  </div>
</section>`;

  const pattern =
    /<section><div class="w-layout-blockcontainer w-container"><div style="padding-top:56\.17021276595745%" class="w-video w-embed"><iframe class="embedly-embed"[\s\S]*?<\/iframe><\/div><\/div><\/section>/;

  if (!pattern.test(html)) {
    throw new Error("Could not find the Webflow YouTube embed section to replace.");
  }

  return html.replace(pattern, replacement);
}

function insertPrototypeAssets(html, overrideCss) {
  const styleTag = `<style>${overrideCss}</style>`;

  return html
    .replace("</head>", `${styleTag}</head>`)
    .replace("</body>", `${prototypeScript}</body>`);
}

function buildPrototypeHtml(overrideCss) {
  let html = originalHtml;
  html = absolutizeRootRelativeUrls(html);
  html = stripTrackingAndUnsupportedExports(html);
  html = replaceYoutubeEmbed(html);
  html = insertPrototypeAssets(html, overrideCss);
  return html;
}

const fullChromeHtml = buildPrototypeHtml(fullChromeOverrideCss);
const viewerOnlyHtml = buildPrototypeHtml(viewerOnlyOverrideCss);

await mkdir(srcDir, { recursive: true });
await mkdir(finalDir, { recursive: true });
await mkdir(viewerOnlyDir, { recursive: true });

await writeFile(path.join(srcDir, "mineraltech-homepage.original.html"), originalHtml, "utf8");
await writeFile(path.join(srcDir, "embed-overrides.full-chrome.css"), fullChromeOverrideCss, "utf8");
await writeFile(path.join(srcDir, "embed-overrides.viewer-only.css"), viewerOnlyOverrideCss, "utf8");
await writeFile(path.join(srcDir, "mineraltech-homepage.full-chrome-source.html"), fullChromeHtml, "utf8");
await writeFile(path.join(srcDir, "mineraltech-homepage.viewer-only-source.html"), viewerOnlyHtml, "utf8");
await writeFile(path.join(finalDir, "index.html"), fullChromeHtml, "utf8");
await writeFile(path.join(viewerOnlyDir, "index.html"), viewerOnlyHtml, "utf8");

console.log(`Wrote ${path.relative(rootDir, path.join(finalDir, "index.html"))}`);
console.log(`Wrote ${path.relative(rootDir, path.join(viewerOnlyDir, "index.html"))}`);

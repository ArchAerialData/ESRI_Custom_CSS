#!/usr/bin/env node

import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import sharp from "sharp";
import ImageTracer from "imagetracerjs";
import { Resvg } from "@resvg/resvg-js";

const usage = `
Usage:
  npm.cmd run trace-logo -- --input <image> --svg <output.svg> [options]

Options:
  --input <path>          Source JPG/PNG/WebP/etc.
  --svg <path>            Output traced SVG path.
  --png <path>            Optional rendered PNG preview from the traced SVG.
  --png-size <px>         Width used for optional PNG preview. Default: 400.
  --remove-white          Convert near-white source pixels to transparent before tracing.
  --white-threshold <n>   RGB threshold for --remove-white. Default: 245.
  --trim                  Trim transparent/near-transparent edges before tracing.
  --colors <n>            Target color count for tracing. Default: 8.
  --palette <hex,...>     Optional fixed palette, e.g. "#024ab8,#eb2518,#ffffff".
  --ltres <n>             ImageTracer line threshold. Default: 1.
  --qtres <n>             ImageTracer curve threshold. Default: 1.
  --pathomit <n>          Drop paths shorter than this. Default: 8.
  --blur <n>              ImageTracer blur radius. Default: 0.
  --help                  Show this help text.

Examples:
  npm.cmd run trace-logo -- --input clients/faulconer_energy/logos/cover/faulconer_mark.png --svg clients/faulconer_energy/logos/cover/faulconer_mark.svg --png clients/faulconer_energy/logos/cover/faulconer_mark_trace.png --trim --colors 4
  npm.cmd run trace-logo -- --input clients/faulconer_energy/logos/cover/faulconer.jpg --svg clients/faulconer_energy/logos/cover/faulconer.svg --remove-white --trim --colors 6
`;

function parseArgs(argv) {
  const args = {};

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected positional argument: ${token}`);
    }

    const key = token.slice(2);
    if (key === "help" || key === "remove-white" || key === "trim") {
      args[key] = true;
      continue;
    }

    const value = argv[i + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    args[key] = value;
    i += 1;
  }

  return args;
}

function numberOption(args, key, fallback) {
  if (args[key] == null) return fallback;
  const value = Number(args[key]);
  if (!Number.isFinite(value)) {
    throw new Error(`--${key} must be a number`);
  }
  return value;
}

function parsePalette(value) {
  if (!value) return undefined;

  return value.split(",").map((entry) => {
    const hex = entry.trim().replace(/^#/, "");
    if (!/^[0-9a-fA-F]{6}$/.test(hex)) {
      throw new Error(`Invalid palette color: ${entry}`);
    }

    return {
      r: Number.parseInt(hex.slice(0, 2), 16),
      g: Number.parseInt(hex.slice(2, 4), 16),
      b: Number.parseInt(hex.slice(4, 6), 16),
      a: 255,
    };
  });
}

function removeWhiteBackground(data, threshold) {
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];
    const a = data[i + 3];

    if (a === 0) continue;
    if (r >= threshold && g >= threshold && b >= threshold) {
      data[i + 3] = 0;
    }
  }
}

function trimImageData(data, width, height, alphaThreshold = 8) {
  let minX = width;
  let minY = height;
  let maxX = -1;
  let maxY = -1;

  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const alpha = data[(y * width + x) * 4 + 3];
      if (alpha <= alphaThreshold) continue;

      minX = Math.min(minX, x);
      minY = Math.min(minY, y);
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);
    }
  }

  if (maxX < minX || maxY < minY) {
    throw new Error("Trim removed the entire image; check the input or white threshold.");
  }

  const trimmedWidth = maxX - minX + 1;
  const trimmedHeight = maxY - minY + 1;
  const trimmed = Buffer.alloc(trimmedWidth * trimmedHeight * 4);

  for (let y = 0; y < trimmedHeight; y += 1) {
    const sourceStart = ((minY + y) * width + minX) * 4;
    const targetStart = y * trimmedWidth * 4;
    data.copy(trimmed, targetStart, sourceStart, sourceStart + trimmedWidth * 4);
  }

  return { data: trimmed, width: trimmedWidth, height: trimmedHeight };
}

async function ensureParent(filePath) {
  await mkdir(path.dirname(path.resolve(filePath)), { recursive: true });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    process.stdout.write(usage);
    return;
  }

  if (!args.input || !args.svg) {
    throw new Error("Both --input and --svg are required. Use --help for examples.");
  }

  const inputPath = path.resolve(args.input);
  const svgPath = path.resolve(args.svg);
  const pngPath = args.png ? path.resolve(args.png) : undefined;
  const whiteThreshold = numberOption(args, "white-threshold", 245);
  const pngSize = numberOption(args, "png-size", 400);

  const image = sharp(inputPath, { limitInputPixels: false }).ensureAlpha();
  const { data: rawData, info } = await image.raw().toBuffer({ resolveWithObject: true });
  let traceData = Buffer.from(rawData);
  let width = info.width;
  let height = info.height;

  if (args["remove-white"]) {
    removeWhiteBackground(traceData, whiteThreshold);
  }

  if (args.trim) {
    const trimmed = trimImageData(traceData, width, height);
    traceData = trimmed.data;
    width = trimmed.width;
    height = trimmed.height;
  }

  const palette = parsePalette(args.palette);
  const tracerOptions = {
    ltres: numberOption(args, "ltres", 1),
    qtres: numberOption(args, "qtres", 1),
    pathomit: numberOption(args, "pathomit", 8),
    numberofcolors: numberOption(args, "colors", 8),
    colorquantcycles: 3,
    scale: 1,
    strokewidth: 0,
    roundcoords: 2,
    viewbox: true,
    desc: false,
    blurradius: numberOption(args, "blur", 0),
    blurdelta: 20,
    ...(palette ? { colorsampling: 0, pal: palette } : {}),
  };

  const svg = ImageTracer.imagedataToSVG(
    { width, height, data: new Uint8ClampedArray(traceData) },
    tracerOptions,
  );

  await ensureParent(svgPath);
  await writeFile(svgPath, svg, "utf8");

  if (pngPath) {
    await ensureParent(pngPath);
    const rendered = new Resvg(svg, {
      fitTo: { mode: "width", value: pngSize },
      background: "rgba(255, 255, 255, 0)",
    }).render();
    await writeFile(pngPath, rendered.asPng());
  }

  process.stdout.write(
    [
      `Traced: ${args.input}`,
      `SVG: ${path.relative(process.cwd(), svgPath)}`,
      pngPath ? `PNG preview: ${path.relative(process.cwd(), pngPath)}` : undefined,
      `Trace size: ${width}x${height}`,
    ]
      .filter(Boolean)
      .join("\n") + "\n",
  );
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});

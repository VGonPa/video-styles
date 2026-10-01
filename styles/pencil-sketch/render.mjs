// Frame renderer shared by every style. The canonical copy lives in tools/render.mjs and is copied
// unchanged into each styles/<slug>/ folder (check_catalog.py verifies the copies match).
//
//   node render.mjs <outDir> [fps=30] [t0=0] [t1=10] [workers=2] [times]
//
// Loads anim.html next to this file in headless Chromium, waits for `window.ready`, then calls
// `window.draw({ t, file })` for each frame; draw() returns a base64 JPEG which is written to disk.
// Without `times`, frames are numbered on a 30 fps grid (00000.jpg, 00001.jpg, ...) from t0 to t1,
// keeping every (30 / fps)th one. With `times` (comma list of seconds), writes t_<t>.jpg stills.
//
// Optional per-style settings in render.json next to this file:
//   gpu          "metal": ANGLE on Metal; "full": Metal plus forced GPU raster; absent: Chromium default
//   schedule     "contiguous": each page renders one unbroken, time-ordered run of frames (needed by
//                path-dependent simulations); absent: pages take frames round-robin
//   eventsGpu    GPU mode for events.mjs (same values as gpu). Kept separate because some styles derive
//                cue timings from what they draw, and their events.json was produced without GPU flags.
//
// Playwright is looked up in $PLAYWRIGHT_DIR, then the global @playwright/test, then local packages.
// events.mjs imports this module to share the browser setup.
import { createRequire } from 'module';
import { execSync } from 'child_process';
import { fileURLToPath, pathToFileURL } from 'url';
import fs from 'fs';
import os from 'os';
import path from 'path';

export const here = path.dirname(fileURLToPath(import.meta.url));

export function settings() {
  const file = path.join(here, 'render.json');
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : {};
}

function playwright() {
  const req = createRequire(import.meta.url);
  const tried = [];
  if (process.env.PLAYWRIGHT_DIR) tried.push(process.env.PLAYWRIGHT_DIR);
  try { tried.push(path.join(execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(), '@playwright/test')); } catch {}
  tried.push('playwright', 'playwright-core');
  for (const name of tried) {
    try { return req(name); } catch {}
  }
  throw new Error(`Playwright not found (tried ${tried.join(', ')}). Install @playwright/test globally or set PLAYWRIGHT_DIR.`);
}

// Newest headless shell from the Playwright cache, if one is installed for this platform.
function headlessShell() {
  const cache = process.env.PLAYWRIGHT_BROWSERS_PATH || path.join(os.homedir(), 'Library/Caches/ms-playwright');
  if (!fs.existsSync(cache)) return undefined;
  const builds = fs.readdirSync(cache).filter(n => n.startsWith('chromium_headless_shell-')).sort().reverse();
  for (const b of builds) {
    const bin = path.join(cache, b, 'chrome-headless-shell-mac-arm64', 'chrome-headless-shell');
    if (fs.existsSync(bin)) return bin;
  }
  return undefined;
}

const GPU_FLAGS = {
  metal: ['--use-angle=metal'],
  full: ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'],
};

export async function launch(gpu) {
  const { chromium } = playwright();
  return chromium.launch({ executablePath: headlessShell(), args: GPU_FLAGS[gpu] || [] });
}

// A 1920x1080 page with anim.html loaded and its `window.ready` promise settled.
export async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', err => console.log('[err]', err.message));
  page.on('console', msg => { if (msg.type() === 'error') console.log('[console]', msg.text()); });
  await page.goto(pathToFileURL(path.join(here, 'anim.html')).href);
  await page.evaluate(() => window.ready);
  return page;
}

function frameList(outDir, fps, t0, t1, times) {
  if (times) {
    return times.split(',').map(Number).sort((a, b) => a - b)
      .map(t => ({ t, file: path.join(outDir, `t_${t.toFixed(2)}.jpg`) }));
  }
  const step = Math.round(30 / fps), first = Math.round(t0 * 30), end = Math.round(t1 * 30);
  const list = [];
  for (let n = first; n < end; n += step) list.push({ t: n / 30, file: path.join(outDir, String(n).padStart(5, '0') + '.jpg') });
  return list;
}

// Indices of the frames page k of `pages` renders.
function share(k, pages, count, schedule) {
  const idx = [];
  if (schedule === 'contiguous') {
    for (let i = Math.floor(k * count / pages); i < Math.floor((k + 1) * count / pages); i++) idx.push(i);
  } else {
    for (let i = k; i < count; i += pages) idx.push(i);
  }
  return idx;
}

async function main() {
  const cfg = settings();
  const [outDir, fps = 30, t0 = 0, t1 = 10, workers = 2, times] = process.argv.slice(2);
  if (!outDir) {
    console.error('usage: node render.mjs <outDir> [fps] [t0] [t1] [workers] [times]');
    process.exit(2);
  }
  fs.mkdirSync(outDir, { recursive: true });
  const frames = frameList(outDir, +fps, +t0, +t1, times);
  const pages = Math.max(1, Math.min(+workers, frames.length));
  const started = Date.now();
  const browser = await launch(cfg.gpu);
  await Promise.all(Array.from({ length: pages }, async (_, k) => {
    const page = await openPage(browser);
    for (const i of share(k, pages, frames.length, cfg.schedule)) {
      const jpeg = await page.evaluate(job => window.draw(job), frames[i]);
      fs.writeFileSync(frames[i].file, Buffer.from(jpeg, 'base64'));
    }
  }));
  await browser.close();
  console.log(`drew ${frames.length} in ${((Date.now() - started) / 1000).toFixed(1)} s`);
}

if (process.argv[1] && fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url))) await main();

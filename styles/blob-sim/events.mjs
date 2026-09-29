// node events.mjs → writes window.events() output in anim.html to events.json (for audio)
import { createRequire } from 'module'; import { execSync } from 'child_process'; import path from 'path'; import fs from 'fs';
const require = createRequire(import.meta.url);
// Playwright: global @playwright/test (as in the other styles), else $PLAYWRIGHT_DIR (a playwright or playwright-core package dir)
const loadPW = () => { const cands = [process.env.PLAYWRIGHT_DIR, path.join(execSync('npm root -g').toString().trim(), '@playwright/test'), 'playwright', 'playwright-core'].filter(Boolean);
  for (const c of cands) { try { return require(c); } catch {} } throw new Error('Playwright not found: npm i -g @playwright/test or set PLAYWRIGHT_DIR'); };
const { chromium } = loadPW();
const dir = path.dirname(new URL(import.meta.url).pathname);
const base = path.join(process.env.HOME, 'Library/Caches/ms-playwright');
const d = fs.readdirSync(base).filter(d => d.startsWith('chromium_headless_shell-')).sort().reverse()[0];
const b = await chromium.launch({ executablePath: path.join(base, d, 'chrome-headless-shell-mac-arm64/chrome-headless-shell'), args: ['--use-angle=metal'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto('file://' + path.join(dir, 'anim.html')); await p.evaluate(() => window.ready);
fs.writeFileSync(path.join(dir, 'events.json'), JSON.stringify(await p.evaluate(() => window.events())));
await b.close();

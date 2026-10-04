#!/bin/bash
# Check the tools a style needs to render: Node.js 18+, Playwright with a Chromium build, ffmpeg + ffprobe,
# and Python 3 with NumPy. Prints one line per tool and exits non-zero if something is missing.
missing=0
have() {  # have <command> <hint>
  if command -v "$1" >/dev/null 2>&1; then echo "ok       $1  $("$1" -version 2>/dev/null | head -1 || true)"
  else echo "MISSING  $1 — $2"; missing=1; fi
}
if command -v node >/dev/null 2>&1; then
  major=$(node -p 'process.versions.node.split(".")[0]')
  if [ "$major" -ge 18 ]; then echo "ok       node $(node --version)"; else echo "OLD      node $(node --version) — need 18 or newer"; missing=1; fi
else echo "MISSING  node — install Node.js 18 or newer"; missing=1; fi
have ffmpeg "install ffmpeg (macOS: brew install ffmpeg; Debian/Ubuntu: apt install ffmpeg)"
have ffprobe "ships with ffmpeg"
if python3 -c "import numpy" 2>/dev/null; then echo "ok       python3 + numpy"
else echo "MISSING  python3 with numpy — python3 -m pip install --user numpy (or in a venv; Homebrew/Debian Pythons refuse a plain pip install)"; missing=1; fi
if command -v git >/dev/null 2>&1; then echo "ok       git (optional: fetch_style.py falls back to the GitHub tarball)"
else echo "info     git not found (optional: fetch_style.py downloads the GitHub tarball instead)"; fi
if command -v node >/dev/null 2>&1; then
  # Same lookup order as render.mjs, then a real headless launch.
  node - <<'JS' || missing=1
const { createRequire } = require('module');
const { execSync } = require('child_process');
const path = require('path');
const req = createRequire(path.join(process.cwd(), 'x.js'));
const tried = [];
if (process.env.PLAYWRIGHT_DIR) tried.push(process.env.PLAYWRIGHT_DIR);
try { tried.push(path.join(execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(), '@playwright/test')); } catch {}
tried.push('playwright', 'playwright-core');
let pw;
for (const name of tried) { try { pw = req(name); break; } catch {} }
if (!pw) {
  console.log('MISSING  Playwright — npm install -g @playwright/test && npx playwright install chromium');
  process.exit(1);
}
pw.chromium.launch().then(b => b.close()).then(
  () => console.log('ok       Playwright + Chromium'),
  e => { console.log('FAILED   Chromium did not launch: either it is not installed (npx playwright install chromium; Linux: also\n         npx playwright install-deps) or a sandbox blocked it (common for coding agents: ask for permission to run\n         it outside the sandbox). Error: ' + e.message.split('\n')[0]); process.exit(1); });
JS
fi
case "$(uname -s)" in
  Darwin) ;;
  *) echo "note     not macOS: render.mjs's GPU flags (render.json \"gpu\") target Metal, so WebGL styles fall back to slower software rendering" ;;
esac
exit $missing

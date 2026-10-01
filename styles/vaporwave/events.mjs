// Writes the style's sound cue list to events.json for audio.py. The canonical copy lives in
// tools/events.mjs and is copied unchanged into each styles/<slug>/ folder next to render.mjs.
//
//   node events.mjs
//
// Opens anim.html like render.mjs does (GPU mode from render.json `eventsGpu`) and saves what
// `window.events()` returns. A style that drives its audio from a raw sample stream instead sets
// render.json `signal` to a file name: `window.signal()` must then return base64 bytes, which are
// written to that file and no events.json is produced.
import fs from 'fs';
import path from 'path';
import { here, launch, openPage, settings } from './render.mjs';

const cfg = settings();
const browser = await launch(cfg.eventsGpu);
const page = await openPage(browser);
if (cfg.signal) {
  const bytes = await page.evaluate(() => window.signal());
  fs.writeFileSync(path.join(here, cfg.signal), Buffer.from(bytes, 'base64'));
} else {
  const cues = await page.evaluate(() => window.events());
  fs.writeFileSync(path.join(here, 'events.json'), JSON.stringify(cues));
}
await browser.close();

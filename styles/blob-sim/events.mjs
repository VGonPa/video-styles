// Writes the style's sound cue list to events.json for audio.py. The canonical copy lives in
// tools/events.mjs and is copied unchanged into each styles/<slug>/ folder next to render.mjs.
//
//   node events.mjs
//
// Opens anim.html like render.mjs does (GPU mode from render.json `eventsGpu`) and saves what
// `window.events()` returns.
import fs from 'fs';
import path from 'path';
import { here, launch, openPage, settings } from './render.mjs';

const browser = await launch(settings().eventsGpu);
const page = await openPage(browser);
const cues = await page.evaluate(() => window.events());
fs.writeFileSync(path.join(here, 'events.json'), JSON.stringify(cues));
await browser.close();

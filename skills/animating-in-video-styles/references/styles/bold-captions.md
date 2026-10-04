# Bold Captions (`bold-captions`)

The word-by-word caption edit of short-form talking-head clips on Reels, Shorts and TikTok, the look business-advice
creators made popular around 2021: a spoken sentence shown one to three words at a time in heavy outlined capitals
over footage, the key word of each chunk popping in colour while the camera punches in and shakes, with flat sticker
cutaways and a progress bar along the top. The captions are the star; picture and sound exist to make every word
land. Urgent, confident, built to stop a scroll.

**Reference film:** a ten-second tip about screen time, captioned over a blurred presenter, with alarm-clock, phone and three-icon cutaways · `styles/bold-captions/`

## Signature
- **S1 Chunked word-by-word captions:** one to three uppercase words per chunk in Montserrat Black, white with a
  thick black outline and a soft drop shadow, on one centred line in the lower third; each word pops in with a
  small overshoot as the line re-centres, and the next chunk replaces it in one frame (`captions()`, `layout()`).
  (In the demo: YOU DON'T NEED from 0.40 s.)
- **S2 One coloured keyword per chunk:** bigger (1.2–1.4×; list items 1.05×), yellow, green or red, dropping in
  tilted with a bigger overshoot while the camera punches in and shakes (`HL`, `punch()`, `shake()`). (In the demo:
  TIME. at 1.36 s.)
- **S3 A soft photographic plate under the words:** the speaker's footage with grain, pushing in slowly and nodding
  on each word (`BG`, `FIG`, `drawSpeaker()`). The demo's plate is a stand-in: a warm studio with rim light and
  bokeh behind an abstract blurred bust.
- **S4 Flat sticker cutaways:** outlined flat-colour stickers with a hard offset shadow on a saturated, slowly
  turning sunburst, entered by a hard cut with a zoom snap and a white flash (`burst()`, `sticker()`, `shp()`).
  (In the demo: a red alarm clock on blue at 1.90 s.)
- **S5 A yellow progress bar** across the top edge, filling with film time (`progress()`).

## Palette
| Role | Colour | In code |
|---|---|---|
| Caption fill | `#FFFFFF` | `captions()` |
| Caption outline; its shadow at 0.6 alpha | `#000`; 0,0,0 | `captions()` |
| Main highlight (payoff, call to action); progress fill; iris ring | `#FFE11A` | `YEL`, `HL` |
| Second highlight (other emphasis, list items) | `#3BF26E` | `GRN`, `HL` |
| Loss or warning highlight, once a film | `#FF3B3B` | `RED`, `HL` |
| Sticker outlines and details | `#101010` | `INK` |
| Footage plate: gradient; warm key; cool fill | `#2a1d18` → `#0f0b0a`; 255,146,72; 58,104,255 | `buildTextures()` |
| Presenter: silhouette; rim from cool to warm | `#1b1412`; 90,130,255 → 255,170,110 | `buildTextures()` |
| Sunbursts, base and rays (one pair per cutaway) | `#2F6BFF` `#3A78FF`; `#FF5446` `#FF6456`; `#6A45FF` `#7654FF` | `burst()` callers |
| Sticker fills: toy-bright, mid-dark greys for metal | `#FF4B4B`, `#FFC21A`, `#2b2b33`, `#FF8A2A`, `#E9B04C`, `#1FAE52`, `#3C4150`, `#C9CED8` | `drawClock()`, `book()`, `moneyBag()`, `dumbbell()` |
| Progress track at 0.22 alpha | 255,255,255 | `progress()` |

- Soft photographic footage (warm in the demo) under flat, hard-edged captions, stickers and bar: that contrast is
  the look. One saturated sunburst hue per cutaway, rays a shade lighter; stickers take flat fills, an ink outline
  and one white streak at 0.35 alpha, never gradients.

## Typography and copy
- **Font:** Montserrat (`fonts/Montserrat-latin.woff2`, variable 100–900, loaded by `fonts.css`); captions use 900
  through `font()` with letter-spacing −2 px, the money bag's $ too. Glyphs: Basic Latin and Latin-1 (á é ñ ü ç ß ¿ ¡
  €), Ă ı Œ œ, curly quotes, en and em dashes, •, …, ™, ↑ ↓; no → or ✓, no ł ő š ž ğ ş, Greek, Cyrillic or emoji.
- **Caption metrics:** size = `BASE` (165) × the word's multiplier (1, or 1.05–1.4 for a keyword) × the chunk's fit
  from `measure()`, which shrinks the words (never the gaps, `BASE` × `GAP`) until the line is at most `MAXW` (1720)
  wide; outline `lineWidth` 0.17 × size under the fill (half shows), shadow blur 0.14 × size, 0.08 × size down.
- **Copy:** spoken, second person, imperative; a chunk ends where a speaker breathes, usually on a full stop; digits
  for numbers. Line roles: a hook (claim or question, on screen within 0.5 s), its payoff word in yellow, supporting
  chunks, optionally a karaoke list of three one-word items in green, a call to action ending in a yellow word. One
  keyword per chunk, list excepted; red once, for a loss or warning. Bakery test (rendered, 16:9): WANT BETTER
  BREAD? / STOP KNEADING. / … / BAKE TOMORROW.
- **Capacity:** capitals measure 0.62–0.84 em (about 0.7). At full size a chunk holds about 13 letters in 16:9, and
  about 9 in 9:16 and 1:1 (7 with a 1.3× keyword); each extra letter shrinks the whole line about 8 %. Keep the fit
  at 0.7 or more (in 9:16 about 13 letters): below it a chunk looks small next to its neighbours (WANT BETTER BREAD?
  is 62 px in 9:16 against 120 px for one word). Longer copy becomes more chunks, not longer lines: in 9:16 WANT
  BETTER / BREAD? fit at 0.86 and 1.0. The exception is a karaoke list, which must stay one chunk: keep its items
  to about five letters (PACK. PLAN. GO. fits at 0.70; TRAIN. READ. BUILD. at 0.56).
- **Reading time:** a plain word at least 0.2 s (0.22 in the demo) before the next; a keyword at least 0.4 s on
  screen (its pop takes 0.22 s); a chunk's last word at least 0.25 s. The demo runs 1.5 chunks, 3 words a second.

## Texture and finish
- `buildTextures()` runs once in `window.ready`: the plate `BG` (warm gradient, five glows, two softbox panels, 34
  bokeh discs, a 22 px blur), the presenter `FIG` (head-and-shoulders silhouette rim-lit cool left and warm right, a
  skin-toned key on the face, an 11 px blur), the vignette `VIG` (speaker shots only) and a 512 px noise tile `GRAIN`.
- `world()` lays the grain over every picture at 0.09 alpha in `overlay`, re-offset every frame; captions and bar
  come after it in `render()`, crisp. `sticker()` adds a black silhouette copy offset 14, 18 px at 0.3 alpha;
  `burst()` turns 18 rays at 0.25 rad/s under a radial gradient (white 0.22 at the centre, black 0.25 at the edge).

## Shapes, line and figures
- Stickers are chunky icons of rounded rectangles, arcs and curves, each part one `shp()` call: a flat fill and a
  9–14 px round-joined `INK` outline. Details (ticks, text, highlights) go inside `if (MODE === 'col')`, skipped in
  the silhouette pass. A new one: two to eight parts, one white streak, drawn round its centre, wrapped in
  `sticker()`, popped with `popIn()`, sized to the slot (Composition), with an idle motion and a reaction on its word
  (in the demo: the bells ring with white marks, the phone shakes and flashes red, each list icon pops).
- The presenter is footage, not a character, and never acts. The stand-in bust is blurred and faceless so it passes
  for footage; real footage or a photo of the user (a data URI) replaces `BG` and `FIG` as shot, with the grain on
  top; with no presenter, any soft shot works.

## Composition and camera
- One caption line, always in the same place: centred, in the lower third, on the presenter's chest and never over
  the face, so the eye never searches. Above it, centred, the face or the sticker; the caption is the top layer and
  may cross a sticker only during a pop or a swipe. Nothing else on screen: no titles, logos or lower thirds.
- 16:9 (the demo): caption baseline `CAPY` 850 on x 960, ink at y 658–877; head at (960, 412); stickers centred
  near (960, 400), settled within y 75–680, a set of three in a row (x 520, 960, 1400). The 580 px phone touches
  GONE. (a 1.4× word): keep settled stickers above y 650.
- Camera (`drawScene()`): zoom 1.04 + 1.2 %/s (speaker) or 1.0 + 0.6 %/s, plus `punch()` (halved on cutaways) and a
  cut `snap`, round (960, 430) or (960, 420); `shake()` offsets the scene, captions 35 %.
- 9:16 (1080 × 1920; all shots rendered at their widest moment):
```js
// canvas width="1080" height="1920"; const W = 1080, H = 1920
// buildTextures(): open a block after `const R = rng(46);` with `{ const W = 1920, H = 1080;` and close it before
//   `VIG = mk(W, H);` so BG and FIG are built at 16:9 (the grain stream stays the same)
// drawSpeaker(): cover-scale the plates; the BG size becomes literal
const K = H / 1080; x.save(); x.translate(W / 2, 0); x.scale(K, K); x.translate(-960, 0);
x.drawImage(BG, -30 + Math.sin(t * .7) * 8, -30, 1980, 1140);
x.drawImage(FIG, Math.sin(t * 1.3) * 7, Math.sin(t * 2.1) * 4 + nod);
x.restore();
const BASE = 120, CAPY = 1300, GAP = .3, MAXW = 800;   // layout(): let x = W / 2 - tot / 2;
// drawScene(): fx = W / 2, fy = 764 (speaker) or 720;  burst(): cx = 540, cy = 720
// drawClock(): translate(540, 700), twice;  drawPhone(): translate(540 + …, 678), scale(s * 1.2, s * 1.2),
//   hearts x0 = 540 + side * (240 + R() * 180), y = 1080 - u * 800
// world() iris: arc(540, 720, …) twice, rad = 20 + 1340 * u
// icons in a column: ICONS rows [fn, t0, 540, y] with y 400, 700, 1000; drawIcons(): for (const [fn, t0, cx, cy] of
//   ICONS), translate(cx, cy + bob …), bob and rock phases from cy instead of cx, scale(s * .7, s * .7)
// optional, captions(): keep an entering word inside the frame (GO EVERYWHERE. then enters at x 1060; no shared ink)
  : lerp(Math.min(PE + gap + ws[i] * f / 2, W - 20 - ws[i] * f / 4), A[i], u)
```
- 9:16 checked in every shot (TIME. 1.48, clock 2.07, 24 HOURS. 2.62, SCROLLING. 4.07, swipe 4.75, GONE. 5.92, BACK.
  6.87, iris 7.32, BUILD. 8.17, TODAY. 8.97 s): each shows S1, S2 when its chunk has a keyword, S5, and S3 or S4,
  whole. Captions at x 127–950, y 1158–1319, clear of review.md's bands (a new word starts at the old line's right
  edge, so for its first frame it passes x 950 by 30–120 px, and a long word after a short one starts past the frame
  edge, at x 1117 for GO EVERYWHERE.; keywords then stay 2–15 px past 950 for up to 0.17 s from overshoot and shake;
  settled lines end at x 949). Settled stickers at x 271–823, y 277–1148; no shared ink between words; torso and
  grain, or rays, in the bottom band. Smallest fit: TRAIN. READ. BUILD. at 0.56 (67 px, 70 px for the 1.05× items).
- 1:1 (1080 × 1080, rendered): all the 9:16 edits (the plate block, `drawSpeaker()` with K = 1, `W / 2` in
  `layout()` and as `fx`), with these values: `BASE` 130, `CAPY` 900, `MAXW` 860, `GAP` 0.3; fy 430 or 420; burst
  and iris at (540, 420), rad = 20 + 850 × u; clock at (540, 400); phone at (540, 378), scale 1; hearts x as 9:16;
  icons in a row at x 230, 540, 850, y 410, scale 0.55. Stickers settle at y 75–680, captions y 747–920.
- Stand-in (bakery copy, a 300 × 640 jar replacing the clock): in 9:16 it fits at scale 1 at (540, 700), y 347–1029;
  in 16:9 it crossed the caption line, so scale 0.85 at (960, 380). Subject-dependent: each sticker's scale and centre,
  the icon layout (their count), fy (the face of real footage); `BASE`, `CAPY`, `MAXW` and the plates did not change.

## Motion
- Easing: `eBack()` (back-out) for every pop: plain words 0.5 → 1 in 0.14 s (peak 1.07×), keywords 0.25 → 1 in
  0.22 s (peak 1.11×, damped by 300 px over the word's width) while dropping 30 px and untilting −0.06 rad, stickers
  through `popIn()` in 0.34–0.36 s (peak 1.18×), `punch()` in 0.1 s (5 % over); `eOut()` for the line's re-centring
  (0.11 s; a new word enters from the old line's right edge) and the iris; `eInOut()` for swipes and the fade.
- Camera: a punch-in of 0.03–0.16 (the sixth `WORDS` field) per keyword, held to the chunk's end and reset like a
  jump cut; a shake of 10, 16 (punch ≥ 0.12) or 22 px (red) decaying in 0.11 s; a nod of 3.5 px per word, 12 px per
  keyword (`nod`, 0.25 or 0.5 s).
- Transitions: hard cut (zoom +10 % easing out in 0.16 s and a one-frame 35 % white flash), swipe up (`SWIPE` 0.24 s,
  a dark seam), iris from the sticker centre with a yellow ring (`IRIS` 0.3 s). Rotate them; the cut is the default.
- Idle motion: rays turn, the plate drifts and sways, stickers jitter, bob or rock (in the demo: clock hands, a feed).
- Never: letter-by-letter typing, words travelling across the frame, captions animating out between chunks (only the
  closing shrink-and-fade), two caption lines, crossfades, a fade as a caption entrance (only the film fades in from
  black).

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.3 | fade in from black on the presenter | `render()` → `blk` |
| 0.40–1.36 | hook in two chunks; TIME. pops in yellow with punch, shake and a boom | `WORDS`, `captions()`, `punch()` |
| 1.90–3.05 | hard cut to the clock on blue; two chunks; 24 HOURS. in green, the bells ring | `SC`, `drawClock()`, `ringA` |
| 3.05–4.60 | cut back; YOU NEED, LESS (yellow 1.3×), SCROLLING. (green 1.35×, biggest punch) on a riser | `drawSpeaker()` |
| 4.60–6.30 | swipe up to the phone on red; three chunks; GONE. in red, the phone shakes and flashes | `SWIPE`, `drawPhone()`, `gone` |
| 6.30–7.20 | swipe back; TAKE THEM BACK. | `world()` |
| 7.20–8.55 | iris to violet; TRAIN. READ. BUILD. as karaoke, each icon popping on its word | `IRIS`, `KARAOKE`, `ICONS`, `drawIcons()` |
| 8.55–9.4 | cut back; START TODAY. with a chime | `SC` |
| 9.4–9.95 | captions shrink 12 % and fade, the bar fades, black from 9.9 | `FADE0`, `progress()` |

- A scene is a run of chunks over one picture: speaker shots 0.9–1.9 s, cutaways 1.1–1.7 s with one to three chunks.
  Reusable: the hook on the presenter, a hard-cut or swiped cutaway, a sticker reacting on its word, the iris into a
  karaoke list, the call to action with a chime, the shrinking fade. Plot: the words, the stickers and their reactions.
- Keys: `KEYS=1.6,2.9,4.3,4.72,6.05,7.3,8.35,9.3 bash <skill>/scripts/contact_sheet.sh <dir>` (payoff, cutaway,
  biggest keyword, swipe, red word, iris, list, final chunk).
- The demo never holds a settled ending: TODAY. lands at 8.85 s and its shake runs into the fade at 9.4 s; with the
  shake taper it settles at 9.367 s. Fixes in Shorter.

## Sound
audio.py reads `events.json` (a list of `{t, k, …}`) and synthesizes 48 kHz stereo with NumPy, through a tanh limiter.
- Per word: `pop` (a blip and click) for every plain word; `hit` (`v`), a sub boom and snap, for every keyword (`v`
  1.2 for a punch of 0.12 or more, 0.7 below 0.05, else 1), dipping the bed to 35 % for 0.45 s (`duck`).
- By role: `whoosh` (`d`) before a cut into a cutaway or an iris; `cut` (a thump) on a cut back to the presenter;
  `swipe` (`d`) before a swipe; `riser` (`d`) ending on the biggest keyword; `boing` per sticker popping on its word;
  `ding` (a chime) on the call to action's keyword. Optional, demo objects: `tick` (`d`, clicks 0.085 s apart),
  `ring` (`d`, an alarm), `flicks` (`d`, every 0.22 s), for any timer, alarm or scroll.
- `bed` (`d`, at 0.2 s for `DUR` − 0.2): lo-fi pads from `chords` (Am7, Fmaj7, Cmaj7, G7, 2.4 s each, counted from
  the cue, not the words), sub bass, a kick every 0.6 s, hats between. Fixed: `DUR`, `fi` (0.1 s), `fo` (0.6 s).
- No cue is looked up by name, but `window.events()` indexes `SC[1]`–`SC[6]` and writes 2.5, 3.27 and 8.85: with
  fewer scenes events.mjs throws. A role-based version (tested in the plans):
```js
window.events = () => {
  const ev = [{ t: .2, k: 'bed', d: DUR - .2 }];
  for (const w of WORDS) ev.push(w.hl ? { t: w.t, k: 'hit', v: w.z >= .12 ? 1.2 : w.z < .05 ? .7 : 1 } : { t: w.t, k: 'pop' });
  for (const s of SC.slice(1)) ev.push(s.tr === 'swipe' ? { t: s.t0 - .04, k: 'swipe', d: .3 } :
    s.tr === 'iris' ? { t: s.t0 - .05, k: 'whoosh', d: .34 } : s.k === 'spk' ? { t: s.t0, k: 'cut' } : { t: s.t0 - .12, k: 'whoosh', d: .3 });
  if (SC.some(s => s.k === 'icons')) for (const [, t0] of ICONS) ev.push({ t: t0 - .02, k: 'boing' });
  const last = HITS[HITS.length - 1]; if (last) ev.push({ t: last.t, k: 'ding' });
  return ev.filter(e => e.t >= 0);   // add tick, ring, riser, flicks by role
};
```
- Breaks (tested): `bed`, `whoosh`, `swipe`, `tick`, `ring`, `riser` or `flicks` without `d` (KeyError); `whoosh`,
  `swipe` or `riser` with `d` under one sample (ValueError); `bed` with a negative `d`; a `bed` before 0 s, or a `hit`
  less than 0.45 s before 0 (ValueError); a `hit` 0.45 s or more before 0 does not fail but ducks the film's last
  0.45 s (the role-based version's `filter(e => e.t >= 0)` prevents both); a cue without `t` or `k`. Other single
  sounds before 0 s and unknown kinds drop silently; `tick` and `flicks` keep the clicks after 0. Pans are constants
  (up to 0.6) or seeded within ±0.3, so no field makes NaN; `v` scales gain and decay (keep 0.7–1.2); any `DUR` works.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Caption engine | `anim.html` → `captions`, `measure()`, `layout()`, `GROUPS` | `WORDS` rows [word, time, chunk, highlight 'y'/'g'/'r', size ×, punch]; `BASE`, `CAPY`, `GAP`, `MAXW` | as is; new rows, values per format |
| Highlight colours, list mode | `HL`, `YEL`, `GRN`, `RED`, `KARAOKE` | `KARAOKE` holds chunk numbers whose earlier items turn white | as is |
| Camera | `anim.html` → `shake`, `punch()`, `drawScene()` | `shake(t)` from `HITS`; `punch(t)` sums the chunk's punches | adapt: taper the shake |
| Easing and helpers | `eBack()`, `eOut()`, `eInOut()`, `seg()`, `lerp()`, `clamp()`, `rng()`, `mk()` | `eBack(u, c)`: back-out, c sets the overshoot | as is |
| Footage plate | `anim.html` → `buildTextures`; `drawSpeaker()`, `BG`, `FIG`, `VIG` | built once; nod per word | as is, or the user's footage still |
| Grain, fades, bar | `world()`, `GRAIN`, `render()`, `progress()`, `FADE0` | captions fade over `FADE0` to `DUR` − 0.1 | as is |
| Sticker kit | `anim.html` → `sticker`, `shp()`, `MODE`, `C()`, `INK`, `popIn()` | `shp(x, path, fill, lw)`; `sticker(x, draw)`; `popIn(t, t0, d)` | as is |
| Sunburst | `anim.html` → `burst` | `burst(x, base, ray, t, cx, cy)` | as is; a new hue per cutaway |
| Scenes and transitions | `SC`, `sceneAt()`, `world()`, `DRAW`, `SWIPE`, `IRIS` | `SC` rows { k, t0, tr: 'cut', 'swipe' or 'iris' } | as is; new rows |
| Demo cutaways | `drawClock()`, `drawPhone()`, `card()`, `heart()`, `drawIcons()`, `dumbbell()`, `book()`, `moneyBag()`, `ICONS`, `FEEDCOL` | `ICONS` rows [drawer, time, x] | replace; keep as models |
| Timeline and cues | `WORDS`, `SC`, `FADE0`, `window.events` | | replace |

## Adapting
- **Style vs demo plot:** style: S1–S5, punch and shake on keywords, the colour roles, cut, swipe and iris, sticker
  reactions, the karaoke list, the call to action and shrinking fade, the ducked bed with pops and booms. Plot: the
  script, the screen-time topic, the clock, phone, hearts and icons. The transformation: a cutaway or a reaction.
- **New subject:** write `WORDS` (chunk numbers from 0 in time order, without gaps, or building `GROUPS` throws),
  new stickers per claim, new `SC` rows and sunburst hues. Two edits first, tested: taper the shake, and time each
  cutaway's pop from its own start (`popIn(lt, 0, .36)` in `drawClock()`, `popIn(lt, .08, .36)` in `drawPhone()`).
  The literals `t > 2.5` (ring) and `t > 5.8` (red flash) are demo word times; their decays never end, so taper them
  as below when a film ends on a cutaway.
```js
// shake(): each hit's jitter reaches exactly zero 0.45 s after its word (it otherwise decays until cut at 0.6 s)
if (a < 0 || a > .45) continue;
const amp = (w.hl === 'r' ? 22 : w.z >= .12 ? 16 : 10) * Math.exp(-a / .11) * (1 - seg(a, .3, .45)), s = w.t * 13.7;
// drawClock(): the reaction ends 0.5 s after its word (2.5 in the demo; the red flash in drawPhone() the same, with .25)
const ra = t - 2.5, ringA = ra < 0 || ra > .5 ? 0 : Math.exp(-ra / .35) * (1 - seg(ra, .3, .5));
// after FADE0: report a final hold under 24 frames (the last word settles 0.5 s after it lands: the nod)
const SETTLE = WORDS[WORDS.length - 1].t + .5;
if (FADE0 - SETTLE < .8 - 1e-6) console.error(`final hold ${(FADE0 - SETTLE).toFixed(2)} s, under 0.8 s`);
```
- **Length:** past 10 s keep the density (a scene change every 0.9–1.9 s, a keyword every 0.4–1 s), rotate transitions
  and hues; past about 20 s leave some punches at 0. Set `DUR` in anim.html, audio.py and build.sh; bed, ducking and
  bar follow. Not rendered past 10 s.
- **Shorter:** re-time `WORDS`, `SC`, `ICONS`, `KARAOKE`, the ring and flash literals, `FADE0` and `DUR` only;
  drift, push, rays and idle loops stay on film time. Ending rule: settle = last word + 0.5 s, `FADE0` ≥ settle +
  0.8 s, `DUR` − 0.05 − `FADE0` ≥ 0.25 s (to 96 % black). Ambient through the hold: the progress bar (the film's
  clock), plate drift and push, grain, rays, idle sticker motion; actions: pops, slides, punch, shake, nod, snaps,
  swipes, irises, sticker reactions. The call to action costs about 1.85 s from its first word to black. From 6 to
  10 s keep the speaker–cutaway alternation and cut chunks; under 6 s cut whole beats: first the swiped cutaway, then
  the iris list, then the second speaker run; keep the hook with a keyword, one hard-cut cutaway and the call to
  action. Shortest opening: 0.3 s fade-in, a word at 0.35 s, S1–S3 and S5 by 1.41 s, S4 at 1.62 s. A dropped scene
  takes its `SC` row and cues (the demo's events emit a `boing` per `ICONS` row regardless) and renumbers `KARAOKE`.
  Plans (holds by pixel difference, no shared ink, `python3 <skill>/scripts/check_audio.py audio.wav 4` and 7.5, 10):
```
all: shake taper, lt pops, role-based window.events(); DUR the same in anim.html, audio.py, build.sh
10 s, the demo's copy with its ending fixed (16:9, 9:16): iris SC t0 7.05; TRAIN., READ., BUILD. and ICONS at 7.17,
  7.45, 7.73; cut 8.05; START 8.08, TODAY. 8.30; FADE0 9.62. Settled 8.80, first faded frame 9.633: 0.83 s
7.5 s, no phone beat (9:16, 16:9), WORDS times: .35 .57 .79 / 1.02 1.26 TIME. / 1.86 2.08 / 2.34 24 HOURS. /
  2.86 3.08 / 3.32 LESS / 3.72 SCROLLING. / 4.42 4.70 4.98 the list (chunk 7, KARAOKE 7) / 5.40 5.62 TODAY.
  SC: clock cut 1.80, speaker cut 2.86, icons iris 4.30, speaker cut 5.36; ring literal 2.34; FADE0 7.1
  settled 6.133, first faded 7.133: 1.0 s; audio peak 0.681
4 s (9:16, 16:9): YOU .35 DON'T .55 NEED .75 / MORE .97 TIME. 1.19 / 24 HOURS. 1.68 (chunk 2) / START 2.10
  TODAY. 2.30; SC: clock cut 1.62, speaker cut 2.08; ring literal 1.68; KARAOKE empty; FADE0 3.62
  settled 2.80, first faded 3.633: 0.83 s; audio peak 0.659. In 16:9 the clock's pop overshoot meets 24 HOURS.
  for 0.17 s (1.73–1.9 s), a caption crossing a sticker mid-pop; 9:16 is clear
```
- **Other formats:** Composition's 9:16 and 1:1 values; timing, cues and plans carry over. In 9:16 chunk to two short
  words; the plans keep the demo's three-word chunks (0.56–0.71 in 9:16) only so they stay comparable with the demo.
  Start a swiped cutaway's first word 0.24 s or more after the swipe (the demo's THAT'S pops over the incoming phone).

## Boundaries
- **Distinct from:** `kinetic-typography`, where the phrase is the whole picture (contrasting families on paper, words
  travelling, colliding and regrouping, no camera); here one outlined line overlays footage in a fixed place, words
  pop in place and the camera moves. `chat-story` uses message bubbles, `product-ui` app screens, `neo-brutalism` UI
  cards; `kawaii` stickers are characters, here B-roll; `mascot-beat-reel` stamps one label per beat-cut scene.
- **Poor fit:** many numbers (`data-visualization`), step-by-step processes (`whiteboard`, `infographic`), calm or
  premium brands (`liquid-glass`), character stories (`storytime`), a quote as typographic art (`kinetic-typography`).
- **Do not:** use real creators' faces, names, logos or platform interface (logos, like buttons); add emoji (not in
  the font: draw a sticker); put two keywords (a karaoke list excepted) or more than three words in a chunk; put
  captions over the face or at the top; give stickers gradients or 3D shading.

## Technical notes
- Canvas 2D, no render.json, no vendored library, one font file; 26 stills render in about 2 s on one page. `DUR` is
  used in anim.html (bar, fade, last scene, bed cue): change it with audio.py and build.sh.
- Hard-coded sizes: the canvas tag; plate coordinates in `buildTextures()`; `W + 60`, `H + 60` in `drawSpeaker()`;
  960 in `layout()`; `fx`, `fy`; `burst()`'s centre; (960, 400) twice in `drawClock()`; 960, 378, 760 in `drawPhone()`;
  `ICONS` x and 410 in `drawIcons()`; the iris centre (twice) and 1200; `BASE`, `CAPY`, `MAXW`; `SH` (`W` × `H`).
- Deterministic (seeded `rng()`, a seed per frame for grain; audio.py's `default_rng(46)` in cue order): the test
  passes on the 9:16 version, the stand-in and the 4 s plan. `drawPhone()` assigns `globalAlpha` (hearts, feed
  copies), so a `globalAlpha` scene fade would miss them; the style fades with the black overlay in `render()`.

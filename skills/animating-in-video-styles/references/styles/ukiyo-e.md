# Ukiyo-e (`ukiyo-e`)

An Edo-period woodblock print made on screen: the key block is rubbed onto washi, then colour blocks land one by one,
off register, in a few flat inks with graded skies. It draws on 18th–19th-century landscape prints (bold outlines,
bokashi, mist bands, a titled cartouche, a red seal) without copying any; the mood is calm and crafted.

**Reference film:** a dawn sea print is pulled, a tall wave breaks and its spray turns into plovers, a dusk print with
a snowy peak is rubbed in behind them, its cartouche prints and a seal is pressed · `styles/ukiyo-e/`

## Signature
- Warm washi (`PAPER`) with the picture inside a thin sumi border (`FRAME`), the margin always showing; the film
  opens on the bare sheet and fades back to it.
- The print is pulled on screen: the key block's black lines are rubbed in left to right behind a streaky baren edge
  (0.06–0.78 s), then five colour blocks land one after another (0.86–1.76 s), each dropping into place off register.
- Flat inks multiplied into the paper, streaked by wood grain: Prussian blue and indigo sea, beni-red sun, straw
  cartouche, pink mist edges. The only gradients are bokashi bands (top of the sky, deepening sea, base of a form).
- Bold sumi key lines of varied weight over the colour, and every white is bare paper: foam as outlined paper blobs,
  near swells as rows with three-blob crests, far waves as hook marks, mist bands (kasumi) as paper bars cut out of
  the colour with a pink lower edge, one of them across the lower part of the sun.
- A cartouche in a top corner: straw panel, beni band, double sumi border, a Zen Antique title, a paper-coloured
  small-caps band line and a date. The second print adds the red seal as the sign-off.

## Palette
| Role | Colour | In code |
|---|---|---|
| Washi sheet and page background | `238, 226, 199` / `#eee2c7` | `PAPER_RGB`, `makePaper()` |
| Sumi: key lines, letters, border | `#241e1a` | `INK.sumi` |
| Prussian blue: wave body, near row | `#22527f` | `INK.prussian` |
| Indigo: front row; wave base and top of the dawn sky | `#1c2f52`; `rgba(28,47,82,0.92)`, `rgba(30,48,86,0.94)` | `INK.indigo`, `waveInk()`, `scene1()` |
| Day sea; far landmass | `#9fbdd0`; `rgba(118,136,158,0.75)` | `scene1()` |
| Pale stripes in wave and rows; wave highlight | `rgba(183,207,224,…)`, `rgba(170,198,218,…)`; `rgba(126,170,202,0.95)` | `waveInk()`, `rowInk()` |
| Beni red: suns, cartouche band, glitter | `#c9452f` | `INK.beni` |
| Straw: cartouche panel | `#eed88f` | `INK.straw` |
| Mist edge | `rgba(234,180,161,0.9)` | `tintMist()` |
| Island: earth, bark, pine, moss | `#a1805a`, `#6b4b35`, `#3f5d48`, `#728856` | `INK.earth`, `INK.bark`, `INK.pine`, `INK.moss` |
| Dusk sky: indigo top, pink and orange horizon | `rgba(28,44,82,0.95)`; `rgba(234,170,148,0.75)`, `rgba(214,112,80,0.9)` | `scene2()` |
| Peak: slate body, blue crown | `#7186a1`; `rgba(30,58,100,0.9)` | `INK.slate`, `scene2()` |
| Dusk sea, top to bottom; sand | `#c4d3d9`, `#86a9c2`, `#2a5683`; `rgba(222,196,140,0.9)`, `rgba(176,140,92,0.95)` | `scene2()` |
| Spray tint; plover wing tips; seal | `rgba(150,186,210,0.45)`; `rgba(52,66,90,0.85)`; `#b22a1e` | `spray()`, `plover()`, `INK.sealRed` |

- Shading is a bokashi band in a form's clip, never modelling. New blocks take these inks (`INK.pale`, `INK.mid` and
  `INK.pink` are unused).

## Typography and copy
- Title: Zen Antique 400 (`fonts/ZenAntique-400-latin.woff2`, `fonts/ZenAntique-400-latin-ext.woff2`), 60 px, centred,
  title case. Band line `SERIES`: Cormorant SC 700, 21 px, 1.5 px spacing, capitals, filled with `paperInk()` on the
  red band (`cartoucheLetters()`). Date `DATES`: Cormorant SC 600, 22 px, right-aligned, small caps. `TITLE` is an
  array of lines drawn by `cartoucheKey()`; put new copy in these constants, which `window.ready` loads fonts for.
- Copy is a print's caption: a short title, a factual series line, a date or number; calm, no slogans. Print one's
  cartouche arrives with its blocks. In print two the panel lands at 6.62 s and the title prints a letter every 0.045 s
  from 6.86 (each fades in over 0.16 s with a 9 px drop, `outC`); the date fades in over 0.2 s from one letter step
  after the last letter (done at 7.375). Text never slides or leaves on its own. Every left-anchored prefix shows
  (rubs from the left, letters in order): check each; the code avoids "JAPAN".
- Widths (`measureText`, real lines). Title: 31–32 px a character, 10 per line ("First Snow" 314 px clears the inner
  border by 16 px; "Night Ferry", 340, touches it); for more, widen the box (all parts follow its `w`). Two lines sit
  at 126 and 192 px below the box top: make `h` 270 and move the seal down 32 px (rendered). Band: about 14 px a
  capital, up to 22 (`fillText` squeezes longer text). Date: up to about 14 characters.
- Glyphs: Latin subsets. Zen Antique lacks ł, ő, š, ž, Ğ, İ, Ā and the macrons ō, ū ("Tōkaidō"); Cormorant SC
  has them. Neither has Greek, Cyrillic, №, arrows or Japanese (kana come out in a system Gothic face).

## Texture and finish
- `makePaper()` (once, `seeded(11)`): cream `PAPER_RGB` with noise and cloudy mottling (`cloudField()` every 8 px),
  2800 kozo fibres, 180 specks, a faint aged vignette. `makeGrain()` (once, `seeded(23)`): bowed cherry-grain streaks
  about 30 px apart and baren blots as pale alpha. Both static: every sheet is printed from the same wood.
- `inkOpen()` clears the ink layer and clips it to `FRAME`; blocks are painted there; `inkClose(g)` lays the grain
  `source-atop` (streaks on colour, clean paper) and multiplies the layer onto the sheet. The key block is drawn
  afterwards straight onto the sheet, crisp. Colour drawn straight onto the sheet misses grain, multiply and register.
- `plate()` offsets: sky [0, 0], sea [2, −1], deep [−2, 2], red [3, 1], earth [−1, −2]. `makeEdge()`: the 520 px ramp
  of every rub. `makeSeal()`: a worn square, border, sun and three swells cut out. No bloom or grain pass; the only
  blur is the seal's falling shadow (`makeSealShadow()`).

## Shapes, line and figures
- Key lines: outlines 3.4–4.6 (wave 4.6, island 4, peak 3.6, rows 3.4), border 2.6, details 1.15–2.6, foam unions 6,
  spray 3.2; round caps and joins on most, clean (no wobble). Paths go through `through()` and `trace()`.
- A form is a key outline over flat blocks, with a bokashi band in its clip (darker toward the wave's base and the
  rock's foot) and interior lines parallel to the outline (12 pale and 3 sumi strokes down the wave's face).
- `blobs()` strokes every circle, then fills them all with paper, so only the union's outer edge stays inked: foam,
  spray, the foam ring, the puffs birds hatch from. Build any cloud, snow or surf puff with it.
- Water is pattern: crest rows (`rowY()`) with three blobs per crest, hooks (`farSeaHooks()`) shrinking toward the
  horizon, level ripples. Snow is `SNOW` erased from the peak; sails, plovers, claws are `paperInk()`. Build a white
  shape under a transform, then restore and fill, as `plover()` does, or its paper slides against the sheet.
- Build new objects like the pine (fans from `clumpPath()`, radial needles), boat (hull, paper sail, battens) or plover
  (paper body, sumi outline, dark wing tip). A 9:16 lighthouse stand-in (paper tower erased from the ink, beni bands,
  slate bokashi on its right half, straw lamp, outline 3.6, sumi cap, earth rock) read as part of the print. People:
  none in the demo; keep them small like the boats (sumi outline, paper face, readable head and shoulders).

## Composition and camera
- One fixed print, no camera: no pan, zoom or shake. Depth is flat layers and drift speed: far landmass, hooks slowing
  toward the horizon, near rows at 34 and 50 px/s, mist 5–9 px/s, boats 4–7 px/s.
- 16:9: `FRAME` x 56, y 50, 1808 × 980; horizons at 640 and 642. Print one: cartouche top left (`BOX1`), sun at
  (700, 292) under a mist band, wave crest right of centre, pine island at the right edge. Print two mirrors it: peak
  left of centre, sun at its right foot (1292, 578), shore bottom left, flock high left, `BOX2`, `SEAL_AT` top right.
  The seal sits right-aligned under its cartouche, 26 px below (x = box x + w − 136, y = box y + h + 26).
- 9:16 and 1:1, rendered with the flock fix (Film grammar); Signature checked at every beat, birds probed per frame.
```js
// 9:16, 1080 × 1920. MIST: [x, y, w, h, v]; ROWS1: [base, amp, per, v, off], prussian and indigo alternating; BOATS: [x, y, s, v]
FRAME: { x: 44, y: 56, w: 992, h: 1808 }, HZ1: 900, SKY1: 440, DW: [-580, 330], FAR: [0, 260], island: none, SUN1: [800, 460],
BOX1: { x: 92, y: 300, w: 362, h: 238 }, MIST1: [[560, 486, 600, 40, 9], [250, 190, 520, 34, -7], [40, 800, 680, 34, 6]],
ROWS1: [[1188, 46, 300, 34, 40], [1262, 40, 250, 50, 170], [1356, 60, 380, 42, 90], [1470, 72, 440, 58, 230], [1604, 84, 500, 48, 10], [1752, 96, 560, 66, 300], [1900, 100, 600, 56, 120]],
HZ2: 1100, SKY2: 520, DUSK: 400, DP: [-300, 458], SUN2: [930, 960], DS: [0, 640], GRIT: [1520, 344, 520], RIPROWS: 13,
MIST2: [[20, 924, 560, 38, 7], [600, 980, 560, 40, -6], [100, 420, 300, 26, 5]], BOATS: [[120, 1120, 0.55, 5], [470, 1148, 0.75, 4], [760, 1180, 0.95, 7]],
BOX2: { x: 588, y: 300, w: 362, h: 238 }, SEAL_AT: { x: 814, y: 564 }, SKEIN offsets × 0.8,
FLOCK: [[4.4, 720, 700], [4.85, 760, 520], [5.3, 750, 370], [5.8, 660, 220], [6.4, 440, 200], [7.0, 330, 215], [7.6, 305, 380], [8.4, 300, 500], [10.2, 280, 540]],
// 1:1, 1080 × 1080 (keys not listed stay as in 16:9)
FRAME: { x: 44, y: 44, w: 992, h: 992 }, DW: [-530, 40], island: none, SUN1: [760, 200], BOX1: { x: 88, y: 88, w: 362, h: 238 },
MIST1: [[600, 226, 520, 40, 9], [160, 400, 420, 34, -7], [60, 548, 600, 34, 6]], DP: [-220, 60], SUN2: [960, 590],
MIST2: [[40, 526, 560, 38, 7], [600, 598, 600, 40, -6], [100, 360, 300, 26, 5]], BOATS: [[160, 662, 0.55, 5], [520, 690, 0.75, 4], [800, 722, 0.95, 7]],
BOX2: { x: 630, y: 88, w: 362, h: 238 }, SEAL_AT: { x: 856, y: 352 }, SKEIN offsets × 0.7, birds' launch offset [-600, 40],
FLOCK: [[4.4, 680, 440], [4.85, 700, 290], [5.3, 720, 190], [5.8, 630, 160], [6.4, 380, 170], [7.2, 300, 220], [8.2, 290, 250], [10.2, 280, 270]],
```
  - Set canvas, `W`, `H` and texture sizes (Technical notes). HZ1 replaces print one's 640: sea and deep blocks fill
    from it to `H` (deep gradient HZ1 + 10 → HZ1 + 260), haze HZ1 − 180 → HZ1 + 5; `farSeaHooks()` clips from HZ1,
    rows from HZ1 + 12 (pass 7 rows, not 8, to `farSeaHooks()` in `scene1Key()`: the eighth falls inside the first
    swell row). Sky bokashi `FRAME.y` → SKY1; FAR shifts the far landmass; SUN1 is the sun's `arc()`.
  - DW is added to every `POSE` point, the `y < 860` heave test, the 690/900 gradient in `waveInk()`, the spray launch
    points (1290, 360 and 1110, 270 in `initSpray()`), the foam ring (1440, 800) and the birds' launch (1220, 300 in
    `initBirds()`). No room for the island beside the lip: skip `islandInk()`, `islandKey()` and `ROCK` in the even-odd
    clip of `scene1Key()` and the avoid list of `farSeaHooks()`.
  - ROWS1 is drawn and keyed in a loop (the code names `ROWS1[0]` and `ROWS1[1]`); each 1100 closing a body is `H` + 20.
    HZ2 replaces 642: indigo sky `FRAME.y` → SKY2, pink HZ2 − DUSK → HZ2, sea HZ2 → bottom, glitter from HZ2 + 10
    at SUN2's x, RIPROWS ripple rows from HZ2 + 18, the ripple clip a rect from HZ2 + 4 to the frame bottom (not 400 px
    tall), even-odd with the sand closed at `H` + 20. DP shifts `PEAK`, `SNOW`, the snow streaks and peak gradients;
    stroke the outline in a rect(0, 0, W, HZ2) clip (1:1 puts its foot 60 px under the horizon). DS shifts `SHORE_D` and
    the sand gradient; GRIT is the specks' top, depth and count.
  - 9:16 cartouches sit at y 300–538, x ≤ 950, clear of review.md's bands; the bottom band carries swells, then sand.
    No bird crosses `BOX1` before the change covers it or `BOX2` after it lands (9:16: birds x 103–1007, y ≥ 81, at
    rest x 130–489, y 289–400; 1:1 at rest x 133–455, y 156–259); a full-width skein cannot share the top band with a
    cartouche. In both, the foam ring's right end leaves the frame for about 0.5 s after 4.5 s.
  - Stand-in (a 590 px lighthouse at x 278–402 instead of the peak): everything held but the flock's keys from 6.4
    ([6.4, 460, 190], [7.2, 380, 190], [8.2, 350, 200], [10.2, 320, 210]) and the mist bands, moved to cross the tower.
    Subject-dependent: flock route, mist, sun (keep it off the outline), cartouche corner (opposite the tallest part).

## Motion
- Everything enters by being printed: the key rubbed in (`smooth`, 0.72 s), a new sheet rubbed over the old from the
  right (`inOut`, 0.96 s), both behind `EDGE`; a block lands in 0.26 s (`landing()`: opaque in 0.1 s while dropping
  22 px with `outBack`, about 3 px past its place); letters print; the seal is pressed.
- Eases: `inOut` (rise, sheet change, flock recession, fade), `inC` (lip falls), `outC` (collapse, letters, foam ring),
  `outBack` (pops). The wave morphs between six `POSE` outlines; spray falls 470 px × age²; the flock path is a spline.
- Ambient through every hold: mist, rows, hooks, ripples, boats, a ±5 px heave, glitter, wavelets, and the flock's bob
  and wingbeat (eased to 45 %, 6.2–7.6 s). Its glide along `FLOCK` and its shrink are action: stop them before the
  hold. Smooth 30 fps; never a camera move, shake, glow, motion blur, cross-dissolve, hard cut, sliding text or 3D turn.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.06 | Bare washi | `PAPER` |
| 0.06–0.78 | Key block rubbed in left to right, cartouche title and date included | `wipeMask()`, `EDGE`, `scene1Key()` |
| 0.86–1.76 | Blocks land 0.16 s apart: sky, sea, deep sea and wave, red (sun, band), earth (mist edges, island, panel) | `landing()`, `plate()` |
| 1.7–3.6 | Swell draws back (to 2.2), then rises; foam heads grow 2.5–3.9, claws 3.05–3.9 (gone by 4.6) | `waveAt()`, `POSE` A, B, C2; `waveFoam()` |
| 3.6–4.35 | Lip pitches forward, then falls, flinging spray | `POSE` C, D; `SPRAY`, `spray()` |
| 4.22–5.25 | Collapse to a low swell (by 5.1), a foam ring swells and sinks; 4.3–4.8 the last spray becomes 11 plovers | `POSE` E, `spray()`, `BIRDS`, `birdAt()` |
| 5.06–6.02 | Dusk sheet rubbed in from the right, behind the flock | `render()`, `wipeMask()` |
| 6.02–10 | Dusk print; the flock recedes (to 8.4), slows to a glide and keeps gliding | `scene2()`, `depth` |
| 6.62–7.4 | Cartouche two lands; title prints letter by letter; date | `landing()`, `cartoucheKey()` |
| 7.5–8.13 | Seal shadow comes down; pressed at 7.93, settled by 8.13 | `SEAL_SHADOW`, `SEAL`, `SEAL_AT` |
| 9.2–9.97 | Fade back to the blank sheet | `render()` |

- Grammar: bare sheet; pull the print (1.7 s); one event (3.5 s); rub in the next sheet; cartouche; seal; hold; fade.
- Holds are measured on the canvas against the same moment with every action (cartouche, letters, seal, the flock's
  travel and shrink) forced to its state at the fade, ambient kept; settled = identical pixels. The demo never settles:
  at 9.2 s the flock still glides to `FLOCK`'s last key (10.2 s) and `depth` still shrinks (over 5,300 px differ
  at every frame from 8.0 s). With this change it settles from 8.33 s, a 0.87 s hold:
```js
const F = flockAt(t <= 7.2 ? t : 7.2 + 1.1 / 3 * outC(span(t, 7.2, 8.3)));  // birdAt(): eased stop at 8.3, no jump in speed
const depth = t => mix(1, 0.7, inOut(span(t, 6.0, 8.3)));                    // the 8.4–10 shrink removed
// drawBirds(): once the route has turned for good (5.8 s here) every bird faces its way, left (flip both signs for a flock
// flying right), so leaders drifting back as the skein closes up and stopped birds never mirror; tilt ignores the bob
if (t >= 5.8) facing = -Math.max(0.55, -facing); else if (Math.abs(facing) < 0.55) facing = facing < 0 ? -0.55 : 0.55;
const tilt = clamp(Math.atan2(o.vy, Math.max(Math.abs(o.vx), 50)), -0.25, 0.25);
```
- Review keys for contact_sheet.sh: 1.8 (print pulled), 3.9 (wave tallest), 4.4 (break), 5.5 (mid change), 8.5 (seal).

## Sound
audio.py reads `events.json` (cues with a time `t` and kind `k`) and synthesizes 48 kHz stereo from noise and sines
(seed 183), `DUR` 10.0. Every kind takes `v` (gain, default 0.5):
- `koto` (`n`, semitones above `BASE`, D4): plucked string with a press-bend. `tok` (`f`): wood block. `rub` (`d`):
  the baren. `sea` (`d`): surf bed, 0.8 s in, 1.2 s out over its own `d`. `swell` (`d`): rising noise. `crash`;
  `taiko` (`f`); `hiss` (`d`): spray. `peep` (`f`): two-note plover call. `tick` (`f`): a letter. `stamp`; `rin` (`f`).
- Demo cues, all literal times in `window.events`: `sea` 0 (`d` 10); `rub` 0.1 and a `tok` for the key; a `tok` and a
  `koto` per block (n 0, 3, 5, 7, 12); `swell` 1.72 (`d` 2.5); a rising `koto` run 2.3–3.56 (n 0, 1, 5, 7, 8, 12, 13);
  `hiss` 4.1, `crash` 4.12, `taiko` 4.28; a `peep` per bird, two more at 4.95 and 5.25; `rub` 5.04 (sheet change); a
  falling `koto` line 6.1–7.5 (12, 8, 7, 5, 3); `tok` 6.66 (panel); a `tick` per character of `TITLE.join('')` from
  6.88; `stamp` 7.93, `rin` 7.96; the closing `koto` pair 8.6 (n 0) and 8.95 (n 7).
- Music is cued, no cue is looked up by name, and nothing is written at fixed times but the 0.8 s master fade (`fade`)
  at the end of `DUR`. Re-time the cues, `DUR`, the `sea` cue's `d`; keep the falling line before the stamp, the
  closing pair after it, nothing after the pair.
- Breaks (tested): a kind missing from `GEN` raises KeyError (not skipped), as does a missing `n` (`koto`), `f` (`tok`,
  `taiko`, `peep`, `tick`, `rin`) or `d` (`rub`, `sea`, `swell`, `hiss`). A `d` ≤ 0 raises ValueError; a negative `t`
  too while the sound is longer than |t|, else it wraps to `DUR` + t (a `tok` at −1 plays at 9.0). Cues at or past
  `DUR` are dropped silently.
- `PAN` pans randomly in fixed ranges: no field can make one NaN. The mix is normalised (peak always 0.732), so a huge
  `v` only quietens the rest. `koto` above n ≈ 40 aliases. Under 8 s the 0.8 s fade eats the last notes: use
  `fade = int(0.4 * SR)`.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Washi, wood grain, rub edge | `anim.html` → `makePaper` | `makePaper()`, `makeGrain()`, `makeEdge()` once in `window.ready` into `PAPER`, `GRAIN`, `EDGE` | as is; sizes in Technical notes |
| Colour pipeline | `anim.html` → `inkOpen` | `const gi = inkOpen()`, blocks into `gi`, then `inkClose(g)` | as is |
| Landing block | `anim.html` → `plate` | `plate(gi, landing(t, t0), [dx, dy], p => …)`: null before t0, `SETTLED` without t0 | as is |
| Rub and sheet change | `anim.html` → `wipeMask` | `wipeMask(front, revealLeft)` into `maskC`; key: `destination-in` on `keyC`; sheet: `source-in` with `twoC` (see `render()`) | as is |
| Paper whites | `anim.html` → `paperInk` | `paperInk(g)` as fill or stroke, at identity transform | as is |
| Outlined paper blobs | `anim.html` → `blobs` | `blobs(g, [{ x, y, r }], lw, tint)` | as is |
| Mist bands | `anim.html` → `eraseMist` | `eraseMist(gi, list, t)`, `tintMist(gi, list, t, colour)`, list of { x, y, w, h, v }; clip key lines per piece as `scene2()` does | as is; new positions |
| Water | `anim.html` → `rowInk` | `rowInk(gi, r, t, stripes ≤ 4)`, `rowKey(g, r, t, foam)`, r = { base, amp, per, v, off, col }; `farSeaHooks(g, t, rows, avoid)` | as is; hooks' 640 adapt |
| Cartouche | `anim.html` → `cartoucheKey` | blocks `cartoucheInk(gi, b)`, `cartoucheBand(gi, b)`; `cartoucheLetters(g, b)`; `cartoucheKey(g, b, lines, num, t, t0)`: letters from t0, all at once without it | as is; new `TITLE`, `SERIES`, `DATES` |
| Seal | `anim.html` → `makeSeal` | the stamp block at the end of `scene2()`, at `SEAL_AT` | as is; carve your own abstract mark |
| Plover, flock | `anim.html` → `plover` | `plover(g, x, y, s, facing, tilt, flap)`, facing's sign = direction; `FLOCK` [t, x, y], `SKEIN`, `birdAt()`, `depth` | adapt: route, eased stop |
| Sounds | `audio.py` → `koto` | cue kinds in Sound | as is; `DUR` |
| The demo | `POSE`, `waveAt()`, `islandInk()`, `scene1()`, `scene2()`, `PEAK`, `SNOW`, `render()`, `window.events` | | replace |

## Adapting
- **Style vs demo plot:** the style is everything in Signature plus the rubbed sheet change, the seal and the fade to
  paper. Plot: the wave, spray into plovers, dawn to dusk, island, peak, boats, the copy. A transformation: a sheet
  change (hour, season, place), something rising, breaking or arriving, one thing turning into another.
- **New subject:** text only in cartouches. No timeline table: times are literals in `waveAt()`, `foamSize()`,
  `waveFoam()`, `initSpray()`, `spray()`, `initBirds()`, `FLOCK`, `depth`, `drawBirds()`, `render()`, `scene1()`,
  `scene2()` and `window.events`. Traps: colour outside the ink layer, white paint (use `paperInk()`), key lines in mist.
- **Length:** a sheet carries 3–5 s with one event. Past 10 s repeat the middle branch of `render()` (next sheet into
  `twoC`, `wipeMask()` from the right) at each change; one seal, at the end. Extend `FLOCK` (birds halt at its last key
  at full speed): end it with the eased stop and guards, 0.8 s or more before the fade:
  `flockAt(t <= A ? t : A + (B - A) / 3 * outC(span(t, A, B)))` keeps the speed at A and halts at B, at route time
  A + (B − A) / 3 (7.57 s in the demo); later keys only steer the curve. Re-time cues, `DUR`, `sea`'s `d`.
- **Shorter:** from 6 s to 10 s keep both prints; shorten holds, the rise and the gap before the cartouche (6 s plan:
  rub 0.47 s, blocks 0.1 s apart, title 0.45 s, seal approach 0.27 s). Under 6 s cut the second print, then the
  plovers. The signature is complete when the blocks are down (1.05 s in the 4 s plan; no fade-in). A title card costs
  0.24 s from landing to first letter, 0.045 s a letter, 0.2 s for the date (0.755 s for "Ukiyo-e"), then 0.8 s held.
  Drop a beat's cues and draw calls with it (flock: `peep` and `drawBirds()`; change: `rub` 5.04, the falling line).
  Both plans map film time to demo time for actions and cues only; ambient drift keeps film time:
```js
const KNOTS = [[0, 0], [0.55, 0.84], [1.15, 1.76], [1.35, 2.2], [2.2, 3.6], [2.4, 3.95], [2.7, 4.35], [3.1, 5.06], [3.7, 6.02],
  [3.95, 6.62], [4.4, 7.375], [4.45, 7.5], [4.72, 7.93], [4.9, 8.4], [5.72, 9.2], [6.0, 9.97], [6.05, 10]];   // 6 s: [film s, demo s]
// 4 s: [[0, 0], [0.5, 0.84], [1.05, 1.76], [1.2, 2.2], [1.85, 3.6], [2.0, 3.95], [2.25, 4.35], [2.75, 5.25], [4.0, 6.5]]
function lerpK(x, a, b) { const K = KNOTS; if (x <= K[0][a]) return K[0][b];
  for (let i = 1; i < K.length; i++) if (x <= K[i][a]) return K[i - 1][b] + (x - K[i - 1][a]) / (K[i][a] - K[i - 1][a]) * (K[i][b] - K[i - 1][b]);
  return K[K.length - 1][b]; }
const toDemo = t => lerpK(t, 0, 1), fromDemo = t => lerpK(t, 1, 0);
// window.draw: AOFF = t - toDemo(t); render(toDemo(t)); AOFF = 0. Add AOFF to the time of the ambient terms only: mistPath(), the
// MIST2 clip in scene2(), rowPts(), rowKey(), farSeaHooks(), waveAt()'s heave and sway, glitter, boatShape(), ripples, wavelets,
// birdAt()'s bob, drawBirds()'s wingbeat. Cues: t -> fromDemo(t), d -> Math.max(0.05, fromDemo(t + d) - fromDemo(t)), sea's d -> DUR.
// 4 s only: scene1() alone (no change, no drawBirds()), no cues from the peeps on; in spray() use
// life = Math.min(s.life, 5.25 - s.te) for both the age test and the radius;
// the seal block becomes stampSeal(g, t, at, t0, near, settle): t0 for 7.5, t0 + near for 7.93, t0 + near + 0.04 for 7.97 (the ink
// ramp), t0 + near + settle for 8.13; call it after scene1() with film time, then fade to PAPER over 3.72–4.0 film time (inOut).
```
  - 6 s, 16:9 (rendered; `DUR` 6.0, `fade` 0.4 s, peak 0.732): rub 0.04–0.51; blocks 0.56–0.98; swell back from 1.11,
    rises 1.35–2.2, falls 2.4–2.7, collapses by 3.13; birds from 2.66; change 3.1–3.7; panel 3.95, letters from 4.09;
    seal 4.72. With the flock fix, settled from 4.9 (4.867 differs in 50 px by ≤ 9 levels); fade 5.72–6.0, 0.82 s held.
  - 4 s, 9:16 (rendered; `DUR` 4.0, `fade` 0.4 s, peak 0.732): rub 0.04–0.46; blocks 0.51–0.9; rise 1.2–1.85; break
    2.0–2.25; collapse and ring to 2.75; seal at (318, 564), t0 2.4, near 0.3, settle 0.2, pressed 2.7. Settled from 2.9
    (2.867 differs by ≤ 6 levels); fade 3.72–4.0, 0.82 s held (one frame of slack: anything added must come out of the
    collapse or the seal's approach). Cues: the mapped ones, then `stamp` 2.7, `rin` 2.73, `koto` n 0 at 3.05 and
    n 7 at 3.3. The break is the transformation.
- **Other formats:** see Composition. Sky and sea stretch; crop the wide wave and peak at the frame edge, never scale.

## Boundaries
- **Distinct from:** `ink-wash` (sumi-e brush and washes, no key block); `chinese-scroll` (silk handscroll, mineral
  greens, unrolling sideways); `linocut` (carved black and red relief, no bokashi); `risograph` (fluorescent halftone).
- **Poor fit:** charts (`data-visualization`), loud social hooks (`bold-captions`), interface demos (`product-ui`),
  inner workings (`blueprint`), character gags (`comic-strip`).
- **Do not:** reproduce a famous print or its layout: Hokusai's Great Wave (a clawed wave over boats, a small snowy
  cone in its trough) or Red Fuji (a red peak under a mackerel sky), Hiroshige's Tōkaidō or Edo views (rain on a
  bridge, the plum garden), a known actor or beauty portrait. Keep the visual language with your own subject, as the
  demo keeps wave and peak in separate prints with no boats under the wave; name no series after real ones.
- **Do not:** invent script (mock Japanese, fake kanji, publisher's marks, signatures or series numbers). The cartouche
  holds the user's real copy in Latin letters; the seal carves an image. Japanese only as verified user text.
- **Do not:** use torii, temples, shrines or deities as decoration, geisha and samurai as costume, or give the sun
  radiating rays (the rising-sun flag); keep it a plain disc. Keep the paper margin, key lines and paper whites:
  without them it is flat vector illustration.

## Technical notes
- No render.json or vendored libraries; canvas 2D; six woff2 fonts. About 12 s for 300 frames on one page.
- Deterministic (tested in 16:9, 9:16 and both plans): one `seeded()` stream per use (11 paper, 23 grain, 57 spray,
  77 seal, 91 birds, 131 ripples, 149 grit), hashed noise (`lattice()`), audio seed 183. `inkC`, `keyC`, `maskC`,
  `twoC` are reset before use; `paperInk()` caches a pattern per context in `patterns`.
- Tied to 1920 × 1080: canvas, `FRAME`, `makePaper()`'s `cw = 242, ch = 137` and `makeGrain()`'s `cw = 322, ch = 182`
  (size them `Math.ceil(W / 8) + 2`, `Math.ceil(W / 6) + 2`, with `H` for ch, or 9:16 grain freezes below y ≈ 1100), the
  vignette radii `H * 0.32`, `H * 1.08` (use `Math.min(W, H)`), the 1100 bottoms (`bodyPath()`, `rowInk()`, the wave
  clip in `scene1Key()`, the sand) and the layout in Composition. `makeEdge()` and the wipes follow `W` and `H`.
- During the change print two is drawn into `twoC`: anything added to `scene2()` must draw on the context it is given.

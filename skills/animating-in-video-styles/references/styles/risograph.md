# Risograph (`risograph`)

An event poster printed on a risograph and animated: three fluorescent spot inks laid down one drum at a time on
off-white uncoated stock, overlapping into new colours, toned only with halftone dots, never quite in register.
It draws on zine and indie gig-poster riso printing; the mood is loud, warm, handmade and upbeat.

**Reference film:** a gig poster, "SOUND & SIGNAL — a night of live electronics": three ink drums slide in and lock into a poster with a pumping speaker, drift apart, and three roller passes re-print a second layout that snaps into register before the inks fade back to paper · `styles/risograph/`

## Signature
- **S1 Three spot inks, multiplied:** fluorescent pink, yellow and blue on off-white paper, nothing else; overlaps make
  orange-red (pink + yellow), green (blue + yellow) and violet-navy (pink + blue). Registration crosshairs at the edge
  midpoints print in every ink: near-black when aligned, a coloured triplet when not.
- **S2 Halftone is the only tone:** rotated dot screens, angle and cell per ink, dots growing from nothing to solid.
- **S3 Each ink is its own drum:** yellow slides in from the left, pink from the right, blue from the top, each
  overshooting and clacking into register by 2 s; the layers then wobble a pixel or two off-register.
- **S4 Riso ink texture:** banding, mottle, pinholes and roller streaks re-printing 10 times a second, on fibred paper.
- **S5 Poster type:** heavy grotesque display words fitted to the column, mono info lines, a knocked-out footer bar.

## Palette
| Role | Colour | In code |
|---|---|---|
| Paper, before its noise (also the fade-in veil) | 243,239,228 | `buildPaper()`, `render()` |
| Yellow, drum 1: screen 0°, 17 px cell | `#FFE800` | `INKS[Y]` |
| Fluorescent pink, drum 2: screen 75°, 16 px cell | `#FF48B0` | `INKS[P]` |
| Blue, drum 3: screen 15°, 15 px cell | `#0078BF` | `INKS[B]` |
| Paper fibres, dark and light | 150,135,110 · 255,255,250 | `buildPaper()` |
| Dirt flecks in the stock | 70,60,50 | `buildPaper()` |
| Roller shadow, multiplied | 90,80,70 | `render()` |

- Each ink is a full-frame layer multiplied on at about 0.93 density: overprints are computed, never picked; tone is
  dot size, colour is overlap. Yellow is the lightest ink: grounds and big shapes, never small text. Where all three
  overlap the print goes near-black (sampled about 20, 40, 20): keep three-ink overlaps to dots or slivers, and keep
  a pink shape that sits on blue off the yellow.

## Typography and copy
- Archivo Black (`GROT`; `fonts/ArchivoBlack-400-latin.woff2`, `-latin-ext`): display words, one per line, capitals,
  `fit(key, str, font, maxW, maxCap)` to a width (A: 1060 px, SOUND 265 px, cap 186) or a cap (B: 250, the "&" 300).
  Cap is 0.70 of the size; capitals advance 0.67–1.0 em (most 0.72–0.83, I 0.39): a nine-letter word fitted to 1060 px
  gets a cap of about 100–125 px (M and W pull it down).
- Space Mono 400 and 700 (`MONO`) for all other lines: `mono(c, str, x, y, size, bold, align, track)`, tracked 1–4 px
  with `letterSpacing`. By `measureText` a character advances 0.612 em plus the track: 9:16 lines (x 90–940) hold 30
  characters at 44 px, 43 at 30 px, the footer 46; 1:1 (x 84–650) 33 at 26 px bold; layout B's block in the solid
  yellow disc (632 px) 20 at 50 px. Longer copy: a new line or a shorter word; never below 26 px.
- Copy: poster shorthand in capitals: one to three display words, a strapline, a when-and-where line, a list split by
  slashes, tags split by em dashes, an issue number; names invented (in the demo's gig poster: date, doors and venue,
  a lineup of acts, genre tags, "No. 026"). Text never types on: it arrives with its drum or roller pass and leaves
  with the ink fade. The footer tags are knocked out of the pink bar (`destination-out`).
- `window.ready` preloads the faces with a sample string: add every new character to it. Otherwise the first frame
  draws it in a fallback face, and `fit()` sizes display words from fallback metrics for the whole film. Both faces
  cover Latin and Latin Extended only (`fonts/` has latin and latin-ext files: no Greek, Cyrillic or Vietnamese).

## Texture and finish
- Built once in `window.ready`: `buildPaper()` (`PAPER`: three octaves of `vnoise()` around 243,239,228, 900 fibres,
  40 dirt flecks), `buildTooth()` (`TOOTH`: near-white grain multiplied over the whole frame at 0.55, speckling ink and
  paper alike) and one `buildDensity()` per ink (`DENS`: the ink's alpha over the frame plus a `PAD` of 60 px, with
  drum banding, seven vertical roller streaks, a 7 % side falloff, mottle at three scales, 15,000 pinholes, 18 skips).
- The boil: each frame `render()` masks the ink layer with its map at an offset of up to ±48 px, re-chosen 10 times
  a second (`BOIL`, `bix()`, seeded `rng(9000 + bi)`): shapes move at 30 fps while the grain flips like successive
  prints. Keep this rate: per-frame grain flickers and compresses badly; a static map looks digital. During a roller
  pass only: a 26 px wet-ink line at the roller edge and a multiplied 80 px shadow band.
- `halftone(c, ink, bb, tone, cellMul)` draws vector dots every frame over the box `bb` = [x0, y0, x1, y1] on the
  ink's own screen (angle and cell from `INKS`, lattice anchored at the layer origin, so it moves with the drum).
  Radius is cell × 0.565 × √tone × 1.18 with tone capped at 1.25; tones under 0.015 draw nothing, dots touch near 0.56
  and fill solid near 1.1. `cellMul` 0.7 gives a finer screen (the cone). Tone functions are multiplied by `grow`.

## Shapes, line and figures
- Flat solids, knock-outs and dot fields only: `circle()`, `rrect()`, `ring()` arcs, 9 px polylines (the traces), type.
- **Splitting a new shape into inks** (the speaker shows all of it): each ink's branch of `compA()` or `compB()`
  (`k === Y`, `P` or `B`) paints coverage in white on the layer canvas `lc`, never colour, and ends with `regMarks()`.
  1. Give the silhouette one key ink: blue reads darkest (the speaker body), pink for type and accents.
  2. Cut details out of it with `destination-out` (driver holes, slot, footer tags), showing paper or the inks
     beneath; restore `source-over` afterwards.
  3. Draw lines inside the hole in the same ink, white on the layer (the driver rings, 9–18 px).
  4. Shade with a halftone: the same ink at `cellMul` 0.7 (the cone), or a second ink on its own screen (the pink disc).
  5. Lay a big shape of a third ink under it (the yellow sun) so part of the object overprints: the speaker is green
     where it sits on yellow and blue beyond it; but not under a pink-on-blue area (near-black, see Palette).
  6. Accept that the parts of one object arrive at different times, each with its drum.
- A new object belongs as a bold 200–700 px silhouette in two inks plus dots, with one knock-out detail.

## Composition and camera
- A flat poster, no camera, depth from overprint only. A layout sets display type against one emblem: the type as a
  column or full-bleed; the emblem on a big disc of another ink, so part of it overprints; a giant glyph or shape in
  yellow (the lightest ink) behind or between the type; mono info lines; a knocked-out footer bar (A only in the
  demo). A re-print must differ visibly (column to full-bleed, emblem moved) so the change reads. In the demo, A: type
  column left, sun with speaker right (`SPK`), a giant yellow "&" behind the column, footer bar over a yellow strip;
  B: full-bleed SOUND and SIGNAL around a yellow disc (solid to 330 px, dot halo to 640) holding the info block, a
  blue disc holding the pink "&", traces between, the lineup rotated at the right edge (`compA()`, `compB()`).
- 9:16 (1080 × 1920; every shot rendered, values on the 16:9 code, `W`, `H` and the canvas tag changed):
```
regMarks points [[W / 2, 34], [W / 2, H - 34], [34, H / 2], [W - 34, H / 2]]; START blue row [60, -2000]
layout A: SPK { x: 560, y: 1250 }; sun cx 600, cy 640, R 440; pink disc cx 820, cy 1110, R 215; ampA (40, 1560)
  fit soundA, signalA maxW 860 (caps 151, 143); soundA (84, 480), signalA (84, 670); strip box [0, 1660, W, 1800]
  footer fillRect(0, 1690, W, 76), copy 'MODULAR  —  AMBIENT  —  TECHNO  —  UNTIL LATE' at (W / 2, 1740), 30 px bold track 3
  info: 44 px line (90, 752); date line split into 'SAT 14 NOV  ·  DOORS 21:00' (92, 806) and 'THE FOUNDRY HALL'
  (92, 848), 30 px bold track 1; lineup (92, 890), 30 px regular track 2; 'No. 026' (W - 108, 78)
layout B: yellow disc cx 440, cy 1250 (radii as is); blue disc cx 740, cy 600, R 250; fit soundB, signalB maxW 840
  soundB (84, 320 + TXT.soundB.asc); signalB (84, 1430); ampB maxCap 260, centred at (740, 600 + TXT.ampB.asc * .5)
  traces [[540, 1, 1], [1262, 1.3, -1]]; info block centred on x 440 at y 1000, 1060, 1124, 1172 (sizes as is)
  lineup unrotated as a fifth line: mono(c, 'KILN  /  MOTH ORBIT  /  VERA LUX', 440, 1216, 30, true, 'center', 2)
```
- 9:16 checks (stills at every shot's widest moment): S1–S5 whole from 1.32 s; key text in x 84–944, y 320–1430;
  SOUND touches the left edge for 0.1 s in pink's overshoot (16:9 too); end card SIGNAL green, the "&" violet-navy
  (sampled 24, 40, 95) on blue. The caption band holds speaker foot, rings, strip and footer (A), halo dots to y 1890
  (B). Captions may cover the footer tags: put nothing the viewer needs there (date and venue stay in the info block).
- 1:1 (1080 × 1080; rendered the same way). The 1280 px halo is wider than the frame, so it shrinks:
```
regMarks as 9:16; START as 16:9
layout A: SPK { x: 800, y: 660 }; the blue speaker (from const pump to the cone's c.restore()) and the pink ring loop
  each wrapped in c.save(); c.translate(SPK.x, SPK.y); c.scale(0.72, 0.72); c.translate(-SPK.x, -SPK.y); ... c.restore()
  sun cx 700, cy 420, R 360; pink disc cx 900, cy 480, R 160; fit soundA, signalA 600; soundA (80, 250), signalA (80, 400)
  info at x 84: 30 px bold track 1 at y 470, split date line 26 px bold at 512, 548, lineup 26 px regular at 584
  'No. 026' (W - 60, 70); ampA (40, 930), maxCap 400; strip [0, 940, W, 1060]; footer fillRect(0, 966, W, 70), 9:16 footer copy at (W / 2, 1012)
layout B: yellow disc cx 340, cy 610; its halftone tone d < 270 ? 0 : grow * clamp(1.15 - (d - 300) / 180) * (d < 480 ? 1 : 0)
  and its circle(c, cx, cy, 300) (was 330); blue disc cx 870, cy 400, R 200; ampB maxCap 240, centred at (870, 400 + TXT.ampB.asc * .5)
  fit soundB, signalB 960; soundB (60, 44 + TXT.soundB.asc); signalB (60, 1040); traces [[290, 1, 1], [866, 1.3, -1]]
  info block on x 360 at 512, 572 (44 px, not 50), 636, 684; lineup unrotated, 26 px bold track 2, at (360, 728)
```
- 1:1 checks at the same moments: S1–S5 whole from 1.32 s; end card SIGN green, AL blue, the "&" violet-navy
  (sampled 26, 40, 104); the drifted left registration mark crosses the info block's first letters for 0.6 s.

## Motion
- Easing: `eBack()` for arrivals (slides s 1.25, 5.7 % overshoot; the lock s 2.2, about 15 %), `eOut()` for A's dot
  growth and the trace reveal, `eInOut()` for sweeps, B's growth and the ink fade, mostly `eIn()` for the drift apart.
- Slides: 0.72 s each from `START` (−1500 px, +1560 px, −1120 px), staggered 0.48 s, yellow and pink turning 0.03 rad.
  Landed layers wobble ±1.6 / ±1.3 px (ramping in over 1.2 s); layout B's wobble ±4 / ±3 px around their `MISB`
  offsets until `offB()` snaps them to exact register. `DRIFT` moves them up to 46 px and 0.012 rad apart in 0.6 s.
- Ambient: `beat()`, a 120 bpm pump on the 0.5 s grid, and the 10 fps boil (in the demo: cone and driver rings 4.5 %,
  sun tone 16 %, blue disc 14 %; four pink sound-ring pairs rippling from radius 200 to 460 at 0.55 cycles a second;
  the traces).
- Never: camera moves, 3D, squash and stretch, or a layer that holds perfectly still in layout A.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.3 | Paper fade-in: a paper-coloured veil lifts | `render()` (`fi`) |
| 0.30–1.98 | Drums slide in, yellow 0.30, pink 0.78, blue 1.26, each 0.72 s; a clack 0.45 s after each start | `T.inA`, `T.slide`, `offA()`, `START` |
| 0.55–2.88 | Dots grow in each ink, from 0.25 s after its start to 0.9 s after it lands | `compA()` (`grow`) |
| 1.50–4.45 | Poster A live: rings fade in from pink's landing, speaker pumps from 1.98, kicks 2.5–4.5; fully settled 3.18–4.25 (measured) | `compA()`, `beat()` |
| 4.45–5.05 | Registration drifts apart | `T.driftA`, `T.driftB`, `DRIFT` |
| 5.02–6.32 | Three roller passes, 0.46 s each: yellow (wiping all of layout A, speaker included), pink, blue | `T.sweep`, `T.sweepD`, `sweepY()` |
| 5.30–7.44 | Layout B's dots grow over 1.3 s per ink; traces draw left to right | `compB()` (`grow`, `reveal`) |
| 7.55–7.89 | Final lock: the wobble stops, layers snap into register | `T.lock`, `T.lockD`, `offB()`, `MISB` |
| 7.89–8.75 | Final poster held: only 0.86 s (measured as under Shorter); an action after 7.89 or an earlier fade breaks it | |
| 8.75–10 | Inks fade to paper, blue, pink, yellow, 0.15 s apart, 0.8 s each; bare paper from 9.85 | `T.fade`, `T.fadeD` |

- Reusable: the drum slide-in, a live hold on the beat, drift then roller re-print (the scene change; the first pass
  clears the old print), the final lock, the ink fade (the sign-off). Speaker, rings, traces, sun and copy are demo.
- Review keys: KEYS=2.0,3.5,4.9,5.3,8.2,9.3 (all inks down, poster A, drift, yellow pass, final poster, ink fade).

## Sound
audio.py reads `events.json` (`{t, k, …}` cues) and synthesizes print-shop sounds over a small electronic bed at
48 kHz stereo into a buffer sized by `DUR` 10.0:
- `slide` (`d`, `v`): a noise swish over `d`, low-pass rising from 300 Hz towards 4200 and back, gain 0.22 × `v`, pan ±0.4.
- `clack` (`v`): click, wood knock and falling thump, gain 0.42 × `v`. `drum` (`d`): a roller whirr for `d` + 0.25 s, four ka-chunks.
  `drift` (`d`): two sines sagging in pitch (D4 by 25 %, A4 by 30 %) with a swish, over `d`.
- `lock`: clack, kick and a D-minor chord (MIDI 50, 57, 62, 65, 69), 2.6 s long with a 1.6 s release.
- `kick` (`v`): kick, an off-beat hat 0.25 s later and a bass note from `BASS` (D, D, F, G) chosen by round(t × 2) mod 4.
- `outro`: the closing pad, D A D E A, 1.3 s with a 0.5 s swell. Bed: room tone at 0.004; master fade-in 0.2 s and
  fade-out 0.7 s at `DUR` (`fi`, `fo`), tanh limiter.
- No cue is looked up by name; unknown kinds and cues outside 0 to `DUR` drop silently. From T the film emits a
  `slide` and `clack` per drum, `drift`, a `drum` per pass, `lock` at T.lock + 0.1, `outro` at the first ink fade.
- What breaks it (tested): `slide`, `drift` or `drum` without `d` raise KeyError; `slide` or `drift` with `d` under one
  sample (1/48000 s) and `drum` with a negative `d` raise ValueError. Pans stay within ±0.4 (no NaN); a large `v` saturates.
- Fixed times live in anim.html: the events function there sends kicks every 0.5 s strictly inside 2.0–4.6 and
  6.4–8.9 s (`v` 0.8 before 5 s), from a loop that stops at 20 s. Re-time both windows on multiples of 0.5 s, where
  beat pumps, giving every pump a kick while its shape is on screen before the first ink fade: the sun until the
  drift, the speaker's cone (never ramped down) until the yellow pass wipes it, the blue disc from the pumpB gate to
  the first ink fade (the demo leaves the speaker's 5.0 pump unkicked); the hat may land up to 0.25 s after `outro`.
  The `lock` chord and `outro` pad still ring at `DUR`, ended by the master fade: keep `outro` 0.85 s or more before `DUR`.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Paper, tooth, ink densities | `anim.html` → `buildPaper`, `buildTooth`, `buildDensity` | built once in `window.ready` into `PAPER`, `TOOTH`, `DENS` | as is |
| Ink set | `anim.html` → `INKS` | `name`, `col`, `ang`, `cell`, `seed` per drum; `Y`, `P`, `B` index it | adapt for two inks (tested): delete the blue row and blue's branches in `compA()`/`compB()`, moving shapes you keep to another ink, and point their `INKS[B]` halftones at that ink; both loops in `render()` to `k < INKS.length`, the fade index `2 - k` to `INKS.length - 1 - k`; drop the third entry of `T.inA`, `T.sweep`, `T.fade`; gate `pumpA` on `T.inA[P]`; to drop yellow or pink instead, first swap blue's row values into the row you drop (the indices `Y`, `P`, `B` are fixed numbers) |
| Layer compositor | `anim.html` → `render` | per ink: white coverage on `L`, masked by its density map (see Texture), tinted, multiplied on at alpha `fade` | as is |
| Halftone | `anim.html` → `halftone` | `halftone(c, ink, bb, tone, cellMul)`: box, tone function (x, y) → 0–1.25, screen scale | as is |
| Shapes | `circle()`, `ring()`, `rrect()`, `regMarks()` | `ring(c, x, y, r, w, a0, a1)` arc stroke; `rrect(c, x, y, w, h, r)` path, then fill | as is |
| Type | `fit()`, `text()`, `mono()`, `TXT` | `fit(key, str, font, maxW, maxCap)` once in `window.ready`, then `text(c, key, x, y, align)`; `mono(c, str, x, y, size, bold, align, track)` | as is; new keys and copy |
| Registration | `offA()`, `offB()`, `place()`, `START`, `DRIFT`, `MISB` | offsets [dx, dy, rot] about the frame centre | as is; `START` per format |
| Roller passes | `sweepY()` | edge y from −60 to `H` + 60 over `T.sweepD` | as is |
| Timeline, boil, beat | `T`, `BOIL`, `bix()`, `beat()` | | adapt `T` |
| Demo layouts | `compA()`, `compB()`, `SPK` | one branch per ink | replace |
| Cues | `anim.html` → `window.events` | from `T`, plus the kick windows | adapt |

## Adapting
- **Style vs demo plot:** style is paper, three multiplied inks, per-ink screens, boil, registration marks, drums
  clacking into register, drift and re-print, the lock, the ink fade, the type system, beat pump and print-shop
  sounds; plot is the copy and the demo's shapes (speaker, rings, traces, sun, "&"), not the layout roles they fill
  (Composition). Transformations: a re-print, a snap into register, dot growth.
- **New subject:** a poster: one to three display words, three or four info lines, one emblem split into inks as in
  Shapes; rewrite `compA()` and `compB()`. Traps: before landing the ring phase is negative and `arc()` throws on a
  negative radius (keep the `t < land` guard on anything similar); `pumpB` starts at the literal 6.4; the growth and
  wobble ramps in `compA()` and `offA()` use literal offsets (0.25, 0.9, 1.2); layout A is drawn only below the
  yellow roller (`eY0`), so the first pass clears all of it.
- **Values that follow the subject's shape** (stand-in rendered in 9:16: a 694 px microphone): `SPK` (in 9:16 the subject
  fits between the lineup, y 900, and the footer bar, y 1690: set `SPK.y` so its top clears 900); the ring centre
  (`SPK.y` + 90 for the woofer, − 60 for the microphone's head), whose rings reach 283 px above it and must clear the
  info block (centre 1190 or lower in 9:16); the footer, clear of the subject's foot (fillRect(0, 1760, W, 76), copy
  y 1810, strip [0, 1730, W, 1870]); `START`'s blue y. Sun, pink disc, "&" and type stayed.
- **Length:** lengthen the live holds; re-time `T`, the kick windows, the `pumpB` gate, audio.py's and build.sh's
  `DUR` (past 20 s raise the kick loop's 40). Hold each poster 4–5 s at most before the next re-print; more than three re-prints tire.
  `render()` hard-codes two layouts; a third (`compA()` re-printed after B) took this, rendered at each pass, 15 s:
```
T: driftC [9.2, 9.8], sweepC [9.77, 10.19, 10.61], lockC 12.3; fade [13.6, 13.75, 13.9]; B's kicks to inside 6.4-9.8, C's inside 10.6-13.6
function sweepYC(k, t) { return lerp(-60, H + 60, eInOut(seg(t, T.sweepC[k], T.sweepC[k] + T.sweepD))); }
offB(): add DRIFT[k] * d2, d2 the drift easing of offA() on T.driftC; offC(k, t): offB()'s lock and wobble on T.lockC
render(): eYC = sweepYC(Y, t); B only if t >= T.sweep[k] && eYC < H + 50, clipped to lc.rect(0, eYC, W, eK - eYC); then,
  before if (!any), when t >= T.sweepC[k]: clip lc.rect(0, 0, W, sweepYC(k, t)), place(lc, offC(k, t)), compA(lc, k, t),
  any = true, the wet-ink line; run the roller-shadow loop over both sweep sets. Cues: drift (d 0.7), drums, lock + .1; DUR 15
  (check_audio peak 0.731). The re-printed compA() keeps its finished ramps: full tone at once, the sun not pumping.
```
- **Shorter:** 6 s up to the demo: keep every beat, shorten slides, ramps and holds; poster A's settled hold goes first
  (to 0.45 s). Under 6 s drop the drift, re-print and lock (3.4 s) and end on poster A, the title card; never the
  slide-in or the ink fade. Cut the copy then to the display words plus one 44 px date-and-venue line (rendered:
  'SAT 14 NOV  ·  FOUNDRY HALL' for the three info lines); footer tags and issue number stay as texture. The signature
  reads 1.2 s after the 0.3 s fade-in (pink over yellow at 1.50), 0.6 s in the 4 s plan; poster A costs its last
  landing plus the ramps plus 0.8 s held (2.5 s in the 4 s plan). Dropped beats stay in the code at times of 99 (cues
  fall past `DUR`). Only `T` and action literals move; boil, `beat()`, ripples and traces stay on film time. Holds:
  pixel difference against the same `t` with every action (slides, growth, ramps, drift, sweeps, reveal, lock) forced
  to its end. Both plans rendered in 16:9 and passed events.mjs, audio.py and `python3 <skill>/scripts/check_audio.py audio.wav 6` (and 4):
```
both: compA grow = eOut(seg(t, T.inA[k] + .15, land + .5)); offA wobble ramp T.inA[k] + T.slide + .6 (was + 1.2)
6 s: T = { inA: [0.20, 0.42, 0.64], slide: 0.55, driftA: 2.45, driftB: 2.85, sweep: [2.80, 3.06, 3.32], sweepD: 0.36,
  lock: 4.00, lockD: 0.30, fade: [5.15, 5.25, 5.35], fadeD: 0.5 }; compB grow p0 + 0.7 (was 1.3); pumpB gate t > 3.7
  kicks if ((bt > 1.0 && bt < 2.8) || (bt > 3.6 && bt < 5.1)), v bt < 3 ? .8 : 1; audio.py DUR 6.0 (peak 0.708)
  poster A settled 1.79-2.25; final poster still 4.30-5.15 (0.85 s); inks gone at 5.85
4 s: T = { inA: [0.20, 0.40, 0.60], slide: 0.50, driftA: 99, driftB: 99.5, sweep: [99, 99, 99], sweepD: 0.46,
  lock: 99, lockD: 0.34, fade: [3.05, 3.15, 3.25], fadeD: 0.5 }; kicks if (bt > 1.0 && bt < 3.1), v .8
  audio.py DUR 4.0 (peak 0.454); poster A still 1.70-3.05 (1.35 s); inks gone at 3.75; no lock chord, the outro closes
```
- **Other formats:** recompose by moving numbers (Composition), never by scaling the 16:9 frame. The re-printed layout
  carries the ending; the first layout's emblem (the speaker) leaves with that layout at the re-print.

## Boundaries
- **Distinct from:** `pop-art` prints CMY plus a black key with outlines and uniform, never size-modulated Ben-Day
  dots; risograph has three fluorescent spot inks, no black, size-modulated rotated screens and drum motion.
  `editorial-illustration` is a flat four-ink illustration with characters and a metaphor, riso grain as surface only.
  `linocut` is black and red relief with carved marks; `collage` is torn paper, tape and stop-motion jitter;
  `newspaper` is black halftone on newsprint with a moving camera; `swiss-style` is a clean digital grid poster;
  `dither-1bit` is two inks and ordered dither.
- **Poor fit:** long explanations (`infographic`), real charts (`data-visualization`), characters and acting
  (`editorial-illustration`), product shots (`product-ui`), solemn subjects the fluorescent inks undercut (`linocut`).
- **Do not:** add a black or fourth ink, outlines, gradients (tone is halftone only), blur, glow, vignette or bloom;
  composite inks any way but multiply; let text type on; use real band, venue or brand names the user did not supply.

## Technical notes
- No render.json, vendored libraries or GPU: canvas 2D, fonts in `fonts/`; about 0.1 s a frame on one page (Apple
  silicon), 35 s per 300 frames. `DUR` in anim.html is unused. Seeded `rng()` and `default_rng(26)` (consumed in cue
  order) keep it deterministic; the determinism test passes on the original and the 9:16 version.
- `render()` recomposites the full-frame layer `L` three times a frame and resets `lc`'s transform, composite, alpha
  and colours per ink; line width, cap, join and font carry over, so wrap any branch you add in `save()`/`restore()`.
- Sizes hard-coded outside `W`/`H`: the canvas tag; `regMarks()` (960, 34, 1046, 540, 1886); the footer bar (y 960,
  76 tall) and its copy (960, 1010); the rotated lineup (1806, 540); `START`'s −1120 (must exceed `H`); the `fit()`
  widths in `window.ready` (1060 for layout A, 1736 for B); every layout coordinate in `compA()`, `compB()` and `SPK`.


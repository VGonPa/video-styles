# Whiteboard (`whiteboard`)

A lesson drawn live on a white dry-erase board with a felt marker, while the camera trails a long arrow to fresh
board and finally pulls back to show the whole process at once. It follows the whiteboard-animation explainer
tradition; the mood is friendly, patient and step by step.

**Reference film:** "How do bees make honey?": a flower, a bee sipping nectar and the hive; a long arrow leads the
camera to bees fanning water off the comb and a jar labelled "honey!", then the camera pulls back to the summary
board · `styles/whiteboard/`

## Signature
- A near-white glossy board fills the frame from frame 0 (no fade-in): soft diagonal glare bands, faint ghost
  scribbles and smears of old erasing, fine grain and a light falloff toward the corners.
- A felt marker (white barrel, black ring, label band and cap, nib top left, soft shadow) sits on whatever is drawn:
  it glides in lifted, its shadow dropped well below it (full lift at 0.15 s), writes the title at 0.3–1.1 s, then
  slides from stroke to stroke nib down (the demo's gaps are 0–0.06 s; only gaps over 0.17 s give a full hop).
- Chunky handwriting in Kalam Bold, black, written on left to right letter by letter as the nib bobs, slightly
  tilted (the title is 96 px).
- Objects build stroke by stroke in 6–7 px black lines with a gentle, fixed hand wobble (it never boils) and round
  caps, then get coloured in with a zig-zag scribble inside the outline (in the demo, the flower at 1.14–1.83 s, its
  red centre at 1.75 s); red marks motion as a dashed path or motion lines (the demo's flight path, 2.06 s).

## Palette
| Role | Colour | In code |
|---|---|---|
| Board | `#f6f6f3` | `BOARD` |
| Ink: every outline, arrow and word | `#18181b` | `INK` |
| Red marker: movement and emphasis (flower centre, flight path, nectar, fan lines, underlines) | `#d4352a` | `RED` |
| Amber marker: the subject's material (honey) | `#e9a21f` | `AMBER` |
| Glare bands; darkening toward the tray (bottom) | `rgba(255,255,255,0.55)`; `rgba(90,95,100,0.06)` | `paintBoard()` |
| Ghost scribbles / wiped smears | `rgba(60,70,80,${0.018 + rand() * 0.03})` / `rgba(80,90,100,${0.008 + rand() * 0.01})` | `paintBoard()` |
| Marker sprite (white barrel; nib, bands and cap) and shadow | `#ffffff` … `#9d9d99`; `#111`, `#3b3b40` … `#060607`; shadow `#2b3036` | `paintMarker()`, `mShadow` |
| Corner falloff | `rgba(70,80,90,0.10)` | `frame()` |

- Black carries every line and word; red marks motion and emphasis; amber is the subject's material (in the demo, honey). A
  fourth colour breaks the three-marker set. Colour is never a flat fill: it is scribbled in (Shapes).

## Typography and copy
- One face: Kalam 700 (`fonts/Kalam-700-latin.woff2`, `fonts/Kalam-700-latin-ext.woff2`), loaded with `loadFont()`
  from `common.js` and named `HAND`; no fonts.css. Sizes: title 96 px tilted −0.012 rad (`rot`); labels 70 px (66 for
  "fan off water"); the answer "honey!" 116 px tilted −0.015, underlined twice in red. All text is `INK`.
- How text is written: `drawLabel()` clips the word to a rectangle that grows left to right; `writing()` gives every
  letter the same time and puts the nib on the midline, bobbing 0.08–0.48 of the size above the baseline one and a
  half times per letter. Text never moves, fades or leaves. The demo writes 27–50 characters a second; the 6 s plan's
  61–65 still reads as handwriting (a 13-character label in 6 frames, the nib bobbing ±13 px); 65 is the fastest tested.
- Width: Kalam 700 runs 0.43–0.52 of its size per character in lower or title case, 0.58 in capitals: budget 0.5.
  16:9: the title at 96 px holds about 36 characters, a label 17 at 70 px. 9:16: the title at 72 px holds 23–24
  (x 68–922), a half-width label 10 at 70 px, the answer slot (centred at screen x 744, right edge 930) about 370 px,
  6 characters at 116 px. Summary scales are 0.57 (16:9), 0.47 (9:16), 0.44 (1:1): keep label size × scale at 20 px
  or more. `text()` draws one line. Longer copy: lower the size to fit one line, size ≈ width ÷ (0.5 × characters)
  (a 31-character title at 54 px in 9:16, 25 px in the summary); a second title line in 9:16 lands on row 1.
- Glyphs: Latin-1, most of Latin Extended-A (Polish, Czech, Hungarian, Turkish, Romanian complete; Esperanto ĉ ĝ ĥ ĵ
  ŝ ŭ, Maltese ċ ġ ħ, Welsh ŵ ŷ missing), × ÷ ± − – — ° · ½ ² ³ € £ © ™ …. Missing: arrows, ✓ ✗, √ π ≈ ≠ ≤ ≥ ∞,
  subscripts (write CO2), Greek, Cyrillic, CJK: draw arrows and ticks as strokes (`arrow()`).
- Copy: a question as title, one to three lowercase words per step, the answer one exclaimed word. No sentences.

## Texture and finish
- `paintBoard()` paints `board` once with `rng(3)` at half resolution (`WB.k` 0.5) over `WB`: fill, 5 glare bands,
  the bottom darkening, 40 faint scribbles, 16 smears blurred 2 px, ±2 levels of grain. `frame()` draws it under the
  camera, so its ghost marks show every camera move (`WB` must cover every framing). Nothing flickers.
- The marker: `paintMarker()` draws the sprite once into `mSprite`; `drawMarker()` stamps it in world space (it
  shrinks with the pull-back). It never turns, and the same black marker draws the red and amber marks.

## Shapes, line and figures
- Every line is a `Path` from `P()` in `common.js` (`M`, `L`, `Q`, `S` smooth curve, `A`), drawn by
  `stroke(path, t0, t1, o)`, whose `jitter()` adds a 1.6 px two-sine wobble once at build (fills 0.2–0.3, the long
  arrow 2). Width 7 for outlines, 6 for petals, cells and wings, 5 for small parts, 15 for bee stripes; round caps.
- Closed outlines run about 0.2 rad past their start (`ell()` from π + 0.1 to 3π + 0.3 for the bee body), as a hand
  closes a loop; polygons come from `poly()` and `hexPts()`. `arrow(from, to, t0, t1, bow, o)`: a bowed shaft, then a
  two-barb 30 px head in the last 0.06 s; the long connector is a looser `S()` curve with a 34 px head.
- Colour is scribbled, never flat: `hatch(x0, y0, x1, y1, step)` rows (step 5–10) stroked 6–12 px wide in `RED` or
  `AMBER` through `clip`: `clipOf(points)` of the outline or an inset copy (hex cells 11–14 px in), leaving white
  slivers between rows (and a white rim when inset). A `BOARD`-coloured stroke over a fill is a glint (the jar).
- Doodles are built from a centre, a scale and a flip, as `bee(cx, cy, s, flip, t0, dur, { drop })` is: body loop,
  three stripes, head, dot eye, smile, antennae, stinger, legs, two wings, each stroke at a fixed fraction of `dur`,
  widths scaled by max(0.8, s). A new object belongs when it is a handful of black 5–7 px strokes: outline, then
  details, then a red or amber scribble, then its label. No people in the demo and none tested: use objects.
- Idle life on finished drawings: `flap` rocks a wing ±0.2 rad at 7 Hz about its pivot (ramping in over 0.25 s);
  `drift` lifts a stroke 20 px at 14 px/s while it wavers ±5 px. The beat and the waver run to the end of the film;
  the 20 px rise is an action that takes 1.43 s, so a drift stroke drawn less than about 1.5 s before `Z1` needs
  28 px/s (0.71 s).

## Composition and camera
- 16:9: each panel is a frame-sized board with one row of items read left to right, labels on one baseline under
  them, small arrows between. Panel A is the frame at scale 1 (`A_C` [960, 540]): title at x 960, baseline 205;
  items near x 330, 910 and 1570, labels on baseline 850; panel B at `BX` 1760, `BY` 420, right of and below A (`B_C`).
- `cameraFor(t)`: a 2 % push on panel A; a glide with `eio` to `B_C` over the long arrow's window ± 0.05 s that
  overtakes the arrow, so its tip sweeps from the right edge to the left third; a 2 % push on panel B; a pull-back with
  `eio` over `Z0`–`Z1` to `SUM`, fitted by `measureLabels()` (1720 × 940 box, scale 0.571); then a 1.2 % pull to 10 s.
- 9:16 (1080 × 1920, rendered with the demo restacked and with a stand-in): two rows per panel, and panel B down and
  to the right, so the glide is diagonal and the summary is a staircase that fills review.md's safe area:
```js
// common.js: const W = 1080, H = 1920; canvas width="1080" height="1920"
const BX = 1000, BY = 1100, A_C = [540, 960], B_C = [BX + 540, BY + 960], WB = { x0: -900, y0: -1100, w: 3800, h: 5600, k: 0.5 };
text('How do bees make honey?', 495, 370, 72, ...)            // one line, x 68-922
flower: cx 230, cy 600; 'flower' at (cx, 1010); flight path: P().M(370, 570).S([[440, 500], [520, 530],
  [512, 602], [456, 596], [466, 530], [550, 496], [635, 550]], 18)
bee(780, 600, 0.95, 1, ...); 'sips nectar' at (745, 1010); arrow([640, 1070], [500, 1150], ...)
HIVE = { cx: 330, cy: 1260, r: 60 }; 'hive' at (cx + 310, cy + 25)    // beside the hive, not under it
long arrow: P().M(500, 1400).S([[620, 1500], [760, 1580], [BX + 60, BY + 470], [BX + 130, BY + 520]], 24)
comb C: [[265, 578], [400, 500], [535, 578]]; bee(BX + 720, BY + 340, 0.78, -1, ...)
fan lines: P().M(BX + 588 - dx, BY + 212 + dy).Q(BX + 540 - dx, BY + 192 + dy, BX + 502 - dx, BY + 230 + dy, 16);
  vapour x 310, 375, 440 and BY + 398 in both places (start point and rising knots)
'fan off water' at (BX + 400, BY + 778); arrow([BX + 520, BY + 810], [BX + 575, BY + 960], ...)
jar: J = BX + 740, Y = BY + 420; ENTER = [700, 2100], EXIT = [BX + 1300, BY + 2300]
measureLabels(): SUM.s = Math.min(870 / (x1 - x0), 1130 / (y1 - y0));
                 SUM.c = [(x0 + x1) / 2 + 45 / SUM.s, (y0 + y1) / 2 + 95 / SUM.s];   // centre on (495, 865)
frame(): ctx.createRadialGradient(540, 840, 400, 540, 960, 1250)
```
- Measured: labels x 59–930, y 300–1313 at 4.45 s; "honey!" x 563–925, y 1268–1398 at 8.6 s; summary (0.470) in
  x 60–930, y 347–1383. As in 16:9, only "honey!" and its underline share ink and every Signature item shows.
- A stand-in (seed, 400 px sprout, sun; rain cloud, 770 px tree) showed what follows the demo's shapes: items must end
  above about 940 for labels on baseline 1010; the end object's slot runs from the top row's right-hand object down to
  the answer's baseline minus about 120 (about 430 px under the stand-in's cloud; a 514 px tree fit under three short
  wind lines); the long arrow's last knots aim at panel B's first object; `SUM` refits itself.
- 1:1 (1080 × 1080, rendered with the demo and the 10 s fix): the 9:16 layout framed below scale 1, because its
  1100 px panels do not fit at scale 1 and the 16:9 row at 0.56 leaves 60 % of the height empty:
```js
// on top of the 9:16 block: common.js W = 1080, H = 1080; canvas 1080 × 1080
const A_C = [494, 850], B_C = [BX + 524, BY + 802], KA = 0.8, KB = 0.72;      // panel scales
// cameraFor(): s = KA * (1 + 0.02 * seg(t, 0, CONN.t0)) on panel A, lerp(1.02 * KA, KB, glide) in the glide,
//   KB * (1 + 0.02 * seg(t, CONN.t1, Z0)) on panel B, lerp(1.02 * KB, SUM.s, out) in the pull-back; ENTER = [700, 1650]
measureLabels(): SUM.s = Math.min(960 / (x1 - x0), 960 / (y1 - y0)); SUM.c = [(x0 + x1) / 2, (y0 + y1) / 2];
frame(): ctx.createRadialGradient(540, 480, 300, 540, 540, 900)
```
- Measured: panel A labels x 192–889 at 57 px, title from y 101; panel B "honey!" x 568–829, y 878–972 at 85 px;
  summary scale 0.436 (labels 29–31 px) in x 137–943, y 60–1020; empty rows 9 % or less; panel B's narrow two-row
  stack leaves its right quarter bare (x 819–1080, 24 %), as bare as the 16:9 summary's lower left; still from 8.70.

## Motion
- Strokes reveal along their arc length, linearly by default (`ease`); the long arrow uses `eio2`, the red
  underlines `eout`. Strokes last 0.01–0.3 s (the long arrow 0.82); within an object they follow with 0–0.02 s gaps.
- `penAt(t)` puts the nib on the current move (`nibOn()`), glides with `eio2` between moves, comes from `ENTER` and
  leaves for `EXIT` over `PEN_OUT` 0.4 s. It visits `moves` in t0 order: overlapping windows make it jump, and a move
  parked past the film's end drags it across the board during the final hold, so delete dropped moves.
- Nothing pops, overshoots, fades, scales or is erased: the board only accumulates. Ambient, allowed through holds:
  wing beats, vapour waver, the slow pushes and the final pull. Actions: strokes, labels, the marker's travel, the wing
  ramp, the vapour's 20 px rise, the glide and the pull-back.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.3 | Marker glides in from below the frame | `ENTER`, `penAt()` |
| 0.3–1.1 | Title written on | `text()`, `writing()` |
| 1.14–2.36 | Flower: stem, leaf, six petals, centre ring, red scribble (1.75–1.83); "flower"; red dashed flight path | `stroke()`, `hatch()`, `dash` |
| 2.4–3.44 | Bee (wings at 2.95–3.02 start beating), red nectar drop (3.04–3.16); "sips nectar" | `bee()` |
| 3.48–4.44 | Arrow; seven hex cells 0.065 s apart; four amber scribbles (4.15–4.3); "hive" | `arrow()`, `HIVE`, `hexPts()` |
| 4.5–5.4 | Long arrow; the camera glides to panel B (4.45–5.45) | `CONN`, `cameraFor()` |
| 5.46–6.55 | Three comb cells half-filled with amber; a second bee, facing left | `BX`, `BY`, `bee()` |
| 6.58–7.22 | Red fan lines; vapour squiggles that rise and waver; "fan off water" | `flap`, `drift` |
| 7.26–8.08 | Arrow; jar lid, body, amber scribble, honey line, glint, drip | `arrow()`, `hatch()` |
| 8.1–8.56 | "honey!" at 116 px; two red underlines | `text()`, `stroke()` |
| 8.56–9.3 | Marker leaves down-right (to 8.96); pull-back to the summary board (8.6–9.3) | `EXIT`, `Z0`, `Z1`, `SUM` |
| 9.62–10 | Fade to board white | `frame()` |

- Reusable grammar: a question title; an item every 0.7–1 s (strokes 0.5–0.7 s, label 0.12–0.26 s) with a small arrow
  to the next; a colour-in reveal; a 1 s glide to fresh board; the answer big and underlined; pull-back; hold; fade.
- The demo's ending is too short: against the same frame with every action forced to its end (Motion's ambient
  kept), it is still from 9.30 to the fade at 9.62, 10 frames. Tested fix (16:9, 9:16, 1:1): still from 8.70, 28
  frames; whoosh and chord follow `Z0` and `Z1`; audio.py unchanged, check_audio.py passes:
```js
const TW = t => t < 5.46 ? t : 5.46 + (t - 5.46) * 0.85;    // first line of stroke() and text(): t0 = TW(t0); t1 = TW(t1);
// in bee(): BEES.push({ t0: TW(t0), cx, cy });   then  const Z0 = 8.1, Z1 = 8.7;
```
- Review keys for contact_sheet.sh: 0.5 (marker writing), 1.8 (first colour-in), 4.45 (panel A whole), 5.0 (mid
  glide), 8.8 (panel B whole, marker gone; 8.1 with the fix, marker leaving), 9.5 (summary; 9.0 with the fix).

## Sound
audio.py reads `events.json` and synthesizes 48 kHz stereo, `DUR` 10.0, with 0.25 s and 0.8 s fades (peak 0.215).
- Derived from every move, so new drawings are scored for free: `marker` (`d`), a felt tap and squeak over `d` (at
  least 0.03 s), per stroke; `write` (`d`, `n`), `n` squeaks over `d`, per label (`n` = letters without spaces).
- `buzz` (`pan`): a 218 Hz drone with a 7 Hz flutter to the end of the buffer, one per `bee()` (`BEES`), panned ±0.3;
  the loop over `buzzes` ducks the first to 0.35 at fixed times (4.5 to 5.6, the glide): move them with `CONN`. It is
  the demo's bee sound, not the style's: a new doodle copied from `bee()` drops its `BEES.push` line unless the thing
  really hums or buzzes; with no `buzz` cue the duck never runs.
- Pushed by hand in `window.events`: `whoosh` (`d`), a noise swell at `CONN.t0` and `Z0`; `chord` at `Z1` − 0.1.
- Bed: room tone (`room`) and an F major pad at fixed times, `tone(nt(m), 9.4, 1.5, 1.4)` from 0.3 s with `tt(9.4)`:
  set both 9.4 to `DUR` − 0.6 (a mismatch raises a shape error). No cue is looked up by name; unknown kinds are skipped.
- What breaks it (tested): a missing `d` (`marker`, `write`, `whoosh`), `n` or `pan` raises KeyError; `pan` beyond ±1
  writes NaN and a silent channel (check_audio.py fails); a `whoosh` with `d` 0 writes one NaN sample that audio.py
  reports as "ok nan" and check_audio.py passes, so keep `d` above 0. Cues past `DUR` are dropped; any `DUR` works.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Board | `anim.html` → `paintBoard` | `paintBoard(cnv, rand)` once into `board`; world rectangle `WB` | as is; size `WB` to every framing |
| Marker | `anim.html` → `paintMarker` | sprite `mSprite`, shadow `mShadow`, `MK`, `PIV`; `drawMarker(m)` with m = `penAt(t)` | as is |
| Timed stroke | `anim.html` → `stroke` | `stroke(path, t0, t1, { jit, color, width, clip, dash, ease, flap, drift })`: defaults 1.6 px wobble, `INK`, 7, linear | as is |
| Handwriting | `anim.html` → `text` | `text(str, x, y, size, t0, t1, { color, align, rot })`, anchored centre by default | as is |
| Shape helpers, arrow | `anim.html` → `hatch` | `ell(cx, cy, rx, ry, a0, a1, rot, n)`, `poly(pts)`, `clipOf(pts)`, `hatch(x0, y0, x1, y1, step)`, `hexPts(cx, cy, r, a0)`, `toward(x, y, ang, len)`, `arrow(from, to, t0, t1, bow, o)` | as is |
| Doodle with scale and flip | `anim.html` → `bee` | `bee(cx, cy, s, flip, t0, dur, { drop })` | adapt: the pattern for new doodles |
| Pen path | `anim.html` → `penAt` | `ENTER`, `EXIT`, `PEN_OUT`; nib from `nibOn()` and `writing()` | as is; move `ENTER`, `EXIT` per format |
| Camera | `anim.html` → `cameraFor` | `A_C`, `B_C`, `CONN`, `Z0`, `Z1`, the pull `seg(t, Z1, 10)`; `SUM` fitted in `measureLabels()` | adapt: panel centres, times, fit box; a panel scale for 1:1 |
| Frame | `anim.html` → `frame` | board, `moves` in save/restore, marker, falloff, fade `seg(t, 9.62, 10)` | as is; re-time the fade |
| Sounds | `audio.py` → `marker` | cue kinds in Sound | as is; re-time pad and duck |
| The bees | flower block, `bee()` calls, `HIVE`, panel B and jar blocks, `BX`, `BY` | | replace |

## Adapting
- **Style vs demo plot:** always the style: board, marker, Kalam written on, black wobbly strokes, red and amber
  scribbles, red motion marks, the question title, the glide to fresh board, the underlined answer, the pull-back, the
  fade (4 s and shorter: see Shorter). Demo plot: the bees, their buzz, all copy. Transformations: a colour-in, steps
  resolving, the pull-back.
- **New subject:** a process in three to six steps, one doodle per step; replace every call between the title and
  the underlines, keep the kit. Traps: a label must clear its object by about 70 px; overlapping time windows make
  the marker jump; steam or vapour on the last object keeps rising into the hold (see Shapes); wrap every new drawer
  in `ctx.save()`/`ctx.restore()`, as `frame()` does for moves.
- **Length:** past 10 s add panels of 3–4 s. A third panel needs code you write: a list of panel centres and
  connector windows in `cameraFor()`, one `whoosh` per glide, `WB` enlarged; `SUM` still fits everything. Re-time
  `CONN`, `Z0`, `Z1`, `seg(t, Z1, 10)`, the fade, audio.py's `DUR`, pad and duck, and build.sh's `DUR`.
- **Shorter:** to about 6 s keep every block and compress strokes more than labels (labels up to 65 characters a
  second, title 0.47 s); the glide reads at 0.5 s, the pull-back at 0.55 s; vapour rises at 28 px/s (Shapes). Under
  6 s cut whole beats: panel B's fan lines and vapour, then panel B with the glide, pull-back and underlines, then the
  flight path and drop; then make the last panel A label the answer (same 70 px, same timing). The signature reads
  from 0.15 s (no fade-in); the summary costs the pull-back, 0.8 s and the fade. Both plans map the demo's blocks
  through a piecewise-linear function in `stroke()`, `text()` and bee()'s `BEES.push`, as the 10 s fix does, except
  the long arrow's two `stroke()` calls, which take `CONN`'s new times as they are (wrap the mapping in an if (!o.raw)
  test and pass raw: true on them):
```js
const TM = t => { for (let i = 1; i < KN.length; i++) if (t <= KN[i][0]) { const [x0, y0] = KN[i - 1], [x1, y1] = KN[i];
  return y0 + (y1 - y0) * (t - x0) / (x1 - x0); } return t; };      // demo time -> new time
// 6 s, 16:9, every block (still 4.80-5.70, 28 frames; audio peak 0.195):
const KN = [[0, 0], [0.3, 0.15], [1.1, 0.62], [1.14, 0.64], [1.83, 0.94], [1.86, 0.96], [2.02, 1.08], [2.06, 1.1], [2.36, 1.22],
  [2.4, 1.24], [3.16, 1.56], [3.2, 1.58], [3.44, 1.76], [3.48, 1.78], [3.64, 1.85], [3.68, 1.87], [4.3, 2.13], [4.32, 2.15],
  [4.44, 2.23], [5.46, 2.79], [5.92, 2.99], [5.95, 3.01], [6.55, 3.27], [6.58, 3.29], [6.94, 3.45], [6.96, 3.47], [7.22, 3.67],
  [7.26, 3.69], [7.42, 3.76], [7.46, 3.78], [8.08, 4.04], [8.1, 4.06], [8.32, 4.2], [8.35, 4.22], [8.56, 4.32]];
// CONN { t0: 2.26, t1: 2.76 }; Z0 4.25, Z1 4.8; seg(t, Z1, 6); fade seg(t, 5.7, 6); vapour k * 28; audio.py:
//   DUR 6.0; tone(nt(m), 5.4, 0.8, 1.0) and tt(5.4); duck np.interp(t, [0, 2.26, 2.96, 6], ...)
// 4 s, 9:16 layout, panel A only (still 2.80-3.75, 29 frames; audio peak 0.198): delete every call from the long arrow on
const KN = [[0, 0], [0.3, 0.15], [1.1, 0.7], [1.14, 0.74], [1.83, 1.08], [1.86, 1.1], [2.02, 1.24], [2.06, 1.27], [2.36, 1.4],
  [2.4, 1.43], [3.16, 1.83], [3.2, 1.86], [3.44, 2.06], [3.48, 2.09], [3.64, 2.17], [3.68, 2.2], [4.3, 2.52], [4.32, 2.55], [4.44, 2.65]];
// CONN { t0: 98, t1: 98.9 }, Z0 99, Z1 99.5 (cameraFor and window.events read them); push seg(t, 0, 4) in cameraFor;
// window.events: ev.push({ t: 2.7, k: 'chord' }) instead of the whoosh and chord pushes; fade seg(t, 3.75, 4)
// audio.py: DUR 4.0; tone(nt(m), 3.4, 0.6, 0.8) and tt(3.4)
```
- **Other formats:** rendered 9:16 and 1:1 values are in Composition and camera; the 4 s plan uses the 9:16 layout.

## Boundaries
- **Distinct from:** `chalkboard` is chalk on green slate with no visible hand and an eraser wipe; here a visible
  marker on white, nothing erased, new steps on fresh board the camera glides to. `blueprint` is ruler-straight
  glowing ink with typed capitals. `single-line` is one unbroken morphing line. `pencil-sketch` is graphite that boils
  at 12 fps. `stick-webcomic` and `existential-stick` tell panelled stick-figure stories; `infographic` pops in icons.
- **Poor fit:** feelings (`storytime`), dense statistics (`data-visualization`), equations that transform
  (`3blue1brown`), product interfaces (`product-ui`), long text (`kinetic-typography`).
- **Do not:** erase, cut, fade or pop single items, type text, add a fourth colour, flat fills or shading. Keep the
  marker on every stroke and the board under the camera: without them it is a drawing app, not a whiteboard.

## Technical notes
- No render.json, fonts.css, vendor folder or WebGL: canvas 2D, 0.1–0.15 s a frame on one page, every started move
  redrawn each frame (a few hundred are fine). `common.js` is the shared kit (`W`, `H`, easing, `rng`, `mk`,
  `loadFont`, `Path`); change `W`/`H` there.
- Determinism: `rng(3)`, wobble seeded by move index, audio `default_rng(5)`. review.md's test differs by 1–3 levels in
  about 300 pixels (88 dB): the board's `imageSmoothingQuality = 'high'` upscale, which review.md counts as rounding.
- Hard-coded for 1920 × 1080: every value the 9:16 block changes, plus the fixed times `seg(t, Z1, 10)` in
  `cameraFor()`, `seg(t, 9.62, 10)` in `frame()`, and audio.py's pad 9.4 and duck 4.5 and 5.6.

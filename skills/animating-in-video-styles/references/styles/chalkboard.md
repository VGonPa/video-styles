# Chalkboard (`chalkboard`)

A lesson written and drawn in chalk on a green slate as it happens: hand-wobbled lines with a grainy tooth and
falling dust, round handwriting, white chalk for the working and yellow for what the lesson finds, and a felt
eraser that wipes half the board for the next problem. It draws on the classroom blackboard and the patient
teacher in front of it; the mood is calm, clear and a little nostalgic.

**Reference film:** "Lesson 3 · Pythagoras": a 3-4-5 triangle gets a square on each side whose cells are
counted (9 + 16 = 25 ✓), an eraser wipes the diagram, and a ladder word problem is drawn and solved to h = 4 m,
closing on a puff of chalk dust · `styles/chalkboard/`

## Signature
- A dark green slate fills the frame from the first frame (after a 0.3 s fade from near-black green): soft mottling, faint ghost swirls of old erasing, a vignette, and a wooden tray along the bottom with chalk powder and one white and one yellow stick at the right.
- Handwriting in Caveat Bold writes itself on, left to right, with no hand or chalk visible: the lesson title at the top left from 0.25 s, then a wobbly chalk underline.
- Every mark is grainy chalk: a fixed tooth mask breaks lines and letters into speckled, faintly streaked texture with a soft wide dust halo, and specks of dust fall from the chalk tip as it moves.
- A diagram builds stroke by stroke with a slight hand wobble and round ends, outline first, then labels written inside it; the first figure starts as the title settles and is outlined by about 2 s (in the demo: the triangle 1.2–1.9 s, its three squares by 2.8 s).

## Palette
| Role | Colour | In code |
|---|---|---|
| Slate, top / bottom of the gradient | `#26352e` / `#1b2621` | `paintSlate()` |
| Light / dark mottles; vignette edge | `rgba(120,150,130,0.05)` / `rgba(0,0,0,0.07)`; `rgba(0,0,0,0.42)` | `paintSlate()` |
| Ghost eraser swirls and swipes | `rgba(225,235,225,…)` at alphas under 0.07 | `paintSlate()` |
| White chalk: every line and word | `#f3f0e6` | `CHALK_WHITE` |
| Yellow chalk: results, the unknown, the tick, the answer's underline | `#f1d35f` | `CHALK_YELLOW` |
| Slate-coloured outline behind count digits | `#22302a` | `drawCount()` |
| Falling dust specks / puff cloud | `rgba(240,240,230,…)` / `rgba(240,240,232,0.26)` | `paintDust()`, `blob` |
| Drag streaks inside the wipe | `rgba(235,240,232,…)` | `streak` |
| Tray wood, top to bottom; powder; the white / yellow sticks | `#8a5a34`, `#6d4424`, `#58361c`, `#3a2312`; `rgba(235,235,225,…)`; `#efece2` / `#efd66a` | `paintTray()` |
| Eraser felt / wooden back | `#5d605c` / `#b99670`, `#9a774f`, `#6c5033` | `paintEraser()` |
| Fade in and out | `rgba(12,17,15,${dark})` | `frameAt()` |

- Two chalks only. White carries everything; yellow is kept for what the lesson finds (in the demo: count totals, 9 + 16
  = 25, h = ?, h = 4 m and their strokes), so the eye jumps to it. A third colour reads as another board.

## Typography and copy
- One face: Caveat 700 (`fonts/Caveat-700-latin.woff2`, `fonts/Caveat-700-latin-ext.woff2`), loaded by `loadFont()`
  in `common.js`, named `HAND_FONT`; no fonts.css. Demo sizes: title 100 px tilted −0.015 rad (`rot`); equations 150
  and 116; yellow results 130 and 140; labels on the drawing 76–84; counts 64 px, popping to 112.
- `drawLabel()` reveals text through a clip edge sweeping left to right, equal time per character (`writtenWidth()`
  over widths from `measureLabels()`), filled twice 0.8 px apart over a 10 px stroke at 0.07 alpha. Text never moves;
  `hide` fades a label out over 0.15 s. Pace: 21 title characters in 0.7 s, working lines 22–28 a second, labels of
  two in 0.12 s; the 6 s plan's 50 a second (about one glyph a frame at 30 fps) still writes glyph by glyph.
- Copy is a teacher's board: a "Lesson 3 · Topic" title, then equations and values with units (3 m), not sentences;
  labels of one to three characters on the drawing; the unknown as a yellow question, the answer yellow and underlined.
- Width: Caveat runs 0.34–0.39 of its size per character in real lines (title 0.36, equations 0.34–0.38, digit-heavy
  0.39; digits alone 0.45); budget 0.38. 16:9, a line centred on `RX`: about 14 characters at 150 px, 16 at 130, 18
  at 116 (measured on the last frame: 14 at 150 px end 28–51 px from the right edge, 16 at 130 and 18 at 116 end
  46–77 px; one character more ends 3–50 px from it). 9:16: the title at x 80 holds about 22 characters at 100 px
  ("Lesson 3 · Pythagoras" is 755 px; 25 characters, 883 px, ran into the right band); a column line centred on x 460
  at 120 px, or on 420 at 104 px, about 16 (rendered: "1250 ÷ 25 = 50 m" and "v = 240 ÷ 3 = 80" with its tick span
  x 90–854 on the last frame; 20 and 24 ran off the left edge). Longer copy takes a second line or a wipe.
- Glyphs: Latin-1 and Latin Extended-A (ñ ç ß ł ő š ž), ² ³ ¹, × ÷ ± −, °, ·, ½, € £, curly quotes, dashes, ….
  Missing, so a fallback face appears: subscripts (write CO2), arrows, √, π, ≈, ≠, ≤, ≥, ∞, ✓, Greek, Cyrillic,
  CJK. Draw a missing symbol as strokes, as the demo draws its tick with `stroke()`, or add a font (contract.md).

## Texture and finish
- `paintSlate()` paints `slateLayer` once (`rng(11)`): gradient, 140 mottles, 16 curved ghost swipes of 26 arcs and
  10 straight ones, ±4.5 grain, vignette; `paintTray()` adds wood, 90 grain lines, the lip, 1400 powder specks and two
  `stick()` sticks. Static.
- `chalkTooth` is a full-frame alpha mask built once with `rng(5)`: rows at 0.82 ± 0.18 (two sines: faint horizontal
  streaks), pixels 0.72–1, 16 % pits at 0.15–0.45. `paintChalk()` draws every mark into the offscreen `chalk` layer,
  then applies it with `destination-in`: one grain for all chalk that never crawls. A mark drawn straight onto the
  main canvas misses the grain and the wipe. Halo: `drawLine()` strokes each path 12 px wider at 0.07 alpha first.
- Dust: `scatterDust()` builds `parts` once in `window.ready`: specks at `chalkTip()` 90 times a second (55 % kept)
  while a line or label draws, four per ticked cell, three every 1/120 s along the eraser, 160 at the puff; each falls
  ever faster (90 px × age²) and fades over 0.5–2.4 s (tip specks 0.6–1.7). `puffs`: 26 soft `blob` clouds swelling
  from 0.6 to 2.8 times their size as they slow. `paintDust()` draws both from `t` alone.
- The wipe: `wipeOut()` stamps the soft `eStamp` (the `ER` footprint, 250 × 92, blurred 9 px) every 7 px along `ePath`
  up to the eraser's reach, cuts it from the chalk at 0.92 (an 8 % ghost stays) and lays the `streak` drag lines inside
  at 0.14, to the end. No bloom, scanlines, grade or refreshed grain; only the push and fades change the whole frame.

## Shapes, line and figures
- Every line is a `Path` built with `P()` from `common.js` (`M`, `L`, `S` for a smooth curve through points, `A`
  for an arc), drawn by `stroke(path, t0, t1, { jit, color, width, ease })` or `poly(pts, t0, t1, o)`. `stroke()`
  calls the path's `jitter()`, 1.8 px by default: a slow two-sine hand wobble, never noise (grid lines `jit` 1;
  hatching, bricks and rungs 0.5–0.6). Weights: main lines 8 (default) or 7, right-angle marks and rungs 5, grid,
  hatching and bricks 3; round caps and joins.
- A teacher's diagram, not an illustration: outlines with conventions (right-angle marks, hatched ground, brick
  courses) and labels with units, built in order: outline, detail (grid, rungs, bricks), labels, then the yellow
  question or result. The only fill is a counted cell: `drawCell()` pops an inset quad (80 %), 0.45 to 0.2 alpha.
- A new object belongs when it is a few 7–8 px white strokes, curves from `S()` and circles from `A()`, built in that
  order, with yellow kept for findings. Rendered in 9:16: a potted plant (closed `S()` loops for leaves, an `A()`
  bud), a sun with eight ray strokes and straight arrows with two-stroke heads read as the same board.
- No people in the demo. A figure is a 7 px chalk outline: an `A()` head with a nose bump for a profile, neck,
  shoulder line, torso, limbs bent at elbow and knee, simple hands. If the brief does not need one, use objects.

## Composition and camera
- 16:9: title top left (x 150, baseline 150) with its underline; the drawing fills the left half (scene 1 x 260–860,
  y 260–920; the ladder x 220–890); a column centred on `RX` (1420) holds the equations at baselines 400, 570, 750 and
  900; the tray takes the bottom 76 px (`TRAY` = 1004). The eraser clears only the drawing half, so the column
  carries the lesson across problems. One flat board: the only move is a 4 % push on the centre over the film
  (`zoom` in `frameAt()`, `eio2(seg(t, 0, 10))`), shared by everything but the fades. One focus at a time.
- 9:16 (1080 × 1920; rendered with the demo restacked and with a stand-in): set `W`, `H` and the canvas, then
  - `TRAY` = H − 76; the vignette's two centres at (W / 2, H / 2 − 60) and (W / 2, H / 2), radii 520 and 1250 as
    before; the `stick()` calls at x W − 440 and W − 298; the push about (W / 2, H / 2).
  - The push carries edges out by 4 %: keep key text inside y 314–1420 and x ≤ 934 at scale 1 to stay clear of
    review.md's bands (top 288, bottom 1440, right 950) on the last frame.
  - Stack: title at x 80, baseline 392, 100 px (its top reaches y 292 on the last frame), underline (76, 426) to
    (820, 412); one drawing zone, y 490–1140 across x 60–930 (scene 1 at `U` 56, `Cx` 363, `Cy` 891: 560 × 616 px);
    under it a two-line column: 120 px centred on x 460 at baseline 1295, 104 px centred on 420 at 1410, its tick
    through (673, 1376), (693, 1399), (735, 1336). Below, y 1440–1844 stays bare slate (its mottling and ghost
    swipes continue; no chalk): review.md keeps it for the platform's captions; linework may dip in, never a label.
  - The wipe clears the zone and spares the column: passes between y 490 and 1138 (path below). Surviving chalk
    needs 60 px beyond the path's ends and 140 px beside its outer passes. In `eraserPose()` send the eraser out to
    y 640 instead of 300, or it leaves across the title.
  - The second drawing shares the zone with two lines on its right: ladder `S` 120, `WX` 470, `GY` 1050, ground x
    40–550, hatches from x 65 to under 545, wall up to GY − 540, bricks from GY − 490; h = ? at (365, 870) 76 px;
    h² = 25 − 9 at (757, 810) 84 px; h = 4 m at (757, 970) 116 px; underline (590, 998) to (925, 994); `PUFF` at
    (935, 992). This needs a second drawing under about 520 px wide: the board has no other room for working lines.
  - Stand-in (a 590 px plant with a sun, arrows and labels across x 100–870): it fitted the zone, but the demo's
    path left its outer labels and sun; the path, `U`, `Cx`, `Cy` and the ladder depend on the subject's footprint:
```js
// 9:16, demo diagram (U 56)
P().M(260, 490).S([[274, 816], [260, 1138], [363, 1124], [456, 816], [461, 490], [559, 499], [652, 816], [662, 1138], [727, 966], [680, 704]], 26)
// 9:16, footprint x 60–930: every pass reaches top and bottom at its own x, with rounded turns
P().M(175, 500).S([[180, 815], [175, 1125], [280, 1145], [385, 1125], [390, 815], [390, 500], [495, 485], [600, 500], [605, 815], [605, 1125], [705, 1145], [800, 1125], [805, 815], [805, 500]], 26)
// 1:1, demo diagram (U 48); first pass at x 160 keeps the eraser in frame, right passes pulled in to spare the column
P().M(160, 306).S([[170, 586], [160, 862], [225, 850], [280, 586], [284, 306], [368, 314], [430, 586], [440, 862], [480, 714], [430, 470]], 26)
```
- 1:1 (1080 × 1080, rendered): kit as in 9:16, layout side by side as in 16:9. Title at x 90, baseline 150, 100 px,
  underline (86, 184) to (830, 170); scene 1 at `U` 48, `Cx` 200, `Cy` 650 (x 56–536, y 314–842); `RX` 800, 92 px at
  400, 78 px at 560 centred on RX − 39 (tick (950, 535), (965, 552), (996, 505)); the path above; ladder `S` 105, `WX`
  480, `GY` 880, ground x 60–560, hatches from x 85 to under 555, wall up to GY − 460, bricks from GY − 420; h = ? at
  (366, 770) 76 px; h² = 25 − 9 at (RX, 740) 84 px; h = 4 m at (RX, 890) 100 px; underline (635, 918) to (960, 914);
  `PUFF` (970, 912). The column ends at x 1022 on the last frame, and line 2 survives the wipe.

## Motion
- Each mark has its own window [t0, t1] in `marks`. Lines reveal along their length, linearly by default; the final
  underline uses `eout`. A figure's strokes follow one another closely, like one hand (0.02 s gaps, or overlaps up
  to 0.06 s); runs of small marks overlap (grid lines 0.05 s each, 0.028 s apart).
- Pops are the only overshoot: a cell with `eback` over 0.08 s, a count total growing from 64 to 112 px with
  `eback()` (overshoot 2.4) over 0.28 s as it turns yellow.
- The eraser, the only object that travels and the only transition (no cuts or cross-fades), slides in from the left
  with `eio2` (0.25 s), follows `ePath` with `eio2` (0.8 s) and lifts away up-left (0.35 s), its blurred shadow
  moving off (`lift` in `paintEraser()`). Smooth 30 fps; a written mark never moves, scales or redraws (counts aside).

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.3 | Fade in from near-black green | `frameAt()` (`dark`) |
| 0.25–1.12 | Title writes on (0.25–0.95); underline (0.97–1.12) | `text()`, `stroke()` |
| 1.2–1.9 | Triangle: base, height, hypotenuse, right-angle mark | `poly()`, `U`, `Cx`, `Cy` |
| 2.12–2.94 | A square on each side; a², b², c² written inside | `poly()`, `add2()`, `NN` |
| 2.96–3.46 | a² + b² = c² heads the working column | `text()`, `RX` |
| 3.45–4.0 | Grid lines inside the squares, 0.028 s apart | `poly()` |
| 3.95–5.27 | Cells ticked one by one as each count runs up; totals pop yellow at 4.31, 4.75, 5.27 | `countSquare()`, `drawCell()`, `drawCount()` |
| 5.35–5.9 | 9 + 16 = 25 in yellow, then a drawn tick | `text()`, `stroke()` |
| 5.9–7.3 | Eraser slides in, wipes the drawing half in up-and-down passes (6.15–6.95), lifts away | `ERASE`, `ePath`, `eraserPose()`, `wipeOut()` |
| 7.0–8.0 | Ladder problem: ground and hatching, brick wall, rails, rungs, 5 m, 3 m, h = ? in yellow | `S`, `WX`, `GY`, `F`, `T` |
| 8.05–8.98 | h² = 25 − 9; h = 4 m in yellow; yellow underline | `text()`, `stroke()` |
| 8.98 | Dust puff at the end of the underline | `PUFF`, `puffs`, `paintDust()` |
| 9.45–10 | Fade to near-black green (the puff still billowing) | `frameAt()` (`dark`) |

- Reusable grammar: title, a figure in about 1.6 s, the rule atop the column, a tally turning white into yellow, a
  0.25 s pause, the wipe (1.4 s), an applied problem in about 1 s, its working, the underlined answer and puff.
- The demo's ending is short (a known defect): its fade starts 0.47 s after the puff. Without the fade the cloud is
  visible at `PUFF.t` + 1.2, faint at + 1.3–1.4, gone by + 1.5: start the fade at least 2.3 s after the puff (1.5 s
  to settle, then the 0.8 s hold), with the specks capped and the push stopped at HOLD = `PUFF.t` + 1.5 (the HOLD
  code in Shorter; in 9:16 the underline's specks otherwise move until + 1.7).
- Review keys (contact_sheet.sh): 5.95 (first result), 6.5 (mid-wipe), 9.4 (answer and puff); in a new film, its
  first result, mid-wipe and the settled final state (HOLD + 0.1).

## Sound
audio.py reads `events.json` (cues with a kind `k` and a time `t`) and synthesizes 48 kHz stereo from noise and
sines, `DUR` 10.0. The film's events function derives the cues from the marks, so new scenes are scored for free:
- `chalk` (`d`, `v`): a gritty scratch with a faint squeak per line; `d` its draw time (at least 0.04), `v` 1 for
  widths of 7 and more, 0.5 below (gain 0.16 × `v`). `write` (`d`, `n`): `n` short scratches over `d`, `n` being the
  label's characters without spaces. `tap`: a click per ticked cell. `ding`: a board knock (`knock()`) per total.
- Pushed by hand at the end of the events function: `thud` (0.02 s before the wipe), `erase` (`d` = the wipe's
  length; `passes` in `erase()` writes 4.5 evenly spaced swells over `d`, which the demo's 3.5 eased passes only
  roughly follow: set it near your path's pass count) and `puff` (a soft burst plus a tap, at the puff's time).
- What breaks it (tested): `chalk` without `d` or `write` without `n` raises KeyError; a `write` with t1 before t0
  (negative `d`) can raise ValueError, and so does an `erase` with `d` 0. Pans are random in fixed ranges, so no field
  can push one past ±1; a large `v` only saturates the limiter (peak 0.8). Unknown kinds are skipped silently.
- Bed: room tone (`room`) and a 60/120 Hz hum (`hum`) over the buffer, no music; 0.2 s fade-in, 0.6 s fade-out (`fo`),
  soft limiter. Nothing at fixed times, no cue looked up by name: set `DUR`; cues past it are dropped silently.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Slate, ghost swipes, vignette, tray; chalk grain | `anim.html` → `paintSlate` | `paintSlate(g, rand)` once into `slateLayer`, calling `paintTray(g, rand)`; `chalkTooth` mask built once | as is |
| Timed line, polyline | `anim.html` → `stroke` | `stroke(path, t0, t1, { jit, color, width, ease })`: defaults 1.8 px wobble, `CHALK_WHITE`, width 8, linear; `poly(pts, t0, t1, o)` strokes straight segments through points | as is |
| Handwriting | `anim.html` → `text` | `text(str, x, y, size, t0, t1, { color, align, rot, w8, hide })`: written over t0–t1, anchored left or centre, turned by `rot` about the anchor | as is |
| Path builder | `common.js` → `Path` | `P().M(x, y).L(x, y).S(pts, steps).A(cx, cy, rx, ry, from, to)` | as is |
| Count-up | `anim.html` → `countSquare` | `countSquare(n, cell, cx, cy, t0, dt)`: ticks n × n quads from `cell(i, j)` dt apart while a count runs at (cx, cy); the total pops yellow | adapt: any tally (cells, dots, coins) |
| Eraser wipe | `anim.html` → `wipeOut` | `ERASE` {t0, t1, in0, out1}, `ePath`, `eraserPose()`, `paintEraser()`; marks with t0 before `ERASE.t0` are wipeable (`preWipe`) | adapt: a path over the new drawing |
| Dust and puff | `anim.html` → `scatterDust` | specks for every mark automatically; `PUFF` {t, x, y} | as is; move `PUFF` |
| Painters | `anim.html` → `PAINTERS` | `drawLabel`, `drawLine`, `drawCell`, `drawCount` keyed by mark kind; `inkMark()` wraps each in save/restore | as is; a new mark kind needs a painter here and a branch in `window.events` |
| Frame | `anim.html` → `frameAt` | push (`zoom`), layers, dust, eraser, fades | adapt: the push's `seg(t, 0, 10)` and the 9.45–10 fade |
| Sounds | `audio.py` → `chalk` | cue kinds in Sound | as is; set `DUR` and the `erase()` pass count |
| The lesson | `U`, `Cx`, `Cy`, `RX`, `S`, `WX`, `GY`, `PUFF` and the times in each call | | replace |

## Adapting
- **Style vs demo plot:** the style is slate and tray, grain, halo and dust, Caveat written on, white working and
  yellow findings, wobbly figures built in order, the eraser wipe and its ghost as the scene change, the push, the
  fades, the yellow underlined answer (with the puff when there is time), and the tally (cells, dots or coins ticked
  white, totalled in yellow). Demo plot: Pythagoras, the unit squares counted cell by cell, the ladder, all copy. A
  transformation: the wipe to a new problem, a tally filling a figure, the unknown turning yellow.
- **New subject:** one idea per board, in a teacher's order: title, figure, labels, rule, worked example, yellow
  result. Replace every call between the title and `PUFF`; keep the kit. Traps: anything with t0 before `ERASE.t0`
  in the eraser's reach becomes a ghost (keep survivors 140 px beside the outer passes, 60 px beyond the ends); turns
  that cut corners leave stubs (the demo leaves one dash), so let each pass reach top and bottom at its own x;
  `stroke()` seeds each wobble with the mark's index, so inserting a mark changes later wobbles (harmless).
- **Length:** a board carries 4–6 s (6 s and 3 s in the demo); past 10 s add boards, one wipe every 6–10 s. A second
  wipe is code you add: split `marks` into three groups by two wipe times and in `paintChalk()` draw group 1, wipe,
  group 2, wipe, group 3; pass the path to `wipeOut()` (it clears its canvas each call); make `eraserPose()`, the
  eraser window in `frameAt()` and the eraser dust in `scatterDust()` loop over a list of wipes; a `thud` and an
  `erase` cue per wipe. Re-time the push, the fade, audio.py's `DUR` and build.sh's `DUR`; a few hundred marks are fine.
- **Shorter:** down to about 6 s keep both boards and the wipe; shorten the count (`dt` down to 0.01), the wipe
  (0.6 s still reads), the writing (up to 50 characters a second) and the holds; drop the a², b², c² placeholders,
  and the puff unless 2.3 s remain before the fade. Under 6 s cut whole beats: the second problem and the wipe
  first, then the count. The signature reads by about 0.9 s (fade-in 0.3 s, title from 0.15 s, first stroke
  0.75–0.87 s); the title (0.6 s with its underline) stays, so there is no separate card. To drop the wipe or puff,
  move `ERASE` or `PUFF.t` past the end rather than delete them (`preWipe`, `scatterDust()`, `eraserPose()` and
  `window.events` read them); their cues then fall outside audio.py's buffer.
  - The hold counts from when the dust has settled, not from the last stroke: tip specks fall about 1.3 s after it
    in 16:9 (out of the frame), 1.5 s in 9:16, and the puff takes 1.5 s. Both plans cut them at a HOLD time (the last
    stroke's end, or `PUFF.t` + 1.5) and end the push there too, where `eio2` reaches zero speed; the fade starts
    0.85 s after HOLD or later. Raw-canvas difference: still from HOLD + 0.07, pixel-identical from HOLD + 0.1:
```js
const HOLD = 2.9;   // specks die by HOLD + 0.05 and the push stops at HOLD
const speck = (t0, x, y, vx, vy, life, s, a) => ({ t0, x, y, vx, vy, life: Math.min(life, Math.max(0.05, HOLD - t0)), s, a });
// in frameAt(): const zoom = 1 + 0.04 * eio2(seg(t, 0, HOLD));
```
  - 6 s, 16:9 (rendered, audio.py peak 0.623): fade in 0–0.3; title 0.15–0.65, underline 0.65–0.75; triangle
    0.75–0.87, 0.88–0.98, 0.99–1.13, mark 1.13–1.18; squares 1.17–1.33, 1.29–1.45, 1.41–1.59; rule 1.57–1.9; grid
    from 1.72, 0.015 s apart; counts at 1.92 (`dt` 0.028), 2.12 (0.014), 2.3 (0.01); result 2.55–2.82, tick
    2.83–2.9; `ERASE` {t0 3.1, t1 3.7, in0 2.9, out1 4.0}; ladder ground 3.75–3.85, hatches from 3.78 (0.004 apart),
    wall 3.8–3.9, bricks from 3.85 (0.007 apart), rails 3.9–4.02 and 3.94–4.06, rungs 4.03 + k × 0.01, mark
    4.1–4.15, 5 m 4.12–4.2, 3 m 4.2–4.28, h = ? 4.28–4.4, h² = 25 − 9 4.4–4.62, h = 4 m 4.62–4.8, underline
    4.8–4.9; no puff; HOLD 4.9 (still 4.95–5.75); fade 5.75–6.
  - 4 s, 9:16 (rendered, audio.py peak 0.595): scene 1 as in the 6 s plan up to the tick at 2.9, in the 9:16
    layout; no wipe, no second problem; HOLD 2.9 (still 2.95–3.75); fade 3.75–4; audio.py `DUR`
    4.0. The count-up is the transformation.
- **Other formats:** rendered 9:16 and 1:1 layouts are in Composition, the sizes to move in Technical notes.

## Boundaries
- **Distinct from:** `whiteboard` is coloured marker on white, drawn by a visible marker with a following camera;
  here grainy chalk on slate, no hand, scenes changed by an eraser. `3blue1brown` is crisp vector maths on black with
  smooth morphs. `blueprint` is ruler-exact drafting in one glowing ink. `pencil-sketch` is graphite on paper.
- **Poor fit:** character stories and emotion (`picture-book` or `existential-stick`), dense statistics
  (`data-visualization`), equations that transform step by step (`3blue1brown`), product launches (`product-ui`).
- **Do not:** add a third chalk colour, fills beyond counted cells, a drawing hand or chalk, typed or fading-in
  text, or sentences of copy. Keep the slate and tray even off-topic: without them it is handwriting on green.

## Technical notes
- No render.json: plain canvas 2D, no GPU or vendored libraries. Stills take about 0.15–0.2 s each on one page
  (Apple silicon): a 10 s build takes under a minute. `common.js` is the shared kit (`W`, `H`, easing, `rng`, `mk`,
  `loadFont`, `Path`): change `W`/`H` there; `slateLayer`, `chalkTooth`, `streak` and the layers follow them.
- Deterministic (`rng(11)`, `rng(5)`, `rng(9)`, `rng(21)`, wobble seeded by mark index; audio `default_rng(6)`):
  `paintChalk()` redraws every started mark, layers clear each frame and `inkMark()` wraps painters in save/restore.
- Hard-coded for 1920 × 1080: the canvas attributes; `TRAY` = 1004; the vignette (960, 480, 520 → 960, 540, 1250);
  the `stick()` x values 1480 and 1622; the push centre `960 - 960 * zoom, 540 - 540 * zoom`; the eraser's entry from
  (−320, 560) and exit to (−300, 300) in `eraserPose()`; every layout number (title 150, 150; underline; `U`, `Cx`,
  `Cy`, `RX`, `ePath`, `S`, `WX`, `GY`; ground 220–890, hatches 250–880, wall top 330, bricks from 380, h = ? at
  (694, 704), the answer underline, `PUFF`). The eraser `ER` (250 × 92) does not scale with the frame.

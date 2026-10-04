# Bauhaus (`bauhaus`)

A Bauhaus exhibition poster that builds itself: circle, square and triangle in flat primaries assemble into a
functional object on a visible grid under flush-left grotesque capitals, then a black block flips half the sheet. The
movement's grammar, not any one poster; calm, constructive, exact.

**Reference film:** a circle, a square and a triangle land on a floor line and assemble into a desk lamp; the switch
clicks, a black block drops over the right half, the beam splits into a triangle composition and type bars finish the
invented poster "LIGHT & FORM — Workshop Exhibition 1926" · `styles/bauhaus/`

## Signature
- Warm paper (`C.paper`) under a hairline grid (12 columns, both edges of every gutter, four horizontal rules) that
  grows down and across in the first second (0.05–0.95 s), with a static print grain over everything.
- A huge flush-left black headline in extended Archivo 900 capitals, tight-tracked, its letters rising one by one out
  of a mask on the baseline (0.35–1.4 s); a small tracked kicker with a short red rule; a heavy black floor rule.
- The three elementary shapes in flat primaries, no outlines, standing on the floor by 1.95 s: a yellow circle with a
  black quarter that turns as it rolls in, a blue square with a red dot that tumbles down, a triangle split into red
  and black halves that rises out of the floor.
- Asymmetric balance: the type mass top left, the geometry bottom right, paper left open; nothing is centred.
- From 2.3 s the shapes assemble into one object, joined only by black rods and round joints (complete at 3.5 s): the
  kit is the subject.

## Palette
| Role | Colour | In code |
|---|---|---|
| Paper (background, fades, line work inside the block) | `#eee8dc` | `C.paper` |
| Ink: headline, floor rule, rods, the black block | `#121212` | `C.black` |
| Red: triangle face, square's dot, switch, kicker rule, first bar | `#d02020` | `C.red` |
| Blue: square, lamp base, light pool, third bar | `#1040c0` | `C.blue` |
| Yellow: circle and bulb, beam, year, second bar | `#f0c020` | `C.yellow` |
| Unlit bulb (blended in as the circle flies up) | `#d6cdbb` | `C.unlit`, `blend()` |
| Grid on paper; grid inside the block | `rgba(18,18,18,0.11)` `rgba(238,232,220,0.07)` | `drawGrid()` |

- Flat fills only: one primary per shape, its second half or a quarter in black (paper inside the block). No
  gradients, tints, shadows or glow. Text is black on paper, paper or black on bars, yellow and paper on the block.

## Typography and copy
- One family, Archivo, variable (weights 400–900, widths 62–125 %), two files in `fonts/` (Latin and Latin Extended
  subsets) declared in `fonts.css`; `setType()` sets weight, size, width and tracking.
- Headline: 900, 164 px, `expanded`, track −6, capitals, flush at `MARGIN` − 6, two lines 176 px apart, drawn by
  `riseText()`: each letter rises 1.1 em out of a mask on its baseline in 0.55 s (`Ease.out`), 0.05 s apart. Bars:
  800, 44 and 34 px, `expanded`, track 2, letters 0.016 s apart. Year: 900, 190 px, normal width, track −6, yellow,
  digits 0.06 s apart. Kicker (set in `render()`) and captions (`caption()`): 700, tracked 3, 24 px, or 22 px when
  `caption()` gets an alpha; they fade in. Text never slides or scales; only the labels leave, into their mask.
- `riseText()` adds its track to an advance that already includes it, so the headline sets about 140 px a capital
  ("& FORM" 796 px): 6 capitals a line in the 16:9 text column (x 90–960). Bars: 44 px a capital at 44 px, 35 at 34; a
  bar's width is text + 24 px inset + 10 px or more, and its 3 % `Ease.settle` overshoot must stay left of 960.
  Kicker: 20 px a capital. At another size scale the track with it (−6 × size / 164, so −4 at 120 px), or letters
  fuse: the 1:1 headline at 120 px sets about 98 px a capital, 9 a line.
- Copy is poster information: a one- or two-word title per line, a category kicker ("EXHIBITION POSTER — NO. 3"), one
  fact per bar (what, when, where), a big number, a practical caption. Capitals, nouns and numbers, no sentences; an
  em dash or a middle dot as the only punctuation. Longer copy is another bar or a smaller headline, never a wrap.
- Glyphs: Western and Central European Latin, Turkish, €, ™, −, ↑ ↓; partial Vietnamese, no Greek or Cyrillic. Accents
  fit `riseText()`'s mask (Å reaches 0.94 em of its 0.95). Add every new string to `FONT_CHECKS`: a Latin Extended
  letter (Ł, ğ) missing from its samples draws in a fallback face on each page's first frame (tested).

## Texture and finish
- `makeGrain()`, once in `window.ready`: a full-frame speckle of black and white pixels (xorshift, alpha up to
  17/255), drawn over everything at 0.55 every frame. It never changes, so it reads as print, not film grain.
- `drawGrid(t, colour)`: 1.5 px hairlines on `GRID_V` (each column edge) and `GRID_H` (rows at `MARGIN`, under each
  headline baseline, and `H` − `MARGIN`); verticals grow over 0.6 s, rows 0.65 s; the block redraws it in paper at 7
  %.
- Nothing else: no halftone, misregistration, paper texture, vignette, bloom or blur.

## Shapes, line and figures
- Everything is circle, square or rectangle, equilateral triangle and straight rod, filled flat with sharp corners.
  Kit: `disc(x, y, r, colour)`, `poly(pts, colour)`, `rod(p, q, width, colour)` (butt caps), `triangle(cx, cy, side,
  angle)` (corners, angle 0 apex up), `twoTone(cx, cy, side, angle, face, half)` (the right half in a second colour).
- The only strokes are the grid, the 22 px rods and the switch-on ring. Joints are discs (22, 20, 18 px) with a 7 px
  red pin; a black quarter on a circle shows it turning; the floor is an 8 px rule. Demo sizes: circle r 90, square
  180, triangle side 210, shade 230, bulb r 40, base slab 300 × 60. Inside the black block the same object redraws
  with its line work in paper (`drawLamp(t, inverted)`).
- A new object: split it into those parts, give each part one primary and at most one black half or quarter, join them
  with rods and joint discs, stand it on the floor rule, and number its parts in tracked capitals if the film explains
  them. Keep forms frontal and flat: no perspective, no curves but full circles and their halves or quarters. No
  people in the demo: a figure of discs and rods reads as a diagram, so tell stories with objects.

## Composition and camera
- 16:9: `MARGIN` 96, `NCOL` 12, `GAP` 24, so `COLW` is 122 and `col(i)` = 96 + 146 i. Columns 0–5 hold type, flush
  left; columns 6–11 (from `PANEL_X`, x 960) hold the object, which the block covers. Kicker at y 150, rule at 165,
  headline baselines 340 and 516, `FLOOR` 900, bars at 612, 706, 780 (widths 820, 640, 740: a stepped edge), year
  right-aligned to `W` − `MARGIN` at 262, caption at 312. The block covers whatever the paper side drew under it: keep
  paper-side copy left of x 960. One fixed poster: no camera move, zoom or shake.
- 9:16 and 1:1 recompose as a stack (type above, block and object below); every value below was rendered:

```js
// 9:16 — canvas width="1080" height="1920" (W, H follow it); a new BLOCK_Y = 1080
MARGIN = 72, NCOL = 6, GAP = 24; FLOOR = 1670; PANEL_X = MARGIN; GRID_H = [MARGIN, 570, 770, BLOCK_Y, H - MARGIN]
kicker fillText y 330, red rule y 345; headline riseText(..., MARGIN - 6, 550, 164) and (..., MARGIN - 6, 726, 164)
BARS y 822, 916, 990 (h, w, px as 16:9) with t0 1.5, 1.65, 1.8: they land during the build (see below)
lamp, every x 900 px left: SQUARE.x 500, CIRCLE.x 200, TRI.x 800, BASE.x 790,
  PIVOT = [750, FLOOR - BASE.h], ELBOW = [640, FLOOR - 325], HEAD = [430, FLOOR - 505]
SATELLITES { x: 205, y: FLOOR - 430 } and { x: 860, y: FLOOR - 210 }
blockClip(): x0 = i === 0 ? 0 : col(2 * i) - GAP / 2, x1 = i === 2 ? W : col(2 + 2 * i) - GAP / 2 + 1;
  ctx.rect(x0, BLOCK_Y, x1 - x0, (H - BLOCK_Y) * k)        // thirds of the width drop from BLOCK_Y
year: setType(900, 150, ...) for yearW and riseText(t, '1926', 940 - yearW, 1240, 150, ...); caption at x 940, y 1286
drawLabels(): clip rect(0, FLOOR - 290, W, 90), caption at FLOOR - 236, translate(0, -90 * away)   // above the shapes
// 1:1 — canvas 1080 x 1080: the same stack; the lamp keeps FLOOR 900 in its own coordinates and is drawn at 0.8
MARGIN = 64, NCOL = 6, GAP = 24, PANEL_X = MARGIN, BLOCK_Y = 588; lamp x as 9:16 (ELBOW [640, 575], HEAD [430, 395]);
  SATELLITES x 205, 860 (y as 16:9); blockClip() as 9:16; GRID_H = [MARGIN, 234, 363, BLOCK_Y, H - MARGIN]
const LS = 0.8, LX = 170, LY = 304, FLOOR_S = LY + LS * FLOOR;   // FLOOR_S 1024; at LX 200 the caption ends 14 px from the elbow
const lampSpace = () => ctx.transform(LS, 0, 0, LS, LX, LY);
render(): ctx.save(); lampSpace(); drawLamp(t, false); ctx.restore();  (drawBars(t), drawLabels(t) stay outside);
  in the block ctx.save(); lampSpace(); drawBeam(t); drawLamp(t, true); ctx.restore(); the flash ring likewise;
  both floor rules at y FLOOR_S
drawBase(): the square starts at y -560, not -300 (LY + LS * y0 must be -102 or less, or it pops into view)
kicker y 84, rule 99; headline 120 px, track -4 (in head), at MARGIN - 5, baselines 214, 343; BARS y 388, 462, 520,
  h 62, 46, 46, w 680, 512, 620, px 35, 27, 27, t0 1.5, 1.65, 1.8; year 120 px, track -4, right edge W - MARGIN,
  baseline 716; caption (W - MARGIN, 760); drawLabels() in screen space (22 px): clip rect(0, FLOOR_S - 267, W, 72),
  caption at x LX + LS * x, y FLOOR_S - 224, translate(0, -72 * away)
```
- Why the bars move into the build in 9:16 and 1:1: at their demo time the middle of the frame stays bare (36 % at
  2.0 s, 22 % until 6.0 s). Landed at 1.5 s, the largest held band is 19–20 % (2.0 s), and from 2.9 s at most the top
  313 px (9:16); larger bands show only while things move (38–49 % in the opening to 1.45 s, 23–34 % while the bars
  grow and the parts fly).
- 9:16 check: every Signature item whole in every beat; the square falls from above the frame across the headline
  (1.35–1.5 s, also in 1:1: a fast pass). Text in x 72–936, y 313–1436, clear of review.md's bands; the shapes (y
  1488–1670), lamp foot, pool and base sit in the bottom band (burned-in captions would cover the shapes at 2 s).
- Stand-in (9:16 clock tower, 260 × 560 px at x 160–420): layout held. Subject-dependent: its height (at most `FLOOR`
  − block top − 30), the year (beside the subject's top, 30 px clear), the pool and `SATELLITES` (one landed on the
  roof; x 600, y `FLOOR` − 250 and x 840, y `FLOOR` − 120 fill the quarter the tower leaves).

## Motion
- Easing (`Ease`): `out` (exponential) for letters, arms, the triangle's rise, the pool and the grid; `in` for the
  labels leaving; `both` (exponential in-out) for the morph, flip, hop, block strips, split and the fade-out (the
  fade-in is linear); `settle`, a cubic with a 3 % overshoot, for the rolling circle, joint pops, satellites, bars and
  beam. The square falls with gravity (progress squared), turning a quarter, and wobbles 8 px on landing. Smooth 30
  fps.
- Actions take 0.3–0.95 s and overlap in staggers (letters 0.05 s, labels 0.1, strips 0.07, bars 0.15, slices 0.12).
- Nothing moves once settled (no ambient drift or idle loop): the hold is a frozen poster. Never: outlines,
  perspective or 3D turns, camera moves, glow or motion blur, rotation of text, a cross-dissolve or a hard cut,
  rubbery squash and stretch, bounces beyond the square's one wobble.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.95 | Fade up from paper (linear, 0.25 s); the grid grows down and across | `render()`, `drawGrid()`, `GRID_V`, `GRID_H` |
| 0.35–1.4 | LIGHT, then & FORM rise letter by letter; floor rule draws 0.45–1.1 | `riseText()`, `FLOOR` |
| 0.75–1.95 | Circle rolls in from the right and overshoots; square tumbles from above, lands 1.65, wobbles; triangle rises out of the floor; kicker 1.2–1.5, red rule 1.3–1.7 | `drawBulb()`, `drawBase()`, `drawShade()` |
| 1.75–2.6 | Numbered labels fade in under the floor, drop away from 2.25 | `drawLabels()`, `LABELS` |
| 2.3–3.5 | Assembly: the square flattens into the base (its dot becomes the switch), joints pop, arms extend, the triangle flips onto the head, the circle hops into the shade and dims | `drawBase()`, `drawArms()`, `drawShade()`, `drawBulb()`, `HEAD` |
| 3.66–4.34 | Switch pressed; at 3.8 the bulb turns yellow, a ring flashes (to 4.3) and three black strips drop over the right half, inside which the lamp redraws in paper | `SWITCH`, `LIGHT_ON`, `blockClip()`, `drawLamp()` |
| 4.2–4.62 | A yellow beam opens to the floor | `drawBeam()`, `BEAM_L`, `BEAM_R` |
| 5.0–6.15 | The beam cuts into four fanning slices that recolour (5.25–5.61); a blue half-disc rises with a black triangle; two two-tone satellites spin in | `SLICE_COLOURS`, `SLICE_DROP`, `SATELLITES` |
| 6.0–7.23 | Bars grow and their text rises; 1926 rises from 6.55; caption fades 6.95–7.2 | `BARS`, `drawBars()`, `caption()` |
| 7.23–9.6 | Hold, 1.97 s measured; fade to paper 9.2–9.6 | `render()` |

- Reusable: opening, shapes (labelled if the film explains them), assembly, block inversion, slicing, type bars (at
  the finish, or with the build in 9:16 and 1:1), a big number, hold, fade. One-off: the lamp, beam, pool, satellites,
  copy.
- Holds: pixel difference against the end state with the closing fade off (no ambient motion: the last frame).
- KEYS for contact_sheet.sh: 2.2 (shapes and labels), 3.55 (lamp assembled), 4.05 (strips falling, ring), 6.15 (split,
  pool and satellites settled), 8.5 (end card); the default thirds land mid-assembly and mid-bars.

## Sound
audio.py reads `events.json` (a list of cues with a time `t` and kind `k`) and synthesizes 48 kHz stereo with NumPy,
`DUR` 9.6. Every kind takes `v` (gain, default 0.5). Dry, mechanical, short:
- `pop` (`f`, falls to 0.45 f), `blip` (`f`), `bloop` (`f`, rises 2.4×), `bloopdn` (`f`, falls), `thud` (`f`, low),
  `tick` (`f`, 30 ms), `clack` (`f`, square wave), `chime` (`f`, a bell on f, 1.5 f, 2.01 f), `click` (the switch),
  `on` (thump and a 100 Hz hum that dies over 1.4 s), `roll` (`d`, rumbling noise), `swish` (`d`, paper noise),
  `chord` (C major, 2.2 s): the only music.
- Demo cues (literal times in `window.events`; the bars' from `b.t0`): 13 `tick` for the grid and one per label, a
  `clack` per headline letter (`f` rising 30 a letter); `roll` 0.8 (`d` 0.9); `pop`, `bloop`, `thud` as shapes land;
  `bloopdn` 2.3 (morph), `pop` per joint, `tick` per arm, `clack` as parts lock, `blip` as the bulb seats; `click`
  3.7; `on` 3.8 and a `thud` per strip; `chime` 4.2 (beam); `swish` and a `tick` per slice; `bloop` and `pop` for pool
  and satellites; per bar a `swish` (`d` 0.35), a `clack` and a `tick` every second character; a `clack` per digit;
  `chord` 7.35, after the last settle.
- Nothing is written at fixed times and no cue is looked up by name: audio.py plays any subset. Re-time it by moving
  cues and `DUR`; the master fades the last 0.5 s (`fo`) and limits with tanh (ceiling 0.8). Send `chord` as the end
  card settles, at least 1.1 s before the end.
- What breaks it (tested): any kind missing from `gen()` raises ValueError (it is not skipped); `pop`, `tick` and the
  other `f` kinds without `f` raise TypeError, the sweeps with `f` 0 ZeroDivisionError; `roll` or `swish` without `d`
  raise KeyError, with `d` ≤ 0 ValueError. Pans are random within ±0.3, so no field can make a NaN; a huge `v` only
  saturates. Cues before 0 or past `DUR` drop silently. Any `DUR` works (sizes go through `int()`).

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Maths and easing | `anim.html` → `span`, `anim.html` → `Ease` | `span(t, t0, t1)` 0→1; `mix`, `box`, `mid`, `along`, `turn`; `Ease.out`, `in`, `both`, `settle` | as is |
| Palette | `anim.html` → `C` | `C.paper`, `red`, `blue`, `yellow`, `black`, `unlit`; `blend(a, b, u)` | as is |
| Shape kit | `anim.html` → `twoTone` | `disc(x, y, r, colour)`, `poly(pts, colour)`, `rod(p, q, width, colour)`, `triangle(cx, cy, side, angle)`, `twoTone(cx, cy, side, angle, face, half)` | as is |
| Type | `anim.html` → `riseText` | `setType(weight, size, { stretch, track })`; `riseText(t, text, x, baseline, size, { weight, stretch, track, start, stagger, colour })` returns its width; `caption(text, x, y, align, colour, alpha)` | as is; new strings in `FONT_CHECKS` |
| Grid | `anim.html` → `drawGrid` | `MARGIN`, `NCOL`, `GAP`, `COLW`, `col(i)`, `GRID_V`, `GRID_H`; `drawGrid(t, colour)` | as is; values per format |
| Grain | `anim.html` → `makeGrain` | `grain = makeGrain()` in `window.ready`, drawn at 0.55 in `render()` | as is |
| Block inversion | `anim.html` → `blockClip` | `blockClip(t)` builds the strip clip from `LIGHT_ON`; `render()` fills it black, redraws grid, floor and subject with paper line work | adapt strips per format |
| Type bars | `anim.html` → `BARS`, `drawBars()` | rows `{ y, h, w, col, txt, tc, px, t0 }`; cues follow `b.t0` | adapt copy |
| The lamp | `drawLamp()`, `drawBase()`, `drawArms()`, `drawBulb()`, `drawShade()`, `SQUARE`, `CIRCLE`, `TRI`, `BASE`, `PIVOT`, `ELBOW`, `HEAD`, `SWITCH`, `BULB` | `drawLamp(t, inverted)` | replace |
| Beam and composition | `drawBeam()`, `SLICE_COLOURS`, `SLICE_DROP`, `SATELLITES`, `MOUTH_L`, `BEAM_L`, `toFloor` | `SATELLITES` rows `{ x, y, side, angle, face, half, t0 }` | adapt: slicing a form is reusable |
| Labels, timeline, cues | `drawLabels()`, `LABELS`, `render()`, `window.events` | | replace |
| Sounds | `audio.py` → `gen` | cue kinds in Sound | as is; `DUR` |

## Adapting
- **Style vs demo plot:** the movement's grammar, and where the demo builds it: primary colours (`C`: one flat red,
  blue or yellow per shape, black second halves, paper ground); elementary geometry (`disc()`, the square,
  `twoTone()`, `rod()`, with the subject assembled from them on screen); the grid (`drawGrid()` visible, all type
  flush to `MARGIN`, block strips on double columns); sans-serif type (Archivo capitals rising in `riseText()`);
  asymmetric balance (the type mass left against object, block and year right; stepped bar lengths). With the grain,
  the block inversion, type bars, exponential easing and the dry clicks and chord, that is the style. The bars are
  style; their moment is plot (the finish in 16:9, the build in tall formats). Plot: the lamp, light, labels,
  exhibition copy, 1926. A transformation in a new story: the shapes assembling into the subject, the block inversion
  (on and off, before and after, day and night), or a form cut into coloured slices (a whole into parts).
- **New subject:** keep the opening, the kit and the poster layout; rewrite the subject's drawers, `BARS`, the copy
  and `window.events`. Traps: times are literals in each drawer's `span()` windows and again in `window.events`
  (`LIGHT_ON` drives `drawBulb()`, `blockClip()` and the ring, not the `on` cue); subject coordinates are absolute
  (`MOUTH_L`, `BEAM_L` and `SOURCE` follow `HEAD`); paper-side drawings under the block vanish unless redrawn in it;
  the demo's bulb, drawn after `drawBeam()`, hangs below the shade into the beam and reads as a yellow bump on the
  paper slice in the split: start a reused beam below its light source, or draw the source before the beam.
- **Length:** past 9.6 s add beats to the same poster (a second object in free cells, another inversion, more bars),
  1.2–2 s each; a frozen poster tires after about 3 s. In audio.py change only `DUR` and the cue times.
- **Shorter:** down to about 7 s shorten holds (the 8 s plan: the 1.97 s final hold, the beam's 0.38 s before the
  split) and, only then, speed the finish (copy barely matters: 0.016 s a character). Letters, bars and block strips
  survived about 1.5× (4 s plan); keep a 0.8 s final hold and a fade of 0.3 s or more. From 6 s down cut whole beats,
  as far as needed, in this order: the split with pool and satellites, the year and caption (the 6 s plan stops here),
  then the labels with their 0.35 s pause and the beam (the 4 s plan); move the bars into the build (they cost no time
  there). Keep the grid, headline, three shapes, assembly and inversion. The signature is complete when the three
  shapes are down: 1.95 s, 1.7 s after the 0.25 s fade-in (4 s plan: 1.31 s, 1.15 s after its 0.17 s fade-in). A
  finish of bars, year and caption costs 1.23 s to settle, then the 0.8 s hold. The plans map film time to demo time
  (no ambient motion, so the whole frame); holds measured as in Film grammar:
```js
const KNOTS = [[0, 0], [4.62, 4.62], [4.77, 5.0], [6.62, 7.233], [7.6, 9.2], [8.0, 9.6]];   // 8 s: [film s, demo s]
// 6 s: [[0, 0], [4.62, 4.62], [5.6, 9.2], [6.0, 9.6]]
// 4 s: [[0, 0], [1.55, 2.3], [2.35, 3.5], [2.38, 3.75], [2.78, 4.34], [3.7, 9.2], [4.0, 9.6]]
function lerpK(x, a, b) { const K = KNOTS; if (x <= K[0][a]) return K[0][b];
  for (let i = 1; i < K.length; i++) if (x <= K[i][a]) return K[i - 1][b] + (x - K[i - 1][a]) / (K[i][a] - K[i - 1][a]) * (K[i][b] - K[i - 1][b]);
  return K[K.length - 1][b]; }
const toDemo = t => lerpK(t, 0, 1), fromDemo = t => lerpK(t, 1, 0);
// window.draw: render(toDemo(t)). Cues: t -> fromDemo(t); d -> fromDemo(t + d) - fromDemo(t); drop a dropped beat's cues.
```
  - 8 s (all kept; 1.21× from demo 5.0 to 7.233): settled 6.633, fade 7.6–8.0, 0.97 s held; `chord` maps to 6.68.
  - 6 s: `BARS` t0 1.5, 1.65, 1.8; in `drawBeam()` split 0, no pool, pip or `SATELLITES`; no year or caption; drop the
    cues from demo 5.0 to 5.8 and the digit `clack`s; move `chord` to film 4.4 s (drop the demo's cue before mapping,
    add it after). Settled 4.433, fade 5.6–6.0, 1.17 s held.
  - 4 s (about 1.5× throughout; at demo speed the kept beats need 4.84 s, and 4.3 s even without the inversion):
    `BARS` t0 1.5, 1.65, 1.8 with their cues, as in the 6 s plan; no `drawLabels()` or `drawBeam()` call, no year or
    caption; drop the label `tick`s (`f` 2600), `chime`, the split and digit cues; move `chord` to film 2.85 s (drop
    the demo's cue before mapping, add it after). Settled 2.8, fade 3.7–4.0, 0.9 s held; it ends on the inverted lamp,
    bulb lit, beside the bars. Largest band from 2.0 s: 15.8 % (16:9), 16.3 % (9:16), 8.4 % (1:1); 23 % and 29 %
    (9:16, 1:1) for 0.5 s before the lamp rises. Map the bars' window (demo 1.5–2.3) at one even rate: a knot inside
    it makes them jump.
  - Rendered with events.mjs, audio.py (`DUR` 8, 6, 4), check_audio.py: peaks 0.537, 0.537, 0.527 (4 s in all
    formats).
- **Other formats:** values in Composition. Type, grid and block recompose by stacking; the subject keeps its size in
  9:16 and is scaled to 0.8 in 1:1, its labels drawn at full size in screen space.

## Boundaries
- **Distinct from:** `de-stijl` (only horizontals and verticals: black bars dividing primary planes, no circles,
  triangles or objects); `constructivism` (red, black and cream on −27° diagonals, wedges, halftone, condensed
  shouting type); `swiss-style` (also a 12-column grid build, a giant number and circles, but objective typography in
  Inter, red and black, no object built; what is Bauhaus here is the three primaries, elementary shapes assembling an
  object, and extended capitals); `memphis` (1980s pastels and neons, terrazzo, squiggles, bouncing).
- **Poor fit:** emotional character stories (`storytime`, `picture-book`); many numbers (`data-visualization`,
  `isotype`); long quotes (`kinetic-typography`); soft, organic subjects such as landscapes (`watercolor-memory`);
  interface walkthroughs (`product-ui`).
- **Do not:** reproduce a known Bauhaus work: Schlemmer's profile-head signet or Triadic Ballet figures, the lettering
  on the Dessau building, Bayer's or Schmidt's exhibition posters, Kandinsky's form-and-colour questionnaire, Brandt's
  tea infuser or Kandem lamp, the Wagenfeld lamp, Breuer's Wassily chair. Build each film's own object from the kit,
  as the demo invents its lamp, and invent the event, names and dates; do not write "Bauhaus" on screen or imply the
  school or its archives made or endorse the film. No outlines, gradients, fourth hue, diagonal type or centred
  symmetry: they turn it into flat illustration or a neighbouring movement.

## Technical notes
- No render.json and no vendor folder: Canvas 2D, no GPU; anim.html, fonts.css, two woff2 files. 288 frames render in
  about 7 s on one page. Deterministic: `makeGrain()` uses its own xorshift (seed 0x2f6b1d3), audio.py's `rs` seed 3.
- The fades paint paper over the whole frame after the grain; they do not set `globalAlpha` on drawers. The kicker in
  `render()`, `caption()` and `drawBulb()` (its black quarter) assign `globalAlpha` and reset it to 1, so a scene
  faded with `globalAlpha` would leave them opaque: save and restore instead (const a0 = ctx.globalAlpha;
  ctx.globalAlpha = a0 * a; … ctx.globalAlpha = a0).
- Sizes outside `W`/`H`: only the canvas tag; but the layout is literal: kicker and rule y, headline baselines,
  `FLOOR`, every subject coordinate, `BARS` y, the year and caption positions, `GRID_H`, `PANEL_X` and `blockClip()`'s
  columns, the circle's start `W` + 220 and the square's −300. `makeGrain()` follows `W` and `H`.

# Blueprint (`blueprint`)

An engineering drawing that drafts itself: near-white ink on a mottled cyanotype-blue sheet with a faint grid,
built from orthographic views, centre lines, section hatching, dimensions, callouts and a title block. It draws
on the drafting-table and blueprint-print tradition and its conventions. The mood is calm and exact: a pen that
never hesitates and a sheet that fills up until it is complete.

**Reference film:** an engineering sheet for an invented mechanical pencil, "Model MP-7": front view, end view,
section A–A, exploded view with balloons, parts list and title block draw in one after another · `styles/blueprint/`

## Signature
- A mottled mid-blue sheet with a fine 24 px drafting grid fills the frame from the first frame (after a 0.35 s fade-in from navy).
- One ink only: near-white lines with a soft glow halo, no filled areas and no second colour.
- Lines draw themselves along their length; a dash-dot centre line comes first, then heavy outlines led by a bright dot at the drawing tip.
- Drafting conventions appear by 3 s: cross-hatching, extension lines, dimension lines with slim filled arrowheads, italic condensed figures ("145").
- The camera starts close (1.58×, chosen so the pencil, without its dimensions, fills about 85% of the frame width) on a single view; the full sheet with its frame is revealed later by a pull-back.

## Palette
| Role | Colour | In code |
|---|---|---|
| Sheet, centre of the wash | `#1f5aa6` | `sheetTex` |
| Sheet, edge of the wash and base fill | `#123b75` | `sheetTex`, `composeFrame()` |
| Light exposure blotches | `rgba(90,150,230,0.07)` | `sheetTex` |
| Dark exposure blotches | `rgba(5,20,60,0.08)` | `sheetTex` |
| Paper fibres | `rgba(200,225,255,0.05)` | `sheetTex` |
| Grid, minor lines (24 px) | `rgba(200,225,255,0.055)` | `paintGrid()` |
| Grid, major lines (every 120 px) | `rgba(200,225,255,0.13)` | `paintGrid()` |
| Ink: every line, letter, arrowhead and dot | `232,241,255` | `LN`, `ink()` |
| Vignette at the edges | `rgba(0,10,40,0.35)` | `composeFrame()` |
| Fade in and out | `rgba(9,33,70,${dark})` | `composeFrame()` |

- Hierarchy comes from line weight and alpha, never from hue: outlines at 0.9–0.92, centre lines 0.6, projection lines 0.4, hatching 0.45–0.75, secondary labels 0.7.
- The glow is additive light, so the ink reads as exposed paper rather than paint; never fill a part, view or region with ink; the only solid marks are arrowheads, dots and the scriber tip.

## Typography and copy
- `FONT_C` is Barlow Condensed (`fonts/BarlowCondensed-*.woff2`: 500, 500 italic, 600) and `FONT_M` is IBM Plex Mono (`fonts/IBMPlexMono-*.woff2`: 400, 500), loaded with `loadFont()` from the `FACES` list; there is no fonts.css.

| Role | Font | Size (px) | Weight / style | Letter-spacing | Alpha |
|---|---|---|---|---|---|
| View title (FRONT VIEW) | `FONT_C` | 34 | 600 upright | 3 | 0.95 |
| End-view title with scale | `FONT_C` | 28 | 600 upright | 2.5 | 0.95 |
| Dimension figure | `FONT_C` | 24–30 | 500 italic | 1 | 0.95 |
| Cutting-plane letter | `FONT_C` | 34 | 600 italic (see below) | 1 | 0.95 |
| Title-block title | `FONT_C` | 34 | 600 upright | 2 | 0.95 |
| Title-block value | `FONT_C` | 27 | 500 upright | 1 | 0.95 |
| NOTES heading | `FONT_C` | 22 | 600 upright | 2 | 0.95 |
| Balloon number | `FONT_C` | 26 | 600 upright | 0 | 0.97 |
| Callout | `FONT_M` | 23 | 400 | 0.5 | 0.95 |
| Parts-list row | `FONT_M` | 22 | 400, item number 500 | 1 | 0.95 |
| Note line | `FONT_M` | 20 | 400 | 1 | 0.85 |
| Field name (parts list, title block) | `FONT_M` | 14–15 | 500 | 1.5 | 0.7 |
| Zone mark | `FONT_M` | 17 | 500 | 1 | 0.95 |

- `txt()` is italic unless you pass `it: false`. The cutting-plane letters ask for 600 italic; only 500 italic ships, so Chrome draws the 500 italic with synthetic bold (keep it to match the reference).
- View titles are centred under their view with a 1.6 px rule 13 px below the baseline, running 5–20 px past each end of the title (about 19 px on FRONT VIEW, 10 on SECTION A–A, 6 on EXPLODED VIEW). The end view carries its scale in its title ("END VIEW  2 : 1") and has no rule. Callouts sit left-aligned on their shelf.
- Text types on character by character at 0.028 s per character (`dur` sets the whole string's typing time instead: zone marks 0.05 s, parts-list cells 0.22 s, notes 0.3 s, the title-block title 0.5 s); centred text is laid out from its full width so it does not shift while typing. Text never leaves before the final fade.
- Coverage is Latin and Latin Extended (`UNICODE_RANGES` in `common.js`): Ø, ·, –, ×, ±, °, µ, ², ³ and ½ work; π, →, ⌀, ≤, ≥ and ≈ are missing from every face (write MAX, MIN, APPROX, and draw arrows with `arrowHead()`), and Greek, Cyrillic or CJK need an added font.
- Copy is deadpan drafting language in capitals: part names, materials, values with units ("SPRING Ø 5.8", "LEAD Ø 0.5 mm, HB"); units keep their SI case (mm, kg, N, µm) and everything else is capitals; a middle dot separates terms. One to four words per label.
- Maximum characters: view title about 20 at 34 px; callout at 23 px takes 14.3 px per character and must end before the next callout's knee, which leaves about 21 characters in the demo's first gap and 16 in its last; parts-list cell about 10 at 22 px; note line about 30 at 20 px; title-block title about 30 at 34 px across its 540 px. Longer copy becomes more numbered NOTES lines or another callout, never a paragraph.
- In 9:16 keep the table's sizes: the frame is 1080 px wide, so they are already about 1.8 times larger relative to it than in the demo. Callouts, notes and view titles may grow by up to about 15% (callout 26, view title 38) when the copy still fits. Nothing the viewer must read goes below 20 px; the 14–15 px field names only label values. There is no headline size: the subject's name goes in the title block.

## Texture and finish
- `sheetTex` is painted once at load with `rng(4)`: a radial wash, 120 soft exposure blotches, per-pixel grain of ±5 (slightly stronger in blue) and 700 faint fibre strokes. It is static, so nothing flickers, and drawn 160 px (sides) and 90 px (top and bottom) oversize under the camera, so zooms around the sheet centre show no edge down to about 0.86×. An off-centre close-up sees further: at scale s centred on sheet point (cx, cy) the camera sees x from cx − (W / 2) / s to cx + (W / 2) / s and y from cy − (H / 2) / s to cy + (H / 2) / s, and the texture and grid must cover that at every camera keyframe (9:16 values in Technical notes).
- `paintGrid()` draws the grid every frame under the camera transform, 240 px past the frame on every side, so it scales with zooms.
- Every ink mark is drawn into the offscreen `inkCv` through `inkCtx`; `composeFrame()` copies it to the quarter-size `glowCv` with a 2 px blur, adds that with `lighter` at alpha 0.55, then draws the sharp ink on top. Anything drawn straight on `ctx` misses the glow.
- A screen-space radial vignette darkens the corners; a navy overlay fades in over 0–0.35 s and out at the end.

## Shapes, line and figures
- Objects are orthographic engineering drawings: no perspective, no shading, no colour fills. Each part is a polygon in millimetres in the `SH` table (x along the axis, y radial), closed and symmetric about the centre line except the one-sided clip, placed on the sheet with `mapper(ox, oy, k)` at k px per mm (7 for main views, 14 for the 2 : 1 end view, 4.4 for the exploded view). Scales are relative: the title block's SCALE is the main views' scale (the demo calls 7 px/mm 1 : 1, so its 14 px/mm end view is 2 : 1), and every other view is labelled with its k ÷ the main k times that. Pick a standard main ratio (1 : 1, 1 : 2, 2 : 1, 1 : 5), never one that contradicts the views and never "SCHEMATIC".
- Line weights follow drafting practice: visible outlines 3 px, inner parts 2.2, secondary edges and seams 1.4, springs 1.8, dimension, extension and leader lines 1.1–1.2, centre lines 1.1 at alpha 0.6 with `CEN` dash-dot, hidden lines with `HID` dashes, projection lines 1 px dotted at alpha 0.4, the lead 3.2. Caps and joins are round, except butt caps on dashed lines.
- Lines are ruler-straight. Curves are true arcs (`P().A()`) or smooth spline curves (`P().S()`); `jitter()` in `common.js` belongs to the sketchy sibling styles and is never used here.
- Surfaces read through hatching: a cut surface gets 45° single hatching (gap 7, alpha 0.7), alternating direction on neighbouring parts; knurl or rubber gets cross-hatching (gap 6–8, alpha 0.45–0.5).
- In a section, stroke a closed outline only where the bore really steps or ends. Where the bore runs on into the next part, or an uncut rod, spring or lead passes in front, stroke an open polyline and keep the closed outer and inner polygons only for the hatch clip. Rods, shafts, springs, balls and pins are never hatched in a lengthwise section.
- Marks: slim filled arrowheads (20 × 11 px triangle), callout dots of radius 4.5, balloons of radius `BR` 21 with the item number inside and a leader dropping to a dot on the part.
- The cutting-plane symbol: a `CEN` line at alpha 0.7 through the view, heavy 4.5 px ends 26 px long, 1.6 px arms 46 px long with arrowheads pointing in the viewing direction, and the section letter beyond each arrow. A–A lives on the end view: if you drop the end view, keep a small one (about 1 s, beside the section) to carry the plane, or omit the plane and title the section SECTION with no letter, which is allowed when the plane obviously runs along the axis. Never write SECTION A–A without an A–A plane, and never lay the plane along the front view's centre line. Mark a detail with a thin circle and a letter not already used by a cutting plane (B when the section is A–A), and title it with that letter and its scale ("DETAIL B  3 : 1", scale = its k ÷ the main k) with no rule, like the end view.
- To draw a new object: outline it in real units about a centre line, give it a front view plus an end or top view, a section with hatching to show the inside, one or two dimensions per view and callouts for the parts that matter. There are no people or faces; a brief about people needs another style.

## Composition and camera
- The sheet is the 1920 × 1080 canvas at camera scale 1: a thin outer frame at 40 px and a 2.6 px inner frame at 62 px, eight zone columns numbered 1–8 top and bottom, rows A–D on both sides.
- The layout follows drafting convention: front view top-left on its axis, end view at 2:1 to its right on the same axis (`EY` equals `FOY`), section A–A directly below the front view sharing its x positions with projection lines between them, exploded view along the lower band, parts list top-right with notes below it, title block in the bottom-right corner against the inner frame.
- Every view has its title centred below it; front, section and exploded titles get a rule, the end view puts its scale in the title instead. Views keep generous empty grid around them; about half the sheet stays empty, so the eye always finds the newest drawing.
- `viewAt(t)` is a 2D camera: it returns the scale and the sheet point placed at screen centre. It opens at 1.58× on the front view, pulls back to the whole sheet (2.95–4.25 s), pushes in 22% on the section (4.3–5.2 s) and eases back out (6.0–6.8 s), with a constant slow push of about 2% so the frame is never frozen. Sheet, grid and ink share the transform; glow, vignette and fade are screen-space.
- One plane only: no parallax and no depth layers. The camera, not the layout, decides the focus.

## Motion
- Lines draw along their arc length with `eio2` (quadratic in-out) unless `ease` overrides it. Long outlines and frames take 0.5–1 s and short edges 0.1–0.2 s; strokes overlap, so several pens work at once and the drawing never pauses.
- Solid strokes wider than 2 px carry a bright dot of radius 3.2 at the moving tip (`drawLine()`): the scriber.
- Small marks pop with overshoot: arrowheads (0.18 s) and dots (0.12 s) with `eback(u, 3)`, balloons (0.32 s) with `eback(u, 2.6)` scaled about their own centre. Nothing else overshoots.
- Hatching is revealed by a slanted edge sweeping left to right (`drawHatch()`); text types on (above).
- Exploded parts slide along the single axis with `eio` over 0.8 s, staggered 0.05 s per step from the middle outward; the spring relaxes from 24 to 30 mm with `eout`.
- Camera moves use `eio` over 0.8–1.3 s. Frames are smooth 30 fps with no stepping.
- Never: wobble, erase or undraw, fade a single element in or out, spin or tumble parts for decoration (a flap or lever may turn about its drawn pivot when that is the mechanism), or bounce a whole view. The sheet only accumulates.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.35 | Fade in from navy on the empty sheet and grid, camera at 1.58× on the front-view area | `composeFrame()` (`dark`), `viewAt()` |
| 0.3–1.0 | Dash-dot centre line of the front view | `line()` with `CEN` |
| 0.75–2.35 | Front-view outlines tip to cap (cone, grip, barrel, clip, cap), seam lines, then the lead | `SH`, `polyPath()`, `fm` |
| 2.1–2.6 | Knurl cross-hatching on the grip | `hatch()` with `cross` |
| 2.35–3.4 | Dimensions 145, 32 and Ø 8.4; FRONT VIEW title and rule (2.8–3.2) | `dimension()`, `txt()` |
| 2.95–4.25 | Camera pulls back to the whole sheet; double frame, zone numbers and letters draw (3.1–4.2) | `viewAt()` |
| 3.55–5.1 | End view at 2:1 with cutting plane A–A and its title; projection lines down from the front view (3.9–4.6) | `EX`, `EY`, `EK` |
| 4.3–6.6 | Camera pushes in (4.3–5.2); section outlines, alternating hatching, clutch, spring, eraser, lead; SECTION A–A title and rule (5.6–6.0); four callouts (5.75–6.6) | `shells`, `springPts()`, `callout()` |
| 6.0–6.8 | Camera eases back out to the sheet | `viewAt()` |
| 6.05–6.55 | Exploded view draws assembled on its own axis | `drawExploded()`, `XD0`, `XD1` |
| 6.6–7.6 | Parts slide apart; parts-list grid draws (6.6–7.3) | `XS0`, `PARTS`, `PL` |
| 7.2–7.6 | EXPLODED VIEW title and rule | `txt()` |
| 7.35–8.3 | Balloons 1–8 pop and drop leaders; matching parts-list rows type in; NOTES | `drawBalloons()`, `BY`, `PC` |
| 7.45–8.6 | Title block frame, title and six cells fill in; closing chord at 8.55 | `TBLK`, `cells` |
| 8.6–9.45 | Hold on the complete sheet | `viewAt()` |
| 9.45–10 | Fade to navy | `composeFrame()` (`dark`) |

- In the 10 s demo the opening view takes about 3 s, alone in the close-up; later views are beats of 1.5–2 s. Each runs in a fixed order: centre line, heavy outline, secondary edges, hatching, dimensions or callouts, with the title and its rule near the end of the beat. The next beat starts 0.3–0.5 s before the last finishes, so the pen never stops.
- The camera carries the story: close on the first view, pull back to reveal the sheet, push in for the inside, back out for the summary.
- Reusable patterns: the view beat, the section reveal, the exploded separation with balloons and parts list, and the title block as sign-off. One-off demo content: the pencil geometry and every coordinate.
- The ending is the complete sheet, held at least 0.8 s before the fade; nothing is ever removed.

## Sound
audio.py synthesizes everything from filtered noise and sines, 48 kHz stereo, with `DUR` 10.0. Cue kinds:
- `scribe` (`d`): drafting-pen scratch for heavy strokes; `line()` emits it when the line width is 2 or more and the stroke lasts at least 0.15 s.
- `pen` (`d`): lighter fine-liner scratch for thinner strokes, under the same 0.15 s rule.
- `hatch` (`d`): a rasp of short scratches, about 22 per second of `d`; `hatch()` emits it.
- `tick`: a 30 ms click from `arrowHead()`, and from `dot()` when the radius is above 3.
- `key`: a soft stencil key; `txt()` emits one for every second non-space character.
- `whoosh` (`d`): a filtered-noise swell, pushed by hand once, for the pull-back that reveals the whole sheet (2.95 s, `d` 1.3); the push-in and ease-out are silent.
- `slide` (`d`, `v` 0–1): parts sliding apart with a short metal ring at the end; `v` scales the gain. One per exploded part.
- `pop` (`v`): a balloon tap; `v` is the item index 0–7, which picks a note of a pentatonic run above G5 and pans left to right. Keep `v` within 0–7: the note wraps after 7, and above 10 the pan gain takes the square root of a negative number and writes NaN. With more than eight balloons, spread the item index over 0–7 (round(i × 7 ÷ (count − 1))) instead of passing i.
- `chord`: a 1.6 s D major chord over a low D, pushed by hand at 8.55 s when the title block completes.

The bed is room tone, which follows `DUR` by itself, and a soft D pad (MIDI 38, 45, 54, 57) written at fixed
times: `tone(nt(m), 9.7, 1.8, 1.4)` placed at 0.2 s, with its shimmer sized by `int(9.7 * SR)`; change both 9.7 values together, to `DUR` minus 0.3, or NumPy raises a shape error. In a film under about 6 s also shorten the 1.8 s attack and 1.4 s release (about 0.6 and 0.8 s for 4 s). The 0.25 s
fade-in, 0.7 s fade-out and soft clip follow the buffer length. audio.py looks up no cue by name, so any subset
of cues runs. A new scene gets its drafting sounds for free through `line()`, `txt()`, `arrowHead()`, `dot()`
and `hatch()`; push a `whoosh` only when a move reveals a whole sheet, and one `chord` on the final completion beat yourself. `slide` (one per part) and `pop` (one per balloon) are pushed in the `PARTS` and balloon setup loops, and `whoosh` and `chord` by the `evs.push(…)` line after the title block; keep those pushes when you rebuild the exploded view, and push any hand cue the same way: `evs.push({ k: 'whoosh', t, d })`.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Cyanotype sheet | `anim.html` → `sheetTex` | painted once at load with `rng(4)` | as is; recentre the wash for 9:16 |
| Drafting grid | `anim.html` → `paintGrid` | `paintGrid(c)` per frame under the camera | as is |
| Glow, vignette, fades | `anim.html` → `composeFrame` | `composeFrame(t)`: sheet and grid, ink into `inkCtx`, blurred `glowCv` added, vignette, fade | as is; call new per-frame drawers on `inkCtx` here, each inside `save()`/`restore()` |
| Camera | `anim.html` → `viewAt` | `viewAt(t)` returns `[s, cx, cy]`: scale and the sheet point at screen centre | adapt: new keyframes per view |
| Timed stroke | `anim.html` → `line` | `line(path, t0, t1, { w, a, dash, ease })`: draws the path over t0–t1; defaults `w` 1.5, `a` 0.9 | as is |
| Typed text | `anim.html` → `txt` | `txt(str, x, y, size, t0, { dur, font, w8, it, align, rot, a, ls })`; italic `FONT_C` by default, pass `it: false` for labels | as is |
| Arrowhead, dot | `anim.html` → `arrowHead` | `arrowHead(x, y, ang, t0)`, `dot(x, y, t0, r)` | as is |
| Hatching | `anim.html` → `hatch` | `hatch(clipFn, t0, t1, { gap, ang, box, a, cross })`: `clipFn(c)` sets the clip; `box` [x0, y0, x1, y1] is required | as is |
| Dimension | `anim.html` → `dimension` | `dimension(vertical, at, base, a, b, t0, label, { size, dx })`: `at` is where the dimension line sits, `base` the part edge, a–b its ends. Extension lines draw over t0 to t0 + 0.25, the dimension line over t0 + 0.2 to t0 + 0.45, arrowheads at t0 + 0.43, the label types from t0 + 0.5; a vertical label sits 12 px left of its line, so put vertical dimensions on the object's left | as is |
| Callout | `anim.html` → `callout` | `callout(px, py, kneeX, shelfY, endX, label, t0)`: dot, kinked leader to a shelf, mono label | as is |
| Geometry helpers | `anim.html` → `polyPath` | `polyPath(pts, close)`, `tracePoly(c, pts)`, `mapper(ox, oy, k)`, `rectMM(x0, x1, r)`, `springPts(x0, len, r, n)` | as is |
| Path builder | `common.js` → `Path` | `P().M(x, y).L(x, y).A(cx, cy, rx, ry, from, to[, steps]).S(pts)`; `line()` calls `done()` | as is |
| Easing | `common.js` → `eio2` | `eio2`, `eio`, `eout`, `eback(k, over)`; `seg(t, start, end)` for progress | as is |
| Exploded view | `anim.html` → `drawExploded` | `drawExploded(c, t)`: parts offset by `sepU()`; outer shells knocked out with `destination-out` to hide inner parts; the axis ends 118 and 1600 are sheet coordinates, and the knockout erases any ink under an outer shell, so keep other marks off the exploded band | adapt: new parts, keep the knockout |
| Balloons | `anim.html` → `drawBalloons` | `drawBalloons(c, t)`; the leader end per part comes from a hard-coded radius chain | adapt |
| Parts list, notes, title block | `anim.html` → `TBLK` | `PL`, `PC`, `TBLK`, `cells`; the dividers 906, 962, 1498 and 1678, `PC`, the NOTES heading and lines (x 1450, y 490 and 526 + 32 per line) and the title baseline 890 are fixed numbers, so move them with `TBLK` and `PL` | adapt: new rows, cells and drawing number |
| The pencil | `anim.html` → `SH` | `SH`, `PARTS`, `R_HEX`, the view origins `FOX`, `FOY`, `EX`, `SOY`, `XY` | replace |
| Drafting sounds | `audio.py` → `scratch` | cue kinds in Sound | as is; re-time the pad |

## Adapting
- **Style vs demo plot:** always the style: the sheet, grid, glow, vignette and fades, one ink, the drafting conventions, a centre line before each outline, the scriber tip, typed capitals (condensed titles and figures, mono labels), a close-up opening that pulls back to a framed sheet, the slow push and the title block as sign-off. Plot a new film replaces: the pencil, its end view and cutting plane, the push-in on the section, the exploded view with balloons and parts list. The transformation can be the pull-back that reveals the sheet, a section that opens the object, parts separating, or a mechanism moving.
- **New subject:** pick something with a shape and an inside: a product, mechanism, building part or device. Keep the sheet, grid, glow, camera logic, action helpers and drafting conventions; replace `SH`, `PARTS`, the views and all copy. Items are static once drawn; anything that moves afterwards needs its own per-frame drawer on `inkCtx`, as `drawExploded()` does. Wrap each drawer in `c.save()` … `c.restore()`: `inkCtx` keeps its state between frames, `drawLine()` leaves its cap, join and dash set and `drawHatch()` sets none of them, so a leak changes later hatching and makes a frame depend on the frames drawn before it. Positions are sheet coordinates under the camera.
- **A working mechanism** fits the style. Draw a moving part only in its drawer, from its first stroke (`drawLine()` with u running 0 to 1 gives the draw-on and the scriber), never also with `line()`, which would leave it behind; then slide it along the axis with `eio` over 0.5–0.8 s, as the exploded parts slide, moving the same part in every view at once (front view and section share x). Dimension only fixed parts, or the stroke itself between its end positions; a dimension on a moving part becomes false. A callout on a moving part needs its dot and leader start to ride with it. Show air or fluid as a 1.6 px line with `arrowHead()` in the same ink, labelled in mono capitals (AIR OUT). With time to spare, two static states, each titled below (STROKE 1 · PULL, STROKE 2 · PUSH), are the traditional drafting alternative.
  - In the drawer, compute each offset from `t` and call `drawLine(c, { path: P()….done(), w, a, ease: eio2 }, u)` (it adds the scriber dot) and `drawHatch(c, { clipFn, box, gap, ang, a, cross }, u)` directly. Never call `line()`, `txt()`, `dot()`, `arrowHead()`, `hatch()`, `dimension()` or `callout()` per frame: they append items and sound cues at load. For a riding callout dot use `drawDot(c, { x, y, r: 4.5 }, 1)`. Push the drawer's `pen` or `scribe` cues and one `slide` cue per stroke by hand; the slide's ring lands at 0.9 × its `d`.
  - A flap or lever turns about its pivot pin with `eio` (translate to the pivot, rotate, translate back) only in a view where its pivot axis points out of the sheet; elsewhere the turn would foreshorten, so leave it static there. In the 4 s plan a stroke fits at about 2.2–2.75 s, overlapping the title block (functional test).
- **Length:** add views or detail push-ins as further 1.5–2 s beats, each framed by its own `viewAt()` move. Past about 20 s, a second sheet works better than a crowded one: fade to navy, change the SHEET value in `cells` ("1 / 2", then "2 / 2"), start close again. Items never end, so give each item the sheet it belongs to (or an end time) and skip finished sheets in `composeFrame()`'s item loop and in `drawExploded()` and `drawBalloons()`, which `composeFrame()` calls on every frame after that loop and which would otherwise keep drawing sheet 1's exploded view and balloons; extend `dark` in `composeFrame()` with the mid-film fade. Long idle holds feel dead; hold only on completion. Re-time the fade (`seg(t, 9.45, 10)` in `composeFrame()`), the slow push (`seg(t, 4.25, 10)` in `viewAt()`), the hand-pushed `whoosh` and `chord`, audio.py's `DUR` and both 9.7 s values of the pad, and build.sh's `DUR`.
- **Shorter (3–6 s):** cut whole beats from the end of the story rather than compressing each. Keep, in order: the close-up on the front view (centre line, outlines, one or two dimensions, its title), starting by 0.15 s and lasting 1.2–1.5 s; the pull-back with frame and zones (0.6–0.8 s), overlapping the end of that beat; one section or detail (about 1 s); the title block as sign-off (title and three cells, about 0.5 s, with the `chord` as it completes); a hold of at least 0.8 s with the slow push still running; a 0.25–0.3 s fade. The kept beats run about twice as fast as the demo's: outlines 0.3–0.45 s, short edges 0.08–0.12 s, the frame 0.6 s, the title-block outline 0.2 s and its title `dur` 0.3 s. Start callouts as soon as their part is outlined, about 0.25 s into the section, or the last label types past the section's end. The title block keeps DRAWING NO, SCALE and SHEET in one row under the title (112 px tall, still in the corner). Re-time the list at the end of Length: the fade, both slow-push `seg()` windows, `whoosh` (`d` = the pull-back's length), `chord`, audio.py's `DUR` and pad, and build.sh's `DUR`.
  - Drop first the exploded view with its balloons and parts list, then the end view (see the cutting plane in Shapes), the push-in on the section and NOTES. Dropping the exploded view means deleting `PARTS` and the `drawExploded()` and `drawBalloons()` calls in `composeFrame()`: `PARTS` is built from `SH` at load and breaks as soon as `SH` changes. Budget `dimension()` at 0.5 s plus typing and `callout()` at 0.4 s plus typing, and shorten the pad's envelope (Sound).
  - A 4 s plan, tested in 9:16 in a functional test: 0–0.3 fade in; 0.15–1.5 front view; 1.2–2.0 pull-back, frame and zones; 1.45–2.5 section and callouts; 2.4–2.9 title block; 2.9–3.7 hold; 3.7–4.0 fade.
- **Other formats:**
  - 9:16 frame and bands (1080 × 1920, rendered): move the frame rather than the title block. review.md keeps key text out of the top ~15%, bottom ~25% and right ~12%, so put the outer frame at x 40–950, y 40–1440 and the inner frame 22 px inside it, zones 4 across and 6 down (216 × 226 px, close to the demo's 224 × 239). The bare sheet and grid continue below and to the right; the title block keeps the inner frame's bottom-right corner. Linework and dimension figures may enter the top band; view titles, callouts, the parts list and the title block may not.
  - 9:16 layout, rendered with the demo's pencil: front view at 5 px/mm on axis y 270; section on y 470 with callout shelves 150 px below it and SECTION A–A below the callouts (y 710), because at this width the leaders cross the usual title spot; at 5 px/mm the callout gaps hold about 15, 12 and 11 characters; end view at (230, 880) at 10 px/mm (2 : 1 of the 5 px/mm views; its fixed pixel offsets, tuned for 14, sit a little loose but nothing collides) beside the parts list (x 500–890 from y 770); exploded view on y 1210 at 2.3 px/mm across x 80–900 with balloons 100 px above; EXPLODED VIEW at x 200, left of the title block (x 388–928, y 1250–1418), with two NOTES lines under it. The end view leaves the front view's axis, which stays correct drafting because it is labelled with its name and scale. Keep balloon centres at least 50 px apart: radius 21 overshoots to about 25 with `eback(u, 2.6)`.
  - 9:16 short cut (rendered with the demo's pencil): with only the front view, one section and the title block, centre the pair above the title block instead of using the full layout's y values, or rows D–E stay empty. Front view on y 470 (open at 1.27× on (507, 470)), section on y 760 with callout shelves at 910 (a mirrored callout at 950), SECTION at 1000, and a title block of title and one cell row at x 388–928, y 1306–1418. Or fill the middle with a 3 : 1 detail, as the functional test did.
  - Mirrored callout: a part near the right end has no room for a label to the right, so copy `callout()` into a mirrored variant whose shelf runs left (endX < kneeX) and whose label types at endX − 10 with `align: 'right'` instead of at endX + 10 (rendered for ERASER, with its shelf 40 px lower than its neighbours' so the leader clears them).
  - 9:16 scale and camera (rendered): dimensions add about 10% to an object's length, so scale the object to about 720 px. Set the opening close-up to about 0.85 × 1080 ÷ the width of everything drawn in the opening view except its dimensions (the object plus any handle travel, hose or callout beside it) at scale 1, then check that no label falls in the right 12% band: 1.27× on (507, 270) for the pencil. Pull back to the canvas centre (540, 960), not the frame's centre, so the frame stays clear of the bands on screen; enlarge the texture and grid for the close-up (Technical notes).
  - Axis: keep it horizontal in every format; a vertical axis means rewriting `mapper()`, the slide and knurl band in `drawExploded()`, and the balloon row.
  - 1:1 (1080 × 1080, budgeted but not rendered): keep the frame at 40 and 62 px; put the front view and the end view on its axis across the top (object about 600 px, opening close-up about 0.85 × 1080 ÷ length, about 1.5×), the section below the front view with the notes to its right under the end view, the exploded view across the full width below, and the parts list bottom-left beside the title block in the bottom-right corner.

## Boundaries
- **Distinct from:** `technical-cutaway` is a shaded 3D model with colour-coded callouts on a light backdrop; blueprint is flat orthographic linework in one ink. `whiteboard` and `chalkboard` wobble by hand and teach in sentences; blueprint is ruler-exact and labels in capitals. `sci-fi-interface` and `vector-arcade` glow on black with HUD readouts or arcade vectors; blueprint is paper with drafting rules. `isometric` builds a 3D miniature world seen from one angled viewpoint; blueprint stays in flat front, end and section views.
- **Poor fit:** people, emotion and narrative (use `pencil-sketch` or `whiteboard`); charts and statistics (`data-visualization`); organic subjects such as anatomy or plants (`scientific-plate`); maths derivations (`3blue1brown`); fast stat-driven explainers (`infographic`).
- **Do not:** put a headline, subtitle or poster title on the sheet (the subject's name and drawing number live in the title block, each view's title sits centred below it); add a second ink colour, filled areas, shading or perspective; hatch anything that is not cut or textured; mix units in dimensions. Drafting-literate viewers notice wrong conventions, so keep centre lines on axes, sections where the cutting plane says, and invented model names and drawing numbers.

## Technical notes
- No render.json: plain canvas 2D, no GPU and no vendored libraries. A 10 s render takes about 15–45 s with 2 workers, depending on the machine and its load.
- `common.js` is the catalog's shared kit (`W`, `H`, easing, `rng`, `mk`, `loadFont`, `Path`); in a project, change `W`/`H` there.
- Deterministic: the only randomness is `rng(4)` at load for the sheet; audio.py uses a seeded NumPy generator. Every item has fixed times, and the exploded view and balloons are functions of `t`.
- Every frame re-traces each started item from its start; cost grows with the item count, which stays fine at a few hundred.
- Sizes hard-coded outside `W`/`H`: the canvas attributes; the wash gradient centre (900, 480 → 960, 540, radius 1200); the full-sheet centre (960, 540) in `viewAt()`; the screen-centre offset `960 - cx * s, 540 - cy * s` and the vignette centre in `composeFrame()`; the sheet frame (40, 62, 1858, 1880, 1018, 1040), zone widths `1796 / 8` and `956 / 4` and zone marks at x 51 and 1869, y 58 and 1036; every view origin (`FOX`, `FOY`, `EX`, `EY`, `SOY`, `XY`, `XAX`, `PL`, `TBLK`, `BY`); the exploded axis ends 118 and 1600 in `drawExploded()`; the title-block dividers 906, 962, 1498 and 1678, the title baseline 890, the parts-list columns `PC` and the NOTES block (x 1450, y 490, 526 + 32 per line), which do not follow `TBLK` and `PL`; and the sheet's oversize margins 160 and 90 in `composeFrame()`.
- 9:16 sheet and grid (rendered): the opening close-up at 1.27× on (507, 270) sees up to y ≈ −490, so paint `sheetTex` at (W + 240) × (H + 1040) with the wash centred on it, scale the 120 blotches and 700 fibres by the area ratio (W + 240)(H + 1040) ÷ (1920 × 1080), draw it unstretched at (−120, −520), and run `paintGrid()` from x −240 and y −600 to W + 240 and H + 600. Keep the grid's start on the 24 px lattice; a multiple of 120 such as −600 is safest (−640 shifts every line 8 px and loses the every-fifth lines). Then check the top of the first second's frames.

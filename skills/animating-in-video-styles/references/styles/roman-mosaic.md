# Roman Mosaic (`roman-mosaic`)

A Roman floor mosaic laid on screen: thousands of small cut stones and glass tesserae, set in rows that follow every
contour of a letter or figure and in plain grids across the ground, with black outlines, a white marble field and
running geometric borders. It draws on the pavements of Roman houses and baths (a central emblema, a meander and
guilloche frame, secular motifs such as dolphins and laurel) without copying any. Calm, crafted, ceremonial.

**Reference film:** a welcome floor: on a mortar bed with a red underdrawing, black tesserae drop in and write SALVE,
the ground and a laurel wreath close the medallion, the camera rises as two dolphins are laid and start to swim by
re-tiling, the borders race round the floor and a raking light makes the gold glass glint · `styles/roman-mosaic/`

## Signature
- A close-up (2.45×, turned a little) on a warm grey mortar bed (`mortarPat`) with the whole design drawn on it in
  red-ochre lines (the sinopia, `sinopia`), showing until stones cover it.
- Small tesserae drop in from above the camera, spinning and shrinking onto the bed (0.3 s, `FD`), and settle with a
  small bounce; black ones write the title letter by letter, left to right (0.45–1.95 s).
- Every stone is a slightly irregular flat quad with mortar showing between (the grout), its own tone, a lit edge
  toward the top left and a shadow toward the bottom right: raised, hand-cut stones, never a pixel grid.
- From 1.75 s the cream ground flows outward in rows that hug each letter and the disc edge (andamento, opus
  vermiculatum); from 2.55 s the emblem's frame is laid round it (in the demo: rings and a laurel wreath), while
  the camera, rising since 0.3 s, pulls back toward the whole floor.

## Palette
| Role | Colour | In code |
|---|---|---|
| White marble: field and border grounds (label 0) | `236, 229, 212` | `PAL` |
| Black limestone: outlines, letters, meander, rings (1; demo: waves) | `40, 36, 33` | `PAL` |
| Terracotta: subtitle, ivy stops, filler centres, a guilloche strand, warm bodies (2) | `176, 80, 47` | `PAL` |
| Ochre and gold glass: gold rule, emblem ring, strand cores, highlights (3) | `204, 156, 60` | `PAL` |
| Deep blue glass: dark bands, the other strand (4; demo: dolphin backs) | `33, 64, 108` | `PAL` |
| Mid blue: mid bands, strand core (5; demo: dolphin flanks) | `84, 124, 164` | `PAL` |
| Olive and sage: plant outlines and fills (6, 7; demo: laurel) | `88, 96, 50`; `146, 152, 92` | `PAL` |
| Cream: the disc under the copy (8); pale grey: light bands (9; demo: bellies) | `226, 212, 181`; `178, 186, 190` | `PAL` |
| Mortar bed and grout | `[176 * k, 165 * k, 146 * k, 255]` | `mortarPat` |
| Sinopia underdrawing | `sid.data[p] = 150; sid.data[p + 1] = 62; sid.data[p + 2] = 40` | `sinopia` |
| Stone shadow on the grout; lit edge | `rgba(52,40,28,0.55)`; `rgba(255,250,236,0.32)` | `window.draw`, `THL` |
| Beyond the floor | `#2a241e` | `window.draw` |
| Sweep: glints, star flashes, warm band | `rgba(255,238,196,`, `rgba(255,245,210,0.9)`, `rgba(255,228,176,` | `sw` |
| Fades; vignette | `rgba(14,9,5,`; `rgba(20,10,0,0.5)` | `fade`, `vign` |

- Each stone is one flat colour from `PAL`, varied among 12 tones (`BUCKET`: 0.84–1.14 brightness, cycling cooler,
  neutral, warmer by ±4) and biased by a random tilt toward the light. Never a gradient across a shape: shading is a
  band of another stone parallel to the outline (dark, mid, pale; in the demo a dolphin's back, flank and belly).
- Gold and glass carry the shine (`TSPEC`: gold 1, blues 0.6, white and cream 0.28, the rest 0.2). As the band
  passes about half of all stones brighten one step; gold and glass reach the upper steps; only gold makes the star.

## Typography and copy
- One face, Cinzel 700 (`fonts/Cinzel-700-latin.woff2`), Roman square capitals, never drawn on screen: `drawDesign()`
  paints it into the label image, so every letter is laid in stones like any motif.
- Main line: black (`LAB[1]`), fitted to 530 px wide (`fs = 150 * 530 / m.width`), centred at CY − 38 (the literal
  862); `SALVE_BOX` times the letters across its box in 1.25 s whatever the word, so copy never moves the settle.
  Subtitle: terracotta (`LAB[2]`), 66 px, `letterSpacing` 10 px, at CY + 102 (1002, x + 5 recentres the trailing
  spacing), between two ivy-leaf stops; a gold rule 300 × 8 px at CY + 38 (938).
- Copy is an inscription: a greeting, name or title in one word, and a subtitle of one or two words, in capitals
  (lowercase comes out as Cinzel's small capitals). Glyphs: Latin-1 plus Œ œ; no Ł, Ő, Š, Greek or Cyrillic.
- Limits (measured): keep the fitted size `fs` between 97 px ("WELCOME", 15 px stems, the least that keeps serifs)
  and 167 px (SALVE: cap 120, stems 25 px, 3.5 disc stones of 7 px): usually 5–8 capitals, but the letters decide
  (WWWWW fits at 109 px, IIIII at 274; "VINEYARDS", 88 px, still reads). Above 167 the word grows into the rule
  ("VALE": 148 px cap): write `Math.min(167, …)` into the fit. Subtitle: at most about 430 px ("WELCOME" 429), or
  the stops leave the disc; never under 66 px (10 px stems).

## Texture and finish
- `mortarPat` (512 px value noise, warm grey, faint trowel arcs) is the bed and grout, in world space under the
  stones, so it enlarges in the close-up; `sinopia` traces the label edges in red ochre over it (half resolution,
  0.7 px blur, 0.55 alpha).
- Per stone, in `window.draw`: a shadow quad offset (1.3, 1.6), the quad in its tone (120 `Path2D` buckets), a 1.1 px
  lit stroke on the two edges facing the light (`THL`, inset to 92 %). Over them `stonePat` (speckle, 0.28), a
  soft-light diagonal, `vign`, static grain (`grains`, 0.05), the fades; all built once in `build()`, none refreshed.

## Shapes, line and figures
- A design is a flat label image: `drawDesign(g)` paints shapes in exact `LAB[i]` colours on a `WW` × `WH` canvas
  (anti-aliased pixels take a neighbour's label). `build()` sets stones on the half-integer lines of a distance field
  to every label and zone edge (turned along the contour, `gradA`), grids where a zone asks, cut pieces in the gaps.
- Zones (`ZONES`, `zoneAt()`): margin 25 px grid; meander 20 px grid (each key cell is one stone); guilloche 10 px
  rows; field 14 px, three rows hugging every motif, then a straight grid (opus tessellatum); the emblem's frame
  (demo: rings and laurel) 10 px rows; its disc 7 px, rows everywhere (opus vermiculatum).
- Stones: half-size 0.41 s (rows) or 0.42 s (grids) ± 5 %, each corner jittered 0.07 s; grid stones also turn up to
  ±0.035 rad. The grout is what is left, about 16–20 % of the pitch, wider where rows meet.
- In the demo: dolphins, a parametric body (`dolphinPose()`, `wProf`, `DL` 520) labelled per point (`dolphinLabel()`);
  a laurel of 17 leaf pairs a branch; rosettes of six rings; crosslets of five stones.
- A new motif looks laid in stone when:
  - it is drawn in `LAB` colours only: no alpha, shadow or gradient (unknown colours become a neighbour's label);
  - a black outline at least one stone wide as seen: 16 px of visible black in the field (the dolphin's `OL`), 10 px
    in the 10 px zone (the laurel's lineWidth 20 stroked under its fill). A stroke under the fill shows half its
    lineWidth, so stroke a silhouette at 32 px under the fills (16 px under leaves no row, tested twice); filling first
    and stroking 16 px on top also works (the stand-in amphorae; inner lines such as a wing edge) but covers 8 px of
    every fill, so a part under about 44 px wide (a fin, a handle, a stern post) loses its colour;
  - it is shaded in two or three flat bands parallel to the outline, each at least two stones wide (28 px in the
    field) and at most about six (84 px): beyond three rows from an edge the field lays its grid (`ZONES` K 3), so a
    wider patch gets a grid core (a 180 px sail came out a third grid); fine only on flat things like a sail or wall;
  - no detail is thinner than one stone (an eye is one black stone, radius 7.5 px; fins and handles two);
  - it keeps about three rows (42 px) of ground from its neighbours, so its white halo rows can form;
  - it gets its own laying order (in the demo the dolphins go head to tail), or it is laid with the field.
- People: none in the demo; a face needs ten or more stones across. Prefer animals, vessels, plants and objects.

## Composition and camera
- The floor's layout: concentric bands (margin, a meander band with corner blocks, a guilloche band, the field) and
  a central emblem whose disc holds the copy; figures in the field in mirrored pairs facing it, small fillers on a
  grid; mirror symmetry, the copy is the focus. In the demo (16:9): a 3200 × 1800 floor (`WW`, `WH`), margin 0–50,
  meander 50–230, guilloche 230–400; the medallion at `CX`, `CY` (rings to radius 482, laurel 338–432, disc under
  322); dolphins at x 810 and 2390, y 915 (`dolphinPose()`), waves, corner rosettes, crosslets on a 200 px grid.
- One shot, `camera()`: from 2.45× on (`CX`, 872), turned −0.03 rad, to 0.585× on the centre, `smoother` over
  0.3–6.8 s on the log of the zoom; twist and centre settle earlier. At 0.585 the floor fills the frame inside a
  24 px and 13 px rim of `#2a241e`. Final sizes: title cap 70 px, subtitle cap 27 px. No cuts, pans or shake.
- 9:16 (rendered): transpose the floor. 1800 × 3200 has the frame's exact shape, so the end zoom stays 0.585 and no
  stone or line changes size. The expressions below also give the demo's 16:9 numbers.

```js
// canvas width="1080" height="1920"; W = 1080, H = 1920; WW = 1800, WH = 3200, CX = 900, CY = 1600
const ROS = [[540, 540], [WW - 540, 540], [540, WH - 540], [WW - 540, WH - 540]];   // rosettes; crosslets avoid 160 px round each
const DPOS = [[957, 790], [843, 2470]];                       // dolphinPose() centres: top faces right, bottom faces left (16:9: [810, 915], [2390, 915])
const WAVES = [[640, 980, 1010, 0], [820, 1160, 2690, 1.5]];  // [x0, x1, y, phase], one line under each dolphin
// use them: dolphinPose() [cx, cy] = DPOS[side < 0 ? 0 : 1]; the rosette loop and crosslet test read ROS; waves loop
//   for (const [xa, xb, y, ph] of WAVES)   (16:9 WAVES: [700, 1020, 1150, 0], [620, 900, 1215, 1.5], [2180, 2500, 1150, 0], [2300, 2580, 1215, 1.5])
// zoneAt(): 3150, 1750 → WW - 50, WH - 50; 2970, 1570 → WW - 230, WH - 230; 2800, 1400 → WW - 400, WH - 400
// meander: len = ((side % 2 === 0 ? WW : WH) - 460) / 20, units = Math.floor(len / 8), off = Math.ceil((len - units * 8) / 2);
//   cell(): 1750 → WH - 50, 3150 → WW - 50; corner blocks [50, 50], [WW - 230, 50], [50, WH - 230], [WW - 230, WH - 230]
// guilloche: 2740 → WW - 460, 1340 → WH - 460, 1556 → WH - 244, 2956 → WW - 244, 1400 → WH - 400, 2800 → WW - 400,
//   1028 → WH - 772; centre line 2885 → WW - 315, 1485 → WH - 315
// crosslets: loops gy, gx < 20, skip x > WW - 480 || y > WH - 480; copy: 862 → CY - 38, 938 → CY + 38, 1002 → CY + 102
// build(): subtitle timing (t.x - 1330) → (t.x - (CX - 270)); perim: px / 1.6 → px * WH / WW * 1.11
// grains: both 960, 540 → W / 2, H / 2 (in mk and createImageData)
// camera(): 2.45 → 1.5, 872 → CY - 28   (at 1.5 the title spans x 142–938, clear of review.md's right 12 %)
```
  - Checked at 0.5–9.0 s: title whole and in the safe area at every zoom (final cap 70 px at y 938); dolphins whole
    and clear of other motifs over a swim cycle; borders whole; nothing unpainted; bare bed with sinopia in the top and
    bottom fifths until about 4 s (as in 16:9), then the caption band holds the lower dolphin, rosettes and borders.
  - Stand-in: two 520 px amphorae instead of the dolphins read as part of the floor, with borders, medallion, copy,
    camera and sweep held; subject-dependent are DPOS, WAVES, the crosslets' exclusion box, ROS (a motif wider than
    about 700 px meets them) and the field timing branch (Adapting).
- 1:1 (rendered): canvas 1080 × 1080, `W` = `H` = 1080; `WW` = `WH` = 2000, `CX` = `CY` = 1000; every other 9:16
  expression as is; no figures (the static path in New subject, WAVES empty); `camera()` from 1.5 on CY − 28 to 0.527
  (a 13 px rim). Rosettes in the field corners, crosslets between; final title cap 63 px, subtitle cap 25 px; with the
  ending fix settled from 8.3 s, 0.97 s held. Dolphin-sized figures do not fit (118 px of field beside the medallion);
  small figures in the corners were not tested.

## Motion
- Appear: a stone falls in 0.3 s (`FD`) from 1.6× its size and up to ±0.7 rad (`TROT`), its shadow offset shrinking
  from about 18 px, eased by (1 − u)²; it lands with a 0.14 s squash of 7 % and a 2 % overshoot that ends at zero.
  Stones land in the order of `TA`, so the rain flows along rows.
- Flip: stones never move; a figure moves by changing which stones carry its colours. `dzState()` relabels the
  stones near each moving figure at 6 poses a second (`SWIM_STEP`); a changed stone flips in 0.08 s (squashed to
  30 % along its axis, colour swapped at half, a white flash mid-flip). At 30 fps one frame in five (frame index
  mod 5 = 1) catches the flips mid-way: a still there shows the figure's edge stones squashed and pale, not a defect.
- A loop round a rest pose (in the demo the dolphins' swim: bob ±9 px, surge ±10 px at 0.55 Hz, a 22 px tail wave at
  1.25 Hz) never travels, so it is ambient in the final hold (review.md: an idle bob); its amplitude ramp (`swimAmp`,
  4.4–5.3 s) is an action. A figure re-tiled along a path (a train crossing the field) is an action: it must arrive
  and stop before the hold. Rows are laid round `DREST` only, so away from it a figure sits on the field's grid,
  stair-stepped, and white rows trace its `DREST` outline where it is not (tested: a locomotive laid at its start and
  moved 416 px ended as a grid figure beside a white ghost of itself). Prefer a loop round the rest pose; to travel,
  see New subject.
- Light up: a raking band crosses the floor diagonally (x + 0.55 y): stones brighten in four steps by `TSPEC`
  (Palette), the brightest gold flash a cross-shaped star, a broad warm band follows.
- Never: a stone sliding across the floor, morphing shapes, outlines drawn as lines, gradients inside the design,
  glow beyond the sweep, text in a font over the floor, cuts or shake.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.55 | Fade up on bare bed and sinopia at 2.45× | `camera()`, `mortarPat`, `sinopia` |
| 0.45–1.95 | Title laid letter by letter, left to right, in black stones | `SALVE_BOX`, `TA`, `FD` |
| 0.3–6.8 | Camera rises to 0.585× and untwists | `camera()` |
| 1.2–2.05 | Subtitle, stops and gold rule laid left to right | `TA` (zone 6, labels 2 and 3) |
| 1.75–3.4 | Disc ground flows out from the letters in rows | `TA`, `wrapA` |
| 2.55–4.0 | Rings and laurel, from the tie up both sides to the boss | `TA` (zone 5) |
| 3.3–4.4 | Dolphins laid head to tail | `dolphinLabel()`, `DREST` |
| 3.35–5.45 | Field spreads out from the medallion: halo rows, grid, rosettes, crosslets | `TA` (zone 4) |
| 4.4–end | Dolphins swim by re-tiling (ramp to 5.3 s, then idle) | `swimAmp`, `dzState()`, `SWIM_STEP` |
| 4.6–6.75 | Guilloche, meander (from 5.0), margin (from 5.55) race round to the bottom | `perim` |
| 6.75–8.85 | Raking light sweep, glints and stars on gold and glass | `sw`, `TSPEC` |
| 9.25–9.97 | Fade to dark | `fade` |

- One continuous build, all reusable: inscription in close-up, the emblem closes, the figures are laid as their own
  beat while the camera rises and field and borders follow, the floor is lit, hold, fade. Forced reference (landings,
  camera and sweep at their end, swim kept): the demo settles from 8.833 s, 13 frames (0.43 s) before the 9.25 fade,
  under review.md's 0.8 s. The ending fix: use `seg(t, 6.75, 8.3)` for the sweep and `d` 1.55 on `glint`; settled
  from 8.3 s, 29 frames (0.97 s) held (measured).
- KEYS: 0.5 (first stones), 1.5 (title on the sinopia), 2.5 (rows hugging letters), 2.8 (laurel rising), 3.33
  (emblem closed, figures starting), 6.0 (borders racing), 7.8 (glints), 9.1 (final state; 9.2 is a mid-flip frame).

## Sound
audio.py synthesizes 48 kHz stereo with NumPy (seed 93) from `events.json`, a list of `{k, t, …}`; unknown kinds are
skipped silently.
- `tick` (`v`, stones landing in that 1/60 s bin): up to five stone clicks (`CLICKS`, made by `click()`: a noise snap,
  a ping, a low thud), quieter each when many land, pan ±0.5. `window.events` builds them from every stone's `TA`
  (365 cues, `v` up to 279), so they follow any re-timing by themselves.
- `lyre` marks two milestones: `v` 0, four rising plucks D F A D, when the inscription is laid (demo 2.05); any other
  `v`, five plucks E G B E D, as the emblem closes and the figures start (demo 3.35); Karplus-Strong `pluck()`, 0.16 s
  apart. `whoosh` (`d`): a filtered-noise swell over `d` with the camera (demo 2.6, `d` 4.2).
- `swish`: a 0.9 s water swish for anything in water (demo: one per dolphin bob, 4.5, 6.3, 8.1). `glint` (`d`): 14
  glass bells (`bell()`) over `d`, panned left to right, with the sweep (demo 6.8, `d` 2.1). `chord`: six strummed
  plucks on D, 1.4 s each, the close (demo 8.55).
- Fixed, not cues: the fountain bed (`fount`) over all of `DUR`; a low drone on D fading in from 1.5 s over 3 s
  (`drenv`): re-time it with the build; master fades of 0.3 s (`fi`) and 0.8 s (`fo`), then a tanh soft clip.
- Breaks (tested): `tick` or `lyre` without `v`, `whoosh` or `glint` without `d` raise KeyError; `whoosh` with `d` ≤ 0
  raises ValueError; a one-sound cue before 0 and any cue from `DUR` on are dropped silently (`lyre`, `chord`, `glint`
  keep notes at or after 0). No cue is looked up by name, pans are fixed ranges (no NaN), any `DUR` works. A new film
  emits `tick`, `whoosh`, `lyre` at those milestones, `glint` with the sweep, `chord` at the settle.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Stones and tones | `anim.html` → `PAL` | `PAL[i]` r, g, b; `LAB[i]` its label colour; `BUCKET[l * NV + v]` its tones | as is; add stones to `PAL` (labels stay unique to 23) |
| Floor design | `anim.html` → `drawDesign` | `drawDesign(g)`: flat shapes in `LAB[i]` on `WW` × `WH`: borders, field, medallion, copy | adapt: keep frame and medallion, replace motifs and copy |
| Zones | `anim.html` → `ZONES` | `{ s, K, ox, oy }` size, rows hugging edges (99 all), grid offset; `zoneAt(x, y)` | as is; thresholds per format |
| Laying engine | `anim.html` → `build` | labels, distance field, rows, grids, cut pieces, per-stone look and `TA`, textures | as is; adapt the `TA` branches |
| Stone drawer | `anim.html` → `quad` | `quad(p, n, ox, oy, sc, rot)` adds stone n to a `Path2D` | as is |
| Camera | `anim.html` → `camera` | `camera(t)` gives z, cx, cy, rot; `window.draw({ t, cam })` takes an override | adapt start zoom and times |
| Landing, flips, sweep, finish | `window.draw` | `FD`, 0.14 s landing, flips at `SWIM_STEP`, sweep `sw`, `fade` | as is; re-time sweep and fades |
| Re-tiled creature | `anim.html` → `dolphinPose`, `anim.html` → `dolphinLabel`, `anim.html` → `dzState` | `dolphinPose(side, t, amp)`; `dolphinLabel(x, y, D)` label or −1; `DREST`, `DZ`, `TDZ`, `swimAmp` | adapt: pose and label functions per creature |
| Sounds | `audio.py` → `click`, `audio.py` → `pluck`, `audio.py` → `bell` | kinds in Sound | as is; `DUR`, `drenv` |
| The demo | `drawDesign()` motifs and copy, `DREST`, `window.events` literals | | replace |

## Adapting
- **Style vs demo plot:** the style is the bed and sinopia, falling stones, centre-outward rows, andamento round every
  contour, tessellatum grids, outlines with white halo rows, the stones' palette, a Cinzel inscription, meander and
  guilloche racing round, the rising camera, the raking light, clicks, lyre, fountain. Plot: the copy, dolphins,
  laurel, waves. Transformations: the floor laying itself, a re-tiling (a figure moving, one emblem turning into
  another), light arriving.
- **New subject:** keep the bands and the emblem in `drawDesign()`, put the user's words in the disc and their
  subject's motifs in the field by the rules in Shapes (a bakery: loaves and a wheat sheaf; a train: a locomotive in
  profile; an app: its icon). A logo is redrawn as flat `LAB` shapes, since an image drawn as is matches no label and
  becomes field; repeat a logo upright and unmirrored, add each brand colour as one flat `PAL` stone (tested: a teal
  icon laid in rows with its halo), and tell the user that a logo needing its exact drawing cannot appear, since
  nothing is drawn over the floor. A static motif (the stand-in): `DREST` empty, the two `s < 2` loops in `build()` →
  `DREST.length`, no `swish`, and a timing branch before the field's (stand-in: stones in its box with a label other
  than 0 get du = 1 − (y − box top) / box height, so `3.3 + du * 0.9` lays them foot to lip). A moving figure needs a
  pose and a label function like `dolphinPose()` and `dolphinLabel()` and is not drawn in `drawDesign()`: build()
  writes its rest pose (`DREST`) into the labels after copying `LABEL0`, which must keep the bare ground the motion
  uncovers (drawn there too, the rest pose stays visible under the moving one). Re-tiling only touches field stones
  within its rest box plus 100 px (`TDZ`). A figure that travels: make `DREST` the pose it stops in, build `TDZ` and
  the crosslets' exclusion from its whole path, run `dzState()` at every t (drop the `t >= 4.4` gate in `window.draw`)
  and fill falling and landing stones with their `cur` label where `TDZ[n]` ≥ 0, so it lands at its start and holds
  in its own rows (tested in 9:16: 416 px in 2.2 s, settled 8.3 s, 0.97 s held). It still crosses grid and its stop
  pose's white rows while moving, and the faster it goes the more of it flashes on mid-flip frames (85 % at 60 px a
  step): start soon after it is laid and keep the trip short. Traps: crosslets inside a motif (exclude its box as the
  crosslet loop excludes `DREST`'s), the copy's y literals, colours outside `LAB`.
- **Length:** the build is one beat; slowing it (K above 1) was not rendered and would thin the stone rain. Past 10 s
  add a beat once the floor is laid. Tested, 14 s with a second light pass: `sw = t < 9.2 ? seg(t, 6.75, 8.3) :
  seg(t, 10.0, 11.55)`, fade from 13.25, a second `glint` at 10.05 (`d` 1.55), `chord` 11.8, `swish` also at 9.9,
  11.7 and 13.5: settled from 11.53 s, 1.7 s held. A second re-tiling or a push is untested. Keep idle loops on film
  time, and any sound tied to them on the same beat (the demo's `swish`, one per bob, every 1.8 s); re-time cues,
  `drenv` and both `DUR`s (audio.py's sizes the buffer; anim.html's drops `tick` cues at or after it); the `chord`
  rings 1.65 s. Cost: about 2.6 s a frame once the whole floor shows.
- **Shorter:** re-time the actions with one factor; leave the stone's own fall and the swim alone. Both plans
  rendered, cues and audio.py run (check_audio passes), holds measured against the forced reference, swim kept:

```js
const K = 0.6;   // action-time scale, both plans (the whole-floor 4 s variant below uses 0.41 for everything)
// build() step 4: TA[n] = ta * K;   window.draw: camera(t / K);   tick cues follow TA by themselves
// swim: 4.4 and 5.3 in swimAmp and the t >= 4.4 gate × K;   cues: lyre 2.05 * K, 3.35 * K; whoosh 2.6 * K with d 4.2 * K
// unchanged: FD 0.3, the 0.14 s landing, SWIM_STEP and the swim itself (film time)
// 6 s, 16:9 or 9:16: sweep seg(t, 3.95, 4.85); fade Math.max(1 - seg(t, 0, 0.4), seg(t, 5.7, 6.0)); swish 2.7, 4.5; glint 3.95, d 0.9;
//   chord 4.75; audio.py DUR 6.0, drenv (t - 0.9) / 1.8, fo 0.6 s.  Floor done 4.1 s, settled from 4.867, 0.87 s held.
// 4 s, 9:16 (Composition values), cut plan: drop the dolphins and waves (DREST = [], WAVES = [], the two s < 2 loops
//   → DREST.length), the swim, the sweep and the border race; keep title, medallion and the field round it.
const KC = 0.41;   // camera; actions keep K = 0.6
// build() step 4: TA[n] = t.zone <= 3 ? 99 : ta * K;   (borders never land and stay out of view; their ticks pass DUR)
// window.draw: camera(t / KC); camera(): Math.log(0.585) → Math.log(1.1) (keep it ≥ 1.08: below, the unlaid
//   guilloche enters the frame edges); cur = null, prev = null; sw = 0; fade Math.max(1 - seg(t, 0, 0.3), seg(t, 3.72, 4.0))
// cues: lyre 2.05 * K, 3.35 * K; whoosh 0.3 * KC, d 6.5 * KC; chord 2.85; audio.py DUR 4.0, drenv (t - 0.62) / 1.23, fo 0.5 s
// Title laid by 1.23 s, medallion by 2.5 s; settled from 2.800, 0.93 s held; end card: medallion 1060 px wide, title
//   cap 132 px, subtitle cap 52 px, the caption band holds field and crosslets.
```
  - From 6 s to 10 s keep every beat and shorten the sweep; under 6 s cut whole beats: the sweep (with `glint`), the
    swim (with `swish`), then border race and figures (end the camera on the medallion). Title: 1.8 s × K + 0.14 s.
  - The whole floor in 4 s (K 0.41 in the 6 s lines, no sweep, no swim; fade and audio.py as in the cut plan, `chord`
    at 2.9; rendered in 9:16: settled from 2.867, 0.87 s held) floods rather than lays: S, A and L land under the
    fade-in, the dolphins in 0.37 s.
- **Other formats:** see Composition (9:16 and 1:1 values, checks, stand-in).

## Boundaries
- **Distinct from:** `byzantine` (the same tesserae engine on a wall: glittering gold-glass ground, frontal haloed
  figures, lamplight); `greek-pottery` (black-figure painted on a turning vase; its meander is painted, here each key
  cell is a stone); `stained-glass` (light through glass and lead, glow, beams); `pixel-art` (a strict pixel grid and
  game UI, no rows following contours); `islamic-geometric` (compass-built star patterns in glazed tiles, no figures);
  `pointillism` (optical dots of paint); `art-nouveau` (a mosaic halo as one ornament of a poster).
- **Poor fit:** charts (`data-visualization`), caption-led hooks (`bold-captions`), interface demos (`product-ui`),
  long or changing text (`kinetic-typography`), lessons (`whiteboard`), stories carried by people (`greek-pottery`).
- **Do not:** use gods, saints or rites as decoration (Neptune's trident, Bacchus, Venus, Orpheus, a Medusa head,
  altars, sacrifices, crosses or the Chi-Rho; keep crosslets small fillers), or the swastika meander, a common Roman
  variant of the key (keep the running key). No pseudo-Latin: no Latin-looking English, no V for U in English words,
  no lorem ipsum or invented inscriptions; Latin only from the user or checked by a speaker (SALVE, AVE and VALE are
  real); Roman numerals must be correct.
- **Do not:** reproduce a famous mosaic or its layout: the Alexander Mosaic, Pompeii's CAVE CANEM dog, the doves at a
  bowl, the Palestrina Nile mosaic, the Piazza Armerina athletes, the unswept floor, Ravenna's apses. No gold ground
  or halos, lead lines, gradients, a uniform grid for figures, or text over the floor.

## Technical notes
- `render.json` sets `{ "gpu": "metal" }`; Canvas 2D, no vendor/, one woff2. `window.ready` builds the floor in about
  2.3 s (32,337 stones; 9:16 32,355). Frames take 0.05–0.1 s in the close-up, 1 s at 5 s and 2.6 s with the whole
  floor (one page, Apple silicon): about 7 minutes per worker for 10 s. The view culls stones (`vr`), the sweep not.
- build.sh encodes at CRF 19 (18 gave 42.5 MB). Fades are a dark rect drawn last, not a scene `globalAlpha`. A frame
  drawn first in a page differs from the same frame drawn after others by up to 24 levels (45 dB; the gradient-state
  effect in contract.md): one transparent gradient `fillRect()` at the end of `window.ready` fixes it (tested).
- Tied to 1920 × 1080 and the 3200 × 1800 floor: see the 9:16 block; keep the subtitle timing's 540 (a span, not a size).

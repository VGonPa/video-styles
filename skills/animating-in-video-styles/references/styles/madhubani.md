# Madhubani (`madhubani`)

Mithila (Madhubani) folk painting from Bihar: every motif is outlined twice in black with a band of pigment
between, filled with flat turmeric, vermilion, indigo and leaf green, then covered in fine black patterns, and
no paper is left empty. The film paints itself in the painter's order (outline, colour, pattern), then the
finished picture comes gently alive. Festive, warm, symmetrical and calm.

**Reference film:** "The Tree That Feeds the Birds": two fish are painted in a pond, the camera pulls back as a
zigzag border draws itself, a tree of life grows, sun, moon and two peacocks are painted, four parrots land,
small flowers fill every gap, a title strip inks in and the sun smiles · `styles/madhubani/`

## Signature
- A tight close-up (2.9×, `ZOOM`) on warm handmade paper where double outlines draw themselves (no pen is shown),
  two ink lines with a band of vermilion or turmeric between (`dbl` ops), round a pond and two fish.
- Colour follows the outline as flat, unshaded pigment brushed in as a diagonal sweep (bharni, `fill`): pale-blue
  water, a turmeric ring, fish in bands of turmeric, pink, green, orange, lime and indigo.
- Fine black patterns then cover the colour (kachni: `scales`, `hatch`, `dots`): fish scales, stripes, dot rows.
- Creatures have a big almond eye in a white ring and a small smile; the fish swim among rippling indigo lines.
- Before 3 s the zigzag-triangle border starts along the bottom and the camera begins to pull back.

## Palette
| Role | Colour | In code |
|---|---|---|
| Handmade paper; the fades | `#f3e3be` | `C.paper` |
| Lamp-black ink: every outline, hatch, dot and letter | `#1c130e` | `C.ink` |
| Turmeric: pond ring, leaf and tree gaps, sun, title strip, border triangles | `#eeb21e` | `C.yel` |
| Marigold: fish head, sun rays, peacock beaks, legs, canopy flowers | `#ec7a1f` | `C.org` |
| Vermilion (outline gaps, fins, rays, triangles); dark vermilion (bark, title dots) | `#d8371d` `#a3230e` | `C.ver`, `C.verD` |
| Indigo (waves, peacock bodies, moon ring, corner squares); light indigo (crescent) | `#26358a` `#5d73c2` | `C.ind`, `C.indL` |
| Pond water | `#bccbe8` | `C.water` |
| Pink, light pink: fish body, flowers, cheeks | `#e2477d` `#f4a7c3` | `C.pink`, `C.pinkL` |
| Leaf greens: leaves, peacock trains, parrots, grass | `#3b8a3a` `#236126` `#8fc24f` | `C.grn`, `C.grnD`, `C.grnL` |
| Root gap | `#8a3f1b` | `C.brown` |
| Off-white: eyes, moon face, body dots, stars | `#fbf4e2` | `C.white` |
| Paper blotches, fibres, specks; vignette | `rgba(214,168,98` `rgba(255,248,226` `rgba(140,100,50` `rgba(120,80,40` `rgba(170,110,50,0.26)` | `bakePaper()` |

- Every fill is one flat pigment, no gradient or shade; shapes split into flat bands instead (fish in head,
  scaled body and striped band; leaves in two halves along the midrib).
- The pigment between the two ink lines contrasts with what it surrounds: vermilion round the turmeric pond and
  sun, turmeric round green leaves and the red tree, turmeric or pink round the indigo peacocks.

## Typography and copy
- One face, Yatra One (`FT`, `fonts/YatraOne-400-latin.woff2`), for the title only: 50 px, mixed case, ink on the
  turmeric strip. The file is a Latin subset (Latin-1, curly quotes, dashes, €): no Devanagari (see Boundaries).
- `drawTitle()` pops each letter from zero about its centre with `eBack`, 0.22 s each, staggered over 0.55 s from
  0.4 s after the strip starts; it stays until the final fade.
- Copy: one folk-tale title in plain English, title case, three to seven words, no punctuation, no other text.
  At 50 px the 29-character demo title is 748 px (about 26 px a character; "M" 43.5, "i" 13.8): keep one line
  under about 880 px in the 948 px 16:9 strip `TR` (about 33 characters), 780 px in 9:16, 760 px in 1:1.

## Texture and finish
- `bakePaper()` builds, once and seeded: `PAPER` (90 soft blotches, 2600 fibre curls, 260 specks), drawn under
  the camera so its fibres enlarge in the close-up; `GRAIN` (warm noise, vignette radii 520–1180 px), multiplied
  over each frame in screen space. `wob()` gives outlines a static hand wobble that never boils. Nothing
  refreshes per frame: no animated grain, blur, bloom or glow.

## Shapes, line and figures
- Every motif is a list of timed strokes, `S(kind, t0, t1, o)` in local coordinates, prepared with `prep()` and
  drawn with `drawMotif(g, ops, lt, M)` (`M` maps points, as in the fish's swim). Kinds: `line`, `dbl`, `fill`,
  `hatch`, `scales`, `dots`, `pop` (a small solid shape that springs in, optionally ink-edged).
- `dbl` is an ink line of width `w` under a pigment line of width `gap`: ink shows (w − gap) / 2 each side.
  Weights at 1×: pond 9 / 3.4, fish, sun and rulings 8 / 3, peacock train 7 / 2.6, fins 6 / 2.2, leaves and
  wings 5 / 1.8, parrots 4.5 / 1.6, roots 11 / 4.5. Kachni: `hatch` `sp` 6–9 with `lw` 1.3–2.2, `scales` `r`
  5–11, dot rows 2.2–3.2 px, white dots on indigo; one pattern and one direction per band.
- Eyes: a white almond, 3 px ink edge, black pupil, catch-light (`makeFish()`); faces add the Mithila eye tail and
  vermilion lips (drawn live by `sunFace()`, `moonFace()`) and arched brows, a long nose and pink cheeks (ops in
  `makeSun()`, `makeMoon()`). Animals in profile.
- Flat and frontal: no perspective, shadow or overlap between large motifs (only parrots over leaves, fish over
  waves); pairs mirror. `drawTree()` draws all ink layers, then all turmeric, then bark, so junctions stay clean.
- No empty space: `buildFillers()` puts flowers, dot triangles, sprigs and spirals (`makeFiller()`) on a 34 px
  grid wherever its occupancy test finds room (register new motifs there, as the peacock polygons are).
- A new motif (an elephant, a boat): a closed `dbl` outline at 7–9 / 2.6–3 with a contrasting gap, two or three
  flat `fill` bands, a kachni pattern per band, a dot row, an almond eye. Build it at final size: scaled up, a
  peacock at 2.2× gets 15 px outlines and 18 px hatch gaps, coarse beside everything else (rendered).

## Composition and camera
- 16:9: a framed painting, a 48 px border between `BO` and `BI`. Tree on the axis x 960, pond under it (`POND`
  640–1280 × 700–985), sun (`SUNP`) and moon (`MOONP`) in the top corners at 1.15 (`frame()`), title strip top
  centre (`TR`), peacocks at x 452 and 1468 (`window.ready`), `PSC` 1.15, baseline 985, facing in; grass y 1004.
- One continuous shot from `camera()`: `ZOOM.s` 2.9 on `ZOOM.c` (the pond), a pull-back over `TL.zoom` (`eInOut`
  on the log of the scale, the centre drifting to the frame centre), a 3.5 % push-in from 8.6 s; no cuts or pans.
- Keep every zoom centre at least W / (2 s) from the side edges and H / (2 s) from top and bottom: `PAPER` covers only
  0…W × 0…H and `frame()` never clears the canvas, so beyond it the view shows the previous frame (unpainted and
  non-deterministic). The 9:16 close-up is 4 px inside the limit: do not move its `ZOOM.c` down or lower `ZOOM.s`.
- 9:16 (1080 × 1920; rendered every beat, the parrots' flights, the fishes' widest drift, right at 1.85 and 9.24 s
  and left at 5.54 s, and the end): canvas, `W`, `H`; all from pond to tree, and the parrots, keep 16:9 coordinates:

```js
const G = { dx: -420, dy: 330, k: 1 }, gx = x => G.dx + G.k * x, gy = y => G.dy + G.k * y;   // 1:1: dx -180, dy 245, k 0.75
// frame(): translate(G.dx, G.dy), then scale(G.k, G.k), round POND_OPS … drawTree() and again round the parrots
// buildFillers(): [gx(x), gy(y), G.k * r] for branch, leaf, flower, bird points; pond box gx(POND.x0 - 10)…gx(POND.x1 + 10),
//   y > gy(POND.y0 - 38) (the root tops, the demo's 662); trunk box gx(915)…gx(1005), y > gy(455); grass pond test likewise
```
  - Frame: `BO` 24, 22, W − 24, H − 22 and `BI` 48 px inside; 960 → `W` / 2 in `perimPos()` and `camera()` (540
    → `H` / 2). Sun [240, 236], moon [848, 226], at scale 1 (the two 1.15 in `frame()`; `free()`'s radii 186 and
    158 → 162 and 137). `TR` x 110–970, y 410–486; `drawTitle()` centres on the strip, not 960, with the baseline
    at `TR.y0` + 55, not 145, and `buildTitle()` starts the outline at the strip centre: the demo title spans
    x 166–914, clear of review.md's top 15 % and right 12 %. Peacocks (drawn outside the group) `PSC` 0.95 at
    x 380 and 700, baseline 1320 (the 985 in `drawPeacock()` and `buildFillers()`). `ZOOM` s 2.7, c [540, 1560].
  - Group: `POND` 770–1150 × 1000–1460 (portrait, so the close-up fills a tall frame); fish at (975, 1120) facing
    right and (945, 1330) facing left; `drawWaves()` draws floor((pond height − 50) / 24) = 17 lines, not 10;
    trunk `tcl` = `bez([960, 1000], [957, 821], [963, 641], [960, 462], 40)` and roots y + 300: the 538 px trunk
    leaves room for the peacocks under the canopy.
  - `buildFillers()` also: a title box, not "all above `TR.y1`" (which empties the 9:16 sky); loops to `H` − 90
    and `W` − 80; 978 → `BI.y1` − 32; ripple centre `W` / 2, `H` / 2. Grass on `BI.y1` − 6; in `buildGrass()`
    960 → `W` / 2, 900 → `W` / 2 − 60.
  - Result: 17 % blank paper above and below the close-up until roots and grass (about 1.3 s), then 12–13 % above;
    every motif whole at the end; the bottom 25 % band holds pond, grass, border and (from 6 s) fillers.
- 1:1 (1080 × 1080; rendered the same way): `G` as commented (lines thin to about 6 px, still readable). Group
  `POND` 720–1200 × 660–985, fish at (915, 765) and (1005, 885), 11 wave lines by the 9:16 formula, trunk `tcl`
  from [960, 660] (`bez([960, 660], [957, 594], [963, 528], [960, 462], 40)`), roots y − 40 (a pond starting higher
  than 660 meets the lowest leaves). Frame: sun [215, 318], moon [880, 295] at 0.85 (radii 137 and 117); `TR`
  x 140–940, y 90–166; peacocks `PSC` 0.68 at x 290 and 790, baseline 988 (beaks 10 px from the pond); `ZOOM`
  s 2.9, c [540, 862]. Blank paper about 16 % above and below until roots and grass (about 1.4 s), 10–12 % after.
- Stand-in (9:16, a 2.2× peacock for the tree): frame values held; y shift, trunk, peacocks, perches follow the tree.

## Motion
- The painter's order in every motif, kept for new ones: double outline (ink leading, pigment line 4 % behind,
  `strokeDash()`), eye pops, bharni colour, kachni patterns, dots.
- `fill` sweeps overlapping strokes across the shape, then snaps solid; `hatch` draws line by line (`eOut`);
  `scales` adds arcs column by column; `dots` and `pop` spring in with `eBack` (about 13 % overshoot). Trunk
  `eInOut`, branches `eOut` (`branchGeom()`), leaves spring out as the tip passes; parrots fly a curve eased by
  a 2.2 power, wings at 5 Hz, and land with a 7 px bounce.
- Living finish, small and slow: fish swim (`fishMap()`: 28 px drift, 9 px tail wave at 1.25 Hz), waves ripple,
  leaves sway ±0.03 rad, birds bob, peacocks nod, the sun smiles and blinks, the moon wakes. Fades: in 0.3 s, out
  with `eInOut`. Never: cuts, shake, blur, 3D, squash, boiling lines, or colour before its outline.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–1.45 | Paper fades up (0.3 s) at 2.9× on the pond: two double outlines, water and turmeric ring brushed in, ring hatched | `frame()`, `ZOOM`, `TL.pond`, `buildPond()` |
| 0.3–2.7 | Two fish painted (outline, eye, bands, scales, hatching, dots); each swims from 0.5 s after its start | `TL.fishA`, `TL.fishB`, `makeFish()` |
| 0.9–1.97 | Ten wave lines run across, alternating direction; four roots traced on the bank 1.05–1.86 | `TL.waves`, `drawWaves()`, `TL.roots` |
| 1.35–4.6 | Grass tufts spring up along the bottom, pond first | `TL.grass`, `buildGrass()` |
| 1.85–4.75 | Border rulings drawn from the bottom centre both ways; triangles and corner flowers pop behind | `TL.border`, `buildBorder()` |
| 2.65–4.1 | Camera pulls back to the whole painting | `TL.zoom`, `camera()` |
| 2.85–5.9 | Trunk and seven branches grow, leaves spring out, tip flowers open; twelve canopy flowers from 4.45 | `TL.trunk`, `buildTree()`, `drawTree()` |
| 3.75–5.85 | Sun painted (face fades in), moon with closed eye and stars, two mirror-image peacocks | `TL.sun`, `TL.moon`, `TL.peaL`, `TL.peaR` |
| 4.85–7.05 | Four parrots fly in and land at 5.85, 6.1, 6.35, 6.6 | `buildBirds()`, `drawBird()` |
| 5.6–7.35 | Fillers ripple out from the centre into every gap | `TL.fill`, `buildFillers()` |
| 6.55–7.7 | Title strip outlined, filled, pennants and dots; letters pop | `TL.title`, `drawTitle()` |
| 7.35–8.9 | The sun smiles; the moon opens its eye 7.8–8.1; the peacocks nod 7.9–8.9 | `TL.smile`, `TL.wake`, `drawPeacock()` |
| 8.6–10 | Push-in to 1.035×; the sun blinks 8.7–8.95; fade to paper 9.25–10 | `camera()`, `TL.blink`, `TL.out` |

- One scene that builds (all reusable): close-up, pull-back, motifs 0.25 s apart and overlapping (1.3–2.2 s each),
  the painting coming alive. The demo holds its final state only 0.3 s: the nod runs to 8.9 s, the blink to
  8.95 s, the fade starts at 9.25 s. Actions (nod, blink, smile, wake) must end 0.8 s before the fade; the ambient
  loops (swim, waves, sway, head bob, sun rock) may run on. In a 10 s film: `TL.blink` 8.15–8.4 and in
  `drawPeacock()` 7.9, 8.3, 8.9 → 7.9, 8.2, 8.45 (rendered: settled at 8.45 s, against the 9.23 s frame).
- KEYS: 1.2 (colour sweeping in), 2.45 (first fish done in close-up), 3.4 (mid pull-back), 6.4 (parrots landing,
  fillers rippling), 7.75 (title done, sun smiling), 9.2 (final state).

## Sound
audio.py synthesizes everything with NumPy (seeded `rs`) from cues `{k, t, …}`; unknown kinds are skipped silently.
- Fixed times, not cues: a tanpura-like drone on D and A (`tanpura()`) over all of `DUR`, fading in over 1.2 s;
  six plucks at 0.05–1.45 s and eight at 2.9–5.2 s (`pluck()`, major pentatonic on D). Re-time both.
- `water` (t): the pond bed from t to the end, ducked to 55 % from 3.0 s over 1.2 s for the demo's pull-back
  (fixed: move it with your zoom). Found with `next()`: without it StopIteration; at or past `DUR` a ValueError.
- Painting: `pen` (t, `d`) a nib scratch of min(`d`, 1.6) s per outline; `brush` (t, `d`) a rustle for colour;
  `hatch` (t, `d`) a softer scratch; `plip` (t) a tap as an eye pops; `dots`, `rays` (t, `d`) eight and six taps
  over `d`; `grow` (t, `d`) a low rustle per branch; `whoosh` (t, `d`) the pull-back. Small events (with `pan`):
  `pop` a tap per three leaves, `bloom` a pluck per flower, `tick` a tap per five fillers, `flap` (also `d`)
  wing flutter, `land` chirp and tap.
- Beats: `title` five rising plucks; `smile` three bells left (sun); `wake` one bell right (moon); `peacock` two
  chirps; `end` five falling plucks, then a low pluck and bell 0.85 s later ringing 2.4 s: send it 1.1–1.4 s before
  the film ends (8.9 s in the demo).
- Limits: `pen`, `brush`, `hatch`, `whoosh`, `grow`, `flap`, `rays`, `dots` read `d` with no default (KeyError);
  `d` ≤ 0 on any but `rays` and `dots` raises a ValueError (an empty FFT). `add()` clips pans (`np.clip`): no
  NaN. Cues past `DUR` drop silently. Master: 0.05 s fade-in, fixed 1.0 s fade-out (`fo`), tanh soft clip.
- Emit `pen`, `brush`, `hatch` per motif, `water` if there is water (or delete its block), `whoosh` with the
  camera, `bloom`, `pop`, `tick` for growth and fillers, and `end`. Offsets and `d` in `window.events` are in
  motif time (fish `brush` at start + 0.85, d 0.65): divide both by the motif's speed-up. Tested in the 6 s plan,
  each cue then lands on its phase; left as is, the fish's hatch comes 0.4 s late. The trunk's `grow` (d 0.8) and
  `flap` (flight start + 0.3, d 0.7) are sized for the demo's 0.7 s trunk and 1.0 s flight: shorten them too.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Paper, pigments, maths | `js/lib.js` → `bakePaper`, `js/lib.js` → `C` | `bakePaper()` builds `PAPER` and `GRAIN` from `W`, `H`; `C.<name>`; `seg(t, a, b)`, `eOut`, `eInOut`, `eBack`, `lerp`, `clamp`, `mulberry(seed)`, `mk(w, h)` | as is; add pigments as hex |
| Polylines and outlines | `js/lib.js` → `bez`, `js/lib.js` → `ell`, `js/lib.js` → `wob`, `js/motifs.js` → `tube`, `js/motifs.js` → `bodyBand` | `bez(p0, p1, p2, p3, n)`, `ell(cx, cy, rx, ry, n, a0, a1)`, `wob(p, amp, seed, step)`; `tube(cl, w0, w1)` a tapered limb or branch; `bodyBand(hw, xa, xb, ba, bb, n)` a body cut into bands | as is |
| Stroke ops | `js/motifs.js` → `S`, `js/lib.js` → `drawMotif` | `S(kind, t0, t1, o)` with o.p, w, gap, gc, c, a, sp, lw, r, dir (`scales`, ±1), d, o (`pop` origin), edge, closed; `prep(ops)`; `drawMotif(g, ops, lt, M)`; lt × k speeds a motif up | as is |
| Fish | `js/motifs.js` → `makeFish`, `js/scene.js` → `fishMap` | `makeFish(pal, seed)`: pal head, body, band, tail, fin, gap; faces +x; painted over 2.15 s; `fishMap(F, t)` swims it at scale 0.85, dir ±1 | as is |
| Leaf, flower, fillers | `js/motifs.js` → `makeLeaf`, `js/motifs.js` → `makeFlower`, `js/motifs.js` → `makeFiller` | `makeLeaf(len, wid, seed, cA, cB)`, `makeFlower(r, petal, heart, seed)`, `makeFiller(kind, s, seed)` (0 flower, 1 dot triangle, 2 sprig, 3 spiral) | as is |
| Parrot, peacock | `js/motifs.js` → `makeParrot`, `js/motifs.js` → `makePeacock` | `makeParrot(body, seed)` returns ops, wing, legs, shoulder, drawn whole by `drawBird()`; `makePeacock(seed, gc)`: feet at origin, faces +x, about 388 × 358, head ops nod about `pivot` (`drawPeacock()`) | as is or replace |
| Sun and moon | `js/motifs.js` → `makeSun`, `js/motifs.js` → `makeMoon` | `sunFace(g, sm, blink, lt)` smiles and blinks; `moonFace(g, open, lt)` | as is |
| Border and grass | `js/scene.js` → `buildBorder`, `js/scene.js` → `buildGrass` | `BO`, `BI`, `TL.border`; spreads from the bottom centre via `perimPos()`; tufts every 26 px on y 1004 | as is (960 → `W` / 2; grass also 900 and 1004, see Composition) |
| Pond and waves | `js/scene.js` → `buildPond`, `js/scene.js` → `drawWaves` | `POND`; ten lines 24 px apart | adapt size |
| Tree of life | `js/scene.js` → `buildTree`, `js/scene.js` → `drawTree` | branch rows: control points, widths, start offset; perches | adapt or replace |
| Fillers | `js/scene.js` → `buildFillers` | occupancy points and polygons, `free()` exclusions, ripple from `TL.fill` | adapt: register every new motif |
| Title strip | `js/scene.js` → `buildTitle`, `js/scene.js` → `drawTitle` | `TITLE`, `TR`, `TL.title` | adapt text and place |
| Camera | `js/scene.js` → `camera` | `ZOOM` (s, c), `TL.zoom`, push 8.6–10 s | adapt target (keep it W / (2 s) and H / (2 s) from the paper edges; clamp a second zoom, see Length) |
| Timeline and cues | `js/scene.js` → `TL`, `js/scene.js` → `frame` | draw order in `frame()`; `window.events` | replace |

## Adapting
- **Style vs demo plot:** the style is paper and grain, the triangle border, pen-traced double outlines, bharni
  then kachni, the pigments, almond eyes, mirrored frontal layout, no empty space, close-up and pull-back, a
  living finish, drone and plucks. Tree, pond, fish, birds, sun and moon and the title are plot. A transformation:
  the painting completing itself, a growth, birds landing, day to night (sun, then moon), a creature waking.
- **New subject:** motifs built with `S()` in the painter's order, each with a `TL` key. Traps: fillers cover what `buildFillers()` is not told about; `frame()` draws fillers above the
  peacocks and below parrots and title; without a white-ringed almond eye a creature reads as another style.
- **Length:** add motifs and arrivals before the fill ripple, the one climax; more than about three similar
  motifs in a row turn monotonous. A second close-up (tested in a 14 s cut: into the sun 10.2–11.0 s, out 12.0–12.8 s)
  multiplies a second scale into `camera()` and clamps the centre (see the zoom limit in Composition):

```js
const [a, b, c, d] = TL.zoom2, v = eInOut(seg(t, a, b)) * (1 - eInOut(seg(t, c, d)));   // Z2 = { s: 2.6, c: SUNP }
const z = Math.exp(lerp(0, Math.log(Z2.s), v)), q = (z - 1) / (Z2.s - 1), S3 = s * push * z;
const zx = clamp(lerp(cx, Z2.c[0], q), W / 2 / S3, W - W / 2 / S3), zy = clamp(lerp(cy, Z2.c[1], q), H / 2 / S3, H - H / 2 / S3);
return [S3, 0, 0, S3, W / 2 - zx * S3, H / 2 - zy * S3];
```
  At 2.6× the sun (or moon) close-up also shows one end of the title strip, cut to "The T" at the frame edge
  (rendered): ink the title after the second close-up. Re-time `TL`, the literals under Shorter, and in audio.py `DUR`, both phrases, the water duck and `end`.
- **Shorter:** besides `TL` (its second values for waves, roots, grass and title are unused) re-time `buildTree()`'s
  branch start 0.45 + b[6] × 1.0, length 0.85 and canopy flowers' 4.45 + …; `buildGrass()`'s 1.5 and 0.9 + u × 2.1;
  the landings and 1.0 s flight in `buildBirds()`; 6.8, 7.9, 8.3, 8.9 in `drawPeacock()`; 0.4 + i / n × 0.55 and
  0.22 in `drawTitle()`; 8.6 and 10 in `camera()`; the `peacock` and `end` cues and the `title` cue's + 0.4 (the
  first-letter offset). Speed a motif with lt × k in `drawMotif()`, `sunFace()`, `moonFace()`; `drawTree()`'s leaf
  loop already uses 1.1, its flower loop draws tip and canopy flowers. Both plans rendered in 16:9 with events.mjs
  and audio.py (numeric peaks); holds measured against the last frame before the fade, push off and ambient loops
  zeroed: from the settle time every frame matches it exactly:
  - 6 s, all beats: fish 0.2 and 0.35 (× 1.4), waves 0.6, roots 0.8, grass 0.9 (0.8; 0.5 + u × 1.2), border 1.2–2.8,
    zoom 1.75–2.65, trunk 1.85–2.3 (branches 0.3 + b[6] × 0.6, 0.55 long; leaf loop 1.1 → 1.6), sun 2.35 and moon
    2.5 (both × 1.3), peacocks 2.6, 2.75 (× 1.3), canopy flowers 2.75 + offsets × 0.5 (flower loop × 1.4), parrots
    land 3.25–3.7 after 0.8 s flights, fill 3.3–4.0, title 3.6 (letters 0.3 + i / n × 0.4, 0.2 each), smile
    4.45–4.85, wake 4.6–4.85, nod 6.8, 7.9, 8.3, 8.9 → 3.9, 4.4, 4.65, 4.95, no blink, push 4.95–6, fade 5.75–6.0;
    settled at 4.95 s. audio.py: `DUR` 6, tree phrase 1.85 + i × 0.2, duck 1.75 over 0.9, `fo` 0.6; cues `peacock`
    4.4, `end` 4.6, `title` at the title + 0.3.
  - 4 s, beats cut: drop the title (and its `free()` test, or fillers leave a hole), the peacocks (`PEA` empty: a
    late start still reserves their silhouettes), the parrots (`buildTree()`'s perch list emptied, or the leaves
    keep gaps), the moon's waking and the blink. Fish 0.1 and 0.25 (× 1.6), waves 0.5, roots 0.7, grass 0.8 (0.6;
    0.4 + u × 0.8), border 1.0–2.3, zoom 1.45–2.2, trunk 1.55–1.9 (branches 0.2 + b[6] × 0.4, 0.45 long; leaf loop
    1.1 → 1.6), sun 1.9 and moon 2.0 (both × 1.6; at × 1 the sun's rays run to 3.3 s), canopy flowers 2.2 + offsets
    × 0.3 (flower loop × 1.4), fill 2.05–2.75 (fillers × 1.5), smile 2.6–2.95, push 3.0–4.0, fade 3.75–4.0; settled
    at 2.95 s. audio.py: `DUR` 4, tree phrase 1.55 + i × 0.15, duck 1.45 over 0.75, `fo` 0.5, `end` 2.6.
  - After the 0.3 s fade-in, outline, colour and the first scales show by about 1.1 s (fish × 1.6); pull back
    no earlier than 1.45 s. Drop first the title (settled 0.9–1.15 s after it starts, then the 0.8 s hold: about
    2 s), then parrots, peacocks, the moon; keep close-up, pull-back, one growth, fill ripple and smile.
- **Other formats:** values in Composition; the frame elements recompose once their numbers use `W` and `H`,
  while the tree group, the pond's shape and the zoom need placing by hand.

## Boundaries
- **Distinct from:** `mesoamerican-codex` (single thick outlines, flat red and turquoise on deerskin, profile
  figures); `persian-miniature` (fine brushwork, gold, tilted gardens); `egyptian-papyrus` (registers,
  processions); `chinese-papercut` (red lace cut live).
- **Poor fit:** charts (`data-visualization`); lessons (`whiteboard`); how things work (`blueprint`); caption-led
  posts (`bold-captions`); stories carried by people (`persian-miniature`; this style has no figure kit).
- **Do not:** use deities or worship as decoration (gods and goddesses, haloes, many arms, sacred syllables, Surya
  on his chariot or a Chhath offering), and do not reproduce a kohbar, the wedding-chamber composition with its
  central lotus ring and bamboo grove. Fish, parrots, peacocks, trees, flowers, and sun and moon as faces also
  appear in kohbar, but they are the everyday motifs of secular Mithila painting and are fine. No invented letters
  imitating Devanagari or Tirhuta: English titles, or a real Hindi or Maithili line in Yatra One's Devanagari
  subset (added to `fonts/`) checked by a speaker. Do not copy a named Mithila artist's painting or present the
  film as authentic Mithila art (a registered Geographical Indication of Bihar). No empty paper at the end.

## Technical notes
- anim.html loads `js/lib.js` (helpers, `C`, ops, paper), `js/motifs.js` (motif builders) and `js/scene.js`
  (layout, `TL`, camera, `frame()`, `window.events`), sharing globals; canvas id `c`. No render.json or vendor/:
  Canvas 2D, no GPU; 300 frames in about 19 s on one worker (measured, Apple silicon), plus the encode.
- Deterministic (`mulberry()` seeds; 6.2 s alone and after other frames is identical); `frame()` resets
  transform, composite and alpha, so wrap added drawers in `save()`/`restore()`.
- Sizes outside `W`/`H`: those in the 9:16 notes, plus 1920 in `buildTree()`'s mirror and the parrots' start
  points (inside the group) and the `pan` formulas (cosmetic: audio.py clips pans). The vignette radii suit any
  frame 1080 px on its short side.

# Isometric (`isometric`)

A miniature model world in true isometric projection: floating square tiles of flat three-tone blocks, cutaway
rooms, toy vehicles and crisp translucent shadows on warm beige paper, in the tradition of isometric
infographics and "tiny world" explainers. Tidy, cheerful and legible; the camera glides over the model and
zooms, but never turns it.

**Reference film:** "The journey of a parcel": packed in a workshop, trucked along a road, scanned at a sorting
hub, carried by van to a doorstep; then the camera pulls back over the four-tile world under the title · `styles/isometric/`

## Signature
- Warm beige paper with a soft central glow and a faint grid; the world stands on floating 10 × 10 tiles whose
  0.8-deep slabs show brown sides (lower-left face lighter, lower-right darker).
- True isometric, the same in every frame: verticals stay vertical, both ground axes run at 30°, all three axes at
  one scale, no perspective; the camera pans and zooms but never rotates.
- Three-tone flat blocks: lid in the base colour, lower-left face 16 % and lower-right face 34 % of the way to plum
  `#3b2946`; a thin white bevel on lid edges; no outlines, no texture.
- Flat translucent plum shadows fall to the lower right.
- Arrival choreography by 3 s: the first tile rises with an overshoot, its walls grow, props drop in one by one
  and squash; a sign painted onto a wall in perspective; a second tile rises and the camera glides towards it.

## Palette
| Role | Colour | In code |
|---|---|---|
| paper | `#efe4d6` | `PAL`, `paintPaper()` |
| paper glow, centre → edge | `rgba(255,250,242,0.9)` → `rgba(214,190,170,0.5)` | `paintPaper()` |
| floor grid | `rgba(120,90,80,…)` at alpha 0.07 | `floorGrid()` |
| shade ink: every face darkens towards it | `#3b2946` | `SHADE_INK`, `sh()` |
| floor shadows | `rgba(70,40,60,…)` at 0.12–0.18 (0.18: the flyer's ellipse) | `shadowFill`, `shadow()`, `oshadow()`, `renderFrame()` |
| lid bevel | `rgba(255,255,255,0.35)` | `edge()` |
| grass, second grass, lawn; workshop floor | `#9fcf8c`, `#b5dc8f`, `#a6d27f`; `#e9b07c` | `PAL`, `tileD()` |
| slab sides of grass tiles / concrete tile, its sides | `#d69a68` / `#ddd6cd`, `#c9bfb3` | `PAL`, `slab()` |
| road / dashes and wall caps | `#5d6178` / `#f7efe4` | `PAL`, `roadX()` |
| room walls, darker / lighter: workshop, hub | `#86c3c3` / `#a9d7cf`, `#9aaee3` / `#b3c3ee` | `PAL` |
| kraft, tape, label cream, ink | `#d9a066`, `#f3d49a`, `#fff6ea`, `#23263b` | `PAL`, `parcelBox()` |
| accents: coral, yellow, green, blue | `#ff7b6b`, `#f2b544`, `#5fb07a`, `#6d8bd8` | `PAL` |
| foliage light, pine, trunk; pond | `#72c28b`, `#4f9e6a`, `#a8744f`; `#6fb9dc` | `tree()`, `pine()`, `tileB()` |
| machines: belt, frame, legs, steel; glass, tyres, chassis | `#3b3f58`, `#a3abc4`, `#7f89a8`, `#c9ccd8`; `#2c3350`, `#2b2d3c`, `#4a4e66` | `PAL`, `belt()`, `truckParts()`, `wheelParts()` |
| window unlit → lit | `#8fb5d6` → `#ffd36b` | `house()` |
| tag shadow / check; subtitle | `rgba(59,41,70,0.22)` / `#4fbf78`; `sh(PAL.coral, 0.25)` | `tag()`, `renderFrame()` |

- Flat fills only (gradients: the paper glow and `cyl()` sides); shade comes from `sh()`, never black, so it reads
  warm. A room's walls are two tints of one hue, the darker facing lower right; coral, yellow, green, blue are accents.

## Typography and copy
- One family, Space Grotesk (`fonts/spacegrotesk_v22_V8mDoQDjQSkFtoMM3T6r8E7mPbF4C_k3HqU.woff2`, a variable
  file declared at 500 and 700 in `fonts.css`; `FF` names it). Add every new string to `FONT_FACES`.
- Wall signs: `700 40px` / `700 42px`, capitals, `letterSpacing` 5–6 px, ink on a cream pill, painted onto the
  wall with `paintOn()` so they skew with it. Painted text scales with the zoom (100 canvas px = one unit = `view.s`
  px): the 40 px sign is 24 px tall at S 60, 13 px at the end card's 33.5; words that must be read go in a tag or title.
- Tags (`tag()`): `700 30px`, one capitalised word ("Scanned", "Delivered"), a cream pill 54 px tall with a green
  check disc, a plum drop shadow and a pointer to a world point; screen-space, so always legible.
- Title: `700 76px`, `letterSpacing` −1 px, ink, centred at x 960, y 150; subtitle `500 30px`, 6 px spacing,
  capital past-tense verbs separated by two spaces, a middle dot and two spaces. Measured: the 23-character title
  is 823 px wide (22 capitals would be 1016 px), the 43-character subtitle 861 px (775 px at 4 px spacing). Copy
  is a labelled diagram: one or two words per sign or tag, a four-to-six-word title. Glyphs: Latin-1 plus
  Œ œ, curly quotes, en and em dashes, •, …, €, ™, ↑ ↓ and the minus sign; no ← →, no ł ő š, Greek or Cyrillic.

## Texture and finish
- `paintPaper()` paints the backdrop once in `window.ready`: the paper fill plus a screen-fixed radial glow from a
  100 px circle at (W/2, 480) to a 1150 px circle at the frame centre.
- `floorGrid()` draws lines 2.4 units apart at z −0.8 (the slab undersides), 1.5 px wide, through the projection, so
  it pans and zooms with the world; it fades in over 0.8 s and out with the sink.
- No grain, blur, vignette or outline: flat polygons, with lid bevels and shadows giving the "maquette" feel. A
  paper-coloured `veil` fades in over 0.25 s and out over the last 0.2 s.

## Shapes, line and figures
- Light comes from the upper left. `box(x0, y0, z0, x1, y1, z1, c, o)` draws only the three faces the camera
  sees: the +y side (lower left, `sh(c, 0.16)`), the +x side (lower right, `sh(c, 0.34)`), then the lid in `c`;
  `o.top`, `o.left`, `o.right` override them, `o.noEdge` drops the bevel. `obox()` turns a box by a heading and
  shades each visible side `sh(c, 0.25 + 0.09 * (n[0] - n[1]))` from its normal, the same rule.
- Round parts: `cyl()` (side band shaded left to right from 10 % to 40 %, lid in the base colour), `sphere()` (a
  dark disc with a lit disc pushed up-left), `cone()` (dark silhouette, lit wedge on the left). Floor circles use
  `flatRadii()`: ellipses √3 times as wide as tall.
- No outlines: `edge()` strokes the two front edges of a lid in 35 % white, `Math.max(1, 0.03 * zoom())` px (1.8 px
  at S 60); legs, posts, wheels and slats skip it. `shadow(x0, y0, x1, y1, h, z, a)` lays the footprint plus a copy
  pushed 0.42 × height towards +x as one flat polygon (`oshadow()` for turned boxes); a body in the air gets a floor
  ellipse that shrinks with height (the flying parcel in `renderFrame()`).
- Rooms are cutaways: only the two back walls (on −x and −y), 0.4–0.45 thick with cream caps, a 0.3-tall skirting
  band and a painted sign or pegboard; the front is open. Details are flat decals drawn with `paintOn(o, u, v, fn)`
  in face space: windows, doors, labels, barcodes. On a wall along x, u `[1, 0, 0]`, v `[0, 0, -1]`; along y, u `[0, -1, 0]`.
- A new object: world units, built from `box()`, `obox()`, `cyl()`, `sphere()`, `cone()`, axis-aligned unless it
  travels; one `PAL` colour per part, sides left to the primitive; a floor shadow; bevels on lids over about 0.3 units;
  decals, never a screen-space sprite. Sizes: room walls 4.4, doors 1.7, bench top 1.55, parcel 0.84 × 0.84 × 0.62,
  truck about 3 × 1.3 × 1.6, house walls 2.5 plus a 1.5 roof, trees 1.8–3.5 (`tree()` 2.4 h, `pine()` 2.9 h).
- No people in the demo. A figure rendered for this recipe reads at S 72 (about 120 px): facing +x; thigh, shin and
  ink shoe boxes per leg; a torso 0.42 wide (y) × 0.24 deep (x) from 0.7 to 1.34; upper-arm and forearm boxes `sh()` 0.18 off the shirt,
  one forearm bent forward, skin hand cubes; a thin `cyl()` neck; a `sphere()` head of radius 0.15 with a dark hair box
  on its −x half and top and a 0.1 nose box on +x. Below S 60 it stops reading: keep people out of wide shots.
- Depth is a painter's sort: each tile pushes pieces keyed by footprint centre x + y (plus its `TO` offsets);
  `renderFrame()` draws a ground list (slabs, `ground()` decals, bridges) first, then items by ascending key. Height
  never enters the key. Within a piece, draw back to front and bottom to top by hand. Where a centre misleads, the demo
  writes keys (turbine 13.8, corner belt 13.95, doormat 7.2) or draws neighbours in one group (the belt parcel before
  or after the scanner's front post); vehicles push each part (`truckParts()`) so cargo sorts between bed and cab.
- Walls take key −100, which holds only while no tile lies behind them, as in the demo's row. In a chain down the
  screen (Other formats) each tile's back walls face the tile before it, whose props and vehicles then draw over them
  (rendered: the truck over the hub's sign, a plant on a wall top). There, sort by chain order:

```js
const CHAIN = { A: 0, B: 1, C: 2, D: 3 };   // place of each tile along the chain
// tile items (not ground): k = key + base + 1000 * CHAIN[k]
// movers (vehicle parts, flying token): add 1000 * the highest CHAIN[q] whose TO[q] is <= the mover's x and y
```

## Composition and camera
- Projection, `iso()`: screen x = W/2 + `ISO_X` · s · (x − y), screen y = H/2 + s · ((x + y)/2 − z), with x, y, z
  measured from the camera point `view` and s = `view.s` (×`local.sxy` inside a squash). +x runs down-right, +y
  down-left, each 30° below horizontal; +z straight up. One unit on any axis is s px, so a 1 × 1 floor cell is a
  rhombus √3·s wide and s tall (104 × 60 px at S 60). Never mix in the 2:1 pixel-art angle (26.6°).
- The camera is `view` {x, y, z, s}: the world point at frame centre and the scale. `camAt()` runs a cubic Hermite
  through `CK` rows [t, x, y, z, S, stop], zoom in log space, stop keys at zero velocity. It never rotates (`box()`
  draws only the +x, +y and top faces) or tilts; raising `view.z` moves the world down the frame.
- The world is a chain of islands 2 units apart (`TO` offsets of 12) joined by bridges. 16:9: tile shots at S 60–66
  (a tile about 1040 px wide), the close-up at 76, the whole world at 33.5 → 32.5 (y 230–930) under the title.
- To frame any group: turn the corners that must show (the slab front corner at z −0.8, the tallest top) into
  sx = 0.866 (x − y), sy = (x + y)/2 − z; S = the smaller of usable width / sx span and usable height / sy span;
  put `view` where its own sx, sy fall at the box centre. With a title, the usable box is the frame below the title
  block: 9:16 y 500–1900 (title at 380), 1:1 y 225–1060 (title at 110); set `view` so the tallest top lands at the
  box's top: view sy = top sy + (H/2 − box top) / S (tested: the stand-in's tower at (3.5, 3.5) needs `view`
  (10.45, 4.45, 0) instead of (11.15, 5.15, 0)). 9:16 and 1:1 need the tiles chained down the screen (Adapting).

## Motion
- Easing: `eOut()` (cubic out) for the title, bridges and tape; `eInOut()` (cubic) for drives and hops (belt 1 is
  linear, belt 2 `eOut()`); `eBack(k, o)` overshoot for arrivals: tiles 1.3, walls 1.4, flaps 1.2, label, tags 2.4.
- Tiles rise from 9 units below over 0.5 s (`tileState()`), opaque after a third; walls grow from the floor (`sz`,
  0.45 s); bridges extend over 0.3 s; props fall 6 units, accelerating, in 0.34–0.42 s, then squash and wobble
  (`drop()`), 0.06–0.1 s apart. Vehicles follow `mkRoute()` with `eInOut()`, heading from `pose()`, bumping and
  puffing exhaust; the parcel hops on arcs 1.1–2.0 units high with take-off squash and landing wobble (`hop()`).
- Ambient, kept through the ending: turbine blades (5 rad/s), belt slats and the background parcel stream, hub
  lights stepping at 5 Hz, the slow end zoom. Everything else is action. Exit: tiles hop up 0.8 then fall 16 units
  over 0.45 s each, 0.08 s apart, fading in the last 45 %.
- Damped motions never settle: the `drop()` wobble, the doorstep landing squash (and `hop()`'s, if you draw a token
  after p = 1) and the rock in `truckAt()` and `vanAt()` decay but never reach zero. Taper each before a hold:

```js
// drop():             0.16 * Math.sin(26 * since) / Math.exp(9 * since) * (1 - seg(since, 0.3, 0.7))
// hop(), doorstep:    ... * 0.22 * (1 - seg(t - t1, 0.2, 0.5))
// truckAt(), vanAt(): Math.exp(-land * 7) * Math.sin(land * 20) * 0.05 * (1 - seg(land, 0.2, 0.5))
```

- Never: camera rotation, perspective, cuts, motion blur, objects turned off the grid axes (only travelling
  vehicles turn, along their route). Known defect: exhaust puffs vanish the frame a vehicle stops.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.52 | fade in from the paper (0.25 s); workshop tile rises with an overshoot; grid fades in | `veil`, `RISE`, `tileState()` |
| 0.3–0.9 | walls grow; bench, shelf, lamp, card stack, tree, plant and truck drop in | `tileA()`, `drop()` |
| 0.85–2.07 | box drops on the bench; flaps fold (1.02), tape runs (1.55), label stamps (1.82) | `TL`, `packing()` |
| 0–1.75 | camera pushes from S 60 to 76 on the bench | `CK` |
| 1.15–1.92 | road tile rises, bridge grows (1.5), pines, lamps, turbine drop | `RISE`, `tileB()` |
| 1.98–4.2 | parcel hops into the truck bed; truck drives the bend 2.42–4.2, the camera gliding along | `hop()`, `truckAt()` |
| 2.05–3.1 | hub tile rises, walls grow (2.35), belts, pallet and bin drop; van drops at 3.1 | `tileC()` |
| 4.26–5.72 | hop onto the belt, belt run, laser 4.84–5.14, "Scanned" tag and green light at 5.05 | `parcelOnBelt()`, `tag()` |
| 4.7–5.64 | neighbourhood tile rises, bridge (5.0), houses, fence, trees drop | `tileD()`, `house()` |
| 5.76–7.44 | hop into the van, drive 6.14–7.02, hop to the doorstep | `vanAt()`, `hop()` |
| 7.5–8.2 | windows light, "Delivered" tag pops, fades 7.95–8.2 | `TL`, `house()` |
| 7.45–8.55 | pull back to the whole world (S 64 → 33.5) to 8.4; van leaves 7.62–8.35; title rises 8.05–8.55 | `CK`, `TL` |
| 9.2–10 | title fades; tiles sink 9.3–9.99; fade to paper 9.8–10 | `TL`, `tileState()`, `veil` |

- One continuous shot. Each stage is a tile: it rises (0.5 s) while the camera is on the previous one, props drop,
  one action happens, the camera glides on (1–1.8 s) with the travelling subject. Reusable: tile rise, cutaway room,
  travelling token, tag, pull-back, title, sink. One-off: parcel, packing, truck, conveyor, scanner, van, houses.
- Review stills: `KEYS=0.5,1.75,5.2,7.6,9.0` (walls growing, packing close-up, "Scanned", "Delivered", end card).
- By raw pixel difference against the same moment with every action forced to its end state (ambient kept), the
  demo holds 1 frame (the untapered `vanAt()` rock moves until 9.17). Tested fix: the tapers above, `TL.leave` [7.5, 8.1], `TL.title` 8.15 (swell from 7.9), title fade `seg(t, 9.4, 9.65)`,
  `TL.sink` 9.4, grid fade 9.4–9.9: frames match the end state from 8.60 s through the exit frame at 9.4 s: 25 frames,
  one more than 0.8 s needs. The start is set by the van's taper (`TL.leave[1]` + 0.5) and the title's rise
  (`TL.title` + 0.45), so ending either later costs frames. For more margin in 16:9, use `TL.leave` [7.5, 8.0] with
  `TL.title` 8.05 (28 frames, tested); a title before 8.05 runs over the hub's sign during the wide pull.

## Sound
- audio.py reads `events.json` cues (kind `k`, time `t`, fields `f` Hz, `v` gain default 0.3, `d` seconds) into
  `gen()`: `pop`, `blip`, `bloop`, `bloopdn`, `thud`, `clack` are short `sweep()` tones; `boing` a wobbling sine; `chime`
  a 1.4 s bell; `zip` tape; `scan` a 0.3 s sweep; `ding` a doorbell; `engine` a toy motor; `belt` a rumble; `whoosh` noise.
- Cue by meaning: `thud` (f 80) for a tile rising and big landings; `clack` (f 520–1370) per prop landing, at its
  drop start + 0.42; `boing` at a hop's take-off, `thud` at its landing; `engine` per drive (`d` = drive + 0.1,
  f 62–74); `belt` per conveyor run; `scan` and two `blip` (1760, 2350 Hz) for a check; `ding` for the final success;
  `whoosh` (`d` 1.0) for the pull-back; `chime` 784 then 1175 Hz 0.08 s later for the title; a `bloopdn` per sinking tile.
- Breakers (tested): a sweep kind without a non-zero `f` stops audio.py (division by zero in `sweep()`); `zip`,
  `engine`, `belt`, `whoosh` without `d` raise KeyError; an unknown kind raises ValueError; `zip` under 0.00015 s or
  `belt` under 0.002 s writes NaN samples (a click; audio.py prints nan). Cues outside 0–DUR are synthesized, then
  dropped, so they still need valid fields. Pans stay within ±0.35; a fractional SR × DUR is fine.
- Nothing is looked up by name. Fixed in time: a four-note pad (C3, G3, E4, A4) over the whole `DUR`, fading in over
  1.2 s, whose `swell` rises from 7.8 to 8.8 s into the title: move that 7.8 to the title's time − 0.25. The 0.2 s
  fade-in and 0.7 s fade-out follow `DUR`; a tanh limiter closes the mix.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| projection, polygons | `anim.html` → `iso`, `poly` | `iso(x, y, z)` → screen point; `view`, `tileOff`, `local`, `zoom()`, `flatRadii()`; `poly(pts, fill)`, `edge(pts)`, `ground(pts, c)` | as is |
| primitives, decals, shadows | `anim.html` → `box`, `obox`, `cyl`, `sphere`, `cone`, `paintOn`, `shadow` | `box(x0, y0, z0, x1, y1, z1, c, o)`; `obox(cx, cy, th, u0, u1, v0, v1, z0, z1, c, deco)`, deco front/back/left/right/top draw on faces; `cyl(cx, cy, zBot, zTop, r, c)`; `paintOn(o, u, v, fn)`: o origin, u right, v down, 100 px per unit | as is |
| colour | `anim.html` → `PAL`, `sh`, `mix` | `sh(c, amount)` towards `SHADE_INK` | adapt: add colours to `PAL` |
| easing, drop-in, hop | `anim.html` → `seg`, `eBack`, `drop`, `withLocal`, `hop` | `seg(t, from, to)`; `drop(t, start, at, dur)`, at = [cx, cy, floor z]; `withLocal(o, fn)`; `hop(t, t0, t1, a, b, hgt)` | as is, tapered |
| tiles | `anim.html` → `tileState`, `inState`, `slab` | `TO`, `RISE`, `TL.sink`; `slab(c, side)` | adapt: layout and times |
| scenery | `anim.html` → `tree`, `pine`, `lamp`, `house`, `roadX`, `roadY` | `tree(x, y, h)`; `house(x0, y0, x1, y1, h, wall, roof, main, glow)` | as is |
| routes, vehicles, parcel, conveyor | `anim.html` → `mkRoute`, `pose`, `truckParts`, `vanParts`, `puffs`, `parcelBox`, `packing`, `belt` | `pose(r, s)` → x, y, heading; `parcelBox(x, y, z, th, o)`, o: sq, tape, label | adapt or replace |
| camera | `anim.html` → `CK`, `camAt` | rows [t, x, y, z, S, stop] | adapt |
| paper, grid, tag | `anim.html` → `paintPaper`, `floorGrid`, `tag` | `tag(p, s, text, col)`: p screen point (`iso()` of a world point), s scale | as is |
| painter's lists, title, veil | `anim.html` → `renderFrame` | ground list, then items by key | adapt |
| tiles' content, timeline, cues | `tileA()` … `tileD()`, `TL`, `window.events` | | replace |
| synth | `audio.py` → `gen` | kinds and fields in Sound | as is; re-time `swell` |

## Adapting
- **Style vs demo plot:** the style is the projection and camera rules, the three-tone `box()` family with `sh()`,
  bevels, shadows, paper and grid, tiles rising and sinking, props dropping, painted signs, tags and the closing
  pull-back with title. The plot is the route and everything on the tiles; the transformation can be a state change
  on a tile (a box packed, windows lit, a tank filled) or the token changing at a stage.
- **New subject:** one tile per stage, a travelling token (parcel, drop, crate) carried or hopping between them, one
  action per tile, a sign per stage, a tag when it completes. Traps: `GA` holds the tile's opacity, so a drawer that
  sets `ctx.globalAlpha` must multiply by `GA` and restore it (as `puffs()` does); draw tile content only through the
  push callback (it runs in `inState()`), world-space movers through a lifted state as `renderFrame()` does for
  vehicles; anchor tags at a world point plus the tile's `dz` and draw them at the tile's alpha.
- **Length:** each extra stage costs about 2–2.5 s (rise 0.5, props 0.5, action 0.5–1, glide 1–1.8); past about 20 s
  the identical drop wobble tires, so vary arrivals. Re-time `TL`, `RISE`, `CK` and the times written as numbers:
  drop starts inside each tile function, wall growth (0.3–0.75 in `tileA()`, 2.35–2.8 in `tileC()`), bridges (1.5,
  2.4, 5.0 in `renderFrame()`), the scanner (4.84–5.14, 5.05), the Scanned pop (5.05–5.35), hub lights (2.9), truck
  and van drops (0.75 and `t < 1.6`, 3.1 and `t < 4`), tag fades (6.2–6.45, 7.95–8.2), title fade (9.2), grid fade
  (9.3), veil (9.8), the numeric cue times in `window.events`, and audio.py's `DUR` and `swell`.
- **Shorter:** from 6 s up, drop stages rather than squeezing beats; minimums: tile rise 0.5 s, wall growth 0.45,
  drop 0.34, hop 0.3, a glide between neighbours 0.9. The shortest signature opening is about 1 s after the 0.25 s
  fade-in (tile up by 0.52, walls by 0.75, first props by 0.9). A title card costs about 2 s: 0.5 s in (settled
  after about 0.45 s by pixel difference), 0.8 s held, then the exit (title fade 0.25, sink 0.45 plus 0.08 per extra
  tile, veil 0.2). Under 6 s keep one or two tiles. Tested 4 s plan (16:9, workshop only): `DUR` 4;
  push `RISE` B, C and D, `TL.hop1` and `TL.truck` past the end (`inState()` skips their invisible tiles, and their
  cues fall past the end); keep the packing; a "Packed" tag pops 2.12–2.44 at world point (4.6, 3.4, 4.6), drawn
  with `ctx.globalAlpha` at the tile's alpha so it sinks and fades with it; `TL.sink` 3.45, grid fade from it, veil
  over the last 0.2 s; delete the literal 1.92 pops and 3.0 clacks, add blips at 2.12 (f 1760) and 2.19 (f 2350),
  make the per-tile sink loop one `bloopdn`; audio.py `DUR` 4.0, `swell` from 1.85. Frames match the end state from
  2.6 s to the exit at 3.45 s; check_audio passes. Camera:

```js
const CK = [[0, 5.5, 4.6, 2.3, 60, 1], [0.95, 5.3, 4.3, 2.25, 64, 0], [1.75, 5.0, 3.9, 2.1, 76, 1],
  [2.1, 5.0, 3.9, 2.1, 76, 1], [2.6, 4.8, 4.8, 2.15, 66, 1], [4, 4.8, 4.8, 2.15, 66, 1]];
```

- **Other formats:** set the canvas and `W`/`H` to 1080 × 1920 (or 1080 × 1080) and the title's x in
  `renderFrame()` to W/2; `iso()` centres itself, and the paper glow's 480 and 1150 px can stay (tested). Chain the
  tiles down the screen with alternating +x and +y steps of 12: `TO` A [0, 0], B [12, 0], C [12, 12], D [24, 12].
  Each tile is then entered across its back edge, so a walled room needs a gate, plus the chain-order sort (Shapes).
  Two tested 9:16 builds:
  - The demo's subject, 10 s, with the ending fix (title at 8.15, y 380; subtitle spacing 4 px, 775 px). B's bend turns
    towards +y: in `tileB()` and `truckPts` use centre y 8.5 and subtract the sine terms, close the road polygon
    through [1.7, 10], [3.3, 10], `roadY(8.5, 10, 2.5)`; the truck ends at (14.5, 15.4). The hub gets a gate: split
    its −y wall and skirting into x 0–1.4 and 3.6–10, sign origin to x 4.6, lights onto the −x wall (u [0, −1, 0],
    from y 6.6), `roadY(0, 2.0, 2.5)` and the bay at y 2.0–5.2 with its lines turned round, the background belt from
    x 4.2 with its stream at 4.5 + ((t · 1.4 + k · 1.35) mod 5.4), fading in over 4.5–5.0. Hop 2 starts at e[1] +
    `BED_U`, turns from π/2 to 0 and lands at (16.1, 16.2, 0.95). Every other point on C and D gains 24 in y: `VAN`
    and `VAN2`, the van drop, hops 3 and 4, both tags, the D `bridge()`; the C bridge grows along y (13.7, 10, 15.3,
    12). The end card spans the width and y 500–1787; frames match the end state from 8.60 s to the exit at 9.4 s
    (25 frames; an exit at 9.5 with `TL.leave` [7.5, 8.0] gives 28; keep the title at 8.15, since 8.05 runs over the
    world); check_audio passes. The hub's −y wall briefly half hides the truck before the gate. Camera:

```js
const CK = [[0, 5, 5, 0.8, 70, 1], [0.95, 4.9, 4.4, 1.2, 74, 0], [1.75, 4.6, 3.4, 1.55, 84, 1], [2.35, 6.6, 5.6, 1.2, 70, 0],
  [3.3, 13.5, 8.5, 1.0, 62, 0], [4.45, 16.6, 16.0, 1.6, 64, 1], [6.05, 19.6, 18.2, 1.6, 64, 0], [7.15, 27.2, 17.0, 1.8, 66, 1],
  [7.45, 27.2, 17.0, 1.8, 66, 1], [8.4, 10.4, 4.4, 0, 39, 1], [10, 10.4, 4.4, 0, 38, 1]];
```

  - A stand-in, 6 s: a 7.6-unit water tower, a filter plant and a house on three tiles, a drop sliding along pipes
    and hopping between them; `CK` stops at (5, 5, 0.3) S 76 for the tower, (17, 5, 0.6) S 68, (18, 18, 3.0) S 72 and
    an end card at (11.15, 5.15, 0), S 40 → 39 (pull 3.75–4.45, title 4.3 at y 380, exit 5.6). The end card spans the
    width and y 512–1542 (these depend on where its tallest object stands; recompute with the formula in
    Composition for yours); frames match the end state from 4.77 s to the exit (26 frames); check_audio passes.
  - A centred line clears the top 15 % and right 12 % at 820 px or less (about 22 mixed-case characters or 17
    capitals at 76 px). Start the title about 80 % into the pull.
  - Pick each shot's `view.z` so the highest top sits near y 300; if the paper above the caption band still exceeds a
    fifth (one tile at S 76 spans about (10.8 + its tallest height) × 76 px), raise S or bring the next tile in
    sooner. Set the last tile low (`view.z` 3 in the stand-in) so its slab fills the caption band. Every 9:16 shot
    shows paper, grid, slabs, three-tone blocks, bevels and shadows. The demo's own row cannot fill 9:16 or 1:1.
  - 1:1 (rendered, title at y 110): tile shots use the 9:16 rows' x and y with the 16:9 demo's z, at S 54–60
    (tested); the demo chain's end card at `view` (11, 5, 0), S 25 → 24.4, spans y 232–1055; the stand-in's at
    (9.9, 3.9, 0), S 31 → 30.2, spans y 228–1029.

## Boundaries
- **Distinct from:** `low-poly` (WebGL perspective camera orbiting a faceted island, sun shading, sky; here 2D
  canvas, parallel projection, fixed light); `voxel` (three.js textured 1-unit cubes, perspective, sandbox
  building); `flat-design` (frontal flat shapes with 45° long shadows, no depth axis); `infographic` (frontal 2D
  icons, counters and a character, lateral pans); `isotype` (rows of pictograms counting quantities);
  `paper-cutout` (layered paper with grain and parallax); `neo-brutalism` (black outlines, hard offset shadows);
  `symmetric-pastel` (frontal centred dollhouse); `blueprint` (line drawing on cyanotype); `technical-cutaway`
  (WebGL perspective model exploded with callout lines; here cutaway rooms in a fixed 2D projection).
- **Poor fit:** charts and numbers (use `data-visualization`), close-up acting and faces (use `clay` or
  `feature-animation-3d`), word-led messages with no place to show (use `kinetic-typography`).
- **Do not:** rotate or tilt the camera, add perspective, outline in black, shade towards black or grey, add
  textures or gradients to blocks, or mix projection angles. Real brands only when the user supplies them.

## Technical notes
- Canvas 2D only: no WebGL, vendored library or render.json; 300 frames render in about 6 s with one worker.
- Deterministic (no random numbers; `GA`, `tileOff`, `local` reset every frame); the determinism test passes.

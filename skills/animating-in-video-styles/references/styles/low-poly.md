# Low-Poly 3D (`low-poly`)

A toy-sized 3D world of flat-coloured triangles, each face one colour with a small seeded tint, lit by one
moving sun with soft shadows over a painted gradient sky: the low-poly diorama look of 2010s indie games and
motion design. Calm, cheerful and tactile; time passes through the light rather than through cuts.

**Reference film:** "Skyhaven", a floating island orbited from noon to dusk: a windmill turns, a striped
hot-air balloon inflates and lifts off, cottage windows light up, then the island shrinks and snaps into a
faceted gem under the title · `styles/low-poly/`

## Signature
- One floating diorama dead centre, about half the frame wide, seen from about 23° above, rising from below with a
  soft overshoot (0–1.5 s) out of a fade from the opening horizon colour (pale sky in the demo).
- Every surface is visibly triangles: one flat colour per face with a slight random tint, so even flat grass reads as
  a mosaic of neighbouring greens (`faceted()`, `tint()`, `flatShading`).
- Saturated toy colours under a warm sun with soft shadows: grass greens, sandy banks, a blue river and a stepped
  waterfall, a brown banded rock underside tapering to a point.
- Chunky props from a few low-segment primitives: six-sided cone pines, icosahedron crowns in greens and autumn
  oranges, a turning windmill, a striped balloon inflating.
- A smooth vertical gradient sky (2D, behind the 3D) with chunky icosahedron clouds drifting, small islets bobbing in
  the distance, and a camera that never stops orbiting.

## Palette
| Role | Colour | In code |
|---|---|---|
| sky zenith at 0 / 7.7 / 10 s | `#56a6f0` → `#2e2f7c` → `#1b1c52` | `PAL` (top) |
| horizon and fog at 0 / 5.9 / 10 s | `#d2efff` → `#ffc79c` → `#7a5aa6` | `PAL` (hor), `scene.fog` |
| sun light at 0 / 7.7 s | `#fff6e8` → `#ff9670` | `PAL` (sun) |
| ambient sky / ground, noon | `#d4ecff` / `#8c8060` | `PAL` (hsky, hgnd), `hemi` |
| grass (one of five) | `#7cc86a` | `GRASS` |
| sand banks / steep rock | `#ecd9a2` / `#a8a296` | `terrainG` |
| underside strata, top → tip | `#a8764e` → `#5a3e36` | `STRATA` |
| river / waterfall blues | `#4bb4e6` / `#5ec4f0`, `#c8f0fc` | `waterG`, `WFC` |
| pine green / trunk | `#2f8a58` / `#7a5238` | `pine()` |
| autumn crowns | `#f0a44a`, `#ec7f4e` | `roundTree()` callers |
| demo props: mill tower / cap, roof, balloon stripes, lit windows | `#f4e8d2` / `#e0584e`, `#3f7fc4`, `#ee5a4c` / `#ffd166`, `0xffc860` | `mill`, `house`, `envelope`, `houseWin` |
| gem table / crown / pavilion | `#8ef0c0` / `#3ed69a` / `#1f9f86` | `gem` |
| title facets | `hsl(${hh},${88 - y * 10}%,${L}%)` | `mosaic` |
| subtitle / rule | `#fff1e4` / `#ffd9a8` | `titleLayer()` |
| fade in (hard-coded to the first `hor` key: change both) / fade out | `rgba(210,239,255,…)`, i.e. `#d2efff` / `rgba(20,18,52,…)` | `window.draw` |

- Colour is one vertex colour per face, picked at build time; light and fog shade it. Materials stay matte (`MAT`,
  roughness 0.92) except water and the gem, so facets read as brightness steps, not highlights.
- The grade is one table keyed in time: `PAL` holds five colours per role at `KEYS` (0, 3.2, 5.9, 7.7, 10 s);
  `palAt()` eases sky, fog, sun, ambient and cloud glow between them (clouds take the fog's horizon colour as
  emissive), `numAt()` the sun and ambient intensity and sun elevation (`SUNI`, `HEMI`, `SUNEL`). Every row holds
  one value per key: add or drop a key in all of them.

## Typography and copy
- One family, Outfit 100–900 (`fonts/Outfit-var-latin.woff2`, `fonts.css`): title `"800 184px 'Outfit'"` in capitals,
  26 px extra per letter, centred; subtitle `"300 44px 'Outfit'"`, lower case, `letterSpacing` 6 px.
- The title is faceted too: `titleLayer()` draws white letters into `txt`, then `source-in` paints the `mosaic`
  canvas (a 26 × 7 grid of jittered quads split into two triangles each, warm creams) inside the glyphs; a blurred
  copy 10 px lower at 35 % reads as a warm glow. Only the small subtitle is flat cream.
- Letters drop 0.055 s apart, 0.5 s each, from 90 px below with `backOut(u, 2.2)` and an alternating ±0.25 rad tilt;
  the subtitle rises 16 px and fades in over 0.6 s while a thin diamond rule grows between the lines.
- The demo's only text is the end card: one invented name (one word, eight letters) and a calm lower-case tagline of
  five to eight words, in `TITLE_TXT` and `SUB_TXT` (preloaded by `window.ready`). The card is optional: add it for a
  name or message; a clip with no words needs none. Mid-film words: a caption function you add with the subtitle's
  font, colour, 6 px spacing and 0.6 s rise-and-fade, up to six words in clear sky, one per beat (in 9:16 about 30
  characters, above the island and below the top 15 %).
- Measured: the title averages 151 px per letter (W is 186 px, I 56; `tot` in `titleLayer()` is the real width), the
  subtitle 25 px per character; a longer name needs a smaller size with the spacing scaled, or a second line you add
  (`titleLayer()` draws one, baseline 230 in `txt`).
- Glyphs: Latin-1 plus Œ œ, curly quotes, en and em dashes, …, •, €, ™ and ↑ ↓ (no ← →); no Central European letters
  (ł ő š ž), Greek, Cyrillic or CJK.

## Texture and finish
- No image textures: the texture is the facet pattern. `tint(hex, amt, rng)` jitters hue by ±0.04·amt, saturation by
  ±0.1·amt and lightness by ±0.08·amt per face; amt is 0.3–0.5 on made things (sails, walls, roofs) and 0.8–1.2 on
  nature (grass, crowns, rock), so nature looks more irregular.
- `jitter(g, amt, rng, keepY)` moves shared vertices together before faceting, so primitives lose their symmetry but
  stay closed: icosahedra and dodecahedra become crowns, rocks and cloud puffs.
- Light: an ambient `THREE.HemisphereLight`, one soft-shadowed sun; `THREE.Fog` reaches only far clouds and islets.
- `drawSky()` paints the 2D layer under the 3D (gradient, 520 px sun glow, twinkling diamond stars from 6.6 s); the
  3D renders into the transparent offscreen `glc`, so an opaque 3D backdrop would hide the sky. Over the 3D come the
  snap flash, `glint()` sparkles, title and fades. No grain, bloom or vignette.
- A large open surface (sea, field, plaza) takes the terrain's jittered rings (`ringStitch()` over the `rings` loop)
  and a random pick (`Math.floor(RNG() * n)`); the water disc's even rings or an `f % n` pick tile into a lattice
  (the demo's disc is regular only because the river hides most of it).
- Moving surfaces stay faceted: `updWater()` ripples the water's vertices so facets flicker in the light; `updFall()`
  steps the waterfall's face colours down through four blues at 9 rows a second, never smoothly.

## Shapes, line and figures
- Everything is a low-segment primitive or hand-built triangle list passed through `faceted()` (3–7-sided cones and
  cylinders, detail-0 polyhedra, a 10-segment `THREE.LatheGeometry` balloon), grouped into parts: trunk plus three
  cones in `pine()`, trunk plus a jittered icosahedron in `roundTree()`. Toy scale: island radius `R` 10, a pine
  about 3 units tall. Terrain: jittered rings stitched by `ringStitch()`, heights from `hTerrain()`.
- The silhouette is a floating spinning top: the top surface over a `STRATA` underside tapering to a point about as
  deep as the radius (tip at −11.8 under radius 10; rings in `LV`). From the camera's 20–23° a shallower base hides
  behind the near rim and the miniature reads as a flat disc, so keep it under any plinth.
- A new object: two to six low-segment primitives, `jitter()` on the organic ones. Colour each part with
  `faceted(geometry, pick)`: `solid(hexes, amt)` for one to four close hexes (amt defaults to 1, the nature level;
  pass 0.3–0.5 for made things) or a pick by face index. Each quad is two triangles: `f % 2` two-tones a side
  diagonally (tower, roof), `f % 4 < 2` alternates quads (sails), a cone's sides show only odd faces; for bands
  around a body pick by the face centre's angle, as `envelope` does. Wrap it with `mesh()` (unfaceted renders black:
  `MAT` reads vertex colours) and add it to `world` (shrinks with the island) or `scene` (stays).
- No people in the demo. A figure, about 0.7 units tall (the windmill's door is 0.75): a low icosahedron head with a
  small wedge nose for a profile, a short neck, a tapered five-sided torso with box shoulders, two-box limbs whose
  parts pivot in groups at the joints, small box hands; never a smooth or rigged mesh.
- Emissive marks light sources (windows, balloon flame) and keeps clouds, waterfall and gem from going dark. A beam
  is an open 4–7-sided `THREE.ConeGeometry` (`openEnded` true) on a `THREE.MeshBasicMaterial` with `vertexColors` and
  `transparent` true, `depthWrite` false, `fog` false and `THREE.DoubleSide`, alpha per face fading away from the
  source in an RGBA colour attribute (without `vertexColors` the alpha is ignored and the beam renders opaque white;
  tested). A halo or flare is a 2D radial gradient after the 3D at `screenOf()`, like `glint()`, no larger than its
  55–70 px glints.

## Composition and camera
- A `THREE.PerspectiveCamera` with a 31° vertical field of view, narrower than three.js's usual 45–75°, which
  flattens perspective a little without being isometric. It orbits at `camAz()` (`A0` plus 0.2 rad per second)
  looking at (0, `camTY()`, 0); clouds at 17–27 units and islets at 44–62 units give depth.
- Axes: the camera sits at (cos `camAz` · D, h, sin `camAz` · D), so at `A0` = −0.35 it is on +x, with +z screen-left
  and −z screen-right. `rotation.y` = θ turns local +x to azimuth −θ and local +z to π/2 − θ, so a front on local +z
  faces the camera with `rotation.y = PI / 2 - FACE`, as the door and windows do; `FACE` is `camAz(3.6)`, so re-aim
  fronts if the orbit changes.
- Moves are slow and continuous: distance 42 → 37 over 0–4 s, height 18 → 13.5 over 0–5 s, then 7.3–8.6 s a push to
  29 and height 5.2 for the gem (`camDist()`, `camH()`). `sunAz()` swings the sun behind the island by 8 s as
  `SUNEL` drops from 52° to 9°.
- End card: gem in the upper half,
  title baseline at y = 830 (`Y0` + 230), subtitle at 922; low clouds sink 7.2–8.8 s to clear it.
- 9:16: the field of view is vertical, so at 31° a portrait frame shows a third of the 16:9 width. Change the
  camera's 31 to about 60 (tested: the island fills four fifths of the width, the middle third of the height);
  pulling back instead sinks the island into the fog unless you scale its 60 and 170 too. Set `Y0` to about `H` ×
  0.55 (baselines near 1286 and 1378, above the bottom 25 % kept for captions). Keep the title's width (`tot`) under
  about 800 px and the subtitle to about 30 characters, out of the right 12 % (WOMEN, 852 px, ends at x 954); six
  average capitals fit at about 150 px, spacing 21. In `updClouds()` sink low clouds 20 units, not 9 (both lines), or
  a far cloud lands behind the subtitle.
- 9:16 when the subject stays (rendered, no gem; each pair is one `easeInOut` over the whole shot, replacing the
  demo's dolly and its 7.3 s push): the demo island at fov 60, `camDist` 40 → 34, `camH` 16 → 12, `camTY` −3.4 → −2.6
  sits in the middle third (top near y 460, tip near 1320). To fill the height: a radius-8.5 plinth, so the camera
  can come closer while the rim still fits the width (scale every radius written as a number with `R`: the trees'
  8.6, the rocks' 2 + 7, `WFP` and the waterfall cloud's 12.4), a tall prop, tip at −12.2, `camDist` 34 → 30, `camH`
  15.5 → 12, `camTY` −2.3 → −1.6; a 9-unit prop then reaches y 300 and the tip 1360–1400 (an end distance of 28.5
  puts the rim against the edges). A title under it needs the tip above its glyph tops (`Y0` + 100): lower `camTY`
  and raise `camH` equally, so the camera tilts without moving (5 units lifted the demo island's tip from 1318 to
  1106); `camTY` alone also drops the camera, which deepens the underside instead. Keep the low-cloud sink at the
  demo's 9 here (rendered): the end card's 20 sinks a far cloud behind the title once the camera tilts down.
- 9:16 clouds and islets (rendered): at fov 60 the islets (y −7 to 0) sit beside the island's top; raise them to y
  14–22 to frame the top corners (placed lower, at −20 to −30, they stay at mid-height beside the island). High
  clouds near the camera loom across the top: raise the positive cloud heights about 1.4× (9–12 to about 13–17).
  `updClouds()` lines the puffs up radially (`g.rotation.y = -a`), so clouds on the camera's side read as rocks
  end-on; `g.rotation.y = PI / 2 - camAz(t)` keeps every cloud side-on.
- 1:1: a field of view of about 40, `Y0` unchanged, and the same deeper cloud sink.

## Motion
- Easing: `sstep()` for light, fade and palette ramps; `easeInOut` (cubic) for camera moves and the sun; `backOut()`
  for every arrival (island rise 1.2, balloon 1.3, gem pop 2.0, title letters 2.2); `easeIn` for the shrink;
  `easeOut` for the subtitle and the gem's spin settling.
- Nothing is ever still: the island rocks slightly, trees sway (`sways`, 0.025 rad, random phases), clouds orbit,
  islets bob, water ripples, the windmill's blades accelerate (`1.2 * t + 0.15 * t * t`).
- Squash and anticipation stay small and physical: the balloon inflates from a flat pancake with overshoot, dips 6 %
  before lift-off, then rises on an accelerating curve with a slight pendulum tilt.
- The demo's snap (`setScene()`): a 5 % swell over 0.35 s, an accelerating spin-and-shrink up to the gem, the gem
  pop, a flash and 44 tetrahedron `shards` in the island's colours.
- Never: cuts, motion blur, whip pans, rubbery squash beyond the balloon's few percent.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.5 | fade in from pale sky | `window.draw` |
| 0–1.5 | island rises into place; orbit and dolly begin | `setScene()`, `camAz`, `camDist` |
| 0.7–1.8 | balloon inflates | `INFLATE`, `updBalloon()` |
| 1.5–3.2 | burner flares (peak at `BURN`; the `burn` cue leads it by 0.2 s), balloon dips, lifts off at `LIFT` with the flame held to 3.2 | `BURN`, `LIFT`, `burnAt` |
| 0–7.7 | noon, golden hour, dusk | `KEYS`, `PAL` |
| 4.0–4.6 | second burner flare (4.3 written in) | `burnAt` |
| 6.15–6.75 | three windows light in turn; stars fade in from 6.6 | `WINDOWS`, `drawSky()` |
| 6.95–8.6 | island swells, spins and shrinks; camera pushes in and levels; gem pops at 7.8 with flash and shards | `SHRINK0`, `SHRINK1`, `camDist`, `GEM`, `shards` |
| 8.25–9.25 | title letters drop in; glints at 8.55 and 9.1; subtitle and rule from 8.65 | `TITLE`, `GLINTS`, `SUB`, `titleLayer()` |
| 9.5–10 | fade to night | `FADE0`, `DUR` |

- One continuous shot: time of day and the orbit carry the structure; each event gets a 0.5–1 s window inside that
  motion, one focus at a time. Reusable: the rise-in, events inside the orbit, lights coming on at dusk, the faceted
  title card, the fade to night. One-off demo content: the balloon sequence and the gem snap.
- The demo's finished card holds only 0.25 s. The last letter lands at `TITLE` + 0.055 × (letters − 1) + 0.5 and the
  subtitle at `SUB` + 0.6; set `FADE0` at least 0.8 s after the later of the two.

## Sound
- audio.py reads `events.json` as a list of cues with a kind `k` and a time `t`. All synthesized: decaying sines for
  `kalimba()`, `marimba()` and `glock()`, detuned sines for `pad()`, swept noise for `whoosh()`. Kinds it does not
  handle are skipped without a message (the demo's own start cue is one), so a misspelt kind gives silence, not an
  error; a `burn` without `d` or a `win` without `i` raises KeyError.
- `rise`: a 1.4 s whoosh. `inflate`: a 1.2 s airy hiss. `burn`: a burner roar (`roar()`) lasting `d` seconds,
  required (0.5–0.6 in the demo). `lift`: a rising sine. `win`: a glockenspiel note; `i` (0, 1 or 2, required) picks
  root, third or fifth. `shrink`: a 0.85 s reverse swell. `gem`: a low thump, a bright D major pad, a five-note
  glockenspiel run and a sparkle. `glint`: two high tinks. `letter`: a marimba note plus a pop; the note climbs
  through eight pitches, then wraps, and the pan moves 0.11 right per cue. From the 14th `letter` cue in a film the
  pan passes 1 and audio.py writes a silent audio.wav while still printing ok: for more letters, clamp the pan or
  reset `let_n` per card. `sub`: a soft whoosh.
- Written at fixed times, not cued: wind for the whole `DUR`; a kalimba arpeggio (`ARP` over `CH`: D, G, Bm, A at 96
  bpm) with pads and bass, chords at 0, 2.5, 5.0 and 6.9 s, stopping at a written-in 7.7 s just before `gem` resolves
  it to D (no cue is looked up by name, but without `gem` the music ends unresolved); windmill whooshes from the
  blade angle (`ang` repeats the formula in anim.html) until 7.1 s (delete that loop with the windmill).
- Music and bright cues share the `wet` bus (2 s room reverb); the mix is tanh-limited and fades over 0.7 s.
- Re-use cues by meaning: `rise` arrivals, `burn`/`lift` take-offs, `win` lights, `shrink` + `gem` the change,
  `glint`, `letter` and `sub` the card. Re-time the fixed parts above and the softer kalimba after 5 s.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| facet kit and maths | `anim.html` → `faceted()`, `tint()`, `jitter()`, `solid()`, `mesh()`, `mulberry32()`, `backOut()` | `faceted(g, pick)`: pick gets face index, centre and normal, returns a colour; `backOut(x, s)`: s sets the overshoot | as is |
| renderer, lights, fog | `anim.html` → `renderer`, `sun`, `hemi`, `scene.fog` | shadow camera ±16 units | as is; widen for a bigger subject |
| grade, sky, sun glow, stars | `PAL`, `KEYS`, `palAt()`, `numAt()`, `drawSky()`, `sunMesh` | five keys per role | adapt: key times and colours |
| camera and sun path | `camAz`, `camDist`, `camH`, `camTY`, `sunAz` | eased lerps between key times | adapt |
| island, water, waterfall | `hTerrain()`, `ringStitch()`, `buildPolys()`, `updWater()`, `updFall()` | `buildPolys(verts, tris, pick, up)`: `up` true turns faces upward (a top surface), false outward from the axis (a skirt) | adapt as a plinth, or replace |
| trees, rocks, flowers | `pine()`, `roundTree()`, `avoid` | `pine(x, z, s)`, `roundTree(x, z, s, hex)` | as is on the island; they stand on `ground()` (= `hTerrain()`), so on a new plinth make `ground()` return its height. Rocks and flowers are the two loops after the tree placement |
| clouds and islets | `cloud()`, `islet()`, `updClouds()` | `cloud(ang, rad, y, s, seed)`: a cloud with y < 0 is low and sinks from 7.2 s | as is in 16:9; re-place in 9:16 (Composition) |
| windmill, cottage, balloon | `mill`, `house`, `balloon`, `updBalloon()` | | replace; models for new props |
| gem, its lights, shards, glints | `gem`, `gemKey`, `shards`, `glint()`, `screenOf()` | `GEM_R`, `GEM_C`; `glint(x, y, r, a)` | adapt: any faceted end icon |
| title | `anim.html` → `titleLayer()`, `mosaic` | `TITLE_TXT`, `SUB_TXT`, `Y0` | adapt: copy, position |
| timeline and cues | `INFLATE`, `LIFT`, `WINDOWS`, `SHRINK0`, `GEM`, `TITLE`, `window.events` | | replace |

## Adapting
- **Style vs demo plot:** the style is the kit: per-face colour from `faceted()`/`tint()` on matte `MAT` and
  low-segment primitives with `jitter()`; the grade keyed in time over the 2D gradient sky, with sun glow and diamond
  stars; a floating miniature over a tapering `STRATA` underside; chunky clouds and bobbing islets; the orbit at
  about 0.2 rad/s, `backOut()` arrivals and the ambient motion in Motion; `titleLayer()`'s faceted letters for any
  title. The plot is yours to replace: windmill, cottage, balloon, the island-to-gem snap with its flash and shards,
  the card's timing. The gem snap is one ending, for revealing a name, logo or product; when the brief has its own
  resolution (a boat docking, a lamp lit), end on that, held. A change of state counts as the transformation: lights
  coming on, day turning to night, a prop arriving or lifting off. To drop the snap and card, push `SHRINK0`,
  `SHRINK1`, `GEM`, `TITLE` and `SUB` past `DUR` (their cues then fall outside audio.py's track) rather than deleting
  `gem` or `shards`, which `setScene()` and `window.draw` use; with no card, also remove the 7.2 s cloud sink, or the
  waterfall's cloud falls away.
- **New subject:** a self-contained miniature on a plinth (an island, a small planet, a product on its rock, a city
  block) at the origin, about 10 units in radius, so camera, shadow and fog numbers still fit. Pack the top as the
  demo does (36 trees, rocks, flowers, three props), keep the plinth no larger than the action, and give an
  abstract idea a physical diorama metaphor.
- **Logos and products:** a user's logo or product shot goes on the 2D end card, drawn into `octx` after the 3D like
  the title, from a data URI (contract.md); never map it onto a mesh. Model the product from primitives.
- **Traps:** `RNG` is one stream consumed at build time, so adding or reordering objects reshuffles every later
  colour and position. Give a new object its own `mulberry32(seed)` and pass it as the last argument of `tint()` and
  `jitter()`, as `cloud()` and `islet()` do; `solid()` always draws from `RNG`, so a seeded part's pick is
  `() => tint(hex, amt, r)`.
- **Length:** the orbit, grade and ambient motion stretch by themselves: spread `KEYS`, and slow `camAz` so the orbit
  stays under half a turn (past it the camera reaches the islets, placed opposite the start at `A0` + π, and sees the
  backs of fronts aimed at `camAz(3.6)`). Add an event every 1.5–3 s (a prop arriving with `backOut()`, lights coming
  on). Move `SHRINK0` through `FADE0`, `DUR`, `GLINTS` and `WINDOWS`, plus the times written as numbers: the 7.3 s
  push in `camDist()`, `camH()` and `camTY()`; the 8 s swing and `camAz(7.5)` in `sunAz()`; the 7.2 s cloud sink in
  `updClouds()` (two lines); the 6.6–8.4 s star fade in `drawSky()`; the 4–8 s sun-disc growth in `setScene()`; the
  4.3 flare in `burnAt` and the `burn` cue at 4.1. One orbit gets monotonous past about 20 s: add a push-in to a
  detail or a second subject. In audio.py set `DUR` and re-time as listed in Sound.
- **Shorter (3–6 s):** compress `KEYS` so the grade still moves (golden hour to night, say). Keep `camAz` at 0.2
  rad/s: four seconds turn only 0.8 rad, and anything slower reads as a still. Rise in 0.8–1.2 s from the same −7
  units, then one or two events. The title card costs about 2.3 s (Film grammar's landing times plus the 0.8 s hold
  and 0.5 s fade): under about 6 s, run it over the last action or leave it out. Move the times written as numbers
  listed under Length to the new end (otherwise a 4 s clip never reaches the stars at 6.6 s and gets half the sun's
  swing) and set audio.py's `DUR`.
- **Other formats:** Composition gives rendered 9:16 values (end card, a subject that stays, clouds and islets) and
  1:1; move the 2D pixels in Technical notes.

## Boundaries
- **Distinct from:** `cel-shaded-3d` (ink outlines, toon bands), `voxel` (textured cubes), `origami` (folded paper),
  `isometric` (flat 2D vector), `inflated-3d` (smooth puffy gloss), `feature-animation-3d` (smooth PBR characters).
- **Poor fit:** charts and numbers (use `data-visualization` or `infographic`), character acting and faces (use
  `clay` or `feature-animation-3d`), fast cutting to a beat (use `kinetic-typography`).
- **Do not:** smooth the shading, add image textures or outlines, or raise segment counts: the style dies when the
  facets disappear. Keep each part's tint inside one hue family; rainbow jitter reads as noise.

## Technical notes
- `render.json` sets `"gpu": "full"` and `"schedule": "contiguous"`, a leftover: frames are a pure function of `t`.
- Keep `vendor/three.min.js` (r159): r160 removed the global `THREE` build the plain script tag loads. The
  intensities (sun 2.3, ambient 1.35) assume physical lighting, the default since r155 (`useLegacyLights` is never
  set); values from older examples look about π times too dark.
- Apple silicon with Metal: 60 frames in 5.5 s, about 30 s for 10 s of film. Without a GPU the 2048 shadow map and
  antialiasing make it much slower; draft with a smaller `sun.shadow.mapSize`.
- Only the canvas attributes and `W`/`H` hold 1920 × 1080; the 2D layer uses absolute pixels (`Y0` = 600, the 400 px
  `txt` and `mosaic` canvases, 184 px title, 520 px glow, 700 px flash): see Composition for 9:16.

# Voxel Blocks (`voxel`)

A sandbox building game seen through its own screen: a floating island made of one-metre cubes with 16 × 16
pixel textures, real sun shadows and soft corner shading, overlaid with the game's HUD. The film is a
tutorial played out in the world: each step is shown by a block being mined or placed, with a satisfying pop
and a material-specific knock. Calm, cosy and methodical, ending at sunset on the finished build.

**Reference film:** a five-step tutorial on a floating island: mine a mossy boulder, lay a cobblestone floor,
raise log-and-plank walls with glass windows, step a clay roof, light two lanterns at dusk, then pull back to
the title "BLOCK BY BLOCK" · `styles/voxel/`

## Signature
- A floating island of textured unit cubes over a sea of flat, blocky clouds, seen wide in the first second
  and resolving out of big square pixels over near-black (`fades()`).
- Hard texels: every face is a 16 × 16 tile magnified with `THREE.NearestFilter`, darkened in corners and
  under overhangs by baked per-vertex ambient occlusion, under one sun with crisp shadows.
- The game HUD by 0.8 s: a dark step card top left ("STEP 1 OF 5" in gold over the instruction typing on),
  a seven-slot hotbar with isometric block icons at the bottom centre, a "BLOCKS 0/140" counter top right.
- A block under a thin dark selection outline being worked on: the boulder cracks in stages with pickaxe
  ticks and bursts into tumbling cube debris at 2.02 s.

## Palette
| Role | Colour | In code |
|---|---|---|
| grass top (one of six) | `#5f9d37` | `GRASS` |
| dirt | `#8a6241` | `DIRT` |
| stone | `#7f7f7f` | `STONE` |
| cobble mortar | `#4e4e4e` | `cobbleLike()` |
| oak planks | `#b3894f` | `paint('planks', …)` |
| log bark | `#6b4e2d` | `paint('log_side', …)` |
| clay roof | `#a4493a` | `paint('roof', …)` |
| leaves | `#437f2d` | `paint('leaves', …)` |
| sand banks | `#dccf96` | `paint('sand', …)` |
| water | `#3b6fd6` | `paint('water', …)` |
| lantern glow | `#ffd36b` | `paint('lantern', …)` |
| sky zenith, day | `vec3(.33,.55,.95)` | `skyMat` fragment shader |
| horizon fog, day → dusk | `#b8d4f7` → `#e89a78` | `setScene()` |
| selection outline | `0x141418` | `olMat` |
| HUD panel | `rgba(16,14,26,0.72)` | `hud()` |
| HUD gold (labels, pips) | `#ffd75e` | `hud()` |
| title face / extrusion | `#ffe7a3` / `#6b3a2a` | `title()` |
| fade-to-black | `rgba(13,11,20,${a})` | `fades()` |

- Each material is a small palette of four to six close shades picked at random per texel by a seeded
  `mulberry32()`, plus a darker seam or speck colour. Never a gradient inside a tile.
- Output is linear (`THREE.ColorManagement.enabled = false`, `THREE.LinearSRGBColorSpace`), so a hex in a tile
  palette lands on screen close to as written, before light and fog.
- The whole grade moves from day to sunset with one number, `sunsetU(t)`: fog, sun, hemisphere, fill and cloud
  colours all lerp between a day and a dusk hex in `setScene()`.

## Typography and copy
- One face, Silkscreen 700 (`fonts/Silkscreen-700-latin.woff2`, declared in `fonts.css`), used at
  `"700 38px 'Silkscreen'"` for instructions, 26 px for labels, 28 px for the item name, 58 px for the counter,
  128 px for the title and 40 px for the subtitle.
- Silkscreen draws lower case as full-height capitals, so sentence-case copy ("Lay a cobblestone floor") reads
  as all caps; labels are written in upper case in the code ("STEP 2 OF 5", "BLOCKS").
- HUD text and the subtitle go through `pixelText()`: drawn twice, a hard shadow 3–5 px down-right, never a
  blur. Title letters get an eight-step diagonal extrusion (`#6b3a2a`, darker at the tail) and a paler top band.
- Instructions type on letter by letter over 0.4 s, starting 0.08 s after the card slides in.
- Voice: short imperative tutorial steps of three to five words ("Clear the ground", "Step the roof", "Light it
  before dusk"); item names in Title Case ("Oak Planks", "Clay Shingles"); a two-to-three-word title in caps.
- Letters advance about 0.875 em: at 38 px a step card holds about 30 characters before it reaches the block
  counter (the demo's longest is 24, "Log corners, plank walls"); at 128 px the title holds about 15 characters
  across 1920 px and 8 across 1080. Split longer copy into more steps, never a smaller size.
- Glyphs: Latin-1 plus Œ œ, curly quotes, en and em dashes, € and ™. No Central European letters (ł, ő),
  Greek, Cyrillic or CJK.

## Texture and finish
- Block textures: `paint(name, fn)` fills a 16 × 16 pixel array once at load; tiles are stamped 3 × 3 into
  32 px cells of the atlas `atlasCv` (8 px of wrapped padding) so mipmaps never bleed. Magnified texels stay
  square; distant faces use `THREE.LinearMipmapLinearFilter` and anisotropy.
- Ambient occlusion: `buildTerrain()` gives each face vertex one of four levels (`AOK`, 0.40 to 1.0) from its
  three neighbours, times a per-face shade (`FACES`: top 1.0, sides 0.84 and 0.92, bottom 0.62), baked into
  vertex colours. Corners and the foot of every wall darken; this is what makes it read as a voxel engine.
- Leaves and glass have transparent texels cut by `alphaTest: 0.5`, so trees show sky through their canopy.
- One sun with a 4096 × 4096 PCF shadow map, a hemisphere ambient, a weak blue fill from below, and linear fog
  (70 to 190 units) tinted to the horizon colour.
- Light sources glow as stepped square halos (`haloTex`, additive sprites), not soft bloom.
- Water scrolls in whole texels (`Math.floor(t * 20) / 16`) so it flows like pixel art, not smoothly.
- No post-processing: no bloom, grain, vignette or lens effects.

## Shapes, line and figures
- Every solid is an axis-aligned unit cube on an integer grid, never rotated or rounded: terrain, trees (log
  trunks, leaf blobs with corners randomly clipped), the house, the boulder. Particles are small cubes too.
- Clouds are 4 × 1.4 × 4 slabs on a grid (`cloudGeo()`); the sun is a square in the sky shader. Flowers
  and tall grass are two crossed quads (`buildPlants()`); water and the waterfall are flat textured quads.
- A new object is a set of blocks: give each material a 16 × 16 tile from a four-to-six-shade palette with
  a darker seam, list its six face tiles in `FACETILES` (BoxGeometry order: +x, −x, +y, −y, +z, −z) and place
  it on whole coordinates. Tools and items in the HUD are 16 × 16 pixel sprites (the pickaxe is a character
  map in `paint('pickaxe', …)`).
- The demo has no people. A character must be built from boxes too (cube head, box torso and limbs) with
  pixel-textured faces; never a smooth mesh.

## Composition and camera
- A perspective camera (vertical field of view 42°) orbits a target: `CAM` rows hold the time, azimuth,
  elevation, radius and target point, and `camAt(t)` interpolates them with a cardinal spline, the radius in
  log space so dollies feel even.
- Shots: the whole island wide (radius 44), a dolly to the work site by 1.3 s (radius 11.5), a slow orbit at
  radius 18–19 during the build, a pull-back to radius 62 at low elevation for the title.
- The work site sits at the centre, slightly low, framed by the HUD: card top left at (72, 70), counter
  right-aligned at `W - 76`, hotbar centred at `H - 150` with the item name above it.
- Every hit and the burst add a small vertical shake (`kick` in `setScene()`).
- 9:16: the field of view is vertical, so a portrait frame shows under a third of the 16:9 width; let the
  island fill the height or raise the wide-shot `CAM` radii about 3×. The 680 px hotbar fits, but at `H - 150`
  it sits in the social caption zone: move it to about `H * 0.72`, stack the counter under the card, and keep
  the title to 8 characters a line. 1:1: same HUD, wide-shot radii about 1.8×.

## Motion
- Easing: `backOut(x, s)` for every pop (overshoot 2.6 for blocks, 2.4 for title letters, 1.8 for cards),
  `easeOut` for dust and the subtitle rise, `sstep(a, b, x)` for every fade and light ramp.
- Placing a block (`placeAnim(b, t)`): 0.24 s from scale 0.35 with overshoot while dropping 0.55 units into
  place, then four dust puffs ring out from its base 0.12 s later.
- Builds are staggered at a steady rate, 0.02–0.031 s per block, in an order that reads as work: the floor
  sweeps diagonally, walls go round the ring by angle, the roof rises layer by layer.
- Mining: six hits 0.17 s apart, each squashing the boulder to 94 % and advancing one of six crack overlays
  (`CRACK`); the burst throws 34 cube fragments under gravity (`ballistic()`) that land and shrink away.
- Ambient motion never stops: clouds drift, water scrolls in texel steps, spray and mist particles loop.
- HUD: the step card slides in from the left with overshoot and fades out; title letters drop in one by one
  0.04 s apart, their offset snapped to 6 px steps so they move like pixel sprites.
- Never: smooth spins of blocks, squash and stretch beyond the placement pop and hit pulse, sub-texel
  scrolling, soft dissolves (transitions are pixel mosaics).

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.75 | mosaic resolves over near-black on the wide island | `fades()` |
| 0–1.3 | dolly from the island to the boulder | `CAM` |
| 0.45 | step 1 card, pickaxe selected | `STEPS`, `slotAt()` |
| 1.0–1.85 | six pickaxe hits, crack stages | `HIT0`, `HITS`, `HIT_DT` |
| 2.02 | boulder bursts into debris | `BREAK`, `DEBRIS` |
| 2.3–3.05 | 25 cobblestone floor blocks | `F0`, `HB` |
| 3.2–4.55 | walls: log corners, planks, glass | `W0` |
| 4.6–8.6 | day turns to sunset | `sunsetU()` |
| 4.75–6.1 | stepped clay roof | `R0` |
| 6.25–6.55 | lamp inside, two lanterns, halos | `LAMP_IN`, `LANT` |
| 7.25–7.75 | pull-back; HUD fades out | `PULL`, `hud()` |
| 8.3–9.0 | title letters drop, subtitle box | `TITLE`, `title()` |
| 9.5–9.95 | mosaic melt to near-black | `FADE`, `fades()` |

- One step per idea, about 1–1.5 s each: card in, the action shown by blocks appearing or breaking, the hotbar
  selection changing with the material, the counter ticking up.
- The day-to-sunset ramp spans the build, so the mood marks progress without a cut. Reusable: the mosaics,
  step card, mining, staggered build, lights-on beat, pull-back and dropping title; the island, house and
  five steps are demo content.

## Sound
- audio.py reads `events.json` as a list of cues with a kind `k` and a time `t`; one kind also carries the
  block type `m`.
- `card`: two square-wave UI blips. `hit`: a pickaxe tick (`pick_hit()`). `break`: a gravel crunch of 26
  grains (`crunch()`) and a low blip.
- `place`: a knock per material (`thock()`) chosen by `m`: `cobble` and `mossy` a stone thud, `planks` and
  `log` a wooden knock, `glass` a high ping, `roof` a clay tick; any other value gets the lantern's metal clink.
  A new material needs its own branch in `thock()`.
- `glow`: a warm pad and a piano arpeggio. `pull`: a noise sweep (`whoosh()`). `letter`: rising blips on a
  major scale. `sub`: two piano notes. `end`: the closing chord.
- The bed is not cued: wind, a waterfall hiss that swells after 7.3 s, birdsong (`chirp()`) until 5.1 s,
  crickets (`cricket()`) from 6.3 s, and a felt-piano theme (`piano()`, Fmaj7, Am7, Cmaj7, G at 72 bpm) with
  slow pads, all written at fixed times in audio.py.
- Music goes through a small room reverb; the mix is soft-limited and fades out over the last 0.5 s.
- A new scene emits `card` per step, `place` with `m` for every block, `hit` and `break` for removal, `glow`
  when lights come on, `pull` for the reveal, `letter` per title letter, `sub` and `end`.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| tile painter | `anim.html` → `paint()` | `paint(name, fn)`: fn gets a texel setter, a seeded random and a getter | as is; add tiles |
| atlas | `anim.html` → `tileUV()` | `TILE_NAMES`, `ACOLS`, `AROWS`, `CELL` (32 cells, 17 used) | adapt: append names |
| block types | `anim.html` → `FACETILES` | six face tiles per type | adapt: add types |
| voxel store and mesher | `anim.html` → `setV()`, `buildTerrain()` | `setV(x, y, z, type)`; merges visible faces of `vox` with AO | as is |
| island shape | `anim.html` → `heightAt()`, `inIsland()`, `Rth` | `HILL`, `HOUSE`, `H0` | adapt |
| trees and plants | `TREES`, `buildPlants()` | rows of x, z and trunk height | adapt |
| animated blocks | `anim.html` → `blockGeo()`, `placeAnim()` | `blockGeo(type)`; `placeAnim(b, t)` pops at `b.t` | as is |
| build list | `HB`, `LANTERNS` | entries with x, y, z, type and placement time | replace |
| mining and outline | `CRACK`, `boulder`, `DEBRIS`, `ballistic()`, `outline` | `ballistic(o, v, dt, g, floor)` | adapt: target |
| water and waterfall | `waterTex()`, `streamTex`, `fallTex` | `SX0`, `SZ`, `FALL_BOT` | adapt or drop |
| clouds and sky | `anim.html` → `cloudGeo()`, `skyMat` | `cloudGeo(y0, seed, thresh)`; uniforms `uSun`, `uS` | as is |
| light, grade, lanterns | `anim.html` → `setScene()`, `haloTex` | `SUN_DAY`, `SUN_SET`, `sunsetU()`, `glowU()`, `halos` | adapt: times |
| particles | `anim.html` → `pushP()` | `pushP(x, y, z, sz, col, rot)`, at most `PMAX` per frame | as is |
| camera | `anim.html` → `camAt()` | `CAM` rows: time, azimuth, elevation, radius, target | adapt: new keys |
| HUD | `anim.html` → `hud()`, `pixelText()`, `isoIcon()` | `pixelText(c, txt, x, y, col, sh, shCol)`; `isoIcon(c, cx, cy, s, type)` | as is |
| hotbar and steps | `SLOTS`, `slotAt()`, `STEPS` | | replace |
| title | `anim.html` → `title()` | `TITLE_TXT`, `SUB_TXT` | adapt: copy |
| mosaic in and out | `anim.html` → `fades()` | `FADE` | as is; fix end times |
| timeline and cues | `HIT0`, `F0`, `W0`, `R0`, `PULL`, `TITLE`, `window.events()` | | replace |

## Adapting
- **New subject:** keep the tile painter, atlas, mesher with AO, lights, sky, clouds, HUD and mosaic fades;
  replace the island terrain, `HB`, `STEPS`, `SLOTS` and the title. Build the subject from blocks on whole
  coordinates and show each step as blocks being placed or removed; a concept with no physical form needs a
  blocky metaphor (a machine, a farm, a bridge), not floating text.
- **Traps:** a new block type needs a tile in `TILE_NAMES`, a row in `FACETILES`, an entry in the `GEO` list and
  a `thock()` branch; the counter's total and the subtitle read `TOTAL`, so they update by themselves.
- **Length:** add steps rather than slowing them; keep each to 1–1.5 s. Move `FADE`, the last `CAM` key, the
  `sunsetU()` ramp and the two hard-coded end times inside `fades()` (9.92 and 9.95); in audio.py retime the
  piano `bars`, the melody, the pads, birds and crickets, and set `DUR`. Each placed block is its own mesh (140
  in the demo); for thousands of static blocks write them into `vox` and mesh them with `buildTerrain()`.
- **Other formats:** the scene recomposes through `CAM` alone; the HUD needs the moves listed in Composition.

## Boundaries
- **Distinct from:** `low-poly` (smooth faceted shapes, flat shading, no textures), `isometric` (a clean
  orthographic model world), `pixel-art` and `nes-8bit` (2D side-on games). Here the world is 3D, textured and
  shadowed, and everything is a cube.
- **Poor fit:** abstract numbers and charts (use `data-visualization`), character drama and faces (use `clay`),
  long spoken arguments (use `whiteboard`).
- **Do not:** this style is inspired by Minecraft: take the voxel language only, never its logo, its
  characters or mobs (Steve, creepers), its Mojang-style font, its actual textures or its menu art; do not imply
  it is the game or endorsed by it.

## Technical notes
- `render.json` sets `"gpu": "full"` and `"schedule": "contiguous"`. Frames are a pure function of `t`
  anyway: the stills determinism test gives byte-identical frames on the untouched project.
- three.js r159 is vendored at `vendor/three.min.js` and loaded before the script; the code uses r159 APIs
  (`renderer.useLegacyLights`), so do not swap the version.
- three.js renders into an offscreen `glc`, copied onto the canvas `c`, where the HUD, title and fades are
  drawn in 2D. `window.ready` loads the font for the film's strings (add new copy to its `document.fonts.load`
  calls) and renders one frame to compile shaders.
- Render time on an Apple-silicon Mac with Metal: 60 frames in 3.6 s, so about 20 s for 10 s of film. Without a
  GPU, the 4096 shadow map and 900 particles make it much slower; draft with `sun.shadow.mapSize` at 2048.
- Only the canvas attributes are hard-coded at 1920 × 1080; everything else uses `W` and `H`, but the HUD's
  pixel offsets (72, 70, 76, 150) are absolute.

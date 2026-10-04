# Cel-Shaded 3D (`cel-shaded-3d`)

Real-time 3D drawn like a cartoon: hard light bands with coloured shadows, a crisp rim and thick ink outlines on
toy-like props, under a painted sky over a stylized sea. It draws on toon-shaded adventure games of the Wind Waker
and anime-game kind. Sunny, warm and playful; time passes through the light, not through cuts.

**Reference film:** an iris opens on an island harbour at noon, a gust fills a sailboat's sails, the sun sets
while the camera glides round, windows and the lighthouse lamp switch on, "HARBOUR LIGHTS" pops in and an iris
closes on the lamp · `styles/cel-shaded-3d/`

## Signature
- An iris in the ink colour opens from the centre over 0.95 s on a toy world in a banded sea (the demo's island),
  seen from about 15° above, with the camera already moving on frame 0 (`iris()`, `camAt`).
- Every solid is lit in hard bands: lit, mid and a violet-blue shadow, never black, with a thin bright rim on
  grazing edges and fine diagonal hatching only on faces turned well away from the sun; cast shadows are hard and
  fall blue on the water (`toon()` in `COMMON_FS`).
- Thick navy ink outlines around every solid prop (inverted hulls: `hullMat`, `hullThin`) plus finer ink at
  creases, silhouettes and depth breaks (`postMat`), and a soft vignette.
- Cartoon surroundings: a painted sky gradient with flat cream cloud puffs edged in ink, a sea of flat colour bands
  with breathing white foam rings round the shore and drifting crescents, small ambient life (demo: white gulls with
  dark wingtips).
- Chunky, slightly crooked primitive props in saturated toy colours (demo: a striped lighthouse, leaning cottages
  with prism roofs, segmented palms, a red sailboat) and an early event with white anime wind streaks (demo: the
  sails fill on a spring at 1.55 s).

## Palette
| Role | Colour | In code |
|---|---|---|
| Sky zenith at 0 / 3.8 / 6.6 / 9.3 s | `#3d8ee6` → `#5b86d6` → `#4b4ca0` → `#1e2262` | `PAL` (top) |
| Horizon, fog, far sea; deep sea / shallows | `#bfe6ff` → `#ffd6a0` → `#ff9064` → `#b85a90`; `#1b86c4` → `#232e72` / `#3fd6d0` → `#4c6aa8` | `PAL` (hor, deep, shal) |
| Lit band; mid band | `#fff7e6` → `#ffe0a8` → `#ffa878` → `#d58ac4`; `#d4d8f0` → `#ecc2b0` → `#d98b98` → `#9a72b4` | `PAL` (light, mid) |
| Shadow band (also shadows on the sea) | `#8f8ad0` → `#a07ec0` → `#7a5fae` → `#4e4290` | `PAL` (shadow) |
| Rim; sun disc and halos | `#ffffff` → `#fff0c0` → `#ffc690` → `#f39ad0`; `#fffbe8` → `#fff2b8` → `#ffd97a` → `#ffb070` | `PAL` (rim, sun), `SKY_FS` |
| Ink: outlines, lines, iris, title strokes | `#1c2138` → `#221c36` → `#241733` → `#17122b` | `PAL` (ink), `uInk` |
| Island sand, grass, rock; lighthouse stripes | `vec3(.93,.80,.55)`, `vec3(.45,.78,.30)`, `vec3(.66,.58,.54)`; `vec3(.97,.95,.92)`, `vec3(.88,.20,.22)` | `TOON_FS` (ISLAND, STRIPES) |
| Props: wood, leaves, red roof, metal, window glass | `#b77a4a`, `#3fae4a`, `#e04638`, `#2c3148`, `#2d3f73` | `M`, lighthouse block |
| Cottage walls; roofs besides the red | `#d7f3cf`, `#fff0da`, `#ffd3dc`, `#ffe79a`, `#c6e8ff`; `#2f6fd0`, `#2aa39a`, `#ef8a2e`, `#7a55c8` | `HOUSES` |
| Boat hull, sails; gull wingtips; lit windows, lantern, beam | `#e8453a`, `#fff8ec`, `#ffd25a`; `#3a3d52`; `#ffd56a`, `#ffe27a`, `#fff0a8` | `boat`, `sailMat`, `sailMat2`, `gulls`, `toonMat()` emisC, `beamMat` |
| Title fill (hard split at 52 %), subtitle; wind streaks | `#fff7e2`, `#ffc56e` → `#ff9a55`, `#fff3e6`; `rgba(255,255,255,0.92)` | `title()`, `wind()` |

- A material's colour is its base hex times the grade's light, mid or shadow tone, so props follow the time of day by
  themselves; keep bases mid to light (the darkest is the `#2c3148` metal), as shadow turns a dark base to mud.
  Emission (`uEmis`) replaces the toon colour with `uEmisC`, flat.
- The grade: `PAL` holds four colours per role at `KEYS` (0, 3.8, 6.6, 9.3 s), eased by `palAt()` with `sstep()`.

## Typography and copy
- One face, Lilita One (`fonts/LilitaOne-400-latin.woff2`, `fonts.css`), preloaded with `TITLE_TXT` and `SUB_TXT`.
  Title: 156 px capitals, one word per line (`TITLE_TXT` split on spaces), 146 px apart, each 34 px further right;
  each letter a cel sticker (ink copy offset 7, 11 px, 17 px ink stroke, fill split hard at 52 % from cream to orange)
  popping 0.05 s apart with `backOut()` (2.2, peaking at 1.15× after about 0.18 s), its alternating ±0.25 rad tilt
  settling over 0.5 s, then a 0.025 rad idle wobble.
- Subtitle: 46 px, 10 px ink stroke, cream fill, two lines 54 px apart, rising 22 px and fading in over 0.45 s from
  `TITLE` + 0.75. Its lines are literals in `title()`; `SUB_TXT` only preloads glyphs, so change both. The `letter`
  cues strip only the first space of `TITLE_TXT`: strip every space, so a three-word title gets no extra cue.
- Copy: a cheerful one- or two-word name, a warm sentence-case tagline of four to six words. Widths at 156 px: 91 px a
  letter in "HARBOUR LIGHTS", about 95 px for unknown copy (M 141, W 149, I 67), so a line holds about nine capitals,
  eight with W or M, one fewer indented: in 16:9 before the end card's lighthouse, in 9:16 before the right 12 % band
  ("WATERFRONT" crosses x 950, rendered). The subtitle, about 21 px a character, takes about 40 a line.
- Glyphs: Latin-1 (no non-breaking space or macron), Œ œ, curly quotes, en and em dashes, …, •, €, ™, −; no arrows,
  Central European letters (ł ő š ž), Greek, Cyrillic or CJK.

## Texture and finish
- No image textures. Shaders make the pattern: sand, two-tone grass and rock by height, slope and noise (`ISLAND`),
  2.3-unit stripes (`STRIPES`), hatching (a 7.5 px screen diagonal darkening 13 % times `uHatch`) where a surface
  faces away from the light by more than about 0.3, and a 28 % vignette in `postMat`.
- Ink is two layers: `prop()` adds an inverted hull on averaged normals at constant pixel width, 3.4 px (`hullMat`)
  or 2.2 px (`hullThin`), scaled 0.55–1.5× by depth around 38 units; `postMat` adds 1–2 px lines from a Laplacian of
  inverse depth and a normal Sobel (`ndMat` pass), fading out 120–230 units away. `renderGL()` runs a 2048 px hard
  shadow map (`SHADOW_N`), a 4× MSAA colour pass, the `ndMat` pass and the composite; the 2D overlay draws on top.
- Sky (`SKY_FS`): gradient with a faint band, a flat sun disc with two stepped halos, stars from 7.6 s. Clouds
  (`CLOUD` define): mostly lit, one mid band, strong rim, no hatching. The sea (`WATER_FS`) adds a wake from `uBoat`,
  blue cast shadows, a broken glitter path. Light falls off in steps: four in the beam, three halo rings.

## Shapes, line and figures
- Low-to-medium primitives (8–28 sides) bent by `deform()` so nothing is quite straight: leaning, bulging boxes under
  wavy prism roofs and crooked chimneys; a tapered tower; palms of seven alternating brown cylinders with serrated
  `frondGeo()` fronds; dodecahedron rocks; a half-sphere pulled into a hull. Scale: island radius 12, lighthouse 12
  units (`TOWER_H` 8.6 plus lantern and roof), cottages 2, palms 4.2–5.5, boat 5 long.
- A new object: two to eight primitives, each `prop(geo, toonMat(hex, o))`, deformed a little, `thin` hulls on small
  parts; `rim` 0.2–1.2 (low on flat walls, high on round or backlit forms), `hatch` 0 on soft things (clouds,
  smoke). Geometry rebuilt per frame (sails, flag) or hand-built sheets (fronds, wings) take `hull: false` and
  `THREE.DoubleSide` and rely on `postMat` lines, because `outNormals()` runs once. Lights are emissive materials
  switched by time (`userData.win`, `userData.lamp`), a beam an additive open cone (`beamMat`), a glow `haloMat`.
- No people in the demo. A tested figure, each part a `prop()` (`thin` on the limbs): a sphere head (radius 0.32 at
  height 1.62), a cylinder torso tapering 0.32 to 0.22 over 0.75, capsule legs (radius 0.1, 0.55 long) and arms (0.08,
  0.5). At 1.9 units (cottage height, 70–80 px on screen) it reads as a toy peg person with bands, hatching and ink;
  face, hands and acting need a close camera the style never uses: use `clay` or the feature-animation-3d style, or
  tell the story with objects (review.md).

## Composition and camera
- One `THREE.PerspectiveCamera`, 34° vertical field of view, gliding the whole film: `camAt` moves from azimuth 16° to
  72°, radius 46 to 41 and height 13.5 to 6.8 round a drifting target; azimuth, radius and target follow 30 % linear
  plus 70 % `easeInOut` over 9.7 s, so the camera moves on frame 0, height `easeInOut` over 9.0 s. In 16:9 it starts
  high, the toy world across the middle 60 % of the width under a horizon a quarter down, and ends low with the
  horizon mid-frame, the hero prop right of centre against the setting sun and the title top-left (in the demo: the
  island, then the lighthouse).
- Axes: the camera sits at target + (sin az, cos az) × radius, starting on +z; `polar(th, rho)` places props by angle
  from +x towards +z and fraction of the coast radius. The action and the props that face out go on the camera's side,
  the hero on the far side, towards the sunset at −x (in the demo: cove, pier and boat on +z, `TH_COVE`; cottages on
  the +z half facing out; the lighthouse on the −x headland, `TH_HEAD`).
- The sun (`sunAz`, `sunElev`) sinks from 26° to −4° behind the island; the light stops at 7°, so the lit band never
  vanishes and shadows stay finite, stretching across the sea from about 6 s (the dusk look). Shadows reach ±27 units.
- 9:16 (1080 × 1920, rendered at 0.3–9.4 s): field of view 60; in `camAt` radius 48 → 42, height 15 → 7, target x
  −0.5 → −6.4, y 11 at both ends, z 0.2 → 5.4 (azimuths unchanged); four more `CLOUDS` rows [−80, 30, 10],
  [−130, 33, 11], [−175, 30, 10], [−215, 34, 9], or the top fifth is bare sky; `iris()` centre `W / 2`, `H / 2`;
  title x0 72, first baseline 425 in both places (Technical notes; stroke tops at y 305, "HARBOUR" ends at x 750,
  subtitle at y 710). The tower top starts near y 770 over an island at about 1050–1600; on the end card the lantern
  sits near (750, 875), clear of the subtitle, with the sun whole behind it from 7.0 s.
- Every Signature item stays whole in that 9:16, with these compromises: a palm crops at the right edge until about 3
  s; from about 4 s the island's east end (a palm, rocks, the shore past the last cottage) runs off the right edge,
  about a third of its width by the end card, while the cottages, tower and boat stay whole; during the gust the
  boat's hull and wake sit at y 1450–1600, in review.md's caption band; the sun enters cropped at the left near 5.5 s,
  as in 16:9; the bottom 17 % stays sea, crescents, shadows.
- Stand-in (9:16, `TOWER_H` 13, 50 % taller): the end-card lantern rose to about y 735 (32 px per unit), clear of the
  title. Field of view, radii and target suit the island's 26-unit width, the end pan the tower: for a taller subject
  raise the end target y (about 40 px down per unit).
- 1:1 (1080 × 1080, rendered): field of view 46, the demo's radius and height, target x −1.5 → −6.8, y 5.2 → 8.0,
  z 0.5 → 6.6, the demo's clouds, `iris()` centre `W / 2`, `H / 2` and opening radius 825, title x0 72, first
  baseline 200 in both places: the lantern ends near (738, 378), right of "LIGHTS".

## Motion
- Easing: `easeInOut` (cubic) for camera, sun and closing iris; `easeOut` for the opening iris, subtitle and letter
  tilt; `backOut()` for letters; `sstep()` for grade, windows and stars. The sails fill on a damped spring,
  `sailFill()` (about 20 % overshoot, settled in 0.8 s); the lamp comes on through `lampOn()`'s eight-step flicker.
- Nothing is still: something always moves on the water, in the air and in the sky, and every living or loose thing
  has an idle motion, while ground, rock and buildings stay put (in the demo: the boat bobs and rolls, slack sails
  flutter until the gust, palms sway, more after it, gulls circle the lighthouse at 7.5–12.3 units, smoke puffs rise
  on a 3.5 s cycle, clouds drift and face the camera, foam breathes, the beam turns at 1.25 rad/s; after the gust the
  boat sails 13.5 units left in 8 s, heeled, `boatX()`).
- Never: stepping (everything is a smooth function of `t` at 30 fps; twos would read as `anime-80s`), cuts, camera
  shake, motion blur, smooth shading on objects, photographic textures or highlights.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.95 | ink iris opens from (960, 560) on the noon island | `iris()` |
| 0–9.7 | one glide: azimuth 16° → 72°, radius 46 → 41, height 13.5 → 6.8; gull calls at 2.55, 4.25, 5.85, 8.35 | `camAt`, `GULLS` |
| 0–9.3 | day, golden 3.8, sunset 6.6, dusk 9.3; the sun sinks behind the lighthouse | `KEYS`, `PAL`, `palAt()`, `sunAz`, `sunElev` |
| 1.0–2.9 | three looping wind streaks curl past the boat | `wind()`, `WIND` |
| 1.55–2.4 | sails fill and overshoot, boom swings out, the boat heels and sets off | `GUST`, `sailFill()`, `boatX()` |
| 6.55–7.5 | windows light one by one (1.0 for 0.12 s, then 0.85); keeper's at 6.8, pier lamp 7.5 | `WIN0`, `winMats`, `HOUSES` |
| 7.15–7.65 | lamp flickers on; two beams sweep, the halo flares facing the camera; stars 7.6–9.6 | `LAMP`, `lampOn()`, `beamMat`, `haloMat` |
| 7.75–8.95 | title letters pop, 13 × 0.05 s; subtitle 8.5–8.95 | `TITLE`, `title()` |
| 9.05–9.95 | iris closes on the lantern: a 125 px ring by 9.55, a wobble, shut at 9.95 | `IRIS_OUT`, `iris()`, `LANTERN` |

- One shot between two irises: the time of day carries the structure, each event gets a window in the glide. Reusable:
  iris in, a gust with streaks, lights at dusk, a lamp and beam, the title pop, an iris closing on a detail. KEYS for
  contact_sheet.sh: 1.6 (streak loop, sails filling), 5.3 (golden light, sun entering), 7.7 (lamp on, beam), 8.95
  (finished card), 9.45 (iris ring on the lantern).
- The demo's ending is too short to copy: its card is settled and whole only 8.87–9.10 s (0.27 s by pixel difference).
  At any length, the last settle (the card at `TITLE` + 1.2, the last light 0.12 s after it switches on, the beam at
  `LAMP` plus its ramp) plus 0.8 s must come by `IRIS_OUT` + 0.1, when the iris inks the first corner, and the iris
  must shut (0.9 s after `IRIS_OUT`) at least 0.1 s before `DUR`; a card costs about 2.9 s. The glide, grade, sun,
  stars, the beam's sweep and halo flare, boat, gulls, clouds, foam, smoke, palms and the letters' 0.025 rad wobble
  are ambient and may continue (the demo keeps them); the lamp flicker, beam ramp, window flashes, letter pop and
  tilt, subtitle fade and iris must have stopped. Measure against the same t with those forced to their end state,
  ignoring differences under 16 levels (the subtitle's last 1 %); with exact comparison every tested hold is 0.80–0.83
  s, so the rule has no slack: keep `TITLE`, `LAMP` and `IRIS_OUT` on 0.1 s steps, since off the 30 fps grid its
  equality case gives 0.77 s (tested).
- Tested 10 s timing (16:9 and 9:16): `WIN0` 6.2, keeper's windows 6.45, `LAMP` 6.8, `TITLE` 7.1, `IRIS_OUT` 9.0, the
  rest as the demo: settled 8.3 s, whole to 9.07 s, shut at 9.9 s. Its audio.py follows the spacing every plan keeps:
  strums 30 % softer after `WIN0` + 0.05 (6.25), the pad from `WIN0` − 0.15 to `DUR` (6.05 s for 3.95 s; shorter plans
  shorten its attack and release), strums and each bar's second bass note (at `b0` + 2 × `B`, which the strum cut-off
  misses) dropped after `IRIS_OUT` + 0.15, the closing chord 0.13 s after `IRIS_OUT` (9.13–9.17), a 0.1 s fade-out
  (`fo`).

## Sound
audio.py reads `events.json` as a list of `{k, t, …}` cues and synthesizes everything with NumPy (seeded `rs`).
- `iris`: a reversed pop. `gust`: a 1.6 s swept whoosh and a canvas `snap()` 0.3 s later (sent 0.25 s before `GUST`).
  `gull`: an FM call panned by `pan` (−0.4 to 0.35 in the demo). `win`: a glockenspiel note climbing C6, D, E, G, A,
  C, D, E. `lamp`: a clunk, tinks and a warm pad. `letter`: a marimba note climbing the scale and a wooden pop. `sub`:
  a soft whoosh. `irisout`: a falling 900 → 220 Hz glide. `close`: a low pop 0.17 s after its time.
- No cue is looked up by name; any subset runs (tested: only `gust`). A cue without `t` or `k` raises KeyError; cues
  outside 0–`DUR` and unknown kinds drop silently; the letter index `letter` cues carry is ignored (`letters` counts).
  Pans break it (tested): the 15th `win` cue in a film (pan −0.3 plus 0.1 per cue, `win_n`), the 25th `letter` cue
  (−0.4 plus 0.06 per cue, never reset between cards) and any `gull` `pan` beyond ±1 give NaN, and audio.py still
  prints "ok" with a nan peak over a broken track: clamp the pan or reset the counter.
- Written at fixed times, not cued: the sea bed (noise with 3.3 s swells) over the whole `DUR`; an island strum:
  `bars` G 0.15, C 2.55, D 4.95, G 7.35 s at 100 bpm, each a `strum` pattern on `uke()` over two `marimba()` bass
  notes, the chord's lowest voiced note an octave down (G, G, A) on the bar and a fifth above it 1.2 s later; the
  14-note `mel` from 0.75 to 8.55 s; strums 30 % softer after 6.6 s and skipped after 9.2 s; a `pad()` from 6.4 s for
  3.8 s; a closing ukulele chord at 9.18–9.22 s. Music runs on the `wet` bus (1.8 s reverb).
- The mix fades out over the last 0.6 s (`fo`) through a tanh limiter, which buries `close` (about −30 dB at 9.94 s)
  and the tail of `irisout`: end the film 0.4 s after `close` + 0.17, or shorten the fade to 0.1 s (0.3 s still takes
  about 12 dB off `close`). New films: `iris`, `gust` for wind or a swoosh, `gull` for birds, one `win` per light,
  `lamp` for the big light, one `letter` per title letter, `sub`, `irisout`, `close`; re-time every fixed part above.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Toon material | `anim.html` → `toonMat` | `toonMat(hex, o)`: `o.rim` (0.2–1.2), `o.hatch`, `o.fog` (0–1), `o.emis`, `o.emisC`, `o.side`, `o.defines` (ISLAND, STRIPES, CLOUD) | as is |
| Solid prop with ink hull, crooked shapes | `anim.html` → `prop`, `deform()` | `prop(geo, mat, o)`: `o.hull` false for per-frame geometry, `o.thin` for 2.2 px, `o.cast` false to skip shadows; `deform(geo, fn)` moves each vertex | as is |
| Toon lighting, ink lines, passes | `COMMON_FS` → `toon()`, `shadowAt()`, `fogIt()`; `postMat`, `ndMat`, `renderGL()`, `hullMat`, `hullThin` | `uLineK` scales the screen lines, `uPx` the hulls | as is |
| Grade, sun, sky and sea | `PAL`, `KEYS`, `palAt()`, `sunAz`, `sunElev`, `setScene()`; `SKY_FS`, `WATER_FS`, `sky`, `water` | four keys per role; sea bands and foam follow `Hf` in `GLSL_H`; `uBoat` = wake x, z, length, strength | adapt the grade's times and colours; sky and sea as is |
| Island terrain | `Hf()`, `Rth()`, `GLSL_H`, `polar()`, `islandGeo` | `polar(th, rho)` returns [x, y, z] on the ground | adapt: edit `Hf`, `Rth` and `GLSL_H` together |
| Clouds, gulls, smoke | `CLOUDS`, `cloudMat`, `clouds`, `gulls`, `wingGeo()`, `puffs`, `CHIMNEY` | cloud rows [azimuth°, elevation°, size]; gulls circle 2.5 units off `LX`, `LZ` | as is; add cloud rows in 9:16, move the gulls' centre |
| Boat, sails, flag, wind streaks | `boat`, `setSail()`, `sailGeo()`, `setFlag()`, `sailFill()`, `boatX()`, `wind()`, `WIND` | `setSail(g, A, B, C, belly, flutter, t)`: corners tack, clew, head | adapt (any sail, banner or cloth) or replace |
| Lighthouse, beam, halo, lights | `LH`, `TOWER_H`, `LANTERN`, `beamMat`, `haloMat`, `lampOn()`, `winMats` | `userData.win` = a material's switch-on time | replace the tower; the lights, beam and halo suit any lamp |
| Cottages, palms, pier | `HOUSES`, `PALMS`, `frondGeo()` | `HOUSES` rows [th, rho, w, h, d, wall, roof, lean] | adapt |
| Iris in and out; title card | `anim.html` → `iris`, `title()` | iris opens from (960, 560), closes on projected `LANTERN`; title `TITLE_TXT`, `SUB_TXT`, x0 116, first baseline 236 (twice) | adapt: centre, radius, target; copy, position |
| Timeline and cues | `GUST`, `LAMP`, `WIN0`, `TITLE`, `IRIS_OUT`, `GULLS`, `window.events` | | replace |

## Adapting
- **Style vs demo plot:** the style is everything in Signature, plus the grade keyed in time, both irises and the
  sticker title. The harbour, the crossing, the lamp and "HARBOUR LIGHTS" are plot. The transformation can be the
  light (noon to dusk, lights coming on), a gust filling a sail or flag, an arrival or a departure.
- **New subject:** a toy world on ground of about 12 units radius at the origin, so camera, shadow frustum and fog
  fit: another island, a hill town, a farm, a product on a rock in the sea. A user's logo goes on the 2D overlay
  (`octx` after the 3D, from a data URI), never as a texture; model products from primitives.
- **Traps:** `Hf` exists twice, in JavaScript and in `GLSL_H`: change one only and the foam leaves the new coast. Both
  raise a 2.6-unit mound at `LX`, `LZ` for the lighthouse and `STRIPES` counts from the ground there: moving the tower
  leaves the mound. `SHORE_Z` comes from scanning `Hf` along +z and places the pier and `BOAT_Z`; with no shore on +z
  it stays 0, near the centre. `R` is one `mulberry32()` stream used at build time: a prop inserted early reshuffles
  every later rock, cottage and palm; seed new parts separately. The keeper's windows switch on at a literal 6.8
  written twice (the window loop and the `mats.filter` after `HOUSES`). `CHIMNEY` is cottage 1's, the gulls circle the
  lighthouse, the closing iris targets `LANTERN`, `wind()` follows `boatX()`: move or remove them with their props;
  props beyond ±27 units get no shadows.
- **Length:** scale every literal time: `KEYS`; 8.2 in `sunAz`; 9.2 (twice) in `sunElev`; in `camAt` 9.7 (twice: the
  azimuth, radius and target blend) and 9.0 (height); the 7.6–9.6 star fade in `setScene()`; the 8 s crossing in
  `boatX()`; the timeline constants and the keeper's 6.8. Scaling alone breaks the settle rule below about 15 s (the
  card needs 7.75k + 1.9 ≤ 9.05k, so k ≥ 1.46): pull `WIN0`, `LAMP` and `TITLE` earlier as in the tested 10 s timing.
  Keep the camera on the +z/+x side (cottages face outwards there, the sun sets towards −x). Add an event every 1.5 to
  3 s; past about 20 s chain scenes with iris pairs, the style's only transition. `DUR` in anim.html is unused. In
  audio.py set `DUR`, add `bars` every 2.4 s cycling G, C, D, G, extend `mel`, and move the pad, closing chord, 9.2
  cut-off and 6.6 softening.
- **Shorter:** from 10 s down to about 6 s keep every beat and cut the 5 s sunset drift between gust and windows.
  Minimums: iris 0.6 s; streaks 1.9 s from `GUST` − 0.55; about 0.7 s between `KEYS`; windows 0.8 s; lamp 0.5 s and
  its beam 1.5 s (the 1.5 in `sstep(LAMP, LAMP + 1.5, t)` in `setScene()`; under about 6 s make it 0.5). Apply the
  settle rule and audio spacing in Film grammar.
  - Tested 7 s plan (stills in 16:9 and 9:16, audio.py): `GUST` 1.3, `GULLS` 2.2, 3.5, 5.0, `KEYS` 0, 2.3, 3.9, 5.9,
    `WIN0` 3.2, keeper's windows 3.45, `LAMP` 3.7, `TITLE` 4.1, `IRIS_OUT` 6.0; 5.6 in `sunAz`, 6.3 in `sunElev`, 6.6
    (twice) and 6.1 in `camAt`, stars 4.6–6.6, crossing over 5.4 s. The card settles at 5.3 s (the beam at 5.2 s), the
    frame is whole to 6.1 s (the card to 6.2 s), the iris shuts at 6.9 s; 9:16 framing holds. audio.py by the Film
    grammar spacing: `DUR` 7, `bars` G 0.15, C 2.55, G 4.95, the first seven `mel` notes plus 4.95 (74) and 5.55 (79),
    the pad from 3.05 s for 3.95 s (attack 1.0, release 1.4).
  - Under about 6 s cut whole beats: the title card first (`TITLE` past the end), then the gull calls; keep the gust,
    the grade to dusk, lights and lamp. The opening iris can take 0.6 s (both 0.95 values in `iris()`).
  - Tested 4 s plan (stills in 16:9 and 9:16, audio.py): iris 0–0.6 s; `GUST` 0.7 (streaks 0.15–2.05); `GULLS` 1.2;
    `KEYS` 0, 0.9, 1.6, 2.3; 2.8 in `sunAz`, 3.1 in `sunElev`, 3.3 (twice) and 3.0 in `camAt`, crossing over 2.8 s;
    `WIN0` 1.3, keeper's windows 1.55, `LAMP` 1.75 with a 0.5 s beam ramp, stars 1.8–3.0; `TITLE` 99; `IRIS_OUT` 3.0.
    Against a fully settled frame (pixel difference) the lit harbour is whole and settled 2.23–3.1 s (0.87 s); the
    ring sits on the lamp at 3.5 s, black from 3.9 s. The camera still turns through the hold, faster than at the
    demo's end (ending `camAt` sooner stops it with a jerk); the streak tails overlap the first windows. audio.py by
    the same spacing: `DUR` 4, `bars` G 0.15 and D 2.55 (whose second bass note, at 3.75 s, drops), the first three
    `mel` notes plus 2.25 (74), 2.55 (78), 2.85 (79), the pad from 1.15 s for 2.85 s (attack 0.5, release 0.9).
- **Other formats:** Composition's 9:16 and 1:1 values, rendered through the closing iris; pixels in Technical notes.

## Boundaries
- **Distinct from:** `low-poly` (flat-shaded facets, no outlines, soft shadows), `inflated-3d` (smooth glossy balloon
  shapes), `feature-animation-3d` (smooth PBR characters, studio light), `voxel` (cubes), `isometric` (flat 2D vector
  world), `anime-80s` (2D cels over painted backgrounds), `saturday-cartoon` (2D TV animation).
- **Poor fit:** charts and numbers (`data-visualization`, `infographic`), how a machine works inside
  (`technical-cutaway`), character acting (`clay`, `feature-animation-3d`), text-led clips (`kinetic-typography`).
- **Do not:** copy Nintendo, Zelda or other game characters, islands, logos or UI; the look is generic toon shading.
  No black or grey shadows, Phong highlights or image textures, never drop the ink, and keep props chunky and crooked:
  precise CAD shapes read as another style.

## Technical notes
- `render.json` sets `"gpu": "full"` and `"schedule": "contiguous"`, a leftover: frames are pure functions of `t` (GPU
  rounding can differ: compare by PSNR, review.md). Metal on Apple silicon: 60 frames in 2.8 s on one page; without a
  GPU it is far slower, so draft with a smaller `SHADOW_N` and fewer MSAA samples on `colorRT`.
- `vendor/three.min.js` is r159, the last with the global build a plain script tag loads. `THREE.ColorManagement` is
  off and output linear, so hexes reach the screen as written (three.js's lit materials would neither band nor follow
  the grade); `inverse()` in the shaders needs WebGL2.
- Sizes hard-coded outside `W`/`H`: the canvas attributes; in `iris()` the opening centre (960, 560) and radius 1180,
  1.06 times the farthest (top) corner's 1111 px, so the corners clear at about 0.58 s (larger finishes early, smaller
  leaves corners inked; 9:16 keeps 1180, 1:1 takes about 810–825); in `title()` x0 116, the first baseline 236 written
  twice (the title's `y0` and the subtitle's `sy`: change both; `sy` assumes two title lines: put it at the last
  line's baseline + 80 for one or three words, or a third line prints under the subtitle, rendered), +146 per line,
  the 34 px indent, the subtitle at +80 and +54, 156 and 46 px fonts, 17 and 10 px strokes; 7 px streaks in `wind()`;
  the vignette's 1.25 aspect factor in `postMat` (fine in 9:16).

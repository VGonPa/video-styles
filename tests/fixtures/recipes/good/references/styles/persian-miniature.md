# Persian Miniature (`persian-miniature`)

A Safavid-era garden miniature: opaque mineral pigments on a burnished gold sky, a ground plane tilted up to a
high horizon, cypresses and blossoming almonds, a tiled pavilion, all framed by a gilded lapis border on
paper sprinkled with gold. Calm, courtly and contemplative; the film paints the page in, then lets the garden
come alive.

**Reference film:** "The Garden of Patience", a gardener with a blue ewer walks through a garden that
blossoms as he passes, closing on the caption "He who waits in the garden is never late for spring." ·
`styles/persian-miniature/`

## Signature
- Warm buff margin paper with gold flecks, and a gold-and-lapis ruling (jadval) traced from the top centre
  around both sides in the first second (`drawRulings(t)`).
- The lapis border band sweeps in as a two-way wedge from the top centre (`drawBand(t)`).
- From 1.15 s the painting appears layer by layer as brush dabs: gold sky first, then the green ground,
  court, pavilion, trees and plants (`drawRevealed(L, t)`).
- No outlines of uniform weight and no shading toward a light source: flat jewel colours with thin dark
  contours.

## Palette
| Role | Colour | In code |
|---|---|---|
| ink contours | `#2b1a12` | `COL.ink` in `js/lib.js` |
| lapis (border, carpets) | `#1f3d98` | `COL.lapis` |
| deep lapis | `#13286a` | `COL.lapisD` |
| vermilion (robe, curtains) | `#d9442b` | `COL.verm` |
| emerald | `#2f8a57` | `COL.emer` |
| cypress | `#1d4f38` | `COL.cyp` |
| ground green | `#6aa55c` | `COL.ground` |
| turquoise tiles | `#35a9a4` | `COL.turq` |
| ivory (pavilion, cartouche) | `#f5ecd6` | `COL.ivory` |
| margin paper | `#efe2c2` | `COL.paper` |
| water | `#9cc0dc` | `COL.water` |
| gold leaf, light to dark | `#fff3b6`, `#f2cf66`, `#d19f34`, `#8f6317`, `#5c3d0c` | `COL.g0` … `COL.g4` |
| gold sky gradient | `#d9a53a`, `#eec65e`, `#d49c34` | `paintSky(g)` |
| skin | `#f2d6b6` | `SKIN` in `js/figure.js` |
| page surround | `#1a0f08` | `drawFrame(t)` |
| fade to and from dark | `rgba(20,12,6,${clamp(fade)})` | `drawFrame(t)` |

- Colours are opaque and flat, like gouache over gesso; the only gradients are the gold (`goldFill(g, x, y, w, h)`
  stripes five gold stops diagonally) and the gentle ground gradient from `COL.groundL` to `COL.groundD`.
- Every object has a darker partner colour for its contour or crease (`verm`/`vermD`, `emer`/`emerD`).

## Typography and copy
- One family, Amiri, in three files: `fonts/Amiri-700-normal-latin.woff2` for the title,
  `fonts/Amiri-400-italic-latin.woff2` for the caption, `fonts/Amiri-400-normal-latin.woff2` spare.
- The title uses `FTITLE` (`700 46px Amiri`) in `COL.lapisD`; the caption uses `FCAP`
  (`italic 400 31px Amiri`) in `COL.ink`. Both sit in an ivory cartouche with gold ends (`cartouche(cx, cy, w, h, u)`).
- Text writes on from left to right behind a soft 60 px gradient edge (`writeText(txt, font, cx, y, u, color)`),
  like ink flowing from a pen; it never slides or pops.
- Copy is a title of three to five words and one proverb-like caption sentence. The 560 px title
  cartouche holds about 26 characters at 46 px; the 820 px caption cartouche holds about 55 at 31 px.
  Longer text needs a wider cartouche or a second caption beat, not a smaller size.
- The files are Latin subsets: no Persian or Arabic script. Never fake Persian calligraphy with Latin
  letters or invented glyphs; write in the user's language.

## Texture and finish
- Margin paper: `bakePaper()` paints warm blotches, 1600 paper fibres, 900 gold flecks (`flake()`) kept
  outside the border, and an edge darkening; it is baked once into `PAPER`.
- Grain: `bakeGrain()` fills a full-frame canvas with warm noise once; `drawFrame(t)` multiplies it over
  everything at the end, so paint sits in the paper.
- The gold sky is burnished in `paintSky(g)`: soft sheens, faint leaf seams and 2200 punched dots.
- Gold glints: `glint(x, y, s, a)` draws an additive radial flare and a cross, riding the gilding fronts
  and twinkling on the larger flecks (`FLECKS`) at the end.

## Shapes, line and figures
- Contours are thin (1–2 px) and dark, never black: `COL.ink`, `COL.inkS` or a darker partner colour.
- Nature is stylised and repeated: cypresses as tapered flames with rows of tiny arcs (`cypress(g, x, base, h, w, seed)`),
  almonds as recursive branches that register blossom sites (`almond(g, x, base, seed, grp, h, bloom0)`),
  plane trees with five-lobed leaves (`chinar(g, x, base, seed)`), tulips, irises and narcissi (`plant(g, x, y, kind, r)`).
- Architecture is flat and frontal with surface pattern everywhere: `hexTiles()`, `starLattice()`,
  `archPath()` for the iwan arch, `arabesque()` in the gold spandrels.
- The figure is slender and elegant: a three-quarter face, almond eye, white turban with an aigrette,
  knee-length qaba with gold dots, sash, pointed shoes (`drawFigure(g, x, y, ph, amp, t, look)`). Head,
  neck, torso, jointed limbs and hands are all drawn.
- A new object is flat, frontally drawn, patterned, contoured in its darker partner colour, and made from
  `COL` only.

## Composition and camera
- The painting fills the rectangle `P` (1620 × 892 at 150, 94) inside the border band (`BO` outer, `BI`
  inner); the paper margin shows around it.
- Space is stacked, not receding: sky in the top band, the ground tilted up to a horizon near y = 300
  (`HZ(x)`), and the action on a walk near the bottom (`PATH`). Nothing shrinks with distance.
- Elements break the frame on purpose: the left cypress rises into the border, as in the manuscripts.
- Camera: one slow push-in of 2.8 % over the whole film about (960, 560) in `drawFrame(t)`; no pans or cuts.
- 9:16 suits the tradition (miniatures are usually portrait): make `P`, `BO` and `BI` tall, stack more
  registers (sky, pavilion, garden, walk), keep the margins. 1:1 drops the side buildings.

## Motion
- Easing from `js/lib.js`: `eOut` and `eInOut` for reveals and gilding, `eSine` for the push-in, `eBack`
  (overshoot 2.2) only for blossoms opening and the fountain jet.
- The gardener walks with a trapezoidal speed profile (`walkU(t)`) and a stride phase driven by distance
  (`FIG.cyc`), so feet never slide; `legPose(ph, amp, rest)` bends knees and lifts toes.
- Secondary life is gentle and cyclic: water highlights flowing in the channels, ripples from the jet,
  doves crossing the gold sky (`BIRDS`), a hoopoe pecking (`drawHoopoe(t)`), petals drifting (`PETALS`).
- Painting-in is directional: each layer's dabs run `'down'`, `'up'`, `'right'`, `'left'` or `'out'`
  with some scatter (`dabs(bb, t0, t1, dir, seed)`).
- Never fast or bouncy: no camera shake, no squash, nothing faster than the walk.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.5 | fade up from dark | `TL.fadeIn` |
| 0.25–1.15 | rulings traced around the page | `TL.rule`, `drawRulings(t)` |
| 0.5–1.45 | lapis border sweeps in | `TL.band`, `drawBand(t)`, `BAND_O` |
| 1.15–3.1 | painting appears layer by layer | `bakeLayers()`, `drawRevealed(L, t)` |
| 2.45 | fountain jet rises | `TL.jet`, `drawWater(t)` |
| 2.55–2.95 | gardener fades in | `TL.appear` |
| 2.85–3.75 | title cartouche and title | `TL.title`, `cartouche()`, `writeText()` |
| 2.95–7.45 | the walk; doves cross | `TL.walk`, `figState(t)`, `BIRDS` |
| 7.15–8.15 | almonds and roses blossom | `TL.bloom2`, `TL.bloom1`, `TL.roses` |
| 7.45–8.1 | gardener looks up | `TL.look` |
| 7.7–8.95 | border gilds with travelling glints | `TL.gild`, `BAND_G`, `glint()` |
| 7.8–8.55 | caption | `TL.caption` |
| 8.8–9.6 | gold flecks twinkle | `TL.twinkle`, `FLECKS` |
| 9.35–10 | fade to dark | `TL.fadeOut` |

- The film is "the page is made, then it lives": build the frame (rulings, border), paint the picture,
  then one long held action with the living garden around it, then a gilded close.
- Reusable patterns: rulings, border sweep, layered paint-in, title cartouche, caption cartouche, gilding.
  The gardener's walk and the blossoming are demo content.

## Sound
- audio.py synthesizes every sound: a santur (struck string pairs, `santur(f, d, bright)`), a tar plucked by
  Karplus–Strong (`tar(f, d)`), a breathy ney (`ney(f, d, vib)`), paper and brush rustles (`rustle(d, lo, hi)`),
  a pen scratch (`pen(d)`), gold shimmer (`shimmer(d, base)`), dove chirps (`chirp()`), slipper taps
  (`tap(bright)`) and bells (`bell(f, d)`). Melodies use the Shur mode on D in `SHUR`, with quarter-flat
  steps (63.5, 75.5).
- Cues read: `rule`; `band` (`d`); `paint` (`d`), one per layer; `jet` (starts the fountain bed and must be
  present); `title`; `step` (`a` for amplitude, `stone` for the brick terrace); `chirp` (`pan`);
  `pop` (`pan`, every fourth plays a santur note); `caption`; `gild` (`d`); `twinkle`; `end`.
- Not cue-driven: the opening santur arpeggio at 0.15 s and the ney phrase from 3.1 to 8.5 s are placed at
  fixed times. Move them when the timeline changes.
- The room tone and fountain bed run under everything; the mix ends with `np.tanh(st * 3.5) * 0.85`.
- A new scene should emit `paint` for each painted layer, `step` for each footfall and `pop` for small
  reveals.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| pigments | `js/lib.js` → `COL` | `COL.lapis`, `COL.g0`–`COL.g4` | as is |
| easing, seeded random | `js/lib.js` → `eOut`, `eBack` | `mulberry(seed)`, `hash(n)` | as is |
| margin paper | `js/lib.js` → `bakePaper()` | sets `PAPER`, `FLECKS` | as is |
| grain | `js/lib.js` → `bakeGrain()` | sets `GRAIN`, multiplied last | as is |
| gold leaf | `js/lib.js` → `goldFill()` | `goldFill(g, x, y, w, h)` returns a gradient | as is |
| blossom and rose stamps | `js/lib.js` → `bakeSprites()` | `SPR.bW`, `SPR.roseR` | as is |
| layer with paint-in | `js/paint.js` → `layer()` | `layer(name, bb, t0, t1, dir, fn, clip = clipP)` | as is |
| paint-in draw | `js/scene.js` → `drawRevealed()` | `drawRevealed(L, t)` | as is |
| trees and plants | `js/paint.js` → `cypress()` | `almond()`, `chinar()`, `pomegranate()`, `plant()` | as is |
| tiles and arches | `js/paint.js` → `hexTiles()` | `hexTiles(g, x, y, w, h, s, c1, c2, line)`, `starLattice()`, `archPath()` | as is |
| border band | `js/paint.js` → `bakeBand()` | `BAND_O`, `BAND_G`, drawn by `drawBand(t)` | as is |
| rulings | `js/scene.js` → `drawRulings()` | `rulePath(g, R, u)` | as is |
| cartouche and text | `js/scene.js` → `cartouche()` | `cartouche(cx, cy, w, h, u)`, `writeText(txt, font, cx, y, u, color)` | as is |
| gardener | `js/figure.js` → `drawFigure()` | `drawFigure(g, x, y, ph, amp, t, look)` | adapt: robe colours, held object |
| walk | `js/scene.js` → `figState()` | `walkU(t)`, `WALK`, `groundAt` | adapt: new path |
| garden scene | `js/paint.js` → `paintSky()`, `paintGround()`, `paintCourt()`, `paintPavilion()`, `paintTrees()` | | adapt: new places |
| timeline and copy | `js/scene.js` → `TL`, `TITLE`, `CAPTION` | | replace |
| cues | `js/scene.js` → `window.events` | | replace |
| instruments | `audio.py` → `santur()` | `tar()`, `ney()`, `shimmer()` | as is |

## Adapting
- **New subject:** keep the page (paper, rulings, border, cartouches), the paint-in and the gilded close;
  replace the garden with the new place built from the same pieces, and give the figure a new action.
- **Length:** the frame build and the gilding are fixed costs (3 s and 2 s); stretch the middle with a
  second held action or a second painted register revealed in place. More than one paint-in per film
  starts to drag.
- **Other formats:** see Composition; the stacked registers recompose well in 9:16, the wide pavilion does
  not fit 1:1 without moving it.

## Boundaries
- **Distinct from:** `illuminated-manuscript` (European vellum, blackletter, marginalia), `islamic-geometric`
  (pure pattern, no figures or landscape), `madhubani` (Indian folk line work).
- **Poor fit:** fast product teasers or data; use `swiss-style` or `infographic`.
- **Do not:** add religious figures or Qur'anic text as decoration, or invent pseudo-Persian script.

## Technical notes
- Canvas 2D only, no `render.json`. Five script files: `anim.html` loads `js/lib.js`, `js/paint.js`,
  `js/figure.js`, `js/scene.js` in that order; scene.js defines `window.ready`, `window.draw` and
  `window.events`.
- `window.ready` bakes six full-frame layers plus paper, grain and two band states, so it takes several
  seconds per worker; frames are then cheap once the static painting is complete (`STATIC`).
- Every random number comes from `mulberry(seed)`; the dabs and blossom sites are fixed at bake time.
- Hard-coded geometry: `P`, `BO`, `BI`, `PATH`, `POOL`, `CHAN`, `PAV` and `HZ(x)` in 1920 × 1080 pixels; the
  wedge and `bandPoint()` centre on 960, 540; cartouches sit at 960, 158 and 960, 952.

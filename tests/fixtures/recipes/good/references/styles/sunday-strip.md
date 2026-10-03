# Sunday Watercolor Strip (`sunday-strip`)

A multi-tier Sunday newspaper strip painted in brush ink and transparent watercolour washes on cold-press
paper. It evokes the golden-age Sunday funnies: a kitchen-table domestic gag whose middle tier blooms into a
fantasy. Warm, nostalgic, gently comic.

**Reference film:** a girl told to eat her broccoli imagines herself a Tyrannosaurus in a broccoli forest · `styles/sunday-strip/`

## Signature
- A whole newspaper page with masthead ("The Sunday Almanac · Funnies") seen on a wooden table, then the camera zooms into tier 1.
- Panels painted in: an irregular wet edge soaks each panel in from a point (`soakClip()`), ink outlines then wash.
- Tapered brush-ink lines with breaks (`inkShape()`), never uniform vector strokes.
- Speech balloons pop in with `backOut` overshoot.

## Palette
| Role | Colour | In code |
|---|---|---|
| paper | `#f5eddb` | `PAPER` |
| ink | `#1e1a17` | `INK` in `js/ink.js` |
| kitchen wall | `#f1dfa6` | `WALL` |
| wallpaper stripe | `rgba(214,170,90,0.28)` | `kitchenWall()` |
| table wood | `#6b4a31` | `buildPage()` → `WOODC` |
| broccoli | `#5f9a3f` | `BROC` in `js/characters.js` |
| rex green | `#6f9447` | `REX` in `js/fantasy.js` |
| title red | `#b8472f` | `buildPanels()` |
| vignette | `rgba(0,0,0,0.45)` | `rgrad(...)` in `buildPage()` |

- Colour is laid as transparent washes with granulation and a darker dried edge (`wash(pts, col, { gran, edge })`), then glazed with gradients in `multiply`.
- Shadows are a second wash, not a darker fill.

## Typography and copy
- `'Caveat Brush'` for the title and balloon lettering, `'Patrick Hand'` for captions, `'IM Fell English SC'` for the masthead and byline (files in `fonts/`).
- Balloon copy: short, kid's voice, 3–7 words per balloon, at most about 18 characters per line at 34 px.
- Latin glyphs only (`-latin.woff2` subsets): no accents beyond Latin-1.

## Texture and finish
- Paper grain: `PAPER_T` pattern built once in `buildInkTextures()`, multiplied over every panel with `paperGrain(w, h)`.
- Panels are baked once to offscreen canvases (`bake(w, h, fn)` with `useCtx`) in `window.ready`; per frame only the characters and camera move.
- Wood table with a radial vignette (`WOODC`).

## Shapes, line and figures
- Line weight 3–6 px at panel scale, tapered at both ends (`ta`, `tb`), drawn by `brush(pts, w, o)` over Catmull-Rom points from `cr()`.
- Objects are built from `part(pts, col, lw)`: a wash fill plus a broken ink outline. A new object is a few polygons through `part()`.
- Figures: big heads, simple bodies (`girlSide()`, `girlClose()`), round eyes, rosy cheeks (`BLUSH`).

## Composition and camera
- The page is 1892 × 2396 page units laid out in three tiers (`TIER`, `PAN`); the camera (`camAt(t)`, `toScr()`) moves between `CAM.full` and tier close-ups.
- 9:16: the page is already portrait, so show it whole and push in panel by panel.

## Motion
- Easing: `eInOut` for camera moves, `eOut` for entrances, `backOut` overshoot on balloons. Never `ease-out` CSS-style linear slides.
- Character acting on twos: `stp(t)` quantises time to `STEP = 12` (12 fps) while the camera moves at 30 fps.
- The snap back from fantasy is a hard cut with a short jolt.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–1.25 | page on the table, zoom into tier 1 | `T.zoomIn`, `camAt(t)` |
| 0.45–1.0 | title panel soaks in | `T.title`, `soakClip()` |
| 1.5 | first balloon pops | `T.bal1`, `balloon(cx, cy, lines, tail, pop)` |
| 3.05–3.65 | glide down to tier 2 | `T.pan2` |
| 5.5 | roar | `T.roar`, `{ k: 'roar' }` |
| 6.3 | snap back to the kitchen | `T.snap` |
| 9.7–10 | fade | `T.fade` |

- A scene opens by soaking in, holds while a balloon pops, then the camera glides to the next tier.

## Sound
- audio.py synthesizes paper rustle, brush swish, glockenspiel, balloon pops, a roar, a snap and piano chords.
- Cues: `rustle` (d), `wash` (d), `pop`, `glide` (d), `jungle` (d), `swell` (d), `roar`, `snap`, `blink`, `chord`.
- A new panel should emit `wash` when it soaks in and `pop` for each balloon.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| brush stroke | `js/ink.js` → `brush()` | `brush(pts, w = 4, { ta, tb, seed, col, a })` | as is |
| watercolour wash | `js/ink.js` → `wash()` | `wash(pts, col, { raw, gran, edge, off, a })` | as is |
| painted part | `js/characters.js` → `part()` | `part(pts, col, lw, { seed })` | as is |
| balloons | `js/ink.js` → `balloon()` | `balloon(cx, cy, lines, tail, pop)` | as is |
| page and panels | `anim.html` → `buildPage()`, `buildPanels()`, `PAN` | | adapt: new panel art |
| fantasy tier | `js/fantasy.js` → `fantasyScene(t)` | | replace |
| timeline | `anim.html` → `T`, `CAM` | | replace |
| sound | `audio.py` | cue kinds above | as is |

## Adapting
- **New subject:** keep the page, the tiers and the soak-in reveal; repaint the panels with `part()` and the brush.
- **Length:** add tiers (a longer page) rather than more panels per tier.
- **Other formats:** 9:16 shows the page whole; 1:1 crops to two tiers.

## Boundaries
- **Distinct from:** `comic-strip` (flat digital colour), `golden-age-comic` (halftone and four-colour print).
- **Poor fit:** data-heavy explainers; use `infographic`.
- **Do not:** copy any real strip's characters or lettering.

## Technical notes
- Canvas 2D only, no `render.json`; renders 10 s in about two minutes.
- Never `Math.random()` or `performance.now()`: use `rng(seed)` and `hash(x)`.
- Hard-coded sizes: the page is 1920 wide (`bake(1920, 2400, …)`), `toScr()` centres on 960 × 540.
